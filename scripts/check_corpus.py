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
BRIEFINGS = ROOT / "docs" / "briefings"

PMID_LINK = re.compile(r"pubmed\.ncbi\.nlm\.nih\.gov/(\d+)")


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

    # --------------------------------------------------------------------
    print(f"cards      {len(cards):,}   missing PMID {missing}, date drift {drifted}")
    print(f"threads    {len(threads):,}   undefined names {len(unknown)}, "
          f"stale opened {0 if args.fix_opened else len(stale)}")
    print(f"briefings  {len(list(BRIEFINGS.glob('20*.md'))):,}   "
          f"unlinked PMIDs {unlinked}, stubs {stubs}")
    print(f"index      {len(index):,} papers")
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
