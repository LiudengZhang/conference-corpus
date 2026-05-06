# scGPT

**Family:** sc-fm
**Modality:** Single-cell RNA-seq (gene-expression value tokens)
**Released:** 2024 (Nature Methods)
**License:** MIT (code); checkpoints distributed via Google Drive under the same terms
**Code/checkpoint:** [github.com/bowang-lab/scGPT](https://github.com/bowang-lab/scGPT) (whole-human, organ-specific, and pan-cancer checkpoints)
**Also surfaced in:** agentic-ai, single-cell-spatial-omics, virtual-cells

> scGPT is a generative single-cell foundation model from the Bo Wang
> Lab at the University of Toronto that treats each cell as a sequence
> of gene–value tokens and pretrains a transformer to reconstruct
> masked expression values. It is trained on more than 33 million
> human cells from CELLxGENE and supports cell-type annotation,
> integration, perturbation prediction, and gene-regulatory inference
> after lightweight fine-tuning. Organ-specific (brain, blood, lung,
> heart, kidney) and pan-cancer (5.7M cells) checkpoints are released
> alongside the whole-human default.

## Architecture & training

scGPT uses a transformer encoder with a custom generative attention
mask: gene tokens are paired with binned expression-value tokens and
condition tokens (batch, modality), and the model is trained to
predict masked expression values given the unmasked context. The
flagship "whole-human" checkpoint is pretrained on ~33M normal human
cells aggregated from CELLxGENE; organ-specific variants range from
~0.8M to ~13M cells, and a pan-cancer variant is trained on ~5.7M
tumor cells. Fine-tuning uses a small task head for cell-type
classification, batch integration, or perturbation response, and the
paper reports competitive or improved performance over scBERT,
Geneformer, and scVI baselines across these tasks.

## Use in the AACR 2026 corpus

<!-- mentions:start -->

**Posters mentioning scGPT (n=2):**

- **4212** — *Baseline peripheral blood scRNA-seq AI estimator framework predicts solid-tumor response and adverse events via molecular foundation models and cell-to-patient learning*
  …e PBMC scRNA-seq counts (with optional cell-type annotations), pre-trained molecular foundation models (FMs) (scGPT v1.0 [1], scFoundation [2]), cell-to-patient Multi-Instance Learning (MIL) [3] with RECIST labels (CR/PR Resp…
- **5478** — *Benchmarking gene expression foundation models on bulk RNA-Seq data*
  …ble models with released weights, including six single-cell models (CellFM, GeneFormer, scBERT, scFoundation, scGPT, and scLong) and BulkFormer, a model trained on bulk RNA-seq data. Embeddings were extracted following each m…

**Sessions mentioning scGPT (n=1):**

- [2026-04-20-am-ai-revolution-in-cancer-research](../../../sessions/2026-04-20-am-ai-revolution-in-cancer-research.md)
  …k and send us any feedbacks you may have. All right, so what's next? I talk about virtual cell models such as scGPT and ExCell. I talk about bioreason models, particularly bioreasons through DNA sequences, bioreasons through…

<!-- mentions:end -->

## What's missing / where evidence is weak

- **The pan-cancer checkpoint is absent.** Despite a 5.7M tumor-cell pan-cancer variant being released alongside the whole-human default, no corpus mention uses or evaluates it. Both poster mentions reach for the v1.0 whole-human checkpoint or a generic "scGPT" baseline.
- **No fine-tuning protocol detail in the corpus.** Poster 4212 (PBMC peripheral-blood AI estimator) calls out scGPT v1.0 as a feature extractor, and poster 5478 benchmarks it, but neither describes fine-tuning hyperparameters, organ-specific checkpoint choice, or perturbation evaluation.
- **The session mention is a name-check.** The April-20 AI Revolution session lists scGPT alongside ExCell as "virtual cell models" without methodological detail; it adds no evidence beyond the posters.
- **No tumor-microenvironment or perturbation work.** scGPT's headline capabilities (perturbation prediction, GRN inference) do not appear in any corpus mention.

## Takeaway

scGPT is present in AACR 2026 as a representative single-cell foundation model — invoked in two posters and one session — but always as a context entry in a foundation-model lineup (typically alongside scFoundation or Geneformer) rather than as the primary engine of an analysis. The corpus pattern mirrors Geneformer's: scGPT is widely *known* and consistently *named*, but no AACR 2026 contribution leans on its generative or perturbation capabilities to drive a finding.
