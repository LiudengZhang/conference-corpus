# SpatialData

**An open and universal data framework for spatial omics** — a FAIR storage format and Python library collection for performant access, alignment, and processing of multi-modal spatial-omics datasets. Cross-language interop with R/Bioconductor is an active development direction and the focus of the EuroBioC2025 talk.

- **Authors / community:** scverse community — lead authors Luca Marconato, Giovanni Palla, Kevin A. Yamauchi, Helena Crowell
- **Upstream framework:** [github.com/scverse/spatialdata](https://github.com/scverse/spatialdata) (Python-primary; R interop layer in development)
- **Paper:** [Marconato et al., *Nature Methods* 2024](https://www.nature.com/articles/s41592-024-02212-x)
- **Status at EuroBioC2025:** external / pre-release in R (Python framework mature; R interop in development — focus of the talk)

## Talk at EuroBioC2025

- **Speaker:** Luca Marconato (lead Python author)
- **Day / session:** Day 2 (Thu Sep 18, 2025) — late-morning short-talk session, before the Ferruz keynote
- **Talk title:** "SpatialData framework for cross-language interoperability"
- **Slides:** [Zenodo 10.5281/zenodo.17293885](https://zenodo.org/records/17293885) (Marconato et al. — cross-community spatial-biology talk)
- **Video:** not recorded
- **Abstract / schedule:** [eurobioc2025 schedule](https://eurobioc2025.bioconductor.org/pages/schedule.html)

## What it does

SpatialData defines a Zarr-backed FAIR storage format and a Python library stack for multi-modal spatial-omics data — co-registered images, tables, shapes (cells, regions), and points (transcripts) — with consistent transforms for alignment across modalities. The Bioconductor angle is interop: how `SpatialExperiment` / `SingleCellExperiment` objects round-trip to and from on-disk SpatialData stores so an R analyst can pick up a scverse-prepared dataset (or vice versa) without losing structure.

## Where it fits in the corpus

- **AACR 2026:** axis = single-cell & spatial omics; SpatialData is the de facto Python-side data substrate for spatial-omics pipelines
- **OSTA** ([entry](osta.md)) — both target spatial omics; OSTA covers the R/Bioc side, SpatialData covers Python with R-interop being the bridge
- **Helena Crowell Day 1 keynote** — Crowell is one of the SpatialData co-authors
- **ISMB 2026:** scaffold; scverse + spatial methods
- **GBCC 2025:** queued

## Notes

This is the cross-language bridge between scverse (Python) and the Bioconductor `SpatialExperiment` / OSTA-book ecosystem. Watching the R-interop layer mature is one of the more consequential storylines for the spatial-omics axis across both EuroBioC and the AACR vault's spatial dossiers.
