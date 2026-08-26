# Convention update — blog timestamps in Central Time, not UTC

Paste-ready note for the server-side agent (send with your next prompt to it).

---

One convention change for the blogs going forward.

**Stamp the `date:` frontmatter in US Central Time (Houston, America/Chicago), not UTC.** Label it `CT`. Houston is the project's anchor timezone, so a UTC stamp reads 5–6 hours off against the actual working day.

- Summer (DST, ~Mar 8 – Nov 1): CT = UTC − 5 (CDT).
- Winter: CT = UTC − 6 (CST).
- Format unchanged otherwise: `date: '2026-06-08 16:00 CT'`.

Example: a post you'd previously have stamped `'2026-06-08 21:00 UTC'` becomes `'2026-06-08 16:00 CT'`.

No need to touch the existing blogs — those 27 have already been converted to CT on `main` (commit `e2e0005`). This is just for everything new.
