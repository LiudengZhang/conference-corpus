# DESpace

**Discover spatially variable genes and differential spatial patterns across conditions** — a Bioconductor framework that uses negative binomial modeling (via edgeR) on pre-annotated spatial clusters to detect (a) genes whose expression varies across tissue space within a sample and (b) genes whose spatial expression *pattern* differs between experimental conditions.

- **Maintainer:** Peiying Cai (University of Zurich) — `peiying.cai@uzh.ch`
- **Bioconductor:** [DESpace v2.4.0](https://bioconductor.org/packages/release/bioc/html/DESpace.html)
- **Source:** [github.com/peicai/DESpace](https://github.com/peicai/DESpace)
- **Vignettes:** [Spatially variable genes (SVG)](https://bioconductor.org/packages/release/bioc/vignettes/DESpace/inst/doc/SVG.html) · [Differential spatial patterns (DSP)](https://bioconductor.org/packages/release/bioc/vignettes/DESpace/inst/doc/DSP.html)
- **License:** GPL-3
- **Status at EuroBioC2025:** methods talk on the differential-spatial-patterns (DSP) capability

## Talk at EuroBioC2025

- **Speaker:** Peiying Cai (University of Zurich)
- **Day / session:** Day 2 (Thu Sep 18, 2025) — morning short-talk session, before the Ferruz keynote
- **Talk title:** "DESpace for differential spatial patterns detection"
- **Slides (Zenodo DOI):** *to verify after publish — Bioconductor speakers typically deposit within ~2 weeks of the meeting*
- **Video:** not recorded — short talks at EuroBioC2025 were not part of the plenary YouTube playlist
- **Abstract / schedule:** [eurobioc2025 schedule](https://eurobioc2025.bioconductor.org/pages/schedule.html)

## What it does

DESpace takes spatial-transcriptomics counts plus a pre-annotated spatial cluster label (from any clustering pipeline) and asks two questions: (1) which genes vary significantly in expression across the spatial clusters within a single sample (SVG mode), and (2) which genes show *different* spatial expression patterns between conditions or samples (DSP mode). The DSP capability — the focus of the EuroBioC2025 talk — treats "pattern" as a first-class statistical object rather than running gene-by-gene SV testing per condition and post-hoc comparing.

## Where it fits in the corpus

- **AACR 2026:** no direct dossier; relevant axis is single-cell & spatial omics — DESpace is a methodological complement to the foundation-model-based spatial dossiers (Cell2Location, etc.) in the AACR vault
- **ISMB 2026:** scaffold; likely overlap on spatial-method talks
- **RECOMB 2026:** scaffold
- **GBCC 2025:** queued — possible overlap if Cai also presented there
- **Nextflow Summit 2026:** not mentioned

## Notes

Mature package (v2.4.0 in Bioconductor 3.23). Negative-binomial modeling via edgeR is a familiar substrate to the Bioconductor audience — that choice plus the explicit DSP framing is what differentiates DESpace from purely SVG-focused methods.
