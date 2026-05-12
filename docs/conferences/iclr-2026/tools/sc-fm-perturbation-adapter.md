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

**Core idea.** Freeze a pretrained single-cell foundation model (scGPT / Geneformer / scFoundation / scMulan-class) and insert a small drug-conditional adapter (<1 % of base parameters) that modulates cell-token representations conditional on a query drug — preserving pretrained cell knowledge while learning the perturbation map.

**Inputs / outputs.** Inputs are (a) a control single-cell expression profile / token sequence and (b) a query drug representation (SMILES or molecular graph — TBD-verify against camera-ready); output is the predicted perturbed expression profile.

**Key innovation.** Prior perturbation predictors fall into two camps: train-from-scratch supervised models (scGen, CPA, GEARS, ChemCPA) that don't leverage the cell-knowledge encoded in foundation-model pretraining, and full-fine-tune approaches that overfit on small perturbation datasets. The adapter-based approach gives zero-shot generalisation to *unseen* drugs and *unseen* cell lines at <1 % trainable-parameter cost — the key gap closed.

**Parameters / training details.** Adapter size: <1 % of base FM parameters. Base FMs: scGPT, Geneformer, scFoundation, scMulan-class (multiple base models swept). Training data: limited perturbation datasets (Perturb-seq / drug-screen-class). The adapter projects molecular structure into the FM's cell-token modulation space.

**Canonical experiment.** Across multiple zero-shot evaluation scenarios — held-out drugs and held-out cell lines — the adapter reports state-of-the-art performance vs scGen / CPA / GEARS baselines, with the headline gains concentrated in *few-shot and zero-shot generalisation to new cell types* (TBD — exact per-task PCC / MMD from camera-ready). The Nature Methods 2025 Csendes et al. linear-baseline caveat applies: any deep-perturbation claim should be checked against the simple baselines.

## Headline benchmarks

The paper reports **state-of-the-art performance across multiple evaluation scenarios**, with the headline gains in **few-shot and zero-shot generalisation to new cell types compared to existing baselines** (scGen, CPA, GEARS-class). Exact per-task PCC and MMD numbers are in the camera-ready tables (TBD — parse from PDF).

## Where it fits in the corpus

- **AACR 2026 virtual-cells axis:** primary cross-link — perturbation prediction is the load-bearing downstream task for virtual-cells claims. Pair with any cell-state-engineering AACR dossier.
- **GBCC 2025 / EuroBioC 2025:** no direct R/Bioconductor implementation, but conceptually adjacent to perturbation-modelling sessions.
- **NeurIPS 2026 LMRL:** likely follow-on with extended molecular conditioning.
- **AACR Pancreatic 2026 / SITC 2026:** primary translational hook — drug-response prediction over pancreatic / immuno-onc cell lines.

## Notes

Prescient Design / Genentech is the same group that ships LBSTER and related single-cell tooling; the lineage here is "use the pretrained scFoundation-class model + a thin adapter" rather than "train a new bigger model" — the parameter-efficiency framing matters because it is the pattern most likely to be adopted by smaller oncology-focused groups that cannot afford fresh pretraining runs. Note the **Nature Methods 2025 caveat**: linear baselines remain competitive with deep methods on this task, so any 2026 perturbation-prediction claim should be checked against the Csendes et al. simple-baseline analysis.
