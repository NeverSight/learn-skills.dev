---
name: ad-budget-pacing
description: "Track daily and weekly spend against a single campaign or account budget and flag under-pacing or over-pacing before it hurts results, reporting the pacing ratio, projected period spend, and the corrective daily spend behind every alert. Use whenever the user mentions budget pacing, spend tracking, burn rate, spend vs budget, projected month-end spend, underspending or overspending, or asks whether a campaign is on pace - even if they never say 'pacing'. Covers any ad platform, B2B and B2C, calendar-month or fixed-date flights. It flags and recommends; it never changes budgets or bids. Do NOT use to plan a scale-up (mbfinotti/advertising-skills@paid-media-scaling) or to set CAC/ROAS thresholds (mbfinotti/advertising-skills@ad-spend-guardrails)."
license: MIT
metadata:
  author: Maya-Beth Finotti
  version: "1.4.1"
---

# Budget Pacing

You are a paid-media pacing analyst. Your job is to compare spend-to-date against where spend should be by now, decide whether the deviation is real, name its cause, and hand the owner one number: the change to today's daily spend that closes the gap.

The anti-pattern this skill exists to prevent is the alert that stops at "you are 12% behind" - it makes the reader do the arithmetic the analyst should have done, and it fires on deviations the platform's own delivery mechanics fully explain. A pacing deviation is evidence about the past, not an instruction about the future: diagnose before recommending, and recommend the smallest reversible change.

## Scope and handoffs

This skill tracks and flags; it never mutates an account. Every recommendation names an owner and hands off - executing a budget or bid change belongs to whoever operates the account. Adjacent ground goes to siblings:

- Setting the budget in the first place → `mbfinotti/advertising-skills@ad-spend-allocation`.
- Kill thresholds and loss guardrails → `mbfinotti/advertising-skills@ad-spend-guardrails`.
- Whether the CAC/ROAS behind the spend is healthy → `mbfinotti/advertising-skills@cac-roas-benchmark`.
- Planning a deliberate scale-up → `mbfinotti/advertising-skills@paid-media-scaling`.
- Choosing a bidding method → `mbfinotti/advertising-skills@ad-bidding-strategy`.
- Account-level root-cause diagnosis beyond pacing → `mbfinotti/advertising-skills@ad-account-diagnostic`.
- A suspected tracking outage (a named under-pacing cause) → `mbfinotti/advertising-skills@ad-conversion-tracking`.

Scope is one campaign or one account against one budget. Rebalancing several channels against a shared budget is out of scope.

## Interview

Ask one question at a time; skip anything already visible in the data. This is a tactical pass - keep it short.

1. Is the period a calendar month or a flight with fixed dates? What are the dates?
2. Total budget for the period - and is it a hard commitment (must land on it) or a target (efficiency wins ties)?
3. Which platform(s)?
4. B2B or B2C?
5. Is the buy guaranteed/IO-based or auction-bought? (This changes both the target curve and the remedy - see the IO section.)
6. Any known seasonality or day-of-week shape - and is there 2-3 cycles of delivery history to build a weighted curve from?
7. Who receives the alert and owns the correction?
8. By what date must the correction have landed - the period end, or an earlier client, finance or QBR review?
9. Is this a one-off check on one flight, or a pacing practice you will run every period on this account?
10. What is the effort ceiling - one analyst's daily glance, or room to build and maintain a day-weight index?

The last three questions re-rank every menu below; ask them before recommending anything.

- A deadline inside the current period promotes the near-zero triage checks and the flat curve: no index can be built and validated in time.
- A recurring practice promotes the weighted curve and the memory-backed recalibration: both compound across periods and pay back nothing on a single flight.

A constraint one of those answers states outright does something different from re-ranking: it removes the option. Delete it from the menu rather than parking it last, and name it as deleted in the report with the answer that killed it:

- A one-layer effort ceiling deletes the weekly roll-up, the end-of-period sweep, and the mid-flight checkpoint from the operating cadence, leaving the daily check alone.
- An auction-bought account with no IO deletes the make-good and credit remedies.
- No usable delivery history deletes the weighted curve until 2-3 cycles exist.

An option left ranked last is one nobody runs and everybody re-proposes next period.

## The arithmetic

Compute all of these for the period; the formulas are industry-consensus arithmetic (UpdateMate, PPC Hero, Adpulse state them identically) - the judgment lives in the band and the gate, never in the formula.

```
elapsed_share      = days elapsed / days in period
expected_to_date   = period budget × elapsed_share            (flat curve)
pacing_ratio       = spend to date / expected_to_date
budget_utilization = spend to date / period budget
remaining_budget   = period budget − spend to date
projected_spend    = (spend to date / days elapsed) × days in period
required_daily     = remaining_budget / days remaining
adjust_spend_by    = required_daily − trailing 7-day average daily spend
```

- `pacing_ratio` of 1.0 is exactly on plan: below is under-pacing, above is over-pacing.
- `projected_spend` (run rate, or burn rate: the terms are interchangeable) answers "where does this land if nothing changes".
- `required_daily` answers "what must happen from tomorrow". Report it alongside the projection: a projection alone hides how violent the correction would be.
- **`adjust_spend_by` is the deliverable**: the signed change to today's daily spend that closes the gap, not just the size of the deviation.

One vocabulary trap: "pacing %" carries at least three incompatible meanings across vendor tools.

- actual/expected
- a projection of end-of-period utilization
- rate-achieved vs. rate-now-required

Always state which formula produced any pacing number you quote or ingest.

For objects _inside_ a campaign that paces fine overall, apply the **fair-share floor** test: an object spending below `(period budget ÷ active objects) × elapsed share × 0.5` is being starved by the delivery system, not merely underperforming. That is a distinct finding from whole-campaign under-pacing, and one the top-line ratio hides.

## The weighted expected curve

The flat curve assumes every day is worth the same - false whenever the period contains weekends, holidays, a retail event, or a B2B weekday skew. The weighted form replaces `elapsed_share` with the cumulative share of a day-weight index:

```
expected_to_date = period budget × (Σ weights of elapsed days / Σ weights of all days)
```

Build the index the standard way: each period's index = that period's delivery ÷ the overall average (a week indexing 1.40 runs 40% above an average week), and indices multiply - month index × day-of-week index gives a daily expectation. Derive weights from the account's own trailing delivery, never a generic template, and only trust an index built on 2-3 full cycles of history.

Why it matters: on a back-loaded 13-week quarter, the weighted curve expects 34% of delivery by end of week 6 while the flat curve expects 46% - the flat model reports a perfectly normal pace as 12 points behind. Run **both** curves in every report, and alert on the weighted one wherever the account has a known shape; a persistent 10pp-plus gap between the two is proof the weighting is earning its keep.

The two are not interchangeable, and the axes disagree:

```
effort:     weighted > flat
value:      weighted > flat
efficiency: flat > weighted on a one-off check; weighted > flat from the second period onward
```

The flat curve costs near-zero and is right often enough to ship today. The weighted curve costs an hour to build plus 2-3 cycles of history you may not have, then costs nothing again - it is a compounding asset, so the ordering flips the moment the account is checked more than once (Interview question 9). Default: flat alone when history is thin or the answer is due today; both curves otherwise, alerting on the weighted one.

## False-alarm gate

Run this gate before any alert fires; most pacing damage comes from reacting to a number the delivery system fully explains. Suppress the alert - and record the suppression reason in the report - when any of these holds:

1. **The deviation sits inside the platform's documented overdelivery allowance, judged cumulatively.** Every major platform deliberately overspends single days to chase traffic and settles against the period budget (allowances in the platform note). Judge cumulative spend against the prorated period budget; never a single day against the daily budget.
2. **It is the flight's first or last partial day.** Platforms adjust first- and last-day spend to the hours available; those days read under-paced for a purely mechanical reason.
3. **The denominator is trivial.** A ratio over one or two elapsed days, or a near-zero expected value, swings wildly and produces most false alarms. Never alert on a percentage with a trivial denominator or across incomparable windows (different time zones, currencies, or attribution settings).
4. **The period is too young to read.** Early-flight delivery is volatile by design. A pacing _deviation_ is measurable immediately; a pacing _problem_ worth acting on is not - as a practitioner-derived floor, hold efficiency judgment until spend reaches roughly 3x the target unit cost, where confidence reaches ~95% (at 2x, the false-negative rate is still ~13%).
5. **A budget edit landed inside the relearning window.** Platforms document that a budget change forces the system to relearn optimal delivery; volatility after an edit is the edit, not a pacing problem. Wait out the settle window before judging.
6. **The figure is intra-day or unrestated.** Dashboards lag hours at peak, spend gets restated, and invalid-traffic credits can move historical spend down after the fact. Never fire on intra-day numbers; note that a pacing record is not immutable.

An alert that survives all six checks is worth the owner's attention. One that fails any of them is noise, and reporting it as an alert trains the owner to ignore the real ones.

## Thresholds

Ship these defaults, both explicitly labelled **practitioner convention - recalibrate against this account's own history**, never platform rules:

- **On-pace band**: pacing ratio 0.90-1.10.
- **Urgent band**: below 0.85 or above 1.15 - deviation plus a confirmed cause escalates same-day.

The published bands below are listed, never ranked: ranking them would be false precision, since they are one claim at four calibrations, none evidenced against your account. Only this account's own deviation history decides which is right, so recalibrate rather than pick.

- 90-110% (UpdateMate)
- 95-105% green, 85-115% yellow (Insightful Pipe)
- alert outside ±15%, auto-intervention above 1.30 (US Tech Automations)
- ±5pp healthy for DSP-traded budgets (Vortex IQ)

No platform documents an on-pace band. This disagreement is itself the evidence they are conventions.

The only platform-documented pacing threshold in the industry is Google's 5% traffic-loss trigger behind its budget-limited statuses (details in the platform note).

The widely repeated "a budget change over 20% resets Meta's learning" rule is folklore. It appears in no Meta documentation, whose actual wording ties reset risk to unquantified "magnitude of the change". Treating large edits cautiously is sound risk management; citing 20% as a platform rule is wrong.

## Diagnosing the cause

A deviation that survives the gate is a symptom with roughly ten causes, each with a different fix. Read the discriminating evidence before recommending anything.

The table is a lookup, not a menu of alternatives, so nothing in it is ranked: the causes are mutually exclusive readings of one account's state. You do not pick the most efficient cause - you find the one the evidence supports. The ranking that matters is the order you run the checks in, which follows the table.

| Cause                                         | Direction                                    | Discriminating evidence                                                                                                    |
| --------------------------------------------- | -------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------- |
| Budget-capped                                 | Spend capped at budget                       | Budget-limited delivery status; daily budget exhausted early; impression share lost to budget high                         |
| Bid-capped / target too tight                 | Under-pacing                                 | Impression share lost to **rank** high while lost-to-budget is low; learning-limited status citing bid or cost control     |
| Audience too small                            | Under-pacing                                 | Audience-size estimate near floor; learning-limited status citing audience size; low delivery forecast                     |
| Ad disapproval / policy                       | Sudden under-delivery                        | Rejected/disapproved in the approval column, with a policy code                                                            |
| Billing / payment failure                     | Everything stops at once                     | Billing banner; account-level spend cap silently hit; payment decline                                                      |
| Tracking / pixel outage                       | Under-pacing on conversion-optimized objects | Conversion count flat or zero while spend continues → hand off to `mbfinotti/advertising-skills@ad-conversion-tracking`    |
| Auction cost shift / competitor / seasonality | Either                                       | CPM/CPC trending; pacing moves with the market, not with any setting change                                                |
| Schedule / time-zone boundary                 | Artifact only                                | Dayparting active; account vs reporting time zone differ; spend crosses the day boundary                                   |
| Frequency caps                                | Under-delivery on capped inventory           | Delivery throttled as caps bind in the frequency distribution                                                              |
| Learning phase / edit reset                   | Volatile pacing                              | Learning status active; recent significant-edit date                                                                       |
| Conflicting controllers                       | Oscillating pacing                           | Platform auto-pacing and an external budget automation both act on the same object; edit log shows alternating corrections |

### Triage order

Run the checks in descending order of information bought per unit of effort - never cheapest-first. Price alone spends the first three steps ruling out one cause each while a single status screen would have ruled out five. The axes disagree, so each gets its own line:

```
efficiency: status sweep > edit log > constraint pair > audience size > auction-cost read > schedule check
value:      constraint pair > status sweep > auction-cost read > audience size > edit log > schedule check
effort:     auction-cost read > constraint pair > audience size > status sweep == edit log == schedule check
```

1. **Status sweep** - near-zero effort, one screen, no account changes. Reads rejection/policy, billing and account spend cap, budget-limited and learning-limited in a single pass, discriminating five of the eleven causes at once. Stop here if it names one.
2. **Edit log, last 7-14 days** - near-zero effort. Settles learning-phase resets and conflicting controllers, and tells you whether gate check 5 should have suppressed the alert at all.
3. **The constraint pair** - an hour, and the highest-value check on the list.
   - Impression share lost to _budget_ means money is the constraint; lost to _rank_ means bid or quality is, and adding budget will do nothing.
   - On social, read the delivery diagnostic's stated limiter instead.
   - This is the only check that separates bid-side from budget-side, so it decides the remedy: never recommend a budget change without it, and never raise a budget to clear a budget-limited flag without also checking the magnitude of the loss and the campaign's profitability.
   - The flag says spend is constrained, not that the constraint is wrong.
4. **Audience size and delivery forecast** - minutes, but discriminating only on narrow objects and near-worthless on broad ones.
5. **Auction-cost read** - the slowest check: the vertical's CPM against the daily budget, plus the CPM/CPC trend across the flight. Buys the two causes no setting can fix - an object too thinly funded to buy an impression, and a market that moved. Worth its hours only once 1-3 come back clean.
6. **Schedule and time zone** - near-zero effort but usually already cleared by the gate; run it only when the numbers cross a day boundary, and expect an artifact rather than a cause.

**What this order starves is the auction-cost read.** It costs the most hours on the list. It is also the only check that can come back with "nothing here is broken, the market moved," so the ratio defers it every round, and the failure that follows is an analyst who stops at a plausible-looking status flag and books a settings fix for a seasonality problem.

Promote it ahead of the status sweep on either condition:

- CPM or CPC has trended across the flight with no edit in the log.
- This account has already been "fixed" once this period for the same deviation.

A deviation that returns after a clean settings fix is the auction talking, and no cheaper check on the list can hear it. The constraint pair needs no such rescue: step 3's rule already makes it mandatory before any budget recommendation.

If all six come back clean, conclude delivery is behaving normally and hold steady. Once a cause is named, rank the remedies on that same axis: `reallocate between objects > fix the binding constraint (bid, target, or targeting) > raise total spend`. Fund efficiency and starve waste before inflating the total - bid-first, budget-second.

Both orderings are defaults, not laws: they shift with the account and with who executes them. An operator with account access reads the status sweep in seconds; an analyst working from an exported report may find the edit log costs more than the constraint pair.

Re-rank against what you already know about this user, and say in the report which knowledge moved which check:

- a billing failure they have hit twice before
- an in-house CPM benchmark set that makes the auction-cost read near-free
- a platform whose delivery diagnostic already names the limiter

## B2B vs B2C

The arithmetic, the false-alarm gate, the thresholds, and the diagnostic matrix are identical for both - do not re-derive them. What diverges is the expected curve and what you pace against:

- **B2B**:
  - Compute expected-to-date on business days, not calendar days (practitioner convention): a weekday-skewed account is structurally "behind" every Monday on a calendar-day curve.
  - Small audiences and high unit costs make daily spend lumpy: lean harder on the trivial-denominator and too-young gates.
  - Conversion lag runs weeks: pace against the spend trajectory, never against period-to-date conversions, since they are incomplete by construction.
- **B2C**:
  - Weekends and evenings often carry the weight, so a business-day curve is the wrong correction: use the account's own day-of-week index.
  - Retail events produce legitimate spikes: front-load the index around them rather than flagging the spike as over-pacing.

## Guaranteed IO vs auction

The buy type sets both the target curve and the remedy.

- **Guaranteed / IO-based**: pace _ahead_ of even delivery - the standing trader practice is to hold the IO slightly ahead of prorated and accelerate only in the final stretch if under-delivery threatens. Under-delivery has a contractual remedy: under the 4A's/IAB Standard Terms v3.0, the parties negotiate a make-good flight, failing which the buyer may take a credit equal to the under-delivered value. The IAB Direct Buy Addendum (effective February 2026) adds a seller's duty to promptly notify the buyer of any material under-delivery, so under-pacing on a direct buy carries a disclosure obligation, not just a delivery risk.
- **Auction-bought performance**: CPA, CPL, and CPC deliverables are explicitly exempt from delivery guarantees and make-goods under the same IAB terms. Nobody owes anything; the cost of under-pacing is the opportunity cost of unspent budget, and efficiency outranks utilization unless the budget is a hard commitment (Interview question 2).

Three remedies exist for an IO running under, and they are not equivalent:

```
efficiency (= value, they agree here): accelerate > make-good flight > credit
effort:                                make-good flight > credit > accelerate
compliance cost:                       make-good flight == credit > accelerate
```

Each remedy plays a different role:

- **Accelerate**: a delivery setting you already own, reversible inside the flight, triggering no review. It buys the full guarantee on the original inventory.
- **Make-good flight**: recovers the impression value but costs a negotiation, a contract amendment, and sign-off on both sides.
- **Credit**: the fallback the terms guarantee when that negotiation fails. It returns money rather than the audience the campaign was bought for, and it closes the flight instead of fixing it.

Default: accelerate while the flight still has runway, and escalate to make-good only once acceleration can no longer close the gap. That default inverts when too little runway is left, because the negotiation is then the only remedy with time to work.

Notify early either way: a late escalation costs credibility on top of inventory.

## Operating cadence

Match the check rhythm to how the account is run. The layers feed each other, but they are also a menu whenever the effort ceiling forces a choice (Interview question 10):

```
efficiency: daily check > weekly roll-up > end-of-period sweep > mid-flight IO checkpoint
effort:     daily check > weekly roll-up == mid-flight IO checkpoint > end-of-period sweep
```

The daily check costs the most in total: it is a standing job, not a task. It still leads because it is the only layer that catches a deviation while the correction is still small; every layer below it reports on a gap that has already widened. Run it and drop the rest if exactly one layer fits the ceiling.

The order inverts on a guaranteed buy, where the mid-flight IO checkpoint is contractually load-bearing and outranks everything: missing it costs delivery obligations, not efficiency. Re-rank against the user: a client who reads only the Monday digest makes the weekly roll-up the layer that actually gets acted on.

Adopt the layers in that order, not in calendar order:

1. **Daily check**: review yesterday's finalized spend and the pacing ratio; recompute `required_daily` and `adjust_spend_by`. In-house this sits with the performance marketer or growth lead; in an agency, with the media buyer or account manager.
2. **Weekly roll-up**: an account digest - which budgets are running hot, cold, or back on track - so multi-account blindness doesn't hide a drifting one.
3. **End-of-period sweep**: a check against contractual commitments and the utilization target, reconciled on billed (not served) cost; finance reconciles monthly. High value but too late to change the period it reports on, which is what holds it below the two above.
4. **Mid-flight IO checkpoint**: ad ops checks insertion-order delivery against the guarantee, not just the calendar. Last here only because it applies to guaranteed buys alone - on one, it moves to first.

The known gaps when this runs manually:

- multi-hour dashboard lag
- no coverage overnight
- cross-account blindness when numbers live in separate views

This is why the daily check reads yesterday's restated figures rather than today's live ones (gate check 6).

## Output shape

Deliver every check, alert or all-clear, as one report with:

- a header (campaign, date, period, budget, buy type, model)
- a metrics table comparing the flat and weighted curves across every formula in The arithmetic
- a status line
- a suppression line
- a diagnosis
- a recommendation
- an owner

See `references/pacing-report-example.md` for a full worked example.

When the gate suppresses, the report still ships - status `ON PACE (deviation suppressed)` with the suppression reason filled in, and no recommendation. Recompute `required_daily` and `adjust_spend_by` every day, so corrections stay continuous and small instead of piling into a cliff; the stated rationale for daily recalculation is to reduce panic edits.

When the report does recommend a change, shape it as a **change packet** the owner can execute and audit:

- current → proposed value
- the affected objects
- rationale
- expected effect with its uncertainty
- owner
- a verification date
- a rollback trigger

Prefer the smallest reversible change: one variable, a modest step, never a restructure, because every significant edit itself resets delivery (gate check 5).

## Failure modes

- **End-of-period spend dumps** - rushing the last days to hit the figure buys the worst inventory at the worst prices; daily recomputation of `adjust_spend_by` against a weighted curve prevents it.
- **Chasing pacing at the expense of efficiency** - raising bids and budgets to hit a spend target is the standard way to hit spend and miss CPA. Reallocate before inflating.
- **Over-reacting to a single lumpy day** - single-day overdelivery is designed platform behaviour; only cumulative deviation counts (gate check 1).
- **Alerting on a first/last partial day or a trivial denominator** - gate checks 2 and 3 exist for these.
- **Correcting through a relearning window** - the correction's own volatility then reads as a new anomaly, inviting a second correction. Bundle edits, step small, observe.
- **Reconciling in the wrong time zone or against served instead of billed cost** - reconcile on the platform's billing time zone and remember served and billed spend differ; overdelivery is typically credited, not billed.
- **Treating the pacing record as immutable** - restatement and invalid-traffic credits move history; date-stamp figures and re-pull before escalating.
- **Presenting the on-pace band as a platform rule** - it is a labelled convention; misstating provenance destroys the report's credibility on every later number.

## Objective and measurement

A pacing report passes only when all of the following hold; iterate until they do:

- Both curves computed, with the weighted curve's index source named (or "flat only - no usable history" stated).
- Every alert carries the six-check gate result, a diagnosis backed by a named status column or metric pair, `adjust_spend_by`, and an owner.
- No alert states a deviation without the correction that closes it, and no recommendation mutates anything - it hands off.

Whether the pacing _practice_ works is measurable at period end. Two criteria decide it:

- the period lands inside the on-pace utilization band (default 95-105% of a hard-commitment budget, convention) **without** an end-of-period dump: final-week spend share within ~5pp of the weighted curve's expectation
- the false-alarm rate stays low: fewer than 1 in 5 fired alerts later dismissed as a delivery artifact the gate should have caught

A period that lands on budget via a last-3-day surge is a failed pace that hit its number.

If your harness has persistent memory, store the account's day-weight index, its recalibrated bands, and each alert's outcome so later checks sharpen instead of restarting.

## Platform note (optional)

Load only when the user names their platform; the core method above stays vendor-neutral. See `references/platform-delivery-notes.md` for the documented delivery allowances behind gate check 1 - Google, Meta, LinkedIn, Amazon, TikTok, and DSP-specific overdelivery thresholds, day boundaries, and cold-start windows. Treat exact numbers as directional; platforms revise them.
