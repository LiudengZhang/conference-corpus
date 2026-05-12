# Pathology Foundation Models — Faisal Mahmood (Harvard / Mahmood Lab)

**ISBI 2026 plenary keynote on pathology foundation models, slide-level aggregation, and multimodal pathology agents — the methods-side bridge from the AACR pathology-FM dossier line (CHIEF / UNI / Prov-GigaPath) into the IEEE imaging community.**

- **Speaker(s) / Authors:** Faisal Mahmood
- **Affiliation(s):** Harvard Medical School / Brigham & Women's Hospital / Broad Institute (Mahmood Lab)
- **Anchor type:** keynote
- **Track / day:** ISBI 2026 main plenary (Thu Apr 9 or Fri Apr 10, ExCeL London)
- **IEEE Xplore:** TBD (keynote — no IEEE Xplore paper; any new artifact tracked via Mahmood Lab GitHub / HuggingFace through Q2 2026)
- **Status:** post-meeting

## What it does

Mahmood's keynote framed the current pathology-FM landscape — CHIEF (slide-level diagnostic + prognostic FM), UNI / UNI2 (tile-level encoder pretrained on >100M H&E patches), and the broader CONCH / multimodal pathology agent line — and outlined where the field is going: larger tile encoders, multimodal (H&E + IHC + report + molecular) pretraining, agentic workflow composition, and clinical deployment. The talk is the direct methods-side complement to the AACR 2026 pathology-FM clinical-deployment readouts.

## How it works / methodology

Pathology FMs share a three-tier stack: (1) self-supervised tile encoders (DINOv2-class) trained on tens-to-hundreds of millions of H&E patches; (2) slide-level aggregation (attention-based MIL, transformers over tile embeddings, set-transformer variants); (3) task heads for subtyping, biomarker prediction, survival, and weakly-supervised molecular regression. Mahmood-line models (UNI, CHIEF) emphasize generalization across cancer types via task-agnostic pretraining plus zero-shot / few-shot evaluation.

## Headline benchmarks

TBD — keynote-level synthesis; specific benchmark deltas not in program-notes. CHIEF and UNI baselines remain the published anchors (CHIEF: 19 cancer types, 60K+ slides; UNI: >100M tiles).

## How it works

**Core idea.** A pathology foundation model is a large image (and increasingly multimodal) encoder pretrained self-supervised on H&E whole-slide tiles at internet scale (tens-to-hundreds of millions of patches), producing a generic slide / tile embedding that transfers to dozens of downstream pathology tasks with minimal task-specific data.

**Inputs / outputs.** Inputs: H&E whole-slide images (typically 20x or 40x magnification); for multimodal extensions, paired IHC, molecular labels, or pathology reports. Outputs: tile-level embeddings (UNI, UNI2), slide-level embeddings or task predictions (CHIEF), or report / answer generation (multimodal pathology agents in the CONCH / PathChat line).

**Key innovation.** Three-tier stack with task-agnostic pretraining: (1) DINOv2-class self-supervised tile encoder pretrained on >100M unlabeled patches, (2) attention-MIL or transformer-over-tiles aggregator that lifts tile embeddings to slide-level representations, (3) light task heads or zero-shot evaluation. Generalization-by-scale rather than task-by-task model design is the field-shaping move; CHIEF added the agentic / multitask synthesis layer.

**Parameters.** UNI: ViT-L/16, ~300M parameters, ~100M H&E tiles. UNI2 / CHIEF v2: scale TBD (likely ViT-H/G, hundreds-of-millions to low-billions parameters, internet-scale tile counts). Slide-aggregation models: transformer over up to ~10K tiles per slide.

**Canonical example.** Zero-shot or few-shot lung-cancer subtyping from H&E: tile a WSI, encode all tiles with UNI, aggregate with attention-MIL, predict LUAD vs LUSC. CHIEF extends this to a single model covering 19 cancer types and 60K+ slides with prognostic outputs alongside diagnostic ones — the headline cross-cancer-type generalist pathology FM result that anchored the keynote.

## Where it fits in the corpus

- **AACR 2026:** direct line to [CHIEF](../../aacr-2026/topics/bioinfo-tools/tools/chief.md), [UNI](../../aacr-2026/topics/bioinfo-tools/tools/uni.md), and [Prov-GigaPath](../../aacr-2026/topics/bioinfo-tools/tools/prov-gigapath.md) dossiers
- **MICCAI 2026:** anticipated COMPAY workshop cousin paper (Sep 27–Oct 1) — likely UNI2 or CHIEF v2 methods write-up
- **RSNA 2026 / CVPR 2026:** RSNA radiology-pathology fusion track; CVPR FMV / MMFM-BIOMED workshops likely surface the same author pool

## Notes

Keynote itself is not a tool page — any new model announced gets either (a) in-place update to the AACR dossier (incremental work) or (b) a new ISBI tool page if fundamentally new. Watch Mahmood Lab GitHub / HuggingFace through May–July 2026 for the artifact drop. Likely TBME Special Section pipeline if a methods companion paper exists.
