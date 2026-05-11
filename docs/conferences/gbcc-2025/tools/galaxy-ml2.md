# Galaxy-ML2

**A curated machine-learning tool suite within Galaxy** — Galaxy-ML's pitch is reproducible, auditable, web-driven supervised ML for biomedical scientists. Wraps scikit-learn-compatible pipelines (preprocessing, feature selection, model training, hyperparameter search, evaluation) as Galaxy tools so end-to-end ML analyses ship as Galaxy workflows rather than ad-hoc notebooks.

- **Authors:** Paulo Cilas Morais Lyra Junior, Junhao Qiu, et al. (Goecks lab)
- **Galaxy tool / platform:** [Galaxy ML community hub](https://galaxyproject.org/community/machine-learning/) / [usegalaxy-eu ML workbench](https://usegalaxy-eu.github.io/index-ml)
- **Source:** [github.com/goeckslab/Galaxy-ML](https://github.com/goeckslab/Galaxy-ML)
- **Documentation / training:** [Galaxy-ML docs](https://goeckslab.github.io/Galaxy-ML/)
- **Status at GBCC2025:** oral talk on a curated ML tool suite within Galaxy

## Talk at GBCC2025

- **Speaker:** Paulo Cilas Morais Lyra Junior (lead) with Junhao Qiu
- **Day / session:** Day 2 (Tue Jun 24, 2025) — Oral Session 2A, Bush Hall
- **Talk title:** "The Galaxy-ML2 tool suite: Using Galaxy to promote best practices in machine learning for biomedical data science"
- **Slides:** TBD
- **Video:** [GBCC2025 playlist](https://www.youtube.com/playlist?list=PLdl4u5ZRDMQTJ0O_FIO9ayqaUDfnMo4-4)
- **Abstract / schedule:** [GBCC2025 program](https://gbcc2025.bioconductor.org/program/scientific_program/)

## What it does

Galaxy-ML2 is the next generation of Galaxy-ML: a unified scikit-learn-compatible pipeline framework exposed as Galaxy tools, with companion Galaxy-Ludwig deep-learning tools sitting alongside. Users assemble preprocessor + estimator + search-cv pipelines in the Galaxy UI, run them at scale on shared infrastructure, and ship the resulting workflow as a single shareable artefact. Validation is published in *PLOS Comp Bio* (Gu et al. 2021) and the suite is actively maintained.

## Where it fits in the corpus

- **AACR 2026:** axes = bioinfo-tools and (loosely) agentic-AI — this is classical ML wrapped for reproducibility, not LM-driven, so it complements rather than overlaps GAIA / GalaxyMCP
- **GAIA** ([entry](gaia.md)) and **GalaxyMCP** ([entry](galaxymcp.md)) — same Goecks-lab umbrella; ML2 supplies the underlying tools an agent might invoke
- **Nextflow Summit 2026:** thematic overlap with reproducible-ML pipeline storylines

## Notes

Galaxy-ML's enduring pitch is reproducible/auditable ML pipelines — relevant when biomedical ML needs to ship in regulated contexts (clinical decision support, FDA-relevant work). The "v2" framing at GBCC suggests a re-architecture pass; verify scope from talk slides.
