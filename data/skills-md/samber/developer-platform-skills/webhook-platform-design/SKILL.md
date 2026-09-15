---
name: webhook-platform-design
description: Design a provider-side outbound webhook platform - event taxonomy and catalog, payload envelope and schema versioning, an HMAC signing scheme (Standard Webhooks), at-least-once delivery with retry/backoff and dead-letter policy, subscription lifecycle states, and the developer-facing debugging surface (delivery logs, replay, test-event triggering). Use whenever the user mentions webhooks, event callbacks, push events to customer endpoints, webhook signatures, delivery retries, or a webhook consumer portal - even if they never say "webhook platform". Provider side only. Do NOT use for consumer-side retry mechanics - use samber/developer-platform-skills@api-idempotency-retry instead.
license: MIT
metadata:
  author: Samuel Berthe
  version: "1.0.0"
---

# Webhook Platform Design

You are an outbound-webhook platform designer. Design how a platform notifies its customers' servers of events - what the events are, how they are signed, how delivery is guaranteed and retried, how subscriptions live and die, and how an integrator debugs a delivery that never arrived.

Svix frames the real scope: "Sending an HTTP POST is easy. Doing it reliably at scale is not." The gap between those two sentences - slow-consumer isolation, retries with backoff, dead-lettering, signing, replay protection - is what this skill designs.

A whole-surface consistency review across every surface, including this one, belongs to `samber/developer-platform-skills@public-api-design-review`; this skill owns the webhook surface's own design. Whether webhooks are the right surface to build at all, against the other integration-surface shapes, is `samber/developer-platform-skills@api-integration-surface-strategy`'s call.

## Clarifying questions

Ask these before designing anything; batch them - this is a tactical design task, not a strategy interview.

1. Greenfield or retrofit? If retrofit, request the current event list, retry behavior, signing scheme, and whatever delivery logging exists.
2. Scale, order of magnitude: how many subscriber endpoints (tens, thousands, more), and peak events per second? (drives fan-out isolation and whether FIFO is even discussable)
3. Which consumer types will integrate: enterprise integrators, typical API developers, no-code workflow tools, or a mix? (see next section)
4. Effort ceiling and data constraints: how much engineering capacity - headcount, standing on-call, operating budget - can you commit to delivery infrastructure, and may customer event data transit a third-party processor at all? (see Build vs buy)
5. Deadline and payoff shape: by what date must webhooks ship, and is this a quick feature launch or the platform's compounding integration surface for years?
6. Is any of the stated need actually interactive, client-facing streaming (live dashboards, chat)? That's GraphQL-subscription/WebSocket territory - complementary to webhooks, not competing. Webhooks own durable server-to-server delivery where the consumer may be offline when the event fires; subscriptions own sub-second client push where occasional loss is tolerable. A platform can legitimately ship both.

Questions 4-5 exist because the build-vs-buy and retry menus diverge sharply on time-to-effect, durability, and effort - neither ranking can be picked without them. A hard ship date promotes managed infrastructure and the shorter retry span; a compounding-surface mandate promotes the pipeline you operate and tune yourself.

If your harness has persistent memory, store the delivery contract's core decisions (guarantee, ordering position, retry schedule, ack timeout, dedup ID location, signing scheme) so a later run - a new event type, a retry-policy change, the docs pass - starts from the contract instead of re-deriving it.

## Consumer sophistication

Webhook consumers are servers, whoever bought the product. The design splits by consumer sophistication, and unlike most audience splits the segments don't nest - each adds its own requirements:

- **Enterprise integrators** - demand the delivery contract in writing: guarantee semantics, retry schedule, signing spec, ack timeout. They will ask for FIFO and for asymmetric signing (verifying with a public key instead of holding your shared secret).
- **Typical API developers** - self-serve through docs and the portal. They need verification snippets that handle the raw-body pitfall, a stable per-event ID for dedup, and replay from the dashboard when their handler was broken for an hour.
- **No-code consumers (workflow-automation tools)** - think in catch URLs: "show me one real payload before I build against it." They never read the signing spec; they need test-event sending and visible recent deliveries far more than prose.

Serve every segment present. A design good enough for enterprise integrators still fails no-code consumers if it ships without test events and a delivery log.

## Build vs buy

Decide this before step 1 - it determines whether steps 4-6 are built or merely configured. Three options, ranked:

- effort: `in-house build > self-hosted open-source webhook gateway > managed sending infrastructure`
- value (working delivery pipeline on day one): `managed > self-hosted gateway > in-house`
- control (data residency, custom semantics): `in-house == self-hosted gateway > managed` - both keep event data on your infrastructure; in-house adds custom semantics at much higher cost
- compliance cost: `managed > self-hosted gateway == in-house` - managed triggers DPA and data-residency review, and reversing it later means re-papering contracts and migrating live endpoints; the other two keep event data on your own infrastructure equally
- efficiency: `managed > self-hosted gateway > in-house`
- **Default rung: managed sending infrastructure**, when webhooks are a feature of your product rather than the product itself - the Svix/Hookdeck/Convoy class of vendor (names are citations, not requirements; evaluate whatever equivalent your ecosystem offers). Svix's own build-vs-buy estimate for replicating the feature set in-house is engineer-years, not engineer-weeks - 3-5 engineers for 6-12 months plus a standing on-call. Treat the exact figure as vendor self-interest, but the order of magnitude matches what the feature list in this skill implies.
- **Move up to a self-hosted gateway** when compliance rules out third-party transit but you can operate the software. In that case the managed rung is **deleted, not demoted**: question 4 answering "customer event data may never transit a third-party processor" removes it from the menu instead of ranking it last, because a rung parked at the bottom on a compliance ground reappears as scope the next time a deadline bites - and re-appears without the legal review that ruled it out. Re-promotion trigger: a signed DPA and a residency posture that covers the vendor.
- **In-house is the starved option**: highest control, highest effort, loses every efficiency round. Promoted when webhook delivery is itself the product you sell, or when both third-party transit and third-party code are ruled out. Whatever you pick, every design decision in steps 1-7 still has to be made - buying infrastructure buys the machinery, not the taxonomy, contract, or docs.
- This ranking is a default, not a law. Re-rank against the interview: a hard ship date promotes managed; an in-house team already operating durable queues at scale gets the build far cheaper than the estimate, which flips the effort line.

## Workflow

1. Define the event taxonomy and catalog.
2. Design the payload envelope and schema-versioning story.
3. Adopt the signing scheme.
4. Set the delivery contract: guarantees, retry policy, dead-lettering.
5. Model the subscription lifecycle.
6. Build the debugging surface: logs, replay, test events.
7. Document everything against the five-element rubric.

Each step has a section below, in order.

## 1. Event taxonomy and catalog

- Name events with the Object-Action pattern: `resource.action`, action in past tense (`invoice.paid`, never `invoice.pay`), dot-delimited, identifiers restricted to `[a-zA-Z0-9_.]`. This is the Standard Webhooks recommendation and the Stripe convention. Production platforms diverge on delimiter and on where the discriminator lives, so pick one convention at launch and never mix. Splitting the event name across a header and a body field, GitHub-style, means no single string names the event - avoid it.
- The catalog is the contract: every event type gets a stable name, a description, and a payload schema before it ships. Subscribers select what to receive by catalog name, so an undocumented event type is effectively unsubscribable.
- Check each event against five design principles: self-contained, immutable (add fields, never repurpose), traceable, actionable, debuggable.
- Decide explicitly whether subresource events bubble to parent events (Stripe's answer: never - `customer.subscription.updated` fires no `customer.updated`). Whichever way, state it; silence here breeds subscriber assumptions.

See [references/event-taxonomy-and-payload-design.md](references/event-taxonomy-and-payload-design.md) for vendor naming comparisons and the design-principle checklist applied.

## 2. Payload envelope and schema versioning

- Choose envelope placement deliberately: all metadata in the JSON body (Stripe), or metadata in HTTP headers with only resource data in the body (GitHub, Shopify, Standard Webhooks). Header-split designs force your delivery log to capture headers and body to replay an event faithfully - build the log for that from day one, not as a retrofit.
- Choose thin vs full payloads as a first-class axis: full payloads embed resource state; thin payloads carry identifiers and force an API fetch. Standard Webhooks recommends keeping payloads small, usually under ~20kb. Thin payloads also sidestep versioning: the notification never changes shape when the API version bumps.
- Pick one of the two schema-versioning camps deliberately: pin each webhook endpoint to an API version and render payloads per that version (Stripe's model), or version event types themselves - a new type name per breaking change, additive-only evolution otherwise (the Svix/Standard Webhooks model). Drifting into both by accident is the failure; an API version bump must never silently reshape event payloads a subscriber already stores.
- Know the standards layering - these are layers, not competitors: Standard Webhooks covers signing and delivery headers, CloudEvents covers the envelope, AsyncAPI and OpenAPI 3.1's `webhooks` section cover description. Document outbound events in the same OpenAPI document as the inbound API; only adopt CloudEvents if you must interoperate with an event mesh that already speaks it.

See [references/event-taxonomy-and-payload-design.md](references/event-taxonomy-and-payload-design.md) for the envelope fork in detail, the Stripe thin/snapshot dual-run migration pattern, and the standards map.

## 3. Signing scheme

You own the signing scheme - what is signed, how, and how consumers verify. Signing-key issuance, storage, and rotation infrastructure belong to sibling `samber/developer-platform-skills@api-auth-key-management`.

- Adopt the Standard Webhooks spec instead of inventing a bespoke scheme - it's the closest thing this fragmented domain has to a standard, with real (self-reported) adoption across major API platforms. Three headers on every delivery: `webhook-id`, `webhook-timestamp`, `webhook-signature`.
- Signature construction: HMAC-SHA256 over `{id}.{timestamp}.{raw_body}`, base64-encoded, algorithm-version-prefixed (`v1,...`). Signing the timestamp is what buys replay protection - the receiver rejects deliveries whose timestamp falls outside a tolerance window (the spec recommends 5 minutes). A body-only signature (GitHub's and Shopify's shape) validates forever, so a captured request replays indefinitely.
- Prefix secrets so leaked keys are identifiable by scanners: `whsec_` for symmetric HMAC secrets, `whsk_`/`whpk_` for asymmetric ed25519 private/public keys (signature id `v1a`). Offer asymmetric signing for consumers who shouldn't hold a shared secret - the recommended choice when you don't control both ends.
- Design zero-downtime rotation in: the `webhook-signature` header carries multiple space-delimited signatures, so old and new secrets validate simultaneously during a rotation window. A platform with a single active secret forces subscribers into revoke-then-deploy, with a window of failed deliveries.
- Your signing docs must cover the three consumer-side pitfalls that dominate integration failures:
  - Verify every request without exception, even notification-only handlers.
  - Verify against the raw body before any JSON parser touches it.
  - Exempt the webhook route from session-auth middleware, since it authenticates by signature, not session.

See [references/signing-scheme-reference.md](references/signing-scheme-reference.md) for the worked construction, the four major non-adopters' schemes contrasted, and the rotation flow.

## 4. Delivery contract: guarantees, retry, dead-letter

- Promise at-least-once delivery, explicitly, as a deliberate choice: you retry until acked, so a subscriber that processes then crashes before responding 200 sees the event twice. Never claim exactly-once - every "exactly-once" claim in this market is at-least-once plus dedup tooling. Ship the honest version of that: a stable per-event ID (same value across retries of the same event) from day one, plus a documented dedup recommendation. Retrofitting the ID later can't help subscribers who already built without it.
- State the ordering position explicitly: best-effort, non-guaranteed ordering is the correct default - retries and parallel workers reorder events, and strict ordering means one failing delivery blocks the whole per-endpoint queue. Every major platform ships non-FIFO by default; offer FIFO only as an explicit opt-in for consumers who structurally cannot tolerate reordering. Warn subscribers not to infer order from timestamps.
- Decouple delivery from the request path via a durable queue, with per-endpoint isolation - one slow or broken subscriber must never delay delivery to the others. This fan-out isolation is the core value the platform sells to its own engineering team.
- Choose the retry policy - this is where real platforms diverge most:
  - effort: `configurable per-endpoint schedules + circuit breaker > fixed day-scale schedule + DLQ + auto-disable > fixed hours-scale schedule > manual redeliver only`
  - value (deliveries recovered without human action): `configurable + circuit breaker > fixed day-scale > fixed hours-scale > manual redeliver only`
  - efficiency: `fixed day-scale schedule > fixed hours-scale schedule > configurable + circuit breaker > manual redeliver only`
  - **Default rung: a fixed exponential-backoff schedule spanning roughly a day** - the shape Svix ships (8 attempts over ~27.5 hours) and Stripe approximates (up to 3 days); Shopify's 8 tries over 4 hours marks the short end. Size the total span against real subscriber incident durations - a deploy takes minutes, an outage can take hours - not a round number. Exponential, never linear: constant-interval retries hammer a struggling endpoint.
  - **Promote to configurable schedules plus a circuit breaker** (half-open probing before resuming, Convoy-style) when endpoint count grows large enough that sustained-failing endpoints materially load the pipeline, or when enterprise consumers negotiate delivery SLAs. High value, high effort - the starved option that those two conditions promote.
  - **Manual redeliver only (GitHub's model: zero automatic retries) is a named anti-pattern**, not a minimalist rung - it works for GitHub only because a deliveries-list-plus-redeliver API and explicit "build your own reconciliation" docs ship with it. Copying the zero without the API is just shipping unreliable delivery.
  - This ranking is a default, not a law - re-rank on the interview: a mostly no-code consumer base devalues configurability nobody will touch; a payments-grade domain promotes the longer span and the circuit breaker.
- Classify subscriber responses instead of treating them alike:
  - 2xx acks and stops retries. Expect the ack within ~10 seconds, the Shopify/GitHub convention.
  - Treat "handler is slow" as distinct from "handler errored" - a subscriber that queues the work and returns fast is doing exactly what you should tell it to.
  - Honor a `Retry-After` header on 429 over your own backoff curve - most senders don't, and it's a differentiator.
  - Send non-retriable 4xx (anything but 408/429) straight to the dead-letter queue - retrying a permanent failure wastes the budget and looks like an attack.
- Dead-letter on exactly two triggers:
  - Retry budget exhausted.
  - A non-retriable error class.
    Retain dead-lettered events 7-30 days with full context (headers included) for investigation and replay. After sustained failure, auto-disable the endpoint and notify the subscriber out-of-band - email or dashboard, since the webhook channel itself is what's broken.
- Recommend consumers of high-stakes event types run periodic reconciliation against your API - vendor-endorsed practice, not a workaround. Your docs setting that expectation is more honest than implying delivery is stronger than at-least-once/best-effort actually promises.

See [references/retry-policy-vendor-comparison.md](references/retry-policy-vendor-comparison.md) for the six documented vendor schedules, timeout values, auto-disable behaviors, and the circuit-breaker reference design.

## 5. Subscription lifecycle

- Model the subscription (endpoint registration) as a first-class stateful object with full CRUD - never fire-and-forget registration. Give it three explicit states:
  - active
  - paused - subscriber-initiated stop without losing configuration
  - disabled - platform-initiated after sustained failure

  The three infrastructure-focused vendors converge on this richer model; binary enabled/disabled is the thinner shape platforms launch with and outgrow. Expose only states a customer-created subscription can legally reach - reject internal-only states at the API boundary.

- Keep filtering's two axes independent: event type (against the catalog) and recipient/channel scoping. An endpoint with no filter receives everything - say so.
- Specify both replay positions: where a newly created subscription starts (new events only vs retained backlog), and where a subscription resumes after a platform-side incident. They can legitimately differ. Document loudly that deleting a subscription destroys its replay/delivery state - recreating it under the same name starts fresh, and a subscriber deleting-to-reset will silently lose or double-replay a backlog.
- Document config-change propagation lag as expected behavior (a subscription edit taking a minute or two to reach the delivery path is normal), so integrators don't file it as a bug.

See [references/subscription-lifecycle-comparison.md](references/subscription-lifecycle-comparison.md) for the six-vendor state/filtering/replay comparison and the state-machine case study.

## 6. Debugging surface

A self-service consumer portal is table stakes in this market, not a nice-to-have - flag "no portal" the way you'd flag a missing signature-verification doc. The portal carries:

- **Delivery logs**: filterable by endpoint, event type, and status, with per-attempt inspection (request headers, body, response code, timing). If your envelope splits metadata into headers (step 2), the log must store them or replay is unfaithful.
- **Replay and retry, as distinct operations** - adopt Hookdeck's terminology verbatim, because the market uses the words interchangeably and your docs shouldn't: a _retry_ is a new delivery attempt of the same event; a _replay_ re-ingests the original as a new event. Offer single-event and range replay; gate a large replay window behind a cost confirmation, since replaying a big backlog is an expensive operation the subscriber may not intend.
- **Test-event triggering**: a "send example event" action driven by each event type's schema, so an integrator sees one realistic payload before writing a line of handler code - the same job a no-code tool's catch-URL solves from the consumer side. Test triggering in a sandbox environment (fake data, test-mode keys) is sibling `samber/developer-platform-skills@api-test-mode-design`'s ground; this skill owns the delivery-side button and the example payloads it sends.
- **Failure visibility**: surface exhausted deliveries as incidents to investigate - grouped by endpoint and status code, with notification - rather than rows in a queue. Document the 200-then-crash blackhole: a handler that acks then throws has told you delivery succeeded, and no debugging surface can see inside it.

See [references/subscription-lifecycle-comparison.md](references/subscription-lifecycle-comparison.md) for what each vendor's portal and testing tooling actually ships, as the benchmark to match.

## 7. Documentation

Grade your webhook docs against the five-element rubric the market's best docs are graded on, all five before launch:

1. Signature verification with runnable snippets.
2. The event catalog with schemas and example payloads.
3. The retry policy - exact schedule, not "we retry with backoff".
4. Troubleshooting and failure recovery.
5. Testing tools.

State the delivery contract as explicit, findable sentences:

- The guarantee (at-least-once).
- The ordering position.
- The retry schedule.
- The ack timeout.
- Which header or field carries the dedup ID.

Every one of these left implicit becomes a subscriber assumption, then a support ticket. Publish the event catalog from the same spec that drives delivery (OpenAPI 3.1 `webhooks` section) so docs and payloads can't drift apart silently.

## Failure modes

Anti-pattern checklist - each is a direct audit finding:

- Zero automatic retries without a deliveries-list-plus-redeliver API and reconciliation docs shipping alongside.
- "Exactly-once delivery" claimed anywhere in the docs.
- Ordering guaranteed implicitly (or subscribers left to assume it) instead of an explicit best-effort statement.
- Linear retry intervals, or retrying non-retriable 4xx responses until the budget exhausts.
- A signature over the body only - no timestamp, so no replay protection.
- One active signing secret, forcing revoke-then-deploy rotation.
- No stable per-event ID across retries of the same event.
- A delivery log that stores only the body while the envelope carries metadata in headers.
- An API version bump silently reshaping event payloads existing subscribers already store.
- Delete-and-recreate of a subscription silently resetting its replay position.
- Slow-but-correct handlers (queue fast, ack fast) treated as failures because the timeout and the queue-fast advice were never documented.
- No consumer portal: no logs, no replay, no test events.

## Measurement

Two binary gates - iterate the design until both pass:

- **Contract completeness**: the guarantee, ordering position, retry schedule, ack timeout, and dedup ID location are each explicitly documented. Five facts, all present - a missing one fails the gate, because each absence is a subscriber assumption waiting to become an incident.
- **Documentation rubric**: all five rubric elements exist before launch. Any missing element fails the gate.

Operational metrics to stand up, watched as trends rather than pass thresholds:

- Per-endpoint delivery success rate - the platform's headline health number.
- Dead-letter rate - a spike means an endpoint in sustained failure, distinct from background transient retries.
- Time-to-detect a failing endpoint - bounded by your auto-disable/notification window. Set the baseline from your first month and improve against it rather than against an external threshold.

## Invocation examples

- "We're adding webhooks to our billing API - design the event catalog, signing, and retry policy from scratch."
- "Our webhook system retries three times in a row then drops the event, and customers keep missing deliveries - redesign the retry and dead-letter policy."
- "Enterprise customers are asking how our webhooks are signed and whether we guarantee ordering - write the delivery contract we should be able to show them."

## References

- [references/event-taxonomy-and-payload-design.md](references/event-taxonomy-and-payload-design.md) - naming conventions across vendors, envelope placement fork, thin vs full payloads, schema-versioning camps, standards map.
- [references/signing-scheme-reference.md](references/signing-scheme-reference.md) - Standard Webhooks construction worked example, non-adopter scheme contrast, rotation flow, consumer-pitfall checklist for your docs.
- [references/retry-policy-vendor-comparison.md](references/retry-policy-vendor-comparison.md) - six vendors' documented retry schedules, timeouts, auto-disable behavior, dead-letter and circuit-breaker patterns.
- [references/subscription-lifecycle-comparison.md](references/subscription-lifecycle-comparison.md) - endpoint states, filtering, replay/backfill, and portal/testing tooling across six vendors, plus a subscription state-machine case study.

- `samber/developer-platform-skills@api-idempotency-retry` - general retry and idempotency mechanics (backoff algorithms, idempotency keys) on the API's request side; this skill applies those ideas to outbound delivery only.
- `samber/developer-platform-skills@integration-error-observability` - how integration errors surface to the developer beyond the webhook delivery log.
- `samber/developer-platform-skills@api-status-communication` - incident and status-page communication when delivery failures are the platform's fault.
- `samber/developer-platform-skills@api-versioning-policy` - the versioning machinery behind step 2's event-schema evolution choice.
- `samber/developer-platform-skills@api-error-design` - the error surface of the subscription-management API itself.
- `samber/developer-platform-skills@public-graphql-api-design` - GraphQL subscriptions, the complementary push mechanism named in question 6: first-party live UI over sub-second push, versus this skill's durable server-to-server delivery.
