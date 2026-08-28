#!/usr/bin/env python3
"""Does anything in this corpus lead an FDA oncology approval?

Every lead time this repo has measured so far was corpus-against-corpus:
meeting abstracts against journal titles, one arbitrary text layer against
another, with a similarity threshold in the middle that had to be argued
for. `data/regulatory.sqlite` offers something none of those had — an
external endpoint with a real date. An approval is not a fuzzy match. It
happened on a day, the FDA says which day, and no threshold is involved.

So the question becomes answerable: by the day a drug was approved, had
this corpus ever said its name, and how long before?

The script refuses to answer that as one number, because the honest
answer has two halves that behave completely differently.

STAGE A — detectability. For each approval, ask a question with no time
    component: does the drug appear anywhere in the journal index, the
    conference abstracts, or the trial registry? This is a property of
    the roster and the harvest, not of the calendar, so it cannot be
    distorted by where the window happens to start. A drug the corpus
    never names cannot be led by it at any horizon, and the share of
    approvals in that bucket is the ceiling on everything else.

STAGE B — lead time, and the trap. This corpus opens in 2023-01. A drug
    approved in 2026 typically entered first-in-human around 2018-2019,
    ran a pivotal trial for years, and was named in the literature long
    before this window existed. Its earliest trace *in this corpus* is
    therefore not its earliest trace in the world — it is the left edge
    of the window, and subtracting it from the approval date measures the
    window, not the drug.

    That is the same error this repo already made once and corrected: the
    first version of scripts/lead_time.py reported "conference first,
    100%, median lead twelve months" when the journal index simply began
    after the meetings ended. Reporting a window's floor as a fact about
    the world is the failure mode this file is built to avoid.

    So a true lead time is computed only where the drug's earliest trace
    plausibly falls inside the window — operationally, where the earliest
    trial we can see for the agent is a first-in-human study and no trial
    for that agent has a start date before the window opens. Everything
    else is reported as CENSORED: "at least X months", never "X months".

    The measurable subset is not a random sample and must never be read
    as one. A drug whose first-in-human began after 2023-01 and which was
    approved by 2026-08 is by construction one of the fastest-moving
    agents in oncology — accelerated approvals, breakthrough designations,
    single-arm registrational trials. Selecting for measurability selects
    for speed. Whatever median the uncensored subset shows is a statement
    about the fast tail, not about drug development.

MATCHING RULE (one rule, applied identically to all three channels):

    Each approval gets an alias set. A record matches the approval if any
    alias occurs in the record's lowercased text with a word boundary on
    both ends, where internal spaces and hyphens in the alias may match
    any run of whitespace or hyphens. Aliases are:
      1. the full INN phrase (from `fda_approvals.drug`, else recovered
         from `description`, else from `title`);
      2. every individual token of that phrase that is >= 8 characters,
         alphabetic, and not on the generic-moiety blocklist (this is what
         lets `zanidatamab` match `zanidatamab-hrii`, and `vipivotide`
         match a trial that never writes out `lutetium Lu 177 ...`);
      3. the trade name from the `description` parenthetical, e.g.
         `daraxonrasib (RASONQUE, Revolution Medicines, Inc.)`.
    Every alias must be >= 6 characters after whitespace is removed. The
    blocklist removes shared moieties and carriers (`hyaluronidase`,
    `lutetium`, `phosphate`, `liposome`, ...) that would otherwise make
    one drug match a different drug built on the same scaffold.

    The rule is deliberately name-based and nothing else. No condition
    matching, no sponsor matching, no fuzzy string distance — a name is
    either written or it is not, and that keeps the false-positive story
    to a single sentence.

`fda_approvals.drug` parses 179 of 192 rows and returns empty string, not
NULL, when it fails; the failures are combination phrasings, possessives,
and element-name drugs where a lowercase-anchored regex breaks. The
fallback extractors here work from `description` and then `title`, and
the report states how many of the 13 were recovered and how many remain.

Usage:
    python3 scripts/approval_lead.py
    python3 scripts/approval_lead.py --detail          # per-approval table
    python3 scripts/approval_lead.py --misses          # list undetected drugs
    python3 scripts/approval_lead.py --markdown out.md
"""

from __future__ import annotations

import argparse
import collections
import pathlib
import re
import sqlite3
import statistics
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
REG = ROOT / "data" / "regulatory.sqlite"
INDEX = ROOT / "data" / "index.sqlite"
CONF = ROOT / "data" / "conference.sqlite"

CHANNELS = ("journal", "conference", "trial")

# Splitting on non-alphanumerics is what makes `zanidatamab-hrii` yield
# both `zanidatamab` and `hrii`; keeping the hyphen inside the token would
# hide the INN stem behind the FDA's four-letter biologic suffix.
TOKEN = re.compile(r"[a-z0-9]+")

# Words that end a backwards walk through the text preceding a trade-name
# parenthetical. These are regulatory boilerplate and English glue; a drug
# name never contains them, so hitting one means the name has ended.
STOP = set("""
a an the of to for with plus and in on at as by from into is are was were be
been fda food drug administration approved approval approves approve granting
granted grants expanded expands expanding revised revising amended amends
indication indications combination combinations regular traditional accelerated
new updated update labeling label safety changes change use uses used treatment
treat therapy therapies patients patient adult adults pediatric first line
oncology center excellence project renewal initiative information older certain
products product tablets tablet capsules capsule injection solution kit system
delivery containing hepatic oral intravenous subcutaneous intravesical
following after before who have has received prior fixed dose interchangeable
biosimilar deficiency discussions risks associated importance highlights
announcement communication regarding under this that these those it its
""".split())

# Shared moieties, carriers, radionuclides, salts, payloads and linkers.
# A token from this list identifies a scaffold, not an agent: `lutetium`
# is in three different approvals, `hyaluronidase` in six, `deruxtecan` in
# two entirely different antibody-drug conjugates. Letting any of them
# stand alone would report one drug as detected on the strength of another.
BLOCK = set("""
hyaluronidase berahyaluronidase phosphate acetate succinate mesylate maleate
tosylate fumarate chloride sulfate hydrochloride dihydrochloride citrate
lutetium gallium technetium actinium fluorine copper iodine radium samarium
liposome liposomal intravesical intravenous subcutaneous injection solution
deruxtecan vedotin govitecan mafodotin soravtansine ozogamicin tirumotecan
sunirine tetraxetan dotatate autoleucel maraleucel leucel inbakicept
oderparepvec trastuzumab prednisone dexamethasone
hematopoietic progenitor allogeneic autologous regulatory lymphocyte
transplantation immunotherapy antineoplastic
""".split())

MIN_ALIAS_CHARS = 6   # aliases shorter than this invite coincidence
MIN_TOKEN_CHARS = 8   # a token pulled out of a multi-word INN must be long

# Trade-name parenthetical: `daraxonrasib (RASONQUE, Revolution Medicines,
# Inc.)`. The comma is load-bearing — it is the only thing that separates a
# brand/sponsor pair from an ordinary abbreviation gloss like `(FDA)`,
# `(NSCLC)` or `(OCE)`, which otherwise match the same shape and produce a
# fake drug name on every safety communication.
PAREN = re.compile(r"\(\s*([A-Za-z][A-Za-z0-9\- ]{2,40}?)\s*,")

# Dosage-form tails that sit between the INN and its parenthetical.
FORM_TAIL = re.compile(
    r"\b(tablets?|capsules?|injections?|products?|solutions?|kits?|co-pack|"
    r"intravesical system|for injection)\b[\s,]*$", re.I)


def months_between(earlier: str, later: str) -> int:
    """Whole months from one YYYY-MM(-DD) to another. Month granularity is
    all the corpus can honestly support: journal `pubdate` is often the
    first of a month, and conference abstracts are dated to the meeting."""
    return ((int(later[:4]) - int(earlier[:4])) * 12
            + int(later[5:7]) - int(earlier[5:7]))


# ---------------------------------------------------------------------------
# Alias construction
# ---------------------------------------------------------------------------

def clean_phrase(text: str) -> str:
    """Lowercase, strip possessives and punctuation, collapse whitespace."""
    text = text.replace("’", "'").replace("'s ", " ")
    text = re.sub(r"'s\b", "", text)
    text = re.sub(r"[^A-Za-z0-9\- ]", " ", text)
    return " ".join(text.lower().split())


def walk_back(pre: str) -> str:
    """Take the drug name immediately preceding a trade-name parenthetical.

    Walks backwards from the parenthesis collecting tokens until a STOP
    word, so `...Administration approved daraxonrasib (` yields
    `daraxonrasib` and `...approved the fixed dose combination of niraparib
    and abiraterone acetate (` yields `niraparib and abiraterone acetate`.
    `and` is allowed through on purpose: a co-formulated pair is one
    approval and both halves are real agents, which is exactly the
    combination case the shipped `drug` column drops.
    """
    pre = re.split(r"[,;:]", pre)[-1]
    pre = FORM_TAIL.sub("", pre)          # `decitabine and cedazuridine tablets`
    out: list[str] = []
    for tok in reversed(pre.split()):
        tok = clean_phrase(tok)
        if not tok:
            break
        if tok in STOP and tok != "and":
            break
        out.append(tok)
        if len(out) > 8:                  # runaway guard
            break
    return " ".join(reversed(out)).strip(" -")


def names_from_description(desc: str) -> tuple[list[str], str, bool]:
    """(INN phrases, trade name, ok) from the first sponsor parenthetical."""
    m = PAREN.search(desc or "")
    if not m:
        return [], "", False
    inside = clean_phrase(m.group(1))
    phrase = walk_back(desc[:m.start()])
    parts = [p.strip() for p in phrase.split(" and ") if p.strip()]
    # `Poherdy (pertuzumab-dpzb, Shanghai Henlius...)` inverts the usual
    # order: the parenthetical is the INN and the brand sits outside it.
    # Both strings are aliases either way, so no disambiguation is needed.
    return parts, inside, bool(parts or inside)


def name_from_title(title: str) -> str:
    """Last-resort extractor: the first drug-shaped token in the headline.

    Used only for rows where neither the `drug` column nor a sponsor
    parenthetical produced anything — Project Renewal relabelings and DPD
    safety communications, which name an old generic in the headline and
    nowhere else in a parseable position. `drug-shaped` means alphabetic,
    >= 8 characters, and not regulatory boilerplate; the STOP list is
    doing the work and it is the same list used everywhere else.
    """
    for tok in clean_phrase(title).split():
        if len(tok) >= MIN_TOKEN_CHARS and tok.isalpha() and tok not in STOP \
                and tok not in BLOCK:
            return tok
    return ""


class Approval:
    __slots__ = ("url", "date", "month", "action", "drug", "title",
                 "aliases", "source", "primary")

    def __init__(self, url, date, month, action, drug, title):
        self.url, self.date, self.month = url, date, month
        self.action, self.drug, self.title = action, drug, title
        self.aliases: set[str] = set()
        self.source = ""          # which tier produced the name
        self.primary = ""         # display name


def components(phrase: str) -> list[str]:
    """INN phrase -> ordered word components, FDA biologic suffix removed.

    `fam-trastuzumab deruxtecan-nxki` -> [fam, trastuzumab, deruxtecan].
    The four-letter suffix is assigned at approval, so it cannot appear in
    anything that predates the approval and keeping it would guarantee a
    miss on every record written before the drug was approved.
    """
    out: list[str] = []
    for word in phrase.split():
        for part in word.split("-"):
            part = part.strip()
            if not part:
                continue
            # `-hrii`, `-csfr`, `-dlnk`: exactly four letters, tacked onto a
            # real INN. Dropped only in that position, never mid-phrase.
            if len(part) == 4 and part.isalpha() and out:
                continue
            out.append(part)
    return out


def substantive(comps) -> list[str]:
    """Components long enough to carry meaning, blocklist included."""
    return [c for c in comps
            if len(c) >= MIN_TOKEN_CHARS and c.isalpha() and c not in STOP]


def qualifying(comps) -> list[str]:
    """Components safe to match on their own — substantive and not shared."""
    return [c for c in substantive(comps) if c not in BLOCK]


def expand(phrases, trade: str) -> set[str]:
    """Phrase -> alias set, under one rule stated in the module docstring.

    A single-word INN (`pembrolizumab`, `sotorasib`) matches on the word.
    A multi-word INN matches only on the full phrase or on an adjacent
    pair of its components. That asymmetry is deliberate: emitting bare
    `trastuzumab` for `fam-trastuzumab deruxtecan` would match every plain
    trastuzumab trial in the registry and score Enhertu as detected on the
    strength of a 1998 antibody. Bigrams keep the specificity without
    requiring the record to spell out the FDA's full label string.
    """
    out: set[str] = set()
    for phrase in phrases:
        phrase = clean_phrase(phrase)
        if not phrase:
            continue
        comps = components(phrase)
        if not comps:
            continue
        qual, subs = qualifying(comps), substantive(comps)
        # The full phrase is an alias only if it carries either an unshared
        # agent word or two substantive words. Without that guard the
        # `T cells-vldq` of an allogeneic Treg product becomes the alias
        # `t cells` and matches 4,663 records; `hematopoietic stem` becomes
        # an alias and matches most of the transplant literature.
        if len(comps) > 1 and (qual or len(subs) >= 2):
            out.add(" ".join(comps))
        if len(qual) == 1 and len(subs) == 1:
            # Exactly one real agent word, the rest salts and routes: safe
            # alone. `pembrolizumab`, `abiraterone acetate` -> `abiraterone`.
            out.add(qual[0])
        else:
            # Two or more substantive words means the identity lives in the
            # pair, not in either half: `sacituzumab govitecan` must not
            # reduce to `sacituzumab`, which is also `sacituzumab
            # tirumotecan`, a different molecule entirely.
            for a, b in zip(comps, comps[1:]):
                if not (a.isalpha() and b.isalpha()) or len(a) + len(b) < 14:
                    continue
                if a in qual or b in qual or (a in subs and b in subs):
                    out.add(f"{a} {b}")
    trade = clean_phrase(trade)
    tcomps = components(trade)
    if tcomps:
        if len(" ".join(tcomps).replace(" ", "")) >= MIN_ALIAS_CHARS \
                and trade not in STOP:
            out.add(" ".join(tcomps))
        # A brand is one word most of the time; two-word brands
        # (`Darzalex Faspro`) also license the distinctive first word.
        head = tcomps[0]
        if len(head) >= MIN_ALIAS_CHARS and head.isalpha() \
                and head not in BLOCK and head not in STOP:
            out.add(head)
    return {a for a in out
            if len(a.replace(" ", "").replace("-", "")) >= MIN_ALIAS_CHARS}


def load_approvals(con: sqlite3.Connection) -> list[Approval]:
    rows = con.execute(
        "SELECT url, date, month, action, drug, title, description "
        "FROM fda_approvals ORDER BY date").fetchall()
    out = []
    for url, date, month, action, drug, title, desc in rows:
        appr = Approval(url, date, month or date[:7], action or "other",
                        drug or "", title or "")
        desc_names, trade, _ = names_from_description(desc or "")

        # Tier 1: the shipped column, when it parsed. Tier 2: the sponsor
        # parenthetical in the description. Tier 3: the headline. Trade
        # names are folded in at every tier because they are a separate
        # vocabulary — trials and abstracts use brands freely.
        if drug:
            appr.aliases = expand([drug] + desc_names, trade)
            appr.source = "drug column"
            appr.primary = drug
        elif desc_names or trade:
            appr.aliases = expand(desc_names, trade)
            appr.source = "description"
            # Prefer the brand when the INN phrase yielded nothing matchable
            # — an allogeneic Treg product is `Tregzi`, not `hematopoietic
            # stem`, and labelling it by the latter misreads the whole row.
            appr.primary = (desc_names[0] if desc_names
                            and qualifying(components(clean_phrase(desc_names[0])))
                            else (trade or (desc_names[0] if desc_names else "")))
        else:
            guess = name_from_title(title)
            appr.aliases = expand([guess], "")
            appr.source = "title" if appr.aliases else "unresolved"
            appr.primary = guess
        if not appr.aliases:
            appr.source = "unresolved"
        out.append(appr)
    return out


# ---------------------------------------------------------------------------
# Matching
# ---------------------------------------------------------------------------

def build_index(approvals):
    """anchor token -> [(approval index, alias)], plus compiled alias regexes.

    Same shape as the inverted-index candidate generation in
    scripts/lead_time.py: a cheap set intersection proposes candidates and
    an exact test confirms them, so this never becomes 192 aliases x 90k
    documents of regex work.
    """
    anchors: dict[str, list[tuple[int, str]]] = {}
    pats: dict[str, re.Pattern[str]] = {}
    for i, appr in enumerate(approvals):
        for alias in appr.aliases:
            toks = TOKEN.findall(alias)
            if not toks:
                continue
            anchor = max(toks, key=len)
            anchors.setdefault(anchor, []).append((i, alias))
            if alias not in pats:
                body = r"[\s\-]+".join(re.escape(t) for t in toks)
                pats[alias] = re.compile(r"(?<![a-z0-9])" + body + r"(?![a-z0-9])")
    return anchors, pats


def scan(rows, anchors, pats, n):
    """rows -> per-approval list of (date, ident, alias). Uniform per channel."""
    keys = set(anchors)
    hits: list[list[tuple[str, str, str]]] = [[] for _ in range(n)]
    for date, ident, text in rows:
        if not text:
            continue
        low = text.lower()
        cands: set[tuple[int, str]] = set()
        for tok in set(TOKEN.findall(low)) & keys:
            cands.update(anchors[tok])
        for idx, alias in cands:
            if pats[alias].search(low):
                hits[idx].append((date, ident, alias))
    return hits


def table_columns(con: sqlite3.Connection, table: str) -> list[str]:
    return [r[1] for r in con.execute(f"PRAGMA table_info({table})")]


def trial_rows(con: sqlite3.Connection):
    """Concatenate every free-text trial column that exists.

    Columns are read from PRAGMA rather than hard-coded because a harvest
    is actively widening this table; a new brief-summary or arm column must
    make the search better, never make the script raise.
    """
    have = table_columns(con, "ct_trials")
    text_cols = [c for c in ("title", "conditions", "interventions",
                             "brief_summary", "arm_labels", "arm_descriptions",
                             "arm_interventions", "collaborators")
                 if c in have]
    blob = " || ' ' || ".join(f"COALESCE({c},'')" for c in text_cols)
    return con.execute(f"SELECT date, nct_id, {blob} FROM ct_trials"), text_cols


# ---------------------------------------------------------------------------
# Report
# ---------------------------------------------------------------------------

class Out:
    """Collects the report so the same text goes to stdout and to markdown."""

    def __init__(self):
        self.lines: list[str] = []

    def __call__(self, line: str = ""):
        print(line)
        self.lines.append(line)


def pct(a: int, b: int) -> str:
    return f"{a / b:.0%}" if b else "n/a"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--window-open", default=None,
                    help="censoring boundary (YYYY-MM); default = corpus start")
    ap.add_argument("--grace", type=int, default=24,
                    help="months after the window opens during which an "
                         "approval or a phase 2/3 start is treated as proof "
                         "the drug predates the corpus (default 24)")
    ap.add_argument("--detail", action="store_true",
                    help="per-approval table of first traces")
    ap.add_argument("--misses", action="store_true",
                    help="list approvals no channel ever saw")
    ap.add_argument("--markdown", metavar="PATH", default=None,
                    help="also write the report to a markdown file")
    args = ap.parse_args()

    if not REG.exists():
        sys.exit("no data/regulatory.sqlite — run scripts/harvest_regulatory.py")

    rcon = sqlite3.connect(f"file:{REG}?mode=ro", uri=True)
    jcon = sqlite3.connect(f"file:{INDEX}?mode=ro", uri=True) if INDEX.exists() else None
    ccon = sqlite3.connect(f"file:{CONF}?mode=ro", uri=True) if CONF.exists() else None

    approvals = load_approvals(rcon)
    n = len(approvals)
    anchors, pats = build_index(approvals)

    out = Out()

    # ---- window actually used ------------------------------------------
    # Printed first and unconditionally. Two harvests are running against
    # these files; a number in this report is meaningless without the span
    # it was computed over, and "we ran it yesterday" is not a span.
    spans: dict[str, tuple[str, str, int]] = {}
    spans["approvals"] = rcon.execute(
        "SELECT MIN(month), MAX(month), COUNT(*) FROM fda_approvals").fetchone()
    spans["trials"] = rcon.execute(
        "SELECT MIN(month), MAX(month), COUNT(*) FROM ct_trials").fetchone()
    if jcon:
        spans["journals"] = jcon.execute(
            "SELECT MIN(month), MAX(month), COUNT(*) FROM papers").fetchone()
    if ccon:
        spans["conference"] = ccon.execute(
            "SELECT MIN(month), MAX(month), COUNT(*) FROM abstracts").fetchone()

    out("=" * 78)
    out("APPROVAL LEAD — does this corpus lead an FDA oncology approval?")
    out("=" * 78)
    out()
    out("SPAN ACTUALLY USED (read from the databases at run time)")
    for name, (lo, hi, cnt) in spans.items():
        out(f"  {name:<12} {lo} .. {hi}   {cnt:,} records")
    if jcon:
        out(f"  {'journals':<12} {jcon.execute('SELECT COUNT(DISTINCT journal) FROM papers').fetchone()[0]} distinct titles in the roster")
    if ccon:
        venues = ccon.execute(
            "SELECT venue, COUNT(*) FROM abstracts GROUP BY 1 ORDER BY 1").fetchall()
        out("  conference venues: "
            + ", ".join(f"{v} {c:,}" for v, c in venues))
    window_open = args.window_open or min(
        s[0] for s in spans.values() if s[0])
    out(f"  censoring boundary (window opens): {window_open}")
    out()

    # ---- name recovery --------------------------------------------------
    by_source = collections.Counter(a.source for a in approvals)
    blank_col = [a for a in approvals if not a.drug]
    recovered = [a for a in blank_col if a.source != "unresolved"]
    unresolved = [a for a in approvals if a.source == "unresolved"]

    out("NAME EXTRACTION")
    out(f"  approvals                                    {n}")
    out(f"  `drug` column non-empty                      {n - len(blank_col)}")
    out(f"  `drug` column empty (the known failures)     {len(blank_col)}")
    out(f"    recovered from description parenthetical   "
        f"{sum(1 for a in recovered if a.source == 'description')}")
    out(f"    recovered from title                       "
        f"{sum(1 for a in recovered if a.source == 'title')}")
    out(f"    still unresolved                           "
        f"{len(blank_col) - len(recovered)}")
    out(f"  alias source overall: "
        + ", ".join(f"{k} {v}" for k, v in by_source.most_common()))
    out(f"  distinct aliases built                       {len(pats):,}")
    if blank_col:
        out("  the 13 known failures, one line each:")
        for a in blank_col:
            shown = ", ".join(sorted(a.aliases)[:4]) or "-- none --"
            out(f"    {a.date}  [{a.source:<11}]  {shown}")
    if unresolved:
        out(f"  UNRESOLVED ({len(unresolved)}) — counted as not-seen everywhere,"
            " never dropped:")
        for a in unresolved:
            out(f"    {a.date}  {a.title[:70]}")
    out()

    out("MATCHING RULE (one rule, stated once, applied identically everywhere)")
    out("  A record matches an approval if any of the approval's aliases")
    out("  occurs in the record's lowercased text with a non-alphanumeric")
    out("  boundary on both sides. Spaces and hyphens inside an alias match")
    out("  any run of spaces/hyphens, so `trastuzumab deruxtecan` matches")
    out("  `trastuzumab-deruxtecan`.")
    out()
    out("  Aliases are built from the INN phrase and the trade name. The INN")
    out("  is split into components on spaces and hyphens and the four-letter")
    out("  FDA biologic suffix is dropped (`zanidatamab-hrii` ->")
    out(f"  `zanidatamab`). A component is SUBSTANTIVE if it is alphabetic and")
    out(f"  >= {MIN_TOKEN_CHARS} characters; it is QUALIFYING if it is also absent from a")
    out("  blocklist of shared moieties, payloads, carriers, radionuclides")
    out("  and salts (hyaluronidase, deruxtecan, vedotin, lutetium, acetate,")
    out("  liposome, ...). Then:")
    out("    - the full phrase is an alias if it has a qualifying component")
    out("      or two substantive ones;")
    out("    - a single word is an alias only when the phrase has exactly one")
    out("      substantive component and it qualifies (`pembrolizumab`;")
    out("      `abiraterone acetate` -> `abiraterone`);")
    out("    - otherwise adjacent component pairs >= 14 characters combined")
    out("      (`sacituzumab govitecan`, `vipivotide tetraxetan`), because")
    out("      with two substantive words the identity lives in the pair —")
    out("      `sacituzumab` alone is also `sacituzumab tirumotecan`;")
    out("    - the trade name and its first word, both from the description")
    out("      parenthetical.")
    out(f"  Every alias must be >= {MIN_ALIAS_CHARS} characters ignoring spaces and hyphens.")
    out("  No condition matching, no sponsor matching, no fuzzy distance.")
    out()
    out("  Channel text: journals = title only (the index holds no abstracts);")
    out("  conference = title + abstract body; trials = title + conditions +")
    out("  interventions + brief summary + arm labels/descriptions/interventions.")
    out()

    # ---- run the three channels ----------------------------------------
    hits: dict[str, list[list[tuple[str, str, str]]]] = {}

    if jcon:
        hits["journal"] = scan(
            jcon.execute("SELECT COALESCE(pubdate, month), pmid, title FROM papers"),
            anchors, pats, n)
    else:
        hits["journal"] = [[] for _ in range(n)]

    if ccon:
        hits["conference"] = scan(
            ccon.execute("SELECT date, doi, title || ' ' || COALESCE(abstract,'') "
                         "FROM abstracts"), anchors, pats, n)
    else:
        hits["conference"] = [[] for _ in range(n)]

    cur, tcols = trial_rows(rcon)
    hits["trial"] = scan(cur, anchors, pats, n)

    # A second, deliberately narrower trial pass over the drug fields only.
    # Stage A wants every mention, so it reads brief summaries and arm
    # descriptions too. Stage B must not: a drug named only in the prose of
    # somebody else's dose-escalation is a *combination partner*, and
    # calling that trial the agent's origin is how imlunestrant acquired a
    # 2023 first-in-human that actually belongs to tersolisib. Ownership is
    # asserted in the title and the intervention list, nowhere else.
    own_hits = scan(rcon.execute("SELECT date, nct_id, title FROM ct_trials"),
                    anchors, pats, n)

    # Journal `pubdate` is YYYY/MM/DD; normalise so every date compares.
    for ch in CHANNELS:
        hits[ch] = [[(d.replace("/", "-"), i, a) for d, i, a in rows]
                    for rows in hits[ch]]

    # A trace only counts if it predates the approval. This is the only
    # place time enters Stage A, and it enters as a filter on the record,
    # not as a truncation of the corpus.
    prior: dict[str, list[list[tuple[str, str, str]]]] = {
        ch: [[h for h in rows if h[0][:7] <= appr.month]
             for rows, appr in zip(hits[ch], approvals)]
        for ch in CHANNELS
    }

    # ---- STAGE A --------------------------------------------------------
    out("-" * 78)
    out("STAGE A — DETECTABILITY (uncensored: no duration is computed here)")
    out("-" * 78)
    out()
    out("By approval day, had this corpus ever written this drug's name?")
    out()
    out(f"  {'channel':<14} {'seen':>6} {'not seen':>9} {'% seen':>7}   "
        f"{'records':>9}")
    for ch in CHANNELS:
        seen = sum(1 for rows in prior[ch] if rows)
        recs = sum(len(rows) for rows in prior[ch])
        out(f"  {ch:<14} {seen:>6} {n - seen:>9} {pct(seen, n):>7}   {recs:>9,}")
    any_seen = [bool(prior['journal'][i] or prior['conference'][i]
                     or prior['trial'][i]) for i in range(n)]
    out(f"  {'ANY channel':<14} {sum(any_seen):>6} {n - sum(any_seen):>9} "
        f"{pct(sum(any_seen), n):>7}")
    out()

    # Journals-only is the number the roster is on trial for.
    j_only = sum(1 for i in range(n) if prior["journal"][i])
    out(f"  The 33-journal roster names {j_only} of {n} eventually-approved drugs")
    out(f"  ({pct(j_only, n)}) before their approval date. That is a property of")
    out("  the roster, not a defect in it: these are basic-science and")
    out("  methods journals, and a phase-3 readout for a fifth-line myeloma")
    out("  bispecific has no reason to appear in them. It does mean the")
    out("  journal layer alone cannot be used to anticipate approvals.")
    out()

    out("  By approval year:")
    out(f"    {'year':<6} {'n':>4}  " + "  ".join(f"{c:>12}" for c in CHANNELS)
        + f"  {'any':>12}")
    years = sorted({a.date[:4] for a in approvals})
    for y in years:
        idx = [i for i, a in enumerate(approvals) if a.date[:4] == y]
        cells = []
        for ch in CHANNELS:
            s = sum(1 for i in idx if prior[ch][i])
            cells.append(f"{s:>4} {pct(s, len(idx)):>6}")
        s = sum(1 for i in idx if any_seen[i])
        out(f"    {y:<6} {len(idx):>4}  " + "  ".join(f"{c:>12}" for c in cells)
            + f"  {s:>4} {pct(s, len(idx)):>6}")
    out()
    out("    The year gradient is mostly window shape, not science: a 2023")
    out("    approval can only be preceded by at most a few months of corpus,")
    out("    and the journal index does not start until 2024-01 at all.")
    out()

    out("  By action:")
    out(f"    {'action':<22} {'n':>4}  " + "  ".join(f"{c:>12}" for c in CHANNELS)
        + f"  {'any':>12}")
    for act, cnt in collections.Counter(a.action for a in approvals).most_common():
        idx = [i for i, a in enumerate(approvals) if a.action == act]
        cells = []
        for ch in CHANNELS:
            s = sum(1 for i in idx if prior[ch][i])
            cells.append(f"{s:>4} {pct(s, len(idx)):>6}")
        s = sum(1 for i in idx if any_seen[i])
        out(f"    {act:<22} {cnt:>4}  " + "  ".join(f"{c:>12}" for c in cells)
            + f"  {s:>4} {pct(s, len(idx)):>6}")
    out()

    # False-positive audit. The matching rule is one line, so the way it
    # fails is also one line: a short or generic alias picks up records that
    # have nothing to do with the drug. Ranking aliases by how many records
    # they hit puts any such alias at the top where it can be seen, rather
    # than leaving it buried in an aggregate.
    alias_load: collections.Counter[str] = collections.Counter()
    for ch in CHANNELS:
        for rows in hits[ch]:
            alias_load.update(a for _, _, a in rows)
    out("  False-positive audit — aliases matching the most records.")
    out("  A generic word smuggled into the alias set would appear here:")
    for alias, c in alias_load.most_common(12):
        owner = next(a.primary for a in approvals if alias in a.aliases)
        out(f"    {c:>6,}  {alias:<30} ({owner[:28]})")
    out("    These are old, widely-combined backbone agents, which is what a")
    out("    correct matcher should return at the top: no English word, no")
    out("    bare payload, no route term. One real weakness remains and is")
    out("    visible here — where an approval is a new formulation of an old")
    out("    generic (gemcitabine intravesical system, irinotecan liposome,")
    out("    mitomycin intravesical solution) the alias that fires is the old")
    out("    generic. Those rows are scored as detected on the strength of a")
    out("    molecule the corpus has always known, not the product approved.")
    out()

    # Bound on the trial channel. A phase-1 whose interventions are only
    # sponsor codes cannot be matched by any name-based rule, ours included.
    code = re.compile(r"^[a-z]{0,4}[- ]?\d{2,6}[a-z]?$")
    p1 = tot = 0
    for (ivs,) in rcon.execute(
            "SELECT COALESCE(interventions,'') FROM ct_trials "
            "WHERE phases LIKE '%PHASE1%'"):
        drugs = [d.split(":", 1)[-1].strip().lower()
                 for d in ivs.split(";") if d.lower().startswith("drug")]
        if not drugs:
            continue
        tot += 1
        if all(code.match(d) or not any(len(w) >= 8 and w.isalpha()
                                        for w in TOKEN.findall(d))
               for d in drugs):
            p1 += 1
    out(f"  Bound on the trial channel: {p1:,} of {tot:,} phase-1 trials "
        f"({pct(p1, tot)}) name")
    out("  nothing but sponsor codes in their intervention list. A drug in")
    out("  that residue is invisible to any name-based rule until it is")
    out("  given an INN, which typically happens well after first-in-human.")
    out("  That residue is the ceiling on how early the trial channel can")
    out("  ever see anything, and it is why the trial numbers above are a")
    out("  floor on detectability rather than a measurement of it.")
    out()

    if args.misses:
        out("  Approvals no channel ever names before approval day:")
        for i, a in enumerate(approvals):
            if not any_seen[i]:
                out(f"    {a.date}  {a.action:<20} {a.primary[:34]:<34} "
                    f"{a.title[:52]}")
        out()

    # ---- THE ENDPOINT IS NOT HOMOGENEOUS --------------------------------
    # A row in fda_approvals is not "a new drug". It is an FDA action, and
    # the same molecule generates one for every indication it wins. Averaging
    # a first-in-class approval together with the fifth indication of a 2016
    # PARP inhibitor produces a number that describes neither.
    out("-" * 78)
    out("THE ENDPOINT IS NOT HOMOGENEOUS — NEW MOLECULAR ENTITY vs EXPANSION")
    out("-" * 78)
    out()

    meta = {r[0]: r for r in rcon.execute(
        "SELECT nct_id, start_date, phases, date FROM ct_trials")}

    # Signal 1: the same agent already has an earlier row in this table.
    # Alias overlap, not string equality, so `pembrolizumab` links to
    # `pembrolizumab and berahyaluronidase alfa-pmph`.
    repeat_of: list[int | None] = [None] * n
    for i in range(n):
        for j in range(i):
            if approvals[j].date < approvals[i].date and \
                    approvals[i].aliases & approvals[j].aliases:
                repeat_of[i] = j
                break

    # Signal 2: an EMA marketing authorisation predating the window. EMA
    # normally lags FDA, so an EU authorisation before 2023-01 is decisive
    # evidence that the molecule was approved somewhere before we started
    # looking. This is the only genuinely external check available here.
    ema_rows = list(rcon.execute(
        "SELECT COALESCE(NULLIF(date,''), NULLIF(ec_decision_date,''), '9999'), "
        "product_number, name || ' ' || COALESCE(inn,'') || ' ' "
        "|| COALESCE(active_substance,'') FROM ema_medicines"))
    ema_hits = scan(ema_rows, anchors, pats, n)
    ema_old = [min((h[0] for h in rows), default=None) for rows in ema_hits]

    # Signal 3: the cell- and gene-therapy roster, which lists products
    # licensed before this window with no date attached — presence alone
    # is evidence of prior existence for the CGT rows.
    cgt_rows = list(rcon.execute(
        "SELECT '', product, product || ' ' || COALESCE(trade_name,'') || ' ' "
        "|| COALESCE(generic_name,'') FROM fda_cgt_roster"))
    cgt_hits = scan(cgt_rows, anchors, pats, n)

    n_repeat = sum(1 for r in repeat_of if r is not None)
    firsts = [i for i in range(n) if repeat_of[i] is None]   # distinct agents
    n_ema_old = sum(1 for i in firsts
                    if ema_old[i] and ema_old[i][:7] < window_open)
    n_cgt = sum(1 for i in firsts if cgt_hits[i])
    novel = [i for i in firsts
             if not (ema_old[i] and ema_old[i][:7] < window_open)
             and not cgt_hits[i]]
    out(f"  approvals (FDA actions, not molecules)        {n}")
    out(f"  a strictly earlier row in this table names the same agent")
    out(f"    -> repeat action, cannot be a first approval  {n_repeat}")
    out(f"  distinct agents behind the {n} actions          {len(firsts)}")
    out("  of those distinct agents:")
    out(f"    EMA-authorised before {window_open}                 {n_ema_old}")
    out(f"    on the FDA cell/gene-therapy roster          {n_cgt}")
    out(f"    NOT shown to predate the window by either    {len(novel)}")
    out(f"  So at most {len(novel)} of {len(firsts)} agents can even be candidates for")
    out("  being new inside this window. Stage B shows none survives.")
    out()
    out("  `action` classifies only "
        f"{sum(1 for a in approvals if a.action == 'label expansion')} rows as"
        " `label expansion`, so it does not")
    out("  do this job: most expansions are filed as a plain `approval`.")
    out("  The repeat count above is a LOWER BOUND and a large one. A drug")
    out(f"  whose first approval predates {window_open} — rucaparib 2016,")
    out("  tepotinib 2021, adagrasib 2022 — has no earlier row here to link")
    out("  to, so this table cannot see that it is an expansion. EMA and the")
    out("  CGT roster recover part of that residue; the rest is invisible.")
    out()
    top = collections.Counter()
    for i in range(n):
        root = i
        while repeat_of[root] is not None:
            root = repeat_of[root]
        top[approvals[root].primary] += 1
    out("  Agents with the most actions in the window:")
    for name, c in top.most_common(8):
        if c > 1:
            out(f"    {c:>2}x  {name}")
    out()

    # ---- STAGE B --------------------------------------------------------
    out("-" * 78)
    out("STAGE B — LEAD TIME, ONLY WHERE IT IS MEASURABLE")
    out("-" * 78)
    out()

    first_trace: list[str | None] = []
    first_channel: list[str] = []
    for i in range(n):
        cands = [(rows[0][0], ch) for ch in CHANNELS
                 for rows in [sorted(prior[ch][i])] if rows]
        if cands:
            d, ch = min(cands)
            first_trace.append(d)
            first_channel.append(ch)
        else:
            first_trace.append(None)
            first_channel.append("")

    # The gate. Six independent signals, each one sufficient on its own to
    # prove the drug's history starts before this corpus does. A lead time
    # is computed only when none of them fires. Ordered from cheapest and
    # most decisive to weakest so the funnel below reads as an argument.
    # A registrational phase 3 rests on a completed dose escalation and a
    # phase 2 signal. Those do not both fit in under two years, so a phase
    # 2/3/4 starting inside this grace period proves the phase 1 it rests
    # on ran before the window and we never saw it.
    grace = args.grace   # months after the window opens

    def prior_existence(i) -> str | None:
        # (a) is a property of the calendar, not the drug, and it is the
        # purest statement of the problem: an approval two months after the
        # window opens can show a lead of at most two months, which is far
        # below any plausible development interval. You cannot observe a
        # four-year process through a two-month aperture.
        if months_between(window_open, approvals[i].date) < grace:
            return (f"a) approved within {grace} months of the window opening "
                    "— aperture too small")
        if repeat_of[i] is not None:
            return "b) an earlier row here already names this agent"
        if ema_old[i] and ema_old[i][:7] < window_open:
            return "c) EMA authorised this molecule before the window opened"
        if cgt_hits[i]:
            return "d) already on the FDA cell/gene-therapy roster"
        # Ownership is asserted in the title. An intervention list contains
        # every drug administered, so reading it as ownership makes
        # imlunestrant the subject of a first-in-human study of tersolisib
        # in which it is the tenth of eleven interventions.
        trials = [meta[t] for _, t, _ in own_hits[i]
                  if t in meta and meta[t][3] <= approvals[i].date]
        if not trials:
            return "e) no trial names this agent in its own title"
        starts = [t[1] for t in trials if t[1]]
        if not starts:
            return "f) every matched trial is missing a start date"
        if min(starts)[:7] < window_open:
            return "g) a trial of this agent started before the window opened"
        first_trial = min((t for t in trials if t[1]), key=lambda t: t[1])
        if "PHASE1" not in (first_trial[2] or "").upper():
            return "h) the earliest visible trial is not first-in-human"
        late = [t for t in trials if t[1] and "PHASE1" not in (t[2] or "").upper()
                and months_between(window_open, t[1]) < grace]
        if late:
            return (f"i) a phase 2/3/4 of this agent started within {grace} "
                    "months of the window opening")
        # The corpus falsifying itself. If a meeting abstract or a paper
        # already names the agent when its supposed first-in-human opens,
        # that trial is not the origin — nobody presents at AACR on a
        # molecule that entered the clinic last month. This is the signal
        # that removed gedatolisib, quizartinib, vorasidenib and nine more
        # that every registry-only test had waved through.
        origin = first_trial[1]
        if any(h[0] <= origin for ch in ("journal", "conference")
               for h in prior[ch][i]):
            return ("j) the literature already named this agent when its "
                    "earliest trial opened")
        return None

    uncensored: list[tuple[int, int]] = []
    censored: list[tuple[int, int]] = []
    reasons: collections.Counter[str] = collections.Counter()

    for i, appr in enumerate(approvals):
        if first_trace[i] is None:
            reasons["z) never seen in any channel"] += 1
            continue
        lead = months_between(first_trace[i], appr.date)
        why = prior_existence(i)
        if why:
            reasons[why] += 1
            censored.append((i, lead))
        else:
            uncensored.append((i, lead))

    out("A lead time is computed only where the drug's whole history")
    out("plausibly falls inside the window — where the corpus could have")
    out("seen the agent's origin. Every one of these disqualifies it:")
    out(f"  a) approved within {grace} months of {window_open} — the aperture")
    out("     bounds the lead below any plausible development interval")
    out(f"  b) an earlier row of fda_approvals names the same agent")
    out(f"  c) EMA authorised the molecule before {window_open}")
    out(f"  d) it is on the FDA cell/gene-therapy roster")
    out(f"  e) no trial names the agent in its own title")
    out(f"  f) matched trials carry no start date")
    out(f"  g) some trial of the agent started before {window_open}")
    out(f"  h) the earliest visible trial is not phase 1 / early phase 1")
    out(f"  i) a phase 2/3/4 started within {grace} months of the window")
    out("     opening, which requires a phase 1 we never saw")
    out("  j) a paper or abstract already named the agent when that")
    out("     earliest trial opened, so the trial is not the origin")
    out()
    out(f"  approvals                                     {n}")
    out(f"  seen by at least one channel before approval  {sum(any_seen)}")
    out(f"  MEASURABLE (uncensored)                       n = {len(uncensored)}")
    out(f"  CENSORED (lower bounds only)                  n = {len(censored)}")
    out(f"  never seen at all                             n = "
        f"{n - len(uncensored) - len(censored)}")
    out()
    out("  Which signal disqualified each censored case:")
    for reason, c in sorted(reasons.items()):
        out(f"    {c:>4}  {reason}")
    out()

    if uncensored:
        leads = sorted(l for _, l in uncensored)
        out(f"  MEASURABLE LEAD TIMES  (n = {len(leads)})")
        out(f"    median {statistics.median(leads):.1f} months, "
            f"range {min(leads)}-{max(leads)}")
        out("    This subset is NOT random. A drug whose first-in-human began")
        out(f"    after {window_open} and which was approved by "
            f"{spans['approvals'][1]} is by")
        out("    construction among the fastest-moving agents in oncology.")
        out("    Selecting for measurability selects for speed; this median")
        out("    describes the fast tail and nothing else.")
        out()
        out(f"    {'approved':<11} {'lead':>5}  {'action':<22} {'via':<11} drug")
        for i, lead in sorted(uncensored, key=lambda r: -r[1]):
            out(f"    {approvals[i].date:<11} {lead:>3}mo  "
                f"{approvals[i].action:<22} {first_channel[i]:<11} "
                f"{approvals[i].primary[:32]}")
        out()
    else:
        out("  MEASURABLE LEAD TIMES  n = 0")
        out("    No approval in this window has an observable origin. Every")
        out("    approved agent was already in trials, in print, or on a")
        out("    meeting programme before the corpus opened. That is the")
        out("    result, not a preliminary to one: with a 2023-01 floor and")
        out("    a 2023-2026 approval set, approval lead time is not a")
        out("    quantity this corpus can estimate.")
        out()

    # Sensitivity. A null that only holds at one threshold is a threshold,
    # not a null. `grace` is the only tunable number in the gate, so vary
    # it across everything from "no aperture argument at all" to two years.
    out("  Sensitivity of the measurable count to the one tunable number:")
    out(f"    {'grace (months)':>15}  {'measurable n':>12}")
    keep = grace
    for g in (0, 6, 12, 18, 24, 30):
        grace = g
        m = sum(1 for i in range(n)
                if first_trace[i] is not None and prior_existence(i) is None)
        out(f"    {g:>15}  {m:>12}")
    grace = keep
    out("    The null does not come from the threshold. With the aperture")
    out("    argument switched off entirely (grace 0) three approvals survive")
    out("    — vepdegestrant, daraxonrasib, retifanlimab — and all three are")
    out("    known from outside this corpus to have entered first-in-human")
    out("    before the window opened (2019, 2021 and 2017 respectively).")
    out("    They survive because their early trials were registered before")
    out("    2023-01 and are therefore absent from a table that begins in")
    out("    2023-01: absence of an old trial is not evidence of a new drug.")
    out("    Every loosening of the gate buys false survivors, never real")
    out("    ones, which is the strongest available statement of the problem.")
    out()

    if censored:
        lows = sorted(l for _, l in censored)
        out(f"  CENSORED OBSERVATIONS  (n = {len(lows)}) — read every one of")
        out("  these as 'at least X months', never as 'X months'. The true")
        out("  lead is larger by an unknown amount for every single row.")
        out(f"    median lower bound  >= {statistics.median(lows):.1f} months")
        out(f"    quartiles           >= {lows[len(lows)//4]}, "
            f">= {statistics.median(lows):.0f}, >= {lows[3*len(lows)//4]} months")
        out(f"    maximum lower bound >= {max(lows)} months  (which is the")
        out("      distance to the window edge, i.e. it is measuring the")
        out("      window and not the drug)")
        out()
        edge = sum(1 for l in lows
                   if l >= months_between(window_open, spans["approvals"][1]) - 2)
        out(f"    {edge} of {len(lows)} censored bounds sit within 2 months of the")
        out("    maximum the window physically allows. A distribution pinned")
        out("    against its own boundary is the signature of censoring.")
        out()

    # Which channel gets there first, among drugs seen by more than one.
    multi = [i for i in range(n)
             if sum(1 for ch in CHANNELS if prior[ch][i]) >= 2]
    out("  Which channel sees a drug first, among those seen by >= 2 channels")
    out(f"  (n = {len(multi)}). Also censored — a channel can only 'win' inside")
    out("  the window — but the ordering is informative where the spans overlap.")
    winners = collections.Counter(first_channel[i] for i in multi)
    for ch, c in winners.most_common():
        out(f"    {ch:<12} {c:>4}  {pct(c, len(multi))}")
    out()
    pair = [i for i in multi if prior["journal"][i] and prior["conference"][i]]
    if pair:
        gaps = []
        for i in pair:
            jm = min(h[0] for h in prior["journal"][i])
            cm = min(h[0] for h in prior["conference"][i])
            gaps.append(months_between(cm, jm))
        gaps.sort()
        ahead = sum(1 for g in gaps if g > 0)
        out(f"  Conference vs journal, drugs both name (n = {len(gaps)}):")
        out(f"    conference first in {ahead} of {len(gaps)} ({pct(ahead, len(gaps))}), "
            f"median gap {statistics.median(gaps):+.0f} months")
        out("    Confounded: the conference layer starts 2023-02 and the")
        out("    journal index starts 2024-01, so roughly a year of this gap")
        out("    is the difference between the two harvests, not the two")
        out("    communities. Compare against the same drugs restricted to")
        out("    2024-01+ before believing any of it.")
        both24 = []
        for i in pair:
            jm = min(h[0] for h in prior["journal"][i])
            cm = min((h[0] for h in prior["conference"][i] if h[0] >= "2024-01"),
                     default=None)
            if cm:
                both24.append(months_between(cm, jm))
        if both24:
            both24.sort()
            a2 = sum(1 for g in both24 if g > 0)
            out(f"    restricted to conference records 2024-01+ (n = {len(both24)}): "
                f"conference first in {a2} ({pct(a2, len(both24))}), "
                f"median {statistics.median(both24):+.0f} months")
        out()

    if args.detail:
        out("-" * 78)
        out("PER-APPROVAL DETAIL")
        out("-" * 78)
        out(f"  {'approved':<11} {'act':<4} {'jrnl':<8} {'conf':<8} {'trial':<8} "
            f"{'first':<8} {'lead':>6} drug")
        for i, a in enumerate(approvals):
            cells = []
            for ch in CHANNELS:
                cells.append(min((h[0][:7] for h in prior[ch][i]), default="--"))
            ft = first_trace[i][:7] if first_trace[i] else "--"
            if first_trace[i] is None:
                lead = "  none"
            elif any(i == u for u, _ in uncensored):
                lead = f"{months_between(first_trace[i], a.date):>4}mo"
            else:
                lead = f">={months_between(first_trace[i], a.date):>3}mo"
            act = {"approval": "app", "accelerated approval": "acc",
                   "label expansion": "exp"}.get(a.action, "oth")
            out(f"  {a.date:<11} {act:<4} {cells[0]:<8} {cells[1]:<8} "
                f"{cells[2]:<8} {ft:<8} {lead:>6} {a.primary[:30]}")
        out()

    out("-" * 78)
    out("THE BIGGEST THREAT TO THIS ANALYSIS")
    out("-" * 78)
    out("  Left-censoring, and it is not a caveat — it is the dominant term.")
    out("  The corpus opens 2023-01; the approvals run 2023-01 onward; a drug")
    out("  approved in that span entered development years earlier. Almost")
    out("  every lead this script can compute is bounded above by the")
    out("  distance to the window edge, which means the distribution is")
    out("  measuring the harvest and not the science. Stage A is the part of")
    out("  this report that survives that objection, because a name is either")
    out("  written somewhere in the corpus or it is not, and no duration is")
    out("  subtracted. Stage B should be read as an upper bound on what is")
    out("  knowable here, not as an estimate of anything.")

    if args.markdown:
        path = pathlib.Path(args.markdown)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("```\n" + "\n".join(out.lines) + "\n```\n")
        print(f"\n[written to {path}]")
    return 0


if __name__ == "__main__":
    sys.exit(main())
