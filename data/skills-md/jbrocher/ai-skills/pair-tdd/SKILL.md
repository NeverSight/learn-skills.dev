---
name: pair-tdd
description: Pair-building test-driven development with explicit human handoffs at red and before refactoring. Use when a developer wants to build or fix behavior collaboratively, test-first, one red-green-refactor slice at a time.
---

# Pair TDD

Use TDD as a pair-building protocol. Either the developer or the agent may write production code or refactor; the agent owns verification of the test state and pauses at the handoff points.

When exploring the codebase, read `CONTEXT.md` if present so test names and interfaces use the project's domain language. Respect relevant ADRs and existing test conventions.

## Agree on the seam

A seam is the public boundary through which behavior is exercised and observed. Before writing a test, state the seam and confirm it with the developer. Do not test an unconfirmed seam.

Prefer ports and adapters when behavior depends on infrastructure:

- Keep domain or application behavior behind a stable public interface.
- Express external capabilities as narrow ports owned by the application.
- Implement infrastructure concerns in adapters.
- Inject a port or adapter rather than constructing infrastructure inside the behavior under test.
- Test application behavior through the public seam with a fixture or fake port; test a real adapter separately against its protocol boundary.

Read [references/testing.md](references/testing.md) when writing tests. Read [references/boundaries.md](references/boundaries.md) when the slice uses dependency injection, FastAPI dependencies, or external HTTP.

## Pair-building cycle

Work in one vertical slice at a time. Never write a batch of tests against imagined behavior.

### 1. Red

Write one test that specifies one observable behavior through the agreed seam. Run the narrowest relevant test command and establish that it fails for the intended reason, not because of test setup, imports, or an unrelated defect.

Report the failing test and its relevant failure. **Then pause.** Do not write production code in the same turn. The developer may implement the behavior, or may explicitly ask the agent to resume and implement it.

### 2. Green

When asked to resume, inspect any implementation changes made during the handoff. If implementation is still needed and the developer asks the agent to do it, write only enough production code to satisfy the current test; do not anticipate later slices.

Run the focused test and prove it passes. Then run the proportionate surrounding suite to catch regressions. A developer-provided implementation is not considered green until the agent has performed this verification.

Report the passing commands and result. **Then pause before refactoring.** Do not refactor in the same turn. The developer may refactor, or may explicitly ask the agent to resume and refactor.

### 3. Refactor

When asked to resume, inspect any developer changes. If the agent is asked to refactor, change structure without changing observable behavior. Run the focused test and surrounding suite again. If either fails, restore green before proposing another slice.

After verification, report the result and ask whether to begin the next red slice.

## Test quality

Tests should read as behavioral specifications, use public interfaces, and survive internal refactors. Expected values must come from an independent source such as a requirement, worked example, or known literal.

Avoid:

- mocking private or internal collaborators;
- asserting internal calls, ordering, or implementation structure unless that interaction is itself the public protocol;
- verifying behavior through a side channel instead of the public interface;
- recomputing the expected result with the same algorithm as production code;
- adding several tests before making the first one green.

Mocks and protocol fakes belong at system boundaries such as external APIs, time, randomness, filesystems, and occasionally databases. Prefer a real test database when proportionate.
