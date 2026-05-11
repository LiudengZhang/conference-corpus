# HistoImagePlot

**Side-by-side visualization of tissue thumbnails and HoVer-Net cell-segmentation output in R/Bioconductor** — an Ilaria Billato package (Waldron lab) for importing HoVer-Net nuclear-segmentation results from histopathology images into Bioconductor spatial-data structures, producing colored-by-cell-type segmentation overlays alongside the source H&E thumbnail.

- **Maintainer:** Ilaria Billato (University of Padova) — `ilaria.billato@phd.unipd.it`
- **Bioconductor:** [HistoImagePlot](https://bioconductor.org/packages/release/bioc/html/HistoImagePlot.html)
- **Source:** [github.com/waldronlab/HistoImagePlot](https://github.com/waldronlab/HistoImagePlot)
- **Vignettes:** [Exploring HoverNet Features from imageFeatureTCGA](https://bioconductor.org/packages/release/bioc/vignettes/HistoImagePlot/inst/doc/HistoImagePlot.html)
- **License:** Artistic-2.0
- **Status at EuroBioC2025:** methods talk on a Bioconductor framework for histopathological-image integration with multi-omics data

## Talk at EuroBioC2025

- **Speaker:** Ilaria Billato (University of Padova)
- **Day / session:** Day 2 (Thu Sep 18, 2025) — late-morning short-talk session (11:00 AM)
- **Talk title:** "A standardized R/Bioconductor framework for integrative analysis of histopathological images with multi-omics data"
- **Companion package:** **ImageTCGA** — Shiny application for visualizing image-derived features alongside TCGA multi-omics data
- **Slides (Zenodo DOI):** *to verify after publish*
- **Video:** not recorded
- **Abstract / schedule:** [eurobioc2025 schedule](https://eurobioc2025.bioconductor.org/pages/schedule.html)

## What it does

HistoImagePlot bridges the gap between a deep-learning histopathology pipeline (HoVer-Net for simultaneous nuclear segmentation and classification) and a Bioconductor spatial-data workflow. It ingests HoVer-Net's per-nucleus output, lays it back over the tissue thumbnail, and produces side-by-side visualizations colored by predicted cell-type label — making the segmentation inspectable as part of a standard R analysis rather than a separate image-viewer step. The companion **ImageTCGA** Shiny app extends the same primitives to TCGA cohorts, letting an analyst link image-derived morphology features back to the multi-omics layer for the same sample.

## Where it fits in the corpus

- **AACR 2026:** axis = bioinfo / AI methods (digital pathology); HistoImagePlot is exactly the kind of small bridge package that lets a histopathology AI model show up inside a Bioc analysis
- **OSTA** ([entry](osta.md)) — Billato is an OSTA author; HistoImagePlot is the operational H&E-side analogue to OSTA's transcriptomic-side framework
- **GBCC 2025:** Billato also gave a related talk at GBCC2025 Day 3 (Oral Session 3) — "A standardized R/Bioconductor framework for integrative analysis of histopathological images with multi-omics data" (with Marcel Ramos Pérez) — cross-walked storyline
- **Nextflow Summit 2026:** not mentioned

## Notes

The Bioconductor release of HistoImagePlot anchors the talk in something concrete and inspectable. The standardization framing (`ImageTCGA` + `HistoImagePlot` as the visualization layer + a planned `SpatialFeatureExperiment`-style container for image features) is the longer-arc story; expect more package releases from the same group threading image features into the broader OSTA / `SpatialExperiment` ecosystem.
