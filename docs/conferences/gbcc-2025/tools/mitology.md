# mitology

**Dissect mitochondrial activity from transcriptome data** — a Bioconductor package that scores RNA-seq samples against a curated reorganization of mitochondria-related Reactome and Gene Ontology pathways, plus pre-configured MitoCarta3.0 pathway sets, to quantify mitochondrial function from bulk or single-cell expression data.

- **Maintainer:** Stefania Pirrotta (University of Padua) — `stefania.pirrotta@unipd.it`
- **Authors:** Stefania Pirrotta (creator/author), Enrica Calura (author, funding); collaborator Massimo Bonora
- **Bioconductor:** [mitology v1.4.0](https://bioconductor.org/packages/release/bioc/html/mitology.html)
- **Source:** [git.bioconductor.org/packages/mitology](https://git.bioconductor.org/packages/mitology)
- **Vignettes:** [Introduction](https://bioconductor.org/packages/release/vignettes/mitology/inst/doc/mitology.html)
- **License:** AGPL-3
- **Status at GBCC2025:** methods talk on the package's mitochondrial-activity scoring workflow

## Talk at GBCC2025

- **Speaker:** Stefania Pirrotta (University of Padua) — co-authors Massimo Bonora, Enrica Calura
- **Day / session:** Day 4 (Thu Jun 26, 2025) — Oral Session 5
- **Talk title:** "Dissect mitochondrial activity by transcriptome data with mitology R package"
- **Slides:** *to verify after publish*
- **Video:** *to verify (TBD)*
- **Abstract / schedule:** [GBCC2025 program](https://gbcc2025.bioconductor.org/program/scientific_program/)

## What it does

mitology takes an expression matrix (bulk or single-cell) and returns sample-level scores for mitochondria-centric pathways — OXPHOS, TCA, mitochondrial translation, fission/fusion, mitophagy, etc. — drawn from a curated reorganization of Reactome and GO terms plus the MitoCarta3.0 inventory. The package abstracts away the gene-set wrangling so an analyst can ask "which samples have low Complex I activity?" or "which clusters lean glycolytic vs. OXPHOS?" without hand-assembling pathway lists.

## Where it fits in the corpus

- **AACR 2026:** axes = bioinfo-tools (mitochondrial metabolism is a recurring cancer-biology theme; mitology gives a transcriptome readout that complements metabolomics dossiers)
- **signifinder** ([entry](signifinder.md)) — same speaker (Pirrotta) and sister Bioc package; signifinder is the broader signature-scoring tool, mitology is the mitochondria-specialized variant of the same intellectual line
- **EuroBioC 2025:** not presented
- **Nextflow Summit 2026:** not mentioned

## Notes

Pirrotta's GBCC slot pairs naturally with her signifinder work — both packages convert expression data to interpretable pathway/signature scores; mitology is the mito-focused descendant. The MitoCarta3.0 integration is the practical hook for cancer-metabolism users who already cite that resource.
