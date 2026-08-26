# First prompt to the server-side agent

Paste this verbatim. Do **not** start downloading until Step 0 is complete — I want to know we agree on what we're doing before you spend a week pulling EGA.

---

## the project — what we're building

We are building a **pan-cancer HRD × TME stratifier** intended to support a future PARPi + anti-CCR8 combination trial. The biological seed is Luo 2024 (Cell, the anchor cohort in the manifest): HRD tumors enrich for CCR8+ effector Tregs, and a PARPi + anti-CCR8 antibody combination is a testable stratified intervention. To run that trial well we want a model that takes a tumor's multi-modal profile and predicts:

- **HRD signal** — from WGS / WES / panel; four-scorer concordance vector (SigProfiler SBS3, HRDetect, CHORD, scarHRD)
- **TME archetype** — from sc / sn / spatial; CCR8-eTreg-high vs IE / IE-F / F / D vs cold
- **PARPi response (CATE)** — observational treatment-effect from same-patient pre/on data (DragonNet-style head)

The model is multi-modal (genomic + TME + clinical encoders), uses HRD as a feature not a label, and has a MoE routing layer over archetypes. The architecture is sketched in the project blogs (`hrd-is-computable`, `outcome-first`, `one-model-many-archetypes`). **You are not building that in this phase.** You are making sure the data it would consume actually exists, is reachable, and passes QC.

## the data landscape

74 public cohorts meet the strict entry condition (tumor genomics + ≥1 high-resolution TME modality on the **same patient**). Indexed by TME modality into four buckets in `cohort_manifest.tsv`:

- **A** — sc/snRNA + genomics: 33 cohorts, ~1,300 pts
- **B** — spatial transcriptomics + genomics: 7 cohorts, ~100 pts
- **C** — spatial proteomics + genomics: 9 cohorts, ~1,400 pts
- **D** — multi-spatial / full-tuple (HTAN + MOSAIC + SPECTRUM + standalones): 25 cohorts, ~3,400 pts

This is roughly the full global supply of paired data of this shape. The HRD-relevant subset is smaller — ~10 cohorts and 200–400 HRD-confirmed patients. That ceiling is real. It's why the model has to bridge between tiers (Tier 1 high-N bulk for power, Tier 4 full-tuple for grounding, Tier 5 treatment-exposed for causality — see the `paired-data-pan-cancer` blog if you need it).

## step 0 — prove you understood (before you touch the data)

Write back to me, **in your own words** (do not quote this prompt):

1. **What this project is about** — the trial it sets up, what HRD means, why CCR8 / eTregs are the second axis, what the model exists to predict. 2–3 short paragraphs.
2. **What data preparation means in this project** — why same-patient genomics + TME pairing is the hard requirement; why bulk-only cohorts (TCGA, HMF, POG570, etc.) are excluded as primary rows; why the four-bucket TME-modality split matters for what the model can learn; how a failed QC on a priority-1 cohort changes the project (not just delays it).
3. **What you understand the Phase-1 deliverable to be** — per cohort, usability on three axes (HRD signal / TME / treatment-response), not any modeling.

If anything in your paraphrase is wrong, I will correct it. Iterate until we're aligned, then begin Step 1. This is not busywork — I need the shared mental model before the parallel subagent fan-out, because once 30+ subagents are running you will have no time to renegotiate scope.

## step 1 — dispatch parallel subagents

You have subagents. Use them. Do not download cohorts serially.

**Pattern: one subagent per cohort.** Each subagent's job is end-to-end for its one cohort:

1. Read its row from `cohort_manifest.tsv`.
2. Create `<DATA_ROOT>/<bucket>/<cohort_id>/` tree per `folder_layout.md`.
3. Download into `raw/` using the right client (see `tools_manifest.md`).
4. Verify checksums.
5. Process to standard form per modality (Step 2 below).
6. Run QC per `qc_rubric.md`.
7. Write `MANIFEST.yaml` + `qc/qc_card.md`.
8. Update `_index/status.tsv` atomically with final state.
9. Return a 5-line summary to the orchestrator: `cohort_id`, state, post-QC patient count, blocker (if any), one-line verdict.

**Concurrency caps — be polite, repos throttle:**
- GEO / SRA: ≤ 6 concurrent (NCBI rate limit)
- EGA: ≤ 3 concurrent (throttles aggressively)
- Synapse / HTAN: ≤ 4 concurrent (fileview is big; API throttles)
- dbGaP / gdc-client: serial (parallel auth sessions break it)
- Zenodo / ArrayExpress / PRIDE / Broad SCP: ≤ 6 concurrent

**Dispatch order:**

1. **First, run `luo-2024-nant-ovarian` alone.** Validate the full pipeline end-to-end on the anchor cohort before fanning out. If this one fails QC, **stop and surface** — it's the cohort the project is built around.
2. **Wave A — open + HRD-direct:** `pal-2021-brca1-breast`, `karaayvaz-2018-tnbc`, `kim-2018-tnbc-chemoresist`, `stur-2022-hgsoc-visium`.
3. **Wave B — Synapse HRD-direct:** `launonen-2022-farkkila-mif-hgsoc`, `farkkila-2020-topacio`, `hms-sorger-ovarian-renamed`.
4. **Wave C — Zenodo / PRIDE breast + STIC:** `ali-danenberg-2020-metabric-imc`, `makhmut-coscia-2025-stic-dvp`.
5. **Then fan out** to everything else marked `priority` 1 and 2 in `cohort_manifest.tsv`. Priority 3 / 4 only on explicit re-tasking.

**In parallel with downloads — submit DAC / DAR applications today** so the paperwork clock starts now:
- `phs002371` — HTAN-HTAPP umbrella; one DAR unlocks Mitri AMTEC + Hwang-Lin PDAC + Klughammer mBC + Chan SCLC
- `phs002857` — MSK SPECTRUM cfDNA / PARPi maintenance (direct project relevance)
- EGA studies listed under "tier-2 EGA" in `access_tier_split.md` — batch submit
- HTAN raw L1/L2 DUAs per sub-atlas — start with HTA1, HTA6, HTA9, HTA12

## step 2 — what each subagent processes to

Run only what's present in the cohort.

- **genomic** → SigProfiler SBS3 + HRDetect (WGS only) + CHORD + scarHRD; BRCA1/2 + HR-pathway-gene status table; tumor purity (PURPLE / Sequenza / ASCAT); verifyBamID2 contamination
- **bulk RNA** → Salmon or STAR counts; ESTIMATE purity / immune / stromal; RSeQC
- **scRNA / snRNA** → cellranger out; scrublet doublet flag; broad-lineage CellTypist label transfer; cell-yield-per-sample table
- **spatial transcriptomic** → SpaceRanger / Xenium Ranger / Stereopy out; tissue mask; H&E registration check; squidpy spatial QC
- **spatial proteomic (CODEX / MIBI / IMC / mIF / t-CyCIF)** → MCMICRO or steinbock or ark-analysis cell tables; marker positivity sanity; segmentation success rate
- **clinical** → tidy long tables: `patient.tsv`, `sample.tsv`, `treatment.tsv`, `outcome.tsv`; `clinical_completeness.tsv` per `qc_rubric.md`

## step 3 — QC verdict per cohort

Each subagent writes `qc/qc_card.md` using the template in `qc_rubric.md`. Per cohort, three booleans (don't be conservative — quote fractions):

- **usable for HRD axis** — yes / partial / no
- **usable for TME axis** — yes / partial / no
- **usable for treatment-response axis** — yes / partial / no

"partial" = some patients pass; quote the fraction. "no" = the data does not support the axis at all (e.g., panel-only genomics → no SBS3 → no HRD axis from this cohort).

## exit condition — what you return at the end of phase 1

When priority-1 + priority-2 cohorts are processed, return three artifacts:

1. `_index/status.tsv` — per-cohort final state
2. `qc/_rollup.md` — pan-cohort summary (template in `qc_rubric.md`): per-bucket pass/warn/fail tally, post-QC patient count by bucket, per-HRD-signal stratum, which cohorts cleared the treatment-causal bar, which are TME-only
3. **One actionable paragraph per warn/fail** — blocker, what would unblock, whether worth chasing

Then **stop**. Do not start Phase 2 (modeling) without my decision.

## constraints — read these once

- **Do not model.** No CATE, integration, MoE, or inference. Phase 1 is download + organize + QC + EDA only.
- **Do not delete `raw/`.** Re-download cost is high for EGA / dbGaP. Reprocess from raw if needed.
- **Do not commit credentials** (tokens, DUA paperwork, eRA-Commons logins) anywhere inside the data tree. Use `_secrets/` outside `<DATA_ROOT>`.
- **Do not chase items in `do_not_attempt.md`.** If you find yourself reading a Tempus white-paper or a sponsor-controlled trial registry, stop.
- **Do not re-bucket cohorts.** Bucket A/B/C/D is locked by the manifest. If you think a cohort is mis-bucketed, write it to `qc_card.md` notes and surface in the rollup — don't move directories.
- **Synapse fileview `syn20446927`** is the HTAN gateway. Filter by `Atlas` column; do **not** download the whole fileview.
- **Owkin MOSAIC-Window `EGAD50000001251`** is **15 patients of MIBC bladder**, not 60 pan-cancer. Older press releases are wrong.
- **HTAN HTA13** is TNP SARDANA (an imaging benchmark), not an ovarian cohort. Our `hms-sorger-ovarian-renamed` is Ludwig-affiliated, outside the HTAN HTA atlas-ID system. The manifest reflects this.

## escalate when

- A cohort needs > 2 DAC contacts or > 4 weeks paperwork — surface, don't burn the clock.
- A cohort's actual modality differs materially from the manifest (paper says Visium HD, deposit is Visium v2).
- A 2025 cohort marked `accession unverified` resolves to a real ID — confirm with me before downloading.
- A priority-1 cohort fails QC — that's a project-level decision.
- A subagent stalls > 24h with no progress — kill it and dispatch a fresh one.

Otherwise — work the queue.

---

end of first prompt.
