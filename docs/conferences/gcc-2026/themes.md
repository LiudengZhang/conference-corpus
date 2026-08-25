# GCC2026 — Themes

Cross-cutting synthesis of [GCC2026](index.md). Talks are cited by number as listed on the [talks page](talks/index.md).

## AI agents as first-class infrastructure — the dominant thread

The IFB/ELIXIR-FR recap notes "numerous presentations focusing on the use of AI," which understates it. An entire talk session ([Talks 6](talks/index.md#talks-6-ai-workflows-and-guided-analysis)), most of another ([Talks 1](talks/index.md#talks-1-galaxy-framework-and-platform-direction)), the new fishbowl format, and two Birds-of-a-Feather were about running Galaxy agentically.

What distinguishes this from conference talk about AI is that **it is shipped engineering**:

- **Building an AI-Native Galaxy** (Baker, Chilton, Van Den Beek) — an Agent Operations layer, an MCP server, and an Agent Framework registry with intent routing and handoffs. Surfaced in-app as **ChatGXY**, and reachable from external MCP clients including Claude Desktop and Cursor.
- **Benchmarking AI Agents in Galaxy** (Collins, Qiu et al.) — the **MCPeval** live integration testing framework, LLM-as-judge evaluation, and **BixBench-Verified-50**. Shipping the benchmark alongside the agent layer, in the same session, is the discipline that is usually missing.
- **User-Defined Tools** (Van Den Beek et al.) — the path from an LLM-generated analysis to a reproducible, validatable workflow.
- **Reproducibility in the Age of Agents** (Chilton, Van Den Beek, Awan, Nekrutenko) — the question underneath all of it.
- **The Galaxy History Graph: From State to Structure** (Guerler et al.) — the provenance substrate that makes agent-composed analyses auditable.
- **AI-Guided Analysis in BRC Analytics** (Baker et al.) — research question to running workflow.
- **Automated Galaxy tool generation** (York, Joshi, Raubenolt, Blankenberg) and **AOP-toolkit** (Durník et al.) — LLM pipelines for tool wrapping and toxicological literature mining.
- **BoF: Galaxy as the Substrate for Agent-driven Science** (Baker, Nekrutenko) — driving Galaxy through Claude Code, Codex, `galaxy-mcp`, Loom, and Orbit.

**Working artifacts** came out of CoFest: [`galaxy-mcp` PR #89](https://github.com/galaxyproject/galaxy-mcp/pull/89), [`galaxy` PR #23027](https://github.com/galaxyproject/galaxy/pull/23027) (validating and displaying reference URLs in LLM responses), [`total-perspective-vortex` PR #198](https://github.com/galaxyproject/total-perspective-vortex/pull/198).

### The convergence worth noting

**PSB 2026 (January, Hawaii) and GCC2026 (June, France) — unrelated communities, six months apart — both had agentic AI as their dominant emergent thread.** At PSB it arrived as four peer-reviewed papers across three sessions including a *second-version* agent benchmark ([PSB themes](../psb-2026/themes.md#agentic-ai-four-papers-three-sessions)); at GCC it arrived as deployed platform architecture. Neither community was talking about the other. That is a stronger signal than either meeting alone, and it is the single most useful thing this corpus can say about 2026 so far. Compare [`aacr-2026/topics/agentic-ai/`](../aacr-2026/topics/agentic-ai/index.md), where the same idea appeared as conference sessions about the possibility.

## The fishbowl — "AI, Galaxy, and Trustworthy Scientific Software"

GCC2026 introduced a **fishbowl discussion** format and spent it entirely on this question. The published consensus points are worth recording verbatim in substance, because they are a working scientific community stating its own terms:

- AI is **already in use**, and Galaxy's job is to shape that use responsibly rather than resist it.
- **"AI should assist, but not draw scientific conclusions."**
- Auditability and provenance tracking are essential, not optional.
- Environmental and ethical costs are a legitimate part of the calculation.
- There is real concern about **eroding public knowledge-sharing** and about **weakening junior-researcher training** — if agents do the analysis, how does anyone learn to do it.
- Training on responsible AI use is critical.

That third-to-last point is the one rarely heard at AI-methods conferences, and it is why this fishbowl is worth citing.

Participants and moderators were not named on any page; recoverable only from the [Day 3 video](https://youtu.be/e10XFwUu1vc?t=7602) at 2:06:42.

## Infrastructure, federation, and scaling

Galaxy operating as an actual federated international infrastructure, not an aspirational one:

- **Canada joining the UseGalaxy.\* federation** (Coulombe et al.) — a new national node.
- **The Global Galaxy Registry** (Savage et al.) — structured metadata and dynamic discovery across **180+ instances**.
- **Evolving TPV** (Goonasekera et al.) — resource-aware scheduling maturing.
- **Modern Analysis Scales, And So Too Must Galaxy** (Coraor) and **Galaxy on AnVIL** (Afgan, Narvaez-Bandera et al.) for secure cloud analysis of human genomic data.
- **Outsourcing user identity management** (Price et al., Galaxy Australia) — the unglamorous federation problem.

Supported by BoFs on multi-HPC federation via Pulsar, identity, the security responsibility boundary, and small-scale local admins; and by CoFest work on Kubernetes, Pulsar DRMAA, CVMFS reference genomes, and time-based quotas.

## Workflow reproducibility, provenance, and FAIR

- **LabID Meets Galaxy** (Thomas et al.) — continuous provenance from physical samples to results, closing the gap most reproducibility stories leave open at the FASTQ.
- **The Galaxy History Graph** (Guerler et al.) — from state to structure.
- **FAIRyMAGs** (Zierep, Batut) — a modular FAIR-compliant workflow suite for metagenome-assembled genome reconstruction.
- **Integration of experimental protocols** (Demange et al.) for FAIR experimental workflows.
- **From legacy pipelines to reusable workflows** at Statens Serum Institut (Matusevicius).
- Poster **SemSec** (Gundersen et al.) on Crypt4GH recryption for EGA/FEGA.

## Single-cell and spatial omics in Galaxy

A real, organized community now — the thread that makes GCC2026 directly relevant to this corpus's core subject matter.

- **FAIR Workflows and Training for Single-Cell Analysis in Galaxy and Beyond** (Loach, Rue-Albrecht) — the anchor talk.
- **BoF: Keeping pace with best practices in single-cell and spatial omics in Galaxy** (Rue-Albrecht, Loach), framed on the **BioFAIR Pathfinder** project and Seurat / Bioconductor / Scanpy interoperability.
- **SPOC** — the Single-cell & sPatial Omics Community SIG (poster #35, Videm).
- Posters: *Unlocking Spatial Biology: End-to-End FAIR Workflows for Spatial Data Analysis in Galaxy* (#25 P2), *BioFAIR Pathfinder: Connecting Bioconductor, Galaxy, and nf-core* (#15 P2), *Repository-Coupled scRNA-seq Analysis with Galaxy* (#14 P2).
- CoFest: Bioconductor tools plus single-cell GTN material (Rue-Albrecht).

**BioFAIR Pathfinder is the item to watch.** It explicitly bridges Bioconductor, Galaxy, and nf-core — the three workflow ecosystems this corpus tracks separately in [`eurobioc-2025/`](../eurobioc-2025/index.md), here, and [`nextflow-2026/`](../nextflow-2026/index.md). If it works, the tools axis of the corpus stops being three parallel stories.

Corpus fit: [`aacr-2026/topics/single-cell-spatial-omics/`](../aacr-2026/topics/single-cell-spatial-omics/index.md).

## Cross-domain expansion beyond genomics

Galaxy is no longer a genomics platform, and GCC2026 made that structural: Earth system science with Data Terra and EOSC (Jossé et al.), ecology (Le Bras et al.), **digital humanities NLP** integrating Stanford CoreNLP and spaCy (Schneider, Suderman), cell-microscopy image analysis over a decade (Kostrykin et al.), metabolomics via Workflow4Metabolomics (Petera et al.), geoscience at BRGM (Delaporte, Keuchkerian), proteomics via Scop3P (Díaz et al.), and synthetic biology and fermentation through the Siduri portal (Barnabé et al.). Training day two had a dedicated Earth Science & Ecology track.

## Public health and pathogen surveillance

National bacterial WGS surveillance at Statens Serum Institut; nasal microbiome in Alzheimer's disease (Hojat Ansari); the withdrawn-to-poster Marburg-virus phylogenomics from Ethiopia's first outbreak. Posters add Galaxy @ Sciensano, *Francisella tularensis* in Bulgaria, SensiTyper for gonorrhea, ABRomics antibiotic-resistance surveillance, and an ISO-accredited lab workflow. CoFest included tool wrapping for public health.

## Microbiology and metagenomics

The **microGalaxy SIG** is one of the most developed communities in the project: the Microbiology Galaxy Lab ships **315+ tools and 115+ curated workflows**, deployed on `microbiology.usegalaxy.{eu,fr,org,org.au}`, with 30+ training events over five years. GCC2026 contributions: FAIRyMAGs, the Alzheimer's microbiome talk, posters on the Lab and on CoDex, the reference-data (IDC) BoF, and CoDex development at CoFest.

## Training and community building

**Updates from the GTN and Galaxy Training Academy** (Hiltemann, Whitaker-Allen, Larivière), six training workshops, the SIG overview session, the **first cross-project roadmap** for the Galaxy ecosystem (Kucher), and posters on CoDex, the Biodiversity Genomics Galaxy Lab, and the launch of a Galaxy UK SIG. A BoF addressed the genuinely hard version of this problem — overlapping communities, and how to structure one without cannibalizing another.

## Sources

- Schedule and abstracts: <https://galaxyproject.org/events/gcc2026/schedule/>
- Fishbowl summary: <https://galaxyproject.org/news/2026-07-09-gcc2026-fishbowl-summary/>
- CoFest outcomes: <https://galaxyproject.org/news/2026-07-20-gcc2026-cofest-outcomes/>
- ML SIG: <https://galaxyproject.org/news/2026-07-01-gcc-ml-2026/> · microGalaxy SIG: <https://galaxyproject.org/news/2026-07-13-gcc-microbiome-2026/>
- BoFs: <https://galaxyproject.org/events/gcc2026/bofs/>
