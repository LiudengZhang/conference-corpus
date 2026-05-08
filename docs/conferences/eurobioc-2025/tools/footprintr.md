# footprintR

**Tools for working with single-molecule footprinting data** — reads base modifications from BAM files or `modkit` output, represents single-molecule footprinting data efficiently as R objects, and provides functions to manipulate and visualize them. Output is a `SummarizedExperiment` with positions × samples and assays for modified/total base counts.

- **Authors:** Charlotte Soneson, Panagiotis Papasaikas, Sebastien Smallwood, Michael Stadler — FMI Basel (Friedrich Miescher Institute)
- **Source / install:** [github.com/fmicompbio/footprintR](https://github.com/fmicompbio/footprintR) · `BiocManager::install("fmicompbio/footprintR")` (not in Bioconductor release as of 3.23)
- **Pkgdown:** [fmicompbio.github.io/footprintR](https://fmicompbio.github.io/footprintR/)
- **Status at EuroBioC2025:** external / GitHub-distributed (Bioconductor submission likely pending)

## Talk at EuroBioC2025

- **Speaker:** Charlotte Soneson (FMI Basel)
- **Day / session:** Day 2 (Thu Sep 18, 2025) — morning short-talk session, after the Sharpe keynote
- **Talk title:** "footprintR for single molecule footprinting data"
- **Slides (Zenodo DOI):** *to verify after publish*
- **Video:** not recorded — short talks at EuroBioC2025 were not part of the plenary YouTube playlist
- **Abstract / schedule:** [eurobioc2025 schedule](https://eurobioc2025.bioconductor.org/pages/schedule.html)

## What it does

footprintR ingests base-modification calls (from BAM files or from `modkit`) and lays them out as a `SummarizedExperiment` keyed by genomic position × sample, with assays for modified and total base counts. From there it provides manipulation and visualization functions tailored to single-molecule footprinting (SMF) experiments — where exogenous methyltransferase footprints reveal TF binding at single-DNA-molecule resolution.

## Where it fits in the corpus

- **AACR 2026:** axis = epigenomics / regulatory genomics; SMF is a niche but powerful TF-binding readout
- **ISMB 2026:** scaffold; epigenomics methods
- **GBCC 2025:** queued
- **Nextflow Summit 2026:** not mentioned — modkit upstream is CLI-based but the analysis side is R

## Notes

Single-molecule footprinting (SMF) reads out TF binding at single-DNA-molecule resolution by exposing chromatin to an exogenous methyltransferase whose footprint marks bound vs. unbound DNA. footprintR sits downstream of `modkit` calls and is complementary to the older `SingleMoleculeFootprinting` package on Bioconductor — same FMI lineage, more modern data structures.
