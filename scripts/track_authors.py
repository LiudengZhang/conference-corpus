#!/usr/bin/env python3
"""Track the conference speaker watchlist through OpenAlex.

data/sources.yml has carried three author-tracking sources at status
`partial` or `none` since it was written. This runs the first of them.

What it is for. Scanning 33 journals costs about 22,000 records a year.
Following 65 named people costs a few hundred. If the people who are
invited to keynote are the people whose work later fills those journals,
the cheap route is a usable early-warning system and the expensive route
is mostly confirmation.

What it cannot do, and this is not a limitation to be engineered around.
The watchlist is a list of people selected by program committees, and
program committees select for results that worked. Nobody is invited to
give a plenary on the compound that did nothing. So this route is
structurally blind to exactly the evidence class that the corpus weights
most heavily — 225 of its 377 cards are refutations. Author tracking can
tell you what is arriving. It cannot tell you what is failing, and a
briefing built only from it would read as unbroken progress no matter
what the field actually did.

Resolution is by name search, narrowed by the affiliation string in
speakers.yml. That affiliation is itself unreliable — sources.yml records
it as wrong on 3 of 22 spot-checked records — so every author lands in
one of three confidence buckets and the bucket is written to the output
rather than being smoothed away.

Usage:
    python3 scripts/track_authors.py --since 2024-01-01
"""

from __future__ import annotations

import argparse
import collections
import json
import pathlib
import re
import sqlite3
import sys
import time
import urllib.parse
import urllib.request

import yaml

ROOT = pathlib.Path(__file__).resolve().parent.parent
SPEAKERS = ROOT / "data" / "speakers.yml"
INDEX = ROOT / "data" / "index.sqlite"
OUT = ROOT / "data" / "authors.yml"

MAILTO = "liudengzhang91@gmail.com"
API = "https://api.openalex.org"

# Affiliation strings in speakers.yml are informal ("Harvard Medical
# School/Brigham"); OpenAlex returns formal institution names. Compare on
# tokens, ignoring the words that appear in half of all institutions.
STOP = {"university", "of", "the", "school", "medical", "center", "centre",
        "institute", "college", "hospital", "and", "for", "research",
        "national", "health", "sciences", "science", "department"}


def get(url: str, tries: int = 4):
    req = urllib.request.Request(url, headers={
        "User-Agent": f"conference-corpus/1.0 (mailto:{MAILTO})"})
    for i in range(tries):
        try:
            return json.load(urllib.request.urlopen(req, timeout=60))
        except Exception:
            time.sleep(1.5 * (i + 1))
    return None


def tokens(text: str) -> set[str]:
    return {t for t in "".join(
        c.lower() if c.isalnum() else " " for c in text or "").split()
        if t not in STOP and len(t) > 2}


SMALL = {"of", "and", "the", "for", "at", "in"}


def initials(institution: str) -> str:
    """NHGRI from 'National Human Genome Research Institute'."""
    return "".join(w[0] for w in institution.split()
                   if w and w.lower() not in SMALL).upper()


def affiliation_matches(affiliation: str, institution: str) -> bool:
    """Speakers.yml writes 'NHGRI' or 'Harvard Medical School/Brigham';
    OpenAlex writes the formal name. Try tokens, then acronyms — the
    acronym rule is what rescues the institutes, which are exactly the
    ones whose informal name shares no word with their formal one."""
    if not affiliation or not institution:
        return False
    for part in re.split(r"[/,;]|\band\b", affiliation):
        part = part.strip()
        if not part:
            continue
        if tokens(part) & tokens(institution):
            return True
        squashed = re.sub(r"[^A-Za-z]", "", part).upper()
        if 2 <= len(squashed) <= 7 and part.upper() == part and squashed == initials(institution):
            return True
    return False


def resolve(name: str, affiliation: str):
    """Return (openalex_id, matched_institution, confidence)."""
    page = get(f"{API}/authors?search={urllib.parse.quote(name)}"
               f"&per-page=25&mailto={MAILTO}")
    time.sleep(0.25)
    if page is None:
        # The request failed, which is NOT the same as the person not being
        # findable, and collapsing the two is how a rate-limited run reads
        # as a watchlist of people who do not exist. Running this script
        # twice at once is enough to produce that.
        return None, None, "lookup-failed"
    results = page.get("results") or []
    if not results:
        return None, None, "no-such-author"
    if not affiliation:
        # Nothing to verify against. Refusing here costs a few speakers and
        # keeps homonyms out; speakers.yml has no affiliation for some.
        return None, "", "no-affiliation-on-file"

    def institutions(cand) -> list[str]:
        """Every institution OpenAlex associates with this person.

        `last_known_institutions[].name` is None on every record — the
        field is `display_name`, and the first version of this script read
        the wrong key, so the affiliation matcher had nothing to compare
        against and returned zero matches for all 65 speakers while
        looking like it was working. The richer source is `affiliations`,
        which lists every institution rather than only the latest, and a
        watchlist built from conference programs is full of people whose
        listed affiliation is one they have since left.
        """
        out = [(i or {}).get("display_name") or ""
               for i in (cand.get("last_known_institutions") or [])]
        out += [((a or {}).get("institution") or {}).get("display_name") or ""
                for a in (cand.get("affiliations") or [])]
        return [i for i in out if i]

    for cand in results:
        for inst in institutions(cand):
            if affiliation_matches(affiliation, inst):
                return cand["id"].rsplit("/", 1)[-1], inst, "affiliation-matched"

    # No institutional evidence. Do NOT guess. An earlier version fell
    # back to the candidate with the most works, on the theory that
    # program committees invite senior people; for "Xin Jin" that picked
    # someone with 10,180 papers, and every work it then pulled was the
    # wrong person's. A watchlist silently populated with homonyms is
    # worse than a short one, because nothing downstream can tell.
    best = results[0]
    first = institutions(best)
    return None, (first[0] if first else ""), "no-affiliation-match"


def works(author_id: str, since: str):
    out, cursor = [], "*"
    while True:
        page = get(f"{API}/works?filter=author.id:{author_id},"
                   f"from_publication_date:{since}"
                   f"&per-page=200&cursor={cursor}&mailto={MAILTO}"
                   f"&select=id,doi,title,publication_date,ids,primary_location,type")
        time.sleep(0.12)
        if not page:
            return out
        results = page.get("results") or []
        out.extend(results)
        cursor = (page.get("meta") or {}).get("next_cursor")
        if not cursor or not results:
            return out


EPMC = "https://www.ebi.ac.uk/europepmc/webservices/rest/search"


def epmc_works(name: str, since: str, until: str = "2026-12-31"):
    """Every Europe PMC record for a named author in a date range.

    sources.yml lists Europe PMC as the fallback for when the OpenAlex
    author id is ambiguous or missing. It became the primary route on
    2026-08-26 for a blunter reason: OpenAlex now meters by daily spend,
    not by request rate, and a single pass over 65 people with works
    pagination exhausts the free budget until midnight UTC. Backoff does
    not help with a quota.

    Affiliation is deliberately NOT in the query. Europe PMC matches AFF
    against the raw affiliation string, so acronyms behave erratically —
    `UCSF` returns 81 records for Marson but `MSKCC` returns 4 for
    Janjigian against 183 for "Memorial Sloan". Filtering on it would
    silently drop most of a person's output. The consequence is that the
    raw work counts here are upper bounds and include homonyms; the
    in-corpus counts are not, because a same-named stranger is very
    unlikely to publish in these particular 33 journals.
    """
    out, cursor = [], "*"
    query = (f'AUTH:"{name}" AND FIRST_PDATE:[{since} TO {until}]')
    while True:
        url = (f"{EPMC}?" + urllib.parse.urlencode({
            "query": query, "format": "json", "pageSize": 100,
            "cursorMark": cursor, "resultType": "lite"}))
        page = get(url)
        if page is None:
            return out, False
        results = (page.get("resultList") or {}).get("result") or []
        out.extend(results)
        nxt = page.get("nextCursorMark")
        if not results or not nxt or nxt == cursor or len(out) >= 1000:
            return out, True
        cursor = nxt
        time.sleep(0.15)


def run_epmc(speakers, corpus, since: str) -> list[dict]:
    records = []
    for i, sp in enumerate(speakers, 1):
        found, ok = epmc_works(sp["name"], since)
        pmids = {r.get("pmid") for r in found if r.get("pmid")}
        hit = pmids & corpus
        preprints = sum(1 for r in found if r.get("source") == "PPR")
        entry = {
            "name": sp["name"],
            "affiliation": sp.get("affiliation") or "",
            "meetings": [a["meeting"] for a in sp.get("appearances", [])],
            "route": "europepmc",
            "status": "ok" if ok else "lookup-failed",
            "works": len(found),
            "pmids": len(pmids),
            "in_corpus": len(hit),
            "preprints": preprints,
        }
        if len(found) >= 1000:
            # Hit the pagination cap, which for a watchlist of individuals
            # means the name is not identifying a person. "Xin Jin" returns
            # the cap. Both counts on this row are meaningless; the row is
            # kept so the total can be corrected rather than quietly wrong.
            entry["name_not_unique"] = True
        records.append(entry)
        print(f"[{i}/{len(speakers)}] {sp['name']:32} {entry['status']:14} "
              f"{len(found):5} works  {len(hit):3} in corpus", flush=True)
    return records


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--source", choices=["openalex", "europepmc"],
                    default="europepmc",
                    help="europepmc is the default: OpenAlex meters by daily "
                         "spend and one full pass exhausts the free budget")
    ap.add_argument("--since", default="2024-01-01")
    ap.add_argument("--limit", type=int, default=0, help="first N speakers only")
    args = ap.parse_args()

    speakers = yaml.safe_load(SPEAKERS.read_text())["speakers"]
    if args.limit:
        speakers = speakers[:args.limit]

    con = sqlite3.connect(INDEX)
    corpus = {p for p, in con.execute("SELECT pmid FROM papers")}

    records, confidence = [], collections.Counter()
    covered = missed = preprints = 0

    if args.source == "europepmc":
        records = run_epmc(speakers, corpus, args.since)
        covered = sum(r["in_corpus"] for r in records)
        missed = sum(r["pmids"] - r["in_corpus"] for r in records)
        preprints = sum(r["preprints"] for r in records)
        confidence = collections.Counter(r["status"] for r in records)
        write_out(records, args, confidence, covered, missed, preprints)
        return 0

    for i, sp in enumerate(speakers, 1):
        aid, inst, conf = resolve(sp["name"], sp.get("affiliation", ""))
        confidence[conf] += 1
        entry = {
            "name": sp["name"],
            "affiliation": sp.get("affiliation", ""),
            "meetings": [a["meeting"] for a in sp.get("appearances", [])],
            "openalex": aid,
            "openalex_institution": inst,
            "confidence": conf,
        }
        if aid:
            found = works(aid, args.since)
            pmids = {(w.get("ids") or {}).get("pmid", "").rsplit("/", 1)[-1]
                     for w in found}
            pmids.discard("")
            hit = pmids & corpus
            pre = sum(1 for w in found
                      if ((w.get("primary_location") or {}).get("source") or {})
                      .get("type") == "repository")
            entry.update(works=len(found), pmids=len(pmids),
                         in_corpus=len(hit), preprints=pre)
            covered += len(hit)
            missed += len(pmids) - len(hit)
            preprints += pre
        records.append(entry)
        print(f"[{i}/{len(speakers)}] {sp['name']:32} {conf:19} "
              f"{entry.get('works', 0):4} works  {entry.get('in_corpus', 0):3} in corpus",
              flush=True)

    write_out(records, args, confidence, covered, missed, preprints)
    return 0


def write_out(records, args, confidence, covered, missed, preprints) -> None:
    OUT.write_text(yaml.safe_dump({
        "meta": {
            "generated_by": "scripts/track_authors.py",
            "route": args.source,
            "since": args.since,
            "watchlist": str(SPEAKERS.relative_to(ROOT)),
            "blind_spot": (
                "Speakers are selected by program committees, which select for "
                "results that worked. Nobody is invited to give a plenary on the "
                "compound that did nothing. This route cannot surface "
                "refutations, and 225 of the corpus's 483 cards are refutations, "
                "so it must never be the only input to a briefing."),
            "count_caveat": (
                "`works` is an upper bound: Europe PMC is queried on author name "
                "without an affiliation filter, because filtering on affiliation "
                "drops most of a person's output when their institution is "
                "usually written as an acronym. `in_corpus` does not have this "
                "problem — a same-named stranger rarely publishes in these 33 "
                "journals."),
        },
        "authors": records,
    }, sort_keys=False, allow_unicode=True, width=88), encoding="utf-8")

    total = covered + missed
    print()
    print("resolution: " + ", ".join(f"{k} {v}" for k, v in confidence.most_common()))
    print(f"PubMed-indexed works by watchlist since {args.since}: {total:,}")
    print(f"  in the 33-journal index: {covered:,}"
          + (f" ({covered / total:.1%})" if total else ""))
    print(f"  outside it:              {missed:,}")
    print(f"preprints seen: {preprints:,}")
    print(f"wrote {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    sys.exit(main())
