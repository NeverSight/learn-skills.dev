---
name: implement
description: Implement requested behavior and verify the result. Use only when explicitly invoked, before and during implementation.
---

# Implement

- Implement the requested behavior.
- Preserve existing behavior outside the requested changes.
- Read and apply [$code](../code/SKILL.md).

## Before coding

- Read the affected code, its callers, and relevant tests.
- Identify existing contracts, conventions, and reusable capabilities.
- Determine what must change and what must remain true.
- Identify the source of truth for each piece of state.
- Resolve ambiguity that materially affects behavior or public contracts.
- Choose the smallest coherent change and how to verify it.
- Keep planning proportional to the task; proceed when the approach is clear.

## Tests

- Test observable behavior and meaningful failure cases.
- Use existing tests when they already cover the behavior.
- Add tests for new behavior and meaningful coverage gaps.
- Avoid tests coupled to internal structure or incidental call order.
- Investigate failures; change existing expectations only when the requested behavior or evidence shows they are incorrect.

## Verification

- Run the smallest set of checks that covers the affected behavior.
- Review the diff for unnecessary complexity and unintended changes.
- Distinguish verified outcomes from assumptions.

## Completion report

- Briefly describe the behavior delivered and how it was verified.
- State material limitations or tradeoffs.
- Omit file inventories, implementation walkthroughs, and design-pattern names.
