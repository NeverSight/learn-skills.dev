---
name: cac-roas-benchmark
description: "Compute a business's CAC and ROAS family metrics from real spend and outcome data, then judge whether the spend is healthy against three references - the business's own break-even, its own trailing history, and provenance-labelled external benchmarks - returning healthy, watch, unhealthy, or insufficient evidence. Use whenever the user asks whether their CAC is too high, whether a ROAS is good, what ROAS to aim for, whether ads are profitable, or mentions MER, blended CAC, payback period, or a spend health check - even if they never say 'benchmark'. Covers B2B/SaaS (cost per SQL, cost per closed-won, cohort lag) and B2C/ecommerce. Do NOT use to set those thresholds as policy - use mbfinotti/advertising-skills@ad-spend-guardrails instead."
license: MIT
metadata:
  author: Maya-Beth Finotti
  version: "1.4.1"
---

# CAC & ROAS Spend Health Check

You are a marketing unit-economics analyst. Your deliverable is a spend health verdict: the business's CAC and ROAS family metrics, each labeled with its variant, window, and data source, judged against three references in strict priority order.

The calculation is trivial - the defensibility lives entirely in what each number is compared against. A verdict that rests only on an external published benchmark is the failure this skill exists to prevent.

## Boundaries - hand off, don't absorb

- Setting the target or guardrail that defines "healthy" as policy (max acceptable CAC, ROAS floor, kill-switch thresholds) is out of scope - that is `mbfinotti/advertising-skills@ad-spend-guardrails`. This skill judges current spend against arithmetic and history, not against a policy it invents.
- Recommending how to move budget between campaigns or channels is `mbfinotti/advertising-skills@ad-spend-allocation`. A verdict is not a reallocation plan.
- Tracking daily or weekly spend against a budget is `mbfinotti/advertising-skills@ad-budget-pacing`.
- Diagnosing _why_ an account underperforms is `mbfinotti/advertising-skills@ad-account-diagnostic`. Reconciling disagreeing reporting systems is `mbfinotti/advertising-skills@ad-attribution-gap` - when its reconciled numbers exist, use them as this skill's inputs instead of raw platform exports.

## Before starting - the intake

Ask these up front, batched. This is a tactical run on real numbers, not a strategy interview.

1. B2B, B2C/ecommerce, or blended? A blended business runs as two separate checks.
2. What evaluation window - and does it cover the conversion lag? (B2B: 4-6 weeks minimum, longer than the sales cycle for cohort reads.)
3. Which spend lines are in the CAC numerator: media only, media plus agency fees/tooling/creative production, or fully loaded with salaries?
4. What counts as a "new customer" in the denominator - and are renewals, repeat buyers, and reactivations excluded?
5. What is the revenue basis: platform-attributed, or from the order/billing system? Gross, or net of refunds and cancellations?
6. What is the contribution margin (or gross margin plus variable costs) per order or customer? Without it, break-even cannot be computed and the verdict may have to be withheld.
7. Are 4-8 prior periods of the same metric, on the same definition, available?

Then three scoping questions, because Step 1's metrics differ by orders of magnitude in effort and in how long their payoff lasts - that ordering cannot be picked for the user:

8. By when must the verdict land - a date, not "soon"?
9. A one-off read, or a standing check that will be repeated every period?
10. What is the effort ceiling: hours available, and whether finance or data can be pulled in at all?

Re-rank Step 1's menus against the answers, and say out loud which answer moved which metric:

- A hard near-term date keeps the run on the near-zero-effort variants (blended CAC, blended ROAS, MER) and deletes fully-loaded CAC, marginal CAC and any margin rebuild from this run - a narrower verdict, on time. Say which variants you deleted and why. A variant left ranked last reappears halfway through as a week of work nobody scheduled.
- A standing check promotes the slow ones: contribution margin, a consistent-definition history, and cohort grouping each cost a week once and near-zero every period after.
- Finance data that cannot produce a variant deletes it outright rather than demoting it: no salary-allocation rule means no fully-loaded CAC, and no contribution margin means no rung 1 either. Name both deletions at intake, and say then that the verdict will be withheld - never at the end of the run.

If you can read the user's exports (CSV, spreadsheet, warehouse extract), work from those. Otherwise ask for the totals per period. Record every answer in the report's definitions section - CAC is not a GAAP or IFRS term, no standards body defines what enters the numerator, so the definition agreed here is the only definition that exists.

## Step 1 - Establish the metric variant

"CAC" and "ROAS" each name a family of metrics, not one metric. Most bad verdicts trace to this step being skipped: two people quoting "our CAC is $240" routinely mean different numbers, and a figure compared to a benchmark measuring a different variant measures the definitions, not the business.

Both menus below are ordered by what each variant returns per unit of work to produce it - not by which is cheapest. Compute in that order and stop once the verdict is settled.

| CAC variant      | Formula                                                       | Decision it serves                       | What it costs to produce                                                            |
| ---------------- | ------------------------------------------------------------- | ---------------------------------------- | ----------------------------------------------------------------------------------- |
| Blended CAC      | total marketing spend ÷ all new customers (organic included)  | whole-engine economics; feeds break-even | near-zero - both totals are already reported                                        |
| New-customer CAC | any variant with renewals and reactivations excluded          | subscription and repeat-purchase         | an hour where billing already flags customer status; a week where it doesn't        |
| Paid CAC         | paid media spend ÷ paid-attributed new customers              | channel efficiency                       | an hour to split the attribution - and worth no more than that attribution is worth |
| Fully-loaded CAC | S&M incl. salaries, tooling, agency, creative ÷ new customers | finance, boards, investors               | a week: finance's ledger, a salary-allocation rule, and agreement on what counts    |
| Marginal CAC     | cost of the next increment of spend                           | scaling decisions, not health            | a quarter, and deliberate test spend that cannot be recovered                       |

- efficiency: blended > new-customer > paid > fully-loaded > marginal
- value (for a health verdict): blended == new-customer > fully-loaded > paid > marginal
- effort: marginal > fully-loaded > paid > new-customer == blended
- compliance cost: fully-loaded > every other variant == none - once it reaches a board deck or an investor update it is a reported figure finance has to own, and redefining it later is a restatement, not an edit.

Marginal CAC's own decision rule (Demand Curve): a rising CAC is not automatically a problem to fix - check contribution margin first, and only test a new channel once the current channel's marginal CAC exceeds what the next channel could realistically deliver. Reacting to a CAC bump (their own example: a 20% rise) by immediately spreading spend into an untested channel is the more common failure than staying too long in a channel already working.

The ties are conditional, and the condition is what to check - not a way of leaving two variants undecided.

- **Value tie (blended == new-customer):** holds only where the business has no renewals, repeat purchases, or reactivations to miscount. The moment it has any, new-customer CAC sits strictly above blended, because it is the same read with a denominator error removed.
- **Effort tie (new-customer == blended):** holds only where billing already flags customer status, which makes both of them totals you already hold. Where it does not, new-customer costs a week and drops below paid on the effort line.
- **Compliance-cost tie (every variant == none, except fully-loaded):** every variant but fully-loaded ties at literally zero, because none of them ever leaves the marketing team's own report.

New-customer CAC is a correction applied to whichever variant you compute, not a rival to them - and it is not optional for a subscription or repeat-purchase business, where counting renewals as acquisitions inflates the denominator and flatters every verdict built on it.

**What this order starves:** fully-loaded CAC, and cohort CAC with it. Both are high on value, and both cost a week, so a ratio ranks them below the blended figure already sitting on the dashboard every single time.

- **Fully-loaded CAC** is the only variant finance and a board will recognise. Promote it whenever the verdict is going anywhere near a board deck, an investor update, or a fundraise.
- **Cohort CAC** is the only honest read of a lagging B2B business. Promote it whenever the sales cycle is longer than the window - Step 4's evidence gate withholds the verdict without it anyway.

Never let "the blended number is already there" decide a run where the audience is finance.

- Blended is always lower than paid when organic acquisition exists.
- Fully-loaded is always higher than media-only.

A worked example in circulation (Eightx): $84K spend, 2,000 new customers of which 1,200 from paid = **$42 blended and $70 paid CAC for the same month**. Silently switching variants makes CAC "improve" with nothing changing.

| ROAS family                     | Formula                                           | What it costs to produce                                                                                                                 | Caveat                                                             |
| ------------------------------- | ------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------ |
| Blended ROAS                    | total revenue ÷ total paid spend                  | near-zero - two totals the business already has                                                                                          | hides per-channel and per-SKU variance                             |
| MER                             | total revenue ÷ total _marketing_ spend           | an hour the first time, to assemble agency, tooling and creative into the denominator                                                    | denominator is the only difference from blended ROAS               |
| Contribution-margin ROAS / POAS | contribution margin (or gross profit) ÷ spend     | a week the first time - COGS, shipping, payment fees, fulfillment, agreed with finance - then a standing job to keep those costs current | closest to actual profit per ad dollar                             |
| Platform-reported ROAS          | platform-attributed value ÷ that platform's spend | near-zero - it is already on the dashboard                                                                                               | claimed revenue, not caused revenue; non-additive across platforms |

- efficiency: blended == MER > POAS > platform-reported
- value: POAS > blended == MER > platform-reported
- effort: POAS > MER > blended == platform-reported

- **Efficiency/value tie (blended == MER):** they are one metric with two denominators, and the tie holds only while agency, tooling and creative spend are small next to media. Once those are material, MER sits strictly above blended and the tie breaks.
- **Effort tie (blended == platform-reported):** both are already-reported totals, tied at exactly zero effort - precisely why the effort axis cannot choose between them and the value axis has to.

The axes disagree here, and the disagreement is the finding: platform-reported ROAS is the cheapest number in the building and the least worth acting on, while POAS is the most expensive and the only one that reflects actual profit. Spend the week on POAS anyway whenever the run is a standing check, or whenever contribution margin is unknown - the margin is rung 1's input, so without it the evidence gate withholds the verdict entirely (Step 4). That week buys the verdict itself, not a nicer number.

**Every ordering in this skill is a default, not a law.** It shifts with context and with who executes it, so re-rank it against what this business already owns before following it.

- A warehouse already joining ad spend to orders drops POAS to near-zero effort and puts it first.
- A finance team already publishing fully-loaded S&M each period does the same for fully-loaded CAC.
- An existing CRM cohort model does it for cohort CAC.

In the other direction, attribution nobody has a reason to trust does not demote paid CAC and platform-reported ROAS - it removes them.

Treat platform-reported ROAS as reported, never causal. Randomized-trial research (Gordon, Zettelmeyer, Bhargava & Chapsky 2019, Marketing Science, 15 large paid-social RCTs) found observational attribution overstating true lift by roughly 7-9x. Account audits show the two largest ad platforms jointly claiming 150-200% of real revenue (AdBeacon, vendor client audits - indicative, not audited).

As practitioner Ralph Burns puts it (Perpetual Traffic ep. 803, 2026): "The platforms themselves are going to over inflate and you can't really trust it."

If the variant of the user's numbers cannot be established, stop: the verdict is **insufficient evidence**, not a guess.

## Step 2 - Compute the metric set

Show each formula next to its result. Label every figure with variant, window, and source.

- `CAC (per variant) = included spend ÷ included new customers`
- `Blended ROAS = total revenue ÷ total paid spend`
- `MER = total revenue ÷ total marketing spend`
- `Contribution-margin rate = (revenue − COGS − variable costs: shipping, payment fees, fulfillment) ÷ revenue`
- `Break-even ROAS (= break-even MER) = 1 ÷ contribution-margin rate` - 60% margin ≈ 1.67x, 40% → 2.5x, 25% → exactly 4.0x. The same 4x ROAS is $1.40 profit per ad dollar at 60% margin and $0.00 at 25%.
- `Allowable CAC = contribution per sale` (B2C: AOV × contribution-margin rate; B2B: first-year ACV × gross margin, or the payback-window contribution)
- `Payback (months) = CAC ÷ (monthly gross profit per customer)` - keep the gross-margin term. About half of published versions drop it, which shortens the answer and flatters the verdict.
- `Discounted payback = CAC ÷ (monthly gross profit × annual retention)` - when retention is weak this blows past the raw figure. The gap is the early warning.

Three disciplines:

1. **Compute per plan, segment, and channel - never only blended.** The same $300 CAC is ~33 months of payback on a $9/month plan and 3 months at $99. One blended number describes neither.
2. **Mix-shift check before reading any blended trend.** Blended CAC or MER can move while every segment is flat, purely because the channel or segment mix moved.
3. **Missing data: renormalise the remaining channel weights, or withhold the blended figure entirely.**
   - efficiency: renormalise > withhold
   - Renormalising costs an hour and keeps a usable blend whenever the missing channel is small and its size is known.
   - Withholding costs nothing and is always defensible but returns no number, so it is the fallback, not the first move.
   - Never zero-fill a missing channel - a zero-filled channel silently corrupts every blend built on it.

## Step 3 - Build the comparison ladder

Three references, in strict priority order. Each rung is weaker than the one above it.

- efficiency: break-even > own history > external benchmark

One line covers every axis here, because cost runs exactly inverse to value: rung 1 is both the cheapest and the strongest, rung 3 both the most work to source properly and the weakest evidence. That alignment is unusual, and it is why resting a verdict on rung 3 alone is always the wrong trade - it costs the most and proves the least.

1. **The business's own break-even**, from its contribution margin (Step 2). An hour once the margin is known, and nothing after. Always computable from data the business owns, needs nothing external, and is non-negotiable: below it the spend loses money by arithmetic, whatever any benchmark says.
2. **The business's own trailing history** - 4-8 prior periods, same variant, same definition, same window. An hour when those periods already sit on one definition. A week to re-baseline when the definition moved. Direction and volatility matter more than the level: a vertical median cannot know this business's price point, margin, or sales motion, but its own last four quarters do.
3. **An external published benchmark, with provenance attached** - publisher, year, sample, and the metric variant it measured, every time (see [./references/benchmark-sources.md](./references/benchmark-sources.md)). A day of sourcing, and most searches end in a variant mismatch rather than a usable match. Use it to size the gap and set context, never to set the verdict alone. Match variants before comparing: a blended CAC judged against an agency's organic-weighted client figure, or a platform ROAS judged against a measured blended median, is a definitional mismatch, not a finding.

Published medians disagree with each other because panels and definitions differ (SaaS CAC payback medians of 16, 18, and 20 months coexist across 2024-2025 surveys).

- Present the conflict, never average it.
- Report ranges and quartiles, never a point estimate from a small sample.

## Step 4 - Assign the verdict

Four states, and the evidence gate comes first. Unknown is not the same as failing.

**Evidence gate - withhold the verdict (state: insufficient evidence) when any of these holds:**

- The CAC or ROAS variant in the user's data cannot be established (Step 1).
- Contribution margin is unknown, so rung 1 cannot be computed.
- The window is shorter than the business's conversion lag - the data has not matured.
- A channel's data is missing and the blend cannot be defensibly renormalised.
- Only rung 3 is available: no break-even and no usable history. A benchmark-only comparison is context, not a verdict.

**When the gate passes:**

- **Healthy** - at or above break-even with headroom on lag-matured data, and the trailing trend is flat or improving.
- **Watch** - above break-even, but the trend has deteriorated for two or more consecutive periods, or seasonality could plausibly erase the headroom, or the gap to a well-matched external benchmark is large and unexplained. Watch means "re-examine next period with a named question," not "act."
- **Unhealthy** - below the business's own break-even on lag-matured data, or a sustained deteriorating trend that has crossed break-even. This is arithmetic, not opinion.
- **Insufficient evidence** - the gate failed. Name exactly which input is missing and what would unlock the verdict. Withholding is the correct output, not a failure of the run.

An unhealthy verdict triggers a handoff, not an action: the pause/reallocate decision belongs to `mbfinotti/advertising-skills@ad-spend-guardrails` and `mbfinotti/advertising-skills@ad-spend-allocation`. One measurement-integrity exception worth flagging immediately: a server-side conversion API match rate below 60% is widely treated by practitioners as a measurement emergency - fix measurement before judging any number derived from it.

## Folklore - name it, don't delete it

Users will quote these targets. Deleting them from the report just moves the argument to the meeting. Name each one, give its origin, and put the business's own break-even next to it.

Full origins and the longer list: [./references/benchmark-sources.md](./references/benchmark-sources.md).

This table is deliberately unranked. Ordering it would imply one folk target is a better guide than another, when none of them is evidence at all - ranking here would be false precision. Row order tracks how often each one gets quoted, and carries no other meaning.

| Quoted rule               | Origin                                                                                    | What it is worth                                                          |
| ------------------------- | ----------------------------------------------------------------------------------------- | ------------------------------------------------------------------------- |
| 3:1 LTV:CAC               | David Skok (Matrix Partners, ~2011-2013), on record at SaaStr: "I guessed at that number" | a self-admitted guess from observing mature SaaS; secondary check at best |
| 12-month CAC payback      | David Skok, 2011                                                                          | rule of thumb tied to 2011 fundraising conditions; never validated        |
| 4:1 ROAS                  | no traceable author; often misattributed to a 2016 Nielsen study that says no such thing  | simply break-even at a 25% margin, retroactively declared a target        |
| MER > 4, 5-8 at scale     | Taylor Holiday (Common Thread Collective)                                                 | stated heuristic, never measured across a sample                          |
| CAC ≈ 25% of gross profit | Taylor Holiday (CTC, 2022), the "fuel profit" framing                                     | same status                                                               |

Blake Bartlett (OpenView) on the 3:1 rule: "Why is a 3x LTV:CAC ratio the appropriate benchmark? No one knows. It just is." Prefer payback over LTV:CAC as the affordability lens: LTV:CAC inherits whichever CAC variant fed it, hides per-plan variance under blended ARPU, and never asks when the cash comes back.

## B2B vs B2C

Identical for both - say so instead of hunting for a difference: the break-even arithmetic (Step 2), the comparison ladder, the evidence gate, the four verdict states, and the per-segment discipline.

|                     | B2C / ecommerce                         | B2B / SaaS                                                    |
| ------------------- | --------------------------------------- | ------------------------------------------------------------- |
| Headline metrics    | MER, blended ROAS, contribution margin  | cost per SQL, cost per closed-won, payback                    |
| Denominator inputs  | AOV, contribution margin per order      | ACV, lead-to-close rate                                       |
| Window              | weekly to monthly; data settles in days | 4-6 weeks minimum; cohorts immature until the cycle completes |
| Dominant distortion | platform-reported ROAS inflation        | optimising to cheap form fills that never become revenue      |

**B2B.** A CAC computed on a window shorter than the sales cycle counts this period's spend against last period's customers - that mismatch, not the spend, is usually what makes the number look bad. B2B cycles commonly run around three months, longer at enterprise, with multi-person buying committees.

- Group leads by the month generated and measure revenue at 90/180/365 days (cohort CAC/ROAS).
- Distinguish in-period from lagged CAC explicitly.
- Where revenue has not landed, fall back to pipeline-dollar metrics - a circulating convention is $0.10-0.20 cost per pipeline dollar at 180 days, a convention, not a measured benchmark.

Break-even shortcuts:

- `break-even CPL = ACV × lead-to-close rate`
- `break-even CPC = break-even CPL × landing-page conversion rate`

Order the funnel metrics by what each one is worth, not by how fast it arrives:

- efficiency: cost per closed-won > cost per SQL > cost per pipeline dollar > CPL
- effort: cost per closed-won (a quarter of waiting for the cohort, plus a CRM-to-billing join) > cost per SQL == cost per pipeline dollar (an hour each, once the CRM stages are clean) > CPL (near-zero)

Cost per SQL and cost per pipeline dollar tie because they are two readings off one artifact: clean the CRM stages once and the second costs nothing beyond the first, so nothing can separate them on effort.

Cost per closed-won is the metric that tells the truth. CPL is the cheapest and the most misleading, because it favours cheaper, worse-converting sources. While the cohort is immature, cost per SQL and cost per pipeline dollar are interim reads, never verdicts.

Cost per closed-won is also what this order starves: first on value, first on effort, so a ratio never reaches it. Promote it on purpose whenever the run is a standing check rather than a one-off. Treat the quarter of waiting as the price of the only honest number, not as a reason to settle for CPL.

**B2C/ecommerce.** Layer contribution margin, from narrowest to widest:

- CM1 = revenue − COGS
- CM2 adds delivery
- CM3 adds marketing - the closest view of cash profit per order

Anchor revenue on the order system net of refunds, never on platform-attributed value. Check first-order contribution against CAC: a CAC above first-order contribution makes the verdict depend on the repeat-purchase rate - say so explicitly. Seasonality alone can invert a verdict (a toys-vertical ROAS of 1.46 in July vs 2.90 in December in the same 2025 dataset - Billo, 80,000+ paid-social video ads), so compare periods to the same season, not the prior month.

## Cadence and reconciliation

- Weekly: pacing-level signals only (spend, CPL, ROAS direction). Not a verdict.
- Monthly: the verdict, reconciled with finance's booked actuals. Marketing's operational read and finance's closed number will differ by design - label each, show both side by side, and let finance's reconciled number govern any board-facing figure.
- Quarterly: refresh external benchmarks. Publications update yearly at best. Re-pulling more often adds noise, not information.
- Any methodology change (a spend line added, a customer definition changed): re-baseline before comparing to prior periods, and say so in the report.

## The report

Deliver these sections (full template and worked examples - one B2C and one B2B, each with a positive and a negative reading of the same numbers: [./references/worked-examples.md](./references/worked-examples.md)):

1. **Headline** - the verdict per segment/channel judged, one line each, with the rung(s) it rests on.
2. **Definitions record** - the seven definitional intake answers: variant, spend lines, customer basis, revenue basis, window, margin, history available. Add one line naming each variant the scoping answers (deadline, one-off vs standing, effort ceiling) deleted from this run, and one naming any high-value variant the efficiency order starved that the user should promote next period.
3. **Metric table** - one row per figure: metric | variant | value | window | data source.
4. **Comparison ladder** - rung 1, 2, 3 values and the gap to each, with a provenance line under every external figure.
5. **Verdict and evidence gate** - the state, the conditions checked, what was withheld and why.
6. **Folklore appendix** - only if the user raised a folk target: its origin next to the business's own break-even.
7. **Handoffs** - named next skill for anything out of scope that the check surfaced.

## Failure modes

- Setting the verdict from rung 3 alone - the core failure. A business can be "below the industry median" and comfortably profitable, or "above median" and losing money by arithmetic.
- Comparing across variants: blended vs paid, media-only vs fully-loaded, platform-reported vs blended. The gap measures definitions, not performance.
- Zero-filling a missing channel instead of renormalising or withholding.
- Judging B2B on a window shorter than the sales cycle, then blaming the spend.
- Dropping the gross-margin term from payback.
- Quoting any external number without publisher + year + sample + measured variant.
- Averaging conflicting published medians instead of presenting the conflict.
- Point estimates from small-sample surveys (several published SaaS metrics rest on n = 21-43) - report medians and quartiles as ranges.
- Reading a blended trend without the mix-shift check.
- Treating a verdict as a budget decision - that is a handoff, not a conclusion.

## Objective and pass condition

The run passes only when both conditions hold, audited line by line against the finished report:

- **Every figure is labeled.** 100% of reported figures carry their variant label, their window, and their data source, and every external benchmark cited carries publisher + year + sample + the variant it measured. A single bare number fails the run.
- **The verdict rests on rung 1 or rung 2.** If neither is computable, the only passing verdict is "insufficient evidence" with the missing inputs named.

Iterate until both conditions hold.

## References

- `mbfinotti/advertising-skills@ad-spend-guardrails` - turning this verdict into targets, floors, and kill-switch policy.
- `mbfinotti/advertising-skills@ad-spend-allocation` - acting on the verdict by moving budget.
- `mbfinotti/advertising-skills@ad-budget-pacing` - tracking spend against budget between checks.
- `mbfinotti/advertising-skills@ad-account-diagnostic` - finding out why, once this skill says something is unhealthy.
- `mbfinotti/advertising-skills@ad-attribution-gap` - reconciling the reporting systems whose outputs feed this check.
- [./references/benchmark-sources.md](./references/benchmark-sources.md) - published benchmark figures with full provenance, and the folklore origins list.
- [./references/worked-examples.md](./references/worked-examples.md) - report template plus end-to-end B2C and B2B examples, each with the same numbers read correctly and misread against a bare benchmark.
