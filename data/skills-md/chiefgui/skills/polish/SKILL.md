---
name: polish
description: Improve existing code through deletion, simplification, and extensibility.
---

# Polish

- Preserve intended behavior.
- Delete before adding.
- Reduce complexity.
- Apply OCP by default.

## Relevant Skills

- Read and apply [$code](../code/SKILL.md).

## Coverage

- Review the entire requested scope against applicable skills.
- Trace root causes through callers and dependencies.
- Reassess after changes; continue until no concrete, justified improvements remain.

## Cleanup

- Remove dead code and unused dependencies.
- Remove redundant state and duplicated logic.
- Remove pass-through wrappers and unnecessary indirection.
- Remove obsolete compatibility paths.
- Fix root causes and remove their workarounds.
- Remove checks duplicated by enforced contracts.
- Remove inline comments.

## Tests

- Keep tests that catch real bugs.
- Delete tests that check the same thing.
- Test what the code does, not how it does it.
- Fix flaky tests.
- Add a test only when it catches a meaningful bug existing tests would miss.
- Investigate failures; never delete tests just to make checks pass.

## Verification

- Verify the behavior affected by the changes.
- Use the smallest set of existing checks that covers that behavior.

## Completion report

- Describe in plain language, focusing on value.
- Keep it brief.
- Use two sections:
  - Better: bullet list with benefits of the changes.
  - Worse: bullet list with drawbacks of the changes. "None identified" when applicable.
- Omit file inventories, implementation walkthroughs, and design-pattern names.
- Support claimed benefits with evidence.
