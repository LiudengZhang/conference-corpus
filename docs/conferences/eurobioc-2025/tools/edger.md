# edgeR

**Empirical Analysis of Digital Gene Expression Data in R** — the foundational Bioconductor package for differential expression analysis of sequence count data using negative binomial distributions, including empirical Bayes estimation, exact tests, GLMs, quasi-likelihood methods, and gene-set enrichment; supports RNA-seq, ChIP-seq, ATAC-seq, Bisulfite-seq, SAGE, CAGE, metabolomics, and proteomics spectral counts at gene or isoform level.

- **Maintainer:** Yunshun Chen, Gordon Smyth, Aaron Lun, Mark Robinson — `yuchen@wehi.edu.au`; `smyth@wehi.edu.au`
- **Bioconductor:** [edgeR v4.10.0](https://bioconductor.org/packages/release/bioc/html/edgeR.html)
- **Source:** [git.bioconductor.org/packages/edgeR](https://git.bioconductor.org/packages/edgeR)
- **Vignettes:** [Introduction](https://bioconductor.org/packages/release/bioc/vignettes/edgeR/inst/doc/intro.html)
- **License:** GPL (>=2)
- **Status at EuroBioC2025:** major update (v4 expansion)

## Talk at EuroBioC2025

- **Speaker:** Lizhong Chen (WEHI)
- **Day / session:** Day 1 (Wed Sep 17, 2025) — afternoon short-talk session, after the Holmes keynote
- **Talk title:** "edgeR v4 functionality expansion"
- **Slides (Zenodo DOI):** *to verify after publish*
- **Video:** not recorded — short talks at EuroBioC2025 were not part of the plenary YouTube playlist
- **Abstract / schedule:** [eurobioc2025 schedule](https://eurobioc2025.bioconductor.org/pages/schedule.html)

## What it does

edgeR fits negative-binomial GLMs to count data and tests for differential abundance using exact tests, likelihood-ratio tests, or quasi-likelihood F-tests, with empirical-Bayes shrinkage of dispersions. It is technology-agnostic across count-based assays — RNA-seq, ChIP/ATAC-seq, BS-seq, SAGE/CAGE, spectral-count proteomics — and operates at gene or isoform resolution.

## Where it fits in the corpus

- **AACR 2026:** no current dossier as a standalone tool, but edgeR is the substrate underlying many AACR transcriptomic analyses
- **DESpace** ([entry](despace.md)) — builds directly on edgeR's NB modeling for spatial cluster testing
- **GBCC 2025:** queued
- **Nextflow Summit 2026:** not mentioned directly; nf-core RNA-seq pipelines commonly hand off to edgeR downstream

## Notes

edgeR is the substrate for many other Bioconductor packages; the v4 expansion broadens single-cell and sparse-count handling, which is what the WEHI talk is foregrounding.
