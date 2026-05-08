# iscream

**Fast, memory-efficient BED file queries** — a Bioconductor package with an Rcpp + htslib backend for querying compressed BED files and returning results as data frames, `GenomicRanges`, or matrices. The performance angle (vs. Rsamtools / native R parsers) is the headline.

- **Maintainer:** James Eapen (Van Andel Institute) — `james.eapen@vai.org`
- **Authors:** James Eapen (author/creator), Jacob Morrison (author), Nathan Spix (contributor), Hui Shen (author, supervisor, funding)
- **Bioconductor:** [iscream v1.2.0](https://bioconductor.org/packages/release/bioc/html/iscream.html)
- **Source:** [github.com/huishenlab/iscream](https://github.com/huishenlab/iscream)
- **Vignettes:** [Introduction](https://bioconductor.org/packages/release/bioc/vignettes/iscream/inst/doc/iscream.html) · [HTSlib guide](https://bioconductor.org/packages/release/bioc/vignettes/iscream/inst/doc/htslib.html) · [Performance](https://bioconductor.org/packages/release/bioc/vignettes/iscream/inst/doc/performance.html) · [Data structures](https://bioconductor.org/packages/release/bioc/vignettes/iscream/inst/doc/data_structures.html) · [Comparison with Rsamtools](https://bioconductor.org/packages/release/bioc/vignettes/iscream/inst/doc/tabix.html) · [TSS methylation](https://bioconductor.org/packages/release/bioc/vignettes/iscream/inst/doc/TSS.html)
- **License:** MIT
- **Status at GBCC2025:** lightning talk on a low-level BED query engine

## Talk at GBCC2025

- **Speaker:** James Eapen (Van Andel Institute)
- **Day / session:** Day 3 — lightning talks
- **Talk title:** "iscream: fast and efficient BED file queries"
- **Slides:** *to verify after publish*
- **Video:** *to verify (TBD)*
- **Abstract / schedule:** [GBCC2025 program](https://gbcc2025.bioconductor.org/program/scientific_program/)

## What it does

iscream wraps htslib's tabix-indexed BED reader in Rcpp and exposes a query API that returns either a tibble, a `GenomicRanges` object, or a numeric matrix (e.g. methylation calls per region × sample) without round-tripping through R-level text parsers. The `tabix` vignette benchmarks against Rsamtools; the `TSS` vignette demonstrates the end-use case (per-TSS methylation matrices across many samples) where the throughput difference matters.

## Where it fits in the corpus

- **AACR 2026:** axis = bioinfo-tools (infrastructure layer; relevant to any methylation / ChIP / ATAC dossier that builds region × sample matrices)
- **Bioc-to-Galaxy** ([entry](bioc-to-galaxy.md)) — performance-critical Bioc tools are exactly the class that benefits from being wrapped as Galaxy workflow steps for non-R users
- **EuroBioC 2025:** not presented
- **Nextflow Summit 2026:** not mentioned

## Notes

The Rcpp + htslib backend signals a performance-focused tool, fitting alongside other low-level Bioc utilities (Rsamtools, GenomicFiles, VariantAnnotation). For methylation pipelines at VAI scale, the speedup likely matters most when assembling per-region matrices across hundreds of samples — the canonical tabix-bottleneck shape.
