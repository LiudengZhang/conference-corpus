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
    time.sleep(0.12)
    results = (page or {}).get("results") or []
    if not results:
        return None, None, "unresolved"

    def inst_of(cand):
        return ((cand.get("last_known_institutions") or [{}])[0] or {}).get("name", "")

    for cand in results:
        if affiliation_matches(affiliation, inst_of(cand)):
            return cand["id"].rsplit("/", 1)[-1], inst_of(cand), "affiliation-matched"

    # No institutional evidence. OpenAlex orders by its own relevance,
    # which put an Eric Green with 8 papers above the one who ran NHGRI.
    # Program committees invite people with long records, so fall back to
    # output volume rather than to search rank — and say so in the file.
    top = max(results, key=lambda c: c.get("works_count", 0))
    rivals = sorted((c.get("works_count", 0) for c in results), reverse=True)
    # Two people of the same name and comparable output is the case that
    # silently corrupts a watchlist. Flag it instead of picking one.
    ambiguous = len(rivals) > 1 and rivals[1] > 0.5 * max(rivals[0], 1)
    return (top["id"].rsplit("/", 1)[-1], inst_of(top),
            "ambiguous" if ambiguous else "name-only")


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


def main() -> int:
    ap = argparse.ArgumentParser()
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

    OUT.write_text(yaml.safe_dump({
        "meta": {
            "generated_by": "scripts/track_authors.py",
            "since": args.since,
            "watchlist": str(SPEAKERS.relative_to(ROOT)),
            "blind_spot": (
                "Speakers are selected by program committees, which select for "
                "results that worked. This route cannot surface refutations and "
                "must never be the only input to a briefing."),
        },
        "authors": records,
    }, sort_keys=False, allow_unicode=True, width=88), encoding="utf-8")

    total = covered + missed
    print()
    print(f"resolution: " + ", ".join(f"{k} {v}" for k, v in confidence.most_common()))
    print(f"PubMed-indexed works by watchlist since {args.since}: {total:,}")
    print(f"  already in the 33-journal index: {covered:,}"
          + (f" ({covered / total:.0%})" if total else ""))
    print(f"  outside it:                      {missed:,}")
    print(f"preprints seen: {preprints:,}")
    print(f"wrote {OUT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
