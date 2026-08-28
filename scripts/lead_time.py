#!/usr/bin/env python3
"""Test the premise: do meeting programs lead the journal literature?

Everything in this repo rests on the assumption that they do — that a
term, a target or a method is said at a meeting a year or two before it
is said in the journals, and that the gap is the edge. The assumption
was never tested, because until August 2026 the journal index started at
2025-01 and every conference vault was 2026: the two layers barely
overlapped, so no lead was measurable in either direction.

The test needs a conference old enough for the literature to have
answered it. AACR and ASCO both qualify: `--cohort 2024` (AACR abstracts
March-April, ASCO symposia in January and February and the annual
meeting in June) and `--cohort 2023`. Which months each cohort actually
occupies is read from data/conference.sqlite, and the journal window is
read from data/index.sqlite, because both keep growing — the index ran
2024-01..2026-08 when this was written and every boundary below used to
be a literal, which meant a harvest could move the data underneath the
script without moving any of its arithmetic.

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
          the cohort's meetings that appear in *no* journal title in all
          of the meeting year. How many arrive later, and when?
          Descriptive — there is no control group for "things nobody
          said anywhere".

  TEST B  The real test. Rank terms by how over-represented they are at
          the meetings relative to the meeting-year journals, then ask
          whether that over-representation predicts growth in the
          journals by the index's last full year. The baseline is the
          journals' own meeting-year rate. If the meeting carries no
          information the journals did not already have, high-excess and
          low-excess terms grow alike and the correlation is zero.

Titles are compared against titles. Conference records carry full
abstract text and journal records carry only titles; letting the
conference use its abstract bodies would hand it several hundred extra
words per record and manufacture a lead on terms too minor to reach any
title. `--abstracts` runs that variant deliberately, and it is the more
realistic picture of what someone sitting at the meeting actually sees.

Usage:
    python3 scripts/lead_time.py
    python3 scripts/lead_time.py --abstracts
    python3 scripts/lead_time.py --papers --cohort 2023
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

DEFAULT_COHORT = 2024

# Share of the cohort's abstracts that has to be deposited before the meeting
# window is called closed. ASCO deposits a long thin tail — two 2023 abstracts
# land in November — and taking a bare MAX(month) would push the "after the
# meetings" boundary five months later on the strength of two records. The
# handful of abstracts past the boundary are dropped from the conference side
# too, so that every abstract compared here really does predate every journal
# title in the "after" arm.
COHORT_COVERAGE = 0.99

# Words in more than this share of a matcher pool are skipped: they cannot
# narrow a candidate list. It has to be a share and not the absolute 400 this
# was written as, because the pools below are deliberately resized — an
# absolute ceiling would mean "top 1.4% of a 29,000-title pool" in one arm and
# "top 3.6%" in another, so the two arms would not be running the same matcher.
DF_CEILING_FRAC = 0.014

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


def index_span(jcon: sqlite3.Connection) -> tuple[str, str]:
    """First and last month the journal index actually holds."""
    lo, hi = jcon.execute("SELECT MIN(month), MAX(month) FROM papers").fetchone()
    if not lo:
        sys.exit("data/index.sqlite has no papers — run scripts/build_index.py")
    return lo, hi


def cohort_window(ccon: sqlite3.Connection, year: int) -> tuple[str, str, int, int]:
    """(first month, last month, abstracts kept, abstracts dropped as tail).

    The meeting window is a fact about the cohort, not a constant. AACR 2024
    deposits across 2024-03..04 and ASCO 2024 across 2024-01..08; the 2023
    cohort sits in different months again, and everything downstream — which
    journal months count as "before" and which as "after" — hangs off it.
    """
    rows = ccon.execute(
        "SELECT month, COUNT(*) FROM abstracts WHERE year=? GROUP BY month "
        "ORDER BY month", (year,)).fetchall()
    if not rows:
        sys.exit(f"data/conference.sqlite holds no {year} abstracts — "
                 f"run scripts/harvest_conference.py")
    total = sum(c for _, c in rows)
    seen = 0
    for month, count in rows:
        seen += count
        if seen >= COHORT_COVERAGE * total:
            return rows[0][0], month, seen, total - seen
    return rows[0][0], rows[-1][0], total, 0


def thinned(rows, target: int):
    """Deterministically cut `rows` down to `target` records.

    Evenly spaced indices over a (month, pmid)-sorted list take the same share
    out of every month, so the thinned pool keeps the shape of the full one,
    and it picks the same records on every rerun — the script must not use
    randomness it cannot reproduce.
    """
    if target >= len(rows):
        return rows
    ordered = sorted(rows, key=lambda r: (r[0], r[1]))
    step = len(ordered) / target
    return [ordered[int(i * step)] for i in range(target)]


def span_of(rows) -> str:
    if not rows:
        return "empty"
    months = {r[0] for r in rows}
    return f"{min(months)}..{max(months)}, {len(months)} months"


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
                threshold: float, year: int, match: str = "title") -> int:
    """Match abstracts to later papers, one document at a time.

    The vocabulary tests answer a question nobody actually asked. The
    premise is not "words are said earlier at meetings" — it is "this
    result was shown at the meeting before it was published", and a term
    that was already common in the meeting year is invisible to any
    frequency method however early the work appeared. So: match the
    abstract to the paper.

    Conference abstracts that become papers usually keep most of their
    title. Jaccard overlap on content words, candidates generated from an
    inverted index on the rarer tokens so this does not become
    tens-of-thousands x tens-of-thousands comparisons.

    The false-match rate is estimated by running the identical matcher
    against journal titles published BEFORE the first abstract of the
    cohort was deposited, where a match cannot be a prediction and can
    only be coincidence. That null is only fair if the two arms are the
    same size: the matcher keeps the best candidate above the threshold,
    so a pool with twice the titles is roughly twice the chance of
    finding a spurious one, and the "excess over chance" figure would
    then be measuring the shape of the index rather than the meeting.
    Both arms are therefore thinned to whichever is smaller before the
    comparison is made, and both pool sizes are printed.

    `match` selects what is compared. Until 2026-08-28 the only option was
    `title`, because the journal index held no abstracts, and the ~1%
    conversion rate this test reports has always been a statement about
    title similarity rather than about work. `abstract` uses the abstract
    text on both sides where it exists.

    Expect the threshold to mean something different under `abstract`.
    Two ~200-word oncology abstracts share far more content words than two
    titles do, so the baseline overlap rises for real and spurious pairs
    alike — which is exactly why the pre-meeting arm matters more here,
    not less. Read the ratio, never the raw rate.
    """
    jlo, jhi = index_span(jcon)
    meet_first, meet_last, kept, tail = cohort_window(ccon, year)
    if match == "abstract":
        # Conference side already carries full text for AACR/ASCO. Journal
        # side needs abstracts.sqlite attached; papers with no abstract are
        # the news and front matter measured at 22.7% of the index, and are
        # dropped rather than matched on their titles, which would silently
        # mix two instruments in one arm.
        store = pathlib.Path(__file__).resolve().parent.parent / "data" / "abstracts.sqlite"
        if not store.exists():
            sys.exit("--match abstract needs data/abstracts.sqlite "
                     "(scripts/harvest_abstracts.py)")
        jcon.execute("ATTACH ? AS ab", (str(store),))
        conf = list(ccon.execute(
            "SELECT venue, month, title || ' ' || COALESCE(abstract,'') FROM abstracts "
            "WHERE year=? AND month<=? AND LENGTH(abstract) > 200", (year, meet_last)))
        jsql = ("SELECT p.month, p.pmid, p.title || ' ' || a.abstract "
                "FROM papers p JOIN ab.abstracts a ON a.pmid = p.pmid "
                "WHERE LENGTH(COALESCE(a.abstract,'')) > 200 AND p.month ")
        after = list(jcon.execute(jsql + "> ?", (meet_last,)))
        before = list(jcon.execute(jsql + "< ?", (meet_first,)))
    else:
        conf = list(ccon.execute(
            "SELECT venue, month, title FROM abstracts "
            "WHERE year=? AND month<=? AND LENGTH(title) > 30", (year, meet_last)))
        after = list(jcon.execute(
            "SELECT month, pmid, title FROM papers WHERE month > ?", (meet_last,)))
        before = list(jcon.execute(
            "SELECT month, pmid, title FROM papers WHERE month < ?", (meet_first,)))

    def content(title):
        return {w for w in WORD.findall(title.lower())
                if w not in STOP and len(w) > 3}

    def build(docs):
        sets = [content(t) for _, _, t in docs]
        df: collections.Counter[str] = collections.Counter()
        for s in sets:
            df.update(s)
        ceiling = max(1, round(DF_CEILING_FRAC * len(docs)))
        inv: dict[str, list[int]] = {}
        for i, s in enumerate(sets):
            for w in s:
                if df[w] <= ceiling:  # skip words too common to narrow anything
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

    real = match(after, *build(after))

    n = len(conf)
    print(f"TEST C — {year} abstracts matched to the papers they became")
    print(f"  journal index spans {jlo}..{jhi}")
    print(f"  {year} cohort deposited {meet_first}..{meet_last}"
          + (f"  ({tail:,} later stragglers dropped)" if tail else ""))
    print(f"  conference abstracts with a usable title: {n:,} of {kept:,}")
    print()
    print("  Matcher pools, in journal titles:")
    print(f"    after  the meetings (> {meet_last}):  {len(after):7,}   "
          f"[{span_of(after)}]")
    print(f"    before the meetings (< {meet_first}):  {len(before):7,}   "
          f"[{span_of(before)}]")
    print(f"  matched to a journal paper published later (Jaccard >= {threshold}): "
          f"{len(real):,}  ({len(real) / n:.1%})")
    print()

    # The null and the yield are two different questions and they need two
    # different pools. The line above is the yield: how much of the cohort this
    # method recovers from everything the index holds after the meetings. The
    # block below is the null, and there the two arms have to be the same size
    # or the difference between them is partly just the difference in how many
    # titles each had to get lucky with.
    fair_n = min(len(after), len(before))
    print("  Excess over chance, both arms thinned to the same number of titles:")
    if not fair_n:
        print(f"    NOT AVAILABLE. The index starts at {jlo}, which is not before")
        print(f"    {meet_first}, so there are no journal titles that predate the")
        print("    cohort and no coincidence rate can be measured. Every figure")
        print("    above is a raw yield with no baseline subtracted from it —")
        print("    extend the index below the meeting months, or run a cohort")
        print("    whose meetings fall inside it.")
        print()
    else:
        fair_after = thinned(after, fair_n)
        fair_before = thinned(before, fair_n)
        real_fair = (real if fair_n == len(after)
                     else match(fair_after, *build(fair_after)))
        fake_fair = match(fair_before, *build(fair_before))
        print(f"    pool size, each arm: {fair_n:,} titles")
        print(f"    after  the meetings [{span_of(fair_after)}]:  "
              f"{len(real_fair):,}  ({len(real_fair) / n:.2%})")
        print(f"    before the meetings [{span_of(fair_before)}]:  "
              f"{len(fake_fair):,}  ({len(fake_fair) / n:.2%})")
        print("    The second line is the coincidence rate. A match there cannot")
        print("    be a prediction, so it is what this method scores on pure")
        print("    chance against a pool of exactly this size.")
        if fake_fair:
            print(f"    excess: x{len(real_fair) / len(fake_fair):.1f} over chance")
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
    ap.add_argument("--match", choices=["title", "abstract"], default="title",
                    help="what to compare; abstract needs data/abstracts.sqlite")
    ap.add_argument("--cohort", type=int, default=DEFAULT_COHORT,
                    help="conference year under test (data/conference.sqlite "
                         "holds AACR/ASCO 2023 and 2024)")
    args = ap.parse_args()

    if not CONF.exists():
        sys.exit("no data/conference.sqlite — run scripts/harvest_conference.py")

    if args.papers:
        return papers_test(sqlite3.connect(CONF), sqlite3.connect(INDEX),
                           args.threshold, args.cohort, args.match)

    jcon = sqlite3.connect(INDEX)
    jlo, jhi = index_span(jcon)
    # The baseline is the meeting year itself and the answer is the last
    # calendar year the index reaches, both read off the data. Written as
    # literals these silently stopped meaning what they said the first time
    # either the index or the cohort moved.
    base = (f"{args.cohort}-01", f"{args.cohort}-12")
    later_year = int(jhi[:4])
    later = (f"{later_year}-01", f"{later_year}-12")
    if later_year - args.cohort < 2:
        print(f"WARNING: the index ends in {later_year}, only "
              f"{later_year - args.cohort} year(s) after the {args.cohort} "
              f"meetings. TEST B needs more room than that to see growth.")

    base_docs = list(jcon.execute(
        "SELECT month, title FROM papers WHERE month BETWEEN ? AND ?", base))
    # Deterministic half of the same year, used as the null predictor.
    # Splitting on the PMID's last digit is stable across rebuilds; the
    # script must not use randomness it cannot reproduce.
    half_docs = list(jcon.execute(
        "SELECT month, title FROM papers WHERE month BETWEEN ? AND ? "
        "AND CAST(SUBSTR(pmid,-1) AS INTEGER) < 5", base))
    later_docs = list(jcon.execute(
        "SELECT month, title FROM papers WHERE month BETWEEN ? AND ?", later))
    all_docs = list(jcon.execute("SELECT month, title FROM papers"))

    ccon = sqlite3.connect(CONF)
    meet_first, meet_last, _, _ = cohort_window(ccon, args.cohort)
    field = "title || ' ' || abstract" if args.abstracts else "title"
    # Only the cohort under test. Left unfiltered this swept in every other
    # venue in the file — the 2026 congresses included — and then compared
    # them against a baseline year they postdate.
    conf_docs = list(ccon.execute(
        f"SELECT month, {field} FROM abstracts WHERE year=?", (args.cohort,)))

    if not base_docs:
        sys.exit(f"index ({jlo}..{jhi}) has no papers in {base[0]}..{base[1]} — "
                 f"rebuild it, or pick a cohort inside the index")

    print(f"journal index span            {jlo}..{jhi}")
    print(f"journal titles {base[0]}..{base[1]}   {len(base_docs):,}")
    print(f"journal titles {later[0]}..{later[1]}   {len(later_docs):,}")
    print(f"conference records {args.cohort} ({meet_first}..{meet_last})  "
          f"{len(conf_docs):,}"
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
    arrived = {t: jfirst[t] for t in novel if t in jfirst and jfirst[t] > base[1]}
    print(f"TEST A — conference vocabulary absent from every {args.cohort} journal title")
    print(f"  terms said at >= {args.min_conf} meeting records, unseen in "
          f"{args.cohort} journals: {len(novel):,}")
    print(f"  later appear in a journal title:  {len(arrived):,}"
          f"  ({len(arrived) / max(len(novel), 1):.0%})")
    print(f"  never appear at all:              {len(novel) - len(arrived):,}"
          f"  ({1 - len(arrived) / max(len(novel), 1):.0%})")
    if arrived:
        # Measured from the month the cohort finished depositing, not from a
        # fixed mid-year month, so the figure means the same thing for a
        # cohort whose meetings sat in February as for one that ran to August.
        close_y, close_m = int(meet_last[:4]), int(meet_last[5:7])
        delays = sorted((int(m[:4]) - close_y) * 12 + int(m[5:7]) - close_m
                        for m in arrived.values())
        print(f"  median delay from the meetings closing ({meet_last}): "
              f"{statistics.median(delays):.0f} months")
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
    # Terms absent from the meeting year's journal titles are mostly
    # register, not content: `pts with metastatic`, `real world`, `mcrpc`.
    # Abstracts are written in a compressed clinical shorthand that journal
    # titles never use, so those terms score maximum conference excess while
    # saying nothing about where the field went. Requiring one journal title
    # anywhere in the base year removes the register layer and leaves the
    # topical one.
    grounded = [r for r in rows if jbase.get(r[2], 0) >= 1]
    rho_grounded = spearman([(r[0], r[1]) for r in grounded])
    print(f"  rho(conference excess, {args.cohort}->{later_year} growth)  "
          f"= {rho:+.3f}")
    print(f"  rho(null: half of {args.cohort} itself, same growth) = {rho_null:+.3f}")
    print(f"  rho, register-controlled (term in >= 1 journal title in "
          f"{args.cohort}, n={len(grounded):,}) = {rho_grounded:+.3f}")
    print(f"    Both predictors carry the {args.cohort} rate in their denominator,")
    print(f"    so a term that was low in {args.cohort} by chance scores high on")
    print("    excess AND on growth.")
    print("    That artefact alone produces the null figure. Only the gap between")
    print("    the two lines is evidence that the meeting knows anything.")
    print()

    # Stratified estimate: within a band of identical base-year journal
    # counts, the shared denominator is held fixed and cannot manufacture
    # anything.
    print(f"  Held-fixed check — within bands of equal {args.cohort} journal")
    print(f"  frequency, does the conference rate still rank the {later_year}"
          f" journal rate?")
    print(f"    {f'{args.cohort} journal titles':>22}  {'terms':>6}  {'rho':>7}")
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

    print(f"  Most over-represented at the meetings, and what the journals did"
          f" by {later_year}:")
    print(f"    {'term':38} {'conf':>5} {f'j{args.cohort}':>6} "
          f"{f'j{later_year}':>6}  growth")
    for row in sorted(top, key=lambda r: -r[0])[:25]:
        t, growth = row[2], row[1]
        print(f"    {t:38} {conf.get(t,0):5} {jbase.get(t,0):6} "
              f"{jlater.get(t,0):6}  x{math.exp(growth):5.2f}")

    print()
    print(f"  Biggest journal growth {args.cohort}->{later_year}, and whether"
          f" the meetings saw it:")
    for row in sorted(rows, key=lambda r: -r[1])[:25]:
        t, growth = row[2], row[1]
        seen = f"{conf.get(t,0):5}" if conf.get(t, 0) else "    -"
        print(f"    {t:38} {seen} {jbase.get(t,0):6} "
              f"{jlater.get(t,0):6}  x{math.exp(growth):5.2f}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
