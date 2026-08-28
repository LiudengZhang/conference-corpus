#!/usr/bin/env python3
"""Generate the machine-produced sections of a monthly briefing.

Sections 1, 2 and 5 of every briefing come from here — reading volume, the
thread curve, and open items. Only sections 3 and 4 (the evidence and the
refutations) are written by hand, because only those require judgement.

The point is that the fixed cost of a monthly briefing should be near zero.
If each month needs its framework rethought, the practice does not survive
three months.

Usage:
    python3 scripts/build_briefing.py 2026-07              # one month
    python3 scripts/build_briefing.py --curve              # all months, thread curve
    python3 scripts/build_briefing.py --check              # regenerate and diff
"""

from __future__ import annotations

import argparse
import collections
import datetime as dt
import json
import pathlib
import sqlite3
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
INDEX = ROOT / "data" / "index.sqlite"
CARDS = ROOT / "data" / "evidence.yml"
OUT = ROOT / "docs" / "briefings"

# The signal stores are regenerable and gitignored, so a fresh clone has the
# journal index and nothing else. Every section built on them has to degrade
# to a stated absence rather than a traceback — a briefing that cannot be
# regenerated on a clean checkout is not reproducible.
CONF = ROOT / "data" / "conference.sqlite"
REGULATORY = ROOT / "data" / "regulatory.sqlite"
NEWS = ROOT / "data" / "news.sqlite"
SOURCES = ROOT / "data" / "sources.yml"


def vaults_meeting_in(month: str) -> list[tuple[str, str]]:
    """Built conference vaults whose meeting falls in this month.

    Nine meetings — AACR 2026 and AACR IO 2026 among them — exist only as
    hand-written vaults and are absent from the abstract store, so a
    section built purely on the store reported ESMO and USCAP while
    silently omitting the corpus's flagship vault. They are linked rather
    than ingested: the vault *is* the judgement layer, and copying its
    prose into a store of raw abstracts would double-count it.
    """
    if not SOURCES.exists():
        return []
    import yaml

    out = []
    for s in yaml.safe_load(SOURCES.read_text())["sources"]:
        if s.get("type") != "conference" or not s.get("vault"):
            continue
        if s.get("status") not in ("built", "partial"):
            continue
        months = {str(s[k])[:7] for k in ("start", "end") if s.get(k)}
        if month in months:
            out.append((s["name"], s["vault"]))
    return sorted(out)

DOMAINS = ["general", "cancer", "immune", "bioinfo", "sysbio"]

# Status is derived, never asserted. Change the rule here and every month
# recomputes — that is the point of writing it down.
#
# MIN_N exists because the ratio rules are meaningless at small counts. Without
# it, a thread whose first two cards happen to be refutations reads `crisis`,
# and in the opening months of the corpus almost everything did. A thread has
# to earn a status; until then it says so.
MIN_N = 5


def status_of(supports: int, refutes: int) -> str:
    if supports + refutes < MIN_N:
        return "too-early"
    if refutes and refutes >= 2 * supports:
        return "crisis"
    if refutes > supports:
        return "contested"
    if supports >= 2 * refutes:
        return "forming"
    return "splitting"


def load_cards() -> list[dict]:
    """Evidence cards. Falls back to the working JSON while the YAML is being built."""
    if CARDS.exists():
        import yaml

        cards = yaml.safe_load(CARDS.read_text())["evidence"]
    else:
        alt = pathlib.Path("/tmp/cards.json")
        if not alt.exists():
            sys.exit("no evidence cards found — expected data/evidence.yml")
        cards = json.loads(alt.read_text())

    # The schema took two passes to settle: `thread` could be a string or a
    # list, and the date lives under `date` in one and is absent in the other.
    # Normalise once here rather than defending against it at every call site.
    out = []
    for c in cards:
        t = c.get("threads", c.get("thread"))
        if isinstance(t, str):
            t = [x.strip() for x in t.split(",")]
        c["threads"] = t or []
        d = c.get("date")
        c["date"] = str(d) if d else ""
        if not c["date"]:
            continue  # a card with no date cannot sit on a curve
        out.append(c)
    return out


def months_in_index(con: sqlite3.Connection) -> list[str]:
    return [r[0] for r in con.execute("SELECT DISTINCT month FROM papers ORDER BY month")]


def journal_gaps(con: sqlite3.Connection):
    """(months in the index, journals that read, gap records worst first).

    A gap record is (journal, months missing, papers contributed, the missing
    months).

    This used to be a remembered list in the warning prose below — *Nucleic
    Acids Research* 2025-12, *Bioinformatics* 2024-04 and three more — which
    was true of the window it was written against and quietly false of every
    window after it. Survey the index instead: the gaps move whenever the
    index grows, and a warning that recites last year's gaps teaches a reader
    to distrust exactly the wrong months.
    """
    months = months_in_index(con)
    present: dict[str, set[str]] = collections.defaultdict(set)
    totals: collections.Counter[str] = collections.Counter()
    for journal, m, n in con.execute(
            "SELECT journal, month, COUNT(*) FROM papers GROUP BY journal, month"):
        present[journal].add(m)
        totals[journal] += n
    gaps = []
    for journal, seen in present.items():
        missing = {m for m in months if m not in seen}
        if missing:
            gaps.append((journal, len(missing), totals[journal], missing))
    gaps.sort(key=lambda g: (-g[1], g[0]))
    return months, sorted(present), gaps


def section_volume(con: sqlite3.Connection, month: str) -> str:
    total = con.execute("SELECT COUNT(*) FROM papers WHERE month=?", (month,)).fetchone()[0]
    by_dom = dict(
        con.execute("SELECT domain,COUNT(*) FROM papers WHERE month=? GROUP BY domain", (month,))
    )
    by_j = con.execute(
        "SELECT journal,COUNT(*) c FROM papers WHERE month=? GROUP BY journal ORDER BY c DESC",
        (month,),
    ).fetchall()

    # A month that swings hard against its neighbours usually means the
    # pipeline broke, not that the field went quiet. Surface it here.
    #
    # Measured per domain, not on the total. Nucleic Acids Research publishes a
    # ~200-paper database issue every January, which by itself pushes the corpus
    # total 25-30% above the median and fires a warning that says "check the
    # harvest" about the one month whose volume is completely explained. A
    # warning that cries wolf every January is a warning nobody reads in July.
    drift = {}
    for d in DOMAINS:
        cur = by_dom.get(d, 0)
        others = [
            r[0] for r in con.execute(
                "SELECT COUNT(*) FROM papers WHERE month!=? AND domain=? GROUP BY month",
                (month, d))
        ]
        if not others:
            continue
        median = sorted(others)[len(others) // 2]
        if median:
            drift[d] = (cur - median) / median * 100

    # Say how many journals actually contributed, not how many are on the
    # list. Every briefing said "33 journals" for a year, when several of
    # them deposit nothing in a given month and one — see the gap survey
    # below — is absent from about half of them, because PubMed indexes only
    # the deposited fraction. The roster and the reading are not the same
    # number, and it was the roster that got printed.
    n_journals = len(by_j)
    lines = [
        "## 1. What was read",
        "",
        f"**{total:,} research articles** from {n_journals} of the 33 journals on "
        f"the roster, filtered to `journal article` and excluding reviews, "
        f"editorials, news, comment and case reports.",
        "",
        "| " + " | ".join(d.capitalize() for d in DOMAINS) + " |",
        "|" + "---|" * len(DOMAINS),
        "| " + " | ".join(f"{by_dom.get(d, 0):,}" for d in DOMAINS) + " |",
        "",
    ]
    swung = {d: v for d, v in drift.items() if abs(v) >= 25}
    if swung:
        detail = ", ".join(f"{d} {v:+.0f}%" for d, v in sorted(swung.items()))
        # Name the journals that are actually missing from THIS month, and
        # size the problem from the current index. The previous version
        # recited five journal-months from the window it was written against
        # and went on reciting them after the window moved, which trains a
        # reader to distrust the wrong months.
        months, reading, gaps = journal_gaps(con)
        here = sorted(j for j, _, _, missing in gaps if month in missing)
        worst = [(j, n, tot) for j, n, tot, _ in gaps[:2]]
        lines += [
            f"!!! warning \"Volume swing against the median month: {detail}\"",
            "    Check the source before reading anything into this. Two benign "
            "causes account for most of these. `bioinfo` every January carries the "
            "Nucleic Acids Research database issue and runs high. And several "
            "journals simply deposit nothing in some months: across the "
            f"{len(months)} months read, {len(gaps)} of {len(reading)} journals "
            "are absent from at least one"
            + (f", worst being "
               + " and ".join(f"*{j}* ({n} months missing, {tot:,} papers in total)"
                              for j, n, tot in worst)
               if worst else "")
            + ". "
            + (f"This month is missing {', '.join('*' + j + '*' for j in here)}. "
               if here else "Every journal on the roster contributed this month. ")
            + "Queried directly, PubMed returns zero for those journal-months too "
            "— the holes are in the source, reproduced exactly by re-running the "
            "harvest. So a swing here is not evidence that a field went quiet, and "
            "is not usually evidence that the pipeline broke either.",
            "",
        ]
    top = ", ".join(f"{j} {c}" for j, c in by_j[:6])
    lines += [f"Largest contributors: {top}.", ""]
    return "\n".join(lines)


def section_curve(cards: list[dict], month: str, prev: str | None) -> str:
    threads = sorted({t for c in cards for t in c["threads"]})
    rows = []
    for t in threads:
        s = sum(1 for c in cards if t in c["threads"] and c["stance"] == "supports" and c["date"][:7] == month)
        r = sum(1 for c in cards if t in c["threads"] and c["stance"] == "refutes" and c["date"][:7] == month)
        cum_s = sum(1 for c in cards if t in c["threads"] and c["stance"] == "supports" and c["date"][:7] <= month)
        cum_r = sum(1 for c in cards if t in c["threads"] and c["stance"] == "refutes" and c["date"][:7] <= month)
        now = status_of(cum_s, cum_r)
        was = None
        if prev:
            p_s = sum(1 for c in cards if t in c["threads"] and c["stance"] == "supports" and c["date"][:7] <= prev)
            p_r = sum(1 for c in cards if t in c["threads"] and c["stance"] == "refutes" and c["date"][:7] <= prev)
            was = status_of(p_s, p_r) if (p_s or p_r) else None
        if not (s or r or cum_s or cum_r):
            continue
        flip = ""
        if was and was != now:
            flip = f" **{was} → {now}**"
        elif was is None and (cum_s or cum_r):
            flip = f" *(opens as {now})*"
        rows.append((t, s, r, cum_s, cum_r, now, flip))

    lines = ["## 2. Net change on the thread curve", ""]
    if not any(r[1] or r[2] for r in rows):
        lines += ["No thread moved this month. That is a finding, not a gap — "
                  "record it and move on.", ""]
    lines += ["| Thread | This month | Cumulative | Status |", "|---|---|---|---|"]
    for t, s, r, cs, cr, now, flip in rows:
        delta = "—" if not (s or r) else f"{'+' + str(s) if s else ''}{' / ' if s and r else ''}{'−' + str(r) if r else ''}"
        lines.append(f"| `{t}` | {delta} | +{cs} / −{cr} | {now}{flip} |")
    lines.append("")
    lines.append(
        "Status is derived by rule, not asserted. Fewer than 5 cards → too-early; "
        "then `refutes ≥ 2×supports` → crisis; "
        "`refutes > supports` → contested; `supports ≥ 2×refutes` → forming; else splitting."
    )
    lines.append("")
    return "\n".join(lines)


def section_open(cards: list[dict], month: str) -> str:
    unresolved = [
        c for c in cards
        if c["date"][:7] <= month and (c.get("verify") or c.get("confidence") == "low")
    ]
    lines = ["## 5. Open items", ""]
    if not unresolved:
        lines += ["Nothing carried forward.", ""]
        return "\n".join(lines)
    lines += ["Checked at the top of next month. Items that cannot be resolved keep rolling.", ""]
    for c in unresolved:
        lines.append(f"- **{c['claim']}** — `{c.get('id', c['pmid'])}`, opened {c['date'][:7]}")
    lines.append("")
    return "\n".join(lines)


def optional_store(path: pathlib.Path, table: str) -> sqlite3.Connection | None:
    """Open a regenerable side store, or None if it is not built here."""
    if not path.exists():
        return None
    con = sqlite3.connect(f"file:{path}?mode=ro", uri=True)
    have = con.execute(
        "SELECT 1 FROM sqlite_master WHERE type IN ('table','view') AND name=?",
        (table,)).fetchone()
    return con if have else None


def section_meetings(month: str) -> str:
    """Which meetings put abstracts into the record this month.

    Conferences do not have a monthly cadence and pretending otherwise
    would be the wrong shape for the data. Abstract books land in a few
    weeks of the year, so most months here are empty by construction, and
    an empty section means the calendar was quiet — not that anything
    failed. Saying so once, in the section itself, is cheaper than
    re-deriving it every time a reader hits a blank month.
    """
    lines = ["## 6. Meetings", ""]

    vaults = vaults_meeting_in(month)
    if vaults:
        lines += [
            f"**{len(vaults)} meeting{'' if len(vaults) == 1 else 's'} with a "
            f"written vault this month.** These are read and summarised rather "
            f"than harvested as abstracts, so they do not appear in the counts "
            f"below.",
            "",
        ]
        for name, vault in vaults:
            lines.append(f"- [{name}](../{vault.removesuffix('.md')}.md)")
        lines.append("")

    con = optional_store(CONF, "abstracts")
    if con is None:
        lines += ["Conference store not built in this checkout — run "
                  "`scripts/harvest_conference.py`.", ""]
        return "\n".join(lines)

    rows = con.execute(
        "SELECT a.venue, COALESCE(v.name, a.venue), COUNT(*), "
        "       SUM(LENGTH(a.abstract) > 200), MIN(a.confirmed) "
        "FROM abstracts a LEFT JOIN venues v ON v.id = a.venue "
        "WHERE a.month = ? GROUP BY a.venue ORDER BY COUNT(*) DESC",
        (month,)).fetchall()

    if not rows:
        span = con.execute(
            "SELECT MIN(month), MAX(month) FROM abstracts").fetchone()
        lines += [
            ("No abstract book was deposited this month either — the vault "
             "above is built from transcripts and programmes rather than from "
             "a published abstract set."
             if vaults else
             "No abstract book published this month.")
            + f" The abstract layer runs {span[0]} to {span[1]} and is seasonal "
            f"by nature — meetings are annual, so most months are empty here "
            f"and that is the expected shape, not a gap in the harvest.",
            "",
        ]
        return "\n".join(lines)

    total = sum(r[2] for r in rows)
    lines += [
        f"**{total:,} abstracts** from {len(rows)} "
        f"{'meeting' if len(rows) == 1 else 'meetings'}.",
        "",
        "| Meeting | Abstracts | With full text |",
        "|---|---|---|",
    ]
    for _, name, n, full, confirmed in rows:
        mark = "" if confirmed else " †"
        lines.append(f"| {name}{mark} | {n:,} | {full or 0:,} |")
    lines.append("")
    if any(not r[4] for r in rows):
        lines += [
            "† The congress behind this abstract book could not be identified. "
            "It is a real, numbered abstract book, but Crossref deposits no "
            "record naming the meeting and the publisher's table of contents "
            "is not reachable. It is carried unattributed rather than assigned "
            "to a plausible congress.",
            "",
        ]
    if not any(r[3] for r in rows):
        lines += [
            "Titles only — these publishers deposit abstract metadata without "
            "abstract text, so anything read off this month's meetings is read "
            "off titles. The 2024 AACR and ASCO books do carry full text.",
            "",
        ]
    return "\n".join(lines)


def section_regulatory(month: str) -> str:
    """Approvals and trial registrations dated to this month.

    This is the one source type in the corpus with a genuinely monthly
    rhythm. Journals publish continuously, meetings once a year, trade
    press in a rolling two-week window — but a regulator's decisions
    arrive dated, in order, and are authoritative for exactly the kind of
    claim the corpus keeps wanting to make ("first approval for X").
    """
    lines = ["## 7. Regulatory", ""]
    con = optional_store(REGULATORY, "events")
    if con is None:
        lines += ["Regulatory store not built in this checkout — run "
                  "`scripts/harvest_regulatory.py`.", ""]
        return "\n".join(lines)

    rows = con.execute(
        "SELECT kind, COUNT(*) FROM events WHERE month=? GROUP BY kind "
        "ORDER BY COUNT(*) DESC", (month,)).fetchall()
    if not rows:
        lines += ["Nothing dated to this month in the regulatory store.", ""]
        return "\n".join(lines)

    # Trial registrations are counted, approvals are listed. There are two
    # orders of magnitude between them — roughly 570 trials a month against
    # about five approvals — and printing both the same way would bury the
    # approvals under the trials.
    onc = con.execute(
        "SELECT COUNT(*) FROM ct_trials WHERE month=? AND onc_conditions=1",
        (month,)).fetchone()[0]
    lines += ["| Event | Count |", "|---|---|"]
    for kind, n in rows:
        extra = (f" (of which {onc:,} genuinely oncology)"
                 if kind == "trial-first-posted" else "")
        lines.append(f"| {kind} | {n:,}{extra} |")
    lines.append("")

    approvals = con.execute(
        "SELECT date, title FROM fda_approvals WHERE month=? ORDER BY date",
        (month,)).fetchall()
    if approvals:
        lines += [f"**{len(approvals)} FDA "
                  f"{'action' if len(approvals) == 1 else 'actions'}** — dated "
                  f"from each notice's own prose, not the table's posting date, "
                  f"which disagrees on 7 of 190 rows and once by enough to move "
                  f"an approval into the wrong month:",
                  ""]
        for date, title in approvals:
            lines.append(f"- {date} — {title}")
        lines.append("")

    ema = con.execute(
        "SELECT date, name FROM ema_medicines WHERE month=? AND oncology=1 "
        "ORDER BY date", (month,)).fetchall()
    if ema:
        lines += [f"**{len(ema)} EMA oncology "
                  f"{'authorisation' if len(ema) == 1 else 'authorisations'}:**",
                  ""]
        for date, name in ema:
            lines.append(f"- {date} — {name}")
        lines.append("")
    return "\n".join(lines)


# STAT files roughly 300 items a month across all of health — drug pricing,
# insurance, hospital politics, public health. Most of it is outside what this
# corpus reads. Listing recent headlines regardless would fill the section with
# material no thread could ever cite, so headlines are selected on the corpus's
# own subject matter and the unfiltered count is reported alongside.
ON_TOPIC = (
    "cancer", "tumor", "tumour", "oncolog", "carcinoma", "leukemia", "leukaemia",
    "lymphoma", "myeloma", "melanoma", "metasta", "chemotherap", "car-t", "car t",
    "checkpoint", "immunotherap", "pd-1", "pd-l1", "antibody", "antibodies",
    "bispecific", "crispr", "gene therapy", "gene-editing", "genome", "genomic",
    "sequencing", "single-cell", "biomarker", "clinical trial", "phase 1",
    "phase 2", "phase 3", "fda approv", "oncogene", "kras", "her2", "egfr",
)


def section_press(month: str) -> str:
    """Trade press, with its coverage limit stated rather than implied.

    The expectation going in was that RSS gives a rolling two-week window
    and cannot be backfilled, which would have made this section empty for
    all but the last month of the corpus. That turned out to be true of
    only one of the three open feeds. STAT and the AACR blog both run
    WordPress and honour `?paged=N`, so walking the same public feed
    backwards recovers the full window — 9,497 and 324 items across all 32
    months. Fierce Biotech returns a byte-identical document for every
    pagination parameter and genuinely accumulates forward only.

    Four registered outlets contribute nothing and never will: Endpoints,
    OncLive and BioWorld are paywalled and are not collected, and Nature
    Briefing is an email newsletter with no feed.
    """
    lines = ["## 8. Trade press", ""]
    con = optional_store(NEWS, "news")
    if con is None:
        lines += ["News store not built in this checkout — run "
                  "`scripts/harvest_news.py`.", ""]
        return "\n".join(lines)

    span = con.execute("SELECT MIN(month), MAX(month) FROM news").fetchone()
    rows = con.execute(
        "SELECT source, COUNT(*) FROM news WHERE month=? GROUP BY source "
        "ORDER BY COUNT(*) DESC", (month,)).fetchall()
    if not rows:
        lines += [
            f"No items. The press archive covers {span[0]} to {span[1]}; feeds "
            f"that cannot be paginated backwards contribute only from the first "
            f"harvest forward.",
            "",
        ]
        return "\n".join(lines)

    where = " OR ".join(["LOWER(title) LIKE ?"] * len(ON_TOPIC))
    args = [month] + [f"%{k}%" for k in ON_TOPIC]
    picked = con.execute(
        f"SELECT source, date, title FROM news WHERE month=? AND ({where}) "
        f"ORDER BY date DESC", args).fetchall()

    total = sum(r[1] for r in rows)
    lines += [
        f"**{len(picked):,} on-topic of {total:,} items** across "
        f"{len(rows)} {'feed' if len(rows) == 1 else 'feeds'} "
        f"({', '.join(f'`{s}` {n:,}' for s, n in rows)}). Headlines are "
        f"selected by subject keyword, not recency — most of what these feeds "
        f"carry is health policy and industry finance the corpus does not read.",
        "",
    ]
    for source, date, title in picked[:12]:
        lines.append(f"- {date} — {title} — `{source}`")
    if len(picked) > 12:
        lines.append(f"- … and {len(picked) - 12:,} more on-topic items.")
    lines.append("")
    return "\n".join(lines)


def build(month: str, con: sqlite3.Connection, cards: list[dict], prev: str | None) -> str:
    label = dt.date(int(month[:4]), int(month[5:]), 1).strftime("%B %Y")
    head = [
        f"# {label} — Monthly Briefing",
        "",
        "<!-- Sections 1, 2 and 5 are generated by scripts/build_briefing.py.",
        "     Sections 3 and 4 are written by hand. Do not edit the generated ones. -->",
        "",
    ]
    hand = [
        "## 3. The evidence that moved it",
        "",
        "<!-- HAND-WRITTEN. Three to five items, ranked: state-flipping first, then",
        "     convergence (3+ independent groups, same target, same month), then",
        "     papers the journal itself flagged with an editorial or News & Views,",
        "     then evidence grade. Two or three sentences each, with PMID. -->",
        "",
        "## 4. Refutations",
        "",
        "<!-- HAND-WRITTEN, and never merged into section 3 — that is what made July",
        "     miss the entire refutation layer. Split into: (a) refutations landing on",
        "     a tracked thread, (b) method-credibility results that undercut the",
        "     reliability of everything else. -->",
        "",
    ]
    return "\n".join(
        head
        + [section_volume(con, month), section_curve(cards, month, prev)]
        + hand
        + [section_open(cards, month), section_meetings(month),
           section_regulatory(month), section_press(month)]
    )


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("month", nargs="?", help="YYYY-MM")
    ap.add_argument("--curve", action="store_true", help="print the full thread curve")
    ap.add_argument("--write", action="store_true", help="write docs/briefings/<month>.md")
    args = ap.parse_args()

    con = sqlite3.connect(INDEX)
    cards = load_cards()
    months = months_in_index(con)

    if args.curve:
        threads = sorted({t for c in cards for t in c["threads"]})
        print(f"{'thread':<30} " + " ".join(f"{m[2:]:>8}" for m in months))
        for t in threads:
            cells = []
            for m in months:
                s = sum(1 for c in cards if t in c["threads"] and c["stance"] == "supports" and c["date"][:7] == m)
                r = sum(1 for c in cards if t in c["threads"] and c["stance"] == "refutes" and c["date"][:7] == m)
                cells.append(("·" if not (s or r) else f"{s:+d}/{-r}" if r else f"{s:+d}").rjust(8))
            print(f"{t:<30} " + " ".join(cells))
        return 0

    if not args.month:
        ap.error("give a month, or --curve")
    if args.month not in months:
        ap.error(f"{args.month} not in index; have {months[0]}..{months[-1]}")

    prev = months[months.index(args.month) - 1] if months.index(args.month) else None
    text = build(args.month, con, cards, prev)
    if args.write:
        OUT.mkdir(parents=True, exist_ok=True)
        path = OUT / f"{args.month}.md"
        path.write_text(text)
        print(f"wrote {path.relative_to(ROOT)}")
    else:
        print(text)
    return 0


if __name__ == "__main__":
    sys.exit(main())
