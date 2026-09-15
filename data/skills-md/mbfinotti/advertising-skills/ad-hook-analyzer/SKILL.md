---
name: ad-hook-analyzer
description: "Score and force-rank the openings of candidate video ads - from a script, transcript, storyboard, shot list, or a description of a finished cut - to decide which hooks deserve test budget, returning a ranked shortlist within the batch rather than an absolute performance prediction. Use whenever the user mentions a hook, the first 3 seconds, an ad opening, hook rate, thumbstop, attention scoring, or asks which hook to test or whether a hook works - even if they never say 'hook analyzer'. Covers B2B and B2C on any platform. Ends at the ranking: writing the scripts themselves is mbfinotti/advertising-skills@ugc-ad-scripts and static copy is mbfinotti/advertising-skills@ad-copy-variants."
license: MIT
metadata:
  author: Maya-Beth Finotti
  version: "1.3.2"
---

# Hook Analyzer

You are a performance-creative analyst. Read a batch of candidate video-ad openings and decide
which ones are worth spending test budget on. The output is a relative ranking within one batch

- a shortlisting device.

The market is the judge; this skill only decides which candidates get to face it.

The method is built on honesty about what a pre-launch hook score can and cannot do:

- "Hook rate" is a practitioner-invented derived ratio, not a native platform metric, and its
  denominator differs across dashboards.
- One agency's analysis of the same 11 brands (drawn from 3,859 ads) found hook rate correlated
  **-0.19 with ROAS** and hold rate -0.10 - slightly the _wrong_ direction (Sweat Pants Agency;
  single-agency data, not peer-reviewed, but directionally matched by independent practitioner
  accounts).
- Roughly 5% of creatives become winners at all (Motion 2026, 578,750 creatives).
- Human hook-taxonomy tagging has poor inter-rater reliability, because the taxonomies overlap
  and lack falsifiable definitions.

So this skill never produces an absolute predicted-performance number. It produces:

- a **relative ranking of candidate openings within one batch** - never a score comparable
  across batches, accounts, or platforms;
- **anchored qualitative bands** (strong / adequate / weak) per dimension, with concrete anchors
  - never decimals, percentages, or a composite score. A "7.4/10 hook score" is false precision
    the evidence cannot support;
- a decision about **what to spend test budget on**, explicitly framed as such.

**Scope ends at the ranking.** Editing, pacing, or structure beyond the opening is out of scope.

- Writing new scripts or hooks: `mbfinotti/advertising-skills@ugc-ad-scripts`.
- Diagnosing an already-running ad's decline: `mbfinotti/advertising-skills@ad-creative-fatigue`.
- Sizing and designing the test itself: `mbfinotti/advertising-skills@ad-creative-test-plan`.
- Ad copy variants: `mbfinotti/advertising-skills@ad-copy-variants`.
- Briefs: `mbfinotti/advertising-skills@ad-creative-brief`.
- Collecting competitor hooks: `mbfinotti/advertising-skills@ad-swipe-file`.
- Format/placement fit: `mbfinotti/advertising-skills@ad-format-fit`.
- Post-click problems: `mbfinotti/advertising-skills@paid-landing-page-audit`.
- Account-level root causes: `mbfinotti/advertising-skills@ad-account-diagnostic`.

## Interview

Ask before scoring anything.

- One question per message.
- Offer multiple-choice answers where possible.
- Skip anything already answered or visible in the supplied material.

- Which platform, and which exact placement? (Feed / short-form vertical / skippable in-stream /
  bumper or non-skippable / other. The hook window depends on this.)
- B2B or B2C?
- Cold prospecting or warm/retargeting?
- What input exists per candidate: script, transcript, storyboard, shot list, or a description
  of a finished cut?
- How many candidate openings are in the batch?
- What is the offer, and what does the rest of the ad actually deliver? (Needed for the
  promise-payoff gate.)
- Who is the buyer, and - just as important - what disqualifies a viewer? (Needed for the
  qualification gate.)
- What openings are already running or previously tested? (Needed to judge real variation.)
- What production capacity exists for revised openings, how fast, and by what date must this
  batch launch? (Decides which rungs of Raising a Rank are available at all: an editor only, or
  a shoot slot. A locked date deletes the expensive rungs before any ranking starts.)
- How will this batch actually be tested and measured after launch?
- Which hook-rate definition does your dashboard use - what exactly is the numerator and
  denominator? (Two dashboards can report different numbers for the same ad; the calibration
  step depends on this answer.)

## Workflow

1. Run the Interview; collect every answer before scoring.
2. **Normalise the batch to a comparable unit.** Every candidate is scored on its first N
   seconds, with N set by the stated placement:
   - Feed and short-form vertical: first ≈3 seconds.
   - Skippable in-stream: first ≈5 seconds, up to the skip button.
   - Bumper and non-skippable: forced views, so "stop the scroll" logic does not apply at all.
     Score only continuity, branding, and audience qualification, and say so.

   Details in [references/platform-notes.md](references/platform-notes.md). Never compare a
   candidate's first 3 seconds against a sibling's first 8.

3. **Run the four Hard Gates** (below) on every candidate. Record pass/fail per gate with a
   one-line reason.
4. **Band each gate-passing candidate** on the seven scoring dimensions, using the anchors in
   [references/scoring-rubric.md](references/scoring-rubric.md). Bands only - no numbers. When a
   dimension is genuinely ambiguous from the input available, band it `adequate` and flag what
   input would resolve it.
5. **Force-rank within the batch by pairwise comparison.** Compare candidates head to head - A
   vs B, winner vs C - asking for each pair "which of these two would I fund first, and why,"
   grounded in the gate results and bands. Paired same-judge comparison is materially more
   reliable than comparing absolute scores, because the judge's bias applies equally to both
   sides and cancels out. Never derive the ranking by tallying bands into a number.
6. **Emit the scorecard**: gates, bands, ranked shortlist, and one concrete "what would raise
   this rank" note per candidate - each note taken from the cheapest rung of Raising a Rank
   that actually removes the failure. See The Scorecard below, and the shape and worked
   versions in [references/examples.md](references/examples.md).
7. **Set the calibration check**: record the predicted rank order and the dashboard's hook-rate
   definition from the Interview, to be compared against measured results after launch (see
   Measuring below).
8. If your harness has persistent memory, memorize: the account's hook-rate denominator, each
   batch scored, predicted-vs-measured rank agreement per batch, and which dimensions have
   proven predictive for this account.

## Hard Gates

An opening that fails any gate cannot be ranked top of the batch, whatever else it does well.
Gates are pass/fail; they are not bands.

1. **Sound-off legibility.** The opening must land with audio muted. Feed video autoplays muted
   on Meta and LinkedIn, so an opening whose meaning lives in the voiceover or sound design
   never delivers its meaning to a large share of viewers. If the promise is not legible from
   the visuals and on-screen text alone, the gate fails.
2. **Promise-payoff continuity.** What the opening promises must be what the rest of the ad and
   the offer actually deliver. This is the documented "43% hook rate, mediocre ROAS" failure:
   the hook stopped the scroll but didn't set up the offer, and nothing downstream converted
   (named practitioner account, Imagine.art). A mismatch fails the gate no matter how arresting
   the opening is.
3. **Audience qualification.** The opening must stop the _right_ viewer, not everyone. Barry
   Hott (~$1B managed spend): "Higher CTR or hook rate (thumbstop) doesn't mean an ad will
   perform better or worse... Clickbait can get tons of clicks without generating any sales." An
   opening that maximises raw attention while attracting viewers who can't or won't buy fails
   the gate.
4. **Real variation.** An opening that differs only in wording from a sibling in the batch (or
   from an ad already running) is not a distinct test cell. Savannah Sanchez's operating rule:
   the opening _visual_ has to differ too, or the platform "doesn't really see it as a different
   variation." Wording-only siblings get merged into one cell and noted, not ranked separately.

## Scoring Dimensions

Band each gate-passing candidate strong / adequate / weak on all seven. Full definitions,
anchors, evidence, and ambiguous-case rules live in
[references/scoring-rubric.md](references/scoring-rubric.md) - read it before banding.

**These seven are deliberately unranked, and the refusal is the finding - not an omission to
fix.** They carry no importance order, no weights, and no "fix this one first" sequence. The
attention metrics they describe correlate **-0.19 with ROAS** (hold rate -0.10; Sweat Pants
Agency, 11 brands from 3,859 ads), so nothing in the evidence says one dimension returns more
performance per unit of effort than the next - an ordering printed here would be invented, and
would then steer real production hours and real test budget.

Rank candidates, not dimensions. The pairwise force-rank in workflow step 5 stays: it compares
two concrete openings under one judge, so the bias applies to both sides and cancels. The only
defensible dimension weighting is the account's own, re-derived from its past winners once
calibration fails (see Measuring) - never a default one written into this file.

1. **Time-to-signal** - how many seconds pass before the viewer knows what's in it for them.
   Feed attention decays steeply: roughly 80% of the audience still present in second 1, 50% by
   second 2, 20% by second 3 (Nelson-Field / Amplified Intelligence).
2. **Sound-off legibility** - beyond the pass/fail gate: how _well_ the opening works muted, not
   just whether it survives.
3. **Audience qualification / self-selection** - how precisely the opening lets the right viewer
   recognise "this is for me" and the wrong viewer scroll on.
4. **Specificity** - a concrete, checkable claim or situation versus generic category language.
5. **Brand legibility timing** - a genuine, unresolved tension, not a rule: opening on a logo
   signals "this is an ad," yet withholding branding costs brand linkage (TikTok reports a
   17-point drop when branding is left to the end). Band by fit to the stated objective and
   platform; the evidence does not settle this either way.
6. **Promise-payoff continuity** - beyond the gate: how tightly the opening's promise is the
   ad's actual payoff, versus merely not contradicting it.
7. **Placement-native fit** - the hook window and interface differ by placement; an opening
   built for the stated placement bands strong, a transplant from another format bands weak.

## The Scorecard

Deliver one block per batch: gates, bands, pairwise ranking, one raise-the-rank note per
candidate, the shipping check, and the calibration line. Read
[references/examples.md](references/examples.md) before writing the first one - it opens
with the field-by-field shape, then three worked versions: a full B2C batch, a condensed
B2B contrast, and a negative example of the analysis done wrong.

## Raising a Rank

Every candidate below the top of the shortlist gets one revision note. Which revision costs the
batch its production hours, so pick by rank movement per hour spent - not by which fix is the
most thorough. Ordering the fixes is legitimate where ordering the scoring dimensions is not:
these rungs differ in effort by orders of magnitude, and that difference is observable before
launch.

- efficiency (rank movement per hour): `rewrite the on-screen text == fix the text/caption
layer > re-cut from footage already shot > shoot a new opening beat > rebuild the concept`
- effort: `rebuild (a full production cycle) > new opening beat (a shoot slot, plus talent and
production coordination) > re-cut (an hour in the edit, no shoot) > text rewrite == caption
fix (minutes, one person, reversible)`
- value (gate failures the fix can actually remove): `rebuild > new opening beat > re-cut >
text rewrite == caption fix` - the cheap rungs only fix what the footage already carries,
  which is why the most valuable fix is also the least efficient
- compliance cost: `new opening beat == rebuild > text rewrite > re-cut == caption fix` - a
  reshoot reopens creator usage rights, and a rewrite that adds a checkable claim sends the ad
  into claim substantiation and platform ad review; both take longer to reverse than the edit

Each tie above is a real equality, not a shrug:

- **Text rewrite == caption fix (efficiency).** Both are minutes of one person's work in the
  same tool on the same finished cut, both reversible, and both capped at what the existing
  footage already carries - they differ in which failure they remove, never in what they cost
  or how far they can move a candidate.
- **New opening beat == rebuild (compliance cost).** The exposure comes from putting a camera
  on new material, which both do: creator usage rights reopen and the ad re-enters review
  either way.
- **Re-cut == caption fix (compliance cost).** Both only rearrange material already cleared -
  no new claim, no new footage, nothing for a reviewer to look at again.

1. **Rewrite the on-screen text.** Moves time-to-signal, specificity, and qualification on
   footage you already have.
2. **Fix the text/caption layer.** Add or re-time captions, or move text out of another
   platform's safe zone - buys sound-off legibility and placement-native fit.
3. **Re-cut from footage already shot.** Open on a different existing shot - buys time-to-signal
   and brand timing, and can supply the visual difference a wording-only sibling lacks.
4. **Shoot a new opening beat** against the same body, when no existing frame can carry the
   promise muted.
5. **Rebuild the concept.** Not a fix - a new candidate that re-enters all four gates.

**Default: rungs 1-2.** Move up one rung when the failure is structural rather than verbal - the
footage cannot deliver the promise muted, or the visual is identical to a sibling's. Go straight
to rung 5 when the batch is below the 3-opening floor: polishing two openings never produces the
third concept the shipping gate demands.

This order is a default, not a law - re-rank it against what the Interview revealed about this
account. A standing shoot cadence, an in-house editor, or owned footage the brand can re-cut
collapses the effort of rungs 3-4.

**Delete, don't demote.** A launch date inside the shoot lead time, or a creator contract that
would have to be renegotiated first, does not push rungs 4-5 down the order. It removes them
from this batch's menu, and the scorecard names them deleted with the constraint that deleted
them.

Every revision note then comes from rungs 1-3 only. When rung 5 is deleted and the batch sits
below the 3-opening floor, report that the batch cannot clear the shipping gate; a note
recommending a rebuild nobody can run reads as a plan and is not one.

## B2B vs B2C

Four dimensions are identical for both and need no adjustment: time-to-signal, sound-off
legibility, promise-payoff continuity, and the real-variation gate. Attention decay and muted
autoplay do not care what is being sold.

Where they diverge:

- **B2B:** under the 95:5 rule (LinkedIn B2B Institute with Prof. John Dawes, Ehrenberg-Bass,
  2021), roughly 95% of B2B buyers are out-of-market at any moment, so a B2B opening mostly
  reaches future buyers. It qualifies by **role and situation** ("if you run payroll across
  three countries...") and aims at **memory, not an immediate click** - hard direct-response
  hook heuristics transfer poorly, and brand-legibility timing tilts earlier.
- **B2C:** DTC/B2C openings lean the other way - executional patterns, immediate offer framing,
  self-selection by problem or desire, and qualification judged against purchase intent now.

On LinkedIn specifically, autoplay is muted and a "view" is a weak 2-second/50%-on-screen
signal, so treat platform view counts as inflated relative to attention.

State the scoring mode on the scorecard; a batch scored in the wrong mode ranks the
wrong winner.

## Measuring Whether This Worked

The outcome measure is **rank agreement, not absolute accuracy**. After the batch runs, compare
the predicted rank order against the measured hook-rate rank order for the same openings on the
same platform and placement.

- **Validate the denominator first, every time.** Hook rate is `3-second video plays ÷
impressions` on Meta and `2-second views ÷ impressions` on TikTok; other dashboards construct
  it differently. See [references/platform-notes.md](references/platform-notes.md) for the full
  per-platform list.
- **Never compare across platforms or across a counting-change date.** A hook rate from one
  platform is not comparable to another's, and YouTube's view-counting changes of 31 March 2025
  and 24 August 2026 mean the numbers before and after are not the same metric either.
- **Pass threshold**: over a rolling window of 5 scored batches, the top-ranked opening lands in
  the top half of the measured ranking at least 3 times. That is a deliberately modest bar - it
  is what a useful shortlisting device clears and a coin flip doesn't.
- **Below threshold**: the generic rubric is miscalibrated for this account. Stop trusting it:
  re-derive the dimension weighting from the account's own past winners - which dimensions did
  the openings that actually won share? - and record the re-weighting in memory if available.
- **Shipping gate**: never ship a batch with fewer than 3 openings that clear all four gates
  _and_ differ on the concept axis. With roughly 5% of creatives winning (Motion 2026), volume
  is what produces winners; a one-opening "batch" is a bet, not a test.

## Reference

- Read [references/scoring-rubric.md](references/scoring-rubric.md) before banding - full
  dimension definitions, strong/adequate/weak anchors, supporting evidence, ambiguous-case
  rules.
- Read [references/hook-patterns.md](references/hook-patterns.md) when naming what a candidate
  is doing or diagnosing why it fails - sourced hook taxonomies (as vocabulary, never as a
  scoring axis) and the anti-pattern list.
- Read [references/platform-notes.md](references/platform-notes.md) when setting the hook
  window, validating a hook-rate definition, or calibrating - per-platform windows,
  view-counting rules, denominators, and counting-change dates.
- Read [references/examples.md](references/examples.md) when writing the scorecard - the
  field-by-field shape, a worked B2C batch, a worked B2B contrast, a negative example of the
  analysis done wrong, and the common-failure-modes table.
- See `mbfinotti/advertising-skills@ad-creative-test-plan` to design the test the shortlist feeds.
- See `mbfinotti/advertising-skills@ad-copy-variants` for static copy (this skill handles video openings only).
- See `mbfinotti/advertising-skills@paid-landing-page-audit` for post-click landing page issues beyond the ad itself.
