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

**Core idea.** Treat the virtual-cell world model and the experimental planner as a *co-evolutionary* system updated on two timescales — fast joint adaptation in response to each experiment, and slower validation-gated changes to the world-model architecture itself.

**Inputs / outputs.** Inputs are a current world-model checkpoint, a candidate perturbation library (Perturb-seq-style genetic or small-molecule), and a held-out validation set; outputs are (a) selected next perturbations to run, (b) updated world-model weights, and (c) accepted/rejected architecture proposals.

**Key innovation.** Prior virtual-cell pipelines (scGen, CPA, GEARS, and the broader Arc / Recursion virtual-cell wave) train the world model on fixed perturbation datasets and treat experimental design as a downstream step; this paper argues the two should be jointly adapted, with the planner's exploration strategy conditioned on world-model uncertainty and recent error patterns, and architecture moves gated by a validation criterion to prevent catastrophic regression.

**Parameters / training details.** Proof-of-concept uses a synthetic Perturb-seq simulator and a small MLP / transformer world model; planner exploration is uncertainty-weighted; the outer-loop architecture-change criterion compares validation loss + capacity constraints before commit (TBD — exact thresholds in workshop PDF).

**Canonical experiment.** On the toy Perturb-seq simulator, the co-evolutionary loop is compared against a fixed-world-model baseline and a fixed-planner baseline; the paper reports that joint adaptation under validation gating outperforms both, with the architecture-change mechanism preventing the runaway drift that plagues naive joint training (TBD — exact numbers behind workshop PDF).

## Headline benchmarks

This is a **position + proof-of-concept paper**, not a benchmark paper. The Gen² accept frames the contribution as a paradigm for "safe model adaptation" coupled with experimental design. Quantitative comparisons against fixed-world-model baselines are reported in the workshop PDF on toy Perturb-seq simulators (TBD — exact numbers behind PDF parsing).

## Where it fits in the corpus

- **AACR 2026 virtual-cells axis:** direct match — pair with the AACR virtual-cell session and with any cell-state-engineering pharma demos.
- **NeurIPS 2026 LMRL:** the natural next venue for the diffusion-based + real-Perturb-seq version this paper telegraphs.
- **ICML 2026 GenBio:** workshop-level cousin contributions on perturbation planners likely.
- **AACR Pancreatic / Brain Tumors 2026:** longer-term — perturbation planning over tissue-specific cell atlases is the obvious oncology adapt.

## Notes

The paper is workshop-stage and explicitly speculative — it is included as the *concept* anchor for the Gen² "engineering cellular states" theme more than as a method release. The Lewis/Zueco framing — "world model + planner, jointly adapted under validation gating" — is the architecture pattern that AACR-vault agentic-AI dossiers should expect to start emerging from labs like Cradle, Recursion, and Insitro within 6–12 months.
