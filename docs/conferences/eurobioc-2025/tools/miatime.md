# miaTime

**Microbiome time series analysis** — a Bioconductor package providing tools for longitudinal microbiome studies on top of the (Tree)SummarizedExperiment infrastructure. Sister to the broader `mia` framework.

- **Maintainer:** Tuomas Borman (University of Turku) — `tuomas.v.borman@utu.fi`
- **Bioconductor:** [miaTime v1.2.0](https://bioconductor.org/packages/release/bioc/html/miaTime.html)
- **Source:** [git.bioconductor.org/packages/miaTime](https://git.bioconductor.org/packages/miaTime)
- **Vignettes:** [miaTime guide](https://bioconductor.org/packages/3.23/bioc/vignettes/miaTime/inst/doc/miaTime.html)
- **License:** Artistic-2.0
- **Status at EuroBioC2025:** methods talk on the longitudinal extension

## Talk at EuroBioC2025

- **Speaker:** Geraldson T. Muluh
- **Day / session:** Day 1 (Wed Sep 17, 2025) — morning short-talk session, after the Crowell keynote
- **Talk title:** "miaTime framework for longitudinal microbiome studies"
- **Slides (Zenodo DOI):** *to verify after publish*
- **Video:** not recorded
- **Abstract / schedule:** [eurobioc2025 schedule](https://eurobioc2025.bioconductor.org/pages/schedule.html)

## What it does

miaTime layers time-aware analyses (e.g. trajectories, time-resolved dissimilarity, change-point detection) on top of `mia`'s TreeSummarizedExperiment containers. The split keeps the core `mia` package focused on cross-sectional analyses while letting longitudinal users opt in to the time-series surface separately.

## Where it fits in the corpus

- **AACR 2026:** no current dossier
- **mia** ([entry](mia.md)) — base package; miaTime extends it for time-series studies
- **GBCC 2025:** queued

## Notes

Borman maintains both `mia` and `miaTime` (and presented the `mia` workshop on Day 2). The two-package split mirrors the `Bioconductor` convention of keeping core data classes separate from method extensions.
