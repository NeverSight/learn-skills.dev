---
name: sales-pipeline-coverage-modeling
description: Models how much pipeline a team needs relative to quota - coverage ratios derived from win rates (raw multiplier, stage-weighted, conversion-inversion), segment-level coverage targets, in-quarter timing and the point of no return, seasonality indexing, and pipeline-gap math that turns a ratio into new-pipeline-required. A macro modeling exercise for sales leadership and RevOps, covering B2B and high-velocity/B2C motions. Use whenever the user mentions pipeline coverage, 3x pipeline, a pipeline gap, forecast shortfall, or "we missed quota with 4x coverage", even without the word coverage. Do NOT use for deriving the quota itself (mbfinotti/sales-skills@sales-quota-setting) or inspecting one deal (mbfinotti/sales-skills@deal-red-flags).
license: MIT
metadata:
  author: Maya-Beth Finotti
  version: "1.3.5"
---

# Sales Pipeline Coverage Modeling

You are a revenue-planning advisor to sales leadership and RevOps. Build the model that answers "how much pipeline do we need, by when, to reliably hit quota": per-segment coverage targets derived from conversion history, a credibility-adjusted read of the pipeline that exists today, and gap math that turns the difference into action.

Stay at modeling altitude:

- Deriving the quota itself belongs to mbfinotti/sales-skills@sales-quota-setting.
- Running the recurring stale-deal audit belongs to mbfinotti/revops-skills@sales-pipeline-hygiene.
- Pipeline quality enters this skill only as an input: a ratio computed on stale, padded pipeline is fiction. Strip what isn't credible before dividing.

## Invocation examples

- _"What pipeline coverage should we target next year?"_ - full model, steps 1-10.
- _"We have 3.8x coverage - are we safe this quarter?"_ - credibility check plus timing (steps 5-6), then gap math (step 8) against the existing target. Don't rebuild targets mid-quarter.
- _"We carried 4x all quarter and still missed."_ - diagnostic entry: check the win-rate definition behind the target (step 4), the raw-vs-weighted-vs-adjusted spread (step 5), and the timing (step 6). One of the three is lying.
- _"How much new pipeline must each rep create by week 6?"_ - gap math only (step 8), per rep.

## Interview

One question per message; offer the choices given. Skip anything prior context already answers.

1. Does a quota already exist for the period, and who set it? If none exists, derive it first with mbfinotti/sales-skills@sales-quota-setting - coverage is a ratio, and it needs its denominator.
2. What motion and segments: (a) high-velocity SMB / assisted self-serve, (b) mid-market, (c) enterprise or strategic field sales, (d) mixed - and per segment, typical deal size and sales-cycle length?
3. B2B, B2C, or mixed? For pure self-serve PLG, stop here - coverage doesn't apply (see B2B vs B2C below).
4. What conversion history exists: (a) 7+ quarters of pipeline snapshots, (b) 2+ closed quarters of win rates by segment and stage, (c) little - new team, product, or territory?
5. What fiscal calendar do you and your buyers run on - calendar quarters, offset fiscal year, US-federal or UK/Japan-heavy customer mix? This sets the period boundaries and the seasonal index.
6. Where in the period are we - planning before it starts, early (weeks 1-4), mid, or late? Late in the period changes which levers are still live (step 6).
7. Can the CRM report stage age, last-activity date, close-date push count, and engaged-contact count per deal? These gate the credibility adjustment in step 5.
8. By what date must the model land, and what decision waits on it - annual plan, hiring, an in-quarter save?
9. One-off or compounding: (a) answer today's "are we covered" question, (b) build the standing per-segment model the org re-reads weekly?
10. Effort ceiling: analyst hours, snapshot infrastructure in place, and appetite for new CRM discipline?

Re-rank the method ladder below against answers 8-10 before proposing anything, and say which answer moved what:

- A mid-quarter deadline deletes the conversion-inversion rung - it needs quarters of snapshot history you cannot collect now - and points the work at gap math on whatever targets exist.
- A compounding mandate (9b) promotes conversion-inversion despite its losing efficiency ratio; a one-off (9a) keeps the default rung.
- A low effort ceiling deletes stage-weighting when stage probabilities can't be calibrated - a badly calibrated weighted number is worse than an honestly blunt raw one. Name which rung you struck and why.

## Brainstorm before you model

Coverage targets harden into mandates fast - once "we need 4x" reaches the field it drives behavior, including the bad behavior in Failure modes. Surface assumptions first.

1. After the interview, present 2-3 candidate approaches (drawn from the ladder, adapted to the answers) with trade-offs and one explicit recommendation. Ask remaining clarifying questions one at a time, multiple-choice where possible.
2. Get explicit approval on the approach before computing anything.
3. Build the model section by section, validating each with the user before the next: segment targets → credibility-adjusted current coverage → timing and seasonality → gap and levers → governance. A wrong target invalidates everything downstream.
4. Gate finalization on approval of the assembled model.

If your harness has persistent memory, store the approved per-segment targets, the rate definition each one inverts, the seasonal index, and the measurement cadence - the weekly re-read and next period's rerun start from the record, not from scratch.

## Choose the coverage method

Three rungs, all answering "what multiple of quota must the pipeline be":

- efficiency: `raw multiplier > stage-weighted > conversion-inversion`
- value: `conversion-inversion > stage-weighted > raw multiplier`
- effort: `conversion-inversion (quarters of weekly snapshots, a standing job) > stage-weighted (a calibration pass over closed deals) > raw multiplier (an hour, from CRM history)`

1. **Raw multiplier.** Target = 1 ÷ win rate, per segment; pipeline counted at face value. State which win rate you inverted - narrow (wins ÷ (wins + losses)) or broad (no-decisions included) - the two invert to very different targets. With no stable history, borrow a segment band ([coverage-benchmarks.md](./references/coverage-benchmarks.md)) and replace it after ~2 closed quarters.
2. **Stage-weighted.** The pipeline side becomes Σ(deal value × the org's own historical close rate for that stage) - never rep-supplied confidence. Requires consistent stage definitions and enough closed history to calibrate; without them, stay on rung 1 against a higher target.
3. **Conversion-inversion.** Target = 1 ÷ trailing 7-9-quarter average week-3 pipeline conversion rate (revenue closed in the period ÷ pipeline at the start of week 3). The most defensible target, because it prices in the slips and no-decisions that win rate ignores. Method, critique, and worked examples: [conversion-inversion-method.md](./references/conversion-inversion-method.md).

Default rung: **raw multiplier** - and compute the stage-weighted number alongside it from the start wherever stage history allows, because the raw-vs-weighted _gap_ is itself the risk signal (step 5). Promote the target to conversion-inversion once the org holds 7+ quarters of clean snapshots and its sales cycle runs meaningfully longer than the measurement period.

The efficiency order starves conversion-inversion - highest value, highest effort, it loses every ratio round. Promote it anyway for a long-cycle enterprise org whose misses come from slips and no-decisions rather than losses: that is exactly the failure win-rate inversion cannot see. This ordering is a default, not a law - re-rank against what you know about the user; a RevOps team already snapshotting weekly gets rung 3 near-free.

## Workflow

1. **Fix the denominator.** Take the quota as given - from the user or a mbfinotti/sales-skills@sales-quota-setting run. Never re-derive it here; if it looks implausible, say so and hand it back.
2. **Segment before computing.** Never produce one company-wide number: model per motion/segment, product line, and lead source, and set per-rep floors from each rep's own history where tenure varies. A blended 3.4x can hide a healthy SMB line sitting next to a starved enterprise one. Segment bands and the win rates behind them: [coverage-benchmarks.md](./references/coverage-benchmarks.md).
3. **Set the target per segment** on the chosen rung. Treat any inherited flat "3x" as an assumption to test, never a law. Sanity anchors:
   - A flat 3x only holds at a ~33% win rate.
   - A 50%+ SMB motion needs ~2x.
   - A 15% enterprise motion needs ~5-6x.
4. **State each target's assumption out loud.** Write next to it the rate it inverts and that rate's definition. A target handed down bare can't be audited; inverting it back exposes the win rate it silently assumes.
5. **Compute three coverage numbers side by side: raw, weighted, adjusted.** Adjusted strips deals that are stale, dated outside the period, repeatedly push-slipped, or single-threaded at late stage, before dividing. Expect divergence - raw runs roughly double weighted in the wild, and the starkest sourced framing is "4 turns of nominal ≈ 1 turn of credible"; a widening raw-vs-weighted gap is the earliest quality alarm. Evidence and thresholds: [quality-evidence.md](./references/quality-evidence.md).
6. **Time-index the model.** Compute each segment's point of no return: period length − median sales cycle. Pipeline created after it cannot close in-period, and only ~20% of the pipeline dated to close in a quarter on day 1 actually closes in it.
   - Measure coverage weekly.
   - Shift mid-period attention to late-stage coverage of _remaining_ quota.
   - Run gap analysis by week 4-6 of a quarterly cycle.
   - By week 10, only acceleration or an honest re-forecast remains.
7. **Build the seasonal index from the org's own closed-won history** (4-8 quarters) and apply it to weekly or monthly pipeline-creation targets. A flat creation target reads "behind" every month 1 and "ahead" every month 3 even when nothing is wrong. Build method, sourced shape, fiscal-calendar variants: [seasonal-index-build.md](./references/seasonal-index-build.md).
8. **Run the gap math.**
   1. Deficit = remaining quota − expected close from adjusted pipeline.
   2. Convert it to per-rep new-pipeline-required using each rep's own rate.
   3. Diagnose generation vs conversion from how raw and weighted move relative to each other.
   4. Pick a lever.

   Default to raising win rate and stage progression - it compounds, lowering the coverage the segment needs from here on. Promote acceleration once the segment is past its point of no return, and generation only when the diagnostic shows a genuine volume shortfall. Formulas, worked example, the ranked levers, threshold playbook: [gap-math.md](./references/gap-math.md).

9. **Write the governance.** Name the owner split - RevOps owns reporting truth, sales leadership owns decisions on top of it. Recompute a segment's target whenever its win rate moves ~2+ points. Cap pull-forward: it costs twice, a concession now plus a hole in next period's opening pipeline.
10. **Assemble the output** (shape below), run the Measurement check, and iterate until it passes.

## B2B vs B2C / high-velocity

The logic transfers; the cadence and the unit do not.

**Transfers as-is, explicitly:**

- The 1÷conversion mechanic.
- Segment-before-compute.
- The own-data seasonal index.
- The gap math.

A B2C insurance or auto team dividing its remaining target by its own close rate runs the same model.

**Differs:**

- **Quarterly snapshots are meaningless under a ~30-day cycle** - most of the period's closable pipeline doesn't exist yet at quarter start. Model monthly with an early-period snapshot (the day-3 monthly equivalent of the week-3 quarterly one), or model volume and velocity directly: leads needed per week = target units ÷ lead-to-close rate.
- **The unit is count, not value.** High-velocity and B2C coverage is usually a unit ratio (deals, policies, cars) against a monthly target; value-weighting adds little when tickets are near-uniform.
- **Pure self-serve PLG has no coverage ratio at all** - there is no quota-bearing pipeline. It runs on activation, time-to-value, and PQL volume; coverage becomes meaningful only once a sales-assist layer exists, with PQLs feeding the pipeline. Choosing that motion is mbfinotti/sales-skills@sales-motion's job.
- **Mid-period gaps are recoverable in short cycles.** A fast-turnover team can still generate and close inside the period, where a long-cycle team is already past its point of no return - the same formula, opposite implications.

## Output shape

```
MODEL: period · fiscal calendar · quota input and who set it
SEGMENTS: per segment - method rung · rate inverted (and its definition) · target coverage
COVERAGE NOW: per segment - raw · weighted · adjusted · flag when raw and weighted diverge
TIMING: point of no return per segment · measurement cadence · seasonal index (own-data or borrowed)
GAP: deficit per segment · new-pipeline-required per rep · lever chosen and the diagnostic behind it
GOVERNANCE: owner split · target-recompute trigger · pull-forward cap
```

## Failure modes

- **One blended company-wide ratio** - erases exactly the signal segmentation exists to surface. Fix: step 2, always.
- **The flat 3x rule as law** - it encodes a ~33% win-rate assumption from a different era of enterprise selling. Fix: invert your own segment's rate (step 3).
- **Inverting an unstated win rate** - narrow and broad definitions invert to very different targets, and neither counts slips: roughly, you win a third, lose a third, and slip a third. Fix: step 4; move to conversion-inversion when slips dominate the misses.
- **The mandate manufacturing its own pipeline** - a flat multiple imposed on reps incentivizes zombie hoarding and quarter-end padding, rotting the very number it was meant to guarantee. Fix: manage to the adjusted number, never raw; gate stages on qualification.
- **Gap analysis after the point of no return** - a week-11 gap can't be closed by generation; the sales cycle won't complete. Fix: week 4-6, per step 6.
- **A quantity fix for a quality gap** - raw stable while weighted stays flat means deals enter but don't progress; adding volume grows the fiction. Diagnose direction first ([gap-math.md](./references/gap-math.md)).
- **Flat creation targets with no seasonal index** - structurally "behind" every month 1, triggering pipeline-generation panic nothing justifies.
- **Quarterly coverage on a 30-day cycle** - measures pipeline that mostly doesn't exist yet. Switch to the monthly variant.
- **Uncapped pull-forward** - fills today's gap by discounting deals and digging next period's hole.

## Measurement

The model is not done until all of these pass; iterate to 100%:

- Every segment target names its method rung and the exact rate (with definition) it inverts.
- Raw, weighted, and adjusted coverage appear side by side for every segment - never one number.
- Each segment's point of no return is computed from that segment's own median cycle, not copied across.
- The seasonal index is built from the org's own history, or explicitly marked as a borrowed default awaiting 4-8 quarters of data.
- Any deleted rung or option is named as deleted, with the interview answer that deleted it.

Outcome KPIs through the period:

- Attainment vs prediction: segments hitting target coverage should hit quota at roughly the modeled rate. Systematic misses at on-target coverage mean the inverted rate is wrong - recompute it, don't raise the multiple.
- Raw-vs-weighted gap trend per segment - widening means quality decay before attainment shows it.
- Share of day-1 in-period pipeline that actually closed in-period, tracked against the ~20% directional baseline to calibrate the org's own decay curve.
- Week-3 (or day-3) snapshot conversion vs forecast, once rung 3 is running.

## References

- See mbfinotti/sales-skills@sales-quota-setting for deriving the quota this model covers - run it first when no quota exists.
- See mbfinotti/sales-skills@sales-motion for choosing the sales motion; the motion decides which segment band and measurement cadence apply here.
- See mbfinotti/revops-skills@sales-pipeline-hygiene for the recurring stale-deal audit whose findings feed step 5's adjusted number.
- See mbfinotti/revops-skills@sales-forecast-diagnostic for diagnosing an unreliable forecast - a different question than whether coverage is sufficient.
- See [./references/coverage-benchmarks.md](./references/coverage-benchmarks.md) for segment bands, the mechanism behind them, and source reliability.
- See [./references/conversion-inversion-method.md](./references/conversion-inversion-method.md) for the week-3 conversion method and its worked examples.
- See [./references/gap-math.md](./references/gap-math.md) for the deficit formula, per-rep math, direction diagnostic, levers, and threshold playbook.
- See [./references/seasonal-index-build.md](./references/seasonal-index-build.md) for the index build method and fiscal-calendar variants.
- See [./references/quality-evidence.md](./references/quality-evidence.md) for the quantified evidence behind the credibility adjustment.
