# PSB 2026 — Themes

Cross-session synthesis of [PSB 2026](index.md). Papers are cited by first author and PDF filename; full tables live on the [session pages](sessions/index.md).

## Foundation models and LLMs — the dominant theme

At least **20 of 55 papers** are LLM- or foundation-model-centric. What distinguishes PSB 2026 from a typical FM-heavy program is the ratio: an unusual share are **evaluations, benchmarks, guardrails, and negative results** rather than model announcements.

**The evaluation cluster is the reason to read this meeting.**

- **Zhang X. et al., *Automated Chest X-ray Report Generation Remains Unsolved*** (`zhang_x.pdf`) — a multi-institution negative result, and the highest-value single citation from PSB 2026 for the argument that benchmark scores overstate clinical readiness.
- **Johri et al., PanEndoAtlas / PanEndoFM** (`johri.pdf`) — 420k endoscopy images, 30 datasets, 13 countries, 111 GI diseases; a GI foundation model pretrained on 10M images and benchmarked against EndoFM-LV, EndoSSL, ViT-B/16, ResNet-50. A clinician-guided benchmark construction, not just a model.
- **Pal et al., ReXVQA** (`pal.pdf`) and **Sambara et al., 3DReasonKnee** (`sambara.pdf`) — vision-language benchmarks with grounded reasoning as the target.
- **Banerjee et al., ReXecution** (`banerjee.pdf`) — names the intention-execution disconnect in medical AI.
- **Mottez et al.** (`mottez.pdf`, [S5](sessions/fairness-bias-biomedical-ai.md)) — chest X-ray bias detection and mitigation, on the same substrate as Zhang's negative result but in a different session.

**EHR foundation models.** Burkhart et al., *Quantifying surprise in clinical care* (`burkhart.pdf`), uses FM-derived event informativeness across a whole hospitalization context — the closest thing here to asking what these models actually represent.

**LLMs applied to genomics and gene function.** Shringarpure et al. of 23andMe use LLMs to identify causal genes in complex-trait GWAS (`shringarpure.pdf`); Rifat et al.'s **BioLM-NET** combines contextual LLM gene embeddings with prior biological knowledge over multi-omics (`rifat.pdf`).

**LLM-as-evaluator infrastructure.** MedFactEval and MedAgentBrief (`grolleau.pdf`), eConsult concordance (`wu_d.pdf`), clinical consultation templates (`mccoy.pdf`), retrieval-augmented guardrails with an error taxonomy (`chen_w.pdf`), and LLM-based bias auditing (`ansari.pdf`).

**Corpus fit:** this is the strongest external evidence base for the position taken in [Why linear baselines win](../../talks/fm-to-virtual-cells/why-linear-baselines-win.md) and [Reading an FM paper critically](../../talks/fm-to-virtual-cells/reading-an-fm-paper-critically.md), and it belongs in the [evaluation papers catalog](../../talks/fm-to-virtual-cells/evaluation-papers-catalog.md).

## Agentic AI — four papers, three sessions

The clearest structural signal at PSB 2026: LLM agents appear as a *method* across unrelated tracks, not as a novelty in one.

| Paper | Session | What it does |
|---|---|---|
| **MedAgentBench v2** (E. Chen, `chen_eric.pdf`) | [S4](sessions/ai-ml-clinical-medicine.md) | Medical LLM agent benchmark, second version |
| **Gene-R1** (Z. Wang, `wang_z.pdf`) | [S2](sessions/biological-molecular-function.md) | Reasoning LLMs for gene-set analysis |
| **LLM Agent Based Protein Function Prediction** (Zhapa-Camacho, `zhapa-camacho.pdf`) | [S2](sessions/biological-molecular-function.md) | Agentic protein function assignment |
| **GenoMAS** (K. Chen, `chen_k.pdf`) | [S3](sessions/systems-biology-network-analysis.md) | Disease-relationship discovery over ~1,300 disease-condition pairs |

That a *second* version of an agent benchmark appears is worth more than any of the individual systems: it means the first version got used.

**Corpus fit:** [`aacr-2026/topics/agentic-ai/`](../aacr-2026/topics/agentic-ai/index.md), its [AT02 synthesis](../aacr-2026/topics/agentic-ai/synthesis-at02-vs-corpus.md), and [how agentic AI meets FMs](../../talks/fm-to-virtual-cells/agentic-meets-foundation.md). Note the convergence with **GCC2026**, where agentic Galaxy was likewise the dominant thread — two unrelated communities landing on the same idea in the same six months.

## Cancer and oncology

**PSB 2026 has no cancer session.** Oncology enters only through methods papers, and there are four worth knowing:

1. **Tamura et al.** (`tamura.pdf`, [S1](sessions/precision-medicine.md)) — the best of them. Weakly supervised neuron selection in sparse autoencoders over **CLIP-derived pathology foundation-model embeddings**, evaluated on **Camelyon16** (breast-cancer lymph-node metastasis) and **PANDA** (prostate cancer grading), explicitly demonstrating tumor-patch identification. Mechanistic interpretability applied to a pathology FM — the natural companion to the [FM-pathology traction synthesis](../aacr-2026/topics/bioinfo-tools/synthesis-fm-pathology-traction.md) and the [Mahmood Lab](../../talks/fm-to-virtual-cells/views/institutes/mahmood-lab.md) material.
2. **Lopez-Garcia et al.** (`lopez-garcia.pdf`, [S4](sessions/ai-ml-clinical-medicine.md)) — scoring physician risk communication in prostate cancer with LLMs (Cedars-Sinai). The most explicitly oncologic paper at the meeting, and it is about communication rather than biology.
3. **Hardy et al., ColonCrafter** (`hardy.pdf`) and **Johri et al., PanEndoAtlas** (`johri.pdf`) — GI and colorectal endoscopy, polyp subtyping, Barrett's grading.
4. **Chang et al., PertSpectra** (`chang_s.pdf`) — perturbation modeling framed toward drug discovery.

Two posters add more: *Mouse lymph node colonization models predict human tumor metastasis in melanoma* (#72, Brendan K. Ball, Andrew J. Gentles) and *Lrg1 as a therapeutic target in cancer cachexia* (#75).

**Read this as a finding, not a gap.** A meeting where AI/ML in clinical medicine takes half the peer-reviewed volume and cancer gets no session is telling you where computational-biology submissions are flowing.

## Single-cell and spatial omics

**Thin in the peer-reviewed proceedings; concentrated in the workshop and posters.**

- **Peer-reviewed anchor:** Chang et al.'s **PertSpectra** (`chang_s.pdf`) is essentially the only one — guided triple matrix factorization for perturbation impact, evaluated on three single-cell RNA-seq Perturb-seq-style datasets with single *and* combinatorial genetic perturbations, using a gene–gene interaction graph prior. Compare [PerturbFate](../../talks/fm-to-virtual-cells/adjacent-methods/perturbfate.md) and [SCGD26's in vivo Perturb-seq talk](../single-cell-genomics-day-2026/talks/xin-jin-in-vivo-perturbseq.md).
- **The workshop is where the field showed up:** [*Advances of AI Methods in Single Cell Spatial Omics*](workshops.md) (Garmire / Xiuwei Zhang / Levy), covering spatial transcriptomics, proteomics, and metabolomics.
- **Posters carry the rest:** *Gene Expression Prediction in Single Cells via Data-Driven Discrete Dynamical Systems* (#41); *Integrating Generative AI Models into Computational Pipelines for Scalable Interpretation of Single-Cell Gene Expression Programs* (#50, St. Jude); ***CELLestial**: a scalable end-to-end spatial proteomics analysis framework* (#79).
- A curiosity worth noting: the [Systems Biology](sessions/systems-biology-network-analysis.md) session was co-organized by **Joshua Welch** (LIGER), yet no single-cell paper landed in it.

**Implication for harvesting:** the [poster/abstract book](https://psb.stanford.edu/previous/psb26/conference-materials/psb26_abstracts_final.htm) — 117 records with affiliations and preprint DOIs, in HTML and XLSX — is where this corpus's core subject matter actually sits at PSB 2026. It is the top unharvested target.

## Precision medicine and intermediate phenotypes

The [S1](sessions/precision-medicine.md) session's consistent finding is that **polygenic scores earn their keep in combination** — with imaging endotypes and plasma proteomics (Venkatesh), with clinical, lifestyle and social risk factors (Cardone), with generative trajectory forecasting (German). Seagle et al. compare PRS construction methods head to head. This is the same structural problem the corpus tracks under biomarker stratification, including the immunoprevention framing in the [SITC Computational IO series](../sitc-computational-io-2026/index.md).

## Multi-omics and network biology

`rifat.pdf` (BioLM-NET), `rajagopalan.pdf` (DRIVE-KG heterogeneous knowledge graphs over Penn Medicine BioBank + Regeneron Genetics Center), `orlenko.pdf` (random-walk framework for Alzheimer's targets), and `jiang.pdf` (literature-driven causal statement extraction) form a coherent block. Tasnina et al.'s provenance tracing for network diffusion (`tasnina.pdf`) asks the interpretability question of graph methods that the FM papers ask of transformers.

## What PSB 2026 says about where the field is going

Three observations, in order of confidence:

1. **Evaluation has become a first-class contribution.** Negative results, benchmark construction, blind-assessment advocacy (the [Trust and Reproducibility workshop](workshops.md)), and LLM-as-evaluator infrastructure together outweigh new-model papers. That is a maturing field, not a stalling one.
2. **Agents crossed from demo to method** — four papers, three sessions, one of them a v2 benchmark.
3. **Clinical AI is absorbing the submission volume.** One session took 27 of 55 papers. Whether that reflects the field or PSB's session-proposal dynamics is worth watching in the 2027 track list.

## Sources

All claims trace to the [PSB 2026 proceedings](https://psb.stanford.edu/psb-online/proceedings/psb26/), the [schedule PDF](https://psb.stanford.edu/previous/psb26/conference-materials/schedule.pdf), and the [poster/abstract book](https://psb.stanford.edu/previous/psb26/conference-materials/psb26_abstracts_final.htm), fetched 2026-08-25. Per-paper PMIDs are on the [session pages](sessions/index.md).
