# Toward Generative Virtual Cells — Lewis & Zueco (AIXC Research)

**One-line description** — A co-evolutionary framework where a virtual-cell *world model* (predicts experimental outcomes) and a *perturbation planner* (chooses which experiments to run) jointly adapt on inner and outer timescales, with validation-gated architecture search closing the loop.

- **Authors:** David Scott Lewis, Enrique Zueco
- **Affiliation(s):** AIXC Research
- **Track / workshop:** ICLR 2026 — **Gen² workshop** (Generative AI in Genomics)
- **OpenReview:** [openreview.net Gen2 ICLR 2026 PDF](https://openreview.net/pdf/58c616e58a32446ea386695fcf2a9f5caa4f5ab1.pdf)
- **Code:** TBD — not released at workshop time
- **Status at ICLR 2026:** Gen² workshop accepted paper (Apr 27, 2026)

## What it does

The paper argues that "virtual cell" research treats the world model and the experimental planner as separable, when in practice they are tightly coupled: a planner only proposes informative perturbations if the world model is calibrated, and a world model only improves on perturbations the planner actually selects. The contribution is a *co-evolutionary* training loop that updates both jointly, with a validation-gated mechanism for safely changing the world-model architecture mid-loop.

## How it works

On the inner timescale, the planner queries the current world model, selects a Perturb-seq-style perturbation, the simulator returns noisy single-cell data, and the world model updates its weights. On the outer timescale, the agent proposes changes to the world-model architecture and training scheme, evaluates them against validation and capacity constraints, and accepts or rejects the change. The planner adapts its exploration strategy based on model uncertainty and recent error patterns. The current paper uses a synthetic simulator and a small MLP/transformer world model as a proof-of-concept; future work explicitly targets diffusion- and transformer-based generative architectures on real Perturb-seq data.

## Headline benchmarks

This is a **position + proof-of-concept paper**, not a benchmark paper. The Gen² accept frames the contribution as a paradigm for "safe model adaptation" coupled with experimental design. Quantitative comparisons against fixed-world-model baselines are reported in the workshop PDF on toy Perturb-seq simulators (TBD — exact numbers behind PDF parsing).

## Where it fits in the corpus

- **AACR 2026 virtual-cells axis:** direct match — pair with the AACR virtual-cell session and with any cell-state-engineering pharma demos.
- **NeurIPS 2026 LMRL:** the natural next venue for the diffusion-based + real-Perturb-seq version this paper telegraphs.
- **ICML 2026 GenBio:** workshop-level cousin contributions on perturbation planners likely.
- **AACR Pancreatic / Brain Tumors 2026:** longer-term — perturbation planning over tissue-specific cell atlases is the obvious oncology adapt.

## Notes

The paper is workshop-stage and explicitly speculative — it is included as the *concept* anchor for the Gen² "engineering cellular states" theme more than as a method release. The Lewis/Zueco framing — "world model + planner, jointly adapted under validation gating" — is the architecture pattern that AACR-vault agentic-AI dossiers should expect to start emerging from labs like Cradle, Recursion, and Insitro within 6–12 months.
