# Patch + status prompt (paste after FIRST_PROMPT.md)

Quick update before you dispatch Wave A. The manifest had three accession
mismatches that would have pulled the wrong cohort. **Re-pull
`cohort_manifest.tsv` from the handoff folder** — these rows changed:

- `couturier-2020-gbm` — was `GEO GSE163108` (wrong: that's Mathewson 2021).
  Now `EGA EGAS00001004422`, controlled access. Add to your EGA DAR batch.
- `sun-2021-hcc-early-relapse` — was `GEO GSE149614` (wrong: that's Lu Y 2021).
  Accession unresolved — **demote to priority 4, do not download**.
- `hwang-lin-2022-pdac-chemo` (renamed from `-2023-`) — was `GEO GSE205013`
  (wrong: that's Simeone). Now `GEO GSE199102` + `dbGaP phs002371`. Hwang 2022 Nat Genet.

If your Wave-A or Wave-B subagents already started on any of these three with the
old accession, **kill those subagents and re-dispatch** against the corrected rows.

Two asks back to me, in your 5-line returns:

1. After Luo anchor QC finishes, surface the verdict **immediately** — don't wait for Wave A.
2. For every cohort, log the actual accession you downloaded from in
   `MANIFEST.yaml.download.source_url` so I can catch any further drift.

Otherwise keep going. Status update from you every ~6h.
