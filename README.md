# Conference Corpus — Multi-Conference Transcripts & Abstracts

Curated content from biomedical and computational biology meetings, served as one searchable MkDocs Material site (private, Cloudflare Pages + Basic Auth) with one nav tab per conference.

## Conferences

| Conference | Status | Sessions | Posters |
|---|---|---|---|
| **AACR 2026** | Live | ~26 unique transcripts | 2,298 (1,953 unique by Id) |
| **Nextflow Summit 2026** | Live | 3 transcripts (~370 KB) | — |
| **JPM 2026** | Placeholder | — | — |

## Layout

```
conference-corpus/
├── aacr-2026/                    # AACR 2026 raw data (transcripts/, raw/)
│   ├── transcripts/{agentic-ai,single-cell-spatial-omics,virtual-cells,bioinfo-tools,clinical-trials}/
│   └── raw/{...}/
├── nextflow-2026/                # Nextflow Summit raw data
│   └── transcripts/sessions/     # 3 .md files
├── jpm-2026/                     # JPM 2026 placeholder
├── docs/                         # MkDocs source
│   ├── index.md                  # 3-conference home
│   ├── conferences/{aacr-2026,nextflow-2026,jpm-2026}/
│   ├── notes/                    # extraction & caveats (shared)
│   ├── assets/{aacr-2026}/posters/{topic}.json   # generated
│   ├── javascripts/, stylesheets/                # shared
│   └── superpowers/specs, superpowers/plans      # design docs
├── scripts/
│   ├── build_site.py             # Preprocessor: poster JSON, session pages, dossier matrix
│   └── conferences.py            # Conference registry (single source of truth)
├── functions/_middleware.js      # Cloudflare Pages Basic Auth
├── mkdocs.yml                    # navigation.tabs — one tab per conference
└── requirements.txt
```

## Build

```bash
pip install -r requirements.txt
python scripts/build_site.py        # generate poster JSON, session pages, tool dossiers
mkdocs build                        # render the static site
```

`python scripts/build_site.py --survey` prints the bioinfo-tools mention table without writing files.

## AACR 2026 — topic breakdown

| Topic | Sessions | Words | Posters | Poster words |
|---|---|---|---|---|
| Agentic AI | 5 full + 3 AT02 slices | ~67,000 | 57 | ~19,000 |
| Single-cell & spatial omics | 20 full (1 shared) | ~273,000 | 1,015 | ~328,000 |
| Virtual cells | 1 native + 5 symlinks | ~80,500 | 48 | ~16,000 |
| Bioinfo / comp bio / AI methods | 12 symlinks (all borrowed) | ~162,000 | 536 | ~170,000 |
| Clinical trials | Deferred | — | 642 | ~230,000 |
| **Totals** | ~26 unique sessions | ~464,000 | 2,298 (1,953 unique by Id) | ~763,000 |

The bioinfo-tools sub-section includes a [tools matrix](https://github.com/LiudengZhang/conference-corpus/tree/main/docs/conferences/aacr-2026/topics/bioinfo-tools/tools) of foundation models and methods that cleared a 3-mention inclusion gate against the corpus (CHIEF, UNI/UNI2, Prov-GigaPath, Geneformer, scGPT, Cell2Location).

## Nextflow Summit 2026

Three sessions (Day 1 AM/PM, Day 2) captured from Goldcast event `ff174b87-316f-47c7-8c7b-a51028b670b7`. Captions are auto-generated; "Vicksville" recurs as a captioner mishearing of "Nextflow."

## JPM 2026

Placeholder folder; content to be added.

## Caveats

- All session captions are auto-generated English from the live stream. Expect misheard names and acronyms ("Foersch" → "Firsch", "Bunne" → "Bonner", "scGPT" → "SC-GPT", "Nextflow" → "Vicksville").
- Sub-talks inside a parent AACR session share the parent's video. Time-slice the parent VTT to extract one sub-talk (see the AT02 per-speaker slices as a worked example).
- VTT signatures in raw Vimeo configs expire after ~6 hours; re-extracting a session means re-navigating the live page.
- Clinical-trials session transcripts are deferred — the AACR poster corpus (~294K words) is the primary artifact for that topic.

See `docs/conferences/aacr-2026/topics/<topic>/README.md` for per-topic extraction methods, keyword unions, and overlap stats.
