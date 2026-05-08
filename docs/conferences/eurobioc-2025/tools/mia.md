# mia

**Microbiome analysis** — tools for microbiome analysis based on the `SummarizedExperiment`, `SingleCellExperiment`, and `TreeSummarizedExperiment` infrastructure; focuses on data handling and analysis for taxonomic information including community indices and data summarization.

- **Maintainer:** Tuomas Borman (University of Turku) — `tuomas.v.borman@utu.fi`
- **Bioconductor:** [mia v1.20.0](https://bioconductor.org/packages/release/bioc/html/mia.html)
- **Source:** [git.bioconductor.org/packages/mia](https://git.bioconductor.org/packages/mia)
- **Vignettes:** [mia introduction](https://bioconductor.org/packages/release/bioc/vignettes/mia/inst/doc/mia.html)
- **License:** Artistic-2.0
- **Status at EuroBioC2025:** mature package, workshop

## Workshop at EuroBioC2025

- **Presenter:** Tuomas Borman (University of Turku)
- **Day / session:** Day 2 (Thu Sep 18, 2025) — afternoon hands-on workshop (parallel with OSTA, msqrob2, Workshop Platform, iSEE)
- **Workshop title:** "Orchestrating Microbiome Analysis with Bioconductor"
- **Format:** hands-on tutorial, attendees follow vignettes in their own R session
- **Workshop materials:** *to verify — typically a per-event GitHub repo from the microbiome group*
- **Video:** workshops not recorded; the Bioconductor YouTube playlist covers plenaries only
- **Abstract / schedule:** [eurobioc2025 schedule](https://eurobioc2025.bioconductor.org/pages/schedule.html)

## What it does

mia wraps microbiome count and taxonomy data into a `TreeSummarizedExperiment` so that taxonomic hierarchy, sample metadata, and feature counts live in one S4 object compatible with the rest of Bioconductor. On top of that substrate it provides community indices (alpha/beta diversity, dominance, divergence), data transformation utilities, and per-rank aggregation — the layer most downstream microbiome analyses (`miaViz`, `miaTime`, miaDash) sit on.

## Where it fits in the corpus

- **AACR 2026:** no direct dossier; microbiome analyses surface in tumor-microbiome and gut-microbiome / immunotherapy talks
- **miaTime** ([entry](miatime.md)) — extends mia for longitudinal microbiome studies
- **ISMB 2026:** scaffold
- **GBCC 2025:** queued — mia workshops are recurring fixtures
- **Nextflow Summit 2026:** not mentioned (different ecosystem)

## Notes

mia is the canonical Bioconductor microbiome data class. Workshop substrate is the OMA (Orchestrating Microbiome Analysis) book also from this group, which is the de-facto entry point for new users.
