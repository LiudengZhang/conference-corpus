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


def papers_test(ccon: sqlite3.Connection, jcon: sqlite3.Connection,
                threshold: float) -> int:
    """Match abstracts to later papers, one document at a time.

    The vocabulary tests answer a question nobody actually asked. The
    premise is not "words are said earlier at meetings" — it is "this
    result was shown at the meeting before it was published", and a term
    that was already common in 2024 is invisible to any frequency method
    however early the work appeared. So: match the abstract to the paper.

    Conference abstracts that become papers usually keep most of their
    title. Jaccard overlap on content words, candidates generated from an
    inverted index on the rarer tokens so this does not become 14,895 x
    35,542 comparisons.

    The false-match rate is estimated by running the identical matcher
    against journal titles published BEFORE the meetings opened, where a
    match cannot be a prediction and can only be coincidence.
    """
    conf = list(ccon.execute(
        "SELECT venue, month, title FROM abstracts WHERE LENGTH(title) > 30"))
    after = list(jcon.execute(
        "SELECT month, pmid, title FROM papers WHERE month >= '2024-07'"))
    before = list(jcon.execute(
        "SELECT month, pmid, title FROM papers WHERE month < '2024-04'"))

    def content(title):
        return {w for w in WORD.findall(title.lower())
                if w not in STOP and len(w) > 3}

    def build(docs):
        sets = [content(t) for _, _, t in docs]
        df: collections.Counter[str] = collections.Counter()
        for s in sets:
            df.update(s)
        inv: dict[str, list[int]] = {}
        for i, s in enumerate(sets):
            for w in s:
                if df[w] <= 400:      # skip words too common to narrow anything
                    inv.setdefault(w, []).append(i)
        return sets, inv

    def match(docs, sets, inv):
        hits = []
        for venue, cmonth, ctitle in conf:
            cs = content(ctitle)
            if len(cs) < 5:
                continue
            counts: collections.Counter[int] = collections.Counter()
            for w in cs:
                for i in inv.get(w, ()):
                    counts[i] += 1
            best, best_score = None, 0.0
            for i, shared in counts.most_common(60):
                if shared < 4:
                    break
                score = shared / len(cs | sets[i])
                if score > best_score:
                    best, best_score = i, score
            if best is not None and best_score >= threshold:
                hits.append((venue, cmonth, docs[best][0], docs[best][1],
                             best_score, ctitle))
        return hits

    sets_a, inv_a = build(after)
    real = match(after, sets_a, inv_a)
    sets_b, inv_b = build(before)
    fake = match(before, sets_b, inv_b)

    n = len(conf)
    print("TEST C — abstracts matched to the papers they became")
    print(f"  conference abstracts with a usable title: {n:,}")
    print(f"  matched to a journal paper published later (Jaccard >= {threshold}): "
          f"{len(real):,}  ({len(real) / n:.1%})")
    print(f"  same matcher against papers published BEFORE the meetings: "
          f"{len(fake):,}  ({len(fake) / n:.1%})")
    print("    The second line is the coincidence rate. A match there cannot be")
    print("    a prediction, so it is what this method scores on pure chance.")
    print()
    if not real:
        return 0
    lags = sorted((int(jm[:4]) - int(cm[:4])) * 12 + int(jm[5:7]) - int(cm[5:7])
                  for _, cm, jm, _, _, _ in real)
    print(f"  median lag abstract -> paper: {statistics.median(lags):.0f} months")
    print(f"  quartiles: {lags[len(lags)//4]}, {statistics.median(lags):.0f}, "
          f"{lags[3*len(lags)//4]} months")
    by_venue = collections.Counter(v for v, *_ in real)
    print(f"  by venue: " + ", ".join(f"{v} {c:,}" for v, c in by_venue.most_common()))
    print()
    print("  Longest-lead matches:")
    for venue, cm, jm, pmid, score, title in sorted(real, key=lambda r: (
            -((int(r[2][:4]) - int(r[1][:4])) * 12 + int(r[2][5:7]) - int(r[1][5:7]))))[:15]:
        lag = (int(jm[:4]) - int(cm[:4])) * 12 + int(jm[5:7]) - int(cm[5:7])
        print(f"    {lag:+3d}mo  {venue} {cm} -> {jm}  {pmid}  {title[:78]}")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--papers", action="store_true",
                    help="match abstracts to the papers they became (TEST C)")
    ap.add_argument("--threshold", type=float, default=0.5,
                    help="Jaccard cutoff for a paper-level match")
    ap.add_argument("--abstracts", action="store_true",
                    help="let the conference use abstract bodies, not just titles")
    ap.add_argument("--min-total", type=int, default=20,
                    help="term must occur this often across both corpora (TEST B)")
    ap.add_argument("--min-conf", type=int, default=5,
                    help="term must occur in this many conference records (TEST A)")
    args = ap.parse_args()

    if not CONF.exists():
        sys.exit("no data/conference.sqlite — run scripts/harvest_conference.py")

    if args.papers:
        return papers_test(sqlite3.connect(CONF), sqlite3.connect(INDEX),
                           args.threshold)

    jcon = sqlite3.connect(INDEX)
    base_docs = list(jcon.execute(
        "SELECT month, title FROM papers WHERE month BETWEEN ? AND ?", BASE))
    # Deterministic half of the same year, used as the null predictor.
    # Splitting on the PMID's last digit is stable across rebuilds; the
    # script must not use randomness it cannot reproduce.
    half_docs = list(jcon.execute(
        "SELECT month, title FROM papers WHERE month BETWEEN ? AND ? "
        "AND CAST(SUBSTR(pmid,-1) AS INTEGER) < 5", BASE))
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
    jhalf, _ = tally(half_docs)
    jlater, _ = tally(later_docs)
    jall, jfirst = tally(all_docs)
    conf, _ = tally(conf_docs)

    n_base, n_later, n_conf = len(base_docs), len(later_docs), len(conf_docs)
    n_half = len(half_docs)

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
    # The two buckets have to be shown, not just counted. A large part of
    # the "never arrived" side is not a failed prediction at all — it is
    # abstract register (`pts with`, `mcrpc`, `real world`) that journal
    # titles would never use whatever the science did. Reading the lists
    # is the only way to tell a wrong call from a vocabulary mismatch.
    loud_arrived = sorted(((conf[t], t, arrived[t]) for t in arrived), reverse=True)
    loud_never = sorted(((conf[t], t) for t in novel if t not in arrived), reverse=True)
    print()
    print("  Loudest that later reached a journal title:")
    for n, t, when in loud_arrived[:14]:
        print(f"    {n:4} abstracts  ->  {when}   {t}")
    print("  Loudest that never did:")
    for n, t in loud_never[:14]:
        print(f"    {n:4} abstracts  ->  never    {t}")
    print()

    # ---- TEST B -------------------------------------------------------
    terms = [t for t in set(jbase) | set(conf)
             if jbase.get(t, 0) + conf.get(t, 0) >= args.min_total]

    rows = []
    for t in terms:
        rb = (jbase.get(t, 0) + 0.5) / n_base
        rl = (jlater.get(t, 0) + 0.5) / n_later
        rc = (conf.get(t, 0) + 0.5) / n_conf
        rh = (jhalf.get(t, 0) + 0.5) / n_half
        rows.append((math.log(rc / rb), math.log(rl / rb), t, math.log(rh / rb)))

    print("TEST B — does over-representation at the meetings predict journal growth?")
    print(f"  terms scored (>= {args.min_total} occurrences across both): {len(rows):,}")
    if len(rows) < 50:
        print("  too few terms to say anything")
        return 0

    rho = spearman([(r[0], r[1]) for r in rows])
    rho_null = spearman([(r[3], r[1]) for r in rows])
    # Terms absent from journal titles in 2024 are mostly register, not
    # content: `pts with metastatic`, `real world`, `mcrpc`. Abstracts are
    # written in a compressed clinical shorthand that journal titles never
    # use, so those terms score maximum conference excess while saying
    # nothing about where the field went. Requiring one journal title
    # anywhere in 2024 removes the register layer and leaves the topical one.
    grounded = [r for r in rows if jbase.get(r[2], 0) >= 1]
    rho_grounded = spearman([(r[0], r[1]) for r in grounded])
    print(f"  rho(conference excess, 2024->2026 growth)  = {rho:+.3f}")
    print(f"  rho(null: half of 2024 itself, same growth) = {rho_null:+.3f}")
    print(f"  rho, register-controlled (term in >= 1 journal title in 2024,"
          f" n={len(grounded):,}) = {rho_grounded:+.3f}")
    print("    Both predictors carry the 2024 rate in their denominator, so a term")
    print("    that was low in 2024 by chance scores high on excess AND on growth.")
    print("    That artefact alone produces the null figure. Only the gap between")
    print("    the two lines is evidence that the meeting knows anything.")
    print()

    # Stratified estimate: within a band of identical 2024 journal counts,
    # the shared denominator is held fixed and cannot manufacture anything.
    print("  Held-fixed check — within bands of equal 2024 journal frequency,")
    print("  does the conference rate still rank the 2026 journal rate?")
    print(f"    {'2024 journal titles':>22}  {'terms':>6}  {'rho':>7}")
    # Bands must be narrow at the top or they defeat their own purpose: an
    # unbounded 31+ band spans 31 to several thousand, so the prevalence
    # the band was meant to hold fixed is still varying inside it, and the
    # correlation it reports is that leftover prevalence rather than any
    # predictive content. The first run of this check read +0.402 there
    # for exactly that reason.
    bands = [(1, 2), (3, 5), (6, 12), (13, 30), (31, 60), (61, 120),
             (121, 250), (251, 10 ** 9)]
    for lo, hi in bands:
        band = [t for t in terms if lo <= jbase.get(t, 0) <= hi]
        if len(band) < 40:
            continue
        pairs = [((conf.get(t, 0) + 0.5) / n_conf,
                  (jlater.get(t, 0) + 0.5) / n_later) for t in band]
        label = f"{lo}-{hi}" if hi < 10 ** 9 else f"{lo}+"
        print(f"    {label:>22}  {len(band):6,}  {spearman(pairs):+7.3f}")
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
    for row in sorted(top, key=lambda r: -r[0])[:25]:
        t, growth = row[2], row[1]
        print(f"    {t:38} {conf.get(t,0):5} {jbase.get(t,0):6} "
              f"{jlater.get(t,0):6}  x{math.exp(growth):5.2f}")

    print()
    print("  Biggest journal growth 2024->2026, and whether the meetings saw it:")
    for row in sorted(rows, key=lambda r: -r[1])[:25]:
        t, growth = row[2], row[1]
        seen = f"{conf.get(t,0):5}" if conf.get(t, 0) else "    -"
        print(f"    {t:38} {seen} {jbase.get(t,0):6} "
              f"{jlater.get(t,0):6}  x{math.exp(growth):5.2f}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
