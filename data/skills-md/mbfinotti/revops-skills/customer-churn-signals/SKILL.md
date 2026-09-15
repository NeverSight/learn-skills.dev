---
name: customer-churn-signals
description: Assemble, define, validate, and rank leading indicators of customer churn from account activity, product usage, and support data into a ranked churn signal register - each signal carrying event, threshold, window, baseline, lift over base rate, lead time, and coverage. Use whenever the user mentions churn signals, churn indicators, leading indicators of churn, an early warning system for at-risk accounts, champion departure, seat utilisation drops, payment failure, or says "our health score misses churn" - even if they never say "signal". Covers B2B and B2C subscription. Do NOT use for combining signals into one composite score, weights, bands, or tiers - use mbfinotti/revops-skills@customer-health-score instead.
license: MIT
metadata:
  author: Maya-Beth Finotti
  version: "1.2.6"
---

# Churn Signals

Identify, operationally define, validate against actually-observed past churn, and rank the signals that precede churn in the user's own accounts. The organizing distinction is leading versus lagging:

- **Lagging** (reports what already happened): churn rate, lost MRR, a falling NPS.
- **Leading** (appears weeks before cancellation and leaves time to act): login decline, narrowing feature adoption, a champion going quiet.

Every candidate must pass a two-part actionability test before it is worth shipping:

1. It fires early enough that someone can still intervene.
2. Someone actually can intervene on it.

Late-firing events - failed payments, downgrade requests, procurement delays, renewal-date slippage - are confirmation tripwires that formalize a decision made weeks earlier. Class them as confirmatory, never as leading.

Lincoln Murphy's Success Milestones frame is the standing caution over the whole exercise: usage is not success. Track progress toward the customer's own outcome, because accounts can look busy right up to an "unexpected" churn.

This skill ends at a ranked, validated signal register; whoever assembles those signals into a composite score - weighting, score scales, red/yellow/green tiers - or the CSM playbooks, save offers, and renewal plays that act on them should use `mbfinotti/revops-skills@customer-health-score`. Pipeline stage design, pre-sale lead scoring, and the sales-to-CS handoff are also out of scope.

## Interview

Ask before proposing anything. One question per message; offer multiple-choice answers where possible; skip anything already answered.

- B2B, B2C/consumer subscription, or both books of business?
- How many churned accounts exist from the last 12-24 months? This decides which ranking method is even possible: backtest-and-lift works on small samples; WoE/IV and any regression need volume (see ranking reference).
- Which data sources are actually reachable, and at what granularity: product event stream, login logs, support ticket system, CRM activity (meetings, emails), billing records, survey scores? Per-account per-day, or only aggregates?
- Contract and renewal shape: monthly self-serve, annual, multi-year? Typical renewal cycle length?
- What intervention capacity exists - who acts on a flagged account, and how many flags per week can they absorb? A signal nobody can act on is not worth ranking.
- Does a health score already exist? If yes: validate its input signals against real churn first, or build the register fresh?
- By what date must the register be live? A date inside the next renewal cycle deletes every signal needing new instrumentation and every method below retention curves.
- A one-off win - save this quarter's renewals - or a compounding asset the team keeps recalibrating? "Compounding" promotes product telemetry and feature-adoption breadth to the front of the build order; "one-off" leaves the register CRM-derived.
- What is the effort ceiling: analyst hours available, engineering time you can actually requisition, and whether anyone will refit a model after ship? No engineering time deletes the product-telemetry categories; nobody to refit deletes logistic regression and Cox at any sample size.

Re-rank the candidate order against these three answers before proposing anything, and say out loud which answer moved which option - a ranking the user cannot trace back to their own constraints reads as arbitrary.

## Workflow

1. Run the Interview; collect every answer before proposing signals.
2. Build the candidate list from [references/signal-taxonomy.md](references/signal-taxonomy.md), working its categories in the efficiency order stated there - login recency first, survey movement last, product telemetry sixth unless the product already emits per-account events. Delete the categories the Interview ruled out instead of listing them for later. Mark confirmatory tripwires as such from the start.
3. Write the operational definition for every candidate: the event, the threshold, the observation window, the comparison baseline, and normalization for account size and seasonality. A signal missing any of the five is not testable; fix the definition or drop the candidate.
4. Pull the churned-account list and reconstruct each candidate's state at 30/60/90 days pre-churn (extend to 120-180 for enterprise motions). If you can query the data directly, compute it; otherwise emit the queries or spreadsheet steps for the user and work from their results.
5. Rank per [references/ranking-methods.md](references/ranking-methods.md): churn-rate lift over base rate, median lead time, and coverage for every candidate, divided by what that candidate costs to stand up. Run the methods in that file's stated order - backtest and lift first - and stop when the register clears; delete the methods the Interview's sample-size and maintenance answers ruled out rather than keeping them as a stretch goal. Lead time is a first-class ranked attribute alongside strength - a strong signal that fires days before cancellation loses to a weaker one that fires 90 days out.
6. Run the survivorship check: for the accounts that churned, was each surviving candidate actually firing 60-90 days before? A signal still green pre-churn on most churned accounts is a blind spot, not a predictor.
7. Fill the register (shape below), verdict every signal ship/watch/reject against the Pass Threshold, and iterate definitions, thresholds, and windows until the register-level bar clears.
8. Validate the register with the user section by section, hand the shipped signals to `mbfinotti/revops-skills@customer-health-score` for composite scoring, and book a re-backtest for when the next quarter of churn outcomes exists.
9. If your harness has persistent memory, memorize the approved register - signals, definitions, lift, lead times, coverage, verdicts, re-backtest date - so later recalibration runs start from it instead of re-interviewing.

## The Signal Register

Deliver every engagement as this artifact. Worked versions live in [references/examples.md](references/examples.md).

```
CHURN SIGNAL REGISTER - <company/book>, <date>, v<n>
Base rate : <B>% of accounts churn per <window>; churned sample = <N> (<period>)
Method    : backtest + lift [+ retention curves | + WoE/IV] - in that order, stopping when
            the register cleared; name any method deleted and why (sample, no refit, deadline)
Rows      : ordered by value per unit of instrumentation effort

signal      : <name>
  category  : usage | adoption | seats | relationship | support | billing | survey | crm | context
  source    : <system category, e.g. product event stream>
  definition: event + threshold + observation window + baseline + normalization
  window    : <observation window>
  baseline  : <what normal is - account's own history and/or segment peers>
  lift      : of accounts showing this, <N>% churned within <window> vs base rate <B>% (<x.x>x)
  lead time : median days between first fire and churn
  coverage  : % of past churned accounts that fired this signal
  effort    : near-zero | an hour | a week | a quarter | a standing job - to instrument and keep alive
  confidence: evidence note - sample size, IV if computed, caveats
  verdict   : ship | watch | reject (confirmatory-flagged where applicable)

Register-level : % of past churns the shipped set would have caught at minimum lead time
Handoff        : shipped signals -> mbfinotti/revops-skills@customer-health-score
```

## Pass Threshold

A signal earns "ship" only when all three clear. Treat the numbers as this skill's practical floor, not researched constants - tighten them from the user's own data when the sample allows:

- **Lift**: accounts showing the signal churn at **at least 2x the base rate** within the observation window. A thinner edge will not survive live noise.
- **Lead time**: median **at least 30 days** before churn - **90 for enterprise/annual-contract motions**, where intervention needs procurement-cycle room. Confirmatory tripwires are exempt but must carry the confirmatory flag.
- **Coverage**: fired for **at least 25% of past churned accounts** - a signal that catches almost none of the real churns is trivia however strong its lift.

Register-level: the shipped set combined must have fired on **at least 70% of past churned accounts** at the minimum lead time or earlier. Iterate - adjust thresholds and windows, add categories, split segments - until it clears; refuse to ship a register that would have missed most known churns.

## B2B vs B2C

- **B2B-only**: champion and executive-sponsor departure, and multi-stakeholder buying-committee dynamics - there is no internal committee to lose a member from in B2C. B2B contract terms also dampen and delay the visible churn event: an annual contract keeps a dissatisfied customer paying until expiry, so the behavioral signals run far ahead of the commercial one, which is exactly why leading signals matter more there, not less.
- **Shared, identical method**: usage/login decline, feature-adoption breadth, and support sentiment are tracked in both B2B and B2C. Only the unit changes: the account and its committee in B2B, the individual subscriber in B2C.
- **B2C-specific**: payment failure is a proportionally larger churn driver; cancellation is a one-person, one-tap decision, so lead times compress and intervention windows shrink; and "churn by indifference" - a forgotten low-cost subscription - has no B2B analogue.

## Common Failure Modes

| Trap                                           | Why it burns                                                                                                                                                                                                                                                                      | Fix                                                                                                                                                                                                                    |
| ---------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Lagging metric shipped as leading              | Churn rate, lost MRR, NPS drops report the past                                                                                                                                                                                                                                   | Classify every signal by measured lead time; tripwires get the confirmatory flag                                                                                                                                       |
| Correlation without prediction                 | Metrics move before churn without forecasting it                                                                                                                                                                                                                                  | Require backtested lift; sanity-check with churned-account interviews                                                                                                                                                  |
| Ranking by ratio starves the telemetry signals | Product usage and adoption breadth carry the highest lift and longest lead times and cost the most to instrument, so a register built purely on efficiency is all CRM-derived and lagging - the same register that survivorship bias produces from whatever the CRM already holds | Promote telemetry when events already exist, when the mandate is compounding, or when the cheap register misses the 70% floor; pull churned accounts' signal state 60-90 days pre-churn - still-green means blind spot |
| Support-ticket volume read one-way             | Engaged customers file more tickets; silent disengagers file none                                                                                                                                                                                                                 | Pair volume with severity, age, and sentiment; treat silence-after-spike as its own signal                                                                                                                             |
| NPS/CSAT weighted as a strong predictor        | Response bias - the quietly disengaging do not answer surveys                                                                                                                                                                                                                     | Rank below product engagement unless the user's own backtest says otherwise                                                                                                                                            |
| Vendor-outreach artefacts                      | A CSM emailing an at-risk account makes "engagement" rise                                                                                                                                                                                                                         | Count customer-initiated activity only                                                                                                                                                                                 |
| Accuracy as the validation metric              | Churners are rare; predicting "no churn" scores high                                                                                                                                                                                                                              | Precision/recall and PR-AUC once any model exists                                                                                                                                                                      |
| Overfitting a small churned sample             | A single train/test split misleads                                                                                                                                                                                                                                                | K-fold rather than one split; widen the outcome period                                                                                                                                                                 |
| Silent churn lost in aggregates                | A slow per-account fade is invisible in book-level reporting                                                                                                                                                                                                                      | Trend each account against its own baseline, not the aggregate                                                                                                                                                         |

## Reference

- Read [references/signal-taxonomy.md](references/signal-taxonomy.md) when building the candidate list - the categories ranked by value per unit of instrumentation effort, the five-part operational template, lead-time expectations, framework credits, and the confirmatory-tripwire list.
- Read [references/ranking-methods.md](references/ranking-methods.md) when validating and ranking - the method order and what each rung buys, which methods a thin sample or an unmaintained model deletes, backtest mechanics, lift, retention-curve comparison, WoE/IV with interpretation bands, and PR-AUC.
- Read [references/examples.md](references/examples.md) when writing the register - a worked B2B register, a compact B2C one, worked lift and WoE/IV computations, and one plausible-looking bad signal decomposed.
- See `mbfinotti/revops-skills@lead-scoring` for the same backtest-and-lift validation logic applied pre-sale to leads instead of post-sale to accounts.
