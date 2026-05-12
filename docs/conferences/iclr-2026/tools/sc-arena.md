# SC-Arena — Jiahao Zhao et al.

**One-line description** — A natural-language benchmark for single-cell reasoning that formalises a "virtual cell" abstraction and evaluates LLMs / single-cell foundation models with knowledge-augmented metrics across five biological tasks.

- **Authors:** Jiahao Zhao, Feng Jiang, Shaowei Qin, Zhonghui Zhang, Junhao Liu, Guibing Guo, Hamid Alinejad-Rokny, Min Yang
- **Affiliation(s):** Shenzhen Institute of Advanced Technology (Chinese Academy of Sciences); Northeastern University (Shenyang); UNSW Sydney — affiliations inferred from co-author roster, TBD-verify
- **Track / workshop:** ICLR 2026 main track — Poster
- **OpenReview:** [forum?id=5RcoUe1tA1](https://openreview.net/forum?id=5RcoUe1tA1)
- **arXiv:** [2602.23199](https://arxiv.org/abs/2602.23199)
- **Code:** TBD — not surfaced in OpenReview camera-ready
- **Status at ICLR 2026:** Poster, Sat Apr 25 (Pavilion 3); license CC-BY 4.0

## What it does

SC-Arena reframes the evaluation problem for single-cell foundation models (scGPT, Geneformer, UCE, CellFM and their LLM-conditioned cousins) as a *natural-language reasoning* benchmark. Instead of measuring embedding quality with proxy metrics, it formalises a "virtual cell" abstraction unifying intrinsic cell attributes and gene-level interactions, then probes models with five free-form tasks: cell-type annotation, captioning, generation, perturbation prediction, and scientific QA.

## How it works

**Core idea.** SC-Arena reformulates single-cell foundation-model evaluation as natural-language reasoning over a "virtual cell" abstraction that unifies intrinsic cell attributes with gene-level interaction context, replacing brittle string-match metrics with a knowledge-augmented scoring pipeline.

**Inputs / outputs.** Inputs are single-cell expression profiles (or their tokenised foundation-model embeddings) plus a free-form natural-language probe; outputs are model responses for five tasks — cell-type annotation, captioning, generation, perturbation prediction, and scientific QA — each scored against ontology- and literature-grounded ground truth.

**Key innovation.** Prior benchmarks (Geneformer / scGPT / UCE / CellFM evaluations) lean on exact-match cell-type F1 or embedding probing; SC-Arena instead uses evidence-grounded knowledge-augmented metrics that consult Cell Ontology, GO, curated marker databases, and the scientific literature to score biological faithfulness with interpretable rationales.

**Parameters / training details.** SC-Arena is an evaluation benchmark (no new model training). Evaluated systems span general-purpose LLMs (GPT-4o-class) and domain-specialised single-cell LMs; scoring weights across the five tasks and the per-task knowledge-base lookups are released as configurable benchmark assets (TBD — exact weighting from camera-ready).

**Canonical experiment.** The paper benchmarks scGPT, Geneformer, UCE, CellFM, and LLM-conditioned cousins side-by-side across the five tasks. Knowledge-augmented metrics consistently re-rank models versus string-matching baselines, and the authors report "uneven performance on biologically complex tasks, particularly those demanding mechanistic or causal understanding" — the load-bearing methodological finding.

## Headline benchmarks

The paper reports "uneven performance on biologically complex tasks, particularly those demanding mechanistic or causal understanding." Specific per-model numbers are reported in the camera-ready tables (TBD — full PDF behind login). Knowledge-augmented metrics consistently rank models differently from string-matching baselines, supporting the methodological argument.

## Where it fits in the corpus

- **AACR 2026:** virtual-cells axis anchor — pair with the AACR virtual-cell methodology session and any TissueAgent / pan-tumor cell-atlas tool entries.
- **NeurIPS 2026:** likely cousin contribution at the NeurIPS LMRL re-run (Dec 2026) — same evaluation framework, expanded benchmark suite expected.
- **ICML 2026:** GenBio / FM4LS workshop submissions in July may target this benchmark directly.
- **ISMB 2026:** scaffold — cell-type-annotation benchmarks overlap.

## Notes

This is the LMRL community's explicit answer to "how do you actually score a virtual cell?" — the 2024–2025 scGPT/Geneformer wave was evaluated mostly on cell-typing F1; SC-Arena's task suite (especially scientific QA + perturbation prediction) reframes virtual-cell quality as scientific-reasoning quality. Mark TBD on exact per-model leaderboard ranks until camera-ready PDF is parsed in full.
