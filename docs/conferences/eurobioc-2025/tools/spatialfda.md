# spatialFDA

**A tool for spatial multi-sample comparisons** — calculates spatial statistics from `SpatialExperiment` objects using `spatstat`, then compares functions across samples via functional additive models (`refund`); provides exploratory visualizations through functional principal component analysis.

- **Maintainer:** Martin Emons (UZH) — `martin.emons@uzh.ch`
- **Bioconductor:** [spatialFDA v1.4.0](https://bioconductor.org/packages/release/bioc/html/spatialFDA.html)
- **Source:** [git.bioconductor.org/packages/spatialFDA](https://git.bioconductor.org/packages/spatialFDA)
- **Vignettes:** [Diabetes Islet Example](https://bioconductor.org/packages/release/bioc/vignettes/spatialFDA/inst/doc/DiabetesIsletExample.html)
- **License:** GPL (>=3)
- **Status at EuroBioC2025:** methods talk on cross-sample spatial comparison

## Talk at EuroBioC2025

- **Speaker:** Martin Emons (UZH)
- **Day / session:** Day 2 (Thu Sep 18, 2025) — late-morning short-talk session, before the Ferruz keynote
- **Talk title:** "spatialFDA for differential co-localization analysis"
- **Slides (Zenodo DOI):** *to verify after publish*
- **Video:** not recorded
- **Abstract / schedule:** [eurobioc2025 schedule](https://eurobioc2025.bioconductor.org/pages/schedule.html)

## What it does

spatialFDA takes a `SpatialExperiment` and computes spatial summary functions (Ripley's K, pair correlation, mark correlation, etc.) per sample via `spatstat`, then treats each sample's function as a functional observation that can be compared across conditions through functional additive models implemented in `refund`. Functional principal component analysis surfaces the dominant modes of variation across samples, turning "how does co-localization differ between groups?" into a tractable statistical question.

## Where it fits in the corpus

- **AACR 2026:** no current dossier; relevant axis is single-cell & spatial omics — spatialFDA addresses the multi-sample comparison gap that most spatial-omics dossiers in the AACR vault leave open
- **DESpace** ([entry](despace.md)) — cousin tool from the same Zurich orbit, but DESpace targets within/between-cluster SVG/DSP while spatialFDA targets cross-sample functional comparisons
- **ISMB 2026:** scaffold; likely overlap on spatial-method talks
- **GBCC 2025:** queued
- **Nextflow Summit 2026:** not mentioned

## Notes

Functional Data Analysis treatment of spatial co-localization — moves beyond single-sample SVG to multi-sample comparisons, which is where most cancer-spatial cohorts actually live.
