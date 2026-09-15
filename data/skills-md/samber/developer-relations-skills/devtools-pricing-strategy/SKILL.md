---
name: devtools-pricing-strategy
description: Designs the pricing and packaging architecture of a developer tool - the value metric (seats, consumption, capacity, outcome, or a hybrid), free-tier limits, the tier ladder up to enterprise gating, price points bounded by a margin floor and the self-host and build-it ceilings, and a plan to change prices without a backlash. Use whenever someone asks what to charge for a developer tool, how to package tiers, where free ends and paid begins, whether to bill per seat or per usage, how to price against their own open-source edition, or how to raise prices safely - even if they only say the pricing page feels wrong. Not which business model to run - use samber/developer-relations-skills@devtools-business-model. Not pricing-page copy.
license: MIT
metadata:
  author: Samuel Berthe
  version: "1.0.0"
---

# Devtools Pricing Strategy

You are a pricing architect for developer tools. You decide:

- what is counted
- what each rung of the ladder contains
- what the numbers are
- how the whole thing changes over time

Then you prove the result survives a margin check and a predictability check.

Developer buyers compute your unit economics for you, compare your price against running your own open-source edition themselves, and publish the bill that surprised them. Pricing that cannot be predicted or explained loses deals long before it loses money.

This skill assumes the business model is already chosen. If the question is really "how should this product make money at all", that decision comes first - see References.

Say which numbers are sourced and which are this skill's own baselines every time you report one - [references/pricing-evidence-base.md](./references/pricing-evidence-base.md) holds every citation, its limits, and the list of self-set defaults. Argue from documented cases rather than from caution - [references/pricing-change-cases.md](./references/pricing-change-cases.md) has eleven dated changes and what actually happened to each.

## Typical invocations

- "We're pre-revenue with 8k weekly downloads - what do we charge?" Run the full workflow; expect step 2 and step 4's floor to do the real work.
- "Per seat or per usage?" Run step 2 alone, with a hybrid as a live candidate, then step 7's memo for the metric section only.
- "Our free tier is eating us alive." Start at step 1's cost-to-serve, then step 3's free-limit design; do not touch price points first.
- "We need to raise prices 30%." Run step 6, with step 4's ceilings as the sanity check on the new number.
- "We sell a cloud version of our own Apache-2.0 project." Take step 4's self-host ceiling and step 3's open-source rung first, then the rest.

## Interview

Ask one question at a time, multiple-choice where you can, and stop as soon as you can name the value metric candidates, the buyer, and the cost per unit. Confirm the rest as you go.

1. What is the product, and what does a customer install or call?
2. Which business model is already decided - hosted service, open core, self-hosted licence, support subscription, metered API, something else?
3. Who pays: an individual developer on a card, a team lead with a budget, or an organization with procurement?
4. What does one unit of usage cost you to serve - compute, storage, egress, third-party inference, support hours? A number, even a rough one.
5. What can you meter reliably today, and what would take a quarter to instrument?
6. Is there a free way to get most of the value - your own open-source edition, a self-hostable build, a competitor's free tier?
7. What is the pricing today, if any, and what is actually wrong with it: conversion, expansion, margin, churn, or sales friction?
8. What does the closest alternative charge, and on what unit?
9. What usage or account data do you already have - usage distribution, conversion rates, win/loss reasons?
10. By what date does the new pricing have to be live - this quarter, before the next renewal cycle, no deadline?
11. Do you want a one-off win (revenue this quarter, a deal unblocked) or a compounding asset - a metric and ladder that keep expanding as customers grow?
12. What is your effort ceiling: how much billing and metering engineering can you fund in the next two quarters, and would you publish a price or a free limit you can never walk back?
13. What is off the table: no sales team, no metering, a public promise about the free tier, an existing contract shape you cannot break?

Answers 10, 11 and 12 re-rank step 2's metric menu and step 3's ladder - carry them there instead of re-asking:

- A date this quarter promotes the metrics billed off state you already hold, capacity and seats, and promotes the self-serve rung over the enterprise one.
- A compounding mandate promotes consumption and business-outcome metrics, the only ones whose revenue grows without a new sale.
- No funded billing engineering deletes consumption outright.
- A refusal to publish an unwalkable number caps the free surface at limits stated as revisable for new accounts.

If your harness has persistent memory, record the value metric, the buyer, the cost per unit and the refusals. Every later packaging and go-to-market decision reuses them.

## Step 1 - Establish the two numbers pricing depends on

Before any option is discussed, get these written down. Everything downstream is unfalsifiable without them.

- **Marginal cost to serve one unit** of each candidate metric, including support. If nobody has computed it, computing it is the first deliverable, not an aside.
- **The free alternative's true cost** to the customer: infrastructure plus operator time plus upgrade risk for self-hosting, or the engineering weeks to build it. This is your ceiling, and it is the number developers actually reason with.

Also fix the deployment reality (who runs it) and the buyer (who signs). A price aimed at an individual's personal card and a price aimed at a procurement cycle are different products, not different discounts.

## Step 2 - Choose the value metric, in explicit brainstorming mode

Say you are entering brainstorming mode, then widen before narrowing.

List candidates from every family - seats, consumption of a technical unit, business-outcome units, capacity or entitlement, a percentage of a flow, flat per-product - using [references/value-metric-families.md](./references/value-metric-families.md). Mark each _plausible_, _unmeterable today_, or _misaligned_, with the reason.

Put the survivors through the five tests, in writing:

1. Does it move when the customer gets more value?
2. Does the customer already count it for their own reasons?
3. Can they forecast it before the invoice arrives?
4. Is it gameable or perverse - does it punish retries, health checks, or good engineering?
5. Does it correlate closely enough with your cost to serve?

Rank the survivors by value returned per unit of effort - effort meaning metering and billing engineering, the forecasting and dispute burden each invoice carries, and the fact that changing a live metric rewrites every contract. Say the order out loud and lead with its top, not with the cheapest unit. Each line is descending on its own axis, highest first.

- efficiency: `capacity or entitlement > business outcome > seats > flat per unit of software > consumption`
- value (how closely the invoice tracks value delivered, and whether it expands without a new sale): `consumption > business outcome > capacity or entitlement > seats > flat per unit of software`
- effort: `consumption > business outcome > capacity or entitlement == seats > flat per unit of software`
- compliance cost: `business outcome > consumption > capacity or entitlement == seats == flat per unit of software`

Effort in magnitudes:

- A flat unit costs near-zero, one line on an invoice.
- Seats and capacity cost about a week each, billed off an account record you already keep.
- A business-outcome unit costs a quarter, because the number lives in the customer's system and has to be collected and agreed.
- Consumption is a standing job: a metering pipeline, caps, alerts, forecasting, and a dispute path behind every invoice.

Tie justifications:

- Effort tie (capacity == seats): both are trivially meterable off state the product already stores, and neither adds a pipeline the other escapes.
- Compliance tie (capacity == seats == flat per unit of software): none of the last three creates a claim on customer data or a contractual audit right.

Read the compliance line as the review triggered and the reversibility spent:

- Business outcome needs a data-sharing or self-reporting clause and usually an audit right.
- Consumption turns usage records into the evidence in every billing dispute, with published caps and credit policies that cannot be quietly withdrawn.

What this order starves: consumption. It aligns price to value better than anything else here and needs metering nobody has built yet, so the ratio buries it every round. A tool whose cost to serve moves with the unit cannot afford a metric decoupled from its own COGS (see the 62% usage-only margin median in step 4). Promote it above everything when cost tracks the unit, or when the buyer already forecasts that unit for their own reasons.

Delete rather than demote, and say which:

- Nothing meterable today, with no funded quarter of billing engineering, deletes consumption instead of ranking it last.
- A product that does not move the customer's money deletes percentage-of-a-flow entirely: it is excellent where it applies and meaningless where it does not, which is why it is absent from the lines above rather than parked at the bottom.
- A product consumed by CI, service accounts or agents deletes seats: the tell is flat seat count against rising usage, and no ranking survives a unit that stops moving.

This order is a default, not a law - it shifts with context and with who executes it. Re-rank it against what you already know:

- An existing metering pipeline promotes consumption to the top, because the standing cost is already paid.
- A stateful product sized at deployment time promotes capacity further.
- A collaboration surface where humans are the load promotes seats.

Then present **two or three candidate architectures**, never one, in that order. For each: the unit, what a typical customer's bill looks like, what it gives up, and how it behaves when the customer succeeds. Recommend one, say why, and let the user choose before detailing further.

Most mature devtool pricing is a hybrid: a platform fee, an included allowance, metered overage, optionally a committed-spend floor. Treat the hybrid as a first-class candidate rather than a compromise - it is also how a starved consumption layer gets bought in stages, under a metric that already works.

## Step 3 - Build the package ladder

Four rungs, each with contents, a trigger event that moves a customer up, _and_ a place in the build order. A rung with no trigger is a price list, not a ladder. Full contents, gate placement and the free-limit checklist are in [references/packaging-ladder-and-gates.md](./references/packaging-ladder-and-gates.md).

Build them in efficiency order - revenue unlocked per unit of engineering and organizational effort - not top-down from the biggest contract. Each line is descending on its own axis, highest first.

- efficiency: `self-serve paid > free surface > team > enterprise`
- value (annual revenue per account the rung unlocks): `enterprise > team > self-serve paid > free surface`
- effort: `enterprise > team > free surface == self-serve paid`
- compliance cost: `enterprise > free surface > team > self-serve paid`

Effort in magnitudes:

- The free surface and the self-serve rung are each about a quarter and share most of it. Limits sit on the same axis as the paid metric, so one meter enforces both - that shared meter is what ties them.
- The team rung adds roles, shared billing and retention, a quarter more.
- The enterprise rung is a standing job of security reviews, questionnaires, custom terms and SLA credits.

1. **Free surface** - permanent, no card, enough to run a real side project. In this market a time-boxed trial is a weak substitute: evaluation takes weeks of unpaid tinkering and internal advocacy.
2. **Self-serve paid** - one developer or one team, published price, instant provisioning, no conversation. Build this rung first; it is the only one that returns revenue without a human in the loop.
3. **Team** - the org becomes the unit: roles, shared billing, environments, retention, a support response target.
4. **Enterprise** - risk removal: enterprise identity, granular RBAC, audit logs, residency, SLA with credits, security review, invoicing, custom terms.

Read the compliance line as the review triggered and the reversibility spent:

- Enterprise signs SLAs with credits, DPAs and residency commitments that legal reviews and nobody withdraws quietly.
- The free surface ranks second on reversibility alone, since a published free limit is close to permanent - step 6 only allows shrinking it for new accounts.

What this order starves: the enterprise rung. It tops the value line and the effort line at once, so the ratio puts it last every round, and the buyers who purchase risk removal rather than features never get a rung to buy. Promote it the moment named deals stall on audit logs, an SLA or an identity requirement - a stalled deal is evidence the ratio cannot see.

Delete rather than demote:

- A product whose users never share state - a single-player CLI with no organization concept - deletes the team rung rather than shipping an empty one.
- No procurement-facing buyer at all deletes enterprise.

This order is a default, not a law. Re-rank it against what you already know: an existing enterprise support organization and a completed security certification promote the enterprise rung, because its standing cost is already paid.

Rules that hold across products:

- Gate on things an _organization_ needs and a solo developer does not. Anything an individual also wants gets rebuilt, forked, or resented.
- Set free limits on the same axis as the paid metric, so hitting the limit is the same event as needing to pay. One or two headline limits, not five interacting ones.
- Never paywall security fundamentals, security patches, data export, or anything the community contributed. On single sign-on, the failure prospects raise unprompted is a 3x-base-price identity tier, not a modest surcharge - so put basic SSO at the team rung and keep only enterprise identity work (custom IdPs, SCIM, directory sync, session policy) at the top. The public catalogue of this failure, sso.tax, sets its inclusion bar at a 10% surcharge; sourcing and the institutional pressure behind it are in the reference.
- Publish prices as far up the ladder as the business can bear. In a bottom-up motion, "contact sales" at the entry rung is not a lead form, it is an exit.
- Add a human to the sale only where the account's revenue can carry the human's cost. The sourced anchors for that judgment: roughly six figures of annual revenue per account before field sales works (Christoph Janz), LTV/CAC ≥ 3x with CAC payback inside 12 months as the general check (David Skok - hardened convention, not a measured constant), and about 4x fully loaded cost returned per salesperson added to a self-serve motion. Below low-four-figure annual contract value, sell self-serve only.

## Step 4 - Bound the price points, then place them

A number is defensible only when both bounds are written down. Method, research techniques and structural mechanics are in [references/price-point-method.md](./references/price-point-method.md).

- **Floor** - marginal cost plus your gross-margin target, modelled on the _90th-percentile_ account rather than the average one (this skill's own baseline), carrying the free surface's total cost as a line item. Usage-only pricing models run a **62% median gross margin** against an 80% software median, because infrastructure sits in COGS. That gap is what changes the decision for a consumption-heavy tool, so choose a consumption-weighted target deliberately instead of discovering it at the first cost review; both figures, their study and their limits are in [references/pricing-evidence-base.md](./references/pricing-evidence-base.md).
- **Ceiling** - the lowest of: self-host it, build it, the next best vendor, do nothing. For anything with a free self-hostable equivalent, the first is almost always the binding one.
- If the lowest ceiling sits below the floor, the problem is the cost structure or the model, not the price. Say so instead of picking a number in between.

Place the number with evidence, buying it in efficiency order rather than strength order - the two disagree, so read both:

- efficiency: `own usage-value correlation and win/loss data > competitor prices > Gabor-Granger demand curve > Van Westendorp sensitivity range`
- value (evidence strength): `own usage-value correlation and win/loss data > Gabor-Granger > Van Westendorp > competitor prices`
- effort: `Gabor-Granger > Van Westendorp > own data > competitor prices` - a fielded survey costs weeks and a respondent panel, reading your own data costs a day, and a competitor's price page costs an hour

Competitor prices rank second on efficiency and last on strength: cheap, and evidence of what someone else guessed. Use them to bound a number, never to justify one. Feature-ranking research (MaxDiff) informs packaging, not the number.

With no data at all, price from the floor plus target margin, sanity-check against the self-host cost, and label it an experiment with a review date.

Set the mechanics deliberately:

- Annual discount, inside the observed distribution - the "two months free" anchor is 16.7%, and over half of a 100-company sample discount between 15% and 20% (range and sourcing in the evidence base). "12 months for the price of 10" explains itself; an undisciplined discount ladder, by contrast, is a price cut nobody decided to make.
- Volume breakpoints on the metered unit.
- Committed-spend discounts.
- A discount ceiling for anyone who negotiates.

## Step 5 - Make the bill predictable

Predictability is a pricing feature, and in this market it is the one that gets talked about. Require all of it before launch:

- A public price page with real numbers, plus a calculator for any metered component.
- Live usage against the limit, a projection to period end, and the same data through an API.
- Alerts at fixed thresholds plus an anomaly alert for a sudden multiple of the normal rate.
- Both cap styles offered - hard cap (service pauses; the sane default for hobby and development accounts) and soft cap (service continues, alert fires; the sane default for production) - with the default stated plainly.
- Itemized invoices: quantity, unit rate, subtotal, plan fee and credits, separately.
- A written policy on what happens at the limit, and a pre-approved credit for runaway usage caused by an obvious defect or an attack. The credit is always cheaper than the story about the bill.

Reason from the documented case: Netlify's $104K bandwidth bill of February 2024, from 190TB of traffic against a 3MB file on a free-tier site. Netlify forgave the bill and published a standing policy - the right response after the fact, and no substitute for the cap, the alert, and the anomaly detection that would have prevented it.

## Step 6 - Plan the change (only when repricing)

Changing a live price is a trust event. Work through it cohort by cohort, and read [references/pricing-change-cases.md](./references/pricing-change-cases.md) first - it holds eleven dated changes, the negative example this step exists to prevent, and the counterexamples where a company absorbed loud backlash and held its ground.

1. Name every affected cohort separately: existing paying customers, free users, self-hosted or open-source users, and anyone under contract.
2. Decide grandfathering explicitly - indefinite, or a stated window with an end date - and put it in the announcement.
3. Announce before shipping, with more notice where annual budgets are involved. Nobody should learn about a price change from an invoice.
4. Pair the increase with delivered value; a rise with nothing new attached is read as extraction, and usually correctly.
5. Never move an existing capability from free to paid, and never reverse a pricing commitment you have made in public. New paid capabilities are legitimate; taking one back is the move that produces forks and front-page threads. Unity's Runtime Fee is the sourced case: the fee itself was survivable, but reversing an explicit 2019 promise to charge "a flat fee per-seat, not a royalty on all of your revenue" was not. The company walked the change back after an organised threat of engine migration.
6. Shrink a free tier by applying the new limits to new accounts only, and say that is what you are doing.
7. Write the migration path per cohort - new price, date, what to do, where to appeal - and publish the FAQ with the announcement.
8. Decide in advance who answers the public thread, in what tone, and what concession is pre-approved.

## Step 7 - Write the pricing memo, validated section by section

```markdown
# Pricing - <product>

## Inputs model, buyer, cost per unit, free alternative's true cost

## Value metric the unit, the four rejected candidates and why

## Ladder the four rungs: contents, trigger to climb, price shape

## Free surface limits with numbers, total marginal cost, abuse policy

## Price points floor, binding ceiling, chosen numbers, evidence behind each

## Mechanics annual, volume breaks, commitments, discount ceiling

## Predictability caps, alerts, calculator, invoice shape, overage policy

## Change plan cohorts, grandfathering, notice period, migration path

## Measurement the metrics watched, targets, and the review date

## Revisit triggers the events that reopen this decision
```

Present one section at a time and get agreement before writing the next. A wrong value metric propagates into every line below it and is far cheaper to catch at the second heading than at the ninth.

A full worked memo, with weak and strong versions of the same sections, is in [references/pricing-memo-example.md](./references/pricing-memo-example.md).

## Name the owner before the memo ships

A memo with no owner is a document, not a decision. Assign ownership by company stage rather than by org chart:

- **Expansion-stage.** More than two-thirds of expansion-stage SaaS companies report that the CEO or company leadership ultimately owns pricing (OpenView survey of 1,000+ SaaS executives), and a dedicated pricing hire typically does not arrive before roughly $50M ARR (Kyle Poyar).
- **Below that.** Name a standing group - product, finance, one customer-facing voice - and give it a review date, because the risk at this stage is neglect. Patrick Campbell's frequently quoted figure is that companies spend something like 10 to 14 hours a year on pricing; treat the hour count as directional and the underlying point as sound.
- **Public company.** The constraint inverts: pricing outcomes are reported to analysts, so a change needs a defensible revenue-retention narrative before it needs a customer announcement.

## Organizations versus individual developers

Both exist in every developer tool, and pricing them identically fails both.

- **Organizations** pay for risk removal and governance, tolerate approval cycles, and expect notice measured in quarters. They will negotiate a committed floor and need paperwork before money moves. Spend escalates through a personal card, a corporate card, then security review and procurement - the escalation is real, but the dollar thresholds attached to it are folklore, so ask the user where their own buyers cross those lines instead of quoting a number.
- **Individual developers** pay small amounts on a personal card, with no approval and no tolerance for an unbounded downside. A metered price that can produce a surprise personal bill suppresses adoption regardless of how fair the rate is; give this segment a hard cap or a flat price.

Use Stephen O'Grady's _The New Kingmakers_ argument - developer adoption precedes and drives the organizational purchase - as what it is: a sourced, influential argument about _sequence_. Do not extend it into the adjacent claim that developers are unusually price sensitive; that is a widely held practitioner belief with no measurement behind it. Say so rather than asserting it, and reason from the sourced fork and reversal cases instead.

Organizations and individual developers agree on two points: the metric should be something the payer already counts, and the bill should be predictable.

## Measurement and the pass threshold

Hold the design to this before the memo is final, and iterate until every line passes. Label each line sourced or self-set when you report the check - a self-set baseline repeated without its label becomes a fake benchmark the moment the user quotes it onward.

Self-set by this skill, not industry benchmarks:

- The value metric has all five tests answered in writing, none of them "no".
- A target customer can estimate their monthly bill from public materials in under two minutes, and the estimate lands within ±20% of what they would actually be invoiced. Test this on three real usage profiles.
- The free surface's total marginal cost is a number, expressed as a share of paid gross profit, with a ceiling the team agrees to.
- Every rung has a written trigger event, and the price of every rung below enterprise is public.

Anchored in sources, cited in [references/pricing-evidence-base.md](./references/pricing-evidence-base.md):

- Gross margin at the proposed price clears the target set in step 4, checked at the 90th-percentile account (that check is this skill's own baseline, not part of the source).
- No gate violates the never-paywall list, and any single-sign-on surcharge stays near the 10% bar rather than becoming an identity tier.
- Where a human enters the sale, the account economics from step 3 hold.
- Any change plan names every cohort with a date and an explicit grandfathering decision, and reverses no public commitment.

Then track, from launch: free-to-paid conversion, time from signup to first payment, net revenue retention, share of accounts sitting near a rung boundary, average discount and its trend, gross margin per account, price-related loss reasons in win/loss, and billing-related support volume - the last is the cleanest proxy for how confusing the pricing is.

Compare conversion against the developer-specific band, never a blended B2B one:

- **Developer-focused products convert free to paid at a median of about 5%, roughly half the non-developer median** (Lenny's Newsletter, survey of 1,000+ products - see the evidence base for what it does not prove).
- Freemium self-serve products sit at 3-5% (good) to 6-8% (great); time-limited trials convert far higher on a much smaller top of funnel.
- Net revenue retention for a bottom-up product is around 100% (good) to 120% (great), from the same corpus.

Measure conversion by cohort at account level within six months of signup, or the bands mean nothing.

Report the threshold check explicitly at the end. Failing the predictability test is not a documentation problem; it means the metric or the tier structure is too complicated to sell.

## Common failure modes

- **A free tier priced in adjectives.** "Generous" is not a number, and nobody discovers the real cost until growth becomes expensive.
- **The invented unit.** Vendor-defined credits or points with no published conversion and no calculator read as obfuscation, whatever the intent.
- **Pricing against the wrong ceiling.** Benchmarking only against other vendors while the real alternative is the customer running your own open-source edition for the cost of a VM.
- **Retroactive gating.** Moving an existing capability behind a paywall costs more in trust than it ever collects in revenue.
- **Discount drift.** A list price nobody pays turns every renewal into a negotiation and punishes the customers who did not push.
- **Three compounding metrics.** Each one defensible alone; together they need a spreadsheet, and a bill that needs a spreadsheet does not get approved.

## References

- [references/value-metric-families.md](./references/value-metric-families.md) - the metric families with fit, failure mode and meterability; the hybrid stack; seat-collapse diagnostics.
- [references/packaging-ladder-and-gates.md](./references/packaging-ladder-and-gates.md) - the four rungs in detail, gate placement per feature, free-limit checklist, add-ons versus tiers.
- [references/price-point-method.md](./references/price-point-method.md) - floor and ceiling computation, research methods with their evidence strength, discount and commitment mechanics.
- [references/pricing-memo-example.md](./references/pricing-memo-example.md) - a full worked memo, plus weak versus strong versions of each section.
- [references/pricing-evidence-base.md](./references/pricing-evidence-base.md) - every sourced figure with its citation and its limits, the claims deliberately not used, and this skill's self-set baselines.
- [references/pricing-change-cases.md](./references/pricing-change-cases.md) - eleven documented pricing and licensing changes, the shape shared by the backlash cases, and a negative example worked through against its survivable rewrite.
- `samber/developer-relations-skills@developer-first-gtm` - designs the adoption motion the ladder feeds.
- `samber/developer-relations-skills@open-source-company-strategy` - decides what is open in the first place.
- `samber/developer-relations-skills@oss-license-strategy` - covers the licence a self-hosted edition ships under.
- `samber/developer-relations-skills@developer-journey-map` - locates where in the journey the paywall lands.
- `samber/developer-relations-skills@developer-segmentation` - the segment cut whose willingness to pay this ladder prices against.

See `samber/developer-platform-skills` when the metering, quota and API-key surfaces behind a consumption price still need to be designed.
