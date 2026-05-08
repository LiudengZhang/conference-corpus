# MOSClip

**Multi Omics Survival Clip** — a topological pathway analysis tool that integrates multi-omics data to identify survival-associated modules and significant modules for two-class analysis, providing both pathway tests and module tests.

- **Maintainer:** Paolo Martini (University of Brescia) — `paolo.martini@unibs.it`
- **Bioconductor:** [MOSClip v1.6.0](https://bioconductor.org/packages/release/bioc/html/MOSClip.html)
- **Source:** [git.bioconductor.org/packages/MOSClip](https://git.bioconductor.org/packages/MOSClip)
- **Vignettes:** [MOSClip vignette](https://bioconductor.org/packages/release/vignettes/MOSClip/inst/doc/mosclip_vignette.html)
- **License:** AGPL-3
- **Status at EuroBioC2025:** methods talk on multi-omics survival pathway analysis

## Talk at EuroBioC2025

- **Speaker:** Anna C E De Lima Tanada (presented; Paolo Martini is maintainer / senior author)
- **Day / session:** Day 1 (Wed Sep 17, 2025) — afternoon short-talk session, after the Holmes keynote
- **Talk title:** "MOSClip for multi-omics pathway analysis"
- **Slides (Zenodo DOI):** *to verify after publish*
- **Video:** not recorded — short talks at EuroBioC2025 were not part of the plenary YouTube playlist
- **Abstract / schedule:** [eurobioc2025 schedule](https://eurobioc2025.bioconductor.org/pages/schedule.html)

## What it does

MOSClip overlays multi-omics measurements onto pathway topology and tests pathway modules for association with survival or two-class outcomes. It returns both a pathway-level test and a finer-grained module-level test, so users can localize *which* part of a pathway carries the signal rather than only learning that the pathway is hit.

## Where it fits in the corpus

- **AACR 2026:** no current dossier; relevant axis is clinical-trials / survival modeling — MOSClip's explicit survival framing maps onto outcome-prediction talks
- **MIRit** ([entry](mirit.md)) — sibling network/pathway method on the same Day 1 short-talk session
- **GBCC 2025:** queued
- **Nextflow Summit 2026:** not mentioned

## Notes

Multi-omics with explicit survival modeling — distinct from purely descriptive multi-omics methods. The module-level test is the differentiator: it pushes interpretation below the pathway aggregate.
