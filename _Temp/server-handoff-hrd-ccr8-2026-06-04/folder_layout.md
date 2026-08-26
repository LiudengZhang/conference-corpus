# folder layout spec

```
<DATA_ROOT>/
├── A/                                  # sc/snRNA + genomics
│   └── <cohort_id>/
│       ├── MANIFEST.yaml
│       ├── raw/
│       │   ├── genomic/                # FASTQ / BAM / VCF
│       │   └── tme/
│       │       └── <modality>/         # scrna / snrna / etc.
│       ├── processed/
│       │   ├── genomic/                # SBS / HRDetect / CHORD / scarHRD output
│       │   ├── tme/                    # cellranger out, h5ad, etc.
│       │   └── clinical/               # patient.tsv, sample.tsv, treatment.tsv
│       └── qc/
│           ├── genomic_qc.tsv
│           ├── tme_qc.tsv
│           ├── clinical_completeness.tsv
│           └── qc_card.md              # one-pager: did it pass?
├── B/                                  # spatial transcriptomics + genomics
├── C/                                  # spatial proteomics + genomics
├── D/                                  # multi-spatial / full-tuple
│   └── htan-htaXX-<center>/
│       └── (HTAN sub-atlas layout — see below)
├── _index/
│   ├── cohort_manifest.tsv             # copy of handoff manifest, kept up to date
│   ├── status.tsv                      # per-cohort: requested / downloading / ready / failed / blocked
│   └── access_log.tsv                  # which DAR/DAC submitted, when, ticket #
└── _scratch/                           # transient — never reference from outside
```

## per-cohort `MANIFEST.yaml`

Echoes the row from `cohort_manifest.tsv` plus runtime fields.

```yaml
cohort_id: luo-2024-nant-ovarian
bucket: A
consortium: standalone
cancer: HGSOC
n_patients: 30
genomic_modality: WGS+HRD
tme_modality: scRNA+scTCR
repository: GEO
accession_primary: GSE222556
accession_secondary: null
access_tier: open
hrd_signal: wgs-sbs3
priority: 1
vault_id: luo-2024-nant-ovarian
doi: 10.1016/j.cell.2024.XX.XXX
download:
  started_utc: 2026-06-04T...
  finished_utc: ...
  bytes_total: ...
  checksum_verified: true
qc:
  status: pass | warn | fail
  notes: ...
```

## HTAN sub-atlas layout

The Synapse fileview `syn20446927` is shared across all sub-atlases — they're distinguished by the `Atlas` metadata column. Each sub-atlas gets its own directory under `D/`:

```
D/htan-hta1-htapp/
├── MANIFEST.yaml
├── raw/
│   ├── genomic/
│   │   ├── wes/                        # bulk WES BAMs
│   │   └── panel/
│   └── tme/
│       ├── scrna/
│       ├── snrna/
│       ├── visium/
│       ├── slideseq/
│       ├── merfish/
│       ├── exseq/
│       ├── codex/
│       └── mibi/
├── processed/
│   ├── genomic/                        # SBS3 / HRDetect-equivalent / scarHRD
│   ├── tme/
│   └── clinical/                       # HTAN biospecimen/diagnosis CSVs
└── qc/
```

Use the HTAN CLI (`htan-cli`) to filter the fileview by `Atlas` + assay type. Treat each sub-atlas as a separate cohort for QC purposes — they have different lead PIs, processing pipelines, and metadata conventions.

## status.tsv columns

```
cohort_id  state  last_updated_utc  bytes_downloaded  qc_status  blocker  notes
```

`state` enum: `pending | requested | approved | downloading | downloaded | processing | ready | failed | blocked`

## naming convention

- All paths lowercase, kebab-case.
- One cohort = one row in the manifest = one directory under its bucket.
- HTAN sub-atlases distinguished by `htan-htaXX-<center>` slug, never collapsed.
- Synonyms or alternate IDs (e.g., MOSAIC parent vs. window release) noted in `MANIFEST.yaml` `notes`, not in directory name.

## no-go

- Do not move files between buckets. Bucket assignment is locked from the manifest.
- Do not delete raw/ once downloaded — re-download cost is high for EGA/dbGaP.
- Do not store credentials, tokens, or DUA paperwork inside the data tree. Use a separate `_secrets/` outside `<DATA_ROOT>`.
