# omicsGMF

**Generalized matrix factorization for omics dimensionality reduction** — performs matrix factorization for dimensionality reduction, visualization, and imputation of RNA-seq, proteomics, and single-cell omics data without requiring log-transformation, with built-in batch-effect correction via covariate adjustment and missing-value handling.

- **Maintainer:** Alexandre Segers — `alexandresegers@outlook.com`
- **Bioconductor:** [omicsGMF v1.2.0](https://bioconductor.org/packages/release/bioc/html/omicsGMF.html)
- **Source:** [git.bioconductor.org/packages/omicsGMF](https://git.bioconductor.org/packages/omicsGMF)
- **Vignettes:** [Proteomics](https://bioconductor.org/packages/release/bioc/vignettes/omicsGMF/inst/doc/Proteomics-vignette.html) · [RNA-Seq](https://bioconductor.org/packages/release/bioc/vignettes/omicsGMF/inst/doc/RNASeq-vignette.html)
- **License:** Artistic-2.0
- **Status at EuroBioC2025:** methods talk on proteomics-specific application

## Talk at EuroBioC2025

- **Speaker:** Lieven Clement (Ghent University) — senior author
- **Day / session:** Day 1 (Wed Sep 17, 2025) — morning short-talk session, after the Crowell keynote
- **Talk title:** "omicsGMF for proteomics dimensionality reduction"
- **Slides (Zenodo DOI):** *to verify after publish*
- **Video:** not recorded
- **Abstract / schedule:** [eurobioc2025 schedule](https://eurobioc2025.bioconductor.org/pages/schedule.html)

## What it does

omicsGMF takes counts (or intensities) plus a sample-covariate matrix and returns a low-dimensional factorization that simultaneously denoises, imputes, and corrects for known batch covariates. It accepts SummarizedExperiment, SingleCellExperiment, and QFeatures inputs, so it slots cleanly into existing Bioconductor pipelines — RNA-seq, bulk proteomics, single-cell proteomics — without an upstream log step.

## Where it fits in the corpus

- **AACR 2026:** no current dossier; relevant axis is bioinfo / AI methods
- **GBCC 2025:** queued
- **iSEE** ([entry](isee.md)) — natural visualization substrate for the factorization output

## Notes

Lieven Clement's group (UGent) is a frequent EuroBioC contributor — also behind msqrob2. omicsGMF complements that line of work by being agnostic to the input modality.
