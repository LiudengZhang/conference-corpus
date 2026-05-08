# GBCC 2025 — Tools

GBCC2025 ran 3 keynotes + 53 oral talks across 5 sessions + 11 lightning talks + 10 hands-on workshops + 50+ posters. A substantial fraction of the oral and lightning talks introduce or update a named Bioconductor package, a Galaxy tool, or a cross-platform integration artifact — that's what this directory captures. Each entry below corresponds to **one tool presented at GBCC2025** (Bioconductor package, Galaxy tool, or integration scaffolding).

> **Status:** Scaffold — talks-with-packages list compiled in `../_program-extracted.md`; bulk extraction queued. The per-tool template below mirrors EuroBioC2025's; the only addition is an "ecosystem" line so a reader can tell at a glance whether they're looking at an R/Bioconductor package, a Galaxy XML tool, or a cross-platform piece (and Open Question 5 below tracks whether that even survives review).

## Per-tool entry template

Each tool gets its own page (`tools/<package-slug>.md`) following this structure:

````markdown
# <PackageName>

**One-line description** — what the package does in plain language.

- **Maintainer:** <name> (<institution>)
- **Ecosystem:** Bioconductor / Galaxy / cross-platform
- **Bioconductor:** [package page] *(if applicable)*
- **Galaxy ToolShed:** [tool page] *(if applicable)*
- **Source:** [GitHub link]
- **Vignette / docs:** [link]
- **Status at GBCC2025:** new release / major update / methods talk / case study / workshop / integration demo

## Talk at GBCC2025

- **Speaker:** ...
- **Day / session:** Day X — Oral Session N / Lightning / Workshop
- **Slides:** [Zenodo DOI]
- **Video:** [GBCC2025 YouTube playlist link if recorded]
- **Abstract / talk page:** [scientific-program link or CSHL abstract-book page]

## What it does

2–3 sentences: the problem it solves, key methodological idea, what it consumes/produces.

## Where it fits in the corpus

- AACR 2026: [link if mentioned]
- ISMB 2026: [link if mentioned]
- RECOMB 2026: [link if mentioned]
- Nextflow Summit 2026: [link if mentioned]
- EuroBioC 2025: [link if also presented at sister event]

## Notes

Free-form impressions, benchmarks claimed, comparisons to alternatives. For Galaxy-wrapped Bioconductor tools: link the wrapper PR or the `tools-iuc` shed entry.
````

## Planned tool index

Targeting ~25–30 entries across Bioconductor packages, Galaxy tools, and cross-platform integration artifacts. Ordered by day and session. The placeholder table below shows the columns; rows will be filled by the bulk extraction pass from `../_program-extracted.md`.

Skipped (not in this table): community / training / non-tool talks (Doyle on Bioconductor in Africa; Gauthier on UseGalaxy Canada; Santana on sertão research; Kucher on AnVIL training; Williams keynote on training equity); methods talks without a clearly named package anchor (Hansen on allele-specific methylation; Nanda on viral-infection signaling networks; Lakshman on orthology-at-scale); the three keynotes (deferred to a separate digest pass).

| Package / Tool | Ecosystem | Domain | Speaker | Day / Session | Slides | Video | Mentioned elsewhere |
|---|---|---|---|---|---|---|---|
| *example* GAIA | Galaxy | NL agent / AI | Junhao Qiu, Jeremy Goecks | Day 2 / Oral 1 | TBD | TBD | — |
| *example* GalaxyMCP | Galaxy | AI integration / MCP | Dannon Baker et al. | Day 2 / Oral 1 | TBD | TBD | — |
| *example* RAIDS | Bioconductor | ancestry inference | Pascal Belleau et al. | Day 2 / Oral 2B | TBD | TBD | — |
| *example* signifinder | Bioconductor | cancer signatures | Stefania Pirrotta et al. | Day 2 / Oral 2B | TBD | TBD | — |
| *example* sosta | Bioconductor | spatial omics | Samuel Gunz, Mark D. Robinson | Day 3 / Oral 3 | TBD | TBD | — |
| *example* atena | Bioconductor | transposable elements | Robert Castelo | Day 3 / Lightning | TBD | TBD | — |
| *example* iscream | R / htslib | BED queries (Rcpp) | James Eapen | Day 3 / Lightning | TBD | TBD | — |
| *example* Tidyomics | Bioconductor | tidyverse for omics | Stefano Mangiola | Day 3 / Lightning + Oral 4 | TBD | TBD | — |
| *example* plyxp | Bioconductor | dplyr for SE objects | Justin Landis, Michael Love | Day 4 / Oral 5 | TBD | TBD | — |
| *example* mitology | Bioconductor | mitochondrial activity | Stefania Pirrotta et al. | Day 4 / Oral 5 | TBD | TBD | — |
| *(~15–20 more)* | | | | | | | |

## Why this format

- **Cross-vault links matter** — same as EuroBioC2025: tool released here, used in cancer-research talk X, benchmarked in methods paper Y, all one click apart
- **Slides + video + vignette + Bioconductor-or-Galaxy page** in one place
- **Ecosystem field** is GBCC-specific — separates R packages from Galaxy tools from cross-platform scaffolding without forcing them into separate directories
- **Status field** distinguishes a v1.0 announcement from a 4-year-old package's annual update from a methods talk from an integration demo
- **Mentioned-elsewhere** points the reader at the EuroBioC2025 vault when the same package was presented at both events (Soneson, Mangiola, Castelo, Pirrotta, Borman, and others appear in both lineups)

## Open questions for the pilot

1. **Granularity** — ✅ inherited from EuroBioC2025: one page per tool
2. **AACR dossier mirroring** — ✅ inherited: full entry in both vaults, cross-linked
3. **Sample tools to draft first** — *open*: candidate set is GAIA + GalaxyMCP (Galaxy AI scaffolding pair, exercises the ecosystem-field variant) and RAIDS / signifinder / sosta (canonical Bioconductor methods talks). plyxp is also a strong template-validation pick because it's a tidyverse-for-SummarizedExperiment package — exactly the cross-cutting kind of tool we want to make sure renders well
4. **Edge case: non-Bioconductor tools** — *open*: GBCC's edge case is GAIA / GalaxyMCP / NOVA — Galaxy-side tools with no Bioconductor page at all. Proposed: same template, swap "Bioconductor" line for "Galaxy ToolShed" and use a "Galaxy" ecosystem badge
5. **Galaxy workflows vs. Bioconductor packages — same template, or split?** — *open*: a Galaxy tool/workflow has different surface (XML wrapper, ToolShed entry, training material) than a Bioconductor package (DESCRIPTION, vignette, BiocCheck). The template above tries to unify them with the "Ecosystem" field plus optional Bioconductor/Galaxy-ToolShed lines. Decision deferred until 3 sample entries (1 Bioconductor, 1 Galaxy-only, 1 integration scaffold) are drafted by hand. If the unified shape is awkward, fall back to two templates and add a third for "integration scaffolding" (Bioc-in-Galaxy wrappers, GalaxyMCP-style protocols, automatic-wrapping pipelines).
