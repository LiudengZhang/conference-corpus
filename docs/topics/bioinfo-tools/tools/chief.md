# CHIEF

**Family:** path-fm
**Modality:** H&E whole-slide image patches (256×256, ~10×–20×) and slide-level aggregation
**Released:** 2024 (Nature)
**License:** AGPL-3.0, non-commercial academic use only
**Code/checkpoint:** [github.com/hms-dbmi/CHIEF](https://github.com/hms-dbmi/CHIEF) (weights gated via repo request form)
**Also surfaced in:** agentic-ai, single-cell-spatial-omics, virtual-cells

> CHIEF (Clinical Histopathology Imaging Evaluation Foundation) is a
> two-stage pathology foundation model from the Mahmood Lab that maps
> H&E whole-slide images to patch- and slide-level embeddings for
> cancer detection, subtyping, biomarker prediction, and outcome
> stratification. It is trained on a multi-cancer cohort spanning 19
> anatomical sites and is positioned as a generalist model whose
> embeddings can be reused across downstream histology tasks without
> task-specific retraining.

## Architecture & training

CHIEF is built in two stages: a CTransPath-based patch encoder
(CHIEF-CTransPath) producing 768-dimensional tile embeddings, and a
weakly supervised attention-based aggregator that pools tile features
into a slide-level representation. Patch-level pretraining uses
self-supervised contrastive learning over ~15 million tiles drawn from
~60,530 whole-slide images spanning 19 anatomical sites (~44 TB of
pixel data); the slide-level head is then trained with anatomic-site
conditioning so embeddings carry organ context. The released
checkpoints are evaluated across 19,491 WSIs from 32 independent
cohorts at 24 hospitals, with reported gains on cancer detection,
genomic biomarker prediction, and survival prediction relative to
prior pathology backbones.

## Use in the AACR 2026 corpus

<!-- mentions:start -->

**Posters mentioning CHIEF (n=0):**

_No posters in the AACR 2026 corpus mention this tool._

**Sessions mentioning CHIEF (n=6):**

- [2026-04-18-ai-in-biomarker-discovery-and-drug-development](../../../sessions/2026-04-18-ai-in-biomarker-discovery-and-drug-development.md)
  …wever, that he was able to send his recorded talk. So we'll get there in a second. I'm George Visilo. I'm the Chief AI for Science Innovation at AstraZeneca, and I'm going to pass here to my impromptu co-chair. Hi. Very nice…
- [2026-04-19-gastric-gastroesophageal-cancer-dynamics](../../../sessions/2026-04-19-gastric-gastroesophageal-cancer-dynamics.md)
  …cling tuft cell into the secretory progenitor. And at the opposite end of the spectrum, these are the gastric chief stem cells. Whereas in metaplastic organoid, you can see they are more complex. So from the cycling isthmus s…
- [2026-04-20-am-plasticity-cancer-progression-clarkson-symposium](../../../sessions/2026-04-20-am-plasticity-cancer-progression-clarkson-symposium.md)
  Morning, everybody. My name is Bill Heit, and I'm honored to serve currently as the AACR Chief Scientific Advisor, but it's really my even greater honor to introduce today's symposium in honor of my frien…
- [2026-04-20-pm-ai-spatial-transcriptomics-pathology](../../../sessions/2026-04-20-pm-ai-spatial-transcriptomics-pathology.md)
  …ry and development. In this virtual biotech, it's a team of tens of thousands of AI agents, which is led by a chief scientist officer, or CSO agent, and working under the CSO agent, we have these different divisions, which co…
- [2026-04-20-pm-late-microenvironmental-determinants-tumor-evolution-immune-escape](../../../sessions/2026-04-20-pm-late-microenvironmental-determinants-tumor-evolution-immune-escape.md)
  …For gastric regeneration, we primarily use a high-dose tamoxifen model, which induces parietal cell loss and chief cell loss, and triggers PEN, a kind of metaplastic response, and normally resolve back to histological baseli…
- [2026-04-22-agentic-ai-as-the-oncologist](../../../sessions/2026-04-22-agentic-ai-as-the-oncologist.md)
  …ion Support and Human AI Collaboration. My name is Renato Umeton. I'm the Vice President of Data Sciences and Chief of AI for St. Jude Children's Research Hospital. And today we're going to explore this session with two giant…

<!-- mentions:end -->

## What's missing / where evidence is weak

- TODO

## Takeaway

TODO — one paragraph on what the AACR 2026 corpus uniquely teaches us
about CHIEF.
