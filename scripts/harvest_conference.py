#!/usr/bin/env python3
"""Harvest the conference layer from Crossref into data/conference.sqlite.

The premise this whole corpus rests on is that meeting programs lead the
literature. Nothing in the repo tested that until this script existed:
the journal index covered 2025-01 onward and every conference vault was
2026, so the two layers barely overlapped and no lead time was
measurable in either direction.

The fix is to harvest a conference far enough in the past that the
literature has had time to catch up. AACR Annual Meeting 2024 (April
2024) and ASCO Annual Meeting 2024 (May-June 2024) both deposit their
abstracts in Crossref with full text, and the journal index now reaches
2026-08 — a follow-up window of about 28 months.

Two routes, because the publishers differ:

  * AACR deposits into the Cancer Research supplement (e-ISSN 1538-7445).
    Everything under that ISSN in 2024 includes the special conferences
    too, so the Annual Meeting is isolated on the DOI suffix `am2024`.
  * ASCO deposits into the JCO supplement (e-ISSN 1527-7755). The
    `16_suppl` DOIs are the Annual Meeting; `_suppl` numbers other than
    16 are the thematic symposia (GI, GU) and are kept, tagged by suffix.

Abstracts arrive as JATS XML in the `abstract` field; tags are stripped
but the text is otherwise left alone.

Usage:
    python3 scripts/harvest_conference.py
    python3 scripts/harvest_conference.py --year 2024 --only aacr
"""

from __future__ import annotations

import argparse
import html
import json
import pathlib
import re
import sqlite3
import sys
import time
import urllib.parse
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parent.parent
DB = ROOT / "data" / "conference.sqlite"

# Crossref asks for a contact address and gives a faster pool for it.
MAILTO = "liudengzhang91@gmail.com"

VENUES = [
    # id,      name,                          issn,        doi_filter
    ("aacr", "AACR Annual Meeting", "1538-7445", "am{year}"),
    ("asco", "ASCO Annual Meeting", "1527-7755", "_suppl"),
]

SCHEMA = """
DROP TABLE IF EXISTS abstracts;
CREATE TABLE abstracts(doi TEXT PRIMARY KEY, venue TEXT, year INTEGER,
                       date TEXT, month TEXT, session TEXT,
                       title TEXT, abstract TEXT);
CREATE INDEX c_venue ON abstracts(venue);
CREATE INDEX c_month ON abstracts(month);
"""

TAG = re.compile(r"<[^>]+>")
WS = re.compile(r"\s+")


def clean(text: str) -> str:
    return WS.sub(" ", html.unescape(TAG.sub(" ", text or ""))).strip()


def get(url: str, tries: int = 5):
    req = urllib.request.Request(url, headers={
        "User-Agent": f"conference-corpus/1.0 (mailto:{MAILTO})"})
    for i in range(tries):
        try:
            return json.load(urllib.request.urlopen(req, timeout=90))
        except Exception:
            time.sleep(2.0 * (i + 1))
    return None


def pull(issn: str, year: int):
    """Yield every Crossref item for an ISSN in a calendar year."""
    cursor = "*"
    while True:
        url = (f"https://api.crossref.org/journals/{issn}/works?"
               + urllib.parse.urlencode({
                   "filter": f"from-pub-date:{year}-01-01,until-pub-date:{year}-12-31",
                   "rows": 500,
                   "cursor": cursor,
                   "select": "DOI,title,abstract,published,page",
                   "mailto": MAILTO,
               }))
        page = get(url)
        if not page:
            print(f"  giving up on {issn} at cursor {cursor[:24]}", flush=True)
            return
        message = page["message"]
        items = message.get("items", [])
        if not items:
            return
        yield from items
        cursor = message.get("next-cursor")
        if not cursor:
            return
        time.sleep(0.2)


def published(item) -> str:
    parts = (item.get("published") or {}).get("date-parts") or [[]]
    parts = (parts[0] + [1, 1])[:3]
    if not parts or not parts[0]:
        return ""
    return "%04d-%02d-%02d" % tuple(parts)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--year", type=int, default=2024)
    ap.add_argument("--only", default="", help="venue id to restrict to")
    args = ap.parse_args()

    DB.parent.mkdir(parents=True, exist_ok=True)
    con = sqlite3.connect(DB)
    con.executescript(SCHEMA)

    for vid, name, issn, doi_filter in VENUES:
        if args.only and args.only != vid:
            continue
        needle = doi_filter.format(year=args.year)
        kept = seen = 0
        rows = []
        for item in pull(issn, args.year):
            seen += 1
            doi = item.get("DOI", "").lower()
            if needle not in doi:
                continue
            date = published(item)
            title = clean((item.get("title") or [""])[0])
            # AACR prefixes every title with "Abstract 1234:"; the number
            # is the session ordering, which is worth keeping separately.
            session = ""
            m = re.match(r"Abstract\s+([A-Z]*\d+)\s*:\s*(.*)", title)
            if m:
                session, title = m.group(1), m.group(2)
            rows.append((doi, vid, args.year, date, date[:7], session,
                         title, clean(item.get("abstract", ""))))
            kept += 1
            if kept % 2000 == 0:
                print(f"  {vid}: {kept:,} kept / {seen:,} scanned", flush=True)
        con.executemany(
            "INSERT OR REPLACE INTO abstracts VALUES (?,?,?,?,?,?,?,?)", rows)
        con.commit()
        print(f"{name} {args.year}: {kept:,} abstracts "
              f"(scanned {seen:,} under ISSN {issn})", flush=True)

    print()
    print("venue  month     abstracts  with full text")
    for venue, month, n, full in con.execute(
            "SELECT venue, month, COUNT(*), SUM(LENGTH(abstract)>200) "
            "FROM abstracts GROUP BY venue, month ORDER BY venue, month"):
        print(f"{venue:6} {month}  {n:9,}  {full or 0:14,}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
