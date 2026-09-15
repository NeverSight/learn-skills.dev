---
name: app-marketplace-monetization-model
description: Design how a B2B SaaS app/connector marketplace makes money, operator side - merchant-of-record posture (marketplace-billed vs developer-billed), billing rails and account configuration, the fee stack (revenue share collected at source, program fees, processing pass-through), fee waivers and incentive tiers, payout cadence and hold windows, and the marketplace-facilitator/VAT tax layer. Use whenever the user mentions charging for apps, rev-share collection, paid-app billing or billing APIs, developer payouts, fee waivers, or merchant of record - even if they never say "marketplace monetization". Mechanics layer only. Do NOT use for take-rate level and tiers - use samber/developer-platform-skills@connector-marketplace-strategy instead.
license: MIT
metadata:
  author: Samuel Berthe
  version: "1.0.0"
---

# App Marketplace Monetization Model

You are a marketplace-monetization designer advising the team that operates a B2B SaaS platform's app or connector marketplace. The strategy layer has (or should have) already set the take-rate level and tier architecture. This skill designs the machinery underneath it:

- Who bills the end customer
- How the platform's cut is collected
- What developers can charge
- When they get paid
- Who owes which tax, where

The output is a monetization design the platform team can implement and publish to its developers.

One question structures everything else: **who is merchant of record** - the marketplace, or each app developer. Fix it first; every later section is a sub-decision of it. Across every platform, that single choice determines:

- Tax liability
- Chargeback ownership
- Available developer pricing models
- How payouts work

## Interview

Ask these before proposing anything. One question per message, multiple-choice where offered - each answer moves a rung in the menus below, and batching them buries the one answer that changes the design.

1. Is the take-rate architecture already decided (level, tiers, zero-take-or-not)? If not, stop and run `samber/developer-platform-skills@connector-marketplace-strategy` first - this skill executes that decision, it doesn't make it.
2. Do you already bill these end customers on a recurring invoice or settlement cycle for your core product?
3. Which pricing models must developers be able to offer? (a) flat subscription (b) per-seat (c) usage-based/metered (d) one-time (e) free with paid tiers.
4. What billing engineering exists in-house - a full billing stack, a managed payment-rails provider, or neither?
5. Where do buyers sit - US only, EU, beyond? And are any end buyers consumers rather than businesses? (This changes the tax layer, not the rest.)
6. What loss appetite do you have - will the platform absorb chargebacks, refunds, and fraud losses, or must developers carry their own?
7. Is there an existing population of apps already billing customers directly that you cannot migrate in one cycle?
8. By when must the model be live - a hard date, or open-ended?
9. Is this a one-off unlock (start collecting the agreed rate) or a compounding asset (billing infrastructure you'll extend)?
10. What is the effort ceiling - billing/payments engineering hours, compliance and legal review capacity, appetite for carrying financial risk?

Questions 8-10 exist because the menus below diverge sharply on time-to-effect, durability, and effort - the default rankings cannot pick for the user.

- A hard date promotes managed rails and the simplest posture.
- A compounding mandate promotes owning more of the stack.
- A low effort ceiling deletes the configurable-per-app posture outright rather than demoting it.

## Where B2B vs B2C actually matters here

The operator this skill serves is a B2B SaaS platform, and most of the design does not split on whether its end buyers are businesses or consumers - merchant-of-record posture, fee stack, and payout mechanics work the same. The one layer that genuinely splits is tax: the EU's deemed-supplier VAT rule attaches to B2C supplies specifically (B2B cross-border VAT is typically reverse-charged to the business buyer instead), and US marketplace-facilitator statutes exist because states wanted consumer sales tax collected at the platform.

- A marketplace with any consumer-facing apps treats question 5's answer as a tax-design input, not demographic trivia.
- A purely B2B-buyer marketplace gets a lighter version of step 7, not a different skill.

## Workflow

1. Confirm the take-rate architecture from the strategy layer (interview question 1).
2. Fix the merchant-of-record posture.
3. Configure the billing rails and account dimensions behind that posture.
4. Compose the fee stack that implements the take-rate.
5. Set the pricing-model menu developers get - after checking the rails support it.
6. Design fee waivers and incentives.
7. Design payout cadence, holds, and thresholds; publish the sale-to-bank timeline.
8. Map the tax layer jurisdiction by jurisdiction and publish the split.
9. Write the enforcement rules and notice commitments.
10. Check the design against the measurement gates.

Draft the design section by section in that order, validating each with the user before the next - a merchant-of-record assumption caught at step 2 is cheap; the same assumption discovered at step 8 rewrites the tax map and the payout system together. Re-rank every menu below against what you know about this user before presenting it: an in-house billing platform, an existing invoice cycle, a legacy developer-billed population, or a hard date each move rungs. The defaults are defaults, not laws.

## 2. Merchant-of-record posture

Three postures, ranked. Mechanics, platform-by-platform postures, and the underlying charge patterns: [references/mor-and-billing-rails.md](references/mor-and-billing-rails.md).

- effort (descending): `configurable per app > marketplace-billed > developer-billed`
- developer-adoption value (descending): `marketplace-billed > configurable per app > developer-billed`
- compliance cost (descending): `configurable per app > marketplace-billed > developer-billed` - the configurable posture papers two tax postures and two liability models at once, so every review runs twice and each app's posture is a commitment to that developer; marketplace-billed triggers tax registration and remittance wherever you sell plus card-network merchant obligations, and unwinding it means re-billing live customers and re-papering developer agreements; developer-billed pushes registration and disputes onto each developer, but facilitator and deemed-supplier statutes still attach by law (step 8) - a lighter review, never none.
- efficiency: `developer-billed while zero-take > marketplace-billed once charging > configurable per app`

- **Default rung: developer-billed (vendor-as-MoR) - but only while the take-rate is zero.** Each developer bills its own customers and carries its own tax, disputes, and dunning; the marketplace builds almost nothing. When the strategy layer chose zero-take as a retention asset, there is no cut to collect, so building collection machinery buys nothing.
- **Promotion condition: the moment a take-rate is charged, promote to marketplace-billed (platform-as-MoR).** Collection at source - netting the platform's share out of money that already flows through it - is the only collection mechanism that doesn't depend on developer self-reporting, and it is what lets the marketplace bundle tax handling, chargeback absorption, and billing automation into its developer pitch. Every mature charging marketplace in the sourced landscape converged here. When you already bill these customers on a cycle (question 2), the strongest variant is consolidating app charges onto that existing invoice - one bill for the customer, near-zero marginal checkout build.
- **Starved option: configurable per app (both postures at once).** It runs two billing branches, two tax postures, two payout systems, and doubled developer documentation, so it loses every efficiency round. Question 7 promotes it anyway: a legacy developer-billed population that can't migrate in one cycle forces running both - and the one sourced platform doing this treats the developer-billed branch as a closing legacy path with a stated end direction, not a permanent choice it offers new developers. If question 7 is a clean no, delete this rung from the discussion entirely.

Marketplace-billed is the high-effort, high-value rung - it wins on value and on efficiency-once-charging simultaneously, which is why the promotion condition is about when, not whether.

## 3. Billing rails

Under a marketplace-billed posture, three dials configure the rails:

- Who the end customer's charge is created against
- Who absorbs unresolved losses
- What dashboard the developer sees

The sourced rails provider exposes them independently, but the compatibility matrix collapses them into two coherent bundles: a marketplace-shaped bundle (platform owns the charge, the losses, and a lightweight branded developer view) and a SaaS-shaped bundle (developer owns all three). À-la-carte combinations outside those bundles are blocked or silently shift liability. Pick the bundle matching the step 2 posture; per-dial detail and the payout-timing patterns each bundle allows are in [references/mor-and-billing-rails.md](references/mor-and-billing-rails.md).

Whatever the rails, budget their real cost against the take-rate: managed marketplace rails carry per-account and per-payout fees on top of processing, and at low per-developer volume those flat fees can outweigh the percentage collected. Build the unit economics per active developer, not per transaction.

## 4. Fee-stack composition

The take-rate level and tiers come from the strategy layer; this step decides which instruments collect it. Four instruments, ranked. Named fee stacks with figures and dates: [references/fee-stack-and-incentives.md](references/fee-stack-and-incentives.md).

- collection effort (descending): `audited self-reported share > revenue share netted at source > flat program fees == processing pass-through`
- revenue and enforcement value (descending): `revenue share netted at source > audited self-reported share > flat program fees > processing pass-through`
- efficiency: `revenue share netted at source > flat program fees > processing pass-through > audited self-reported share`

- **Default rung: revenue share netted at source.** Once marketplace-billed, the platform's cut is deducted before payout - no invoicing, no audit, no chasing. Its build sits upstream in step 3, so what remains here is netting and reconciliation: more setup than a flat charge, far less than a standing audit function, and it collects a percentage neither flat instrument can.
- **Flat program fees** (one-time registration, per-app review fee, annual listing fee) complement the share where they price a real cost or filter low-intent submissions - the sourced stacks charge a review fee that funds the security review and a registration fee small enough to deter spam without deterring developers. The `==` with processing pass-through is genuine: both are simple flat charges with no per-transaction machinery.
- **Processing pass-through**: keep payment-processing cost a separately labeled flat line, as the sourced marketplaces do, rather than burying it inside the share - a share that silently includes processing reads as a higher take than it is, and can't be compared honestly against competitors' headline rates.
- **Starved option: audited self-reported share.** Under a developer-billed posture it is the only way to collect a percentage, and it loses every round on enforcement - the platform learns its own revenue from numbers the payer reports. It is a fallback forced by posture, never a choice; if step 2 landed on marketplace-billed, delete it. Where it must exist, it needs the anti-circumvention rule and delisting path from step 9 more than any other instrument.

## 5. Pricing-model menu for developers

Decide which of question 3's models the marketplace supports:

- Flat subscription
- Per-seat
- Usage-based
- One-time
- Free with paid tiers

This menu is deliberately unranked: developer demand and rails capability decide it jointly, so there is no operator trade-off left for an efficiency order to resolve.

The trap is ordering: the rails choice caps this menu, not the other way around. One sourced enterprise marketplace's checkout supports only one-time and subscription - no usage-based - so developers wanting consumption pricing simply can't offer it there; another platform's billing supports recurring, usage-based, and one-time charges natively. Verify each promised model against the step 3 rails before publishing the menu, and treat usage-based as a maturity ladder (simple metering versus dimensional, contract-grade metering) rather than one feature - scope which rung developers actually need.

Two rules are worth adopting whatever the rails:

- Model each pricing tier as its own product object, never as price-variants of one product: variants of one product become indistinguishable on customer invoices.
- Let the marketplace recommend defaults, such as free trials or an entry plan, rather than mandate them. This is how the sourced platforms shape pricing adoption without owning developers' pricing decisions.

## 6. Fee waivers and incentives

Waivers are now a standard menu item across major marketplaces, not an exceptional discount - expect to offer at least one shape. Three shapes, ranked; program details and dates in [references/fee-stack-and-incentives.md](references/fee-stack-and-incentives.md).

- effort (descending): `migration incentive > behavior-based discount > revenue-exemption tier`
- supply-breadth value (descending): `revenue-exemption tier > migration incentive > behavior-based discount`
- steering value (descending): `behavior-based discount == migration incentive > revenue-exemption tier`
- efficiency: `revenue-exemption tier > behavior-based discount > migration incentive`

- **Default rung: a revenue-exemption tier** - zero or reduced share below a revenue threshold. The sourced programs cluster tightly around a $1M threshold (annual for most, lifetime for one), so anchor there rather than inventing a number; the honest variation to decide is annual-reset versus lifetime, a one-way tightening one platform made explicit. Default eligible developers in automatically: two major programs require manual enrollment, and a qualifying developer who misses it silently pays the full rate - an opt-in waiver changes paper, not behavior.
- **Promote behavior-based discounts** (a lower rate for a pricing or architecture choice - subscriptions over one-time, the platform's preferred framework over a legacy one) when you have a specific choice to steer developers toward. The `==` with migration incentives is argued: both pay for a named choice rather than a revenue level - one prospective, one retrospective.
- **Starved option: migration incentives** - waived or discounted fees for moving existing off-marketplace agreements or legacy-architecture apps onto the marketplace. Verification, attestation, and eligibility tooling make it the costliest shape, and it loses every efficiency round. A measurable back-book of existing off-platform revenue promotes it anyway: the sourced cases use differential rates as a migration lever worth more than the waived fees, pairing an accelerated benefit on the preferred path with a deferred increase on the legacy one. With no back-book to migrate, delete this shape from the menu rather than parking it at the bottom.

## 7. Payout design

Four cadences, ranked. The seven-platform payout comparison behind these rungs: [references/payout-and-tax-mechanics.md](references/payout-and-tax-mechanics.md).

- operator risk and effort (descending): `instant for a fee > rolling with reserves > monthly plus hold window > invoice-cycle consolidation`
- developer cash-flow value (descending): `instant for a fee > rolling with reserves > monthly plus hold window == invoice-cycle consolidation`
- efficiency: `monthly plus hold window > invoice-cycle consolidation > rolling with reserves > instant for a fee`

- **Default rung: monthly cycle plus an explicit hold window** sized to your refund/chargeback exposure - the norm across the sourced platform-as-MoR stores, whose holds run roughly thirty to sixty days. The `==` on value is argued: consolidation and monthly-plus-hold both land developer money in the same order of magnitude - weeks from sale to bank - so developers feel no difference between them.
- **Invoice-cycle consolidation** outranks the default on efficiency when question 2 is yes: app payouts riding the settlement cycle you already run cost near-zero marginal build. It only exists behind that precondition - without an existing cycle, delete it.
- **Promote to rolling payouts with reserves** (daily or weekly, with a percentage held on a rolling window against disputes) when you compete for supply against faster-paying alternatives - managed rails make this the fastest configurable shape.
- **Starved option: instant payouts for a fee.** Highest developer value, and it loses every round on operator risk and cost. A supply side of small developers for whom cash flow is the binding adoption constraint promotes it - as an option layered on a slower default, never as the default.

Two rules apply whatever the rung:

- The cash-flow lever developers actually feel is the hold window, not the minimum payout threshold. Sourced thresholds are small enough that active developers clear them every cycle, while real sale-to-bank lags run weeks past the headline "monthly" language. Publish the honest end-to-end timeline.
- Under marketplace-billed, the platform owns cross-border mechanics, such as payout currency conversion and rail choice, as part of the posture. Budget it, don't discover it.

## 8. The tax layer

Tax is a separate legal layer that can override the step 2 posture: US marketplace-facilitator statutes (in most sales-tax states since the 2018 _Wayfair_ decision) and the EU's deemed-supplier VAT rule can force the platform to collect and remit tax on transactions it doesn't bill. Marketplace-facilitator or deemed-supplier status is tax law; merchant of record is card-network status - they are legally distinct and don't always coincide, a distinction the sourced rails provider's own documentation states verbatim.

The design deliverable is a published, jurisdiction-by-jurisdiction split of who handles which tax, never a single "we handle tax" or "you handle tax" toggle. The sourced counter-examples make the point: one platform splits by country (platform-managed in some, developer-managed in others), another by tax regime (platform collects US sales tax, developers keep VAT liability).

Detail, legal framework summaries, and the silent-failure trap live in [references/payout-and-tax-mechanics.md](references/payout-and-tax-mechanics.md). This skill is not tax advice: route the published split through qualified counsel before shipping it.

## 9. Enforcement and notice

Every percentage instrument needs two enforcement commitments.

- **Anti-circumvention rule.** Routing billing around the marketplace to dodge the share is a terms violation, backed by a delisting path. The sourced precedent is high-revenue apps rerouting payments through an external processor and reversing only under delisting threat: circumvention pressure rises with the rate, and a rule without a removal path is a preference.
- **Notice period for fee changes, committed in writing.** The sourced pattern is six months for standard-rate changes, with unfavorable changes deferred and favorable ones accelerated. Publish it with the fee schedule.

## 10. Measurement

The design passes when three gates hold - self-set from the sourced rules above, since no industry pass-standard exists for a monetization-design artifact; iterate until all three pass:

1. The merchant-of-record posture is stated per app population, with tax, chargeback, and payout ownership each explicitly assigned - no transaction type left ambiguous.
2. Every fee instrument names its collection mechanism, its enforcement pair, and its notice commitment in writing.
3. The published developer docs state the end-to-end sale-to-bank payout timeline and the jurisdiction-by-jurisdiction tax split.

Post-launch, track:

- Net take revenue against billing-ops cost (the model's actual margin, not its headline rate)
- Median sale-to-bank days against the published timeline
- Dispute and chargeback rate, with losses attributed to whoever the posture assigned them
- Waiver coverage among eligible developers (an enrollment gap means the default-in rule failed)
- Tax-registration coverage of transaction volume
- Circumvention incidents, with their resolution

Baseline against your own first quarter: the platform figures in the references are context, not targets.

If your harness has persistent memory, record these decisions so later runs (fee changes, new jurisdiction, payout renegotiation) inherit them instead of re-deriving them:

- The chosen posture
- The rails bundle
- Each menu's chosen rung, with its promotion condition
- The published notice period
- The tax split

## Failure modes

- **Tax-layer/MoR confusion.** Choosing developer-billed and assuming tax went with it - facilitator and deemed-supplier obligations attach by law regardless of billing posture. Fix: step 8's published split, checked by counsel.
- **Silent zero-tax collection.** Automatic tax calculation with no active registration in a jurisdiction collects nothing, returns no error, and cannot be retroactively corrected. Verify tax collection as its own monitored system - watching payouts won't surface it.
- **Liability mismatch in the rails.** Picking rails dials à la carte outside the two coherent bundles leaves the platform carrying dispute losses it believes it pushed to developers. Fix: pick a bundle in step 3, never dials.
- **Rails capping the pricing menu.** Promising developers usage-based pricing before confirming the checkout supports it - the sourced enterprise marketplace's checkout doesn't. Fix: step 5's verify-before-publish order.
- **Circumvention with no enforcement pair.** A share with no anti-circumvention rule and delisting path erodes exactly as fast as the rate makes rerouting worth it.
- **The opt-in waiver.** A manual-enrollment exemption silently charges qualifying developers full rate; the program exists on paper and changes nothing. Default eligible developers in.
- **Rate changes without notice.** An unannounced increase burns partner trust the marketplace spent years buying; adopt the six-months-notice pattern before the first change, not after the backlash.
- **Modeling cash flow on headline language.** "Monthly payouts" reads as thirty days; sourced sale-to-bank lags run to twice that once holds and escrows stack. Publish and plan on the real number.

## Invocation examples

- "We're adding paid apps to our marketplace - should we bill customers ourselves or let developers charge directly, and what does each choice mean for tax and chargebacks?"
- "Our marketplace take-rate is set at 15% above a revenue threshold - design how it actually gets collected, paid out, and enforced."
- "Design our marketplace fee stack and payout schedule: rev-share collection, a small-developer waiver, and a sale-to-bank timeline we can publish to partners."

## References

- [references/mor-and-billing-rails.md](references/mor-and-billing-rails.md) - the merchant-of-record taxonomy table, charge patterns and account-configuration bundles, per-platform postures, and the tax-vs-MoR legal distinction.
- [references/fee-stack-and-incentives.md](references/fee-stack-and-incentives.md) - named fee stacks with figures and dates, the waiver-program taxonomy, and enforcement precedents.
- [references/payout-and-tax-mechanics.md](references/payout-and-tax-mechanics.md) - the seven-platform payout comparison, holds and thresholds, cross-border handling, and the US/EU tax-law frameworks.

See also, same collection:

- `samber/developer-platform-skills@app-marketplace-review` - the review and approval process a per-app review fee funds.
- `samber/developer-platform-skills@app-marketplace-listing-standards` - listing quality standards and the approval rubric, separate from what a listing costs.
- `samber/developer-platform-skills@app-marketplace-launch-marketing` - launch and co-marketing budgets for the marketplace, spend rather than revenue design.
- `samber/developer-platform-skills@partner-app-onboarding` - the partner journey where registration fees and seller agreements actually land on developers.
