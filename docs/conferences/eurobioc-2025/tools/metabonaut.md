# Metabonaut

**Exploring and analyzing LC-MS data** — an online tutorial book and end-to-end workflows for LC-MS/MS metabolomics analysis using R/Bioconductor packages. Covers preprocessing, normalization, differential abundance, and annotation; ships a small example LC-MS/MS dataset for reproducible demos.

- **Maintainer:** Philippine Louail (RforMassSpectrometry community)
- **Source / install:** [github.com/rformassspectrometry/metabonaut](https://github.com/rformassspectrometry/metabonaut) · `BiocManager::install("rformassspectrometry/Metabonaut")` (not in Bioconductor release as of 3.23)
- **Website:** [rformassspectrometry.github.io/Metabonaut](https://rformassspectrometry.github.io/Metabonaut/)
- **R-universe:** [rformassspectrometry.r-universe.dev/Metabonaut](https://rformassspectrometry.r-universe.dev/Metabonaut)
- **Status at EuroBioC2025:** external / tutorial book (R-universe distribution)

## Talk at EuroBioC2025

- **Speaker:** Philippine Louail
- **Day / session:** Day 1 (Wed Sep 17, 2025) — morning short-talk session, after the Crowell keynote
- **Talk title:** "Metabonaut tutorials for metabolomics workflows"
- **Slides (Zenodo DOI):** *to verify after publish*
- **Video:** not recorded
- **Abstract / schedule:** [eurobioc2025 schedule](https://eurobioc2025.bioconductor.org/pages/schedule.html)

## What it does

Metabonaut is curriculum-shaped, not a method package: it walks LC-MS/MS metabolomics analysis end-to-end on the Bioconductor mass-spec stack (xcms, MsExperiment, Spectra, MetaboAnnotation, …) — preprocessing, normalization, differential abundance, and compound annotation — with a small example dataset embedded so each chapter is runnable.

## Where it fits in the corpus

- **AACR 2026:** axis = bioinfo / AI methods; metabolomics is adjacent to cancer-metabolism dossiers
- **notame** ([entry](notame.md)) — same LC-MS metabolomics audience and complementary roles (Metabonaut = curriculum, notame = workflow library)
- **SpectriPy** ([entry](spectripy.md)) — same Bioconductor mass-spec subcommunity (Johannes Rainer's group)
- **ISMB 2026:** scaffold
- **GBCC 2025:** queued

## Notes

Sister to notame in role — curriculum, not a method package. Useful as the "where to send a new lab member" link for anyone starting LC-MS metabolomics on the Bioconductor stack.
