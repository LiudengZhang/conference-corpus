#!/usr/bin/env python3
"""Regenerate sections 1, 2 and 5 of every briefing without losing 3 and 4.

build_briefing.py writes whole files, so running it over a briefing that
already has hand-written prose destroys that prose. This lifts sections 3
and 4 out first, regenerates, and puts them back.

It has to exist because the generated sections are not per-month
constants. Section 1's volume warning compares a month against the median
of every *other* month, and section 2's cumulative columns count every
card up to that month — so adding a single evidence card, or a single new
month at either end of the window, silently invalidates the generated
half of every briefing in the corpus. Extending the index back to 2024
changed all nineteen.

Preserving edits made directly to the file, rather than through whatever
script first authored it, is the whole point: the corrections issued on
2026-08-26 were typed straight into the markdown.

Usage:
    python3 scripts/regen_briefings.py              # every briefing
    python3 scripts/regen_briefings.py 2025-03 2025-04
"""

from __future__ import annotations

import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "docs" / "briefings"

S3 = "## 3. The evidence that moved it"
S5 = "## 5. Open items"


def main() -> int:
    months = sys.argv[1:] or [p.stem for p in sorted(OUT.glob("20*.md"))]
    kept = made = failed = 0

    for month in months:
        path = OUT / f"{month}.md"
        body = None
        if path.exists():
            text = path.read_text()
            _, _, rest = text.partition(S3)
            if rest:
                mid, _, _ = rest.partition(S5)
                # The generator's own placeholder carries this marker. Its
                # presence means nobody has written the month yet, so there
                # is nothing to preserve.
                if "HAND-WRITTEN" not in mid:
                    body = mid.rstrip() + "\n\n"

        result = subprocess.run(
            [sys.executable, "scripts/build_briefing.py", month, "--write"],
            cwd=ROOT, capture_output=True, text=True)
        if result.returncode:
            tail = (result.stderr.strip().splitlines() or ["?"])[-1]
            print(f"  {month}: generator failed — {tail}")
            failed += 1
            continue

        if body is None:
            made += 1
            continue

        text = path.read_text()
        head, _, rest = text.partition(S3)
        _, _, tail = rest.partition(S5)
        path.write_text(f"{head}{S3}\n{body}{S5}{tail}")
        kept += 1

    print(f"regenerated {kept + made} briefings: {kept} with prose preserved, "
          f"{made} left as skeletons"
          + (f", {failed} failed" if failed else ""))
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
