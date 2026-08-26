# QC rubric per modality

One short checklist per file type. The agent runs these on every cohort and writes a one-pager `qc_card.md` per cohort summarising pass / warn / fail.

The point of this stage is not to model — it is to find out **which cohorts are usable** before we commit to any downstream analysis.

## WGS / WES / panel-DNA

1. **Coverage** — mean coverage histogram per sample; WGS ≥ 30× target / ≥ 60× tumor common; WES ≥ 100× target. Flag any sample below threshold.
2. **Contamination** — `verifyBamID2` or `CHARR`; flag samples with `FREEMIX > 0.03`.
3. **Tumor purity** — `Sequenza` / `ASCAT` / `PURPLE` purity estimate. Flag `purity < 0.20` as low-confidence for HRD calls.
4. **Ploidy + CNA** — same caller; report ploidy + segment count.
5. **HRD signal** — run these in order; the first that succeeds wins:
   - WGS → SigProfiler SBS3 + HRDetect + CHORD + scarHRD; report 4-scorer concordance vector
   - WES → CHORD + scarHRD (HRDetect needs WGS — skip); report 2-scorer vector
   - panel → BRCA1/2 + HR-pathway gene status + LOH-at-locus
6. **HR-gene mutation status** — BRCA1, BRCA2, PALB2, RAD51C/D, ATM, BARD1, CHEK2, BRIP1. Note germline vs somatic if both layers exist.
7. **Sample swaps** — fingerprint check vs paired RNA / sc data using common SNP panel.

## bulk RNA-seq

1. **Read counts + alignment rate** — `STAR` / `Salmon` log; flag samples below 20M aligned reads.
2. **rRNA %** — flag > 30%.
3. **Library complexity** — flag duplicate rate > 70%.
4. **Sex check** — XIST + Y-chr gene expression vs reported sex.
5. **Tumor-purity estimate** — `ESTIMATE` immune + stromal scores; cross-check with DNA-based purity.
6. **Gene-expression cohort drift** — PCA on top-2k variable genes; flag obvious batch/lab clusters.

## scRNA / snRNA

1. **Counts per cell** — distribution; flag if median < 1,000 UMI (snRNA) or < 2,000 UMI (scRNA).
2. **Genes per cell** — distribution; flag if median < 500.
3. **% mito** — distribution; flag samples with median > 20% (scRNA) or > 5% (snRNA, single nuclei have less).
4. **Doublet flag** — `scrublet` or `DoubletFinder`; expected ~5–8% doublet rate.
5. **Broad-lineage cluster sanity** — quick Leiden + label transfer onto a reference (CellTypist Encyclopedia, Tabula Sapiens, or HCA pan-tissue). Confirm three broad classes are detectable: epithelial, immune, stromal. If not, flag.
6. **Per-sample cell yield** — table of cells passing QC per sample; flag samples below 500 post-QC cells.

## Visium / Visium HD / Xenium / Stereo-seq / Slide-seq / MERFISH

1. **Spot / cell count per section** — Visium expect 1k–5k spots / section; Xenium 50k–500k cells / section; flag low.
2. **UMI / counts per spot or cell** — distribution; flag medians below modality norm.
3. **Genes detected per spot or cell** — distribution.
4. **H&E registration** — visual check; flag misregistration > 100 μm.
5. **Tissue fraction** — proportion of spots under tissue vs background.
6. **Pathologist annotation availability** — confirm tumor / stroma / invasive-front masks exist if claimed in paper.

## CODEX / MIBI / IMC / mIF / t-CyCIF

1. **Marker intensity distribution** — per-channel histogram; flag dead channels.
2. **Background / autofluorescence** — flag if dynamic range < 2× background.
3. **Cell segmentation success** — `mesmer` / `cellpose` / `deepcell`; flag if segmented cells per ROI < 1k or > 100k (too few = bad seg; too many = oversegmentation).
4. **Marker positivity rates** — sanity check against panel design (CD45 positivity 20–50%, CK positivity 10–60%, etc.).
5. **Batch drift** — UMAP / PCA on cell-level marker means by batch / slide; flag obvious slide-clustering.

## clinical metadata

For every cohort, build `clinical_completeness.tsv` per patient:

| field | required | present | notes |
| --- | --- | --- | --- |
| `patient_id` | yes | y/n | |
| `cancer_type` | yes | y/n | |
| `stage` | preferred | y/n | |
| `histology` | preferred | y/n | |
| `hrd_status` | preferred | y/n | source: clinical assay / inferred / unknown |
| `brca12_status` | preferred | y/n | germline / somatic / both / unknown |
| `treatment_lines` | preferred | y/n | platinum exposure, PARPi exposure, IO exposure |
| `os_months` | preferred | y/n | |
| `pfs_months` | preferred | y/n | |
| `response` | preferred | y/n | RECIST / pCR / MPR / clinical |
| `sample_timepoint` | yes | y/n | pre / on / post / met / residual / progression |

Flag cohort as low-clinical-yield if < 50% of patients have `treatment_lines` + `os_months`.

## qc_card.md template (per cohort)

```markdown
# QC card — <cohort_id>

- bucket: A | B | C | D
- n_patients_expected: <from manifest>
- n_patients_post_qc: <count>
- access tier: open | controlled | synapse-mixed
- download status: complete | partial | failed
- overall: pass | warn | fail

## genomic
- coverage: pass | warn | fail (n samples failing)
- contamination: pass | warn | fail
- purity median: 0.XX
- HRD signal: SBS3 / HRDetect / CHORD output present (Y/N), concordance vector summary

## tme
- modality: scRNA | snRNA | Visium | ...
- post-QC cells / spots: N
- broad-lineage sanity: pass | warn | fail

## clinical
- treatment annotation: pass | warn | fail
- HRD / BRCA12 status: pass | warn | fail
- outcomes present: OS / PFS / response y/n

## blockers
- ...

## verdict
- usable for HRD axis: yes | partial | no
- usable for TME axis: yes | partial | no
- usable for treatment response: yes | partial | no
```

## pan-cohort rollup at end of phase

After all P1 + P2 cohorts pass through QC, write `qc/_rollup.md`:

- per-bucket count of cohorts at pass / warn / fail
- total post-QC patient count by bucket
- per-HRD-signal stratum: how many patients with SBS3-callable WGS, how many WES-only, how many panel-only
- which cohorts cleared the bar for treatment-causal modeling (have HRD + OS/PFS + treatment lines)
- which cohorts are TME-only (good for archetype routing but not response)
