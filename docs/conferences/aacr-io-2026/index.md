# AACR IO 2026

**AACR Immuno-Oncology Conference** — JW Marriott Los Angeles L.A. Live, Los Angeles, CA · **February 18–21, 2026**.
Theme: *Discovery and Innovation in Cancer Immunology: Revolutionizing Treatment through Immunotherapy*.

> **Status: ✅ built from the abstract supplement and archived program.** All **245 published abstracts** were harvested with full text via Crossref. The program pages themselves are gone from the live AACR site (see below), so day-by-day content comes from Wayback snapshots.

- **Edition:** the **second** annual AACR IO. The inaugural edition was AACR IO **2025** (Feb 23–26, 2025, same venue, 600+ attendees).
- **Co-chairs:** **Nina Bhardwaj** (Icahn School of Medicine at Mount Sinai) and **Antoni Ribas** (UCLA Jonsson Comprehensive Cancer Center) — both MD, PhD, FAACR, and both former AACR Presidents
- **Scale:** "more than 600 registrants and 250 submitted abstracts" per AACR; **245 abstracts were actually published**
- **Format:** **in-person only**, with lecture sessions on demand 7–14 days after the conference
- **Hashtag:** #AACRIO26
- **Next edition:** AACR IO 2027, Feb 28 – Mar 3, 2027, same venue; **Elizabeth Jaffee joins Bhardwaj and Ribas as a chair**

!!! danger "The AACR IO 2026 program pages are dead — archive-only"
    `https://www.aacr.org/meeting/aacr-io-2026/` and every sub-page now return **HTTP 404**; AACR retired them after the meeting. The [program](program.md) and [keynotes](keynotes.md) pages here are reconstructed from Wayback Machine snapshots, which are the only citable source. Snapshot URLs are recorded on each page. Note that the Wed/Thu/Fri snapshots predate the meeting (Jan 13–20, 2026) and still contain "to be announced" placeholders; the Saturday snapshot (Feb 8) is the most complete. **A final as-delivered program was never archived and is not recoverable.**

## Why this is in the vault

**This is the densest immuno-oncology corpus available to us before SITC in November, and unlike SITC it is already complete and open.** 245 abstracts with full text, 100% with author lists, mean length ~3,459 characters — the entire scientific content of the meeting, retrievable through a public API with no scraping and no authentication.

It also fills a specific hole. The corpus tracks IO through [`sitc-2026/`](../sitc-2026/index.md) (a scaffold for a meeting six months out), the [SITC Computational IO webinar series](../sitc-computational-io-2026/index.md) (methods, recordings gated), and the clinical-trials topic at [AACR 2026](../aacr-2026/topics/clinical-trials/index.md). AACR IO 2026 is the one IO meeting in the collection with delivered abstracts, named speakers, and real readouts in hand.

Two things at this meeting are genuinely unusual and worth the vault on their own:

1. **A full symposium on neuro-psych-immunology** (MS8) — serotonin, antidepressants, and GABA as modulators of tumor immunity. That is not standard programming at a major IO meeting.
2. **A Nobel laureate's closing keynote about autoimmunity, not cancer** — Fred Ramsdell (2025 Nobel, Physiology or Medicine) presenting CAR-Treg data in rheumatoid arthritis. See [Keynotes](keynotes.md#fred-ramsdell).

## Corrections to two things you may believe

Both were assumptions we carried into this build, and both are wrong:

- **It is not the inaugural edition.** AACR's own blog calls it "the second annual AACR Immuno-Oncology Conference," and the meeting overview page refers to "the inaugural AACR IO 2025 program."
- **It is not Swapcard-backed, and the `aacr-video-transcripts` scraping approach will not work on it.** There is no `connect.aacr26.org`-style virtual platform — that domain pattern belongs to the **AACR Annual Meeting**, a different event (Apr 17–22, 2026). AACR IO's digital layer was the **EventPilot**-based AACR IO Conference App (Android package `com.eventpilot.aacrshell`), with offline abstract access.

## The abstract supplement — how to harvest it

- **Journal:** *Cancer Immunology Research*, **Volume 14, Issue 2_Supplement** — [issue page](https://aacrjournals.org/cancerimmunolres/issue/14/2_Supplement)
- **DOI pattern:** `10.1158/2326-6074.io2026-<id>` (lowercase), e.g. `10.1158/2326-6074.io2026-lb-a010`
- **Electronic ISSN:** 2326-6074 — query this one
- **Prior year for cross-linking:** AACR IO 2025 = *Cancer Immunology Research* Vol 13, Issue 2_Supplement

**`aacrjournals.org` is Cloudflare-blocked** (HTTP 403, JS challenge) to both WebFetch and curl. **Use Crossref instead** — it carries the complete content:

```
https://api.crossref.org/journals/2326-6074/works
  ?filter=from-pub-date:2026-01-01,until-pub-date:2026-12-31
  &rows=200&cursor=*
  &select=DOI,title,abstract,author,page
```

Filter results to DOIs containing `io2026`. Verified composition:

| | Count |
|---|---|
| Total published abstracts | **245** |
| With full JATS abstract text | 245 / 245 (100%) |
| With complete author lists | 245 / 245 (100%) |
| Poster block A | 79 (incl. 13 LB-A) |
| Poster block B | 86 (incl. 13 LB-B) |
| Poster block C | 76 (incl. 12 LB-C) |
| Invited abstracts (IA01–IA04) | 4 |
| Late-breaking (LB-\*) | 35 |
| Published 2026-02-18 (regular) | 210 |
| Published 2026-03-18 (late-breaking) | 35 |

!!! warning "Free to read, but not formally open access"
    AACR describes the regular abstracts as published "as a freely available supplement," but **Unpaywall has no OA record** for these DOIs — AACR does not deposit OA license metadata for abstracts. Treat them as free-to-read without a registered license, and do not assume redistribution rights.

    Also note: **late-breaking and clinical-trial abstracts were distributed through the conference app only** at meeting time, not in the supplement. Their DOIs did appear in *Cancer Immunology Research* on 2026-03-18, so they are retrievable via Crossref now regardless.

## Vault contents

- [Program](program.md) — day by day, all sessions and chairs
- [Keynotes](keynotes.md) — all seven, with titles where published
- [Themes](themes.md) — 15 themes with abstract counts from a full census of the 245
- [Notable readouts](readouts.md) — OBX-115, obrixtamig, CART19/20, NIBIT-ML1, and the chronotherapy null result

## What we have to work with

| Source | Coverage | Notes |
|---|---|---|
| **Crossref API** | all 245 abstracts, full text | The primary harvest route. No auth, no scraping |
| **CIR supplement** | same content, human-readable | [Vol 14, Issue 2_Supplement](https://aacrjournals.org/cancerimmunolres/issue/14/2_Supplement) — Cloudflare-blocked to automation |
| **Wayback program pages** | sessions, chairs, speakers | Live pages are 404; snapshot URLs on the [program page](program.md) |
| **AACR blog** | 3 recap posts | Live and fetchable — the only prose narrative of the meeting |
| **Media advisory** | format, on-demand policy | [aacr.org](https://www.aacr.org/about-the-aacr/newsroom/media-advisories/register-today-aacr-immuno-oncology-conference-february-18-21-2026/) |
| **Company materials** | one full poster PDF | Obsidian's OBX-115 poster — see [readouts](readouts.md) |
| **On-demand recordings** | lecture sessions | myAACR-gated; **current availability unverified** |
| **BioWorld feed** | trade-press index | [keyword feed](https://www.bioworld.com/keywords/65495-aacr-io-2026) — paywalled, contents unverified |

**No AACR press-program news release exists** for AACR IO 2026 — only three blog posts and one pre-meeting media advisory. That is a smaller press footprint than the corpus's other AACR vaults, and worth knowing before going looking for one.

## Known gaps

- **Two keynote titles were never published** — Rafi Ahmed's and Alexander Marson's.
- **Fred Ramsdell's title is likely truncated** on AACR's page, reading literally as "The bomb to a therapy."
- **Most short-talk speakers are unrecoverable.** The Wed/Thu/Fri snapshots predate speaker assignment; only the two Saturday short talks are named.
- **"Special sessions" appear in AACR's format boilerplate but in no archived 2026 program** — possibly not held.
- **AACR has published no rationale** for launching AACR IO relative to its own Annual Meeting or to SITC. The closest thing is a blog line that "one-third of AACR membership identifies as cancer immunology researchers." The plausible reading — that AACR IO promoted the former Special Conference on Tumor Immunology and Immunotherapy to flagship status — is **unconfirmed** and should not be asserted.
- **On-demand recording availability as of today is unverified**; the conference-resources page is 404 live and would not load from Wayback.

## What to harvest next

1. **Ingest the 245 abstracts.** This is the main event and it is a solved problem — one Crossref query. It would make this the second-largest abstract corpus in the collection after AACR 2026's poster set.
2. **Archive the Wayback program snapshots locally.** They are the only record of the program and there is no guarantee of their persistence.
3. **Cross-link NIBIT-ML1** to its re-presentation at the AACR Annual Meeting 2026 as abstract CT236 (*Cancer Res* vol 86, 8_Supplement) — a rare case where the corpus can track one study across two meetings.

## Sources

- AACR blog recaps: [Feb 20](https://www.aacr.org/blog/2026/02/20/aacr-io-2026-keynote-highlights-cancer-vaccines-are-here-and-upgrading-t-cells-to-thrive-in-the-tumor-microenvironment/) · [Feb 26](https://www.aacr.org/blog/2026/02/26/aacr-io-2026-keynote-highlights-the-tale-of-tregs-told-by-nobel-laureate-fred-ramsdell/) · [Mar 6](https://www.aacr.org/blog/2026/03/06/highlights-from-aacr-io-2026-breaching-the-tumor-microenvironment-fortress-with-new-car-t-and-chimeras/)
- Meeting overview (archived): <https://web.archive.org/web/20260220134901id_/https://www.aacr.org/meeting/aacr-io-2026/>
- Abstract supplement: <https://aacrjournals.org/cancerimmunolres/issue/14/2_Supplement>
- AACR IO 2027: <https://www.aacr.org/meeting/aacr-io-2027/>
- All fetched 2026-08-25.
