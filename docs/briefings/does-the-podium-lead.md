# Does the podium lead the page?

*Measured 26 August 2026. Reproduce with `python3 scripts/lead_time.py` and
`python3 scripts/lead_time.py --papers`.*

Every monthly briefing in this corpus rests on one assumption: that a meeting
programme shows you where a field is going before the journals do, and that the
gap is worth having. The assumption was never tested. It could not be — the
journal index started at 2025-01 and every conference vault was 2026, so the two
layers barely overlapped and no lead was measurable in either direction.

Testing it needed a meeting old enough for the literature to have answered it.
**AACR 2024 and ASCO 2024 — 14,895 abstracts with full text, from Crossref —
against a journal index of 35,542 research articles running 2024-01 to
2026-08.**

## The answer

**Meetings do lead, by about ten to thirteen months. Almost nothing said at them
arrives.**

| | |
|---|---|
| Median abstract-to-paper lag | **10–13 months** (IQR ≈ 7–20) |
| Stability of that lag | unchanged across every match threshold tried |
| Abstracts becoming papers in these 33 journals | **≈1%** |
| Previous estimate in `threads.yml` | 4–6 months, from five hand-picked cases |

The lag is the robust part. Tightening or loosening the matching threshold moves
the hit rate by an order of magnitude and barely moves the median lag, which is
what a real effect looks like. The old 4–6 month figure was low by about a
factor of two, and it came from five cases chosen by someone who already
believed the answer.

The hit rate is the part that should change behaviour. At a Jaccard cutoff of
0.5, 98 of 14,890 abstracts (0.7%) match a paper published later.

!!! danger "Retracted 2026-08-27 — the chance rate below was not a chance rate"
    **Every "chance" and "excess" number in this section is withdrawn.** The
    conclusions above it — the 10–13 month lag, the ~1% conversion — do not
    depend on it and stand.

    The baseline was built by running the same matcher against journal papers
    published *before* the meetings, where a match cannot be a prediction. The
    query selecting them was `month < '2024-04'`, against a journal index whose
    first month is 2024-01. So the "before" arm was three months —
    **2024-01, 2024-02 and 2024-03** — and those are exactly the months this
    cohort deposits into: ASCO's GI and GU symposia in January and February
    (752 and 708 abstracts) and AACR in March (6,642).

    A journal paper from March 2024 matching an AACR March 2024 abstract is not
    a coincidence. It is the same work appearing in both places at once. The
    arm built to measure luck was measuring simultaneity, which is the one thing
    it had to exclude.

    It was also a tenth the size of the arm it was compared against, so the two
    rates were never comparable even in principle.

    `scripts/lead_time.py` now derives both arms from the cohort's own meeting
    months and refuses to report an excess when the pre-meeting pool is empty,
    rather than printing a number. Extending the journal index to 2023-01 —
    running as this was written — gives twelve journal months that genuinely
    predate the 2024 meetings, and will produce the first uncontaminated
    baseline this measurement has ever had. The table is left blank until then
    rather than filled with the old figures.

| Match threshold | Matched later | Matched *earlier* (chance) | Excess |
|---|---|---|---|
| 0.35 | 3.0% | *withdrawn* | *withdrawn* |
| 0.45 | 1.0% | *withdrawn* | *withdrawn* |
| 0.50 | 0.7% | *withdrawn* | *withdrawn* |
| 0.60 | 0.3% | *withdrawn* | *withdrawn* |

So of the order of one abstract in a hundred becomes a paper in the tracked
journals within two years. Reading an abstract book to find them means reading
about two hundred abstracts per eventual paper. The meeting is a real leading
indicator and a terrible filter, and those two facts have to be held at once.

!!! warning "What this does not measure"
    These are the corpus's 33 elite journals. Most AACR and ASCO abstracts were
    never going to appear in *Nature* or *NEJM* — they publish in specialty
    journals outside the window, and that is not a failed prediction. The
    ~1% is a conversion rate **into this corpus**, not into the literature.
    Title-similarity matching also misses any abstract whose title was rewritten
    for publication, so the true conversion is higher than 1% by an unknown
    margin. The lag is the number to carry forward; the rate is a lower bound.

## The vocabulary version is dead

A cheaper version of the premise says you do not need to track individual
results — just watch which words are getting loud at the meeting, because that
is where the literature goes next. That version is refuted.

Ranking terms by how over-represented they are at the 2024 meetings relative to
the 2024 journals, and asking whether that predicts journal growth by 2026:

| Predictor | Spearman ρ |
|---|---|
| Conference over-representation, raw | +0.168 |
| Conference over-representation, register-controlled | **+0.091** |
| Null: a random half of the journals' own 2024 output | **+0.088** |

The gap between the meeting and a coin-flip split of the journals' own back
catalogue is **0.003**. The apparent signal in the raw figure is not science, it
is dialect: `mcrpc`, `pts with metastatic`, `real world`, `first-line 1l` —
abstract shorthand that journal titles never use whatever the underlying work
does. Require a term to appear in at least one journal title and the effect
evaporates.

The same confound wrecks the naive first-appearance version. Of terms said at
five or more meeting records and absent from every 2024 journal title, 43% later
appear in a journal title and 57% never do — but reading the two lists shows
they contain the *same kind of term*. `mcrpc` arrived; `mcrc` did not. `hnscc`
arrived; `hcc` did not. That split is a coin flip on which abbreviation an
editor tolerated.

## Why this took nineteen months to check

Both predictors in the growth test carry the 2024 journal rate in their
denominator, so a term that was rare in 2024 by chance scores high on
over-representation *and* on growth. That artefact alone produces a positive
correlation from nothing, and the first version of this analysis reported it as
a result. It needed a null model built from the journals' own data to see.

The first version of the first-appearance test was worse: it returned
"conference first, 100% of terms, median lead twelve months", which was purely
the shape of two non-overlapping windows. The fix for that was harvesting 2024.

Which is the general lesson, and it is not really about conferences. Every
"first appearance" claim this corpus has published — five of them — moved
earlier the moment the window was extended, and none has ever survived. A
bounded window cannot date a beginning. It can only report its own floor.

## What follows

- The `clinical-practice` thread now carries measured numbers instead of an
  estimate. See `data/threads.yml`.
- A meeting abstract is worth logging when it names a specific trial, target or
  readout that can be checked against the literature in a year. It is not worth
  mining for emerging vocabulary.
- Ten to thirteen months is the planning horizon the corpus can actually claim.

## The conference layer has since grown, and it does not change this

On 2026-08-27 the store went from two venues to nine — 18,749 abstracts, adding
ELCC, ESMO Breast, ESMO GI, ESMO Gynaecological, USCAP 2026 and two ESMO Open
supplements whose congress could not be identified. **None of them can extend
this measurement**, and it is worth being explicit about why, because a bigger
number invites the assumption that the finding got stronger.

Everything new is from 2026. The lag being measured is ten to thirteen months,
and the journal index ends at 2026-08 — so a March 2026 abstract book has about
five months of follow-up against a median lag of twelve. Testing it now would
return a low hit rate that means "not enough time has passed", and would be
indistinguishable from "these meetings do not lead". The 2024 cohort is the only
one with a follow-up window longer than the effect it is measuring, so the
numbers above are still computed on AACR 2024 and ASCO 2024 alone.

The 2026 venues also arrive as titles only — the ESMO family and *Laboratory
Investigation* deposit abstract metadata without abstract text. The 2024 test
used full text. Re-running it in 2027, when the follow-up window is long enough,
will therefore be a weaker test on those venues, not merely a later one.

What the new venues are good for now is coverage of what was actually said in
2026, which is what sections 6 of the monthly briefings report.
