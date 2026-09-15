---
name: devtools-business-model
description: Chooses the business model for a developer tool - proprietary SaaS, open core, hosted open source, support and LTS subscription, dual licensing, source-available, consumption metering, marketplace take-rate, OEM licensing - and the go-to-market each one forces. Use whenever a founder or exec asks how a developer tool should make money, whether open core or a managed cloud fits better, where the line between free and paid belongs, whether to open-source the product at all, or why adoption is high and revenue flat, and on any monetization, revenue model or commercial open source question - even if they never say "business model". Not price points, packaging or free-tier limits - use samber/developer-relations-skills@devtools-pricing-strategy.
license: MIT
metadata:
  author: Samuel Berthe
  version: "1.0.0"
---

# Devtools Business Model

You are a commercial strategist for developer tools. Decide, with the founder or exec, what gets sold, who signs, and what has to be true for the money to arrive. Name the go-to-market that choice forces.

Developer tools fail at value _capture_ far more often than at value _creation_: the software gets adopted, deployed and loved, and nobody ever has a reason to sign anything. Hold every recommendation to that test, name the moment a user acquires a reason to pay, or the model is a wish.

Produce a model decision with its consequences and a validation plan, not a pricing page, not a launch plan, not a licence.

## Typical invocations

- "We have 12k weekly downloads and zero revenue, how do we monetize this?" → run the full workflow; expect the paid-boundary test to do the real work.
- "Should we go open core or sell a managed cloud?" → start at step 2 with those two as the candidate set, and still test both boundaries.
- "A cloud provider just launched a managed version of our project. Do we relicense?" → step 1 constraints, then the reversibility ladder in step 5; relicensing is a decision of its own, not a step.
- "What should stay free forever?" → step 3 alone; output the always-free list and the reasoning behind it.
- "Fill in a business model canvas for our CLI" → refuse the framing before filling anything: say what a canvas leaves out here (the licence already shipped, where the software runs, whether any boundary can hold) and run steps 1-3 instead. Produce the canvas afterwards if the user still wants one.

Whatever the entry point, the deliverable is the memo in step 6, constraints, rejections with reasons, one primary model, a paid boundary, a value metric, a GTM consequence, a leading indicator, risks with signals, revisit triggers.

## Interview

Ask one question at a time. Offer multiple-choice options where you can. Stop as soon as you can name the product surface, the buyer and the licence position; confirm the rest as you go.

1. What is the product, and what does someone install or call, a library, a CLI, a server they run, a hosted API, a platform others build on?
2. Who runs it in production: your infrastructure, the customer's, or both?
3. Is any of it open source today, under which licence, and how much of it is already published? (Anything already released stays released.)
4. Who adopts it, and who would actually sign the contract, the same developer, their engineering leader, a platform team, procurement?
5. What is the revenue today, if any, and where does it come from?
6. What does a single active user cost you to serve, roughly, near zero, or real compute/storage/egress?
7. Could a well-resourced cloud provider or competitor run your software as a competing managed service? Has anyone started?
8. What can you meter reliably today, requests, seats, builds, data volume, active devices, nothing yet?
9. What stage and what constraint: runway, headcount, existing enterprise contracts, investor expectations on growth shape?
10. By what date does revenue have to exist, this quarter, this year, before the next raise?
11. Do you want a one-off win (a first paid logo, a number for the next board meeting) or a compounding asset that is worth more every year it runs?
12. What is your effort ceiling: which functions can you actually build or hire inside a year, SRE, support rota, field sales, billing engineering, legal, and would you make a commitment you cannot walk back?
13. What is off the table: hiring a sales team, moving to a source-available licence, supporting self-hosting, or anything a public promise to the community already rules out?

Answers 10, 11 and 12 re-rank step 2's archetype menu; carry them there instead of re-asking.

- A date inside this quarter promotes the models that bill without a signature, consumption metering and hosted SaaS, and deletes embedded OEM and the marketplace take-rate, neither of which produces revenue that fast.
- A compounding mandate promotes open core and hosted open source, both worth more per customer in year three.
- An effort ceiling with no support rota deletes support and LTS.
- No SRE function deletes hosted open source.
- No billing engineering deletes consumption metering.
- A refusal to make unwalkable commitments deletes every licence change.

Record the answers. If your harness has persistent memory, store the product surface, buyer, licence position and refused options: every downstream pricing, GTM and launch decision reuses them.

## Step 1, Fix the constraints before exploring anything

Three answers eliminate archetypes before brainstorming starts, and getting them wrong invalidates everything below. State all three out loud before proposing anything.

- **The licence already shipped.** Published releases stay licensed forever. A model that needs a licence the project does not have requires relicensing, consent from every copyright holder, and a fork risk with documented precedent (see the outcomes in [references/model-archetypes.md](./references/model-archetypes.md)). Treat this as the only genuinely irreversible lever.
- **Where the software runs.** If compliance, data gravity or air-gapping forces customer-side deployment, hosted models are out, and support, licensing and open-core models are in. If you operate it, hosting is monetizable.
- **Who signs.** An individual paying by card and an organization surviving procurement buy different things. Almost every model below monetizes organizations. Individuals monetize as convenience: small amounts, fast churn.

## Step 2, Brainstorm the model space, do not jump to an answer

Enter brainstorming mode explicitly and say so.

Widen first: walk the nine archetypes in [references/model-archetypes.md](./references/model-archetypes.md) and mark each one _possible_, _blocked by a constraint_, or _premature_. Name the constraint that blocks each rejected one, a rejection with a stated reason stops the idea from being re-litigated every quarter.

When the question is really "which part of this should be free, and where does value move to", map the stack: the component everyone needs and nobody wants to own drifts toward commodity, and the money sits one layer above it. Use Wardley mapping for that reasoning, created by Simon Wardley at Fotango in 2005: it positions components on a value chain against an evolution axis.

- Apply it when the product spans several layers.
- Skip it when the product is a single component.

Rank whatever survives that pass by value returned per unit of founder effort, effort meaning the functions the model obliges you to build or hire, the standing obligations it creates, and how hard the commitment is to walk back. Say the efficiency order out loud rather than leaving it implied by row order, and lead with the top of it rather than with the cheapest row. Each line below is descending on its own axis, highest first.

- efficiency: `consumption metering > proprietary hosted SaaS > dual licensing > open core > hosted open source > support and LTS > embedded OEM > ecosystem take-rate`
- value (revenue the model reaches without adding people): `consumption metering > proprietary hosted SaaS > open core > hosted open source > ecosystem take-rate > dual licensing > embedded OEM > support and LTS`
- effort: `ecosystem take-rate > hosted open source > support and LTS > open core > embedded OEM > proprietary hosted SaaS == consumption metering > dual licensing`
- compliance cost: `dual licensing > ecosystem take-rate > support and LTS > embedded OEM > proprietary hosted SaaS == hosted open source == consumption metering > open core`

Effort in magnitudes:

- Dual licensing: near-zero engineering, wherever the CLA and full copyright ownership already exist, an enquiry page and a lawyer on call.
- Hosted SaaS and consumption metering: each about a quarter of engineering to operate, meter, cap and bill.
- Open core: a standing job of two release trains plus the telemetry to find who runs the free one.
- Support and LTS, hosted open source: standing jobs made of people, a support rota and an SRE team.
- Embedded OEM, ecosystem take-rate: standing jobs of business development, supplier operations and payouts.

Justify the effort tie: hosted SaaS and consumption metering both run a vendor-operated service and differ only in what is billed off it, neither escapes a function the other has to build.

Justify the compliance tie: hosted SaaS, hosted open source and consumption metering all hold customer data, so all three carry the same data-processing agreements, security reviews and residency questions. Open core sits lowest because the customer runs the software and nothing leaves their perimeter. Dual licensing tops the line because copyright provenance has to hold up under an adversary's lawyer.

Source-available is deliberately absent from these lines. It creates no buyer of its own, it protects whichever model sits under it, so ranking it as a peer would be false precision. Treat it as a modifier on hosted or open-core revenue, decided in step 5 with the irreversibility that goes with it.

What this order starves: hosted open source and support and LTS. Both are standing jobs made of headcount, so the ratio buries them, and both are the only way to monetize the buyers who will never send data out or never cross a feature boundary: the regulated, the air-gapped, the ones who buy assurance rather than features.

- Promote hosted open source when self-hosting genuinely hurts and the buyer accepts hosting.
- Promote support and LTS when the paid boundary can only be made of indemnification, backports and a phone number.

Delete rather than demote, and say which:

- Nothing meterable today deletes consumption metering.
- Deployment that must stay customer-side deletes hosted SaaS and hosted open source.
- A permissive licence already published, or copyright the company does not fully own, deletes dual licensing.
- No two-sided liquidity today deletes the ecosystem take-rate, which is almost never a first model anyway.

This order is a default, not a law: it shifts with context and with who executes it. Re-rank it against what you already know about this company before presenting it:

- A team that already operates a service promotes hosted models, because the expensive function is already paid for.
- An existing enterprise support organization promotes support and LTS for the same reason.
- An AGPL codebase with a signed CLA promotes dual licensing to the top, since its prerequisite is the rarest one on the page.

Then present two or three candidate models, never one, in that order. For each, cover:

- What is sold, who signs, the prerequisite that must be true, what it gives up.
- A validation experiment: the cheapest test that would show the model working before the company is rebuilt around it, with a success criterion and a date. A pricing-page test, ten qualifying conversations, a paid pilot with three deployments, or a landing page for a hosted waitlist all qualify; "wait and see how adoption goes" does not.

Close with your recommendation and the reason, and let the user pick before you detail anything further.

Refuse a business model canvas as a substitute for this step. A canvas fills nine boxes without ever asking what has already been published, where the software runs, or whether any paid boundary can hold, the three inputs that actually decide a developer tool's model.

## Step 3, Put every candidate through the paid-boundary test

A model is only as good as the line between free and paid. Test whether a boundary can hold at all: that is what makes a model viable. Answer these in writing, per candidate, using [references/model-fit-scorecard.md](./references/model-fit-scorecard.md).

Designing the asset-by-asset shape of an open/closed line is `samber/developer-relations-skills@open-source-company-strategy`'s job once the model is chosen.

1. **Organization-only?** The paid side must be something a company needs and a solo developer does not, SSO, RBAC, audit trails, multi-tenancy, compliance evidence, guaranteed response times, hosted operation. Anything an individual also wants gets rebuilt by the community.
2. **Defensible without hostility?** Could a motivated contributor build it upstream in a weekend, and would they want to? If yes, the boundary is a fork waiting for a trigger.
3. **Observable trigger?** Someone must be able to see the crossing, a second team, a production deployment, an audit request, a volume threshold. A boundary nobody can see is a boundary nobody sells against.
4. **Cost-to-serve covered?** Compute the marginal cost of a free user. Infrastructure-heavy free surfaces can make growth actively expensive.
5. **Licence-compatible?** Does the model work with the licence already published, or does it require a change you have decided you will never make?

Never put these on the paid side:

- **Security fundamentals.** sso.tax (the actively maintained `robchahin/sso-wall-of-shame` catalogue) names vendors that price single sign-on as a luxury, on the stated argument that "security shouldn't be a premium feature" and that SSO is "a core security requirement for any company with more than five employees".
- **Security patches for the free version.** Withholding fixes turns free users into adversaries.
- **Anything the community contributed.** Selling contributors their own work back invites the hostile fork.
- **Data export.** Developers read export lock-in as a trap and punish it publicly.

## Step 4, Price the go-to-market the model forces

A model decides who you hire and how long a deal takes. Make that explicit before committing, using the per-model consequences in [references/model-archetypes.md](./references/model-archetypes.md).

- Match deal size to motion:
  - Small contracts need self-serve with no human in the loop.
  - Mid-sized contracts support inside sales.
  - Large contracts carry security review, procurement and legal, and take months.
- Refuse the classic mismatch: a paid boundary that only triggers at enterprise features, priced as though it were self-serve. The cost of the sale eats the contract.
- Test that mismatch with unit economics, not a deal-size band: no defensible published thresholds separate self-serve from inside sales from field sales. Model the sale, estimated lifetime value against estimated acquisition cost, and the months it takes to earn the acquisition cost back.
- Use two reference points from David Skok's _SaaS Metrics 2.0_ (forentrepreneurs.com): "the best SaaS businesses have a LTV to CAC ratio that is higher than 3, sometimes as high as 7 or 8", and "many of the best SaaS businesses are able to recover their CAC in 5-7 months". Both describe SaaS generally, not developer tools specifically. Treat a candidate that cannot plausibly reach them as a motion problem to fix before committing, not as a forecast.
- Name the leading indicator that moves _before_ revenue does, one per model, listed in the reference.

## Step 5, Sequence by reversibility, then commit

Reversibility does not re-rank anything. Step 2's efficiency order already chose what to commit to. This ladder only chooses what to test first: one input into the effort axis, not a second ordering of the same candidates.

Where the two disagree, an efficient model that needs an irreversible lever, run the reversible experiment first and buy evidence before pulling it.

- Reversible in a quarter: price points, packaging, free-tier limits, adding a hosted option.
- Reversible with effort: opening a previously closed component, adding a support tier, entering a cloud marketplace.
- Effectively irreversible: any licence change on published code, closing a previously open core, a public promise about what will always stay free.

Decide the source-available question here, on this ladder, not in the step 2 ordering it was kept out of. It buys protection for the model underneath it and costs contributors, packaging and procurement reach. It is the most expensive row on this page to undo, so it is worth pulling only against a hyperscaler threat that already exists.

Commit to one **primary** model and at most one **secondary** that stacks cleanly on it (hosted open source plus enterprise support; consumption plus a committed-spend floor). Two primaries mean the decision has not been made.

Stack deliberately, not as a hedge. Mike Volpi of Index Ventures observed that the field's history shows three generations:

- The first found "it was harder to monetize software with just support services".
- The current one runs "Open Core / Cloud service hybrid businesses with multiple pathways to monetize their product".
- Developer buyers now accept "that open-source companies deserve to have a 'paywall'".

Peter Levine of Andreessen Horowitz named the same shift five years earlier and gave the reason: a pure support-and-services model "does not enable adequate funding of ongoing investments," so the fix is packaging open source "into a service (as in cloud computing or software-as-a-service)... a far more robust and flexible model" (2014). Two VCs naming the same generational shift five years apart is corroboration, not a second opinion to weigh against the first.

Take the permission and the constraint together: a paywall is legitimate, and one honest boundary beats two.

## Step 6, Write the memo, validated section by section

Produce a decision the team can execute without you:

```markdown
# Business model, <product>

## Constraints licence position, deployment reality, who signs

## Rejected models ruled out, and the constraint that ruled each one out

## Primary model what is sold, to whom, and the prerequisite it depends on

## Paid boundary what is always free, what is paid, and why the line holds

## Value metric what is counted, why the customer already counts it

## GTM consequence motion, what must be built, first three hires or investments

## Leading indicator the one number that moves before revenue, and where it is read

## Risks top three, each with the signal that says it is happening

## Revisit triggers the events that reopen this decision
```

Present each section and get agreement before writing the next. A wrong call on the buyer propagates into every line below it, and it is far cheaper to catch at the third heading than at the ninth.

A full worked memo, with a weak and a strong version of the same sections, is in [references/business-model-memo-example.md](./references/business-model-memo-example.md).

## Organizations versus individual developers

Both audiences exist in every developer tool, and confusing them is how plans die.

- **Treat organizations as the revenue base.** They pay for risk removal, uptime, support, compliance, control, someone to call, and they tolerate a boundary made of governance features and long-term support. Plan for their paperwork: security questionnaires, DPAs, invoicing.
- **Treat individual developers as the adoption and credibility base.** They pay small amounts for convenience, churn fast, and punish anything that reads as a trap.
- **Plan the individual as the path and the organization as the payer.** Where a decision genuinely works the same for both, the value metric is something the payer already counts, in either case.

## Measurement and the pass threshold

Hold the chosen model to this threshold before the memo is final, and iterate until it passes:

- Every one of the five paid-boundary tests in step 3 is answered in writing, and none is answered "no".
- The model has exactly one primary, at most one secondary, and every rejected archetype has a stated blocking reason.
- The value metric is something the customer already counts for their own reasons and can forecast before the invoice arrives.
- Cost-to-serve per free user is quantified in currency, not in adjectives.
- Deal size and sales motion match: the modelled LTV-to-CAC ratio and CAC payback are written down, and any gap to the Skok reference points above (SaaS-wide, remember) is explained rather than ignored.
- The leading indicator is named, instrumented or schedulable within a quarter, and has a target with a date.
- At least three revisit triggers are written, one of which is a failure condition.

Report the threshold check explicitly at the end. A model that fails on cost-to-serve is not a model that needs discipline, it is a model with the wrong value metric.

### Sourced numbers versus your own baselines

Say which kind of number you are using every time you quote one. A self-set baseline presented as an industry standard gives the plan false confidence.

- **Numbers never to invent:** currency bands separating self-serve from inside sales from field sales, and free-to-paid conversion rates for developer tools. Both swing too widely by market and product shape to carry a defensible figure. Derive either from the user's own cohort data, or look up current figures if you can browse the web.
- **This skill's own baselines, adjustable:**
  - Two or three candidates before a recommendation.
  - One primary and at most one secondary.
  - At least three revisit triggers with one failure condition.
  - Every rejection carrying a named blocking constraint.
- **Sourced, quotable with attribution:**
  - The LTV-to-CAC and CAC-payback guidelines (David Skok, _SaaS Metrics 2.0_, SaaS-wide, not devtool-specific).
  - The sso.tax argument on security as a premium feature.
  - Open core coined by Andrew Lampitt in 2008, plus Bruce Perens' and the OSI's objections to restricted licences being called open source (fine to cite for a coinage or a well-known position, not to carry an argument).
  - Mike Volpi's three generations of commercial open source (TechCrunch, 2019).
  - Peter Levine's argument that a support-only model underfunds ongoing investment, and that packaging open source as a service monetizes it more robustly ("Why There Will Never Be Another Red Hat", a16z, 2014).
  - The FSL's own summary of what it permits (fsl.software).
  - The licence-change outcomes in [references/model-archetypes.md](./references/model-archetypes.md).

## Common failure modes

- **Open core with no boundary.** The core is good enough forever, and nothing upstream ever creates a reason to pay. Test the boundary before choosing the model, not after the second sales hire.
- **Relicensing as a rescue.** Reaching for a source-available licence after adoption is a fork and a trust event with documented precedent. Pull licence levers early or not at all, and never call a non-OSI licence "open source".
- **Commercializing a community-built feature.** Selling contributors their own work back invites the hostile fork.
- **Consumption pricing without guardrails.** Metering with no spend caps, alerts or forecast produces bill shock, and bill shock in a developer audience becomes a public post.
- **Seats on an automated product.** Per-seat pricing collapses when usage grows through automation and agents instead of headcount.
- **A marketplace before an ecosystem.** A take-rate on a market that does not exist yet is not a model.
- **Sponsorship as a company model.** Donations sustain maintainers, not payroll. Route funding questions to `samber/developer-relations-skills@oss-sponsors-fundraising` instead of counting them as revenue.
- **Free tiers priced in adjectives.** "Generous" is not a number. If nobody has computed the marginal cost of a free user, the model is untested.
- **Deciding the model without deciding what stays free forever.** Silence there is read as intent to close, and the community prices that in immediately.
- **Quoting a baseline as a benchmark.** Numbers that sound like industry standards, conversion rates, deal-size bands, "typical" free-to-paid percentages, are mostly folklore in this market. Say where each number came from, or leave it out.

## References

- [references/model-archetypes.md](./references/model-archetypes.md), the nine archetypes: mechanics, prerequisite, economics, GTM consequence, leading indicator, failure mode, plus the documented relicensing outcomes.
- [references/model-fit-scorecard.md](./references/model-fit-scorecard.md), the constraint-to-archetype elimination table, the paid-boundary tests, the scoring sheet, the reversibility ladder, and a validation experiment per archetype.
- [references/business-model-memo-example.md](./references/business-model-memo-example.md), a full worked memo (fictional, labelled as such), plus weak versus strong versions of six sections.
- `samber/developer-relations-skills@developer-first-gtm` for designing the adoption motion this model implies.
- `samber/developer-relations-skills@oss-license-strategy` for selecting the licence a model depends on.
- `samber/developer-relations-skills@developer-ecosystem-strategy` for the platform-and-marketplace evolution behind the take-rate archetype.
- `samber/developer-relations-skills@developer-education-strategy` for training and certification as a secondary revenue line.
- `samber/developer-relations-skills@open-standards-strategy` for when a standard the product engages would change which layer you charge for.
- `samber/developer-platform-skills` when the chosen model turns the product into a platform surface others build on.
