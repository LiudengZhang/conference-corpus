# GAIA (Galaxy All-in-One Agent)

**A unified natural-language interface for cross-Galaxy data analysis** — an agentic AI front-end that lets researchers drive Galaxy tools, workflows, and histories through natural-language conversation, federating across Galaxy instances. The Goecks-lab counterpart to GalaxyMCP: GAIA is the user-facing agent, GalaxyMCP is the server-side protocol bridge.

- **Lead authors:** Junhao Qiu, Jeremy Goecks (Cleveland Clinic — Goecks lab)
- **Galaxy tool / platform:** TBD — verify from the talk slides (likely under `goeckslab/` on GitHub)
- **Source:** TBD — verify from the talk slides
- **Documentation / training:** TBD — verify from the talk slides
- **Status at GBCC2025:** oral talk on a natural-language interface for Galaxy

## Talk at GBCC2025

- **Speakers:** Junhao Qiu, Jeremy Goecks
- **Day / session:** Day 2 (Tue Jun 24, 2025) — Oral Session 1, Grace Auditorium (chair: Sehyun Oh)
- **Talk title:** "Galaxy All-in-One Agent: A Unified Natural Language Interface for Cross-Galaxy Data Analysis"
- **Slides:** TBD
- **Video:** [GBCC2025 playlist](https://www.youtube.com/playlist?list=PLdl4u5ZRDMQTJ0O_FIO9ayqaUDfnMo4-4)
- **Abstract / schedule:** [GBCC2025 program](https://gbcc2025.bioconductor.org/program/scientific_program/)

## What it does

GAIA wraps Galaxy's tool registry, workflow engine, and history/dataset model behind an LLM-driven conversational layer. A user describes an analysis in English ("run variant calling on these PacBio reads, then annotate with VEP"); the agent picks tools, sets parameters, kicks off jobs, and surfaces results — federating across multiple Galaxy instances rather than locking the user to one server. The pitch is to lower the on-ramp for biologists who'd otherwise hit the Galaxy UI's tool-discovery cliff.

## Where it fits in the corpus

- **AACR 2026:** axis = agentic AI; this is the most-relevant non-AACR talk for the agentic-AI dossier — a working agent grounded in a real, large bioinformatics tool ecosystem rather than a benchmark
- **GalaxyMCP** ([entry](galaxymcp.md)) — sister talk, same authors, same session; GAIA is the agent, GalaxyMCP is the protocol substrate
- **EuroBioC 2025:** no direct counterpart on the agentic-AI side
- **Nextflow Summit 2026:** thematic overlap with the AI-for-pipelines storyline

## Notes

GAIA + GalaxyMCP appear back-to-back in Oral Session 1 — together they're the AI/automation half of GBCC2025's "joint Galaxy + Bioconductor" rationale. Watch for whether the agent is a hosted service or a local-LLM-friendly client; the answer changes how reproducible an AI-driven Galaxy session can be.
