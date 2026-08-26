# do-not-attempt list

Save the agent dead-end work. Each row here looks reachable but isn't; cite in positioning, do not chase the data.

## sponsor-controlled PARPi pivotal trials

Raw multi-omic data is contractually sponsor-held; no academic DUA path. We cite trial design + published summary stats only.

| trial | sponsor | drug | tumor | reason |
| --- | --- | --- | --- | --- |
| SOLO-1 | AstraZeneca | olaparib 1L maint. | HGSOC BRCAm | sponsor-controlled |
| SOLO-2 | AZ | olaparib 2L | HGSOC BRCAm | sponsor-controlled |
| PRIMA | GSK / Tesaro | niraparib 1L maint. | HGSOC all | sponsor-controlled |
| NOVA | GSK / Tesaro | niraparib 2L | HGSOC | sponsor-controlled |
| OlympiA | AZ / Merck | olaparib adjuvant | HER2- breast BRCAm | sponsor-controlled |
| OlympiAD | AZ | olaparib mBC | gBRCAm mBC | sponsor-controlled |
| VELIA / GOG-3005 | AbbVie | veliparib 1L | HGSOC | sponsor-controlled |
| DUO-O | AZ | durva + olaparib + bev | HGSOC | sponsor-controlled |
| ATHENA-MONO | Clovis | rucaparib 1L maint. | HGSOC | sponsor-controlled + Clovis defunct |
| ATHENA-COMBO | Clovis | rucaparib + nivolumab | HGSOC | same |
| TRITON2/3 | Clovis | rucaparib | mCRPC HRR-mut | same |
| PROfound | AZ | olaparib | mCRPC HRR-mut | sponsor-controlled |
| MAGNITUDE | J&J | niraparib + abi | mCRPC HRR-mut | sponsor-controlled |
| PROpel | AZ | olaparib + abi | mCRPC all | sponsor-controlled |
| EMBRACA | Pfizer | talazoparib | gBRCAm mBC | sponsor-controlled |
| TALAPRO-2 | Pfizer | talazo + enza | mCRPC all | sponsor-controlled |

Use these for positioning in [[outcome-first]] and methods narrative — never as data sources.

## commercial / proprietary platforms

Public-facing claims, no accessible patient-level data.

- **Tempus xT / xR / xH** — proprietary 648-gene panel + RNA + WGS heme; aggregate stats only
- **Caris POA** — proprietary DNA + WTS + 23k-protein; aggregate stats only
- **Foundation Medicine FoundationOne CDx + Liquid** — clinical reports only
- **BostonGene MFP product line** — model + 29-gene ssGSEA signature published (Bagaev 2021 — citable), proprietary patient-level data is not
- **Owkin MOTRY / RlearnCT** — product names; no peer-reviewed paper, no accession; treat as company claim only
- **Owkin GMI** — same; aspirational
- **Tahoe-100M / Tahoe-Bio** — perturbation atlas, different problem shape; not in scope here even though it's public

## non-tumor / wrong-shape data

Don't waste the slot.

- **HCA Pan-Tissue Tumor sub-cohorts** — only the tumor-only subsets count, and most are duplicates of cohorts already in the manifest (HTA1 HTAPP etc.). Confirm dedupe before adding.
- **scRNA atlases without matched tumor genomics** (much of CellxGene Census tumor entries) — TME side present, genomic side absent → fails the entry condition.
- **TCGA scRNA pilots** — single-sample demos, not cohort-scale.
- **Pan-Immune Working Group (Thorsson 2018) raw** — already in TCGA backbone; bulk-only; cite in methods only.

## bulk-only "near misses"

These have HRD signal but no matching sc / spatial — they belong in `paired-data-pan-cancer.md` Tier 1 backbone, **not** in this matched-multi-omic table:

- TCGA-PANCAN (33 cancers, ~10k)
- HMF / Priestley 2019 (~5k metastatic WGS+RNA)
- POG570 / Pleasance 2020 (~570 treated WGS+RNA)
- MSK-CHORD / Cheng et al. (clinical panel + outcomes; no sc/spatial)
- MET500 / Robinson 2017 (~500 metastatic WES+RNA)
- Genomics England 100k Cancer / Sosinsky 2024 (~13.9k WGS, NHS)
- DKTK MASTER / Horak 2021 (~1.3k WGS+RNA)
- SU2C-PCF mCRPC / Abida 2019 (~400 WES+RNA)
- PCAWG / ICGC 2020 pan-cancer WGS

The agent processes these only if explicitly asked. They are the **cross-link backbone**, not primary rows.

## paperwork-blocked but worth tracking

These will become accessible later — don't burn cycles now, but keep them on the radar:

- HTAN Phase 2 atlases (HTA200–HTA209) — funded Sep 2024, no public data as of June 2026; HTA201 (OHSU PDAC BRCA carriers) and HTA208 (MDACC HGSOC MOSAIC-Ov3D) are the two HRD-relevant ones
- ASTRA consortium (Garvan + U-Tokyo + 10x, Nov 2025) — Asia-Pacific Xenium pan-cancer; pilot only currently
- MOSAIC pan-cancer release beyond MIBC-15 — Owkin published a 60-patient window, then narrowed the public release; future tumor types will land on EGA over 2026–2027

Re-audit Q4 2026.
