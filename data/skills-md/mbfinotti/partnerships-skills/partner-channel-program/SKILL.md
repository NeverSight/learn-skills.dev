---
name: partner-channel-program
description: Design the overall structure of a B2B partner or channel program from scratch - a readiness gate that can conclude not yet, partner value proposition, which motions to run (referral, reseller, services, technology), tier count, benefit stack, program-wide economics envelope, governance, and success horizon. Covers B2C analogs (dealer, franchise, ambassador). Use whenever the user mentions building a partner program, channel program design, launching a channel, a partner ecosystem program, or asks whether they are ready for partners, even if they never say program. Do NOT use for reworking tiers inside a program that already exists - use mbfinotti/partnerships-skills@partner-tiering instead.
license: MIT
metadata:
  author: Maya-Beth Finotti
  version: "1.0.6"
---

# Partner Channel Program

Design the overall architecture of a B2B partner/channel program from scratch. This skill is the architect: it decides whether a program should exist at all, which structural components it needs - motions, tiers, economics envelope, governance, horizon - and how they fit together, then hands the detailed design of each component to a specialist skill (see Reference).

The field's best-documented failure cause is structural, not tactical: launching a program to fix a direct motion that is not working. Partners amplify a working motion; they do not fix a broken one. The sequence below runs strategy before structure, and its gate is allowed to answer "not yet."

## Interview

Ask before designing anything. Ask one question per message, offering multiple-choice answers when possible. Skip a question only when the user already gave the answer.

- Is the business B2B or B2C? For consumer businesses (dealer, franchise, ambassador models) part of the design genuinely diverges - see [references/b2b-b2c-contrast.md](references/b2b-b2c-contrast.md).
- What is the ACV or price point of what partners would sell or influence?
- Is the direct sales motion already repeatable, with product-market fit proven? What is the evidence?
- What is the gross margin, and how much of it could fund partner compensation?
- Do informal partners already exist - agencies, integrators, consultants servicing your customers - or has anyone approached you about partnering?
- Who will own the program day to day, and who do they report to?
- What resourcing is committed: dedicated headcount, budget, and an executive sponsor by name?
- How are direct reps compensated today on a deal a partner touches - neutral, penalized, or undefined?
- What does success mean, and by what date must the first partner-sourced result land? Name the metric (revenue share, pipeline, coverage), the date, and who judges it then.
- Do you want a one-off win this year or a compounding asset? Both are legitimate answers; they select different motions.
- Given that resourcing, what is the effort ceiling this program must live inside - hours per week for the owner, whether standing headcount is fundable at all, and how much of the design must stay reversible?

Those last three answers re-rank step 4's motion menu - carry them there instead of re-asking:

- A hard date inside two quarters deletes reseller and services-SI: neither produces revenue that fast.
- A compounding mandate promotes technology partnerships and reseller coverage.
- A number needed this year promotes referral.
- No fundable standing headcount deletes reseller and services-SI again, and a team of one leaves referral plus at most one integration.

## Workflow

1. Run the Interview; collect every answer the gate and the architecture depend on.
2. Apply the readiness gate. Disqualifiers, any one of which means the honest answer is "not yet":
   - The direct motion is not repeatable, or partnerships are expected to fix a growth problem.
   - ACV too low to fund human-heavy partner work (very low ACV supports referral-only at most - reseller/SI motions need far more).
   - Gross margin that cannot fund partner margin.
   - No named executive sponsor.

   Say so, name what must change and the lighter motion (if any) that still fits, and stop. Full gate: [references/readiness-and-failure-modes.md](references/readiness-and-failure-modes.md).

3. Write the partner value proposition before any vendor ask - a one-sentence answer to "what is in this for the partner", plus the economic shape behind it. A program must give (a clear way to make money, training, deal protection, vendor air cover) before it may ask (dedicated reps, certifications, registration discipline). Capture it as a Partner Hypothesis - 1-2 pages naming the target partner type, why they would engage, and the expected economics - to be validated with 2-3 real prospective partners before anything is built on it.
4. Choose partner motions before any partner-profile work, from this menu, ranked by value returned per unit of effort - not by ceiling, and not cheapest-first. Say the order out loud to the user, then pick the minimum viable set, not every motion. The axes disagree, so read all of them:
   - efficiency: `referral > technology > services-SI > reseller`
   - effort: `reseller > services-SI > technology > referral`
   - value ceiling: `reseller > services-SI > technology > referral`
   - time-to-effect: `reseller > technology > services-SI > referral`
   - compliance cost: `reseller > services-SI > technology == referral` (tie argued: neither a technology nor a referral motion creates a contractual margin commitment or third-party delivery liability, and both are terminable in a paragraph)

   Each motion, with its trade-off:
   - **Referral** - near-zero standing effort: a commission rule, a link or a form, one tracking field. Buys warm introductions into accounts you already know how to sell. Low ceiling, adds no delivery capacity. Default first rung unless a constraint below deletes it.
   - **Technology** - a quarter of engineering, then a standing maintenance obligation, and no margin paid out. Buys durable surface: an integration keeps producing joint accounts and retention after the launch push stops. Slowest of the light motions to first revenue, so it needs the compounding mandate from the Interview to justify itself.
   - **Services-SI** - enablement content, a delivery-quality bar, and standing partner-manager time. Buys delivery capacity you did not hire and unblocks deals that stall on implementation. Pays only where implementation is a real buying obstacle; where it is not, this is coordination bought for nothing.
   - **Reseller** - a standing job: agreements, a margin table, order flow, deal registration, conflict policy, direct-rep comp neutrality, legal sign-off on resale terms. Buys coverage - segments and geographies you cannot reach directly - at the highest ceiling and the longest lead time. Hardest to reverse: unwinding it means re-papering signed agreements.

   What this order starves: reseller and services-SI. Both top the value-ceiling line and top the effort line at once, so the ratio puts them last in every round. A program that only ever obeys the efficiency line stays a referral program permanently: the coverage direct cannot reach and the delivery capacity that unblocks stalled implementations both stay unbought.

   Promote reseller above the light motions when reaching a named segment or geography is the stated goal of the program and standing headcount is funded. Promote services-SI when implementation shows up as a named reason in lost or stalled deals, not when an SI relationship merely exists. Neither is promoted by ambition, and neither wins a ratio it is built to lose.

   Constraints delete rows rather than demoting them. A deleted motion goes on the spec's Motions line with the trigger that would reopen it:
   - An ACV that cannot fund the partner's own cost of sale deletes reseller and services-SI outright.
   - A product that cannot be resold for contractual or technical reasons deletes reseller.
   - No fundable standing headcount deletes both.

   This order is a default, not a law: it shifts with context and with who executes it. Re-rank it against what you already know about this user before presenting it:
   - An agency or SI already servicing their customers promotes services-SI to the top, because the recruitment effort is already spent.
   - An existing platform-marketplace relationship promotes technology for the same reason.
   - A team of one collapses the menu to referral plus at most one integration.

   Sort borderline candidates with the build/sell/service typology and the influence/transact/retain lens. Ideal Partner Profile detail comes later, inside a chosen motion, and formal scored profiling waits until recruiting volume needs it. See [references/decision-sequence-and-frameworks.md](references/decision-sequence-and-frameworks.md).

5. Decide whether to tier, and what differentiation is for, before designing any tier. A tier exists only when something measurable changes at its boundary, and criteria and benefit delta are designed as a pair:
   - Criteria with no benefits delta is a leaderboard nobody plays.
   - A benefits delta with no criteria is favoritism wearing a logo.

   Hand the tier count, criteria, and benefit design to `mbfinotti/partnerships-skills@partner-tiering`, which owns all three: decide only whether to tier and what the differentiation is for here. Two tiers is the right instinct for a small or new program, and four is usually vanity, but that skill sets the count against partner-base size. Do not fix a number here that it will re-derive, or signed partner agreements get re-papered.

   Do not rank tier counts by efficiency here either, since a second order on this page would contradict the one that skill derives from a base size you do not yet know.

6. Set the program-wide economics envelope: partner margin must come out of a cost the partner takes off your hands ("if you're paying margin for work you would have done anyway, you're not buying anything"), and total program cost must fit inside gross margin. Neutralize direct-rep compensation on partner deals here, not later.

   Hand per-partner modeling to `mbfinotti/partnerships-skills@partner-economics`. See [references/economics-and-benchmarks.md](references/economics-and-benchmarks.md).

7. Fix governance: a named owner and reporting line, and a deal-registration/channel-conflict policy written before the first selling partner signs, not after the first dispute. Practitioners argue for CEO-reporting at early stage, since ownership under the sales chief imposes quarterly horizons on a function that matures over 2-3 years. Hand rule detail to the co-selling and conflict skills (see Reference).
8. Set the success horizon at design time: year 1 judged on leading indicators only (partners activated, first deals registered, time-to-first-deal), year 2 on partner-sourced pipeline, year 3 on material revenue share. The most common structural error in this field is judging a channel on direct-sales 30-90 day cycles; the horizon decision is part of the architecture, made now. Hand the measurement system itself to `mbfinotti/partnerships-skills@partner-performance`.
9. Present the architecture section by section - for each, 2-3 candidate approaches with trade-offs and an explicit recommendation - and validate each section with the user before moving to the next. Where the profession's own collaboration formats fit, propose them in the order that file ranks them - evidence bought per hour of coordination, leading with partner-hypothesis validation: [references/collaboration-formats.md](references/collaboration-formats.md).
10. After explicit approval on every section, emit the Program Architecture Spec (next section) and check it against the pass threshold. Iterate until it passes; if no architecture passes, recommend not launching and record why.
11. If your harness has persistent memory, memorize the approved architecture's key decisions, economics envelope, and gate answers - later tactical runs (tiering, enablement, performance) start from them instead of re-interviewing.

## The Program Architecture Spec

Deliver every from-scratch engagement as this artifact - a decision record the user can hand to finance, legal, and sales:

```
PROGRAM ARCHITECTURE - <company>, <date>
Readiness    : direct-motion evidence, ACV band, gross-margin headroom, named executive sponsor
Partner value: one-sentence partner value proposition + validation record (2-3 named
               prospective partners, what each confirmed or contradicted)
Motions      : which of referral / reseller / services-SI / technology, why each, and the
               efficiency order they were chosen in after re-ranking for this user; motions
               deleted by a constraint, and the trigger that would reopen each
First cohort : target size (~10), qualification bar (capability, capacity, coverage,
               commitment), activation milestone per partner
Tiers        : whether to tier + what differentiation is for; count set by partner-tiering,
               or "no tiers - revisit
               when <condition>"
Economics    : compensation shape per motion, program cost envelope vs gross margin,
               direct-rep comp neutrality statement
Governance   : owner + reporting line, deal-registration/conflict policy status
               (written before first selling partner)
Horizon      : year-1 leading indicators, year-2 pipeline expectation, year-3 revenue
               share target; review cadence and who judges
```

Three rules about the spec itself:

- **Every line carries a reason.** "Two tiers because the only motion is referral and nothing measurable changes at a third boundary" is reviewable; a bare tier count is not.
- **The validation record is not optional.** A partner value proposition that has never met a real prospective partner is a guess; the spec must name who it was tested on and what happened.
- **The spec has a pass threshold.** The economics must fit inside gross margin, the partner value proposition must have survived contact with 2-3 real prospective partners, and a named executive sponsor must exist. Iterate motions, tiers, or economics until all three hold - if no architecture passes, recommend not launching.

## Diagnosing an Existing Program

When the user arrives with a running program instead of a blank page ("we have 200 partners and no revenue"), diagnose structure before tactics. Several rows below usually apply at once; the table is a lookup, so the fix order is stated here rather than implied by row order:

- efficiency: `horizon reset > conflict and registration policy > activation over recruitment > funds mechanics > comp neutrality > tier rebuild`
- effort: `comp neutrality > tier rebuild > activation over recruitment > conflict and registration policy > funds mechanics > horizon reset`
- value: `comp neutrality > activation over recruitment > conflict and registration policy > tier rebuild > funds mechanics > horizon reset`
- compliance cost: `tier rebuild == comp neutrality > conflict and registration policy > all others` (tie argued: each reopens a signed instrument - partner agreements in one case, rep comp plans in the other - and neither rolls back without a second amendment)

Resetting the horizon leads because it costs one leadership conversation and stops the program being killed before any other fix can land. Comp neutrality is the highest-value fix and still not first: it is a mid-year comp change, slow and politically expensive. Re-rank against the user - a program with neutral comp already deletes that row, and a single-tier program deletes the tier rebuild.

| Symptom                            | Structural cause to check first                                                               |
| ---------------------------------- | --------------------------------------------------------------------------------------------- |
| Many signed partners, few active   | Recruitment tracked instead of activation; no partner value proposition ever validated        |
| Partners ignore tier progression   | Cosmetic tiers - nothing measurable changes at the boundary                                   |
| Program funds unclaimed            | Market-development funds designed apart from deal registration, claims friction               |
| Partners stopped registering deals | Vendor competes on registered deals (house accounts); conflict policy written after the fact  |
| Direct reps block partner deals    | Compensation penalizes partner involvement - an architecture decision, not a behavior problem |
| Program "failing" at month 6       | Horizon error: judged on direct-sales cycles; reset expectations to the year-1/2/3 ladder     |
| Overloaded partner managers        | Portfolio far beyond the sustainable range; program scaled recruitment before activation      |

Full failure catalog with fixes and a worked negative example: [references/readiness-and-failure-modes.md](references/readiness-and-failure-modes.md).

## B2B and B2C

Identical in both:

- Deep-qualify a small first cohort before scaling recruitment.
- Model the economics from the partner's side before setting any number.
- A compelling economic offer, not marketing, is what recruits.

Genuinely different:

- Franchising's legal instruments and exclusive territories.
- Day-one documentation depth: exhaustive in franchising, deliberately minimal in B2B SaaS.
- Consumer programs' point-of-sale attribution versus B2B's multi-month pipeline attribution.
- Front-line mindshare/findability requirements unique to consumer-facing dealers.

Details and reliability flags: [references/b2b-b2c-contrast.md](references/b2b-b2c-contrast.md).

## Invocation Examples

- "We have inbound partner requests and no formal program. Are we even ready for partners, and if so what should the program look like?"
- "Design a referral program for a $12K ACV product - we tried resellers and the margin math never worked."
- "Our partner program has requirements nobody meets and benefits nobody wants. Rebuild the structure from the readiness gate up."

## Reference

- See [references/decision-sequence-and-frameworks.md](references/decision-sequence-and-frameworks.md) for the full decision sequence, ACV-banded motion selection, and named frameworks with honest status flags.
- See [references/readiness-and-failure-modes.md](references/readiness-and-failure-modes.md) for the complete readiness gate and the failure-mode catalog.
- See [references/collaboration-formats.md](references/collaboration-formats.md) for how channel professionals actually workshop a program design.
- See [references/economics-and-benchmarks.md](references/economics-and-benchmarks.md) for the economics-envelope method and benchmark bands with reliability flags.
- See [references/b2b-b2c-contrast.md](references/b2b-b2c-contrast.md) for the dealer/franchise/ambassador contrast.
- See `mbfinotti/partnerships-skills@co-selling-strategy` for deal registration rules, credit splits, and engagement rules.
- See `mbfinotti/partnerships-skills@partner-channel-conflict` for direct-versus-partner conflict resolution.
