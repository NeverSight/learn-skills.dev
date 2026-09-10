---
name: tdd
description: Use test-driven development for behavior-changing feature or fix work, and whenever the user mentions TDD, test-first, red-green-refactor, tracer bullets, integration tests, or public-interface behavior tests. Skip for docs-only, path-only rename, formatting-only, or purely mechanical chores unless explicitly requested.
license: MIT
compatibility: Requires bun for Plaited repository validation
---

# Test-Driven Development

## Core Rule

Work in vertical red-green-refactor slices:

1. **RED**: write one test for one observable behavior.
2. **GREEN**: implement the smallest production change that makes that test pass.
3. **REFACTOR**: clean up only while tests are green.

Do not write a batch of imagined tests before implementation. Each new test should respond to
what the last cycle taught you about the actual behavior and interface.

## Plaited Defaults

- Use `bun test` for targeted tests and `bun --bun tsc --noEmit` for the type gate.
- Use `test`, not `it`, and organize with `describe`.
- Prefer real dependencies and real runtime boundaries over mocks.
- Mock only external boundaries such as remote APIs, time, randomness, or rare filesystem cases.
- Avoid conditional assertions: assert the branch first, then assert branch-specific values.
- Test both branches for conditionals, fallbacks, and error paths.
- Exercise public interfaces and runtime contracts rather than private helpers.
- Follow applicable repo skills and `AGENTS.md` rules for the touched area.

## When Starting Work

Explore the codebase first. If the public interface, expected behavior, or risk boundary is
discoverable from code, tests, or docs, use that evidence instead of asking the user.

Ask one concise question only when the decision cannot be discovered and a reasonable assumption
would be risky. Include your recommended answer.

Before writing production code, identify:

- the public interface or runtime boundary under test
- the first observable behavior to prove
- the targeted test command for the cycle
- the broader validation needed before handoff

## Cycle Discipline

For each behavior:

1. Add or update exactly one focused test.
2. Run the targeted test and confirm it fails for the intended reason.
3. Implement only enough code to pass.
4. Run the same targeted test and confirm it passes.
5. Refactor if useful, then rerun the affected tests.

If the test passes before production code changes, it is not a valid RED signal. Tighten the test,
choose a different behavior, or explain why existing coverage already proves the behavior.

## Reference Files

- [references/tests.md](references/tests.md): behavior-test examples and implementation-detail red flags
- [references/mocking.md](references/mocking.md): boundary-only mocking guidance
- [references/interface-design.md](references/interface-design.md): testable public interface design
- [references/deep-modules.md](references/deep-modules.md): small interface, deep implementation guidance
- [references/refactoring.md](references/refactoring.md): refactor checks to run after green
