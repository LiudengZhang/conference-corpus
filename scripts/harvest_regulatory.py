#!/usr/bin/env python3
"""Harvest the regulatory layer into data/regulatory.sqlite.

The journal layer (L1) and the conference layer both answer "when was this
said". Neither answers "when did a regulator act on it", and that is the
date a translational claim is finally settled against: a target is either
in a registered trial or it is not, and a drug is either approved for an
indication or it is not. This script builds that third clock.

Four sources from data/sources.yml, and the single most important thing
about them is that they are NOT the same kind of object:

  * r-fda-oncology-approvals -- an EVENT STREAM. A plain server-rendered
    HTML table, Webpage | Description | Date, dates as M/D/YYYY, running
    back several years. Every row is a dated act by the OCE, and this is
    the highest-value source in the file.

    One correction had to be made here. The table's Date column is when
    FDA *posted the notice*, not when it acted. Each description restates
    the real date in prose ("On August 26, 2026, the Food and Drug
    Administration approved ..."), and the two disagree on 7 of 192 rows
    -- usually by a day, but treosulfan was approved 2025-01-21 and posted
    2025-02-06, which is a 16-day slip across a month boundary and would
    have filed that approval under the wrong month. So `date` (and hence
    `month`) is taken from the prose where it parses, the table value is
    kept alongside as `posted_date`, and `date_confirmed` records whether
    the two agreed.

  * r-fda-cellular-gene-therapy -- a STATE ROSTER. Product & Trade Name |
    Manufacturer, and *no date column at all*. It answers "what is
    licensed right now", never "what happened in March". Approval dates
    for these products exist, but only on each product's own page, and
    inferring them from this table would be invention. It is therefore
    stored in a separate table with a `captured` snapshot date and no
    `month` column, so that it is structurally impossible to join it into
    a month query by accident. If you want CAR-T approval dates, most of
    them are already in the FDA oncology stream above.

  * r-ema-medicines -- an EVENT STREAM, but not at the URL in sources.yml.
    /en/medicines is a JavaScript shell; fetching it returns 200 and no
    medicines. EMA's actual public artifact is the "Medicines output"
    spreadsheet regenerated nightly from the same database, at
    .../documents/report/medicines-output-medicines-report_en.xlsx. It
    carries what the registry entry did not promise: `Marketing
    authorisation date`, `Opinion adopted date`, `European Commission
    decision date`, refusal and withdrawal dates. So EMA is dated after
    all. (A second, older EPAR spreadsheet under /system/files/ also
    responds 200 but was last generated in December 2023 and has no date
    columns -- do not use it.)

  * r-clinicaltrials-gov -- an EVENT STREAM. `studyFirstPostDate` is the
    event: the day the trial became publicly visible. Not the start date,
    which is a plan and slips, and not the completion date, which is a
    forecast. First-posted is the one date that cannot be revised
    backwards, so it is the only one safe to bin by month.

    The row also stores `brief_summary` and the arm-group text, which look
    like padding and are not. `interventions` gives an agent's INN or its
    sponsor code and never its target, so a search over title+interventions
    cannot see a first-in-human antibody registered as "IPN01203" -- 42% of
    2025's phase-1 oncology rows named only a bare code, and any question
    about which targets reached the clinic was answerable only up to that
    residue. The prose fields state mechanism ("a bispecific antibody
    targeting PD-1 and VEGF") where the structured fields do not.

Two consequences for the schema. First, every dated row carries `date`,
`month` (YYYY-MM, derived from that row's own date) and `source_id`, and
the three event tables are UNIONed by a view `events` so that one month
can be pulled across all regulators in a single query. Second, the roster
table is deliberately not in that view.

Parsing is stdlib only, matching the rest of scripts/. bs4 happens to be
installed but is not imported: the FDA tables are two hand-checked shapes,
and the EMA workbook is read with zipfile + ElementTree because xlsx is a
zip of XML and openpyxl would be a dependency for forty lines of code.

Volume note, and the reason the ClinicalTrials.gov harvest is chunked.

The window was widened from 2023-01 to 2013-01, because scripts/approval_lead.py
returned n=0 measurable / 185 censored and named the cause: with a table
starting 2023-01 no drug approved in 2023-2026 has a visible first-in-human,
so every lead time it could compute was the distance to the window edge.
2013-01..2026-08 is ~70k interventional oncology trials against ~24k before.

That crosses --max-trials (40,000), and the old code responded to crossing it
by silently re-issuing the query narrowed to Phase 1/2/3. The consequence is
not a smaller harvest, it is a different table: the 2023+ rows already on disk
contain PHASE4, NA and EARLY_PHASE1, so a phase-narrowed backfill would have
made every count spanning 2022 and 2023 a comparison between two populations
with nothing in the schema to say so. Three changes close that off:

  * the window is harvested one CALENDAR YEAR at a time. The largest year in
    the range is ~6.4k, a sixth of the cap, so the narrowing branch is out of
    reach structurally rather than by the cap happening to be generous;
  * --max-trials is now a per-chunk ceiling and crossing it REFUSES the chunk.
    Narrowing requires --allow-phase-narrowing, passed by hand. A missing
    chunk is a visible hole; a phase-restricted one is an invisible one;
  * `ct_chunks` records phases per chunk, so "is this table one population?"
    is answered by SUM(phases)=0 against the database rather than by a prose
    note in `sources` that the next run would overwrite.

A re-run of ClinicalTrials.gov is now a MERGE, not the DELETE-then-INSERT
full re-download it used to be. Completed chunks are skipped (--refetch-ct
overrides), rows are committed page by page, and nothing is ever deleted, so
an interruption at year 7 resumes at year 7 instead of restarting -- and,
more importantly, cannot leave the table emptier than it found it. The other
three sources are still per-source refreshes. ClinicalTrials.gov
matches `query.cond` as free text over a record's whole condition list, so
a multi-condition trial gets pulled in on one oncology term among five
(a COPD rehabilitation study lists "Lung Neoplasms" fourth). Rather than
guess at a stricter server-side query, every trial is stored with an
`onc_conditions` flag set only when an oncology term actually appears in
the conditions; about 11% of the set does not clear that bar and can be
excluded downstream without re-harvesting.

Usage:
    python3 scripts/harvest_regulatory.py
    python3 scripts/harvest_regulatory.py --only r-clinicaltrials-gov
    python3 scripts/harvest_regulatory.py --rebuild
"""

from __future__ import annotations

import argparse
import datetime as dt
import html
import io
import json
import pathlib
import re
import sqlite3
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
import zipfile
from html.parser import HTMLParser

ROOT = pathlib.Path(__file__).resolve().parent.parent
DB = ROOT / "data" / "regulatory.sqlite"

MAILTO = "liudengzhang91@gmail.com"
UA = f"conference-corpus/1.0 (mailto:{MAILTO})"

FDA_ONC = ("https://www.fda.gov/drugs/resources-information-approved-drugs/"
           "oncology-cancer-hematologic-malignancies-approval-notifications")
FDA_CGT = ("https://www.fda.gov/vaccines-blood-biologics/"
           "cellular-gene-therapy-products/"
           "approved-cellular-and-gene-therapy-products")
# Not the sources.yml endpoint -- see the module docstring.
EMA_XLSX = ("https://www.ema.europa.eu/en/documents/report/"
            "medicines-output-medicines-report_en.xlsx")
CTGOV = "https://clinicaltrials.gov/api/v2/studies"

# ClinicalTrials.gov indexes conditions by free text, so "cancer" alone
# misses trials registered only as "Diffuse Large B-Cell Lymphoma" or
# "Multiple Myeloma". This widening adds ~700 trials over `cancer`.
ONC_COND = ("cancer OR neoplasm OR tumor OR tumour OR carcinoma OR lymphoma "
            "OR leukemia OR leukaemia OR myeloma OR sarcoma OR melanoma "
            "OR glioma OR oncology")

# `fields` takes v2 "piece names", not JSON paths. The arm-group pieces are
# leaves *inside* protocolSection.armsInterventionsModule.armGroups, and
# naming them is what makes the API emit that array at all -- the previous
# field list asked only for InterventionName, so armGroups came back absent
# and the extractor had nothing to read. Requesting the three leaves returns
# armGroups[] carrying exactly label/description/interventionNames (asking
# for the `ArmGroup` container instead would also return `type`, which is
# EXPERIMENTAL/PLACEBO_COMPARATOR boilerplate and names no target).
# BriefSummary comes back whole, not clipped: checked against the same
# study fetched with no `fields` at all.
CT_FIELDS = ("NCTId,BriefTitle,OverallStatus,StudyFirstPostDate,Condition,"
             "Phase,StudyType,LeadSponsorName,LeadSponsorClass,"
             "CollaboratorName,InterventionName,InterventionType,"
             "EnrollmentCount,StartDate,BriefSummary,"
             "ArmGroupLabel,ArmGroupDescription,ArmGroupInterventionName")

# `interventions` names an INN or a bare code ("IPN01203", "BNT329") and
# almost never a target, so a first-in-human antibody against a newly
# nominated checkpoint is invisible to a title+interventions search. The
# prose fields do name mechanism, and this is the cap that keeps them from
# unbounded growth -- same 4000 the EMA `indication` column uses.
TEXT_CAP = 4000

# Flags rows rather than dropping them: both the EMA workbook and the
# ClinicalTrials.gov set are stored whole, because they are small enough
# that a bad oncology filter costs more than the rows it saves.
ONC_RE = re.compile(
    r"neoplas|carcinom|cancer|lymphom|leuk[ae]m|myelom|sarcom|melanom|"
    r"gliom|glioblast|tumou?r|myelodysplas|myeloprolifer|mesotheliom|"
    r"blastoma|adenom|oncolog|malignan|metasta", re.I)

SOURCES = ["r-fda-oncology-approvals", "r-fda-cellular-gene-therapy",
           "r-ema-medicines", "r-clinicaltrials-gov"]

SCHEMA = """
-- Event stream: dated acts by the FDA Oncology Center of Excellence.
-- `date` is the approval date stated in the notice's own prose; the
-- table's own Date column is the later posting date, kept as posted_date.
--
-- Two columns record how much that is worth, and they must not be conflated
-- (an earlier version stored only date_confirmed=int(prose==posted), which
-- put "the two dates disagree" and "there was no prose date to compare"
-- both in the 0 bucket -- one is a finding, the other is a parse failure):
--   date_source     'prose'  -- date came from the notice's own sentence
--                   'posted' -- no prose date parsed; date IS posted_date
--   date_confirmed  1    prose and posted agree
--                   0    prose and posted DISAGREE (date is the prose one)
--                   NULL no prose date was found, so nothing was compared
-- So `date_confirmed IS NULL` is the data-quality signal (how many notices
-- the DESC_DATE regex failed on) and `date_confirmed = 0` is the substantive
-- one (how often FDA posts a notice later than it acted).
CREATE TABLE IF NOT EXISTS fda_approvals(
    url TEXT PRIMARY KEY, source_id TEXT,
    date TEXT, month TEXT, posted_date TEXT,
    action TEXT, drug TEXT, title TEXT, description TEXT,
    date_confirmed INTEGER, date_source TEXT);
CREATE INDEX IF NOT EXISTS r_fda_month ON fda_approvals(month);

-- STATE ROSTER, not an event stream. The source page has no dates; this
-- table therefore has no `date` and no `month`, only `captured`, the day
-- the snapshot was taken. Do not join it into a month query.
CREATE TABLE IF NOT EXISTS fda_cgt_roster(
    product TEXT PRIMARY KEY, source_id TEXT,
    captured TEXT, trade_name TEXT, generic_name TEXT,
    manufacturer TEXT, url TEXT);

-- Event stream: EMA centrally authorised medicines, human only.
CREATE TABLE IF NOT EXISTS ema_medicines(
    product_number TEXT PRIMARY KEY, source_id TEXT,
    date TEXT, month TEXT,
    name TEXT, inn TEXT, active_substance TEXT,
    therapeutic_area TEXT, atc TEXT, status TEXT,
    orphan INTEGER, conditional INTEGER, accelerated INTEGER,
    prime INTEGER, advanced_therapy INTEGER, oncology INTEGER,
    holder TEXT, opinion_date TEXT, ec_decision_date TEXT,
    refusal_date TEXT, withdrawal_date TEXT,
    indication TEXT, url TEXT, captured TEXT);
CREATE INDEX IF NOT EXISTS r_ema_month ON ema_medicines(month);
CREATE INDEX IF NOT EXISTS r_ema_onc ON ema_medicines(oncology);

-- Event stream: date is studyFirstPostDate, the day the record went public.
--
-- The last four columns are the prose layer. `interventions` gives an agent
-- name and no mechanism, so searching title+interventions cannot see a
-- first-in-human antibody registered as a bare code; brief_summary and the
-- arm-group text usually say what the agent is against. Both prose columns
-- are capped at TEXT_CAP characters.
--
-- They are APPENDED, not slotted next to `interventions`, and must stay
-- appended: an existing database gains them via ALTER TABLE ADD COLUMN,
-- which can only append, so putting them mid-table here would give a fresh
-- database a different column order from a migrated one and silently
-- scramble the positional INSERT below.
CREATE TABLE IF NOT EXISTS ct_trials(
    nct_id TEXT PRIMARY KEY, source_id TEXT,
    date TEXT, month TEXT,
    status TEXT, title TEXT, conditions TEXT, phases TEXT,
    study_type TEXT, lead_sponsor TEXT, sponsor_class TEXT,
    collaborators TEXT, interventions TEXT,
    enrollment INTEGER, start_date TEXT, onc_conditions INTEGER, url TEXT,
    brief_summary TEXT, arm_labels TEXT, arm_descriptions TEXT,
    arm_interventions TEXT);
CREATE INDEX IF NOT EXISTS r_ct_month ON ct_trials(month);
CREATE INDEX IF NOT EXISTS r_ct_sponsor ON ct_trials(sponsor_class);
CREATE INDEX IF NOT EXISTS r_ct_onc ON ct_trials(onc_conditions);

-- Resume log for the ClinicalTrials.gov harvest, one row per calendar-year
-- chunk. The point of this table is that a 14-year harvest is long enough to
-- be interrupted, and a restart must not re-download what already landed or
-- (worse) discard it. `done=1` means every page of that chunk was written and
-- committed; a chunk that died mid-page stays done=0 and is re-fetched whole
-- on the next run, which is safe because nct_id is the primary key and the
-- writes are INSERT OR REPLACE.
--
-- `phases` records, per chunk, whether the Phase-1/2/3 narrowing was applied.
-- It exists so the question "is this table one population or two?" is
-- answerable from the database itself rather than from a prose note that a
-- later run could overwrite. SUM(phases) must be 0 for the table to be a
-- single population.
CREATE TABLE IF NOT EXISTS ct_chunks(
    chunk TEXT PRIMARY KEY, start TEXT, end TEXT,
    expected INTEGER, n INTEGER, phases INTEGER, done INTEGER, captured TEXT);

-- Provenance / run log, one row per sources.yml id.
CREATE TABLE IF NOT EXISTS sources(
    id TEXT PRIMARY KEY, name TEXT, endpoint TEXT, kind TEXT,
    n INTEGER, captured TEXT, first_month TEXT, last_month TEXT,
    ok INTEGER, note TEXT);
"""

# CREATE TABLE IF NOT EXISTS is a no-op on a database that already exists,
# so columns added to SCHEMA after the first run have to be walked in by
# hand. Order here must match the tail of the CREATE TABLE above, because
# ADD COLUMN appends and the INSERTs are positional.
MIGRATIONS = {
    "fda_approvals": [("date_source", "TEXT")],
    "ct_trials": [("brief_summary", "TEXT"), ("arm_labels", "TEXT"),
                  ("arm_descriptions", "TEXT"),
                  ("arm_interventions", "TEXT")],
}


def migrate(con) -> None:
    """Add any SCHEMA column the on-disk table predates. Idempotent."""
    for table, cols in MIGRATIONS.items():
        have = {r[1] for r in con.execute(f"PRAGMA table_info({table})")}
        if not have:
            continue  # table does not exist yet; SCHEMA just created it right
        for name, decl in cols:
            if name not in have:
                con.execute(f"ALTER TABLE {table} ADD COLUMN {name} {decl}")
    con.commit()
    backfill_date_source(con)


def backfill_date_source(con) -> int:
    """Re-derive date_source / date_confirmed for pre-split fda_approvals rows.

    Rows written before the split carry date_confirmed=0 for two different
    situations, and leaving them that way would make the new NULL bucket
    mean "written recently" rather than "no prose date". The notice text is
    stored in `description`, so the same DESC_DATE regex the harvester uses
    can be replayed offline -- no refetch, and the 192 existing rows keep
    their identity. Idempotent: only touches rows with date_source unset.
    """
    todo = con.execute("SELECT url, description, posted_date FROM fda_approvals "
                       "WHERE date_source IS NULL").fetchall()
    if not todo:
        return 0
    upd = []
    for url, desc, posted in todo:
        m = DESC_DATE.search(desc or "")
        acted = prose_date(m.group(1)) if m else ""
        upd.append(("prose" if acted else "posted",
                    int(acted == posted) if acted else None, url))
    con.executemany("UPDATE fda_approvals SET date_source=?, date_confirmed=? "
                    "WHERE url=?", upd)
    con.commit()
    return len(upd)

# The roster is deliberately absent from this view.
EVENTS_VIEW = """
DROP VIEW IF EXISTS events;
CREATE VIEW events AS
    SELECT source_id, 'fda-approval' AS kind, date, month,
           title, url FROM fda_approvals
    UNION ALL
    SELECT source_id, 'ema-authorisation', date, month, name, url
      FROM ema_medicines WHERE date <> ''
    UNION ALL
    SELECT source_id, 'trial-first-posted', date, month, title, url
      FROM ct_trials;
"""

WS = re.compile(r"\s+")
# "On August 26, 2026, the Food and Drug Administration approved
#  daraxonrasib (RASONQUE, Revolution Medicines, Inc.), ..."
DESC_DATE = re.compile(
    r"On\s+([A-Z][a-z]+\s+\d{1,2},\s+\d{4})", re.I)
DESC_DRUG = re.compile(
    r"\b(?:approved|granted\s+accelerated\s+approval\s+to|granted"
    r"\s+traditional\s+approval\s+to)\s+([a-z][a-z0-9\-]*(?:\s+[a-z][a-z0-9\-]*)"
    r"{0,3}?)\s*\(", re.I)


def clean(text: str) -> str:
    return WS.sub(" ", html.unescape(text or "")).strip()


# --------------------------------------------------------------------------
# network


def fetch(url: str, tries: int = 5, timeout: int = 90) -> bytes | None:
    """GET with retry-and-backoff. Returns None once the budget is spent."""
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    for i in range(tries):
        try:
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                return resp.read()
        except urllib.error.HTTPError as exc:
            # 4xx other than 429 will not fix themselves.
            if exc.code != 429 and 400 <= exc.code < 500:
                print(f"  HTTP {exc.code} on {url[:90]}", flush=True)
                return None
            time.sleep(2.0 * (i + 1))
        except Exception:  # noqa: BLE001 - retry anything, report at the call site
            time.sleep(2.0 * (i + 1))
    return None


def fetch_json(url: str, tries: int = 5):
    raw = fetch(url, tries=tries)
    if raw is None:
        return None
    try:
        return json.loads(raw)
    except ValueError:
        return None


# --------------------------------------------------------------------------
# stdlib HTML table reader


class TableReader(HTMLParser):
    """Collect the first <table> as rows of (cell text, first href).

    Deliberately minimal: both FDA pages are one server-rendered table with
    no nesting, which is exactly the case where a full parser earns nothing.
    """

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.rows: list[list[tuple[str, str]]] = []
        self._in_table = False
        self._done = False
        self._row: list[tuple[str, str]] | None = None
        self._cell: list[str] | None = None
        self._href = ""

    def handle_starttag(self, tag, attrs):
        if self._done:
            return
        a = dict(attrs)
        if tag == "table" and not self._in_table:
            self._in_table = True
        elif not self._in_table:
            return
        elif tag == "tr":
            self._row = []
        elif tag in ("td", "th"):
            self._cell, self._href = [], ""
        elif tag == "a" and self._cell is not None and not self._href:
            self._href = a.get("href", "")

    def handle_endtag(self, tag):
        if not self._in_table or self._done:
            return
        if tag in ("td", "th") and self._cell is not None:
            if self._row is not None:
                self._row.append((clean("".join(self._cell)), self._href))
            self._cell = None
        elif tag == "tr" and self._row is not None:
            if self._row:
                self.rows.append(self._row)
            self._row = None
        elif tag == "table":
            self._in_table, self._done = False, True

    def handle_data(self, data):
        if self._cell is not None:
            self._cell.append(data)


def read_table(raw: bytes) -> list[list[tuple[str, str]]]:
    p = TableReader()
    p.feed(raw.decode("utf-8", "replace"))
    p.close()
    return p.rows


def absolute(href: str) -> str:
    return urllib.parse.urljoin("https://www.fda.gov/", href) if href else ""


# --------------------------------------------------------------------------
# source 1: FDA oncology approvals (event stream)


MONTHS = {m: i for i, m in enumerate(
    ["january", "february", "march", "april", "may", "june", "july",
     "august", "september", "october", "november", "december"], 1)}


def us_date(text: str) -> str:
    """'8/26/2026' -> '2026-08-26'. Returns '' on anything else."""
    m = re.fullmatch(r"\s*(\d{1,2})/(\d{1,2})/(\d{4})\s*", text or "")
    if not m:
        return ""
    mo, da, yr = (int(x) for x in m.groups())
    try:
        return dt.date(yr, mo, da).isoformat()
    except ValueError:
        return ""


def prose_date(text: str) -> str:
    """'August 26, 2026' -> '2026-08-26'. Returns '' on anything else."""
    m = re.fullmatch(r"([A-Za-z]+)\s+(\d{1,2}),\s+(\d{4})", (text or "").strip())
    if not m or m.group(1).lower() not in MONTHS:
        return ""
    try:
        return dt.date(int(m.group(3)), MONTHS[m.group(1).lower()],
                       int(m.group(2))).isoformat()
    except ValueError:
        return ""


def classify(title: str) -> str:
    t = title.lower()
    if "accelerated approval" in t:
        return "accelerated approval"
    if "withdraw" in t:
        return "withdrawal"
    if "expand" in t:
        return "label expansion"
    if re.search(r"\bapprov", t):
        return "approval"
    if "d.i.s.c.o" in t or "burst edition" in t:
        return "disco summary"
    return "other"


def harvest_fda_approvals(con, sid: str, captured: str) -> tuple[int, str]:
    raw = fetch(FDA_ONC)
    if raw is None:
        return 0, "fetch failed after retries"
    rows = read_table(raw)
    if not rows:
        return 0, "no <table> found in response"

    out, undated, agree, checked, moved = [], 0, 0, 0, 0
    for cells in rows:
        if len(cells) < 3:
            continue
        title, href = cells[0]
        desc = cells[1][0]
        posted = us_date(cells[2][0])
        if not posted:
            # The <thead> row lands here, as would any format change.
            undated += 1
            continue
        url = absolute(href) or f"fda-onc:{title[:80]}"

        # Prefer the approval date the notice states about itself; the
        # column date is when FDA published the page, up to weeks later.
        dm = DESC_DATE.search(desc)
        acted = prose_date(dm.group(1)) if dm else ""
        # NULL, not 0, when there was no prose date: "the dates disagree" and
        # "there was no second date to compare" are different facts and only
        # the first says anything about FDA's posting lag. See the schema.
        confirmed = None
        if acted:
            checked += 1
            confirmed = int(acted == posted)
            agree += confirmed
            moved += int(acted[:7] != posted[:7])
        date = acted or posted

        gm = DESC_DRUG.search(desc)
        out.append((url, sid, date, date[:7], posted, classify(title),
                    (gm.group(1).strip() if gm else ""), title, desc,
                    confirmed, "prose" if acted else "posted"))

    con.execute("DELETE FROM fda_approvals WHERE source_id=?", (sid,))
    con.executemany(
        "INSERT OR REPLACE INTO fda_approvals VALUES (?,?,?,?,?,?,?,?,?,?,?)",
        out)
    con.commit()
    named = sum(1 for r in out if r[6])
    note = (f"binned on the approval date stated in each notice, not the "
            f"page's posting date; {agree}/{checked} agree, {moved} landed in "
            f"a different month; {len(out) - checked} rows had no prose date "
            f"and fall back to the posting date (date_source='posted', "
            f"date_confirmed NULL); drug name parsed for "
            f"{named}/{len(out)}; {undated - 1} non-header rows undated")
    return len(out), note


# --------------------------------------------------------------------------
# source 2: FDA cellular & gene therapy (state roster -- NO dates)


def harvest_fda_cgt(con, sid: str, captured: str) -> tuple[int, str]:
    raw = fetch(FDA_CGT)
    if raw is None:
        return 0, "fetch failed after retries"
    rows = read_table(raw)
    if not rows:
        return 0, "no <table> found in response"

    out = []
    for cells in rows:
        if len(cells) < 2:
            continue
        product, href = cells[0]
        manufacturer = cells[1][0]
        if not product or product.lower().startswith("product"):
            continue  # header row
        # "ABECMA (idecabtagene vicleucel)" -> trade name + generic name
        m = re.match(r"^(.*?)\s*\((.*)\)\s*$", product)
        trade, generic = (m.group(1), m.group(2)) if m else (product, "")
        out.append((product, sid, captured, trade.strip(), generic.strip(),
                    manufacturer, absolute(href)))

    con.execute("DELETE FROM fda_cgt_roster WHERE source_id=?", (sid,))
    con.executemany(
        "INSERT OR REPLACE INTO fda_cgt_roster VALUES (?,?,?,?,?,?,?)", out)
    con.commit()
    return len(out), ("state roster, not an event stream: the source table has "
                      "no date column, so rows carry only `captured` and are "
                      "excluded from the `events` view")


# --------------------------------------------------------------------------
# source 3: EMA medicines output workbook (event stream)


XL = "{http://schemas.openxmlformats.org/spreadsheetml/2006/main}"
EPOCH = dt.date(1899, 12, 30)  # Excel's 1900 system, with its leap-year bug


def col_index(ref: str) -> int:
    letters = re.match(r"[A-Z]+", ref or "A").group(0)
    n = 0
    for ch in letters:
        n = n * 26 + ord(ch) - 64
    return n - 1


def read_xlsx(raw: bytes) -> list[list[str]]:
    """Read sheet1 of an xlsx into a dense list of rows of strings."""
    z = zipfile.ZipFile(io.BytesIO(raw))
    shared: list[str] = []
    if "xl/sharedStrings.xml" in z.namelist():
        for si in ET.fromstring(z.read("xl/sharedStrings.xml")):
            shared.append("".join(t.text or "" for t in si.iter(XL + "t")))

    def value(cell) -> str:
        t = cell.get("t")
        if t == "inlineStr":
            return "".join(x.text or "" for x in cell.iter(XL + "t"))
        v = cell.find(XL + "v")
        if v is None or v.text is None:
            return ""
        if t == "s":
            i = int(v.text)
            return shared[i] if 0 <= i < len(shared) else ""
        return v.text

    rows = []
    for row in ET.fromstring(z.read("xl/worksheets/sheet1.xml")).iter(XL + "row"):
        cells = {col_index(c.get("r", "A")): value(c) for c in row}
        width = (max(cells) + 1) if cells else 0
        rows.append([clean(cells.get(i, "")) for i in range(width)])
    return rows


def ema_date(text: str) -> str:
    """EMA writes dd/mm/yyyy. Also tolerate a raw Excel serial number."""
    text = (text or "").strip()
    if not text:
        return ""
    m = re.fullmatch(r"(\d{1,2})/(\d{1,2})/(\d{4})", text)
    if m:
        da, mo, yr = (int(x) for x in m.groups())
        try:
            return dt.date(yr, mo, da).isoformat()
        except ValueError:
            return ""
    if re.fullmatch(r"\d+(\.\d+)?", text):
        try:
            return (EPOCH + dt.timedelta(days=int(float(text)))).isoformat()
        except (ValueError, OverflowError):
            return ""
    return ""


def yn(text: str) -> int:
    return int((text or "").strip().lower() in ("yes", "y", "true", "1"))


def harvest_ema(con, sid: str, captured: str) -> tuple[int, str]:
    raw = fetch(EMA_XLSX, timeout=180)
    if raw is None:
        return 0, ("fetch failed after retries -- note that the sources.yml "
                   "endpoint /en/medicines is a JavaScript shell and can never "
                   "be scraped; this harvester uses the nightly xlsx export")
    if not raw.startswith(b"PK"):
        return 0, f"response was not an xlsx (first bytes {raw[:16]!r})"
    try:
        rows = read_xlsx(raw)
    except Exception as exc:  # noqa: BLE001 - surface the reason, do not guess
        return 0, f"xlsx parse failed: {exc.__class__.__name__}: {exc}"

    # The sheet has ~8 rows of agency letterhead before the real header.
    head = next((i for i, r in enumerate(rows)
                 if r and r[0].strip() == "Category"), -1)
    if head < 0:
        return 0, "header row ('Category') not found in the workbook"
    idx = {name.replace("\n", " ").strip(): i
           for i, name in enumerate(rows[head]) if name.strip()}

    def col(row: list[str], name: str) -> str:
        i = idx.get(name, -1)
        return row[i] if 0 <= i < len(row) else ""

    required = ["Name of medicine", "EMA product number",
                "Marketing authorisation date"]
    missing = [c for c in required if c not in idx]
    if missing:
        return 0, f"workbook layout changed, missing columns: {missing}"

    out, vet, seen = [], 0, set()
    for row in rows[head + 1:]:
        if not any(row):
            continue
        if col(row, "Category").strip().lower() != "human":
            vet += 1
            continue
        pnum = col(row, "EMA product number") or col(row, "Name of medicine")
        if not pnum or pnum in seen:
            continue
        seen.add(pnum)
        date = ema_date(col(row, "Marketing authorisation date"))
        area = col(row, "Therapeutic area (MeSH)")
        atc = col(row, "ATC code (human)")
        onc = int(bool(ONC_RE.search(area))
                  or atc.upper().startswith(("L01", "L02")))
        out.append((
            pnum, sid, date, date[:7],
            col(row, "Name of medicine"),
            col(row, "International non-proprietary name (INN) / common name"),
            col(row, "Active substance"), area, atc, col(row, "Medicine status"),
            yn(col(row, "Orphan medicine")), yn(col(row, "Conditional approval")),
            yn(col(row, "Accelerated assessment")),
            yn(col(row, "PRIME: priority medicine")),
            yn(col(row, "Advanced therapy")), onc,
            col(row, "Marketing authorisation developer / applicant / holder"),
            ema_date(col(row, "Opinion adopted date")),
            ema_date(col(row, "European Commission decision date")),
            ema_date(col(row, "Refusal of marketing authorisation date")),
            ema_date(col(row, "Withdrawal / expiry / revocation / lapse of "
                              "marketing authorisation date")),
            col(row, "Therapeutic indication")[:4000],
            col(row, "Medicine URL"), captured))

    con.execute("DELETE FROM ema_medicines WHERE source_id=?", (sid,))
    con.executemany("INSERT OR REPLACE INTO ema_medicines VALUES ("
                    + ",".join("?" * 24) + ")", out)
    con.commit()
    dated = sum(1 for r in out if r[2])
    onc_n = sum(r[15] for r in out)
    return len(out), (f"nightly xlsx export, not the JS page in sources.yml; "
                      f"{dated} have a marketing authorisation date, "
                      f"{onc_n} flagged oncology; {vet} veterinary rows dropped")


# --------------------------------------------------------------------------
# source 4: ClinicalTrials.gov API v2 (event stream)


def ct_advanced(start: str, end: str, phases: bool) -> str:
    end_day = last_day(end)
    q = (f"AREA[StudyFirstPostDate]RANGE[{start}-01,{end_day}] "
         f"AND AREA[StudyType]INTERVENTIONAL")
    if phases:
        q += " AND AREA[Phase](PHASE1 OR PHASE2 OR PHASE3)"
    return q


def last_day(month: str) -> str:
    y, m = int(month[:4]), int(month[5:7])
    nxt = dt.date(y + (m == 12), 1 if m == 12 else m + 1, 1)
    return (nxt - dt.timedelta(days=1)).isoformat()


def ct_count(start: str, end: str, phases: bool) -> int | None:
    url = CTGOV + "?" + urllib.parse.urlencode({
        "query.cond": ONC_COND, "filter.advanced": ct_advanced(start, end, phases),
        "countTotal": "true", "pageSize": "1", "fields": "NCTId"})
    page = fetch_json(url)
    return None if page is None else page.get("totalCount")


def year_chunks(start: str, end: str) -> list[tuple[str, str, str]]:
    """Split a YYYY-MM..YYYY-MM window into (label, start, end) calendar years.

    Chunking is not an optimisation, it is the correctness fix. `harvest_ctgov`
    used to probe the count for the WHOLE window and, above --max-trials,
    silently re-issue the query narrowed to Phase 1/2/3. Widening this harvest
    from 44 months to 14 years takes the single-window count from ~24k to ~70k,
    which is over the 40,000 default, so a one-shot run would have tripped that
    branch and rewritten the already-published 2023-2026 years as a
    Phase-1/2/3-only table -- while the 2023+ rows already on disk contain
    PHASE4, NA and EARLY_PHASE1. Every count computed across the combined
    table would then have compared two different populations without saying so.
    The largest calendar year in 2013..2026 is ~6.4k, a sixth of the cap, so
    per-year chunks put the whole harvest structurally out of reach of that
    branch instead of relying on a threshold being generous enough.

    Binning by studyFirstPostDate also makes the chunks genuinely disjoint:
    first-post is the one date ClinicalTrials.gov cannot revise backwards, so
    a trial belongs to exactly one year forever and re-running one chunk can
    never duplicate or strand a row in another.
    """
    out = []
    for y in range(int(start[:4]), int(end[:4]) + 1):
        lo = start if y == int(start[:4]) else f"{y}-01"
        hi = end if y == int(end[:4]) else f"{y}-12"
        out.append((str(y), lo, hi))
    return out


def harvest_ct_chunk(con, sid: str, captured: str, label: str,
                     start: str, end: str, cap: int,
                     allow_narrow: bool) -> tuple[int, int, str]:
    """Download one chunk and commit it page by page. (n, phases, status).

    Rows are written and committed as each page arrives rather than
    accumulated and flushed at the end, so an interruption costs at most the
    page in flight. There is no DELETE anywhere in this function: the old
    whole-table DELETE-then-INSERT meant a run that died at year 7 left the
    table emptier than it found it, which for a multi-hour harvest is the one
    failure mode that must not exist.
    """
    total = ct_count(start, end, phases=False)
    if total is None:
        return 0, 0, "count probe failed after retries"

    phases = False
    if total > cap:
        # Deliberately NOT a silent fallback. Narrowing changes what the table
        # IS, so it now requires --allow-phase-narrowing to be passed by hand
        # and the chunk is abandoned otherwise. A chunk missing from the table
        # is a visible hole; a chunk quietly restricted to Phase 1/2/3 is an
        # invisible one, and only the second kind corrupts a downstream count.
        if not allow_narrow:
            return 0, 0, (f"REFUSED: {total:,} studies exceeds --max-trials "
                          f"{cap:,}; narrowing to Phase 1/2/3 would make this "
                          f"chunk a different population from the rest of the "
                          f"table. Re-run with a higher --max-trials (or "
                          f"--allow-phase-narrowing if you really want a "
                          f"phase-restricted chunk).")
        phases = True
        total = ct_count(start, end, phases=True)
        if total is None:
            return 0, 0, "phase-narrowed count probe failed after retries"

    token, pages, got = None, 0, 0
    while True:
        params = {
            "query.cond": ONC_COND,
            "filter.advanced": ct_advanced(start, end, phases),
            "pageSize": "1000", "fields": CT_FIELDS,
        }
        if token:
            params["pageToken"] = token
        page = fetch_json(CTGOV + "?" + urllib.parse.urlencode(params))
        if page is None:
            return got, int(phases), (f"page {pages + 1} failed after retries; "
                                      f"{got:,}/{total:,} rows committed, chunk "
                                      f"left incomplete for the next run")
        studies = page.get("studies") or []
        if not studies:
            break
        out = []
        for s in studies:
            p = s.get("protocolSection", {})
            ident = p.get("identificationModule", {})
            st = p.get("statusModule", {})
            design = p.get("designModule", {})
            spon = p.get("sponsorCollaboratorsModule", {})
            lead = spon.get("leadSponsor", {})
            date = (st.get("studyFirstPostDateStruct") or {}).get("date", "")
            nct = ident.get("nctId", "")
            if not nct or not date:
                continue
            conds = "; ".join(
                (p.get("conditionsModule") or {}).get("conditions") or [])
            # armGroups and interventions are siblings in the same module.
            # An arm may carry no description at all (single-arm CAR-T
            # studies routinely do), so join only the ones that exist --
            # otherwise every trial gets a string of blank separators that
            # a LIKE '%...%' search cannot tell from real text.
            arms = ((p.get("armsInterventionsModule") or {})
                    .get("armGroups") or [])
            out.append((
                nct, sid, date, date[:7],
                st.get("overallStatus", ""), ident.get("briefTitle", ""),
                conds,
                "; ".join(design.get("phases") or []),
                design.get("studyType", ""),
                lead.get("name", ""), lead.get("class", ""),
                "; ".join(c.get("name", "")
                          for c in (spon.get("collaborators") or [])),
                "; ".join(f"{i.get('type', '')}:{i.get('name', '')}"
                          for i in ((p.get("armsInterventionsModule") or {})
                                    .get("interventions") or [])),
                (design.get("enrollmentInfo") or {}).get("count"),
                (st.get("startDateStruct") or {}).get("date", ""),
                int(bool(ONC_RE.search(conds))),
                f"https://clinicaltrials.gov/study/{nct}",
                ((p.get("descriptionModule") or {})
                 .get("briefSummary", "") or "")[:TEXT_CAP],
                " | ".join(a.get("label", "") for a in arms if a.get("label")),
                " | ".join(a.get("description", "")
                           for a in arms if a.get("description"))[:TEXT_CAP],
                " | ".join("; ".join(a.get("interventionNames") or [])
                           for a in arms if a.get("interventionNames"))))
        # 21 columns; the tuple built above is positional, so this count and
        # the CREATE TABLE have to be recounted together whenever either moves.
        con.executemany(
            "INSERT OR REPLACE INTO ct_trials VALUES ("
            + ",".join("?" * 21) + ")", out)
        con.commit()
        got += len(out)
        pages += 1
        token = page.get("nextPageToken")
        print(f"    {label} page {pages}: {got:,}/{total:,}", flush=True)
        if not token:
            break
        time.sleep(0.2)

    con.execute("INSERT OR REPLACE INTO ct_chunks VALUES (?,?,?,?,?,?,?,?)",
                (label, start, end, total, got, int(phases), 1, captured))
    con.commit()
    return got, int(phases), "ok"


def harvest_ctgov(con, sid: str, captured: str, start: str, end: str,
                  cap: int, allow_narrow: bool = False,
                  refetch: bool = False) -> tuple[int, str]:
    """Harvest the window one calendar year at a time, resumably.

    A re-run is now a MERGE, not the full re-download the old version did.
    Chunks already marked done in ct_chunks are skipped unless --refetch-ct,
    so an interrupted 14-year harvest resumes where it stopped and a rerun
    over a narrower window no longer silently discards the years outside it.
    """
    chunks = year_chunks(start, end)
    done = {r[0] for r in con.execute(
        "SELECT chunk FROM ct_chunks WHERE done=1")} if not refetch else set()

    fetched, skipped, failures = 0, 0, []
    for label, lo, hi in chunks:
        if label in done:
            skipped += 1
            print(f"  {label}: already complete, skipping", flush=True)
            continue
        print(f"  {label}: {lo}..{hi}", flush=True)
        got, ph, status = harvest_ct_chunk(con, sid, captured, label, lo, hi,
                                           cap, allow_narrow)
        fetched += got
        if status != "ok":
            failures.append(f"{label}: {status}")
            print(f"    !! {status}", flush=True)

    # Totals are read back from the table, not accumulated in memory, so they
    # describe what is actually on disk after a resumed or partial run.
    n = con.execute("SELECT COUNT(*) FROM ct_trials").fetchone()[0]
    onc = con.execute("SELECT COUNT(*) FROM ct_trials "
                      "WHERE onc_conditions=1").fetchone()[0]
    prose = con.execute(
        "SELECT COUNT(*) FROM ct_trials WHERE COALESCE(brief_summary,'') <> '' "
        "OR COALESCE(arm_descriptions,'') <> ''").fetchone()[0]
    narrowed = con.execute(
        "SELECT COALESCE(SUM(phases),0) FROM ct_chunks").fetchone()[0]
    lo, hi = con.execute("SELECT MIN(month), MAX(month) FROM ct_trials "
                         "WHERE month <> ''").fetchone()

    note = (f"interventional, studyFirstPostDate in {lo}..{hi}, harvested in "
            f"{len(chunks)} calendar-year chunks ({fetched:,} rows fetched this "
            f"run, {skipped} chunks already complete and skipped); condition "
            f"query widened beyond 'cancer'; {onc:,}/{n:,} name an oncology "
            f"condition outright (onc_conditions=1); {prose:,} carry "
            f"brief_summary or arm-group prose, the fields that name a "
            f"mechanism where `interventions` gives only a code")
    if narrowed:
        note += (f"; WARNING: {narrowed} chunk(s) were narrowed to Phase 1/2/3 "
                 f"and this table is NOT a single population")
    else:
        note += ("; NO phase filter was applied to any chunk (every chunk's "
                 f"count was under --max-trials {cap:,}), so the table is one "
                 "population across all years: PHASE4, NA and EARLY_PHASE1 "
                 "are present throughout")
    if failures:
        note += "; INCOMPLETE -- " + " | ".join(failures)
    return n, note


# --------------------------------------------------------------------------


HANDLERS = {
    "r-fda-oncology-approvals": (
        "FDA Oncology (OCE) approval notifications", FDA_ONC, "event-stream"),
    "r-fda-cellular-gene-therapy": (
        "FDA approved cellular and gene therapy products", FDA_CGT,
        "state-roster"),
    "r-ema-medicines": (
        "EMA medicines register", EMA_XLSX, "event-stream"),
    "r-clinicaltrials-gov": ("ClinicalTrials.gov", CTGOV, "event-stream"),
}

TABLES = {
    "r-fda-oncology-approvals": "fda_approvals",
    "r-fda-cellular-gene-therapy": "fda_cgt_roster",
    "r-ema-medicines": "ema_medicines",
    "r-clinicaltrials-gov": "ct_trials",
}


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--only", default="",
                    help="sources.yml source id to restrict to")
    ap.add_argument("--from", dest="start", default="2013-01",
                    help="ClinicalTrials.gov window start, YYYY-MM")
    ap.add_argument("--to", dest="end", default="2026-08",
                    help="ClinicalTrials.gov window end, YYYY-MM")
    ap.add_argument("--max-trials", type=int, default=40000,
                    help="per-CHUNK ceiling, not a whole-window one; a chunk "
                         "over it is refused, never silently phase-narrowed")
    ap.add_argument("--allow-phase-narrowing", action="store_true",
                    help="opt in to Phase 1/2/3 narrowing for oversized chunks."
                         " Makes the table two populations; do not use.")
    ap.add_argument("--refetch-ct", action="store_true",
                    help="re-download ClinicalTrials.gov chunks already marked "
                         "complete in ct_chunks (default is to resume)")
    ap.add_argument("--rebuild", action="store_true",
                    help="drop every table first instead of per-source refresh")
    args = ap.parse_args()

    if args.only and args.only not in HANDLERS:
        sys.exit(f"unknown source id {args.only!r}; "
                 f"expected one of {', '.join(SOURCES)}")

    DB.parent.mkdir(parents=True, exist_ok=True)
    con = sqlite3.connect(DB)
    if args.rebuild:
        con.executescript(
            "DROP VIEW IF EXISTS events;"
            + "".join(f"DROP TABLE IF EXISTS {t};" for t in TABLES.values())
            + "DROP TABLE IF EXISTS ct_chunks;"
            + "DROP TABLE IF EXISTS sources;")
    con.executescript(SCHEMA)
    migrate(con)

    captured = dt.date.today().isoformat()
    todo = [s for s in SOURCES if not args.only or s == args.only]

    for sid in todo:
        name, endpoint, kind = HANDLERS[sid]
        print(f"\n{sid}  ({kind})", flush=True)
        if sid == "r-fda-oncology-approvals":
            n, note = harvest_fda_approvals(con, sid, captured)
        elif sid == "r-fda-cellular-gene-therapy":
            n, note = harvest_fda_cgt(con, sid, captured)
        elif sid == "r-ema-medicines":
            n, note = harvest_ema(con, sid, captured)
        else:
            n, note = harvest_ctgov(con, sid, captured,
                                    args.start, args.end, args.max_trials,
                                    args.allow_phase_narrowing,
                                    args.refetch_ct)

        table = TABLES[sid]
        if kind == "event-stream":
            lo, hi = con.execute(
                f"SELECT MIN(month), MAX(month) FROM {table} "
                f"WHERE source_id=? AND month<>''", (sid,)).fetchone()
        else:
            lo = hi = None
        con.execute("INSERT OR REPLACE INTO sources VALUES (?,?,?,?,?,?,?,?,?,?)",
                    (sid, name, endpoint, kind, n, captured, lo, hi,
                     int(n > 0), note))
        con.commit()
        status = f"{n:,} rows" if n else "FAILED / empty"
        print(f"  {status}  -- {note}", flush=True)

    con.executescript(EVENTS_VIEW)
    con.commit()

    # ---------------- summary -------------------------------------------
    print()
    print(f"{'source id':30} {'kind':13} {'rows':>8} {'months':>18}  ok")
    print("-" * 82)
    for sid, kind, n, lo, hi, ok in con.execute(
            "SELECT id, kind, n, first_month, last_month, ok "
            "FROM sources ORDER BY id"):
        span = f"{lo}..{hi}" if lo else ("no dates (roster)"
                                         if kind == "state-roster" else "-")
        print(f"{sid:30} {kind:13} {n or 0:8,} {span:>18}  "
              f"{'yes' if ok else 'NO'}")

    print()
    print(f"{'year':6} {'fda':>8} {'ema':>8} {'trials':>9} {'all events':>12}")
    years = con.execute(
        "SELECT substr(month,1,4) AS y, "
        " SUM(kind='fda-approval'), SUM(kind='ema-authorisation'), "
        " SUM(kind='trial-first-posted'), COUNT(*) "
        "FROM events WHERE month<>'' GROUP BY y "
        "HAVING y>='2013' ORDER BY y").fetchall()
    for y, f, e, t, all_ in years:
        print(f"{y:6} {f:8,} {e:8,} {t:9,} {all_:12,}")
    pre = con.execute("SELECT COUNT(*) FROM events "
                      "WHERE month<>'' AND month<'2013-01'").fetchone()[0]
    print(f"{'<2013':6} {'':8} {'':8} {'':9} {pre:12,}")
    total = con.execute("SELECT COUNT(*) FROM events").fetchone()[0]
    roster = con.execute("SELECT COUNT(*) FROM fda_cgt_roster").fetchone()[0]
    print(f"\n{total:,} dated events in the `events` view; "
          f"{roster:,} products in the roster table (undated, by design)")
    print(f"-> {DB}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
