---
name: tdd
description: >-
  Guides test-driven development using a vertical-slice tracer bullet
  workflow. Use when implementing features, fixing bugs, or writing tests
  that should drive design. Enforces planning before coding, incremental
  red-green-refactor cycles, and behavior-based testing through public
  interfaces. Triggers: "TDD," "test first," "write tests," "tracer
  bullet," or incremental feature implementation with tests.
---

# Core Principle

Tests verify **behavior through public interfaces**, not implementation details. Code can change entirely; tests shouldn't. A good test reads like a specification — "user can checkout with valid cart" tells you exactly what capability exists. These tests survive refactors because they don't care about internal structure.

See [tests.md](references/tests.md) for good vs bad test examples.

# Anti-Pattern: Horizontal Slicing

**DO NOT write all tests first, then all implementation.** This is "horizontal slicing" — treating RED as "write all tests" and GREEN as "write all code."

This produces crap tests:

- Tests written in bulk test _imagined_ behavior, not _actual_ behavior
- You end up testing the _shape_ of things (data structures, function signatures) rather than user-facing behavior
- Tests become insensitive to real changes — they pass when behavior breaks, fail when behavior is fine
- You outrun your headlights, committing to test structure before understanding the implementation

**Correct approach**: Vertical slices via tracer bullets. One test → one implementation → repeat. Each test responds to what you learned from the previous cycle.

```
WRONG (horizontal):
  RED:   test1, test2, test3, test4, test5
  GREEN: impl1, impl2, impl3, impl4, impl5

RIGHT (vertical):
  RED→GREEN: test1→impl1
  RED→GREEN: test2→impl2
  RED→GREEN: test3→impl3
```

# Workflow

## Step 1: Planning

Before writing any code:

- [ ] Confirm with user what interface changes are needed
- [ ] Confirm with user which behaviors to test (prioritize)
- [ ] Identify opportunities for [deep modules](references/interface-design.md) (small interface, deep implementation)
- [ ] Design interfaces for [testability](references/interface-design.md)
- [ ] List the behaviors to test (not implementation steps)
- [ ] Get user approval on the plan

Ask: "What should the public interface look like? Which behaviors are most important to test?"

**You can't test everything.** Confirm with the user exactly which behaviors matter most. Focus testing effort on critical paths and complex logic, not every possible edge case.

## Step 2: Tracer Bullet

Write ONE test that confirms ONE thing about the system:

```
RED:    Write test for first behavior → test fails
GREEN:  Write minimal code to pass → test passes
VERIFY: Run project lint + full test suite → must pass
COMMIT: Atomic commit (conventional commits v1)
```

This is your tracer bullet — proves the path works end-to-end.

**Do not proceed if lint or tests fail.** Fix first.

## Step 3: Incremental Loop

For each remaining behavior:

```
RED:    Write next test → fails
GREEN:  Minimal code to pass → passes
VERIFY: Lint + tests → must pass
COMMIT: Atomic commit
```

Rules:

- One test at a time
- Only enough code to pass current test
- Don't anticipate future tests
- Keep tests focused on observable behavior
- Never proceed past a failing lint or test — fix before moving on
- One commit per cycle — never batch unrelated changes

## Step 4: Refactor

After all tests pass, look for refactor candidates:

- [ ] Extract duplication into functions/classes
- [ ] Deepen modules — move complexity behind simple interfaces
- [ ] Apply SOLID principles where natural
- [ ] Move logic to where data lives (feature envy)
- [ ] Introduce value objects for primitive obsession
- [ ] Consider what new code reveals about existing code
- [ ] Long methods → break into private helpers (keep tests on public interface)
- [ ] Run tests after each refactor step

**Never refactor while RED.** Get to GREEN first.

## Step 5: Completion

After all acceptance criteria met and all checks pass:

- Print `## Manual Testing Checklist` with concrete steps to verify manually (if applicable)
- Stop

# Per-Cycle Checklist

```
[ ] Test describes behavior, not implementation
[ ] Test uses public interface only
[ ] Test would survive internal refactor
[ ] Code is minimal for this test
[ ] No speculative features added
[ ] Lint + tests pass
[ ] Atomic commit made (conventional commits v1)
```

# References

Load these on demand when the situation calls for it:

- [tests.md](references/tests.md) — Good vs bad test examples. Load when writing or reviewing tests.
- [mocking.md](references/mocking.md) — When and how to mock. Load when deciding whether to mock a dependency.
- [interface-design.md](references/interface-design.md) — Testable interfaces and deep modules. Load when designing interfaces or when tests feel hard to write.
