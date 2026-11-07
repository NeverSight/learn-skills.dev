---
name: writing-tests
description: Write high-signal automated tests and avoid test theatre. Use when adding, reviewing, deleting, or restructuring unit, integration, property, golden, fixture, or regression tests.
---

# Writing Tests

The rule is **no earned signal, no test**. Do not add tests to mirror a diff, preserve a literal, or make a tiny change look safer. A test earns its place when it proves behavior that can regress independently from the edit.

Tests are for business behavior, invariants, transformations, runtime and permission boundaries, generation contracts, and user-visible workflows. A test whose only meaningful failure is "this static value changed" is usually duplication, not protection.

## Is This Test Worth Writing?

A test earns its place only if it passes all of these. If it fails one, rewrite it or do not write it.

1. **Behavior, not implementation.** It asserts an observable contract: return value, thrown error, persisted-state change, rendered/exported output, API/CLI response, generated artifact, or externally visible side effect. A harmless internal refactor should not break it.
2. **Mutation-sensitive.** At least one assertion fails if behavior is subtly wrong: a condition is negated, a boundary changes, a constant is returned, or persisted state is missing.
3. **Non-trivial.** It is not a getter returning what was set, a pass-through helper returning its input, a wrapper calling the function it wraps, an enum array equalling a hand-copied literal of itself, a public-export assertion, or a runtime assertion of the type system.
4. **Independent.** It passes in isolation and in any order. No shared mutable state, hidden clock coupling, or fixture order dependency.
5. **Right layer.** Pure calculation/parser/reducer/selector logic belongs in a fast unit test. Database, schema, validator, permission, runtime, and multi-unit wiring behavior belongs in an integration test using the project's real harness. Full user journeys belong in end-to-end verification.
6. **Not duplicated.** The same behavior is not already covered at a cheaper layer.

For bug fixes, start from the original failure. The highest-value verification is usually the route, API, browser flow, command, or integration seam that failed. A unit test for a helper invented during the fix does not count as regression coverage unless that helper owns the failing behavior.

## Do Not Add These

- Tests that mirror implementation data or single changed literals: static config rows, catalogue statuses, navigation membership, route tables, feature flag defaults, labels, copy, or status lists.
- Tests of library behavior already owned by the library.
- Tests created only because code was extracted.
- Getter/setter, pass-through, one-line wrapper, public-export, or type-only tests.
- Tests that assert a mock was called with exactly what the test told it to call.
- React/component mount tests when extracted logic plus browser/e2e verification proves the behavior more directly.
- Fake integration tests that cannot catch the bug class they claim to cover, such as hand-rolled database emulators for behavior that depends on real schema, validators, indexes, triggers, permissions, or runtime behavior.
- Snapshots or goldens that will be regenerated without reasoning.

## Good Test Shapes

- Business calculations, state transitions, validation, filtering, derivation, permissions, parser behavior, data transformations, generation contracts, cross-file consistency, idempotency, and class-wide invariants.
- Property tests for broad invariants such as round-trips, conservation, commutativity, normalization, monotonicity, or "round once at the boundary" rules. Prefer an invariant property over a "does not throw" property.
- Integration tests for behavior that depends on real schema, validators, indexes, triggers, permissions, provider/runtime boundaries, or multi-unit wiring.
- Golden tests only when the artifact itself is the contract: emitted event shape, public protocol output, rendered document text/structure, migration behavior, generated code, or provider response parsing. Keep the update command explicit and regenerate only with intent.

## Structure And Runner

Follow the project's established testing architecture: runner, directory layout, fixture convention, filename suffixes, package scripts, and tiering. Do not invent a parallel pattern.

If the project has a default runner, use it. Use an alternate runner only for a real forcing constraint such as a required runtime, DOM environment, native visual harness, module-reset facility, framework compiler, or integration test library. Do not mix runners in one package or surface without an explicit project rule.

Fixtures and builders should live beside the tests unless the project has a shared fixture convention. Provider/API fixtures should preserve the semantics of real responses; cut size if needed, not meaning.

## AI Authoring Guidance

Write the assertion first, then the setup. Prefer one to three meaningful assertions per test. Target the failure modes agents tend to skip: null, empty, boundary, error, concurrency, permissions, and business-rule edges.

Run the targeted test and the project checks required for the touched surface. For bug fixes, prove the test would fail on the original failure when practical.
