# msqrob2

**Robust statistical inference for quantitative LC-MS proteomics** — robust linear mixed model framework for differential abundance assessment in mass spectrometry proteomics; supports raw peptide intensities or summarized protein values, with stabilization through ridge regression, empirical Bayes variance estimation, and robust M-estimation; the hurdle workflow handles missing data without imputation assumptions.

- **Maintainer:** Lieven Clement (Ghent University) — `lieven.clement@ugent.be`
- **Bioconductor:** [msqrob2 v1.20.0](https://bioconductor.org/packages/release/bioc/html/msqrob2.html)
- **Source:** [git.bioconductor.org/packages/msqrob2](https://git.bioconductor.org/packages/msqrob2)
- **Vignettes:** [CPTAC case study](https://bioconductor.org/packages/3.23/bioc/vignettes/msqrob2/inst/doc/cptac.html)
- **License:** Artistic-2.0
- **Status at EuroBioC2025:** mature package (v1.20.0), workshop

## Workshop at EuroBioC2025

- **Presenter:** Christophe Vanderaa (UCLouvain — Lieven Clement's collaborator)
- **Day / session:** Day 2 (Thu Sep 18, 2025) — afternoon hands-on workshop (parallel with OSTA, mia, Workshop Platform, iSEE)
- **Workshop title:** "msqrob2 for proteomics workflows"
- **Format:** hands-on tutorial, attendees follow vignettes in their own R session
- **Workshop materials:** *to verify — typically a per-event GitHub repo from the Clement group*
- **Video:** workshops not recorded; the Bioconductor YouTube playlist covers plenaries only
- **Abstract / schedule:** [eurobioc2025 schedule](https://eurobioc2025.bioconductor.org/pages/schedule.html)

## What it does

msqrob2 frames LC-MS proteomics differential abundance as a robust linear mixed model on either peptide-level or protein-level intensities, stabilizing variance via ridge penalties and empirical Bayes shrinkage, and handling outliers through M-estimation. The hurdle workflow is the methodological signature: rather than imputing missing peptide intensities (and propagating untestable assumptions), it splits the inference into a presence/absence component and an intensity component combined into a single test.

## Where it fits in the corpus

- **AACR 2026:** no current dossier; proteomics is an emerging axis at AACR via translational/biomarker tracks
- **omicsGMF** ([entry](omicsgmf.md)) — same Clement-group lineup; matrix-factorization sister to msqrob2's regression framing
- **ISMB 2026:** scaffold
- **GBCC 2025:** queued
- **Nextflow Summit 2026:** not mentioned (different ecosystem)

## Notes

msqrob2's hurdle approach for proteomics missing data is the methodological signature — explicitly avoiding imputation rather than working around it; sister to omicsGMF in the Clement-group methods stack.
