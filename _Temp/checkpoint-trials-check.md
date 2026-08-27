# Did any newly nominated checkpoint enter a phase 1 in 2025?

The check `data/sources.yml` set for itself under `r-clinicaltrials-gov`, run against
`data/regulatory.sqlite` for the first time. Scratch working note — not part of the site.

Run 2026-08-27. All stores opened read-only (`file:...?mode=ro`). Nothing was modified.

---

## 1. The claim as written

Two texts state it, and they are not the same statement.

**`data/sources.yml`, `r-clinicaltrials-gov` → `harvest.notes`:**

> Used to check whether a nominated target has any registered trial. The
> finding that no newly nominated checkpoint entered a phase 1 anywhere in
> 2025 was read off the literature only and should be confirmed here.

**`data/threads.yml`, thread `next-gen-checkpoints` → `note` (final two sentences):**

> Across all of 2025 not one newly nominated checkpoint entered a phase 1.
> 2025-10 returned zero hits for the entire target list.

Thread claim (the parent statement being tested): *"Targets beyond PD-1/CTLA-4 deliver a
second generation of checkpoint blockade."* `opened: 2024-03`.

**Reconciliation.** sources.yml is the honest version: it labels the finding as read off
the literature and flags it as unconfirmed. threads.yml states it flatly, with no such
qualifier, inside a `note` — and a `note` is the one field in that file with no
provenance discipline attached to it. The two also differ in scope: sources.yml says
"anywhere", which is a claim about the trial registry; threads.yml says nothing about
where, and in context ("2025-10 returned zero hits for the entire target list") it is
plainly a claim about *literature search hits*, not registrations. The second sentence
in threads.yml is a fact about a month's reading and should never have been adjacent to
a sentence about phase 1 entry. That adjacency is what made a literature observation
read as a registry fact.

**Status and evidence count.** `threads.yml` deliberately stores no status — it is
derived by `scripts/build_briefing.py:status_of()` from the cards, with `MIN_N = 5`.
`data/evidence.yml` carries **32 cards** on `next-gen-checkpoints`: **13 supports,
19 refutes**. Under that rule (n=32 ≥ 5; refutes 19 > supports 13; but 19 < 2×13=26)
the derived status is **`contested`**, not `crisis`. Worth noting because the note's
prose ("the category is dissolving") reads considerably more terminal than the cards
support.

---

## 2. Method

### 2.1 How the target list was derived

Not from recall. Two corpus-internal passes, both scripted:

**Pass A — journal index (`data/index.sqlite`, 35,542 titles, 2024-01..2026-08).**
Selected every title matching
`checkpoint|co-?inhibitory|co-?stimulatory|immune evasion|don'?t[- ]eat[- ]me|inhibitory receptor`
→ 398 titles. From each, extracted gene-symbol-shaped tokens
(`\b[A-Z][A-Z0-9]{1,9}(-[A-Za-z0-9]{1,4})?\b` plus `Xxxxx-\d{1,2}` for `Siglec-10`,
`CLEVER-1` forms) and ranked by document frequency. Note the index stores **titles only**
— no abstracts — so this pass is low-recall by construction and was used to *confirm*
candidates rather than to generate them exhaustively.

**Pass B — 2024 conference abstracts (`data/conference.sqlite`, aacr-2024 n=7,326 +
asco-2024 n=7,569, full abstract text).** Split each abstract into sentences, kept
sentences matching the same context regex (3,005 sentences), extracted symbols by the
same rule, counted once per abstract.

**Pass C — false-negative sweep over the registry itself.** Over all 4,214 phase-1
oncology trials, extracted every string following
`anti[- ]|α-|targeting |directed (against|at) |bispecific (antibody )?(targeting )?`
→ 167 distinct declared targets. This is what caught GARP, LLT1, LILRA6, CD94 and CD83,
none of which the literature passes would have surfaced as checkpoint terms.

Candidates were then sorted into tiers by **when the corpus itself first names them**:

| tier | definition |
|---|---|
| **A — established** | the six named in the task: PD-1, PD-L1, CTLA-4, LAG-3, TIM-3, TIGIT |
| **B — prior wave** | non-PD-1 co-inhibitory targets already clinical-stage *before* the 2024-01 window opens. Nominated, but not newly |
| **C — newly nominated** | first named as an immunotherapy target inside this corpus's own 2024-01..2026-08 material. This is the tier the claim is about |
| **D — co-stimulatory agonists** | ICOS, OX40, 4-1BB, GITR, CD40, CD27. Surfaced by the same regex; reported but not counted as checkpoints |

**Tier C, with the corpus citation that put it there:**

| target | corpus evidence for the nomination |
|---|---|
| IGSF8 | *IGSF8 is an innate immune checkpoint and cancer immunotherapy target*, Cell 2024-05 |
| ITPRIPL1 | *ITPRIPL1 binds CD3ε to impede T cell activation…*, Cell 2024-04 |
| BTN1A1 | *BTN1A1 is a novel immune checkpoint mutually exclusive to PD-L1*, JITC 2024-03 |
| SLC6A6 | *Cancer SLC6A6-mediated taurine uptake transactivates immune checkpoint genes*, Cell 2024-04 |
| LRIG1 | *LRIG1 engages ligand VISTA and impairs tumor-specific CD8+ T cell responses*, Sci Immunol 2024-05 |
| Siglec-10 | *Identification of Siglec-10 as a new dendritic cell checkpoint*, JITC 2024-08 |
| CLEVER-1 (STAB1) | JITC 2025-05 and 2025-12 — named in the thread note |
| PSGL-1 (SELPLG) | *PSGL-1 is a phagocytosis checkpoint*, Sci Immunol 2025-06 (also card `ev-2025-06-40512837`) |
| CISH | Lancet Oncol 2025-05 (card `ev-2025-05-40315882`) |
| CD300e | JITC 2025-12 — named in the thread note |
| TIPE2 | JITC 2025-12 — named in the thread note |
| NEAT1 | JITC 2025-12 — named in the thread note |
| CD161 / LLT1 (KLRB1/CLEC2D) | 3 journal titles, 9+3 abstracts |
| GARP (LRRC32) | Cancer Discov / JITC 2026-02 ×2 (*GARP/TGFβ axis*), 6 abstracts |
| VSIG4 | 2 journal titles 2026-06, incl. *"…metabolic-ionic checkpoint"* |
| TIM-4 | 1 journal title 2026-05 |
| SIGLEC11 / Siglec-E | JITC 2025-01 ×2 |

**Tier B** (prior wave): CD47/SIRPα, B7-H3/CD276, VISTA, NKG2A, CD155/PVR, PVRIG,
IDO1, CD73, CD39, HPK1, LILRB1/2/4 (ILT2/3/4), BTLA/HVEM, Siglec-15, CD24, TREM2,
CD96, B7-H4, MERTK, IL-18BP, CD200R.

### 2.2 Inclusion rule for trials

```sql
FROM ct_trials
WHERE onc_conditions = 1
  AND phases IN ('PHASE1', 'PHASE1; PHASE2', 'EARLY_PHASE1')
```
→ **4,214 trials** of the 16,145 oncology rows. A trial counts as a hit for target *T*
if `title || ' || ' || interventions` matches any of *T*'s name regexes **or** any of
*T*'s known agent names (INN or code). Every Tier B/C/D hit — 60-odd rows — was then
**read individually** and classified; only the Tier A counts are left unread, because
they run to hundreds and Tier A is not what the claim is about.

### 2.3 Which date

Binned on **`date` = `studyFirstPostDate`**, because the claim is about a trial
*entering* phase 1 — becoming a registered, public, recruiting programme — and that is
the event `studyFirstPostDate` records. `start_date` is partly prospective: 147 rows in
the oncology set carry a start date in 2027-2030, and rows first posted in 2026 carry
start dates as early as 1991.

**Sensitivity checked, and it does not change the answer.** Rebinned on
`substr(start_date,1,4)` the Tier C row is still 2024:1 / **2025:0** / 2026:2. The
choice moves individual trials in both directions — NCT07461181 (anti-OX40 CS01) is
first posted 2026-03 but started 2024-12; NCT06487624 (SIRPα-PD-L1-TGFβ, HCB301) is
posted 2024-07 but started 2025-04 — and it moves the Tier A totals by 10-30%, but no
Tier C trial crosses into 2025 under either field.

### 2.4 Backbone versus target — how the two were separated

This is the trap the task flags, and it bites almost entirely on Tier A. Each hit
records *why* it matched. A hit was classed **backbone-only** when the sole match was a
marketed anti-PD-(L)1/CTLA-4/LAG-3 INN and no target string appeared in the text:

| | 2024 | 2025 | 2026 |
|---|---|---|---|
| PD-1, marketed-drug-only (backbone) | 147 | 127 | 85 |
| PD-1, target named in text | 41 | 48 | 30 |
| PD-L1, backbone / named | 52 / 14 | 27 / 6 | 11 / 8 |
| CTLA-4, backbone / named | 11 / 3 | 16 / 7 | 11 / 4 |

So roughly **three-quarters of every PD-1 "hit" is a trial of something else that
happens to be given with pembrolizumab or nivolumab.** Reading the raw 175 as "175
PD-1 trials in 2025" would be the confident wrong answer this exercise is designed to
produce.

For Tier B and C the problem inverts and mostly disappears — nobody administers
anti-VISTA or bexmarilimab as a backbone — but two false positives survived keyword
matching and were killed on reading:

- **BTN1A1 / "STAR-001"** (NCT07431216, 2026-02) — the intervention is
  `STAR-001 (LP-184)`, Lantern/Starlight's acylfulvene alkylator. Name collision with
  the anti-BTN1A1 antibody programme. **Not a checkpoint trial.** Had this one been
  taken at face value it would have produced a false 2026 refutation.
- **PVRIG / "nadunolimab"** (NCT06548230, NCT07281716) — nadunolimab is anti-IL1RAP,
  not anti-PVRIG; my own alias table was wrong. Removed.

One regex miss found on manual review and corrected: `\bSIRP-?a(lpha)?\b` failed on the
Unicode `Sirpα` in NCT06487624, and `\bCD200\b` failed on `CD200AR-L` in NCT06305910.
Both are 2024 rows and neither affects 2025.

---

## 3. Per-target counts

Phase-1 oncology trials (`PHASE1` ∪ `PHASE1; PHASE2` ∪ `EARLY_PHASE1`, `onc_conditions=1`),
binned on `studyFirstPostDate`. **2026 is a partial year — through 2026-08 only.**

### Tier A — established

| target | 2024 | 2025 | 2026¹ | total | note |
|---|---:|---:|---:|---:|---|
| PD-1 | 188 | 175 | 115 | 478 | ~73% backbone-only |
| PD-L1 | 66 | 33 | 19 | 118 | ~79% backbone-only |
| CTLA-4 | 14 | 23 | 15 | 52 | ~73% backbone-only |
| LAG-3 | 5 | 2 | 3 | 10 | relatlimab / fianlimab / favezelimab |
| TIM-3 | 2 | 0 | 0 | 2 | cobolimab; INCAGN02390 |
| TIGIT | 2 | 4 | 0 | 6 | all rilvegostomig, tiragolumab, vibostolimab — no new agent |

### Tier B — prior-wave non-PD-1 checkpoints

| target | 2024 | 2025 | 2026¹ | what the rows actually are |
|---|---:|---:|---:|---|
| B7-H3 (CD276) | 13 | 18 | 13 | almost all CAR-T / ADC using B7-H3 as a surface antigen |
| CD73 | 2 | 3 | 2 | 2025: GI-108 bispecific, CD73/AXL CAR-T, a PET probe |
| CD47 / SIRPα | 1 | **0** | 1 | 2024 HCB301 fusion; 2026 CD47 siRNA |
| PVRIG | 0 | **1** | 0 | **NCT06888921, COM701, Compugen, posted 2025-03-21** |
| BTLA | 2 | 0 | 0 | tifcemalimab; JS004 |
| LILRB1/2/4 | 2 | 0 | 0 | SPX-303 (LILRB2×PD-L1); MK-4830 microdosing |
| IL-18BP axis | 1 | 1 | 0 | ST-067 / vevoctadekin — a decoy-resistant IL-18, arguably not a checkpoint |
| VISTA | 0 | **0** | 0 | zero rows in the entire 32-month window |
| NKG2A | 0 | **0** | 0 | zero — S095029's phase 1 predates the harvest window |
| IDO1, CD39, HPK1, Siglec-15, Siglec-10/CD24, TREM2, CD96, B7-H4, MERTK, CD155/PVR, CD200R | 0 | **0** | 0 | zero rows each |

### Tier C — newly nominated (the tier the claim is about)

| target | 2024 | 2025 | 2026¹ | what |
|---|---:|---:|---:|---|
| CLEVER-1 (STAB1) | 0 | **0** | 2 | bexmarilimab combos, posted 2026-03 and 2026-07 |
| GARP (LRRC32) | 0 | **1** | 0 | **NCT06964737, anti-GARP CAR-T, Ohio State, posted 2025-05-09** |
| LLT1 / CD161 | 1 | **0** | 0 | NCT06451497, ZM008 anti-LLT1, Zumutor, posted 2024-06-11 |
| CD200 axis | 1 | **0** | 0 | NCT06305910, CD200AR-L, OX2 Therapeutics, posted 2024-03-12 |
| IGSF8, ITPRIPL1, BTN1A1, SLC6A6, LRIG1, Siglec-10, PSGL-1, CISH, CD300e, TIPE2, NEAT1, VSIG4, TIM-4, SIGLEC11/Siglec-E | 0 | **0** | 0 | **zero rows each, all three years** |

### Tier D — co-stimulatory agonists (context only)

ICOS 0/1/0 · OX40 0/0/1 · 4-1BB 1/1/0 · CD40 1/0/1 · GITR 0/0/0 · CD27 0/0/0.
The 2025 ICOS row is a GSK sub-study of feladilimab with a 2019 start date, re-posted.

**Adjacent rows deliberately not counted as checkpoints**, though the regex found them:
LILRA6 CAR-T (NCT07263906, 2025-12), CD83 CAR-T (NCT06871410, 2025-03), CD94 CAR-T
(NCT07382817, 2026-02). All three use an immune-receptor gene as a *lineage antigen* for
a CAR against a haematological malignancy. None is checkpoint blockade. Counting them
would be the easiest available way to manufacture a refutation.

---

## 4. Verdict

**The claim holds, under the reading it was meant to have — and it is materially
overstated under the reading its words invite.**

**True as intended (Tier C).** Of the seventeen checkpoint targets this corpus itself
nominated between 2024-01 and 2026-08, **exactly zero entered a phase 1 anywhere in the
registry during 2025.** Not one. The tier produced four phase-1 registrations across the
whole 32-month window — LLT1 and CD200AR-L in 2024, GARP in 2025, bexmarilimab ×2 in
2026 — and the 2025 count under the strict definition of *checkpoint blockade* is zero.
The result is unchanged when binned on `start_date` instead of `studyFirstPostDate`.

**One trial sits on the line and should be named rather than buried.**
**NCT06964737** — *Anti-GARP Chimeric Antigen Receptor T Cell Therapy for Recurrent
Grade III or IV Gliomas*, Ohio State University Comprehensive Cancer Center, phase 1,
first posted **2025-05-09**, start 2025-05-21. GARP/TGFβ is described as a checkpoint
axis in this corpus's own journals (Cancer Discovery and JITC, both 2026-02) and appears
in six AACR/ASCO 2024 abstracts. If "newly nominated checkpoint entering a phase 1" is
read as *any agent directed at a newly nominated immunosuppression target*, this trial
refutes the claim on its own. It survives only because it is a CAR-T using GARP as a
surface antigen, not a blockade of the GARP–TGFβ interaction — a distinction that is
real but is a distinction the claim's wording does not make. **The wording has to be
tightened or this trial refutes it.**

**False under the looser reading (Tier B).** If "newly nominated" is read as "anything
other than the established six", 2025 is not empty:
**NCT06888921** (COM701, anti-PVRIG, Compugen, phase 1b/2, posted 2025-03-21),
**NCT07172802** (GI-108, anti-CD73×IL-2v, GI Innovation, posted 2025-09-15), and
**eighteen B7-H3 phase 1s**. But none of those targets is *newly* nominated — COM701's
first-in-human ran in 2018, CD73 and B7-H3 are older still — so this reading fails on
"newly", not on the trial data.

**The number the thread should be quoting instead of the binary.** Strip B7-H3 (an
ADC/CAR antigen, not a blockade target) and the phase-1 pipeline for *every* non-PD-1
co-inhibitory checkpoint, prior-wave and new together, is **6 trials in 2024, 6 in 2025,
4 in 2026-to-August** — against 175 PD-1 phase 1s in 2025 alone. That ratio, roughly
**1 in 30**, says what the thread is trying to say and survives the definitional
argument that the binary claim does not. VISTA, NKG2A, IDO1, CD39, HPK1, Siglec-15,
TREM2, CD96, B7-H4 and MERTK returned **zero phase-1 rows across all 32 months** —
that, not 2025 specifically, is the actual finding.

---

## 5. The biggest threat to this conclusion

**Code-named agents.** Of the 1,473 phase-1 oncology trials first posted in 2025,
**1,147 (78%) contain no recognisable target string anywhere in title or interventions,
and 614 (42%) name only a bare code.** Sixty-nine of those 614 are immune-therapeutic in
character and target-opaque: `IPN01203` and `IPN60300` (Ipsen), `DT-7012` (Domain),
`GB18`, `KK2845` (Kyowa Kirin), `BNT329` (BioNTech), `CER-1236` (CERo), `MOMA-341`,
`STAR0602`, `GB3226` and others. A first-in-human antibody against a 2025-nominated
checkpoint, registered as `XYZ-101` with no target named, is **invisible to every method
used here** — the exact failure mode the task's `MK-7684` warning describes.

This is not a hypothetical: the corpus's own `vibostolimab` example is only legible
because it later acquired an INN.

So the verdict is confirmed **up to a 42% target-opaque residue**. What would close it:
the ClinicalTrials.gov `armGroups`/`briefSummary`/`detailedDescription` fields, which
routinely spell out mechanism where `interventions` does not, and which the current
harvest does not store. That is a one-field change to the harvester, and it would make
this check decisive rather than merely strong.

Two smaller threats, both bounded:
- **Window.** The registry starts 2024-01 on `studyFirstPostDate`. Any programme whose
  phase 1 posted in 2023 or earlier is invisible — which is why NKG2A reads zero
  despite S095029 having a phase 1 that the corpus's own journals report in 2026-05.
  This *inflates* the appearance of emptiness in Tier B. It cannot affect Tier C, whose
  targets were not nominated until 2024 or later.
- **`onc_conditions=1`.** 1,994 rows are excluded by it. Spot-checking the excluded set
  for the Tier C target list returned nothing, but this was not exhaustive.

---

## 6. Proposed change to `data/threads.yml`

**Not applied.** Diff for review.

The core edit deletes the unqualified sentence and replaces it with a measured block
carrying its own rule, its own denominator, and its own stated blind spot — matching the
pattern `method-credibility` and `clinical-practice` already use, and the pattern the
file's own header demands ("a count is only comparable across months if the counting
rule was written down before the counting, and quoted with the number afterwards").

```diff
--- a/data/threads.yml
+++ b/data/threads.yml
@@ -157,15 +157,46 @@
   - id: next-gen-checkpoints
     claim: >-
       Targets beyond PD-1/CTLA-4 deliver a second generation of checkpoint blockade.
     opened: 2024-03
     note: >-
       The measured failure mode is not that individual targets fail — it is that the
       category is dissolving. A novel surface co-inhibitory receptor name has a
       half-life of two to four months in this corpus; ligand-side and intracellular
       nominations last longer. By 2025-12 the new nominations (CLEVER-1, CD300e,
       TIPE2, NEAT1) are macrophage and lncRNA targets rather than T-cell surface
       receptors, and the only clinical-stage non-PD-1 content is B7-H3 and an
       Fc-enhanced CTLA-4 — both from waves preceding the current preclinical set.
-      Across all of 2025 not one newly nominated checkpoint entered a phase 1.
-      2025-10 returned zero hits for the entire target list.
+      An earlier version of this note asserted that across all of 2025 not one
+      newly nominated checkpoint entered a phase 1, and followed it with
+      "2025-10 returned zero hits for the entire target list". The second
+      sentence is a fact about one month's reading and was never evidence for
+      the first. Both are superseded by `registry_check` below, which tested
+      the first sentence against the trial registry rather than the literature.
+    registry_check: >-
+      Checked 2026-08-27 against data/regulatory.sqlite (ct_trials, 16,145
+      oncology trials first posted 2024-01..2026-08), which did not exist when
+      the claim was written. Rule, fixed before counting: phases in PHASE1 /
+      PHASE1;PHASE2 / EARLY_PHASE1, onc_conditions=1, binned on
+      studyFirstPostDate; target implicated in `title` or `interventions` by
+      name or by agent INN; every non-PD-1 hit read individually and classified
+      as target-directed or backbone-only. Target list derived from the corpus,
+      not from recall: 398 checkpoint-context journal titles and 3,005
+      checkpoint-context sentences in the AACR/ASCO 2024 abstracts, plus a sweep
+      of every "anti-X / targeting X" string in the registry's own phase-1 rows.
+      THE CLAIM SURVIVES, NARROWLY AND ONLY AS STATED ABOUT NEW TARGETS. Of the
+      seventeen checkpoint targets this corpus first named in 2024-01..2026-08 —
+      IGSF8, ITPRIPL1, BTN1A1, SLC6A6, LRIG1, Siglec-10, PSGL-1, CISH, CLEVER-1,
+      CD300e, TIPE2, NEAT1, CD161/LLT1, GARP, VSIG4, TIM-4, Siglec-E — zero
+      entered a phase 1 in 2025. The tier produced four phase-1 registrations in
+      32 months: LLT1 (NCT06451497, Zumutor, 2024-06) and CD200AR-L
+      (NCT06305910, 2024-03); GARP (NCT06964737, Ohio State, 2025-05); and
+      bexmarilimab twice in 2026. Unchanged when binned on start_date.
+      ONE TRIAL SITS ON THE LINE. NCT06964737 is an anti-GARP CAR-T posted
+      2025-05-09, and GARP/TGFβ is called a checkpoint axis in this corpus's own
+      journals (2026-02, twice). It survives the claim only because a CAR using
+      GARP as a surface antigen is not checkpoint blockade — a distinction the
+      old wording did not make. Read loosely, 2025 also holds COM701 (anti-PVRIG,
+      NCT06888921) and GI-108 (anti-CD73, NCT07172802); both targets are older
+      than the window, so that reading fails on "newly", not on the data.
+    denominator: >-
+      Quote this instead of the binary, because it survives the definitional
+      argument the binary does not. Excluding B7-H3, which is an ADC/CAR antigen
+      rather than a blockade target, the phase-1 pipeline for EVERY non-PD-1
+      co-inhibitory checkpoint — prior wave and new together — is 6 trials in
+      2024, 6 in 2025 and 4 in 2026-to-August, against 175 PD-1 phase 1s in 2025
+      alone. VISTA, NKG2A, IDO1, CD39, HPK1, Siglec-15, TREM2, CD96, B7-H4 and
+      MERTK each returned zero phase-1 rows across all 32 months. The emptiness
+      is a property of the whole window, not of 2025.
+    blind_spot: >-
+      Confirmed only up to a 42% target-opaque residue. Of 1,473 phase-1
+      oncology trials first posted in 2025, 614 name only a bare code in title
+      and interventions, 69 of them immune-therapeutic (IPN01203, DT-7012,
+      BNT329, CER-1236, KK2845 and others). A first-in-human antibody against a
+      2025-nominated checkpoint registered as XYZ-101 is invisible to this
+      method — the same failure mode that hides MK-7684 behind a code name.
+      Storing armGroups and briefSummary in the harvest would close it.
```

And, so that sources.yml's open question is closed rather than left standing — a
separate one-line edit, also not applied:

```diff
--- a/data/sources.yml
+++ b/data/sources.yml
@@ -1692,7 +1692,10 @@
     notes: >-
-      Used to check whether a nominated target has any registered trial. The
-      finding that no newly nominated checkpoint entered a phase 1 anywhere in
-      2025 was read off the literature only and should be confirmed here.
+      Used to check whether a nominated target has any registered trial. The
+      finding that no newly nominated checkpoint entered a phase 1 anywhere in
+      2025 was read off the literature only; it was confirmed here on
+      2026-08-27 for the seventeen targets this corpus itself nominates, with
+      one borderline trial (NCT06964737, anti-GARP CAR-T, posted 2025-05) and a
+      42% target-opaque residue. See threads.yml next-gen-checkpoints.
       Dated on studyFirstPostDate. Trap: query.cond matches free text across a
       record's entire condition list, so a COPD rehabilitation study that
       lists "Lung Neoplasms" fourth comes back as oncology. Every row carries
       an onc_conditions flag instead; 16,145 of 18,139 clear it.
+      Second trap, unsolved: `interventions` names an INN or a bare code, never
+      a target. 42% of 2025 phase-1 rows are target-opaque. Harvesting
+      armGroups and briefSummary would fix it.
```

**A third change worth considering, outside the scope of this check.** The derived
status of `next-gen-checkpoints` is `contested` (13 supports / 19 refutes), while the
note's prose says the category "is dissolving". `contested` and "dissolving" are not the
same reading. The note should either be softened to match the cards, or — if the prose
is right — the gap is evidence that the card set under-samples the refuting side, and
that belongs in a `denominator` field rather than being asserted in prose.

---

## Appendix — reproduction

Working scripts (scratchpad, not committed):
`ct_check.py` (target table + per-target binning, writes `hits.json`) and the four
inline one-off queries quoted in §2.1 and §2.4. Every query is read-only via
`sqlite3.connect('file:...?mode=ro', uri=True)`. Core selector:

```sql
SELECT nct_id, date, start_date, phases, title, interventions, lead_sponsor
  FROM ct_trials
 WHERE onc_conditions = 1
   AND phases IN ('PHASE1', 'PHASE1; PHASE2', 'EARLY_PHASE1');
-- 4,214 rows; 1,473 of them first posted in 2025
```
