# MIRit

**Integrate microRNA and gene expression to decipher pathway complexity** — a Bioconductor framework that investigates relationships between miRNAs and genes across biological conditions, supporting differential expression analysis and network characterization between miRNA and mRNA expression.

- **Maintainer:** Jacopo Ronchi (University of Milano-Bicocca, UniMiB) — `jacopo.ronchi@unimib.it`
- **Bioconductor:** [MIRit v1.8.0](https://bioconductor.org/packages/release/bioc/html/MIRit.html)
- **Source:** [git.bioconductor.org/packages/MIRit](https://git.bioconductor.org/packages/MIRit)
- **Vignettes:** [MIRit](https://bioconductor.org/packages/release/vignettes/MIRit/inst/doc/MIRit.html)
- **License:** GPL (>=3)
- **Status at EuroBioC2025:** methods talk on miRNA-mRNA network integration

## Talk at EuroBioC2025

- **Speaker:** Jacopo Ronchi (University of Milano-Bicocca)
- **Day / session:** Day 1 (Wed Sep 17, 2025) — afternoon short-talk session, after the Holmes keynote
- **Talk title:** "MIRit framework for miRNA-mRNA network identification"
- **Slides (Zenodo DOI):** *to verify after publish*
- **Video:** not recorded — short talks at EuroBioC2025 were not part of the plenary YouTube playlist
- **Abstract / schedule:** [eurobioc2025 schedule](https://eurobioc2025.bioconductor.org/pages/schedule.html)

## What it does

MIRit jointly models miRNA and mRNA expression to recover regulatory relationships across biological conditions. It performs differential expression analysis on both modalities and characterizes miRNA-mRNA interaction networks, so that pathway-level signal is interpreted through the regulatory layer rather than from gene expression alone.

## Where it fits in the corpus

- **AACR 2026:** no current dossier; relevant axis is bioinfo / AI methods — network-based miRNA-mRNA integration is conceptually adjacent to MOSClip's pathway-based multi-omics
- **MOSClip** ([entry](mosclip.md)) — sibling pathway/network method on the same Day 1 short-talk session
- **GBCC 2025:** queued
- **Nextflow Summit 2026:** not mentioned

## Notes

miRNA-mRNA integration sits in the network-based pathway analysis tradition; complement to MOSClip ([entry](mosclip.md)) on the same session, with MIRit emphasizing the regulatory-network framing rather than survival.
