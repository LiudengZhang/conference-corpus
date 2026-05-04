# Geneformer

**Family:** sc-fm
**Modality:** Single-cell RNA-seq (rank-encoded gene expression, human)
**Released:** 2023 (Nature); V2 update 2024
**License:** Apache-2.0
**Code/checkpoint:** [huggingface.co/ctheodoris/Geneformer](https://huggingface.co/ctheodoris/Geneformer)
**Also surfaced in:** agentic-ai, single-cell-spatial-omics, virtual-cells

> Geneformer is a transformer foundation model for single-cell
> transcriptomics from Christina Theodoris's group at Gladstone/UCSF
> that represents each cell as a rank-ordered list of its most
> distinctively expressed genes and learns gene-context relationships
> via masked language modeling. It is pretrained on Genecorpus-30M, a
> ~30 million-cell corpus assembled from public human scRNA-seq, and
> was the first widely adopted single-cell FM. Standout claims center
> on zero- and few-shot transfer to disease modeling, in-silico
> perturbation, and identifying candidate gene targets in
> data-limited settings such as cardiomyopathy.

## Architecture & training

Geneformer encodes a cell as the ranked list of its top expressed
genes (rank-value encoding, deprioritizing housekeeping genes) and
runs a BERT-style transformer encoder over that sequence. The
original V1 model (2023) is ~10M parameters with a 2,048-token input
and ~25K-gene vocabulary, pretrained with 15% masked-gene-prediction
on Genecorpus-30M (~30M human single-cell transcriptomes). V2 (2024)
scales to 104M and 316M parameter variants with a 4,096-token input,
restricts the vocabulary to ~20K protein-coding genes, and is
pretrained on a ~104M-cell expanded corpus, with a separate
14M-cell cancer-domain-tuned variant. Pretraining is fully
self-supervised and the released models are typically used either
zero-shot for embeddings/perturbation or fine-tuned on small labeled
sets.

## Use in the AACR 2026 corpus

<!-- mentions:start -->

**Posters mentioning Geneformer (n=4):**

- **2752** — *CancerSTFormer enables multi-scale analysis of spot-resolution spatial transcriptomes and dissects the gene and immune regulatory responses of targeted therapies*
  …results using the PD1-sensitive/resistant gene sets of the Holdout group. When compared against a fine-tuned Geneformer and a norefinement control, both Local and Extended CancerSTFormer variants consistently achieved higher accu…
- **5478** — *Benchmarking gene expression foundation models on bulk RNA-Seq data*
  …thods: We compared publicly available models with released weights, including six single-cell models (CellFM, GeneFormer, scBERT, scFoundation, scGPT, and scLong) and BulkFormer, a model trained on bulk RNA-seq data. Embeddings we…
- **978** — *Deep learning frameworks for translating cancer drug response from cell-level to patient-level by modeling transcriptome*
  …e can be also seen as transcriptomic cellular state change, we used an existing pre-trained rank-based model (Geneformer, Nature 2024). Given these models of transcriptomic changes, we model the cancer patient in two different app…
- **LB169** — *scCAP: An ontology-aware large language model framework for hierarchical and standardized single-cell type annotation*
  …remains challenging in single-cell RNA sequencing analysis. Existing tools (CellTypist, SCimilarity, SingleR, Geneformer) exhibit distinct biases and lack standardized nomenclature, hindering cross-study comparability. Furthermore…

**Sessions mentioning Geneformer (n=0):**

_No session transcripts in the AACR 2026 corpus mention this tool._

<!-- mentions:end -->

## What's missing / where evidence is weak

- TODO

## Takeaway

TODO — one paragraph on what the AACR 2026 corpus uniquely teaches us
about Geneformer.
