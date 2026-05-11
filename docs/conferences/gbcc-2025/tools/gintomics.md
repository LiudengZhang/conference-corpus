# gINTomics

**Multi-omics data integration and visualization** — a Bioconductor package that identifies associations between a target gene's expression and its regulatory factors (Copy Number Variations, methylation), bundling the integration models with a Shiny app for interactive exploration of the results.

- **Maintainer:** Angelo Velle (University of Padua) — `angelo.velle@unipd.it`
- **Bioconductor:** [gINTomics v1.8.0](https://bioconductor.org/packages/release/bioc/html/gINTomics.html)
- **Source:** [github.com/angelovelle96/gINTomics](https://github.com/angelovelle96/gINTomics)
- **Vignettes:** [gINTomics intro](https://bioconductor.org/packages/release/bioc/vignettes/gINTomics/inst/doc/gINTomics.html)
- **License:** AGPL-3
- **Status at GBCC2025:** methods talk on multi-omics integration

## Talk at GBCC2025

- **Speakers:** Angelo Velle, Francesco Patanè, Chiara Romualdi (University of Padua)
- **Day / session:** Day 2 (Tue Jun 24, 2025) — Oral Session 2A, Bush Hall (chair: Jenny Drnevich)
- **Talk title:** "gINTomics, a powerful Bioconductor package for multiomics data integration and visualization"
- **Slides (Zenodo DOI):** *TBD — Zenodo deposits typically 2–4 weeks post-conference*
- **Video:** [GBCC2025 playlist](https://www.youtube.com/playlist?list=PLdl4u5ZRDMQTJ0O_FIO9ayqaUDfnMo4-4)
- **Abstract / schedule:** [GBCC2025 program](https://gbcc2025.bioconductor.org/program/scientific_program/)

## What it does

gINTomics ties expression data to its regulatory layer — CNV and methylation — and tests for associations gene by gene. The output is a per-target model surfaced through a Shiny-based app, so the integration step and the visualization step ship together rather than expecting the user to wire one to the other. The Romualdi lab's positioning is "powerful + visual" rather than "novel statistics."

## Where it fits in the corpus

- **AACR 2026:** axis bioinfo / AI methods — gINTomics is one of the multi-omics-integration tools relevant to the cancer-genomics dossiers
- **MOSClip** ([entry](../../eurobioc-2025/tools/mosclip.md)) — same lab family; both are multi-omics integration packages, but MOSClip is survival-focused while gINTomics is regulator-association-focused with explicit visualization
- **ISMB 2026:** scaffold
- **Nextflow Summit 2026:** not mentioned

## Notes

Mature package (Bioconductor 3.23, v1.8.0). The differentiator versus MOSClip and the broader multi-omics ecosystem is the embedded Shiny app — Romualdi's group is consolidating an "integration + interactive exploration" workflow rather than shipping a bare modeling library.
