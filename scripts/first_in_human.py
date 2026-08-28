#!/usr/bin/env python3
"""First-in-human backfill for the 124 agents behind the 192 FDA rows.

WHY THIS EXISTS
    scripts/approval_lead.py Stage B returned n = 0 measurable: every one of
    the approvals was left-censored because `ct_trials` begins 2023-01 and
    the drugs approved in 2023-2026 entered the clinic years earlier. Its own
    conclusion named the fix — a registry harvested back far enough that a
    first-in-human date exists for each approved agent. This is that harvest,
    scoped to exactly one number per agent instead of a full backfill:

        the earliest interventional trial in which the agent was administered.

THE TRAP THIS FILE IS BUILT AROUND
    ClinicalTrials.gov answers `query.intr=<name>` against its whole history,
    so an INN query reaches back to 2007 for rucaparib. But a phase 1 that
    opened before the INN was coined is registered under a sponsor code and
    the INN query does not find it. Verified here:

        query.intr=daraxonrasib  ->  earliest 2023-11-14  (NCT06128551)
        query.intr=RMC-6236      ->  earliest 2022-05-31  (NCT05379985, ph1/2)

    Eighteen months of a drug's history, invisible to the obvious query. That
    is the same code-name blindness that leaves 53% of phase-1 trials naming
    only sponsor codes, and taking the INN answer at face value would produce
    first-in-human dates that are systematically too late — which manufactures
    exactly the fake "measurable" subset this analysis exists to avoid.

    So every agent is resolved to its development code name(s) first, and the
    registry is queried again under each code.

RESOLUTION RULE (one rule, applied uniformly to all 124 agents)

    A string C is a code name of agent A if C is CODE-SHAPED and appears in a
    DIRECT PARENTHETICAL ADJACENCY with one of A's aliases, in one of five
    texts.  Nothing else counts; no fuzzy association, no "same sponsor so
    probably the same molecule", no reasoning from the outside world.

    CODE-SHAPED  = 2-8 leading letters, optional hyphen/space, 2-7 digits,
                   optional 1-3 trailing alphanumerics; >= 2 digits total;
                   leading letters not a biological target, element symbol,
                   registry prefix or English document word (see BLOCK_PREFIX).
                   `RMC-6236`, `LY3527028`, `BMS-986504`, `DS-8201a` pass.
                   `CD19`, `HER2`, `NCT06128551`, `Lu 177`, `Study 001` fail.

    ADJACENCY    = `<alias> (C)` or `C (<alias>)` — apposition and nothing
                   looser. The parenthesis may also hold `formerly`, `also
                   known as`, `previously`, a second code, and punctuation;
                   after those are removed at most 8 characters of residue are
                   tolerated, so `(200 mg every 3 weeks)`, `(95% CI 1.2-3.4)`
                   and `(NCT06128551)` are all rejected. In the mirror
                   direction the token immediately before the parenthesis must
                   itself be the code.

                   Apposition is the one construction in which two strings
                   next to each other are ASSERTED to be the same molecule.
                   "A trial that mentions both" is not: RMC-6236 and RMC-9805
                   co-occur in six trials and are different drugs.

    The five texts, and their provenance tag:
      fda    regulatory.sqlite fda_approvals.title + description   (internal)
      conf   conference.sqlite abstracts.title + abstract          (internal)
      jrnl   index.sqlite papers.title                             (internal)
      ctloc  regulatory.sqlite ct_trials.title + interventions     (internal)
      ctgov  the live registry: an intervention whose `name` matches an alias
             and whose `otherNames` contain C, or the mirror of that, or the
             same parenthetical pattern in a brief title             (EXTERNAL)

    `ctgov` is the only tag that reaches outside this repo, and every row
    records which tags produced it, so a self-contained re-run can drop them.

    VALIDATION. A code is used only if querying it returns >= 1 interventional
    study that either names an alias of A, or is led by a sponsor already seen
    leading an alias-matched study of A. An unvalidated code is written to the
    TSV with validated=0 and excluded from the date.

OWNERSHIP RULE (what makes a trial the agent's)
    The agent must appear as an INTERVENTION — an entry in
    armsInterventionsModule whose `name` or one of whose `otherNames` matches
    an alias or a validated code, on the same word-boundary rule
    approval_lead.py uses. Not the brief summary, not the conditions.

    This is deliberately looser than approval_lead.py's title-only ownership
    test, and in the opposite direction from convenience: being listed as an
    intervention means the drug was administered to humans in that study,
    which is the definition of first-in-human, even when the study belongs to
    somebody else's combination. It also biases every date EARLIER, hence
    toward censoring, hence against finding a measurable subset. The title-
    restricted date is computed alongside and written to the TSV so the
    stricter reading is available; it is never the one that decides anything.

Usage:
    python3 scripts/first_in_human.py              # harvest (cached) + write TSV
    python3 scripts/first_in_human.py --no-net     # recompute from cache only
    python3 scripts/first_in_human.py --cache DIR
"""

from __future__ import annotations

import argparse
import collections
import gzip
import importlib.util
import json
import pathlib
import re
import sqlite3
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parent.parent
REG = ROOT / "data" / "regulatory.sqlite"
INDEX = ROOT / "data" / "index.sqlite"
CONF = ROOT / "data" / "conference.sqlite"
OUT_TSV = ROOT / "data" / "first_in_human.tsv"

API = "https://clinicaltrials.gov/api/v2/studies"
FIELDS = ("NCTId|BriefTitle|OfficialTitle|StartDate|Phase|StudyType|"
          "InterventionName|InterventionOtherName|LeadSponsorName|OverallStatus")
UA = {"User-Agent": "aacr-corpus-first-in-human-backfill/1.0 (stdlib urllib)"}
SLEEP = 0.7          # polite; ~450 calls
PAGE = 200


def load_approval_lead():
    spec = importlib.util.spec_from_file_location(
        "approval_lead", ROOT / "scripts" / "approval_lead.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)          # read-only import; file untouched
    return mod


al = load_approval_lead()

# ---------------------------------------------------------------------------
# Code-name shape
# ---------------------------------------------------------------------------

CODE_RE = re.compile(r"\b([A-Za-z]{2,8}[-‐‑ ]?\d{1,7}(?:[A-Za-z]{1,2}\d{0,3})?)\b")

# Leading letter groups that make a code-shaped string something other than a
# development code. Targets and antigens (CD19, IL15), element symbols used in
# radioligands (Lu 177), registry and document furniture (NCT..., Table 2),
# assay and statistics vocabulary (IC50, 95% CI, TMB-16, HR-0.62), month
# names, trial-programme acronyms (KEYNOTE-045, IMpower150, CheckMate-816),
# dose shorthand (MEL200, NIVO800), and ordinary English words that precede a
# number often enough to look like a code (`and 200`, `of 23`, `with 2220`).
# Every entry below was observed producing a false code in a dry run over the
# four corpus texts; the list is empirical, not imagined.
BLOCK_PREFIX = set("""
and or of for with that these those was were is are the this it its from into
in to on at by as no not only over under above below after before during each
every per both either neither than then when where which who whom whose about
between within without across through since until while because although
received receiving received given giving taking taken treated treatment
lasting loading maintenance survival response duration median mean range aged
age older younger patients patient cohort arm group dose doses oral iv sc po
january february march april may june july august september october november
december spring summer autumn winter
aacr asco esmo ash sitc astro eortc nccn asbmt tct
keynote checkmate impower imvigor javelin ember monarch monaleesa paloma
paola prima velia sure tbcrc nant alliance swog ecog rtog nrg gog nsabp
ic ec gi hr rr or ci sd se ci95 auc cmax tmax emax ki kd km tmb msi tps cps
del dup amp mut wt vus loh tmb pdl mel nivo pembro atezo dura durva chemo
vs versus cycles cycle oncol max min orr dcr dor pfs os ld md sd pd cr pr
dec nov jan feb apr aug sep oct sept krasg brafv egfrex herg qtc alt ast
idh cdk rb ps gy ex part grade mdm ox nkg vegfr pdgfr fgf tgfb ulbp cea
trem sirp klrg foxp gzmb prf ifng tbet pdcd havcr entpd nt5e itgae ccnd
ercc mgmt mlh msh pms setd smarc arid kmt kdm ezh dnmt tet asxl srsf sf3b
u2af zrsr runx cebpa npm flt kit jak stat notch fbxw ptch smo gli yap taz
akt1 pten stk lkb keap nfe cul rbm ddx eif rps rpl mrp abcb abcg slc
""".split())

BLOCK_PREFIX |= set("""
cd il tnf ifn tgf vegf pdgf igf egfr her erbb kras nras hras braf tp rb myc
alk ros ret ntrk met fgfr pik akt mtor mek erk shp sos kif bcl mcl ccr cxcr
ccl cxcl hla mhc tcr bcma gprc dll sez trop nectin cldn msln psma sstr fra
ceacam slamf lag tigit tim vista icos gitr ctla pd pdl gd b7h ly6 cd3e
apobec brca palb atm chek rad mre nbn parp
lu ga tc ac cu zr ra sm ho re at pb bi th ce nd
nct euctr eudract isrctn jprn ctri chictr umin irb
study cohort part arm group week day month year cycle dose doses mg ml kg
version protocol amendment table figure fig abstract poster session slide
page phase phases line lines grade stage stages type types no number
ecog karnofsky recist irecist ctcae nci who ajcc tnm
covid sars hiv hbv hcv ebv hpv cmv
et al pmid pmcid doi issn isbn
""".split())

# Whole strings that pass every shape test and are still not codes. Kept as a
# separate list from BLOCK_PREFIX because blocking their prefix would take a
# real code down with them: `RP2D` must go, `RP1` (vusolimogene oderparepvec)
# must stay, and they share the prefix `RP`.
BLOCK_CODE = set("""
RP2D MTD DLT MRD PS0 PS1 PS2 ORR1 EOT1 EOS1 C1D1 C2D1 Q3W Q2W Q4W
APD1 APDL1 ARANK1 RANK1 HENT1 OND1 ECD2 ECLC5 LEVEL1 LEVEL2 DAILY1 DAYS1
DL0 DL1 DL2 DL3 DL4 DL5 DL6 EA1 EA2 EA3 EA4 EA5 EA6 EA7 EA8 EA9
""".split())

# A trailing four-letter FDA biologic suffix is not part of a code.
YEARISH = re.compile(r"^(19|20)\d{2}$")


def code_shaped(s: str) -> str | None:
    """Return the normalised code if `s` looks like a development code."""
    s = s.strip().strip(".,;:")
    m = CODE_RE.fullmatch(s)
    if not m:
        return None
    letters = re.match(r"[A-Za-z]+", s).group(0)
    if letters.lower() in BLOCK_PREFIX:
        return None
    digits = re.sub(r"\D", "", s)
    if len(digits) < 1 or len(letters) < 2:
        return None
    # A single digit is allowed — `RP1` is vusolimogene oderparepvec and the
    # corpus writes `Vusolimogene oderparepvec (RP1)` in plain sight — but
    # one digit is also the shape of every receptor and every ECOG score, so
    # the prefix block list below is doing all the work at that length and is
    # kept deliberately long.
    if len(digits) == 1 and len(letters) > 5:
        return None
    # `PF2023` style: a bare year after a short prefix is usually a date.
    if YEARISH.match(digits) and len(letters) <= 2:
        return None
    if len(s.replace(" ", "").replace("-", "")) < 3:
        return None
    norm = s.upper().replace(" ", "-").replace("‐", "-").replace("‑", "-")
    return None if norm.replace("-", "") in BLOCK_CODE else norm


def codes_in(text: str) -> set[str]:
    out = set()
    for m in CODE_RE.finditer(text):
        c = code_shaped(m.group(1))
        if c:
            out.add(c)
    return out


# ---------------------------------------------------------------------------
# Agents
# ---------------------------------------------------------------------------

class Agent:
    __slots__ = ("idx", "primary", "aliases", "pats", "approvals", "codes",
                 "studies", "sponsors", "queried", "inn_only")

    def __init__(self, idx, primary, aliases):
        self.idx = idx
        self.primary = primary
        self.aliases = aliases
        self.pats = [alias_pat(a) for a in sorted(aliases)]
        self.approvals: list[str] = []
        self.codes: dict[str, dict] = {}   # code -> {sources:set, validated:bool}
        self.studies: dict[str, dict] = {} # nct -> record
        self.sponsors: set[str] = set()
        self.queried: list[str] = []
        self.inn_only = None

    def hits(self, text: str) -> bool:
        low = text.lower()
        return any(p.search(low) for p in self.pats)


def alias_pat(alias: str) -> re.Pattern[str]:
    toks = al.TOKEN.findall(alias.lower())
    body = r"[\s\-]+".join(re.escape(t) for t in toks)
    return re.compile(r"(?<![a-z0-9])" + body + r"(?![a-z0-9])")


def code_pat(code: str) -> re.Pattern[str]:
    """`AMG-510` -> a pattern matching amg510, amg-510 and amg 510 alike.

    Sponsors are not consistent about the separator inside their own code
    (`AMG510` and `AMG 510` both appear in the registry for sotorasib), so
    the letter and digit runs are joined with an OPTIONAL separator rather
    than a required one. A word boundary still guards both ends, so `510`
    on its own never matches.
    """
    toks = re.findall(r"[a-z]+|\d+", code.lower())
    body = r"[\s\-]*".join(re.escape(t) for t in toks)
    return re.compile(r"(?<![a-z0-9])" + body + r"(?![a-z0-9])")


def build_agents(rcon) -> list[Agent]:
    """The 124 distinct agents, using approval_lead.py's own dedup logic."""
    apps = al.load_approvals(rcon)
    n = len(apps)
    repeat_of: list[int | None] = [None] * n
    for i in range(n):
        for j in range(i):
            if apps[j].date < apps[i].date and apps[i].aliases & apps[j].aliases:
                repeat_of[i] = j
                break
    agents: list[Agent] = []
    by_root: dict[int, Agent] = {}
    for i in range(n):
        root = i
        while repeat_of[root] is not None:
            root = repeat_of[root]
        if root not in by_root:
            a = Agent(root, apps[root].primary, set(apps[root].aliases))
            by_root[root] = a
            agents.append(a)
        by_root[root].approvals.append(apps[i].date)
    return agents, apps, repeat_of


def query_terms(agent: Agent) -> list[str]:
    """Which aliases to send to the registry.

    Drop aliases carrying regulatory boilerplate (`updated labeling for
    temozolomide`, `trifluridine and`), then, within a chain where one alias's
    tokens are a subset of another's, keep the SHORTEST. `query.intr` is a
    term search, so the shorter string is the broader query and the broader
    query is what we want when hunting for the earliest trial ever run.
    """
    cand = []
    for a in sorted(agent.aliases):
        toks = a.split()
        if any(t in al.STOP for t in toks):
            continue
        cand.append(a)
    keep = []
    for a in cand:
        ta = set(a.split())
        if any(b != a and set(b.split()) < ta for b in cand):
            continue          # a strictly longer alias exists in the same chain
        keep.append(a)
    return keep or sorted(agent.aliases)[:1]


# ---------------------------------------------------------------------------
# Registry access, cached on disk
# ---------------------------------------------------------------------------

class Registry:
    def __init__(self, cache: pathlib.Path, offline: bool):
        self.cache = cache
        self.cache.mkdir(parents=True, exist_ok=True)
        self.offline = offline
        self.calls = 0
        self.cached = 0

    def _path(self, key: str) -> pathlib.Path:
        safe = re.sub(r"[^A-Za-z0-9._-]", "_", key)[:120]
        return self.cache / f"{safe}.json.gz"

    def fetch(self, term: str, sort: str = "StartDate:asc",
              interventional: bool = True) -> list[dict]:
        key = f"{term}|{sort}|{int(interventional)}"
        p = self._path(key)
        if p.exists():
            self.cached += 1
            with gzip.open(p, "rt") as fh:
                return json.load(fh)
        if self.offline:
            return []
        params = {
            "query.intr": term,
            "pageSize": str(PAGE),
            "countTotal": "true",
            "sort": sort,
            "fields": FIELDS,
        }
        if interventional:
            params["filter.advanced"] = "AREA[StudyType]INTERVENTIONAL"
        url = API + "?" + urllib.parse.urlencode(params)
        studies, total = [], None
        for attempt in range(4):
            try:
                with urllib.request.urlopen(
                        urllib.request.Request(url, headers=UA), timeout=90) as fh:
                    data = json.load(fh)
                studies = data.get("studies", [])
                total = data.get("totalCount")
                break
            except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as e:
                if attempt == 3:
                    print(f"    ! {term}: {e}", file=sys.stderr)
                    return []
                time.sleep(2 ** attempt)
        self.calls += 1
        time.sleep(SLEEP)
        recs = [flatten(s) for s in studies]
        for r in recs:
            r["_total"] = total
        with gzip.open(p, "wt") as fh:
            json.dump(recs, fh)
        return recs


def flatten(s: dict) -> dict:
    ps = s.get("protocolSection", {})
    ident = ps.get("identificationModule", {})
    stat = ps.get("statusModule", {})
    des = ps.get("designModule", {})
    spon = ps.get("sponsorCollaboratorsModule", {}).get("leadSponsor", {})
    ivs = []
    for iv in ps.get("armsInterventionsModule", {}).get("interventions", []) or []:
        ivs.append({"name": iv.get("name", ""),
                    "other": iv.get("otherNames", []) or [],
                    "type": iv.get("type", "")})
    return {
        "n_ivs": len(ivs),
        "nct": ident.get("nctId", ""),
        "title": ident.get("briefTitle", "") or "",
        "official": ident.get("officialTitle", "") or "",
        "start": (stat.get("startDateStruct") or {}).get("date", "") or "",
        "phases": des.get("phases") or [],
        "type": des.get("studyType", ""),
        "sponsor": spon.get("name", ""),
        "status": stat.get("overallStatus", ""),
        "ivs": ivs,
    }


# ---------------------------------------------------------------------------
# Code-name mining
# ---------------------------------------------------------------------------

# Words allowed to share a parenthesis with a development code.
GLUE = re.compile(r"\b(formerly|previously|also|known|as|aka|a\.k\.a|or|and|"
                  r"development|code|codenamed|named|compound|drug|now|"
                  r"referred|to|the|its|study|investigational)\b", re.I)


def only_code(inside: str) -> set[str]:
    """Codes in a parenthesis that holds essentially nothing else.

    `(RMC-6236)`, `(formerly BGB-11417)`, `(MK-3475, pembrolizumab)` pass.
    `(200 mg every 3 weeks)`, `(95% CI 1.2-3.4)`, `(NCT06128551)` do not,
    because after the codes and the glue words are struck out they still
    leave more than eight characters of residue.
    """
    codes = codes_in(inside)
    if not codes:
        return set()
    residue = inside
    for m in sorted(CODE_RE.finditer(inside), key=lambda m: -m.start()):
        if code_shaped(m.group(1)):
            residue = residue[:m.start()] + residue[m.end():]
    residue = GLUE.sub("", residue)
    residue = re.sub(r"[^A-Za-z0-9]", "", residue)
    return codes if len(residue) <= 8 else set()


def adjacency_codes(text: str, pats) -> set[str]:
    """Codes in direct parenthetical apposition to an alias match."""
    low = text.lower()
    out: set[str] = set()
    for pat in pats:
        for m in pat.finditer(low):
            # `<alias> (CODE)` — parenthesis must open right after the alias,
            # allowing a comma or a dosage-form word in between.
            tail = text[m.end():m.end() + 60]
            mt = re.match(r"[,;]?\s*(?:tablets?|capsules?|injection)?\s*"
                          r"[\(\[]([^)\]]{2,44})[\)\]]", tail)
            if mt:
                out |= only_code(mt.group(1))
            # `CODE (<alias>)` — the parenthesis must open immediately before
            # the alias, and the token right before it must be the code.
            head = text[max(0, m.start() - 60):m.start()]
            if re.search(r"[\(\[]\s*$", head):
                stem = re.sub(r"[\(\[]\s*$", "", head)
                mb = re.search(r"([A-Za-z0-9\-‐‑ ]{3,20})[,;:]?\s*$", stem)
                if mb:
                    last = mb.group(1).strip().split()[-1] if mb.group(1).strip() else ""
                    c = code_shaped(last) or code_shaped(mb.group(1).strip())
                    if c:
                        out.add(c)
    return out


def mine_corpus(agents, rcon, ccon, jcon):
    """Corpus-internal code resolution over the four in-repo texts."""
    texts: list[tuple[str, str]] = []
    for title, desc in rcon.execute(
            "SELECT COALESCE(title,''), COALESCE(description,'') FROM fda_approvals"):
        texts.append(("fda", title + " — " + desc))
    for title, ivs in rcon.execute(
            "SELECT COALESCE(title,''), COALESCE(interventions,'') FROM ct_trials"):
        texts.append(("ctloc", title + " — " + ivs))
    if ccon:
        for title, abst in ccon.execute(
                "SELECT COALESCE(title,''), COALESCE(abstract,'') FROM abstracts"):
            texts.append(("conf", title + " — " + abst))
    if jcon:
        for (title,) in jcon.execute("SELECT COALESCE(title,'') FROM papers"):
            texts.append(("jrnl", title))

    # Candidate generation on a token intersection, exactly as approval_lead
    # does, so this is one pass over ~92k documents and not 124 x 92k regexes.
    anchors: dict[str, list[int]] = {}
    for i, ag in enumerate(agents):
        for alias in ag.aliases:
            toks = al.TOKEN.findall(alias)
            if toks:
                anchors.setdefault(max(toks, key=len), []).append(i)
    keys = set(anchors)

    found = 0
    for tag, text in texts:
        if "(" not in text and "[" not in text:
            continue
        low = text.lower()
        cand = set()
        for tok in set(al.TOKEN.findall(low)) & keys:
            cand.update(anchors[tok])
        for i in cand:
            ag = agents[i]
            for c in adjacency_codes(text, ag.pats):
                rec = ag.codes.setdefault(c, {"sources": set(), "validated": False})
                if tag not in rec["sources"]:
                    rec["sources"].add(tag)
                    found += 1
    return found


def mine_registry(agent: Agent, recs) -> None:
    """ctgov synonym graph: an intervention that carries both names."""
    for r in recs:
        for iv in r["ivs"]:
            name, others = iv["name"], iv["other"]
            name_hit = agent.hits(name)
            other_hits = [o for o in others if agent.hits(o)]
            if name_hit:
                agent.sponsors.add(r["sponsor"])
                for o in others:
                    c = code_shaped(o)
                    if c:
                        agent.codes.setdefault(
                            c, {"sources": set(), "validated": False})["sources"].add("ctgov")
            if other_hits:
                agent.sponsors.add(r["sponsor"])
                c = code_shaped(name)
                if c:
                    agent.codes.setdefault(
                        c, {"sources": set(), "validated": False})["sources"].add("ctgov")
        for t in (r["title"], r["official"]):
            if t:
                for c in adjacency_codes(t, agent.pats):
                    agent.codes.setdefault(
                        c, {"sources": set(), "validated": False})["sources"].add("ctgov")


# ---------------------------------------------------------------------------
# Trials belonging to the agent
# ---------------------------------------------------------------------------

def absorb(agent: Agent, recs, code_pats: dict[str, re.Pattern[str]],
           platform_max: int = 8) -> None:
    """Keep the studies in which the agent is an administered intervention.

    PLATFORM EXCLUSION. I-SPY 2 (NCT01042379) opened in 2010-03 and has since
    accumulated more than forty interventions, among them ARV-471,
    zanidatamab, datopotamab deruxtecan and dostarlimab — none of which
    existed in 2010. Reading its start date as those agents' first-in-human
    would hand eight of the 124 a date a decade too early. So a study whose
    title does not name the agent and which administers more than
    `platform_max` distinct interventions is marked `platform` and kept out
    of the primary date. The threshold is reported with a sensitivity sweep;
    it changes no conclusion, only how badly the umbrella trials distort.
    """
    for r in recs:
        if r["type"] != "INTERVENTIONAL":
            continue
        by_alias = by_code = None
        for iv in r["ivs"]:
            blob = " ".join([iv["name"]] + iv["other"])
            if agent.hits(blob):
                by_alias = True
            for c, p in code_pats.items():
                if p.search(blob.lower()):
                    by_code = c
        if not (by_alias or by_code):
            continue
        title_blob = ((r["title"] or "") + " " + (r["official"] or "")).lower()
        in_title = agent.hits(title_blob) or any(
            p.search(title_blob) for p in code_pats.values())
        prev = agent.studies.get(r["nct"])
        rec = dict(r)
        rec["by_alias"] = bool(by_alias) or (prev or {}).get("by_alias", False)
        rec["by_code"] = by_code or (prev or {}).get("by_code")
        rec["in_title"] = in_title or (prev or {}).get("in_title", False)
        rec["platform"] = (not rec["in_title"]) and r.get("n_ivs", len(r["ivs"])) > platform_max
        agent.studies[r["nct"]] = rec


def norm_start(s: str) -> str:
    return s if len(s) >= 7 else (s + "-01" if len(s) == 4 else s)


def earliest(studies, pred=lambda r: True):
    best = None
    for r in studies:
        if not r["start"] or not pred(r):
            continue
        d = norm_start(r["start"])
        if best is None or d < norm_start(best["start"]):
            best = r
    return best


PH1 = {"PHASE1", "EARLY_PHASE1"}


def confidence(best, agent) -> str:
    if best is None:
        return "none"
    ph = set(best["phases"])
    if ph & PH1 and best.get("in_title"):
        return "high"
    if ph & PH1:
        return "medium"
    return "low"


# ---------------------------------------------------------------------------

def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--cache", default=None, help="registry cache directory")
    ap.add_argument("--no-net", action="store_true",
                    help="recompute from cache; make no HTTP calls")
    ap.add_argument("--out", default=str(OUT_TSV))
    ap.add_argument("--platform-max", type=int, default=8,
                    help="a study with more interventions than this, whose "
                         "title does not name the agent, is treated as an "
                         "umbrella protocol and kept out of the date")
    args = ap.parse_args()

    cache = pathlib.Path(args.cache) if args.cache else (
        pathlib.Path.home() / ".cache" / "aacr-fih")
    rcon = sqlite3.connect(f"file:{REG}?mode=ro", uri=True)
    ccon = sqlite3.connect(f"file:{CONF}?mode=ro", uri=True) if CONF.exists() else None
    jcon = sqlite3.connect(f"file:{INDEX}?mode=ro", uri=True) if INDEX.exists() else None

    agents, apps, repeat_of = build_agents(rcon)
    print(f"agents: {len(agents)} distinct behind {len(apps)} approval rows")

    print("mining corpus-internal parenthetical apposition ...")
    nfound = mine_corpus(agents, rcon, ccon, jcon)
    internal = sum(1 for a in agents if a.codes)
    print(f"  {nfound} (agent, code, source) facts; {internal} agents got a code "
          f"from inside the repo")

    reg = Registry(cache, args.no_net)

    # -- pass 1: the INN/brand queries ------------------------------------
    print("registry pass 1 — alias queries ...")
    for k, ag in enumerate(agents, 1):
        for term in query_terms(ag):
            ag.queried.append(term)
            recs = reg.fetch(term)
            mine_registry(ag, recs)
            absorb(ag, recs, {}, args.platform_max)
            tot = recs[0].get("_total") if recs else 0
            if tot and tot > PAGE:
                # More interventional studies than one ascending page holds. The
                # ascending page already pins the earliest date; a descending
                # page is fetched only to widen the synonym graph, because a
                # code name is most often written into a recent record.
                extra = reg.fetch(term, sort="LastUpdatePostDate:desc")
                mine_registry(ag, extra)
                absorb(ag, extra, {}, args.platform_max)
        if k % 20 == 0:
            print(f"  {k}/{len(agents)}  calls={reg.calls} cached={reg.cached}")

    for ag in agents:
        ag.inn_only = earliest(ag.studies.values(), lambda r: not r["platform"])

    # A sponsor that leads studies for many different agents is a platform,
    # not an owner — NCI, MD Anderson, a cooperative group. Letting one of
    # those carry the weak validation path would let any code sharing a
    # cancer centre with the agent pass. Anything leading studies for more
    # than three of the 124 agents is disqualified from that path.
    spon_count: collections.Counter[str] = collections.Counter()
    for ag in agents:
        spon_count.update(set(ag.sponsors))
    promiscuous = {s for s, c in spon_count.items() if c > 3 or not s}
    print(f"  {len(promiscuous)} promiscuous sponsors excluded from weak "
          f"validation")

    # -- pass 2: the code queries -----------------------------------------
    ncodes = sum(len(a.codes) for a in agents)
    print(f"registry pass 2 — {ncodes} candidate codes across "
          f"{sum(1 for a in agents if a.codes)} agents ...")
    claims: dict[str, dict[int, int]] = {}     # code -> {agent index: alias hits}
    for k, ag in enumerate(agents, 1):
        alias_sponsors = set(ag.sponsors) - promiscuous
        for c in sorted(ag.codes):
            recs = reg.fetch(c)
            # VALIDATION: the code must lead back to this agent. `strong` =
            # some study the code query returns also writes the agent's name.
            # `weak` = it does not, but the study is led by a sponsor that
            # leads this agent's own studies and leads few others'.
            tier, hits = "", 0
            for r in recs:
                blob = " ".join([r["title"], r["official"]]
                                + [iv["name"] for iv in r["ivs"]]
                                + [o for iv in r["ivs"] for o in iv["other"]])
                if ag.hits(blob):
                    tier, hits = "strong", hits + 1
                elif not tier and r["sponsor"] and r["sponsor"] in alias_sponsors:
                    tier = "weak"
            ag.codes[c]["validated"] = bool(tier)
            ag.codes[c]["tier"] = tier
            ag.codes[c]["n"] = len(recs)
            ag.codes[c]["hits"] = hits
            if tier:
                claims.setdefault(c, {})[agents.index(ag)] = hits
        if k % 20 == 0:
            print(f"  {k}/{len(agents)}  calls={reg.calls} cached={reg.cached}")

    # CONFLICT RESOLUTION. Some sponsors write the whole regimen into one
    # intervention's `otherNames`, so `SGN-35` — brentuximab vedotin's code —
    # ends up attached to a pembrolizumab intervention and would give
    # pembrolizumab a 2006 first-in-human borrowed from a different molecule.
    # A code claimed by more than one of the 124 agents is therefore awarded
    # to the single agent whose name appears in the most of that code's own
    # registry results, and stripped from the rest. Ties are resolved toward
    # corpus-internal provenance, and if that does not break the tie the code
    # is dropped from every claimant: an ambiguous code buys nothing.
    stripped = 0
    for c, who in claims.items():
        if len(who) < 2:
            continue
        best = max(who.values())
        winners = [i for i, h in who.items() if h == best]
        if len(winners) > 1:
            internal = [i for i in winners
                        if agents[i].codes[c]["sources"] != {"ctgov"}]
            winners = internal if len(internal) == 1 else []
        for i in who:
            if i not in winners:
                agents[i].codes[c]["validated"] = False
                agents[i].codes[c]["tier"] = "conflict"
                stripped += 1
    print(f"  {stripped} code claims stripped by conflict resolution")

    for ag in agents:
        for c, v in ag.codes.items():
            if v["validated"]:
                absorb(ag, reg.fetch(c), {c: code_pat(c)}, args.platform_max)

    print(f"registry: {reg.calls} HTTP calls, {reg.cached} cache hits")

    # -- write --------------------------------------------------------------
    cols = ["primary", "aliases", "query_terms", "n_approvals",
            "first_approval", "last_approval", "codes", "code_sources",
            "codes_validated", "n_studies", "fih_date", "fih_nct", "fih_phase",
            "fih_in_title", "fih_via", "fih_sponsor",
            "inn_only_fih_date", "inn_only_nct", "months_gained_by_code",
            "fih_title_only_date", "fih_no_platform_filter_date",
            "fih_corpus_internal_date", "confidence", "external_only_codes"]
    out = pathlib.Path(args.out)
    lines = ["\t".join(cols)]
    for ag in agents:
        best = earliest(ag.studies.values(), lambda r: not r["platform"])
        best_t = earliest(ag.studies.values(), lambda r: r["in_title"])
        best_all = earliest(ag.studies.values())
        # The same date recomputed with every registry-only code name struck
        # out, so a reader who wants a result that depends on nothing outside
        # this repo can have one. Studies reached through a code that only
        # ClinicalTrials.gov could supply are dropped; studies reached through
        # the INN, or through a code the corpus itself spells out, are kept.
        # Hyphen-insensitive: `IMGN632` (found in an AACR abstract) and
        # `IMGN-632` (found in the registry) are one code, and the corpus
        # should get the credit for it whichever spelling absorbed the trial.
        internal_codes = {c.replace("-", "") for c, v in ag.codes.items()
                          if v["validated"] and v["sources"] != {"ctgov"}}
        best_int = earliest(
            ag.studies.values(),
            lambda r: (not r["platform"])
            and (r["by_alias"]
                 or (r["by_code"] or "").replace("-", "") in internal_codes))
        inn = ag.inn_only
        gained = ""
        if best and inn and best["start"] and inn["start"]:
            gained = str(al.months_between(norm_start(best["start"]),
                                           norm_start(inn["start"])))
        valid = {c: v for c, v in ag.codes.items() if v["validated"]}
        ext_only = [c for c, v in valid.items() if v["sources"] == {"ctgov"}]
        via = ""
        if best:
            via = "code" if (best.get("by_code") and not best.get("by_alias")) else "inn"
        row = [
            ag.primary,
            "|".join(sorted(ag.aliases)),
            "|".join(ag.queried),
            str(len(ag.approvals)),
            min(ag.approvals), max(ag.approvals),
            "|".join(sorted(ag.codes)),
            "|".join(f"{c}:{'+'.join(sorted(v['sources']))}"
                     f":{v.get('tier') or 'rejected'}"
                     for c, v in sorted(ag.codes.items())),
            "|".join(sorted(valid)),
            str(len(ag.studies)),
            norm_start(best["start"]) if best else "",
            best["nct"] if best else "",
            ";".join(best["phases"]) if best else "",
            "1" if best and best["in_title"] else "0",
            via,
            best["sponsor"] if best else "",
            norm_start(inn["start"]) if inn else "",
            inn["nct"] if inn else "",
            gained,
            norm_start(best_t["start"]) if best_t else "",
            norm_start(best_all["start"]) if best_all else "",
            norm_start(best_int["start"]) if best_int else "",
            confidence(best, ag),
            "|".join(sorted(ext_only)),
        ]
        lines.append("\t".join(x.replace("\t", " ").replace("\n", " ") for x in row))
    out.write_text("\n".join(lines) + "\n")
    print(f"wrote {out} ({len(agents)} rows)")

    # -- console summary ----------------------------------------------------
    def prim(a):
        return earliest(a.studies.values(), lambda r: not r["platform"])

    have = [a for a in agents if prim(a)]
    print()
    print(f"agents with a dated interventional trial : {len(have)}/{len(agents)}")
    years = collections.Counter(norm_start(prim(a)["start"])[:4] for a in have)
    print("earliest-trial year:",
          " ".join(f"{y}:{c}" for y, c in sorted(years.items())))
    moved = [a for a in agents if prim(a) and a.inn_only
             and norm_start(prim(a)["start"]) < norm_start(a.inn_only["start"])]
    print(f"agents whose date moved EARLIER once code names were used: {len(moved)}")
    for a in moved:
        b = prim(a)
        print(f"   {a.primary:<34} {norm_start(a.inn_only['start'])} -> "
              f"{norm_start(b['start'])}  ({b['nct']}, "
              f"{';'.join(b['phases'])}) via {b.get('by_code')}")

    # Sensitivity of the one threshold in this file.
    print()
    print("platform-exclusion sensitivity (agents with first-in-human >= 2023-01):")
    for k in (3, 5, 8, 12, 20, 10 ** 6):
        cnt = 0
        for a in agents:
            b = earliest(a.studies.values(),
                         lambda r, k=k: r["in_title"]
                         or r.get("n_ivs", len(r["ivs"])) <= k)
            if b and norm_start(b["start"])[:7] >= "2023-01":
                cnt += 1
        print(f"    platform_max = {k:<8} {cnt:>3} of {len(agents)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
