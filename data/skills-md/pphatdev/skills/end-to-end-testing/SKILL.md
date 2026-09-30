---
name: end-to-end-testing
description: Load this skill when verifying complete user journeys through the real stack - journey selection, deterministic data, wait strategies, flakiness protocol, and suite budget.
user-invocable: true
---

# End-to-End Testing

Category: Testing (Quality Assurance) - Verification

## Purpose

Verify the critical user journeys work through the real stack - and only
those. End-to-end is the most expensive level; every test must earn its
place.

## Journey selection

Cover only journeys whose failure costs the business: authentication and
authorization, signup/checkout/payment, the core loop of the product.
Typical budget: under 20 tests. If logic can be verified at unit or
integration level, it does not belong here.

## Standards

1. **Deterministic data.** Each run creates its own users, sessions, and
   records (unique per run), and cleans up. Never share accounts or data
   between parallel runs.
2. **Wait on conditions, never on time.** Poll for selectors, URL changes,
   or API responses. A fixed `sleep` is a flake scheduled in advance and
   makes the suite slow.
3. **Stable selectors.** Prefer test-id attributes and accessible roles;
   never CSS paths or generated class names. Selectors that survive
   styling changes keep the suite maintainable.
4. **Independent journeys.** Each test stands alone: fresh session, no
   dependency on a previous test's end state.
5. **Assert at the right altitude.** Verify the outcome the user came for
   (the confirmation, the saved record, the visible result), not pixels,
   not intermediate spinners.

## Flakiness protocol

1. A test that fails intermittently is a defect - in the test or in the
   system (race condition, unwaited async, shared state).
2. Reproduce by running in isolation and under parallel load. Fix the
   cause: add the missing condition-wait, isolate the data, report the
   system bug.
3. If it cannot be fixed immediately, quarantine it with a tracked reason
   and a deadline. Never delete a flaky test to go green, and never mark
   the suite green while a quarantined test rots silently.

## Anti-patterns

- E2E as the default level ("it feels more real") - the suite becomes slow,
  flaky, and diagnostic-poor. Push down first.
- Screenshots/videos as assertions.
- One mega-journey testing five features: every failure is ambiguous.

## Review gate

Suite runtime under the team's budget, zero fixed sleeps, and every test
traceable to a named business journey.
