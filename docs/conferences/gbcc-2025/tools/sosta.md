# sosta

**Spatial Omics STructure Analysis** — a Bioconductor package that reconstructs anatomically relevant tissue structures from spatial omics data (using molecular features or cell-type labels), then computes structure-level quantitative metrics — bridging the gap between cell-level spatial-omics analysis and tissue-architecture readouts.

- **Maintainer:** Samuel Gunz (University of Zurich, Robinson Lab) — `samuel.gunz@uzh.ch`
- **Bioconductor:** [sosta v1.4.0](https://bioconductor.org/packages/release/bioc/html/sosta.html)
- **Source:** [github.com/sgunz/sosta](https://github.com/sgunz/sosta) · [project site](https://sgunz.github.io/sosta/)
- **Vignettes:** [Overview](https://bioconductor.org/packages/release/bioc/vignettes/sosta/inst/doc/StructureReconstructionVignette.html) · [Pancreatic islets (IMC diabetes)](https://bioconductor.org/packages/release/bioc/vignettes/sosta/inst/doc/ImcDiabetesIsletsVignette.html)
- **License:** GPL (>= 3)
- **Status at GBCC2025:** methods talk on spatial-omics anatomical-structure analysis

## Talk at GBCC2025

- **Speakers:** Samuel Gunz, Mark D Robinson (University of Zurich)
- **Day / session:** Day 3 (Wed Jun 25, 2025) — Oral Session 3, Grace Auditorium (chair: Lambda Moses)
- **Talk title:** "sosta: a framework to analyze anatomical structures from spatial omics data"
- **Slides (Zenodo DOI):** *TBD — Zenodo deposits typically 2–4 weeks post-conference*
- **Video:** [GBCC2025 playlist](https://www.youtube.com/playlist?list=PLdl4u5ZRDMQTJ0O_FIO9ayqaUDfnMo4-4)
- **Abstract / schedule:** [GBCC2025 program](https://gbcc2025.bioconductor.org/program/scientific_program/)

## What it does

Most spatial-omics tooling stops at the cell — segmentation, neighborhood graphs, niche detection. sosta goes one level up: take a spatial-omics object and reconstruct anatomical structures (e.g. islets, glomeruli, tumor regions, lobules) from molecular features or cell-type labels, then compute morphology and composition metrics on the resulting structures. That gives downstream analysis a tissue-architecture handle that doesn't require external segmentation masks.

## Where it fits in the corpus

- **AACR 2026:** axis single-cell-spatial-omics — structural-level readouts complement the cell-level dossiers (Cell2Location, etc.)
- **spatialFDA** ([entry](../../eurobioc-2025/tools/spatialfda.md)) — same UZH / Robinson lab; spatialFDA tests differences in spatial summary functions, sosta produces the structures those functions can be evaluated on
- **SpatialData** ([entry](../../eurobioc-2025/tools/spatialdata.md)) — sosta operates on the SpatialExperiment / SpatialData container family
- **OSTA** ([entry](../../eurobioc-2025/tools/osta.md)) — community textbook covering the broader spatial-omics methods stack
- **ISMB 2026:** scaffold

## Notes

Robinson lab (UZH) is consolidating a coherent spatial-omics methods stack — DESpace and spatialFDA at EuroBioC2025, now sosta at GBCC2025. The pancreatic-islets IMC vignette is a good showcase: islet reconstruction is a textbook anatomical-structure problem, and getting it for free out of the cell-level data is the value proposition.
