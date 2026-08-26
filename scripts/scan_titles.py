#!/usr/bin/env python3
"""Surface candidate evidence cards from the index under one written rule.

This script exists because of a specific failure. Every month of this
corpus was read by someone searching that month alone, each applying
roughly-remembered criteria, and the result was three published findings
that had to be withdrawn: a preclinical-block count whose "trend" was
between-reader spread, a vocabulary "arrival" that predated the reading
window, and an "inversion" whose premise never existed. The between-month
differences were smaller than the between-reader differences.

The fix is not to read more carefully. It is to make the first pass
mechanical, so that every month is filtered by the same rule, and to
leave judgement for the step where it is actually needed — deciding
whether a surfaced title states a direction.

THE RULE FOR A CARD, unchanged from how the corpus has been curated:
a finding qualifies only if its DIRECTION is stated in the title, or in
the title of a companion editorial cited on the card. "Effects of X on Y"
is not a finding. "X does not improve Y" is. This is strict on purpose —
it is what makes a card checkable by someone who never reads the paper.

What is surfaced here is a candidate, not a card. Roughly half of these
will be titles that merely contain the word `not` in a subordinate
clause, or JAMA news items that slipped the publication-type filter.

Usage:
    python3 scripts/scan_titles.py 2024-05
    python3 scripts/scan_titles.py 2024-01 2024-12 --kind method
    python3 scripts/scan_titles.py 2024-01 2026-08 --kind refute --journal-tier top
"""

from __future__ import annotations

import argparse
import pathlib
import re
import sqlite3
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
INDEX = ROOT / "data" / "index.sqlite"

# A refutation states that something expected did not happen. Every
# phrase here is one that can only appear in a title when the author has
# committed to a direction.
#
# These are kept as a list, not as one triple-quoted re.VERBOSE blob. The
# blob version silently severed its own alternation groups when it was
# split on newlines to be joined with `|`, and the resulting pattern
# matched roughly every title in the corpus — which looked, at a glance,
# exactly like a productive scan.
REFUTE = [
    r"does not", r"do not", r"did not", r"fails? to", r"failed to",
    r"no (significant )?(benefit|improvement|difference|effect|association"
    r"|advantage|survival)",
    r"not associated", r"dispensable", r"unnecessary",
    r"(is|are|was|were) not required", r"not sufficient", r"insufficient to",
    r"contrary to", r"challenges? the", r"questions? the", r"overturn",
    r"refut", r"negative (trial|results?)", r"futility",
    r"no better than", r"worse (than|outcomes)",
    r"lack of (benefit|efficacy)", r"without improving",
    r"did not meet", r"failure of",
]

# Method credibility is the second axis, tracked separately because it
# undercuts the reliability of everything else rather than any one claim.
METHOD = [
    r"pitfalls?", r"confound", r"artefact", r"artifact", r"irreproducib",
    r"not reproducible", r"reproducibility (crisis|problem|of)",
    r"overestimat", r"underestimat", r"spurious", r"data leakage",
    r"shortcut", r"simple (controls?|models?|methods?|baselines?)",
    r"outperform(s|ed)? (deep|complex|state)", r"limitations of",
    r"misleading", r"retraction", r"expression of concern",
    r"fails? to generalize", r"batch effect", r"benchmarking (crisis|reveals)",
    r"caution(ary)?", r"biases in", r"is not absence",
]

# Approvals, first-in-class and phase 3 readouts: the clinical spine.
CLINICAL = [
    r"phase 3", r"phase iii", r"randomi[sz]ed", r"approval", r"approved",
    r"first-in-(class|human)", r"interim analysis",
    r"did not meet", r"met its primary", r"open-label",
]

KINDS = {"refute": REFUTE, "method": METHOD, "clinical": CLINICAL}

# The tier split the corpus curates by. Not a ranking of importance —
# a filter for where a direction-stating title carries enough weight
# that it is worth a card on its own.
TOP = {"Nature", "Science", "Cell", "N Engl J Med", "Lancet", "JAMA",
       "Nat Med", "Nat Genet", "Cancer Discov", "Nat Cancer", "Cancer Cell",
       "Lancet Oncol", "Immunity", "Nat Immunol", "Nat Methods",
       "Nat Biotechnol"}


def compile_kind(kind: str) -> re.Pattern:
    return re.compile("|".join(f"(?:{p})" for p in KINDS[kind]), re.IGNORECASE)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("start", help="YYYY-MM")
    ap.add_argument("end", nargs="?", help="YYYY-MM (defaults to start)")
    ap.add_argument("--kind", default="refute", choices=sorted(KINDS))
    ap.add_argument("--journal-tier", choices=["top", "all"], default="all")
    ap.add_argument("--domain", default="")
    args = ap.parse_args()
    end = args.end or args.start

    if not INDEX.exists():
        sys.exit("no data/index.sqlite — run scripts/build_index.py")

    pattern = compile_kind(args.kind)
    con = sqlite3.connect(INDEX)
    query = ("SELECT month, pmid, journal, domain, title FROM papers "
             "WHERE month BETWEEN ? AND ?")
    params: list = [args.start, end]
    if args.domain:
        query += " AND domain=?"
        params.append(args.domain)
    query += " ORDER BY month, journal"

    hits = 0
    scanned = 0
    for month, pmid, journal, domain, title in con.execute(query, params):
        scanned += 1
        if args.journal_tier == "top" and journal not in TOP:
            continue
        if not pattern.search(title):
            continue
        hits += 1
        print(f"{month}  {pmid:9}  {journal:22} {domain:8} {title}")

    print(f"\n{hits:,} candidates from {scanned:,} titles "
          f"({args.kind}, {args.start}..{end})", file=sys.stderr)
    print("A candidate is not a card. Keep only the ones whose title states "
          "a direction.", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
