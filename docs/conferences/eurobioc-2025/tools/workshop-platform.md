# Bioconductor Workshop Platform

**Hosted infrastructure for authoring and running Bioconductor workshops** — Galaxy-based infrastructure providing containerized, Bioconductor-pre-installed workshop environments. Workshop authors ship Quarto/Rmarkdown content paired with a Docker image so attendees get a one-click reproducible session.

- **Maintainer:** Alexandru Mahmoud (Bioconductor core team)
- **Platform:** [workshop.bioconductor.org](https://workshop.bioconductor.org/)
- **Related package:** [BiocBook](https://bioconductor.org/packages/release/bioc/html/BiocBook.html) (Jacques Serizay) — the Quarto-book authoring framework that pairs with the platform
- **Status at EuroBioC2025:** infrastructure / runtime platform

## Workshop at EuroBioC2025

- **Presenter:** Alexandru Mahmoud (Bioconductor core)
- **Day / session:** Day 2 (Thu Sep 18, 2025) — afternoon hands-on workshop (parallel with OSTA, mia, msqrob2, iSEE)
- **Workshop title:** "Bioconductor Workshop Platform authoring"
- **Format:** hands-on tutorial walking authors through building a workshop image and deploying it to the hosted platform
- **Workshop materials:** *to verify — typically linked from [workshop.bioconductor.org](https://workshop.bioconductor.org/)*
- **Video:** workshops not recorded; the Bioconductor YouTube playlist covers plenaries only
- **Abstract / schedule:** [eurobioc2025 schedule](https://eurobioc2025.bioconductor.org/pages/schedule.html)

## What it does

The Workshop Platform is a Galaxy-style on-demand container hosting service: an attendee opens a URL, gets a fresh Bioconductor-preinstalled R/RStudio session in a browser, and runs the workshop's Quarto/Rmarkdown materials without any local install. Authors build a Docker image with their package + dependencies, register the workshop, and the platform handles spin-up, isolation, and tear-down. It is the runtime that hosts BiocBook-authored content during BioC, EuroBioC, and GBCC hands-on sessions.

## Where it fits in the corpus

- **AACR 2026:** no direct dossier; relevant as runtime infrastructure for any AACR adjacent workshop content
- **BiocBook** — pairs with the platform as the authoring half (BiocBook → Workshop Platform pipeline)
- **iSEE** ([entry](isee.md)) — iSEE workshops are typical Workshop Platform tenants
- **OSTA** ([entry](osta.md)) — OSTA chapters can be served via the platform for hands-on sessions
- **Day 3 closing keynote (Jacques Serizay)** — likely covered the BiocBook half of this pipeline
- **GBCC 2025:** queued — used for GBCC hands-on tutorials too

## Notes

Distinct from BiocBook: BiocBook is the *authoring* tool (Quarto-based book scaffolding tied to a package); Workshop Platform is the *runtime* (Galaxy-style on-demand container hosting). Together they form the pipeline used by EuroBioC, BioC, and GBCC for hands-on tutorials.
