# Keynote — Rayan Chikhi: assembling and exploring the world's sequencing data

**Speaker:** **Rayan Chikhi** — group leader, Sequence Bioinformatics group, Department of Computational Biology, **Institut Pasteur**, France
**Title:** *"Assembling and exploring the world's sequencing data for biological discovery"*
**Slot:** [GCC2026](index.md), Tuesday, June 23, 2026, 09:00–10:00, Amphitheater A
**Recording:** [Day 2 video](https://www.youtube.com/watch?v=1ZH5GkP3Ip0), from 00:04
**Status:** Documented from the published program and bio; **not yet transcript-derived**

This was the **only keynote** at GCC2026 — confirmed against both the schedule and highlights pages.

## Thesis

Public sequence archives hold petabases of data that almost nobody can actually query. Chikhi's argument is that assembling and indexing that entire corpus, rather than sampling it, turns the archive itself into a discovery instrument — and that the discoveries which follow are not incremental.

## Speaker

A computer scientist working on algorithms and data structures for large-scale biological sequence analysis, with emphasis on **genome assembly, k-mer-based methods, and scalable indexing of massive sequencing collections**. PhD in computer science from ENS Rennes (2012); postdoc at Penn State; joined CNRS and founded his Institut Pasteur group in 2019. Holds an **ERC Consolidator Grant (IndexThePlanet, 2023–2028)**.

He initiated **Logan** — an assembly and index of petabase-scale public DNA and RNA sequencing data — and used it, alongside **Serratus**, to discover new viruses and plastic-degrading enzymes.

## Why this keynote, at this conference

Placing a petabase-scale indexing talk in front of the Galaxy community is a pointed choice. Galaxy's problem is making analysis *accessible and reproducible*; Chikhi's is making the world's data *searchable at all*. The two meet at the question GCC2026 spent three days on: if an agent can now compose an analysis for you, what corpus is it composing over? A platform with agentic tooling and no access to the full archive is answering only half the problem.

## Connections to the corpus

- **Scale-first infrastructure** is the same instinct behind the atlas-building efforts tracked in [`single-cell-genomics-2026/`](../single-cell-genomics-2026/index.md) and [SCGD26](../single-cell-genomics-day-2026/index.md) — index everything, then ask questions.
- **Sequence indexing and k-mer methods** are the classical counterpart to the learned-representation approach in [genome language models](../../talks/fm-to-virtual-cells/adjacent-methods/genome-language-models.md). Worth reading as the "do we need a model for this?" position.
- The virus-discovery result connects to the pathogen-surveillance thread in [Talks 4](talks/index.md#talks-4-fair-data-analysis-workflows-and-public-health-applications).

## Open items

- [ ] Transcribe the keynote from the Day 2 recording; the published bio and one-line recap are all that exist in text.
- [ ] Capture the Q&A, which is not separately chaptered.

## Sources

- Highlights page (bio and title): <https://galaxyproject.org/events/gcc2026/highlights/>
- Schedule: <https://galaxyproject.org/events/gcc2026/schedule/>
- Recap (topic summary): <https://galaxyproject.org/news/2026-07-06-gcc2026-recap/>
- Recording: <https://www.youtube.com/watch?v=1ZH5GkP3Ip0>
