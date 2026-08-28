#!/usr/bin/env python3
"""Build data/index.sqlite (L1) from the per-month PubMed harvest.

The harvest is one TSV per (month, domain), columns:

    pmid <tab> date <tab> journal <tab> authors <tab> title

and the folder a row sits in is the *query* month, not the paper's month.
Those two disagree for about a fifth of all rows, for two separate reasons:

  1. PubMed `[dp]` matches every date attached to a record, so an
     ahead-of-print in November and an issue date in January both hit.
     One paper is then harvested two or three times.
  2. Journals that assign issue dates in advance (Cell Press, JCO,
     Ann Oncol) deposit records dated up to six months in the future.
     Those leak into whichever pull happens to catch them.

Both are fixed the same way: ignore the folder, bin on the record's own
date, keep one row per PMID. Anything outside the corpus window is
dropped rather than clamped into the nearest month — a clamped record is
a silent lie about when something was published, and the whole point of
this index is being able to say when.

Usage:
    python3 scripts/build_index.py                 # rebuild from HARVEST
    python3 scripts/build_index.py --harvest DIR
"""

from __future__ import annotations

import argparse
import collections
import glob
import os
import pathlib
import sqlite3
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
INDEX = ROOT / "data" / "index.sqlite"

# 2024 was added in August 2026, after three separate "first appearance"
# claims turned out to be artefacts of where reading started rather than
# facts about the field. A floor is not a beginning: anything this window
# reports as first is still only first *within the window*.
WINDOW = ("2023-01", "2026-08")
DOMAINS = {"general", "cancer", "immune", "bioinfo", "sysbio"}

SCHEMA = """
DROP TABLE IF EXISTS papers;
CREATE TABLE papers(pmid TEXT PRIMARY KEY, pubdate TEXT, month TEXT,
                    journal TEXT, domain TEXT, authors TEXT, title TEXT);
CREATE INDEX i_month ON papers(month);
CREATE INDEX i_journal ON papers(journal);
CREATE INDEX i_domain ON papers(domain);
"""


def rows(harvest: pathlib.Path):
    """Yield (pmid, pubdate, month, journal, domain, authors, title)."""
    for path in sorted(glob.glob(str(harvest / "**" / "*.tsv"), recursive=True)):
        domain = pathlib.Path(path).stem
        if domain not in DOMAINS:
            continue
        with open(path, encoding="utf-8", errors="replace") as fh:
            for line in fh:
                parts = line.rstrip("\n").split("\t")
                if len(parts) < 5:
                    continue
                pmid, date, journal, authors, title = parts[:5]
                month = date[:7].replace("/", "-")
                if len(month) != 7 or not month[:4].isdigit():
                    continue
                yield pmid, date, month, journal, domain, authors, title


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--harvest", default=os.environ.get("HARVEST", ""),
                    help="directory holding <month>/<domain>.tsv")
    args = ap.parse_args()
    if not args.harvest:
        sys.exit("give --harvest DIR (or set HARVEST)")
    harvest = pathlib.Path(args.harvest)
    if not harvest.is_dir():
        sys.exit(f"no such harvest dir: {harvest}")

    seen: dict[str, tuple] = {}
    raw = dropped = 0
    per_month_dropped: collections.Counter[str] = collections.Counter()

    for row in rows(harvest):
        raw += 1
        month = row[2]
        if not (WINDOW[0] <= month <= WINDOW[1]):
            dropped += 1
            per_month_dropped[month] += 1
            continue
        # First writer wins. The rows are identical apart from which pull
        # they came from, so this only matters for `domain`: a paper that
        # matched two domain queries is credited to the alphabetically
        # first one, which keeps the domain totals summing to the total.
        seen.setdefault(row[0], row)

    INDEX.parent.mkdir(parents=True, exist_ok=True)
    con = sqlite3.connect(INDEX)
    con.executescript(SCHEMA)
    con.executemany("INSERT INTO papers VALUES (?,?,?,?,?,?,?)", seen.values())
    con.commit()

    print(f"harvested rows      {raw:,}")
    print(f"out of window       {dropped:,}  ({', '.join(f'{m} {c}' for m, c in sorted(per_month_dropped.items()))})")
    print(f"deduplicated papers {len(seen):,}")
    print()
    print("month     total   general  cancer  immune  bioinfo  sysbio")
    for m, in con.execute("SELECT DISTINCT month FROM papers ORDER BY month"):
        by = dict(con.execute(
            "SELECT domain,COUNT(*) FROM papers WHERE month=? GROUP BY domain", (m,)))
        tot = sum(by.values())
        print(f"{m}  {tot:6,}   " + "  ".join(
            f"{by.get(d,0):6,}" for d in ["general", "cancer", "immune", "bioinfo", "sysbio"]))

    # A journal contributing nothing to a month is worth surfacing, but it
    # is NOT automatically a harvest defect, and the first version of this
    # check said it was. Every gap it found on its first run — Nucleic
    # Acids Research in 2025-12, Bioinformatics in four months, Genome
    # Research in 2024-01 — returns zero from PubMed itself when queried
    # directly. Those are the journals' own date assignments, not a broken
    # pull. Nature Machine Intelligence is absent from fifteen months
    # because PubMed indexes only the deposited fraction of it.
    # So: check the gap against PubMed before calling it a defect.
    all_months = [m for m, in con.execute(
        "SELECT DISTINCT month FROM papers ORDER BY month")]
    gaps = collections.defaultdict(list)
    for journal, in con.execute("SELECT DISTINCT journal FROM papers ORDER BY journal"):
        present = dict(con.execute(
            "SELECT month, COUNT(*) FROM papers WHERE journal=? GROUP BY month",
            (journal,)))
        for m in all_months:
            if not present.get(m):
                gaps[m].append(journal)
    print()
    if gaps:
        print("ZERO ROWS — journal absent from a month. Query PubMed for that")
        print("journal and month before treating it as a harvest defect:")
        for m in sorted(gaps):
            print(f"  {m}  {', '.join(sorted(gaps[m]))}")
    else:
        print("every journal contributed to every month")
    return 0


if __name__ == "__main__":
    sys.exit(main())
