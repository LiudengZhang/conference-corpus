#!/usr/bin/env python3
"""Check the invariants the corpus keeps breaking.

Every failure this corpus has had to publish a correction for was
detectable mechanically before it went out, and none of them were
detected, because the checks lived in whoever happened to be reading.
This is that reading, written down.

  1  Every card's PMID is in the index.
  2  Every card's date matches the index's date for that PMID. A card
     dated by hand drifts from the record it cites, and the drift is
     invisible: the thread curve moves a month and nothing looks wrong.
  3  Every thread a card names exists in threads.yml.
  4  threads.yml `opened` equals the first card on that thread. This
     field is documented in threads.yml as computed rather than
     asserted; twelve of thirteen were stale when the check was first
     run, all of them left behind by a backfill.
  5  Every PMID linked from a briefing is in the index — a briefing that
     cites a paper the corpus never read is citing a memory.
  6  No briefing still contains the generator's HAND-WRITTEN placeholder.
  7  Every source claiming status `harvested` has rows in the store it
     claims. sources.yml describes `harvested` as "the only status that is
     checkable rather than asserted, and the only one a generator should
     trust" — which was true of its definition and false of its practice,
     because nothing checked it. This is that check.
  8  Every source named by a store — a venue in the conference store, a
     journal name in the index — is one the registry defines, and every
     source with rows says so, so the two can actually be joined.
  9  ADVISORY, not a failure: cards whose `claim` shares no content word
     with their own `title`. Two cards were found on 2026-08-27 carrying a
     claim about an entirely different paper than the PMID they cite — one
     claimed metallophilic macrophages cross-prime CD8 T cells while citing
     a MEF2C microglia paper. Checks 1 and 2 passed both, because the PMID
     existed and the date matched; all 712 titles then in the corpus matched
     the index exactly, so a title check would not have caught them either.
     (712 was the card count on 2026-08-27, when this was written. It is 2,875
     now, and the review queue this check prints is correspondingly longer.)
     Nothing can decide
     mechanically whether a paraphrase is faithful, so this prints a review
     queue and never fails the run.

Checks 7 and 8 skip, rather than fail, when a regenerable side store is
absent — a fresh clone has the journal index and nothing else, and a
missing store is a thing you have not built, not a broken invariant.

Exit code is non-zero if anything fails, so it can gate a commit.

Usage:
    python3 scripts/check_corpus.py
    python3 scripts/check_corpus.py --fix-opened
"""

from __future__ import annotations

import argparse
import collections
import pathlib
import re
import sqlite3
import sys

import yaml

ROOT = pathlib.Path(__file__).resolve().parent.parent
INDEX = ROOT / "data" / "index.sqlite"
CARDS = ROOT / "data" / "evidence.yml"
THREADS = ROOT / "data" / "threads.yml"
SOURCES = ROOT / "data" / "sources.yml"
BRIEFINGS = ROOT / "docs" / "briefings"

PMID_LINK = re.compile(r"pubmed\.ncbi\.nlm\.nih\.gov/(\d+)")

# Which store backs each source type, the column holding the key, and the
# registry field that key joins to. Journals join on `pubmed` rather than `id`
# because the index stores PubMed abbreviations ("Nucleic Acids Res") and the
# registry stores names ("Nucleic Acids Research"); the abbreviation lives on
# the source so the join is looked up, never derived.
STORES = {
    "conference": ("conference.sqlite", "abstracts", "venue", "id"),
    "journal": ("index.sqlite", "papers", "journal", "pubmed"),
    "news": ("news.sqlite", "news", "source", "id"),
    "regulatory": ("regulatory.sqlite", "sources", "id", "id"),
}


def store_ids(filename: str, table: str, column: str) -> set[str] | None:
    """Distinct source ids present in a side store, or None if unbuilt."""
    path = ROOT / "data" / filename
    if not path.exists():
        return None
    con = sqlite3.connect(f"file:{path}?mode=ro", uri=True)
    if not con.execute(
            "SELECT 1 FROM sqlite_master WHERE type IN ('table','view') AND name=?",
            (table,)).fetchone():
        return None
    return {r[0] for r in con.execute(f"SELECT DISTINCT {column} FROM {table}")}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--fix-opened", action="store_true",
                    help="rewrite threads.yml `opened` to the computed value")
    args = ap.parse_args()

    con = sqlite3.connect(INDEX)
    index = dict(con.execute("SELECT pmid, month FROM papers"))
    cards = yaml.safe_load(CARDS.read_text())["evidence"]
    threads = yaml.safe_load(THREADS.read_text())["threads"]
    thread_ids = {t["id"] for t in threads}
    aliases = {a for t in threads for a in (t.get("aliases") or [])}

    problems: list[str] = []

    # 1 + 2 --------------------------------------------------------------
    missing = drifted = 0
    for c in cards:
        pmid = str(c.get("pmid", "")).strip()
        card_month = str(c.get("date", ""))[:7]
        if pmid not in index:
            problems.append(f"card {c.get('id', pmid)}: PMID {pmid} not in index")
            missing += 1
            continue
        if index[pmid] != card_month:
            problems.append(
                f"card {c.get('id', pmid)}: dated {card_month}, "
                f"index says {index[pmid]}")
            drifted += 1

    # 3 ------------------------------------------------------------------
    unknown: collections.Counter[str] = collections.Counter()
    for c in cards:
        for t in c.get("threads") or []:
            if t not in thread_ids:
                unknown[t] += 1
    for t, n in unknown.most_common():
        note = " (an alias — point the card at the surviving id)" if t in aliases else ""
        problems.append(f"thread `{t}` named by {n} cards but not defined{note}")

    # 4 ------------------------------------------------------------------
    first: dict[str, str] = {}
    for c in cards:
        month = str(c.get("date", ""))[:7]
        for t in c.get("threads") or []:
            if t not in first or month < first[t]:
                first[t] = month
    stale = []
    for t in threads:
        want = first.get(t["id"])
        if want and str(t.get("opened")) != want:
            stale.append((t["id"], str(t.get("opened")), want))
            problems.append(
                f"thread `{t['id']}`: opened says {t.get('opened')}, "
                f"first card is {want}")

    if stale and args.fix_opened:
        text = THREADS.read_text()
        for tid, was, now in stale:
            # Rewrite only the `opened:` line inside this thread's block,
            # located from its id, so surrounding comments survive.
            pattern = re.compile(
                rf"(- id: {re.escape(tid)}\n(?:.*\n)*?\s*opened: )\S+")
            text, n = pattern.subn(rf"\g<1>{now}", text, count=1)
            if not n:
                print(f"  could not rewrite opened for {tid}", file=sys.stderr)
        THREADS.write_text(text)
        print(f"rewrote {len(stale)} `opened` values in data/threads.yml")
        problems = [p for p in problems if "opened says" not in p]

    # 5 + 6 --------------------------------------------------------------
    unlinked = stubs = 0
    for path in sorted(BRIEFINGS.glob("20*.md")):
        text = path.read_text()
        if "HAND-WRITTEN" in text:
            problems.append(f"{path.name}: still has the generator placeholder")
            stubs += 1
        for pmid in set(PMID_LINK.findall(text)):
            if pmid not in index:
                problems.append(f"{path.name}: links PMID {pmid}, not in index")
                unlinked += 1

    # 7 + 8 --------------------------------------------------------------
    sources = yaml.safe_load(SOURCES.read_text())["sources"]
    store_lines: list[str] = []
    for stype, (filename, table, column, field) in sorted(STORES.items()):
        # Key the registry the way its store keys it, but report by id: an id
        # is what a reader can grep for, and "Nat Med" on its own is not.
        owner: dict[str, str] = {}
        for s in sources:
            key = s.get(field)
            if not key:
                continue
            if key in owner and owner[key] != s["id"]:
                problems.append(
                    f"sources `{owner[key]}` and `{s['id']}` both claim "
                    f"`{field}` {key!r} — the join is ambiguous")
            owner.setdefault(key, s["id"])

        claimed = set()
        for s in sources:
            if s.get("type") != stype or s.get("status") != "harvested":
                continue
            if not s.get(field):
                problems.append(
                    f"source `{s['id']}` claims status harvested but has no "
                    f"`{field}` to join it to data/{filename}")
                continue
            claimed.add(s[field])

        present = store_ids(filename, table, column)
        if present is None:
            store_lines.append(
                f"{stype:11} store not built — {len(claimed)} claimed, unchecked")
            continue
        for key in sorted(claimed - present):
            problems.append(
                f"source `{owner[key]}` claims status harvested but has no rows "
                f"in data/{filename}")
        for key in sorted(present - set(owner)):
            problems.append(
                f"data/{filename} holds `{key}`, which the registry does not define")
        unclaimed = present & set(owner) - claimed
        note = f", {len(unclaimed)} harvested but not marked" if unclaimed else ""
        store_lines.append(
            f"{stype:11} {len(present):,} in store, {len(claimed)} claimed{note}")
        for key in sorted(unclaimed):
            problems.append(
                f"source `{owner[key]}` has rows in data/{filename} but status is "
                f"not `harvested`")

    # 9 ------------------------------------------------------------------
    # A claim legitimately paraphrases, so low overlap is a smell and not a
    # defect. Printed for a human to read, deliberately outside `problems`.
    stop = set("the a an of and or in for to with by on from as is are be been that this "
               "these those at into over under after before during than then not no its "
               "their it we our study patients cancer tumour tumor cell cells human "
               "clinical trial results data new using via can may show shows shown "
               "reveal reveals identify identifies".split())

    def content(text: str) -> set[str]:
        return {w for w in re.findall(r"[a-z0-9-]{4,}", (text or "").lower())
                if w not in stop}

    incoherent = []
    for c in cards:
        ct, cl = content(c.get("title", "")), content(c.get("claim", ""))
        if not ct or not cl:
            continue
        if not (ct & cl):
            incoherent.append(c.get("id", c.get("pmid")))

    # --------------------------------------------------------------------
    print(f"cards      {len(cards):,}   missing PMID {missing}, date drift {drifted}")
    print(f"threads    {len(threads):,}   undefined names {len(unknown)}, "
          f"stale opened {0 if args.fix_opened else len(stale)}")
    print(f"briefings  {len(list(BRIEFINGS.glob('20*.md'))):,}   "
          f"unlinked PMIDs {unlinked}, stubs {stubs}")
    print(f"index      {len(index):,} papers")
    for line in store_lines:
        print(f"{line}")
    print()

    if incoherent:
        print(f"review     {len(incoherent)} card(s) whose claim shares no content word "
              f"with their title — advisory, not a failure:")
        for cid in incoherent[:12]:
            print(f"  {cid}")
        if len(incoherent) > 12:
            print(f"  ... and {len(incoherent) - 12} more")
        print()

    if not problems:
        print("all invariants hold")
        return 0
    print(f"{len(problems)} problem(s):")
    for p in problems[:60]:
        print(f"  {p}")
    if len(problems) > 60:
        print(f"  ... and {len(problems) - 60} more")
    return 1


if __name__ == "__main__":
    sys.exit(main())
