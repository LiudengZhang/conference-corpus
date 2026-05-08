# EuroBioC 2025 — Tools

EuroBioC2025 ran 5 keynotes + ~25 short talks + 5 hands-on workshops + posters. Most short talks introduce or update a Bioconductor package — that's what this directory captures. Each entry below corresponds to **one package presented at EuroBioC2025**.

> **Status:** Template stub. We're proposing the per-tool format here for review before bulk extraction. Once locked, ~30 entries get populated from the talk + workshop list.

## Per-tool entry template

Each tool gets its own page (`tools/<package-slug>.md`) following this structure:

````markdown
# <PackageName>

**One-line description** — what the package does in plain language.

- **Maintainer:** <name> (<institution>)
- **Bioconductor:** [package page]
- **Source:** [GitHub link]
- **Vignette:** [vignette link]
- **Status at EuroBioC2025:** new release / major update / methods talk / case study / workshop

## Talk at EuroBioC2025

- **Speaker:** ...
- **Day / session:** ...
- **Slides:** [Zenodo DOI]
- **Video:** [YouTube link if recorded]
- **Abstract / talk page:** [conf-site link]

## What it does

2–3 sentences: the problem it solves, key methodological idea, what it consumes/produces.

## Where it fits in the corpus

- AACR 2026: [link if mentioned]
- ISMB 2026: [link if mentioned]
- RECOMB 2026: [link if mentioned]
- Nextflow Summit 2026: [link if mentioned]
- GBCC 2025: [link if mentioned]

## Notes

Free-form impressions, benchmarks claimed, comparisons to alternatives.
````

## Tool index

Three pilot entries (drafted by hand to pressure-test the template). Bulk extraction over the remaining ~25 short talks + 5 keynotes + 4 workshops will land below.

| Package | Domain | Speaker | Day | Slides | Video | Mentioned elsewhere |
|---|---|---|---|---|---|---|
| [DESpace](despace.md) | spatial omics | Peiying Cai | Day 2 | TBD | not recorded | — |
| [DeeDeeExperiment](deedeeexperiment.md) | infra / data class | Najla Abassi | Day 1 | TBD | not recorded | iSEE (consumer) |
| [iSEE](isee.md) | visualization | Federico Marini | Day 2 (workshop) | TBD | not recorded | DeeDeeExperiment |
| *bulk extraction follows* | | | | | | |

## Why this format

- **Cross-vault links matter** — this is the only place where "tool released here, used in cancer-research talk X, benchmarked in methods paper Y" can be one click apart
- **Slides + video + vignette + Bioconductor page** in one place — none of the other vaults have this complete quartet
- **Domain field** lets the table slice by single-cell / spatial / etc. without duplicating into topic pages
- **Status field** tells a reader at a glance whether they're looking at a v1.0 announcement or a 4-year-old package's annual update

## Open questions for the pilot

1. **Granularity** — ✅ locked: one page per tool
2. **AACR dossier mirroring** — ✅ locked: full entry in both vaults, cross-linked (no canonical/stub asymmetry)
3. **Sample tools to draft first** — ✅ done: DESpace / DeeDeeExperiment / iSEE drafted; the DDE ↔ iSEE pair exercises the cross-vault link mechanic
4. **Edge case: non-Bioconductor tools** — *open*: SpatialData (Marconato Day 2 talk) is Python-primary with R interop in development. The current template assumes a Bioconductor package page. Need a variant for cross-language or pre-release tools — proposed: a "Status: external / pre-release" badge that swaps the Bioconductor field for "(Python-primary; R interop layer in development)" plus a link to the upstream framework
