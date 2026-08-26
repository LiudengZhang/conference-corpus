# Resource cards added to HRD-CCR8 vault — 2026-06-04

Vault: `papermap_fresh/examples/hrd-ccr8-pancancer.yaml`
Item count: 186 → 236 (+50 dataset cards)

## Top 3 to read

1. **Luo 2024 NANT** (`luo-2024-nant-ovarian`) — Cell 2024, GSE222556 — the project anchor.
2. **Färkkilä 2020 TOPACIO** (`farkkila-2020-topacio`) — Nat Commun 2020 — niraparib + pembro mIF + WES, treatment-causal.
3. **MSK-SPECTRUM** (`vazquez-garcia-2022-mskspectrum`) — Nature 2022 — n≈42 HGSOC scWGS-DLP+ + scRNA + multi-site.

## 50 cards added (by batch)

**Batch 1 — Bucket A sc/sn (10):** pelka-2021-crc, lee-2020-crc-korea, maynard-2020-nsclc-longitudinal, neftel-2019-gbm, karaayvaz-2018-tnbc, puram-2017-hnscc, kim-2020-nsclc-mets, tirosh-2016-melanoma, jerby-arnon-2018-mel, stewart-2020-sclc-cdx

**Batch 2 — Bucket A sc/sn (10):** wang-2021-gastric-peritoneal, zhang-2022-gastric-tcell, couturier-2020-gbm, lambrechts-2018-nsclc, goveia-2020-nsclc-ec, sun-2021-hcc-early-relapse, kim-2018-tnbc-chemoresist, hwang-lin-2023-pdac-chemo, htan-hta3-bu-lung-precancer, su-2025-hcc-snrna

**Batch 3 — Bucket B/C spatial (11):** erickson-2022-prostate-visium, khaliq-sun-2024-pdac, pei-min-2025-pdac-autopsy, wu-2025-hgsoc-visium-hd, ji-2020-cscc-st, risom-2022-dcis-mibi, jackson-2020-breast-imc, tietscher-2023-breast-imc, ali-danenberg-2020-metabric-imc, magness-enfield-2024-tracerx-imc, makhmut-coscia-2025-stic-dvp

**Batch 4 — HTAN sub-atlases (10):** htan-hta4-chop-pediatric, htan-hta5-dfci-resistance, htan-hta6-duke-stanford-dcis, htan-hta7-hms-patch-sorger, htan-hta8-msk-metastasis, htan-hta9-ohsu-smmart-mbc, htan-hta10-stanford-fap, htan-hta11-vanderbilt-crc, htan-hta12-wustl-pancancer, htan-hta8-sclc-chan-2021

**Batch 5 — non-HTAN Bucket D (9):** mskspectrum-cfdna-parpi-2025, owkin-mosaic-window-bladder, htapp-klughammer-2024-mbc, hwang-2025-pdac-neural, sun-2024-hcc-primary-met, liu-2024-pediatric-hgg-filbin, ravi-2022-gbm-multiomics, greenwald-2024-gbm-suva-tirosh, denisenko-2024-hgsoc-visium-cosmx

## 8 cards carry `# TODO: verify`

These flag accession mismatches surfaced against published GEO/EGA records — the cohort_manifest.tsv accessions are wrong for these rows and must be corrected before download.

| cohort_id | manifest accession | actual accession (best guess) | severity |
|---|---|---|---|
| zhang-2022-gastric-tcell | GSE183904 (scRNA only) | WES + scTCR deposited elsewhere | minor |
| **couturier-2020-gbm** | GSE163108 (this is Mathewson 2021, not Couturier!) | EGA EGAS00001004422 | **MAJOR** |
| **sun-2021-hcc-early-relapse** | GSE149614 (this is Lu Y 2021, not Sun!) | unresolved | **MAJOR** |
| **hwang-lin-2023-pdac-chemo** | GSE205013 (this is Simeone, not Hwang) | GSE199102 + dbGaP phs002371 | **MAJOR** |
| su-2025-hcc-snrna | OK accession; mismatch is scRNA-not-snRNA | n/a | flag only |
| pei-min-2025-pdac-autopsy | UNVERIFIED in manifest | Nature 642:212 (2025) — accession still pending | known deferred |
| wu-2025-hgsoc-visium-hd | UNVERIFIED in manifest | bioRxiv 10.1101/2025.11.24.690313 | known deferred |
| risom-2022-dcis-mibi | Synapse syn17773547 candidate | needs Mendeley/Synapse confirmation | minor |
| hwang-2025-pdac-neural | UNVERIFIED in manifest | likely Chen 2025 Cancer Cell (different author) | known deferred |
| sun-2024-hcc-primary-met | NOT-LOCATED in manifest | likely EGA / GSA mainland-China | known deferred |

## Recommended next step

Patch `cohort_manifest.tsv` accession_primary column for the three **MAJOR** mismatches before the server-side agent starts the download wave — otherwise the agent will pull the wrong cohort.
