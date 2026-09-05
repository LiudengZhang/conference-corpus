#!/usr/bin/env python3
"""What did adding cards do to the thread verdicts?

Thread status in this corpus is derived, never stored — `status_of()` in
build_briefing.py recomputes it from cumulative supports and refutes every
time a briefing is generated. That is the right design, and it has a
consequence nobody had looked at: adding cards to a past month rewrites the
published thread history in place, silently, for every month after it.

On 2026-09-04 the back-scan added 1,634 cards to months that had already been
carded, briefed and deployed. The briefings regenerated correctly. Nothing was
wrong. But 160 of 528 thread-months changed status and the corpus shipped that
without anyone reading it, because there was no instrument that could see it.
This is that instrument.

What it reports:

  1  Integrity of the comparison. A card present in both versions that
     changed `stance`, `date` or `threads` means the diff is no longer a
     clean measurement of what ADDING cards did, because something was also
     edited. The back-scan changed none, so its effect is cleanly
     attributable; a future re-read might not be, and then this must say so
     rather than let the reader assume.
  2  The trajectory, per thread, per month — not just the final verdict.
     Three threads changed where they ended up; eight changed how they got
     there. `suppressive-population-inversion` reads differently in 41 of its
     44 months and ends one status away from where it started.
  3  What the rule cannot see. `status_of` counts supports and refutes and
     ignores `neutral` entirely, so a thread can hold 81 cards and read
     `too-early`. That is not a bug — a neutral card is one that genuinely
     does not move the claim — but the share matters when reading a verdict,
     and it is invisible in every briefing table.
  4  Cards attached to no thread. There are 13 and they are deliberate: each
     carries a `revised_note` saying why its thread was removed. They are the
     record of those retractions. They are printed so that a future reader
     does not mistake them for a leak and helpfully reattach them.

The rule itself is imported from build_briefing.py rather than restated here.
Two copies of a rule is one copy and one bug waiting for the day they differ.

Usage:
  python3 scripts/thread_diff.py                       # since the back-scan
  python3 scripts/thread_diff.py --since HEAD~3
  python3 scripts/thread_diff.py --format trajectory
  python3 scripts/thread_diff.py --format json > diff.json
"""
import argparse
import collections
import json
import pathlib
import subprocess
import sys

import yaml

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

from build_briefing import status_of  # noqa: E402  the rule lives there, not here

CARDS = ROOT / "data" / "evidence.yml"

# The commit before the 2026-09-04 back-scan. Defaulting to it makes the
# common question — "what did the re-read do?" — a bare invocation.
DEFAULT_SINCE = "6c4da63"

# One character per month, so a 44-month trajectory fits on a line and the
# eye catches the shape before it reads the words.
GLYPH = {
    "too-early": "e",
    "crisis": "C",
    "contested": "c",
    "splitting": "s",
    "forming": "F",
    None: "·",
}


def load_ref(ref: str) -> list[dict]:
    """Read data/evidence.yml as of a git ref, without touching the tree."""
    out = subprocess.run(
        ["git", "show", f"{ref}:data/evidence.yml"],
        cwd=ROOT, capture_output=True, text=True)
    if out.returncode:
        tail = (out.stderr.strip().splitlines() or ["?"])[-1]
        sys.exit(f"cannot read evidence.yml at {ref}: {tail}")
    return yaml.safe_load(out.stdout)["evidence"]


def month_of(card: dict) -> str:
    return str(card["date"])[:7]


def month_range(*card_sets: list[dict]) -> list[str]:
    """Every month from the earliest card to the latest, gaps included.

    Derived from the cards rather than from the briefing filenames: a month
    with no cards still carries a cumulative status, and a month whose
    briefing has not been written yet still belongs on the curve.
    """
    months = {month_of(c) for cards in card_sets for c in cards}
    lo, hi = min(months), max(months)
    out, y, m = [], int(lo[:4]), int(lo[5:])
    while f"{y:04d}-{m:02d}" <= hi:
        out.append(f"{y:04d}-{m:02d}")
        y, m = (y + 1, 1) if m == 12 else (y, m + 1)
    return out


def trajectory(cards: list[dict], months: list[str]) -> dict[str, list[str | None]]:
    """Per thread, the status at the end of each month.

    Mirrors section_curve() in build_briefing.py exactly: cumulative counts
    over `date[:7] <= month`, supports and refutes only, and None until the
    thread has its first non-neutral card — which is the same condition that
    makes a briefing print `(opens as ...)`.
    """
    threads = sorted({t for c in cards for t in c["threads"]})
    by_thread: dict[str, list[tuple[str, str]]] = collections.defaultdict(list)
    for c in cards:
        for t in c["threads"]:
            by_thread[t].append((month_of(c), c["stance"]))

    out = {}
    for t in threads:
        rows = by_thread[t]
        line = []
        for m in months:
            s = sum(1 for mo, st in rows if st == "supports" and mo <= m)
            r = sum(1 for mo, st in rows if st == "refutes" and mo <= m)
            line.append(status_of(s, r) if (s or r) else None)
        out[t] = line
    return out


def stance_counts(cards: list[dict]) -> dict[str, collections.Counter]:
    out: dict[str, collections.Counter] = collections.defaultdict(collections.Counter)
    for c in cards:
        for t in c["threads"]:
            out[t][c["stance"]] += 1
    return out


def integrity(old: list[dict], new: list[dict]) -> dict:
    """Is this a clean measurement of addition, or was something also edited?"""
    o = {c["id"]: c for c in old}
    n = {c["id"]: c for c in new}
    shared = set(o) & set(n)
    changed = {
        field: sorted(i for i in shared if str(o[i][field]) != str(n[i][field]))
        for field in ("stance", "date", "threads")
    }
    return {
        "old": len(o), "new": len(n),
        "added": sorted(set(n) - set(o)),
        "removed": sorted(set(o) - set(n)),
        "changed": changed,
        "clean": not any(changed.values()) and not (set(o) - set(n)),
    }


def build(since: str) -> dict:
    new = yaml.safe_load(CARDS.read_text())["evidence"]
    old = load_ref(since)
    months = month_range(old, new)
    ta, tb = trajectory(old, months), trajectory(new, months)
    threads = sorted(set(ta) | set(tb))
    blank = [None] * len(months)

    rows = []
    for t in threads:
        a, b = ta.get(t, blank), tb.get(t, blank)
        diff = [i for i in range(len(months)) if a[i] != b[i]]
        rows.append({
            "thread": t,
            "before": a, "after": b,
            "changed_months": [months[i] for i in diff],
            "first_divergence": months[diff[0]] if diff else None,
            "final_before": a[-1], "final_after": b[-1],
            "flipped": a[-1] != b[-1],
        })

    counts = stance_counts(new)
    mute = {
        t: {
            "total": sum(counts[t].values()),
            "neutral": counts[t]["neutral"],
            "supports": counts[t]["supports"],
            "refutes": counts[t]["refutes"],
        } for t in sorted(counts)
    }
    orphans = [
        {"id": c["id"], "stance": c["stance"],
         "why": (c.get("revised_note") or "").split(".")[0] or "(no revised_note)"}
        for c in new if not c["threads"]
    ]

    return {
        "since": since,
        "months": months,
        "integrity": integrity(old, new),
        "threads": rows,
        "mute": mute,
        "orphans": orphans,
        "thread_months_changed": sum(len(r["changed_months"]) for r in rows),
        "thread_months_total": len(rows) * len(months),
    }


def render(d: dict, fmt: str) -> str:
    out: list[str] = []
    ig = d["integrity"]
    months = d["months"]

    out.append(f"evidence.yml at {d['since']} → working tree")
    out.append(f"  {ig['old']:,} cards → {ig['new']:,}  "
               f"(+{len(ig['added']):,} added, −{len(ig['removed']):,} removed)")
    if ig["clean"] and not ig["added"]:
        out.append("  identical card sets — nothing to attribute.")
    elif ig["clean"]:
        out.append("  purely additive: no shared card changed stance, date or threads,")
        out.append("  so every status change below is attributable to the added cards.")
    else:
        out.append("  NOT purely additive — this diff does not isolate the effect of adding:")
        for field, ids in ig["changed"].items():
            if ids:
                out.append(f"    {len(ids)} card(s) changed {field}: {', '.join(ids[:5])}"
                           + (" …" if len(ids) > 5 else ""))
        if ig["removed"]:
            out.append(f"    {len(ig['removed'])} card(s) removed: {', '.join(ig['removed'][:5])}")
    out.append("")

    pct = 100 * d["thread_months_changed"] / d["thread_months_total"]
    out.append(f"{d['thread_months_changed']} of {d['thread_months_total']} thread-months "
               f"changed status — {pct:.0f}% of the curve, over "
               f"{len(months)} months ({months[0]} .. {months[-1]}).")
    out.append("")

    flips = [r for r in d["threads"] if r["flipped"]]
    out.append(f"FINAL VERDICT CHANGED — {len(flips)} thread(s)")
    if not flips:
        out.append("  none")
    for r in flips:
        m = d["mute"].get(r["thread"], {})
        out.append(f"  {r['thread']:34} {r['final_before']} → {r['final_after']}"
                   f"   (+{m.get('supports', 0)} / −{m.get('refutes', 0)} now)")
    out.append("")

    out.append("TRAJECTORY MOVED WITHOUT CHANGING THE ENDPOINT")
    quiet = [r for r in d["threads"] if not r["flipped"] and r["changed_months"]]
    for r in sorted(quiet, key=lambda r: -len(r["changed_months"])):
        out.append(f"  {r['thread']:34} {len(r['changed_months']):>3} of {len(months)} months, "
                   f"from {r['first_divergence']}, still {r['final_after']}")
    out.append("")

    if fmt == "trajectory":
        out.append("PER-MONTH TRAJECTORY   "
                   + "  ".join(f"{k}={v}" for v, k in
                               [(g, s) for s, g in GLYPH.items() if s]))
        out.append(f"{'':36}{months[0]}{'':>{max(0, len(months) - 14)}}{months[-1]}")
        for r in d["threads"]:
            before = "".join(GLYPH[s] for s in r["before"])
            after = "".join(GLYPH[s] for s in r["after"])
            mark = "".join("^" if a != b else " "
                           for a, b in zip(r["before"], r["after"]))
            out.append(f"  {r['thread']:34}{before}   was")
            out.append(f"  {'':34}{after}   now")
            out.append(f"  {'':34}{mark}".rstrip())
        out.append("")

    out.append("WHAT THE RULE CANNOT SEE — neutral cards never enter status_of()")
    out.append(f"  {'thread':34} {'cards':>6} {'neutral':>8} {'share':>6}")
    for t, m in sorted(d["mute"].items(), key=lambda kv: -kv[1]["neutral"] / max(kv[1]["total"], 1)):
        if not m["total"]:
            continue
        out.append(f"  {t:34} {m['total']:6} {m['neutral']:8} "
                   f"{100 * m['neutral'] / m['total']:5.0f}%")
    out.append("")

    out.append(f"ATTACHED TO NO THREAD — {len(d['orphans'])} card(s), deliberately")
    out.append("  Each was stripped of its thread by an earlier repair and keeps a")
    out.append("  revised_note saying why. They are the record of those retractions.")
    for o in d["orphans"]:
        out.append(f"  {o['id']:26} {o['stance']:9} {o['why'][:70]}")
    return "\n".join(out)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--since", default=DEFAULT_SINCE,
                    help=f"git ref to compare against (default {DEFAULT_SINCE}, "
                         "the commit before the back-scan)")
    ap.add_argument("--format", choices=("table", "trajectory", "json"),
                    default="table")
    args = ap.parse_args()

    d = build(args.since)
    if args.format == "json":
        print(json.dumps(d, indent=1, default=str))
    else:
        print(render(d, args.format))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
