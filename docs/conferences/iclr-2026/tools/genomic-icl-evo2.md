# Genomic Next-Token Predictors are In-Context Learners — Breslow et al. (JHU)

**One-line description** — A controlled-experiment study showing that the Evo2 genomic foundation model exhibits *organically emergent* in-context learning on symbolic reasoning tasks in genomic form, with log-linear gains as in-context demonstrations scale — mirroring large language model ICL behaviour.

- **Authors:** Nathan Breslow, Aayush Mishra, Michael Schatz, Anqi Liu, Mahler Revsine, Daniel Khashabi
- **Affiliation(s):** Johns Hopkins University (Schatz, Khashabi groups)
- **Track / workshop:** ICLR 2026 — **Sci4DL workshop** (Science for Deep Learning)
- **OpenReview:** [forum?id=BJxPhTcrsr](https://openreview.net/forum?id=BJxPhTcrsr)
- **Code:** TBD — JHU groups typically release on github post-meeting
- **Status at ICLR 2026:** Sci4DL workshop accepted paper; March 2, 2026 acceptance

## What it does

The paper asks whether *in-context learning* — the well-known LLM phenomenon where models infer and apply patterns from a few in-context examples — emerges naturally in genomic foundation models trained on DNA next-token prediction. The answer is yes: Evo2 (Arc Institute's 40B-parameter, 1Mb-context DNA model) exhibits ICL on symbolic reasoning tasks framed in genomic form, with log-linear gains as the number of in-context demonstrations grows. The contribution is *the first systematic evidence of organically emergent ICL in genomic sequences*.

## How it works

The methodology is a paired controlled experiment: identical symbolic reasoning tasks are encoded both in natural-language form (presented to a language model like Qwen3) and in genomic form (presented to Evo2). The in-context demonstration count is varied; ICL is measured as task accuracy versus number of demonstrations. The log-linear scaling is the load-bearing result — it suggests Evo2's pretraining on 9.3 trillion nucleotides has induced general-purpose pattern-induction capabilities, not just sequence-specific memorisation.

## Headline benchmarks

The paper reports **log-linear gains in pattern induction as the number of in-context demonstrations increases**, matching the canonical LLM ICL scaling behaviour. Specific accuracy curves and task-suite definitions are in the workshop PDF (TBD — full numbers).

## Where it fits in the corpus

- **AACR 2026 virtual-cells axis:** indirect — ICL in genomic LMs is the methodological precondition for using these models as zero-shot variant-effect predictors over patient genomes.
- **ICML 2026 LCFM (long-context FM workshop):** primary venue for follow-on work on context scaling and ICL in DNA LMs.
- **NeurIPS 2026:** Evo2 is the headline genomic-FM release of 2025–2026; expect a NeurIPS paper from Arc Institute itself.
- **AGBT 2026:** likely Evo2 application demos at the platform session.
- **ASHG 2026 / ESHG 2026:** clinical-genomics adaptation venues.

## Notes

Evo2 itself (Arc Institute, Hyena-based, 40B params, 1Mb context) was published in *Nature* March 2026; this ICLR 2026 Sci4DL paper is a methodological study *of* Evo2 rather than a new model release. It serves the AACR vault's "long-context genomic LM" slot as the canonical 2026-era reference point — and the JHU-led "Evo2 as in-context learner" framing is the bridge between the genomic-FM and LLM-reasoning communities that the AACR agentic-AI axis sits on top of. The Sci4DL workshop venue (not LMRL or MLGenX) is itself notable — this is methods-paper community, not bio community, signalling that genomic LMs are now methodologically interesting *on their own terms*.
