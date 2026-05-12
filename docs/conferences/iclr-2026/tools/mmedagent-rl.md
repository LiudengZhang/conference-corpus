# MMedAgent-RL — Multi-Agent RL for Multimodal Medical Reasoning

**One-line description** — A reinforcement-learning–trained multi-agent collaboration framework for multimodal medical reasoning over images and clinical text, where specialist agents (radiology, pathology, EHR) are coordinated by a planner agent and tuned end-to-end with RL.

- **Authors:** TBD — author roster not surfaced in scrape; "MMedAgent-RL" team at a Chinese-academia / industry consortium per ICLR 2026 papers digest
- **Affiliation(s):** TBD
- **Track / workshop:** ICLR 2026 main track — poster (designation TBD-verify against virtual schedule)
- **OpenReview:** TBD — to be linked once forum ID is parsed
- **Code:** TBD
- **Status at ICLR 2026:** main-track accept (per Paper Copilot / Bohrium digest)

## What it does

MMedAgent-RL coordinates a team of specialist LLM-based agents — each pinned to a different medical modality (CT/MRI, whole-slide pathology, structured EHR, free-text clinical notes) — and trains the *coordination policy* between them with reinforcement learning. The framework targets the multi-hop medical-reasoning regime where no single modality is sufficient (e.g. radiology + pathology + history to triage a tumour case).

## How it works

Each specialist agent is initialised from a domain-tuned LLM (radiology VLM, pathology VLM, EHR-trained LLM). A planner agent issues sub-queries, aggregates evidence, and emits the final diagnosis or recommendation. RL is used to optimise *which* specialist gets called *when*, using verifiable medical reasoning tasks (likely multi-modal MedQA-class benchmarks) as reward. The methodology aligns with the broader 2026 wave of agent-RL papers (AgentFlow, GLM-Agent) but ports the recipe into the clinical-imaging multi-agent setting.

## Headline benchmarks

Bohrium / Paper Copilot ICLR 2026 highlights flag MMedAgent-RL alongside MedAgentGym, M3CoTBench, MedVLSynther, and CARE as the main-track medical-AI cohort. Specific accuracy numbers across MedQA / multi-modal benchmarks are in the camera-ready (TBD — parse).

## Where it fits in the corpus

- **AACR 2026 agentic-AI axis:** secondary cross-link — pair with the AACR tumour-board agent demos and the RSNA-style radiology-pathology integration sessions.
- **MedAgentGym (this vault):** sibling submission; MedAgentGym is the *training environment*, MMedAgent-RL is a *trained multi-agent policy* using a similar paradigm.
- **MICCAI 2026 / RSNA 2026:** primary clinical-imaging cross-link — expect adapted versions at RSNA's AI plenary.
- **SITC 2026:** if extended to immuno-oncology multi-modal trial-matching, plausible adapt.

## Notes

This entry is **lightly verified** — title and accept status are confirmed via two third-party ICLR 2026 highlights digests (Paper Copilot, Bohrium), but the author roster and OpenReview forum ID need a second pass once camera-ready PDFs are fully indexed. Hold this entry as a placeholder for the multi-agent medical-reasoning slot until the metadata pass completes. The 2026 main-track medical-AI cohort (MedAgentGym + MMedAgent-RL + M3CoTBench + MedVLSynther + CARE) collectively is the strongest single-conference clustering of clinical agentic-AI to date — the AACR vault's "agentic AI for oncology" axis should treat this cohort as the methodological substrate for SITC 2026 / AACR 2027 demos.
