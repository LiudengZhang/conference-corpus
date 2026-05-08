# consICA

**Consensus Independent Component Analysis** — data-driven deconvolution method using consensus ICA to decompose heterogeneous omics data and extract features for patient diagnostics and prognostics.

- **Maintainer:** Petr V. Nazarov — `petr.nazarov@lih.lu`
- **Bioconductor:** [consICA v2.10.0](https://bioconductor.org/packages/release/bioc/html/consICA.html)
- **Source:** [git.bioconductor.org/packages/consICA](https://git.bioconductor.org/packages/consICA)
- **Vignettes:** [consICA introduction](https://bioconductor.org/packages/release/bioc/vignettes/consICA/inst/doc/ConsICA.html)
- **License:** MIT
- **Status at EuroBioC2025:** methods talk on signal decomposition for omics deconvolution

## Talk at EuroBioC2025

- **Speaker:** Maryna Chepeleva (presented; Nazarov is the maintainer / senior author)
- **Day / session:** Day 2 (Thu Sep 18, 2025) — late-morning short-talk session, before the Ferruz keynote
- **Talk title:** "consICA for functional signal decomposition"
- **Slides (Zenodo DOI):** *to verify after publish*
- **Video:** not recorded
- **Abstract / schedule:** [eurobioc2025 schedule](https://eurobioc2025.bioconductor.org/pages/schedule.html)

## What it does

consICA runs Independent Component Analysis many times with different initializations, then aggregates the results into stable consensus components — the "consensus" step is what turns ICA from a stochastic exploratory method into a reproducible deconvolution tool. The output is a set of statistically independent signal components extracted from heterogeneous omics data, with downstream utilities for linking components to patient survival, clinical covariates, and gene-set enrichment.

## Where it fits in the corpus

- **AACR 2026:** no current dossier; relevant axis is bioinfo / AI methods — consICA complements PCA/NMF/omicsGMF dimensionality reduction with an ICA-based alternative
- **omicsGMF** ([entry](omicsgmf.md)) — adjacent matrix-factorization framing, different statistical assumptions
- **ISMB 2026:** scaffold
- **GBCC 2025:** queued
- **Nextflow Summit 2026:** not mentioned

## Notes

ICA-based deconvolution — explicitly oriented toward extracting clinically interpretable signal components, with the consensus step addressing the standard ICA reproducibility concern.
