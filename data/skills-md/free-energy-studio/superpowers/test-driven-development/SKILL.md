---
name: test-driven-development
description: Use when implementing a testable behavior change or bug fix, especially when a regression test can demonstrate the defect.
---

# Test the Behavior

Prefer a focused failing test before changing behavior. It makes the intended
contract explicit and checks that the test can detect the problem.

1. Write a test for the requested behavior or observed failure.
2. Run it and confirm it fails for the expected reason, not a broken fixture.
3. Implement the simplest correct change.
4. Run the focused test, then relevant surrounding checks.
5. Simplify while preserving behavior and passing tests.

Test observable contracts, not private call sequences or one mock per internal
helper. Use realistic integration coverage at important boundaries. Follow the
repository's test conventions; do not introduce a new framework without need.

If implementation already exists, preserve it. Add the regression test and, where
safe, demonstrate that it detects the old behavior in an isolated copy or reversible
local experiment. Never delete working code or user changes to recreate the preferred
order. Be honest if a pre-fix failure was not demonstrated.

For changes without a meaningful automated behavioral test—such as prose,
exploratory work, or a visual adjustment—use an appropriate check and state its
limits. Do not manufacture brittle tests to satisfy a ritual. Explicit repository
requirements still apply.

Keep tests readable and focused. A test should earn its cost by detecting a
meaningful regression. See `writing-good-tests.md` for detailed test-design guidance.
