# GCC2026 — Talks

All **35 peer-reviewed talks** at [GCC2026](../index.md), in final schedule order, grouped by session block. Talks ran 15 minutes (12 + 3 Q&A).

**Author lists are verbatim from the official schedule and abstract book.** No institutional affiliations were published for any presenter — see the [caveat on the overview page](../index.md#known-data-caveats). Full abstracts for every talk are inline on the [schedule page](https://galaxyproject.org/events/gcc2026/schedule/) and in the [abstract book PDF](https://galaxy-community-conference.s3.us-east-1.amazonaws.com/GCC2026-abstract-book.pdf).

**Video:** three day-long recordings with session-level chapters. Per-talk links do not exist; offsets must be derived from the 15-minute slot grid.

| Day | Video | Session chapters |
|---|---|---|
| Mon Jun 22 | [4h 36m](https://www.youtube.com/watch?v=9x-2MSZEcT4) | 00:00 Opening · 08:30 Galaxy Live · 50:20 SIG overview · **1:01:35 Talks 1** · **2:10:35 Talks 2** · **3:35:55 Talks 3** |
| Tue Jun 23 | [3h 28m](https://www.youtube.com/watch?v=1ZH5GkP3Ip0) | 00:04 Keynote · **59:00 Talks 4** · **2:16:15 Talks 5** · 2:58:34 Lightning talks |
| Wed Jun 24 | [5h 15m](https://www.youtube.com/watch?v=e10XFwUu1vc) | 00:04 Community Update · **48:25 Talks 6** · 2:06:42 Fishbowl · **3:20:04 Talks 7** · 4:50:55 Galaxy in Research |

---

## Talks 1 — Galaxy framework and platform direction

**Monday, 10:50–12:05** · moderator Marisa Loach · video from [1:01:35](https://youtu.be/9x-2MSZEcT4?t=3695)

This session, together with [Talks 6](#talks-6-ai-workflows-and-guided-analysis), is where Galaxy declared its agentic direction. Read them as a pair.

| Time | Title | Authors |
|---|---|---|
| 10:50 | **Building an AI-Native Galaxy: Agent Operations, Agent Framework, and MCP** | Baker Dannon, Chilton John, Van Den Beek Marius |
| 11:05 | **Benchmarking AI Agents in Galaxy: Live Integration Testing and Bioinformatics Workflow Evaluation** | Collins Tyler\*, Qiu Junhao\*, Morais Paulo Cilas Lyra Jr, Savage Michelle, Goecks Jeremy (\*equal) |
| 11:20 | Beyond the Tool Panel: New Features for Improved Tool Discovery and Management | Awan Ahmed, Grüning Björn, Lopez David, Schatz Michael |
| 11:35 | **User-Defined Tools: From LLM-Generated Analysis to Reproducible, Validatable Workflows** | Van Den Beek Marius, Baker Dannon, Chilton John |
| 11:50 | Charting the Course: Developing the First Cross-Project Roadmap for the Galaxy Ecosystem | Kucher Natalie |

**Building an AI-Native Galaxy** is the architectural statement: an Agent Operations layer, an MCP server, and an Agent Framework registry with intent routing and handoffs, surfaced in-app as ChatGXY and reachable from external MCP clients including Claude Desktop and Cursor. **Benchmarking AI Agents in Galaxy** is its necessary complement — the MCPeval live integration framework, LLM-as-judge evaluation, and BixBench-Verified-50. A platform shipping an agent layer *and* a benchmark for it in the same session is the healthy version of this trend.

## Talks 2 — Infrastructure, federation, and service operations

**Monday, 13:00–14:30** · moderator Martin Čech · video from [2:10:35](https://youtu.be/9x-2MSZEcT4?t=7835)

| Time | Title | Authors |
|---|---|---|
| 13:00 | If you love something, set it free. If it comes back, it's yours — A Galaxy perspective on outsourcing user identity management | Price Gareth, Goonasekera Nuwan, Bromhead Catherine, Mather Marius, Zhu Amanda, Mok Winnie, Winter Uwe, Lee Justin, Makunin Igor, Hyde Cameron, Ward Nigel, Manos Steven, Amarapathy Samitha |
| 13:15 | **A New Star in the Galaxy: Canada is Joining the UseGalaxy.\* International Federation** | Coulombe Charles, Davis John, Gauthier Carol, Fortin Jérôme, Barrette Michel, Jacques Pierre-Étienne |
| 13:30 | Modern Analysis Scales, And So Too Must Galaxy | Coraor Nate |
| 13:45 | Evolving TPV: recent advances in resource-aware scheduling for Galaxy | Goonasekera Nuwan, Van Den Beek Marius, Bromhead Catherine, Bernt Matthias, Chilton John, Grüning Björn |
| 14:00 | **The Global Galaxy Registry: Structured Metadata and Dynamic Discovery Across 180+ Instances** | Savage Michelle, Grüning Björn, Price Gareth, Schatz Michael |
| 14:15 | Secure Cloud-based Analysis of Human Genomic Data with Galaxy on AnVIL | Afgan Enis\*, Narvaez-Bandera Isis\*, Suderman Keith, Morais Lyra Jr Paulo Cilas, Schatz Michael, Goecks Jeremy (\*equal) |

The federation story is the one to track: Canada joining UseGalaxy.\*, a registry spanning 180+ instances, and resource-aware scheduling (TPV) maturing. Galaxy is operating as a genuinely federated international infrastructure, which is the thing most workflow platforms claim and few achieve.

## Talks 3 — Communities, provenance, and cross-domain expansion

**Monday, 16:00–17:00** · moderator Pierre-Étienne Jacques · video from [3:35:55](https://youtu.be/9x-2MSZEcT4?t=12955)

| Time | Title | Authors |
|---|---|---|
| 16:00 | Galaxy Ecology: 2026 update | Le Bras Yvan, Seguineau Pauline, Galaxy Ecology Community |
| 16:15 | Advancing Earth System Research Through Galaxy, Data Terra, and EOSC Collaboration | Jossé Marie, Seguineau Pauline, Le Bras Yvan, Detoc Jérôme, Norvez Olivier, Grellet Sylvain, Rizzo Alessandro, Keuchkerian Samuel, Delaporte Pascal, Bodéré Erwan, Sarramia David, Guimont Mathieu |
| 16:30 | Natural Language Processing in Galaxy: Integrating Stanford CoreNLP and spaCy for the Digital Humanities | Schneider Daniela, Suderman Keith |
| 16:45 | **LabID Meets Galaxy: Continuous Provenance from Samples to Results** | Thomas Laurent, Girardot Charles, Scholtalbers Jelle, Monfort Matthias, Reza Nayeem |

**LabID Meets Galaxy** is the one with the broadest relevance: provenance carried continuously from physical sample to computational result. That is the missing link in most reproducibility stories, which typically start at the FASTQ.

## Talks 4 — FAIR data analysis workflows and public health applications

**Tuesday, 10:30–12:00** · moderator Solenne Correard · video from [59:00](https://youtu.be/1ZH5GkP3Ip0?t=3540)

| Time | Title | Authors |
|---|---|---|
| 10:30 | FAIRyMAGs: A Modular, FAIR-Compliant Galaxy Workflow Suite for Flexible and Scalable Metagenome-Assembled Genome Reconstruction | Zierep Paul, Batut Bérénice |
| 10:45 | **FAIR Workflows and Training for Single-Cell Analysis in Galaxy and Beyond** | Loach Marisa, Rue-Albrecht Kevin (Fellow) |
| 11:00 | From legacy pipelines to reusable Galaxy workflows for national bacterial WGS surveillance at Statens Serum Institut | Matusevicius Povilas |
| 11:15 | Leveraging Galaxy's Superpowers to Enhance Fermentation Innovation through the Siduri portal | Barnabé Agnès, Fernandez Emilie, Le Floch Erwan, Lacroix Thomas, Schbath Sophie, Loux Valentin |
| 11:30 | Galaxy-based workflows for genome-resolved and multi-kingdom microbiome analysis: application to the nasal microbiome in Alzheimer's disease | Hojat Ansari Mina |

**FAIR Workflows and Training for Single-Cell Analysis in Galaxy and Beyond** is the anchor for this corpus — see [Themes → single-cell and spatial](../themes.md#single-cell-and-spatial-omics-in-galaxy).

!!! note "Withdrawn from this session"
    *Phylogenomic and Functional Analysis of Ethiopia's First Marburg Virus Outbreak Highlights a Single Spillover Event and Preserved Vaccine Targets* (Bashea Chala, Getu Melak, Gebremicael Gebremedhin, Ali Abraham, Marburg Virus Outbreak Task Force, Tadese Gemechu, Tollera Getachew) appears in the abstract book at Tue 11:00 but was dropped from the final talk program, shifting the rest of the session up a slot. It remained as **Posters 2 #7**.

## Talks 5 — Tool integration and method development

**Tuesday, 13:00–13:45** · moderator Yvan Le Bras · video from [2:16:15](https://youtu.be/1ZH5GkP3Ip0?t=8175)

| Time | Title | Authors |
|---|---|---|
| 13:00 | **Open Source Resources for the Automated Generation of Galaxy Tools** | York Spencer, Joshi Jayadev, Raubenolt Bryan, Blankenberg Daniel |
| 13:15 | Integration of experimental protocols into the Galaxy platform to support FAIR experimental workflows | Demange Fanny, Refahi Yassin, Loux Valentin, Paës Gabriel |
| 13:30 | Launching the Scop3P Toolkit Starship into Galaxy: From Earth-Bound Services to Galactic Interactive Tools | Adrián Díaz, Tichshenko Natalia, De Geest Paul, Depoortere Boris, Andrade Buono Rafael, Martens Lennart, Vranken Wim, Ramasamy Pathmanaban |

Followed by **lightning talks** (13:45–14:30) whose titles and speakers were never published — recoverable only from the Day 2 video at [2:58:34](https://youtu.be/1ZH5GkP3Ip0?t=10714).

## Talks 6 — AI, workflows, and guided analysis

**Wednesday, 10:30–12:00** · moderator Jeremy Goecks · video from [48:25](https://youtu.be/e10XFwUu1vc?t=2905)

**The most important session at GCC2026 for this corpus.**

| Time | Title | Authors |
|---|---|---|
| 10:30 | **Reproducibility in the Age of Agents** | Chilton John, Van Den Beek Marius, Awan Ahmed, Nekrutenko Anton |
| 10:45 | **Workflows in the Age of LLMs: Building a Galaxy Workflow Community** | Van Den Beek Marius, Delisle Lucille, Bernt Matthias, Maier Wolfgang, Lariviere Delphine, IWC Contributors |
| 11:00 | Starting from Data: Connecting External Resources and Analysis in Galaxy | Callan Danielle, Van Den Beek Marius, Baker Dannon, Rogers David, Cain Scott, Smeds Patrik, Clawson Hiram, Coraor Nate, Beavers Kelsey, Haeussler Maximilian, Schatz Michael, Pond Sergei, Nekrutenko Anton |
| 11:15 | **From Research Question to Running Workflow: AI-Guided Analysis in BRC Analytics** | Baker Dannon, Van Den Beek Marius, Callan Danielle, Rogers Dave, Nekrutenko Anton |
| 11:30 | The Galaxy History Graph: From State to Structure | Guerler Aysam, Chilton John, Awan Ahmed, Baker Dannon, Van Den Beek Marius, Heidari Alireza, Lopez David, Savage Michelle, Gruening Bjoern, Nekrutenko Anton, Schatz Michael C. |
| 11:45 | AOP-toolkit: Galaxy-enabled LLM pipelines for large-scale toxicological literature mining with secure credential management | Durník Robin, Hecht Helge, Babica Pavel, Sovadinová Iva, Bajard Lola |

*Reproducibility in the Age of Agents* is the title that should travel outside the Galaxy community. When an LLM agent composes an analysis, what exactly is the reproducible artifact — the prompt, the plan, the resulting workflow, or the run? Galaxy is one of the few platforms with the provenance machinery to answer that concretely, and this session plus *The Galaxy History Graph: From State to Structure* is that answer taking shape.

**Note the reordering:** *Starting from Data* moved from 11:45 in the abstract book to 11:00 on the final schedule.

## Talks 7 — Community platforms, mature ecosystems, and field reports

**Wednesday, 15:00–16:30** · moderator Yvan Le Bras · video from [3:20:04](https://youtu.be/e10XFwUu1vc?t=12004)

| Time | Title | Authors |
|---|---|---|
| 15:00 | Updates from the Global Galaxy Training Network (GTN) and Galaxy Training Academy (GTA) | Saskia Hiltemann, Natalie Whitaker-Allen, Larivière Delphine |
| 15:15 | A journey around Galaxy on the W4M boat: a feedback from someone caught in the middle | Petera Mélanie, Workflow4metabolomics Coreteam |
| 15:30 | Leveraging Galaxy Across Multiple Scientific Domains | Watson Greg |
| 15:45 | **Galaxy Image Analysis: A Decade of Development for Cell Microscopy Image Analysis and Beyond** | Kostrykin Leonid, Wollmann Thomas, Gao Qi, Rohr Karl |
| 16:00 | Rewriting the Galaxy Hub — Migrating 4,300 Pages from Gridsome to Astro | Baker Dannon, Alireza Heidari, Grüning Björn |
| 16:15 | Galaxy at BRGM: From Strategic Integration to Operational Challenges in a National Research Infrastructure | Delaporte Pascal, Keuchkerian Samuel |

**Galaxy Image Analysis** is a decade-scale retrospective on cell microscopy tooling — relevant to the imaging thread the corpus tracks through [`miccai-2026/`](../../miccai-2026/index.md) and [`isbi-2026/`](../../isbi-2026/index.md), from the open-infrastructure side rather than the methods-paper side.

## Posters

74 items across two sessions (37 each), all with full abstracts in the [abstract book](https://galaxy-community-conference.s3.us-east-1.amazonaws.com/GCC2026-abstract-book.pdf), pp. 53–130. Because GCC allows a "talk & poster" submission option, the number of *distinct* works is lower than 74.

Most relevant to this corpus:

- **#35 (Posters 1)** — SPOC, the Single-cell & sPatial Omics Community (Videm Pavankumar)
- **#25 (Posters 2)** — *Unlocking Spatial Biology: End-to-End FAIR Workflows for Spatial Data Analysis in Galaxy* (Naghsh Nilchi et al.)
- **#15 (Posters 2)** — *BioFAIR Pathfinder: Connecting Bioconductor, Galaxy, and nf-core*  (Rue-Albrecht Kevin et al.)
- **#14 (Posters 2)** — *Repository-Coupled scRNA-seq Analysis with Galaxy* (Olha Jaroslav et al.)
- **#26 (Posters 2)** — *AI ecosystem for life science data analysis in Galaxy* (Kumar Anup et al.) · [Zenodo](https://doi.org/10.5281/zenodo.21133087)
- **#34 (Posters 2)** — *SemSec: Crypt4GH Recryption for EGA/FEGA* (Gundersen Sveinung et al.)
- **#13 (Posters 1)** — *Three Galaxies, One Grid, One Foundation: National Bioinformatics Infrastructure in Czechia* (Cech Martin, Demko Martin)

## Sources

- Schedule (authoritative running order, with inline abstracts): <https://galaxyproject.org/events/gcc2026/schedule/>
- Abstract book: <https://galaxy-community-conference.s3.us-east-1.amazonaws.com/GCC2026-abstract-book.pdf>
- Video playlist: <https://www.youtube.com/playlist?list=PLB4YWcG-HSbw>
