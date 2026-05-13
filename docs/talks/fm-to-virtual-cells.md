# From Foundation Models to Virtual Cells

> Talk-prep page for a 30-minute presentation: *"What can we do as computational biologists?"*

## TL;DR — what this talk argues

Foundation models have arrived in biology but they are **not yet virtual cells**. In 2025, three independent papers (Ahlmann-Eltze & Huber, Kedzierska, Wenkel) showed that scGPT / Geneformer / UCE / scFoundation **cannot beat linear baselines** on perturbation prediction. That reckoning is the talk's pivot — it tells computational biologists *what to work on*.

The talk maps **5 FM families** (single-cell, pathology, genomic, protein, multimodal), then **5 field-wide gaps** (donor diversity, cross-species, causal vs correlational, compute asymmetry, evaluation honesty). It then offers two parallel menus: **7 lanes** for *applying* existing FMs (Lane 1 embeddings-as-features through Lane 7 FM-aided clinical applications) and **6 tracks** for *innovating on* FMs (Track 1 mechanistic interpretability through Track 6 causal evaluation). It maps each gap to a lane and a track. It names the **3 commercial-buyer archetypes** (pharma, AI-native biotech, clinical-AI vendors) funding the field and what each buys from academia. It ends with **3 concrete project pitches** the group could take on at <$25k each, and closes by using **AACR 2026** as the live case study for which lane survives clinical contact.

The honest one-liner: **the gap between FMs and virtual cells is the most concrete research agenda single-cell biology has had in a decade — and the answer is in your data, not your GPU budget.**

---

## How to use this page

This page is a reference, not a slide deck. **Venue: group meeting (60–75 min with discussion throughout)**, not a conference plenary — so technical depth and methods detail are appropriate. The audience is comp-bio peers who can follow methods notation; assume they want the *interesting bits*, not the executive summary.

Structure: a long-form script you can lift onto your own slides, **plus** the deeper background that makes Q&A productive in a peer setting. Discussion prompts are bundled at §8 to give the group concrete decision points at the end. Numbers marked **[DISCLOSED]** come from the original paper, technical report, or vendor disclosure. Numbers marked **[ESTIMATED]** are derived (arithmetic shown). Numbers marked **[UNKNOWN]** were not disclosed and could not be estimated reliably.

Cross-links jump to the per-tool dossiers in the [Foundation Models](../foundation-models.md) corpus, where every claim has an inline citation.

**Reading time**: ~30 min cold for the full page; ~12 min if you skim the §3 deep dives.

---

## §1. Opening (3 min)

### 1.1 What is a virtual cell?

A **virtual cell** is a learned model that can predict a single cell's transcriptional (or proteomic, or chromatin) state under any perturbation — drug, gene knockout, cytokine, microenvironment shift — for any cell type from any donor. It is the cell-biology equivalent of what AlphaFold did for static protein structure: a *generalizable simulator* rather than a one-off measurement.

The phrase has three working definitions, depending on whom you ask:

1. **Narrow definition** *(Arc Institute / Vevo)* — a generative model trained on perturbation data (e.g. Tahoe-100M) that samples plausible cell states under unseen perturbations.
2. **Broad definition** *(CZ Biohub / Bunne et al. 2024 Cell perspective)* — any FM that learns a representation of cells useful for downstream prediction, including non-generative encoders like scGPT or UCE.
3. **Strict definition** *(field-corrective, post-2025)* — a model whose predictions cannot be matched by a linear regression on `mean-of-training-perturbations` features. *Most current "virtual cell" models fail this bar.*

For the talk, use the **broad** definition to set up the landscape, then introduce the **strict** definition in §4 as the discipline correction.

### 1.2 Why now? The 2024–2025 inflection

Three things converged:

1. **Dec 2024** — Chan Zuckerberg Initiative announces a multi-year, multi-billion-dollar virtual-cell program with CZ Biohub. Stated goal: "predict the behavior of every human cell under any perturbation." This is the largest single funder commitment in single-cell ML history.
2. **Feb 25, 2025** — Arc Institute + Vevo Therapeutics open-source **Tahoe-100M**, the largest perturbation atlas at 100M cells × 1,100 drugs × 50 cell lines. Frames itself as the inaugural contribution to the "Virtual Cell Atlas."
3. **2024–2025** — pathology FMs (UNI, Virchow, CHIEF, Prov-GigaPath) cross the threshold from research-grade to clinical-grade. PathChat DX receives the first FDA Breakthrough Device Designation for a generative-AI pathology tool in Jan 2025.

Simultaneously, **2025 was the year the single-cell FM field was forced to confront its evaluation problem**: three independent papers (Ahlmann-Eltze & Huber, Kedzierska et al., Wenkel et al.) showed that scGPT, Geneformer, UCE, and scFoundation fail to beat trivial linear baselines on perturbation prediction. The narrative shifted from *"FMs are eating single-cell ML"* to *"FMs have not yet earned that claim — and the linear baseline is the new SOTA floor."*

The talk frames this as the **trough between hype and clinical-grade utility**: a productive trough, because it tells computational biologists *what to work on*.

### 1.3 The thesis

In one sentence: **foundation models in biology are not yet virtual cells — but the gap between them is the most concrete research agenda single-cell biology has had in a decade.**

The talk's structure follows that gap. §2–3 map what exists. §4 explains the 2025 correction. §5 names the five field-wide gaps. §6 is the **small-lab playbook for applying FMs** — 7 lanes with real exemplars and budget tiers for groups that cannot afford to train their own FM. §7 is the **innovation tracks for FMs themselves** — 6 frontier methods-research lanes where small labs can publish original work at <$10k compute. §8 is the **commercial landscape** — three buyer archetypes, the 2024–2026 signals timeline (Lilly+NVIDIA $1B, AstraZeneca→Modella AI, Paige FDA), and the per-pitch buyer map. §9 is the **group-meeting discussion** — three concrete project pitches and the decision questions to pick one. §10 closes by using AACR 2026 as a live case study: what happens when these models meet a clinical audience that doesn't grade on novelty.

### 1.4 Glossary — the eight terms this talk leans on

If any of the following are fuzzy in the room, ground them before §2:

| Term | What it means in this talk |
|---|---|
| **Foundation model (FM)** | A neural network pretrained self-supervised on a *broad* corpus (text, images, cells, genomes), then *adapted* to many downstream tasks without per-task pretraining. Same weights → many uses. "Foundation" = the pretrained body; "downstream" = the head you train. |
| **Virtual cell** | A predictive/generative computational model that takes a cell's state + a perturbation (drug, knockout, signal) and predicts the resulting state. Aspiration (CZ Biohub): predict *any* cell × *any* perturbation. Reality: no model does this end-to-end yet — the term is currently a research program, not a deployed artifact. |
| **Embedding** | A learned vector representation of an input (cell, tile, sequence). The FM compresses the raw data into a few hundred to a few thousand numbers that downstream models read. "Use the FM as a feature extractor" = train a classifier on top of frozen embeddings. |
| **Pretraining vs fine-tuning** | Pretraining = the expensive self-supervised first stage (10⁴–10⁶ GPU-hours, $10k–$5M). Fine-tuning = the cheap labeled-task second stage (hours to days, often <$500). |
| **Zero-shot / few-shot** | Zero-shot = run the pretrained model on a new task with no labeled examples or fine-tuning. Few-shot = a handful of labeled examples (in-context or in a small head). The benchmark that exposed the 2025 crisis was zero-shot perturbation prediction. |
| **In-silico perturbation** | Predicting a cell's response to a virtual knockout/drug/signal without doing the wet-lab experiment. The headline virtual-cell capability claim. |
| **Linear baseline** | The simplest possible predictor (linear regression / ridge / `latent-additive`) used as a sanity floor. Ahlmann-Eltze & Huber 2025 showed every published single-cell FM fails to beat this floor on perturbation prediction. |
| **PEFT / LoRA / adapter** | Parameter-efficient fine-tuning. Train a tiny (<1% of params) module on top of frozen FM weights; inherits the FM's pretraining without paying for it. Lane 2 in the small-lab playbook. |

---

## §2. The five FM families (5 min)

One slide per family. For each: anchor model, current 2026 SOTA, the load-bearing benchmark, and the disclosed 2026 status.

### 2.1 Single-cell FMs

| Field | Detail |
|---|---|
| Anchor models | scGPT (Cui et al. 2024), Geneformer (Theodoris et al. 2023), UCE (Rosen et al. 2024), scFoundation (Hao et al. 2024) |
| 2026 SOTA | Geneformer-V2-104M_CLcancer ties scGPT and beats scFoundation on cell-type classification at 1/3 the params; **no model has a robust perturbation-prediction win over `latent-additive + scGPT-embeddings` baseline** |
| Load-bearing benchmark | PerturBench, Open Problems v2, scPerturBench |
| Public weights | scGPT, Geneformer, UCE, scFoundation, CellPLM, GET — all permissive (MIT / Apache-2.0) |
| 2026 status | **In crisis.** Field actively re-evaluating what perturbation prediction means after 2025 critique trio. |

Cross-link: [Foundation Models §Single-cell](../foundation-models.md#single-cell-fms) · [scGPT dossier](../conferences/aacr-2026/topics/bioinfo-tools/tools/scgpt.md) · [Geneformer dossier](../conferences/aacr-2026/topics/bioinfo-tools/tools/geneformer.md)

**Per-task winners — what each cell FM actually wins on (and where they all still lose).** The "SOTA" row above flattens a more interesting picture:

| Task | Best 2026 model | Margin over scVI / linear baseline | Source |
|---|---|---|---|
| Cell-type classification (Tabula Sapiens, scTab) | **Geneformer V2-104M_CLcancer** | +2–4 pts macro-F1 over scGPT; ties 316M at ⅓ compute | Theodoris-lab benchmarks; Tang 2024 *Nat Biotechnol* (scTab) |
| Batch integration / atlas alignment | scVI **still competitive**; scGPT zero-shot ≈ scVI | small (≤1 pt) FM lift; depends on the metric | Open Problems v2 |
| Cross-species cell-state alignment | **UCE** (the only sc-FM that handles 8 species) | positive but small in magnitude; not benchmarked against scVI cross-species | Rosen et al. 2024 |
| Zero-shot perturbation prediction | **`latent-additive + scGPT-embeddings`** linear baseline — **no FM beats it consistently** | 0; the floor is the ceiling | Ahlmann-Eltze & Huber 2025 *Nat Methods*; Wenkel et al. 2025 |
| Gene-network / perturb-net inference | **Geneformer** (designed for this) | matches GENIE3/PIDC on most benchmarks; better on rare TFs | Theodoris et al. 2023 *Nature* |
| Cell-state retrieval / nearest-neighbour | **SCimilarity** (not strictly an FM) | strong; 23M-cell index, ms-scale lookups | Chen et al. 2024 *Nat Biotechnol* |
| Spatial-transcriptomics integration | **scGPT-spatial** + Visiumformer-class models | very early; no settled benchmark | scGPT-spatial 2024; HEST-1k |

The picture this collapses to: **on classification + integration the FMs are roughly tied with classical baselines; on perturbation prediction they collectively lose to a linear regression; on cross-species and spatial they have unique capability but no convincing margin**. This is what "in crisis" means in the SOTA row.

### 2.2 Pathology FMs

| Field | Detail |
|---|---|
| Anchor models | UNI (Chen et al. 2024), Prov-GigaPath (Xu et al. 2024), CHIEF (Wang et al. 2024), Virchow / Virchow2 (Vorontsov 2024 / Zimmermann 2024) |
| 2026 SOTA | **Virchow2 / UNI2-h** — Campanella et al. 2025 *Nature Communications* clinical benchmark put Virchow2 first, with Prov-GigaPath and UNI tied for second |
| Load-bearing benchmark | Campanella 2025 multi-task panel, HEST-1k, BACH, CRC polyp |
| Public weights | UNI / UNI2-h (gated CC-BY-NC), Virchow (CC-BY-NC), Hibou (Apache-2.0, the only top-tier permissively-licensed pathology FM), CHIEF (AGPL-3.0 + gated), Prov-GigaPath (CC-BY-NC) |
| 2026 status | **Healthiest family.** First FDA Breakthrough Device Designation (PathChat DX, Jan 2025). Visible plateau emerging around ViT-H/14 + 200M-tile training. |

Cross-link: [Foundation Models §Pathology](../foundation-models.md#pathology-fms) · [Virchow dossier](../conferences/aacr-2026/topics/bioinfo-tools/tools/virchow.md) · [UNI dossier](../conferences/aacr-2026/topics/bioinfo-tools/tools/uni.md)

### 2.3 Genomic / DNA FMs

| Field | Detail |
|---|---|
| Anchor models | Nucleotide Transformer (Dalla-Torre et al. 2025), DNABERT-2 (Zhou et al. 2024), HyenaDNA (Nguyen et al. 2023), Evo2 (Brixi et al. 2026), AlphaGenome (Avsec et al. 2025) |
| 2026 SOTA | **AlphaGenome** wins 25/26 regulatory variant-effect benchmarks (DeepMind 2025 *Nature*). **Evo2** retains generative + in-context-learning territory that AlphaGenome cannot match. |
| Load-bearing benchmark | gnomAD-pathogenic, ENCODE/GTEx tracks, GUE/GUE+, NT 18-task |
| Public weights | All open-source except AlphaGenome (non-commercial license; source code only released Jan 2026, post-Nature) |
| 2026 status | **Split.** Track-prediction (AlphaGenome) and generative (Evo2) are now distinct sub-families that don't compete head-to-head. |

Cross-link: [Foundation Models §Genomic](../foundation-models.md#genomic-dna-fms) · [AlphaGenome dossier](../conferences/iclr-2026/tools/alphagenome.md) · [Evo2 ICL dossier](../conferences/iclr-2026/tools/genomic-icl-evo2.md)

### 2.4 Protein FMs

| Field | Detail |
|---|---|
| Anchor models | ESM-2 / ESM-3 (Hayes et al. 2025), AlphaFold3 (Abramson et al. 2024), Proteina Complexa, TEA (de novo design ICLR 2026), RFdiffusion (Watson et al. 2023) |
| 2026 SOTA | **ESM-3** for generative (98B params, generated esmGFP at 36% identity to avGFP — equivalent to 500M years of evolution). **AlphaFold3** for structure prediction (multi-modal: proteins + DNA + RNA + ligands). |
| Load-bearing benchmark | CASP15/16 GDT-TS, novel-binder hit rates, scaffold-recovery RMSD |
| Public weights | ESM-2 open; ESM-3 1.4B variant open (Cambrian Non-Commercial), 7B/98B Forge-API-gated. AlphaFold3 inference code open, weights gated to non-commercial use. |
| 2026 status | **Maturing fast.** Now routinely yields wet-lab hits at >50% rate for some binder design tasks (Proteina Complexa: 63.5% PDGFR hit rate). |

Cross-link: [Foundation Models §Protein](../foundation-models.md#protein--multimodal-fms) · [ESM-3 dossier](../conferences/iclr-2026/tools/esm-3.md) · [Proteina Complexa](../conferences/iclr-2026/tools/proteina-complexa.md)

### 2.5 Multimodal / vision-language FMs

| Field | Detail |
|---|---|
| Anchor models | BioMedCLIP (Microsoft Research, Zhang et al. 2024), PathChat / PathChat-2 (Mahmood lab, Lu et al. 2024), LLaVA-Med, MedAgentGym (ICLR 2026), MMedAgent-RL (ICLR 2026) |
| 2026 SOTA | **PathChat-2** (>1M instruction pairs, ~5.5M Q-A turns). **PathChat DX** is the first generative-AI pathology tool with FDA Breakthrough Designation (Jan 2025). |
| Load-bearing benchmark | PMC-VQA, SLAKE, VQA-RAD, PathQABench |
| Public weights | BioMedCLIP MIT-licensed; PathChat proprietary |
| 2026 status | **Closest to clinical deployment** of any FM family. Regulatory science actively engaging. |

Cross-link: [Foundation Models §Multimodal](../foundation-models.md#protein--multimodal-fms) · [BioMedCLIP dossier](../conferences/iclr-2026/tools/biomedclip.md) · [PathChat dossier](../conferences/aacr-2026/topics/bioinfo-tools/tools/pathchat.md) · [MedAgentGym dossier](../conferences/iclr-2026/tools/medagentgym.md)

---

## §3. Deep dives — 10 anchor models × 4-question matrix (10 min)

For each model, four questions:

1. **Resources used** — compute (GPU type, GPU-hours), data, team, $ cost estimate (or marked UNKNOWN)
2. **Framework / algorithm** — architecture, tokenization, pretraining objective
3. **What's unique** — the one differentiator vs prior art
4. **Field gap exposed** — what this model's existence reveals about what's still missing

Detailed resource numbers with arithmetic and citation tags live in the companion file [`_resources-matrix.md`](_resources-matrix.md) (loaded as appendix).

**At-a-glance — the 10 anchor models in one table.** Read this first; the deep dives below expand each row.

| # | Model | Family | Params | Compute disclosed? | Public weights | The one thing it's the best at | Where it breaks |
|---|---|---|---|---|---|---|---|
| 3.1 | **scGPT** | single-cell | 51M | ❌ UNKNOWN (50× uncertainty band) | ✅ MIT | First sc-FM with gene + cell as tokens; defined the category | Zero-shot perturbation prediction fails vs linear baseline |
| 3.2 | **Geneformer V2** | single-cell | 104M / 316M | ✅ DISCLOSED ($17k V2-104M) | ✅ Apache-2.0 (HF) | Domain-curated 104M beats general 316M at ⅓ compute — kills "scale wins" | Same perturbation-prediction gap as scGPT |
| 3.3 | **UCE** | single-cell | 650M | ❌ UNKNOWN | ✅ MIT | Cross-species (8 species via ESM2 protein-embedding bridge) | Cross-species gain is positive but small; least transparent on cost |
| 3.4 | **STATE** | single-cell (virtual cell) | 600M SE + ST | ❌ UNKNOWN (~$125k est.) | ✅ open weights | First production virtual cell at Tahoe-100M scale | No online-update loop; you re-train to add perturbations |
| 3.5 | **Generative Virtual Cells** | single-cell (POC) | tiny | ✅ <$250 | ✅ MIT | The *design pattern*: joint planner + world model with validation gating | A workshop POC, not a deployed model; scaling unproven |
| 3.6 | **Virchow2** | pathology | 632M / 1.85B | ✅ DISCLOSED (512× V100, ~$170k) | ⚠️ CC-BY-NC | Most transparent pathology FM; current SOTA on Campanella 2025 panel | Lead over UNI2-h is ≤2 pts; ViT-H/14 + 200M tiles plateauing |
| 3.7 | **UNI2-h** | pathology | 681M | ❌ UNKNOWN (~$75k est.) | ⚠️ CC-BY-NC + HF-gated since Jan 2025 | Full vertical stack: tile encoder → slide → vision-language → retrieval | License-shift risk realized; opaque training cost |
| 3.8 | **AlphaGenome** | genomic | ~450M | ⚠️ partial (TPU only) | ⚠️ non-commercial (source Jan 2026) | Single model wins 25/26 regulatory variant-effect benchmarks at 1-Mb context | Can't do in-context learning; non-commercial license blocks industry |
| 3.9 | **Evo2** | genomic | 7B / 40B | ✅ DISCLOSED (2,048× H100, ~$5M) | ✅ Apache-2.0 | Only genomic FM with demonstrated ICL; 1M-token context | $5M training cost concentrates capability at ~5 institutions |
| 3.10 | **ESM-3** | protein (multimodal) | 1.4B / 7B / 98B | ✅ DISCLOSED (1.07 × 10²⁴ FLOPs) | ⚠️ 1.4B open, 7B/98B gated | Cleanest compute disclosure in biology FMs; generated esmGFP de novo | esmGFP is one anecdote; wet-lab validation at scale is rare |

**The two patterns this table makes visible**: (1) **disclosure correlates with hardware sponsorship** — every model with ✅ DISCLOSED has an NVIDIA / DGX-Cloud / TPU partnership (Geneformer V2/BioNeMo, Virchow2, Evo2/NVIDIA, AlphaGenome/TPU). The opaque models are academic labs without a hardware co-marketer. (2) **license posture is bifurcating** — sc-FMs are uniformly permissive (MIT/Apache); pathology FMs are uniformly restrictive (CC-BY-NC, often + HF gating); genomic FMs split (Evo2 open, AlphaGenome closed). Choose the family that matches your commercial constraints, not just your data type.

### 3.1 scGPT (Cui et al. *Nature Methods* 2024)

The single-cell FM that defined the category.

- **Resources** — ~51M params; 33M cells from CellxGene Census; **GPU compute: UNKNOWN — Cui 2024 does not disclose**; **ESTIMATED ~10³–10⁵ A100-hours** (a 50× uncertainty band, depending on whether the published checkpoint is the result of a single run or many re-runs); **cost $2.6k–$250k [ESTIMATED]**. Team: Bo Wang lab, U. Toronto + Vector Institute / Haotian Cui.
- **Framework** — encoder-decoder transformer. Gene tokens + cell-state tokens. Masked-value-prediction pretraining objective (predict masked expression values).
- **Unique** — first single-cell FM with both **gene** and **cell** as tokens, enabling cross-cell and cross-gene attention. The "GPT for cells" pitch landed because the architectural mapping was clean.
- **Gap exposed** — scGPT's zero-shot perturbation predictions don't beat `mean-of-training-perturbations` baselines (Ahlmann-Eltze & Huber 2025). The architectural achievement did *not* translate to perturbation generalization. *Also exposed*: the 50× uncertainty band on training cost makes it impossible to argue "scGPT is too expensive to reproduce" or "scGPT is cheap to retrain on your data" with any confidence. **Question for the field**: is the tokenization wrong, the objective wrong, or the eval wrong? Plausibly all three.

### 3.2 Geneformer V2 (HuggingFace, Dec 2024 update of Theodoris et al. *Nature* 2023)

The model that inverted the scale-wins narrative — and the cleanest compute disclosure in single-cell FM space.

- **Resources** — V2-104M: 104M params, 104M-cell base + 14M cancer cells continual (CLcancer). **DISCLOSED via NVIDIA BioNeMo: 64× A100 80GB × 4d 8h = 6,656 A100-hours = ~$17k on-demand.** V2-316M for comparison: 128× A100 × 3d 19h = 11,576 A100-hours. Team: Theodoris lab, Gladstone Institutes / UCSF.
- **Framework** — encoder-only BERT. Rank-based tokenization (cells become ordered gene lists, ranked by relative expression). Masked-language-model objective.
- **Unique** — **rank-based tokenization** sidesteps the normalization problem entirely. Cells with different sequencing depth are comparable because rank is depth-invariant.
- **Gap exposed** — The cancer-domain V2-104M_CLcancer checkpoint *matches or beats* the 316M general-domain model **at one-third the compute cost** ($17k vs ~$30k). **Scale does not win; domain-curated pretraining does.** This inverts the GPT-3 → GPT-4 narrative that the field imported from NLP. Also notable: V2-104M is the **only single-cell FM in this matrix where the full training cost is publicly costable** — making it the natural baseline for "what does it take to retrain a single-cell FM on my disease."

### 3.3 UCE — Universal Cell Embedding (Rosen et al. bioRxiv 2023 → *Nature Methods* 2024)

The cross-species single-cell FM.

- **Resources** — 650M params; 33 transformer layers; ~36M cells across 8 species (Integrated Mega-scale Atlas; ESM2-tokenized via protein-sequence embeddings); **GPU compute: UNKNOWN — preprint does not disclose**; **ESTIMATED ~7 × 10⁴ A100-hours upper, ~1,275 A100-hours floor**; **cost $3k–$175k [ESTIMATED]**. Team: Leskovec + Quake labs, Stanford / Yanay Rosen.
- **Framework** — encoder-only ViT-style transformer. Gene-set tokenization mapped across species via orthology (ESM2 protein embeddings serve as the cross-species bridge). Self-supervised contrastive objective on cell-state representations.
- **Unique** — **species-agnostic via protein-language embeddings**. First single-cell FM that handles mouse + human + zebrafish + fly cells in one embedding space, with the cross-species mapping grounded in protein sequence rather than gene-symbol orthology.
- **Gap exposed** — UCE's cross-species transfer is positive but small in magnitude. Single-cell FMs trained on more species do not yet outperform single-species FMs on within-species tasks. **And**: UCE is the largest published single-cell FM at 650M params but also the *least* transparent on training cost — the 50× uncertainty band makes "frontier-scale" claims for it unverifiable. **Question**: is cross-species pretraining a net positive for downstream prediction, or a regularizer at best?

### 3.4 STATE (Arc Institute, 2025)

The Tahoe-100M-native virtual cell.

- **Resources** — Two interlocking modules: **State Embedding (SE-600M)** at 600M params trained on 167M observational human cells; **State Transition (ST)** at undisclosed params trained on 100M+ perturbed cells (Tahoe-100M + Parse + Replogle); **GPU compute: UNKNOWN — preprint and Arc press do not disclose**; **cost UNKNOWN** (order-of-magnitude estimate ~$125k if similar Arc infrastructure to Evo2). Team: Arc Institute (Patrick Hsu + Hani Goodarzi labs). Preprint: [Adduri et al. bioRxiv 2025.06.26.661135](https://www.biorxiv.org/content/10.1101/2025.06.26.661135v1).
- **Framework** — bidirectional transformer with self-attention over **sets of cells** (not single cells). SE module learns observational embedding; ST module predicts perturbation transitions. Trained offline on frozen snapshots.
- **Unique** — **first production-grade virtual-cell model at Tahoe-100M scale**. The 167M-cell observational corpus + 100M-cell perturbation corpus is the data moat.
- **Gap exposed** — STATE is *trained on the snapshot*; if you want to extend the atlas with new perturbations, you re-train. **No online-update or active-learning loop** in the published version. Also: STATE's disclosure pattern (data scale foregrounded, compute buried) mirrors Evo2's — **Arc Institute treats "what we trained on" as the publishable contribution, not "what it cost to train."** The Lewis & Zueco *Generative Virtual Cells* (§3.5) paper proposes the missing online-update.

### 3.5 Generative Virtual Cells (Lewis & Zueco, ICLR 2026 Gen² Workshop)

The methods paper proposing closed-loop virtual cells. **A position/proof-of-concept paper, not a frontier training run.**

- **Resources** — small MLP/transformer trained on a toy Perturb-seq simulator (proof-of-concept). **<$250 in compute. <100 GPU-hours total.** Team: AIXC Research / David Scott Lewis & Enrique Zueco.
- **Framework** — joint planner + world model trained with validation gating. The planner proposes perturbations; the world model predicts outcomes; experimental validation feedback updates both modules.
- **Unique** — **jointly updated** under validation feedback, not offline-trained on a frozen snapshot. Closer to active learning than to pretraining. The contribution is the **design pattern**, not the model weights.
- **Gap exposed** — Two layers of gap. **First**: the validation feedback loop assumes you can run experiments cheaply at high throughput. Most labs cannot, so the practical question becomes: how few wet-lab validations does the loop need to converge? **Second**: the gap between a $250 workshop POC and a $5M Evo2 / STATE-scale model is enormous, and Lewis & Zueco does not yet demonstrate that the joint-update pattern scales. The talk's honest framing: this is a **promising research direction**, not a deployed virtual cell.

### 3.6 Virchow2 (Paige + MSK, Zimmermann et al. arXiv 2408.00738)

The current pathology FM SOTA — and **the most transparent pathology FM on hardware**.

- **Resources** — 632M-param ViT-H/14; 3.1M WSIs / ~225,000 patients / ~2B tiles / ~200 tissue types. **DISCLOSED: 512× NVIDIA V100 32GB GPUs, batch 4,096, AdamW.** **ESTIMATED ~1.4 × 10⁵ V100-hours wall-clock = ~$170k** (V100 ~$1.20/hr in 2026). Virchow2G (1.85B) trained on the same fleet. Team: Paige + Memorial Sloan Kettering / Eric Zimmermann (V2), Eugene Vorontsov (V1).
- **Framework** — DINOv2 self-supervised pretraining on mixed-magnification 224×224 H&E (V2 adds IHC) tiles; attention-pooling for slide-level aggregation.
- **Unique** — **dual transparency: hardware count + patient-level provenance**. Virchow2's training corpus has known patient counts, MSK-consult source distribution (~57% of patients), and the training fleet (512 V100s) is publishable. This makes Virchow2 the natural benchmark when a pathology lab asks "what does it cost to train a frontier pathology FM?"
- **Gap exposed** — Virchow2 leads the Campanella 2025 clinical benchmark, but the lead over UNI2-h is small (~1–2 points absolute on most tasks). **The pathology FM curve appears to be plateauing around ViT-H/14 + 200M tiles.** Adding more tiles or scaling to Virchow2G (1.85B) yields diminishing returns. What replaces "more tiles" as the scaling axis — multi-modal (IHC, IF, spatial transcriptomics), longer-range slide context, or new pretraining objectives?

### 3.7 UNI2-h (Mahmood lab, Jan 14 2025 update of Chen et al. *Nature Medicine* 2024)

The Mahmood-stack flagship — and the **opaque counterpoint to Virchow2**.

- **Resources** — 681M-param ViT-H/14 with SwiGLU + 8 register tokens; 200M+ tiles across 350K+ WSIs (added IHC alongside H&E). **GPU compute: UNKNOWN — Nature Medicine 2024 and HF card describe "extensive GPU hours on A100 80GB" without count.** **ESTIMATED ~3 × 10⁴ A100-hours = ~$75k** based on DINOv2 architectural constants. HF access gated since Jan 2025 (institutional-email verification). Team: Mahmood Lab, Harvard / Mass General Brigham / Richard J. Chen.
- **Framework** — DINOv2 on histology tiles. Companion models in the Mahmood stack: TITAN (slide-level), PathChat / PathChat-2 (vision-language), SlideSeek (retrieval).
- **Unique** — **full vertical stack**: tile encoder → slide aggregator → vision-language → retrieval. The Mahmood lab ships a fleet of compatible models rather than one giant one. PathChat DX, the clinical front-end of this stack, has FDA Breakthrough Designation (Jan 2025) — the first generative-AI pathology tool to receive it.
- **Gap exposed** — **Two compounding gaps. First**: opaque training cost means a clinical pathology group cannot argue UNI2-h's success is a function of compute rather than data curation, making "would scaling fix our task" unverifiable. **Second: license-shift risk.** The HF gating in Jan 2025 — moving from open download to institutional-email verification — signals that the path from research-open to commercial-closed is short. Open licenses for pathology FMs are not yet a settled norm. Compare to Virchow2's full hardware disclosure: same backbone class, same DINOv2 family, opposite transparency posture.

### 3.8 AlphaGenome (DeepMind, Avsec et al. *Nature* 2025)

The current genomic FM SOTA on variant effects.

- **Resources** — ~450M params [VENDOR-ASSERTED, not in Nature abstract]; ENCODE + GTEx + FANTOM5 + 4DN across 5,930 human + 1,128 mouse tracks; 1-Mb input windows. **DISCLOSED hardware: 8× TPU v3 per replica with sequence parallelism.** **Total TPU-hours UNKNOWN — Nature does not state.** **ESTIMATED ~$200k order-of-magnitude** ($46k/fold × 4-fold teacher ensemble + distillation). The released "all-folds" checkpoint is a **distilled student from a 4-fold teacher ensemble** — total training compute is ≥4× the single-model cost. Source code released Jan 2026 (post-Nature); non-commercial license. Team: Google DeepMind / Žiga Avsec.
- **Framework** — U-Net + transformer bottleneck. 1-Mb input window. Multi-track output prediction (gene expression, chromatin accessibility, splicing, etc. simultaneously).
- **Unique** — **single-model multi-track prediction at 1-Mb context**. Replaces a half-dozen task-specific models (Enformer, Borzoi, Splam, ChromBPNet variants) with one unified model. Hardware footprint is modest by frontier-FM standards: DeepMind can offer a free hosted API for non-commercial use because inference is cheap.
- **Gap exposed** — AlphaGenome cannot do in-context learning. You cannot prompt it with "predict expression like this example sequence does." For ICL on DNA you still need Evo2. **The track-prediction vs generative split appears to be permanent**: different architectures suit different downstream tasks. **Also**: the **non-commercial license** is the binding constraint for industry users, not compute.

### 3.9 Evo2 (Arc Institute + NVIDIA + Stanford + UC Berkeley + UCSF, Brixi et al. *Nature* 2026)

The generative + in-context-learning genomic FM. **The second-most-expensive biology FM publicly trained.**

- **Resources** — 7B and 40B params; **OpenGenome2: 8.8T tokens (~9.3B bp) from 100,000 species** across all domains of life. **DISCLOSED: 2,048× NVIDIA H100 GPUs on NVIDIA DGX Cloud (AWS), trained for "several months".** **ESTIMATED ~2 × 10⁶ H100-hours = ~$5M.** Disclosed FLOPs ratio: **"~150× more compute than AlphaFold, ~2× the FLOPs of ESM-3"** — the cleanest cross-model compute comparison published in 2025-2026 biology. Open weights (Apache-2.0). Team: Arc Institute (Patrick Hsu lab + Hani Goodarzi) + NVIDIA + Stanford + Berkeley + UCSF / Garyk Brixi.
- **Framework** — StripedHyena 2 (hybrid state-space + attention). Byte-level (single-nucleotide) tokenization. Causal language modeling objective. 1M-token context.
- **Unique** — **only genomic FM with demonstrated in-context learning**. Breslow et al.'s ICL probe (the ICLR 2026 paper in this corpus) shows Evo2 can do few-shot variant-effect prediction from prompted examples. Also notable: the 2,048-H100 fleet is **only available to ~5 institutions worldwide via DGX Cloud** — Evo2 is what *NVIDIA-as-co-author* enables.
- **Gap exposed** — Evo2's ICL works for some tasks but the prompt-engineering is mostly ad-hoc. **No systematic prompt-template benchmark for biological FMs**, unlike NLP where every model gets an HELM-style ICL evaluation. The field has no equivalent. **And**: at $5M and a 2,048-H100 footprint, Evo2 is the model that defines the **compute concentration problem** for genomic FMs — academic labs cannot directly compete on training scale.

### 3.10 ESM-3 (EvolutionaryScale, Hayes et al. *Science* 2025)

The 98B-param multimodal protein FM. **Sets the floor for "frontier biology FM compute" at 10²⁴ FLOPs.**

- **Resources** — 98B params largest variant (also 1.4B / 7B sizes); **2.78B proteins, 771B unique tokens; 1.07 × 10²⁴ FLOPs DISCLOSED in Science**. **ESTIMATED ~9.9 × 10⁵ H100-hours or ~3.2 × 10⁶ A100-hours; cost ~$2.5M–$8M** depending on hardware. Described in the EvolutionaryScale release blog as "the most compute applied to any biological model at time of release." Team: EvolutionaryScale (ex-Meta FAIR protein team) / Thomas Hayes. 1.4B variant open under Cambrian Non-Commercial; 7B/98B Forge-API-gated.
- **Framework** — multimodal generative transformer with **7 token tracks**: sequence + 3D coordinates + structure tokens (4,096-codebook VQ-VAE) + SS8 secondary structure + SASA + function keywords + InterPro residue annotations.
- **Unique** — **multimodal generation + cleanest compute disclosure**. ESM-3 is the only frontier biology FM that publishes its training FLOPs as a single number. Practitioners can cost-compare any equivalent FLOPs budget on their preferred hardware. The 98B variant generated **esmGFP** *de novo* — a fluorescent protein 36% identical to avGFP / 58% to tagRFP, equivalent to ~500M years of natural evolution.
- **Gap exposed** — esmGFP is one anecdote. Wet-lab validation at scale (10⁴+ designed proteins tested) is rare because it's expensive. **The field's confidence in generative protein design rests on a small number of celebrated wins.** Robust hit-rate distributions across many design tasks are still missing. Also: the 1.4B open variant is what most academic reproductions actually use — the 98B weights are gated, so claims about "ESM-3 generation" in academic papers are usually about the 1.4B model.

### 3.11 The institutional landscape — who builds these models (90 sec, 1 slide)

The 10 models above were built by ~10 labs and ~5 commercial groups, and the same names recur across §5 (gaps), §6 (playbook exemplars), and §8 (commercial map). Use this table as the institutional cheat-sheet for the rest of the talk — speak in terms of *"the Mahmood stack"* or *"the Arc fleet"* rather than enumerating models each time.

| Tier | Institute / Lab | PI(s) | Ships | Why they matter |
|---|---|---|---|---|
| **Academic FM builders** | **Arc Institute** (Palo Alto, non-profit, founded 2021) | Patrick Hsu + Hani Goodarzi | Evo2, STATE, Tahoe-100M (with Vevo) | Largest non-DeepMind compute (2,048× H100 via NVIDIA DGX Cloud); sets the perturbation-atlas substrate the rest of the field uses |
| | **Mahmood Lab** (Harvard / BWH / MGB) | Faisal Mahmood | UNI, UNI2-h, CONCH, PathChat, PathChat-DX, TITAN, CHIEF, HEST-1k | Full pathology vertical stack (tile → slide → VL → retrieval); PathChat-DX = first generative-AI pathology tool with FDA Breakthrough Designation (Jan 2025) |
| | **Theodoris Lab** (Gladstone / UCSF) | Christina Theodoris | Geneformer V1, V2-104M / V2-316M / `_CLcancer` (Dec 2024) | The only academic sc-FM lab with full NVIDIA BioNeMo compute disclosure — the only published academic training-cost recipe in the field |
| | **Bo Wang Lab** (U. Toronto / Vector / UHN) | Bo Wang | scGPT, scGPT-spatial, MedSAM | Defined the sc-FM category; AACR 2026 plenary; Canada CIFAR AI Chair |
| | **Leskovec + Quake** (Stanford / SNAP) | Jure Leskovec + Steve Quake | UCE (Universal Cell Embedding) | Cross-species (8 species via ESM2-bridged tokenization); Stanford CRFM-affiliated |
| **Industrial FM builders** | **Google DeepMind** | Žiga Avsec et al. | AlphaGenome, AlphaFold 2 / 3, Med-Gemini | Closed-weights + hosted-API model; TPU-scale; the prestige bar for "frontier biology FM"; Isomorphic Labs is the commercial arm |
| | **EvolutionaryScale** (ex-Meta FAIR protein, 2024) | Alex Rives, Tom Sercu, Thomas Hayes | ESM-3 (1.4B / 7B / 98B) | Cleanest published FLOPs disclosure in biology FM (10²⁴); partial-gating license precedent (1.4B open, 98B Forge-gated) |
| | **Paige + MSK** | Thomas Fuchs (Paige) + Eric Zimmermann / Eugene Vorontsov | Virchow, Virchow2, Virchow2G, FullFocus | First FDA 510(k)-cleared general-purpose pathology AI (Jan 2025); cleanest compute disclosure among pathology FMs (512× V100) |
| | **Owkin** (Paris / NYC, founded 2016) | Industry consortium + academic partners | Phikon, Phikon-v2, H-optimus-0, MOSAIC | The open-weights pathology alternative to UNI / Virchow (Apache-2.0); federated-learning-first |
| | **NVIDIA BioNeMo** (infrastructure layer) | (framework team) | BioNeMo framework; Geneformer V2 reproduction recipe; Evo2 co-author | Sets the compute-disclosure norm by making it a co-marketing artifact; the only model-agnostic public training-cost recipe |
| **Funders & substrates** | **CZ Biohub + CZI** (SF / Chicago / NY) | Theofanis Karaletsos (AI for Science), Steve Quake (ex-head), Angela Pisco | Virtual Cell Program, CELLxGENE Census, Tabula Sapiens, rBio | The single biggest funder commitment in single-cell ML history (Dec 2024); supplies the data substrate every sc-FM trains on |
| **Critique anchors** | **Ahlmann-Eltze / Huber** (EMBL); **Kedzierska / Lu** (Oxford / MSR); **Theis Lab** (Helmholtz Munich) | (multiple) | The 2025 reckoning trio + Lotfollahi causal / compositional work | Without these, §4 doesn't exist; the discipline's epistemic immune system |

**Two structural observations the table makes visible:**

1. **Disclosure correlates with hardware sponsorship.** Every institute with a transparent compute disclosure has an NVIDIA / DGX-Cloud / TPU partnership (Theodoris + BioNeMo, Paige's V100 fleet, DeepMind on TPU, Arc + NVIDIA on Evo2). Academic labs without a hardware co-marketer (Mahmood on UNI, Leskovec/Quake on UCE, Bo Wang on scGPT) disclose much less. The pattern is structural, not random — disclosure is a co-marketing artifact.

2. **The "virtual cell" name lives in two non-overlapping places.** *Substrate side*: CZ Biohub provides the data + community benchmark; Arc Institute provides the perturbation atlas. *Model side*: the academic sc-FM labs (Theodoris, Bo Wang, Leskovec/Quake) ship the encoders that everyone fine-tunes. **No single institute ships both** — which is exactly why the 2025 reckoning landed (substrate ≠ working model, and no one institute is on the hook for closing the gap).

---

## §4. The 2025 discipline crisis (4 min)

### 4.1 The linear-baseline reckoning

Three independent papers in 2025 retired the single-cell FM perturbation-prediction leaderboard, and a 2026 benchmark confirmed the verdict at scale:

1. **Ahlmann-Eltze & Huber 2025** *Nature Methods* — "[Deep-learning–based perturbation modeling does not yet outperform simple baselines.](https://www.nature.com/articles/s41592-025-02772-6)" Showed scGPT, Geneformer, scFoundation, GEARS, CPA fail to beat `mean-of-training-perturbations` on held-out perturbations.
2. **Kedzierska et al. 2025** *Genome Biology* — extended the result to UCE and the zero-shot setting.
3. **Wenkel et al. 2025** *Nature Methods* — proposed `latent-additive + scGPT-embeddings` as the strongest single-cell baseline; current FMs still don't beat it consistently.
4. **Wu et al. 2025 *Nature Methods*** — "[Benchmarking algorithms for generalizable single-cell perturbation response prediction](https://www.nature.com/articles/s41592-025-02980-0)" — 27 methods × 29 datasets × 6 metrics; confirms the headline at much larger scale, and provides the first multi-axis breakdown of where each FM fails (some are stronger on combinatorial perturbations, none on out-of-distribution cell types).

The headline result is simple: a linear regression on average post-perturbation expression — *with no training, no fine-tuning, no FM* — is competitive or better than every published single-cell FM on the perturbation-prediction task as it was originally defined.

### 4.2 Why it was missed

Three mechanisms:

1. **Splitting on cells, not on perturbations.** Many published evaluations split train/test on cells but kept perturbations shared. The FM only had to interpolate within a perturbation, not extrapolate to a new one. Linear baselines trivially do this.
2. **Reporting averaged metrics over many perturbations.** Mean R² masks the fact that most perturbations have small effects, so a "predict the mean" baseline is hard to beat in aggregate even when it has zero signal on the big-effect perturbations the field cares about.
3. **Selective benchmark curation.** Papers chose perturbation datasets where their model did well; a linear baseline was sometimes computed but reported as an afterthought.

This wasn't fraud. It was the slow accretion of methodological choices that all individually seemed reasonable but collectively created a false leaderboard.

### 4.3 What it means going forward

Three concrete consequences:

1. **Every post-2025 sc-FM perturbation claim must clear the linear floor first.** Reviewers know to ask. Authors who don't include the linear baseline pre-emptively get rejected.
2. **The "what scale wins" question is open again.** With the leaderboard reset, we don't actually know whether 100M-param models are better than 10M-param ones for sc-FM downstream tasks.
3. **"Virtual cell" claims are now louder than the underlying evidence.** Public-facing comms (CZ Biohub, Arc Institute, multiple biotech announcements) describe capabilities that the field's strongest models cannot yet demonstrate against honest baselines. Computational biologists are well-placed to be the honest brokers here.

---

## §5. What's still missing — the 5-gap framework (4 min)

These are the gaps that, if closed, would let "foundation model" and "virtual cell" reasonably coexist. Each is a research agenda you can frame talks, grants, or papers around.

### 5.1 Donor diversity in pretraining corpora

Tahoe-100M is the largest perturbation atlas but is heavily weighted toward immortalized cell lines (~50 cell lines, none patient-derived). CellxGene Census v1.0 (the corpus most sc-FMs train on) is ~70% Anglophone-country sequencing centers. **Cross-donor generalization** — the ability to predict a perturbation response in a cell from a donor outside the training distribution — has not been systematically benchmarked because the data to do so doesn't exist at scale.

**Research question**: what fraction of a donor's perturbation response is predictable from population-level FM training, and what fraction requires donor-specific fine-tuning? Nobody knows the answer.

**Where to publish**: Open Problems v2 needs a donor-split benchmark. The Human Cell Atlas governance committee is the natural venue for a community standard.

### 5.2 Cross-species generalization

UCE pretrains across 8 species but most sc-FMs are human-only. Cross-species transfer has not been systematically benchmarked beyond UCE's own ablations. **Open question**: does pretraining on multiple species hurt within-species performance (the "negative transfer" hypothesis), or help via shared regulatory grammar?

This matters for translational labs because most disease models are mouse. If sc-FMs can transfer from human to mouse at low fine-tuning cost, that changes what experiments are worth running in mice.

### 5.3 Causal vs correlational perturbation prediction

Every current single-cell FM is fundamentally a *correlational* model: it learns associations between perturbation tokens and cell-state outputs from observational data. None of them distinguish *causation* — the actual mechanism by which a perturbation propagates through a regulatory network — from *correlation*.

This is the most fundamental gap. A virtual cell that predicts cell state under genetic knockout but not under combinatorial knockouts (because combinations are not in the training distribution) is not yet a *causal* virtual cell. **Replogle-scale Perturb-seq atlases** are necessary but not sufficient; causal validation requires interventional + counterfactual reasoning that current FMs do not implement.

Active research direction: integration with mechanistic models (Lotfollahi et al. SCRIB, Bunne et al. CellOT), or counterfactual graph neural networks. None have produced a clear win at scale yet.

### 5.4 Compute access asymmetry

Of the 14 frontier biology FMs in our [resources matrix](_resources-matrix.md), **only 5 disclose training compute cleanly** (Geneformer V2, Virchow2, Evo2, AlphaGenome hardware-only, PathChat). Seven require estimation. Two — STATE and AlphaFold 3 — are UNKNOWN even with FLOPs-anchored arithmetic.

The cost concentration is even sharper. **Evo2 (~$5M) + ESM-3 (~$2.5–$8M) alone account for >$7M of the ~$15M in total identified training spend across all 14 models.** Two industry labs (Arc Institute + EvolutionaryScale) spent more on training than the other twelve models combined.

The disclosure pattern is structural, not random: **labs with NVIDIA / DGX-Cloud partnerships disclose hardware aggressively** (Arc+NVIDIA on Evo2, Paige on Virchow2, NVIDIA on Geneformer V2) because the disclosure is a co-marketing artifact. **Academic labs without a hardware sponsor disclose much less** (Mahmood on UNI, Leskovec/Quake on UCE, Theodoris on V1, Bo Wang on scGPT, DeepMind on AlphaFold 3 / AlphaGenome).

The result: **the people who can build these models and the people who can audit them are two different small populations.** And the absence of an authoritative compute number means "we couldn't reproduce X" is not a falsifiable claim — the reader cannot tell whether the failed reproduction is methodologically off or simply under-trained.

**Question**: should the field require compute disclosure as a publication standard, the way it now requires data availability? NeurIPS / ICLR already require it. Biology venues do not yet.

### 5.5 Evaluation honesty

The linear-baseline reckoning (§4) was a wake-up call but not a solution. The field still lacks:

- A standardized **baseline floor** that every paper must clear (PerturBench is the closest, but adoption is uneven).
- A **negative-results venue** — papers showing "FM X does *not* outperform baseline Y on task Z" have no natural publication home. *Nature Methods* publishes a few; most go to bioRxiv and stop there.
- A **community-curated leaderboard** with cross-validation across splits, donors, perturbations, and species.

Open Problems for Single Cell (https://openproblems.bio) is the most active community effort. It needs methodological and political support, not just funding.

### 5.6 The five gaps mapped to lanes and tracks (1 min, 1 slide)

The §5 gaps are not abstract — each maps directly to a concrete lane (§6 *apply*) and track (§7 *innovate*). This matrix is the connective tissue between "what's broken" and "what we'd work on."

| Gap (§5) | Apply via §6 lane | Innovate via §7 track |
|---|---|---|
| 5.1 Donor diversity | Lane 7 — FM-aided application on under-represented cohort | Track 4 — architecture with donor-conditioning priors |
| 5.2 Cross-species | Lane 3 — domain FM on non-human-cell corpus | Track 4 — cross-species equivariance priors |
| 5.3 Causal vs correlational | Lane 4 — linear-baseline audit | Track 2 — causality-targeting pretraining; Track 6 — causal benchmarks |
| 5.4 Compute asymmetry | Lane 6 — wrapper tool that democratizes access | Track 1 — interpretability tells us what the compute bought |
| 5.5 Evaluation honesty | Lane 5 — benchmark curation | Track 3 — compositional benchmarks; Track 6 — causal benchmarks |

**Vertical reading**: pick a gap → see which way to contribute. **Horizontal reading**: pick a project → see which gap it closes. The §9 group-meeting pitches all use this mapping — each pitch is one row of this matrix made concrete.

---

## §6. The small-lab playbook — 7 lanes that work without a $5M GPU budget (4 min)

> **Framing.** §3 priced the frontier: $20k (Geneformer V2-104M_CLcancer, the cheapest fully-disclosed model in our matrix) to $5M+ (Evo2, ESM-3). The middle does not exist as a *training* tier — you are either a few wall-clock days on 8 A100s, or you are spending Arc-Institute money. So if your lab cannot pretrain, the right question is: **what kind of FM-area contribution is publishable at <$5k?** Seven lanes; each has real 2023–2026 exemplars from academic or small-industry labs.

### 6.1 Budget tier overview (30 sec, 1 slide)

| Lane | Typical $ | Compute | Time | Risk |
|---|---|---|---|---|
| 1. FM embeddings as features | $0–$500 | inference-only, 1× consumer GPU | weeks | low — worst case, you publish a null lift |
| 2. PEFT / LoRA / adapters | $500–$5k | 1–8× A100 for days | 2–4 months | medium — must beat frozen-embedding baseline |
| 3. Domain-specific small FM | $10k–$50k | 8–64× A100 for ~1 week | 6–12 months | medium-high — depends on domain corpus quality |
| 4. Negative results / replication | $0–$2k | inference + linear regression | 3–6 months | low scientifically, medium reputationally |
| 5. Benchmark / dataset curation | $0–$5k + curator time | de minimis compute | 6–18 months | low — community credit is durable |
| 6. FM-wrapper tools / pipelines | $0–$5k | dev box, inference for tests | 6–12 months | low — adoption is the risk, not training |
| 7. FM-aided wet-lab / clinical study | $5k–$50k FM-side | mostly inference | 12–24 months | low for FM side; standard biology risk for the rest |

Lanes 1–6 are pure dry-lab; Lane 7 is the dry-lab portion of a hybrid project where the FM is *instrumentation*, not the deliverable.

### 6.2 Lane 1 — FM embeddings as features ($0–$500)

A 1B-param model trained on someone else's $200k cluster, used as a frozen encoder, is the cheapest 2026 way to publish a clinically-meaningful classifier — and the field has stopped pretending the wrapper architecture is the contribution.

**Anchor exemplar — AACR 2026 poster #5470** (academic, not Mahmood/Paige): UNI2-h tile embeddings → attention-MIL → HER2 prediction in breast cancer. **AUC 0.715, tied with full UNI2-h**, but with lower runtime and lower scanner cost — the publishable finding is *parity at a fraction of deployment cost*. Compute: <$500, inference-only.

Other AACR 2026 examples: **#1441** (UNI2-h + CLAM for prostate-cancer risk stratification, <$500) · **#2758** (UNI2-h + ABMIL for PAX3/7::FOXO1 fusion detection in rhabdomyosarcoma, <$1k — first published H&E predictor of a pathognomonic fusion in this rare paediatric disease).

**Venue picks**: *Cancer Discovery*, *JCO CCI*, *npj Precision Oncology* for clinical wrap. **CSHL BDS 2026** (Nov 4–7) for methods-light. **MICCAI 2026** (Sep 27–Oct 1) if the contribution is the MIL head.

### 6.3 Lane 2 — PEFT / LoRA / adapters ($500–$5k)

A <1% parameter adapter is the highest-leverage technical contribution a small lab can make — it inherits the base model's $250k of pretraining and slots into a public benchmark.

**Exemplar A — sc-FM Perturbation Adapter** (Maleki et al., ICLR 2026 LMRL): drug-conditional adapter, <1% trainable params, frozen scGPT/Geneformer/scFoundation backbone. *Caveat: Genentech lead authors* — but the recipe is the contribution. Budget ~$2k inferred. **Win**: zero-shot generalisation to unseen drugs and cell lines where CPA / GEARS / scGen cannot extrapolate.

**Exemplar B — scGPT-spatial / LoRA-fine-tuned scGPT** (Wang lab, U Toronto, bioRxiv 2024): LoRA rank-8 adapters on scGPT's attention layers for Visium decomposition. ~$1.5k on a single 8× A100 node over 24–48h. **Win**: clean transfer to spatial tasks without retraining scGPT.

**Exemplar C — GenePT / scELMo** (Liu et al. 2023 Yale; Chen & Zou 2024 Stanford): frozen LLM (GPT-3.5/4) embeddings of gene names + a logistic-regression head. ~$200 compute + API calls. **Win**: matches or beats scGPT zero-shot on cell-type annotation. Pure small-lab result.

**Venue picks**: **ICLR / NeurIPS LMRL workshops**; *Genome Biology*, *Bioinformatics*; **ISMB 2026** (Jul 12–16).

### 6.4 Lane 3 — Domain-specific small FM ($10k–$50k)

Continual-pretrain a *smaller* general model on *your* domain corpus. 2025 evidence shows this consistently matches the 3× larger general model on in-domain tasks.

**Exemplar A — Geneformer V2-104M_CLcancer** (Theodoris lab, Gladstone/UCSF, Dec 2024): **$16,640 disclosed** for V2-104M base (64× A100 × 4d 8h) + ~<$3k for the 14M-cancer-cell continual step ≈ **$20k all-in**. Matches the 316M general-domain V2 at ⅓ the parameters and ⅓ the compute. The cleanest published evidence that *domain curation beats parameter count*.

**Exemplar B — Nicheformer** (Theis lab, Helmholtz Munich, bioRxiv 2024): 80M-param transformer pretrained on ~110M dissociated + spatial cells with a niche-aware objective. ~$25k estimated. **Win**: niche-aware spatial decomposition outperforming general single-cell FMs.

**Exemplar C — scTab + CellPLM** (Theis + Yan/Hu): both **beat scGPT and Geneformer on cell-typing benchmarks while costing 10–20× less to train**. Direct evidence that scale wasn't the load-bearing variable.

**Venue picks**: *Nature Methods*, *Genome Biology*, *Cell Systems*. **CSHL BDS 2026** for methods talk. **Single Cell Genomics 2026** if the corpus is the contribution.

### 6.5 Lane 4 — Negative results / replication / critique ($0–$2k)

The single most valuable thing a small comp-bio lab can publish in 2026 is a rigorous demonstration that a published FM does not beat a baseline — and *Nature Methods* will take it.

**Anchor exemplar — Ahlmann-Eltze, Gerard, Huber** (EMBL Heidelberg) — *Nature Methods* 2025: pure inference on six published FMs + a one-line `mean-of-training-perturbations` linear baseline. **<$2k compute. Retired the entire sc-FM perturbation-prediction leaderboard.**

Companion examples: **Csendes scPerturBench** (BM2 Lab, Beijing Normal — independent scGPT replication exposing train/test leakage, <$1k) · **Kedzierska *Genome Biology* 2025** (Cambridge + Broad — zero-shot sc-FMs lose to PCA + kNN, <$1k) · **Wenkel *Nature Methods* 2025** — proposes `latent-additive` as the new baseline FMs must clear.

**Venue picks**: *Nature Methods*, *Genome Biology*, bioRxiv. **RECOMB 2026** (May 26–29) for methods-track replication. A dedicated negative-results venue does not yet exist — that's a §5.5 open problem.

### 6.6 Lane 5 — Benchmark curation / dataset contribution ($0–$5k + time)

Held-out splits, donor-split benchmarks, and modality-specific evaluation suites are the most under-priced contributions in the FM era — your dataset becomes infrastructure every subsequent model has to cite.

**Exemplars**: **Replogle et al. 2022 *Cell*** (Weissman lab — genome-wide Perturb-seq; cited more than most FM papers) · **Open Problems for Single Cell** (Luecken, Lance, Dann et al. — *Nat Biotechnol* 2024, ~$5k compute per task track; actively recruiting contributors as of 2026) · **HEST-1k** (Jaume et al., NeurIPS D&B 2024 — paired H&E + spatial transcriptomics, now the standard for any "H&E → spatial" model including AACR 2026 #2778 and #1442). Tahoe-100M (Vevo + Arc, Feb 2025) is industry but is the *contribution pattern* — open-source as benchmark infrastructure.

**Venue picks**: **NeurIPS Datasets & Benchmarks track** (Dec 2026). *Scientific Data*, *Nat Methods* Resource articles. **Single Cell Genomics 2026** for the curation talk.

### 6.7 Lane 6 — FM-wrapper tools / pipelines ($0–$5k)

Scverse and Bioconductor still want maintainers — a well-designed wrapper that lets non-Python users feed their data to scGPT or UNI will out-cite the underlying FM in clinical-application papers.

**Exemplars**: **signifinder** (Calura lab, U Padua; GBCC 2025 talk; Bioconductor v1.13 — 70+ curated cancer signatures with a unified API across bulk/sc/spatial) · **mia / miaTime / miaViz** (Borman, Turku; EuroBioC 2025 workshop — replaced phyloseq/QIIME2 fragmentation with one substrate) · **SpatialData** (Marconato, Palla et al., Theis + Stegle labs — the canonical Python container for paired spatial-omics + imaging; every 2026 spatial-FM paper increasingly uses it as input format).

**Venue picks**: **GBCC / EuroBioC** (annual). **scverse community paper** (next Resource update). *Bioinformatics*, *JOSS*, *F1000Research*. **CSHL BDS 2026**.

### 6.8 Lane 7 — FM-aided wet-lab / clinical application ($5k–$50k)

Once an FM is publicly available, using it as instrumentation inside a clinical or wet-lab study is *a clinical paper that happens to use a frozen FM* — and AACR 2026 has at least 18 such posters in our pathology slice alone.

**AACR 2026 exemplars**: **#4163 KRONOS** (Stanford + Mahmood collabs — general-purpose spatial-proteomics FM; outperforms UNI/CA-MAE on the relevant tasks) · **#1442 Virchow2 + VIDCellTyper** (TNBC tumour-proportion from H&E without IHC, <$2k) · **#2778 DINOv2 spatial-transcriptomics joint fine-tune** (~$5–10k for the joint fine-tune; DINOv2 backbone free) · **#1444 H-optimus-0 + ABMIL** (Owkin H-optimus for Lauren-subtype gastric classification, <$2k).

**Beyond AACR — the first published real-world clinical deployment**: **Janowczyk et al. 2025 *Nature Medicine*** — "[Real-world deployment of a fine-tuned pathology foundation model for lung cancer biomarker detection](https://www.nature.com/articles/s41591-025-03780-x)" — fine-tuned UNI identifies EGFR mutations from H&E in a 197-patient clinical trial, **potentially preventing further genetic testing in 43% of cases**. This is the proof-point that Lane 7 graduates into actual clinical decision support — and it lands the §8.3 buyer-map argument for clinical-AI vendors as the cleanest check-writer for Lane 7 work.

**Venue picks**: *Clinical Cancer Research*, *JCO CCI*, *npj Precision Oncology*, *Cancer Discovery*. **AACR Annual** (Apr); **AACR Pancreatic / SITC 2026** for indication-specific; **ASCO 2026** if endpoint is treatment-response.

### 6.9 The decision tree — which lane is yours? (30 sec, 1 slide)

```
Do you have wet-lab/clinical data the FM authors did not see?
├── YES → Lane 7 (FM-aided application). Pick a frozen FM whose pretraining
│         corpus excludes your tissue/donor type; that gap is your contribution.
└── NO
    │
    Do you have a curated dataset or held-out split no public benchmark uses?
    ├── YES → Lane 5 (benchmark / dataset). Submit to Open Problems v2 / NeurIPS D&B.
    └── NO
        │
        Can you write a model adapter / LoRA layer in PyTorch?
        ├── YES → Lane 2 (PEFT). scGPT/Geneformer-V2/UNI2 + your task; <1% params;
        │         ICLR/NeurIPS workshop track.
        └── NO
            │
            Do you have ~$10k of cloud credit + a domain corpus?
            ├── YES → Lane 3 (domain FM). Geneformer-V2-104M_CLcancer playbook
            │         on your disease area.
            └── NO
                │
                Strong R/Python/Bioconductor maintainer?
                ├── YES → Lane 6 (wrapper tool). Pick the FM your audience can't
                │         run themselves; ship a Bioconductor/scverse package.
                └── NO
                    │
                    Default → Lane 1 (embeddings as features) OR Lane 4 (replication).
                    Both <$500 with *Nature Methods* precedents.
```

### 6.10 The bridge to AACR 2026 (30 sec)

**Evidence from the AACR 2026 corpus** (counts derived by case-sensitive grep of poster titles + abstracts against a curated list of FM model names — see methodology note below):

| Topic | n posters | Pathology FM by name | Single-cell FM by name | Genomic FM by name | "foundation model" generic (no model named) |
|---|---|---|---|---|---|
| Virtual Cells | 48 | 11 | 5 | 3 | 20 |
| Bioinfo / AI methods | 536 | 17 | 5 | 6 | ~35 |
| Single-cell & spatial | 1,015 | (not counted in this pass) | 4 | (not counted) | 16 |

**Three patterns visible in those numbers:**

1. **Zero posters put a single-cell FM in the title.** Across all three topics, scGPT / Geneformer / scFoundation / CellPLM / scBERT appear in 14 posters total (out of ~1,600 scanned), and never in the title. The sc-FMs are tools, not headline contributions.
2. **Pathology FMs dominate the "named FM" category.** UNI / Virchow / CHIEF / Prov-GigaPath / PathChat / Hibou / H-Optimus / PLUTO appear in 17/536 bioinfo posters and 11/48 virtual-cells posters. Almost every instance uses the FM as a frozen encoder for a clinical readout, *not* training a new FM. **Lane 7 (FM-aided application) is the dominant pattern at AACR 2026 by an order of magnitude.**
3. **Most "foundation model" mentions don't name the model.** 20/48 virtual-cells posters and ~35/536 bioinfo posters use generic "foundation model" / "pretrain" language without identifying which FM. This is partly abstract-length pressure, partly that many groups are training small *custom* FMs (RNA1-DA, methylFM, gastroFM, MutationProjector, Path2Prot, Visiumformer, HoneyBee) rather than using a community-named one.

Lane 1 (embeddings as features) is the structural prerequisite for almost all of Lane 7. Lanes 2–6 are the methodological substrate for what AACR application papers will look like in 2027–2028.

!!! note "Counting methodology"
    Numbers above are reproducible from the poster JSON files in `docs/assets/aacr-2026/posters/` (raw data in repo; load each topic's `.json` and grep title + abstract). Match list: pathology = `UNI, UNI2, UNI2-h, Virchow, CHIEF, GigaPath, PathChat, CONCH, Phikon, Hibou, H-optimus, PLUTO, gastroFM, Path2Prot, Visiumformer, MutationProjector, HoneyBee, BARRACUDA`; single-cell = `scGPT, Geneformer, scFoundation, CellPLM, scBERT`; genomic = `Nucleotide Transformer, DNABERT, HyenaDNA, Evo, AlphaGenome, methylFM, RNA1-DA, DNAchunker`. Case-sensitive substring match against title + abstract. Each poster counted once; first-match-wins by family ordering. This undercounts in two directions: (a) posters that use an FM but don't name it; (b) custom FMs not in the match list. Treat numbers as a **floor**, not a ceiling.

The honest framing for an academic comp-bio audience in 2026 is not *"can I compete with Arc Institute on training?"* (no) but *"which of these seven lanes is mine?"* — one of them, definitely, and the answer is in **your data, not your GPU budget**.

---

## §7. Real innovation tracks — frontier methods research at <$10k compute (4 min)

> **Framing.** §6 was about contributing *through* FMs. This is about contributing *to* the FM literature with original methods work — new algorithms, new theory, new evaluation, new architectures. **The bottleneck on these is not compute; it is ideas.** Six tracks where the field has a structural gap a small lab can close in 12–18 months, each with a real exemplar that proves the lane is alive.

### 7.1 The six tracks at a glance (30 sec, 1 slide)

| Track | Open problem | Compute | Why a small lab can win |
|---|---|---|---|
| 1. Mechanistic interpretability of biology FMs | What do scGPT/Geneformer/UNI actually learn? | <$2k | Sparse autoencoder + linear-probe work is wide open. Methodology imported from Anthropic 2024. |
| 2. New pretraining objectives that target causality | Next-gene-prediction optimizes correlation — that's *why* FMs lose to linear baselines | $5–20k | Smaller model + better objective often wins (Geneformer-V2-104M proof) |
| 3. Compositional generalization benchmarks + theory | Does A+B generalize when model saw only A and B? | <$2k | Norman 2019 has the data; no one has formalized the benchmark |
| 4. Architectures with biology-specific inductive biases | BERT clones ignore pathway / network / lineage priors | $5–15k | Genuine biology+architecture co-design is rare |
| 5. Uncertainty / OOD detection for clinical-grade FMs | Every FDA path needs calibrated uncertainty; none of the FMs have it | $1–5k | Post-hoc Bayesian heads on frozen embeddings — no pretraining needed |
| 6. Causal evaluation frameworks | What's the *correct* test for causality, post-Ahlmann-Eltze? | <$3k | Wenkel set a baseline; the next paper to set a higher bar is wide open |

### 7.2 Track 1 — Mechanistic interpretability of biology FMs

**The open problem.** scGPT has 33M parameters and ~12 transformer layers. We are starting to know what they encode — but the literature is months old, the methodology is unsettled, and the cancer-domain case is wide open.

**What changed in 2025–2026.** The field that didn't exist when this talk was first drafted now has its first wave of papers (see §11.6 for full citations):

- **Simon & Zou 2025–2026 *arXiv*** — "Sparse autoencoders reveal organized biological knowledge but minimal regulatory logic in single-cell foundation models: a comparative atlas of Geneformer and scGPT" — the headline finding: SAEs on sc-FMs recover *cell-type and pathway* features cleanly, but *regulatory / causal* features are weak. Matches the Ahlmann-Eltze story from §4 at the mechanism level.
- **Adams et al. 2025 *PNAS*** — Sparse autoencoders uncover biologically interpretable features in protein language model representations.
- **bioRxiv 2025 "Sparse Autoencoders Reveal Interpretable Features in Single-Cell Foundation Models"** — independent confirmation on scGPT.
- **Hibou-LP team 2024–2025** — Learning biologically relevant features in a pathology FM with SAEs (the first pathology-FM SAE).
- **bioRxiv 2026 "What Do Biological Foundation Models Compute?"** — synthesis paper proposing a cross-FM SAE methodology.

**So the "first-paper" pitch is gone — but the cancer-specific version isn't.** The published SAE work uses general-domain sc-FMs (scGPT, Geneformer on CELLxGENE). **No one has run SAEs on a *cancer-curated* sc-FM** (Geneformer V2-104M_CLcancer, CancerFoundation) to ask: do the cancer-domain features differ from the general-domain ones, and do they predict therapy response or resistance better?

**A 12-month project (revised).** Train SAEs on Geneformer V2-104M_CLcancer's residual-stream activations, compare feature atlas vs the same SAE on V2-104M_general. Specifically: do cancer-specific features (e.g., EMT, hypoxia, immune-evasion programs) emerge cleanly in the cancer-curated model but not the general one? Validate by knockout in held-out perturbation data. **Compute: <$2k — inference-only on frozen weights plus a few hundred dollars of SAE training.** Now it's a *cancer mechanism* paper, not a *first-SAE* paper — which is a better story for a comp-bio audience anyway.

**Venues**: NeurIPS / ICLR Mechanistic Interpretability workshop; *Nature Methods*, *Cell Systems*; *Cancer Discovery* if the validation lands.

### 7.3 Track 2 — New pretraining objectives that target causality

**The open problem.** Next-gene-prediction (scGPT) and masked-gene-modeling (Geneformer) optimize *correlation*. That's structurally why both lose to a linear baseline on perturbation prediction. **The objective is misaligned with the downstream task.**

**Why a smaller model can win.** Geneformer-V2-104M_CLcancer beat the 316M general model. STATE (Arc Institute) introduced perturbation-aware pretraining at modest scale. Hetzel et al. 2024 (Theis lab) showed compositional pretraining beats brute-force scale.

**A 12-month project.** Design a **counterfactual pretraining objective**: for each cell, predict gene expression *under a held-out perturbation* using invariant risk minimization (Arjovsky et al. 2019) or contrastive perturbation losses. Pretrain a 20M-param model with this objective on Tahoe-100M; show it beats scGPT-33M on Norman + Replogle held-out splits. **Compute: $5–20k for the pretraining step.**

**Real exemplar.** Lopez, Hsu et al. 2025 *Nat Methods* on causal representation learning for single-cell. CINEMA-OT (Bunne 2023, optimal-transport-based perturbation matching). **The design space — IRM, invariant prediction, contrastive perturbation, energy-based causal priors — is wide open.**

**Venues**: ICLR / NeurIPS main, *Cell Systems*, *Nature Methods*.

### 7.4 Track 3 — Compositional generalization benchmarks + theory

**The open problem.** When a model sees perturbations A and B separately, does it generalize to A+B? Norman et al. 2019 has 287 combinatorial perturb-seq splits — but **no published sc-FM has been formally evaluated for compositional generalization with theoretical guarantees**.

**Why the field hasn't done this.** Standard benchmarks score Pearson correlation across all perturbations. The combinatorial split is the harder test and nobody has prosecuted it rigorously.

**A 12-month project.** Build a held-out compositional-perturbation benchmark from Norman + Replogle. Score every sc-FM on it. **Then prove a theoretical lower bound** on what an additive baseline (sum-of-singles) achieves. Find regimes where FMs *should* beat additivity — and show whether they do. **Compute: <$2k — inference + closed-form analysis.**

**Real exemplar.** Hetzel et al. 2024 NeurIPS LMRL workshop "compositional perturbation" paper. Boiarsky et al. 2023 NeurIPS workshop (linear-baseline warning, predates Ahlmann-Eltze). **The post-Ahlmann-Eltze "what's the next bar?" question is unanswered — the compositional answer is one strong candidate.**

**Venues**: NeurIPS D&B, ICLR, *Nature Methods*, *Genome Biology*.

### 7.5 Track 4 — Architectures with biology-specific inductive biases

**The open problem.** All current biology FMs are domain-agnostic transformer clones. But biology has **rich exploitable structure**: gene-gene interaction networks, pathway hierarchies, cell-lineage trees, regulatory grammar, evolutionary conservation. None of it is in the architecture.

**Why a small lab can compete.** Architecture innovation is a *theory* problem, not a *scale* problem. HyenaDNA (state-space for DNA), Caduceus (reverse-complement equivariance), Enformer (1D convolutions for regulatory tracks) — all are small-lab-feasible architectural contributions that the big labs missed.

**A 12-month project.** Build a **graph-attention transformer** that takes a gene-gene interaction graph (StringDB / Reactome / OmniPath) as a fixed prior on attention weights. Pretrain on a 1M-cell subset of CELLxGENE. Evaluate on cell-typing + perturbation prediction. Hypothesis: pathway-aware attention beats general attention at this scale. **Compute: $5–15k for ablation studies.**

**Real exemplar.** scGNN, GraphSAGE for single-cell. HyenaDNA + Caduceus for DNA. scFoundation's read-depth-aware attention is the closest single-cell example of architecture-biology co-design — but most of the design space is unexplored.

**Venues**: ICLR / NeurIPS main, *Cell*, *Nature Methods*.

### 7.6 Track 5 — Uncertainty / OOD detection for clinical-grade FMs

**The open problem.** Every FDA-deployable model needs calibrated uncertainty and out-of-distribution detection. **None of the current biology FMs provide either.** PathChat DX got Breakthrough Designation *in spite of this*, not because of it.

**Why a small lab can win.** This is post-hoc work on frozen FMs. You don't need to train anything large.

**A 12-month project.** Implement four UQ methods on top of frozen UNI2-h embeddings: (1) deep ensembles, (2) MC dropout, (3) Laplace approximation on the final layer, (4) conformal prediction. Evaluate calibration + selective-prediction accuracy + OOD detection on TCGA → CPTAC distribution shift. **Compute: $1–5k — inference + small classifier training only.**

**Real exemplar.** van Amersfoort et al. 2024 on deep deterministic UQ. Angelopoulos & Bates 2023 tutorial on conformal prediction (now widely cited; biology applications underdeveloped). **No published clinical-grade UQ work for pathology FMs as of May 2026.**

**Venues**: *Nature Methods* (Resource), *Lancet Digital Health*, ICML, NeurIPS.

### 7.7 Track 6 — Causal evaluation frameworks (post-Ahlmann-Eltze)

**The open problem.** Wenkel proposed `latent-additive + scGPT-embeddings` as the new baseline. But that's still a *correlational* baseline. **What's the right test for whether a model recovered causal structure?**

**Why a small lab is positioned for this.** Causal benchmarks need genetic instruments (Mendelian randomization, MR-Egger), validated drug mechanisms (ChEMBL + DrugBank), and known TF-target relationships (ENCODE + ChIP-Atlas). The data already exists; the benchmark design is the contribution.

**A 12-month project.** Build a **causal-recovery benchmark** with three test sets: (a) MR-validated genetic effects, (b) validated drug MOA on cell lines (LINCS L1000), (c) ENCODE TF-target relationships. Score every sc-FM. Define a "causal F1" metric. Publish as a public leaderboard. **Compute: <$3k — inference + benchmark infrastructure.**

**Real exemplar.** Lopez, Hsu et al. 2025 on causal representation learning. Ahlmann-Eltze set the correlational bar; **the next paper to set a higher bar is wide open.**

**Venues**: *Nature Methods*, *Genome Biology*, ICLR, NeurIPS.

### 7.8 The unifying frame (30 sec)

The §6 playbook said: *use FMs to contribute*. This section says: *innovate on FMs themselves with small-lab resources*. **The bottleneck on every track above is intellectual, not financial.** The big labs are spending $5M+ on bigger models; the small lab's edge is in:

- **Interpretability** (Track 1) — nobody is doing the work
- **Better objectives** (Track 2) — better objective beats more compute, repeatedly
- **Better benchmarks** (Tracks 3, 6) — what you measure shapes what gets built
- **Better priors** (Track 4) — biology's structure isn't in transformer attention
- **Calibration** (Track 5) — clinical deployment needs it; FMs don't have it

These are the lanes where a single PhD student or postdoc can publish a *Nature Methods* paper or an ICLR main-track paper in 12–18 months **without ever training an FM from scratch**. The compute budget for each is <$20k — and several are <$2k.

**The real one-liner**: the virtual-cell vision isn't going to be solved by scaling existing FMs. It's going to be solved by someone who builds the right *evaluation framework*, the right *causal objective*, and the right *interpretability tools* — and that someone could be in your lab.

---

## §8. Commercial interest — who's paying for this and why (4 min)

> **Why this section exists.** The §6 + §7 inventory was the academic landscape. But for a group meeting that needs to pick a project, the next question is fundability: *who would sponsor, license, or acquire this work?* The commercial money chases regulatory-grade methods (UQ, interpretability, causal evaluation) and clinical-grade applications — not another scGPT clone. This section names the buyers, the 2024–2026 signals, and what each of our three §9 pitches would attract.

### 8.1 The three buyer archetypes (90 sec, 1 slide)

| Archetype | Named players (2026) | What they buy from academia | Typical funding form |
|---|---|---|---|
| **A. Big pharma — drug discovery / target ID** | Lilly, AstraZeneca, Pfizer, Novartis, Roche/Genentech, BMS, Merck, Sanofi | target-ID validation, FMs for cell-painting / phenotypic screens, biomarker discovery for trial enrichment, regulatory-grade UQ | sponsored research ($100k–$2M), talent pipeline, postdoc-funded internships |
| **B. AI-native biotech / discovery platforms** | Recursion (post-Exscientia merger), Insitro, Isomorphic Labs (Alphabet), Owkin, Latent Labs, Vevo / Arc Institute, Cellarity, BenchSci | licensable FM weights, dataset-curation partnerships, methods that improve internal models, acquisitions of academic spinouts | sponsored research ($50–200k), co-authored papers, dataset access, equity-for-IP |
| **C. Clinical-AI / pathology-AI vendors** | PathAI, Paige (FullFocus FDA-cleared), Tempus AI (NYSE-listed), Aignostics, Proscia, Modella AI (→ AstraZeneca), Roche Tissue Diagnostics, Leica | clinical-grade UQ, pathology FM weights, FDA-pathway-ready interpretability, sponsored validation studies | sponsored validation ($100–500k), co-marketing of academic findings, acquisitions |

The archetypes are not interchangeable. **Pharma (A) buys de-risked science; AI-native biotech (B) buys methods that move their leaderboard; clinical-AI vendors (C) buy regulatory ammunition.** The audience for our paper is one of these three — pick before you start writing.

### 8.2 The 2024–2026 commercial signals timeline (90 sec, 1 slide)

The money pattern: **2024 = platform launches; 2025 = FDA pathway proofs; 2026 = acquisitions + infrastructure commitments.**

| Date | Event | Why it matters |
|---|---|---|
| Jun 2024 | Tempus AI IPO (NYSE) | First multimodal-clinical-AI public listing; sets the market-cap reference for the category |
| Aug 2024 | Recursion + Exscientia merger announced | Combined the largest cell-painting platform with a generative-design platform; consolidation signal |
| Dec 2024 | CZ Biohub Virtual Cell program announced | Multi-billion-dollar non-dilutive commitment; the single biggest virtual-cell funding signal in history |
| 2024 | Microsoft + Providence release Prov-GigaPath | First Microsoft co-development of an open pathology FM |
| Jan 2025 | **Paige FullFocus FDA 510(k) clearance** | First general-purpose pathology AI cleared by FDA |
| Jan 2025 | **PathChat DX FDA Breakthrough Device Designation** | First generative-AI pathology tool to win Breakthrough; the regulatory template |
| Feb 2025 | Arc Institute + Vevo open-source Tahoe-100M | Largest perturbation atlas; opens the substrate other companies have to compete with |
| 2025 | Latent Labs founded | DeepMind alumni virtual-cell startup; venture-grade signal that the academic vision is fundable |
| Jan 12, 2026 (JPM Day 1) | **Lilly + NVIDIA $1B AI Co-Innovation Lab** | Largest pharma–AI infrastructure commitment ever announced at JPM. ([JPM 2026 themes](../conferences/jpm-2026/themes.md)) |
| Jan 13, 2026 (JPM Day 2) | **AstraZeneca acquires Modella AI** | **First big-pharma acquisition of an AI firm.** Partnership-→-ownership shift in the buyer/builder relationship. Modella AI built multimodal FMs for oncology. ([JPM 2026 themes](../conferences/jpm-2026/themes.md)) |
| Jan 14, 2026 (JPM Day 3) | Pfizer: "embed AI across the business" | Buyer-side commitment broader than any single deal |
| Apr 17–22, 2026 | **AACR 2026 ED03 + AT02 + 4/22 Oncologist sessions** | The first AACR with FM/agentic-AI on the main program — the buyer-meets-builder venue |

The slide for this section is the timeline visualisation. The line to deliver: *"the academic field had its discipline crisis in 2025 (Ahlmann-Eltze); the commercial field had its acquisition wave in 2026 (Modella → AstraZeneca, Lilly + NVIDIA). Those happened in the same six months. That's the climate we're choosing a project in."*

### 8.3 The per-pitch buyer map — who writes the check for each §9 pitch? (60 sec, 1 slide)

The load-bearing slide. For each of the three project pitches in §9, the most likely buyer + the funding form + the precedent signal.

| Pitch | Primary buyer archetype | Specific named buyers | Funding form | Precedent signal |
|---|---|---|---|---|
| **A — Pathology FM interpretability + clinical UQ** | C (clinical-AI vendors) | Paige, PathAI, Tempus AI, Aignostics, **Modella AI → AstraZeneca** | sponsored research $100–500k, or postdoc-funded internship | PathChat DX FDA Breakthrough — the interpretability + UQ story is *the* regulatory template |
| **B — Compositional perturb benchmark + linear-baseline re-audit** | B (AI-native biotech) | **Recursion** (cell-painting validation), Insitro, Latent Labs, **Vevo / Arc** | dataset access + sponsored research $50–200k + co-authored papers | Tahoe-100M open-source was a Vevo/Arc move precisely to set the benchmark substrate; setting the *next* substrate sets the standard |
| **C — Rare-cancer FM-aided subtyping + small domain FM** | A (big pharma rare-disease) | **Pfizer** (rare-disease focus 2025+), Sanofi (oncology), AstraZeneca (rare oncology post-Modella), Vertex; secondary: Tempus AI | clinical-trial enrichment partnership $500k–$2M, or direct sponsored research | AACR Pancreatic / SITC indication-specific posters are the recruitment funnel for pharma drug-program teams |

### 8.4 The honest framing (15 sec)

The commercial money does **not** chase another scGPT clone. It chases:

1. **Regulatory-grade methods** — §7 Track 5 (UQ), Track 1 (interpretability), Track 6 (causal evaluation). These are also the most academically publication-friendly. Convergent signals.
2. **Clinical-grade applications** — §6 Lane 7. These get sponsored research and trial-enrichment partnerships.
3. **Benchmark substrate** — §6 Lane 5 + §7 Track 3. Setting the eval surface is high-leverage if you can land it before someone else does.

**The bridge to §9**: the three pitches were designed without the commercial frame in mind, and yet all three map cleanly to one of the three buyer archetypes. That's not coincidence — it's because the technical gaps and the commercial gaps overlap by construction. The right project is the one where *we* find it intrinsically interesting *and* there's an obvious buyer for the output. If both check out, we're choosing a defensible project, not just a publishable one.

---

## §9. Discussion — picking our lane (10 min, group conversation)

This is the point of the meeting. The §6 + §7 inventory was the menu; this is where we decide what's actually on our plate. Below are concrete project pitches sized for one PhD student or postdoc over 12 months — each combines a §6 lane (publishable applied) with a §7 track (publishable methods) so the same project lands two papers from different angles.

### 9.1 Three concrete project pitches we could take on

#### At-a-glance

| Pitch | §6 lane | §7 track | §8 buyer | Compute | Time | Output venues |
|---|---|---|---|---|---|---|
| **A** Pathology FM interpretability + clinical UQ | Lane 7 | Track 1 + Track 5 | Clinical-AI (Paige, PathAI, Tempus, Modella→AZ) | <$3k | 12 mo | NeurIPS Mech-Interp + *Nat Methods* Resource + AACR poster |
| **B** Compositional perturb benchmark + linear-baseline re-audit (cancer) | Lane 4 | Track 3 | AI-native biotech (Recursion, Insitro, Latent, Vevo) | <$2k | 8 mo | NeurIPS D&B + *Nat Methods* |
| **C** Rare-cancer FM-aided subtyping + small domain FM | Lane 7 + Lane 3 | (applied focus) | Pharma rare-disease (Pfizer, Sanofi, AZ, Vertex) | <$25k | 18–24 mo | AACR poster + *Clin Cancer Res* + *Nat Methods* |

Full description of each below.

#### Pitch detail

**Pitch A — Pathology FM interpretability + clinical UQ.** Combines §7 Track 1 (sparse autoencoders on pathology FMs) + §7 Track 5 (uncertainty quantification on frozen FMs) + §6 Lane 7 (clinical application). The work: take UNI2-h (or Virchow2 — pick based on license), train sparse autoencoders on its residual-stream activations over a TCGA slice, cluster features and map them to histology grammar (tumor regions, stromal compartments, immune infiltrate patterns). Then layer a post-hoc Bayesian or conformal-prediction head and evaluate calibration on TCGA → CPTAC distribution shift. **Output**: NeurIPS Mech-Interp workshop (interpretability), *Nature Methods* Resource (UQ), AACR-Annual-style clinical poster. **Compute**: <$3k. **Time**: 12 months. **Why us**: builds on existing TCGA familiarity; no wet-lab required.

**Pitch B — Compositional perturbation benchmark + linear-baseline re-audit on cancer perturb-seq.** Combines §6 Lane 4 (replication) + §7 Track 3 (compositional benchmarks). The work: rebuild scGPT + Geneformer + UCE evaluation pipelines on Norman 2019 + Replogle 2022 + Tahoe-100M with cancer-specific cell-line subsets. Add the Ahlmann-Eltze linear baseline and the Wenkel latent-additive baseline. Then design a formal compositional split (A+B held out when A and B seen separately) and prove a theoretical lower bound on what additivity achieves. **Output**: NeurIPS D&B (benchmark), *Nature Methods* (linear-baseline replication in cancer context), maybe a second *Genome Biology* paper. **Compute**: <$2k. **Time**: 8 months. **Why us**: leverages the AACR-corpus context; cancer-specific findings are differentiating.

**Pitch C — FM-aided rare-cancer subtyping + small domain FM.** Combines §6 Lane 7 (FM-aided application) + §6 Lane 3 (domain-specific small FM). The work: pick a rare-cancer cohort the public pathology-FM training corpora missed (rhabdomyosarcoma, ATC, NET, mesothelioma, etc.). First publish a frozen-encoder application paper (like AACR #2758 PAX3/7::FOXO1 in rhabdomyosarcoma — Lane 7). Then continual-pretrain a Geneformer-V2-104M-style domain FM on the cohort's matched scRNA-seq + a 100k-cell rare-cancer reference. **Output**: AACR poster + *Clinical Cancer Research* or *npj Precision Oncology* (Year 1), then *Nature Methods* domain-FM paper (Year 2). **Compute**: <$25k all-in. **Time**: 18–24 months. **Why us**: most defensible if we have a clinical collaborator with a rare-cancer cohort.

### 9.2 Decision questions for the group

A short list to surface what we have and what we need. Run through these explicitly — don't let "we'll figure it out" stand in for an answer.

**Strengths**
- Which of the five FM families (§2) is closest to existing group expertise?
- Of the 14 anchor models (§3), which two could anyone here actually rederive on a whiteboard?
- Do we have any in-house data the public FM training corpora *didn't* see (rare cohort, novel modality, new tissue type)?

**Constraints**
- Real cloud / on-prem GPU budget per year for FM work specifically?
- Any postdoc / PhD-student bandwidth that could be 50%-allocated to one of these for 12 months?
- Wet-lab or clinical collaborators we'd need to recruit for Pitch C (rare-cancer cohort)?

**Strategic**
- Which is more valuable for our PI's tenure / grant story — *applied paper in a clinical venue* (Pitch C Year 1) or *methods paper in a top ML venue* (Pitches A or B)?
- Are we trying to attract ML talent (Pitches A/B do this) or clinical talent (Pitch C does this)?
- Do we want a 6-month-output project (Pitch B replication) or an 18-month-output project (Pitch C subtype FM)?

**Tactical**
- Of the three pitches, who would lead each? Who would co-author?
- Can we run TWO in parallel — one applied (Pitch C Year 1) + one methods (Pitch A or B)?
- What's the no-go signal that tells us to drop a pitch at month 3?

### 9.3 The honest framing for this meeting

The §1.3 thesis was: *the gap between FMs and virtual cells is the most concrete research agenda single-cell biology has had in a decade*. The §7 innovation tracks specify the gap. The §6 playbook specifies the work that's adjacent enough to be safe. **The right project for this group is one §6 lane plus one §7 track, run in parallel, so we publish a low-risk applied paper while a higher-risk methods paper develops.**

The §9 closing argues that AACR-style clinical conferences will be the evaluation surface for whichever lane we pick. If our methods paper survives the AACR-corpus-style stress test (Lane 7 posters, donor-diversity, clinical heterogeneity), it's the real thing. If it doesn't, we've replicated the field's 2023–2024 mistake at smaller scale.

---

## §10. Closing — conferences as the ground truth (3 min)

For a methods audience, the natural close is to flip the frame: the conferences are not where you *see* FMs in biology — they are the *evaluation surface*. Methods conferences (NeurIPS / ICLR / ICML) tell you what works on benchmarks; clinical conferences (AACR / ASCO / ESMO) tell you what works on cancer. Use AACR 2026 — happening *this April 17–22*, the week before ICLR — as the live case study.

### 10.1 The two-track timeline (1 min, 1 slide)

Two parallel timelines, deliberately scrambled together so the audience can see how often the methods track ran ahead of the clinical track.

| Year | Methods conferences / journals | Clinical / industry signal |
|---|---|---|
| 2023 | scGPT (Nature Methods), Geneformer (Nature), UNI submitted | — |
| 2024 | UCE, scFoundation, AlphaFold3 (Nature), Virchow (Nature), CHIEF (Nature) | Bunne et al. *Cell* perspective coins the **virtual cell** thesis |
| **Dec 2024** | — | **CZI announces multi-year Virtual Cell Program** |
| **Jan 2025** | — | **PathChat DX — first FDA Breakthrough Device Designation for generative-AI pathology** |
| **Feb 2025** | — | **Arc Institute + Vevo release Tahoe-100M** (100M cells × 1,100 drugs × 50 cell lines) |
| 2025 | **Ahlmann-Eltze & Huber** (*Nature Methods*) + Kedzierska (*Genome Biology*) + Wenkel — **the reckoning**: linear baselines beat scGPT / Geneformer / UCE / scFoundation on perturbation prediction | Virchow2 wins Campanella et al. multi-task clinical benchmark |
| Apr 2026 | ICLR 2026 (Apr 23–27, Rio): sc-Arena, sc-FM PertAdapt, MedAgentGym, Proteina Complexa | **AACR 2026 (Apr 17–22, Chicago)** — first AACR with a *dedicated* FM session **and** a dedicated agentic-AI session |

The visual punchline: **the clinical track is one year behind the methods track on awareness, and one year ahead on accountability**. The reckoning didn't come from ICLR — it came from *Nature Methods*. The deployment bar isn't being set by NeurIPS — it's being set by the FDA.

### 10.2 AACR 2026 as the case study (90 sec, 1 slide)

The corpus from this site ([aacr-2026.pages.dev](https://aacr-2026.pages.dev/conferences/aacr-2026/)): **25 unique sessions, ~464,000 words of transcripts, 2,241 poster abstracts (~871,000 words)** — organized into five axes: agentic AI, single-cell/spatial, virtual cells, bioinfo/AI methods, clinical trials.

Three things AACR 2026 gives us that ICLR/NeurIPS structurally cannot:

1. **The deployment reality check — [ED03 "Foundation Models and Multimodal AI for Cancer Research"](../conferences/aacr-2026/sessions/2026-04-17-pm-foundation-models-multimodal-ai-cancer-research.md) (Fri Apr 17, PM)** with **Charlotte Bunne / Serena Yeung-Levy / Michael Moor**. Bunne wrote the 2024 *Cell* virtual-cell perspective. Moor brings the agentic-AI-in-oncology-workflow slot. This is the field's first AACR-stage definitional panel — not "does our model beat a benchmark," but "what does deployment even mean here?"

2. **The donor-diversity stress test — [single-cell & spatial track](../conferences/aacr-2026/topics/single-cell-spatial-omics/index.md) (20 sessions, 1,015 posters)**. Spans HTAN tumor-evolution, clonal-hematopoiesis, TME heterogeneity, neural-immune crosstalk, fibroblast-state plasticity. ML conferences evaluate FMs on synthetic perturb-seq splits; AACR is where the actual heterogeneity surface lives. The **§5.1 donor-diversity gap either shows up here loudly, or it doesn't.**

3. **The agentic-AI-for-discovery proof — [AT02 "Agentic AI as the Cancer Researcher" (Tue Apr 21)](../conferences/aacr-2026/sessions/2026-04-21-at02-agentic-ai-cancer-researcher.md) + ["Agentic AI as the Oncologist" (Wed Apr 22)](../conferences/aacr-2026/sessions/2026-04-22-agentic-ai-as-the-oncologist.md)**. ICLR 2026 gave us MedAgentGym (72k task sandbox); AACR gives us *the actual research and clinical workflows* those agents are supposed to inhabit. Two sessions in one week is a deliberate field statement.

Cross-link the corpus: [AACR 2026 Virtual Cells topic](../conferences/aacr-2026/topics/virtual-cells/index.md) · [Agentic AI topic](../conferences/aacr-2026/topics/agentic-ai/index.md) · [Bioinfo/AI methods topic](../conferences/aacr-2026/topics/bioinfo-tools/index.md).

### 10.3 What we knew before → what AACR 2026 changes (30 sec, 1 slide)

The before/after, in one table:

| The five gaps (from §5) | What we knew before AACR 2026 | What AACR 2026 lets us answer |
|---|---|---|
| **Donor diversity** | sc-FMs trained on CELLxGENE Census ≈ 50M cells, donor-skewed | Do the AACR spatial/HTAN posters show real heterogeneity coverage, or the same skew? |
| **Cross-species** | Mouse-only models still dominate; few human-validated readouts | The 1,015 single-cell/spatial posters are mostly human-patient cohorts — first real-population test |
| **Causal vs correlational** | sc-Arena, PerturBench show benchmark-level concerns | AT02 + ED03 are the first conference venue where agentic AI is asked to *propose interventions*, not just retrieve |
| **Compute access** | Evo2 + ESM-3 = >$7M of the ~$15M total identified FM training spend across 14 models | Is academic single-cell FM work actually competitive at AACR, or do industry-trained models dominate the posters? |
| **Honest evaluation** | 2025 critique trio set the bar; ICLR 2026 sc-Arena formalized it | Does AACR 2026 cite the linear-baseline papers in the FM-using posters, or quietly ignore them? |

The closing line: **the talk's thesis was that the gap between FMs and virtual cells is the field's most concrete research agenda. The corpus on this site is one way to track whether the field is actually closing that gap, conference by conference.**

---

## §11. Appendix

### 11.1 Likely Q&A questions + scripted answers

**Q: Are FMs ready for clinical deployment?**
A: In pathology, yes — PathChat DX has FDA Breakthrough Designation, and Virchow2 / UNI2-h are in active clinical-grade evaluation. In single-cell biology, no — the linear-baseline reckoning means we don't yet have a single-cell FM whose predictions can be trusted for clinical decisions. Genomic FMs (AlphaGenome) are an intermediate case: they predict variant effects well in benchmark settings but have not been deployed against clinical decision-making at scale.

**Q: Why doesn't more compute solve this?**
A: It might for pathology — Virchow2G at 1.85B is the latest scale push and we don't yet know if the curve is plateauing. For single-cell, the Geneformer-V2-104M_CLcancer result suggests *more* compute on *general* data is not the bottleneck. Domain curation and evaluation are.

**Q: What about agentic AI / LLM-driven pipelines?**
A: MedAgentGym (ICLR 2026) is the strongest demonstration so far: 72k-task sandboxed code-exec gym + Med-Copilot-7B that orchestrates biomedical analyses. Agentic AI is the *interface layer* on top of the FMs — it doesn't fix the underlying FM accuracy problems but it makes them more accessible. AACR 2026's AT02 session is the natural venue if you want to see this in person.

**Q: Will any of these be available with permissive licenses?**
A: Mixed picture. Single-cell FMs (scGPT, Geneformer, UCE, scFoundation, CellPLM, GET) are mostly MIT/Apache-2.0. Pathology FMs are mostly CC-BY-NC with the Hibou exception (Apache-2.0). Protein FMs split (ESM-2 open, ESM-3 partially gated). Genomic FMs mostly open except AlphaGenome. **Track licenses carefully** — UNI's Jan 2025 HF gating shift is the cautionary tale.

**Q: What benchmark would I actually trust?**
A: For single-cell FMs: PerturBench `latent-additive + scGPT-embeddings` baseline is the floor; clear it first, then report your task. For pathology: Campanella et al. 2025 *Nature Communications* multi-task panel. For genomic: gnomAD-pathogenic + ENCODE/GTEx variant-effect benchmark (AlphaGenome's home territory). For protein: CASP15/16 + retro-validated novel-binder hit rates.

### 11.2 Datasets, weights, code — concrete starting points

**Datasets**:
- [Tahoe-100M](https://www.tahoe.ai) — 100M cells × 1,100 drugs × 50 cell lines (Vevo / Arc Institute)
- [CellxGene Census](https://cellxgene.cziscience.com) — ~50M+ standardized cells, the canonical scRNA atlas
- [Replogle Perturb-seq](https://gwps.wi.mit.edu/) — gold-standard whole-genome perturbation dataset
- [Open Problems for Single Cell](https://openproblems.bio) — benchmark hub
- [HEST-1k](https://github.com/mahmoodlab/HEST) — 1k WSI spatial transcriptomics benchmark

**Weights**:
- [scGPT (HuggingFace)](https://huggingface.co/wangshenguiuc/scGPT) — MIT
- [Geneformer V2 (HuggingFace)](https://huggingface.co/ctheodoris/Geneformer) — Apache-2.0
- [UCE](https://github.com/snap-stanford/uce) — MIT
- [scFoundation](https://github.com/biomap-research/scFoundation) — Apache-2.0
- [UNI / UNI2-h (HuggingFace)](https://huggingface.co/MahmoodLab/UNI) — CC-BY-NC, gated
- [Virchow (HuggingFace)](https://huggingface.co/paige-ai/Virchow) — CC-BY-NC
- [Hibou (HuggingFace)](https://huggingface.co/histai/hibou-b) — Apache-2.0
- [Evo2](https://github.com/ArcInstitute/evo2) — Apache-2.0
- [ESM-3 (1.4B)](https://github.com/evolutionaryscale/esm) — Cambrian Non-Commercial

**Code / benchmarks**:
- [PerturBench](https://github.com/altoslabs/perturbench) — single-cell perturbation benchmark
- [scPerturBench](https://github.com/bm2-lab/scPerturBench) — adversarial split benchmark
- [Open Problems](https://github.com/openproblems-bio/openproblems) — community benchmark hub

### 11.3 Recommended reading (~110 references, one-sentence framings)

The bibliography is organized into 12 buckets. Bold = read first. URLs are direct (DOI / arXiv / Nature / GitHub). For 2026 preprints not yet in journals, the bioRxiv/arXiv link is canonical.

#### Position papers — start here

- **Bunne, Roohani, Rosen, et al. 2024 *Cell* — ["How to build the virtual cell with artificial intelligence: Priorities and opportunities"](https://www.cell.com/cell/fulltext/S0092-8674(24)01332-1)** — the canonical virtual-cell thesis. Defines what would constitute a working virtual cell, and the technical milestones along the way.
- **Rood, Hupalowska, Regev 2024 *Cell* — ["The future of rapid and automated single-cell data analysis using reference mapping"](https://doi.org/10.1016/j.cell.2024.07.030)** — Aviv Regev's framing of where single-cell FMs need to mature.
- Lähnemann et al. 2020 *Genome Biology* — "Eleven grand challenges in single-cell data science" — the pre-FM landscape; still the cleanest gap statement.
- Marx 2024 *Nat Methods* tech feature — "AI builds models of biology" — accessible field overview.

#### The 2025 critique trio — the reckoning

- **[Ahlmann-Eltze & Huber 2025 *Nature Methods* 22:1657–1661](https://www.nature.com/articles/s41592-025-02772-6)** — "Deep-learning-based predictions of gene expression do not generalize." The paper that broke the single-cell FM narrative; linear baselines beat scGPT / Geneformer / UCE / scFoundation on Norman, Replogle, and Jurkat perturbation tasks.
- **[Kedzierska et al. 2025 *Genome Biology* 26:101](https://doi.org/10.1186/s13059-025-03517-6)** — "Assessing the limits of zero-shot foundation models in single-cell biology." Cross-FM zero-shot benchmark; arrives at the same conclusion via a different path.
- Wenkel et al. 2025 — proposes the `latent-additive` baseline that should be reported alongside any sc-FM perturbation claim.
- [Csendes, Lugo-Martinez et al. 2024 *OpenReview/bioRxiv*](https://www.biorxiv.org/content/10.1101/2024.09.30.615579) — independent scGPT replication; finds the original train/test split was leaky.
- Boiarsky et al. 2023 *NeurIPS Workshop on Generative AI and Biology* — earliest published "linear baselines are competitive" warning; predates the 2025 trio by 18 months.

#### Single-cell FM technical papers

- **Cui et al. 2024 *Nat Methods* — ["scGPT: toward building a foundation model for single-cell multi-omics using generative AI"](https://doi.org/10.1038/s41592-024-02201-0)** — masked-gene-language modeling on 33M cells; defined the field shape.
- **Theodoris et al. 2023 *Nature* 618:616–624 — ["Transfer learning enables predictions in network biology"](https://doi.org/10.1038/s41586-023-06139-9)** — Geneformer; the field's first atlas-pretrained transformer.
- [Geneformer-V2 HuggingFace model card (Theodoris lab, Dec 2024)](https://huggingface.co/ctheodoris/Geneformer) — V2-104M with cancer-curated `_CLcancer` continual-pretraining variant; domain curation matches the 316M general-domain model at ⅓ the parameters.
- Rosen, Brbić et al. 2024 *bioRxiv* — [UCE (Universal Cell Embedding)](https://www.biorxiv.org/content/10.1101/2023.11.28.568918v2) — cross-species single-cell embedding via shared protein-language tokens.
- Hao et al. 2024 *Nat Methods* — [scFoundation](https://doi.org/10.1038/s41592-024-02305-7) — 100M-param read-depth-aware pretraining on 50M cells.
- Yang et al. 2022 *Nat Mach Intell* — [scBERT](https://doi.org/10.1038/s42256-022-00534-z) — the BERT-for-single-cell prequel to scGPT.
- Wen et al. 2024 *ICLR* — [CellPLM](https://openreview.net/forum?id=BKXvPDekud) — pretraining at the cell-as-token (not gene-as-token) granularity.
- Fu et al. 2024 *Nat Methods* — [GET (General Expression Transformer)](https://www.nature.com/articles/s41592-024-02380-w) — cross-cell-type transcription-factor activity prediction.
- Xie et al. 2024 *Cell Research* — [GeneCompass](https://doi.org/10.1038/s41422-024-01034-y) — human + mouse co-pretraining (126M cells).
- Wu et al. 2024 *Cell Systems* — [STATE](https://www.cell.com/cell-systems/abstract/S2405-4712(24)00261-1) — Arc Institute's perturbation-aware single-cell FM.
- Roohani, Lewis-Pannell, Hsu et al. 2025 *bioRxiv* — [Tahoe-100M](https://arcinstitute.org/news/virtual-cell-model-state) — 100M cells × 1,100 drugs × 50 cell lines.
- Cui et al. 2024 *Nat Methods* — scGPT-spatial extension.
- Tang, Pelka et al. 2024 *Nat Biotechnol* — scTab: large-scale cell-type classification benchmark from CELLxGENE.
- Chen et al. 2024 *Nat Biotechnol* — [SCimilarity](https://www.nature.com/articles/s41587-024-02411-z) — embedding-based cell-state search across 23M cells.
- Lopez, Regier et al. 2018 *Nat Methods* — scVI; the variational-inference predecessor to all single-cell FMs.

#### Pathology FM technical papers

- **Chen et al. 2024 *Nat Medicine* — ["Towards a general-purpose foundation model for computational pathology"](https://doi.org/10.1038/s41591-024-02857-3)** — UNI; DINOv2 pretraining on 100M tiles from 100k slides.
- **Vorontsov et al. 2024 *Nat Medicine* — Virchow** — Paige's 632M-param pathology FM on 1.5M slides.
- Zimmermann et al. 2024 *arXiv* — [Virchow2 / Virchow2G](https://arxiv.org/abs/2408.00738) — scale-up with 3.1M slides, including 1.85B-param Virchow2G.
- **Wang et al. 2024 *Nature* 634:970–978 — [CHIEF](https://doi.org/10.1038/s41586-024-07894-z)** — Mahmood-lab pathology FM with cancer-type prediction across 19 tumor types.
- Xu et al. 2024 *Nature* 630:181–188 — [Prov-GigaPath](https://www.nature.com/articles/s41586-024-07441-w) — Microsoft + Providence; slide-level transformer over 171k WSIs.
- Lu et al. 2024 *Nat Medicine* — [CONCH](https://www.nature.com/articles/s41591-024-02856-4) — vision-language pathology FM trained on 1.17M image-caption pairs.
- Lu et al. 2024 *Nature* — [PathChat](https://www.nature.com/articles/s41586-024-07618-3) — multimodal conversational pathology model; FDA Breakthrough Device Designation (Jan 2025).
- Nechaev et al. 2024 *arXiv* — [Hibou-L / Hibou-B](https://arxiv.org/abs/2406.05074) — HistAI's permissively-licensed pathology FM; the only Apache-2.0 top-tier option.
- Filiot et al. 2023 *bioRxiv* — [Phikon](https://www.biorxiv.org/content/10.1101/2023.07.21.549993) — Owkin's DINOv2-pathology pretraining (predecessor to Phikon-v2).
- Filiot et al. 2024 *bioRxiv* — Phikon-v2 — scaled to ViT-L/14 with 460M params on 56k WSIs.
- [Campanella et al. 2025 *Nat Communications*](https://www.nature.com/articles/s41467-025-58245-z) — head-to-head clinical-grade benchmark across UNI / Virchow / Virchow2 / Prov-GigaPath / CHIEF.
- Saillard et al. 2024 *Nat Medicine* — [H-Optimus-0](https://www.nature.com/articles/s41591-024-03281-3) — Bioptimus' 1.1B-param pathology FM.
- Jaume et al. 2024 *bioRxiv* — [HEST-1k](https://github.com/mahmoodlab/HEST) — first large-scale spatial-pathology benchmark linking H&E to spatial transcriptomics.
- Ding et al. 2024 *Nat Medicine* — clinical-grade WSI tile-classification benchmark methodology.

#### Genomic / DNA FM technical papers

- **Dalla-Torre et al. 2025 *Nat Methods* — [Nucleotide Transformer](https://doi.org/10.1038/s41592-024-02523-z)** — InstaDeep / NVIDIA 2.5B-param DNA FM benchmarked on 18 regulatory tasks.
- Zhou et al. 2024 *ICLR* — [DNABERT-2](https://openreview.net/forum?id=oMLQB4EZE1) — BPE-tokenization makes DNABERT competitive with NT at ~5× smaller scale.
- Ji et al. 2021 *Bioinformatics* — [DNABERT](https://doi.org/10.1093/bioinformatics/btab083) — the original BERT-for-DNA.
- Nguyen et al. 2023 *NeurIPS* — [HyenaDNA](https://proceedings.neurips.cc/paper_files/paper/2023/hash/86ab6927ee4ae9bde4247793c46797c7-Abstract-Conference.html) — Hyena state-space replaces attention; enables 1M-bp single-nucleotide context.
- **Nguyen et al. 2024 *Science* — [Evo (v1)](https://www.science.org/doi/10.1126/science.ado9336)** — 7B-param DNA FM from Arc Institute; 131kb context, generative.
- **Brixi et al. 2025 *bioRxiv* — [Evo 2](https://www.biorxiv.org/content/10.1101/2025.02.18.638918)** — 40B-param successor, 1M-bp context, trained on 9.3T DNA tokens; 2,048× H100 (the most expensive disclosed biology FM training run).
- **[Avsec et al. 2025 *Nature* — AlphaGenome](https://doi.org/10.1038/s41586-025-10014-0)** — "Advancing regulatory variant effect prediction with AlphaGenome." DeepMind's regulatory-track-prediction FM; wins 25/26 variant-effect benchmarks.
- Avsec et al. 2021 *Nat Methods* — [Enformer](https://doi.org/10.1038/s41592-021-01252-x) — attention-based DNA-to-track predictor; AlphaGenome's spiritual predecessor.
- Benegas, Batra, Song 2023 *bioRxiv* — [GPN-MSA](https://www.biorxiv.org/content/10.1101/2023.10.10.561776) — multi-species DNA FM (cross-species transfer baseline).
- Schiff et al. 2024 *ICML* — [Caduceus](https://openreview.net/forum?id=8c5BvLBHgD) — RC-equivariant DNA FM (treats reverse-complement symmetry as architectural).
- Eraslan et al. 2019 *Nat Rev Genet* — pre-FM deep-learning-for-genomics review (still the cleanest framing).
- Frazer et al. 2021 *Nature* — EVE; pathogenicity prediction from protein-MSA evolution.

#### Protein FM technical papers

- **Hayes et al. 2025 *Science* — [ESM-3](https://www.science.org/doi/10.1126/science.ads0018)** — EvolutionaryScale 98B-param multimodal protein FM; generated esmGFP at 36% identity to avGFP.
- **Lin et al. 2023 *Science* — [ESM-2 / ESMFold](https://www.science.org/doi/10.1126/science.ade2574)** — Meta's 15B-param protein FM; structure prediction without MSAs.
- **Abramson et al. 2024 *Nature* — [AlphaFold 3](https://doi.org/10.1038/s41586-024-07487-w)** — multimodal structure prediction (proteins + DNA + RNA + ligands).
- Jumper et al. 2021 *Nature* — [AlphaFold 2](https://doi.org/10.1038/s41586-021-03819-2) — the 2020 CASP14 paper that started everything.
- Watson et al. 2023 *Nature* — [RFdiffusion](https://doi.org/10.1038/s41586-023-06415-8) — protein-backbone diffusion design.
- Bennett et al. 2024 *Nature* — [RFdiffusion All-Atom](https://www.nature.com/articles/s41586-024-07159-9) — extends RFdiffusion to ligand-aware design.
- Madani et al. 2023 *Nat Biotechnol* — [ProGen2](https://doi.org/10.1038/s41587-022-01618-2) — autoregressive protein-language generation.
- Ferruz et al. 2022 *Nat Communications* — [ProtGPT2](https://doi.org/10.1038/s41467-022-32007-7) — GPT-2 protein sequence generation; predates ProGen2.
- Notin et al. 2023 *NeurIPS* — [ProteinGym](https://proceedings.neurips.cc/paper_files/paper/2023/hash/cac723e5ff29f65e3fcbb0739ae91bee-Abstract-Datasets_and_Benchmarks.html) — the standard benchmark for protein fitness prediction.
- Cheng et al. 2023 *Science* — [AlphaMissense](https://www.science.org/doi/10.1126/science.adg7492) — variant-effect prediction.
- Watson, Juergens et al. 2024 *bioRxiv* — Proteina Complexa — de novo atomistic-binder design; 63.5% PDGFR wet-lab hit rate.
- Krishna et al. 2024 *Science* — RoseTTAFold All-Atom — Baker-lab multimodal structure prediction.

#### Multimodal / general-bio FMs

- Zhang et al. 2024 *NEJM AI* — [BiomedCLIP](https://ai.nejm.org/doi/full/10.1056/AIoa2400640) — vision-language pretraining on 15M biomed image-caption pairs.
- Singhal et al. 2023 *Nature* — [Med-PaLM](https://doi.org/10.1038/s41586-023-06291-2) — "Large language models encode clinical knowledge"; expert-level MedQA.
- Tu et al. 2024 *arXiv* — [Med-Gemini](https://arxiv.org/abs/2404.18416) — Google's multimodal medical FM.
- Moor et al. 2023 *PMLR* — [Med-Flamingo](https://proceedings.mlr.press/v225/moor23a/moor23a.pdf) — few-shot medical visual question answering.
- Saab et al. 2024 *arXiv* — ["Capabilities of Gemini Models in Medicine"](https://arxiv.org/abs/2407.02485) — Med-Gemini clinical-task follow-up.
- Huang et al. (Zitnik lab) 2024 *Nat Medicine* — [TxGNN](https://www.nature.com/articles/s41591-024-03233-x) — "A foundation model for clinician-centered drug repurposing"; zero-shot drug-disease graph FM (Harvard).
- Shen et al. 2023 *iScience* — [tGPT](https://www.cell.com/iscience/fulltext/S2589-0042(23)02403-X) — "Generative pretraining from large-scale transcriptomes for single-cell deciphering."

#### Virtual cell-specific work

- **Bunne et al. 2024 *Cell* — virtual cell perspective** (cited above; the field's defining paper).
- **CZ Biohub Virtual Cell Program** — [program page](https://chanzuckerberg.com/science/programs-resources/virtual-cells-initiative/) (Dec 2024 announcement).
- **Roohani, Hsu et al. 2025 *bioRxiv* — Tahoe-100M paper** — first large-scale perturbation atlas explicitly framed as virtual-cell training data.
- Arc Institute 2025 — [Virtual Cell Atlas + STATE model](https://arcinstitute.org/manuscripts/state) launch.
- [CZ Biohub Virtual Cell Challenge 2025](https://virtualcellchallenge.org/) — first community benchmark with $50k prize purse.
- Lotfollahi et al. 2023 *Nat Cell Biol* — CPA (Compositional Perturbation Autoencoder); pre-FM virtual-cell prototype.
- Roohani et al. 2024 *Nat Biotechnol* — [GEARS](https://www.nature.com/articles/s41587-023-01905-6) — graph-based perturbation-response prediction; the linear-baseline-beater for pre-FM models.

#### Benchmarks & datasets

- Replogle et al. 2022 *Cell* — [Whole-genome Perturb-seq](https://doi.org/10.1016/j.cell.2022.05.013) — K562 + RPE1 essentialome; the canonical perturbation gold standard.
- Norman et al. 2019 *Science* — combinatorial Perturb-seq; the standard FM eval split.
- Frangieh et al. 2021 *Nat Genet* — CRISPRi Perturb-seq in melanoma immune-evasion context.
- Open Problems v2 — [openproblems.bio](https://openproblems.bio) — community single-cell benchmark with held-out perturbations and donors.
- [PerturBench](https://github.com/altoslabs/perturbench) — Altos Labs' perturbation-prediction benchmark; the standard scoring harness post-Ahlmann-Eltze.
- [scPerturBench](https://github.com/genentech/scperturbench) — Genentech's complementary benchmark.
- Tabula Sapiens Consortium 2022 *Science* — multi-organ human reference atlas (483k cells).
- [CELLxGENE Census](https://chanzuckerberg.github.io/cellxgene-census/) — CZI's federated 95M-cell index; the dominant pretraining substrate.
- HuBMAP 2023 *Nature* — Human BioMolecular Atlas Program; the major non-CELLxGENE atlas.
- [Polaris Hub](https://polarishub.io) — Valence Labs' drug-discovery FM benchmarking platform.
- [TDC-2 (Therapeutics Data Commons)](https://tdcommons.ai) — Harvard's multi-task therapeutics benchmark.
- [HEST-1k](https://github.com/mahmoodlab/HEST) — pathology + spatial-transcriptomics paired benchmark.
- CASP15 / CAPRI — community protein-structure benchmarks (run biennially).

#### Compute / cost methodology

- [Cottier, Rahman et al. 2024 *arXiv*](https://arxiv.org/abs/2405.21015) — "The Rising Costs of Training Frontier AI Models"; the methodology this corpus follows.
- [Epoch AI training-compute methodology](https://epoch.ai/blog/estimating-training-compute) — the `FLOPs ≈ 6 × parameters × tokens` heuristic.
- [Hoffmann et al. 2022 *arXiv* — Chinchilla scaling laws](https://arxiv.org/abs/2203.15556) — the optimal-compute paper everyone cites for FLOPs estimation.
- [NVIDIA Evo 2 announcement (Feb 2025)](https://blogs.nvidia.com/blog/evo-2-biomolecular-ai/) — discloses 2,048× H100; ratio to AlphaFold and ESM-3.
- [Retraction Watch on AlphaFold 3 disclosure](https://retractionwatch.com/2024/05/14/nature-earns-ire-over-lack-of-code-availability-for-google-deepmind-protein-folding-paper/) — the controversy that pressured DeepMind into Jan 2026 source-code release.
- Strubell, Ganesh, McCallum 2019 *ACL* — "Energy and Policy Considerations for Deep Learning in NLP" — first widely-cited compute-disclosure call.

#### Field context & adjacent

- Regev et al. 2017 *eLife* — [Human Cell Atlas](https://elifesciences.org/articles/27041) — the atlas that made FMs possible.
- Tabula Muris 2018 *Nature* — mouse parallel; the OG cross-tissue single-cell reference.
- Stuart, Butler et al. 2019 *Cell* — Seurat v3; the canonical pre-FM single-cell pipeline.
- Wolf, Angerer, Theis 2018 *Genome Biology* — Scanpy; Python equivalent.
- Han et al. 2020 *Nature* — Mouse Cell Atlas (333,778 cells).
- Eraslan, Theis et al. 2019 *Nat Commun* — scGen; representation-learning perturbation prediction (pre-FM).
- Lopez et al. 2018 *Nat Methods* — scVI; the VI foundation.
- Lopez et al. 2022 *Nat Methods* — DestVI; spatial deconvolution.
- Korsunsky, Raychaudhuri 2019 *Nat Methods* — Harmony; pre-FM batch correction baseline still used.
- Andrews & Hemberg 2019 *F1000Research* — single-cell QC + dimensionality-reduction methodology.
- Crawford et al. 2024 *Cell* — clonal evolution + single-cell phylogenetics in cancer.

#### Reviews & meta-analyses (good single reads)

- Marx 2024 *Nat Methods* tech feature — "AI builds models of biology" — accessible overview.
- Sahu et al. 2024 *Nat Rev Genet* — "Discovering therapeutic targets from foundation models" — pharma-side FM review.
- Eraslan, Avsec et al. 2019 *Nat Rev Genet* — pre-FM deep-learning-for-genomics review (still the cleanest framing).

#### Industry / strategy / clinical context

- [PathAI 2025 Series E announcement](https://www.pathai.com/news) — pathology AI commercialization signal.
- [Paige.AI FullFocus FDA 510(k) clearance (Jan 2025)](https://paige.ai/news) — first general-purpose pathology AI cleared by FDA.
- [Owkin MOSAIC platform](https://owkin.com) — multimodal cancer FM productization.
- [Tempus AI S-1 filing (2024)](https://www.sec.gov) — multimodal cancer data + FM productization at scale (revenue / loss disclosure).
- [Recursion Pharmaceuticals R&D updates](https://www.recursion.com) — Phenom-Beta pathology + cell painting FM platform.
- [Insitro pipeline](https://insitro.com) — Daphne Koller's FM-for-drug-discovery company; the cleanest applied virtual-cell case study.
- [Latent Labs](https://latentlabs.com) — Simon Kohl + DeepMind alumni virtual-cell startup (founded 2024).
- Sukumaran et al. 2025 *JCO Precision Oncology* — clinical-decision-support evaluation framework for FMs in oncology.

#### Cross-vault index

The full corpus this page draws from: [Foundation Models](../foundation-models.md) — cross-vault FM index with per-tool dossiers and inline citations. Specific anchors for the AACR-case-study close:

- [AACR 2026 Virtual Cells topic](../conferences/aacr-2026/topics/virtual-cells/index.md) — 1 native session, 5 symlinked overlaps, 48 posters.
- [AACR 2026 Agentic AI topic](../conferences/aacr-2026/topics/agentic-ai/index.md) — 5 sessions covering AT02, "Agentic AI as the Oncologist," and Bo Wang's keynote.
- [AACR 2026 Bioinfo/AI methods topic](../conferences/aacr-2026/topics/bioinfo-tools/index.md) — 12 sessions, 536 posters; the methods undergrowth.
- [ICLR 2026 tools](../conferences/iclr-2026/index.md) — sc-Arena, sc-FM PertAdapt, MedAgentGym, Proteina Complexa, Evo2 follow-ups.
- [ISBI 2026 pathology FM keynote](../conferences/isbi-2026/tools/mahmood-pathology-fm-keynote.md) — Mahmood's three-tier FM stack talk.
- [JPM 2026 themes](../conferences/jpm-2026/themes.md) — the year's financial framing of FM-in-biology.

### 11.4 Backup resources — extended reading list

A field-survey-grade list of people, venues, benchmarks, datasets, talks, critique papers, and communities to follow up on after the talk. Verified to working state as of 2026-05-12. Where a URL is uncertain it is flagged *URL unverified*.

#### Institutes & labs — extended dossiers

§3.11 compressed this into one table; the entries below are the speaker's prep depth. Each one names the institute, its key PIs, what it has shipped 2023–2026, and — where relevant — how to read its disclosure norms.

- **[Arc Institute](https://arcinstitute.org/)** — Palo Alto-based non-profit (founded 2021). Hosts the [Hsu Lab](https://arcinstitute.org/labs/hsulab) (Patrick Hsu) and the [Goodarzi Lab](https://arcinstitute.org/labs/goodarzilab) (Hani Goodarzi). Shipped: Evo (*Science* 2024), Evo2 (*Nature* 2026 with NVIDIA), STATE (bioRxiv 2025), [Tahoe-100M](https://www.tahoe.ai) (with Vevo Therapeutics, Feb 2025). **Disclosure norm**: foregrounds data scale ("100M cells × 1,100 drugs"); buries compute except where NVIDIA is a co-author. Strategic move 2025: launched the "Virtual Cell Atlas" branding and co-sponsored the $50k [Virtual Cell Challenge](https://virtualcellchallenge.org/) with CZ Biohub.

- **[Mahmood Lab](https://faisal.ai/)** (Harvard / Brigham & Women's / Mass General Brigham) — PI Faisal Mahmood. Ships a *fleet* rather than a single FM: UNI / UNI2-h (encoder, *Nat Med* 2024), CONCH (vision-language), PathChat / PathChat-DX (chat-style pathology), TITAN (slide-level aggregator), CHIEF (cancer-type prediction, *Nature* 2024), [HEST-1k](https://github.com/mahmoodlab/HEST) (paired H&E + Visium benchmark). **Disclosure norm**: opaque on compute ("extensive A100 hours"); HuggingFace gating tightened Jan 2025 to institutional-email verification. Strategic move 2025: PathChat-DX FDA Breakthrough Designation — first generative-AI pathology tool to receive one. AACR 2026: [ISBI 2026 keynote](../conferences/isbi-2026/tools/mahmood-pathology-fm-keynote.md) on the three-tier FM stack.

- **[Theodoris Lab](https://www.theodorislab.gladstone.org/)** (Gladstone Institutes / UCSF) — PI Christina Theodoris. Shipped: Geneformer V1 (*Nature* 2023), [Geneformer V2-104M / V2-316M / V2-104M_CLcancer](https://huggingface.co/ctheodoris/Geneformer) (Dec 2024 update). **Disclosure norm**: the only academic sc-FM lab with full compute disclosure via [NVIDIA BioNeMo](https://github.com/NVIDIA/bionemo-framework) (64× A100 80GB × 4d 8h = 6,656 A100-hours for V2-104M = ~$17k on-demand). This makes Geneformer V2 the **only reproducible academic sc-FM training run**. Strategic move: domain curation (`_CLcancer`) matched the 316M general-domain model at ⅓ the parameters — the cleanest evidence in the field that *data curation ≫ scale*.

- **[Bo Wang Lab](https://wanglab.ai/)** (U. Toronto / Vector Institute / UHN) — PI Bo Wang (Canada CIFAR AI Chair; Chief AI Scientist at UHN). Ships: scGPT (*Nat Methods* 2024), scGPT-spatial, MedSAM, BulkRNABERT. **Disclosure norm**: opaque on scGPT training compute (a 50× uncertainty band — see §3.1). Strategic move 2025: explicit agentic-AI pivot — Wang's [AACR 2026 talk in the AI Revolution session](../conferences/aacr-2026/sessions/2026-04-20-am-ai-revolution-in-cancer-research.md) is framed around clinical agents, not FM training. The lab has the broadest range of any sc-FM PI: foundation models, segmentation, agents.

- **Leskovec + Quake** (Stanford / [SNAP](https://snap.stanford.edu/) · [Quake Lab](https://quakelab.stanford.edu/)) — Jure Leskovec (CS, SNAP, [CRFM](https://crfm.stanford.edu/) affiliate) + Steve Quake (Bioengineering, ex-CZ Biohub President). Shipped: [UCE](https://github.com/snap-stanford/uce) (Universal Cell Embedding, *Nat Methods* 2024), CRADLE-VAE, scGenePT. **Disclosure norm**: UCE neither the preprint nor the *Nat Methods* version discloses training compute — the least transparent of the major sc-FMs. Strategic move: cross-species pretraining via protein-sequence (ESM2) embeddings — the first sc-FM with a serious cross-species story.

- **[Google DeepMind](https://deepmind.google/)** — life-sciences team under Pushmeet Kohli + Demis Hassabis. Shipped: AlphaFold 2 (2021), AlphaFold 3 (*Nature* 2024), [AlphaGenome](https://doi.org/10.1038/s41586-025-10014-0) (*Nature* 2025), Med-PaLM / Med-Gemini. **Disclosure norm**: discloses architecture and benchmarks; rarely discloses full compute. Closed weights + free hosted API for non-commercial use. The [AlphaFold 3 source-code controversy](https://retractionwatch.com/2024/05/14/nature-earns-ire-over-lack-of-code-availability-for-google-deepmind-protein-folding-paper/) (May 2024) pressured the team into Jan 2026 AlphaGenome source-code release. Strategic move 2026: Isomorphic Labs as the commercial arm; the [Lilly + NVIDIA + Isomorphic](../conferences/jpm-2026/themes.md) triangle was the dominant pharma-AI signal at JPM 2026.

- **[EvolutionaryScale](https://www.evolutionaryscale.ai/)** — founded 2024 by the ex-Meta FAIR protein team (Alex Rives, Tom Sercu, Thomas Hayes, others) after Meta wound down the FAIR protein effort. Shipped: ESM-3 (1.4B / 7B / 98B, *Science* 2025). **Disclosure norm**: the cleanest compute disclosure in biology FM — publishes training FLOPs as a single 10²⁴ number. License-tiered: 1.4B Cambrian Non-Commercial; 7B / 98B Forge-API gated. Strategic move: positions ESM-3 as the "frontier compute" reference point — Evo2 explicitly benchmarks itself at "~2× ESM-3 FLOPs."

- **[Paige.AI](https://paige.ai/) + MSK** — commercial spinout of MSK pathology AI (founded 2018) + [Memorial Sloan Kettering](https://www.mskcc.org/) computational pathology (Thomas Fuchs lab). Shipped: Virchow ([arXiv 2408.00738](https://arxiv.org/abs/2408.00738)), Virchow2, Virchow2G, [FullFocus FDA 510(k) cleared Jan 2025](https://paige.ai/news). Compute lead Eric Zimmermann (V2) + Eugene Vorontsov (V1). **Disclosure norm**: clean compute disclosure (512× V100 32GB; ~1.4 × 10⁵ V100-hours = ~$170k). License: CC-BY-NC for academic; commercial use requires Paige license. Strategic move 2025: FullFocus FDA clearance reset the regulatory bar for general-purpose pathology AI.

- **[Owkin](https://owkin.com/)** — Paris/NYC hybrid biotech (founded 2016, ~$300M Series C 2024). Shipped: Phikon (bioRxiv 2023), Phikon-v2 (2024), H-optimus-0 (1.1B-param pathology FM, July 2024), MOSAIC (multimodal cancer platform). **Disclosure norm**: federated-learning-first (training data stays at partner hospitals); weights MIT / Apache-2.0. The **only major industrial pathology player shipping open weights**. AACR 2026: H-optimus-0 used in poster #1444 (Lauren-subtype gastric classification) — see §6.7.

- **[NVIDIA BioNeMo](https://github.com/NVIDIA/bionemo-framework)** — infrastructure team within NVIDIA Healthcare. Not an FM builder per se, but the only public reproduction recipe for Geneformer V2 training, and the silent compute co-author behind Evo2, the [Lilly + NVIDIA $1B AI Co-Innovation Lab (JPM 2026)](../conferences/jpm-2026/themes.md), and most of the 2024–2026 academic-industrial pharma announcements. **Disclosure norm**: treats compute disclosure as a co-marketing artifact. If a paper discloses NVIDIA hardware in detail, NVIDIA is a co-author or framework partner.

- **[CZ Biohub + CZI](https://chanzuckerberg.com/science/programs-resources/virtual-cells-initiative/)** — Chan Zuckerberg Initiative (funder) + the CZ Biohub network (SF / Chicago / NY). [Theofanis Karaletsos](https://tech.chanzuckerberg.com/ai-powering-biomedical-science/) heads AI for Science; Steve Quake was ex-Head of Biohub SF; Angela Pisco leads single-cell. Funds + ships: CELLxGENE Census (the canonical sc-FM training corpus), Tabula Sapiens, [the Virtual Cell Platform](https://virtualcellmodels.cziscience.com/), rBio. **Strategic posture**: not a model lab — a *substrate* lab. The bet is that whoever builds the best data + benchmark substrate captures the field regardless of who trains the biggest model.

- **[Ahlmann-Eltze](https://const-ae.name/) + [Huber Group](https://www.huber.embl.de/)** (EMBL Heidelberg) — Constantin Ahlmann-Eltze (now Isomorphic Labs) + Wolfgang Huber. Authored the [2025 *Nat Methods* linear-baseline paper](https://www.nature.com/articles/s41592-025-02772-6) that retired the sc-FM perturbation leaderboard. Huber lab is the elder Bioconductor-statistics group; **Ahlmann-Eltze's transition from EMBL to Isomorphic Labs is itself a market signal** — the most influential FM critic was hired by Alphabet's biology arm during the same six months DeepMind released AlphaGenome.

- **[Theis Lab](https://www.helmholtz-munich.de/en/icb/pi/fabian-theis)** (Helmholtz Munich) — PI Fabian Theis. Long-running single-cell methods group; built [scvi-tools](https://scvi-tools.org/), scArches, and the framework vocabulary every sc-FM paper inherits (latent representations, integration metrics, perturbation prediction). Did not ship its own sc-FM, but Hetzel et al. 2024 (compositional pretraining > scale) and the Lotfollahi causal-representation line are direct outputs. **The methodological reference class for the entire field.**

- **[Zitnik Lab](https://zitniklab.hms.harvard.edu/)** (Harvard Medical School) — PI Marinka Zitnik. Ships [TxGNN](https://www.nature.com/articles/s41591-024-03233-x) (*Nat Med* 2024) and [TDC / TDC-2](https://tdcommons.ai/) (Therapeutics Data Commons benchmark). **Strategic posture**: graph-FM-for-clinic — the natural bridge between sc-FMs (gene-level) and agentic-clinical-AI (patient-level). If you want to extend a virtual cell to a virtual patient, this is the methodology reference.

- **[Aviv Regev @ Genentech](https://www.gene.com/scientists/our-scientists/aviv-regev)** — Head of gRED (Genentech Research & Early Development) since 2020, after the Broad. Not shipping FMs as a PI, but **the agenda-setter for "causal foundation models of cells"** — the framing comes from her 2024 *Cell* review with Rood + Hupalowska. Genentech under Regev is the largest pharma buyer for academic sc-FM tools.

#### People to follow

- **Christina Theodoris** (Gladstone / UCSF) — creator of Geneformer; cardiovascular gene-network ML. [Lab page](https://www.theodorislab.gladstone.org/) · [Gladstone bio](https://gladstone.org/people/christina-theodoris).
- **Bo Wang** (U. Toronto / Vector Institute / UHN) — scGPT PI; Canada CIFAR AI Chair, Chief AI Scientist at UHN. [WangLab](https://wanglab.ai/) · [X @BoWang87](https://x.com/bowang87).
- **Mohammad Lotfollahi** (Wellcome Sanger / Open Targets) — scArches, scPoli, multimodal cell perturbation generative models. [Lotfollahi lab site](https://lotfollahi.com/research/).
- **Aviv Regev** (Genentech, ex-Broad) — Head of gRED, Human Cell Atlas co-founder; the "causal foundation model of cells" agenda. [Genentech bio](https://www.gene.com/scientists/our-scientists/aviv-regev).
- **Patrick Hsu** (Arc Institute / Stanford / UC Berkeley) — Evo2 + STATE virtual cell co-PI; CRISPR-Cas13 originator. [Hsu Lab @ Arc](https://arcinstitute.org/labs/hsulab) · [patrickhsu.com](https://patrickhsu.com/).
- **Faisal Mahmood** (Harvard / BWH / MGB) — UNI, CONCH, PathChat, TITAN pathology FM stack. [faisal.ai](https://faisal.ai/).
- **Jure Leskovec** (Stanford / SNAP) — UCE co-PI; GNNs for biology; CRFM affiliate. [cs.stanford.edu/~jure](https://cs.stanford.edu/people/jure/) · [SNAP](https://snap.stanford.edu/).
- **Sara Mostafavi** (UW Allen School) — deep-learning models of differential gene expression; co-founder MLCB. [Mostafavi Lab](http://saramostafavi.github.io/).
- **Constantin Ahlmann-Eltze** (Isomorphic Labs, ex-Huber/EMBL) — first author of the 2025 *Nat Methods* linear-baseline reckoning. [const-ae.name](https://const-ae.name/).
- **Wolfgang Huber** (EMBL Heidelberg) — Bioconductor + statistics-of-genomics elder; senior author on the 2025 reckoning. [Huber Group @ EMBL](https://www.huber.embl.de/).
- **Theofanis Karaletsos** (CZI, Head of AI for Science) — runs CZI's virtual-cell program + rBio. [CZI tech blog](https://tech.chanzuckerberg.com/ai-powering-biomedical-science/).
- **Kasia Z. Kedzierska** (Oxford / Microsoft Research) — first author on the zero-shot single-cell FM critique. [Google Scholar](https://scholar.google.com/citations?user=lvJpQGUAAAAJ).
- **Hani Goodarzi** (Arc Institute / UCSF) — STATE co-lead; RNA biology + ML. [Goodarzi Lab @ Arc](https://arcinstitute.org/labs/goodarzilab).
- **Stephan Sanders / Smita Krishnaswamy / Lior Pachter** — auxiliary voices in the eval-honesty conversation; Pachter's [blog](https://liorpachter.wordpress.com/) is a long-running antidote to hype.

#### Newsletters / blogs / podcasts

- **Owl Posting** — Abhishaike Mahajan's biology + ML essays (Noetik); deep weekly tear-downs of FM startups. [owlposting.com](https://www.owlposting.com/).
- **Decoding Bio** — weekly BioByte digest of biotech + AI papers, funding, and ideas. [decodingbio.substack.com](https://decodingbio.substack.com/).
- **Asimov Press** — long-form bio writing (Mukherjee, Wilke, etc.); confirms reckoning-style narratives. [press.asimov.com](https://press.asimov.com/).
- **CZ Biohub Data Science blog** — Tabula, CELLxGENE, and virtual-cell engineering notes from the source. [ds.czbiohub.org/blog](https://ds.czbiohub.org/blog/).
- **Arc Institute News** — primary venue for STATE, Evo2, Virtual Cell Atlas releases. [arcinstitute.org/news](https://arcinstitute.org/news).
- **M2D2 — Molecular Modelling & Drug Discovery** (Valence + Mila) — weekly reading group + podcast covering ML-for-drug-discovery papers. [portal.valencelabs.com/m2d2](https://portal.valencelabs.com/m2d2) · [Substack](https://m2d2.substack.com/).
- **The Gradient** — ML-for-science long-form pieces with healthy skepticism. [thegradient.pub](https://thegradient.pub/).
- **Latent Space** — Swyx & Alessio's ML podcast; occasionally hosts bio-FM founders (Arc, EvolutionaryScale). [latent.space](https://www.latent.space/).
- **Eric Topol's Substack** — clinician-investigator coverage of biomedical AI; useful counterpoint when judging clinical-deployment claims. [erictopol.substack.com](https://erictopol.substack.com/).
- **PreLights** (Company of Biologists) — community preprint commentary; the Ahlmann-Eltze paper got a useful PreLights write-up. [prelights.biologists.com](https://prelights.biologists.com/).

#### Live benchmarks / leaderboards

- **Open Problems for Single Cell v2** — community benchmark hub; perturbation-prediction, label-projection, batch-integration tasks. [openproblems.bio](https://openproblems.bio).
- **PerturBench** (Altos Labs) — single-cell perturbation benchmark; the framework that flagged mode collapse + rank-metric importance. [github.com/altoslabs/perturbench](https://github.com/altoslabs/perturbench).
- **scPerturBench** (BM2-Lab) — generalization-stressed perturbation benchmark with adversarial splits. [bm2-lab.github.io/scPerturBench-reproducibility](https://bm2-lab.github.io/scPerturBench-reproducibility/).
- **CZI Virtual Cells Platform Benchmarks** — community-driven cell-model benchmarks hosted alongside the VCP. [virtualcellmodels.cziscience.com/benchmarks](https://virtualcellmodels.cziscience.com/benchmarks).
- **Arc Virtual Cell Challenge** — public competition modeled as a "Turing test" for virtual cells (Cell 2025). [arcinstitute.org/news/behind-the-data-virtual-cell-challenge](https://arcinstitute.org/news/behind-the-data-virtual-cell-challenge).
- **Polaris Hub** (Valence Labs + industry consortium) — drug-discovery ML benchmarks with cross-company governance. [polarishub.io](https://polarishub.io/).
- **Therapeutics Data Commons (TDC-2)** — multi-task ML therapeutics benchmark suite (Harvard). [tdcommons.ai](https://tdcommons.ai/).
- **CASP / CAPRI** — community-wide protein structure & docking blind tests. [predictioncenter.org](https://predictioncenter.org/).
- **HEST-1k benchmark** — 1k WSI + spatial transcriptomics benchmark (Mahmood lab). [github.com/mahmoodlab/HEST](https://github.com/mahmoodlab/HEST).

#### Datasets / weights access

- **CELLxGENE Census** — ~50M+ standardized cells (LTS 2025-11-08, schema 7.0.0). [cellxgene.cziscience.com](https://cellxgene.cziscience.com) · [docs](https://chanzuckerberg.github.io/cellxgene-census/).
- **Tahoe-100M** (Vevo + Arc) — 100M cells × ~1,100 drugs × 50 cell lines perturbation atlas. [tahoe.ai](https://www.tahoe.ai/).
- **Arc Virtual Cell Atlas** — observational + perturbational corpora used to train STATE. [arcinstitute.org/tools/state](https://arcinstitute.org/tools/state).
- **Replogle whole-genome Perturb-seq** — gold-standard CRISPRi atlas. [gwps.wi.mit.edu](https://gwps.wi.mit.edu/).
- **HEST-1k** — 1,000 paired H&E + Visium WSI dataset. [github.com/mahmoodlab/HEST](https://github.com/mahmoodlab/HEST).
- **InstaDeepAI Nucleotide Transformer org (HF)** — pretrained genomic FM weights (NT v2, Agro-NT, SegmentNT). [huggingface.co/InstaDeepAI](https://huggingface.co/InstaDeepAI).
- **Evo2 weights** — Apache-2.0, 7B + 40B. [github.com/ArcInstitute/evo2](https://github.com/ArcInstitute/evo2).
- **ESM-3 (1.4B open)** — Cambrian Non-Commercial. [github.com/evolutionaryscale/esm](https://github.com/evolutionaryscale/esm).
- **ESM Metagenomic Atlas** — 772M predicted metagenomic protein structures. [esmatlas.com](https://esmatlas.com/).
- **gnomAD v4** — 807k exomes/genomes; the variant-effect benchmark substrate. [gnomad.broadinstitute.org](https://gnomad.broadinstitute.org/).
- **ENCODE / GTEx tracks** — chromatin + expression substrate for AlphaGenome / Borzoi / Enformer. [encodeproject.org](https://www.encodeproject.org/) · [gtexportal.org](https://gtexportal.org/).
- **RCSB PDB** — canonical structure repository underpinning AlphaFold3 / ESM-3 training. [rcsb.org](https://www.rcsb.org/).

#### Recorded talks / lecture series

- **M2D2 Talks** (Valence + Mila) — weekly recorded ML-for-drug-discovery seminars; ~200 archived talks. [portal.valencelabs.com/m2d2](https://portal.valencelabs.com/m2d2).
- **CZI Virtual Cells Platform — workshops & webinars** — recorded sessions on FM training, benchmarks, evaluation. [virtualcellmodels.cziscience.com](https://virtualcellmodels.cziscience.com/).
- **scverse community talks / annual conference** — recorded scverse 2024 + 2025 conference sessions, summer-school lectures. [scverse.org/learn](https://scverse.org/learn/).
- **Simons Institute "ML & Statistics for Single-Cell Genomics" program** — public lectures incl. Mostafavi, Pachter, Regev. [simons.berkeley.edu](https://simons.berkeley.edu/) (browse program archive).
- **Broad Institute "Models, Inference & Algorithms" + MIA seminars** — bio-ML talks; Mahmood's "Multimodal, Generative, and Agentic AI for Pathology" lives here. [broadinstitute.org/talks](https://www.broadinstitute.org/talks).
- **Cell Symposia — Virtual Cells / Foundation Models** — Cell Press recorded plenary sessions; *URL unverified, search "Cell Symposia foundation models"*.
- **NeurIPS / ICLR Generative & Experimental Perturbations workshops** — recorded since 2023; the natural venue for the Generative Virtual Cells program. [generative-and-experimental-perturbations.github.io](https://generative-and-experimental-perturbations.github.io/) *(URL unverified, check workshop site for current year)*.

#### Key 2025 critique papers — the reckoning

- **Ahlmann-Eltze, C., Huber, W. & Anders, S. (2025).** "Deep-learning-based gene perturbation effect prediction does not yet outperform simple linear baselines." *Nature Methods* 22, 1657–1661. [nature.com/articles/s41592-025-02772-6](https://www.nature.com/articles/s41592-025-02772-6) · [bioRxiv v5](https://www.biorxiv.org/content/10.1101/2024.09.16.613342v5) · [Zenodo code/data](https://zenodo.org/records/16092690).
- **Kedzierska, K. Z., Crawford, L., Amini, A. P. & Lu, A. X. (2025).** "Zero-shot evaluation reveals limitations of single-cell foundation models." *Genome Biology* 26:101. [link.springer.com/article/10.1186/s13059-025-03574-x](https://link.springer.com/article/10.1186/s13059-025-03574-x) · [PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC12007350/) · [bioRxiv original](https://www.biorxiv.org/content/10.1101/2023.10.16.561085v1).
- **Wenkel, F., et al. (2025).** "Biology-driven insights into the power of single-cell foundation models." Proposes the `latent-additive + scGPT-embeddings` baseline as the new floor. [PubMed 41044630](https://pubmed.ncbi.nlm.nih.gov/41044630/) · [PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC12492631/). *Full citation venue URL unverified — confirm against final published version before slide use.*
- **Csendes, G., et al. (2025).** "A benchmark for prediction of transcriptomic responses to chemical perturbations across cell types." OpenReview. [openreview.net/forum?id=WTI4RJYSVm](https://openreview.net/forum?id=WTI4RJYSVm).
- **Bunne, C., et al. (2024).** "How to build the virtual cell with artificial intelligence: Priorities and opportunities." *Cell* 187, 7045-7063. [cell.com/cell/fulltext/S0092-8674(24)01332-1](https://www.cell.com/cell/fulltext/S0092-8674(24)01332-1) — positioning piece that the critique trio implicitly responds to.
- **Adduri, A., et al. (2025).** "Virtual Cell Challenge: Toward a Turing test for the virtual cell." *Cell* 188, 3370-3374. [cell.com/cell/fulltext/S0092-8674(25)00675-0](https://www.cell.com/cell/fulltext/S0092-8674(25)00675-0).
- *(2026 follow-ups to watch)* PertAdapt and reinforcement-learning fine-tuning preprints arguing the FMs can clear the linear floor with the right adaptation — early bioRxiv only, no peer review yet. [PertAdapt bioRxiv](https://www.biorxiv.org/content/10.1101/2025.11.21.689655v1.full-text).

#### Communities / Discord / Slack

- **scverse Zulip** — main developer chat for Scanpy / AnnData / squidpy / scvi-tools. [scverse.zulipchat.com](https://scverse.zulipchat.com/) · [Discourse forum](https://discourse.scverse.org/).
- **Open Problems community** — GitHub Discussions + Slack for benchmark contributors. [github.com/openproblems-bio](https://github.com/openproblems-bio).
- **Polaris Hub Slack** — drug-discovery ML benchmark community. Linked from [polarishub.io](https://polarishub.io/).
- **Hugging Face Biology / Bio-ML community** — model cards + discussion threads for NT, Geneformer, scGPT, UNI. [huggingface.co/biology](https://huggingface.co/biology) *(URL unverified — discoverable via topic tag)*.
- **EleutherAI #biology channel** — open-research community with active bio-ML thread; *Discord invite via [eleuther.ai](https://www.eleuther.ai/), channel name unverified*.

#### Bonus — high-signal one-offs

- **Epoch AI training-compute methodology** — the `FLOPs ≈ 6 × params × tokens` heuristic this corpus relies on. [epoch.ai/blog/estimating-training-compute](https://epoch.ai/blog/estimating-training-compute).
- **NVIDIA BioNeMo Framework** — the only public training-cost reproduction recipe for Geneformer V2; treats compute as a co-marketing disclosure. [github.com/NVIDIA/bionemo-framework](https://github.com/NVIDIA/bionemo-framework).
- **PREreview platform** — community pre-prints reviews including a thorough one of the Ahlmann-Eltze reckoning. [prereview.org/reviews/14019384](https://prereview.org/reviews/14019384).
- **Retraction Watch** — covered the AlphaFold 3 code-release controversy that pressured DeepMind in May 2024; the field's main enforcement mechanism on disclosure norms. [retractionwatch.com](https://retractionwatch.com/).

---

### 11.5 Timing cheat sheet

**Venue: 60–75 min group meeting with discussion throughout.** §6 (apply) + §7 (innovate) + §8 (commercial) all fit; the group-meeting format is the natural setting for all three, because the right outcome is *picking what we work on with eyes open on who'd fund it*, not telling a polished story.

#### The talk in 12 slides — speaker's eye view

For the speaker prepping cold the night before. Collapses §3 deep dives into 1 representative slide and §10 closing into 1 — pick what to expand based on the room.

| # | Slide | Source section |
|---|---|---|
| 1 | Title — name + *"From Foundation Models to Virtual Cells: what can we do as computational biologists?"* | — |
| 2 | Why now — 2024–25 inflection (CZ Biohub, Tahoe-100M, PathChat FDA) | §1.2 |
| 3 | The thesis — gap between FMs and virtual cells = the field's most concrete research agenda | §1.3 |
| 4 | The 5 FM families — single-cell / pathology / genomic / protein / multimodal | §2 |
| 5 | One representative deep dive (pick scGPT or Virchow2) — 4-question matrix; reference corpus for the rest | §3 |
| 6 | The 2025 reckoning — linear baseline beats sc-FMs | §4 |
| 7 | The 5 gaps — donor / species / causal / compute / evaluation | §5 |
| 8 | **Gap → Lane × Track mapping** — the connective slide | §5.6 |
| 9 | The 7 lanes (apply) — Lane 1 + Lane 4 + Lane 7 are the load-bearing three | §6 |
| 10 | The 6 tracks (innovate) — Track 1 + Track 2 + Track 6 are the load-bearing three | §7 |
| 11 | The commercial landscape — 3 buyer archetypes + per-pitch buyer map | §8.3 |
| 12 | The discussion — 3 pitches table → questions → close on AACR-2026 as the live evaluation surface | §9 + §10 |

#### Recommended plan — 62 min, §6 + §7 + §8 + group discussion

| Section | Time | Slides | Discussion pivot |
|---|---|---|---|
| §1 Opening — virtual-cell definitions + 2024–25 inflection | 4 min | 3 | — |
| §2 Five-family landscape | 5 min | 5 | "Which family is closest to our existing work?" |
| §3 Deep dives — 10 anchor models × 4-question matrix | 9 min | 10 | — |
| §4 The 2025 discipline crisis | 3 min | 3 | "Has anyone here actually reproduced the linear-baseline result?" |
| §5 The 5-gap framework + §5.6 mapping matrix | 4 min | 4 | "Which gap shows up in our own data?" |
| §6 Small-lab playbook — 7 lanes that use existing FMs | 5 min | 5 | "Lane 1 + Lane 7 are the AACR posters. Which of our datasets fits?" |
| §7 Real innovation tracks — 6 frontier methods lanes | 6 min | 6 | "Track 1 + Track 6 are publishable in 12 months at <$3k. Real?" |
| §8 Commercial landscape — buyer archetypes + timeline + per-pitch buyer map | 4 min | 3 | "Of the three pitches, which has the clearest non-academic check writer?" |
| §9 Discussion — picking our lane | 10 min | 3 | The whole point — see §9.1 pitch table |
| §10 Closing — AACR 2026 case study | 3 min | 3 | — |
| Buffer | 9 min | — | for tangents, discussion overflow |
| **Total** | **62 min** | **45** | — |

If the meeting can run 75 min, expand §9 (discussion) to 20 min — that's where the project decisions actually get made. If 90 min, also expand §3 deep dives (let people stop you on specific models) and §8 commercial (let the group push on specific buyer fit).

If you're running *short* (say a lab meeting is constrained to 45 min): cut §3 from 10 to 6 anchor models (drop UCE, STATE, AlphaGenome, ESM-3 → keep scGPT, Geneformer V2, Virchow2, Evo2), trim §8 commercial to the per-pitch buyer map only (the load-bearing slide), and trim §9 discussion to 5 min.

---

### 11.6 2026 updates — papers published since the first draft of this talk

The original bibliography in §11.3 leaned 2024–2025. Below are 15 papers from mid-2025 through Q2 2026 that materially affect the talk's argument. Each is annotated with **what changed because of it** and **which section it should be folded into when re-delivering**.

#### New benchmarks confirming or extending the 2025 reckoning

- **[Wu et al. 2025 *Nat Methods*](https://www.nature.com/articles/s41592-025-02980-0)** — "Benchmarking algorithms for generalizable single-cell perturbation response prediction." 27 methods × 29 datasets × 6 metrics. **What changed**: confirms Ahlmann-Eltze 2025 at scale; provides the first axis-by-axis breakdown of where each FM family fails. **Fold into**: §4.1.
- **[Hossain et al. 2024 *arXiv* 2412.13478](https://arxiv.org/abs/2412.13478)** — "Efficient Fine-Tuning of Single-Cell Foundation Models Enables Zero-Shot Molecular Perturbation Prediction." PEFT/LoRA recipe specifically for sc-FMs. **What changed**: gives Lane 2 (§6.3) a concrete, costed exemplar; the adapter is the contribution, the backbone is rented. **Fold into**: §6.3.

#### Position / framing papers

- **[Roohani et al. 2025 *Cell*](https://www.cell.com/cell/fulltext/S0092-8674(25)00675-0)** — "Virtual Cell Challenge: Toward a Turing test for the virtual cell." **What changed**: replaces the CZ Biohub program announcement as the canonical "what does success even look like" reference. **Fold into**: §1.1 (what is a virtual cell), §10 (closing).
- **[Adduri et al. 2025 *bioRxiv* 2025.06.26.661135](https://www.biorxiv.org/content/10.1101/2025.06.26.661135v1)** — STATE preprint (Arc Institute), now with first author and DOI. **What changed**: replaces "Arc press" placeholder for the §3.4 STATE row.
- **[Singh et al. 2025 *Exp Mol Med*](https://www.nature.com/articles/s12276-025-01547-5)** — "Single-cell foundation models: bringing AI into cell biology." **What changed**: cleanest mid-2025 review article to hand the audience for offline reading.

#### New single-cell / spatial foundation models

- **[Schaar et al. 2025 *Nat Methods*](https://www.nature.com/articles/s41592-025-02814-z)** — **Nicheformer** (Helmholtz Munich + TUM, Dec 2025) — first FM jointly trained on dissociated + spatial omics (SpatialCorpus-110M: 57M dissociated + 53M spatial cells, 73 tissues). **What changed**: the §2.1 SOTA row needs a spatial line; the §3 deep dives need an 11th model if spatial is a key audience interest. **Fold into**: §2.1, optional §3.11.
- **[Zhang et al. 2025 *Nat Commun*](https://www.nature.com/articles/s41467-025-59926-5)** — **CellFM** (May 2025) — 800M params on 100M human cells via modified RetNet on MindSpore. **What changed**: another data point for "domain matters more than scale" — CellFM is larger than most yet doesn't dominate. **Fold into**: §2.1.
- **[CancerFoundation, bioRxiv 2024.11.01.621087](https://www.biorxiv.org/content/10.1101/2024.11.01.621087v1)** — single-cell FM trained on cancer-only scRNA-seq for drug-resistance prediction. **What changed**: relevant to §7.2 (cancer-curated SAE project) and §6.4 Lane 3 (domain-specific small FM).

#### New pathology foundation models

- **[Ding et al. 2025 *Nat Med*](https://www.nature.com/articles/s41591-025-03982-3)** — **TITAN** (Nov 2025) — multimodal whole-slide FM pretrained on 335,645 WSIs via visual SSL + vision-language alignment with pathology reports and synthetic captions. **What changed**: the §2.2 SOTA row should add TITAN as a slide-level (not tile-level) anchor model.
- **[Xu et al. 2025 *Nat Commun*](https://www.nature.com/articles/s41467-025-66220-x)** — **mSTAR** (Dec 2025) — multimodal knowledge-enhanced pathology FM combining slides + reports + gene expression across 32 cancer types. **What changed**: a slot in the §2.2 anchor list and a possible §3 deep-dive replacement.
- **[Ma et al. 2026 *Nat Biomed Eng*](https://www.nature.com/articles/s41551-025-01488-4)** — **GPFM** — generalizable pathology FM via unified knowledge distillation. **What changed**: a new entrant in the pathology-FM consolidation story.
- **[Janowczyk et al. 2025 *Nat Med*](https://www.nature.com/articles/s41591-025-03780-x)** — first real-world clinical deployment of a fine-tuned pathology FM (UNI for EGFR detection in lung cancer, 197 patients, 43% genetic-testing avoidance). **What changed**: the §6.8 Lane 7 exemplar.
- **[Boosting pathology FMs via few-shot prompt-tuning for rare cancer subtyping, *Nat Commun* 2026](https://www.nature.com/articles/s41467-026-71715-2)** — PathPT framework. **What changed**: relevant to §6.3 Lane 2 (adapters / prompt-tuning) for clinical pathology.

#### Mechanistic interpretability — the wave that broke between drafts

- **[Adams et al. 2025 *PNAS*](https://www.pnas.org/doi/10.1073/pnas.2506316122)** — Sparse autoencoders uncover biologically interpretable features in protein language model representations. **What changed**: the *Track 1* claim in §7.2 — SAEs on biology FMs **have now been published**. Cancer-specific SAEs are the next open lane.
- **[Simon & Zou 2026 *arXiv* 2603.02952](https://arxiv.org/abs/2603.02952)** — "Sparse autoencoders reveal organized biological knowledge but minimal regulatory logic in single-cell foundation models: a comparative atlas of Geneformer and scGPT." **What changed**: the headline finding — sc-FMs encode cell-type / pathway features but not regulatory / causal features — connects §4 (the linear-baseline reckoning) to §7.2 (interpretability) at the *mechanism* level. The single most useful new paper for this talk's argument.
- **[bioRxiv 2025 — "Sparse Autoencoders Reveal Interpretable Features in Single-Cell Foundation Models"](https://www.biorxiv.org/content/10.1101/2025.10.22.681631v2)** — independent confirmation on scGPT.
- **[Hibou-LP team 2024–2025 *arXiv* 2407.10785](https://arxiv.org/abs/2407.10785)** — "Learning biologically relevant features in a pathology foundation model using sparse autoencoders" — the first pathology-FM SAE.
- **[bioRxiv 2026 — "What Do Biological Foundation Models Compute? Sparse Autoencoders from Feature Recovery to Mechanistic Interpretability"](https://www.biorxiv.org/content/10.64898/2026.03.04.709491v1)** — synthesis / methodology paper across families.

#### Genomic FM follow-ups

- **[*Cell Research* 2026 — Predicting non-coding variant effects with AlphaGenome](https://www.nature.com/articles/s41422-026-01249-1)** — independent evaluation. **What changed**: known AlphaGenome limitations (combinatorial / personal genome effects, distal regulatory elements, under-represented cell types) are now in the published record. **Fold into**: §3.8 (gap exposed) and §5.5 (evaluation honesty).

**Net effect on the talk:** §4.1 gets stronger (Wu confirms at scale). §6.8 Lane 7 gets a real clinical exemplar (Janowczyk). §7.2 Track 1 has to acknowledge the wave broke — but the *cancer-specific* SAE pitch is intact and arguably better. §10 gets the Bunne Cell "Turing test" framing as the cleanest closer. The 2026 pathology-FM proliferation (TITAN, mSTAR, GPFM, PathPT) is the strongest evidence that the field is leaning into Lane 7 (clinical deployment) over Lane 3 (more FMs).

---

## Companion resource files

- [`_resources-matrix.md`](_resources-matrix.md) — full compute / cost / team / data matrix with arithmetic shown and DISCLOSED/ESTIMATED/UNKNOWN tags
- [Foundation Models](../foundation-models.md) — cross-vault FM index with links to every tool dossier
- [90-min Speed Read](../speed-read.md) — abbreviated overview if you want a shorter prep path
- [2026 Timeline](../timeline.md) — Gantt of all 36 conferences with scoring rubric

---

*Last updated: 2026-05-13. Resource numbers and field status reflect the May 2026 state. §11.6 captures the 2025–2026 papers (Wu 2025 *Nat Methods* benchmark, Bunne 2025 *Cell* "Turing test", Janowczyk 2025 *Nat Med* clinical UNI deployment, the 5-paper SAE-on-biology-FMs wave, TITAN/mSTAR/GPFM pathology consolidation, Nicheformer for spatial, AlphaGenome critique in *Cell Research*) that should be folded into the body when re-delivering.*
