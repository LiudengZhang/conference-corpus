# SeqArray

**Big-data storage and analysis of whole-genome sequencing variant calls in R/Bioconductor** — an array-oriented, compressed GDS-backed container for genotypes and annotations from population-scale WGS, designed to scale to biobank-class cohorts where VCF stops being usable.

- **Maintainer:** Xiuwen Zheng (AbbVie, formerly UW Genetic Analysis Center) — `zhengx@u.washington.edu`
- **Bioconductor:** [SeqArray](https://bioconductor.org/packages/release/bioc/html/SeqArray.html)
- **Source:** [github.com/zhengxwen/SeqArray](https://github.com/zhengxwen/SeqArray)
- **Vignettes:** [SeqArray Data Format and Access](https://bioconductor.org/packages/release/bioc/vignettes/SeqArray/inst/doc/SeqArrayTutorial.html)
- **Paper:** [Zheng et al., *Bioinformatics* 2017](https://academic.oup.com/bioinformatics/article/33/15/2251/3072873)
- **License:** GPL-3
- **Status at GBCC2025:** methods talk on biobank-scale rare-variant annotation workflows using GDS files

## Talk at GBCC2025

- **Speakers:** Xiuwen Zheng, Raven Chen
- **Day / session:** Day 2 (Tue Jun 24, 2025) — Oral Session 2B, Grace Auditorium (chair: Vincent Carey)
- **Talk title:** "Enhancing rare variant analysis in biobanks: whole-genome annotation using GDS files"
- **Slides:** TBD
- **Video:** TBD
- **Abstract / schedule:** [GBCC2025 program](https://gbcc2025.bioconductor.org/program/scientific_program/)

## What it does

SeqArray builds on the GDS (Genomic Data Structure) format — a hierarchical, array-oriented, compressed on-disk container — to store genotype matrices, allele frequencies, and per-variant annotations from WGS at biobank scale. Access is through an R interface with C++-level performance, and the data layout is designed so that filtering by sample, variant, or annotation is fast without re-streaming the whole file. The GBCC2025 talk extends this with workflows for **whole-genome annotation** during rare-variant analysis — folding functional annotation directly into the GDS container so that downstream rare-variant tests (in SeqVarTools, SNPRelate, GENESIS) can access annotations without a separate join.

## Where it fits in the corpus

- **AACR 2026:** axis = bioinfo / AI methods; biobank rare-variant infrastructure is upstream of any large-scale germline-cancer or pharmacogenomics analysis
- **EuroBioC 2025:** no direct counterpart; biobank-scale GDS work is GBCC-side
- **ISMB 2026:** scaffold; expect overlap on biobank methods
- **Nextflow Summit 2026:** not mentioned

## Notes

SeqArray anchors a multi-package ecosystem (SeqVarTools, SNPRelate, GENESIS) used across UK Biobank, All of Us, and TOPMed analyses. The Day-2 talk is an annotation-pipeline update layered on a mature substrate — the news is workflow ergonomics, not a new container.
