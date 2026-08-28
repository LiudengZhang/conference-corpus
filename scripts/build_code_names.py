#!/usr/bin/env python3
"""Development-code decoder built from the conference abstract corpus.

WHY THIS EXISTS
    The approval-lead study found one clean positive about the conference
    layer: 45 development code names were recoverable from AACR/ASCO abstract
    text and zero from FDA announcements. On the other side of the same
    corpus, 34% of 2025 phase-1 oncology trials name nothing but a bare
    sponsor code, so their target is invisible. A drug is a code long before
    it is an INN, and that dark interval is what the conference layer is
    supposed to see into. This file turns the observation into a lookup
    table: code -> INN -> target.

    It also measures whether the table is worth having, by re-running the
    opacity count in `data/threads.yml` -> next-gen-checkpoints.blind_spot
    with the decoder applied. That measurement is the point. A decoder that
    closes nothing is a real finding and is reported as one.

EXTRACTION IS TRIVIAL. VALIDATION IS THE WHOLE JOB.
    A naive apposition regex over the 29,168 full-text abstracts returns 586
    pairs whose most frequent members are `IC50 <-> concentration`,
    `CD68 <-> macrophages`, `EP300 <-> protein`, `CT26 <-> colorectal`.
    Assay metrics, surface markers, gene symbols, cell lines. The real pairs
    are in there — `AMG-510 <-> sotorasib`, `MRTX849 <-> adagrasib` — but a
    rule that ships without a filter on BOTH sides ships mostly noise.

    So both sides are typed, and then the typed pair is validated:

    LEFT SIDE (the code) reuses scripts/first_in_human.py wholesale. That
    file's `code_shaped` / `only_code` / `adjacency_codes` were validated at
    scale — 416 codes across 124 agents — and carry block lists for targets,
    element symbols, assay and statistics vocabulary, trial acronyms and dose
    shorthand. Re-deriving them here would be re-deriving a solved problem
    worse. Two block lists are ADDED, for traps that only appear when the
    right-hand side is a drug name rather than a known agent alias:

      EXTRA_PREFIX  gene symbols that only turn into codes when an inhibitor
                    is written `WEE1i` / `TOP1i` — the `i` becomes the
                    trailing alphanumeric the code shape allows.
      PAYLOAD       `SN-38`, `DM1`, `MMAE`, `DXd`. These pass every shape
                    test and sit in true apposition with an INN — `irinotecan
                    (SN-38)` is written in the corpus — but SN-38 is
                    irinotecan's active METABOLITE and DM1 is trastuzumab
                    emtansine's PAYLOAD. Neither is a development code, and a
                    decoder that resolves `DM1 -> emtansine` would be
                    resolving a chemical moiety to a drug. This block list is
                    the single largest precision fix in the file.

    RIGHT SIDE (the INN) is typed by WHO stem. An international nonproprietary
    name is not an arbitrary string: the stem is assigned, so `-tinib` is a
    tyrosine-kinase inhibitor, `-mab` a monoclonal antibody, `-ciclib` a CDK
    inhibitor. Requiring a stem is what separates `sotorasib` from
    `concentration`, `macrophages` and `colorectal` in one test, and it is a
    property of the naming system rather than a list of observed noise, so it
    generalises to INNs coined after this corpus was frozen.

    Three stems that appear in the WHO scheme are DELIBERATELY NOT USED:
      -ase   (enzymes)  matches disease, release, decrease, kinase, protease,
                        and produced `TDO2 <-> dioxygenase`, `HK2 <->
                        hexokinase`, `DCAS9 <-> endonuclease` in a dry run —
                        gene symbol apposed to the name of its own product.
      -ment  (2022 mAb) matches treatment, development, assessment,
                        engagement. Unusable in English prose.
      -mer   (polymers) matches polymer, dimer, primer, former.
    Their loss costs a handful of real agents (asparaginase). Keeping them
    cost more than that in one dry run, which is why they are out.

VALIDATION RULE (the part that decides what ships)
    A pair is EXTRACTED from one sentence in one abstract. It is VALIDATED
    only if the link survives being looked up again somewhere the extraction
    did not come from. This mirrors first_in_human.py, which re-queried each
    candidate code and demanded a link back to the INN. Four independent
    supports, strongest first:

      ctgov     ClinicalTrials.gov: an intervention whose `name` matches one
                side and whose `otherNames` carry the other. EXTERNAL — the
                only tag reaching outside this repo, and recorded per row so
                a self-contained re-run can drop it.
      trial     regulatory.sqlite ct_trials: code and INN both present in one
                trial record (title, interventions, brief_summary, arms).
      repeat    the same apposition asserted in >= 2 abstracts with different
                DOIs. Two authors independently writing `X (Y)`.
      cooc      code and INN co-occur in a DIFFERENT abstract from the one
                the apposition came from, >= 15 tokens apart being irrelevant
                — mere co-occurrence, the weakest support, and never enough
                on its own to reach `high`.

    A pair with no support at all is still written, tagged `unsupported`, so
    the file records what the extractor believed and an auditor can see the
    tail it is judged on. Downstream consumers should filter on confidence.

    TWO APPOSITIVE CONSTRUCTIONS SHIP, `inn(code)` and `code(inn)`. A third,
    `code+inn` — both names inside one parenthesis, `(MK-3475,
    pembrolizumab)` — was built, measured at 22% precision, and deleted. See
    the note above `coformulation` for why it cannot be repaired.

CONFLICT RULE
    One code, two INNs is usually not an error: `ASTX727` decodes to both
    `decitabine` and `cedazuridine` because it is a co-formulation, and
    `zipalertinib` legitimately owns both `TAS6417` and `CLN-081` because
    sponsors change. What is an error is one code decoding to two unrelated
    molecules. So a code with multiple INNs is left alone when the INNs share
    the same trial or abstract evidence (co-formulation / synonym), and
    demoted to `ambiguous` when they do not.

TARGET RESOLUTION (best effort, and labelled as such)
    The target is read off the same corpus, by voting over every window of
    +/- 90 characters around a mention of the code or the INN, using five
    appositive constructions (`a KRAS G12C inhibitor`, `anti-TIGIT`,
    `targeting CLDN18.2`, `CD3 bispecific`, `directed against BCMA`). The
    window and the combination guard on it are load-bearing and are explained
    at `target_windows` and `target_vote`. It is a convenience column, not a
    claim: `target_votes` records how many windows voted for the winner and
    how many voted at all, and a target carried by one window is a hint.

MEASURED PRECISION (2026-08-27)
    Hand audit, 60 rows drawn with random.Random(20260827).sample() from the
    177 rows at confidence high|medium, each judged against the supporting
    abstract sentence, by the rule "is this INN the international
    nonproprietary name of the molecule the code denotes?": 60/60 correct.
    A separate read of all 177 found two errors the sample missed, both since
    fixed by the guards they motivated, so the honest figure is 60/60 in
    sample and ~99% over the shipped table. The 42 `unsupported` rows were
    read too and are about half right, which is why they do not ship.

Usage:
    python3 scripts/build_code_names.py                # offline, ~2.5 min
    python3 scripts/build_code_names.py --ctgov        # + registry validation
    python3 scripts/build_code_names.py --audit 60     # print an audit sample
    python3 scripts/build_code_names.py --opacity-only # just the residue count
"""

from __future__ import annotations

import argparse
import collections
import gzip
import importlib.util
import json
import pathlib
import random
import re
import sqlite3
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parent.parent
CONF = ROOT / "data" / "conference.sqlite"
REG = ROOT / "data" / "regulatory.sqlite"
INDEX = ROOT / "data" / "index.sqlite"
OUT_TSV = ROOT / "data" / "code_names.tsv"

# State lives outside the repo, next to first_in_human.py's own cache, so an
# interrupted run resumes from disk and a re-run costs no HTTP calls.
CACHE = pathlib.Path.home() / ".cache" / "aacr-codenames"

API = "https://clinicaltrials.gov/api/v2/studies"
FIELDS = ("NCTId|BriefTitle|InterventionName|InterventionOtherName|"
          "LeadSponsorName|StartDate|Phase|StudyType")
UA = {"User-Agent": "aacr-corpus-code-name-decoder/1.0 (stdlib urllib)"}
SLEEP = 0.7
PAGE = 100


def load(name: str):
    """Import a sibling script read-only, the way first_in_human.py does."""
    spec = importlib.util.spec_from_file_location(name, ROOT / "scripts" / f"{name}.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


fih = load("first_in_human")          # code shape, block lists, only_code
al = fih.al                           # approval_lead, already loaded by fih


# ---------------------------------------------------------------------------
# Left side: the code. first_in_human.py's shape test plus two block lists.
# ---------------------------------------------------------------------------

# `WEE1i`, `TOP1i`, `PARPi`: a gene symbol with the inhibitor-shorthand `i`
# stuck on the end is code-shaped and sits in apposition with the inhibitor's
# own INN (`WEE1i (adavosertib)`). The pair is semantically right and
# structurally wrong — the left side names a target class, not a molecule —
# and letting it through would put target abbreviations in the code column.
EXTRA_PREFIX = set("""
wee top chk atr atm parp cdk aurk plk brd ezh menin kat usp arid smarc setd
hdac dnmt idh shp sos pim syk btk jak alk ros ret met fgfr pi3k akt mtor mek
erk raf kras nras braf egfr her erbb vegfr pdgfr kit flt aurora bcl mcl xpo
lsd prmt hpk nlrp sting tlr cgas stat notch wnt yap hif nrf keap myc mdm
""".split())

# A second empirical block list, every entry observed producing a false row in
# a dry run of THIS file. Three kinds, and the kinds are the useful part:
#   pharmacogene / chaperone / receptor symbols that sit in apposition with a
#     drug for pharmacology reasons -- `irinotecan (UGT1A1)`, `HSP90
#     (doxorubicin)` -- where the apposition is real and the relation is not
#     identity but metabolism or target;
#   virus and isotope names, which are code-shaped by accident (`HSV1`,
#     `GALLIUM68`, `MIR126`);
#   trial acronyms carrying a number, which first_in_human.py blocks by
#     programme name (`KEYNOTE`, `CHECKMATE`) but which continue to appear
#     under sponsor-specific names (`FIRE-3`, `TRIBE-2`).
EXTRA_PREFIX |= set("""
hsp ugt cyp sult nqo gst abcb abcg slco tpmt dpyd nudt comt vkorc
hsv hpv ebv cmv hbv hcv siv fiv mmtv mir let snhg linc neat malat xist
gallium lutetium fluorine technetium copper zirconium actinium indium yttrium
tgfbr tnfrsf tnfsf slamf klrb klrc klrd cxcl ccl ifnar il1r il2r il6r il7r
hnf foxa gata sox pax hox runx cebp nfkb irf ets klf ppar rxr rar vdr esr ar
pkmyt myt polq rad51 nlrp3 trex sting1 cgas1
fire tribe cairo focus atlas horizon summit compass legend triumph destiny
panorama radiant lumina harmony bridge nexus origin voyager horizon impact
csf rh rhil rhu
""".split())

# Symbols whose LETTER PREFIX cannot be blocked without collateral damage,
# exactly the situation first_in_human.BLOCK_CODE was written for: blocking
# `pi` would take `PI-88` down with `PI3K`. Compared on code_key, so spelling
# variants collapse.
GENE_CODE = {"PI3K", "PIK3CA", "PIK3CD", "MTORC1", "MTORC2", "IL2R", "IL15RA",
             "TGFB1", "TGFB2", "CDK46", "CD3XCD20", "HER2XHER3", "NFKB1"}

# Payloads, linkers and active metabolites. Every one of these passes the code
# shape and appears in genuine apposition with an INN somewhere in the corpus,
# because that is how ADC and prodrug chemistry is written. None of them is a
# development code, and each would decode a moiety to a molecule.
PAYLOAD = set("""
SN38 SN22 DM1 DM4 DXD MMAE MMAF PBD DUOCARMYCIN CALICHEAMICIN EXATECAN
DOLASTATIN AURISTATIN MAYTANSINE PNU159682 SC209 TOPO1 T-DM1 TDM1 DM21
""".split())

# Radiochemistry: an isotope-labelled ligand is written `177Lu-PSMA-617` and
# `68Ga-FAPI-46`. The trailing fragment is code-shaped, the leading isotope is
# already blocked upstream, and the residue is a chelator/ligand name rather
# than a development code, so the pair adds a false row per tracer.
TRACER = re.compile(r"^(PSMA|FAPI|DOTA|PENTIXA|NEUROTENSIN|RGD|MIP)[- ]?\d", re.I)


def norm_code(s: str) -> str | None:
    """Reuse first_in_human.code_shaped, then apply this file's own blocks."""
    c = fih.code_shaped(s)
    if not c:
        return None
    letters = re.match(r"[A-Za-z]+", c).group(0)
    if letters.lower() in EXTRA_PREFIX:
        return None
    if c.replace("-", "") in PAYLOAD or TRACER.match(c):
        return None
    if c.upper().replace("-", "").replace(" ", "") in GENE_CODE:
        return None
    # A code carrying no letters after the digits and only two leading letters
    # is usually a figure or panel reference (`Fig 2B` is blocked upstream but
    # `AB 12` is not). Three characters of alphanumeric is the floor.
    if len(re.sub(r"[^A-Za-z0-9]", "", c)) < 4:
        return None
    return c


def code_key(c: str) -> str:
    """`AMG-510`, `AMG 510` and `AMG510` are one code; the separator is not
    part of the identity and sponsors are not consistent about it even inside
    their own registry records."""
    return c.upper().replace("-", "").replace(" ", "")


# ---------------------------------------------------------------------------
# Right side: the INN, typed by WHO stem.
# ---------------------------------------------------------------------------

# Assigned WHO stems, oncology-weighted, plus the second words of the ADC and
# radioligand vocabulary (`deruxtecan`, `vedotin`, `tetraxetan`), which are
# stems in their own right. Longest match wins, so `-rasib` is preferred over
# `-ib` when both fit and the specific stem is what gets reported.
INN_STEMS = """
mab zumab ximab umab omab tug bart mig
tinib anib rafenib metinib ciclib lisib parib degib sertib rasib tasib zomib
sidenib fitinib ertinib lastinib clax toclax citinib tectinib vatinib nib ib
stat nostat depsin xostat
tecan rubicin platin taxel taxane mustine citabine tabine uridine fosfamide
sulfan exed ubicin trexed zolomide xantrone bulin templin
vec adenovec parepvec logene plasmid
leucel cabtagene eucel autoleucel maraleucel cel
tide sen rsen siran nersen mersen ersen pegtide
limus rolimus
lutamide domide estrant arotene enolone sterone
leukin kinra cept ercept
grastim poetin
pegol
dotatate tetraxetan vipivotide edotreotide
vedotin deruxtecan govitecan mafodotin tansine ozogamicin tirumotecan
soravtansine emtansine ejaduotin nesiran duocarmazine pasudotox
limab olimab relimab tolimab sudotin
demstat clostim spirin
"""
STEMS = set(INN_STEMS.split())

# Stems drop out under two conditions. `-ase` / `-ment` / `-mer` are excluded
# by never being listed above. These are the words that reach a listed stem
# and are still not drugs: `-ib` catches `crib`, `-cel` catches `parcel`,
# `-tide` catches `oligonucleotide`, `-stat` catches nothing yet but will.
INN_STOP = set("""
oligonucleotide polynucleotide nucleotide dinucleotide polypeptide peptide
antibodies antibody carbohydrate candidate mandate validate irradiate
associate correlate accumulate translate demonstrate investigate
inhibitor inhibitors activator adjuvant covalent equivalent
parcel cancel excel morsel personnel channel panel model level label
prescribe describe subscribe transcribe ascribe
resistant assistant persistent consistent
distribute contribute attribute institute substitute
antigen oncogene transgene endogenous
statistic statistical substrate prostate
conjugate aggregate segregate integrate
protein proteins pathway pathways
cytokine chemokine
manuscript transcript
combination population
represent different important
"""
.split())

MIN_INN = 8          # `afatinib` is 8; nothing real is shorter and safe
MAX_INN = 24


def inn_stem(word: str) -> str | None:
    """Return the longest assigned WHO stem the word ends in, or None."""
    w = word.lower().strip(".,;:()[]'\"")
    if not w.isalpha() or not (MIN_INN <= len(w) <= MAX_INN):
        return None
    if w in INN_STOP or w in al.STOP:
        return None
    for k in range(10, 1, -1):
        if len(w) > k and w[-k:] in STEMS:
            return w[-k:]
    return None


def inn_phrase(tokens: list[str]) -> tuple[str, str] | None:
    """Longest INN phrase ending at a stem-bearing token: (phrase, stem).

    `disitamab vedotin`, not `vedotin`. This matters more than it looks:
    `vedotin` alone is the payload of at least nine different ADCs, so a
    decoder that maps `RC48 -> vedotin` has mapped a code to a linker.

    THE HEAD RULE, AND THE BUG IT FIXES. The obvious way to grow the phrase
    leftward is "any long word that is not English glue". A dry run of that
    produced `efficacy pimicotinib`, `cancer samuraciclib`, `tumors
    ulixertinib`, `assess sunvozertinib` and `immune signaling emavusertib` —
    five of ninety-five high-confidence rows with a sentence fragment welded
    to the front of a correct INN. The fix is not a longer stop list, it is
    the naming system: EVERY word of a multi-word INN carries its own WHO
    stem, because each word names a moiety. `sacituzumab govitecan` is
    `-umab` + `-tecan`; `ofranergene obadenovec` is `-nergene` + `-adenovec`;
    `decitabine cedazuridine` is `-tabine` + `-uridine`. `efficacy` carries
    nothing, so it cannot be part of an INN, and no stop list is needed.
    """
    for i in range(len(tokens) - 1, -1, -1):
        stem = inn_stem(tokens[i])
        if not stem:
            continue
        head = [tokens[i].lower().strip(".,;:()[]'\"")]
        for j in range(i - 1, max(-1, i - 3), -1):
            t = tokens[j].lower().strip(".,;:()[]'\"-")
            if inn_stem(t):
                head.insert(0, t)
            else:
                break
        # `fam-trastuzumab deruxtecan-nxki` -> drop the four-letter FDA suffix
        comps = al.components(" ".join(head))
        # A single word that approval_lead.py already classes as a shared
        # moiety is a payload, not an agent: `vedotin` is the linker of at
        # least nine ADCs and `emtansine` of two. Reaching it alone means the
        # antibody half was outside the parenthesis and was not captured, so
        # the pair would decode a code to a fragment of the wrong resolution.
        if len(comps) == 1 and comps[0] in al.BLOCK:
            return None
        if len(comps) > 1 and not multiword_ok(comps):
            comps = comps[-1:]
            if comps[0] in al.BLOCK:
                return None
        return " ".join(comps), stem
    return None


# Second words that make a multi-word INN one molecule rather than two. Every
# entry names a moiety a molecule is BUILT FROM — a payload, a linker, a
# cell-therapy suffix, a vector, a salt, a chelator — not an agent in its own
# right. The list is the discriminator for the trap below.
MOIETY = set("""
vedotin deruxtecan govitecan mafodotin tansine emtansine ravtansine
soravtansine ozogamicin tirumotecan tazevibulin ecteribulin duocarmazine
pasudotox nesiran botansine autoleucel maraleucel leucel adenovec parepvec
obadenovec logene plasmid cedazuridine tetraxetan vipivotide dotatate
edotreotide acetate hyaluronidase pegol tazevibulin
""".split())


def multiword_ok(comps: list[str]) -> bool:
    """Is this multi-word phrase one INN, or two agents written side by side?

    THE TRAP. Requiring every word of a multi-word INN to carry a WHO stem
    fixes `efficacy pimicotinib` but not `cediranib durvalumab` or `olaparib
    durvalumab`, because both halves of a COMBINATION are also real INNs and
    both carry stems. Read as one name, `MEDI4736 -> olaparib durvalumab`
    decodes durvalumab's code to a regimen.

    The structural difference is that a genuine multi-word INN is an antibody
    plus a moiety, or a base plus a moiety — `sacituzumab govitecan`,
    `decitabine cedazuridine`, `obecabtagene autoleucel` — so either the head
    is an antibody (`-mab` in any of its infix forms) or the tail names a
    moiety. Two free-standing agents satisfy neither, and are cut back to the
    last word, which is the one the parenthesis was actually apposing.
    """
    return (comps[0].endswith("mab") or comps[-1] in MOIETY
            # `idecabtagene vicleucel`, `obecabtagene autoleucel`: the
            # cell-therapy vocabulary is open-ended (one new `-cabtagene`
            # per CAR construct), so it is matched by suffix rather than
            # enumerated, which a closed MOIETY list cannot do.
            or comps[0].endswith("cabtagene") or comps[-1].endswith("leucel"))


# ---------------------------------------------------------------------------
# Extraction: three appositive constructions, and nothing looser.
# ---------------------------------------------------------------------------

# Everything allowed to share a parenthesis with an INN without counting as
# residue. Same idea as first_in_human.GLUE, aimed at the other side.
INN_GLUE = re.compile(
    r"\b(formerly|previously|also|known|as|aka|or|and|now|generic|inn|"
    r"trade|brand|name|named|marketed|sold|the|its|a|an|drug|agent|"
    r"compound|molecule|tablets?|capsules?|injection|hydrochloride|"
    r"mesylate|maleate|tosylate|fumarate|succinate|phosphate|sulfate|"
    r"citrate|acetate|dihydrochloride)\b", re.I)

SPLIT = re.compile(r"[^A-Za-z0-9\-‐‑]+")

REGIMEN = re.compile(r"\+|\bwith\b|\bplus\b|\bversus\b|\bvs\b|"
                     r"\bfollowed\b|\bcombination\b|\bcombined\b", re.I)

# `<something> (<something>)`. The left group is bounded at 44 characters so
# it cannot reach backwards across a clause; the parenthesis interior at 70 so
# it cannot swallow a whole sentence.
APPOS = re.compile(r"([A-Za-z0-9][A-Za-z0-9\-‐‑ /\.]{0,44}?)\s*[\(\[]([^)\]]{2,70})[\)\]]")


def inn_only(inside: str) -> tuple[str, str] | None:
    """An INN phrase in a parenthesis holding essentially nothing else.

    Mirror of first_in_human.only_code, and the residue budget is the same
    eight characters, for the same reason: `(a potent and selective inhibitor
    of KRAS G12C, sotorasib-like)` must not read as an assertion of identity,
    and `(200 mg sotorasib)` is a dose, not a gloss.
    """
    # `AU-007 (+/- aldesleukin)` and `X (with pembrolizumab)` annotate a
    # REGIMEN inside the parenthesis. Read as a gloss they decode a code to
    # its combination partner. Narrower than COMBO on purpose: bare `and`
    # and `/` stay legal here, because `ASTX727 (decitabine and
    # cedazuridine)` is one co-formulated product and must survive.
    if REGIMEN.search(inside):
        return None
    toks = [t for t in SPLIT.split(inside) if t]
    got = inn_phrase(toks)
    if not got:
        return None
    phrase, stem = got
    chosen = set(phrase.split())
    # A SECOND drug name left over in the parenthesis means it is a list or a
    # regimen — `(olaparib, durvalumab)` — not a gloss on one agent. Caught
    # here rather than by the residue budget because `olaparib` is exactly
    # eight characters and would have slipped through it.
    if any(inn_stem(t) and t.lower() not in chosen for t in toks):
        return None
    residue = inside.lower()
    for w in chosen:
        residue = residue.replace(w, "")
    residue = INN_GLUE.sub("", residue)
    residue = re.sub(r"[^a-z0-9]", "", residue)
    return got if len(residue) <= 8 else None


# The single most productive false-positive generator in this file, and the
# reason `both_inside` needs its own guard. A parenthesis holding a code and
# an INN separated by `and`, `plus`, `with` or `+` is a REGIMEN, not a gloss:
# `(APL-1202 plus tislelizumab)`, `(AU-007 and aldesleukin)`, `(TAS-102 and
# oxaliplatin)`. Read as identity, each of those decodes a code to its
# combination partner — the worst failure available here, because the result
# is a plausible, well-formed, completely wrong mapping. `and` is allowed
# through in first_in_human.py's GLUE for the opposite reason (a co-formulated
# pair is one approval); in this direction it has to go.
COMBO = re.compile(r"\b(and|plus|with|combination|combined|versus|vs|"
                   r"followed|added|added to|co-?administered)\b|[+/&]", re.I)


# A THIRD CONSTRUCTION WAS BUILT, MEASURED, AND REMOVED. `both_inside`
# accepted a parenthesis holding one code and one INN — `(MK-3475,
# pembrolizumab)` — on the reasoning that it is the cleanest identity
# assertion in the corpus. It is not, because it is STRUCTURALLY IDENTICAL to
# a two-drug list: `(capecitabine, TAS-102)` has the same shape and asserts
# that the two agents are different. No amount of glue-word filtering
# separates them, since the difference is semantic and not syntactic.
#
# Measured rather than argued: of the nine pairs this construction was the
# sole source of, seven were wrong — `TAS-102 -> capecitabine`, `MRTX1133 ->
# sotorasib` (a G12D inhibitor decoded to a G12C inhibitor), `BMS-509744 ->
# ibrutinib`, `PJ34 -> olaparib`, `TAS0728 -> tucatinib`, `KK2269 ->
# docetaxel`, `PI3KI -> alpelisib`. Two were right. 22% precision against
# 95% for the two appositive constructions that remain, and two of the three
# errors in the hand audit came from here. It is deleted rather than patched:
# a construction that cannot be made to work is worth more as a recorded
# negative than as a tuned filter.


def coformulation(pre: str) -> bool:
    """Does the text before an INN show it is one HALF of a coformulation?

    `coformulated vibostolimab and pembrolizumab (MK-7684A)` is a true
    apposition, and reading it as `MK-7684A -> pembrolizumab` is still wrong:
    MK-7684A is the vibostolimab/pembrolizumab coformulation and pembrolizumab
    already owns MK-3475. The tell is a combination connector immediately
    before the captured INN with ANOTHER INN in front of it, which is a thing
    a single drug name never contains.
    """
    toks = [t for t in SPLIT.split(pre) if t][-6:]
    if not toks or not COMBO.search(" ".join(toks[-1:])):
        return False
    return any(inn_stem(t) for t in toks[:-1])


def extract(text: str) -> list[tuple[str, str, str, str]]:
    """(code, inn, stem, construction) asserted by apposition in `text`."""
    out = []
    for m in APPOS.finditer(text):
        left, inside = m.group(1), m.group(2)
        ltoks = [t for t in SPLIT.split(left) if t]
        if not ltoks:
            continue
        # (a) INN outside, code inside:  `sotorasib (AMG 510)`
        codes = {norm_code(c) for c in fih.only_code(inside)}
        codes.discard(None)
        if codes:
            got = inn_phrase(ltoks)
            if got and not norm_code(ltoks[-1]):
                # The stem-bearing token must be the LAST token before the
                # parenthesis. `treated with sotorasib and trametinib (AMG
                # 510)` would otherwise attach the code to trametinib.
                nwords = len(got[0].split())
                pre = " ".join(ltoks[:len(ltoks) - nwords])
                if inn_stem(ltoks[-1]) and not coformulation(pre):
                    for c in codes:
                        out.append((c, got[0], got[1], "inn(code)"))
        # (b) code outside, INN inside:  `AMG 510 (sotorasib)`
        c = norm_code(ltoks[-1])
        if c:
            got = inn_only(inside)
            if got:
                out.append((c, got[0], got[1], "code(inn)"))
    return out


# ---------------------------------------------------------------------------
# Target resolution, by vote over the corpus.
# ---------------------------------------------------------------------------

SYM = r"([A-Za-z][A-Za-z0-9]{1,11}(?:[-/\.][A-Za-z0-9]{1,6}){0,2})"
TARGET_PATS = [
    (re.compile(r"\banti[-\s]?" + SYM), "anti-X"),
    (re.compile(SYM + r"[-\s](?:inhibitor|antagonist|agonist|degrader|blocker)"), "X inhibitor"),
    (re.compile(r"(?:target|targets|targeting|targeted|directed against|"
                r"specific for)\s+(?:the\s+)?" + SYM), "targeting X"),
    (re.compile(SYM + r"[-\s](?:directed|targeting|targeted|specific)"), "X-directed"),
    (re.compile(SYM + r"[\s-](?:bispecific|CAR[- ]?T|ADC|antibody[- ]drug)"), "X bispecific"),
]

# Words that match SYM and are never a target. Kept short on purpose: the
# vote, not the block list, is what makes this column usable, and a block
# list here would be an invitation to curate the answer.
NOT_TARGET = set("""
tumor tumour tumors tumours cancer cancers cell cells patient patients human
mouse mice murine this that these those which their there other another such
the a an and or of to in on at by for with from into is are was were be been
therapy therapies treatment treatments drug drugs agent agents combination
novel potent selective oral small molecule first class new dual multi
receptor protein kinase pathway target targets targeting disease control
efficacy activity response responses safety dose doses phase study trial
group groups arm arms cohort cohorts model models line lines type types
immune immunotherapy chemotherapy radiotherapy checkpoint blockade tumor
antibody antibodies conjugate conjugates bispecific specific vaccine
positive negative expressing expression mutant mutation wild high low
adc adcs tki tkis car cars mab mabs ici icis ic50 ec50 mtd rp2d dlt orr
inhibition activation signaling signalling mechanism mechanisms function
""".split())


TARGET_WINDOW = 90


def target_windows(text: str, needles: list[re.Pattern[str]]) -> list[str]:
    """Text within TARGET_WINDOW characters of a mention of the agent.

    WHY A WINDOW AND NOT A SENTENCE. Voting over whole sentences returns
    `PD-1` for almost everything, because almost every oncology abstract
    names pembrolizumab or an anti-PD-1 backbone somewhere in the same
    sentence as the agent under study. A dry run over sentences gave
    `CA-4948 -> PD-1` (it is an IRAK4 inhibitor), `CTL-002 -> PD-1` (GDF-15),
    `TST001 -> PD-1` (CLDN18.2) and `SAR408701 -> PD-1` (CEACAM5): four
    wrong answers, all the same wrong answer, all produced by a combination
    partner sitting eighty words away. Ninety characters is roughly the
    reach of the appositive constructions the patterns are written for —
    `sotorasib, a KRAS G12C inhibitor` and `the anti-TIGIT antibody
    tiragolumab` — and outside that reach the association is topical rather
    than grammatical.
    """
    # The needles come from first_in_human.code_pat / alias_pat, which are
    # built lowercase; matching happens on the folded copy and slicing on the
    # original, which is index-safe because str.lower() is length-preserving
    # for the ASCII this corpus is stored in.
    low = text.lower()
    out = []
    for pat in needles:
        for m in pat.finditer(low):
            out.append((text[max(0, m.start() - TARGET_WINDOW):m.start()],
                        text[m.end():m.end() + TARGET_WINDOW]))
    return out


def target_vote(windows) -> tuple[str, str, int, int]:
    """(target, how, votes_for_winner, votes_total) over (left, right) windows.

    THE COMBINATION LEAK, AND WHY THE WINDOW ALONE DOES NOT CLOSE IT.
    Narrowing from a sentence to ninety characters removes the far-away
    backbone but not the near one: `evaluating CTL-002 in combination with
    an anti-PD-1 antibody` puts `anti-PD-1` eight words from the agent, and
    visugromab is an anti-GDF-15 antibody. So the span BETWEEN the agent and
    the candidate target is checked for combination language, and a target
    that can only be reached by crossing a `with` / `plus` / `and` /
    `following` is not counted. What survives is the appositive reading —
    the target as a modifier of the agent — which is the only reading that
    licenses the inference.
    """
    votes: collections.Counter[tuple[str, str]] = collections.Counter()
    for left, right in windows:
        for side, s in (("l", left), ("r", right)):
            for pat, how in TARGET_PATS:
                for m in pat.finditer(s):
                    between = s[m.end():] if side == "l" else s[:m.start()]
                    if COMBO.search(between):
                        continue
                    sym = m.group(1).strip("-/.")
                    if (len(sym) < 2 or sym.lower() in NOT_TARGET
                            or not re.search(r"[A-Za-z]", sym)):
                        continue
                    # A target symbol is upper-case-bearing or contains a
                    # digit. Lower-case English words that survive NOT_TARGET
                    # are far more likely prose than a gene.
                    if not (any(ch.isupper() for ch in sym)
                            or any(ch.isdigit() for ch in sym)):
                        continue
                    votes[(sym.upper(), how)] += 1
    if not votes:
        return "", "", 0, 0
    # Collapse the how-dimension: the same symbol found by two constructions
    # is one target with two witnesses, not two targets.
    by_sym: collections.Counter[str] = collections.Counter()
    hows: dict[str, set[str]] = {}
    for (sym, how), n in votes.items():
        by_sym[sym] += n
        hows.setdefault(sym, set()).add(how)
    sym, n = by_sym.most_common(1)[0]
    return sym, "+".join(sorted(hows[sym])), n, sum(by_sym.values())


# ---------------------------------------------------------------------------
# ClinicalTrials.gov, cached
# ---------------------------------------------------------------------------

class Registry:
    def __init__(self, offline: bool):
        self.dir = CACHE / "ctgov"
        self.dir.mkdir(parents=True, exist_ok=True)
        self.offline = offline
        self.calls = self.hits = 0

    def fetch(self, term: str) -> list[dict]:
        p = self.dir / (re.sub(r"[^A-Za-z0-9._-]", "_", term)[:100] + ".json.gz")
        if p.exists():
            self.hits += 1
            with gzip.open(p, "rt") as fh:
                return json.load(fh)
        if self.offline:
            return []
        params = {"query.intr": term, "pageSize": str(PAGE), "fields": FIELDS,
                  "filter.advanced": "AREA[StudyType]INTERVENTIONAL"}
        url = API + "?" + urllib.parse.urlencode(params)
        recs = []
        for attempt in range(3):
            try:
                with urllib.request.urlopen(
                        urllib.request.Request(url, headers=UA), timeout=60) as fh:
                    data = json.load(fh)
                for s in data.get("studies", []):
                    ps = s.get("protocolSection", {})
                    ivs = ps.get("armsInterventionsModule", {}).get("interventions", []) or []
                    recs.append({
                        "nct": ps.get("identificationModule", {}).get("nctId", ""),
                        "title": ps.get("identificationModule", {}).get("briefTitle", "") or "",
                        "ivs": [{"name": iv.get("name", "") or "",
                                 "other": iv.get("otherNames", []) or []} for iv in ivs],
                    })
                break
            except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as e:
                if attempt == 2:
                    print(f"    ! {term}: {e}", file=sys.stderr)
                    return []
                time.sleep(2 ** attempt)
        self.calls += 1
        time.sleep(SLEEP)
        with gzip.open(p, "wt") as fh:
            json.dump(recs, fh)
        return recs


# ---------------------------------------------------------------------------
# Opacity residue — the measurement that decides whether this was worth it.
# ---------------------------------------------------------------------------

# Reproduces threads.yml next-gen-checkpoints.blind_spot as closely as a
# re-derivation can. The recorded rule: phase-1 oncology trials first posted
# in 2025 (n = 1,473 — matched exactly here), opaque if title + interventions
# name no drug and no target. Recorded residues: 42% (614/1,473) on title +
# interventions, 34% (500/1,473) once brief_summary and the arm-group fields
# are included. This file's rule returns 626 (42%) and 480 (33%) on the same
# two field sets, so it reproduces the first figure to within 2% and the
# second to within 4%. The original script was a scratchpad one-off and was
# not committed, so exact reproduction is not available; what matters is that
# ONE rule, stated here, is applied identically before and after the decoder.
OPACITY_SQL = """
SELECT nct_id, COALESCE(title,''), COALESCE(interventions,''),
       COALESCE(brief_summary,''), COALESCE(arm_labels,''),
       COALESCE(arm_descriptions,''), COALESCE(arm_interventions,''),
       COALESCE(lead_sponsor,'')
  FROM ct_trials
 WHERE substr(date,1,4)=? AND onc_conditions=1
   AND (phases LIKE '%PHASE1%' OR phases LIKE '%EARLY_PHASE1%')
"""

OPAQUE_TARGET = re.compile(
    r"\banti[-\s]?[A-Za-z][A-Za-z0-9]{1,9}\b"
    r"|\b[A-Za-z][A-Za-z0-9]{1,9}[-\s](?:inhibitor|agonist|antagonist|degrader|blocker)"
    r"|targeting\s+[A-Za-z][A-Za-z0-9]{1,9}"
    r"|directed against\s+[A-Za-z][A-Za-z0-9]{1,9}"
    r"|\b[A-Za-z][A-Za-z0-9]{1,9}[-\s]directed"
    r"|CAR[-\s]?T|chimeric antigen", re.I)


def names_a_drug(text: str) -> bool:
    return any(inn_stem(w) for w in SPLIT.split(text))


def opaque(text: str) -> bool:
    return not names_a_drug(text) and not OPAQUE_TARGET.search(text)


def dark_targets(rcon, ccon, year: str) -> int:
    """Why the decoder misses the dark set — the diagnostic behind the null.

    A code->INN decoder can only close a dark trial if the meeting named the
    agent AND named its INN. Those are two different conditions and this
    separates them, because the answer decides what the null result means:

      if the corpus does not mention the dark codes at all, the populations
      are disjoint and no amount of extraction quality would help;
      if it mentions them but never with an INN, the INN is what is missing,
      not the corpus — the agents are pre-INN, and a code->TARGET map off the
      same text would close what a code->INN map cannot.

    Both are measured. The second is the interesting one and its precision is
    NOT the precision of the shipped table — a target here is a vote over
    prose, is reported with its vote counts, and several are visibly wrong
    (an oncolytic virus voted `PD-1` off its combination partner). It is a
    diagnostic, not a deliverable, which is why it prints and does not write.
    """
    rows = rcon.execute(OPACITY_SQL, (year,)).fetchall()
    op = [r for r in rows if opaque(" ".join(r[i] for i in (1, 2, 3, 4, 5, 6)))]
    dark: set[str] = set()
    for r in op:
        for t in SPLIT.split(" ".join(r[i] for i in (1, 2))):
            c = norm_code(t)
            if c:
                dark.add(code_key(c))
    print(f"{len(op)} opaque trials in {year}; {len(dark)} distinct codes in them")
    wins: dict[str, list] = collections.defaultdict(list)
    inn_near: set[str] = set()
    for _doi, _v, title, abst in ccon.execute(
            "SELECT doi, venue, COALESCE(title,''), COALESCE(abstract,'') "
            "FROM abstracts WHERE abstract IS NOT NULL AND length(abstract) > 200"):
        text = title + ". " + abst
        seen = {code_key(t) for t in SPLIT.split(text)} & dark
        for ck in seen:
            pat = fih.code_pat(ck)
            wins[ck].extend(target_windows(text, [pat]))
            for w in target_windows(text, [pat]):
                if any(inn_stem(t) for t in SPLIT.split(w[0] + " " + w[1])):
                    inn_near.add(ck)
    print(f"  mentioned anywhere in the conference corpus : {len(wins)}")
    print(f"  ... with any INN-shaped word within 90 chars: {len(inn_near)}")
    got = 0
    for ck in sorted(wins):
        t, how, v, n = target_vote(wins[ck])
        if t:
            got += 1
        print(f"    {ck:<12} win={len(wins[ck]):3} target={t:<14} {v}/{n} {how}")
    print(f"  ... with a target resolved by vote          : {got}")
    return 0


# ---------------------------------------------------------------------------

def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--out", default=str(OUT_TSV))
    ap.add_argument("--ctgov", action="store_true",
                    help="validate candidate codes against ClinicalTrials.gov "
                         "(polite: 0.7 s between calls, cached on disk)")
    ap.add_argument("--audit", type=int, default=0,
                    help="print N randomly sampled rows for hand audit")
    ap.add_argument("--audit-seed", type=int, default=20260827)
    ap.add_argument("--opacity-only", action="store_true")
    ap.add_argument("--dark-targets", action="store_true",
                    help="diagnostic: for every code in the opaque residue, "
                         "does the conference corpus mention it at all, and "
                         "does it name a target for it?")
    ap.add_argument("--year", default="2025")
    args = ap.parse_args()

    CACHE.mkdir(parents=True, exist_ok=True)
    ccon = sqlite3.connect(f"file:{CONF}?mode=ro", uri=True)
    rcon = sqlite3.connect(f"file:{REG}?mode=ro", uri=True)
    jcon = sqlite3.connect(f"file:{INDEX}?mode=ro", uri=True) if INDEX.exists() else None

    if args.opacity_only:
        rows = rcon.execute(OPACITY_SQL, (args.year,)).fetchall()
        for label, idx in (("title+interventions", (1, 2)),
                           ("+brief_summary+arms", (1, 2, 3, 4, 5, 6))):
            n = sum(1 for r in rows if opaque(" ".join(r[i] for i in idx)))
            print(f"{label:24} {n:5}/{len(rows)}  {n / len(rows) * 100:.0f}%")
        return 0

    if args.dark_targets:
        return dark_targets(rcon, ccon, args.year)

    # -- stage 1: extraction -------------------------------------------------
    print("stage 1  extracting appositions from the conference corpus ...")
    abstracts = ccon.execute(
        "SELECT doi, venue, COALESCE(title,''), COALESCE(abstract,'') "
        "FROM abstracts WHERE abstract IS NOT NULL AND length(abstract) > 200"
    ).fetchall()
    print(f"         {len(abstracts)} full-text abstracts")

    # pair -> {dois, constructions, venues}
    pairs: dict[tuple[str, str], dict] = {}
    naive = set()
    for doi, venue, title, abst in abstracts:
        text = title + ". " + abst
        if "(" not in text and "[" not in text:
            continue
        # The unfiltered count, for the report's before/after line: the same
        # apposition scan with the type tests on both sides switched off.
        for m in APPOS.finditer(text):
            lt = [t for t in SPLIT.split(m.group(1)) if t]
            it = [t for t in SPLIT.split(m.group(2)) if t]
            if lt and it and fih.CODE_RE.fullmatch(lt[-1] or "") and it[0].isalpha():
                naive.add((lt[-1].upper(), it[0].lower()))
            if lt and it and fih.CODE_RE.fullmatch(it[0] or "") and lt[-1].isalpha():
                naive.add((it[0].upper(), lt[-1].lower()))
        for code, inn, stem, how in extract(text):
            rec = pairs.setdefault((code_key(code), inn), {
                "code": code, "inn": inn, "stem": stem,
                "spellings": set(), "dois": set(), "hows": set(), "venues": set()})
            rec["spellings"].add(code)
            rec["dois"].add(doi)
            rec["hows"].add(how)
            rec["venues"].add(venue)
    print(f"         naive apposition (no type tests) : {len(naive)} pairs")
    print(f"         typed extraction                 : {len(pairs)} pairs")
    state = CACHE / "pairs.json"
    state.write_text(json.dumps(
        [{**v, "spellings": sorted(v["spellings"]), "dois": sorted(v["dois"]),
          "hows": sorted(v["hows"]), "venues": sorted(v["venues"])}
         for v in pairs.values()], indent=1))
    print(f"         state -> {state}")

    # -- stage 2: validation -------------------------------------------------
    print("stage 2  validating ...")
    codes = {v["code"] for v in pairs.values()}
    inns = {v["inn"] for v in pairs.values()}
    inn_head = {i.split()[0] for i in inns} | {i.split()[-1] for i in inns}

    # (a) repeat: the same apposition in two different DOIs. Free.
    for v in pairs.values():
        v["support"] = set()
        if len(v["dois"]) >= 2:
            v["support"].add("repeat")

    # (b) cooc: code and INN in a DIFFERENT abstract. One pass over the corpus,
    #     indexed by code key so this is not len(pairs) x len(abstracts).
    by_code: dict[str, list[dict]] = collections.defaultdict(list)
    for v in pairs.values():
        by_code[code_key(v["code"])].append(v)
    for doi, venue, title, abst in abstracts:
        text = (title + ". " + abst)
        low = text.lower()
        toks = {t for t in SPLIT.split(text) if t}
        seen = {code_key(t) for t in toks} & set(by_code)
        if not seen:
            continue
        for ck in seen:
            for v in by_code[ck]:
                if doi in v["dois"]:
                    continue
                if all(w in low for w in v["inn"].split()):
                    v["support"].add("cooc")
                    v.setdefault("cooc_doi", doi)

    # (c) trial: code and INN in the same ct_trials row. Also the source of
    #     the NCT ids written to the TSV, which is what makes a row auditable
    #     against a registry record rather than only against prose.
    trial_rows = rcon.execute(
        "SELECT nct_id, COALESCE(title,''), COALESCE(interventions,''), "
        "COALESCE(brief_summary,''), COALESCE(arm_labels,''), "
        "COALESCE(arm_descriptions,''), COALESCE(arm_interventions,'') "
        "FROM ct_trials").fetchall()
    print(f"         scanning {len(trial_rows)} registry rows ...")
    for row in trial_rows:
        text = " ".join(row[1:])
        low = text.lower()
        toks = {t for t in SPLIT.split(text) if t}
        seen = {code_key(t) for t in toks} & set(by_code)
        for ck in seen:
            for v in by_code[ck]:
                if all(w in low for w in v["inn"].split()):
                    v["support"].add("trial")
                    v.setdefault("ncts", set()).add(row[0])

    # (d) journal titles: same test, one more independent text.
    if jcon:
        for (title,) in jcon.execute("SELECT COALESCE(title,'') FROM papers"):
            if "(" not in title and not any(ch.isdigit() for ch in title):
                continue
            low = title.lower()
            toks = {t for t in SPLIT.split(title) if t}
            for ck in {code_key(t) for t in toks} & set(by_code):
                for v in by_code[ck]:
                    if all(w in low for w in v["inn"].split()):
                        v["support"].add("journal")

    # (e) ctgov: the external check. Query the CODE and demand the INN come
    #     back — first_in_human.py's own validation rule, in its own direction.
    reg = Registry(offline=not args.ctgov)
    if args.ctgov:
        print(f"         ctgov: {len(codes)} codes to query "
              f"(~{len(codes) * SLEEP / 60:.0f} min uncached) ...")
    for k, code in enumerate(sorted(codes), 1):
        recs = reg.fetch(code)
        if not recs:
            continue
        for v in by_code[code_key(code)]:
            for r in recs:
                blob = " ".join([r["title"]] + [iv["name"] for iv in r["ivs"]]
                                + [o for iv in r["ivs"] for o in iv["other"]]).lower()
                if all(w in blob for w in v["inn"].split()):
                    v["support"].add("ctgov")
                    v.setdefault("ncts", set()).add(r["nct"])
                    break
        if args.ctgov and k % 50 == 0:
            print(f"           {k}/{len(codes)}  calls={reg.calls} cached={reg.hits}")

    # -- stage 3: conflict ---------------------------------------------------
    # One code -> several INNs. Co-formulations and renamed programmes are
    # legitimate; two unrelated molecules are not. The discriminator is
    # whether the INNs share evidence: co-formulated agents appear in the same
    # trial and the same abstract, unrelated ones do not.
    ambiguous = 0
    for ck, vs in by_code.items():
        if len(vs) < 2:
            continue
        for v in vs:
            others = [o for o in vs if o is not v]
            shared = any(v["dois"] & o["dois"]
                         or (v.get("ncts") or set()) & (o.get("ncts") or set())
                         for o in others)
            # A shared word means one is a longer spelling of the other
            # (`vedotin` vs `disitamab vedotin`), not a conflict.
            samefam = any(set(v["inn"].split()) & set(o["inn"].split()) for o in others)
            if not (shared or samefam):
                v["ambiguous"] = True
                ambiguous += 1
    print(f"         {ambiguous} pair(s) demoted to ambiguous by conflict rule")

    # -- stage 4: targets ----------------------------------------------------
    print("stage 3  resolving targets by windowed vote ...")
    want = {code_key(v["code"]) for v in pairs.values()}
    inn_index: dict[str, list[dict]] = collections.defaultdict(list)
    for v in pairs.values():
        inn_index[v["inn"].split()[0]].append(v)
        # One needle per agent, matching every spelling of the code and the
        # INN's leading word, so `AMG-510`, `AMG 510` and `sotorasib` all
        # open the same window.
        alts = sorted({fih.code_pat(c).pattern for c in v["spellings"]})
        alts.append(fih.alias_pat(v["inn"].split()[0]).pattern)
        v["needle"] = re.compile("|".join(alts))
    for doi, venue, title, abst in abstracts:
        text = title + ". " + abst
        low = text.lower()
        toks = {t for t in SPLIT.split(text) if t}
        hit_codes = {code_key(t) for t in toks} & want
        hit_inns = {t.lower() for t in toks} & set(inn_index)
        if not hit_codes and not hit_inns:
            continue
        seen: set[int] = set()
        cands = [v for ck in hit_codes for v in by_code[ck]]
        cands += [v for h in hit_inns for v in inn_index[h]]
        for v in cands:
            if id(v) in seen:
                continue
            seen.add(id(v))
            v.setdefault("win", []).extend(target_windows(text, [v["needle"]]))
    for v in pairs.values():
        v["target"], v["target_how"], v["tv"], v["tn"] = target_vote(
            v.get("win", [])[:600])

    # -- stage 5: write ------------------------------------------------------
    def confidence(v) -> str:
        sup = v["support"]
        if v.get("ambiguous"):
            return "ambiguous"
        if {"ctgov", "trial"} & sup and ("repeat" in sup or len(sup) >= 2):
            return "high"
        if {"ctgov", "trial"} & sup or "repeat" in sup:
            return "medium"
        if sup:
            return "low"
        return "unsupported"

    cols = ["code", "inn", "target", "inn_stem", "resolved_by", "support",
            "confidence", "n_abstracts", "dois", "ncts", "spellings",
            "target_how", "target_votes", "venues"]
    lines = ["\t".join(cols)]
    rows_out = []
    for (ck, inn), v in sorted(pairs.items()):
        conf = confidence(v)
        row = [
            v["code"], v["inn"], v.get("target", ""), v["stem"],
            "+".join(sorted(v["hows"])),
            "+".join(sorted(v["support"])) or "none",
            conf,
            str(len(v["dois"])),
            ";".join(sorted(v["dois"])[:4]),
            ";".join(sorted(v.get("ncts", set()))[:4]),
            "|".join(sorted(v["spellings"])),
            v.get("target_how", ""),
            f"{v.get('tv', 0)}/{v.get('tn', 0)}",
            "|".join(sorted(v["venues"])),
        ]
        rows_out.append((conf, row))
        lines.append("\t".join(x.replace("\t", " ").replace("\n", " ") for x in row))
    pathlib.Path(args.out).write_text("\n".join(lines) + "\n")
    dist = collections.Counter(c for c, _ in rows_out)
    print(f"wrote {args.out}  ({len(rows_out)} rows)")
    print("         confidence:", " ".join(f"{k}={dist[k]}" for k in
          ("high", "medium", "low", "unsupported", "ambiguous")))
    ship = {k: v for k, v in pairs.items() if confidence(v) in ("high", "medium")}
    print(f"         shippable (high|medium)          : {len(ship)} pairs, "
          f"{len({code_key(v['code']) for v in ship.values()})} distinct codes")
    print(f"         with a resolved target           : "
          f"{sum(1 for v in ship.values() if v.get('target'))}")

    # -- stage 6: does it close the blind spot? ------------------------------
    print()
    print("stage 4  opacity residue, threads.yml next-gen-checkpoints.blind_spot")
    lookup: dict[str, dict] = {}
    for (ck, inn), v in pairs.items():
        if confidence(v) in ("high", "medium"):
            lookup.setdefault(ck, v)
    rows = rcon.execute(OPACITY_SQL, (args.year,)).fetchall()
    print(f"         denominator: {len(rows)} phase-1 oncology trials "
          f"first posted in {args.year}")
    closed_rows = []
    for label, idx in (("title+interventions", (1, 2)),
                       ("+brief_summary+arms", (1, 2, 3, 4, 5, 6))):
        op = [r for r in rows if opaque(" ".join(r[i] for i in idx))]
        closed = []
        for r in op:
            text = " ".join(r[i] for i in idx)
            for t in SPLIT.split(text):
                v = lookup.get(code_key(t))
                if v:
                    closed.append((r[0], t, v["inn"], v.get("target", ""), r[7]))
                    break
        print(f"         {label:22} opaque {len(op):5}/{len(rows)} "
              f"({len(op) / len(rows) * 100:.0f}%)  ->  decoder closes "
              f"{len(closed):3} ({len(closed) / len(rows) * 100:.1f} pts), "
              f"residue {len(op) - len(closed)} "
              f"({(len(op) - len(closed)) / len(rows) * 100:.0f}%)")
        if idx == (1, 2, 3, 4, 5, 6):
            closed_rows = closed
    if closed_rows:
        print("         trials made legible:")
        for nct, code, inn, tgt, spon in closed_rows[:40]:
            print(f"           {nct}  {code:<14} -> {inn:<28} {tgt:<10} {spon[:28]}")

    # How much of the dark set is even code-shaped and how much of that the
    # decoder covers — the number that says whether the miss is a coverage
    # problem or a population problem.
    op = [r for r in rows if opaque(" ".join(r[i] for i in (1, 2, 3, 4, 5, 6)))]
    dark_codes: collections.Counter[str] = collections.Counter()
    for r in op:
        for t in SPLIT.split(" ".join(r[i] for i in (1, 2))):
            c = norm_code(t)
            if c:
                dark_codes[code_key(c)] += 1
    covered = sum(1 for c in dark_codes if c in lookup)
    print(f"         distinct codes in the dark set   : {len(dark_codes)}")
    print(f"         of those, present in the decoder : {covered}")
    known_any = sum(1 for c in dark_codes if c in by_code)
    print(f"         present at any confidence        : {known_any}")

    # -- audit sample --------------------------------------------------------
    if args.audit:
        print()
        print(f"AUDIT SAMPLE  n={args.audit}  seed={args.audit_seed}  "
              f"(population: confidence in high|medium)")
        pool = [r for c, r in rows_out if c in ("high", "medium")]
        rnd = random.Random(args.audit_seed)
        for r in rnd.sample(pool, min(args.audit, len(pool))):
            print(f"  {r[0]:<16} {r[1]:<32} tgt={r[2]:<12} {r[6]:<7} "
                  f"{r[5]:<22} n={r[7]} {r[4]}")
    print(f"\nctgov: {reg.calls} HTTP calls, {reg.hits} cache hits")
    return 0


if __name__ == "__main__":
    sys.exit(main())
