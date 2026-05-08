# OSTA — Orchestrating Spatial Transcriptomics Analysis with Bioconductor

**Open-source online book and companion data package** — reproducible code examples and end-to-end workflows for spatial-omics analysis using Bioconductor in R, including interoperability with Python; the companion `OSTA.data` package ships example datasets across multiple spatial-omics platforms.

- **Maintainer (data package):** Yixing E. Dong — `estelladong729@gmail.com`
- **Authors:** Helena L. Crowell, Yixing Dong, Ilaria Billato, Peiying Cai, Martin Emons, Lukas Weber, Stephanie Hicks, Ellis Patrick, Mark Robinson, Vince Carey, others
- **Bioconductor (companion data):** [OSTA.data v1.4.0](https://bioconductor.org/packages/release/bioc/html/OSTA.data.html)
- **Book:** [bioconductor.org/books/OSTA/](https://bioconductor.org/books/OSTA/)
- **Source:** [github.com/lmweber/OSTA](https://github.com/lmweber/OSTA)
- **License:** Artistic-2.0
- **Status at EuroBioC2025:** workshop / book in active development

## Workshop at EuroBioC2025

- **Presenters:** Yixing Dong & Ellis Patrick
- **Day / session:** Day 2 (Thu Sep 18, 2025) — afternoon hands-on workshop (parallel with mia, msqrob2, Workshop Platform, iSEE)
- **Workshop title:** "OSTA: Orchestrating Spatial Transcriptomics Analysis with Bioconductor"
- **Format:** hands-on tutorial walking through book chapters using `OSTA.data` example datasets
- **Workshop materials:** [github.com/lmweber/OSTA](https://github.com/lmweber/OSTA) and [bioconductor.org/books/OSTA/](https://bioconductor.org/books/OSTA/)
- **Video:** workshops not recorded; the Bioconductor YouTube playlist covers plenaries only
- **Abstract / schedule:** [eurobioc2025 schedule](https://eurobioc2025.bioconductor.org/pages/schedule.html)

## What it does

OSTA is an online textbook (in the OSCA / OHCA tradition) that walks through spatial-transcriptomics analysis end-to-end on the Bioconductor stack — preprocessing, QC, normalization, clustering, spatially-variable-gene detection, cell-type deconvolution, and cross-language interop with Python. The companion `OSTA.data` Bioconductor package provides the example datasets across multiple spatial-omics platforms (Visium, Xenium, MERFISH, etc.) so every chapter is runnable.

## Where it fits in the corpus

- **AACR 2026:** axis = single-cell & spatial omics — OSTA is the curricular spine for the R/Bioconductor side of the spatial-omics dossiers
- **DESpace** ([entry](despace.md)) — Peiying Cai is both the DESpace presenter and an OSTA author; OSTA is the natural place a DESpace tutorial would live
- **SpatialData** ([entry](spatialdata.md)) — the Python-side framework that OSTA's interop chapters bridge to
- **Helena Crowell Day 1 keynote** — overlaps directly; Crowell is both a keynote speaker and an OSTA author
- **ISMB 2026:** scaffold; spatial-omics tracks
- **GBCC 2025:** queued

## Notes

OSTA is the consensus textbook around which much of the European spatial-omics Bioconductor work is converging. Tracking OSTA chapter additions is a good proxy for which spatial methods the Bioc community considers stable enough to teach.
