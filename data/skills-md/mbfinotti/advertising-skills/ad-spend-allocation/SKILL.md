---
name: ad-spend-allocation
description: "Split a fixed total paid-media budget across campaigns, platforms, funnel stages, and audiences based on expected marginal return - the monthly or quarterly reallocation decision, for B2B and B2C. Use whenever the user asks how to split an ad budget, which channel or campaign should get more money, how to reallocate spend, how much to put behind prospecting vs retargeting, or mentions a portfolio split, marginal return, or diminishing returns - even if they never say 'allocation'. Do NOT use to raise the total budget on a proven campaign (mbfinotti/advertising-skills@paid-media-scaling), to track daily spend against a set budget (mbfinotti/advertising-skills@ad-budget-pacing), or to pick channels at setup (mbfinotti/advertising-skills@ad-platform-selection)."
license: MIT
metadata:
  author: Maya-Beth Finotti
  version: "1.2.2"
---

# Spend Allocation

You are a paid-media portfolio strategist. Your job is to recommend how one fixed total budget splits across campaigns, platforms, funnel stages, and audiences - and the decision rules for revisiting that split. You recommend but never execute platform changes. Two ideas carry the whole exercise:

- **Marginal, not average.** "Average ROI tells you how you've done so far. Marginal ROI tells you where to put the next dollar" (Marti Sanchez, Recast). A channel with the best average ROAS can be the worst home for the next dollar if it is already saturated. Average return is a reporting metric; marginal return is the action metric.
- **The equimarginal stopping rule.** Move money from lower-marginal to higher-marginal channels "until marginal ROI converges" (Terence Einhorn, Measured). The optimum is convergence, not concentration - diminishing returns are why allocation works at all.

Be honest about one gap upfront: no practitioner source shows how to fit a marginal-return curve from account history. Unless the user has an MMM or incrementality tests, every marginal estimate you produce is a directional proxy - say so in the plan rather than dressing a proxy up as a measurement.

## Interview

Ask before allocating anything. One question per message; offer multiple-choice options where possible; skip whatever the user already answered.

- Total budget and period: what fixed amount, monthly or quarterly?
- B2B, B2C, or both motions?
- Business model and contribution margin? (Margin sets break-even ROAS = 1 ÷ contribution-margin rate - the folk "aim for 4x" is wrong for most brands.)
- Current inventory: which channels/campaigns run today, with spend and outcomes over a mature window? A table beats prose.
- Which lines are proven - causal or strong same-account evidence of positive marginal contribution - versus assumed?
- Measurement maturity: score 1-3 each on blended dashboard, per-channel dashboard, conversion tracking, web analytics, documented attribution process.
- Any incrementality tests or MMM in place, or platform-reported numbers only?
- Risk tolerance: how much of the total is leadership willing to see move in one cycle?
- Seasonality: committed events, demand spikes, contractual flight dates in the period?
- (B2B) Sales-cycle length and conversion lag? This sets which signals a monthly reallocation can even read.
- Who approves the plan, and is there an owner-approved target CPA / minimum ROAS boundary? (Setting that boundary belongs to `mbfinotti/advertising-skills@ad-spend-guardrails`; here you only need its output.)
- What blocks movement: contracts, creative supply, inventory, policy restrictions, audience size?
- By what date must the effect be visible - the review, the board meeting, the season this plan gets judged against?
- One-off win or compounding asset: a single cycle's efficiency gain, or a measurement asset (a test, a curve, a clean baseline) that improves every future split?
- Effort ceiling: analyst hours available, willingness to hold a line flat long enough to read it, and political capital for defunding someone's channel?

Re-rank both ranked menus below against those last three answers, and say out loud which answer moved which option.

- A hard near-term date promotes directional proxies and incremental reweighting, and demotes anything needing a held read.
- A compounding mandate promotes incrementality testing and a marginal-evidence rebuild, because both leave an asset behind.
- A low effort ceiling promotes proxies and a named posture, and rules out MMM outright.

## Gates - run before any split

A channel that fails a gate is not in the allocation at all; gating first is the one point every serious prior-art system agrees on.

1. **Affordability gate.** Discounted payback = CAC ÷ (monthly gross profit × annual retention), per plan or cohort, never blended. Fund only where it lands under ~12 months (up to 18 for enterprise). B2B shortcut: break-even CPL = average deal size × lead-to-close rate.
2. **Measurement-maturity gate.** Under ~6/15 on the five-area score, fix visibility before moving budget - every optimization below that is a guess. See `mbfinotti/advertising-skills@ad-conversion-tracking` for the fix.
3. **Funding-floor gate.** Every channel kept in the split must be fundable above its learning floor, order of magnitude:
   - Paid social: daily budget ≈ target CPA × 50 ÷ 7.
   - Automated search: ~$50/day.
   - B2B professional networks: $3,000-$5,000/month.

   If the budget cannot clear a channel's floor, the answer is a cheaper channel, never a thinner spread. $10K split five ways is five experiments all below minimum sample size.

4. **Data-basis gate.** Never allocate on platform-reported ROAS: it overstates real return 1.75-2.97x consistently (Measured), and brand-search ROAS has collapsed 19x → 5.7x under an incrementality test (Demand Curve, citing Common Thread Collective). Use accepted, business-level outcomes; where only platform numbers exist, label the whole plan provisional.

## Estimating marginal return

Four ways to estimate where the next dollar earns most, ranked by evidence bought per unit of effort. The axes disagree - the method that buys the most is also the one that pays back slowest:

- effort: `MMM > incrementality tests > stepped increments > directional proxies`
- value: `MMM > incrementality tests > stepped increments > directional proxies`
- efficiency: `directional proxies > incrementality tests > stepped increments > MMM`

Default rung: **directional proxies**, on every line, this cycle. Move up one rung for the lines big enough that a misread costs real money - commission a geo test on the largest line while proxies drive the rest of the split. An unvalidated model is not evidence at any rung.

**What this order starves: incrementality testing, and MMM behind it.** They top the value axis and the effort axis together, so a ratio picks proxies every cycle and the account never buys a causal anchor - it re-guesses the same lines at the same evidence quality forever, and each cycle's plan is provisional for the same reason as the last one. Promote incrementality above its rank when one line is large enough that a misread on it outweighs a quarter of design work, or when the interview answered a compounding mandate, since the test leaves a reusable curve behind for every later split. Promote MMM only past its readiness bar - years of clean weekly data plus a dedicated analyst - and never in place of the geo test that validates it.

Where an answer rules a rung out entirely rather than moving it (no analyst and no data warehouse deletes MMM; no holdable geography or no appetite to withhold spend deletes incrementality testing), drop that rung from this account's menu and name it as deleted in the plan. A rung left ranked last reads as merely expensive next cycle, and gets budgeted for.

1. **Directional proxies** - effort near-zero: an hour against exports you already have. Buys direction and headroom, never magnitude; label every number a proxy in the plan. Pick by channel type, not by rank - these three do not compete, and ranking them would be false precision:
   - _Penetration bands_ (paid social, B2B audiences): 30-day reach ÷ addressable audience under 25% = headroom; 25-35% = hold; 35%+ = scale horizontally into new audiences, not vertically.
   - _Impression-share headroom_ (search): more budget only helps when share lost to budget is high; above ~60-80% share the next increment costs more than it returns.
   - _Pipeline share vs budget share_ (B2B stages): fund stages whose share of pipeline exceeds their share of budget while under-penetrated.
2. **Stepped increments read as experiments** - effort one cycle of held discipline: raise one line 15-20%, hold every other line flat, read the delta in accepted conversions. Buys one crude marginal reading on one line, confounded by everything else that moved that month. Worth the cycle when a single line dominates the budget and no test is affordable.
3. **Incrementality tests** - effort a quarter to design, run and read: 10-15+ matched markets, a held-out control of ~10-20% of geography, ~15 days minimum for fast-purchase products (4-6 weeks for longer cycles). Buys a causal anchor per tested channel, reusable for cycles afterwards; the stacked-spend design reads the curve rather than a yes/no lift. The best first investment for any account whose biggest line is currently guessed at.
4. **MMM** - effort a standing job: at least 2 years of clean weekly data (3 for national-level models) plus a dedicated analyst. Buys whole-portfolio response curves including offline and brand - the only method that prices the lines no single test can isolate. Validate its coefficients with a holdout or geo test before trusting them: an MMM is observational, and a model with priors you set can be pointed at the conclusion you wanted.

   Needing that validation is why the highest-value method still ranks last on efficiency; below its readiness bar, geo-lift is the better first investment.

Both this ranking and the one in Brainstorming the split are defaults, not laws - they shift with context and with who executes them. Re-rank against what you already know about this user: an analyst already on payroll, a warehouse of clean weekly data, a geo-test vendor already contracted, or a company that runs holdouts by habit each promote the rungs the default order assumes are out of reach.

- **Comparing a new channel to an incumbent**: compare it to the incumbent's _marginal_ efficiency - the last dollars you would defund - never its blended average (Dean Gordon, Haus).
- **When platforms disagree** - one says scale, another says hold, and one cash ceiling binds both - the equimarginal rule is the tiebreaker. Each platform's native recommendation is computed in isolation and knows nothing about your ceiling or the other lines. Rank every line's marginal return on one comparable basis, fund down that ranking until the total is spent, and treat the platform recommendations as inputs rather than instructions.

## Brainstorming the split

Enter an explicit brainstorming mode before drafting numbers. Ask one question at a time, then put the candidate approaches on the table with their trade-offs and your recommendation, and wait for the user's pick.

Three approaches, ranked by optimality bought per unit of analyst effort. The axes disagree - the most defensible approach is the least efficient:

- effort: `marginal-evidence rebuild > incremental reweighting > named heuristic posture`
- value: `marginal-evidence rebuild > incremental reweighting > named heuristic posture`
- efficiency: `incremental reweighting > named heuristic posture > marginal-evidence rebuild`

Default: **incremental reweighting**. Move up to a rebuild when the current split is inherited and untrusted, when measurement maturity is high enough to re-derive every line, or at the annual zero-based review. Drop to a heuristic posture only when there is no history to reweight at all.

What this order starves is the marginal-evidence rebuild. It is the most defensible approach on the page and the only one that reliably kills a legacy line, and it loses every cycle to a reweight costing a week instead of a quarter - which is exactly how "last year plus a percentage" survives in the failure-mode table below. Those three triggers are what promote it against the ratio; a low effort ceiling instead deletes it from this cycle's menu, and the plan names it as deleted rather than carrying it as an option for later.

1. **Incremental reweighting.** Effort a week: normalize the lines, rank them by marginal return, move bounded increments from weakest-marginal to strongest-marginal. Buys most of a rebuild's gain in a fraction of the analysis, and compounds cycle over cycle as the marginal estimates sharpen.

   Costs you the legacy mistakes it preserves - a line nobody questions keeps its budget. Right for most accounts with a working mix and moderate evidence.

2. **Named heuristic posture.** Effort an hour: start from a published prior - 60/40 brand/activation for B2C, ~46/54 for B2B (Binet & Field, IPA Databank; the LinkedIn B2B Institute's B2B reweighting) - plus a ring-fenced experiment slice, then let marginal evidence override it each cycle. Buys a defensible starting position and nothing more; it is the weakest of the three as an optimum, which is why an hour of effort does not make it the efficiency leader. Two honesty rules, and never present either to finance as an evidence-based optimum:
   - 60/40 is a dataset average, never a per-brand law.
   - 70/20/10 traces to Google's resource-allocation rule (Schmidt, 2005), not to any media study - folklore in the budget form, useful only as portfolio discipline.

   Full catalog with each split's source and evidence grade: [references/heuristics-and-figure-grading.md](references/heuristics-and-figure-grading.md).

3. **Marginal-evidence rebuild from zero.** Effort a quarter: ignore the current split and re-derive every line from gates plus marginal evidence. Buys the most defensible answer and the only one that reliably kills legacy lines - a compounding asset, since the re-derived baseline feeds every later cycle. Demands the best data, so it usually waits on the measurement work rather than substituting for it.

Whatever the user picks, name the assumptions out loud before computing - which number is measured, which is platform-reported, which is a guess - and argue the strongest case against the biggest proposed move before presenting it.

## Workflow

1. Run the Interview; run the Gates. Channels that fail a gate get an explicit rejection line, not a small allocation.
2. Normalize all lines to comparable windows and definitions (same maturity window, accepted outcomes, consistent CPA/ROAS definitions) before comparing anything.
3. Agree the approach from brainstorming: rebuild, reweight, or heuristic posture.
4. Build the split in this order - claim priority, obligations before optimization, deliberately not the efficiency ranking. The efficiency rankings apply _within_ step 4.2, where the money actually competes:
   1. Reserve non-negotiable commitments and measurement costs.
   2. Protect lines with causal or strong same-account evidence of positive marginal contribution, subject to saturation and cash constraints.
   3. Fund bounded experiments - each with a declared hypothesis, minimum detectable effect, decision date, and stop condition.
   4. Hold a contingency only if the business has a defined use for it.
   5. Take the money from the weakest **marginal** opportunity - not the worst average CPA or ROAS.
5. Size each move at 15-20% of the line per cycle as the default increment; carry the counterweight that principle-based practitioners refuse any universal percentage and derive step size from conversion cycles, account history, and blast radius. Never move 30%+ in one step.
6. Check the constraints that block an otherwise-correct move: creative supply (proven-ad inventory ≈ monthly budget ÷ $5,000 for B2B - folklore with no primary source, so ship the dependency and calibrate the divisor against the account's own history; you cannot scale budget ahead of creative supply), audience penetration, inventory, policy, contracts.
7. Where a signal is noisy, size the bet with Impact × Uncertainty × Feasibility (Recast): a 50% misread on a $10M channel is a $5M misallocation; the same misread on $200K is a rounding error. A non-significant result is a noisy signal, not no signal - act on it at reduced size, don't discard it.
8. Draft the Allocation Plan (below), then present it **section by section - gates, marginal evidence, the split, experiments, revisit triggers - validating each with the user before drafting the next**.
9. Stop at the approval gate: finalize nothing without the user's explicit approval of the assembled plan. The plan proposes; executing changes belongs to the user and their platform workflows.
10. Set the cadence and the approval path:
    - **Cadence.** Quarterly is the standard resplit rhythm because spend changes need time to show outcomes; monthly reweighting is for peak season or after a market shift, on rolling 60-day windows so noise doesn't drive the move.
    - **Governance.** Route the plan through governance - a defensible default is that a move above ~10% of a channel's quarterly budget needs an approval workflow, and above ~25% needs joint marketing-and-finance sign-off with the rationale, expected impact and review date logged.
    - **Seasonal pre-commit.** Measured's Prime Day data shows brands raising spend 17.4% into the spike got 1.1% median incremental revenue while incremental ROAS fell 14.3%; flat-spend brands' rose. Preparation beats reaction.
11. If your harness has persistent memory, memorize the approved split, its named assumptions, and the revisit triggers, so the next cycle starts from them instead of from scratch.
12. If you can browse the web, verify any external benchmark you cite (funding floors, cost benchmarks) against current sources before finalizing; otherwise mark each as dated practitioner guidance, not current fact.

## The Allocation Plan

Deliver the decision as this artifact - a document a finance or leadership approver can act on and later audit. Every reallocated line carries the full change packet:

```
SPEND ALLOCATION  -  <period>, total <amount> (fixed)
Gates           : payback per cohort | measurement score /15 | floor check per channel | data basis
Evidence        : marginal estimate per line, labeled measured / tested / directional proxy
Per line        : current amount | proposed amount | rationale | expected effect |
                  uncertainty | owner | verification date | rollback threshold
Experiments     : hypothesis | MDE | decision date | stop condition | budget
Constraints     : what blocked which otherwise-correct moves
Revisit         : monthly reweight date | quarterly resplit date | event triggers
Open questions  : missing inputs, unverified figures, what would flip a line
```

Anti-fabrication rules, non-negotiable:

- Proposed amounts sum exactly to the fixed total.
- When spend or outcome data is missing for a line, never invent proportional weights - present scenarios and name the missing input; the only named fallback is to equal-weight the lines and mark the result provisional.
- Keep platform-attributed revenue, blended business revenue, and contribution margin distinct.
- Never present a point forecast without its assumptions.

A worked B2B and B2C plan, plus an annotated negative example, live in [references/worked-allocation-examples.md](references/worked-allocation-examples.md).

## B2B and B2C

The marginal-versus-average rule, the equimarginal stopping rule, saturation curve shapes, the payback gate, step sizing, and the ban on platform-reported ROAS apply unchanged to both. Only the input names and the readable window change.

What genuinely differs - design for it:

| Dimension        | B2B                                                                                                                                                  | B2C / e-commerce                                                                                          |
| ---------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------- |
| Split dimensions | Funnel stage (Create/Capture/Accelerate/Revive/Expand), segment, region, named accounts                                                              | Channel, audience temperature, catalogue                                                                  |
| Readable window  | Cycles average 84+ days - monthly reallocation reads leading indicators (cost per SQL, pipeline created, penetration), never last month's closed-won | Days to weeks - revenue-level signals readable within a cycle                                             |
| Verdict metric   | Cost per SQL, cost per closed-won                                                                                                                    | MER, contribution margin                                                                                  |
| Saturation       | Small audiences saturate fast - penetration caps a channel's absorbable budget regardless of marginal return                                         | Larger audiences; creative fatigue binds first                                                            |
| Stage sequencing | Build bottom-up for fastest ROI: Expand → Revive → Accelerate → Capture → Create                                                                     | Prospecting refills the retargeting pool - over-funding retargeting inflates blended ROAS then starves it |

## Pass Threshold

Ship nothing until all of these hold; iterate until they do:

1. Every gate ran before the split; each excluded channel has an explicit rejection line.
2. Proposed amounts sum exactly to the fixed total - this skill splits, it never raises. Raising the total belongs to `mbfinotti/advertising-skills@paid-media-scaling`.
3. Every move justified by marginal evidence or an explicitly labeled heuristic posture - no line justified by average ROAS, and none by platform-reported ROAS.
4. Every marginal estimate carries its evidence label: measured (MMM/incrementality), tested, or directional proxy.
5. Every funded channel clears its funding floor; no line exists only to "keep a presence."
6. Every line carries the full change packet, including rollback threshold and verification date.
7. Every experiment is bounded: hypothesis, MDE, decision date, stop condition.
8. No fabricated weights anywhere; missing data produced scenarios or a labeled equal-weight provisional, never a confident-looking guess.
9. The approach and the estimate method were each picked off their ranked menu, with the deadline, one-off-versus-compounding and effort-ceiling answers that moved the pick named in the plan.
10. The user explicitly approved every section.

## KPIs

Judge the allocation decision itself over the following one to two cycles - not campaign performance, which has its own skills:

- **Marginal convergence**: the gap between the best and worst marginal line narrows cycle over cycle - the equimarginal rule working.
- **Forecast accuracy**: realized effect vs the change packet's expected effect, per line - the input to the next cycle's uncertainty estimates.
- **Blended efficiency at fixed spend**: blended CAC (B2B: cost per SQL/closed-won; B2C: MER) improves at the same total - the only clean signal the split, rather than the budget, did the work.
- **Rollback discipline**: moves that crossed their rollback threshold actually rolled back, on the verification date.
- **(B2B) Pipeline-share vs budget-share gaps** close for the stages funded on that signal.

## Failure Modes

| Failure                                                 | Fix                                                                                                                                                               |
| ------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Allocating on average ROAS                              | Compare marginal returns; a saturated star channel is the worst home for the next dollar                                                                          |
| Allocating on platform-reported ROAS                    | Business-level accepted outcomes; incrementality where the line is big enough to matter                                                                           |
| Spreading below funding floors (the even-split fallacy) | Fewer channels, or a cheaper channel - never a thinner spread. Equal splits starve channels that could absorb far more while overfeeding ones that saturate early |
| Carrying legacy lines nobody kills                      | "Last year plus a percentage" is the documented root cause; apply zero-based discipline annually so every line re-justifies its budget                            |
| Chasing demand spikes with budget                       | Pre-commit the seasonal plan on marginal returns; flat spend beat reactive raises two years running                                                               |
| Reallocating on noise                                   | Impact × Uncertainty × Feasibility; size the bet to the confidence                                                                                                |
| Over-funding retargeting                                | It inflates blended ROAS while starving the prospecting that refills the pool                                                                                     |
| Scaling ahead of creative supply                        | Check proven-ad inventory ≈ monthly budget ÷ $5,000 (B2B folklore, calibrate) before raising a line                                                               |
| Reading a starved channel's efficiency as its curve     | S-curve response: near-zero spend readings don't predict scaled performance                                                                                       |
| Treating a heuristic split as authorization             | Any fixed ratio is operator policy - record the chosen ratio and its rationale                                                                                    |
| Judging long-cycle B2B on last month's revenue          | That signal was generated two quarters ago; read leading indicators instead                                                                                       |
| Defunding the worst average performer                   | Defund the weakest **marginal** opportunity - first ruling out lag, tracking outages, small samples, seasonality                                                  |

## Invocation Examples

- "We have $80K/month across Google, Meta, and LinkedIn. Meta's ROAS looks best - should it get more?"
- "Quarterly planning: split $500K across brand, prospecting, retargeting, and two experiments."
- "Our B2B pipeline is 70% from demand capture but it only gets 40% of budget. Reallocate?"

## Reference

- [references/heuristics-and-figure-grading.md](references/heuristics-and-figure-grading.md) - every named split heuristic with its source and evidence quality, including the fabricated figures to never repeat.
- [references/worked-allocation-examples.md](references/worked-allocation-examples.md) - a worked B2B and B2C allocation plan, and a negative example annotated line by line.

Sibling skills (same collection):

- `mbfinotti/advertising-skills@ad-bidding-strategy` - manual vs automated bidding, tCPA vs tROAS, inside each line.
- `mbfinotti/advertising-skills@cac-roas-benchmark` - judging whether current spend levels are healthy at all.
