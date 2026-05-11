# ipd

**Inference on Predicted Data — valid statistical inference when an outcome has been imputed by an ML/AI prediction algorithm** — an R package that implements several recent methods (PostPI, PSPA, PPI / PPI++, PSPS, Chen & Chen, etc.) for downstream regression with ML-predicted outcomes, behind a single unified `ipd()` wrapper.

- **Lead author / maintainer:** Stephen Salerno (Fred Hutchinson Cancer Center) — `ssalerno@fredhutch.org`
- **Co-authors:** Jiacheng Miao, Awan Afiaz, Kentaro Hoffman, Anna Neufeld, Qiongshi Lu, Tyler H. McCormick, Jeffrey T. Leek
- **CRAN:** [ipd on CRAN](https://cran.r-project.org/web/packages/ipd/index.html) (v0.1.4+, July 2025)
- **Source:** [github.com/ipd-tools/ipd](https://github.com/ipd-tools/ipd)
- **Project site:** [ipd-tools.github.io/ipd](https://ipd-tools.github.io/ipd/)
- **Paper:** [Salerno et al., *Bioinformatics* 41(2):btaf055, 2025](https://academic.oup.com/bioinformatics/article/41/2/btaf055/7997267)
- **Preprint:** [arXiv:2410.09665](https://arxiv.org/abs/2410.09665)
- **License:** MIT
- **Status at GBCC2025:** Oral 5 methods talk + Day-2 workshop ("Inference Challenges and Corrections for AI-Predicted Outcomes")

## Talk at GBCC2025

- **Speakers:** Stephen Salerno, Jiacheng Miao, et al.
- **Day / session:** Day 4 (Thu Jun 26, 2025) — Oral Session 5, Grace Auditorium (chair: Scott Cain)
- **Talk title:** "Inference with predicted data – what do we do after we have machine learned everything?"
- **Companion workshop:** Day 2 (Tue Jun 24) — "Inference Challenges and Corrections for AI-Predicted Outcomes"
- **Slides:** TBD
- **Video:** TBD
- **Abstract / schedule:** [GBCC2025 program](https://gbcc2025.bioconductor.org/program/scientific_program/)

## What it does

When an outcome variable in a downstream regression is partially imputed by an ML model (e.g. predicted survival from a deep model, predicted phenotype from an LLM, predicted cell-type label from a foundation model), naive statistical inference on that mixed real-and-predicted outcome is biased and has wrong standard errors. ipd implements the recent statistical-correction methods — PostPI, Prediction-Powered Inference (PPI / PPI++), PSPA, PSPS, Chen & Chen — behind a single user-facing `ipd()` wrapper that takes the labeled data, the unlabeled (predicted) data, and a formula, and returns a properly-corrected fit with valid coverage. Custom `print`, `summary`, `tidy`, `glance`, and `augment` methods make the corrected fit drop in to a tidyverse-style modeling pipeline.

## Where it fits in the corpus

- **AACR 2026:** axis = agentic AI / ML; valid inference on ML-predicted outcomes is one of the foundational methodological questions for any "AI-first" cancer-biology workflow
- **EuroBioC 2025:** no direct counterpart on post-prediction inference
- **ISMB 2026:** scaffold; expect overlap on PPI-family methods
- **Nextflow Summit 2026:** thematic adjacency with the AI-for-pipelines storyline (validating model outputs in production pipelines)

## Notes

This is one of the more directly-useful methods talks at GBCC2025 for any group doing downstream stats on ML-labeled data. The fact that it ships as both a workshop *and* an oral talk indicates that the organizers expected significant user demand — and the field as a whole (PPI from Angelopoulos et al., PostPI from Wang et al., PSPA from Miao et al.) has converged on this being a real problem.
