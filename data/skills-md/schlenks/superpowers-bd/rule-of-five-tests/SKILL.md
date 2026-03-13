---
name: rule-of-five-tests
description: Use when writing 50+ lines of test code, adding test suites, or before claiming test work complete - apply 5 focused passes (Draft, Coverage, Independence, Speed, Maintainability) to catch issues single-shot generation misses
---

# Rule of Five — Tests

Each pass has ONE job. Re-read the entire artifact through that lens. See `references/pass-order-rationale.md` for order rationale.

## Quick Start

**Create native tasks for 5 passes with sequential dependencies:**

```
TaskCreate: "Pass 1: Draft"
  description: "Shape and structure. Test organization mirrors source. All test cases exist."
  activeForm: "Drafting"

TaskCreate: "Pass 2: Coverage"
  description: "Significant code paths tested? Happy, error, boundary? Every public function covered?"
  activeForm: "Checking coverage"
  addBlockedBy: [draft-task-id]

TaskCreate: "Pass 3: Independence"
  description: "Each test runs alone? Shared state? Order dependence? Test coupling?"
  activeForm: "Checking independence"
  addBlockedBy: [coverage-task-id]

TaskCreate: "Pass 4: Speed"
  description: "Unnecessary waits? Heavy fixtures? Could mock I/O? Any test >1s unjustified?"
  activeForm: "Checking speed"
  addBlockedBy: [independence-task-id]

TaskCreate: "Pass 5: Maintainability"
  description: "Descriptive names? Clear intent? DRY helpers? A newcomer could add tests by following patterns?"
  activeForm: "Improving maintainability"
  addBlockedBy: [speed-task-id]
```

**ENFORCEMENT:**
- Each pass is blocked until the previous completes
- Cannot commit until all 5 tasks show `status: completed`
- TaskList shows your progress through the passes
- Skipping passes is visible - blocked tasks can't be marked in_progress

For each pass: re-read the full artifact, evaluate through that lens only, make changes, then mark task complete.

## Detection Triggers

Invoke when: >50 lines of test code written/modified, new test suites, comprehensive test refactoring, or about to claim test work "done".

For code, use `rule-of-five-code`. For plans/design docs, use `rule-of-five-plans`.

Skip for: Single test additions, trivial test fixes, changes under 20 lines.

Announce: "Applying rule-of-five-tests to [artifact]. Starting 5-pass review."

## The 5 Passes

| Pass | Focus | Exit when... |
|------|-------|--------------|
| **Draft** | Shape and structure. Test organization mirrors source. All test cases exist. | All test cases exist; structure follows source |
| **Coverage** | Significant code paths tested? Happy, error, boundary? | Every public function tested; error paths covered |
| **Independence** | Each test runs alone? Shared state? Order dependence? | Each test passes individually; no coupling |
| **Speed** | Unnecessary waits? Heavy fixtures? Could mock I/O? | No test >1s unjustified; no unnecessary I/O |
| **Maintainability** | Descriptive names? Clear intent? DRY helpers? | A newcomer could add tests by following patterns |

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Multiple lenses in one pass | ONE lens per pass. Coverage pass ignores naming. |
| Checking for code bugs in tests | Tests don't have "bugs" in the traditional sense — check coverage and independence instead. |
| Skipping Independence pass | Shared state is the #1 cause of flaky tests. Always check. |
| Testing implementation details | Test behavior, not internal state. Mock at boundaries, not everywhere. |
| Speed pass removes useful tests | Speed pass optimizes execution, not coverage. Never remove tests to go faster. |
| Not running tests after each pass | Run the test suite after each pass to catch regressions in test code itself. |

## Reference Files

- `references/pass-definitions.md`: Detailed pass definitions with checklists
- `references/pass-order-rationale.md`: Why this order for tests

<!-- compressed: 2026-02-11, original: 510 words, compressed: 510 words -->
