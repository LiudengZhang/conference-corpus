# notame

**Workflow for non-targeted LC-MS metabolic profiling** — a Bioconductor package covering tabular preprocessing, quality control, and uni-/multi-variate analysis of untargeted LC-MS metabolomics data, packaging the recommendations from the *Metabolomics Data Processing and Data Analysis — Current Best Practices* special issue.

- **Maintainer:** Vilhelm Suksi (University of Turku) — `vksuks@utu.fi`
- **Bioconductor:** [notame v1.2.0](https://bioconductor.org/packages/release/bioc/html/notame.html)
- **Source:** [git.bioconductor.org/packages/notame](https://git.bioconductor.org/packages/notame)
- **Vignettes:** [Introduction](https://bioconductor.org/packages/release/vignettes/notame/inst/doc/introduction.html)
- **License:** MIT
- **Status at EuroBioC2025:** methods talk on the package's analysis workflow

## Talk at EuroBioC2025

- **Speaker:** Vilhelm Suksi (University of Turku)
- **Day / session:** Day 1 (Wed Sep 17, 2025) — morning short-talk session, after the Crowell keynote
- **Talk title:** "notame package for LC–MS metabolomics analysis"
- **Slides (Zenodo DOI):** *to verify after publish*
- **Video:** not recorded
- **Abstract / schedule:** [eurobioc2025 schedule](https://eurobioc2025.bioconductor.org/pages/schedule.html)

## What it does

notame is a one-stop workflow for untargeted LC-MS metabolomics: it ingests feature tables, runs QC visualizations and drift correction, performs univariate and multivariate analysis (PCA, PLS-DA, etc.), and emits diagnostic reports — a curated translation of the field's best-practice recommendations into runnable R.

## Where it fits in the corpus

- **AACR 2026:** no current dossier; relevant axis is bioinfo / AI methods (metabolomics is adjacent to the cancer-metabolism talks)
- **GBCC 2025:** queued
- **Nextflow Summit 2026:** not mentioned

## Notes

Mature workflow package (Bioconductor 3.23, v1.2.0). The value is curation more than novelty — converting consensus best-practice into one importable pipeline.
