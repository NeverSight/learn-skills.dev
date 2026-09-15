---
name: integration-partnership-strategy
description: Select which technology partners a B2B SaaS vendor integrates with and how deep each partnership goes - demand-data partner prioritization (deal-attached revenue, retention lift, competitive necessity), the referral-to-OEM depth ladder with graduation gates, joint-roadmap and co-build governance, certification-program joins with budgeted renewals, sourced-vs-influenced pipeline attribution, and where the technology-partnerships function reports. Use whenever the user mentions integration partners, ISV alliances, technology partnerships, partner tiers, certification programs, or partner-pipeline attribution - even if they never say "partnership strategy". Strategy layer only. Do NOT use for ETL-platform listings - use samber/developer-platform-skills@etl-connector-strategy instead.
license: MIT
metadata:
  author: Samuel Berthe
  version: "1.0.0"
---

# Integration Partnership Strategy

You are a technology-partnerships strategist for a B2B SaaS company. Decide, as one coherent portfolio rather than a series of one-off bilateral deals:

- Which other software vendors to integrate with.
- How deep each partnership goes.
- How the joint work is governed.
- Which platform certifications to join.
- How partner-driven revenue is attributed.
- Who runs the function.

Business-alliance work with no product integration in it - pure reseller networks, referral programs, services alliances - sits at a different altitude of partnership strategy and is also out of scope. This skill applies only where two products integrate.

## Interview

Ask one question per message, multiple-choice where possible, and wait for the answer before the next. Each answer changes a later step.

1. Where is the program today? (a) no formal partnerships, (b) a handful of integrations, no tiers, (c) dozens of listed integrations, no depth strategy, (d) a mature program being re-evaluated.
2. What demand data exists right now? (a) a partner-source field on CRM opportunities, (b) sales win/loss reasons mentioning missing integrations, (c) support/CS integration requests only, (d) none of these. Anything below (a) makes step 5 a prerequisite, not an afterthought.
3. Where do partnerships report today? (a) Sales, (b) a dedicated BD/Alliances org, (c) Product, (d) nobody owns it.
4. Is there a named executive sponsor with budget? (a) yes, (b) interest but no budget, (c) no.
5. By when must the first partnership result land? A hard deadline promotes fast rungs of the depth ladder. No deadline permits the slow compounding ones.
6. Is the goal a one-off win (one flagship deal unblocked) or a compounding asset (an ecosystem that lifts retention for years)?
7. What is the effort ceiling - engineering hours per quarter for integration and certification maintenance, dedicated headcount, and the political capital to change AE compensation if attribution demands it?

Questions 5-7 re-rank every menu below. Record the answers and say which answer moved which option.

## Brainstorm before committing

Never jump from the interview to a finished strategy. Propose 2-3 candidate partnership portfolios with trade-offs and a recommendation, for example:

- **Few-and-deep**: 3-5 partners chosen on demand evidence, each on a co-sell or deeper rung. Okta runs 5-6 deep partnerships on 12-18 month joint roadmaps despite having 7,000+ total integrations (company-reported, not independently audited) - the strongest sourced case for this shape.
- **Category-coverage breadth**: one integration per adjacent category the customer base uses, all at referral/co-sell depth, no deep alliances yet. Cheapest to start, weakest per-partner economics.
- **Platform-anchor**: one dominant platform partnership (certification, marketplace presence, co-sell) plus a thin long tail. Concentrates effort where ecosystem gravity is highest, and concentrates risk the same way.

Recommend one against the interview answers. Then draft the strategy and validate it with the user section by section - partner shortlist, depth placements, governance, certifications, attribution, org - with an explicit approval gate before finalizing. If your harness has persistent memory, store the chosen portfolio, each partner's rung, and the re-ranking answers so later tactical sessions start from decisions, not re-interviews.

## Workflow

1. Build the demand-data prioritization scorecard.
2. Place each selected partner on the depth ladder.
3. Set up joint-roadmap governance for the deep rungs.
4. Decide certification joins, with renewals budgeted.
5. Wire attribution before the program scales.
6. Place the function in the org.

Each step has a section below, in order.

## 1. Prioritize partners with data, not relationships

Partner selection is a data problem. Score every candidate on three filters, evidenced from your own records rather than BD enthusiasm:

- **Customer and prospect demand** - the strongest signal: share of the base already running the candidate's product, plus sales-pipeline data showing which missing integrations kill deals.
- **Market (SAM) expansion** - does the integration open a use case or segment the product cannot reach alone.
- **Competitive necessity** - is the integration table stakes for a segment, or does it neutralize a competitor's advantage.

Mature teams add three quantified signals:

- **Deal-attached revenue** - the dollar value of open deals blocked on each missing integration. A large stalled deal can justify an accelerated build.
- **Ecosystem gravity** - the heavy hitters recurring across the base.
- **Retention/attach lift** - customers with several integrations churn less and close faster. Measure it in your own cohort data.

Run a quarterly prioritization review with monthly intake from sales and CS.

Every partner that makes the shortlist carries a written demand-evidence line - named deals, request counts, or retention data. A candidate with none is rejected or parked, never grandfathered in because someone knows someone.

## 2. Place each partner on the depth ladder

The ladder runs referral → reseller → co-sell/integration alliance → co-build/strategic alliance → OEM/embed. Deeper rungs shift customer ownership toward the partner and add roadmap commitment - full rung-by-rung mechanics in [references/depth-ladder-and-tier-programs.md](references/depth-ladder-and-tier-programs.md).

- effort: `OEM/embed > co-build > co-sell > reseller > referral`
- value: `OEM/embed > co-build > co-sell > reseller > referral`
- compliance cost (descending): `OEM/embed > co-build > reseller > co-sell > referral`
  - OEM licensing puts your product behind the partner's paper with minimum commitments, IP, and indemnity terms, and is the hardest rung to unwind once their customers depend on it.
  - Co-build triggers a joint development agreement with legal sign-off on IP, support, and roadmap.
  - Reselling makes the partner the transacting party, pulling in order-of-record and tax review.
  - Co-sell needs mutual NDA and revenue-share terms.
  - Referral is terminable at will.
- efficiency: `co-sell > referral > reseller > co-build > OEM/embed`

- **Default rung: co-sell/integration alliance.** One built-and-maintained integration plus a joint pipeline motion is where partner-market fit gets proven - repeatable sourced deals, usage uplift, retention improvement - at medium effort. Start with one referral or co-sell motion for 1-3 partner types, prove it, then add depth.
- **Step down to referral** when no integration demand evidence exists yet: near-zero effort buys a signal about whether the partner's base wants you at all.
- **Delete the reseller rung**, rather than demoting it, when your business model cannot support partner-transacted deals. A parked rung silently reappears as scope.
- **Co-build is the starved option**: highest value short of OEM and high effort (a 12-18 month joint roadmap, shared pipeline targets), so it loses every efficiency round. It is promoted anyway when a partner already sources pipeline at a rate justifying the investment, joint customers pull for a productized integration, or platform dynamics make deep embedding defensive.
- **OEM/embed** is promoted only when the partner owns the customer end-to-end and minimum commitments are on the table. Market rev-share runs roughly 10-30% of the partner's revenue from the powered feature.

Gate every graduation on proven joint economics plus the three-fit test (Forecastable): product fit, commercial fit, and operational fit must line up simultaneously, or the deeper motion underperforms regardless of what the contract says. This ranking is a default, not a law - re-rank against questions 5-7 and anything else known about the user: a hard deadline promotes referral, a compounding mandate promotes co-build, and an existing deep relationship with proven joint economics jumps the ladder legitimately.

## 3. Govern the deep rungs like a product

For every partner at co-build depth or beyond:

- Share roadmap visibility from the start, not at launch. Sync at least quarterly on integration performance, upcoming platform changes, and customer feedback.
- Treat each co-build like a product, never a project: its own roadmap, quality bar, security review, and definition of done. Post-launch decay is the default outcome of project framing.
- Write a joint business plan both sides work from: shared targets on a timeline, and which side carries the heavier lift at each phase - so a stall obligates the other side to unblock rather than letting the roadmap slip.
- Run real QBRs: a working session reviewing last quarter against the previous QBR's commitments and setting the next quarter's, with someone in the room on each side who can approve resources. A meeting producing no dated commitments is a status update, not a QBR.
- Default the legal shape to contractual co-development (a joint development agreement scoped to the specific integration, with IP, support, and roadmap terms explicit). Reserve a joint venture for a genuinely shared new entity or product. For the largest alliances, add two-tier governance: an executive steering committee above an operating committee that allocates resources quarterly.

## 4. Join certifications with renewals budgeted

Certification and verification programs are what you join on someone else's platform - distinct from any tier program you might run for your own partners. Two decision inputs: does the platform reach a segment your step-1 evidence names, and can the effort ceiling from question 7 absorb the carrying cost.

The trap is budgeting certification as a one-time project. Across platforms, the renewal is recurring by design:

- Some programs re-certify every major platform release (twice yearly on some platforms); others annually.
- Security reviews carry per-release obligations, and roughly half of first submissions fail on the strictest programs.

Budget certification maintenance as standing engineering work with a named owner, and count it against integration-engineer headcount, before signing up.

Per-program requirements, fees, and renewal cadences - plus current tier names for the major platforms and a warning about widely cited deprecated ones - are in [references/depth-ladder-and-tier-programs.md](references/depth-ladder-and-tier-programs.md). The 2024-2026 restructuring wave renamed tiers on nearly every major platform. Verify against the platform's own current docs before citing any tier name.

## 5. Wire attribution before scaling

A blended "partner-touched" revenue number is discounted by finance for a structural reason: uncapped influence credit is how partner-attributed revenue exceeds total revenue, a result that ends the conversation with the CFO immediately. Report **sourced** (the deal would not exist without the partner) and **influenced** (the deal existed and the partner materially advanced it) as two separate, capped numbers - never one blend.

Four requirements make the data credible:

1. A partner-source field on the CRM opportunity record - attribution in a spreadsheet is structurally impossible to defend.
2. Compensation alignment - AEs paid less on partner deals deprioritize them every quarter. Equalize comp treatment, or co-sell will not happen.
3. Unified forecast review - partner pipeline rolls into the same forecast review as direct pipeline, same exit criteria.
4. Motion-specific design - referral, co-sell, and OEM need different attribution rules. One generic scheme fits none.

Defensible defaults:

- Attribution claimed at deal creation with a dated ID, never reverse-engineered at close.
- A short attribution window: about 14 days from deal creation.
- One sourced partner per deal.
- Credit caps set before the quarter starts.

Report a small executive set inside the dashboards leadership already checks, not a separate partner report nobody opens:

- Sourced vs. influenced revenue.
- Activation rate.
- Time to first deal.
- Partner CAC vs. direct CAC.

Full definitions and benchmark figures, with their sourcing labels, in [references/attribution-and-case-studies.md](references/attribution-and-case-studies.md).

## 6. Place the function in the org

Three placements, ranked:

- effort: `standalone Alliances org > integrations under Product > report into Sales`
- value: `standalone Alliances org > integrations under Product > report into Sales`
- efficiency: `report into Sales > integrations under Product > standalone Alliances org`

- **Default: report into Sales** (Crossbeam's explicit early-stage guidance) - it keeps an unproven function tied to revenue with zero reorganization cost. Build the step-5 attribution plumbing during this phase, before scale.
- **Promote to split roles around the ~100-employee mark** (Crossbeam's Rule of 99, when partnerships get materially more complex): partner/alliance managers plus a partner or integration engineer plus an integration product manager, with the top 10-15 partners treated as named strategic accounts.
- **Migrate integrations under Product when productization becomes the goal** - the Contentsquare pattern: integrations under Product get built for scale and best practices instead of as bespoke BD favors.
- **The standalone Alliances org is the starved option**: a VP-level org with partner ops and partner marketing delivers the most at scale and costs the most to stand up, so efficiency never picks it. It is promoted when partner-sourced revenue becomes a board-level metric and the deep-rung governance of step 3 needs dedicated owners.

Re-rank against question 3: a team already sitting under Product keeps integrations there rather than paying a migration. A company with no owner at all starts at the default rung regardless of size.

## Failure modes

- **Relationship-vibes selection** - a partner shortlisted because the BD lead knows someone. Fix: no shortlist entry without a demand-evidence line (step 1).
- **Too many shallow partnerships** - dozens of listed integrations, none deep, none producing pipeline. Spreading thin is the documented anti-pattern the Okta case argues against. Fix: 1-3 partner types, few-and-deep portfolio.
- **Blended attribution** - one sourced+influenced number, assigned at close, maintained by the person whose quota depends on it. Fix: step 5's two capped numbers and four requirements.
- **Certification-renewal surprise** - the badge budgeted as a launch project, then a platform release lands and re-certification competes with the roadmap. Fix: standing renewal owner and budget before joining (step 4).
- **Vanity partner count** - 200 signed partners, 12 active is not 200 partners. Track activation rate (share of signed partners ever producing a lead or revenue).
- **Comp misalignment** - AEs quietly deprioritizing partner deals because they pay less. The program stalls without anyone deciding it should.
- **Integration run as a project** - no roadmap, no quality bar, no definition of done. It decays the quarter after launch (step 3).
- **Citing deprecated tier names** - several major platforms renamed their programs in 2024-2026, and third-party guides still describe the old tiers. Verify against current platform docs.

## Measurement

No industry pass-standard exists for a strategy document, so these gates are self-set. Iterate the strategy until all three pass.

1. **Evidence coverage**: every partner in the plan carries a demand-evidence line - zero partners selected on relationship alone.
2. **Attribution is structural**: sourced and influenced defined as two capped CRM-level numbers with dated claim IDs and a stated window, before the plan asks for headcount.
3. **Renewals owned**: every certification the plan joins names a renewal owner and a budgeted standing cost.

Watch as trends afterwards, baselined against your own first two quarters:

- Activation rate.
- Partner CAC - a common working benchmark is staying under ~1.5x direct CAC (vendor-published, directional).
- Partner-sourced pipeline.
- Time to first deal.
- Retention/attach lift for integrated customers.

Expect revenue concentration in the top 10-20% of partners. That is normal, not a red flag by itself.

## Invocation examples

- "We have 40 integrations listed and no partnership strategy - help me pick which 5 vendors to actually go deep with."
- "Salesforce is pushing us to certify on their platform. Should we join, and what does it really cost us per year?"
- "Our CFO stopped trusting the partner-influenced revenue number. Rebuild our attribution so it survives finance review."
- "Design a technology-partnership program for our CRM add-on: who to partner with first, how deep, and who should own it internally."

## References

- [references/depth-ladder-and-tier-programs.md](references/depth-ladder-and-tier-programs.md) - the five-rung depth ladder with commercial models, graduation triggers, current tier structures across seven major platforms, and the certification-program comparison with renewal obligations.
- [references/attribution-and-case-studies.md](references/attribution-and-case-studies.md) - precise sourced/influenced definitions, the executive KPI set, named case studies (Okta, ecosystem multipliers, ELG stats) with sourcing labels, QBR mechanics, JDA-vs-JV detail, and the six core roles.

See also, same collection:

- `samber/developer-platform-skills@api-integration-surface-strategy` - the technical umbrella: which integration surfaces (API, webhooks, SDK, MCP…) the product offers. This skill decides who to build with, that one decides what integrations are built on.
- `samber/developer-platform-skills@connector-marketplace-strategy` - whether to run your own marketplace vs. joining others'. This skill covers the bilateral partnerships either way.
- `samber/developer-platform-skills@etl-connector-strategy` - your presence as a source connector on third-party ETL/ELT platforms, a specific partnership surface this skill only points at.
- `samber/developer-platform-skills@partner-app-onboarding` - the partner-developer onboarding path (docs, sandbox tenancy, certification steps) once the partners chosen here start building.
