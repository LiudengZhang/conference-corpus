# AACR Annual Meeting 2026 — Session Transcripts & Poster Abstracts

Curated topic-specific subsets of AACR 2026 content. Session transcripts are Vimeo auto-generated English captions from `connect.aacr26.org`; poster abstracts are structured extracts from `www.abstractsonline.com` (frontend at `cattendee.abstractsonline.com`).

## Interactive site

An MkDocs Material site is generated from this repo and deployed on Cloudflare Pages (private, Basic Auth). It renders the corpus as filterable poster tables (Tabulator) + one page per unique session transcript, plus topic-level analysis pages (Overview / Landscape / Synthesis) — starting with Virtual Cells (ED03 theses vs 48-poster corpus) — and a dedicated **Tools** sub-section under bioinfo-tools with reference dossiers for the named foundation models / methods that cleared a 3-mention inclusion gate against the corpus (CHIEF, UNI/UNI2, Prov-GigaPath, Geneformer, scGPT, Cell2Location). Hypothes.is annotation layer enabled site-wide.

- Source: `docs/` (MkDocs), `scripts/build_site.py` (preprocessor), `functions/_middleware.js` (Basic Auth)
- Build: `pip install -r requirements.txt && python scripts/build_site.py && mkdocs build`

## Layout

```
AACR/
├── transcripts/
│   ├── agentic-ai/                  ← 5 full parent sessions + 3 AT02 per-speaker slices
│   │   ├── full-sessions/                + 57 posters
│   │   ├── at02-per-speaker/
│   │   ├── posters/
│   │   └── README.md
│   ├── single-cell-spatial-omics/   ← 20 full parent sessions (19 unique + 1 symlinked overlap)
│   │   ├── full-sessions/                + 1,015 posters
│   │   ├── posters/
│   │   └── README.md
│   ├── virtual-cells/               ← 1 native + 5 symlinked sessions + 48 posters
│   │   ├── full-sessions/
│   │   ├── posters/
│   │   └── README.md
│   ├── bioinfo-tools/               ← 12 symlinked sessions (methods-heavy) + 536 posters
│   │   ├── full-sessions/                (all symlinks — no native extractions)
│   │   ├── posters/
│   │   └── README.md
│   └── clinical-trials/             ← Posters-only (642 posters, ~294K words)
│       ├── full-sessions/                (empty — see README)
│       ├── posters/
│       └── README.md
└── raw/
    ├── agentic-ai/                  ← 5 Vimeo player-config JSONs
    ├── single-cell-spatial-omics/   ← 19 Vimeo player-config JSONs
    ├── virtual-cells/               ← 1 Vimeo player-config JSON (native extract)
    ├── bioinfo-tools/               ← empty (all sessions symlinked)
    └── clinical-trials/             ← empty (session extraction deferred)
```

## Topics covered

| Topic | Sessions | Words | Posters | Poster words |
|---|---|---|---|---|
| Agentic AI | 5 full + 3 AT02 slices | ~67,000 | 57 | ~19,000 |
| Single-cell & spatial omics | 20 full (1 shared) | ~273,000 | 1,015 | ~328,000 |
| Virtual cells | 1 native + 5 symlinks | ~80,500 | 48 | ~16,000 |
| Bioinfo / comp bio / AI methods | 12 symlinks (all borrowed) | ~162,000 | 536 | ~170,000 |
| Clinical trials | Deferred | — | 642 | ~230,000 |
| **Totals** | ~26 unique sessions | ~464,000 | 2,298 (1,953 unique by Id) | ~763,000 |

(Session word totals are sums of the underlying unique transcripts; symlinked sessions are not double-counted at the topic level.)

## Session overlaps (symlinks, same Vimeo video)

- `2026-04-20-pm-ai-spatial-transcriptomics-pathology` — primary in `agentic-ai/`, symlinked into `single-cell-spatial-omics/` and `bioinfo-tools/`
- `2026-04-20-am-ai-revolution-in-cancer-research`, `2026-04-18-ai-in-biomarker-discovery-and-drug-development`, `2026-04-21-at02-agentic-ai-cancer-researcher` — primary in `agentic-ai/`, symlinked into `virtual-cells/` and `bioinfo-tools/`
- `2026-04-18-pm-3d-tissue-imaging-and-cancer`, `2026-04-21-pm-dissecting-hematologic-malignancies-single-cell-spatial` — primary in `single-cell-spatial-omics/`, symlinked into `virtual-cells/` and `bioinfo-tools/`
- `2026-04-17-pm-foundation-models-multimodal-ai-cancer-research` — primary in `virtual-cells/`, symlinked into `bioinfo-tools/`
- `2026-04-22-agentic-ai-as-the-oncologist`, `2026-04-20-am-decoding-cancer-ecosystem-pathology-tme-heterogeneity`, `2026-04-21-pm-late-spatial-biomarkers-single-cell-resolution`, `2026-04-19-spatial-and-single-cell-omics-at-scale`, `2026-04-18-mapping-neural-immune-circuits-spatial-multi-omics` — primary in their respective source topics, symlinked into `bioinfo-tools/`

Edit once, read everywhere. `ls -L` to dereference.

## Poster overlaps (duplicated `.txt` files, same `Id`)

Posters are harvested independently per topic and duplicated on disk rather than symlinked — each topic folder is self-contained for `rg`. Unique-to-topic counts:

| Topic | Total posters | Unique to topic |
|---|---|---|
| agentic-ai | 57 | 10 |
| single-cell-spatial-omics | 1,015 | 784 |
| virtual-cells | 48 | 3 |
| bioinfo-tools | 536 | 308 |
| clinical-trials | 642 | 544 |
| **Total posters across topics (sum)** | 2,298 | 1,953 unique by Id |

Note the low virtual-cells unique count (3): 45 of the 48 VC posters also surface under bioinfo-tools or agentic-ai, because the FM / agent / multimodal keywords overlap heavily. Duplication cost is ~4 KB × ~345 cross-topic duplicates ≈ 1.4 MB — trivial.

## Caveats

- All session captions are Vimeo AI-generated English — expect misheard names ("Foersch" → "Firsch", "Bunne" → "Bonner") and acronyms ("scGPT" → "SC-GPT", "AACR" → "ACR"). Find/replace before publishing or quoting.
- Sub-talks inside a parent session share the parent's video. To extract one sub-talk, time-slice the parent VTT (see the AT02 per-speaker slices as a worked example).
- VTT signatures in raw Vimeo configs expire after ~6 hours; re-extracting a session means re-navigating the live session page, not re-using the saved JSON.
- Clinical-trials session transcripts are **deferred** — the poster corpus (294k words) is the primary artifact for that topic. See `transcripts/clinical-trials/README.md` for the list of 25 CT session IDs extractable on demand.

## Extraction method

### Sessions (Swapcard + Vimeo)
1. Log into `connect.aacr26.org` (Fastly CAPTCHA requires manual solve).
2. Search the Sessions listing for topic terms.
3. Navigate to each parent session page; the Vimeo iframe triggers a config fetch at `player.vimeo.com/video/<id>/config?...transcript=1`.
4. Read `request.text_tracks[0].url` — a signed `captions.vimeo.com` URL.
5. `curl` with `-H 'Referer: https://vimeo.com/'` to download the `.vtt`.
6. Strip cue numbers and timestamps for the `.txt`.

### Posters (abstractsonline API)

Two patterns:

- **Keyword-union** (agentic-ai, virtual-cells, clinical-trials, single-cell-spatial-omics): `POST https://www.abstractsonline.com/oe3/Program/21436/Search/new/presentation` with phrase-quoted queries and `Accept: application/json` header; poll `Search/<sid>/Results` until `Status=Complete`; union unique `Id` values; fetch `/Presentation/<Id>` for details; filter `Activity ∈ {Abstract Submission, Late Breaking and Clinical Trials}` + `PlayerUrl present`. Best for narrow topics.
- **Session endpoint** (bioinfo-tools): `GET /Session/<sid>/Presentations` for known methods-oriented sessions. Returns all presentations in the session directly — complete session coverage, no false positives. Best for broad methods topics.

HTML-decode via `DOMParser`, strip tags, emit JSONL. If Chrome download flow is blocked, POST the JSONL to `httpbin.org/anything` and capture the echoed response via MCP's `get_network_request --responseFilePath`; extract the `.data` field with `jq`.

Per-topic READMEs document the specific keyword unions, session IDs, and overlap stats used.
