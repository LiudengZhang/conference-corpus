# TPV Broker

**Dynamic meta-scheduling for Galaxy** — a metascheduler that sits on top of Total Perspective Vortex (TPV), Galaxy's pluggable rules engine for routing jobs to destinations. The broker ranks short-listed destinations across heterogeneous backends (HPC clusters, cloud, on-prem) and distributes load across the usegalaxy.* federation rather than treating each instance as an island.

- **Authors:** Paul De Geest, Sanjay Srikakulam, et al. (usegalaxy-eu / VIB-UGent)
- **Galaxy tool / platform:** [usegalaxy-eu/tpv-broker](https://github.com/usegalaxy-eu/tpv-broker)
- **Source:** [github.com/usegalaxy-eu/tpv-broker](https://github.com/usegalaxy-eu/tpv-broker); core TPV at [galaxyproject/total-perspective-vortex](https://github.com/galaxyproject/total-perspective-vortex)
- **Documentation / training:** [TPV docs (readthedocs)](https://total-perspective-vortex.readthedocs.io/) · [shared rules database](https://github.com/galaxyproject/tpv-shared-database)
- **Status at GBCC2025:** oral talk on cluster-side scheduling for Galaxy

## Talk at GBCC2025

- **Speakers:** Paul De Geest, Sanjay Srikakulam
- **Day / session:** Day 2 (Tue Jun 24, 2025) — Oral Session 2A, Bush Hall
- **Talk title:** "Dynamic meta-scheduling in Galaxy with TPV Broker for smarter workload distribution"
- **Slides:** TBD
- **Video:** TBD
- **Abstract / schedule:** [GBCC2025 program](https://gbcc2025.bioconductor.org/program/scientific_program/)

## What it does

Total Perspective Vortex is a YAML-driven rules engine that maps Galaxy entities (Tools, Users, Roles) to destinations with appropriate resources (cores, GPUs, memory, walltime). TPV Broker plugs into TPV's ranking function: after candidate destinations are short-listed for a job, the broker — operating as a network service across the federation — ranks them based on real-time load, queue state, and policy. The result is dynamic load balancing across usegalaxy.org / .eu / .org.au and partner sites instead of static, per-instance routing.

## Where it fits in the corpus

- **AACR 2026:** infrastructure layer — orthogonal to research axes but underpins reproducibility-at-scale arguments
- **EuroBioC 2025:** no direct counterpart (Bioconductor doesn't have a federation in this sense)
- **Nextflow Summit 2026:** parallel to discussions of executor/cloud burst routing

## Notes

TPV = Total Perspective Vortex (the *Hitchhiker's Guide* reference is intentional). The broker's value proposition only materialises at federation scale — included here as a reminder that the Galaxy infra story is increasingly multi-site, which matters when claiming workflow portability for cancer-research pipelines.
