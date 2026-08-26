# tools manifest

Version-pinned. Install via conda + pip with the lockfile pattern below.

## download clients

| tool | purpose | install |
| --- | --- | --- |
| `synapseclient` ≥ 4.6.0 | Synapse + HTAN | `pip install synapseclient` |
| `synapseutils` | bulk syncFromSynapse | bundled |
| `htan-cli` (Sage Bionetworks) | HTAN fileview queries | `pip install htan-cli` |
| `pyega3` ≥ 5.2.0 | EGA download | `pip install pyega3` |
| `ega-download-client` (alt) | EGA java client | jar from EGA |
| `gdc-client` ≥ 1.6.1 | dbGaP / GDC (TCGA backbone) | binary from NCI GDC |
| `prefetch` + `fasterq-dump` (SRA-toolkit ≥ 3.0.10) | SRA / GEO raw | conda `sra-tools` |
| `aws-cli` ≥ 2.15 | S3 (some HTAN, 10x portal, GDC mirror) | OS package |
| `gsutil` | GCS mirrors | `gcloud` SDK |
| `wget` / `aria2c` | Zenodo / ArrayExpress / PRIDE / GEO supplementary | OS package |
| `curl` | metadata lookups | OS |

## genomic processing

| tool | purpose |
| --- | --- |
| `samtools` ≥ 1.20 | BAM ops |
| `bcftools` ≥ 1.20 | VCF ops |
| `verifyBamID2` ≥ 2.0.1 | contamination |
| `CHARR` | alternate contamination |
| `Sequenza` (R) / `PURPLE` (HMF) / `ASCAT` (R) | tumor purity + CNA |
| `SigProfilerExtractor` + `SigProfilerAssignment` | mutational signatures (SBS3) |
| `HRDetect` (R, Davies et al.) | WGS-based HRD score |
| `CHORD` (R) | random-forest HRD predictor |
| `scarHRD` (R) | LOH + TAI + LST composite |
| `myChoice` equivalents | open re-implementations only (proprietary algorithm) |
| `Mutect2` / `Strelka2` | somatic SNV |
| `Manta` / `GRIDSS` | structural variants |
| `VEP` / `SnpEff` | annotation |

## bulk RNA

| tool | purpose |
| --- | --- |
| `STAR` ≥ 2.7.11 | alignment |
| `Salmon` ≥ 1.10 | pseudo-alignment / quant |
| `RSeQC` | QC |
| `ESTIMATE` (R) | immune + stromal scores |

## single cell

| tool | purpose |
| --- | --- |
| `cellranger` ≥ 8.0 (10x) | scRNA / snRNA / multi |
| `cellranger-arc` | multiome |
| `cellranger-atac` | scATAC |
| `STARsolo` | alternative aligner |
| `scrublet` ≥ 0.2.3 | doublet detection |
| `DoubletFinder` (R) | alternative doublet |
| `scanpy` ≥ 1.10 | analysis |
| `anndata` ≥ 0.10 | I/O |
| `scvi-tools` ≥ 1.1 | integration baselines |
| `CellTypist` ≥ 1.6 | label transfer |
| `souporcell` | snRNA demux |

## spatial

| tool | purpose |
| --- | --- |
| `SpaceRanger` ≥ 3.0 | Visium / Visium HD |
| `Xenium Ranger` ≥ 3.0 (10x) | Xenium |
| `Slide-seq Tools` (Broad) | Slide-seq |
| `STOmics / Stereopy` | Stereo-seq (BGI) |
| `Vizgen post-processing` | MERSCOPE |
| `squidpy` ≥ 1.6 | spatial analysis |
| `cellpose` ≥ 3.0 / `Mesmer` / `deepcell` | nuclear / cell segmentation |
| `qupath` | imaging QC + annotation |

## spatial proteomic / IMC / MIBI / CODEX

| tool | purpose |
| --- | --- |
| `steinbock` (Bodenmiller) | IMC pipeline |
| `imcsegpipe` | alt IMC pipeline |
| `ark-analysis` (Angelo lab) | MIBI |
| `CODEX` SciSeq pipeline | CODEX |
| `MCMICRO` (Sorger lab) | t-CyCIF / mIF — used heavily by HTAN HTA1, HTA5, HTA7, Färkkilä cohorts |

## conda env pattern

```bash
# one env per modality family — keeps tool versions clean
mamba create -n hrd-genomic -c bioconda -c conda-forge \
    samtools bcftools verifybamid2 sequenza-utils \
    star=2.7.11 salmon=1.10 sra-tools=3.0.10 mutect2 manta

mamba create -n hrd-sc -c bioconda -c conda-forge \
    cellranger scanpy anndata scvi-tools scrublet celltypist souporcell

mamba create -n hrd-spatial -c bioconda -c conda-forge \
    spaceranger squidpy cellpose=3 mesmer steinbock

mamba create -n hrd-mibi-cycif -c bioconda -c conda-forge \
    mcmicro ark-analysis qupath

mamba create -n hrd-download -c bioconda -c conda-forge \
    synapseclient pyega3 gdc-client awscli gsutil aria2

pip install htan-cli HRDetect CHORD SigProfilerExtractor SigProfilerAssignment
```

Lock with `mamba env export --no-builds > env-<name>.yaml` after creation. Commit the lockfiles to whichever repo the agent's pipeline lives in.

## reference data

| ref | purpose | source |
| --- | --- | --- |
| GRCh38 / GRCh38.p14 | alignment | NCBI |
| GENCODE v44+ | annotation | GENCODE |
| 1000 Genomes phase 3 sites | contamination + ancestry | 1000G |
| COSMIC v99+ | known cancer mutations | Sanger (license required for commercial) |
| TCGA-PANCAN PCAWG MAF | reference HRD scores for calibration | NCI GDC |
| HRDetect / CHORD training-set reference | model weights | distributed with tool |
