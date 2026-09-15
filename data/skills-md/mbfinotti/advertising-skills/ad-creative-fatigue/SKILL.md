---
name: ad-creative-fatigue
description: "Decide whether a running ad creative is genuinely wearing out, or whether a confounder - budget change, learning-phase reset, audience saturation, auction CPM inflation, seasonality, tracking breakage - explains the decline, and return a verdict with confidence plus the highest-return remedy per unit of effort. Use whenever the user mentions creative or ad fatigue, wear-out, climbing frequency, dropping CTR, a rising CPA on an older ad, when to refresh creative, or whether to kill an ad - even if they never say 'fatigue'. Covers B2B and B2C across search, social, video, and native. Ends at the verdict: replacement creative belongs to mbfinotti/advertising-skills@ad-copy-variants and mbfinotti/advertising-skills@ugc-ad-scripts."
license: MIT
metadata:
  author: Maya-Beth Finotti
  version: "1.1.4"
---

# Creative Fatigue

Read a creative's performance-over-time data and decide whether it is genuinely wearing out, how confident that call is, and what to do about it. The core discipline is refusal: many things can cause a declining metric, and creative wear-out is only one of them. Most refresh decisions are made too early, off one metric, against no baseline.

This skill runs a differential diagnosis in a fixed order, confounder screen before the fatigue call, never after:

1. Baseline
2. Confounder screen
3. Decay measurement
4. Confidence gate
5. Verdict

Two further tensions stay live throughout:

- Fatigue is often hook fatigue rather than whole-ad fatigue (Ben Heath).
- Some ads improve with repeated exposure, the "wear-in" effect Les Binet describes in brand advertising, though Meta's 2023 research found no wear-in for direct-response objectives - wear-in is a real verdict only where the objective is brand, not DR.

There are no universal thresholds here: every trigger is derived from the creative's own trailing baseline and the account's own history. Named practitioner numbers appear only as attributed starting reference points.

This skill ends at the verdict and the recommended action.

- Producing the replacement asset belongs to `mbfinotti/advertising-skills@ad-copy-variants`, `mbfinotti/advertising-skills@ugc-ad-scripts`, and `mbfinotti/advertising-skills@ad-creative-brief`.
- Sample-sizing a pre-launch test belongs to `mbfinotti/advertising-skills@ad-creative-test-plan`.
- Scoring a video opening before launch belongs to `mbfinotti/advertising-skills@ad-hook-analyzer` (here, hook rate is only read as a decay signal on ads already running).
- When the confounder screen shows the problem is not the creative at all (structure, targeting, tracking), hand off to `mbfinotti/advertising-skills@ad-account-diagnostic`.
- Retargeting-sequence and frequency-cap architecture design is `mbfinotti/advertising-skills@retargeting-funnel`.
- Scaling and pacing decisions after a win are `mbfinotti/advertising-skills@paid-media-scaling` and `mbfinotti/advertising-skills@ad-budget-pacing`.

## Interview

Ask before diagnosing anything. One question per message; offer multiple-choice answers where possible; skip anything already answered or visible in supplied data.

- Which platform(s) is the creative running on? (Meta / Google Ads - search, Performance Max, or YouTube / LinkedIn / TikTok / other)
- B2B or B2C/ecommerce?
- Funnel stage: cold prospecting or retargeting/warm? (Tolerated exposure differs sharply between the two.)
- What can you actually export, and at what granularity: per-creative per-day, per-creative weekly aggregate, or only ad-set/campaign level? Per-creative per-day is the working assumption; anything coarser weakens every step downstream.
- Daily spend and conversion volume on the creative in question? (Decides whether the confidence gate can clear at all.)
- Rough audience size for the ad set, and is the audience list-based/ABM or broad?
- How many creatives are live in the same ad set? (Sibling mix changes what "losing spend share" means.)
- When was the ad, or its parent ad set/campaign, last edited - creative, budget, bid, audience, optimization event? Exact date matters.
- Did budget change during the window under suspicion? By how much?
- By what date does the result have to land? (A hard deadline promotes the Action Ladder's same-day rungs - rotation, budget shift, frequency cap - and demotes iteration and new concepts.)
- Do you want a one-off win on this creative, or a compounding asset? (A compounding mandate promotes iteration and new concepts even where a configuration fix would hold this week.)
- What is your effort ceiling: creative production capacity and lead time, in-house editing hours, whose sign-off list work needs, and how reversible the change has to be? (A refresh recommendation nobody can execute is worthless - this answer deletes rungs from the Action Ladder rather than reordering them.)
- What is the target CPA or ROAS the creative is judged against?

## Workflow

1. Run the Interview; collect every answer before touching the data.
2. Fix the unit of analysis. Analyse at creative and concept level, never at campaign averages: forty rows for forty variants of five concepts hides the real pattern, and one fatigued ad dragging an ad-set average looks like a campaign-wide problem. Where the platform rotates variants automatically (Advantage+-style delivery, dynamic creative), read the asset-level breakdown - automated rotation masks individual asset decay. Conversely, a creative silently losing budget share with no manual change is itself a decay signal.
3. Build the creative's own baseline. Never compare single days.

   Sourced methods to offer as starting defaults, picked per the user's data granularity and overridden by their own history - the two are not ranked against each other, since both cost the same single export and only granularity decides:

   - 3-day moving average against the creative's own trailing 14-day baseline (AdSights).
   - Rolling 7-day window against a 30-day baseline (Segwise).

   Exclude known outages and match the comparison window's day-of-week composition to the baseline's. If your harness can read the export or run the calculation, compute it; otherwise emit the exact export steps and spreadsheet formulas (columns, moving-average ranges, delta formula `(current - baseline) / baseline`) for the user to run and report back.

4. Run the confounder screen, before any fatigue talk. Work through [references/confounders.md](references/confounders.md) and mark every confounder pass (ruled out) or fail (present):

   - budget/bid change
   - learning-phase reset
   - audience overlap/saturation
   - auction CPM inflation
   - seasonality and window composition
   - tracking breakage
   - attribution-window skew
   - placement/device mix shift
   - statistical noise
   - landing-page/offer change
   - sibling-mix shift

   Any fail that explains the decline ends the fatigue inquiry: the verdict is `confounded` (or `saturating` for the audience case) and the fix targets the actual cause. Structure/targeting/tracking root causes hand off to `mbfinotti/advertising-skills@ad-account-diagnostic`.

5. Measure decay against the baseline using [references/signal-reference.md](references/signal-reference.md). Apply the field's consensus decision rule: no single metric confirms fatigue - require at least two signals moving together across two or more consecutive periods (Segwise; AdSights). Weight leading signals (link CTR decay, hook-rate decay on video, falling first-time-impression ratio, silent budget-share loss) over lagging ones. Frequency is a lagging, confirming signal only - Meta's own analytics team notes reported frequency is measured at ad/ad-set level while fatigue happens at creative level, and is a period average, not the marginal effect of the next impression. Do not build the call on frequency.
6. Apply the Confidence Gate (below). If it fails, the verdict is `insufficient data` - state what extra spend or days would clear it and stop; refuse to recommend a refresh on noise.
7. Separate fatigue from saturation before finalising. The discriminating logic:

   - Fatigue: costs rise while conversion rate holds.
   - Saturation: both degrade, alongside a falling first-time-impression ratio and flattening reach.

   Where the user can run it, the definitive test is Meta's own:

   - A new creative restoring performance on the same audience proves fatigue.
   - Performance recovering only on a fresh audience proves saturation.

   Their fixes are opposite, new creative versus audience expansion, so the split matters.

8. Issue the verdict from the Verdict Ladder, then pick the remedy from the Action Ladder - top of its efficiency ordering first, re-ranked against the Interview's deadline, one-off-versus-compounding and effort-ceiling answers - and fill one Fatigue Verdict block per creative (shape below; worked versions in [references/examples.md](references/examples.md)).
9. Set the re-check date (one full comparison window after any action) and log the decision for the Measuring section's scorecard.
10. If your harness has persistent memory, memorize the account's baselines, per-creative verdicts, actions taken, and re-check dates, so the next run starts from history instead of re-deriving it.

## The Fatigue Verdict

Deliver one block per creative analysed:

```
FATIGUE VERDICT - <creative id/name>, <date>
platform      : <platform> | funnel stage: <cold prospecting | retargeting>
window        : <comparison window> vs baseline <baseline definition>
volume        : <spend> spent, <impressions> impressions, <conversions> conversions in window

signals
  <signal>    : <current> vs <baseline> (<+/-x%>)   [leading|lagging]
  <signal>    : <current> vs <baseline> (<+/-x%>)   [leading|lagging]
  ...

confounder screen
  budget/bid change        : pass | FAIL - <note>
  learning-phase reset     : pass | FAIL - <note>
  audience saturation      : pass | FAIL - <note>
  auction CPM inflation    : pass | FAIL - <note>
  seasonality/window mix   : pass | FAIL - <note>
  tracking breakage        : pass | FAIL - <note>
  attribution-window skew  : pass | FAIL - <note>
  placement/device mix     : pass | FAIL - <note>
  statistical noise        : pass | FAIL - <note>
  landing page/offer change: pass | FAIL - <note>
  sibling-mix shift        : pass | FAIL - <note>

confidence    : high | medium | low - <one-line basis: gate math, signal count, window length>
verdict       : fatigued | saturating | confounded | insufficient data | healthy | wear-in
action        : <chosen action-ladder rung + who produces the asset, if any>
ruled out     : <every rung the account's stated constraints delete, each with the constraint that deleted it - or "none">
expected      : <what should recover, by roughly how much, based on which evidence>
re-check      : <date - one full comparison window after action>
```

## Confidence Gate

No verdict may be issued below the data floor, and the floor is the user's own math, not a copied constant:

- **Noise check.** For a rate signal (CTR, hook rate, CVR) the observed decline must exceed sampling noise. Approximate the baseline rate's noise band as `p ± 2 × sqrt(p × (1-p) / n)`, with `n` the impressions (or clicks, for CVR) in the comparison window. A "decline" still inside that band is noise, whatever it looks like on a chart.
- **Two-signal rule.** At least two signals, at least one of them leading, moving the same direction across two or more consecutive periods (Segwise; AdSights). One metric, one period, never clears the gate.
- **Conversion floor.** For CPA/ROAS-based claims, enough conversions in both baseline and comparison windows that the delta survives the same noise check on CVR. Low-conversion accounts (most B2B) should gate on leading engagement signals instead and say so in the verdict's confidence line.

When the gate is not met: report `insufficient data`, compute the additional days or spend needed (days ≈ what it takes for `n` to make the noise band narrower than the observed delta at current traffic), and refuse to recommend a refresh. Killing a creative on an underpowered read is the most expensive false positive this skill exists to prevent.

## Verdict Ladder

Each verdict maps to its own action - they never all collapse to "make new creative". These verdicts are deliberately not ranked against each other: the evidence picks exactly one, so an efficiency ordering over them would be false precision. The ranking happens one level down, inside the Action Ladder.

| Verdict             | Meaning                                                                                                                                                                  | Action                                                                                                                                                                                 |
| ------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `fatigued`          | Two-plus signals decayed vs own baseline, confounders ruled out, gate cleared                                                                                            | Action Ladder, highest return per unit of effort first - rung 1 unless the evidence rules it out                                                                                       |
| `saturating`        | The audience pool is depleting - falling first-time-impression ratio, flattening reach, CVR degrading with costs                                                         | Audience expansion, fresh seed, or exclusions - not new creative; Action Ladder rung 6, promoted to first under this verdict; see `mbfinotti/advertising-skills@ad-audience-targeting` |
| `confounded`        | A non-creative cause explains the decline                                                                                                                                | Fix the actual cause; hand structural/tracking causes to `mbfinotti/advertising-skills@ad-account-diagnostic`                                                                          |
| `insufficient data` | Confidence Gate not met                                                                                                                                                  | Report the gap, state days/spend needed, re-check then; no refresh                                                                                                                     |
| `healthy`           | Signals inside the noise band of the creative's own baseline                                                                                                             | Leave it alone; note next scheduled review                                                                                                                                             |
| `wear-in`           | Performance improving with exposure - plausible for brand objectives (Les Binet); Meta found no wear-in for direct response, so treat a DR "wear-in" read with suspicion | Leave it alone; do not rotate it on a frequency number                                                                                                                                 |

## Action Ladder

Ranked by return per unit of effort - what each rung buys, against what it costs you to ship it. Not by price: the cheapest rung and the one worth doing first are rarely the same rung, and "buys a week" is not the same purchase as "restores the ad".

- efficiency (the default order, and the numbering below): hook swap > rotate & rest > budget shift > iterate the winner > frequency cap > audience expansion > new concept > pause
- effort, lightest first: rotate == budget shift == pause > frequency cap > hook swap > audience expansion > iterate > new concept - the three-way tie is a real equality, not indecision: each is one console change, produces no asset, needs no sign-off, and is reversible the same day
- durability of what it buys: new concept > iterate > audience expansion > hook swap > frequency cap > rotate > budget shift > pause - a concept is the parent of every iteration run off it, so it outlives any single one of them
- compliance cost, heaviest first: audience expansion (customer-list and ABM uploads need a lawful-basis attestation and a data-processing review, and an uploaded list is not easily un-shared) > every other rung (near-zero - all are platform settings or new assets)

Default to rung 1 and take the highest-placed rung the evidence supports. Move one rung down the list when the rung above has already been tried and the decay resumed, or when the signal pattern rules it out - hook, hold rate and CVR decaying together means the whole ad is spent, not its opening.

**What the efficiency order starves.** New concept is high on value and high on effort, so a ratio buries it at rung 7 every round - and it is the only rung that fixes an exhausted concept, which no hook swap or iteration can touch. Promote it above everything else when iteration stops recovering performance across successive attempts on the same concept: that pattern says the concept is spent rather than its execution, and every cheaper rung above is then buying nothing. Audience expansion has the same value-and-effort shape but is not starved here, because the `saturating` verdict already promotes it to rung 1 by rule - its failure mode is the reverse, reaching for it under `fatigued`, where it wastes a good audience.

Every ordering above is a default, not a law: it shifts with the account's context and with who executes it. Re-rank against what you already know about this account, and against the Interview's deadline and mandate answers:

- An always-on challenger bench promotes rotation to first.
- An in-house editor who can ship a new opening the same day keeps the hook swap ahead of every configuration fix.
- A `saturating` verdict overrides the whole order: audience expansion becomes rung 1 and creative work is wasted effort.
- A hard deadline promotes the same-day rungs.
- A compounding mandate promotes iteration and new concepts.

The effort ceiling does something different: it **deletes** rungs from this account's ladder rather than demoting them.

- No production capacity, or a lead time longer than the deadline, deletes new concept and iterate.
- No editor deletes the hook swap.
- A locked or empty creative library deletes rotation.
- No lawful-basis sign-off deletes audience expansion.

Name each deleted rung and the constraint that deleted it on the verdict's `ruled out` line, then take the highest-ranked survivor. A rung merely parked at the bottom of the list is still on the list, and comes back later as scope nobody agreed to fund.

1. **Hook/thumbnail swap on the same body**
   - Effort: an hour or two of editing, no brief cycle.
   - Buys: the ad back on the same audience, for as long as the body holds.
   - Right when: hook rate or thumbstop decayed but hold rate and CVR held - the opening is tired, not the ad (Ben Heath's "ad fatigue is usually hook fatigue").
   - Caution: if negative-feedback rate is elevated, a hook swap on the same creative ID does not clear the algorithmic penalty; ship a new asset ID.
2. **Rotate from existing inventory and rest the creative**
   - Effort: near-zero, configuration only.
   - Buys: a window while the audience cycles, not a fix - the decay waits where you left it.
   - Right when: the account keeps an always-on challenger bench; worth nothing without one.
   - Note: reintroduce the rested creative after the pool has turned over, and promote a proven challenger meanwhile.
3. **Budget shift to a healthier creative**
   - Effort: near-zero, reversible the same day.
   - Buys: time and CPA protection while a replacement ramps.
   - Note: keep a still-profitable fatigued ad running; never pause a producer with nothing staged. Pairs with any other rung rather than competing with one.
4. **Iterate the winner**
   - Effort: days, plus a production brief and a test slot.
   - Buys: the largest durable payoff on the ladder - the same proven concept in a new execution (new hook, opening seconds, format, aspect ratio, or copy) running for weeks.
   - Evidence: practitioners report element-level iteration often recovers most of original performance without a full rebuild (Hawky's reported band is 60-80% - treat as their number, not a promise).
   - Reference: brief production via `mbfinotti/advertising-skills@ad-copy-variants`, `mbfinotti/advertising-skills@ugc-ad-scripts`, or `mbfinotti/advertising-skills@ad-creative-brief`.
5. **Frequency cap or exclusion**
   - Effort: configuration, plus agreement on who owns the cap.
   - Buys: relief on one over-exposed warm pool, and nothing at all on a cold prospecting decay.
   - Right when: exposure is concentrating on a warm pool that has seen it enough.
   - Reference: design of the cap architecture itself belongs to `mbfinotti/advertising-skills@retargeting-funnel`.
6. **Audience expansion or fresh seed**
   - Effort: configuration plus list work and, for customer-list or ABM uploads, a lawful-basis sign-off - days to a week, and hard to walk back once the list is uploaded.
   - Buys: a new pool, the only thing that moves a `saturating` verdict.
   - Caution: applying it to true fatigue wastes a good audience; under `saturating` it is rung 1.
7. **New concept**
   - Effort: weeks, full production and a test plan.
   - Buys: a fresh line of assets when the concept, not the execution, is exhausted - the lowest hit rate per attempt on the ladder, and the highest ceiling.
   - Reference frame: a commonly cited portfolio split is 70% proven / 20% tests / 10% experiments; treat it as an operator heuristic to adapt, not a rule.
   - Reference: test-plan the launch with `mbfinotti/advertising-skills@ad-creative-test-plan`.
8. **Pause**
   - Effort: near-zero and instantly reversible.
   - Buys: a stopped loss and nothing else - the creative's remaining contribution goes with it.
   - Caution: last resort, and only with a replacement live or the budget re-homed. Pausing does not reset platform learning; editing a live ad does.

## Per-Platform Notes

Pointers only - metric mechanics and platform quirks live in [references/signal-reference.md](references/signal-reference.md).

- **Meta**: native "Creative fatigue" and "Creative limited" delivery statuses exist but lag badly (reported to fire around a doubling of cost per result, per Meta docs as relayed by industry sources) - if they are firing, detection was already too slow. First-time impression ratio is native. Advantage+ shifts budget away from fatigued assets silently, masking the signal; read per-asset breakdowns. Any significant edit resets the learning phase.
- **Google Ads**: on RSAs, asset performance labels (Learning/Low/Good/Best) are the performance-based signal. Ad Strength is not - it measures diversity and completeness, and Optmyzr's analysis found "Average"-strength ads with the best CPA/CVR; never read Ad Strength as fatigue. Performance Max is opaque at combination level - work from the per-asset report. YouTube: view-rate decay and per-user frequency are the levers.
- **LinkedIn**: official guidance is to rotate the lowest-engagement ad every 1-2 weeks and keep 4-5 ads per campaign. Delivery mechanics tie exposure to creative count (AJ Wilcox's observed "7 in 48" pattern), so a small creative set throttles itself. Small B2B audiences accumulate frequency slowly but relentlessly against expensive CPMs.
- **TikTok**: fastest wear-out of the major platforms; TikTok's own guidance suggests roughly 7-day refresh cycles, framed around a consistently declining delivery trend. Hook rate moves first; daily new-user reach flags saturation directly; automated creative optimization masks per-asset decay - read asset breakdowns.

## B2B vs B2C

The method (own-baseline, confounder screen, two-signal rule, verdict ladder) is identical in both. What differs is data volume, exposure mechanics, and which signals carry the call.

**B2B:**

- Addressable audiences are small and sometimes platform-throttled, so frequency climbs structurally rather than as a decay symptom.
- Conversion volume is usually too low for the conversion floor; lean on leading engagement signals (link CTR, engagement-rate trend, CPL drift over 3-6 week windows) and say so in the confidence line.
- The long sales cycle means the conversion signal lags the creative signal by weeks. Never read a flat pipeline week as creative failure.
- ABM and list-based audiences saturate by design; expect the `saturating` verdict more often than `fatigued`.

**B2C/ecommerce:**

- Large pools and high conversion volume make the full statistical gate usable.
- Wear-out runs fastest on narrow retargeting segments.

**Both:** warm/retargeting audiences tolerate far higher exposure than cold. Ben Heath reports Meta results commonly holding at frequency 10+ on warm audiences versus a drop-off he sees around 2.0-2.5 on cold. Always split cold from warm before reading any exposure number.

## Measuring Whether This Worked

The skill's own KPI is decision quality, tracked on a rolling log of every verdict:

- **Refresh win rate**: share of fatigue-triggered replacements that beat the retired creative's pre-decline baseline (same audience, full comparison window) at the re-check date.
- **False-positive rate**: share of retired creatives that were, in retrospect, still healthy - the replacement did no better, or the "decay" reversed on its own in a holdout.

As a starting floor (this skill's practical target, not a researched constant), iterate until at least 60% of refreshes beat the retired creative and under 20% of retirements were false positives. Tighten both from the account's own history once a dozen decisions are logged.

- A low win rate with a clean gate usually means the diagnosis is right but production quality is the constraint.
- A high false-positive rate means the gate or the confounder screen is being skipped.

If refreshes stop recovering performance across several concepts at once, stop refreshing: that pattern is an offer, landing-page, or product problem no new creative will fix.

## Common Failure Modes

| Trap                                                     | Why it burns                                                                                                | Fix                                                                                                                                                       |
| -------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Calling fatigue from one metric, one bad day             | Noise and weekends mimic decay; retires healthy creatives                                                   | Two signals, two-plus periods, vs the creative's own baseline                                                                                             |
| Reading a learning-phase reset as decay                  | Any significant edit restarts volatile delivery for days                                                    | Check last-edit date first; wait a full window post-edit before judging                                                                                   |
| Treating a frequency number as causal                    | Frequency is lagging, ad-set-level, and an average - a creative at 3.0 can be spent, another at 5.0 healthy | Frequency confirms; link CTR, hook rate, and first-time-impression ratio lead                                                                             |
| Campaign averages hiding per-creative decay              | One fatigued ad drags the average; the rest get refreshed for nothing                                       | Per-creative, per-concept reporting; asset breakdowns under auto-rotation                                                                                 |
| Blaming creative for Q4/auction CPM inflation            | CPM up with CTR flat is the auction, not the ad                                                             | CPM is diagnostic only when paired with falling CTR                                                                                                       |
| Reading CVR collapse with healthy CTR as fatigue         | That pattern is landing page, offer, or tracking - no creative will fix it                                  | CTR healthy + CVR down → funnel check before creative check                                                                                               |
| Trailing-window "decay" from attribution lag             | Recent days always under-report conversions; every trailing window looks like decline                       | Compare windows of equal conversion-lag maturity                                                                                                          |
| Fixing saturation with new creative                      | Opposite remedies: fatigue wants creative, saturation wants audience                                        | Run the fatigue-vs-saturation split (step 7) before acting                                                                                                |
| Editing the live ad to "refresh" it                      | Edits reset learning and destroy the baseline mid-measurement                                               | Launch new ads alongside; pause, never edit, a measured creative                                                                                          |
| Treating Google Ad Strength as a fatigue signal          | It scores diversity/completeness, not performance                                                           | Use asset performance labels; ignore Ad Strength for this call                                                                                            |
| Hook-swapping a creative with elevated negative feedback | The algorithmic penalty rides the asset ID, not the hook                                                    | Ship the iteration as a new asset ID                                                                                                                      |
| Recommending refresh volume beyond production capacity   | An unexecutable plan defaults to letting everything decay                                                   | Delete every Action Ladder rung beyond the Interview's effort ceiling, name each on the verdict's `ruled out` line, then take the highest-ranked survivor |
| Retiring a producer with nothing staged                  | The ad set goes dark or re-enters learning on a gap                                                         | Stage the replacement, ramp it, then retire                                                                                                               |

## Reference

- `mbfinotti/advertising-skills@ad-copy-variants` - to produce replacement assets for a `fatigued` verdict
- `mbfinotti/advertising-skills@ugc-ad-scripts` - to produce replacement assets for a `fatigued` verdict
- `mbfinotti/advertising-skills@ad-creative-brief` - to produce replacement assets for a `fatigued` verdict
- `mbfinotti/advertising-skills@ad-creative-test-plan` - for pre-launch test design on replacement creatives
- `mbfinotti/advertising-skills@ad-account-diagnostic` - for structural/tracking root causes when the confounder screen fails
- `mbfinotti/advertising-skills@retargeting-funnel` - for frequency-cap architecture design under a `fatigued` verdict
