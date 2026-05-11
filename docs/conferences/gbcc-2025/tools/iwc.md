# Intergalactic Workflow Commission (IWC)

**Curated, tested, versioned registry of reproducible Galaxy workflows** — the Galaxy ecosystem's answer to "how do we standardize, test, and distribute community workflows?" IWC ingests workflow contributions, runs CI tests against reference data, versions releases, and publishes them so any Galaxy server can install a known-good copy.

- **Galaxy tool / platform:** [iwc.galaxyproject.org](https://iwc.galaxyproject.org/)
- **Source:** [github.com/galaxyproject/iwc](https://github.com/galaxyproject/iwc)
- **Documentation / training:** [iwc.galaxyproject.org](https://iwc.galaxyproject.org/) and the [Galaxy Training Network](https://training.galaxyproject.org/)
- **Lead author at GBCC2025:** Marius van den Beek
- **Status at GBCC2025:** workflow infrastructure / standardization

## Talk at GBCC2025

- **Speaker:** Marius van den Beek
- **Day / session:** Day 3 (Wed Jun 25, 2025) — Oral Session 3, Grace Auditorium
- **Talk title:** "The Intergalactic Workflow Commission: Standardizing, Testing, and Distributing Reproducible Galaxy Workflows"
- **Slides:** TBD
- **Video:** [GBCC2025 playlist](https://www.youtube.com/playlist?list=PLdl4u5ZRDMQTJ0O_FIO9ayqaUDfnMo4-4)
- **Abstract / schedule:** [GBCC2025 program](https://gbcc2025.bioconductor.org/program/scientific_program/)

## What it does

IWC sits between workflow authors and Galaxy server admins. Authors PR a `.ga` workflow plus a test definition; CI runs the workflow on reference inputs and validates outputs; on merge, the workflow is versioned and published. Galaxy admins (and `usegalaxy.*` mirrors) can pull releases via Ephemeris into their tool panel, knowing each version was machine-tested. The system enforces metadata (license, author, tags), tracks tool dependencies via Conda / containers, and supports semver releases so reruns of an old version are reproducible long after publication.

## Where it fits in the corpus

- **AACR 2026:** axis = bioinfo-tools (workflow-as-code / reproducibility — the substrate beneath any analysis claim that wants to survive review)
- **Nextflow Summit 2026** ([cross-vault](../../nextflow-2026/index.md)) — IWC is to Galaxy what nf-core is to Nextflow: a curated, tested registry sitting on top of a workflow language. Worth tracking which conventions converge.
- **bioc-to-galaxy** ([entry](bioc-to-galaxy.md)) — auto-wrapped Bioconductor tools eventually flow into IWC-curated workflows
- **Workshop Platform** ([cross-vault](../../eurobioc-2025/tools/workshop-platform.md)) — IWC workflows are frequent tenants of hands-on tutorials

## Notes

The nf-core analogy is the fastest way in: IWC is the curation layer, not the runtime. Galaxy itself is the engine; IWC is the package index. Standardizing test fixtures across community workflows is the durable contribution — it converts "works on my server" into "passes CI on a clean install."
