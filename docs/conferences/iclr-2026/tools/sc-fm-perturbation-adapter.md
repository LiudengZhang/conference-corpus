# Efficient Fine-Tuning of Single-Cell FMs for Zero-Shot Perturbation Prediction — Maleki et al. (Genentech)

**One-line description** — A drug-conditional adapter for pretrained single-cell foundation models that adds <1 % trainable parameters yet enables zero-shot prediction of cellular responses to *novel* drugs and generalisation to *unseen* cell lines.

- **Authors:** Sepideh Maleki, Jan-Christian Huetter, Kangway V. Chuang, Gabriele Scalia, Tommaso Biancalani
- **Affiliation(s):** Prescient Design / Genentech (Roche)
- **Track / workshop:** ICLR 2026 LMRL workshop — paper continuation of the ICLR 2025 main-track submission
- **OpenReview:** [forum?id=tKn6gpvlUX](https://openreview.net/forum?id=tKn6gpvlUX)
- **arXiv:** [2412.13478v2](https://arxiv.org/html/2412.13478v2)
- **Code:** TBD — Prescient Design typically releases on github.com/genentech post-camera-ready
- **Status at ICLR 2026:** workshop continuation (originally accepted ICLR 2025; LMRL 2026 re-presentation with extended ablations)

## What it does

This paper attacks the single-cell perturbation-prediction problem by *re-using* large pretrained single-cell foundation models (scGPT, Geneformer, scFoundation, scMulan-class) rather than training new architectures from scratch. The contribution is a parameter-efficient drug-conditioning adapter that lets the foundation model respond to molecular perturbations it never saw at pretraining, while preserving the broad cellular knowledge encoded in the base weights.

## How it works

A drug-conditional adapter — fewer than 1 % of the original foundation-model parameters — is inserted on top of the pretrained single-cell LM and trained on a limited perturbation dataset. The adapter encodes molecular structure (likely a SMILES-conditioned or molecular-graph projection — TBD-verify against camera-ready) and modulates the cell-token representations of the base model. At inference, the model takes a control-cell embedding and a query drug, and predicts the perturbed expression profile zero-shot — even for unseen drugs and unseen cell types.

## Headline benchmarks

The paper reports **state-of-the-art performance across multiple evaluation scenarios**, with the headline gains in **few-shot and zero-shot generalisation to new cell types compared to existing baselines** (scGen, CPA, GEARS-class). Exact per-task PCC and MMD numbers are in the camera-ready tables (TBD — parse from PDF).

## Where it fits in the corpus

- **AACR 2026 virtual-cells axis:** primary cross-link — perturbation prediction is the load-bearing downstream task for virtual-cells claims. Pair with any cell-state-engineering AACR dossier.
- **GBCC 2025 / EuroBioC 2025:** no direct R/Bioconductor implementation, but conceptually adjacent to perturbation-modelling sessions.
- **NeurIPS 2026 LMRL:** likely follow-on with extended molecular conditioning.
- **AACR Pancreatic 2026 / SITC 2026:** primary translational hook — drug-response prediction over pancreatic / immuno-onc cell lines.

## Notes

Prescient Design / Genentech is the same group that ships LBSTER and related single-cell tooling; the lineage here is "use the pretrained scFoundation-class model + a thin adapter" rather than "train a new bigger model" — the parameter-efficiency framing matters because it is the pattern most likely to be adopted by smaller oncology-focused groups that cannot afford fresh pretraining runs. Note the **Nature Methods 2025 caveat**: linear baselines remain competitive with deep methods on this task, so any 2026 perturbation-prediction claim should be checked against the Csendes et al. simple-baseline analysis.
