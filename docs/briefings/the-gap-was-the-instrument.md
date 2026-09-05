# The gap was the instrument

*Measured 4 September 2026, over all 36,597 research abstracts in the index.
Reproduce with `python3 scripts/check_corpus.py` against `data/evidence.yml`.*

Every card this corpus held for 2023, 2024 and 2025 was written from a
**title**. Every card for 2026 was written from an **abstract**. Nobody chose
that; it is where the reading happened to start, and it was never visible as a
choice. What it produced was a card-density curve that looked like a finding
about the field:

| Year | Cards per 1,000 papers, before | after | Cards | Research papers |
|---|---|---|---|---|
| 2023 | 25.1 | **80.4** | 733 | 9,114 |
| 2024 | 10.0 | **69.8** | 656 | 9,395 |
| 2025 | 24.0 | **80.1** | 811 | 10,126 |
| 2026 | 84.8 | **84.8** | 675 | 7,962 |

2024 and 2026 differed **eight-fold** under the old instrument. Under the new
one they differ by 15 points on the same scale, and all four years sit in a band
of 69.8 to 84.8. Nothing about the literature changed between those two
readings. All 36,597 research abstracts across 44 months have now been read with
the instrument 2026 was read with, and **1,634 cards were added** — the corpus
went from 1,241 to 2,875.

The lesson is not that the old numbers were low. It is that a density curve
computed across months read by different methods measures the method, and this
corpus published such a curve for a year without noticing.

## What titles hide

Every card written from an abstract carries `title_sufficient`: whether the
claim it records could have been reached from the title alone. That makes the
record its own instrument, and it now has four independent years in it.

| Year | Cards measured | Claim not in the title | …among refutations | …among supports |
|---|---|---|---|---|
| 2023 | 504 | **59%** | 82% | 44% |
| 2024 | 562 | **67%** | 77% | 58% |
| 2025 | 568 | **67%** | 82% | 58% |
| 2026 | 529 | **65%** | 74% | 54% |

**Refutations are hidden worse than supports in every year measured.** Four
independent replications, and the asymmetry never reverses. The mechanism is
genre rather than intent: a methods paper puts its result in the title because
the result is the method; an audit names the *object* it audited and not the
verdict; a clinical trial names the cohort and the intervention and not the
outcome. A corpus built from titles therefore over-collects announcements and
under-collects findings — which is the opposite of what it is for.

!!! warning "What this does not license"
    The residual spread between years — 69.8 to 84.8 cards per thousand — is
    real, small, and **not explained**. Twelve readers sharing one brief are not
    one instrument, and the honest reading is that the remaining differences are
    as likely to be reader variance as field variance. Do not build on them.

    Separately: any figure quoted elsewhere in this repo from before 2026-09-04
    — thread ratios, genre series, the templated-block counts — rests on the old
    uneven denominators and has not been re-run.

## Two things the titles were hiding

**Tumour mutational burden predicts checkpoint survival at chance.**
[39762425](https://pubmed.ncbi.nlm.nih.gov/39762425/) (2025-02): across 9,745
patients including ten phase 3 trials, TMB reaches an AUC of **0.503**, and
PD-L1 immunohistochemistry is beaten by routine bloodwork. Its title states none
of that, which is why this corpus missed it for a year while carding weaker
biomarker results either side of it.

**The intratumoral microbiome was re-analysed away, twice, in one month.** Two
*Science Translational Medicine* papers in 2025-09 re-analyse 8,908 Genomics
England genomes and all 5,734 TCGA whole genomes and find the intratumoral
microbiome largely absent. The corpus had carded the decontamination argument at
2023-12 and again in 2026, while these two sat unread inside the title-only
window — against roughly ten supporting cards on the same thread.

## What it did to the verdicts

Levelling the reading did not only change how many cards exist. Because thread
status is derived from the cards at render time, it rewrote the published thread
history in place: 160 of 528 thread-months now carry a different status, and
three threads ended up somewhere else entirely. That is measured separately in
[What the back-scan did](what-the-back-scan-did.md).
