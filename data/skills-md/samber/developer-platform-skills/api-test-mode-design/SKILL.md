---
name: api-test-mode-design
description: Design the test/sandbox mode of a public API platform so external integrators build and validate without touching real money, messages, or data - isolation architecture (soft test-mode toggle vs hard separate-copy sandbox), test-key prefixing, magic test values, simulated objects and personas, on-demand test events, deterministic time manipulation, reset and seeding, sandbox quotas, abuse controls, and graduation to live. Use whenever the user mentions a sandbox, test mode, test API keys, magic or dummy test values, simulated webhook events, or demo data - even if they never say "test mode". Not code-execution sandboxing or unit-test mocking. Do NOT use for partner sandbox provisioning - use samber/developer-platform-skills@partner-app-onboarding instead.
license: MIT
metadata:
  author: Samuel Berthe
  version: "1.0.0"
---

# API Test Mode Design

You are a test-mode designer for an API platform. Design the sandbox environment external integrators build against - its isolation boundary, credentials, deterministic test values, simulated events and time, quotas, abuse controls, and the path to live - so an integration is fully validated before it ever touches real money, messages, or data.

A sandbox is table stakes for developer trust on any platform that expects third-party integrators. It is a _stateful_ environment that validates business logic across a sequence of calls, not a mock server's static request→response mapping. The gap shows up around week three of an integration: bugs a stateless mock cannot reproduce because it has no concept of what happened on a prior call.

## Scope

Designs sandbox/test-mode environments (test keys, deterministic fixtures, simulated events) so integrators build without real data. This is product test-mode design, distinct from the existing `developer-sandbox` marketing-playground skill on skills.sh: that skill builds a marketing try-it playground. This one designs the product's own test mode.

Boundaries with siblings:

- **Key lifecycle** (issuance, rotation, hashing, dashboard UX): `samber/developer-platform-skills@api-auth-key-management`. Test-key prefixing is the shared ground; this skill owns only the mode identity inside the prefix.
- **Webhook delivery** mechanics (signing, retries, delivery logs): `samber/developer-platform-skills@webhook-platform-design`. How a test event gets triggered is this skill's.
- **Sandbox controls in the portal**: `samber/developer-platform-skills@developer-portal-design`.

## Clarifying questions

Ask before designing anything; each answer changes a later step. Batch them - this is a tactical design task, not a strategy interview.

1. Product domain: payments-like (money moves), communications-like (messages reach real people), data-aggregation-like (third-party data flows in), or something else? (shapes the magic-value carrier and the graduation gate - see next section)
2. Isolation appetite: is a mode toggle on the live account acceptable, or does the domain demand a structurally separate environment? What is the engineering budget - weeks or quarters? (drives step 1)
3. What compliance regime gates going live - KYC, partner vetting, marketplace listing review, plan tier, or nothing? (drives step 5)
4. What test infrastructure already exists - a staging environment, seeded fixtures, a mock server integrators were told to use? (a retrofit starts from what integrators already depend on)
5. Does the product have time-dependent state (trials, renewals, expirations, scheduled jobs) and/or async events? (decides whether step 3 is a core deliverable or a stub)
6. Is there an end-user-facing surface (checkout page, hosted flow) integrators must also test, or is the API the whole product?
7. By when must integrators be able to build against the sandbox, and is this a one-off unblock (one partner waiting on a deal) or a compounding platform surface you will run for years? (with question 2's budget, these are the re-rank inputs for steps 1 and 2)

Question 7 exists because the isolation menu (step 1) and the simulation menu (step 2) diverge sharply on time-to-effect, durability, and effort. Neither ranking can be picked without it.

- A hard date promotes the soft toggle and magic values.
- A compounding mandate promotes the hard separate-copy and the fixture builder.
- A budget of weeks, rather than quarters, deletes the hard separate-copy from this pass rather than parking it last. Unblocking condition: "the first cross-mode leakage incident, or the compliance regime landing."

## Product domain split

The **product domain** is the axis that changes this design, because it dictates what the magic values look like and what regulators gate graduation on:

- **Payments-like**: magic values ride the transaction instrument (card numbers mapping to specific declines, disputes, fraud-risk levels, step-up auth); graduation is compliance-gated (KYC); the sandbox must simulate settlement it cannot actually perform.
- **Communications-like**: magic values ride addresses (phone numbers, per operation); the hard guarantee is that no real message ever leaves the sandbox - the strongest isolation in the survey refuses to even _reference_ production resources from test credentials.
- **Data-aggregation-like**: magic values ride identities (test usernames/personas selecting fixture shapes, password suffixes selecting error conditions); the design center is fixture variety, not transaction outcomes.

Design for your domain's carrier and gate. The worked catalogs in [references/magic-value-catalogs.md](references/magic-value-catalogs.md) cover all three.

## Workflow

1. Choose the isolation model - the decision every later step builds on.
2. Make every failure path triggerable - deterministic test values and simulated objects.
3. Simulate events and time - test-event triggering, time manipulation, reset and seeding.
4. Harden credentials, quotas, and abuse controls.
5. Design the graduation path - compliance gate, cutover checklist, canary.

Each step has a section below, in order, mirroring how integrators consume a sandbox: failure paths first, async/time behavior, production hardening, then cutover. Ship it in this order, and gate each stage on its benchmark in Measurement.

## 1. Choose the isolation model

Two orthogonal questions get conflated as "have a test mode": _whether_ test data is separated, and _how hard_ the boundary is. Three models, ranked:

- efficiency: `soft toggle > hard separate-copy > no test mode (integrator convention)`
- effort: `hard separate-copy > soft toggle > no test mode`
- value: `hard separate-copy > soft toggle > no test mode`

- **Default rung: the soft toggle.** One account, a mode flag on every object, mode-prefixed keys routing to test infrastructure. Test data stays invisible to live calls and vice versa. Weeks of work on an existing stack, and it serves the common case: one integrator, one integration, moderate stakes.
- **Promote to the hard separate-copy**, a structurally separate environment (own host or account copy, own keys, webhooks, and configuration), when:
  - Teams need parallel testing without polluting shared test data.
  - The compliance regime demands demonstrable isolation.
  - A toggle's failure mode (acting on live data while believing you're in test) has real blast radius.

  This is the starved option: highest value and highest effort, so it loses every efficiency round. Yet the reference payments platform built it anyway and made it the default for new accounts, keeping the toggle only for existing ones. Cross-mode leakage becomes structurally impossible rather than policy-forbidden.

- **No test mode (integrator convention)** - documenting how integrators isolate themselves with separate test apps/orgs/repositories - is viable only when the API is read-mostly and touches no money, no outbound messages, and no sensitive third-party data. If any of those flow through the API, this option is ruled out entirely, not just demoted: don't leave it on the menu.

This ranking is a default, not a law. Re-rank against the answers to questions 1-2 and anything else you know:

- A greenfield platform can build the hard model from day one for far less than a retrofit.
- A regulated domain rules the toggle out.
- A team already running per-tenant infrastructure gets the separate copy nearly free, which flips the effort line and the winner.

Whichever model wins, state the isolation level explicitly in the design and the docs. "Sandbox" guarantees nothing by itself - surveyed vendor sandboxes are frequently shared, rate-limited, and only partially isolated under the same word. And if the product has an end-user-facing surface (question 6), the sandbox needs a mirrored end-user side too, not just API responses.

See [references/isolation-models-and-key-prefixes.md](references/isolation-models-and-key-prefixes.md) for the six-vendor comparison behind this menu.

## 2. Make every failure path triggerable

The sandbox's core deliverable is determinism: an integrator must be able to summon any documented outcome - especially failures - on demand. Three simulation primitives, ranked:

- efficiency: `magic values > on-demand simulation endpoints > config-driven fixture builder`
- effort: `config-driven fixture builder > on-demand simulation endpoints > magic values`
- value: `config-driven fixture builder > on-demand simulation endpoints > magic values`

- **Default rung: magic values.** A documented fake input deterministically selects an outcome. Days of work per outcome family, no new API surface, and integrators memorize them.

  Design rules:
  - Pick the carrier integrators already type in your domain (see Product domain split above).
  - Include deliberate-failure values and step-up flows, not just the happy path.
  - Map each value one-to-one onto a real error code from your published catalog (`samber/developer-platform-skills@api-error-design` territory). Magic values must trigger the _real_ taxonomy, never a sandbox-only error shape.
  - Label values per operation when the same input means different things in different calls. An unlabeled multi-operation catalog is a documented integrator trap.

- **Step up to on-demand simulation endpoints** the moment outcomes stop being a function of request input: sandbox-only endpoints that mint test objects for seeding, force an object into a specific state (login-required, verification-passed), or fire a specific event now. These cover what no input value can encode.
- **The config-driven fixture builder** - one endpoint accepting a full fixture description (accounts, history, forced errors) - is the starved option: the most granular mechanism surveyed and the most work, losing every efficiency round. Promote it when integrators' data shapes genuinely vary (data-aggregation domains) - and ship a starter-fixture library with it rather than making every integrator hand-write configs.

Treat magic values as API contract: stable, documented, non-expiring. Integrators' CI suites will depend on every entry, so additions are free but changes are breaking. Recommend tokens over raw sensitive values in example code - raw card-like values in test code become a compliance habit that leaks into production paths.

Worked catalogs from five vendors: [references/magic-value-catalogs.md](references/magic-value-catalogs.md).

## 3. Simulate events and time

A sandbox that freezes _data_ but leaves _time_ real cannot exercise time-triggered logic - renewals, trial expirations, dunning, scheduled jobs. A deterministic clock primitive is the fix, not a documentation workaround telling integrators to wait.

- **Test-event triggering**: give integrators an explicit "fire this event now" mechanism, a sandbox endpoint or CLI trigger per event type. You own when and how a test event gets triggered; delivery mechanics (signing, retries, logs) belong to `samber/developer-platform-skills@webhook-platform-design`.

  Two traps:
  - If state changes and event delivery are decoupled in your sandbox, document it. Integrators otherwise wait for events that never come.
  - If your CLI trigger cannot produce a valid signature, say so next to your "always verify signatures" rule, or the rule breaks your own test tooling.

- **Time manipulation**: a clock object with a frozen time that test objects attach to, advanced deliberately, with state transitions and events firing as if the time had passed. Cap the advance per call and the complexity of what one clock can carry - the reference implementation limits both, as a deliberate simulation-complexity cap. A cheaper rung for simple cases: auto-aging fixtures whose date fields shift daily so the newest data is always "today".
- **Reset and seeding**:
  - Seed with synthetic data only; never copy in production data.
  - Give integrators both object-minting endpoints (seed a known state in one call) and reset endpoints (return to a clean state).
  - Automate periodic resets of shared sandboxes so accumulated test data doesn't drift into an unrepresentative state.
- **Parity**: derive the sandbox's configuration from the same infrastructure-as-code as production, so any difference is intentional and documented. Environment drift - config, data staleness, version skew - is the "works in sandbox, fails live" root cause.

## 4. Harden credentials, quotas, and abuse controls

- **Mode-prefixed keys**: adopt the externally codified prefix convention, a type prefix plus a `_test_`/`_live_` mode substring.
  - The exact reference prefixes are zero-false-positive push-protection targets in GitHub secret scanning. A recognized shape buys free leak detection from tooling you don't control; a novel scheme buys nothing.
  - Enforce the boundary bidirectionally: live keys reject test values, test keys reject real ones.
  - Key format and lifecycle beyond the mode substring belong to `samber/developer-platform-skills@api-auth-key-management`.
- **Test keys are not risk-free**: on a toggle model, test keys still read and write real account configuration (customers, webhook endpoints), so they deserve real secret hygiene - the prefix communicates mode, not risk level. Tell integrators to never use live secrets in local development, and keep per-environment separation (data stores, redirect allowlists, credentials) rather than one codebase branching on a runtime flag.
- **Two abuse classes, distinct mitigations. Never conflate them.**
  - **Leaked-key risk**: prefixed keys are machine-identifiable and routinely harvested from public repositories. Mitigations: server-side-only secrets, scoped/restricted keys, secret-scanning enrollment.
  - **Card-testing/carding abuse**: attackers validate stolen instrument batches against **live** checkout endpoints. The sandbox is generally useless for carding, since test transactions never touch real networks, so this is a live-mode control, not a sandbox one. Mitigations: edge bot challenges, endpoint-scoped rate limits, and rules capping instruments-per-customer and consecutive declines per IP.

  Stripe's own fraud-team guidance reports that managed CAPTCHA for all Checkout users cut card testing by 80% with under 0.02% impact on authorization rates, a rare fraud control with a quantified, near-negligible legitimate-user cost.

- **Sandbox quotas**: don't assume the sandbox needs its own rate-limit tier. Three of six vendors reviewed here reuse their production limits unchanged in test mode, which also keeps integrators' throttling code honest.
  - Sandbox-specific numeric limits are the sparsest-documented axis across those vendors, so treat "every vendor publishes a distinct sandbox throttle" as false.
  - Build a dedicated sandbox quota only when the failure mode is _evaluation-volume abuse_ (free-tier scraping, load tests against a shared sandbox). Model it as an aggregate volume-and-scope cap on the pre-production tier, not a faster per-minute limiter.
  - Per-vendor quota postures: [references/isolation-models-and-key-prefixes.md](references/isolation-models-and-key-prefixes.md). Limit-tier design mechanics belong to `samber/developer-platform-skills@api-rate-limit-policy`.

## 5. Design the graduation path

Graduation is never purely technical, even when the credential swap is trivial - every surveyed vendor gates production behind a compliance or review step. Design three things:

1. **The gate**: pick the shape matching your actual obligation - KYC activation, tiered/auto-approved review, partner vetting, publisher verification, or plan tier. Don't import a heavier gate than the domain requires. Make pre-approval failures legible: an explicit "environment not yet approved" error, never an opaque 401.
2. **The cutover checklist**:
   - Credentials swapped everywhere.
   - Fresh live-mode event endpoints and signing secrets (test-mode secrets do not carry over).
   - Abuse rules on before the first live transaction.
   - A small live canary per integration path, confirmed effect _and_ confirmed event delivery, ideally reversed afterwards.

   A green sandbox run is necessary but not sufficient: no sandbox replicates real networks, real settlement timing, or full-strength fraud systems.

3. **The publishable version**: hand integrators the checklist and the five recurring cutover pitfalls as documentation - they are the same five support tickets every platform eventually answers.

Gate shapes, the full checklist, pitfalls, and reactive go-back triggers: [references/graduation-gates-and-cutover-checklist.md](references/graduation-gates-and-cutover-checklist.md).

## Failure modes

Anti-pattern checklist - each is a direct design-review finding:

- A mock server shipped as "the sandbox": stateless, it tests the integrator's assumptions about your API, not their correctness - when the API changes, the mock keeps simulating the old behavior while production breaks silently. Vendor-exercised real objects cannot drift this way.
- A documented failure outcome with no way to trigger it deterministically in the sandbox.
- Magic values that return a sandbox-only error shape instead of the real published error taxonomy.
- Time-dependent logic testable only by waiting real calendar time.
- The word "sandbox" in docs with no stated isolation level.
- A wrong-environment credential producing an opaque authentication failure instead of a clear "wrong environment" error - a named, recurring support-ticket generator.
- The five cutover pitfalls (key swap forgotten, cross-environment paste, sandbox-predicts-live assumption, stale live webhook endpoints, untested real-money failure paths) left undocumented for integrators.
- Real production data copied into the sandbox as seed data.
- A shared sandbox with no reset mechanism and no periodic cleanup.

## Measurement

- **Failure-path coverage**: every documented failure outcome (declines, error codes, step-up flows, disputes/reversals) is triggerable deterministically via a magic value or simulation endpoint - a gate at 100%; one untriggerable failure path fails the audit.
- **Event/time coverage**: every async event type is fireable on demand, and every time-dependent flow is testable via simulated time, never by waiting - also a gate.
- **Cross-environment incidents**: track support tickets and auth failures caused by wrong-mode credentials; the design target is zero, achieved structurally (self-describing prefixes plus a legible wrong-environment error), not by warning integrators to be careful.
- **Graduation exercise**: the cutover checklist is walked end-to-end - including one live canary with confirmed event delivery - before any integration is declared launched; treat an unexercised checklist as an unshipped feature.

Iterate the design until both coverage gates pass. They apply from the soft toggle up; the "no test mode" rung of step 1 has no provider-side sandbox to trigger anything in, so its gates are out of scope rather than failed. Holding that rung to the gates would reject an option this skill itself prescribes as viable.

What replaces them there: the published integrator-isolation guidance exists, and step 1's read-mostly/no-money/no-messages/no-sensitive-data conditions are each confirmed in writing. Cross-environment incidents and sandbox-to-live conversion time are trends to baseline from the first month and improve against, since no cross-industry threshold exists to borrow.

## Invocation examples

- "Design a test mode for our payments API - integrators currently test against staging with real card numbers."
- "We're adding webhooks; integrators need a way to trigger test events and simulate a subscription renewing without waiting 30 days."
- "Choose between a test-mode toggle and a fully separate sandbox environment for our new public API, and design the graduation path to live."

## References

- [references/isolation-models-and-key-prefixes.md](references/isolation-models-and-key-prefixes.md) - six-vendor isolation comparison, the test-key prefix taxonomy, per-vendor sandbox quota postures, and the non-prefix alternatives with their support cost.
- [references/magic-value-catalogs.md](references/magic-value-catalogs.md) - worked magic-value catalogs across payments, communications, and data aggregation, with the design lessons each teaches.
- [references/graduation-gates-and-cutover-checklist.md](references/graduation-gates-and-cutover-checklist.md) - five compliance-gate shapes, the cutover checklist, the five pitfalls, and reactive go-back triggers.
- `samber/developer-platform-skills@api-integration-surface-strategy` - the umbrella decision that schedules each surface; every surface it schedules needs a test mode before partners go live, and this skill designs that layer.
