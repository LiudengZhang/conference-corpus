# 90-Minute Speed Read

A reader's path through the highest-value content in the corpus. Each item shows the time budget plus a one-line reason to read it. Stop markers at **10 / 35 / 60 / 75 / 90** minutes let you bail with what you've absorbed.

Read top-to-bottom. Each link opens the canonical page for that conference / trial / tool / talk.

---

## 0:00 — orient yourself (5 min)

| Item | Why read |
|---|---|
| [Home](index.md) | Quick skim of the 37-conference landscape — what's built vs scaffolded. |
| [2026 Timeline](timeline.md) | Year-at-a-glance Gantt + 4-criterion scoring rubric for all 36 scored conferences. |

## 0:05 — the cancer-research anchor (5 min)

| Item | Why read |
|---|---|
| [AACR 2026 — Overview](conferences/aacr-2026/) | The anchor. Five axes (agentic AI, single-cell/spatial, virtual cells, bioinfo/AI methods, clinical trials) organize the rest of the corpus. |

> 🟢 **Stop at 0:10** — you now know the corpus shape.

---

## 0:10 — what changed in cancer treatment this year (25 min)

**ASCO GI (Jan 8–10, San Francisco) — 9 min:**

| Trial | Why read |
|---|---|
| [HERIZON-GEA-01](conferences/asco-gi-2026/trials/herizon-gea-01.md) | Zani+chemo displaces 1L HER2+ G/GEJ; the PD-L1 CPS≥1 line is the IO-benefit threshold. |
| [BREAKWATER cohort 3](conferences/asco-gi-2026/trials/breakwater-cohort3.md) | Enco+cetux+FOLFIRI gives BRAF mCRC ~30 vs 15 mo OS — new 1L SOC. |
| [Daraxonrasib + zoldonrasib PDAC](conferences/asco-gi-2026/trials/daraxonrasib-zoldonrasib-pdac.md) | The RAS(ON) wave hits the clinic; ctDNA dynamics are the early-readout biomarker. |

**ASCO GU (Feb 26–28, San Francisco) — 9 min:**

| Trial | Why read |
|---|---|
| [KEYNOTE-B15 / EV-304](conferences/asco-gu-2026/trials/keynote-b15-ev304.md) | EV+pembro displaces cisplatin in MIBC — EFS HR 0.53. |
| [LITESPARK-022](conferences/asco-gu-2026/trials/litespark-022.md) | First adjuvant ccRCC trial to layer a mechanism on already-active pembro; raises the additive-benefit bar. |
| [PEACE-3](conferences/asco-gu-2026/trials/peace-3.md) | Ra-223 rehabilitated as combo with enza in mCRPC; mid-trial bone-protection amendment was the pivot. |

**SGO (Apr 10–13, San Juan) — 7 min:**

| Trial | Why read |
|---|---|
| [ROSELLA](conferences/sgo-2026/trials/rosella.md) | First GR-antagonist Phase 3 solid-tumor win; relacorilant+nab-pac for platinum-resistant ovarian. |
| [RUBY 4-yr OS](conferences/sgo-2026/trials/ruby-4yr-os.md) | Dostarlimab+chemo dMMR endometrial — 73% 4-yr OS plateau. |

> 🟢 **Stop at 0:35** — you have the 2026 cancer-clinical pulse.

---

## 0:35 — bioinformatics tools (25 min)

**EuroBioC 2025 (Sep, Barcelona) — 14 min:**

| Item | Why read |
|---|---|
| [Themes & takeaways](conferences/eurobioc-2025/themes.md) | Spatial-omics convergence + cross-language interop as the year's two big patterns. |
| [DESpace](conferences/eurobioc-2025/tools/despace.md) | Reframes SVG/DSP as a familiar NB-GLM problem on cluster covariates. |
| [SpatialData](conferences/eurobioc-2025/tools/spatialdata.md) | The Zarr/OME-NGFF cross-language framework that bridges Python scverse to R/Bioc. |
| [iSEE](conferences/eurobioc-2025/tools/isee.md) | The canonical interactive viz citizen — S4 panel graph + code-extraction. |

**GBCC 2025 (Jun, Cold Spring Harbor) — 11 min:**

| Item | Why read |
|---|---|
| [Themes & takeaways](conferences/gbcc-2025/themes.md) | The "joint" Galaxy+Bioc rationale and the agentic-AI-augmented-analysis inflection. |
| [plyxp](conferences/gbcc-2025/tools/plyxp.md) | dplyr for SummarizedExperiment — Mike Love's bridge from S4 to tidyverse. |
| [bioc-to-galaxy](conferences/gbcc-2025/tools/bioc-to-galaxy.md) | LLM-assisted DESCRIPTION → Galaxy-XML translator; the load-bearing meta-story of GBCC. |

> 🟢 **Stop at 1:00** — you know the 2025 bioinformatics-tools landscape.

---

## 1:00 — AI/ML inflections in biology (15 min)

**ICLR 2026 (Apr 23–27, Rio) — 9 min:**

| Tool | Why read |
|---|---|
| [MedAgentGym](conferences/iclr-2026/tools/medagentgym.md) | 72k-task sandboxed code-exec gym + Med-Copilot-7B; primary AACR agentic-AI anchor. |
| [Proteina Complexa](conferences/iclr-2026/tools/proteina-complexa.md) | Atomistic protein binder design; 63.5% PDGFR hit rate, first de novo carbohydrate binders. |
| [sc-Arena](conferences/iclr-2026/tools/sc-arena.md) | Knowledge-augmented virtual-cell benchmark — answers "how do you actually score a virtual cell?". |

**ISBI 2026 (Apr 8–11, London) — 6 min:**

| Item | Why read |
|---|---|
| [Mahmood pathology FM keynote](conferences/isbi-2026/tools/mahmood-pathology-fm-keynote.md) | Three-tier FM stack (DINOv2 encoder + attention-MIL + task heads) scaling to >100M H&E tiles. |
| [Segmentation FMs synthesis](conferences/isbi-2026/tools/segmentation-foundation-models-isbi.md) | The SAM-3 / MedSAM / SegVol line — promptable medical FMs with native-3D extensions. |

> 🟢 **Stop at 1:15** — you have the 2026 AI/ML-in-biology map.

---

## 1:15 — brain cancer deep cut (10 min)

**AACR Brain Tumors 2026 (Mar 23–25, Philadelphia):**

| Talk | Why read |
|---|---|
| [Monje GD2 CAR-T DIPG](conferences/aacr-brain-tumors-2026/talks/monje-gd2-cart-dipg.md) | Strongest pediatric CNS CAR-T signal to date — H3K27M-locked OPC-like DMG. |
| [Suva glioma cell states](conferences/aacr-brain-tumors-2026/talks/suva-glioma-cell-states.md) | The AC/MES/OPC/NPC four-state framework that dictates CAR-T antigen-escape geography. |
| [Neuroscience of gliomas + TAM (synthesis)](conferences/aacr-brain-tumors-2026/talks/neuroscience-of-gliomas-tam.md) | Neuron-glioma AMPAR synapses + TREM2/SPP1 TAM convergence — the year's most coherent CNS story. |

> 🟢 **Stop at 1:25** — you've gone deep on one disease.

---

## 1:25 — sequencing platforms (5 min)

**AGBT 2026 (Feb 22–25, Marco Island):**

| Launch | Why read |
|---|---|
| [Roche Axelios 1](conferences/agbt-2026/launches/roche-axelios-1.md) | $150 / 30× duplex genome anchor; Roche's nanopore SBX comeback resets the cost-per-genome conversation. |

> 🟢 **Stop at 1:30** — full speed-read complete.

---

## If you have more time

Stretch picks for a 2-hour follow-on:

- [JPM 2026 themes](conferences/jpm-2026/themes.md) — the year's financial/strategic frame
- [Element VITARI](conferences/agbt-2026/launches/element-vitari.md) + [Ultima UG200](conferences/agbt-2026/launches/ultima-ug200.md) — the $100 genome floor
- [ACMG Presidential Plenary — NBS expansion](conferences/acmg-2026/talks/presidential-plenary-nbs-expansion.md) — newborn genomic screening at population scale
- [PSMAaddition](conferences/asco-gu-2026/trials/psmaaddition.md) — Lu-PSMA-617 moves three lines earlier into 1L mHSPC
- [sc-FM Perturbation Adapter](conferences/iclr-2026/tools/sc-fm-perturbation-adapter.md) — <1% drug-conditional adapter for zero-shot perturbation prediction
- [DeeDeeExperiment](conferences/eurobioc-2025/tools/deedeeexperiment.md) + [Tidyomics](conferences/gbcc-2025/tools/tidyomics.md) — the data-class evolution for Bioconductor

Or pivot to a scaffolded vault to track an upcoming meeting:

- **May 26–29**: [RECOMB 2026](conferences/recomb-2026/) — methods/algorithms
- **May 29–Jun 2**: [ASCO 2026](conferences/asco-2026/) — biggest oncology readout of the year
- **Jun 11–14**: [EHA 2026](conferences/eha-2026/) — European hematology
- **Jun 13–16**: [ESHG 2026](conferences/eshg-2026/) — European human genetics (same week as EHA)

---

## How this was curated

The speed-read picks favor (1) practice-changing or class-defining results, (2) tools likely to recur across multiple 2026 vaults, and (3) the cross-vault stories (cancer-clinical pulse, bioinformatics-tools evolution, AI/ML-in-biology inflection). Each section is sized to land at a natural stopping point so you can quit early without losing the through-line.

Comprehensive coverage lives in the conference vaults themselves — this page is the optimized path for someone who has 90 minutes and wants the highest-value cross-section.
