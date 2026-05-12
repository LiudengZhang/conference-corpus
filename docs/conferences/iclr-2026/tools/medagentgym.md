# MedAgentGym — Ran Xu et al. (Emory + UT Southwestern + collaborators)

**One-line description** — A scalable agentic training environment for code-centric biomedical reasoning, with 72,413 task instances across 129 categories drawn from 12 real-world biomedical scenarios, plus an open-sourced 7B "Med-Copilot" agent that competes with GPT-4o after RL fine-tuning.

- **Authors:** Ran Xu, Yuchen Zhuang, Yishan Zhong, Yue Yu, Zifeng Wang, Xiangru Tang, Hang Wu, May D. Wang, Peifeng Ruan, Donghan Yang, Tao Wang, Guanghua Xiao, Xin Liu, Carl Yang, Yang Xie, Wenqi Shi
- **Affiliation(s):** Emory University; UT Southwestern Medical Center; Georgia Tech; Yale — full affiliation map inferred from author roster, TBD-verify against camera-ready
- **Track / workshop:** ICLR 2026 main track — **Oral**
- **OpenReview:** [forum?id=jHDZEUgS4r](https://openreview.net/forum?id=jHDZEUgS4r)
- **arXiv:** [2506.04405](https://arxiv.org/abs/2506.04405)
- **Code:** [github.com/wshi83/MedAgentGym](https://github.com/wshi83/MedAgentGym)
- **Status at ICLR 2026:** Main-track Oral, Jan 26 2026 acceptance; CC-BY 4.0

## What it does

MedAgentGym is an interactive training-and-evaluation environment for LLM agents that write executable code over biomedical datasets. It bundles 72,413 task instances spanning 129 categories — pulled from 12 authentic biomedical scenarios (EHR cohort analytics, biostats over clinical trials, single-cell / bulk omics processing, medical-imaging analysis, etc.) — each wrapped in a sandboxed executable environment with verifiable ground-truth annotations and multi-turn feedback.

## How it works

Each task is encapsulated with detailed specifications, an interactive feedback channel, ground-truth checkers, and scalable trajectory-generation hooks. The team benchmarks 29 LLMs (commercial + open-source) on the environment, then trains a domain-specialised **Med-Copilot-7B** agent via multi-threaded multi-turn trajectory sampling, supervised fine-tuning, and online RL. The environment doubles as a benchmark suite and as a training loop — the standard recipe for "Gym"-class agentic infrastructure adapted to biomedical code.

## Headline benchmarks

- Med-Copilot reports **+43.02 % (offline RL) and +45.28 % (online RL) performance gains** over the SFT baseline across the full task suite.
- After tuning, Med-Copilot-7B is **competitive with GPT-4o** as a privacy-preserving, cost-efficient alternative for code-based biomedical reasoning.
- A substantial gap between commercial and open-source models is reported across all 29 LLMs at the zero-shot evaluation tier (numbers in camera-ready tables, TBD-parse).

## Where it fits in the corpus

- **AACR 2026 agentic-AI axis:** primary cross-link — this is the closest 2026-vintage analogue to TissueAgent / TumorBoard agents from the AACR program, but with a public training environment and a released 7B model.
- **ICML 2026:** likely follow-on submissions to GenBio / FM4LS workshops; Med-Copilot agent is the natural baseline for future SITC / RSNA agentic-AI demos.
- **NeurIPS 2026:** expect an extended benchmark + leaderboard track.
- **Nextflow Summit 2026:** workflow-execution overlap — MedAgentGym sandboxes have similar reproducibility framing to Nextflow's compute-aware execution.

## Notes

The release strategy (full Gym + Med-Copilot-7B weights + 72k task instances) is unusually generous for an ICLR oral and is what makes this the load-bearing agentic-AI entry from ICLR 2026. The closest sibling at NeurIPS 2025 was AgentClinic; MedAgentGym is broader (data-science, not bedside dialogue) and explicitly code-centric, which is the right scope for the AACR vault's "agent that writes a CCLE re-analysis" downstream use case.
