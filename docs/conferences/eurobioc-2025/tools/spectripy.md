# SpectriPy

**Cross-language mass spectrometry: bridging R Spectra and Python matchms** — enables R users of the `Spectra` package to call Python MS analysis code (matchms, MS-similarity scoring, etc.) without leaving R, and vice versa.

- **Maintainer:** Johannes Rainer (Eurac Research) — `Johannes.Rainer@eurac.edu`
- **Bioconductor:** [SpectriPy v1.2.0](https://bioconductor.org/packages/release/bioc/html/SpectriPy.html)
- **Source:** [git.bioconductor.org/packages/SpectriPy](https://git.bioconductor.org/packages/SpectriPy)
- **Vignettes:** [SpectriPy guide](https://bioconductor.org/packages/release/vignettes/SpectriPy/inst/doc/SpectriPy.html)
- **License:** Artistic-2.0
- **Status at EuroBioC2025:** methods talk on cross-language integration

## Talk at EuroBioC2025

- **Speaker:** Johannes Rainer (Eurac Research)
- **Day / session:** Day 1 (Wed Sep 17, 2025) — morning short-talk session, after the Crowell keynote
- **Talk title:** "SpectriPy for cross-language mass spectrometry analysis"
- **Slides (Zenodo DOI):** *to verify after publish*
- **Video:** not recorded
- **Abstract / schedule:** [eurobioc2025 schedule](https://eurobioc2025.bioconductor.org/pages/schedule.html)

## What it does

SpectriPy converts R `Spectra` objects to and from Python MS data structures, then wraps Python similarity-scoring functions from `matchms` so they can be called from R as if they were native. The practical effect: R-pipeline authors can pull in Python MS-ML models without rewriting them, and Python authors can ship their work to R-heavy MS communities.

## Where it fits in the corpus

- **AACR 2026:** no current dossier; cross-language interop is conceptually adjacent to AACR's pathology FM dossiers (also Python-trained, R-consumed)
- **GBCC 2025:** queued
- **Nextflow Summit 2026:** related axis (workflow-level cross-language interop)

## Notes

Same author (Rainer) maintains the `xcms` package for raw LC-MS preprocessing — SpectriPy slots downstream of `xcms`'s output.
