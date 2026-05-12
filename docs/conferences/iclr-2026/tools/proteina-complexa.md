# Proteina-Complexa — Didi, Zhang, Kreis et al. (NVIDIA + Mila + Oxford + SNU)

**One-line description** — A fully atomistic protein-binder design method unifying flow-based generative pretraining (built on La-Proteina) with inference-time test-time-compute optimisation, achieving up to 63.5 % in-silico hit rate against PDGFR plus nanomolar binders to Nipah-virus glycoprotein and a myostatin-pathway receptor.

- **Authors:** Kieran Didi, Zuobai Zhang, Guoqing Zhou, Danny Reidenbach, Zhonglin Cao, Sooyoung Cha, Tomas Geffner, Christian Dallago, Jian Tang, Michael M. Bronstein, Martin Steinegger, Emine Kucukbenli, Arash Vahdat, Karsten Kreis
- **Affiliation(s):** NVIDIA; Mila / Université de Montréal / HEC Montréal; University of Oxford; Seoul National University
- **Track / workshop:** ICLR 2026 main track — **Oral / Poster** (Sat Apr 25, Pavilion 3 P3-#1718; Oral session)
- **OpenReview:** [forum?id=qmCpJtFZra](https://openreview.net/forum?id=qmCpJtFZra)
- **Project page:** [research.nvidia.com/labs/genair/proteina-complexa](https://research.nvidia.com/labs/genair/proteina-complexa/)
- **Code:** [github.com/NVIDIA-Digital-Bio/proteina-complexa](https://github.com/NVIDIA-Digital-Bio/proteina-complexa)
- **arXiv:** [2603.27950](https://arxiv.org/abs/2603.27950)
- **Status at ICLR 2026:** Main-track Oral

## What it does

Proteina-Complexa generates fully atomistic protein binders against protein and small-molecule targets. It unifies two design paradigms that were previously separate: (a) generative flow-matching models for protein structure, and (b) hallucination / inference-time optimisation against a structure-prediction oracle. The result is a single pipeline that emits binders with both high generative diversity and high computed hit rate.

## How it works

The base generative model extends La-Proteina, a flow-matching architecture for atomistic protein generation, with a binder-conditioning track. Pretraining uses **Teddymer**, a synthetic dataset built from domain-domain interactions of computationally predicted monomeric structures — sidestepping the experimental binder dataset bottleneck. At inference, novel test-time-compute strategies (latent generative search, normalised against fixed compute budgets) outperform classical hallucination loops. The method generalises beyond simple protein targets to small-molecule docking, enzyme design, fold-class-guided generation, and interface hydrogen-bond optimisation.

## Headline benchmarks

- **63.5 % hit rate against PDGFR** (in-silico) — state of the art on the standard generative-binder benchmark suite.
- **Nanomolar binders against Nipah virus** glycoprotein.
- **Nanomolar binders against a muscle-wasting receptor** blocking myostatin signalling in cells.
- **First de novo carbohydrate binders** demonstrated.
- Markedly higher in-silico success rate than prior generative binder methods; novel test-time strategies beat prior hallucination methods under matched compute.

## Where it fits in the corpus

- **AACR 2026:** drug-discovery axis — pair with any RFdiffusion / Boltz-class binder dossiers in the AACR vault. PDGFR is the explicit cancer-target hook (PDGFR signalling is a known oncology pathway).
- **GEM workshop sibling:** the GEM workshop's RBX-1 binder competition (RBX-1 = cancer-relevant E3 ligase) is the natural follow-on benchmark.
- **NeurIPS 2026 MLSB / ICML 2026 GenBio:** expect an extended version with wet-lab follow-up.
- **MICCAI 2026 / AACR 2026 wet-lab confirmation:** Bronstein / Steinegger / NVIDIA likely to ship a follow-on at SITC or AACR with experimental validation of the oncology targets.

## Notes

This is the headline biomolecular-design paper of ICLR 2026 — the NVIDIA + Mila + Oxford + SNU consortium is the same team that shipped La-Proteina in 2025; Complexa is the binder-conditioned successor. The "test-time-compute" framing — scaling sampling at inference rather than at training — is shared with the broader 2025–2026 reasoning-LLM trend and is one of the methodological bridges between ICLR's LLM and bio tracks. NVIDIA's developer-blog companion piece confirms the public github release and pretrained checkpoints.
