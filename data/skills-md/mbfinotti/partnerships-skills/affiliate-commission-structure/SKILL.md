---
name: affiliate-commission-structure
description: Design the commission and payout structure of a commission-based affiliate program: rate model (revenue share, flat CPA, hybrid), rate level derived from unit economics, payout tiers, recurring duration and caps, attribution/cookie window, validation, clawback, and payment terms. Covers B2B SaaS and B2C ecommerce programs with professional affiliates. Use whenever the user mentions an affiliate commission rate, commission tiers, lifetime vs 12-month recurring commission, a cookie window, or a rate-card migration, even if they only ask how much to pay affiliates. Do NOT use for end-customer refer-a-friend rewards - use mbfinotti/partnerships-skills@referral-incentive-design instead. Terms drafting, payout auditing, and fraud rules are separate skills.
license: MIT
metadata:
  author: Maya-Beth Finotti
  version: "1.2.7"
---

# Affiliate Commission Structure

Design the commission and payout structure of an affiliate program: rate model, rate level, tiers, recurring duration, attribution window, and validation/clawback/payment terms.

No named, proprietary framework exists for this discipline. Robert Glazer's _Performance Partnerships_ (2017) and Geno Prussakov's _Affiliate Program Management: An Hour a Day_ (2011) teach doctrine and process, not a branded algorithm. Prussakov's "5/80 rule" (5% of affiliates drive 80% of the work) is the one real, attributable coinage.

What exists instead is a convergent craft, taught in near-identical form across the industry:

- Derive a ceiling from unit economics.
- Set the headline rate below it.
- Differentiate by partner type and incrementality.
- Protect with validation and clawback.
- Reward top performers with tiers.

That derivation is this skill's spine - compute the rate from margin, never copy it from a benchmark.

## Interview

Run these rules before designing anything:

- One question per message.
- Offer multiple-choice answers when possible.
- Skip any question the user already answered.

- B2B SaaS or B2C ecommerce? Subscription or one-time purchase?
- Gross margin? Variable costs per order (COGS, fulfilment, shipping, payment processing, platform fees)?
- Expected return/refund rate (ecommerce) or monthly churn rate (SaaS)?
- AOV or entry-plan price? How wide is the AOV/ACV spread across products or plans?
- Customer LTV? Target CAC and current blended CAC?
- Existing commission rates, if any - and which partners are on them today?
- Which partner types are enrolled or wanted: content/review/comparison sites, coupon/cashback/loyalty, agencies/consultants, creators/influencers?
- Do you have competitor program terms to calibrate against?
- Has finance set a payout budget ceiling?
- What can tracking attribute: last-click cookies, server-side events, new-vs-existing-customer flag, recurring billing events per referred account?
- By what date must the new structure be live and showing results?
- A one-off fix (get this quarter's payouts back inside the ceiling) or a compounding asset (a rate card that survives three years of plan and catalog changes)?
- What is the effort ceiling: who administers the program week to week, and what can the affiliate platform actually express - per-product payout tables, a second rate step for a taper, a new-customer flag, per-partner attribution windows?

Missing margin, churn/return, and CAC answers block the derivation - insist on estimates before proposing any rate.

Those last three answers re-rank every option menu in this skill, and each ranking says which:

- A hard date promotes whatever is one field on the platform and demotes anything needing a negotiation or a tracking change.
- A compounding mandate promotes the derivation and the partner-type split, while a one-off mandate promotes duration and threshold changes that land this cycle.
- A low effort ceiling deletes the options the platform cannot express, rather than demoting them.

Every ordering below is a default, not a law: it shifts with context and with who executes it. Re-rank against what you already know about the user:

- An existing published rate card that network rules make expensive to cut.
- A platform that cannot express a taper.
- A narrow order-value spread.
- An in-house partner manager who can run the per-partner negotiations the default order assumes away.

## Workflow

1. Run the Interview. Collect every economic input before touching a number.
2. Derive the commission ceiling from unit economics - never from a competitor's rate:
   - **Ecommerce**: gross margin → subtract variable costs → contribution margin → net out expected returns → pay one-third to one-half of post-return contribution margin. Sanity band: total commission at 20-30% of gross margin.
   - **SaaS**: treat commission as part of CAC. Keep LTV:CAC ≥ ~3:1 and CAC payback ≤ ~12 months. Total lifetime commission per customer: 5-15% of LTV, never above 30-40% of gross margin.
   - Full worked math in [references/rate-derivation.md](references/rate-derivation.md).
3. Pick the rate model - `percentage of order/revenue > flat CPA > hybrid` on efficiency. Full axes, margin behaviour per model, and the constraints that delete an option: Rate Model section below.
4. For recurring revenue share (SaaS): fix the duration rule before the headline percentage - it moves effective cost far more than the percentage does. Default to a 12-month cap. Ranking and cost arithmetic are in Recurring Duration (SaaS) below.
5. Differentiate rates by partner type, driven by incrementality:
   - Content and creator partners run ~78-82% incremental.
   - Coupon/cashback partners are often 66-71% non-incremental: they capture last-click credit on demand others created.
   - Apply the controls in efficiency order: `new-customer gate > rate cap below content > shorter attribution window > exclusive codes`.
   - Delete the gate from the menu when tracking has no new-customer flag, which promotes the rate cap to first.
   - Applies identically to B2B and B2C: only the partner mix differs.
   - Axes in [references/partner-types-and-tiers.md](references/partner-types-and-tiers.md).
6. Decide tiers - `flat > marginal tiers > retroactive tiers` on efficiency. Launch flat: with no historical performance data there is nowhere to place a breakpoint, which deletes both tiered options rather than demoting them. Axes and mechanics in [references/partner-types-and-tiers.md](references/partner-types-and-tiers.md).
7. Set the payout terms that belong to the structure (details below):
   - Attribution window
   - Validation/locking period
   - Net payment terms
   - Minimum threshold
   - Clawback clause
8. Check the pass threshold (below). Iterate the levers in the efficiency order given in [references/rate-derivation.md](references/rate-derivation.md) until it holds. If nothing passes, narrow the program to high-margin SKUs or plans first, and recommend not launching only when no narrowing leaves a ceiling partners will work for.
9. Calibrate against benchmarks only after deriving - [references/benchmarks.md](references/benchmarks.md). A derived rate far below the vertical's norm predicts a recruiting problem, not a math error. If you can browse the web, verify any competitor's published terms on its live page - third-party directories often cite stale cookie windows and rates.
10. Present the decisions one section at a time - options, trade-offs, recommendation - and validate each with the user before moving on. After approval, emit the full commission structure spec (below).
11. If your harness has persistent memory, memorize the approved spec's key decisions and economics (ceiling, rates per partner type, duration, windows) so a later revision run starts from them instead of re-interviewing.

## Rate Model

All three models are sized to the same ceiling from step 2 - the model decides who gets paid what inside it, not what the program costs in total. So rank it on effort and reversibility, never on headline generosity.

- efficiency: percentage of order/revenue > flat CPA > hybrid
- value: percentage > flat CPA on a narrow order-value spread, and flat CPA > percentage once the spread is wide, while hybrid > both only for a publisher that refuses pure performance
- effort: hybrid > flat CPA > percentage
- compliance cost: hybrid > flat CPA == percentage - publishing any rate card is already a contractual commitment bound by network decrease rules, which is why those two tie, and only hybrid adds a signed placement contract with its own term on top

| Model                                              | What it buys                                                              | Effort                                                                                                           | Margin behaviour                                                                                                                                                |
| -------------------------------------------------- | ------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Percentage of order/revenue** (default)          | incentive alignment across the whole partner base                         | near-zero - one field on every affiliate platform                                                                | effective rate is constant by construction, so the step-2 ceiling holds at every order size                                                                     |
| **Flat CPA**                                       | protects unit economics where a percentage would overpay large orders     | an hour to derive the payout table, then a standing job to re-derive it whenever plan prices or the catalog move | effective rate swings inversely with order value - across a 25x catalog spread, one payout sits far above the ceiling at the bottom and far below it at the top |
| **Hybrid** (flat placement fee + lower percentage) | access to high-authority publishers who will not work on pure performance | a week of negotiation per partner, then off-platform invoicing and reconciliation every cycle                    | the fee is paid before any conversion, so it is the only model whose cost the ceiling derivation does not bound                                                 |

What this order starves: hybrid. It is the only model that lands a publisher refusing pure performance, the top of the value line for that one job. But it costs a week of negotiation per partner plus off-platform invoicing every cycle, so the ratio buries it in every round it is eligible for.

Promote it deliberately, rather than waiting for a round it cannot win, when a named high-authority publisher has already refused a performance-only deal and the program has the negotiation hours. Say out loud that the fee sits outside the step-2 ceiling: nothing else in this section does.

Constraints delete an option, they do not demote it:

- Narrow order-value spread, or a platform with no per-product payout table: flat CPA leaves the menu - do not present it as an alternative.
- No publisher asking for a placement fee: hybrid leaves the menu - it exists only for that negotiation.
- A hard launch date leaves percentage alone: hybrid cannot close inside one.

## Recurring Duration (SaaS)

Rank the duration rule before negotiating the percentage - it moves effective cost far more than the headline does (arithmetic in [references/rate-derivation.md](references/rate-derivation.md)).

- efficiency: 12-month cap > taper > renewal bonus > lifetime
- cost: on a 30% headline over a 20-month tenure, lifetime pays 30.0% of customer revenue, the cap 18.0%, the taper 13.5% - the renewal bonus sits lowest of all because it only pays on revenue that actually renewed
- value (recruiting pull): lifetime > 12-month cap > taper > renewal bonus - partners compare headline and duration together, and the taper spends its headline in the first six months
- effort: renewal bonus > taper > lifetime == 12-month cap - the last two tie because each is a single duration field and nothing else, while the taper needs a second rate step and the bonus a renewal-event trigger, both of which many platforms cannot express, leaving a standing manual reconciliation
- compliance cost: lifetime > renewal bonus > taper == cap - published lifetime terms commit to an open-ended liability, and retracting one later runs into network decrease caps plus grandfathering for every partner already on it

What this order starves: the taper and the renewal bonus. Both cost less per acquired customer than the cap. On the same 30% headline the taper pays 13.5% of customer revenue against the cap's 18.0%, and the bonus pays only on revenue that renewed.

Yet the cap wins the ratio because it is one duration field. Each of the other two needs a second rate step or a renewal-event trigger, and, on a platform that cannot express it, a standing manual reconciliation. Promote the taper or the bonus above the cap when the payout budget rather than manager hours is the binding constraint, and the platform expresses the mechanic natively.

- Default to a 12-month cap. Use 24 months when recruiting against generous competitors.
- Lifetime is off the menu unless all three hold: gross margin > ~80%, monthly churn < ~5%, and competing programs pay lifetime. Below that bar it is deleted, not demoted - do not price it and do not offer it as the generous option.
- A platform that cannot express a second rate step deletes the taper. The renewal bonus takes its place, or the plain cap does.
- Prefer a renewal bonus (5-10% of renewal value) over uncapped lifetime - keeps partners engaged past the cap without the open-ended liability.
- Pay recurring commission in arrears on confirmed billing events, so churned customers stop costing automatically.
- Uncapped lifetime on a sticky product is a balance-sheet trap: a seven-year customer can earn an affiliate more than that customer's margin.
- B2C ecommerce: recurring duration rarely applies, since commissions are one-shot per order. Skip this section unless the product is a subscription box.

## Payout Terms in the Structure

These terms are part of the rate design, not legal boilerplate - each one changes the effective cost and the program's competitiveness.

- **Attribution/cookie window**: varies by traffic type.
  - 24 hours-7 days for impulse and coupon traffic.
  - 30 days as the ecommerce default.
  - 60-180 days for B2B SaaS with long sales cycles.
  - Set coupon/cashback partners shorter than content partners.

  Deliberately unranked: these are per-traffic-type defaults, not competing answers to one question - a coupon partner and a B2B content partner never take the same window at any effort budget.

- **Validation/locking**: hold commissions pending 30-60 days. B2C: tie it to the return/refund window. B2B SaaS: tie it to trial-to-paid conversion plus the refund window.
- **Payment terms**: net-30 default. Note the stacking cost: 30-day validation plus net-30 already means affiliates wait ~2-4 months for cash.
- **Minimum threshold**: $50-100.
- **Clawback**: refund, chargeback, or in-window cancellation voids the commission. If already paid, deduct from the next payout and carry negative balances forward. Payout rails rarely reverse a paid commission automatically - a clawback must be explicitly triggered, so write the mechanism into operations, not just the terms.
- Net terms, thresholds, and clawback mechanics work the same for B2B and B2C. Only the window lengths and validation triggers differ.

Payout speed is a recruiting lever - slower terms lose partners to faster-paying rivals - and three levers pull on it. Rank them before shortening anything:

- efficiency: lower the minimum threshold > shorten net terms > shorten validation
- value (speed the partner actually feels): shorten validation > shorten net terms > lower threshold
- effort: shorten net terms > lower threshold == shorten validation - the last two tie because each is a single field, while net terms change the finance cadence every cycle
- reversibility cost: shorten validation > shorten net terms > lower threshold - a shortened validation window pays commissions before refunds land, and a paid commission comes back only through a manual clawback

Lowering the threshold adds no risk at all - the money is owed either way - and it is the lever small and new partners feel first. Shorten validation last, and only once the reversal rate is measured and low.

## Migrating an Existing Rate Card

1. Derive the target structure first - a migration to a copied rate repeats the original mistake.
2. Lead every announcement with what stays the same.
3. Give advance notice: 60 days for tier or rate changes. Never change rates silently - silent migrations are a documented cause of partner churn.
4. Grandfather existing affiliates at the old rate, high performers for at least one cycle.
5. Phase the rollout top-partners-first, with direct conversations before the broadcast.
6. Check network guardrails before cutting rates - networks contractually cap the size, frequency, and notice period of decreases (verbatim example in [references/partner-types-and-tiers.md](references/partner-types-and-tiers.md)).

## The Commission Structure Spec

Deliver every engagement as this artifact - a decision record with a reason on every line, ready for finance and partner-facing docs:

```
COMMISSION STRUCTURE - <program>, <date>
Rate model        : % of order | flat CPA | recurring rev-share | hybrid, and why
Headline rates    : per partner type (content / coupon-cashback / agency / creator), each with its reason
Tiers             : marginal breakpoints + measurement window + reset rule, or "flat - revisit when <condition>"
Recurring duration: cap (e.g. 12 months) or taper or lifetime + renewal bonus, with the margin/churn justification
Attribution       : cookie/window length per partner type, new-customer gating
Validation        : locking period + what event releases it (return window / trial-to-paid)
Payment           : net terms, minimum threshold, clawback clause + negative-balance carry-forward
Economics         : ceiling computation shown; projected cost per acquired customer vs current blended CAC
Validation plan   : 30-day holdout on top coupon partners; new-customer share tracking
KPIs              : cost per incremental affiliate customer vs blended CAC, effective commission rate,
                    new-customer share, reversal/clawback rate, revenue share of top 10% partners
```

- **Every line carries a reason.** "25% for 12 months = 13% of LTV, inside the 5-15% band" is reviewable. A bare percentage is not.
- **The spec has a pass threshold.** Projected blended cost per incremental affiliate-acquired customer must sit below current blended CAC AND inside the computed margin ceiling. Iterate the levers in their efficiency order until both hold. If nothing passes, narrow to high-margin SKUs/plans, and recommend not launching only when that fails too.
- **The validation plan is not optional.** Last-click attribution structurally overpays bottom-funnel partners. The holdout test is how the spec proves its incrementality assumption.

Worked B2B SaaS and B2C ecommerce specs, plus a negative example, in [references/spec-and-examples.md](references/spec-and-examples.md).

## Failure Modes

| Failure                                       | Why it happens                                                                       | Fix                                                                                                                    |
| --------------------------------------------- | ------------------------------------------------------------------------------------ | ---------------------------------------------------------------------------------------------------------------------- |
| Rate above contribution margin                | Copied from a benchmark instead of derived; loss surfaces only after returns net out | Re-derive the ceiling; cut rate or narrow to high-margin SKUs                                                          |
| Tier cliff demotivates or invites junk volume | Retroactive tier near a breakpoint; partner at 49/50 pushes low-quality sign-ups     | Marginal tiers; breakpoints from historical data                                                                       |
| Uncapped lifetime outlives customer margin    | Lifetime used as a recruiting weapon on a sticky product                             | 12-month cap + renewal bonus; buy out legacy lifetime streams                                                          |
| Overpaying coupon/loyalty partners            | Last-click credits bottom-funnel clicks on demand others created                     | In order: new-customer gate, cap below content rates, shorter window; exclusive codes and the holdout test to prove it |
| Partner churn after a rate change             | Silent or abrupt migration breaks trust and tracking                                 | Notice, grandfathering, top-partner-first phasing                                                                      |
| Flat percentage over a wide AOV spread        | One big order wipes out unit economics                                               | Flat CPA, or percentage banded by product/plan                                                                         |

One honesty note: the best-sourced program data shows most affiliate programs stall on partner activation, not rate miscalibration - a perfectly derived structure does not rescue a program nobody promotes. Flag this when the user's real problem is recruitment or engagement.

## Invocation Examples

- "We pay 20% recurring forever and finance says it is too expensive - rework the structure. $79/mo plan, 82% margin, 16-month average tenure."
- "Set the commission rate for a new B2C ecommerce affiliate program. AOV $65, 44% contribution margin after returns, and we want coupon partners on a lower rate than content partners."
- "Design payout tiers that reward our top 10 affiliates without blowing the LTV ceiling - here are last year's per-affiliate revenue numbers."

## Reference

- See [references/rate-derivation.md](references/rate-derivation.md) for the two ceiling calculations, the lifetime-vs-cap-vs-taper cost comparison, and the pass-threshold math.
- See [references/benchmarks.md](references/benchmarks.md) for vertical rate tables, cookie-window norms, validation/net-terms/threshold norms, and published program terms - each with source, date, and reliability flag.
- See [references/partner-types-and-tiers.md](references/partner-types-and-tiers.md) for incrementality-based rate differentiation, the holdout test, tier mechanics, and migration guardrails.
- See [references/spec-and-examples.md](references/spec-and-examples.md) for one worked B2B SaaS spec, one worked B2C ecommerce spec, and a negative example that fails the threshold.
- See `mbfinotti/partnerships-skills@partner-economics` for a full channel-partner P&L beyond affiliate rates.
- See `mbfinotti/partnerships-skills@affiliate-program-terms` for drafting the T&C document that encodes this structure.
- See `mbfinotti/partnerships-skills@affiliate-payout-audit` for auditing a payout run downstream of this design.
- See `mbfinotti/partnerships-skills@affiliate-fraud-detection` for the fraud ruleset - this skill only flags where a structure creates fraud incentives.
