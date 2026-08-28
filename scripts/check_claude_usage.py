#!/usr/bin/env python3
"""Estimate Claude Code usage in the rolling 5-hour window.

WHY THIS EXISTS, AND WHAT IT IS NOT

An agent cannot read its own rate-limit state. `/usage` is rendered by the
Claude Code client, there is no `claude usage --json`, and the Admin API's
usage report covers API keys rather than the subscription quota that the
5-hour limit is drawn from. So an agent asked to "watch the limit" can only
either guess or lie.

What it *can* read is the evidence Claude Code already writes to disk. Every
assistant turn in every transcript under ~/.claude/projects carries an ISO
timestamp and the exact `usage` block the API returned. Summing those over the
last five hours gives a number computed from the same events the limit counts.

THIS IS AN ESTIMATE AND WILL DRIFT. It cannot see usage from claude.ai, from
other machines, or from any client that does not write these transcripts, and
the true limit is not published as a token count. Calibrate it once — run
`/usage`, compare, and set BUDGET to whatever makes this agree — then treat it
as a rough brake with margin, never as a precise threshold.

CALIBRATE IT OR DO NOT TRUST IT. The first version of this script weighted
cache reads at 0.1 and reported 82% against a real 20% — wrong by a factor of
four, and it stopped work on the strength of that. The cause is structural:
cache reads are ~98% of all tokens in a normal session, so the estimate is
almost entirely one uncertain weight, and the script did not say so.

The fix is not a better guess. Record an observation from /usage —
`--calibrate 20` — and the scalar is fitted to it. One observation fits one
number, so the weights below are held fixed and only the budget moves; with
several observations taken at different work mixes you could fit more.
Uncalibrated, this prints a warning and no percentage.

Usage:
    python3 scripts/check_claude_usage.py
    python3 scripts/check_claude_usage.py --hours 5 --budget 40000000
    python3 scripts/check_claude_usage.py --quiet     # one line, for hooks
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import pathlib
import sys

PROJECTS = pathlib.Path.home() / ".claude" / "projects"

# Input-token-equivalents, from published price ratios. Visible on purpose:
# if they are wrong the number is wrong, and a reader should be able to see
# which assumption to attack.
# Price ratios, used as a cost proxy. The cache-read weight dominates every
# result — see the docstring — so it is the one to attack if calibration keeps
# drifting. 0.02 rather than the 0.1 price ratio because rate limiting appears
# to discount cached input far more heavily than billing does.
WEIGHTS = {
    "input_tokens": 1.0,
    "output_tokens": 5.0,
    "cache_creation_input_tokens": 1.25,
    "cache_read_input_tokens": 0.02,
}

CALIB = pathlib.Path.home() / ".claude" / "usage-calibration.json"

def calibrated_budget() -> int | None:
    """Budget fitted to recorded /usage observations, or None if never told.

    Returns None rather than a guess. A number with no provenance is what
    produced the 4x error this file exists to not repeat.
    """
    env = os.environ.get("CLAUDE_5H_BUDGET")
    if env:
        return int(env)
    if not CALIB.exists():
        return None
    try:
        obs = json.loads(CALIB.read_text()).get("observations") or []
    except Exception:  # noqa: BLE001
        return None
    if not obs:
        return None
    # Each observation implies a budget; take the median so one mistyped
    # reading cannot move the answer much.
    implied = sorted(o["weighted"] / (o["observed_pct"] / 100.0)
                     for o in obs if o.get("observed_pct"))
    if not implied:
        return None
    return int(implied[len(implied) // 2])


def scan(hours: float):
    """Sum weighted usage over the window, deduplicated by message id.

    A resumed session can rewrite assistant turns into a new transcript, so
    the same API call appears twice on disk. Counting both would inflate the
    estimate exactly when a long session is being resumed — which is when the
    number matters most.
    """
    cutoff = dt.datetime.now(dt.timezone.utc) - dt.timedelta(hours=hours)
    seen: set[str] = set()
    totals: dict[str, int] = {k: 0 for k in WEIGHTS}
    by_model: dict[str, float] = {}
    calls = 0
    earliest = None

    if not PROJECTS.is_dir():
        return None

    for path in PROJECTS.rglob("*.jsonl"):
        # Cheap skip: a file untouched since the cutoff holds nothing in it.
        if dt.datetime.fromtimestamp(path.stat().st_mtime,
                                     dt.timezone.utc) < cutoff:
            continue
        try:
            fh = path.open(encoding="utf-8", errors="replace")
        except OSError:
            continue
        with fh:
            for line in fh:
                try:
                    rec = json.loads(line)
                except Exception:  # noqa: BLE001 - a partial trailing write
                    continue
                msg = rec.get("message") or {}
                usage = msg.get("usage")
                stamp = rec.get("timestamp")
                if not usage or not stamp:
                    continue
                try:
                    when = dt.datetime.fromisoformat(stamp.replace("Z", "+00:00"))
                except ValueError:
                    continue
                if when < cutoff:
                    continue
                key = msg.get("id") or f"{path.name}:{stamp}"
                if key in seen:
                    continue
                seen.add(key)
                calls += 1
                earliest = when if earliest is None else min(earliest, when)
                weighted = 0.0
                for field, weight in WEIGHTS.items():
                    n = usage.get(field) or 0
                    totals[field] += n
                    weighted += n * weight
                model = msg.get("model") or "unknown"
                by_model[model] = by_model.get(model, 0.0) + weighted

    return totals, by_model, calls, earliest


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--hours", type=float, default=5.0)
    ap.add_argument("--budget", type=int, default=None,
                    help="override the fitted budget")
    ap.add_argument("--calibrate", type=float, metavar="PCT",
                    help="record what /usage says right now, and fit to it")
    ap.add_argument("--quiet", action="store_true",
                    help="one line, for hooks and CLAUDE.md gating")
    args = ap.parse_args()

    result = scan(args.hours)
    if result is None:
        print("no ~/.claude/projects — cannot estimate", file=sys.stderr)
        return 2
    totals, by_model, calls, earliest = result

    weighted = sum(totals[f] * w for f, w in WEIGHTS.items())

    if args.calibrate is not None:
        CALIB.parent.mkdir(parents=True, exist_ok=True)
        try:
            blob = json.loads(CALIB.read_text())
        except Exception:  # noqa: BLE001
            blob = {}
        blob.setdefault("observations", []).append({
            "at": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"),
            "observed_pct": args.calibrate,
            "weighted": weighted,
            "raw": totals,
            "weights": WEIGHTS,
        })
        CALIB.write_text(json.dumps(blob, indent=2))
        fitted = calibrated_budget()
        print(f"recorded: /usage says {args.calibrate:g}% while this window "
              f"weighs {weighted:,.0f}")
        print(f"fitted budget now {fitted:,} equiv "
              f"(from {len(blob['observations'])} observation(s))")
        print("take another reading at a different work mix to improve it.")
        return 0

    budget = args.budget or calibrated_budget()
    if not budget:
        print("NOT CALIBRATED — no percentage will be shown.")
        print(f"  this window weighs {weighted:,.0f} equiv over {calls:,} calls")
        print("  run /usage, then: ./check-claude-usage --calibrate <pct>")
        print("  a guessed budget is what made this report 82% against a real")
        print("  20% the first time, so it guesses nothing now.")
        return 0
    pct = weighted / budget * 100

    if args.quiet:
        print(f"5h usage: {pct:.0f}% ({weighted/1e6:.1f}M of "
              f"{args.budget/1e6:.0f}M equiv, {calls} calls) — ESTIMATE")
        return 0 if pct < 80 else 1

    short = {"input_tokens": "input", "output_tokens": "output",
             "cache_creation_input_tokens": "cache write",
             "cache_read_input_tokens": "cache read"}
    print(f"Claude Code usage, rolling {args.hours:g}h window")
    print(f"  {'':12} {'tokens':>14}  {'weight':>6}  {'equiv':>14}")
    for field, weight in WEIGHTS.items():
        n = totals[field]
        print(f"  {short[field]:12} {n:>14,}  {weight:>6.2f}  {n*weight:>14,.0f}")
    print(f"  {'':12} {'':>14}  {'':>6}  {'-'*14}")
    print(f"  {'total':12} {'':>14}  {'':>6}  {weighted:>14,.0f}")
    print()
    print(f"  API calls counted     {calls:,}")
    if earliest:
        age = dt.datetime.now(dt.timezone.utc) - earliest
        print(f"  oldest call in window {age.total_seconds()/3600:.1f}h ago")
    if by_model:
        print("  by model:")
        for model, w in sorted(by_model.items(), key=lambda kv: -kv[1]):
            print(f"    {model:28} {w:>14,.0f}  ({w/weighted*100:.0f}%)")
    print()
    bar = "#" * min(40, int(pct / 2.5))
    print(f"  ESTIMATED {pct:.0f}% of budget   [{bar:<40}]")
    print(f"  budget {budget:,} equiv, fitted from /usage observations")
    dom = max(WEIGHTS, key=lambda k: totals[k] * WEIGHTS[k])
    share = totals[dom] * WEIGHTS[dom] / weighted * 100 if weighted else 0
    print(f"  {share:.0f}% of that total is `{dom}` — if its weight is wrong,")
    print(f"  this number is wrong, and that is the failure mode to watch.")
    print()
    print("  This is an estimate from local transcripts, not the real quota.")
    print("  It cannot see usage from claude.ai or another machine. Calibrate")
    print("  it once against /usage, then leave margin.")
    if pct >= 80:
        print()
        print("  >= 80%: stop starting expensive work.")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
