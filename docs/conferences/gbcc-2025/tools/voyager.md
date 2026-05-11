# Voyager

**Exploratory spatial data analysis (ESDA) on Bioconductor spatial-omics objects with geospatial statistics** — a Bioconductor package by Lambda Moses (Caltech) that applies tools from geographic-information-systems and spatial statistics (Moran's I, local indicators of spatial association, variograms, Geary's C) to `SpatialFeatureExperiment` (SFE) data so spatial transcriptomics analysts can quantify spatial autocorrelation at the gene and cell level.

- **Maintainer:** Lambda Moses (Caltech) — `dlu2@caltech.edu`
- **Bioconductor:** [Voyager](https://bioconductor.org/packages/release/bioc/html/Voyager.html)
- **Companion package:** [SpatialFeatureExperiment](https://bioconductor.org/packages/release/bioc/html/SpatialFeatureExperiment.html) (SFE)
- **Source:** [github.com/pachterlab/voyager](https://github.com/pachterlab/voyager)
- **Project site:** [pachterlab.github.io/voyager](https://pachterlab.github.io/voyager/)
- **Paper (Voyager):** [Moses et al., bioRxiv 2023](https://www.biorxiv.org/content/10.1101/2023.07.20.549945)
- **Paper (SFE):** [Moses et al., *Nature Methods* 2025](https://pubmed.ncbi.nlm.nih.gov/40060564/) — "Geospatially informed representation of spatial genomics data with SpatialFeatureExperiment"
- **License:** Artistic-2.0
- **Status at GBCC2025:** methods talk applying the framework to lung adenocarcinoma Xenium data

## Talk at GBCC2025

- **Speakers:** Lambda Moses, Bianca Dumitrascu (Columbia)
- **Day / session:** Day 2 (Tue Jun 24, 2025) — Oral Session 2B, Grace Auditorium (chair: Vincent Carey)
- **Talk title:** "Multiscale analysis of lung adenocarcinoma spatial transcriptomics data"
- **Slides:** TBD
- **Video:** [GBCC2025 playlist](https://www.youtube.com/playlist?list=PLdl4u5ZRDMQTJ0O_FIO9ayqaUDfnMo4-4)
- **Abstract / schedule:** [GBCC2025 program](https://gbcc2025.bioconductor.org/program/scientific_program/)

## What it does

Voyager treats a spatial-transcriptomics sample as a geographic dataset: gene expression at each cell or spot is a value at a coordinate, and the natural questions are "where is it autocorrelated", "how do its patterns relate to a neighborhood graph", "what's the variogram". The package wraps `spdep` and related GIS-stats packages so that those tests can be run on `SpatialFeatureExperiment` objects (which carry geometries as Simple Features alongside the count matrix). The GBCC2025 talk extends this with multiscale analysis — patterns at fine-grained cellular scales often co-exist with coarser tissue-level patterns, and the LUAD case study demonstrates the package's ability to characterize both simultaneously and track how the scale–response profile shifts during tumor progression.

## Where it fits in the corpus

- **AACR 2026:** axis = single-cell & spatial omics; LUAD-specific spatial-progression dossier
- **OSTA** ([eurobioc entry](../../eurobioc-2025/tools/osta.md)) — Voyager is one of the canonical exploratory tools in the OSTA book
- **spatialLIBD** ([entry](spatiallibd.md)) — sister spatial-omics package, both target SpatialExperiment-family objects
- **SpatialData** ([eurobioc entry](../../eurobioc-2025/tools/spatialdata.md)) — Python-side counterpart; cross-language interop is an active direction
- **sosta** ([entry](sosta.md)) — same Day-3 session, also targets spatial-omics structure analysis
- **Nextflow Summit 2026:** not mentioned

## Notes

Voyager is the operational counterpart to SFE: SFE is the data structure, Voyager is the analysis layer. The multiscale angle in this GBCC talk is the methodological news — applying it to LUAD progression connects the geospatial-stats framing to a concrete cancer-biology question.
