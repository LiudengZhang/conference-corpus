# GCC2026

**2026 Galaxy Community Conference** — IUT Clermont Auvergne, Université Clermont Auvergne, Clermont-Ferrand, France · **June 22–24, 2026** (main conference), with training and CoFest June 25–26.

> **Status: ✅ built from the published program.** Conference concluded; source material public and stable. All 35 talks, 74 posters/demos, 10 BoFs, and the keynote are documented from the official schedule and the 130-page abstract book. **Video exists** — three day-long recordings, publicly posted — but has not yet been transcript-harvested. See [What to harvest next](#what-to-harvest-next).

- **Hosts:** Université Clermont Auvergne (UCA) and the Institut Français de Bioinformatique (IFB / ELIXIR-FR), co-organized with Johns Hopkins University; the AuBi platform is credited by IFB
- **Attendance:** ~200 in person plus ~50 remote via video link *(figure from the IFB/ELIXIR-FR recap; Galaxy Project publishes no number)*
- **Program Committee chair:** Enis Afgan (Johns Hopkins University)
- **Event site:** [galaxyproject.org/events/gcc2026](https://galaxyproject.org/events/gcc2026/)
- **Abstract book:** [130-page PDF](https://galaxy-community-conference.s3.us-east-1.amazonaws.com/GCC2026-abstract-book.pdf) — every talk and poster with full abstract
- **Video:** [Galaxy Community Conference 2026 playlist](https://www.youtube.com/playlist?list=PLB4YWcG-HSbw) — three day-long recordings

## Why this is in the vault

**The headline finding: GCC2026 was an AI-agents conference wearing a workflow-platform's clothes.** An entire talk session, most of another, the new fishbowl discussion format, and a dedicated Birds-of-a-Feather were given over to running Galaxy agentically — MCP servers, agent frameworks, LLM-generated tools, and the reproducibility problem that follows. For a corpus tracking [agentic AI](../aacr-2026/topics/agentic-ai/index.md), this is the most substantial body of *implemented, deployed* agentic-science engineering in the collection, as opposed to conference talks about the idea.

The convergence is worth stating plainly: **PSB 2026 in January and GCC2026 in June — unrelated communities, six months apart — both had agentic AI as their dominant emergent thread.** See [PSB themes](../psb-2026/themes.md#agentic-ai-four-papers-three-sessions).

Three further reasons:

1. **It completes the workflow-tooling axis.** The corpus has [`eurobioc-2025/`](../eurobioc-2025/index.md) for the Bioconductor/R side and [`nextflow-2026/`](../nextflow-2026/index.md) for the Nextflow side. Galaxy is the third pillar, and GCC2026 talks explicitly bridge all three (the **BioFAIR Pathfinder** project connects Bioconductor, Galaxy, and nf-core).
2. **Single-cell and spatial omics has a Galaxy community now.** The SPOC SIG (Single-cell & sPatial Omics Community), a dedicated BoF, a FAIR-workflows talk, and four posters — a real thread, connecting to [`aacr-2026/topics/single-cell-spatial-omics/`](../aacr-2026/topics/single-cell-spatial-omics/index.md).
3. **The material is genuinely open.** Full abstracts for all 35 talks and 74 posters, complete BoF and CoFest documentation, three video recordings, and slide deposits on HAL, Zenodo, and F1000Research. Very little is gated.

## Program shape

| Day | Content |
|---|---|
| **Mon Jun 22** | Open and welcome · **Galaxy Live!** · Overview of Galaxy SIGs · [Talks 1 — framework and platform direction](talks/index.md#talks-1-galaxy-framework-and-platform-direction) · [Talks 2 — infrastructure, federation, service operations](talks/index.md#talks-2-infrastructure-federation-and-service-operations) · Posters 1 (37) · [Talks 3 — communities, provenance, cross-domain](talks/index.md#talks-3-communities-provenance-and-cross-domain-expansion) · [BoFs ×5](community.md#birds-of-a-feather) |
| **Tue Jun 23** | [**Keynote — Rayan Chikhi**](keynote-chikhi.md) · [Talks 4 — FAIR workflows and public health](talks/index.md#talks-4-fair-data-analysis-workflows-and-public-health-applications) · [Talks 5 — tool integration and method development](talks/index.md#talks-5-tool-integration-and-method-development) · Lightning talks · Posters 2 (37) + ELIXIR virtual posters · ELIXIR F2F · conference dinner |
| **Wed Jun 24** | Galaxy Community Update · [Talks 6 — AI, workflows, guided analysis](talks/index.md#talks-6-ai-workflows-and-guided-analysis) · [**Fishbowl discussion**](themes.md#the-fishbowl-ai-galaxy-and-trustworthy-scientific-software) · [Talks 7 — community platforms and field reports](talks/index.md#talks-7-community-platforms-mature-ecosystems-and-field-reports) · Galaxy in Research · closing · [BoFs ×5](community.md#birds-of-a-feather) |
| **Thu–Fri Jun 25–26** | [Training](community.md#training) (3 parallel tracks each morning) · [CoFest](community.md#cofest) (16–19 projects, ~85+ contributors) |

Talks are a rigid 15 minutes (12 + 3 Q&A), which makes deriving per-talk video offsets from session chapter markers tractable.

## Organization

```
conferences/gcc-2026/
├── index.md              # this page
├── talks/index.md        # all 35 talks, by session, with abstracts summarized
├── keynote-chikhi.md     # Rayan Chikhi — petabase-scale sequence indexing
├── themes.md             # cross-cutting synthesis, incl. the fishbowl consensus
└── community.md          # BoFs, SIGs, training, CoFest, sponsors
```

## Organizing committee

The only pages on the entire GCC2026 site that publish affiliations are the organizers page and the keynote bio — see the [caveat below](#known-data-caveats).

**Organizing Committee:** Ahmed Awan (Johns Hopkins) · Anthony Bretaudeau (GenOuest / IRISA-CNRS / IFB) · Bérénice Batut (IFB & Auvergne Bioinformatique, UCA) · Enis Afgan (Johns Hopkins) · Gildas Le Corguillé (Station Biologique de Roscoff / Sorbonne Université / IFB) · Jenn Vessio (Johns Hopkins) · Natalie Whitaker-Allen (Johns Hopkins) · Tyler Collins (Johns Hopkins) · Marie Jossé (CNRS)

**Scientific Program Committee** — chair **Enis Afgan** (JHU), with Daniela Schneider (Freiburg), Hans-Rudolf Hotz (FMI Basel), Helge Hecht (Masaryk), Leonid Kostrykin (Heidelberg), Marie Jossé (CNRS / Data Terra), Mohammad Saeed Tajdary (Isfahan), Oriana Barros (Aveiro), Pavan Videm (Freiburg), Pratik Jagtap (Minnesota), Sunita Sharma (Georgia), Wolfgang Maier (Freiburg), Yvan Le Bras (MNHN).

**Sponsors:** Silver — Data Terra, PNDB. Bronze — GalaxyWorks, IFB, de.NBI, Limagrain. Friend of GCC — SFBI. Fellowships from the JXTX Foundation, the JJ Fund, the Galaxy Community Fund, and GTA2026 scholarships.

## What we have to work with

| Source | Coverage | Notes |
|---|---|---|
| **Schedule** | full program + **inline abstracts for every talk** | [galaxyproject.org/events/gcc2026/schedule/](https://galaxyproject.org/events/gcc2026/schedule/) — authoritative for final running order |
| **Abstract book** | 35 talks + 74 posters, 130 pp. | [PDF](https://galaxy-community-conference.s3.us-east-1.amazonaws.com/GCC2026-abstract-book.pdf) — posters are pp. 53–130 |
| **Video** | 3 day-long recordings | [playlist](https://www.youtube.com/playlist?list=PLB4YWcG-HSbw) — session-level chapters only |
| **Main recap** | overview | [galaxyproject.org/news/2026-07-06-gcc2026-recap/](https://galaxyproject.org/news/2026-07-06-gcc2026-recap/) |
| **Fishbowl summary** | AI consensus points | [news/2026-07-09-gcc2026-fishbowl-summary/](https://galaxyproject.org/news/2026-07-09-gcc2026-fishbowl-summary/) |
| **CoFest outcomes** | 16–19 projects | [news/2026-07-20-gcc2026-cofest-outcomes/](https://galaxyproject.org/news/2026-07-20-gcc2026-cofest-outcomes/) |
| **SIG recaps** | ML, microGalaxy | [ML SIG](https://galaxyproject.org/news/2026-07-01-gcc-ml-2026/) · [microGalaxy](https://galaxyproject.org/news/2026-07-13-gcc-microbiome-2026/) |
| **BoFs / training / organizers** | full lists | `/bofs/`, `/training/`, `/organizers/` under the event site |
| **Slides & posters** | ~20 deposits, decentralized | HAL (13 confirmed), Zenodo (ad-hoc), F1000Research (French mirrors) — see [community.md](community.md#slides-and-posters) |
| **IFB recap** | attendance figures | [ifb-elixir.fr](https://www.ifb-elixir.fr/en/global/a-look-back-at-the-galaxy-community-conference-2026/) |

## Known data caveats

- **No speaker affiliations exist for the 35 talks.** Neither the schedule nor the 130-page abstract book publishes institutional affiliations for presenters. Affiliations are available *only* for the organizing and program committees and the keynote. Any affiliation column would be inference — we do not present one.
- **Per-talk video links do not exist.** The playlist holds exactly three videos, one per day, with chapters at *session* granularity. Anyone citing an individual GCC2026 talk URL is mistaken. Per-talk offsets must be derived from the rigid 15-minute slot structure.
- **Lightning talk titles and speakers were never published** anywhere. Recoverable only from the Day 2 video, from 2:58:34.
- **Galaxy Live!, Galaxy Community Update, Galaxy in Research, and the fishbowl participants are unnamed** on every page. Video only.
- **The abstract book cover says "June 23-26, 2026"** — an error. Every other source says June 22–26.
- **The abstract book and final schedule disagree on running order.** A Marburg-virus phylogenomics talk (Bashea Chala et al., Ethiopia's first outbreak) was dropped from Talks 4 and kept as a poster, shifting that session up a slot; Talks 6 was also reordered. **Trust the schedule page.**
- **Poster counts double-count.** 37 + 37 = 74 listed items, but GCC allows "talk & poster" submission, so distinct works number fewer.
- **Training instructors are unpublished** for five of six workshops.
- **No GCC2027 date or location has been announced** — the recap's "Looking Ahead to GCC2027" heading is empty.

## What to harvest next

1. **Transcribe the three day recordings.** This is the single highest-value action for this vault: it would recover the lightning talks, the Galaxy Live! and Community Update content, the fishbowl exchange, and per-talk detail — turning this from a program-derived vault into a transcript-backed one like [SCGD26](../single-cell-genomics-day-2026/index.md).
2. **Mine the poster half of the abstract book** (pp. 53–130). The single-cell/spatial and public-health posters are not yet represented here beyond the named highlights.
3. **Follow the agentic-Galaxy engineering artifacts** — `galaxy-mcp` PR #89, `galaxy` PR #23027, `total-perspective-vortex` PR #198 — which are the working code behind [Talks 1](talks/index.md#talks-1-galaxy-framework-and-platform-direction) and [Talks 6](talks/index.md#talks-6-ai-workflows-and-guided-analysis).

## Sources

- Event site and schedule: <https://galaxyproject.org/events/gcc2026/>
- Abstract book: <https://galaxy-community-conference.s3.us-east-1.amazonaws.com/GCC2026-abstract-book.pdf>
- Recap: <https://galaxyproject.org/news/2026-07-06-gcc2026-recap/>
- IFB/ELIXIR-FR recap (attendance): <https://www.ifb-elixir.fr/en/global/a-look-back-at-the-galaxy-community-conference-2026/>
- All fetched 2026-08-25.
