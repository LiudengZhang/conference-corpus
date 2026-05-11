# scp + distributional inference (Beerland)

**Interpretable distributional inference for single-cell proteomics** — a methods extension layered on top of the `scp` Bioconductor package (UCLouvain-CBIO single-cell-proteomics framework) that models the *full distribution* of per-cell protein abundance rather than a point estimate, surfacing uncertainty and skew alongside the mean for interpretability.

- **Speaker / lead:** Lucas Beerland (affiliation TBD from slides — likely UCLouvain-CBIO Gatto-lab orbit given the scp connection)
- **Underlying framework:** [scp](https://www.bioconductor.org/packages/release/bioc/html/scp.html) (Christophe Vanderaa, Laurent Gatto, UCLouvain-CBIO)
- **scp source:** [github.com/UCLouvain-CBIO/scp](https://github.com/UCLouvain-CBIO/scp)
- **Standalone package:** *no public package name surfaced as of the talk* — methods extension presented; package release status TBD
- **Methodological lineage:** the talk explicitly builds on "Lindsey's Method" (a distributional regression technique); not the *bioRxiv* `distributional` R package per se
- **Status at EuroBioC2025:** methods short-talk — work-in-progress, no public package URL yet

## Talk at EuroBioC2025

- **Speaker:** Lucas Beerland
- **Day / session:** Day 1 (Wed Sep 17, 2025) — afternoon short-talk session, 2:45 PM
- **Talk title:** "Interpretable Distributional Inference in Single-Cell Proteomics"
- **Slides (Zenodo DOI):** *to verify after publish*
- **Video:** not recorded
- **Abstract / schedule:** [eurobioc2025 schedule](https://eurobioc2025.bioconductor.org/pages/schedule.html)

## What it does

Single-cell proteomics (SCP) is heteroskedastic, sparse, and right-skewed: a point-estimate-only summary collapses a lot of the cell-to-cell biological signal. The Beerland talk argues for *distributional* inference — modeling the per-cell protein-abundance distribution (mean, variance, skew, etc.) jointly — using a Lindsey's-method-flavored approach so that downstream differential analyses can flag cells/proteins where the *shape* of the distribution shifts even when the mean does not. The package is positioned as a method-layer on top of `scp`'s `SingleCellExperiment`/`QFeatures` data container rather than a replacement.

## Where it fits in the corpus

- **AACR 2026:** axis = single-cell & spatial omics (proteomics flank); distributional methods for SCP are an emerging methodology area
- **scp upstream:** [`scp`](https://www.bioconductor.org/packages/release/bioc/html/scp.html) is the canonical Bioconductor SCP processing package — Beerland's work sits atop it
- **GBCC 2025:** no direct SCP-distributional counterpart
- **Nextflow Summit 2026:** not mentioned

## Notes

No standalone package name was surfaced from the EuroBioC2025 schedule entry or the public summary — the talk is methods-first, with the implementation likely to surface as either an scp extension or a separate small package. Recheck the Zenodo DOI / a follow-up preprint when posted. Listed here as a flagged work-in-progress (external / pre-release) rather than a confirmed Bioconductor package.
