---
name: writing-plans
description: Use when implementation needs meaningful sequencing, coordination, or a durable handoff beyond a straightforward local change.
---

# Write an Executable Plan

Use `applying-development-principles`. Inspect the code and the approved requirements.
A plan should resolve dependencies and make completion testable, not prewrite the
implementation or repeat the spec.

Include what the executor needs:

- Goal and a link to the canonical requirements.
- Ordered chunks of work, affected areas, and dependencies.
- Decisions or contracts that must be settled before those chunks can start.
- Acceptance checks and the relevant verification commands, where known.
- Concrete risks or open questions that affect execution.

Use exact paths and signatures where they are known and important. Label proposals
as proposals. Do not invent API details to make the plan appear complete, paste
full implementations, or duplicate shared constraints in every task.

Group work by coherent outcomes, not arbitrary minutes, files, or a required
test/edit/commit checklist. Small changes can use a few steps in chat. Save a
durable plan only when requested or useful for execution/handoff, following the
repository's location convention.

Check that the plan covers the current request without introducing extra work.
Use one canonical spec; the plan links to it.

When work is tracked in Linear, read
[the Linear workflow](../applying-development-principles/references/linear.md)
for specification, evidence, and implementation-plan placement.

If implementation is already authorized, continue through `executing-plans`.
If the user asked only for a plan, deliver the plan. Do not force a choice between
agent workflows or assume permission to implement.
