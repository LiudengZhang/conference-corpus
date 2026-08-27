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
2026-08 -- a follow-up window of about 28 months.

Three routes, because publishers mark up meeting abstracts differently:

  * DOI substring. AACR deposits into the Cancer Research supplement
    (e-ISSN 1538-7445). Everything under that ISSN in 2024 includes the
    special conferences too, so the Annual Meeting is isolated on the DOI
    suffix `am2024`. ASCO deposits into the JCO supplement (e-ISSN
    1527-7755); `_suppl` DOIs are the meetings.

  * Supplement number. The ESMO family publishes one abstract book per
    congress as a numbered supplement of ESMO Open or Annals of Oncology.
    Crossref exposes this as the non-standard top-level key
    `special_numbering` ("S3", "S4", ...). It is absent from the `select`
    whitelist, so these routes must pull whole records.

  * Issue number. USCAP's abstract book is an ordinary numbered issue of
    Laboratory Investigation (issue 3), not a supplement.

Which congress a supplement belongs to is not stated anywhere in the
Crossref metadata -- there is no front-matter record naming the meeting.
Where the registry asserted a mapping it was checked against the
abstracts' own disease-site vocabulary before being trusted: S3 is 99%
lung (ELCC), S4 99% breast (ESMO Breast), S6 99% gynaecological. Two
further 2026 supplements, S2 and S5, are multi-site meetings that the
content cannot identify and that the registry never listed. They are
harvested under provisional ids with confirmed=0 rather than guessed at;
`--confirmed-only` excludes them from analysis.

Abstracts arrive as JATS XML in the `abstract` field; tags are stripped
but the text is otherwise left alone.

Usage:
    python3 scripts/harvest_conference.py
    python3 scripts/harvest_conference.py --only elcc-2026
"""

from __future__ import annotations

import argparse
import html
import pathlib
import re
import sqlite3
import sys
import time
import urllib.parse
import urllib.request
from dataclasses import dataclass

ROOT = pathlib.Path(__file__).resolve().parent.parent
DB = ROOT / "data" / "conference.sqlite"

# Crossref asks for a contact address and gives a faster pool for it.
MAILTO = "liudengzhang91@gmail.com"


@dataclass(frozen=True)
class Venue:
    """One meeting, plus how to cut it out of a journal's Crossref feed."""

    id: str
    name: str
    year: int
    issn: str
    doi: str = ""          # route 1: DOI substring
    suppl: str = ""        # route 2: special_numbering
    issue: str = ""        # route 3: issue number
    confirmed: bool = True
    note: str = ""

    def matches(self, item: dict) -> bool:
        if self.doi:
            return self.doi.format(year=self.year) in item.get("DOI", "").lower()
        if self.suppl:
            return str(item.get("special_numbering")) == self.suppl
        if self.issue:
            return str(item.get("issue")) == self.issue
        raise ValueError(f"{self.id}: no discriminator")

    @property
    def needs_full_records(self) -> bool:
        # `special_numbering` is dropped by Crossref's `select` projection.
        return bool(self.suppl)

    @property
    def requires_number(self) -> bool:
        """Is a leading abstract number the thing that separates content
        from front matter?

        Only on the supplement and issue routes. There, the whole journal
        issue is the abstract book, so the author index and the welcome
        note are the only unnumbered records and dropping them is exactly
        right. On the DOI route the filter has already isolated the
        meeting, and ASCO does not number its titles at all -- applying
        the rule there discarded 7,557 of 7,569 ASCO abstracts while
        looking like it was working.
        """
        return bool(self.suppl or self.issue)


VENUES = [
    # --- the 2024 premise cohort -------------------------------------
    # Venue ids are the join key back to data/sources.yml, so they have to be
    # the registry's ids exactly. These two were `aacr`/`asco` until the
    # registry check started enforcing the join.
    Venue("aacr-2024", "AACR Annual Meeting 2024", 2024, "1538-7445", doi="am{year}"),
    Venue("asco-2024", "ASCO Annual Meeting 2024", 2024, "1527-7755", doi="_suppl"),
    # --- ESMO family, one abstract book per supplement ----------------
    Venue("elcc-2026", "European Lung Cancer Congress 2026", 2026,
          "2059-7029", suppl="S3",
          note="99% lung vocabulary; matches the registry's Suppl S3"),
    Venue("esmo-breast-2026", "ESMO Breast Cancer 2026", 2026,
          "2059-7029", suppl="S4",
          note="99% breast vocabulary; matches the registry's Suppl S4"),
    Venue("esmo-gyn-2026", "ESMO Gynaecological Cancers Congress 2026", 2026,
          "2059-7029", suppl="S6",
          note="99% gynaecological vocabulary; venue absent from the registry"),
    Venue("esmo-gi-2026", "ESMO Gastrointestinal Cancers Congress 2026", 2026,
          "0923-7534", suppl="S1",
          note="76% GI vocabulary; published in Annals of Oncology, not "
               "ESMO Open as the registry assumed"),
    Venue("esmo-open-2026-s2", "ESMO Open 2026 Suppl S2 (meeting unidentified)",
          2026, "2059-7029", suppl="S2", confirmed=False,
          note="multi-site: breast/lung/GU/gyn. No front-matter record names "
               "the meeting and the content does not disambiguate."),
    Venue("esmo-open-2026-s5", "ESMO Open 2026 Suppl S5 (meeting unidentified)",
          2026, "2059-7029", suppl="S5", confirmed=False,
          note="multi-site: renal/sarcoma/lymphoma/breast/GI. Same problem "
               "as S2."),
    # --- USCAP rides an ordinary issue, not a supplement --------------
    Venue("uscap-2026", "USCAP 115th Annual Meeting", 2026,
          "0023-6837", issue="3",
          note="Laboratory Investigation issue 3 is the abstract book"),
]

SCHEMA = """
CREATE TABLE IF NOT EXISTS abstracts(
    doi TEXT PRIMARY KEY, venue TEXT, year INTEGER,
    date TEXT, month TEXT, session TEXT,
    title TEXT, abstract TEXT, confirmed INTEGER DEFAULT 1);
CREATE INDEX IF NOT EXISTS c_venue ON abstracts(venue);
CREATE INDEX IF NOT EXISTS c_month ON abstracts(month);
CREATE TABLE IF NOT EXISTS venues(
    id TEXT PRIMARY KEY, name TEXT, year INTEGER, issn TEXT,
    route TEXT, confirmed INTEGER, note TEXT, n INTEGER);
"""

TAG = re.compile(r"<[^>]+>")
WS = re.compile(r"\s+")
# Meeting abstract numbering: a leading integer plus an optional short
# presentation code -- 78P, 1MO, 26eP, 2RO, 12TiP -- or bare, as USCAP
# numbers them. Requiring it drops each book's front matter and indexes.
ABSNUM = re.compile(r"^\s*(\d+)\s*([A-Za-z]{0,4})(?![A-Za-z0-9])")
# AACR writes "Abstract 1234: Real title here".
AACR_PREFIX = re.compile(r"Abstract\s+([A-Z]*\d+)\s*:\s*(.*)", re.DOTALL)


def clean(text: str) -> str:
    return WS.sub(" ", html.unescape(TAG.sub(" ", text or ""))).strip()


def get(url: str, tries: int = 5):
    import json
    req = urllib.request.Request(url, headers={
        "User-Agent": f"conference-corpus/1.0 (mailto:{MAILTO})"})
    for i in range(tries):
        try:
            return json.load(urllib.request.urlopen(req, timeout=90))
        except Exception:  # noqa: BLE001 - retry anything, report below
            time.sleep(2.0 * (i + 1))
    return None


def pull(issn: str, year: int, full: bool):
    """Yield every Crossref item for an ISSN in a calendar year."""
    cursor = "*"
    total = 0
    while True:
        params = {
            "filter": f"from-pub-date:{year}-01-01,until-pub-date:{year}-12-31",
            "rows": 500,
            "cursor": cursor,
            "mailto": MAILTO,
        }
        if not full:
            params["select"] = "DOI,title,abstract,published,page,issue"
        page = get(f"https://api.crossref.org/journals/{issn}/works?"
                   + urllib.parse.urlencode(params))
        if not page:
            print(f"  giving up on {issn} at cursor {cursor[:24]}", flush=True)
            return
        message = page["message"]
        items = message.get("items", [])
        if not items:
            return
        yield from items
        total += len(items)
        cursor = message.get("next-cursor")
        if not cursor or total >= message.get("total-results", 0):
            return
        time.sleep(0.2)


def published(item) -> str:
    parts = (item.get("published") or {}).get("date-parts") or [[]]
    parts = (parts[0] + [1, 1])[:3]
    if not parts or not parts[0]:
        return ""
    return "%04d-%02d-%02d" % tuple(parts)


def split_title(title: str, venue: Venue) -> tuple[str, str]:
    """Return (session/abstract number, title without it)."""
    m = AACR_PREFIX.match(title)
    if m:
        return m.group(1), m.group(2).strip()
    m = ABSNUM.match(title)
    if m:
        return (m.group(1) + m.group(2)), title[m.end():].lstrip(" :.–-")
    return "", title


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", default="", help="venue id to restrict to")
    ap.add_argument("--rebuild", action="store_true",
                    help="drop and rebuild the whole table")
    args = ap.parse_args()

    DB.parent.mkdir(parents=True, exist_ok=True)
    con = sqlite3.connect(DB)
    if args.rebuild:
        con.executescript("DROP TABLE IF EXISTS abstracts; DROP TABLE IF EXISTS venues;")
    con.executescript(SCHEMA)

    todo = [v for v in VENUES if not args.only or v.id == args.only]
    # One journal-year feed can serve several venues (ESMO Open 2026 holds
    # four). Pull each feed once and fan the items out.
    feeds: dict[tuple[str, int, bool], list[Venue]] = {}
    for v in todo:
        feeds.setdefault((v.issn, v.year, v.needs_full_records), []).append(v)

    for (issn, year, full), vs in feeds.items():
        buckets: dict[str, list] = {v.id: [] for v in vs}
        seen = 0
        for item in pull(issn, year, full):
            seen += 1
            for v in vs:
                if not v.matches(item):
                    continue
                title = clean((item.get("title") or [""])[0])
                session, body = split_title(title, v)
                # Inside an abstract book, numbering is what separates the
                # abstracts from the front matter. See Venue.requires_number.
                if v.requires_number and not session:
                    continue
                date = published(item)
                buckets[v.id].append(
                    (item.get("DOI", "").lower(), v.id, v.year, date, date[:7],
                     session, body, clean(item.get("abstract", "")),
                     int(v.confirmed)))
                break
        for v in vs:
            rows = buckets[v.id]
            con.execute("DELETE FROM abstracts WHERE venue=?", (v.id,))
            con.executemany(
                "INSERT OR REPLACE INTO abstracts VALUES (?,?,?,?,?,?,?,?,?)", rows)
            route = (f"doi~{v.doi}" if v.doi else
                     f"suppl={v.suppl}" if v.suppl else f"issue={v.issue}")
            con.execute("INSERT OR REPLACE INTO venues VALUES (?,?,?,?,?,?,?,?)",
                        (v.id, v.name, v.year, v.issn, route,
                         int(v.confirmed), v.note, len(rows)))
            con.commit()
            flag = "" if v.confirmed else "  [venue unconfirmed]"
            print(f"{v.name}: {len(rows):,} abstracts "
                  f"({route}, scanned {seen:,} under ISSN {issn}){flag}",
                  flush=True)

    print()
    print(f"{'venue':22} {'month':8} {'abstracts':>10} {'with full text':>15}")
    for venue, month, n, fulltext in con.execute(
            "SELECT venue, month, COUNT(*), SUM(LENGTH(abstract)>200) "
            "FROM abstracts GROUP BY venue, month ORDER BY venue, month"):
        print(f"{venue:22} {month:8} {n:10,} {fulltext or 0:15,}")
    total = con.execute("SELECT COUNT(*) FROM abstracts").fetchone()[0]
    conf = con.execute(
        "SELECT COUNT(*) FROM abstracts WHERE confirmed=1").fetchone()[0]
    print(f"\ntotal {total:,} abstracts across "
          f"{con.execute('SELECT COUNT(*) FROM venues').fetchone()[0]} venues "
          f"({total - conf:,} in venues whose meeting is unidentified)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
