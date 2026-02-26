---
name: tdd
description: Guides agent through test-driven development using red-green-refactor. Use when user mentions TDD, red-green-refactor, test-first development, outside-in TDD, mockist TDD, London-school TDD, acceptance TDD, or double-loop TDD. Do not use for writing E2E/Playwright tests, configuring test runners or frameworks, adding tests without TDD methodology, or general testing advice.
---

# Test-Driven Development

## Philosophy

**Core principle**: Tests should verify behavior through public interfaces, not implementation details. Code can change entirely; tests shouldn't.

**Good tests** are integration-style: they exercise real code paths through public APIs. They describe _what_ the system does, not _how_ it does it. A good test reads like a specification - "user can checkout with valid cart" tells you exactly what capability exists. These tests survive refactors because they don't care about internal structure.

**Bad tests** are coupled to implementation. They mock internal collaborators, test private methods, or verify through external means (like querying a database directly instead of using the interface). The warning sign: your test breaks when you refactor, but behavior hasn't changed. If you rename an internal function and tests fail, those tests were testing implementation, not behavior.

Read [references/tests.md](references/tests.md) for test naming rules and examples when writing tests. Read [references/mocking.md](references/mocking.md) for when and how to mock. Read [references/test-tiers.md](references/test-tiers.md) for organizing unit vs component tests. Read [references/component-testing.md](references/component-testing.md) for UI component testing patterns.

## Task Analysis

Two legitimate TDD styles. Pick one per feature; don't mix mid-feature. **Actively classify the task before writing any tests.**

### Step 1 — Check for explicit request

If user said "classical", "Detroit", or "inside-out" → **Classical**. Done.
If user said "outside-in", "London", "mockist", or "double-loop" → **[Outside-in](references/outside-in.md)**. Done.

Otherwise, proceed to Step 2.

### Step 2 — Examine task and codebase

- [ ] **Entry point** — where does the change enter? (UI component, route, API handler, domain service, utility)
- [ ] **Scope** — single module or crosses multiple layers?
- [ ] **Collaborators** — existing with stable interfaces, or new ones to discover?
- [ ] **Task language** — user-visible behavior ("user can...") or internal logic ("calculate", "transform")?

**[Outside-in](references/outside-in.md)** when ANY:
- Entry point is UI / route / controller
- Spans 2+ layers with new collaborators to discover
- Describes user journey or end-to-end flow
- Greenfield multi-component feature

**Classical** when:
- Single module with existing interface
- Algorithms, data transforms, domain rules
- Integrating with existing deep modules
- No outside-in signals

**Default: classical** when ambiguous. Outside-in requires discipline to replace mocks with real implementations; classical has no such cleanup tax.

### Step 3 — State classification

Before proceeding, copy the template from [assets/classification-template.md](assets/classification-template.md), fill it in, and present it to the user. Wait for user confirmation before writing any tests.

## Anti-Pattern: Horizontal Slices

**DO NOT write all tests first, then all implementation.** This is "horizontal slicing" - treating RED as "write all tests" and GREEN as "write all code."

This produces **crap tests**:

- Tests written in bulk test _imagined_ behavior, not _actual_ behavior
- You end up testing the _shape_ of things (data structures, function signatures) rather than user-facing behavior
- Tests become insensitive to real changes - they pass when behavior breaks, fail when behavior is fine
- You outrun your headlights, committing to test structure before understanding the implementation

**Correct approach**: Vertical slices via tracer bullets. One test → one implementation → repeat. Each test responds to what you learned from the previous cycle. Because you just wrote the code, you know exactly what behavior matters and how to verify it.

```
WRONG (horizontal):
  RED:   test1, test2, test3, test4, test5
  GREEN: impl1, impl2, impl3, impl4, impl5

RIGHT (vertical):
  RED→GREEN: test1→impl1
  RED→GREEN: test2→impl2
  RED→GREEN: test3→impl3
  ...
```

## Workflow (Classical / Inside-Out)

### 1. Planning

Using the entry point and scope identified in [Task Analysis](#task-analysis):

- [ ] Confirm with user what interface changes are needed
- [ ] Confirm with user which behaviors to test (prioritize)
- [ ] Identify opportunities for [deep modules](references/deep-modules.md) (small interface, deep implementation)
- [ ] Design interfaces for [testability](references/interface-design.md)
- [ ] List the behaviors to test (not implementation steps)
- [ ] Get user approval on the plan

Ask: "What should the public interface look like? Which behaviors are most important to test?"

**You can't test everything.** Confirm with the user exactly which behaviors matter most. Focus testing effort on critical paths and complex logic, not every possible edge case.

### 2. Tracer Bullet

Write ONE test that confirms ONE thing about the system:

```
RED:   Write test for first behavior → test fails
GREEN: Write minimal code to pass → test passes
```

This is your tracer bullet - proves the path works end-to-end.

### 3. Incremental Loop

For each remaining behavior:

```
RED:   Write next test → fails
GREEN: Minimal code to pass → passes
```

Rules:

- One test at a time
- Only enough code to pass current test
- Don't anticipate future tests
- Keep tests focused on observable behavior

### 4. Refactor

After all tests pass, read [references/refactoring.md](references/refactoring.md) and look for refactor candidates:

- [ ] Extract duplication
- [ ] Deepen modules (move complexity behind simple interfaces)
- [ ] Apply SOLID principles where natural
- [ ] Consider what new code reveals about existing code
- [ ] Run tests after each refactor step

**Never refactor while RED.** Get to GREEN first.

## Checklist Per Cycle

```
[ ] Test describes behavior, not implementation
[ ] Test uses public interface only
[ ] Test would survive internal refactor
[ ] Code is minimal for this test
[ ] No speculative features added
```

---

When using outside-in TDD, read [references/outside-in.md](references/outside-in.md) for the full double-loop workflow.
When deciding test file placement, read [references/test-tiers.md](references/test-tiers.md) for unit vs component tier rules.
When testing UI components, read [references/component-testing.md](references/component-testing.md) for mount helpers and boundary faking patterns.

## Validation

To validate changes to this skill, run the 4-stage process: discovery validation (test frontmatter triggers), logic validation (simulate execution), edge case testing (attack the logic), and architecture refinement (enforce progressive disclosure). See [skills best practices](https://github.com/mgechev/skills-best-practices) for prompts.
