---
name: integration-error-observability
description: Design how a platform surfaces integration failures to the external developers and partners who built against it - per-integration request/event/delivery logs with replay, correlation IDs that survive from response header to support ticket, error-rate aggregation per API key or app split by 4xx/5xx/429, proactive partner notification with cooldowns against alert fatigue, and a provider-side fleet view of which integrations are breaking. Use whenever the user mentions a developer-facing error dashboard, exposing request logs to integrators, alerting partners about broken integrations, or cutting integration support tickets - even if they never say "observability". Do NOT use for platform-wide incident comms - use samber/developer-platform-skills@api-status-communication instead.
license: MIT
metadata:
  author: Samuel Berthe
  version: "1.0.0"
---

# Integration Error Observability

You are designing what an external developer can find out about their own broken integration, without opening a support ticket. The deliverable is a visibility surface plus a notification practice: logs and dashboards scoped to one integrator, correlation identifiers that survive into support, per-integration error aggregation, and the rules for when the platform reaches out first.

The asymmetry is the whole problem. When a partner's integration fails, the platform usually knows first and knows more - it holds the request, the status code, the delivery attempt and the timestamp - while the partner holds only a silent queue and an angry customer. Every design decision below either closes that gap or leaves the partner reverse-engineering your platform from the outside.

## Clarifying questions

Ask these before designing anything. Each answer moves a later ranking. Batch them - this is a tactical design task, not a strategy interview.

1. What can an integrator see today without asking you? Send the URL if any surface exists. "Nothing" is a valid and common answer.
2. Who breaks: engineers at a single customer integrating for their own use, commercial partners whose app runs across a fleet of installs, no-code and agent builders, or a mix? (see next section)
3. Classify the last 20 integration support tickets: request not found, webhook never arrived, silent data mismatch, auth or credential failure, rate-limit confusion. The shape of that pile decides which surface to build first.
4. Is every inbound request already tagged with an integration identity - API key, app or client ID - at ingestion? Aggregation is only ever as granular as the tag it is keyed on.
5. Do webhooks exist, and does the delivery machinery already record per-attempt outcomes? (decides the default rung in step 2)
6. When an integration breaks, does the partner lose money within hours, or is it noticed at the next reconciliation? (decides the notification posture in step 5)
7. What can you legally show? Do request and response bodies carry PII, secrets, or data belonging to another tenant, and who signs off on exposing them to a third party?
8. Deadline, payoff shape and effort ceiling: by what date must this be live, is it a one-off fix after a bad support quarter or a compounding platform surface you will run for years, and what can you spend - engineering weeks, log storage, an on-call rotation to answer the alerts you start sending?

Question 8 exists because every menu below diverges sharply on effort and on how long the payoff lasts. A hard deadline promotes whatever you already record and merely have to expose, while a compounding-surface mandate promotes the rungs that need new storage, new state, or a new outbound channel.

Question 7 can delete rungs outright rather than reorder them - a legal answer of "those bodies can never leave our tenancy boundary" removes payload-level logging from the menu instead of demoting it.

If your harness has persistent memory, store the surface's core decisions - which logs are exposed, the retention window, the identity the aggregation is keyed on, the alert thresholds and cooldown, the redaction rules - so a later run adding an event type or tuning an alert starts from the design instead of re-deriving it.

## Integration ownership

How many end users sit behind the failing integration decides whether a dashboard is enough:

- **Single-account integrators** - a customer's own engineers wiring your API into their systems. One account, one dashboard, one set of credentials. A good self-serve log surface genuinely finishes the job for them: they will go look when something breaks, because their own users are already complaining.
- **Partners and ISVs with a fleet of installs** - their app runs across tens or thousands of customer accounts, and each install can fail independently. A per-account dashboard is structurally useless to them: nobody watches a thousand dashboards, so they need cross-install aggregation and push notification instead, or they learn about breakage from their own customers. This is the segment that makes steps 5 and 6 load-bearing rather than optional.
- **No-code and agent builders** - assemble a flow, cannot read a stack trace, and will not correlate anything. They need one plain-language failure list scoped to their flow, and a "what do I do about it" line next to each entry. Detail that helps the other two segments reads as noise here.

Serve every segment your answer to question 2 names. A surface designed only for the first segment is the documented default failure: the platform ships logs, calls integration visibility done, and its partner base still finds out about outages from end users.

## Workflow

1. Audit what an integrator can see today.
2. Expose per-integration failure detail.
3. Make the correlation ID reach support.
4. Aggregate error rates per integration identity.
5. Decide the notification posture.
6. Build the provider-side fleet view.

Each step has a section below, in order.

## 1. Audit what an integrator can see today

Start from the support pile (question 3), not from an architecture diagram. For each of the last 20 integration tickets, answer one question: could the integrator have answered this themselves with a surface you could reasonably ship? The share that says yes is your baseline, and it is the number every later step is trying to move.

- Walk each failure class separately: synchronous API errors, webhooks that never arrived, auth or credential expiry, rate-limit rejections, and silent data mismatches. Platforms routinely ship a surface for one and assume it covers the others.
- Check the failure that produces no error at all: an integration that stopped calling you entirely. Nothing in an error log shows an absence, so a volume-drop signal is a separate design item, not a side effect of error logging.
- Record retention honestly. A log an integrator cannot reach back to the moment of the incident is a log that generates a support ticket anyway.
- Note who can see it. A surface that only the account owner can open fails the partner whose engineer is not a user of that account - an access-model gap, not a logging gap.

Write the audit as a table of failure class against current visibility, and carry it into every step below. The gaps are the build order.

## 2. Expose per-integration failure detail

Three distinct surfaces exist here, and conflating them is the common design error. Stripe's developer dashboard is the reference implementation to copy the shape of, and it keeps them separate (sourced: Stripe docs):

- **Request log** - every API call with its outcome. Answers "did my call work".
- **Event log** - the business-level events those calls produced. Answers "what did it change".
- **Webhook delivery log** - every delivery attempt per endpoint with the failure reason. Answers "did you tell me about it".

An integrator debugging in the dark needs whichever one matches their failure class.

Rungs, from what you can expose cheapest to what costs most to build:

- value (support tickets deflected): `request log with per-request detail > delivery-attempt log > replay > failure counts only`
- effort: `replay > request log with per-request detail > delivery-attempt log > failure counts only`
- compliance cost: `request log with per-request detail > delivery-attempt log > replay == failure counts only` - exposing request and response bodies to a third party triggers a data-classification and redaction review, and it is close to irreversible: once integrators build tooling against a field set you cannot quietly withdraw it.
- efficiency: `delivery-attempt log > request log with per-request detail > failure counts only > replay`

**Default rung: expose the delivery-attempt log you already write**, when the platform sends webhooks. The delivery machinery records every attempt and its failure reason regardless. Exposing it is mostly an access-control and interface job, and it retires the single most support-expensive question in webhook platforms ("your webhook never arrived").

Where there are no webhooks, the request log is the default instead.

**Move up to the full request log** - per call: timestamp, endpoint, status code, error code, request ID, and as much of the payload as question 7 permits - as soon as the audit shows synchronous API failures in the ticket pile. This is the rung that covers every integrator segment rather than only the webhook consumers.

**Failure counts alone** are the floor rung: a number per integration with no detail behind it. It is cheap, and worth shipping the same week if nothing exists today. But understand what it buys: it tells a partner something is wrong and gives them no way to act, which converts a silent failure into a support ticket rather than into a fix.

**The starved option: replay.** Letting an integrator re-send a failed event or re-run a request recovers value no other rung measures - the deflection axis above does not count it. But it carries the highest effort on the menu: idempotency guarantees, a bounded window, and a clear relationship to your own retry schedule. It loses every efficiency round as a result.

Promote it when the audit shows integrators regularly losing events during their own downtime, which is exactly when a dashboard that only explains the loss is cold comfort.

Design it as independent of automatic retry. On Stripe, a failed event can be manually resent for up to 15 days after creation, and doing so does not cancel the platform's own retry schedule (sourced: Stripe docs). So a partner's manual replay never fights the platform's machinery.

This ranking is a default, not a law. Re-rank it against what you already know:

- A platform with no webhooks has no delivery log to expose, and starts at the request log.
- A team already storing full request/response bodies for its own debugging gets the request-log rung for the cost of an access-scoped view.
- A "no bodies leave our boundary" answer to question 7 deletes payload detail from the menu, leaving metadata-only logging as the ceiling rather than a compromise.

See [references/visibility-surfaces.md](references/visibility-surfaces.md) for the three-surface taxonomy expanded, the fields a log row has to carry, a good/bad log-row pair, replay semantics, and the tenant-isolation and redaction rules.

## 3. Make the correlation ID reach support

Two identifiers, kept separate in your vocabulary:

- **Request ID** - identifies one HTTP call and its response.
- **Correlation ID** - identifies a whole multi-call transaction that may span many request IDs.

Most platforms need both and ship only the first.

The convention is `X-Request-Id` carrying an opaque random value - a UUIDv4 by default, since it is collision-safe under load and leaks nothing, unlike a sequential or timestamp-derived identifier. Named platform variants exist (GitHub's `request-id`, Vercel's `X-Vercel-Id`, Cloudflare's `Cf-Ray`) and are citations, not requirements. The W3C `traceparent` header is the standards-track alternative that carries a span hierarchy and sampling flag instead of a bare string.

- value (a support ticket resolved in one lookup): `searchable in the developer-facing log > echoed in the response header > present in the error body > propagated to sub-processors`
- effort: `propagated to sub-processors > searchable in the developer-facing log > echoed in the response header == present in the error body` - that tie is genuine rather than an evasion: both write an identifier you already hold into the response you are already serialising, in the same code path, with no new storage behind either.
- efficiency: `echoed in the response header > present in the error body > searchable in the developer-facing log > propagated to sub-processors`

**Default rung: echo the ID in the response headers of every response**, success and failure alike. An integrator cannot paste an identifier into a support ticket if it was never returned to them, and this rung is usually a middleware change measured in hours. Success responses matter too - plenty of tickets are about a call that returned 200 and did the wrong thing.

**Promote to searchable-in-the-log the moment step 2 ships.** These two rungs are the pair that actually closes the loop: the header hands the integrator a string, the log lets them resolve it themselves before they ever write to you. Shipping the header alone produces a distinctive failure - integrators dutifully quoting an ID nobody outside your platform can look up.

The error body rung exists but belongs to a sibling: `samber/developer-platform-skills@api-error-design` owns the shape of the error payload, including whether the ID rides in it. Coordinate rather than redesign it here.

**The starved option: propagation to sub-processors.** Forwarding the same identifier onward when your platform calls a payment processor, carrier or other downstream provider, and keeping it on retries, is high effort and invisible until it matters. Promote it when your support answer today is "that failure came from our provider, we cannot see it" - at that point one lookup spanning the whole chain is the difference between a resolved ticket and a handoff.

This ranking is a default, not a law. Re-rank it against your stack:

- A platform already emitting W3C trace context internally gets propagation nearly free, which flips the effort line.
- A platform whose failures are overwhelmingly its own code gains little from propagation regardless of cost.

See [references/correlation-id-conventions.md](references/correlation-id-conventions.md) for header conventions, request-versus-correlation-ID modelling, propagation rules, the support-lookup workflow, and a negative example.

## 4. Aggregate error rates per integration identity

A platform-wide error rate can look healthy while one specific integration is failing 100% of its calls. Per-identity aggregation is what makes that visible, and the architecture is consistent across API-monitoring practitioner sources (sourced: Zuplo, Last9, dotcom-monitor, Odown):

1. **Tag at ingestion, not after the fact** - API key, app or client ID, attached to the request as it arrives. Retrofitting the tag later means your history is unqueryable for exactly the period you want to investigate.
2. **Split by status-code family rather than one blended rate** - 4xx (the integrator's payloads or auth), 5xx (yours), and 429 isolated on its own because rate-limit rejection is neither party's bug and has a different remediation. Blending them produces a number nobody can act on: you cannot tell a partner "your error rate is 8%" without saying whose fault the 8% is.
3. **Compute a rolling rate per identity**, and compare each integration against its own recent baseline rather than a global threshold - integrations differ so widely in traffic shape that one platform-wide percentage is either noisy for the small ones or blind to the large ones. Moesif's API monitoring documents both halves of this: status-code distribution recorded per endpoint and per customer in real time, and a "Dynamic Alert" that builds a historical baseline from a few days of data before alerting on deviation from it (sourced: Moesif docs).
4. **Correlate against your own deploy timeline** before concluding anything. A spike that lines up with your last release is your regression, and telling a partner otherwise is a trust cost you pay once. This is a named, shipped practice rather than a hypothetical - Datadog's Deployment Tracking overlays deploy and version markers on error-rate graphs specifically to answer whether a new release introduced the errors (sourced: Datadog docs).
5. **Read distribution, not just volume** - errors clustered around one time or one action pattern point to a logic bug or a bulk operation. Errors spread evenly point at infrastructure instead. This changes both who you notify and what you say.

429 specifically hands off to `samber/developer-platform-skills@api-rate-limit-policy`: the surfacing is yours, the quota design and headers are that skill's.

See [references/alerting-and-notification.md](references/alerting-and-notification.md) for the aggregation schema, the status-code bucket definitions, and burn-rate detection windows.

## 5. Decide the notification posture

Aggregation without notification only helps the integrators who think to go look - which excludes the entire fleet segment from the audience split. But push notification is where this design most easily destroys itself: an alert stream that fires on every failure gets muted, and a muted channel delivers nothing at all.

- value (partner learns before their own customers do): `threshold alert with cooldown > digest > immediate alert on state changes > pull-only dashboard`
- effort: `threshold alert with cooldown > digest > immediate alert on state changes > pull-only dashboard`
- efficiency: `digest > threshold alert with cooldown > immediate alert on state changes > pull-only dashboard`

**Default rung: a periodic digest per integration** - a scheduled summary of failures by class, with links into the log from step 2. It needs an aggregation window and a scheduler, nothing more, and it is the rung that respects the partner's attention by default rather than by tuning.

**The starved rung is threshold alerting with a cooldown** - top of the value line, top of the effort line, and beaten on efficiency by the digest every round. Promote it when question 6 says the partner loses money within hours. The concrete mechanic to copy comes from Salesforce's Agentforce health monitoring (sourced: Salesforce): notify immediately on an error-rate spike or latency creep, then hold a cooldown - 30 minutes by default there - before the same integration can alert again.

The cooldown is what makes immediacy survivable. Without it, the same incident alerts continuously until someone mutes the channel permanently.

**Immediate alerts on integration state changes** - credentials revoked, integration disabled, subscription expired - are a separate, narrow rung that coexists with the others. These are single discrete events, not a stream, and they are the class where an hour of digest delay is genuinely too slow.

Per-failure immediate alerting on error _volume_ is not on this menu. It is the alert-fatigue failure mode itself rather than a rung, and parking it at the bottom of a list is how it quietly reappears as scope later.

Ship the logging first, but do not mistake that for finishing. This is a documented real-world gap rather than a hypothetical one: Shopify's partner dashboard surfaces function error counts and billable-event errors while threshold-based email alerting on those errors remains a developer request rather than a shipped capability (sourced: Shopify dev docs and developer community). Logging existing without push alerting is the normal resting state of platforms that considered the job done at step 2.

This ranking is a default, not a law. Re-rank it against the user:

- A platform that already runs an outbound notification channel to partners gets every push rung cheaper, which compresses the effort line.
- A partner base of single-account integrators who watch their own systems closely can legitimately stop at the digest.
- Question 8's effort ceiling decides how much threshold tuning you can commit to, because an alert you cannot afford to tune becomes an alert nobody reads.

Notification templates and the anti-fatigue rules are in [references/alerting-and-notification.md](references/alerting-and-notification.md).

## 6. Build the provider-side fleet view

The same aggregation from step 4, read from your own side, answers a different question: which of our integrations are failing right now, and which partner should we contact? This is the surface your partner and support teams use, and it is what makes proactive outreach possible instead of reactive.

- Rank integrations by blast radius, not by raw error count - a partner app failing across 200 installs matters more than a single account throwing more errors, and a flat leaderboard by volume inverts that.
- Separate "broken since our last deploy" from "broken since their last release". You own the first outright. The second is the outreach case.
- Include the silent-failure signal from step 1: an integration whose call volume dropped to zero shows up nowhere in an error ranking.
- A weighted per-partner health score is a real shipped pattern rather than an invention. Third-party tooling built specifically for ISVs on Salesforce computes exactly this per managed package (sourced: ISVapp product documentation). Treat the specific weights as yours to set and to defend, not as something to borrow.

On borrowing SLO framing here, be careful. The published error-budget and SLO literature is written consumer-side, for a team measuring its own dependence on somebody else's API, and it does not transfer wholesale to a provider publishing reliability numbers _for_ partners. The mirror-image framing - the platform being the trustworthy real-time source about integration health, so the partner does not have to build independent monitoring of you - is this skill's own construction, not a sourced practice.

Use it as a design intent. Do not present it to partners as an industry standard, and do not publish a per-partner reliability number until you can defend how it is computed.

See [references/fleet-view-and-health-scoring.md](references/fleet-view-and-health-scoring.md) for the fleet-view layout, health-score construction, and the SLO adaptation gap in full.

## Failure modes

Each of these is a direct audit finding:

- Logging shipped, alerting called out of scope, and the platform still learns about partner outages from end users.
- Alert fatigue: an alert per failure, no cooldown, and a partner base that has muted the channel - after which the platform is functionally back to pull-only while believing it notifies.
- A request ID echoed in headers that no external surface can resolve, so integrators quote a string nobody but your engineers can look up.
- A correlation ID dropped on downstream or retried calls, breaking the chain at exactly the hop the partner cannot see.
- One blended error rate per integration, with 4xx, 5xx and 429 mixed together, so no notification can say whose problem it is.
- A healthy global error rate hiding one integration failing every call.
- Consumer-side SRE error-budget framing lifted wholesale into a partner-facing reliability promise the platform never designed to meet.
- A dashboard scoped to the account owner, invisible to the partner engineer who actually maintains the integration.
- Log retention shorter than the time it takes a partner to notice, so the evidence expires before the investigation starts.
- Payloads exposed without a redaction pass, leaking PII, secrets, or another tenant's data into a third party's console.
- Replay that fights the platform's own retry schedule, producing duplicate side effects the partner then has to reconcile.
- An integration that stopped calling entirely and shows up in nothing, because absence produces no errors.

## Measurement

- **Failure-class coverage** - the share of failure classes from the step 1 audit that an integrator can now diagnose unaided. This is the gate: iterate until every class in your ticket pile has a surface, or a written reason it does not.
- **Request-ID resolvability** - every error response carries an identifier that resolves in a surface the integrator can reach. Binary, and cheap to test by taking one ID from a real response and looking it up as an outside user would.
- **Self-serve deflection** - re-run the step 1 classification on a fresh batch of tickets after shipping and compare. The direction is the signal. The level is not, so baseline from your own before-and-after rather than any published figure (self-set: no industry benchmark exists for this).
- **Time from failure to partner awareness** - measured from first failure to the partner acting, not to the alert being sent. Track it per notification rung, since it is the number that justifies promoting a rung.
- **Alert action rate** - the share of alerts a partner acts on. A falling rate is the alert-fatigue failure mode arriving. Treat a sustained decline as a signal to widen thresholds or lengthen the cooldown (self-set: threshold is yours to pick from your own baseline).

The first two are gates. The last three are trends to watch, never pass thresholds - none of them has a defensible industry number behind it.

## Invocation examples

- "Our partners find out their integration is broken when their customers complain - design what we should be showing them."
- "Build the developer-facing request log for our API; we already store every request internally."
- "We alert partners on every failed webhook and they've all muted us. Fix the notification design."
- "Audit what an external integrator can actually see about their own failures on our platform today."
- "Design a fleet view so our partner team knows which ISV apps are breaking across installs."

## References

- [references/visibility-surfaces.md](references/visibility-surfaces.md) - the request/event/delivery three-surface taxonomy, required log-row fields, a good/bad log-row pair, replay semantics, retention and access scoping, redaction rules.
- [references/correlation-id-conventions.md](references/correlation-id-conventions.md) - request versus correlation ID, header conventions and platform variants, echo and propagation rules, the support-lookup workflow, a negative example.
- [references/alerting-and-notification.md](references/alerting-and-notification.md) - per-identity aggregation schema, status-code buckets, threshold and cooldown mechanics, multi-window burn-rate detection, notification templates, anti-fatigue rules.
- [references/fleet-view-and-health-scoring.md](references/fleet-view-and-health-scoring.md) - provider-side fleet-view layout, blast-radius ranking, per-partner health-score construction, the consumer-side SLO adaptation gap.

See also, same collection:

- `samber/developer-platform-skills@webhook-platform-design` - the delivery semantics, retry schedule and dead-lettering underneath the delivery log. This skill is the visibility layer over that machinery.
- `samber/developer-platform-skills@developer-portal-design` - where these logs and dashboards live in the portal's information architecture and access model.
- `samber/developer-platform-skills@partner-app-onboarding` - the partner lifecycle that decides who is watching these surfaces in the first place.
