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

Weights: the limit is not a raw token count, so components are converted to
input-token-equivalents using Anthropic's published price ratios (output costs
5x input, cache writes 1.25x, cache reads 0.1x). That is a proxy for cost, not
a claim about how the limiter works.

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
WEIGHTS = {
    "input_tokens": 1.0,
    "output_tokens": 5.0,
    "cache_creation_input_tokens": 1.25,
    "cache_read_input_tokens": 0.1,
}

# No published figure exists for the subscription 5-hour cap, so this default
# is a placeholder to be calibrated against /usage, not a real limit.
DEFAULT_BUDGET = int(os.environ.get("CLAUDE_5H_BUDGET", 40_000_000))


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
    ap.add_argument("--budget", type=int, default=DEFAULT_BUDGET,
                    help="input-token-equivalents; calibrate against /usage")
    ap.add_argument("--quiet", action="store_true",
                    help="one line, for hooks and CLAUDE.md gating")
    args = ap.parse_args()

    result = scan(args.hours)
    if result is None:
        print("no ~/.claude/projects — cannot estimate", file=sys.stderr)
        return 2
    totals, by_model, calls, earliest = result

    weighted = sum(totals[f] * w for f, w in WEIGHTS.items())
    pct = weighted / args.budget * 100 if args.budget else 0.0

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
    print(f"  budget {args.budget:,} equiv — set CLAUDE_5H_BUDGET or --budget")
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
