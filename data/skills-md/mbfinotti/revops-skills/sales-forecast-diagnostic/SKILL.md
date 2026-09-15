---
name: sales-forecast-diagnostic
description: Diagnose why an existing sales forecast is unreliable and recommend fixes - stage inflation and happy ears, sandbagging, deals without verifiable buyer evidence, stale or mass-pushed close dates, wrong forecast-category assignment, zombie and duplicate opportunities, late-created deals, manager roll-up overrides, and comp incentives that reward bias - separating data-quality from behavioral from genuine demand problems. Use whenever the user mentions forecast accuracy, a forecast miss, reps sandbagging, deals that keep slipping, "why did we miss the number", or "our commit is never right" - even if they never say "forecast". Covers B2B deal-based and B2C/high-volume. Do NOT use for pipeline coverage modeling - use mbfinotti/sales-skills@sales-pipeline-coverage-modeling instead.
license: MIT
metadata:
  author: Maya-Beth Finotti
  version: "1.3.4"
---

# Forecast Diagnostic

Investigate a forecast that missed, or that nobody trusts, and name the root cause with evidence. A forecast call asks "what's the number?" This diagnostic asks "was the number ever real?"

Practitioners converge on the view that most misses are inspection failures, not market failures: the evidence that a committed deal was fiction usually existed in the record before the miss.

Scope boundary, stated up front: this skill consumes whatever forecasting methodology already exists - the category set, roll-up rules, commit criteria, and coverage targets are inputs, not deliverables. Designing or redesigning that methodology is out of scope. When the investigation shows the methodology itself is undefined or ambiguous ("commit means different things to different reps"), report that as a finding and stop at the boundary.

Every confirmed root cause lands in exactly one of three classes, because each class has a different owner and a different fix:

- **Data**: the record was wrong, a human knew better.
- **Behavior**: the record faithfully reflects a biased human call.
- **Demand**: honest, evidenced pipeline still fell short.

The most common diagnostic error is issuing a behavior verdict for a data problem.

## Interview

Ask before analyzing:

- One question per message; offer multiple-choice options when possible.
- Skip anything already answered.
- Ask the first three questions below before any of the rest. Their fixes diverge by two orders of magnitude in effort and in how long they take to reach a forecast, and the answers decide the order the whole deliverable is ranked in.

Questions:

- By when must the number be more reliable - this period's call, the next one, or the next planning cycle? A fix that lands after the period closes does not help this forecast: a mid-period deadline deletes every fix slower than one cycle from the plan and leaves the hour-tier CRM-admin fixes carrying the whole load.
- One-off correction of this miss, or a standing accuracy program? One-off promotes the reconstruction, the zombie purge, and the date cleanup; standing promotes evidence gates, calibration scorecards, and threshold derivation.
- Effort ceiling: how many analyst hours, whether a CRM admin can ship a field or validation change this week, and who has authority to reopen the comp plan or change a review cadence. No admin turns every hour-tier fix into a week-tier request; no comp authority deletes the comp fix outright.
- What triggered this - a specific missed period, chronic inaccuracy, or a suspicion (sandbagging, inflated pipeline)? Which period(s)?
- Which direction is the error - over-forecast (missed the call), under-forecast (beat it by a lot), or erratic both ways?
- At which level does the number go wrong - individual rep, manager roll-up, or company-wide? Where in the roll-up can a human override the sum?
- What does the process look like today - forecast categories in use, submission cadence, who calls the final number? (Recorded as-is; not redesigned.)
- What history exists - opportunity snapshots, field history (stage, close date, category, amount changes), activity logs? How far back?
- What is the motion - B2B deal-based, B2C/high-volume/self-serve model-based, or mixed? Roughly how many deals per period?
- How is the team paid - quota cliffs, accelerators, quarter-end discount authority, anything rewarded or punished based on the forecast number itself?
- Any confounders in the period - CRM migration, stage redefinition, territory change, a bulk hygiene cleanup?

## Workflow

1. Run the Interview; establish the period, direction, and level of the error before touching deal data.
2. Quantify the miss before explaining it: forecast vs. actual per period, per roll-up level, per forecast category. Compute both signed error (bias) and absolute error - a symmetric average hides offsetting errors, since the same miss reads very differently depending on the chosen denominator, so fix one error definition first. Both numbers always ship together, as a correctness rule rather than a menu to rank and pick from - see [references/evidence-and-metrics.md](references/evidence-and-metrics.md).
3. Inventory the evidence base: period-start snapshot, field history, activity logs. If no snapshots or field history exist, start capturing them now, diagnose from current-state fingerprints plus interviews, and label every conclusion lower-confidence - without history, behavior verdicts are hard to defend.
4. Reconstruct the missed period from the period-start snapshot. Classify every deal that was in a forecast category by outcome (won as called, slipped, lost, removed, still open) and every deal actually won by origin (in the forecast? which category? when created?). If your harness can execute code, script this from a two-file export (period-start forecast, period-end actuals); otherwise ask the user for both lists and reconcile them by hand.
5. Run the root-cause fingerprints in [references/root-cause-fingerprints.md](references/root-cause-fingerprints.md) over the reconstruction. Require two independent signals per suspected cause, at least one from recorded history.
6. Interview reps and managers on flagged deals to split data from behavior. The discriminating question: "did you know this deal was dead (or real) before the CRM said so?" Yes means the record lagged reality - a data problem. No means behavior or demand.
7. Isolate demand last: rebuild the period-start forecast with hindsight-corrected data - zombies removed, honest categories, evidence-backed close dates. Whatever gap survives the correction is a genuine demand or coverage shortfall that no forecasting-process fix will recover; say so plainly.
8. Attribute the gap: every dollar of miss maps to a named deal (or a named model assumption in high-volume motions), each with one primary root cause and one class. Offsetting errors (sandbagged wins masking inflated losses) are attributed separately, never netted silently.
9. Check the pass thresholds in Measurement below; tune the fingerprints and re-run until every threshold holds.
10. Rank the confirmed causes for delivery using Fix leverage below: attributed dollars first, then divided by fix effort, with the adjustment shown rather than the two orders silently merged. One fix per cause matched to its class, plus the metric that will prove each fix worked within one period.
11. Deliver section by section for user approval; report shape and worked examples in [references/worked-diagnosis-example.md](references/worked-diagnosis-example.md).
12. If your harness has persistent memory, memorize the confirmed causes, the thresholds derived from this team's history, the effort tiers as they turned out for this team, and rep-level calibration baselines - the next period's re-run starts from them.

## Root causes in scope

The compact map: full detection fingerprints, second signals, and fixes live in [references/root-cause-fingerprints.md](references/root-cause-fingerprints.md), in this same order.

The value axis cannot be pre-ranked here and this skill does not pretend to: which cause is worth the most dollars is the output of the attribution table, and it differs with every engagement. What is stable is the fix - what it costs to ship and how long before a forecast reflects it - so the register is ordered by that, and the diagnosis then re-ranks it against the dollars it actually found (see Fix leverage).

- fix effort (most first): `comp-driven bias > rep sandbagging > stage inflation == missing evidence > late-created deals > manager override == wrong category > stale dates == zombies`
- time-to-effect (slowest first): `comp-driven bias > rep sandbagging > manager override > late-created deals > stage inflation == missing evidence > stale dates == wrong category > zombies`
- compliance cost (most first): only two carry any - `comp-plan change > a behavior verdict naming an individual rep`; every other fix is a CRM setting or a review habit with no external sign-off, so the axis is not worth a full ordering.
- efficiency at equal dollars (best first): `zombies > stale dates == wrong category > stage inflation == missing evidence > late-created deals > manager override > rep sandbagging > comp-driven bias`

Ties, each earned rather than dodged:

- **Stage inflation == missing evidence**: both fixes are literally one intervention, a buyer-evidence gate on commit entry, same owner, same week, same standing inspection.
- **Manager override == wrong category**: both are an hour of CRM admin (a reason field, category field history) plus exactly one negotiation with the people whose judgment the change constrains.
- **Stale dates == zombies**: both are one admin change plus a recurring sweep, constrain nobody's judgment, and are reversible the day they ship.
- **Stale dates == wrong category**, on time-to-effect only: both bite at the next edit, so one full cycle either way.

| Root cause                       | Usual class                   | Signature                                                                                                                               | Fix effort                                                                                                                                                             |
| -------------------------------- | ----------------------------- | --------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Zombie / duplicate opportunities | Data                          | Long-dead deals still open and counted; the same buying intent counted twice                                                            | An hour to purge with reason codes, then a standing hygiene sweep; coverage is honest in the same cycle                                                                |
| Stale / mass-pushed close dates  | Data                          | Push counts pile up; date edits cluster on a single day near period end                                                                 | An hour of admin for reason-required date moves, then a standing job; bites at the next push, so one cycle                                                             |
| Wrong category assignment        | Data or behavior              | Category contradicts stage and evidence; an omitted/excluded category used as a soft delete; category set at creation and never touched | An hour of admin for logged category changes - a week if the definitions themselves must be re-agreed across the team                                                  |
| Stage inflation / happy ears     | Behavior                      | Late-stage deals with no buyer-side evidence; stage skips in field history; wins far below what the stage implies                       | A week to define the buyer-evidence gate and change the review questions, then a standing inspection; the call gets honest one cycle later, win rates two              |
| Missing / unverifiable evidence  | Data or behavior              | Required fields filled with placeholders; nobody can say what the buyer last did                                                        | Same week, same gate, same owner as stage inflation - shipping one ships the other                                                                                     |
| Late-created deals               | Data                          | Deals created and closed within days, or created directly in a late stage - pipeline visibility is bookkeeping after the fact           | A week to set the logging rule, then a rep-habit change; coverage math is untrustworthy for a cycle or two after                                                       |
| Manager roll-up override         | Behavior                      | Manager number diverges from the rep sum in a consistent direction with no logged reason                                                | An hour to capture reasons, but a quarter of trailing overrides before the per-manager score means anything, and managers must accept being scored                     |
| Rep sandbagging                  | Behavior                      | Rep beats commit by a wide margin repeatedly; wins close from outside the forecast                                                      | A week to build the open calibration scorecard, 2+ periods of history before the pattern can be named at all; anything touching the incentive belongs to the row below |
| Comp-driven bias                 | Behavior (root of the others) | Slips cluster just past quota cliffs; predictable quarter-end discounts teach buyers to wait                                            | A quarter at best - plan amendments land at the next plan period, need finance/HR/legal sign-off, and are barely reversible once issued                                |

The efficiency order starves comp-driven bias, the one cause that drives the others: top of the impact axis in most diagnoses, bottom of the ratio in every one. A register read by ratio alone recommends the same CRM hygiene every period while the incentive that produces the behavior stays untouched, and the behavioral causes regrow.

Promote comp-driven bias above everything else when:

- Fingerprints show slips clustering at a quota cliff.
- The same rep's bias flips with their attainment position.
- A previous cycle's data fixes shipped and the behavior class did not improve.

At that point, the cheap fixes have no remaining value, and the deliverable says so instead of relisting them.

Boundary with neighbors: this skill detects deals sitting in a stage without evidence, but it does not redesign the stage set (see `mbfinotti/revops-skills@pipeline-stage-definition-audit` when the definitions themselves are the problem). It is a root-cause investigation of a specific miss, not the recurring stale-deal/missing-field sweep (see `mbfinotti/revops-skills@sales-pipeline-hygiene` for prevention once causes are fixed).

## Fix leverage

The register above is the tiebreak, not the answer. Once the attribution table exists, rank the confirmed causes for delivery in three passes, and put all three in the deliverable:

1. **Impact order** - causes sorted by attributed gap dollars, straight off the attribution table. This is the arithmetic of the miss and it never gets adjusted away; it is what makes the size of each problem auditable.
2. **Leverage order** - the same causes divided by their fix effort tier from the register. Never divide by a currency amount: the denominator is analyst hours, admin or engineering work, cross-team negotiation, and the number of forecast cycles before the fix reaches a call.
3. **The adjustment, shown** - every cause that moved between the two orders, with one line naming the effort that moved it. Presenting only the leverage order looks like the impact arithmetic was silently overruled, and the first executive question is always why the biggest number is not first.

Deliver in leverage order, with the impact order printed beside it. Lead with the best ratio, which is frequently not the cheapest fix - a large attributed cause with an hour-tier fix outranks a small one with the same hour-tier fix, and outranks everything week-tier. A worked adjustment is in [references/worked-diagnosis-example.md](references/worked-diagnosis-example.md).

## Re-rank before delivering

Every ordering here is a default, not a law. It shifts with the team and with who executes it, so re-rank against what the Interview and the reconstruction revealed:

- Deadline inside the current period - delete every week-tier and quarter-tier fix from this cycle's plan and say which, rather than listing them at the bottom where they come back as scope. What survives is `zombies > stale dates > wrong category`, and the deliverable states plainly that the behavior causes are untouched.
- A CRM admin on hand with authority to ship a validation rule this week - the hour-tier fixes stay an hour and lead. Without one, they become a week-tier request in someone else's queue and lose their ratio advantage to the evidence gate, which at least ships in the same week.
- A sales leader who will not reopen the comp plan - delete the comp fix from the plan, and name the specific behavior causes that will regrow because of it. Do not park it at the bottom as a demoted option.
- No snapshots or field history - the manager-override and sandbagging causes cannot be evidenced this pass at all. Delete them from the fix plan, start capturing history now, and schedule them for the re-run.
- Mid-quarter, forecast cycle already running - a fix shipped now changes the next call, not this one. Say which of the two periods each fix is aimed at, and stop offering the ones that reach neither.
- Anything the team already owns that the default order assumes away - a working evidence gate, a scored override log, a hygiene automation - drops that cause out of the register instead of being re-recommended.

## Data vs. behavior vs. demand

- **Data**: someone knew the truth; the record did not. Fix with hygiene automation and field ownership rules (`mbfinotti/revops-skills@crm-data-governance`), not with rep coaching.
- **Behavior**: the record faithfully reflects a biased judgment - optimism, self-protection, or a rational response to incentives. Fix with evidence standards for category entry, incentive changes, and review discipline. A dashboard never fixes behavior.
- **Demand**: honest, evidenced pipeline still fell short - coverage was genuinely thin or win rates genuinely moved. The fix belongs to pipeline generation and market strategy, not the forecast process. The coverage rule of thumb (target ≈ inverse of win rate, hence the popular "3x") is a widely repeated heuristic with no traceable primary study - derive the real target from the team's own conversion history.

Verdict discipline: a behavior verdict is an accusation. Make one only with the two-signal evidence rule satisfied plus the rep interview done, and keep the accuracy conversation separate from the performance/comp conversation - a diagnostic that feeds punishment teaches reps to sandbag, and the next miss becomes the diagnostic's own doing.

## B2B vs. B2C / high-volume / self-serve

- **B2B deal-based**: the workflow above applies literally - deal-by-deal reconstruction, deal-level fingerprints.
- **B2C / high-volume / self-serve**: the forecast is usually a model (run rate, cohort conversion, funnel math) with a human overlay. Apply deal-level fingerprints to whatever human layer exists (an inside-sales commit list, a manual adjustment). Translate the rest to the model layer:
  - Stale conversion assumptions are the stale close dates.
  - Over-inclusive funnel definitions are the stage inflation.
  - A chronically conservative manual overlay is the sandbagging.

  Track overlay-vs-model accuracy exactly like manager-override-vs-roll-up accuracy.

- **Identical for both motions**: the miss-decomposition method, the three-class verdict system, the measurement thresholds, and the statistics discipline do not change.

## Failure modes

| Trap                                            | Why it is wrong                                                                                               | Fix                                                                                                                                                               |
| ----------------------------------------------- | ------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Diagnosing sandbagging from one strong quarter  | One beat is noise; sandbagging is a repeated pattern by the same person                                       | Require the pattern across 2+ periods against the rep's own history                                                                                               |
| Behavior verdict on a data problem              | Ambiguous category definitions make honest reps look dishonest                                                | Run the discriminating interview question first; check definition consistency across reps                                                                         |
| Judging period-start calls with period-end data | Hindsight bias - the call must be judged on what was knowable then                                            | Reconstruct from the period-start snapshot, never from today's record                                                                                             |
| Anchoring on the biggest slipped deal           | One vivid deal rarely explains the gap; the long tail usually does                                            | Decompose all gap dollars before concluding anything                                                                                                              |
| Symmetric accuracy metric as the goal           | Over- and under-forecast have different causes and costs, and they net out                                    | Always report signed bias and absolute error separately, per level. Not a menu to rank and pick one from - both numbers are required for the other to be readable |
| Ranking the fixes by attributed dollars alone   | The comp-plan redesign outranks the field change that would have landed this cycle, and nothing ships in time | Divide dollars by the fix effort tier and show the adjustment (Fix leverage), then re-rank against the Interview answers                                          |
| Deleting zombies and declaring victory          | The evidence standard that admitted them is untouched; they regrow                                            | Pair every cleanup with the entry-standard fix, and hand recurring prevention to the hygiene audit                                                                |
| Punishing forecast error in comp                | Reps respond by sandbagging; error flips sign instead of shrinking                                            | Measure accuracy openly, separate it from performance reviews                                                                                                     |
| Trusting circulating benchmark statistics       | Most quoted forecast-accuracy numbers have no traceable primary study                                         | Derive every threshold from the team's own history; see the evidence reference                                                                                    |

## Measurement and pass thresholds

The diagnostic must meet every threshold below before it ships; iterate until it does:

- **Attribution coverage**: at least 90% of the gap dollars attributed to named deals (or named model assumptions), each with exactly one primary root cause and one class; the residual, at most 10%, is explicitly labeled unexplained - never silently absorbed.
- **Evidence rule**: every confirmed cause rests on at least two independent signals, at least one from recorded history (snapshot, field history, activity log). Interview testimony alone never confirms a cause.
- **Backtest**: the same fingerprint rules, run on an earlier closed period, flag at least 80% of the deals that actually slipped or were lost from commit in that period. Below 80%, the rules fit the story rather than the data - revise and re-run.
- **Actionability**: every shipped fix names its cause class, its owner, its effort tier, and the single metric that will show within one period whether it worked. The fix list ships in leverage order with the impact order printed beside it and every move between them explained; a list carrying only one of the two orders fails this threshold.

After fixes ship, keep scoring each period: signed bias and absolute error per level, rep calibration against their own baseline. Improvement in the named metrics - not a quieter forecast call - is what closes the investigation.

## Optional integration note

Skip this section unless the user names one of these platforms.

**Salesforce:**

- Forecast categories (Commit / Best Case / Pipeline / Omitted) are distinct from stage and independently editable; diagnose both fields.
- Field history tracking is opt-in per field and not retroactive. Enable it on stage, close date, amount, and forecast category immediately, even if this period must be diagnosed without it.
- The Pipeline Inspection feature surfaces week-over-week deal changes on supporting editions.

**HubSpot:**

- Deal-stage probabilities are editable defaults, not measured conversion. Replace them with the team's own history before trusting any weighted number.
- Manual forecast submissions are recorded and can be compared against the computed roll-up.

## Reference

- See [references/root-cause-fingerprints.md](references/root-cause-fingerprints.md) for per-cause detection signals, discriminators, and fixes, plus how to derive thresholds from the team's own history.
- See [references/worked-diagnosis-example.md](references/worked-diagnosis-example.md) for the report shape, a worked diagnosis, and a negative example (a wrong diagnosis and why it failed).
- See [references/evidence-and-metrics.md](references/evidence-and-metrics.md) for error-metric choices, the rep calibration scorecard, and which circulating statistics are safe to repeat.
- See `mbfinotti/revops-skills@pipeline-stage-definition-audit` to judge whether stage definitions are buyer-verifiable when the fingerprints implicate the definitions themselves.
- See `mbfinotti/revops-skills@sales-pipeline-hygiene` for the recurring audit that prevents the data-class causes from regrowing.
- See `mbfinotti/revops-skills@crm-data-governance` for field ownership and source-of-truth rules behind data-class fixes.
- See `mbfinotti/revops-skills@revenue-reporting` for turning a finished diagnosis into the executive or board narrative.
