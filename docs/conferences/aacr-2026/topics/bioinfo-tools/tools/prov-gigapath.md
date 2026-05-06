# Prov-GigaPath

**Family:** path-fm
**Modality:** H&E whole-slide image tiles (256×256 at 20×, resized to 224 for the ViT) plus a slide-level encoder
**Released:** 2024 (Nature)
**License:** Code Apache-2.0; model weights gated, non-commercial research only (Microsoft Research / Providence terms)
**Code/checkpoint:** [github.com/prov-gigapath/prov-gigapath](https://github.com/prov-gigapath/prov-gigapath); checkpoint on HuggingFace ([prov-gigapath/prov-gigapath](https://huggingface.co/prov-gigapath/prov-gigapath))
**Also surfaced in:** single-cell-spatial-omics, virtual-cells

> Prov-GigaPath is a whole-slide pathology foundation model from
> Microsoft Research and Providence Health that pairs a tile-level
> encoder with a slide-level aggregator, so a single forward pass can
> turn an entire gigapixel slide into a fixed-length representation.
> It is pretrained on more than 1.3 billion tiles from over 170,000
> real-world H&E slides drawn from 31 Providence-affiliated hospitals,
> making it one of the largest published pathology corpora to date.
> The Nature 2024 paper claims state-of-the-art results across cancer
> subtyping, mutation prediction, and pathology-genomics retrieval.

## Architecture & training

The tile encoder is a ViT-style backbone trained with DINOv2-style
self-supervision on roughly 1.3 billion 256×256 H&E patches sampled
from 171,189 whole-slide images. The slide-level encoder uses a
LongNet-based dilated-attention transformer that ingests the full
sequence of tile tokens for a slide (tens of thousands per WSI) and
is pretrained with a masked tile-modeling objective, producing a
single slide embedding without needing weakly supervised MIL. The
public checkpoint comprises both the tile and slide encoders; the
authors report improved performance over UNI, CTransPath, and other
pathology backbones across 26 downstream clinical and biomarker
tasks.

## Use in the AACR 2026 corpus

<!-- mentions:start -->

**Posters mentioning Prov-GigaPath (n=2):**

- **1457** — *Prediction of gene expression and molecular pathway activity from H&E whole slide images in non-small cell lung cancer*
  …ted internal dataset of 67 commercial non-small cell lung cancer (NSCLC) patient samples with matched RNA-seq.Gigapath, a large-scale pathology foundation model pre-trained on over 170,000 WSIs, was used to extract patch and pat…
- **1470** — *Selecting representative histologic sections for cost-efficient 3D spatial transcriptomics and tumor microenvironment reconstruction*
  …mune aggregates, and mucosa&#8212;were segmented using a graph neural network. For each section, we extracted Prov-GigaPath embeddings and tissue class area proportions. Pairwise similarities, incorporating histology features and z-d…

**Sessions mentioning Prov-GigaPath (n=1):**

- [2026-04-20-am-decoding-cancer-ecosystem-pathology-tme-heterogeneity](../../../sessions/2026-04-20-am-decoding-cancer-ecosystem-pathology-tme-heterogeneity.md)
  …get a lot of those related image. For example, that's how, for example, Gabriele and team build on using the gigapath to actually model sort of pathology slide. They are using in just specific kind of scenario that are very dif…

<!-- mentions:end -->

## What's missing / where evidence is weak

- **Only the tile encoder is being used.** Both poster mentions (1457 NSCLC gene expression; 1470 3D spatial-transcriptomics tile selection) extract patch / tile embeddings — neither exercises the LongNet slide-level encoder that is Prov-GigaPath's actual architectural contribution.
- **No head-to-head benchmark in the corpus.** None of the posters compare Prov-GigaPath against UNI / UNI2-h or CONCH on a shared task; the choice of backbone reads as convenience, not the result of evaluation.
- **The session mention is glancing.** The April-20 session reference is a name-drop ("using gigapath to … model pathology slide") with no method detail, so it adds no evidence beyond the posters.
- **No discussion of the gated weights or non-commercial terms** in any corpus mention, despite this being a real adoption barrier for industry-adjacent work.

## Takeaway

Prov-GigaPath shows up as a working tile-feature backbone in two specialized methods posters — gene-expression prediction from H&E in NSCLC, and tile-similarity-based section selection for 3D spatial transcriptomics — plus one passing session reference. The AACR 2026 corpus thus uses Prov-GigaPath the same way it uses UNI: as a frozen patch encoder feeding a downstream model. The slide-level LongNet encoder, which is the paper's main novelty, never appears in the corpus, suggesting that even where Prov-GigaPath is preferred over UNI, it is not yet preferred *because of* its slide-level capability.
