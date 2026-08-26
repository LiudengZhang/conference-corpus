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

    lines = [
        "## 1. What was read",
        "",
        f"**{total:,} research articles** across 33 journals, "
        f"filtered to `journal article` and excluding reviews, editorials, news, "
        f"comment and case reports.",
        "",
        "| " + " | ".join(d.capitalize() for d in DOMAINS) + " |",
        "|" + "---|" * len(DOMAINS),
        "| " + " | ".join(f"{by_dom.get(d, 0):,}" for d in DOMAINS) + " |",
        "",
    ]
    swung = {d: v for d, v in drift.items() if abs(v) >= 25}
    if swung:
        detail = ", ".join(f"{d} {v:+.0f}%" for d, v in sorted(swung.items()))
        lines += [
            f"!!! warning \"Volume swing against the median month: {detail}\"",
            "    Check the harvest before reading anything into this. A swing this size is "
            "usually indexing lag or a broken query, not the field going quiet. The known "
            "benign case is `bioinfo` every January, which carries the Nucleic Acids "
            "Research database issue.",
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
        + [section_open(cards, month)]
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
