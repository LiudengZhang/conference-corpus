# From Foundation Models to Virtual Cells

> Talk-prep page for a 30-minute presentation: *"What can we do as computational biologists?"*

## How to use this page

This page is a reference, not a slide deck. It is structured as a 30-min talk script (~24 slides at 75 sec each) you can lift onto your own slides, plus deeper background you can dip into for Q&A. Numbers marked **[DISCLOSED]** come from the original paper, technical report, or vendor disclosure. Numbers marked **[ESTIMATED]** are derived (arithmetic shown). Numbers marked **[UNKNOWN]** were not disclosed and could not be estimated reliably.

Cross-links jump to the per-tool dossiers in the [Foundation Models](../foundation-models.md) corpus, where every claim has an inline citation.

**Reading time**: ~25 min cold; ~10 min if you skim the §3 deep dives.

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

The talk's structure follows that gap. §2–3 map what exists. §4 explains the 2025 correction. §5 names the five field-wide gaps. §6 gives five things any computational biologist can do *today* to close them. §7 closes by using AACR 2026 as a live case study: what happens when these models meet a clinical audience that doesn't grade on novelty.

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
| Anchor models | Nucleotide Transformer (Dalla-Torre et al. 2025), DNABERT-2 (Zhou et al. 2024), HyenaDNA (Nguyen et al. 2023), Evo2 (Brixi et al. 2026), AlphaGenome (Avsec et al. 2026) |
| 2026 SOTA | **AlphaGenome** wins 25/26 regulatory variant-effect benchmarks (DeepMind 2026 *Nature*). **Evo2** retains generative + in-context-learning territory that AlphaGenome cannot match. |
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

- **Resources** — Two interlocking modules: **State Embedding (SE-600M)** at 600M params trained on 167M observational human cells; **State Transition (ST)** at undisclosed params trained on 100M+ perturbed cells (Tahoe-100M + Parse + Replogle); **GPU compute: UNKNOWN — preprint and Arc press do not disclose**; **cost UNKNOWN** (order-of-magnitude estimate ~$125k if similar Arc infrastructure to Evo2). Team: Arc Institute (Patrick Hsu + Hani Goodarzi labs).
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

### 3.8 AlphaGenome (DeepMind, Avsec et al. *Nature* 2026)

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

---

## §4. The 2025 discipline crisis (4 min)

### 4.1 The linear-baseline reckoning

Three independent papers in 2025 retired the single-cell FM perturbation-prediction leaderboard:

1. **Ahlmann-Eltze & Huber 2025** *Nature Methods* — "[Deep-learning–based perturbation modeling does not yet outperform simple baselines.](https://www.nature.com/articles/s41592-025-02772-6)" Showed scGPT, Geneformer, scFoundation, GEARS, CPA fail to beat `mean-of-training-perturbations` on held-out perturbations.
2. **Kedzierska et al. 2025** *Genome Biology* — extended the result to UCE and the zero-shot setting.
3. **Wenkel et al. 2025** *Nature Methods* — proposed `latent-additive + scGPT-embeddings` as the strongest single-cell baseline; current FMs still don't beat it consistently.

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

---

## §6. What computational biologists can do TODAY (3 min)

Five concrete, achievable lanes. Each is sized for a 6–18 month research project. None require pretraining your own FM.

### 6.1 Lane 1 — Use FMs as feature extractors (low-risk, high-utility)

Even where FMs lose on perturbation prediction, **their embeddings are useful for downstream tasks** like cell-type classification, batch correction, and trajectory inference. A scGPT or UCE embedding fed to a downstream classifier routinely matches or beats handcrafted features.

This is the *boring win*: stop trying to use FMs as generators; use them as feature extractors. Many AACR 2026 posters that didn't put scGPT/Geneformer in the title still use the embeddings under the hood.

**Concrete project**: take your lab's existing scRNA classification pipeline, swap PCA + Leiden for scGPT/UCE embeddings, measure the lift. Publish even if the lift is small — null/small-effect results are the most useful kind here.

### 6.2 Lane 2 — Replicate the linear-baseline audit

Pick a 2023–2024 sc-FM paper, run the `mean-of-training-perturbations` baseline alongside the FM, and report the comparison. Ahlmann-Eltze & Huber did this for ~6 models; the corpus of unaudited sc-FM papers is in the dozens.

This is the most valuable kind of replication right now. **Negative results are publishable** in *Nature Methods*, *Genome Biology*, and *bioRxiv* with a clear path to citation.

### 6.3 Lane 3 — Build a domain-specific small FM (the Geneformer-V2-104M_CLcancer playbook)

You don't need to compete with the 316M general-domain model. You need to **fine-tune or pretrain a small model on your domain** — pediatric cancer, neurodegeneration, ovarian organoids, your favorite cell type.

The Geneformer-V2-104M_CLcancer result (104M model trained on 14M cancer cells, matches or beats the 316M general model) is the proof. Scale doesn't win; domain curation does.

**Concrete project**: download your favorite atlas, finetune Geneformer-V2 (open weights, Apache-2.0), report transfer to your disease task. 3–6 month project. Publishable in a domain journal.

### 6.4 Lane 4 — Curate an honest benchmark

The field's biggest bottleneck is evaluation. If you have a perturbation dataset, contribute it to **Open Problems v2** with a proposed train/test split that holds out perturbations, donors, and cell types simultaneously. This is unsexy but field-defining work.

The Open Problems team is actively recruiting benchmark contributors as of 2026.

### 6.5 Lane 5 — Push for compute and benchmark transparency

This is the political lane. Co-sign with peers. Push reviewers to require **compute disclosure** and **linear-baseline reporting**. Push funders (NIH, EMBO, CZI) to require benchmark contributions as part of grant deliverables. Push journals to require negative-result-acceptable policies in their author guidelines.

Compute disclosure is now field standard in NLP (NeurIPS/ICLR require it). Biology FM venues do not yet require it. Computational biologists with venue-shaping influence (program committees, editorial boards) are the natural advocates.

---

## §7. Closing — conferences as the ground truth (3 min)

For a methods audience, the natural close is to flip the frame: the conferences are not where you *see* FMs in biology — they are the *evaluation surface*. Methods conferences (NeurIPS / ICLR / ICML) tell you what works on benchmarks; clinical conferences (AACR / ASCO / ESMO) tell you what works on cancer. Use AACR 2026 — happening *this April 17–22*, the week before ICLR — as the live case study.

### 7.1 The two-track timeline (1 min, 1 slide)

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

### 7.2 AACR 2026 as the case study (90 sec, 1 slide)

The corpus from this site ([aacr-2026.pages.dev](https://aacr-2026.pages.dev/conferences/aacr-2026/)): **25 unique sessions, ~464,000 words of transcripts, 2,241 poster abstracts (~871,000 words)** — organized into five axes: agentic AI, single-cell/spatial, virtual cells, bioinfo/AI methods, clinical trials.

Three things AACR 2026 gives us that ICLR/NeurIPS structurally cannot:

1. **The deployment reality check — [ED03 "Foundation Models and Multimodal AI for Cancer Research"](../conferences/aacr-2026/sessions/2026-04-17-pm-foundation-models-multimodal-ai-cancer-research.md) (Fri Apr 17, PM)** with **Charlotte Bunne / Serena Yeung-Levy / Michael Moor**. Bunne wrote the 2024 *Cell* virtual-cell perspective. Moor brings the agentic-AI-in-oncology-workflow slot. This is the field's first AACR-stage definitional panel — not "does our model beat a benchmark," but "what does deployment even mean here?"

2. **The donor-diversity stress test — [single-cell & spatial track](../conferences/aacr-2026/topics/single-cell-spatial-omics/index.md) (20 sessions, 1,015 posters)**. Spans HTAN tumor-evolution, clonal-hematopoiesis, TME heterogeneity, neural-immune crosstalk, fibroblast-state plasticity. ML conferences evaluate FMs on synthetic perturb-seq splits; AACR is where the actual heterogeneity surface lives. The **§5.1 donor-diversity gap either shows up here loudly, or it doesn't.**

3. **The agentic-AI-for-discovery proof — [AT02 "Agentic AI as the Cancer Researcher" (Tue Apr 21)](../conferences/aacr-2026/sessions/2026-04-21-at02-agentic-ai-cancer-researcher.md) + ["Agentic AI as the Oncologist" (Wed Apr 22)](../conferences/aacr-2026/sessions/2026-04-22-agentic-ai-as-the-oncologist.md)**. ICLR 2026 gave us MedAgentGym (72k task sandbox); AACR gives us *the actual research and clinical workflows* those agents are supposed to inhabit. Two sessions in one week is a deliberate field statement.

Cross-link the corpus: [AACR 2026 Virtual Cells topic](../conferences/aacr-2026/topics/virtual-cells/index.md) · [Agentic AI topic](../conferences/aacr-2026/topics/agentic-ai/index.md) · [Bioinfo/AI methods topic](../conferences/aacr-2026/topics/bioinfo-tools/index.md).

### 7.3 What we knew before → what AACR 2026 changes (30 sec, 1 slide)

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

## §8. Appendix

### 8.1 Likely Q&A questions + scripted answers

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

### 8.2 Datasets, weights, code — concrete starting points

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

### 8.3 Recommended reading (~30 references, one-sentence framings)

**Position papers**:
- Bunne et al. 2024 *Cell* — "How to build the virtual cell": the canonical positioning piece.
- Rood et al. 2024 *Cell* perspective — what single-cell FMs need to mature.
- Theodoris et al. 2023 *Nature* — Geneformer paper, the field's "atlas-level pretraining" demo.

**The 2025 critique trio**:
- [Ahlmann-Eltze & Huber 2025 *Nature Methods*](https://www.nature.com/articles/s41592-025-02772-6) — linear baselines beat sc-FMs.
- Kedzierska et al. 2025 *Genome Biology* — zero-shot benchmark across UCE / scGPT / Geneformer / scFoundation.
- Wenkel et al. 2025 *Nature Methods* — proposes `latent-additive` baseline.

**FM technical papers** (by family):
- *Single-cell*: Cui 2024 (scGPT), Theodoris 2023 (Geneformer), Rosen 2024 (UCE), Hao 2024 (scFoundation), Wen 2024 (CellPLM).
- *Pathology*: Chen 2024 (UNI), Vorontsov 2024 (Virchow), Zimmermann 2024 (Virchow2), Lu 2024 (PathChat), Nechaev 2024 (Hibou).
- *Genomic*: Dalla-Torre 2025 (NT), Zhou 2024 (DNABERT-2), Nguyen 2023 (HyenaDNA), Brixi 2026 (Evo2), Avsec 2026 (AlphaGenome).
- *Protein*: Hayes 2025 (ESM-3), Abramson 2024 (AlphaFold3), Watson 2023 (RFdiffusion).
- *Multimodal*: Zhang 2024 (BioMedCLIP), Lu 2024 (PathChat-2).

**Initiatives**:
- [CZ Biohub Virtual Cell announcement (Dec 2024)](https://chanzuckerberg.com/science/programs-resources/virtual-cells-initiative/)
- [Arc Institute STATE / Virtual Cell Atlas](https://arcinstitute.org/news/virtual-cell-model-state)
- [Open Problems for Single Cell](https://openproblems.bio)

**Compute / cost methodology**:
- [Cottier, Rahman et al. 2024](https://arxiv.org/abs/2405.21015) "The Rising Costs of Training Frontier AI Models" — the methodology this corpus follows for $ estimation.
- [Epoch AI training-compute methodology](https://epoch.ai/blog/estimating-training-compute) — `FLOPs ≈ 6 × parameters × tokens` heuristic.
- [NVIDIA Evo 2 announcement](https://blogs.nvidia.com/blog/evo-2-biomolecular-ai/) — discloses 2,048× H100 + ratio comparison to AlphaFold and ESM-3.
- [retractionwatch.com on AlphaFold 3 disclosure](https://retractionwatch.com/2024/05/14/nature-earns-ire-over-lack-of-code-availability-for-google-deepmind-protein-folding-paper/) — the May 2024 controversy that pressured DeepMind to release inference code.

**Field context**:
- Replogle et al. 2022 *Cell* — whole-genome Perturb-seq gold standard.
- Campanella et al. 2025 *Nature Communications* — pathology FM clinical benchmark.
- The full corpus this page draws from: see [Foundation Models](../foundation-models.md) for cross-vault index.

### 8.4 Backup resources — extended reading list

A field-survey-grade list of people, venues, benchmarks, datasets, talks, critique papers, and communities to follow up on after the talk. Verified to working state as of 2026-05-12. Where a URL is uncertain it is flagged *URL unverified*.

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

### 8.5 Timing cheat sheet

| Section | Time | Slides | Pace |
|---|---|---|---|
| §1 Opening | 3 min | 3 | ~60 sec/slide |
| §2 Landscape | 4 min | 5 | ~50 sec/slide |
| §3 Deep dives | 8 min | 10 | ~50 sec/slide |
| §4 Crisis | 4 min | 3 | ~80 sec/slide |
| §5 Gaps | 4 min | 3 | ~80 sec/slide |
| §6 What to do | 3 min | 3 | ~60 sec/slide |
| §7 Closing — AACR 2026 case study | 3 min | 3 | ~60 sec/slide |
| Q&A buffer | 1 min | — | — |
| **Total** | **30 min** | **30** | — |

If you're running long, cut §3 from 10 to 6 anchor models (drop UCE, STATE, AlphaGenome, ESM-3 → keep scGPT, Geneformer V2, Virchow2, Evo2). Sections §4–7 are non-negotiable — §4-6 are where the *"what can we do?"* answer lives, and §7 is where the corpus you built lives.

---

## Companion resource files

- [`_resources-matrix.md`](_resources-matrix.md) — full compute / cost / team / data matrix with arithmetic shown and DISCLOSED/ESTIMATED/UNKNOWN tags
- [Foundation Models](../foundation-models.md) — cross-vault FM index with links to every tool dossier
- [90-min Speed Read](../speed-read.md) — abbreviated overview if you want a shorter prep path
- [2026 Timeline](../timeline.md) — Gantt of all 36 conferences with scoring rubric

---

*Last updated: 2026-05-12. Resource numbers and field status reflect the May 2026 state. The 2025 linear-baseline critique trio and the Jan–Feb 2025 events (CZ Biohub announcement, Tahoe-100M release, PathChat DX FDA designation, UNI2-h gated release) are the most recent reference events.*
