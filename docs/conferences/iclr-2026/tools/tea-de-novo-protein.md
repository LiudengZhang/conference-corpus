# Reading TEA Leaves for de novo Protein Design — Pantolini & Durairaj (Basel)

**One-line description** — A protein-language-model-derived 20-letter "TEA" alphabet enables fast Monte-Carlo de-novo protein design without invoking expensive structure-prediction oracles inside the inner loop, expanding the functional protein design space at a fraction of prior compute cost.

- **Authors:** Lorenzo Pantolini, Janani Durairaj
- **Affiliation(s):** SIB Swiss Institute of Bioinformatics / University of Basel (Schwede lab adjacent)
- **Track / workshop:** ICLR 2026 — **LMRL workshop oral talk** (Apr 27, 2026; 16:13 oral slot)
- **OpenReview:** TBD — workshop PDF not yet directly linked
- **bioRxiv:** [10.64898/2026.02.09.704813v2](https://www.biorxiv.org/content/10.64898/2026.02.09.704813v2)
- **Code:** TBD — Durairaj lab github
- **Status at ICLR 2026:** LMRL workshop **Oral** (12-min slot)

## What it does

The paper attacks the Monte-Carlo bottleneck in de novo protein design: classical MCMC over sequence space is under-explored because each step either requires a slow structure-prediction oracle (AlphaFold/Boltz/ESMFold-class) or a noisy proxy. The contribution is **TEA**, a learned 20-letter alphabet derived from contrastive training over protein-language-model embeddings, which captures functional equivalence classes well enough to substitute for full structure prediction inside the MCMC inner loop.

## How it works

A contrastive learning objective is applied to protein-LM embeddings to produce a compact 20-letter discrete alphabet ("TEA") that aligns with functional / fold-class equivalence rather than literal sequence identity. The same alphabet had previously been shown to enable highly efficient large-scale homology searches (Durairaj's earlier work). In de-novo design mode, MCMC proposals are scored in TEA-space instead of via folding, dramatically accelerating the sampler; structure prediction is reserved for final candidate verification.

## Headline benchmarks

The bioRxiv preprint reports "highly efficient large-scale protein homology search" performance for the TEA alphabet, and demonstrates Monte-Carlo de-novo design over functional targets at compute cost far below structure-oracle-in-the-loop baselines (TBD — exact wall-clock and success-rate numbers from bioRxiv v2 PDF).

## Where it fits in the corpus

- **AACR 2026:** drug-discovery axis — design of small protein binders for cancer targets without full Boltz inside the loop.
- **GEM workshop sibling:** the GEM RBX-1 binder competition is the natural benchmark for TEA-driven design pipelines.
- **NeurIPS 2026 MLSB:** likely follow-on with experimental validation.
- **ESHG / ASHG 2026:** protein-variant effect prediction is the diagnostic adaptation.

## Notes

Janani Durairaj's TEA-alphabet line of work bridges the protein-LM-embeddings and protein-design communities — the same alphabet that enabled efficient homology search (Nature 2023, "Uncovering new families and folds in the natural protein universe") is being repurposed for generative inner loops. The ICLR 2026 LMRL oral slot signals the community sees this as the next step beyond RFdiffusion / Boltz-driven design for the "design-at-scale" regime where the structure-oracle cost dominates. Pair with Proteina-Complexa (NVIDIA, this vault) as the two methodological poles of 2026 protein design — one scales by atomistic generative pretraining + test-time compute, the other scales by sidestepping the oracle entirely.
