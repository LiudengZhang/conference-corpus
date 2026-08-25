# SITC Computational IO Series 2026

**A ten-part webinar series from the SITC Big Data and Data Sharing Committee — computational methods and clinical utility for biomarker development in immuno-oncology, with the 2026 edition aimed squarely at early-disease settings, immunoprevention, and immune interception.**

- **Event:** 2026 SITC Computational Immuno-Oncology Series — the sixth iteration of the series
- **Format:** 10 virtual webinars, 1–1.5 h each, live Zoom + Q&A
- **Dates:** May 19, 2026 → November 9, 2026 (session 10 date TBD)
- **Host:** Society for Immunotherapy of Cancer (SITC), Big Data and Data Sharing Committee
- **Series page:** [sitcancer.org/edu/webinars/computational](https://www.sitcancer.org/edu/webinars/computational)
- **Access:** free for SITC members; $45–$125 for non-members. Registrants get four weeks of Zoom access, after which recordings are hosted permanently on **SITC OnDemand**.

> **Status: scaffold, speaker slate verified against the SITC series page (fetched 2026-08-25).** Four of the ten sessions have been delivered (May 19, Jun 9, Jul 9, Jul 21); session 5 runs Aug 27. **No transcripts are in this vault** — unlike [SCGD26](../single-cell-genomics-day-2026/index.md), the recordings sit behind SITC OnDemand's member/registrant wall, so per-session pages currently carry the verified slate (title, date, moderator, faculty) plus corpus-fit notes, and the science sections are marked as *pending recording access*. Anything not attributable to the SITC page is flagged inline.

## Brand disambiguation (read this first)

**This is not the SITC Annual Meeting.** The [`sitc-2026/`](../sitc-2026/index.md) vault covers the **SITC 41st Annual Meeting**, Phoenix Convention Center, November 4–8, 2026 — ~6,000 attendees, JITC abstract supplement, embargoed press program, `trials/` + `tools/` templates.

This vault covers a **separate, year-round educational webinar series** run by one SITC committee. Different format (virtual, single-speaker, recorded), different cadence (monthly, May–November), different content type (methods tutorials and lab-in-progress talks, not embargoed abstract readouts), different audience gate (registration, not meeting badge). The two are siblings and cross-link — several series faculty are likely to also present in Phoenix — but they should not be merged, for the same reason [`single-cell-genomics-day-2026/`](../single-cell-genomics-day-2026/index.md) is kept separate from [`single-cell-genomics-2026/`](../single-cell-genomics-2026/index.md): same society branding, different meeting.

## Why this is in the vault

- **It is a methods series, delivered, and recorded.** The corpus is mostly pre-meeting scaffolds. This is a set of talks that have already happened, with a permanent hosted archive — the same reason SCGD26 earned its own vault. It is the highest-yield SITC-adjacent material available before the Phoenix meeting in November.
- **It sits on the corpus's AI-for-biology axis, in an IO frame.** Session 4 is explicitly foundation models for medical imaging; session 9 is AI prediction of TCR–antigen binding; session 6 is trajectory modeling of immune escape. These map onto [`aacr-2026/topics/virtual-cells/`](../aacr-2026/topics/virtual-cells/index.md), [`aacr-2026/topics/bioinfo-tools/`](../aacr-2026/topics/bioinfo-tools/index.md), and [`aacr-2026/topics/single-cell-spatial-omics/`](../aacr-2026/topics/single-cell-spatial-omics/index.md).
- **The 2026 framing — immunoprevention and immune interception — is a genuinely new axis for this corpus.** Early detection, pre-cancer atlases, and epigenetic risk stratification in high-risk populations are not well covered by any existing vault. Sessions 2, 3, and 10 are the seed of that thread.
- **It previews Phoenix.** Series faculty and committee members are a reasonable leading indicator of who will chair and present at [SITC 2026](../sitc-2026/index.md) in November, and the biomarker-methods content feeds directly into that vault's [`tools/`](../sitc-2026/tools/index.md) template.

## Organizing committee

SITC Big Data and Data Sharing Committee:

| Name | Affiliation | Role |
|---|---|---|
| Song Liu, PhD | Roswell Park Comprehensive Cancer Center | Chair |
| Alan Hutson, PhD | Roswell Park Comprehensive Cancer Center | Past Chair |
| Carsten Krieg, PhD | Medical University of South Carolina | Co-Chair |
| Riyue Bao, PhD | UPMC Hillman Cancer Center | Member |

## The full slate

Times are US Eastern, as published by SITC. **Delivered** = the session date has passed as of 2026-08-25.

| # | Session | Date | Faculty | Status |
|---|---|---|---|---|
| 1 | [Virome & engineered probiotic bacteria](sessions/01-virome-probiotics.md) | May 19 | Demehri, Arpaia, Tan | Delivered |
| 2 | [Epigenetic-based prevention & early detection](sessions/02-epigenetic-early-detection.md) | Jun 9 | Bock | Delivered |
| 3 | [Immune-based early cancer detection](sessions/03-immune-early-detection.md) | Jul 9 | Li | Delivered |
| 4 | [AI, foundation models & medical imaging](sessions/04-ai-foundation-models-imaging.md) | Jul 21 | Yu | Delivered |
| 5 | [Structure-based design of immunogens](sessions/05-structure-based-immunogen-design.md) | Aug 27 | Babu | Upcoming |
| 6 | [Modeling immune escape trajectories](sessions/06-immune-escape-trajectories.md) | Sep 15 | Jerby | Upcoming |
| 7 | [Precision immune oncology](sessions/07-precision-immune-oncology.md) | Oct 1 | Balachandran | Upcoming |
| 8 | [Systems immunology & T-cell memory](sessions/08-systems-immunology-t-cell-memory.md) | Oct 27 | Chi, Chen | Upcoming |
| 9 | [AI prediction of TCR–antigen binding](sessions/09-ai-tcr-antigen-binding.md) | Nov 9 | Wang, Zhang, Bradley | Upcoming |
| 10 | [Pre-Cancer Atlas](sessions/10-pre-cancer-atlas.md) | TBD | Shain | Unscheduled |

See [Sessions](sessions/index.md) for the per-session pages.

## Threads running through the series

**Immunoprevention / interception (new to this corpus).** Sessions 1, 2, 3, and 10 all address the pre-malignant window — microbiome and probiotic engineering, epigenetic risk in high-risk cohorts, immune-based early detection, and a pre-cancer atlas. No existing vault covers this; it is the strongest argument for building this one out.

**Antigen and receptor prediction.** Sessions 5 and 9 bracket the structural-design problem from both ends: designing immunogens and predicting TCR–antigen binding. Both are protein-ML problems and connect to the protein-language-model material in [`talks/fm-to-virtual-cells/adjacent-methods/protein-lm-explainability.md`](../../talks/fm-to-virtual-cells/adjacent-methods/protein-lm-explainability.md).

**Modeling cell state and trajectory.** Sessions 6 and 8 are single-cell/systems-immunology modeling in an IO frame — immune-escape trajectories and T-cell memory programs — and are the natural bridge to the [AACR single-cell + spatial](../aacr-2026/topics/single-cell-spatial-omics/index.md) and [virtual-cells](../aacr-2026/topics/virtual-cells/index.md) topics.

**Clinical translation.** Session 7 (precision IO) and the biomarker framing throughout feed the [SITC 2026 `tools/`](../sitc-2026/tools/index.md) template and, on the trial side, [`asco-2026/trials/`](../asco-2026/trials/index.md).

## What to harvest next

1. **Recording access.** The four delivered sessions are on SITC OnDemand. With registrant or member access, these pages can be upgraded from scaffold to transcript-backed, matching the SCGD26 standard.
2. **Speaker-work linkage.** Each faculty page should link the specific methods and papers the talk covered — deliberately left out for now rather than guessed at.
3. **Sessions 5–10 as they land.** Session 5 is two days out; the series runs to November 9, finishing the same week as the SITC Annual Meeting.

## Sources

- Series overview, slate, faculty, committee, and access terms: <https://www.sitcancer.org/edu/webinars/computational> (fetched 2026-08-25)
- Registration portal: <https://sitc.execinc.com/edibo/COMPIO26Webinars>
- SITC OnDemand (recording archive): <https://www.sitcancer.org/>
