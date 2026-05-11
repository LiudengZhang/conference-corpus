# atena

**Transposable-element expression quantification from RNA-seq** — a Bioconductor package implementing multiple TE-quantification methods (ERVmap, TEtranscripts, Telescope) under a single API so analysts can choose, compare, or benchmark approaches for measuring transposable-element activity from bulk RNA-seq.

- **Maintainer:** Robert Castelo (Universitat Pompeu Fabra) — `robert.castelo@upf.edu`
- **Authors:** Beatriz Calvo-Serra (author), Robert Castelo (author/creator)
- **Bioconductor:** [atena v1.18.0](https://bioconductor.org/packages/release/bioc/html/atena.html)
- **Source:** [git.bioconductor.org/packages/atena](https://git.bioconductor.org/packages/atena)
- **Vignettes:** [Introduction](https://bioconductor.org/packages/release/bioc/vignettes/atena/inst/doc/atena.html)
- **License:** Artistic-2.0
- **Status at GBCC2025:** lightning talk teaser

## Talk at GBCC2025

- **Speaker:** Robert Castelo (Universitat Pompeu Fabra)
- **Day / session:** Day 3 — lightning talks
- **Talk title:** "atena (transposable element analysis)" (lightning teaser)
- **Slides:** *to verify after publish*
- **Video:** [GBCC2025 playlist](https://www.youtube.com/playlist?list=PLdl4u5ZRDMQTJ0O_FIO9ayqaUDfnMo4-4)
- **Abstract / schedule:** [GBCC2025 program](https://gbcc2025.bioconductor.org/program/scientific_program/)

## What it does

atena ingests RNA-seq alignments and quantifies expression of transposable elements (LINEs, SINEs, ERVs, etc.) under three published method backends — ERVmap, TEtranscripts, Telescope — exposed through one Bioconductor API. Method choice matters because TEs share sequence with ancestral copies and the assignment strategy (best-hit, EM, family-collapsed) drives the answer; atena lets users pick deliberately or compare estimates from the same reads.

## Where it fits in the corpus

- **AACR 2026:** axis = bioinfo-tools (TE biology — ERVs, LINE-1, retrotransposon de-repression — is increasingly mainstream in cancer transcriptomics, immunotherapy response, and aging-cancer interfaces)
- **GSVA / Bioc-to-Galaxy** ([entry](bioc-to-galaxy.md)) — Castelo also leads the GSVA Galaxy-wrapper CoFest deliverable; atena is a candidate next package for the same auto-integration pipeline
- **EuroBioC 2025:** not presented
- **Nextflow Summit 2026:** not mentioned

## Notes

A lightning teaser at GBCC; the substantive value is the unified API across three published TE-quantification methods. For cancer transcriptomics groups exploring TE / ERV signatures (immunogenicity, replication stress, aging), atena removes the "which tool / will my numbers reproduce" hurdle by carrying all three backends.
