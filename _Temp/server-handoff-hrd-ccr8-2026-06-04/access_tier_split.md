# access tier split

Derived from `cohort_manifest.tsv`. Three lists: what you can download today, what needs paperwork now, what stays deferred.

## tier-0 — immediate download (no application)

GEO / ArrayExpress / SRA / Broad SCP / Zenodo / PRIDE / 10x portal. Just pull.

- luo-2024-nant-ovarian (GEO `GSE222556`) — **start here; project anchor**
- pal-2021-brca1-breast (GEO `GSE161529`)
- olbrecht-2021-hgsoc (ArrayExpress `E-MTAB-8107`)
- karaayvaz-2018-tnbc (GEO `GSE118390`)
- kim-2018-tnbc-chemoresist (SRA `SRP114962`)
- stur-2022-hgsoc-visium (GEO `GSE211956`)
- khaliq-sun-2024-pdac (GEO `GSE272362`)
- ji-2020-cscc-st (GEO `GSE144236`)
- pelka-2021-crc (GEO `GSE178341`) — processed; raw on dbGaP `phs002407`
- lee-2020-crc-korea (GEO `GSE132465`)
- yost-2019-bcc (GEO `GSE123813`)
- caushi-2021-nsclc (GEO `GSE176021`)
- luoma-2022-hnscc (GEO `GSE200996`)
- sade-feldman-2018-mel (GEO `GSE120575`)
- bi-2021-ccrcc (Broad SCP `SCP1288`) — sc-processed open; WES via dbGaP
- neftel-2019-gbm (Broad SCP `SCP393` + GEO `GSE131928`)
- puram-2017-hnscc (GEO `GSE103322`)
- tirosh-2016-melanoma (GEO `GSE72056`)
- jerby-arnon-2018-mel (GEO `GSE115978`)
- wang-2021-gastric-peritoneal (GEO `GSE163558`)
- zhang-2022-gastric-tcell (GEO `GSE183904`)
- couturier-2020-gbm (GEO `GSE163108`)
- lambrechts-2018-nsclc (ArrayExpress `E-MTAB-6149`)
- goveia-2020-nsclc-ec (ArrayExpress `E-MTAB-8221`)
- sun-2021-hcc-early-relapse (GEO `GSE149614`)
- hwang-lin-2023-pdac-chemo (GEO `GSE205013`) — raw on dbGaP `phs002371`
- su-2025-hcc-snrna (GEO `GSE282701`)
- liu-2024-pediatric-hgg-filbin (GEO `GSE231860`)
- ravi-2022-gbm-multiomics (GEO `GSE194329`)
- greenwald-2024-gbm-suva-tirosh (GEO `GSE237183` + Zenodo `10.5281/zenodo.8105466`)
- hwang-2022-pdac-neoadj (GEO `GSE202051`) — raw on dbGaP `phs002789`
- wu-2021-breast-visium (GEO `GSE176078`)
- jackson-2020-breast-imc (Zenodo `4607374`)
- tietscher-2023-breast-imc (Zenodo `7647079`)
- ali-danenberg-2020-metabric-imc (Zenodo `6036188`) — IMC open; genomic via METABRIC `EGAS00000000083` (controlled)
- magness-enfield-2024-tracerx-imc (Zenodo `12587543`)
- makhmut-coscia-2025-stic-dvp (PRIDE per bioRxiv `2025.03.19.643504`)
- xenium-5k-demo-10x (10x portal)

## tier-1 — synapse (mixed: account-only for processed, DAC for raw)

Free Synapse account gets processed L3/L4 + metadata immediately. Raw L1/L2 sequencing needs the matching DUA per sub-atlas.

- launonen-2022-farkkila-mif-hgsoc (Synapse `syn26230540`) — HMS-LSP processed-open
- farkkila-2020-topacio (Synapse `syn22177117`) — HMS-LSP processed-open
- vazquez-garcia-2022-mskspectrum (Synapse `syn25569736`)
- hms-sorger-ovarian-renamed (Synapse — Sorger lab page; processed CyCIF open)
- risom-2022-dcis-mibi (Synapse `syn17773547` — candidate; verify before pulling)
- **HTAN gateway** `syn20446927` (all sub-atlases below, filter by `Atlas`):
  - htan-hta1-htapp (Atlas=HTA1)
  - htan-hta3-bu-lung-precancer (Atlas=HTA3)
  - htan-hta4-chop-pediatric (Atlas=HTA4)
  - htan-hta5-dfci-resistance (Atlas=HTA5)
  - htan-hta6-duke-stanford-dcis (Atlas=HTA6)
  - htan-hta7-hms-patch-sorger (Atlas=HTA7)
  - htan-hta8-msk-metastasis (Atlas=HTA8)
  - htan-hta9-ohsu-smmart-mbc (Atlas=HTA9)
  - htan-hta10-stanford-fap (Atlas=HTA10)
  - htan-hta11-vanderbilt-crc (Atlas=HTA11)
  - htan-hta12-wustl-pancancer (Atlas=HTA12)

## tier-2 — controlled-access applications (start the paperwork now; expect 2–6 weeks)

Each row needs a DAR / DAC application. Group these by repo and submit in batches.

### dbGaP (NIH eRA-Commons login + DAR)

- pelka-2021-crc raw — `phs002407`
- bi-2021-ccrcc raw — `phs002252`
- hwang-lin-2023-pdac-chemo raw — `phs002371` (HTAN-HTAPP umbrella)
- mitri-2024-amtec-parpi-mtnbc — `phs002371.v1.p1` (same HTAN-HTAPP umbrella)
- htapp-klughammer-2024-mbc — `phs002371` (same umbrella; covers multiple sub-cohorts)
- htan-hta8-sclc-chan-2021 — `phs002371`
- hwang-2022-pdac-neoadj raw — `phs002789`
- mskspectrum-cfdna-parpi-2025 — `phs002857` — **direct PARPi-maintenance HGSOC; high priority**

**Note**: `phs002371` HTAN-HTAPP umbrella covers Mitri AMTEC + Hwang-Lin PDAC + Klughammer mBC + Chan SCLC + others. One DAR.

### EGA (DAC application per study; each has its own DAC)

- bassez-2021-biokey — `EGAS00001004809`
- liu-2022-nsclc — `EGAS00001005003`
- maynard-2020-nsclc-longitudinal — `EGAS00001004422`
- kim-2020-nsclc-mets — `EGAS00001004001`
- stewart-2020-sclc-cdx — `EGAS00001004025`
- erickson-2022-prostate-visium — `EGAS00001006124`
- krishna-2021-adapter-ccrcc-io — `EGAS00001005188`
- ali-danenberg-2020-metabric-imc raw — `EGAS00000000083`
- denisenko-2024-hgsoc-visium-cosmx — `EGAS00001006816`
- owkin-mosaic-window-bladder — `EGAD50000001251` (parent `EGAS50000000689`)

## tier-3 — deferred (do not attempt this round)

Track; don't burn cycles.

- **`accession unverified`** — wait until paper is indexed or preprint resolves to a deposit:
  - wang-2025-sclc-parpi
  - pei-min-2025-pdac-autopsy (Nature 642:212)
  - wu-2025-hgsoc-visium-hd (preprint `10.1101/2025.11.24.690313`)
  - hwang-2025-pdac-neural
- **`accession not located`** — wrong-ID in original blog; needs author contact or paper re-check:
  - magen-2023-hcc
  - sun-2024-hcc-primary-met
- **needs verify** before reliance:
  - risom-2022-dcis-mibi (candidate `syn17773547`)

## priority order for tier-0 + tier-1 in this batch

Process this sequence first — open + HRD-relevant:

1. luo-2024-nant-ovarian (anchor — proves the pipeline end-to-end on the cohort the project is built around)
2. pal-2021-brca1-breast
3. karaayvaz-2018-tnbc
4. kim-2018-tnbc-chemoresist
5. stur-2022-hgsoc-visium
6. launonen-2022-farkkila-mif-hgsoc (Synapse)
7. farkkila-2020-topacio (Synapse)
8. hms-sorger-ovarian-renamed (Synapse)
9. ali-danenberg-2020-metabric-imc
10. makhmut-coscia-2025-stic-dvp

Then expand outward by bucket. HTAN sub-atlases (HTA1, HTA6, HTA9, HTA12) need a separate workflow because the Synapse fileview is large — see `folder_layout.md` for the per-sub-atlas directory pattern.
