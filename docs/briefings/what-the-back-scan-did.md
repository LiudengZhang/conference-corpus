# What the back-scan did to the verdicts

*Measured 4 September 2026. Reproduce with `python3 scripts/thread_diff.py` and
`python3 scripts/thread_diff.py --format trajectory`.*

Thread status in this corpus is derived, never stored. `status_of()` in
`scripts/build_briefing.py` recomputes it from cumulative supports and refutes
every time a briefing is generated, and `data/threads.yml` says why: the first
version of that file asserted a status per thread, every one of them from a
single month's reading, and none of them ever recomputed.

Deriving it is the right design. It also has a consequence nobody had looked
at. **Adding cards to a past month rewrites the published thread history in
place, for every month after it.** On 2026-09-04 the back-scan added 1,634
cards to months that had already been carded, briefed and deployed. Everything
regenerated correctly. Nothing was wrong. And the curve moved underneath the
whole record while the prose describing it stayed where it was.

## 30% of the curve moved

Twelve carded threads across 44 months is 528 thread-months. **160 of them —
30% — now carry a different status than they did before the re-read.**

Three threads changed where they end up:

| Thread | Before | After |
|---|---|---|
| `neoantigen-vaccines` | +25 / −26 contested | **+91 / −56 splitting** |
| `next-gen-checkpoints` | +33 / −38 contested | **+81 / −68 splitting** |
| `suppressive-population-inversion` | +20 / −73 crisis | **+58 / −112 contested** |

Reading only the endpoint would have missed most of it. Two of the largest
threads in the corpus end exactly where they ended before and were a different
thread for the whole run-up:

| Thread | Months changed | Was | Is now |
|---|---|---|---|
| `immunotherapy-resistance` | 39 of 44 | splitting in 35 months | **forming in all 44** |
| `cell-therapy` | 35 of 44 | splitting in 33 months | **forming in all 44** |
| `suppressive-population-inversion` | 41 of 44 | crisis in 42 months | contested in 38 |
| `ctdna-mrd` | 13 of 44 | forming in 42 months | forming in 31, splitting in 12 |

`cell-therapy` and `immunotherapy-resistance` were read as `splitting` for three
years. Read completely, they were never splitting. `suppressive-population-inversion`
was called a crisis for its entire life and was contested for almost all of it.

## Which direction, and why

The global stance mix barely moved: the 1,241 pre-existing cards are 40.9%
refutations, the 1,634 added ones 38.5%. That two-point difference cannot
produce a 30% rewrite, and the explanation is not global. It is per thread.

| Thread | Refutation share, pre-existing | in the added cards | shift |
|---|---|---|---|
| `suppressive-population-inversion` | 78.5% | 50.6% | **−27.8** |
| `neoantigen-vaccines` | 51.0% | 31.2% | **−19.7** |
| `next-gen-checkpoints` | 53.5% | 38.5% | **−15.1** |
| `cell-therapy` | 30.5% | 20.3% | −10.2 |
| `foundation-models` | 45.8% | 38.4% | −7.4 |
| `method-credibility` | 96.9% | 95.5% | −1.4 |
| `immunotherapy-resistance` | 24.0% | 25.5% | +1.5 |
| `interception` | 12.8% | 14.9% | +2.1 |
| `neuro-immune-microbiome-axis` | 8.1% | 10.4% | +2.3 |
| `ctdna-mrd` | 23.7% | 27.5% | +3.8 |
| `single-cell-3d-genome` | 16.1% | 21.1% | +5.0 |

**The threads that moved are exactly the threads that were most
refutation-heavy, and they moved toward the middle.** The threads that were
already support-heavy stayed put or drifted very slightly the other way. This is
not the field changing its mind between 2023 and 2026 — every one of these cards
was written about the same papers in the same months. It is the reading
regressing toward its own mean once the instrument stopped varying.

The corpus predicted this about itself and never acted on it. Three 2023
briefings carry a section headed *How to read the ratio* saying the quarter's
40% refutation share "is a property of how these months were read rather than of
the months themselves: the reading brief ranked refutations first and
deliberately hunted them." That warning was published, and then the thread
verdicts computed from those cards were published beside it as though the
warning did not apply to them.

### The sharpest case

`suppressive-population-inversion` exists to test whether depleting a population
identified as immunosuppressive improves outcomes. Its `denominator` field in
`data/threads.yml` said, until today:

> The supporting side is not carded and cannot be, because it is a genre rather
> than a set of citable findings.

The back-scan carded 38 of them. The claim was not a fact about the literature;
it was a fact about a reading brief that recognised "population X turns out to
be protective" as a finding and "we depleted X and the tumour shrank" as
wallpaper. Under one instrument the thread reads 58 supports against 112
refutes — still refutation-led, which is the honest form of the original
observation, but not the 20-against-73 that made it a crisis.

### The one thread that got worse

`ctdna-mrd` is the only thread the re-read moved against. It was `forming` in 42
of 44 months; it now opens `contested`, spends twelve months `splitting`, and
reaches `forming` later than the record used to say. The refutations that
abstracts surfaced there — trials where the assay predicts well and changes
nothing — were sitting in abstracts whose titles named the cohort and not the
outcome. That is the trial-title problem this corpus already had a rule for.

## What the rule cannot see

`status_of` counts supports and refutes. `neutral` cards do not enter it at all.
Across the corpus that is 205 cards, 7%, which is unremarkable. Per thread it is
not:

| Thread | Cards | Neutral | Share |
|---|---|---|---|
| `agentic-ai` | 81 | 30 | **37%** |
| `ctdna-mrd` | 153 | 35 | **23%** |
| `next-gen-checkpoints` | 164 | 15 | 9% |
| `interception` | 218 | 19 | 9% |

`agentic-ai` holds 81 cards and more than a third of them are invisible to its
own verdict. This is not a defect — a neutral card is one that genuinely does
not move the claim, and counting it either way would be worse. But it means a
status is computed on a fraction of a thread that varies from 63% to 97%
depending which thread you are reading, and no briefing table shows that
fraction. **The rule is not being changed in this pass.** Changing a derivation
rule and re-reading the evidence in the same commit makes neither of them
checkable.

!!! note "Corrected 2026-09-04 — two fields in threads.yml were false"
    `method-credibility.denominator` said "computed on 2026-09-04 over 370
    cards it is 347 refutes, 13 neutral, 10 supports — 94%". The thread holds
    **654 cards: 610 refutes, 19 neutral, 25 supports**. The figure was
    computed midway through the back-scan and dated as though it were final,
    which is worse than an old number: it carries today's date. Note how it
    hid — the percentage moves 94% to 93% while the counts nearly double, so
    the ratio stayed plausible while the denominator went stale underneath it.

    `suppressive-population-inversion.denominator` said the supporting side
    "is not carded and cannot be". It is now carded 58 times. Both fields are
    rewritten; the claims they made are retracted here rather than edited away.

!!! warning "What this does not license"
    None of this is evidence that any scientific claim got stronger or weaker.
    Every card involved describes a paper published between January 2023 and
    August 2026, and no paper changed. What changed is how completely each
    month was read. A thread that moved from `crisis` to `contested` did not
    recover; it was never in a crisis, and the corpus said so for three years.

    Nor is the new mix proven unbiased. It is proven *uniform* — one brief,
    one instrument, every month. Twelve readers sharing one brief are still
    twelve readers, and the same caveat that hangs over the residual spread in
    the density census hangs over these ratios.

## What follows

- `scripts/thread_diff.py` exists now, so the next re-read cannot do this
  silently. Run it before publishing any pass that adds cards to past months.
- The status rule's blindness to `neutral` is documented here and left alone.
  If it is ever changed, change it in `status_of` and nowhere else, and re-run
  this comparison across the change rather than across an evidence edit.
- Every figure in this corpus computed before 2026-09-04 rests on the old card
  set. The density census makes the same point for card counts; this makes it
  for verdicts.
