---
name: unit-testing
description: Load this skill when writing or reviewing unit tests - verifying individual functions or modules in isolation, fast and deterministic.
user-invocable: true
---

# Unit Testing

Category: Testing (Quality Assurance) - Verification

## Purpose

Verify individual units of behavior in isolation: milliseconds per test, no
external systems, one behavior per test.

## Standards

1. **Scope.** A unit test exercises one function or one class through its
   public surface. If a test needs a database, network, or filesystem to
   pass, it is not a unit test - move it up a level.
2. **Determinism.** No network, no wall clock (inject time), no randomness
   (seed it), no filesystem unless it is the unit under test. A test that
   fails sometimes is a defect in the test suite, not a feature of CI.
3. **Structure.** Arrange - Act - Assert. One logical assertion cluster per
   test. The name states the behavior and the expectation:
   `parse rejects empty input`, not `test_parse_3`.
4. **Boundaries.** Mock only at the module's declared dependencies (ports),
   never its internal collaborators. A test that mocks what the production
   code reaches through is testing the mock.
5. **Coverage of failure.** Every error branch the unit can produce gets a
   test: invalid input, null/undefined, out of range, wrong type. The
   error paths are where unit tests earn their keep.

## Techniques

- Parameterized tests for input classes instead of copy-pasted cases.
- Property-based tests for pure functions (invariants, round-trips,
  idempotence) when example-based cases feel insufficient.
- Table-driven expected values for parsers, validators, and serializers.

## Anti-patterns

- Testing private functions directly - if it needs a test, test it through
   the public surface, or the split is wrong.
- Shared mutable fixtures across tests; every test builds or owns its data.
- Order-dependent tests; the suite must pass in any order, in isolation.
- Assertion-free tests that only exercise code (proves nothing).

## Review gate

A unit test is acceptable when: it fails for the right reason when the
behavior breaks, passes when the behavior is correct, and its name alone
tells you what went wrong when it fails.
