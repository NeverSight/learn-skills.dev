---
name: tdd
description: Use before implementing a feature or bug fix that adds or changes behavior users or callers rely on, including requests that do not mention tests or TDD. Not for removing features or code, behavior-preserving refactors, design or UX exploration, prototypes, styling, copy, configuration, or data cleanup.
---

# Test-Driven Development

Work in small red → green → refactor cycles: write one behavior as a test, watch it fail, implement it, then tidy the changed code. Read `CONTEXT.md` and relevant ADRs if they exist, so tests use the project's domain terms.

## Decide whether a test is warranted

Write a test only when the change adds or alters a rule that users or callers will rely on from now on. Tests exist to catch realistic regressions of such rules; coverage by itself is not a reason to write one. If the change does not create such a rule, say so in one line and implement without the cycle.

Tests describe what the system does. Do not write a test that asserts a feature, route, option, or default is absent. When removing behavior, delete the tests that covered it and run the remaining suite, which already catches anything that still depended on it.

Do not write tests while drafting designs, UI, or ideas. Write them once the behavior is agreed and you are building it.

## Choose the test

Before writing a test, name the requirement that sets the expected outcome, the starting conditions, and the realistic failure the test should catch.

- Test through the interface that owns the behavior. This can be a public API or an internal module interface. Prefer existing interfaces and the test conventions near the code.
- Use real collaborators when their behavior is part of what the test claims. Replace a dependency only to control time, randomness, or failures, or when it sits outside the test's claim. [test-evidence.md](test-evidence.md) lists what counts as evidence for common contracts and when test doubles are appropriate.
- Cover critical paths and complex logic. Do not cover every edge case.
- Do not expose private state or add public methods, wrappers, or configuration only to make a test easier to write. When the interface itself is in question, use the `codebase-design` skill.

## Cycle

Features and bug fixes follow the same cycle. For a bug, the first test reproduces the reported failure at the narrowest level already tested near that code.

1. Pick the smallest observable behavior.
2. Write one focused test for it.
3. Run it before changing production code, and confirm it fails because the behavior is missing. If it passes, or fails because of a setup or test error, fix the test first.
4. Make the simplest production-quality change that passes it. Don't add behavior for later tests.
5. Run it and confirm it passes.
6. Refactor the changed code if ownership or cohesion suffered, and rerun the test.
7. Choose the next behavior based on what you learned. Don't write all the tests up front.

For a flaky bug, make the regression test deterministic and say what it locks down. If the bug belongs to a broader class of failures, fix the reported case first, then consider sibling cases.

## Keep the expectation honest

Change a test's expected outcome only when the requirement changed, the test was wrong against the requirement, or an interface change keeps the same protected behavior. Say why when you do. The implementation's new output is never a reason to change the expected output.

These moves make a failing test pass without fixing the behavior. Do not use them:

- updating an assertion, snapshot, or fixture to match the new output
- seeding state in setup that the real workflow does not guarantee, such as a flag, a backfill, or initialized data
- mocking away the logic or integration the test claims to check
- accepting an error as success, or testing only graceful rejection when the requirement is a working path
- skipping the test, marking it as an expected failure, or excluding it from the run
- computing the expected value with the same logic as the production code

If a valid failing test needs a domain decision, a missing prerequisite, or work outside the agreed scope, keep the test red, keep the completed work, and report the blocker and that the work is unfinished. A request only to reproduce a bug is complete with the test still red and does not authorize fixing production code.

## When a failing test is impractical

Don't build substantial test infrastructure, slow end-to-end setups, or elaborate mocks just to follow the cycle. Before implementing, explain the limitation and pick another check that shows the behavior is missing and then fixed, such as a script, a command, a browser workflow, or a log check. If nothing can run, report the gap.

A test written after the implementation still protects against regressions, but it is not evidence of test-first work. If you run it against the old code to show it would have failed, say that is what you did.

## Validation

In each cycle, run the focused test and tests near the change. Run broader checks when a shared contract or a repository rule calls for it, and run the repository's required checks once at the end. Confirm the tests you rely on actually ran. A command that passed because it skipped them proves nothing.

## Final response

- the test or check that failed before the change and how it failed, or the one-line reason no test was warranted
- the passing run after the change, or the still-failing test and its blocker
- other checks run, with results
- if failing-before evidence was not possible, why, and which check was used instead
