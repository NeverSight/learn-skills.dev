---
name: waiting-list
description: >-
  Design and build waiting-list portals for anticipated goods or services:
  classify whether the experience needs interest capture, verified early access,
  referral growth, a virtual waiting room, appointment backfill, or scarce-item
  allocation; choose a reversible architecture; and define the state machine,
  abuse controls, consent and email lifecycle, fairness, observability, and
  release gates. Optionally validate supplied email and phone contacts with
  expiring magic links or provider-managed verification, then feed eligible,
  consented records to a runtime-configured CRM adapter. Use for prelaunch
  signups, beta access, launches, bookings, reservations, traffic-spike queues,
  and premium or cinematic campaign experiences. Do not use for generic
  landing-page copy, ordinary CRM or email operations, or checkout and
  inventory systems in isolation; route those parts to the appropriate
  specialist skill.
license: MIT
metadata:
  source-index: references/source-index.md
---

# Waiting-list portals

Use this skill to turn “we need a waitlist” into a truthful product promise,
an appropriate system boundary, and a buildable delivery plan. A list of
interested people, a fair order of service, a traffic gate, and a reservation
are different things. Never let a polished landing page silently choose the
semantics.

## When to load

Load this skill when the user is designing, reviewing, implementing, or
comparing a portal for early access, product launch demand, scarce goods,
appointments, memberships, events, beta programs, or high-traffic admission.

## When not to use

- For copy, visual design, SEO, or accessibility in isolation, use the relevant
  frontend or content skill and bring this skill in only for the list behavior.
- For a general API, database, email, security, or payment implementation, use
  the owning specialist skill; this skill supplies the waitlist-specific
  contract and failure modes.
- For a live waiting-room vendor or queue datastore, read its current official
  documentation. This skill is a design method, not a substitute for vendor
  runbooks or legal advice.
- For a standalone CRM migration or email/SMS campaign, use the owning
  integration skill. Load this skill when the CRM is a downstream of the
  waitlist's verified-contact lifecycle.

## Core workflow

### Default posture and marketer experience

For a new marketing waitlist, use one static HTML page, Alpine.js (CSP build),
Vite packaging, custom CSS, TypeScript API functions on Vercel's Node.js runtime,
and managed Neon Postgres. Use Twilio Verify codes for email (with SendGrid)
and optional SMS verification; keep the CRM selectable through server-side
runtime configuration. Avoid Python backends and Rails. Go or Rust are explicit
alternatives for a campaign whose existing hosting or requirements warrant them.
These are defaults, not reasons to replace an existing working integration.

Read [references/default-stack.md](references/default-stack.md) before building
or deploying. It defines the provider posture, Vercel limitations,
repository shape, worker execution, and escape hatches. Read
[references/brand-and-marketer-workflow.md](references/brand-and-marketer-workflow.md)
for all new portals: gather the campaign brief, brand guide, logos, reference
images, and optional video; show a branded preview before connecting production.
Use [templates/campaign-brief.md](templates/campaign-brief.md) as the plain-language
intake. The agent fills technical records; do not ask a marketer to select an
ORM, framework, retry algorithm, or database schema.
For a premium, cinematic, motion-rich, or reference-led campaign, also read
[references/engagement-and-visual-system.md](references/engagement-and-visual-system.md)
and record its relevant experience brief, fallback, performance, and visual-test
decisions. Treat a reference site as a source of observable interaction
principles, not as permission to copy its brand, assets, source, layout,
scarcity language, or product claims.
Use approved supplied assets or original image-generated artwork for campaign
heroes, product scenes, and editorial illustration. Preview generated artwork
for approval before publication. Do not substitute CSS shapes or gradients,
inline SVG drawings, canvas sketches, emoji, ASCII, or icon collages for
campaign artwork unless the user explicitly requests that aesthetic.
Programmatic graphics remain appropriate when geometry is the information,
such as charts, diagrams, controls, and status indicators.
Use [templates/campaign-config.example.json](templates/campaign-config.example.json)
as a server-side configuration example; its unset production choices must be
resolved before enabling live sends.

Default campaign: email interest capture with required email confirmation,
phone collection off, referrals off, no displayed rank, no implied reservation,
and CRM awaiting connection. If SMS is enabled without a specified interaction,
prefer managed OTP. An explicit SMS magic-link requirement overrides that
default; preserve it and explain the provider capability boundary.

This skill can create deployments and send messages when used to implement a
portal. Confirm the target, scope, and rollback path before acting. Read-only
discovery may proceed without confirmation. Use existing authorization where
it already covers those details; prepare local artifacts and previews first.
Never describe a mock form as collecting real registrations.

### 1. Write the promise before choosing technology

Answer these questions in plain language:

1. What does joining mean: interest, a place in line, eligibility for an
   invitation, a chance in an allocation, or a request for a service slot?
2. What, if anything, is guaranteed? State explicitly that joining does not
   reserve inventory, payment priority, an appointment, or admission unless a
   separate confirmed action does so.
3. What event advances the person: verification, capacity, a scheduled release,
   a cancellation, a score, a referral, a lottery, or an operator decision?
4. Which contact proofs are optional, required, or absent? What does a verified
   email or phone actually authorize, for how long, and what happens when an
   invitation expires, a person unsubscribes, or a duplicate arrives?
5. What must be true at launch: peak arrivals, acceptable loss, fairness rule,
   regions, accessibility, languages, data residency, integrations, and
   rollback path?

Record assumptions as assumptions. Do not use “current position” when the
operator may select by segment or fit; call it an interest list or an
estimated rank instead.

### 2. Select one primary pattern

Use the smallest pattern that makes the promise true. Combine patterns only
when the boundary and transition are explicit.

| Pattern | System of record | Good default | Main trap |
| --- | --- | --- | --- |
| Interest list | Relational table, CRM, or ESP | Static/SSR page plus a server-side form endpoint and async email | It is not a queue; do not display a fabricated position |
| Verified early-access queue | Database plus event/outbox record | Unique program + normalized contact, double opt-in when appropriate, invite states | A verified email is not proof of a person or a purchase |
| Referral priority | Database event ledger | Immutable arrival key plus verified referral events and a versioned policy | Self-referrals, purchased traffic, and “viral” claims can corrupt fairness |
| Virtual waiting room | Edge/gateway plus durable queue | Signed admission token, cookie continuity, atomic admission, bounded polling | Admission to a page is not inventory authority or checkout serialization |
| Appointment backfill | Scheduling/capacity service | Match people to released slots, preferences, and expiry windows | A global FIFO queue may be unfair or operationally useless |
| Allocation, lottery, or preorder | Inventory/payment/allocation service | Separate eligibility from allocation, reservation, payment, and fulfillment | Calling an allocation “a waitlist” hides overselling and refund obligations |
| Headless/embedded API | Independent API and event boundary | Public write contract with scoped credentials, CORS, idempotency, and webhooks | A browser-held secret is not a server secret |

For a simple prelaunch page, start with the interest-list pattern. For a
launch-day traffic spike, start with a virtual waiting-room or edge product.
For a product or service whose scarce resource is the real problem, design the
inventory or scheduling boundary first and attach the list to it.

Load [references/architecture-patterns.md](references/architecture-patterns.md)
when comparing patterns, modeling scale, or deciding whether a queue, referral
loop, reservation, or vendor is warranted.

### 3. Define the state machine and data contract

When implementing, read [references/implementation-contract.md](references/implementation-contract.md)
for concrete endpoint, persistence, verification, CRM, and failure contracts.

Use opaque IDs and keep contact data out of URLs, logs, analytics labels, and
public ranking pages. A useful baseline is:

```text
submitted -> verification_pending -> active -> invited -> claimed
                                  \-> suppressed/removed
invited -> expired
```

Use a separate queue/admission state for a waiting room:

```text
identified -> queued -> admitted -> consumed
                     \-> abandoned/expired
```

If the portal validates contacts, model each channel independently rather than
using one overloaded `verified` flag:

```text
email: unrequested -> sent -> clicked/verified | expired/revoked
phone: unrequested -> sent -> clicked/verified | expired/revoked
```

“Verified” means the channel's proof was accepted under a named method and
timestamp. It does not prove legal identity, that the supplied person owns the
account, that the number is suitable for marketing, or that the contact will
remain accurate. Load
[references/contact-verification-and-crm.md](references/contact-verification-and-crm.md)
when either contact proof or CRM delivery is in scope.

For each transition define the actor, precondition, side effect, retry
behavior, audit event, and user-visible message. Store at least:

- `program_id`, opaque `entry_id`, `created_at`, and a stable tie-break key;
- normalized-contact uniqueness with a documented normalization version and
  protected original; plan key rotation if keyed lookup hashes are introduced;
- consent purpose, source/UTM attribution, verification and suppression times;
- explicit status, policy/version identifiers, invitation/claim expiry, and
  only the attributes needed for selection or service matching;
- referral code ownership and referral events, if enabled; never infer counts
  from mutable client state;
- per-channel verification method, proof ID, `verified_at`, expiry/revocation,
  and consent purpose; do not store raw tokens;
- CRM sync status, mapping/version, provider record ID, idempotency key, and
  last error; keep this as integration state, not as the waitlist's source of
  truth;
- an append-only audit/event record for state changes and outbound effects.

Make `POST` safe to retry with an idempotency key or a database uniqueness
constraint. Define duplicate behavior deliberately: normally return a generic
success for an already-known contact so the endpoint does not become an email
enumeration oracle. Do not expose a raw row count as a personal position unless
the ordering and visibility rules make that claim true.

### 4. Build the normal request path

The default path is:

```text
page -> server endpoint -> validate/normalize -> abuse gates -> durable write
     -> enqueue notification -> generic response
                                      \-> worker/provider -> delivery events
```

Validate on the server. Apply layered controls: schema and length limits,
CSRF protection for same-origin forms, strict CORS for headless clients,
per-IP and per-contact rate limits, honeypot or timing signals, and a bot
challenge for higher-risk traffic. If using Turnstile, the server must call
Siteverify; a browser token alone is not protection. Do not promise a specific
latency such as “under 200 ms” until it is measured for the chosen provider and
failure mode.

Write the entry and the notification intent transactionally or through a
durable outbox. Make workers retryable and outbound webhooks idempotent. Keep
the synchronous response short, but do not silently lose the email intent when
the provider is unavailable.

Use double opt-in when list quality, consent proof, or typo resistance matters;
make the unverified record's permissions and retention explicit. Separate
transactional verification/invitation mail from marketing updates, honor
suppression and unsubscribe state, authenticate the sending domain, and process
bounces and complaints. Load
[references/operations-and-abuse.md](references/operations-and-abuse.md) for
the detailed control checklist.

If CRM delivery is enabled, enqueue it only after the configured eligibility
gate—often active contact verification and the relevant consent. Map only
approved fields, use a server-side credential, and make the adapter retryable
and idempotent. A CRM outage must not prevent confirmation of a durable local signup or
silently lose the local record; it should leave a visible sync state and a
recoverable outbox item.

### 5. Make ranking and admission truthful

For FIFO, assign the arrival/tie-break key exactly once in a durable atomic
operation. For segmentation, scoring, referrals, or lotteries, publish the
selection rule, inputs, policy version, and whether the outcome is guaranteed,
estimated, or discretionary. Recompute derived rank from durable facts; do not
let the client submit `referrals_count`, `position`, or `priority`.

For referral overlays:

- generate unguessable, revocable codes and treat them as attribution tokens,
  not authorization;
- count only eligible downstream entries after the required verification and
  deduplication window; record both the click and the conversion;
- prevent self-referral and obvious automation, cap influence, and preserve the
  original queue key so the policy can be changed or removed;
- show a clear benefit and a range/estimate when competing events can change
  rank. Obtain legal and policy review before tying commercial rewards to
  forwarding or referrals.

For a virtual waiting room, use signed admission tokens verified locally where
possible, cookie/session continuity, atomic queue transitions, jittered polling,
and a deliberate fail-open versus fail-closed decision. Fail-open may protect
availability for a marketing preview; it is unsafe as the sole control for
scarce inventory. The downstream reservation, checkout, or allocation service
still needs its own idempotency and concurrency controls.

### 6. Design the user and operator surfaces

The public flow should state what joining means, what data is collected, how to
correct or leave, what happens next, and whether the position is fixed. Provide
an accessible form, keyboard-visible errors, a no-JavaScript or retry story
where practical, and generic duplicate/error messages that do not leak account
existence. For a queue, show last-updated time and an honest estimate rather
than false precision.

Operators need authenticated, least-privilege views for search, segments,
status transitions, exports, invite batches, suppression, audit history,
provider health, verification status, CRM sync status, and incident controls.
Every manual bulk action needs a
preview, scope, actor, timestamp, reason, and reversible path.

### 7. Verify before calling it ready

Use the template in
[templates/waitlist-decision-record.md](templates/waitlist-decision-record.md)
for a durable decision. Test at least:

- duplicate and concurrent submissions, retries, replayed verification and
  invite tokens, expired claims, and webhook duplicates/out-of-order delivery;
- bot bursts, rate-limit behavior, queue churn, abandoned sessions, provider
  outage, database outage, and fail-open/closed behavior;
- ranking invariants, referral abuse, allocation oversell, reservation expiry,
  and operator bulk-action rollback;
- accessibility, privacy/retention, suppression/unsubscribe, generic error
  messaging, and no-JavaScript or slow-network behavior;
- verification link/code replay, expiry, resend throttling, scanner/prefetch
  behavior, wrong-channel attempts, and CRM mapping, retry, deduplication,
  deletion/suppression propagation;
- a representative peak-load test and a manual review of the rendered mobile
  and desktop experience.

## Output contract

For an architecture or implementation response, return:

Lead with the marketer's preview, campaign choices, connection status, and next
action. Retain the following engineering detail in project artifacts, linking
to it rather than placing it in the main setup conversation:

1. the named promise and selected primary pattern;
2. a context diagram and state/transition table;
3. schema and endpoint/event contracts, including idempotency and privacy;
4. optional email/phone proof semantics and the runtime CRM mapping/outbox;
5. abuse, email, fairness, accessibility, and failure-mode controls;
6. an incremental build order with a reversible fallback;
7. tests, operational signals, and an explicit list of unknowns.

Do not call a template production-ready based on its README, GitHub stars, or a
successful happy-path demo. Inspect the actual code and current provider
documentation, then retain the evidence and date it.

## Completion criteria

Stop when the promise, primary pattern, state machine, data boundary, abuse and
email lifecycle, fairness/admission semantics, operator controls, and bounded
validation plan are explicit. If contact verification is in scope, the proof
semantics, token lifecycle, consent, abuse limits, and recovery path are also
explicit; if CRM is in scope, its runtime configuration, field mapping,
idempotency, retry/dead-letter handling, and suppression/deletion behavior are
explicit. If a provider, legal rule, inventory fact, or current project
capability is material and cannot be verified, report that blocker instead of
filling the gap from memory.

For a build request, a decision record alone is insufficient. Deliver runnable
HTML/JavaScript and TypeScript source, migrations, provider adapters, setup instructions,
and retained functional/visual test evidence. Apply the release gates in
[references/release-evidence.md](references/release-evidence.md). Report preview,
connected-test, and live readiness separately; untested provider configuration
does not establish a working integration.
