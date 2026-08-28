#!/usr/bin/env python3
"""Re-run approval_lead.py's Stage B with real first-in-human dates.

scripts/approval_lead.py is imported, not edited. Everything it defines —
the alias rule, the tokenizer, the inverted index, the scanner, the
approval dedup — is reused verbatim from that module, so the two scripts
cannot drift apart on the definition of "the same drug". The only thing
replaced is the Stage B censoring gate, and it is replaced with the one
piece of evidence approval_lead.py said it was missing:

    data/first_in_human.tsv — the earliest interventional trial in which
    each of the 124 agents was administered to humans, harvested from
    ClinicalTrials.gov across its whole history and resolved through
    development code names as well as INNs.

WHAT CHANGES, AND WHAT DOES NOT

    approval_lead.py had to infer prior existence from ten proxies (a-j)
    because it could not see before 2023-01. Signals (e) through (j) exist
    only to guess whether a trial visible inside the window is really the
    agent's origin. With an actual first-in-human date, all six collapse
    into one test that needs no guessing:

        fih_date < window_open  ->  the corpus opened after this drug
                                    entered the clinic. CENSORED.

    Signal (a), the aperture argument, was also a proxy — "approved so
    soon after the window opened that no plausible lead fits". It is kept
    as a SEPARATE, reported variant rather than folded in, because with a
    real first-in-human date it is no longer needed to establish prior
    existence, and the point of this re-run is to find out whether the
    null survives without any tunable number in it.

    Signals (b), (c) and (d) — an earlier approval row, an EMA
    authorisation before the window, the FDA cell/gene-therapy roster —
    are independent of the registry and are kept, as cross-checks. They
    are reported both folded in and held out.

GATES, in the three variants this prints:

    FIH-ONLY     censor iff first-in-human < window_open, or no dated
                 trial exists for the agent. One rule, no threshold.
    FIH + PRIOR  additionally censor on (b) earlier approval row,
                 (c) EMA pre-window, (d) CGT roster.
    FIH + PRIOR + APERTURE
                 additionally censor approvals landing within `--grace`
                 months of the window opening.

Lead time, where a lead time is computed, keeps approval_lead.py's own
definition: approval date minus the earliest date at which any of the
three corpus channels wrote the drug's name.

Usage:
    python3 scripts/approval_lead_fih.py
    python3 scripts/approval_lead_fih.py --markdown out.md
    python3 scripts/approval_lead_fih.py --exclude-external
"""

from __future__ import annotations

import argparse
import collections
import csv
import importlib.util
import pathlib
import sqlite3
import statistics
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
REG = ROOT / "data" / "regulatory.sqlite"
INDEX = ROOT / "data" / "index.sqlite"
CONF = ROOT / "data" / "conference.sqlite"
FIH = ROOT / "data" / "first_in_human.tsv"


def load_approval_lead():
    spec = importlib.util.spec_from_file_location(
        "approval_lead", ROOT / "scripts" / "approval_lead.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


al = load_approval_lead()
CHANNELS = al.CHANNELS


class Out:
    def __init__(self):
        self.lines: list[str] = []

    def __call__(self, line: str = ""):
        print(line)
        self.lines.append(line)


def pct(a, b):
    return f"{a / b:.0%}" if b else "n/a"


def quantiles(v):
    v = sorted(v)
    if not v:
        return None
    return (v[0], v[len(v) // 4], statistics.median(v), v[3 * len(v) // 4], v[-1])


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--window-open", default=None)
    ap.add_argument("--grace", type=int, default=24)
    ap.add_argument("--date-column", default="fih_date",
                    help="which first-in-human definition to gate on; "
                         "fih_corpus_internal_date is the self-contained one")
    ap.add_argument("--markdown", default=None)
    ap.add_argument("--detail", action="store_true")
    args = ap.parse_args()

    if not FIH.exists():
        sys.exit("no data/first_in_human.tsv — run scripts/first_in_human.py")

    rcon = sqlite3.connect(f"file:{REG}?mode=ro", uri=True)
    jcon = sqlite3.connect(f"file:{INDEX}?mode=ro", uri=True) if INDEX.exists() else None
    ccon = sqlite3.connect(f"file:{CONF}?mode=ro", uri=True) if CONF.exists() else None

    approvals = al.load_approvals(rcon)
    n = len(approvals)
    anchors, pats = al.build_index(approvals)

    # ---- agent dedup: approval_lead.py's own rule, reproduced exactly ----
    repeat_of: list[int | None] = [None] * n
    for i in range(n):
        for j in range(i):
            if approvals[j].date < approvals[i].date and \
                    approvals[i].aliases & approvals[j].aliases:
                repeat_of[i] = j
                break
    root_of = []
    for i in range(n):
        r = i
        while repeat_of[r] is not None:
            r = repeat_of[r]
        root_of.append(r)

    # ---- first-in-human table -------------------------------------------
    with FIH.open() as fh:
        fih_rows = list(csv.DictReader(fh, delimiter="\t"))
    # keyed by the agent's display name, which is unique across the 124 rows
    fih = {r["primary"]: r for r in fih_rows}
    assert len(fih) == len(fih_rows), "agent names are not unique"

    def agent_row(i):
        return fih.get(approvals[root_of[i]].primary)

    # ---- spans ------------------------------------------------------------
    spans = {}
    spans["approvals"] = rcon.execute(
        "SELECT MIN(month), MAX(month), COUNT(*) FROM fda_approvals").fetchone()
    spans["trials"] = rcon.execute(
        "SELECT MIN(month), MAX(month), COUNT(*) FROM ct_trials").fetchone()
    if jcon:
        spans["journals"] = jcon.execute(
            "SELECT MIN(month), MAX(month), COUNT(*) FROM papers").fetchone()
    if ccon:
        spans["conference"] = ccon.execute(
            "SELECT MIN(month), MAX(month), COUNT(*) FROM abstracts").fetchone()
    window_open = args.window_open or min(s[0] for s in spans.values() if s[0])

    out = Out()
    out("=" * 78)
    out("APPROVAL LEAD, STAGE B RE-RUN WITH REAL FIRST-IN-HUMAN DATES")
    out("=" * 78)
    out()
    out("SPAN ACTUALLY USED (read from the databases at run time)")
    for name, (lo, hi, cnt) in spans.items():
        out(f"  {name:<12} {lo} .. {hi}   {cnt:,} records")
    out(f"  censoring boundary (window opens): {window_open}")
    out(f"  first-in-human table: {len(fih_rows)} agents, "
        f"{sum(1 for r in fih_rows if r['fih_date'])} with a dated trial")
    out()

    # ---- corpus traces (approval_lead.py's Stage A, verbatim) ------------
    hits = {}
    hits["journal"] = al.scan(
        jcon.execute("SELECT COALESCE(pubdate, month), pmid, title FROM papers"),
        anchors, pats, n) if jcon else [[] for _ in range(n)]
    hits["conference"] = al.scan(
        ccon.execute("SELECT date, doi, title || ' ' || COALESCE(abstract,'') "
                     "FROM abstracts"), anchors, pats, n) if ccon else [[] for _ in range(n)]
    cur, _ = al.trial_rows(rcon)
    hits["trial"] = al.scan(cur, anchors, pats, n)
    for ch in CHANNELS:
        hits[ch] = [[(d.replace("/", "-"), i, a) for d, i, a in rows]
                    for rows in hits[ch]]
    prior = {ch: [[h for h in rows if h[0][:7] <= appr.month]
                  for rows, appr in zip(hits[ch], approvals)] for ch in CHANNELS}

    first_trace, first_channel = [], []
    for i in range(n):
        cands = [(sorted(prior[ch][i])[0][0], ch) for ch in CHANNELS if prior[ch][i]]
        if cands:
            d, ch = min(cands)
            first_trace.append(d)
            first_channel.append(ch)
        else:
            first_trace.append(None)
            first_channel.append("")

    # ---- independent prior-existence signals (b, c, d) -------------------
    ema_rows = list(rcon.execute(
        "SELECT COALESCE(NULLIF(date,''), NULLIF(ec_decision_date,''), '9999'), "
        "product_number, name || ' ' || COALESCE(inn,'') || ' ' "
        "|| COALESCE(active_substance,'') FROM ema_medicines"))
    ema_old = [min((h[0] for h in rows), default=None)
               for rows in al.scan(ema_rows, anchors, pats, n)]
    cgt_hits = al.scan(list(rcon.execute(
        "SELECT '', product, product || ' ' || COALESCE(trade_name,'') || ' ' "
        "|| COALESCE(generic_name,'') FROM fda_cgt_roster")), anchors, pats, n)

    # ---- the new evidence, described before it is used -------------------
    dated = [r for r in fih_rows if r["fih_date"]]
    out("-" * 78)
    out("THE NEW EVIDENCE — WHEN THESE 124 AGENTS ENTERED HUMANS")
    out("-" * 78)
    out()
    yrs = collections.Counter(r["fih_date"][:4] for r in dated)
    out(f"  agents with a dated interventional trial   {len(dated)} of {len(fih_rows)}")
    out(f"  earliest first-in-human                    {min(r['fih_date'] for r in dated)}")
    out(f"  latest first-in-human                      {max(r['fih_date'] for r in dated)}")
    out()
    out("  first-in-human year:")
    line = ""
    for y in sorted(yrs):
        line += f"  {y}:{yrs[y]}"
        if len(line) > 62:
            out("   " + line)
            line = ""
    if line:
        out("   " + line)
    out()
    before = sum(1 for r in dated if r["fih_date"][:7] < window_open)
    out(f"  first-in-human BEFORE {window_open}                  "
        f"{before} of {len(dated)}  ({pct(before, len(dated))})")
    out(f"  first-in-human on or after {window_open}             "
        f"{len(dated) - before}")
    out()
    moved = [r for r in dated if r["months_gained_by_code"]
             and int(r["months_gained_by_code"]) > 0]
    out(f"  agents whose date moved EARLIER once development code names")
    out(f"  were resolved: {len(moved)}. Median gain "
        f"{statistics.median([int(r['months_gained_by_code']) for r in moved]):.0f}"
        f" months, max {max(int(r['months_gained_by_code']) for r in moved)}."
        if moved else "  no agent's date moved.")
    for r in sorted(moved, key=lambda r: -int(r["months_gained_by_code"]))[:15]:
        out(f"    {r['primary'][:30]:<30} {r['inn_only_fih_date']} -> "
            f"{r['fih_date']}  (+{r['months_gained_by_code']}mo via "
            f"{r['codes_validated'][:24]})")
    out()
    conf = collections.Counter(r["confidence"] for r in fih_rows)
    out("  confidence in the first-in-human date: "
        + ", ".join(f"{k} {v}" for k, v in conf.most_common()))
    out()

    # ---- exclusion of externally-resolved rows ---------------------------
    ext_only = {r["primary"] for r in fih_rows if r["external_only_codes"]}
    moved_ext = {r["primary"] for r in fih_rows
                 if r["fih_date"] != r["fih_corpus_internal_date"]}
    out(f"  agents carrying a code name resolvable ONLY from the live")
    out(f"  registry (not from anything in this repo):  {len(ext_only)}")
    out(f"  agents whose date actually depends on one of those:  {len(moved_ext)}")
    out("    " + ", ".join(sorted(moved_ext)))
    out()
    out("  EXCLUDING THOSE — the column `fih_corpus_internal_date` recomputes")
    out("  every date with registry-only code names struck out, keeping only")
    out("  the INN and codes this repo's own text spells out:")
    for col, name in (("fih_date", "full resolution"),
                      ("fih_corpus_internal_date", "corpus-internal only"),
                      ("inn_only_fih_date", "INN query alone (no codes)"),
                      ("fih_title_only_date", "title-ownership variant"),
                      ("fih_no_platform_filter_date", "no platform exclusion")):
        vals = [r[col] for r in fih_rows if r[col]]
        late = [r["primary"] for r in fih_rows if r[col] and r[col][:7] >= window_open]
        out(f"    {name:<28} n={len(vals)}  latest {max(vals)}  "
            f"FIH >= {window_open}: {len(late)}")
        if late:
            out(f"      {', '.join(sorted(late))}")
    out()
    out("  The INN-alone row is the trap made visible. Query the registry with")
    out("  the INN and nothing else and four agents appear to have entered")
    out("  humans after this corpus opened — four apparently measurable")
    out("  approvals, every one of them an artefact of a trial registered")
    out("  under a sponsor code before the INN existed. Resolving the codes")
    out("  removes all four. The naive harvest does not merely add noise; it")
    out("  manufactures precisely the positive result one would want.")
    out()

    date_col = args.date_column

    # ---- the gate --------------------------------------------------------
    def gate(i, use_prior: bool, use_aperture: bool) -> str | None:
        r = agent_row(i)
        if r is None:
            return "B) no first-in-human row for this agent"
        if not r[date_col]:
            return "B) no dated interventional trial anywhere in the registry"
        if r[date_col][:7] < window_open:
            return f"A) first-in-human predates {window_open}"
        if use_prior:
            if repeat_of[i] is not None:
                return "C) an earlier fda_approvals row names this agent"
            if ema_old[i] and ema_old[i][:7] < window_open:
                return "D) EMA authorised this molecule before the window"
            if cgt_hits[i]:
                return "E) already on the FDA cell/gene-therapy roster"
        if use_aperture and \
                al.months_between(window_open, approvals[i].date) < args.grace:
            return (f"F) approved within {args.grace} months of the window "
                    "opening — aperture too small")
        return None

    variants = [("FIH-ONLY", False, False),
                ("FIH + PRIOR (b,c,d)", True, False),
                (f"FIH + PRIOR + APERTURE({args.grace}mo)", True, True)]

    out("-" * 78)
    out("STAGE B RE-RUN — HOW MANY APPROVALS BECOME MEASURABLE")
    out("-" * 78)
    out()
    results = {}
    for label, up, ua in variants:
        unc, cen, reasons = [], [], collections.Counter()
        for i in range(n):
            if first_trace[i] is None:
                reasons["z) never named by any channel before approval"] += 1
                continue
            lead = al.months_between(first_trace[i], approvals[i].date)
            why = gate(i, up, ua)
            (cen if why else unc).append((i, lead))
            if why:
                reasons[why.split(")")[0] + ") " + why.split(") ", 1)[1][:52]] += 1
        results[label] = (unc, cen, reasons)
        out(f"  {label:<34} measurable n = {len(unc):<4} censored n = {len(cen)}")
    out()

    label, _, _ = variants[0]
    unc, cen, reasons = results[label]
    out(f"  Censoring reasons under {label} (the gate with no tunable number):")
    for reason, c in sorted(reasons.items(), key=lambda kv: -kv[1]):
        out(f"    {c:>4}  {reason}")
    out()

    for label, _, _ in variants:
        unc, cen, reasons = results[label]
        out(f"  MEASURABLE LEAD TIMES under {label}   n = {len(unc)}")
        if not unc:
            out("    none.")
            out()
            continue
        leads = sorted(l for _, l in unc)
        out(f"    median {statistics.median(leads):.1f} months, "
            f"range {min(leads)}-{max(leads)}")
        out(f"    {'approved':<11} {'lead':>6}  {'fih':<9} {'conf':<7} "
            f"{'via':<11} drug")
        for i, lead in sorted(unc, key=lambda r: -r[1]):
            r = agent_row(i)
            out(f"    {approvals[i].date:<11} {lead:>4}mo  "
                f"{(r[date_col] if r else '')[:7]:<9} "
                f"{(r['confidence'] if r else ''):<7} {first_channel[i]:<11} "
                f"{approvals[i].primary[:30]}")
        out()

    # ---- what the FIH dates say about the corpus's reach -----------------
    out("-" * 78)
    out("HOW FAR BACK WOULD THE CORPUS HAVE TO REACH?")
    out("-" * 78)
    out()
    out("  For an approval to be measurable the corpus must open before the")
    out("  agent's first-in-human. This is the distribution of that gap, in")
    out("  months, over the distinct agents with a dated trial:")
    gaps = sorted(al.months_between(r["fih_date"][:7], window_open)
                  for r in dated)
    q = quantiles(gaps)
    out(f"    n = {len(gaps)}   min {q[0]}  q1 {q[1]}  median {q[2]:.0f}  "
        f"q3 {q[3]}  max {q[4]}   (months of history needed)")
    out()
    out("    window would have to open   agents thereby made reachable")
    for back in (0, 12, 24, 36, 48, 60, 84, 120, 180, 240):
        yy = int(window_open[:4]) - back // 12
        mm = int(window_open[5:7]) - back % 12
        if mm <= 0:
            yy, mm = yy - 1, mm + 12
        k = sum(1 for g in gaps if g <= back)
        out(f"      {yy:04d}-{mm:02d}  ({back:>3} months earlier)   "
            f"{k:>3} of {len(gaps)}  ({pct(k, len(gaps))})")
    out()

    out("  Development time itself — approval date minus first-in-human,")
    out("  for the FIRST approval of each distinct agent. This quantity does")
    out("  not depend on the corpus at all and is the one thing the harvest")
    out("  measures cleanly:")
    dev = []
    for r in dated:
        if r["first_approval"]:
            dev.append(al.months_between(r["fih_date"][:7], r["first_approval"][:7]))
    dev = sorted(d for d in dev if d >= 0)
    q = quantiles(dev)
    out(f"    n = {len(dev)}   min {q[0]}  q1 {q[1]}  median {q[2]:.0f}  "
        f"q3 {q[3]}  max {q[4]}  months")
    out(f"    median {q[2] / 12:.1f} years from first-in-human to the first FDA")
    out(f"    approval seen in this window; a quarter of these agents took")
    out(f"    more than {q[3] / 12:.1f} years.")
    out()
    fast = [r for r in dated
            if r["first_approval"] and
            al.months_between(r["fih_date"][:7], r["first_approval"][:7]) <= 60]
    out(f"    agents approved within 5 years of first-in-human: {len(fast)}")
    for r in sorted(fast, key=lambda r: al.months_between(
            r["fih_date"][:7], r["first_approval"][:7]))[:12]:
        out(f"      {al.months_between(r['fih_date'][:7], r['first_approval'][:7]):>3}mo  "
            f"{r['fih_date']} -> {r['first_approval']}  {r['primary'][:34]}")
    out()

    if args.detail:
        out("-" * 78)
        out("PER-AGENT DETAIL")
        out("-" * 78)
        out(f"  {'fih':<11} {'1st appr':<11} {'dev':>5} {'conf':<7} {'phase':<14} "
            f"{'nct':<12} agent")
        for r in sorted(fih_rows, key=lambda r: r["fih_date"] or "9999"):
            d = (al.months_between(r["fih_date"][:7], r["first_approval"][:7])
                 if r["fih_date"] else "")
            out(f"  {r['fih_date'] or '--':<11} {r['first_approval']:<11} "
                f"{str(d):>5} {r['confidence']:<7} {r['fih_phase'][:14]:<14} "
                f"{r['fih_nct']:<12} {r['primary'][:32]}")
        out()

    if args.markdown:
        p = pathlib.Path(args.markdown)
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text("```\n" + "\n".join(out.lines) + "\n```\n")
        print(f"\n[written to {p}]")
    return 0


if __name__ == "__main__":
    sys.exit(main())
