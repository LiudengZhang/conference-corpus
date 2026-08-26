#!/usr/bin/env python3
"""Test the premise: do meeting programs lead the journal literature?

Everything in this repo rests on the assumption that they do — that a
term, a target or a method is said at a meeting a year or two before it
is said in the journals, and that the gap is the edge. The assumption
was never tested, because until August 2026 the journal index started at
2025-01 and every conference vault was 2026: the two layers barely
overlapped, so no lead was measurable in either direction.

The test needs a conference old enough for the literature to have
answered it. AACR 2024 (abstracts published March-April 2024) and ASCO
2024 (symposia in January and February, annual meeting in June) against
a journal index running 2024-01 to 2026-08.

The first version of this script measured first appearance: earliest
conference month for a term against its earliest journal month. It
returned "conference first, 100%, median lead twelve months", which is
not a result — it is the shape of the two windows, since the journal
index at the time began after the meetings ended. Worse, once 2024 was
added the ranking was still dominated by `powered`, `unknown`,
`decreases` and `potentially`. First appearance of a *term* is a
statement about word frequency, not about novelty: a common word crosses
any threshold late simply by being spread thin. That measure is gone.

What replaced it is a prediction with a baseline, which is the only
version of this question that can come out negative:

  TEST A  Vocabulary genuinely absent from the journals. Terms said at
          the 2024 meetings that appear in *no* journal title in all of
          2024. How many arrive later, and when? Descriptive — there is
          no control group for "things nobody said anywhere".

  TEST B  The real test. Rank terms by how over-represented they are at
          the meetings relative to the 2024 journals, then ask whether
          that over-representation predicts growth in the journals by
          2026. The baseline is the journals' own 2024 rate. If the
          meeting carries no information the journals did not already
          have, high-excess and low-excess terms grow alike and the
          correlation is zero.

Titles are compared against titles. Conference records carry full
abstract text and journal records carry only titles; letting the
conference use its abstract bodies would hand it several hundred extra
words per record and manufacture a lead on terms too minor to reach any
title. `--abstracts` runs that variant deliberately, and it is the more
realistic picture of what someone sitting at the meeting actually sees.

Usage:
    python3 scripts/lead_time.py
    python3 scripts/lead_time.py --abstracts
"""

from __future__ import annotations

import argparse
import collections
import math
import pathlib
import re
import sqlite3
import statistics
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
INDEX = ROOT / "data" / "index.sqlite"
CONF = ROOT / "data" / "conference.sqlite"

BASE = ("2024-01", "2024-12")   # the year the meetings happened
LATER = ("2026-01", "2026-12")  # far enough out for the literature to answer

WORD = re.compile(r"[a-z0-9][a-z0-9\-']*")

STOP = set("""a an and are as at be by for from has have in into is it its of on or
that the their to was were which with we our this these those study results
using use used based new novel high low non more most can may show shows shown
between during after before both each other than then when where how why
patients patient cell cells human analysis data model models method methods
approach effect effects role expression response associated association
identification characterization evaluation assessment development potential
significant increased decreased via through among against without within
""".split())


def grams(text: str, n_max: int = 3):
    words = WORD.findall(text.lower())
    out = set()
    for n in range(1, n_max + 1):
        for i in range(len(words) - n + 1):
            span = words[i:i + n]
            if span[0] in STOP or span[-1] in STOP:
                continue
            term = " ".join(span)
            if len(term) < 5:
                continue
            out.add(term)
    return out


def tally(docs):
    """term -> document count, plus term -> earliest month."""
    count: collections.Counter[str] = collections.Counter()
    first: dict[str, str] = {}
    for month, text in docs:
        for term in grams(text):
            count[term] += 1
            if term not in first or month < first[term]:
                first[term] = month
    return count, first


def spearman(pairs) -> float:
    """Rank correlation, ties averaged. No scipy in this repo."""
    def ranks(values):
        order = sorted(range(len(values)), key=lambda i: values[i])
        out = [0.0] * len(values)
        i = 0
        while i < len(order):
            j = i
            while j + 1 < len(order) and values[order[j + 1]] == values[order[i]]:
                j += 1
            avg = (i + j) / 2 + 1
            for k in range(i, j + 1):
                out[order[k]] = avg
            i = j + 1
        return out

    xs, ys = ranks([p[0] for p in pairs]), ranks([p[1] for p in pairs])
    n = len(pairs)
    mx, my = sum(xs) / n, sum(ys) / n
    num = sum((a - mx) * (b - my) for a, b in zip(xs, ys))
    den = math.sqrt(sum((a - mx) ** 2 for a in xs) * sum((b - my) ** 2 for b in ys))
    return num / den if den else 0.0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--abstracts", action="store_true",
                    help="let the conference use abstract bodies, not just titles")
    ap.add_argument("--min-total", type=int, default=20,
                    help="term must occur this often across both corpora (TEST B)")
    ap.add_argument("--min-conf", type=int, default=5,
                    help="term must occur in this many conference records (TEST A)")
    args = ap.parse_args()

    if not CONF.exists():
        sys.exit("no data/conference.sqlite — run scripts/harvest_conference.py")

    jcon = sqlite3.connect(INDEX)
    base_docs = list(jcon.execute(
        "SELECT month, title FROM papers WHERE month BETWEEN ? AND ?", BASE))
    later_docs = list(jcon.execute(
        "SELECT month, title FROM papers WHERE month BETWEEN ? AND ?", LATER))
    all_docs = list(jcon.execute("SELECT month, title FROM papers"))

    ccon = sqlite3.connect(CONF)
    field = "title || ' ' || abstract" if args.abstracts else "title"
    conf_docs = list(ccon.execute(f"SELECT month, {field} FROM abstracts"))

    if not base_docs:
        sys.exit(f"index has no papers in {BASE[0]}..{BASE[1]} — rebuild it first")

    print(f"journal titles {BASE[0]}..{BASE[1]}   {len(base_docs):,}")
    print(f"journal titles {LATER[0]}..{LATER[1]}   {len(later_docs):,}")
    print(f"conference records 2024      {len(conf_docs):,}"
          + ("  (titles + abstract bodies)" if args.abstracts else "  (titles only)"))
    print()

    jbase, _ = tally(base_docs)
    jlater, _ = tally(later_docs)
    jall, jfirst = tally(all_docs)
    conf, _ = tally(conf_docs)

    n_base, n_later, n_conf = len(base_docs), len(later_docs), len(conf_docs)

    # ---- TEST A -------------------------------------------------------
    novel = {t for t, c in conf.items()
             if c >= args.min_conf and jbase.get(t, 0) == 0}
    arrived = {t: jfirst[t] for t in novel if t in jfirst and jfirst[t] > "2024-12"}
    print("TEST A — conference vocabulary absent from every 2024 journal title")
    print(f"  terms said at >= {args.min_conf} meeting records, unseen in 2024 journals: {len(novel):,}")
    print(f"  later appear in a journal title:  {len(arrived):,}"
          f"  ({len(arrived) / max(len(novel), 1):.0%})")
    print(f"  never appear at all:              {len(novel) - len(arrived):,}"
          f"  ({1 - len(arrived) / max(len(novel), 1):.0%})")
    if arrived:
        delays = sorted(
            (int(m[:4]) - 2024) * 12 + int(m[5:7]) - 6 for m in arrived.values())
        print(f"  median delay from the meetings closing: {statistics.median(delays):.0f} months")
    print()

    # ---- TEST B -------------------------------------------------------
    terms = [t for t in set(jbase) | set(conf)
             if jbase.get(t, 0) + conf.get(t, 0) >= args.min_total]

    rows = []
    for t in terms:
        rb = (jbase.get(t, 0) + 0.5) / n_base
        rl = (jlater.get(t, 0) + 0.5) / n_later
        rc = (conf.get(t, 0) + 0.5) / n_conf
        rows.append((math.log(rc / rb), math.log(rl / rb), t))

    print("TEST B — does over-representation at the meetings predict journal growth?")
    print(f"  terms scored (>= {args.min_total} occurrences across both): {len(rows):,}")
    if len(rows) < 50:
        print("  too few terms to say anything")
        return 0

    rho = spearman([(r[0], r[1]) for r in rows])
    print(f"  Spearman rho(conference excess, 2024->2026 journal growth) = {rho:+.3f}")
    print()

    rows.sort()
    d = len(rows) // 10
    top, bottom = rows[-d:], rows[:d]
    print(f"  top decile by conference excess    median growth  "
          f"x{math.exp(statistics.median(r[1] for r in top)):.2f}")
    print(f"  bottom decile                      median growth  "
          f"x{math.exp(statistics.median(r[1] for r in bottom)):.2f}")
    print()

    print("  Most over-represented at the meetings, and what the journals did by 2026:")
    print(f"    {'term':38} {'conf':>5} {'j2024':>6} {'j2026':>6}  growth")
    for excess, growth, t in sorted(top, key=lambda r: -r[0])[:25]:
        print(f"    {t:38} {conf.get(t,0):5} {jbase.get(t,0):6} "
              f"{jlater.get(t,0):6}  x{math.exp(growth):5.2f}")

    print()
    print("  Biggest journal growth 2024->2026, and whether the meetings saw it:")
    for excess, growth, t in sorted(rows, key=lambda r: -r[1])[:25]:
        seen = f"{conf.get(t,0):5}" if conf.get(t, 0) else "    -"
        print(f"    {t:38} {seen} {jbase.get(t,0):6} "
              f"{jlater.get(t,0):6}  x{math.exp(growth):5.2f}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
