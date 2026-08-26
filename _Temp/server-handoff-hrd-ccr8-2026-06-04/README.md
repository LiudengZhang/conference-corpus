# server-handoff — HRD × CCR8 pan-cancer (2026-06-04)

Hand-off package for the remote server-side agent to do download + organize + QC + EDA on the matched multi-omic cohorts inventoried in the matched-multi-omic-tumor-table blog. **No modeling in this phase.**

## what's here

| file | what it is |
| --- | --- |
| `FIRST_PROMPT.md` | **paste this into the agent first.** kickoff brief + priority order + exit condition |
| `cohort_manifest.tsv` | canonical 74-row table (4 buckets A/B/C/D) — the load-bearing artifact |
| `access_tier_split.md` | three-tier access split: open / Synapse-mixed / controlled |
| `folder_layout.md` | directory tree under `<DATA_ROOT>`, per-cohort `MANIFEST.yaml` schema |
| `qc_rubric.md` | per-modality QC checklist + `qc_card.md` template |
| `tools_manifest.md` | version-pinned tool list + conda env pattern |
| `do_not_attempt.md` | sponsor-controlled PARPi pivotals + bulk-only cohorts to skip |

## upstream source

The cohorts come from the matched-multi-omic-tumor-table blog at:

```
examples/blogs/hrd-ccr8-pancancer/matched-multi-omic-tumor-table.md
```

74 cohorts, ~6,200 patients pan-total. Six accession IDs were corrected after a verification round; four 2025 cohorts have `accession unverified` and are deferred. See the blog's `## access status` section for the full audit trail.

## how to share

Zip the folder and hand it over:

```bash
cd /Users/lzhang34/Desktop/AACR/_Temp
zip -r server-handoff-hrd-ccr8-2026-06-04.zip server-handoff-hrd-ccr8-2026-06-04/
```

Or rsync the folder directly to the server.

## phase 1 exit condition

The agent returns:

1. `_index/status.tsv` per cohort
2. `qc/_rollup.md` (per-bucket pass/warn/fail tallies + per-HRD-signal stratification)
3. One actionable paragraph per warn/fail

Then we decide which subset goes into Phase 2 (modeling). Do not start Phase 2 without that decision.
