#!/usr/bin/env python3
"""Harvest the news layer from RSS/Atom feeds into data/news.sqlite.

Read this before trusting anything the table says about coverage.

A news feed is not an archive. The default endpoint of an RSS feed is a
*rolling window* of the most recent items -- 25 for Fierce Biotech, 20
for STAT, 10 for the AACR blog. That is roughly two days of Fierce and
one day of STAT. The corpus this feeds runs 2024-01 through 2026-08, 32
months. A single poll of a default feed therefore covers well under 1%
of the window, and re-polling the same endpoint tomorrow does not
recover yesterday's missing months -- it only moves the window forward.
No amount of patience turns a rolling window into a back catalogue.

Two consequences shape this script:

  * It accumulates rather than snapshots. Rows are upserted on a stable
    key (the feed GUID where one is published, the normalised link
    otherwise), so running it weekly grows the table instead of
    replacing it. `--rebuild` is the only path that drops anything, and
    it exists for schema changes, not for routine use. A harvester that
    rewrote the table on each run would quietly cap this source at
    whatever the window happened to hold that morning.

  * It records what it actually got. The `sources` table stores the real
    earliest and latest item date per source, so the coverage limit is a
    value you can query rather than an assumption you have to remember.
    If a source contributed eleven days, the table says eleven days.

Backfill was investigated per source and the answer is not uniform:

  * STAT and the AACR blog run WordPress, whose feed honours `?paged=N`.
    Page 490 of the STAT feed serves November 2023; page 32 of the AACR
    feed serves January 2024. Both therefore backfill the full window
    for real, and this script walks them page by page until the items
    fall past `--from`. This is ordinary pagination of a public feed,
    not a paywall workaround: every item returned is the same open
    headline-and-summary the default feed serves.

  * Fierce Biotech does not paginate. `?page=N`, `?paged=N` and
    `?offset=N` all return a byte-identical 25-item document. Its
    sitemap does list historical URLs, but it is served behind a
    Cloudflare interstitial to non-browser clients and carries no
    titles, summaries or publication dates in any case -- only
    `lastmod`. Fierce is a forward-accumulating source and nothing more.
    Its history before the day this script first ran is not obtainable.

  * The ACIR weekly digest has no feed at all -- /feed/ is a 404, /rss
    and /atom.xml are 404s, ?feed=rss2 silently returns the homepage,
    and there is no WP-JSON API (/wp-json/ is a custom 404 page, so the
    site is not the WordPress install those paths assume). It is
    nonetheless the most completely backfillable source here, because
    /weekly-digests/ is a hand-enumerable archive: every year links to
    every month, and the active month's nav lists each week's digest
    with its date. Walking year x month over the window addresses every
    issue directly, with no pagination to guess at. Each weekly digest
    is stored as one row -- the papers a digest cites are deliberately
    not expanded into rows of their own, because those belong to the
    journal index and would double-count here.

  * Nature Briefing has no feed. It is an email newsletter; the
    endpoint in sources.yml is a signup form, and the page exposes no
    RSS or Atom link. nature.com publishes journal feeds, but a journal
    table of contents is a different artefact from the Briefing and
    substituting one for the other would misrepresent the source. It is
    recorded as unharvestable with that reason and produces no rows.

Endpoints News, OncLive and BioWorld are paywalled. They are registered
in the `sources` table with harvestable=0 so that their absence is
visible rather than merely unexplained, and they are never fetched.
This is a deliberate boundary, not an unfinished feature.

Dates are the other practical hazard. Feeds in this set publish three
mutually incompatible formats -- RFC 822 with an offset ("Thu, 27 Aug
2026 19:47:01 +0000"), ISO 8601 from Atom, and Fierce's own
human-readable "Aug 26, 2026 4:32pm" -- so every date goes through
`parse_date`, and an item whose date cannot be parsed is dropped rather
than filed under a guessed month. The `month` column is derived from the
item's own publication date, never from the day of the run.

Usage:
    python3 scripts/harvest_news.py
    python3 scripts/harvest_news.py --only n-stat
    python3 scripts/harvest_news.py --only n-fierce-biotech --no-backfill
    python3 scripts/harvest_news.py --rebuild --from 2024-01 --to 2026-08
"""

from __future__ import annotations

import argparse
import datetime as dt
import email.utils
import html
import pathlib
import re
import sqlite3
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass

ROOT = pathlib.Path(__file__).resolve().parent.parent
DB = ROOT / "data" / "news.sqlite"

MAILTO = "liudengzhang91@gmail.com"
UA = f"conference-corpus/1.0 (mailto:{MAILTO})"

# The corpus window. Backfill walks stop once a page falls past FROM.
DEFAULT_FROM = "2024-01"
DEFAULT_TO = "2026-08"


@dataclass(frozen=True)
class Source:
    """One news feed, plus what it can and cannot be asked for.

    `page_param` is set only where pagination was verified to return
    genuinely older items. Fierce Biotech accepts the parameter and
    ignores it, which is worse than rejecting it -- a naive walk would
    re-fetch page 1 forever and look like it was making progress -- so
    it is left empty and the rolling window is taken at face value.
    """

    id: str
    name: str
    endpoint: str = ""
    kind: str = "feed"          # "feed" (RSS/Atom) or "acir-archive"
    page_param: str = ""        # "" means the feed does not paginate
    path_filter: str = ""       # keep only links containing this
    harvestable: bool = True
    max_pages: int = 600
    note: str = ""

    @property
    def can_backfill(self) -> bool:
        return bool(self.page_param) or self.kind == "acir-archive"


SOURCES = [
    # --- open, forward-only ------------------------------------------
    Source("n-fierce-biotech", "Fierce Biotech",
           "https://www.fiercebiotech.com/rss/xml",
           note="25-item rolling window; ?page/?paged/?offset all return "
                "the identical document, and the sitemap is Cloudflare-"
                "gated and dateless. No backfill exists."),
    # --- open, WordPress, genuinely paginated -------------------------
    Source("n-stat", "STAT News",
           "https://www.statnews.com/feed/", page_param="paged",
           note="20 items/page. Verified back to 2021 via ?paged=N; the "
                "feed carries open headlines and summaries even for "
                "STAT+ articles whose full text is metered."),
    Source("n-aacr-blog", "AACR Blog",
           "https://www.aacr.org/feed/", page_param="paged",
           path_filter="/blog/", max_pages=120,
           note="/blog/feed/ is a 404; the site-wide /feed/ is the blog "
                "feed -- every item resolves under /blog/ -- and is "
                "filtered on that path. 10 items/page, verified to 2015."),
    # --- open, no feed, but a fully enumerable archive ----------------
    Source("n-acir", "ACIR Weekly Digest (Cancer Research Institute)",
           "https://acir.org/weekly-digests/", kind="acir-archive",
           note="No feed exists (/feed/, /rss, /atom.xml all 404; "
                "?feed=rss2 returns the homepage; no WP-JSON). Harvested "
                "from the /weekly-digests/YYYY/<month>/ archive, which "
                "enumerates every issue with its date."),
    # --- open in principle, but no machine-readable artefact ----------
    Source("n-nature-briefing", "Nature Briefing", harvestable=False,
           note="Email newsletter. The sources.yml endpoint is a signup "
                "form exposing no RSS/Atom link, and no feed URL for the "
                "Briefing itself resolves. nature.com journal feeds are a "
                "different artefact and are not a substitute."),
    # --- paywalled: registered so the exclusion is visible, never fetched
    Source("n-endpoints", "Endpoints News", harvestable=False,
           note="Paywalled. https://endpts.com/feed/ returns HTTP 403 to "
                "automated clients. Deliberately not harvested."),
    Source("n-onclive", "OncLive", harvestable=False,
           note="Paywalled and Cloudflare-protected to automated "
                "fetchers. Deliberately not harvested."),
    Source("n-bioworld", "BioWorld", harvestable=False,
           note="Paywalled. Deliberately not harvested."),
]

SCHEMA = """
CREATE TABLE IF NOT EXISTS news(
    key       TEXT PRIMARY KEY,   -- feed GUID, else normalised link
    source    TEXT NOT NULL,
    title     TEXT,
    link      TEXT NOT NULL,
    date      TEXT,               -- YYYY-MM-DD, from the item itself
    month     TEXT,               -- YYYY-MM, derived from date
    author    TEXT,
    summary   TEXT,               -- description/summary, tags stripped
    first_seen TEXT,
    last_seen  TEXT);
CREATE UNIQUE INDEX IF NOT EXISTS n_link   ON news(link);
CREATE INDEX        IF NOT EXISTS n_month  ON news(month);
CREATE INDEX        IF NOT EXISTS n_source ON news(source);
CREATE TABLE IF NOT EXISTS sources(
    id TEXT PRIMARY KEY, name TEXT, endpoint TEXT,
    harvestable INTEGER, backfill TEXT, note TEXT,
    n INTEGER, earliest TEXT, latest TEXT, last_run TEXT);
"""

TAG = re.compile(r"<[^>]+>")
WS = re.compile(r"\s+")
# Tracking parameters the feeds bolt onto their own links. Stripping them
# is what makes the link a stable dedup key across runs; STAT appends
# ?utm_campaign=rss to every item and would otherwise look new whenever
# the campaign tag changed.
TRACKING = re.compile(r"^(utm_[a-z_]+|mc_[a-z]+|_hsenc|_hsmi|fbclid|gclid)$")


def clean(text: str) -> str:
    """Strip tags and entities, collapse whitespace."""
    return WS.sub(" ", html.unescape(TAG.sub(" ", text or ""))).strip()


def normalise(link: str) -> str:
    """Drop tracking parameters so the link is a stable dedup key.

    Done through urlsplit rather than a regex over the raw string: a
    regex that eats "?utm_source=a" out of "?utm_source=a&id=7" leaves
    "&id=7" with no leading "?", quietly corrupting the URL. Rebuilding
    the query from parsed pairs cannot produce that.
    """
    link = (link or "").strip()
    if not link:
        return ""
    parts = urllib.parse.urlsplit(link)
    kept = [(k, v) for k, v in urllib.parse.parse_qsl(parts.query, keep_blank_values=True)
            if not TRACKING.match(k.lower())]
    return urllib.parse.urlunsplit((
        parts.scheme, parts.netloc, parts.path,
        urllib.parse.urlencode(kept), ""))


def local(tag: str) -> str:
    """Local name of a possibly namespaced ElementTree tag."""
    return tag.rsplit("}", 1)[-1]


def text_of(elem) -> str:
    """All text under an element, tags included as children.

    Fierce Biotech nests real markup inside <title> and <dc:creator>
    (`<title><a href="...">Headline</a></title>`), so `elem.text` is
    empty there. itertext() is the only reading that works for both
    that and the ordinary CDATA case.
    """
    if elem is None:
        return ""
    return clean("".join(elem.itertext()))


# Formats observed across these four feeds, in the order they are tried.
DATE_FORMATS = [
    "%a, %d %b %Y %H:%M:%S %z",   # RFC 822 with offset (STAT, AACR)
    "%a, %d %b %Y %H:%M:%S",      # RFC 822, no zone
    "%b %d, %Y %I:%M%p",          # "Aug 26, 2026 4:32pm" (Fierce)
    "%B %d, %Y",                  # "January 31, 2024" (ACIR digest page)
    "%b %d, %Y",
    "%Y-%m-%dT%H:%M:%S%z",        # Atom
    "%Y-%m-%dT%H:%M:%S",
    "%Y-%m-%d %H:%M:%S",
    "%Y-%m-%d",
]


def parse_date(raw: str) -> str:
    """Return YYYY-MM-DD, or "" if the string cannot be trusted.

    Returning "" rather than today's date matters: an unparsed date that
    silently became the run date would file the item under the wrong
    month, and month is the axis the whole corpus is organised on.
    """
    raw = (raw or "").strip()
    if not raw:
        return ""
    # RFC 822 with named zones ("EST", "GMT") that strptime %z rejects.
    try:
        parsed = email.utils.parsedate_to_datetime(raw)
        if parsed:
            return parsed.strftime("%Y-%m-%d")
    except (TypeError, ValueError, IndexError):
        pass
    iso = raw.replace("Z", "+00:00")
    try:
        return dt.datetime.fromisoformat(iso).strftime("%Y-%m-%d")
    except ValueError:
        pass
    for fmt in DATE_FORMATS:
        try:
            return dt.datetime.strptime(raw, fmt).strftime("%Y-%m-%d")
        except ValueError:
            continue
    return ""


def get(url: str, tries: int = 4) -> bytes | None:
    """Fetch with backoff. A 403/404 is final and is not retried."""
    req = urllib.request.Request(url, headers={
        "User-Agent": UA, "Accept": "application/rss+xml, application/xml, */*"})
    for i in range(tries):
        try:
            with urllib.request.urlopen(req, timeout=60) as resp:
                return resp.read()
        except urllib.error.HTTPError as err:
            if err.code in (403, 404, 410):
                return None       # the feed is telling us to stop, not to wait
            time.sleep(2.0 * (i + 1))
        except Exception:  # noqa: BLE001 - retry anything else, report below
            time.sleep(2.0 * (i + 1))
    return None


def parse_feed(blob: bytes, src: Source) -> list[dict]:
    """Parse one RSS 2.0 or Atom document into item dicts.

    Both dialects are handled here because the registry does not record
    which one a source speaks, and a source can change dialect without
    notice.
    """
    import xml.etree.ElementTree as ET

    try:
        root = ET.fromstring(blob)
    except ET.ParseError:
        return []

    entries = [e for e in root.iter() if local(e.tag) in ("item", "entry")]
    rows = []
    for entry in entries:
        fields: dict[str, list] = {}
        for child in entry:
            fields.setdefault(local(child.tag), []).append(child)

        def first(*names):
            for name in names:
                if fields.get(name):
                    return fields[name][0]
            return None

        title = text_of(first("title"))

        # Atom puts the URL in <link href>; RSS puts it in the text.
        link = ""
        for cand in fields.get("link", []):
            href = cand.get("href") or (cand.text or "")
            rel = cand.get("rel", "alternate")
            if href and rel == "alternate":
                link = href.strip()
                break
        if not link and fields.get("link"):
            link = (fields["link"][0].text or "").strip()

        guid_el = first("guid", "id")
        guid = (guid_el.text or "").strip() if guid_el is not None else ""
        # An RSS guid with isPermaLink="true" and no link element is the URL.
        if not link and guid.startswith("http"):
            link = guid

        link = normalise(link)
        if not link:
            continue
        if src.path_filter and src.path_filter not in link:
            continue

        date_el = first("pubDate", "published", "date", "updated", "modified")
        date = parse_date(date_el.text if date_el is not None else "")
        if not date:
            continue

        author = text_of(first("creator", "author"))
        if not author and fields.get("author"):
            # Atom <author><name>..</name></author>
            author = text_of(fields["author"][0])

        summary_el = first("description", "summary", "subtitle")
        summary = text_of(summary_el)
        if not summary:
            summary = text_of(first("encoded", "content"))[:2000]

        rows.append({
            "key": guid or link,
            "source": src.id,
            "title": title,
            "link": link,
            "date": date,
            "month": date[:7],
            "author": author,
            "summary": summary,
        })
    return rows


# --- ACIR archive ------------------------------------------------------
# The digest pages are plain server-rendered HTML with no feed behind
# them, so these three regexes are the whole parser. They are anchored on
# structural markers (the archive URL shape, <h1>, the first <h2>) rather
# than on CSS classes, which are the part of a template most likely to be
# restyled without notice.
ACIR_MONTHS = ["january", "february", "march", "april", "may", "june",
               "july", "august", "september", "october", "november",
               "december"]
ACIR_H1 = re.compile(r"<h1[^>]*>(.*?)</h1>", re.S | re.I)
ACIR_H2 = re.compile(r"<h2[^>]*>\s*([A-Z][a-z]+ \d{1,2}, \d{4})\s*</h2>", re.I)
ACIR_BODY = re.compile(r"<article[^>]*>(.*?)(?:<h2|</article>)", re.S | re.I)
SCRIPT = re.compile(r"<(script|style)\b.*?</\1>", re.S | re.I)


def iter_months(start: str, end: str):
    y, m = int(start[:4]), int(start[5:7])
    ey, em = int(end[:4]), int(end[5:7])
    while (y, m) <= (ey, em):
        yield y, m
        y, m = (y + 1, 1) if m == 12 else (y, m + 1)


def acir_digest(url: str, fallback_date: str) -> dict | None:
    """Fetch one weekly digest page and pull out title, date, summary."""
    blob = get(url)
    if blob is None:
        return None
    page = blob.decode("utf-8", "replace")

    m = ACIR_H1.search(page)
    title = clean(m.group(1)) if m else ""
    if not title:
        m = re.search(r"<title[^>]*>(.*?)</title>", page, re.S | re.I)
        title = clean(m.group(1)) if m else ""
    if not title:
        return None

    # The digest page states its own date ("January 31, 2024"); the month
    # nav only says "January 31" and needs the year bolted on, so the
    # page's own line is preferred and the nav is the fallback.
    m = ACIR_H2.search(page)
    date = parse_date(m.group(1)) if m else ""
    if not date:
        date = fallback_date
    if not date:
        return None

    m = ACIR_BODY.search(page)
    summary = clean(SCRIPT.sub(" ", m.group(1)))[:1200] if m else ""

    return {"key": url, "source": "n-acir", "title": title, "link": url,
            "date": date, "month": date[:7], "author": "", "summary": summary}


def pull_acir(src: Source, start: str, end: str) -> tuple[list[dict], list[str]]:
    """Walk /weekly-digests/<year>/<month>/ across the whole window."""
    rows: list[dict] = []
    notes: list[str] = []
    missing = 0

    for year, month in iter_months(start, end):
        name = ACIR_MONTHS[month - 1]
        blob = get(f"https://acir.org/weekly-digests/{year}/{name}")
        if blob is None:
            missing += 1
            notes.append(f"no archive page for {year}-{month:02d}")
            continue
        page = blob.decode("utf-8", "replace")

        # Only the active month's nav is expanded, so restricting the
        # match to this year/month is what keeps the walk from
        # re-collecting the whole site on every request.
        pattern = re.compile(
            r'href="(https://acir\.org/weekly-digests/%d/%s/[^"]+)"[^>]*>\s*'
            r'([A-Z][a-z]+ \d{1,2})\s*<' % (year, name))
        found = {}
        for url, daytext in pattern.findall(page):
            found.setdefault(url, f"{daytext}, {year}")

        if not found:
            missing += 1
            notes.append(f"{year}-{month:02d}: archive page listed no digests")
            continue

        for url, daytext in found.items():
            row = acir_digest(url, parse_date(daytext))
            if row is None:
                continue
            if start <= row["month"] <= end:
                rows.append(row)
            time.sleep(0.3)
        time.sleep(0.3)

    if missing:
        notes.append(f"{missing} of the window's months yielded nothing")
    return rows, notes


def page_url(src: Source, page: int) -> str:
    if page <= 1 or not src.page_param:
        return src.endpoint
    sep = "&" if "?" in src.endpoint else "?"
    return f"{src.endpoint}{sep}{src.page_param}={page}"


def pull(src: Source, start: str, end: str, backfill: bool,
         max_pages: int) -> tuple[list[dict], list[str]]:
    """Walk a feed until it falls past `start`. Returns (rows, notes)."""
    seen: dict[str, dict] = {}
    notes: list[str] = []
    limit = max_pages if (backfill and src.can_backfill) else 1
    page = 1
    empty_streak = 0

    while page <= limit:
        blob = get(page_url(src, page))
        if blob is None:
            notes.append(f"stopped at page {page}: no response")
            break
        rows = parse_feed(blob, src)
        if not rows:
            notes.append(f"stopped at page {page}: no parsable items")
            break

        fresh = [r for r in rows if r["key"] not in seen]
        # A feed that ignores its page parameter serves page 1 forever.
        # Two consecutive all-duplicate pages is that signature, and the
        # walk stops rather than looping to max_pages pretending to work.
        if not fresh:
            empty_streak += 1
            if empty_streak >= 2:
                notes.append(
                    f"stopped at page {page}: pagination returns duplicates "
                    f"(the feed ignores ?{src.page_param})")
                break
        else:
            empty_streak = 0

        for row in rows:
            if start <= row["month"] <= end:
                seen.setdefault(row["key"], row)

        newest = max(r["date"] for r in rows)
        oldest = min(r["date"] for r in rows)
        # Feeds are reverse-chronological: once the newest item on a page
        # predates the window, every later page does too.
        if newest[:7] < start:
            notes.append(f"reached {oldest} at page {page}, past --from {start}")
            break
        if limit == 1:
            break
        page += 1
        time.sleep(0.4)
    else:
        notes.append(f"hit the {limit}-page cap without reaching {start}")

    return list(seen.values()), notes


def upsert(con: sqlite3.Connection, rows: list[dict], now: str) -> tuple[int, int]:
    """Add new rows, refresh existing ones. Never deletes.

    INSERT OR IGNORE then UPDATE, rather than INSERT OR REPLACE: REPLACE
    deletes the conflicting row first, which would reset first_seen and
    destroy the record of when an item entered the corpus.
    """
    added = updated = 0
    for row in rows:
        cur = con.execute(
            "INSERT OR IGNORE INTO news"
            "(key, source, title, link, date, month, author, summary,"
            " first_seen, last_seen) VALUES (?,?,?,?,?,?,?,?,?,?)",
            (row["key"], row["source"], row["title"], row["link"], row["date"],
             row["month"], row["author"], row["summary"], now, now))
        if cur.rowcount:
            added += 1
            continue
        cur = con.execute(
            "UPDATE news SET title=?, date=?, month=?, author=?, summary=?,"
            " last_seen=? WHERE key=?",
            (row["title"], row["date"], row["month"], row["author"],
             row["summary"], now, row["key"]))
        updated += cur.rowcount
    return added, updated


def month_span(start: str, end: str) -> int:
    ys, ms = int(start[:4]), int(start[5:7])
    ye, me = int(end[:4]), int(end[5:7])
    return (ye - ys) * 12 + (me - ms) + 1


def main() -> int:
    ap = argparse.ArgumentParser(
        description="Harvest news feeds into data/news.sqlite")
    ap.add_argument("--only", default="", help="source id to restrict to")
    ap.add_argument("--rebuild", action="store_true",
                    help="drop and rebuild the tables (discards accumulated "
                         "history that the feeds can no longer serve)")
    ap.add_argument("--from", dest="start", default=DEFAULT_FROM, help="YYYY-MM")
    ap.add_argument("--to", dest="end", default=DEFAULT_TO, help="YYYY-MM")
    ap.add_argument("--no-backfill", action="store_true",
                    help="poll only the default feed window")
    ap.add_argument("--max-pages", type=int, default=0,
                    help="override the per-source page cap")
    args = ap.parse_args()

    start, end = args.start, args.end
    now = dt.datetime.now().strftime("%Y-%m-%d %H:%M")

    DB.parent.mkdir(parents=True, exist_ok=True)
    con = sqlite3.connect(DB)
    if args.rebuild:
        con.executescript("DROP TABLE IF EXISTS news; DROP TABLE IF EXISTS sources;")
    con.executescript(SCHEMA)

    todo = [s for s in SOURCES if not args.only or s.id == args.only]
    if not todo:
        sys.exit(f"no source with id {args.only!r}")

    for src in todo:
        backfill = "none"
        if args.no_backfill and src.can_backfill:
            backfill = "skipped"
        elif src.kind == "acir-archive":
            backfill = "archive"
        elif src.page_param:
            backfill = f"?{src.page_param}=N"

        if not src.harvestable:
            con.execute(
                "INSERT OR REPLACE INTO sources VALUES (?,?,?,?,?,?,?,?,?,?)",
                (src.id, src.name, src.endpoint, 0, "n/a", src.note,
                 0, None, None, now))
            con.commit()
            print(f"{src.name}: not harvested -- {src.note}", flush=True)
            continue

        if src.kind == "acir-archive" and not args.no_backfill:
            rows, notes = pull_acir(src, start, end)
        elif src.kind == "acir-archive":
            rows, notes = [], ["--no-backfill: ACIR has no feed to poll, so "
                               "skipping the archive leaves nothing to fetch"]
        else:
            cap = args.max_pages or src.max_pages
            rows, notes = pull(src, start, end, not args.no_backfill, cap)
        added, updated = upsert(con, rows, now)
        n, earliest, latest = con.execute(
            "SELECT COUNT(*), MIN(date), MAX(date) FROM news WHERE source=?",
            (src.id,)).fetchone()
        con.execute("INSERT OR REPLACE INTO sources VALUES (?,?,?,?,?,?,?,?,?,?)",
                    (src.id, src.name, src.endpoint, 1, backfill, src.note,
                     n, earliest, latest, now))
        con.commit()
        print(f"{src.name}: {len(rows):,} items in window "
              f"({added:,} new, {updated:,} refreshed); table now {n:,}",
              flush=True)
        for note in notes:
            print(f"    {note}", flush=True)

    # ---- summary -----------------------------------------------------
    print()
    print(f"{'source':18} {'rows':>7} {'earliest':>10} {'latest':>10} "
          f"{'months':>7} {'backfill':>10}")
    print("-" * 68)
    want = month_span(start, end)
    for sid, name, harvestable, backfill, n, earliest, latest in con.execute(
            "SELECT id, name, harvestable, backfill, n, earliest, latest "
            "FROM sources ORDER BY harvestable DESC, n DESC"):
        if not harvestable:
            print(f"{sid:18} {'--':>7} {'--':>10} {'--':>10} "
                  f"{'--':>7} {'excluded':>10}")
            continue
        months = con.execute(
            "SELECT COUNT(DISTINCT month) FROM news WHERE source=?",
            (sid,)).fetchone()[0]
        print(f"{sid:18} {n or 0:7,} {earliest or '--':>10} "
              f"{latest or '--':>10} {months:>4}/{want:<2} {backfill:>10}")

    total = con.execute("SELECT COUNT(*) FROM news").fetchone()[0]
    covered = con.execute(
        "SELECT COUNT(DISTINCT month) FROM news WHERE month BETWEEN ? AND ?",
        (start, end)).fetchone()[0]
    print("-" * 68)
    print(f"{'TOTAL':18} {total:7,} across {covered}/{want} months of "
          f"{start}..{end}")
    print()
    print("Coverage note: STAT and the AACR blog paginate, and ACIR has a "
          "fully\nenumerable /weekly-digests/ archive, so all three are "
          "backfilled across the\nwhole window. Fierce Biotech serves a "
          "25-item rolling window with no archive\nof any kind, so it can "
          "only accumulate forward from the first run of this\nscript -- its "
          "early months will stay empty no matter how often this is\nre-run. "
          "Nature Briefing has no feed; Endpoints, OncLive and BioWorld are\n"
          "paywalled and excluded by design.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
