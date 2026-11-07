---
name: five-case-model
description: Develops an integrated investment or business case across strategic, economic, commercial, financial, and management dimensions using HM Treasury's Five Case Model. Use when a decision owner needs a proportionate, option-based case for committing resources.
metadata:
  author: labdotsa
  category: product
---

# Five Case Model

Develop five interdependent views of one proposal:

~~~text
Strategic: is there a compelling case for change?
Economic: which option provides the best value?
Commercial: can a viable deal and supply arrangement be made?
Financial: is it affordable and fundable?
Management: can it be delivered and governed?
~~~

These are not five separate narratives. Iterate them together and preserve one shared option set and assumptions.

## Set the business-case stage

State the decision, sponsor, approval authority, investment, scope, appraisal period, and maturity:

| Stage | Decision supported |
| --- | --- |
| Strategic outline | whether to develop the case and which broad options survive |
| Outline case | preferred option and route before major procurement/commitment |
| Full case | final deal, affordability, and delivery authorization |

Scale evidence and detail to value, risk, and reversibility. A full-case verdict requires current commercial, financial, and delivery evidence.

| Stage | Gate depth required | `proceed` authorizes |
| --- | --- | --- |
| Strategic outline | Strategic gate passes; genuine longlist and preliminary tests show credible options; commercial/financial/management routes and fatal constraints are bounded | develop the Outline Case and reversible option/market work only |
| Outline case | Strategic and Economic gates pass at shortlist level; commercial, financial, and management cases demonstrate credible routes with bounded conditions | develop procurement/deal and Full Case within stated limits |
| Full case | All five gates pass with current deal, affordability, funding, delivery, benefits, and risk evidence | final scoped implementation/commitment |

At every stage, a case not yet due is `bounded_for_next_stage`, not falsely passed. The Decision Record states the stage and commitment ceiling.

## Build the Strategic Case

Create:

1. current arrangement/business as usual;
2. problem or opportunity evidence;
3. drivers and strategic fit;
4. SMART objectives and outcomes;
5. theory of change from inputs → activities → outputs → outcomes;
6. scope, constraints, dependencies, benefits, and risks;
7. consequences of no action and delay.

**Strategic gate:** the need and objectives remain valid without naming the preferred option.

If the gate fails because the case is solution-led, reframe need/objectives and repeat it. If credible evidence rejects the need or strategic fit, stop the proposal. Do not appraise commercial or financial detail for an option that has no independent case for change.

## Build the Economic Case

### Create the longlist

Use dimensions such as scope, service solution, delivery, implementation, timing, funding, and scale to generate a genuine range. Include business as usual, minimum intervention, and credible alternatives.

### Apply critical success factors

Define must-have criteria from the Strategic Case before screening.

| Option | CSF pass/fail | Reason | Advance/reject |
| --- | --- | --- | --- |

If no option passes, first test whether the CSFs faithfully represent the Strategic Case. If they do, regenerate or redesign options; if no credible option can pass, stop or return `rework_or_reappraise`. Never name a preferred option from a rejected shortlist.

### Appraise the shortlist

Compare costs, benefits, risks, timing, distributional effects, unmonetized impacts, opportunity cost, and uncertainty over the appraisal period. Use common assumptions and discounting where fit.

| Option | Benefits | Costs | Risks | Unmonetized effects | Value finding |
| --- | --- | --- | --- | --- | --- |

Avoid using only the benefit-cost ratio. Explain why the preferred option provides the best value relative to alternatives and the counterfactual.

## Build the Commercial Case

Test:

| Area | Evidence |
| --- | --- |
| Supply market/capacity | capable suppliers/partners and competition |
| Sourcing/delivery model | make, buy, partner, license, or hybrid |
| Deal structure | scope, price/payment, term, incentives, allocation |
| Risk allocation | party best able to manage each risk |
| Procurement/legal | route, approvals, IP, data, compliance |
| Exit/continuity | termination, transition, service continuity |

Do market engagement without predetermining a supplier. State dependencies and conditions precedent.

## Build the Financial Case

Show affordability from the organization’s cash and accounting perspective:

- investment and operating costs by period;
- revenue/savings where applicable;
- funding versus financing sources;
- cash flow, cash trough, runway, and headroom;
- tax, inflation, FX, working capital, contingencies;
- scenario and sensitivity;
- budget ownership and release conditions.

Keep economic/social value distinct from financial affordability. A high-value option can still be unaffordable.

## Build the Management Case

Define:

| Element | Required evidence |
| --- | --- |
| Governance | sponsor, board, decision rights, assurance |
| Delivery plan | milestones, dependencies, critical path |
| Resources | team, capability, partners, budget |
| Change/adoption | affected workflows, incentives, training |
| Benefits realization | measures, owners, timing, evaluation |
| Risk/issue control | triggers, escalation, contingencies |
| Procurement/implementation | approvals, acceptance, transition |
| Monitoring/evaluation | baseline, review, post-implementation learning |

The delivery plan must explain how outputs become the outcomes claimed in the Strategic Case.

## Reconcile the five cases

Maintain one case-gate record:

| Case | Minimum finding | Result | Failure route | Reopen evidence |
| --- | --- | --- | --- | --- |
| Strategic | independent case for change and measurable outcomes | | reframe or stop | |
| Economic | at least one CSF-passing option demonstrates best value against counterfactual | | regenerate/reappraise/stop | |
| Commercial | viable market/deal/risk-allocation/exit path | | market engagement, restructure, or stop | |
| Financial | affordable cash/funding/headroom under downside | | rescope, rephase, fund, or stop | |
| Management | credible governance, capacity, delivery, adoption, and benefits realization | | resource/replan/rephase or stop | |

A failed or insufficient case blocks final authorization. Continue another case only to diagnose a repair or compare a live option—not to manufacture completeness.

Create a shared-assumption table:

| Assumption | Strategic | Economic | Commercial | Financial | Management | Conflict/resolution |
| --- | --- | --- | --- | --- | --- | --- |

At minimum reconcile option scope, volume/demand, schedule, price, cost, capacity, procurement route, risk treatment, benefits, funding, and ownership.

Run the questions below and record the work, not merely the answers:

| Challenger / independence | Evidence or assumption tested | Finding | Sponsor response | Affected case/option | Reopen action | Unresolved blocker |
| --- | --- | --- | --- | --- | --- | --- |

Challenge whether the preferred option still wins under credible downside; whether the counterfactual/minimum intervention was dismissed; whether commercial evidence supports model cost/timing; whether funding exists before irreversibility; whether management can realize outcomes; and which condition reverses the recommendation.

## Issue the Product Investment Case

Deliver the stage statement, five cases, longlist/shortlist, critical success factors, option appraisal, shared-assumption reconciliation, conditions, red-team challenge, and Decision Record.

Use the controlling case state:

| Verdict | Required state |
| --- | --- |
| `proceed` | Every gate required at the declared stage passes; later-stage routes are bounded; counterfactual and challenge survive; only that stage's next commitment is authorized |
| `proceed_conditionally` | Every gate required at the declared stage supports the option and remaining conditions are bounded, owned, dated, funded, enforceable, precede exposure, and stay within that stage's commitment |
| `rework_or_reappraise` | One or more cases fail, but a credible rescope, alternative, commercial structure, funding route, or delivery repair survives |
| `stop` | Strategic need fails or every credible option fails a fatal CSF/case with no plausible remedy |
| `not_decision_ready` | Any material case or dependency is insufficient, stale, internally conflicting, or awaiting challenge/authority |

Decision readiness is stage-relative: every case required at the declared stage must support the same scoped next commitment, while later cases are bounded for the next stage and no current unknown may invalidate the present authorization. Only a **Full Case** can authorize implementation, and it requires all five dimensions to support the same option, a visible counterfactual, established affordability and value, credible commercial/management conditions, and explicit unresolved evidence.

Foundation: [HM Treasury Green Book 2026](https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government/the-green-book-2026) and [business-case guidance](https://www.gov.uk/government/publications/guidance-on-developing-business-cases).
