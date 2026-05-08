# barbieQ

**Analyze barcode data from clonal tracking experiments** — statistical tools for barcode count data from cell clonal tracking experiments, where each clone carries a unique inherited barcode; supports preprocessing, statistical testing, and visualization of clone abundance changes under experimental conditions.

- **Maintainer:** Liyang Fei (Peter MacCallum Cancer Centre) — `liyang.fei@petermac.org`
- **Bioconductor:** [barbieQ v1.4.0](https://bioconductor.org/packages/release/bioc/html/barbieQ.html)
- **Source:** [git.bioconductor.org/packages/barbieQ](https://git.bioconductor.org/packages/barbieQ)
- **Vignettes:** [barbieQ introduction](https://bioconductor.org/packages/release/vignettes/barbieQ/inst/doc/barbieQ.html)
- **License:** GPL-3
- **Status at EuroBioC2025:** methods talk on clonal-tracking statistics

## Talk at EuroBioC2025

- **Speaker:** Liyang Fei (Peter MacCallum Cancer Centre)
- **Day / session:** Day 2 (Thu Sep 18, 2025) — late-morning short-talk session, before the Ferruz keynote
- **Talk title:** "barbieQ package for clonal tracking barcode analysis"
- **Slides (Zenodo DOI):** *to verify after publish*
- **Video:** not recorded
- **Abstract / schedule:** [eurobioc2025 schedule](https://eurobioc2025.bioconductor.org/pages/schedule.html)

## What it does

barbieQ ingests barcode count tables from clonal-tracking experiments (lentiviral or CRISPR-based barcode libraries delivered into cell populations), performs preprocessing and quality filtering, runs statistical tests for differential clone abundance across experimental conditions, and visualizes how individual clones expand or contract over time. The package is built around a dedicated barcode-experiment data class so that downstream comparisons stay aware of clone-level structure rather than collapsing to bulk counts.

## Where it fits in the corpus

- **AACR 2026:** clinical-trials axis — clonal tracking is heavily used for drug-resistance and metastasis lineage analysis, which is core AACR territory
- **ISMB 2026:** scaffold
- **GBCC 2025:** queued
- **Nextflow Summit 2026:** not mentioned (different ecosystem)

## Notes

Cancer-research relevance: clonal tracking sees use in CRISPR screens, drug-resistance studies, and metastasis seeding experiments — direct overlap with AACR's clinical-research lineage analyses, and one of the more clinically-anchored methods talks at EuroBioC2025.
