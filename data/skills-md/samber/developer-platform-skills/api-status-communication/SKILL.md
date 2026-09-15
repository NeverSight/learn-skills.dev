---
name: api-status-communication
description: Design how an API platform communicates status and incidents to external consumers - status-page modeling (the four-stage incident lifecycle, degraded/partial/major component semantics, component granularity), monitoring-driven status instead of a hand-flipped green light, pull and push channels, incident-update cadence and templates, public postmortems for a developer audience, public SLA/SLO reporting, and maintenance-window notices. Use whenever the user mentions a status page, Statuspage, incident updates, uptime or SLA reporting, postmortems, or scheduled maintenance - even if they never say "status communication". Do NOT use for deprecation and breaking-change notices - use samber/developer-platform-skills@api-versioning-policy instead.
license: MIT
metadata:
  author: Samuel Berthe
  version: "1.0.0"
---

# API Status Communication

You are designing how an API platform tells its external consumers what is happening - the status page, incident updates, public postmortems, SLA/SLO reporting, and maintenance notices. The deliverable is a communication practice, not a monitoring stack: measurement belongs to the platform's observability tooling; you own what the outside world sees and when.

Trustworthiness is the design constraint every step below serves. A status page is a trust signal before it is a technical tool, and the documented failure mode is status theater: one sourced case (OneUptime) shows a page reading green for the first 35 minutes of a 54-minute incident because a human had to decide to flip it.

The visible symptom of lost trust is migration to third-party complaint aggregators (DownDetector et al.) - users prefer them not because they are more accurate but because they aren't controlled by the company having the outage. Treat that migration as this practice's failure metric, and tie status to real monitoring rather than human gatekeeping throughout.

## Clarifying questions

Ask these before designing anything; each answer changes a later step. Batch them - this is a tactical design task, not a strategy interview.

1. Existing status page or greenfield? If one exists, request its URL and the full update history of the last 2-3 incidents.
2. Is status set by monitoring today, or does a human flip it? Which health checks, latency thresholds, and uptime probes already exist?
3. Who reads the page: integrating developers, business stakeholders/end customers, enterprise customers - in what mix? (see next section)
4. Are there contractual SLAs with consequences attached, and do any contracts specify a maintenance-notice floor?
5. Does the status page share infrastructure with the platform itself (same DNS, CDN, cloud account)? (drives channel redundancy in step 3)
6. In the last few incidents, how did consumers actually find out - and did any third party report the outage before the page did?
7. Deadline and effort ceiling - three sub-questions:
   - By when must this practice be live?
   - Is it a one-off fix after a bad incident, or a compounding trust asset you will run for years?
   - What can you spend: engineering hours to wire monitoring, an on-call rotation to hold cadence, budget for per-message channels?

Question 7 exists because the channel and postmortem menus diverge sharply on effort and on how long the payoff lasts, and neither ranking in steps 3 and 5 can be picked without it.

- A hard deadline promotes the rungs hosted tooling gives you nearly free.
- A compounding-asset mandate promotes out-of-band redundancy and the deep write-up.

If your harness has persistent memory, store the practice's core decisions: component model and blend rule, escalation thresholds, channel set, postmortem-depth policy, published SLA edge cases. Later runs - a live incident, a postmortem, a maintenance notice - start from the practice instead of re-deriving it.

## Reader roles

Regardless of whoever bought the product, the people reading a status page during an incident split by role, and the two roles want different pages:

- **Integrating developers** - want component-level technical detail: which endpoints, per-region scoping, latency numbers, timestamps, and a postmortem deep enough to trust. They wire status into their own alerting, which makes machine-readable push channels (webhook, RSS) first-class.
- **Business stakeholders and end customers** - want plain language: is it down, what's affected, when will it be fixed. Latency metrics read as noise to them.

Audience-tiered pages are the established pattern for API providers when the mix demands it:

- A public developer-facing page with API-level detail.
- An enterprise page behind SSO showing SLA compliance.
- Plain-language end-user messaging.

Default to one public developer-facing page and add tiers only when question 3 shows a real second audience - every extra tier is another surface to keep consistent during a live incident.

## Workflow

1. Model the status vocabulary and component granularity.
2. Wire status to monitoring - the trust step.
3. Choose the channels: pull page plus push subscriptions.
4. Design the incident-lifecycle communication practice.
5. Set the postmortem policy.
6. Publish SLA/SLO reporting.
7. Set maintenance-window conventions.

Each step has a section below, in order.

## 1. Model statuses and components

- Use the four de facto incident-lifecycle statuses below. Subscribers already read this vocabulary (it is Statuspage's, industry-wide); a custom set costs comprehension and buys nothing.
  - **Investigating** - alerted, looking into a potential problem.
  - **Identified** - cause or affected component confirmed.
  - **Monitoring** - fix deployed, being watched.
  - **Resolved**
- Model component severity as **breadth of impact, not felt severity** - the single most load-bearing decision here.
  - Degraded Performance: works but slow for everyone.
  - Partial Outage: completely broken for a subset (e.g. one region).
  - Major Outage: unavailable for everyone.
- Cap the page at four visual states (operational / degraded / partial / major, the industry green-yellow-orange-red). Five severities across many components is a matrix no reader holds in their head mid-incident.
- Aggregate the top-level page status from the worst component state, and document the blend rule you choose so it is applied consistently, not re-argued per incident.
- Choose component granularity by the user's mental model of the product, never by internal architecture - forty microservice names turn the page into noise exactly when it must be parseable. Group into a handful of consumer-recognizable components (e.g. API, dashboard, webhooks, docs) rather than one flat internal list.
- Scope regional incidents regionally: one data center down should read as a scoped partial outage, not a blanket "degraded" alarming users elsewhere - Cloudflare's page signals per-region for exactly this reason.
- Note the uptime-math consequence now: Degraded Performance conventionally counts as 0% downtime in SLA arithmetic, so a headline uptime figure can look excellent while masking real incidents. Step 6 handles the honest-reporting side of this.

## 2. Wire status to monitoring

- Tie page state directly to health checks, latency thresholds, and uptime data. No human gate decides whether customers "deserve to know" - that gate is what produced the 35-minute green lie.
- Auto-open an **Investigating** incident from the monitoring alert; humans then add substance, scope, and cadence. The human role is enrichment, never first disclosure.
- Write down your own staged escalation pipeline - the explicit rule for when an internal event becomes a public communication. Copy Cloudflare's citable staging below, set your own thresholds.
  1. Events trigger alerts.
  2. Some alerts become incidents of note.
  3. All are triaged.
  4. Some become problems.
  5. "Major" problems trigger status-page updates.
  6. P1 majors require a full published incident report.
- Include at least one workflow-level probe (a real multi-step user journey), not only infrastructure checks: infrastructure-green and product-broken are different claims. The sourced cautionary case (Sentry) is a retailer at perfect uptime while checkout was silently broken for a user segment.
- Hold the granularity tension honestly rather than resolving it by fiat: in almost any real outage most components still show green, and ThousandEyes' point is that a locked-out user does not care that everything but authentication is fine.
- An all-red page fails the reader in the other direction - that is the "sea of green dots" criticism aimed at AWS, cutting both ways. Step 1's granularity is the mitigation here, not a slogan.
- Aim for calibrated accuracy, not maximal alarm. A long green history honestly earned is itself valuable (Splunk): it stops one outage from reading as "the whole product is unreliable".
- Expect transparency to pay back: the trust–transparency paradox documented around Cloudflare's practice is that openly admitting failure increases customer trust in the provider's competence to handle the next one. A well-run public incident is evidence, not only liability.

## 3. Choose the channels

A status page is a **pull** channel - the customer has to go check it. Subscriptions (email, RSS, webhook, SMS) are **push**. Cloudflare's own self-critique of its pull-only page - it creates "confusion and wasted resources" during live incidents - is the design argument: a mature practice needs both, not either.

- efficiency: `page + built-in email/RSS subscription > webhook push > SMS push`
- value during a live incident: `any push channel > the pull page alone`
- effort: `SMS push > webhook push > page + email/RSS subscription`

- **Default rung: the status page with email and RSS subscription enabled.** With hosted status tooling this comes nearly free, and subscription is a support-load lever, not a courtesy - letting affected users self-serve the answer measurably reduces inbound tickets during an incident (Atlassian).
- **Promote webhook push** when question 3 says developers: an integrator audience wires status into its own alerting, and machine-readable push is what makes that possible. If the platform already runs webhook infrastructure, this rung gets cheap - the delivery machinery is sibling `samber/developer-platform-skills@webhook-platform-design` territory; you only define the status event.
- **Promote SMS/phone-grade push** for enterprise customers with contractual SLAs - the audience whose contracts (question 4) often expect it, and the only rung whose per-message cost and deliverability work justify the effort.
- **Deleted, not demoted: SMS/phone-grade push with no contractual audience.** When question 4 returns no SLAs with consequences and question 3 no enterprise tier, this rung leaves the menu rather than sitting at its bottom - per-message cost and deliverability work bought for nobody. Not parked last, because "we could add SMS later" reappears as scope every time an incident feels loud. Re-promotion trigger: the first contract that specifies a notification channel.
- **The starved option: out-of-band redundancy** - hosting the page off the platform's own infrastructure and keeping at least one channel that works when your DNS or CDN is down. Highest effort, invisible value on a good day, so it loses every efficiency round; question 5 is what promotes it, because a status page that dies with the platform is worth nothing at the only moment it matters. Status pages becoming unreachable during the outage they should be reporting is a documented failure mode.
- This ranking is a default, not a law. Re-rank against what you know about the user and say which answer moved which rung:
  - An enterprise-heavy base promotes SMS.
  - An integrator base that already consumes the platform's webhooks gets webhook push nearly free.
  - A page already hosted on shared infrastructure makes redundancy the first task rather than the last.
  - Question 7's effort ceiling decides how many rungs land in the first pass.

## 4. Design the incident-lifecycle communication practice

Run every incident through the four statuses of step 1, writing updates against Atlassian's five practices - the industry checklist:

1. **Early** - an update saying "still investigating, nothing new yet" beats silence; silence makes readers assume the worst.
2. **Often** - commit to a cadence: every update names the time of the next one, and that promise is kept even with nothing new to say.
3. **Precise** - facts over speculation; state what is confirmed, not what is suspected.
4. **Consistent across channels** - page, social, email must say the same thing at the same time; a customer mid-incident experiences "your service is broken" regardless of whose fault it technically is.
5. **Own it with empathy** - acknowledge impact, apologize when warranted, and never deflect to an upstream vendor even when the root cause is genuinely theirs.

Title incidents in plain language stating the nature of the problem ("Elevated error rates on the REST API in eu-west"), never internal codenames - internal template names exist for team organization and must not surface publicly. Map your internal severity vocabulary (SEV1-4 or equivalent) onto component states once, in writing, so responders know what to flip without debating it mid-incident.

See [references/incident-update-templates.md](references/incident-update-templates.md) for per-status update templates, a severity-to-component-state mapping, and good/bad update pairs.

## 5. Set the postmortem policy

Publishing a postmortem externally is a deliberate decision - it affects legal exposure, customer trust, and reliability culture. The sourced default for developer platforms leans toward publishing anyway.

Google SRE's position is that a postmortem's value is proportional to the learning it creates, so sharing it "perhaps even with your customers" multiplies that value. Google SRE also calls a thoughtful and honest postmortem "a key tool in restoring shaken trust."

Depth ladder for what to publish per incident:

- value for rebuilding developer trust: `engineering-blog postmortem > status-page summary postmortem > resolved-note only`
- effort: `engineering-blog postmortem > status-page summary postmortem > resolved-note only`
- compliance cost: `engineering-blog postmortem > status-page summary postmortem > resolved-note only` - the deep write-up triggers legal and comms sign-off on cause language and named third parties, and every rung is irreversible once published: you can append a correction, never unpublish an admission an enterprise customer already screenshotted.
- efficiency: `status-page summary postmortem > resolved-note only > engineering-blog postmortem`

- **Default rung: the status-page summary postmortem** - impact, cause, fix, prevention in a few paragraphs, attached to the incident. Owed for any incident that consumers visibly felt.
- **Step down to a resolved-note only** for brief blips with no consumer-visible impact beyond the incident entry itself.
- **Promote to a full public postmortem** for major (P1-class) incidents - Cloudflare mandates a published incident report at that tier - and whenever trust is visibly shaken. For an API audience the engineering blog is the right channel: that audience is technical and reads the deep version for trust-building, not just resolution confirmation.
- The full blog write-up is the starved rung - highest value, highest effort, loses every efficiency round - and the promotion conditions above are exactly what override that. This ranking is a default, not a law: re-rank against question 7 and the user's assets, and say which answer moved which rung.

- An active engineering blog and practiced writers get the deep write-up nearly free, which flips the effort line.
- A one-off fix under a hard deadline holds every incident at the summary rung.

Structure the external document around the three questions a customer actually has - why did this happen, could it have been worse, how do you make sure it won't happen again - and keep it blameless in the concrete sense: never name an individual human. Postmortems without follow-through are theater; action-item completion is part of this skill's measurement, not an afterthought.

See [references/public-postmortem-structure.md](references/public-postmortem-structure.md) for the full structure, the internal-to-external filtering step, blameless-writing rules, and a skeleton.

## 6. Publish SLA/SLO reporting

- Keep the three terms distinct in everything public:
  - **SLIs** are measured metrics.
  - **SLOs** are internal targets.
  - **SLAs** are contractual commitments with consequences.
- Publishing a number you privately treat as aspirational is how disputes start.
- A public SLA/uptime page is a distinct artifact from the status page, not a rebrand: it shows historical uptime against commitments; the status page shows discrete current incidents and can cover components with no formal SLA at all. A mature practice offers both - they answer "are you meeting your number" and "what is happening right now" respectively.
- Define the edge cases in writing before publishing any number, each a documented dispute source:
  - The response-time threshold above which a slow response counts as down.
  - Whether the SLA is evaluated service-wide or per affected component.
  - That planned maintenance is excluded only when adequate notice was given.
- Translate percentages into stakes: state targets as minutes of allowed downtime per month alongside the percentage, and show error-budget burn where that model is in use.
- Publish incident history next to the headline uptime figure. Step 1's uptime-math caveat means the percentage alone can mask real degradation - the honest page lets a reader check the number against the incidents behind it. "Monitoring without reporting is just watching"; reporting is what turns the metric into either evidence of a kept promise or a transparent admission of a missed one.

See [references/sla-maintenance-reporting.md](references/sla-maintenance-reporting.md) for edge-case definitions, the percentage-to-minutes table, and worked examples.

## 7. Set maintenance-window conventions

This skill owns the 24-hour-to-2-week notice horizon. The 6-12-month runway for deprecations and breaking changes is sibling `samber/developer-platform-skills@api-versioning-policy` territory - a maintenance window and a deprecation are different communications with different timelines; never blend them into one announcement.

- Scale notice with impact and audience:
  - Roughly 24 hours for minor low-impact work.
  - Weeks plus reminder notifications for major changes.
  - Enterprise customers conventionally get a week or more, even for changes that would be same-day for self-serve users.
- Check question 4's contracts for hard floors - a 5-business-day contractual minimum is a documented real-world example.
- State exact start and end times with an explicit time zone - ambiguous timing is the single most common cause of maintenance confusion - and schedule against the affected users' low-traffic hours, not the provider's office hours.
- State scope precisely: which endpoints and features are affected and which stay available, never a blanket "the API will be down".
- Post start and completion confirmations even for short windows; visible progress signals the work is controlled.
- Publish through the status page plus at least one push channel, never the page alone (step 3's pull-vs-push logic applies to planned work too).
- Do not treat SLA exclusion as trust exclusion: a badly communicated window still costs trust even when the arithmetic forgives it.

Notice templates live in [references/sla-maintenance-reporting.md](references/sla-maintenance-reporting.md).

## Failure modes

Anti-pattern checklist - each is a direct audit finding:

- Status theater: monitoring is red, the page is green, because a human hadn't decided to flip it yet.
- A third-party aggregator or social media reports the outage before the status page does.
- Silent degraded: latency doubles for everyone and nothing is posted because the service is "technically up".
- Components mirror internal architecture; the page is unreadable mid-incident.
- Severity modeled as felt badness instead of breadth of impact.
- The status page shares infrastructure with the platform and goes down with it.
- An open incident with no update and no promised next-update time.
- A public update deflecting blame to an upstream vendor.
- A postmortem that names an individual, or one whose action items quietly die.
- A headline uptime percentage published with no incident history beside it.
- A maintenance notice with no time zone, or a blanket "the API will be down".

## Measurement

- Detection-to-disclosure lag: the first public status change is generated from monitoring; measure alert-fired-to-page-updated on every incident and drive it to minutes. A lag in tens of minutes means a human gate is still in the loop - the 35-minutes-green case is the anti-benchmark.
- Third-party-first disclosures: zero incidents where an outside aggregator or social post beat the page. Binary, per incident.
- Lifecycle completeness: every incident shows all four statuses with timestamps, and every update's next-update promise was kept.
- Postmortem follow-through: track public action-item completion; below ~50% is the sourced threshold at which postmortems become theater, so set your target above it and report against it.
- Support-load trend: inbound tickets during incidents should fall as status subscriptions grow - the sourced direction (Atlassian); no industry threshold exists, so baseline from your own next incident and improve against it.

The first three are gates - iterate the design until they pass. The last two are trends to watch afterwards, never pass thresholds.

## Invocation examples

- "Design a status page for our public API - today we only tweet when something breaks."
- "Our status page stayed green through yesterday's outage and customers found out from DownDetector - fix the practice, not just the page."
- "Write the public postmortem for last week's 90-minute API outage and tell me whether it belongs on the status page or the engineering blog."
- "We're taking the API down for a two-hour migration in ten days - plan the maintenance communication."

## References

- [references/incident-update-templates.md](references/incident-update-templates.md) - per-status update templates, severity-to-component-state mapping, good/bad update pairs, the five-practices checklist expanded.
- [references/public-postmortem-structure.md](references/public-postmortem-structure.md) - public postmortem structure, internal-to-external filtering, blameless-writing rules, action-item tracking, skeleton.
- [references/sla-maintenance-reporting.md](references/sla-maintenance-reporting.md) - SLI/SLO/SLA distinctions, edge-case definitions, percentage-to-minutes table, maintenance-notice scaling and worked examples.

See also, same collection:

- `samber/developer-platform-skills@api-error-design` - designs what a single failed request returns; when the failure is the platform's fault at scale, this skill owns telling everyone.
- `samber/developer-platform-skills@api-versioning-policy` - deprecation and breaking-change communication on the 6-12-month horizon; this skill stops at the 2-week maintenance notice.
- `samber/developer-platform-skills@webhook-platform-design` - the webhook delivery machinery a status webhook-push channel rides on, and delivery status of webhooks themselves.
- `samber/developer-platform-skills@integration-error-observability` - per-integration error surfacing to an individual consumer, versus this skill's one-to-many broadcast.
- `samber/developer-platform-skills@developer-portal-design` - the portal that links the status page as a first-class entry point.
