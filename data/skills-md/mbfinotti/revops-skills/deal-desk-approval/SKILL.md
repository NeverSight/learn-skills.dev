---
name: deal-desk-approval
description: Design the deal desk approval chain and exception-handling process for non-standard B2B SaaS deals - a tiered discount approval matrix and delegation of authority across five concession levers (price, payment terms, services, contract risk, security), margin floor policy, exception intake, two SLA clocks with a sales escalation path, and precedent control. Includes the rules-driven promo/discount-policy equivalent for PLG, self-serve, and B2C. Use whenever the user mentions deal desk, discount approval, quote approval, approval matrix, delegation of authority, non-standard deals, concessions, margin floors, or discount creep - even if they never say "deal desk". Covers deal-level commercial approvals only, not general business-process approval workflows.
license: MIT
metadata:
  author: Maya-Beth Finotti
  version: "1.3.8"
---

# Deal Desk Approval

Design who may approve what on non-standard deals - discounts, custom terms, risky structures - and deliver it as a spec: an approval matrix across five concession levers, a prohibited-terms class, exception intake with SLA clocks and escalation, and precedent control. This skill covers deal-desk approvals only: general business-process approvals (expense, procurement, HR, engineering change) are out of scope - say so and stop when asked for them.

Deal-desk thresholds are not standardized: every number in circulation comes from practitioner blogs and consultancies, several from content farms. The skill's core discipline is therefore provenance: label where each threshold comes from, and derive the real ones from the user's own deal data, not from an imported "industry" number.

## Ground Rules

- Tag every numeric threshold with its provenance. Never present a vendor heuristic as an industry constant.
  - Published practitioner source
  - Single vendor blog (illustrative only)
  - Derived from the user's own deal data
- Never state these circulating numbers as fact. Each is repeated across content without attribution. Omit them, or name them as circulating and unverified:
  - "75% gross-margin floor"
  - "1 deal-desk FTE per $40M ARR"
  - "35% mid-market / 70% enterprise deal-desk hit rates"
  - Stripe-attributed "4.2x churn at 30%+ discount"
  - Gartner-attributed "90% of B2B purchases AI-intermediated by 2028"
- "The customer asked for it" is not a justification. The highest-weight intake field is impact of denial - what changes if the exception is refused.
- Treat accounting and legal constraints as design constraints routed to Finance, Legal, Security, or Product. Never give legal or accounting advice.
- State the negative finding plainly where relevant: pricing-discrimination law barely constrains a non-dominant SaaS vendor's differential discounting (see [references/accounting-legal-constraints.md](references/accounting-legal-constraints.md)). Do not manufacture that compliance risk.
- Be honest where public practitioner guidance is thin. Design these explicitly with the user instead of presenting invented practice as standard:
  - Renewal treatment of granted exceptions
  - Reseller/MSP pricing governance
  - Approver-absence protocol
- Treat every option ordering in this skill and its references as a default, not a law. It shifts with context and with who executes it, so re-rank it against what you already know about the user before recommending anything.
- Concretely:
  - A deal desk of one analyst cannot fund a step-up register or a quarterly re-derivation.
  - A sales leader with veto over policy raises the political cost of tightening any floor, which promotes floors derived from data they cannot argue with.
  - A renewal book already full of grandfathered terms makes sunset a re-negotiation rather than an expiry, and step-up the realistic first move.
- Express effort as analyst review hours, approval-chain latency, the political capital of tightening a policy sales relies on, and reversibility - never as a currency amount. Discount percentages, margin floors, and win-rate arithmetic are the subject matter and stay as they are.

## Interview

Ask before designing anything. One question per message; multiple-choice where possible; skip anything already answered.

- GTM motion: sales-led, PLG with sales assist, hybrid, or pure self-serve/B2C?
- Segment mix and ACV bands - what does a small, typical, and large deal look like?
- Who approves discounts today, and through what channel: nobody, manager ping, email chain, quote tool, formal desk?
- What deal data can be queried: discount distribution by segment, win rate by discount band, per-deal margin, approval cycle time?
- Margin structure: near-zero marginal cost (classic software), or usage-scaling COGS (AI/inference, data, infra-heavy)?
- Which non-price concessions show up today: payment terms, free services, legal redlines, custom SLAs, security/privacy addenda, roadmap asks?
- Deal volume per quarter, and roughly what share needs any exception today?
- Where does the pain sit: speed (deals stuck in approval) or leakage (margin erosion, unlogged concessions) - or both?
- Which functions exist to route to: Finance, Legal, Security, Product/Delivery?
- Renewals: who owns them, and do prior discounts silently carry over today?
- Does discounting spike in the final weeks of the quarter?
- Deadline: what date must this spec be live by - before this quarter closes, next quarter, or no fixed date?
- One-off win or compounding asset: fix this quarter's discounting, or set the policy every future renewal and every new rep argues from? Compounding is literal here - a concession granted once is argued from forever.
- Effort ceiling: how many analyst hours per week can the desk fund, who holds veto over tightening policy, and how much political capital can you spend with sales?

Re-rank the reference menus against those last three answers, and say out loud which answer moved which option:

- A hard deadline promotes the fast-acting options - a placeholder auto-approve floor and sunset renewal treatment both land in a day - and demotes anything needing a data pull.
- A compounding mandate promotes the win-rate-derived floor over any placeholder even at the cost of a quarter's delay, because the placeholder becomes the discount level reps expect.
- A low effort ceiling deletes step-up renewal treatment, whose per-account tracking is a standing job, and pushes the exception lane's package assembly onto fewer, larger batches.

## Workflow

1. Run the Interview; collect every answer the spec depends on.
2. Confirm the scope boundary: this desk governs non-standard deals. If the request is really pricing strategy (list price, packaging, tiers) or a non-deal approval process, say so and route out.
3. Establish the five governed levers from [references/approval-matrix-design.md](references/approval-matrix-design.md):
   - Price/discount
   - Payment terms and billing
   - Services and delivery commitments
   - Contract risk
   - Security/privacy commitments

   A matrix that governs only price pushes concessions into the other four levers.

4. Design the matrix from the same reference:
   - Dimensions beyond discount %: deal size, segment, motion, term, product line, margin impact.
   - 3-4 tiers with an auto-approve floor at the bottom.
   - A policy margin floor underneath every tier.
   - The prohibited-regardless-of-approver class: MFN/best-price, open-ended price holds, uncapped liability outside carve-outs, unapproved roadmap commitments.
5. Map each exception type to its owning function and escalation trigger using [references/exception-taxonomy.md](references/exception-taxonomy.md).
6. Design intake, routing lanes, the two SLA clocks, elapsed-SLA escalation, approver-absence delegation, and quarter-end peak mode from [references/intake-routing-and-precedent.md](references/intake-routing-and-precedent.md). The completeness standard gates the SLA clock: incomplete requests bounce with a structured return, they never queue.
7. Design precedent control from the same reference:
   - Exception register, expiry on every granted exception, the pattern-to-policy review, and a renewal treatment per exception class.
   - Default to sunset: it recovers the whole concession for near-zero standing effort and stays reversible. Promote step-up only where a price snap-back has already driven churn in that segment.
   - Silent grandfathering is not one of the options.
   - Public guidance is genuinely thin here: decide it with the user and record it as house policy.
8. Encode accounting and legal constraints as routing rules from [references/accounting-legal-constraints.md](references/accounting-legal-constraints.md): which deal structures must reach Finance or Legal before any tier can approve, and why.
9. Handle B2B and B2C explicitly per the section below - asymmetrically, not with fake symmetry.
10. Calibrate thresholds in that reference's priority order:
    - Derive the auto-approve floor from win rate by discount band where the data exists.
    - Fall back to a percentile of the user's own discount distribution where win-rate data is thin.
    - Use an illustrative ladder only as a one-cycle placeholder that never ships as policy.

    Expect to need roughly two quarters of data before patterns are judgeable (RevOps Co-op); if it does not exist yet, say so in the deliverable.

11. Emit the spec (Output Shape below) one section at a time for user validation; ground it in a matching worked example from [references/worked-examples.md](references/worked-examples.md).
12. Attach the KPIs and Pass Threshold below and iterate until the pass conditions hold.
13. If your harness has persistent memory, memorize the decided tiers, floors, prohibited list, and renewal treatment so a later recalibration starts from them instead of re-interviewing.

## B2B and B2C

A human deal desk is a B2B/enterprise construct: B2B prices per customer - quoted and negotiated - while B2C prices per product - published and taken. No B2C deal desk exists; do not invent one.

- PLG, self-serve, and high-volume transactional SMB: the equivalent is a rules-driven discount policy - an automated promo engine, published discount bands, coupon governance, and exception rules published in the terms, with no human chain. A human enters only above the deal size where sales assist begins.
- B2C commerce: promo/markdown calendar governance, coupon issuance and stacking rules, and a published price-adjustment policy play the deal desk's role.
- What transfers identically to all of it: the erosion-by-exception dynamic, undocumented precedent as its root cause, and the discipline of defining bands, logging every exception, and monitoring creep.

State this contrast as reasoning about how the mechanics carry across the two motions, not as a documented industry finding.

## Output Shape

Deliver every engagement as this artifact. Every threshold line carries a provenance tag; every approver has a named delegate.

```
DEAL DESK APPROVAL SPEC - <company>, <date>
Scope        : what counts as non-standard; what this desk explicitly does not govern
Levers       : how each of the five levers is governed (price, payment, services, risk, security)
Matrix       : dimensions x tiers, approver + delegate per tier, auto-approve floor,
               policy margin floor (or cost floor for usage-scaling COGS), fences per segment
Prohibited   : terms no tier approves without an explicit give-get trade
Intake       : required fields (impact-of-denial weighted highest), completeness standard,
               bounce protocol for incomplete requests
Routing      : fast / complex / exception lanes, with lane criteria and the target volume
               share per lane - bulk in fast; exception lane forced by structure, not size
SLAs         : response clock + decision clock per lane (business hours, complete-submission
               to recorded-and-communicated decision), 50/80/100 elapsed-SLA escalation,
               delegation and quarter-end peak mode
Precedent    : register fields, expiry on every exception, pattern-to-policy cadence,
               renewal treatment per exception class (sunset by default; step-up only
               where snap-back churn is evidenced; no silent grandfathering)
Constraints  : accounting/legal routing table - which structures reach Finance/Legal and why
Calibration  : data source per threshold, provenance tags, recalibration cadence
KPIs         : five-KPI scoreboard + measurement definitions
```

## KPIs

- Track the five-KPI scoreboard together, never one alone (Umbrex):
  - Cycle time
  - Win rate
  - Discount rate
  - Margin
  - Leakage

  Speed-only approves bad deals fast; margin-only produces gridlock, and reps route around the desk.

- Measure cycle time from complete submission to recorded-and-communicated decision, in business hours; report median AND 90th percentile, never the mean - the p90 tail is what fuels bypass behavior.
- Also watch:
  - Exception rate by type: the pattern-to-policy trigger.
  - Late-discovery rate: non-standard terms surfacing after proposal, an intake gap.
  - Price realization: pocket price / list price (SBI Growth).
  - End-of-period discount spikes.

## Pass Threshold

The spec passes only when all completeness conditions hold, then iterates on the calibration loop.

Completeness - iterate the spec until every item holds:

- All five levers governed; a prohibited class exists; the margin (or cost) floor is stated and approver-independent.
- Every tier names an approver and a delegate; both SLA clocks and the 50/80/100 escalation are defined per lane.
- Every numeric threshold carries a provenance tag, and none of the warned-off numbers appears as fact.
- The register has expiry dates, and a renewal treatment is decided and recorded.

Calibration - iterate the matrix on the exceptions-review cadence until both hold (RevOps Co-op heuristic):

- Approvals near-instant: too many things require approval, raise the auto-approve floor.
- Decision time slow (p90 beyond the exception-lane SLA): the tiers are wrong, re-cut them.
- No recurring exception older than two review cycles remains: promote it to standard policy or reject it explicitly, while discount rate and margin hold on the scoreboard.

## Common Failure Modes

| Defect                                                 | Consequence                                                          | Fix                                                                        |
| ------------------------------------------------------ | -------------------------------------------------------------------- | -------------------------------------------------------------------------- |
| Matrix governs only discount %                         | Concessions migrate to payment terms, services, legal, security      | Govern all five levers in one matrix                                       |
| One executive as the top approval point                | Deals sit for days while buyer procurement moves on                  | Named delegate per approver + 50/80/100 escalation                         |
| Approval logic living in chat threads and spreadsheets | Context does not travel; breaks at quarter end; no audit trail       | Route and record in the system of record, log every decision               |
| No completeness gate on intake                         | Clock burns on incomplete requests; rework loops                     | Gate the SLA clock on required fields; structured bounce                   |
| "One-time exception" with no expiry                    | Customer cites it as precedent the following year                    | Time-box every exception; register it; decide renewal treatment            |
| Relaxing rules under quarter-end pressure              | Period-end discount spikes; precedent set at the worst moment        | Peak mode adds capacity and cutoffs, never relaxed rules                   |
| Reporting mean cycle time                              | Tail pain hidden; reps bypass the desk                               | Median + p90, from complete submission to communicated decision            |
| Cost floor treated as the binding floor                | Near-zero software COGS makes it meaningless; margin erodes above it | Policy margin floor - except usage-scaling COGS products, where cost binds |
| Every deal labeled "strategic" to justify concessions  | If 40% of deals are strategic, nothing is                            | Separate strategic (executive-approved, logged) from tactical bands        |

## Invocation Examples

- "Our AEs discount whatever it takes and everything routes to the CFO by email - design a real discount approval chain with tiers and SLAs."
- "We're formalizing a deal desk at $30K median ACV. Build the approval matrix and the exception process for non-standard terms: net-90, custom SLAs, security addenda."
- "Discounts spike every quarter-end and last year's 'one-time' exceptions are all back at renewal. Fix our exception handling and precedent control."

## Reference

- [references/approval-matrix-design.md](references/approval-matrix-design.md) - Matrix dimensions, tiers, floors, prohibited class, and threshold calibration
- [references/exception-taxonomy.md](references/exception-taxonomy.md) - Exception types and routing to owning functions
- [references/intake-routing-and-precedent.md](references/intake-routing-and-precedent.md) - Intake fields, lanes, SLAs, escalation, and exception register
- [references/accounting-legal-constraints.md](references/accounting-legal-constraints.md) - Revenue-recognition and legal routing rules
- [references/worked-examples.md](references/worked-examples.md) - B2B spec, PLG/B2C equivalent, and negative example
- See `mbfinotti/revops-skills@revenue-leakage` to detect margin erosion
- See `mbfinotti/revops-skills@sales-pipeline-hygiene` for stage discipline and pipeline integration
- See `mbfinotti/revops-skills@sales-forecast-diagnostic` for period-end deal slip
