---
name: affiliate-performance-dashboard
description: Define the metric set and layout for an affiliate performance dashboard, delivered as a dashboard specification document - metric definitions with explicit formulas, views per audience, refresh and review cadence, and alert thresholds for top affiliates, conversion by source, and program ROI. Covers B2B SaaS recurring revenue-share and B2C ecommerce order-level CPA programs. Use whenever the user mentions affiliate program reporting, affiliate KPIs, affiliate ROI, revenue concentration, or what to put on an affiliate dashboard, even if they never say dashboard. Specifies metrics, never builds them in a BI tool. Do NOT use for one creator campaign's measurement plan - use mbfinotti/partnerships-skills@influencer-measurement-framework instead.
license: MIT
metadata:
  author: Maya-Beth Finotti
  version: "1.4.5"
---

# Affiliate Performance Dashboard

Define what an affiliate program dashboard measures and how it is laid out, then deliver a dashboard specification document. The spec - not a built dashboard - is the artifact: whoever owns the BI tooling implements it from the spec.

No canonical affiliate-dashboard framework exists, and metric definitions are not standardized: no standards body enforces them, IAB and the PMA publish guidance only. Say this plainly to the user; never present a branded framework that does not exist.

The method borrows four established things and nothing else:

- **Incrementality measurement**, via holdout and geo-lift testing, resting on explicit definitions of incrementality, baseline conversions, and model validation.
- **Attributed ROAS vs attributed ROI split**, where ROAS divides attributed revenue by media cost and ROI divides it by media cost plus COGS.
- **Sourced vs influenced separation rule**.
- **Tiered metric hierarchy plus good-metric criteria**, from Croll & Yoskovitz's _Lean Analytics_: a metric must be comparative, a ratio or rate, understandable, and behavior-changing.

The platform glossary behind the first two definitions is named in [references/metric-definitions.md](references/metric-definitions.md), not here; the definitions are the skill's operative ones regardless of which platform the program runs on.

## Ground Rules

- Report validated/approved commission and net revenue, never gross - gross is the bigger number and the most-named practitioner error.
- Give every metric a one-sentence definition naming numerator, denominator, window, timezone, and counting method. A definition that cannot fit one sentence is theater.
- Provenance-tag every benchmark: vendor, trade body, synthesis, or the program's own derived baseline. Nearly all published affiliate benchmarks come from parties with an incentive to inflate the channel.
- Never sum partner-sourced and partner-influenced revenue; report them as two separate, capped numbers.
- Never compare two periods with different validation windows - reversal lag makes the recent one look artificially good.
- Keep fraud and compliance signals on the same view as performance, never in a separate tool - daily decision-makers need both at once.

## Interview

Ask before specifying anything, following these rules:

- One question per message.
- Multiple-choice where possible.
- Skip anything already answered.

- B2B SaaS, B2C ecommerce, or both?
- Program size and maturity: active partner count, monthly commission spend, program age?
- Who reads the dashboard - executive, operator, or both - and what decision should it drive?
- Commission model, and is any of it recurring?
- Validation/locking window length and clawback policy?
- Attribution model and cookie window?
- Which data sources exist - affiliate platform, billing/orders, CRM, warehouse - and does the partner ID reach billing or orders at all?
- Is partner type / promotional method captured per partner?
- Is new-vs-returning customer captured per conversion?
- Refresh capability and tooling constraints - live queries, daily batch, manual export?
- Current pain: what question can the program not answer today?
- Reporting cadence today, and which review meetings already exist?
- By what date must the first version be in front of its readers?
- One-off win - settle one contested question now - or a compounding asset the program is run from every week?
- Effort ceiling: analyst hours available, who owns the data join, and whether standing maintenance is fundable at all?

Those last three answers re-rank every option menu in this skill and its references. Say out loud which answer moved which option:

- A near date pins the spec to the orders spine and deletes every metric needing a join that does not exist yet.
- A compounding mandate promotes the customer-file join, cohort views, and churn-adjusted partner LTV.
- A thin effort ceiling deletes the modeled warehouse, the brand-bidding alert, and the creative slice outright rather than parking them at the bottom of the spec.

Every ranking here is a default, not a law - it shifts with context and with who executes it. Re-rank against what you already know about this user: a network that exports partner classification cleanly, a warehouse already loaded with billing and CRM, or no analyst at all each move different rungs.

## Workflow

1. Run the Interview; collect every answer the spec depends on.
2. Fix the source of truth and write the comparability contract - event definition, date basis, timezone, currency, counting method - before specifying any metric. Every later number inherits these choices; changing them afterwards invalidates all history. Three data foundations compete here, ranked by value per unit of effort, where effort is reconciliation work and standing maintenance:
   - efficiency: `billing/orders spine > customer-file join > modeled warehouse`
   - value: `modeled warehouse > customer-file join > billing/orders spine`
   - effort (most first): `modeled warehouse > customer-file join > billing/orders spine`

   Three costs distinguish these foundations:

   - The spine: a week of reconciling the platform export against orders or billing, then near-zero standing cost.
   - The customer-file join: a quarter, because the partner ID has to be stamped at order or account creation before new-to-file and sourced-vs-influenced are computable at all.
   - The modeled warehouse: a standing job.

   Default to the spine and climb only when a named decision needs it.

   Deleted, not demoted: the affiliate platform's own export as source of truth. Those are the claimant's numbers, so no effort saving redeems them; the platform stays the source for clicks and traffic, reconciled to the money spine.

   What this order starves is the modeled warehouse: highest value, loses every round. Promote it when the program's live question is incrementality rather than reporting, or when one repricing decision moves more money than the build costs.

3. Select the metric tier set: business/headline tier, input/driver tier, health/guardrail tier.

   Four metrics are floor rather than choice, because the Pass Threshold cannot be met without them:

   - Net program contribution
   - Cost of sale
   - Top-N partner concentration
   - Partner-sourced MRR/ARR in B2B

   Everything beyond that floor is a menu: take the top rungs of your segment's efficiency order in [references/metric-definitions.md](references/metric-definitions.md), which ranks B2B and B2C separately and names what each order starves. Reject any metric failing the four good-metric criteria, and stop adding rungs before the dashboard shows everything and therefore nothing. Delete every metric whose data the Interview says does not exist, naming it under Open items instead of leaving it in the spec as a wish.

4. Write each metric's spec row (see Output Shape), resolving every competing definition explicitly - the chosen numerator, denominator, window, and counting method go in the row, not in anyone's head.
5. Choose the slicing dimensions the program's data can actually support, in the efficiency order of [references/layout-cadence-and-alerts.md](references/layout-cadence-and-alerts.md): `partner > partner type > product/plan > geography > device > landing page > creative`. Partner type is not the cheapest slice and is the one that pays - build it anyway.
6. Lay out one view per audience: executive and operator views differ in metrics, not just detail level.
7. Set refresh and review cadence per tier - each tier has its own natural rhythm; one refresh rate for the whole dashboard is a defect.
8. Set alert thresholds, each with an owner, a channel, and an expected response time; prefer rolling-baseline dynamic thresholds over static ones. Ship them in the efficiency order of [references/layout-cadence-and-alerts.md](references/layout-cadence-and-alerts.md) - `reversal-rate spike > single-partner share spike > click-to-conversion anomaly > EPC drop > brand-bidding flag` - and stop when the team's attention runs out rather than filling the strip.
9. Derive the program's own baselines from its history; adopt no vendor benchmark as a baseline. Published figures calibrate expectations only ([references/concentration-and-cohorts.md](references/concentration-and-cohorts.md), [references/roi-and-incrementality.md](references/roi-and-incrementality.md)).
10. Validate the spec with the user section by section - definitions, then views, then cadence, then alerts - before assembling the final document. Ground it in a matching worked example from [references/worked-examples.md](references/worked-examples.md).
11. Check the Pass Threshold below; iterate until every criterion holds.
12. If your harness has persistent memory, memorize the comparability contract, agreed metric definitions, and derived baselines so later runs start from them instead of re-negotiating.

## Output Shape

Deliver every spec as this artifact:

```
DASHBOARD SPEC - <program>
Header    : program, audiences, source of truth, period conventions
            (timezone, date basis, currency, validation window)
Metrics   : one row per metric -
            Metric | Definition (formula, window, counting method) | Tier | Source |
            Visualization | Target | Alert threshold | Provenance
Views     : layout per audience - KPI tiles (value + delta vs stated prior period)
            -> trend/composition charts -> leaderboard/detail table -> alert strip
Dimensions: slicing dimensions (partner, partner type/promotional method, product,
            geography, device, landing page, creative)
Cadence   : tier -> refresh rate + review ritual (who reviews, when, deciding what)
Alerts    : register - metric | trigger | owner | channel | expected response time
Open items: data gaps, unconfirmed definitions, metrics and dimensions deleted
            because the data or the effort ceiling rules them out, and what would
            make each computable; questions for the next revision
```

Record in the header which data foundation was chosen and what moved it there - a later reader cannot re-derive that choice from the metric rows alone.

Full worked examples live in [references/worked-examples.md](references/worked-examples.md), never inline.

## Pass Threshold

The spec passes only when a program owner can answer at a glance: _is this program profitable, and who drives it_. Concretely, all six must hold; iterate until they do:

- Every headline number is reproducible from its written formula by someone who did not build the dashboard.
- Net program contribution - validated commission plus network/agency fees against attributed net revenue - is visible without leaving the top view.
- Top-partner concentration is visible on that same top view.
- Every metric on the dashboard has a named decision it informs; drop it otherwise.
- Zero metrics whose definition cannot be stated in one sentence.
- Every metric, dimension and alert that did not make the spec appears under Open items with what would make it computable - nothing was silently parked at the bottom.

## B2B SaaS vs B2C Ecommerce

These apply identically to both:

- The comparability contract
- Metric tiering
- Concentration analysis
- Cadence discipline
- Alert design
- Validated-not-gross reporting

What genuinely diverges:

- **Revenue object.** B2B tracks partner-sourced MRR/ARR and churn-adjusted partner LTV; B2C tracks order-level CPA, AOV, and basket composition.
- **Funnel.** B2B adds trial-to-paid as a second conversion stage plus deal-registration and MQL/SQL pipeline stages; B2C is click to order, with new-to-file as the extra dimension.
- **Windows.** B2B cookie windows run 60-180 days for long cycles; B2C defaults to ~30 days, and coupon/cashback traffic runs shorter still. `mbfinotti/partnerships-skills@affiliate-commission-structure` owns these ranges - read a window against its numbers, never against a second set stated here.
- **Reversal driver.** B2B: trial failure, refund, downgrade, churn - recurring commission makes reversal a per-cycle event. B2C: returns and chargebacks inside the return window.

## Failure Modes

| Defect                                                 | Consequence                                                         | Fix                                                                                     |
| ------------------------------------------------------ | ------------------------------------------------------------------- | --------------------------------------------------------------------------------------- |
| Vanity metrics headline (clicks, impressions, signups) | Dashboard looks busy; informs no decision                           | Every metric needs a named decision; demote counts to diagnostics                       |
| Gross commission reported instead of validated         | Program looks more expensive and more productive than it is         | Headline validated/approved only; show pending separately                               |
| Last-click-only program ROI                            | Coupon/cashback/extension partners inflate; content partners starve | Add new-to-file share and incrementality tests; report sourced vs influenced separately |
| No concentration view                                  | One partner's exit erases a large revenue share unseen              | Top-1/5/10% share on the executive view, reviewed quarterly                             |
| Pending and approved states mixed                      | Totals unreproducible; trends meaningless                           | Comparability contract fixes the state per metric                                       |
| Reversal lag ignored                                   | Recent periods look artificially good                               | Compare only fully-validated periods; flag immature ones                                |
| Periods with different validation windows compared     | False trend in either direction                                     | Never compare them; annotate window changes on every chart                              |
| Sub-network counted as many partners                   | Partner counts and concentration both distorted                     | Count one credited entity per conversion; break out sub-networks separately             |
| Sourced + influenced summed                            | Double-counted partner revenue                                      | Two capped numbers; sourced takes precedence when a deal qualifies for both             |
| Network/agency fees excluded from cost of sale         | True program cost understated                                       | Cost of sale includes commission, network, agency, and placement fees                   |
| Vendor benchmark adopted as the program's baseline     | Targets and alerts miscalibrated in both directions                 | Derive baselines from the program's own history; tag vendor numbers as calibration only |
| Static alert thresholds                                | Alert fatigue; team ignores the strip                               | Rolling-baseline dynamic thresholds with owner, channel, response time                  |
| Metric with no decision attached                       | Review meetings recite numbers and decide nothing                   | Name the decision in the spec row or delete the metric                                  |

These rows carry no efficiency ordering, deliberately. Each is a defect with one fix, not a menu of competing fixes for one problem - ranking them would rank the reader's symptoms rather than their options. Apply every row that matches.

## Invocation Examples

- "Our SaaS affiliate program pays 20% recurring across 400 partners. Leadership asks every month whether it's profitable and I can't answer. Spec a dashboard for us."
- "I run an ecommerce affiliate program on last-click and the coupon sites look like heroes. Define the metrics and views for a program dashboard my team reviews weekly."
- "Write an affiliate program KPI spec for a program spending $80K/month in commissions - what we track daily vs monthly, with alert thresholds and owners."

## Reference

- Read [references/metric-definitions.md](references/metric-definitions.md) when writing metric spec rows - formulas, where credible sources disagree, B2B/B2C variants, provenance.
- Read [references/roi-and-incrementality.md](references/roi-and-incrementality.md) when specifying ROI metrics or judging checkout-adjacent partners - test designs, proxies, last-click failure cases.
- Read [references/concentration-and-cohorts.md](references/concentration-and-cohorts.md) when adding concentration views, lifecycle stages, and recruitment-cohort analysis.
- Read [references/layout-cadence-and-alerts.md](references/layout-cadence-and-alerts.md) when laying out views, choosing dimensions, and designing cadence and alerts.
- Read [references/worked-examples.md](references/worked-examples.md) when shaping the deliverable - one B2B SaaS spec, one B2C ecommerce spec, one negative example.
- See `mbfinotti/partnerships-skills@affiliate-payout-audit` for pre-disbursement accuracy of one payout run - this skill tracks the ongoing program, not a run.
- See `mbfinotti/partnerships-skills@affiliate-fraud-detection` for the fraud rule set - this dashboard surfaces its signals but never defines the rules.
- See `mbfinotti/partnerships-skills@partner-performance` for B2B channel-partner scorecards and QBR structure - out of scope here.
- See `mbfinotti/partnerships-skills@affiliate-program-terms` for the contract clauses behind validation windows and clawbacks.
