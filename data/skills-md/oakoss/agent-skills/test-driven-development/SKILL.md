---
name: test-driven-development
description: |
  Red-green-refactor discipline for writing code driven by tests. Covers the TDD cycle, test quality, mocking boundaries, and design for testability.

  Use when: implementing features, fixing bugs, refactoring existing code, designing module interfaces, or working within vertical slices from a tracer-bullets workflow.
license: MIT
metadata:
  author: oakoss
  version: '1.0'
  source: https://www.aihero.dev/skill-test-driven-development-claude-code
user-invocable: false
---

# Test-Driven Development

Write one failing test that describes the next behavior, write the minimal code to pass it, then refactor while green. Every production change starts with a test that proves the need exists. This is the discipline within each vertical slice — not framework syntax, but when and why to write tests.

Skip for exploratory prototyping, config-only changes (environment variables, feature flags), visual/CSS-only tweaks, and one-off scripts that won't be maintained.

## Quick Reference — TDD Cycle

| Phase    | Action                                           | Rule                                        |
| -------- | ------------------------------------------------ | ------------------------------------------- |
| RED      | Write one test that fails for the right reason   | No production code without a failing test   |
| GREEN    | Write the simplest code that makes the test pass | Resist the urge to generalize prematurely   |
| REFACTOR | Improve structure while all tests stay green     | Never change behavior and structure at once |

## Quick Reference — Principles

| Principle                    | Practice                                                                           |
| ---------------------------- | ---------------------------------------------------------------------------------- |
| One test at a time           | Complete the full red-green-refactor cycle before writing the next test            |
| Behavior over implementation | Test what code does, not how it does it; assert outputs and side effects           |
| Vertical slices              | TDD one end-to-end behavior at a time, not one layer at a time                     |
| Mock at boundaries           | Mock I/O, network, filesystem, clock. Never mock internal collaborators            |
| Deep modules                 | Design small interfaces with rich internals; fewer tests cover more behavior       |
| Refactor only when green     | All tests pass before touching structure; refactoring under red hides new bugs     |
| Design through tests         | The first test IS the API design decision; awkward tests signal awkward interfaces |
| Failing test for every bug   | Reproduce the bug as a failing test before writing the fix                         |

## Planning Before Coding

| Step | Action                   | Output                                                 |
| ---- | ------------------------ | ------------------------------------------------------ |
| 1    | Identify behaviors       | List of observable behaviors the feature must exhibit  |
| 2    | Order by dependency      | Sequence where each test builds on prior passing tests |
| 3    | Design the interface     | Function signatures, parameter types, return types     |
| 4    | Identify mock boundaries | External dependencies that need test doubles           |

## Common Mistakes

| Mistake                            | Correct Pattern                                                              |
| ---------------------------------- | ---------------------------------------------------------------------------- |
| Writing all tests first            | One test at a time. Complete the cycle before starting the next              |
| Testing private methods            | Test through the public interface; private methods are implementation detail |
| Mocking internal collaborators     | Only mock at I/O boundaries; trust your own code                             |
| Writing code before a failing test | RED first. The failing test proves the behavior is missing                   |
| Refactoring while tests are red    | Get to GREEN first, then refactor with confidence                            |
| Tests coupled to call sequences    | Assert on outputs and state, not on which internal methods were called       |
| Skipping the refactor phase        | GREEN is not done. Clean up duplication and naming before moving on          |
| Hardcoding expected values         | Use triangulation: add a second test case to force the general solution      |
| One giant test per feature         | One test per behavior — small, focused, independently meaningful             |

## Delegation

- **Slice decomposition**: If the `tracer-bullets` skill is available, use it to decompose features into vertical slices before applying TDD within each slice
- **Test framework syntax**: Delegate framework-specific patterns to `vitest-testing`, `e2e-testing`, or `api-testing` skills
- **Feature planning**: If the `plan-first-development` skill is available, use it for upfront planning before entering the TDD cycle
- **Individual TDD cycles**: Delegate each red-green-refactor cycle to a `Task` subagent to keep context focused

## References

- [Test Quality](references/test-quality.md) — good vs bad tests, what to test, naming, triangulation, refactoring signals
- [Mocking Boundaries](references/mocking-boundaries.md) — boundary rule, test doubles, dependency injection, anti-patterns
- [Design for Testability](references/design-for-testability.md) — deep modules, interface-first design, pure functions, computation vs I/O
