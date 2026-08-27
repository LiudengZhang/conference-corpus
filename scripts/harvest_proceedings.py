#!/usr/bin/env python3
"""Harvest the conference venues that Crossref does not carry.

`harvest_conference.py` gets its abstracts from Crossref, which works
only where a publisher deposits each meeting abstract as its own record.
That covers the oncology congresses (AACR, ASCO, the ESMO family, USCAP)
and nothing else. The computational and immunotherapy meetings this
corpus also cares about publish their programmes as web pages, proceedings
volumes or a single PDF, and Crossref either never sees them or sees only
one lump record standing for the whole abstract book. This script picks
those up. It writes into the same `abstracts`/`venues` tables, one
`DELETE FROM abstracts WHERE venue=?` followed by inserts per venue, so
re-running it is safe and never touches the Crossref-sourced rows.

Six routes, one per publishing habit:

  * PMLR volume (chil-2026). The AHLI Conference on Health, Inference and
    Learning publishes through Proceedings of Machine Learning Research.
    The volume index lists every paper in a `div class="paper"` block; the
    abstract lives only on the per-paper detail page, in
    `div id="abstract"`. PMLR stamps one `citation_publication_date` on
    the whole volume (2026-06-29 for v333), so that date is a volume-level
    date that happens to fall inside the meeting -- it is not a per-paper
    presentation date.

  * Conference website with inline abstracts (mlhc-2026, bioc-2026,
    eurobioc-2026). All three hide the abstract inside an HTML
    `<details>` element whose `<summary>` is the title, which is why a
    naive tag-strip yields "TitleAbstract text..." run together. Each
    also carries the real session date in the page: MLHC in a
    `p.session-time` line per poster session, the two Bioconductor
    schedules in a `colspan=4` day-header row. Those give genuine
    per-paper dates.

    MLHC deserves a note. Its PMLR volume for 2026 does not exist yet --
    the index goes v298 (MLHC 2025) and stops -- so the conference site is
    the only route, and it is a better one anyway because it carries the
    clinical-abstract track that PMLR never publishes.

  * OJS issue pages (aaai-2026). AAAI-26 proceedings are 48 OJS issues.
    AAAI is a general AI conference and ingesting all ~3,000 papers would
    swamp the corpus, so the venue is cut down by one written rule stated
    in `AAAI_ISSUES` and `BIOMED` below and nowhere else: four
    application-oriented tracks, then a fixed biomedical vocabulary applied
    to title and abstract. The issue page gives title, authors and article
    id but not the abstract, so each kept issue costs one page per article.
    Trap: ojs.aaai.org gzips the response body even though urllib never
    sends `Accept-Encoding`, and sets no `Content-Encoding` header, so the
    bytes have to be sniffed for the gzip magic number. Second trap: the
    OJS `citation_date` is when the proceedings were posted (2026-03), not
    when the meeting ran (2026-01-20..27); the meeting date is what a
    lead-time corpus needs, so that is what is stored.

  * PDF abstract book (cimt-2026). CIMT deposits nothing anywhere; the
    only artefact is a 158-page abstract book linked from the
    call-for-abstracts page, not from the programme page. Text is
    recovered from the Flate-compressed content streams with the stdlib.
    The reliable structure is not the prose -- abstract numbers collide
    with "2 Gy" and with affiliation superscripts -- but the font runs:
    the Word export uses F3/18pt for the session header, F1/12pt for the
    abstract number, F4/13.98pt for the title, F1/5.52pt for affiliation
    superscripts and F1/9pt for body text, consistently across all 159
    pages. Records are cut on an F1/12pt numeric run followed by an
    F4/13.98pt run. The body begins after the last superscript run; the
    tail of the final affiliation runs into it with no space
    ("...GermanyRadiotherapy can elicit..."), which is exactly why the
    lowercase-to-uppercase seam is used to trim it. Also: 51 posters are
    scheduled in both poster sessions and so appear twice under the same
    number; those are deduplicated on (number, title).

Three venues were checked and produce nothing. They are recorded in
`venues` with n=0 and a note rather than silently dropped, because "we
looked and there is nothing there" is a finding:

  * midl-2026. OpenReview's `/notes` endpoint now answers
    `ChallengeRequiredError` with HTTP 403 to any unauthenticated client,
    for every venue, not just MIDL -- `?limit=1` with no filter 403s too.
    `/groups` and `/notes/search` still answer, which is how the venue was
    confirmed to exist (title "Medical Imaging with Deep Learning",
    Taipei, start Jul 08 2026) and to be closed (`public_submissions:
    false`). The conference site publishes no paper list.

  * asgct-2026. Molecular Therapy 2026 has exactly one record for the
    meeting, `10.1016/j.ymthe.2026.04.047`, "ASGCT 2026 Annual Meeting
    Abstracts", pages 1-3610 -- the entire supplement as a single item.
    Mol Ther Methods Clin Dev has no 2026 records at all.

  * eacr-2026. Molecular Oncology 2026 likewise: `10.1002/mol2.v20.s1`
    (the issue) and `10.1002/1878-0261.70318` titled "Abstracts",
    pages 1-692. No individual abstracts are deposited.

  * scverse-2026 is scheduled for 2026-10-12..14 in Copenhagen and has
    not happened; registration is still open. Not attempted.

Usage:
    python3 scripts/harvest_proceedings.py
    python3 scripts/harvest_proceedings.py --only chil-2026
    python3 scripts/harvest_proceedings.py --rebuild-venue cimt-2026
"""

from __future__ import annotations

import argparse
import datetime as dt
import gzip
import html
import pathlib
import re
import sqlite3
import sys
import time
import urllib.error
import urllib.request
import zlib
from dataclasses import dataclass, field

ROOT = pathlib.Path(__file__).resolve().parent.parent
DB = ROOT / "data" / "conference.sqlite"

MAILTO = "liudengzhang91@gmail.com"
UA = f"conference-corpus/1.0 (mailto:{MAILTO})"

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
SLUG_BAD = re.compile(r"[^a-z0-9]+")


def clean(text: str) -> str:
    """Strip tags and collapse whitespace, as harvest_conference.py does."""
    return WS.sub(" ", html.unescape(TAG.sub(" ", text or ""))).strip()


def slug(text: str, n: int = 60) -> str:
    return SLUG_BAD.sub("-", (text or "").lower()).strip("-")[:n]


# --------------------------------------------------------------------------
# fetching
# --------------------------------------------------------------------------

def fetch(url: str, tries: int = 4) -> bytes | None:
    """GET with a contact User-Agent, retry-with-backoff, gzip sniffing.

    ojs.aaai.org returns a gzip body with no Content-Encoding header, so
    the magic number is checked rather than the header.
    """
    req = urllib.request.Request(url, headers={
        "User-Agent": UA, "Accept": "*/*"})
    for i in range(tries):
        try:
            body = urllib.request.urlopen(req, timeout=90).read()
            if body[:2] == b"\x1f\x8b":
                body = gzip.decompress(body)
            return body
        except urllib.error.HTTPError as exc:
            # 4xx other than 429 will not improve by waiting.
            if exc.code not in (429, 500, 502, 503, 504):
                return None
            time.sleep(2.0 * (i + 1))
        except Exception:  # noqa: BLE001 - retry anything, report below
            time.sleep(2.0 * (i + 1))
    return None


def get_text(url: str, tries: int = 4) -> str:
    body = fetch(url, tries)
    return body.decode("utf-8", "replace") if body else ""


# --------------------------------------------------------------------------
# venue registry
# --------------------------------------------------------------------------

@dataclass
class Venue:
    """One meeting plus how to reach its programme."""

    id: str
    name: str
    year: int
    route: str
    start: str                       # meeting first day, YYYY-MM-DD
    end: str                         # meeting last day, YYYY-MM-DD
    harvester: str = ""              # name of the harvest_* function
    issn: str = ""
    confirmed: bool = True
    note: str = ""
    rows: list = field(default_factory=list, repr=False)
    status: str = "pending"


VENUES = [
    Venue("chil-2026", "AHLI Conference on Health, Inference and Learning 2026",
          2026, "pmlr:v333", "2026-06-28", "2026-06-30", "harvest_chil",
          issn="2640-3498",
          note="PMLR volume 333. Date is the volume-level PMLR publication "
               "date 2026-06-29, identical on all 40 papers and inside the "
               "meeting window; not a per-paper presentation date."),
    Venue("mlhc-2026", "Machine Learning for Healthcare 2026",
          2026, "mlforhc.org/accepted-*", "2026-08-12", "2026-08-14",
          "harvest_mlhc",
          note="No PMLR volume for 2026 exists yet (index stops at v298 = "
               "MLHC 2025). Harvested from the conference site, which also "
               "carries the clinical-abstract track PMLR never publishes. "
               "Dates are the real per-poster-session dates."),
    Venue("aaai-2026", "AAAI-40 (AAAI-26) -- biomedical subset",
          2026, "ojs.aaai.org issues 683,684,727,728 + biomedical vocabulary",
          "2026-01-20", "2026-01-27", "harvest_aaai",
          note="Deliberate subset, not the whole conference. Two filters, "
               "applied uniformly: (1) only the four application-oriented "
               "tracks -- Application Domains I/II and AI for Social Impact "
               "I/II; the other 44 method tracks are excluded wholesale. "
               "(2) title or abstract must match the fixed BIOMED vocabulary "
               "in this script. Date is the meeting start date, not the OJS "
               "posting date (2026-03)."),
    Venue("bioc-2026", "Bioconductor Conference 2026 (North America)",
          2026, "bioc2026.bioconductor.org/schedule/",
          "2026-08-10", "2026-08-14", "harvest_bioc",
          note="Schedule table; per-day dates come from the day-header rows. "
               "Talks with an inline abstract are a subset -- keynotes, "
               "workshops and community sessions are title-only."),
    Venue("eurobioc-2026", "European Bioconductor Conference 2026",
          2026, "eurobioc2026.bioconductor.org/pages/schedule.html",
          "2026-06-03", "2026-06-05", "harvest_eurobioc",
          note="The blog recap is prose only; the conference site's own "
               "schedule page carries full abstracts in <details> blocks "
               "with real per-day dates, so that is used instead."),
    Venue("cimt-2026", "CIMT 23rd Annual Meeting",
          2026, "abstract-book PDF (font-run parse)",
          "2026-05-11", "2026-05-13", "harvest_cimt",
          note="Book of Abstracts PDF, linked from /call-for-abstracts and "
               "not from the programme page. Parsed from PDF font runs. "
               "Date is meeting-level -- the book carries poster session but "
               "no per-abstract day. 51 posters run in both poster sessions "
               "and are deduplicated on (number, title). Known limitation: "
               "about 24 of 195 abstracts keep a leading fragment of the "
               "author affiliation in the abstract field, because the PDF "
               "text layer marks no boundary between affiliation and body."),
    # --- checked, nothing to harvest ------------------------------------
    Venue("midl-2026", "Medical Imaging with Deep Learning 2026",
          2026, "openreview (blocked)", "2026-07-08", "2026-07-10", "",
          confirmed=False,
          note="UNREACHABLE. OpenReview /notes answers HTTP 403 "
               "ChallengeRequiredError to any unauthenticated client for "
               "every venue, including ?limit=1 with no filter; api.openreview"
               ".net v1 behaves identically. /groups confirms the venue "
               "exists (Taipei, start Jul 08 2026) and sets "
               "public_submissions=false. 2026.midl.io publishes no paper "
               "list, only livestream links."),
    Venue("asgct-2026", "ASGCT 29th Annual Meeting",
          2026, "crossref (lump record only)", "2026-05-12", "2026-05-15", "",
          issn="1525-0016", confirmed=False,
          note="NOT DEPOSITED. Molecular Therapy 2026 carries the meeting as "
               "one record, 10.1016/j.ymthe.2026.04.047 'ASGCT 2026 Annual "
               "Meeting Abstracts', pages 1-3610. Mol Ther Methods Clin Dev "
               "(2329-0501) has zero 2026 records."),
    Venue("eacr-2026", "EACR 2026 Congress",
          2026, "crossref (lump record only)", "2026-06-10", "2026-06-13", "",
          issn="1878-0261", confirmed=False,
          note="NOT DEPOSITED. Molecular Oncology 2026 carries only "
               "10.1002/mol2.v20.s1 (the issue) and 10.1002/1878-0261.70318 "
               "titled 'Abstracts', vol 20 issue S1, pages 1-692."),
    Venue("scverse-2026", "scverse conference 2026",
          2026, "not yet held", "2026-10-12", "2026-10-14", "",
          confirmed=False,
          note="FUTURE. Scheduled 2026-10-12..14 at DTU, Copenhagen; "
               "registration still open at harvest time. Nothing to harvest."),
]


# --------------------------------------------------------------------------
# route 1 -- PMLR volume
# --------------------------------------------------------------------------

PMLR_PAPER = re.compile(
    r'href="(https://proceedings\.mlr\.press/v333/[^"]+\.html)">abs</a>')
PMLR_ABSTRACT = re.compile(
    r'<div id="abstract" class="abstract">(.*?)</div>', re.S)
PMLR_TITLE = re.compile(r'name="citation_title" content="([^"]*)"')
PMLR_DATE = re.compile(r'name="citation_publication_date" content="([^"]*)"')


def harvest_chil(v: Venue) -> list[tuple]:
    index = get_text("https://proceedings.mlr.press/v333/")
    if not index:
        return []
    urls = []
    for url in PMLR_PAPER.findall(index):
        if url not in urls:
            urls.append(url)
    rows = []
    for url in urls:
        page = get_text(url)
        time.sleep(0.7)
        if not page:
            continue
        title = clean(html.unescape(
            PMLR_TITLE.search(page).group(1) if PMLR_TITLE.search(page) else ""))
        body = PMLR_ABSTRACT.search(page)
        m = PMLR_DATE.search(page)
        date = m.group(1).replace("/", "-") if m else v.start
        if not title:
            continue
        rows.append((url.lower(), v.id, v.year, date, date[:7], "",
                     title, clean(body.group(1)) if body else "",
                     int(v.confirmed)))
    return rows


# --------------------------------------------------------------------------
# route 2 -- conference sites with <details> abstracts
# --------------------------------------------------------------------------

MLHC_SECTION = re.compile(
    r'<section class="poster-session">(.*?)</section>', re.S)
MLHC_HEAD = re.compile(r"<h3>(.*?)</h3>", re.S)
MLHC_TIME = re.compile(r'<p class="session-time">(.*?)</p>', re.S)
MLHC_ITEM = re.compile(r"<details>(.*?)</details>", re.S)
MLHC_TITLE = re.compile(r'<span class="paper-title">(.*?)</span>', re.S)
MLHC_BODY = re.compile(r'<div class="abstract-body">(.*?)</div>', re.S)
# Three date dialects appear across these sites and all three land here:
#   MLHC       "Thursday August 13, 2026, 11:00 AM - 12:15 PM"
#   Bioc NA    "Monday, August 10"          (year appended by the caller)
#   EuroBioc   "Wed. - Jun. 03, '26"        (abbreviated month, 2-digit year)
LONGDATE = re.compile(
    r"([A-Za-z]{3,9})\.?\s+(\d{1,2})(?:st|nd|rd|th)?,?\s*[’']?(\d{2,4})\b")
_NAMES = ["january", "february", "march", "april", "may", "june", "july",
          "august", "september", "october", "november", "december"]
MONTHS = {n: i + 1 for i, n in enumerate(_NAMES)}
MONTHS.update({n[:3]: i + 1 for i, n in enumerate(_NAMES)})


def parse_longdate(text: str, fallback: str) -> str:
    for m in LONGDATE.finditer(text or ""):
        month = MONTHS.get(m.group(1).lower())
        if not month:
            continue
        year = int(m.group(3))
        if year < 100:
            year += 2000
        return "%04d-%02d-%02d" % (year, month, int(m.group(2)))
    return fallback


def harvest_mlhc(v: Venue) -> list[tuple]:
    rows = []
    pages = [("research", "https://www.mlforhc.org/accepted-research-papers"),
             ("clinical", "https://www.mlforhc.org/accepted-clinical-abstracts")]
    for track, url in pages:
        page = get_text(url)
        time.sleep(1.0)
        if not page:
            continue
        for block in MLHC_SECTION.findall(page):
            head = MLHC_HEAD.search(block)
            name = clean(head.group(1)) if head else ""
            when = MLHC_TIME.search(block)
            date = parse_longdate(clean(when.group(1)) if when else "", v.start)
            session = f"{name} ({track})" if name else track
            for item in MLHC_ITEM.findall(block):
                t = MLHC_TITLE.search(item)
                title = clean(t.group(1)) if t else ""
                if not title:
                    continue
                body = MLHC_BODY.search(item)
                rows.append((f"mlhc-2026:{track}/{slug(title)}", v.id, v.year,
                             date, date[:7], session, title,
                             clean(body.group(1)) if body else "",
                             int(v.confirmed)))
    return rows


TOKEN = re.compile(r"<h[1-6][^>]*>(.*?)</h[1-6]>|<tr[^>]*>(.*?)</tr>", re.S)
CELL = re.compile(r"<t[dh][^>]*>(.*?)</t[dh]>", re.S)
SPAN4 = re.compile(r'<td colspan="4"[^>]*>(.*?)</td>', re.S)
DETAILS = re.compile(r"<details[^>]*>(.*?)</details>", re.S)
SUMMARY = re.compile(r"<summary[^>]*>(.*?)</summary>", re.S)
AUTHORS_DIV = re.compile(
    r'<div class="schedule-details-authors">.*?</div>', re.S)


def split_details(cell: str) -> tuple[str, str]:
    """Return (title, abstract) for a table cell that may hold <details>.

    Both Bioconductor schedules and MLHC put the title in <summary> and the
    abstract in the sibling div. Stripping tags first would weld them into
    one string with no separator, which is the trap here.
    """
    d = DETAILS.search(cell)
    if not d:
        return clean(cell), ""
    inner = d.group(1)
    s = SUMMARY.search(inner)
    title = clean(s.group(1)) if s else ""
    body = inner[s.end():] if s else inner
    # EuroBioc repeats the author list in its own div ahead of the
    # abstract. It has to be dropped on the markup, not on the text: an
    # "Author(s): ... ." rule cuts at the period in "Thomaz F.S." and eats
    # the abstract's opening sentence.
    body = AUTHORS_DIV.sub("", body)
    return title, clean(body)


def harvest_schedule(v: Venue, url: str) -> list[tuple]:
    """Shared parser for the two Bioconductor schedule pages.

    Both interleave two table shapes in one document and both must be
    walked in document order, because the day a row belongs to is carried
    by whatever came *before* it:

      * the programme table is four columns (time / type / author / title)
        with `colspan=4` day-header rows, and leaves time and type blank on
        continuation rows, so the last non-blank value is carried forward;
      * the poster tables are two columns (author / title). Bioc-NA drops
        them straight after the Monday "Poster session" row and gives them
        no header of their own, so they inherit the running date;
        EuroBioc puts them under their own `<h3>` day headings, which is
        why headings are tracked alongside table rows.
    """
    page = get_text(url)
    if not page:
        return []
    rows, date, session, heading = [], v.start, "", ""
    seen: set[str] = set()
    for tok in TOKEN.finditer(page):
        if tok.group(1) is not None:                 # a heading
            text = clean(tok.group(1))
            got = parse_longdate(text, "")
            if got:
                date, session = got, ""
            else:
                heading = text
            continue
        raw = tok.group(2)
        span = SPAN4.search(raw)
        if span:                                     # in-table day header
            text = clean(span.group(1))
            got = parse_longdate(
                text if re.search(r"\d{4}", text) else f"{text} {v.year}", "")
            if got:
                date, session = got, ""
            continue
        if "<th" in raw:
            continue                                 # column-header row
        cells = CELL.findall(raw)
        if len(cells) >= 4:
            label = clean(cells[1])
            if label:
                session = label
            cell = cells[3]
        elif len(cells) == 2:
            # Poster table. Column 1 is the presenting author, sometimes
            # with a poster number; there is no column for it in the
            # schema, so it is read only to confirm the row is a poster.
            cell = cells[1]
            session = heading if heading and heading.lower() != "schedule" \
                else "Posters"
        else:
            continue
        title, abstract = split_details(cell)
        if not title:
            continue
        key = f"{v.id}:{date}/{slug(title)}"
        if key in seen:
            continue
        seen.add(key)
        rows.append((key, v.id, v.year, date, date[:7], session,
                     title, abstract, int(v.confirmed)))
    return rows


def harvest_bioc(v: Venue) -> list[tuple]:
    return harvest_schedule(v, "https://bioc2026.bioconductor.org/schedule/")


def harvest_eurobioc(v: Venue) -> list[tuple]:
    return harvest_schedule(
        v, "https://eurobioc2026.bioconductor.org/pages/schedule.html")


# --------------------------------------------------------------------------
# route 3 -- AAAI OJS issues, application tracks, biomedical vocabulary
# --------------------------------------------------------------------------

# THE AAAI INCLUSION RULE, part 1: which tracks.
# AAAI-26 is 48 OJS issues covering 50+ tracks. Only the four that are
# defined by *application* rather than by method are in scope; every
# method track (Computer Vision, Machine Learning, NLP, Robotics, Search,
# Game Theory, Knowledge Representation, ...) is excluded wholesale.
AAAI_ISSUES = {
    "683": "AAAI Technical Track on Application Domains I",
    "684": "AAAI Technical Track on Application Domains II",
    "727": "AAAI Special Track on AI for Social Impact I",
    "728": "AAAI Special Track on AI for Social Impact II",
}

# THE AAAI INCLUSION RULE, part 2: which papers inside those tracks.
# A paper is kept iff its title or its abstract, lowercased, matches at
# least one of these patterns. The list is fixed, applied identically to
# every paper, and never adjusted per paper.
#
# Stems are used where the stem is unambiguous (`oncolog`, `epidemi`) and
# word boundaries are forced where a stem would over-match (`\bgenes?\b`
# so that "generate" and "general" do not qualify). Four terms an earlier
# draft carried were removed because in an AI venue they are dominated by
# a non-biomedical sense, and every genuinely biomedical paper that
# matched them also matched something else: `treatment` (causal-inference
# treatment effects), `cells?`/`cellular` (spreadsheet cells), `neuro`
# (neuro-symbolic reasoning) and bare `genetic` (genetic algorithms).
#
# Terms deliberately kept despite occasional over-match, because the
# AI-for-Social-Impact track is public-health adjacent by design:
# `health` (also matches "battery state of health"), `molecular` (also
# matches computational chemistry), `hospitals?`.
BIOMED = re.compile(
    r"\b(?:"
    r"health|healthcare|clinical|clinician|patients?|hospitals?|medical|"
    r"medicine|diagnos|prognos|therap|drugs?|pharmac|epidemi|"
    r"diseases?|illness|symptoms?|comorbid|"
    r"cancers?|tumou?rs?|oncolog|carcinoma|metasta|leukemia|lymphoma|"
    r"genes?|genom|transcriptom|proteom|metabolom|epigen|"
    r"dna|rna|proteins?|molecular|molecules?|biolog|biomed|bioinformatic|"
    r"microbio|viral|virus|bacteri|pathogen|infections?|antibod|antigen|"
    r"immune|immunolog|vaccin|antibiotic|"
    r"neurons?|neuronal|neurolog|neuroimag|neuroscien|neurodegener|"
    r"brains?|eeg|ecg|ekg|mri|ct\s+scans?|radiolog|radiograph|ultrasound|"
    r"histopatholog|patholog|biopsy|biopsies|"
    r"electronic\s+health\s+record|ehrs?|mimic-|icu|sepsis|mortality|"
    r"diabet|cardiac|cardiovascular|pulmonar|respiratory|asthma|"
    r"covid|influenza|malaria|tuberculosis|hiv|"
    r"mental\s+health|psychiatr|surgery|surgical|nursing|triage|biomarkers?|"
    r"protein\s+folding|drug\s+discovery|physiolog|anatom|dental|ophthalm|"
    r"dermatolog"
    r")\b", re.I)

OJS_ARTICLE = re.compile(
    r'<h3 class="title">\s*<a id="article-(\d+)"[^>]*href="([^"]+)"[^>]*>\s*'
    r"(.*?)\s*</a>", re.S)
OJS_SECTION = re.compile(r'<div class="section">\s*<h2>\s*(.*?)\s*</h2>', re.S)
OJS_ABSTRACT = re.compile(
    r'<section class="item abstract">(.*?)</section>', re.S)
OJS_DOI = re.compile(r'name="citation_doi" content="([^"]*)"')


def harvest_aaai(v: Venue) -> list[tuple]:
    rows = []
    date = v.start           # meeting start, not the OJS posting date
    for issue, track in AAAI_ISSUES.items():
        page = get_text(
            f"https://ojs.aaai.org/index.php/AAAI/issue/view/{issue}")
        time.sleep(1.5)
        if not page:
            print(f"  aaai: issue {issue} unreachable", flush=True)
            continue
        found = OJS_SECTION.findall(page)
        if found and clean(found[0]) != track:
            # Guard: if AAAI renumbers its issues this must not silently
            # ingest a different track under the same label.
            print(f"  aaai: issue {issue} is now "
                  f"'{clean(found[0])}', expected '{track}' -- skipped",
                  flush=True)
            continue
        articles = OJS_ARTICLE.findall(page)
        print(f"  aaai: issue {issue} {track}: {len(articles)} papers",
              flush=True)
        for _aid, url, title in articles:
            title = clean(title)
            art = get_text(url)
            time.sleep(1.0)
            abstract = ""
            key = url.lower()
            if art:
                body = OJS_ABSTRACT.search(art)
                if body:
                    abstract = re.sub(r"^Abstract\s+", "",
                                      clean(body.group(1)))
                doi = OJS_DOI.search(art)
                if doi:
                    key = doi.group(1).lower()
            if not BIOMED.search(f"{title} {abstract}"):
                continue
            rows.append((key, v.id, v.year, date, date[:7], track,
                         title, abstract, int(v.confirmed)))
    return rows


# --------------------------------------------------------------------------
# route 4 -- CIMT abstract-book PDF, parsed on font runs
# --------------------------------------------------------------------------

CIMT_PDF = ("https://cdn.prod.website-files.com/613f568daaa1552c8518f71c/"
            "6a01adecc2e9190d24c4c0c0_20260511_LB_CIMT26MZBook_of_Abstracts_"
            "by_ProgramAuthors_2026-05-11.pdf")

PDF_STREAM = re.compile(rb"stream\r?\n")
PDF_FONT = re.compile(r"/(F\d+)\s+([\d.]+)\s+Tf")
PDF_STR = re.compile(r"\((?:\\.|[^\\()])*\)")
# The Word export tags every span with its language; the tag lands in the
# text layer and has to come back out.
LANGTAG = re.compile(r"(?:en-US|de-DE)")
SEAM = re.compile(r"[a-z](?=[A-Z])")
COMMA_SEAM = re.compile(r",[^,]{0,40}?[a-z](?=[A-Z])")

SZ_SESSION, SZ_NUMBER, SZ_TITLE, SZ_SUPER, SZ_BODY = 18.0, 12.0, 13.98, 5.52, 9.0
# Largest run-gap still counted as part of the affiliation block.
SUPER_GAP = 4


def pdf_font_runs(pdf: bytes) -> list[tuple[int, float, str]]:
    """Return (page index, font size, text) for every text run in the PDF."""
    runs = []
    page = 0
    for m in PDF_STREAM.finditer(pdf):
        start = m.end()
        end = pdf.find(b"endstream", start)
        try:
            raw = zlib.decompress(pdf[start:end]).decode("latin-1")
        except Exception:  # noqa: BLE001 - non-text streams (images, fonts)
            continue
        if "Tj" not in raw and "TJ" not in raw:
            continue
        marks = [(mm.start(), mm.end(), float(mm.group(2)))
                 for mm in PDF_FONT.finditer(raw)]
        for i, (_start, pos, size) in enumerate(marks):
            stop = marks[i + 1][0] if i + 1 < len(marks) else len(raw)
            text = "".join(x.group(0)[1:-1]
                           for x in PDF_STR.finditer(raw[pos:stop]))
            text = LANGTAG.sub("", text).replace("\\(", "(").replace("\\)", ")")
            if text.strip():
                runs.append((page, size, text))
        page += 1
    return runs


def near(a: float, b: float) -> bool:
    return abs(a - b) < 0.01


def harvest_cimt(v: Venue) -> list[tuple]:
    pdf = fetch(CIMT_PDF)
    if not pdf or not pdf.startswith(b"%PDF"):
        return []
    runs = pdf_font_runs(pdf)
    if not runs:
        return []

    sessions = [(i, r[2].strip()) for i, r in enumerate(runs)
                if r[1] >= SZ_SESSION]
    starts = []
    for i, (_p, size, text) in enumerate(runs):
        if not (near(size, SZ_NUMBER) and re.fullmatch(r"\s*\d{1,3}\s*", text)):
            continue
        if any(near(runs[j][1], SZ_TITLE) for j in range(i + 1,
                                                         min(i + 3, len(runs)))):
            starts.append((i, int(text.strip())))

    rows, seen = [], set()
    for k, (i, number) in enumerate(starts):
        stop = starts[k + 1][0] if k + 1 < len(starts) else len(runs)
        session = ([s for j, s in sessions if j < i] or [""])[-1]
        block = runs[i + 1:stop]
        title = clean("".join(t for _p, sz, t in block if near(sz, SZ_TITLE)))
        if not title:
            continue
        # Superscript runs mark the affiliation block, but a handful of
        # abstracts also carry superscript reference markers in the body,
        # so the last superscript in the record is not the end of the
        # affiliations. The affiliation superscripts sit 1-4 runs apart;
        # anything further out is body text, so the walk stops at the
        # first big gap.
        supers = [x for x, (_p, sz, _t) in enumerate(block)
                  if near(sz, SZ_SUPER)]
        cut = -1
        for idx in supers:
            if cut < 0 or idx - cut <= SUPER_GAP:
                cut = idx
            else:
                break
        body = clean("".join(t for _p, sz, t in block[cut + 1:]
                             if near(sz, SZ_BODY)))
        # The tail of the final affiliation runs into the body with no
        # space ("...(HI-TRON), GermanyRadiotherapy can elicit..."), so the
        # boundary is a lowercase-uppercase seam. Not just any seam:
        # institution names are full of them ("BioNTech"), so the seam has
        # to sit shortly after a comma, which is how an affiliation's
        # trailing ", <Country>" reads. Where an abstract numbers no
        # affiliations at all the whole author-plus-affiliation preamble
        # lands in `body` instead, and there the last plain seam in the
        # preamble is the boundary.
        if supers:
            seam = COMMA_SEAM.search(body[:400])
            if seam:
                body = body[seam.end():]
        else:
            seams = list(SEAM.finditer(body[:300]))
            if seams:
                body = body[seams[-1].end():]
        key = (number, title.lower())
        if key in seen:      # same poster shown in both poster sessions
            continue
        seen.add(key)
        rows.append((f"cimt-2026:{slug(session, 24)}/{number}-{slug(title)}",
                     v.id, v.year,
                     v.start, v.start[:7], session, title, body,
                     int(v.confirmed)))
    return rows


# --------------------------------------------------------------------------
# driver
# --------------------------------------------------------------------------

def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--only", default="",
                    help="comma-separated venue ids to restrict to")
    ap.add_argument("--rebuild-venue", default="",
                    help="comma-separated venue ids whose rows are deleted "
                         "before harvesting, even if the harvest then fails")
    args = ap.parse_args()

    wanted = {s.strip() for s in args.only.split(",") if s.strip()}
    rebuild = {s.strip() for s in args.rebuild_venue.split(",") if s.strip()}

    if not DB.exists():
        print(f"{DB} does not exist -- run harvest_conference.py first",
              file=sys.stderr)
        return 1
    con = sqlite3.connect(DB)
    con.executescript(SCHEMA)

    before = dict(con.execute(
        "SELECT venue, COUNT(*) FROM abstracts GROUP BY venue"))

    todo = [v for v in VENUES if not wanted or v.id in wanted]
    for v in todo:
        if v.id in rebuild:
            con.execute("DELETE FROM abstracts WHERE venue=?", (v.id,))
            con.commit()
        if not v.harvester:
            v.status = "not harvested"
            con.execute("DELETE FROM abstracts WHERE venue=?", (v.id,))
            con.execute("INSERT OR REPLACE INTO venues VALUES (?,?,?,?,?,?,?,?)",
                        (v.id, v.name, v.year, v.issn, v.route,
                         int(v.confirmed), v.note, 0))
            con.commit()
            print(f"{v.id}: nothing to harvest -- {v.note.split('.')[0]}",
                  flush=True)
            continue
        print(f"{v.id}: {v.route}", flush=True)
        try:
            v.rows = globals()[v.harvester](v)
        except Exception as exc:  # noqa: BLE001 - one venue must not stop the run
            v.rows, v.status = [], f"error: {exc}"
            print(f"  FAILED: {exc}", flush=True)
        if not v.rows:
            if v.status == "pending":
                v.status = "no rows"
            print(f"  0 rows -- existing rows for {v.id} left untouched",
                  flush=True)
            continue
        v.status = "ok"
        con.execute("DELETE FROM abstracts WHERE venue=?", (v.id,))
        con.executemany(
            "INSERT OR REPLACE INTO abstracts VALUES (?,?,?,?,?,?,?,?,?)",
            v.rows)
        con.execute("INSERT OR REPLACE INTO venues VALUES (?,?,?,?,?,?,?,?)",
                    (v.id, v.name, v.year, v.issn, v.route, int(v.confirmed),
                     v.note, len(v.rows)))
        con.commit()
        full = sum(1 for r in v.rows if len(r[7]) > 200)
        print(f"  {len(v.rows):,} rows, {full:,} with abstract text",
              flush=True)

    ids = tuple(v.id for v in VENUES)
    print()
    print(f"{'venue':16} {'months':18} {'rows':>6} {'w/ abstract':>12} "
          f"{'title only':>11}  conf")
    for vid, months, n, full in con.execute(
            "SELECT venue, MIN(month)||'..'||MAX(month), COUNT(*), "
            "SUM(LENGTH(abstract)>200) FROM abstracts "
            f"WHERE venue IN ({','.join('?' * len(ids))}) "
            "GROUP BY venue ORDER BY venue", ids):
        full = full or 0
        conf = con.execute("SELECT confirmed FROM venues WHERE id=?",
                           (vid,)).fetchone()
        print(f"{vid:16} {months:18} {n:6,} {full:12,} {n - full:11,}"
              f"  {'y' if conf and conf[0] else 'n'}")
    for v in VENUES:
        if not v.harvester:
            print(f"{v.id:16} {'--':18} {0:6,} {0:12,} {0:11,}  n")

    print()
    print("pre-existing Crossref venues (must be unchanged):")
    after = dict(con.execute(
        "SELECT venue, COUNT(*) FROM abstracts GROUP BY venue"))
    ok = True
    for venue, n in sorted(before.items()):
        if venue in ids:
            continue
        now = after.get(venue, 0)
        flag = "" if now == n else f"  <-- CHANGED from {n:,}"
        ok = ok and now == n
        print(f"  {venue:20} {now:7,}{flag}")
    print("  all unchanged" if ok else "  MISMATCH -- investigate")
    total = con.execute("SELECT COUNT(*) FROM abstracts").fetchone()[0]
    print(f"\ntotal {total:,} abstracts across "
          f"{con.execute('SELECT COUNT(*) FROM venues').fetchone()[0]} venues "
          f"({dt.date.today()})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
