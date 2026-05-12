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

The talk's structure follows that gap. §2–3 map what exists. §4 explains the 2025 correction. §5 names the five field-wide gaps. §6 gives five things any computational biologist can do *today* to close them.

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

## §7. Appendix

### 7.1 Likely Q&A questions + scripted answers

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

### 7.2 Datasets, weights, code — concrete starting points

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

### 7.3 Recommended reading (~30 references, one-sentence framings)

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

### 7.4 Timing cheat sheet

| Section | Time | Slides | Pace |
|---|---|---|---|
| §1 Opening | 3 min | 3 | ~60 sec/slide |
| §2 Landscape | 5 min | 5 | ~60 sec/slide |
| §3 Deep dives | 10 min | 10 | ~60 sec/slide |
| §4 Crisis | 4 min | 3 | ~80 sec/slide |
| §5 Gaps | 4 min | 3 | ~80 sec/slide |
| §6 What to do | 3 min | 3 | ~60 sec/slide |
| Q&A buffer | 1 min | — | — |
| **Total** | **30 min** | **27** | — |

If you're running long, cut §3 from 10 to 6 anchor models (drop UCE, STATE, AlphaGenome, ESM-3 → keep scGPT, Geneformer V2, Virchow2, Evo2). Section §4–6 are non-negotiable — they're where the *"what can we do?"* answer lives.

---

## Companion resource files

- [`_resources-matrix.md`](_resources-matrix.md) — full compute / cost / team / data matrix with arithmetic shown and DISCLOSED/ESTIMATED/UNKNOWN tags
- [Foundation Models](../foundation-models.md) — cross-vault FM index with links to every tool dossier
- [90-min Speed Read](../speed-read.md) — abbreviated overview if you want a shorter prep path
- [2026 Timeline](../timeline.md) — Gantt of all 36 conferences with scoring rubric

---

*Last updated: 2026-05-12. Resource numbers and field status reflect the May 2026 state. The 2025 linear-baseline critique trio and the Jan–Feb 2025 events (CZ Biohub announcement, Tahoe-100M release, PathChat DX FDA designation, UNI2-h gated release) are the most recent reference events.*
