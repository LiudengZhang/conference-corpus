# signifinder

**Compute and explore public cancer transcriptional signatures** — a Bioconductor package containing 70+ curated tumor signatures from the literature and applying them as single-sample / single-cell / single-spot scores across bulk RNA-seq, microarray, single-cell, and spatial transcriptomics inputs.

- **Maintainer:** Stefania Pirrotta (University of Padua) — `stefania.pirrotta@phd.unipd.it`
- **Bioconductor:** [signifinder v1.13.0](https://bioconductor.org/packages/release/bioc/html/signifinder.html)
- **Source:** [github.com/CaluraLab/signifinder](https://github.com/CaluraLab/signifinder)
- **Vignettes:** [signifinder intro](https://bioconductor.org/packages/release/bioc/vignettes/signifinder/inst/doc/signifinder.html)
- **License:** AGPL-3
- **Status at GBCC2025:** methods talk on cross-modality cancer signature scoring

## Talk at GBCC2025

- **Speakers:** Stefania Pirrotta, Laura Masatti, et al. (Calura Lab, University of Padua)
- **Day / session:** Day 2 (Tue Jun 24, 2025) — Oral Session 2B, Grace Auditorium (chair: Vincent Carey)
- **Talk title:** "Public gene expression cancer signatures across bulk, single-cell and spatial transcriptomics data with signifinder Bioconductor package"
- **Slides (Zenodo DOI):** *TBD — Zenodo deposits typically 2–4 weeks post-conference*
- **Video:** *TBD — GBCC2025 YouTube playlist not yet surfaced*
- **Abstract / schedule:** [GBCC2025 program](https://gbcc2025.bioconductor.org/program/scientific_program/)

## What it does

signifinder is a curation play: 70+ published cancer signatures (hypoxia, EMT, immune-infiltrate, stemness, and dozens of indication-specific scores) packaged with one consistent scoring API that runs across bulk RNA-seq, microarray, single-cell, and spatial inputs. Instead of every analyst re-implementing each signature from a paper's supplement, signifinder has them in one place with the same input contract — so a user can compute and compare a panel of signatures on the same object.

## Where it fits in the corpus

- **AACR 2026:** axes single-cell-spatial-omics + clinical-trials — cancer signatures are clinically-actionable readouts and the cross-modality coverage matches the AACR spatial / single-cell dossiers
- **mitology** ([entry](mitology.md)) — same speaker (Pirrotta), Day 4; sister package on the same "transcriptome-interpretation" track
- **ISMB 2026:** scaffold
- **Nextflow Summit 2026:** not mentioned

## Notes

Pirrotta presents twice at GBCC2025 — signifinder on Day 2 and mitology on Day 4 — which signals the Calura lab is consolidating a "transcriptome interpretation" suite (signature scoring + pathway / organelle-specific scoring) rather than shipping one-off packages. The cross-modality angle (bulk + sc + spatial) is the key value-add over older signature collections that targeted bulk only.
