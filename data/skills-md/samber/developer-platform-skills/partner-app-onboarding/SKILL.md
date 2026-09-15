---
name: partner-app-onboarding
description: Design the partner-developer onboarding journey on a B2B SaaS platform - from partner signup through dev-account and sandbox provisioning, docs, education and certification posture, and support channels, to the first submitted app. Use whenever the user mentions partner developer onboarding, developer program entry, self-service vs application-gated registration, sandbox tenancy for partners, certification gating submission, partner support channels, or time-to-first-submitted-app - even if they never say "onboarding". Journey design only. Do NOT use for review-gate mechanics (samber/developer-platform-skills@app-marketplace-review) or sandbox isolation architecture (samber/developer-platform-skills@api-test-mode-design).
license: MIT
metadata:
  author: Samuel Berthe
  version: "1.0.0"
---

# Partner App Onboarding

You are a platform-program designer. Design the journey a partner developer travels on the user's B2B SaaS platform, from "signs up as a partner" to "first app submitted for review".

The journey covers:

- the registration gate
- dev-account and sandbox provisioning
- education and certification posture
- support channels
- the funnel instrumentation that shows where partners stall

The output is an onboarding design the platform team can implement and measure.

## Interview

Ask before proposing anything. One question per message, multiple-choice where offered - the answers pick rungs in every menu below.

1. What do partners build? (a) marketplace apps (b) private integrations for shared customers (c) both.
2. What exists today? (a) no program - designing from zero (b) signup exists, the journey after it is ad-hoc (c) full journey live, being revisited.
3. How long does a competent developer need to reach a first working app on your platform? Hours / days / weeks-to-months. This is the strongest gate-selection signal.
4. How sensitive is the data partner apps touch (regulatory exposure, customer-trust risk)? High / medium / low.
5. Who are the partners? (a) mostly individual developers and small teams (b) mostly commercial ISVs selling through you (c) a mix.
6. What support capacity exists as a standing commitment - docs writers, community moderation, partner-manager headcount?
7. By when must the journey be live - a hard date, or open-ended?
8. Is the goal a one-off win (specific partners already waiting to build) or a compounding asset (a growing developer ecosystem)?
9. What is the effort ceiling - engineering hours for provisioning automation, education-content budget, support headcount?

Questions 7-9 re-rank the menus below:

- a hard deadline promotes low-effort rungs (own-account sandbox, docs-plus-forum support)
- a compounding mandate promotes slow ones (credentialed education, community programs)
- the effort ceiling deletes rungs outright rather than demoting them

## Workflow

1. Map the journey stages and pick a stage model.
2. Choose the entry gate.
3. Design provisioning - sandbox tenancy and credentials.
4. Set the education and certification posture.
5. Build the support-channel ladder.
6. Sequence the commercial decisions late.
7. Instrument the funnel.

Validate each step's choice with the user before moving to the next - every later step assumes the gate chosen in step 2.

## 1. Map the journey

Write the journey as explicit named stages before designing any single one - an unnamed stage never gets an owner or a metric. Two citable models exist, both platform-documented:

- Atlassian's own onboarding guide: a four-phase model, Plan, Build, Launch, Grow
- Salesforce's seven-milestone ISV journey

Adopt, adapt, or replace them, but name the stages.

One structural rule dominates, observed at four of the five major ecosystems studied (platform-documented, see [references/platform-archetypes.md](references/platform-archetypes.md)): decouple "start building" from "get approved." Accounts, sandboxes, and credentials provision instantly and free. Human review concentrates at the app-submission gate, where it actually protects end customers.

## 2. Entry gate

Three rungs, ranked:

- effort (descending): `application-reviewed registration > agreement-split entry > self-service signup`
- trust and control (descending): `application-reviewed registration > agreement-split entry > self-service signup`
- compliance cost (descending): `application-reviewed registration > agreement-split entry > self-service signup`
  - a reviewed gate needs a countersigned company-level agreement and a documented admission decision per applicant, and unwinding an admitted partner is a contract termination
  - the seller track adds KYC/KYB identity data, so privacy and data-residency review applies, but only for partners who opt into selling and only reversibly
  - a click-through program agreement needs one legal sign-off, then none per partner
- efficiency: `self-service signup > agreement-split entry > application-reviewed registration`

- **Default rung: self-service signup.** A form plus a program-agreement checkbox, no human in the loop - the entry shape at four of the five ecosystems studied (platform-documented). Every reviewer hour spent at registration is spent before the partner has produced anything worth reviewing.
- **Promote to agreement-split entry** when commercial sellers transact through the platform: keep building ungated for everyone, and add a separate verified seller track - agreement signature, KYC/KYB identity checks - that gates selling, never building. This is the split Atlassian formalized in its 2025 marketplace-security update (platform-documented).
- **Starved option: application-reviewed registration** - a human reviews every partner application before any access (the Salesforce shape: a days-long review, company-level agreement acceptance blocking every user until signed - platform-documented). Highest trust per admitted partner, and its cost scales with every applicant, so it loses every efficiency round. It gets promoted anyway when either applies:
  - question 3 answers weeks-to-months: the environment model is complex enough that unguided partners fail, so guided pre-launch stages earn their overhead
  - question 4's answer means you must know who is building before granting any data access

Every ranking in this skill is a default, not a law - re-rank each against questions 3-5 and anything else you know about the user, and say which answer moved which rung.

Entry tiers deserve a separate warning: at four of five platforms studied, the "entry tier" gates nothing - real partner tiers are earned post-launch on performance (platform-documented). Ladder depth belongs to `samber/developer-platform-skills@connector-marketplace-strategy`.

Don't invent a graded entry ladder. Salesforce's pre-launch Registered → Exploration → Build stages are the documented exception, justified by its build complexity, not a norm to copy.

## 3. Provisioning

Grant sandbox tenancy and credentials at signup, not after review. Three rungs, ranked:

- effort (descending): `production-mirror sandboxes > instant dedicated dev tenancy > own-account-as-sandbox`
- fidelity and partner experience (descending): `production-mirror sandboxes > instant dedicated dev tenancy > own-account-as-sandbox`
- efficiency: `own-account-as-sandbox == instant dedicated dev tenancy > production-mirror sandboxes`

The `==` is genuine: own-account buys less for near-zero effort, dedicated tenancy buys more for more, and the ratios are comparable - question 4, not the ratio, makes this pick.

- **Default rung: instant dedicated dev tenancy** - a free dev instance, store, or account created at signup, no time limit, no payment info (the Shopify and Atlassian shape, platform-documented). This is what "decouple building from approval" looks like as infrastructure.
- **Step down to own-account-as-sandbox** when partner actions are safe and reversible inside a real tenant: the partner's own workspace doubles as the test environment, and a first app runs live there minutes after signup (the Slack CLI shape, platform-documented). Near-zero platform effort. The moment apps touch money, irreversible actions, or other tenants' data: delete this rung, don't demote it - a parked unsafe option silently reappears as scope.
- **Starved option: production-mirror sandboxes** - full-fidelity replicas with realistic data and scale. Highest fidelity, heaviest to build and meter, so this rung loses every efficiency round. The sourced platforms ration them (platform-documented):
  - Slack quotas its provisioned enterprise sandboxes
  - HubSpot gates production-mirror sandboxes behind a paid tier

  Promoted when partner apps genuinely can't be validated without production-realistic behavior: enterprise-grade apps, data-heavy integrations.

Isolation architecture, test-key prefixes, magic test values, and graduation-to-live mechanics belong to `samber/developer-platform-skills@api-test-mode-design` - this step decides when tenancy is granted and what shape it takes, not how the sandbox isolates.

## 4. Education and certification posture

Three rungs, ranked:

- effort (descending): `mandatory pre-submission certification > credentialed education loop > optional parallel track`
- first-submission quality (descending): `mandatory pre-submission certification > credentialed education loop > optional parallel track`
- efficiency: `optional parallel track > credentialed education loop > mandatory pre-submission certification`

- **Default rung: optional parallel track.** Courses and docs available from day one, required by nothing - the posture at all five ecosystems studied: none gates first submission on certification (platform-documented). The review gate is where quality gets enforced; education exists to help partners pass it faster.
- **Promote to a credentialed education loop** when partner credibility is a buyer-facing signal: named, displayable certificates (Shopify Academy's Verified Skills path, Atlassian's Forge Fundamentals certificate, HubSpot Academy's "Learn. Build. Certify. Repeat." loop - all platform-documented), still non-gating, refreshed continuously rather than cleared once.
- **Starved option: mandatory pre-submission certification.** Highest first-submission quality per partner, highest friction, loses every efficiency round - and it is not standard practice on any major marketplace. Promoted only when first-review fail rates stay above roughly 30-40% (self-set, not an industry standard) after a pre-submission validator already exists, and failure analysis traces to partner knowledge gaps rather than docs gaps.

Beware the certification wall: where certification exists but sits behind post-launch eligibility bars (HubSpot requires at least 6 months listed and 60 active installs before certification opens - platform-documented), partners discover the wall after believing onboarding was done. Whatever the posture, disclose every post-launch threshold inside the onboarding docs, never at the moment the partner hits it.

## 5. Support channels

These rungs stack - each layers on the previous, never replaces it.

- effort (descending): `named partner managers > office hours > real-time community chat > docs + community forum`
- unblock power (descending): `named partner managers > office hours > real-time community chat > docs + community forum`
- efficiency: `docs + community forum > real-time community chat > office hours > named partner managers`

- **Default rung: docs plus a self-serve community forum.** Answers compound - every answered thread deflects the next partner's ticket.
- **Promote to real-time community chat** (plus periodic townhalls) once repeated questions cluster; the heaviest self-service program studied runs a 35,000+-member partner chat community (platform-documented).
- **Promote to office hours** when a recurring hard step - a review gate, a complex environment model - generates questions that need a platform engineer rather than a peer (Salesforce runs biweekly partner office hours plus case-based security-review office hours - platform-documented).
- **Starved option: named partner managers.** Highest unblock power, scales only with headcount, loses every efficiency round. Question 5 answering commercial-ISV promotes it for that segment only - the platform-documented pattern assigns named managers to commercial partners, never to every individual developer.

## 6. Sequence commercial decisions late

- Defer the monetization-model choice to the launch stage, never registration: the platform-documented pattern asks Free / Paid-via-platform / Paid-via-vendor as the last gate before listing. A partner forced to price an app they haven't built answers randomly and resents the form.
- Same for commercial agreements beyond the basic program agreement: a seller or distribution agreement belongs at first listing (that's the agreement-split entry from step 2), a revenue-reporting obligation at first sale.
- Post-launch performance tiers and featured placement are `samber/developer-platform-skills@connector-marketplace-strategy`'s scope - link partners to them from onboarding docs, but keep them out of the entry path.

## 7. Instrument the funnel

Marketplaces keep their partner-onboarding conversion numbers internal, so instrument your own from day one at four checkpoints:

1. signup → sandbox/credentials provisioned
2. provisioned → first API call
3. first API call → first app submitted
4. submission → approval

The headline metric, time-to-first-submitted-app, is effectively yours to coin: the named metrics sit either side of it - time-to-first-call before, "time to first deal" after. Flag it as self-defined wherever you report it. Definitions, the adjacent named frameworks, and the underlying evidence live in [references/funnel-metrics-and-benchmarks.md](references/funnel-metrics-and-benchmarks.md).

Working thresholds, each attributed in that reference file:

- Checkpoint 2 above ~10 minutes → fix onboarding friction before anything else; the drop-off evidence, drawn from general developer-tool funnels rather than marketplace-partner data, puts the largest leak before the first API call.
- First-review fail rate above ~30-40% → build a pre-submission validator before considering mandatory education (self-set threshold).
- Time-to-first-submitted-app far exceeding review duration → the bottleneck is docs and enablement, not the review team.

Baseline against your own first quarter and iterate the journey until every checkpoint's conversion improves quarter over quarter - measure the trend, and set no absolute pass bar.

If your harness has persistent memory, record the chosen entry gate, provisioning rung, certification posture, support ladder, and each rung's promotion condition - later runs (review-process design, listing standards, tier ladders) should inherit these choices instead of re-asking.

## Failure modes

- **Sandbox behind the review gate.** Partners approved to build but unable to test churn silently in the gap. Fix: provisioning at signup (step 3) - the four-of-five-platform norm exists because this failure is universal.
- **Graded entry ladder nobody needs.** Copying a pre-launch stage model onto an hours-to-first-app platform adds friction with no guidance value. Fix: step 2's default honestly applied; entry tiers gate nothing at most real programs.
- **Monetization asked at registration.** An upfront pricing form collects noise and scares off partners still exploring. Fix: step 6 - commercial decisions land at launch.
- **Hidden post-launch walls.** Install-count or tenure thresholds for review eligibility or certification (both platform-documented: a marketplace review requiring ≥5 active installs before it starts; certification requiring 6 months and 60 installs) hit partners after they think they're done. Fix: disclose every threshold in the onboarding docs.
- **Review-gate surprise.** Partners discover requirements at first rejection; developer-community threads at two studied platforms describe 2-3 rejection cycles, clustering on UI standards, data-privacy webhooks, and billing compliance (developer-community-reported). Fix: publish the review checklist inside onboarding docs and offer a pre-submission validator.
- **Certification as bouncer.** Gating submission on a course completes the funnel's leak, not the app's quality. Fix: step 4's default - enforce quality at review, teach in parallel.
- **Unmeasured funnel.** Without the four checkpoints, "partners sign up but nothing ships" has no diagnosis. Fix: step 7 before launch, not after the first stall.

## Invocation examples

- "We're launching a developer program for our CRM platform - design the journey from partner signup to first submitted app."
- "Partners sign up but never submit anything. Audit our onboarding: where are they stalling and what do we fix first?"
- "Should partner registration be application-reviewed like Salesforce or self-service like Shopify, and when do we provision sandbox tenancy?"

## References

- [references/platform-archetypes.md](references/platform-archetypes.md) - five onboarding archetypes: entry gate, provisioning, education, support, and review-stage shape per platform.
- [references/funnel-metrics-and-benchmarks.md](references/funnel-metrics-and-benchmarks.md) - metric definitions, adjacent named frameworks, review-stage durations, drop-off evidence, and thresholds.

See also, same collection:

- `samber/developer-platform-skills@app-marketplace-listing-standards` - listing content standards the partner meets at submission time.
- `samber/developer-platform-skills@app-marketplace-monetization-model` - the seller-agreement, fee, and payout mechanics behind the commercial decisions this journey sequences late.
- `samber/developer-platform-skills@developer-portal-design` - the docs and portal surface the whole journey runs through.
- `samber/developer-platform-skills@integration-partnership-strategy` - which partners to court in the first place, upstream of onboarding them.
- `samber/developer-platform-skills@app-marketplace-launch-marketing` - recruiting and promoting a founding cohort; this journey is what those recruited partners then walk, so a launch date sets the deadline the provisioning and support rungs here must meet.
