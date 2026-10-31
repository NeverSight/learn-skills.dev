---
name: tech-spec
description: Create or maintain a ticket-focused technical specification as a working document, with an editable commit checklist and a record of implementation and testing decisions. Use when a conversation or ticket needs to be turned into an actionable engineering spec.
---

# Technical Spec

Turn the current conversation, ticket context, and codebase understanding into a working technical specification. Do not interview the developer unless missing information prevents a responsible decision; otherwise record uncertainty explicitly and keep moving.

The spec follows one specific ticket or bounded change. It is not a product requirements document and must not contain user stories.

## Choose the destination

Inspect the applicable `AGENTS.md` files and equivalent repository instructions. If they define specific support for writing specs—such as a command, template, naming rule, or destination—use that support.

If no project-specific support exists, write the spec to `docs/specs/<id>.md`:

- Use the ticket identifier as `<id>` when one was provided, preserving the project's normal identifier form.
- Otherwise use a short, relevant kebab-case name derived from the change.

Do not require an issue tracker, label vocabulary, setup skill, or other skill to create the spec.

## Understand the change

Explore enough of the repository to describe the current behavior and a credible implementation approach. Use the project's domain vocabulary and respect relevant ADRs.

Identify the public seams through which the change will be exercised and tested. Prefer existing seams and keep new interfaces as few and as high-level as practical. Record unresolved questions instead of inventing requirements.

## Write and maintain the spec

Use this structure unless repository-specific support supplies a required template:

```markdown
# <Ticket or change title>

## Context

Why this ticket exists, the current behavior, and the concrete problem being addressed.

## Scope

The observable outcome and boundaries of this ticket.

## Commit Plan

- [ ] `<proposed commit subject>` — the coherent behavior or structural change delivered by this commit, including the verification needed for it.

## Decision Record

### Implementation Decisions

- The modules or components to build or modify.
- Public interfaces and seams that will change.
- Technical clarifications and architectural choices.
- Schema changes, API contracts, and important interactions.

### Testing Decisions

- The externally observable behavior to verify.
- The seams and modules covered by tests.
- Relevant testing precedent already present in the repository.

## Out of Scope

Explicit exclusions that keep the ticket bounded.

## Open Questions

Unknowns that could affect the plan or its decisions.

## Notes

Additional ticket-specific context that does not belong above.
```

Never add a user-stories section or rewrite requirements in “As a … I want …” form.

## Commit checklist rules

The commit plan is the operational center of the document:

- Make every checkbox a coherent, reviewable commit that leaves the repository in a valid state.
- Order commits by dependency and implementation flow.
- Describe outcomes, not a sequence of low-level editing steps.
- Include the relevant verification in each item rather than creating a detached testing phase.
- Avoid speculative commits outside the ticket's scope.
- Treat proposed commit subjects as editable guidance, not a promise that history must match word-for-word.

When work proceeds with `pair-tdd`, update the checklist as each vertical slice teaches the pair more: split, reorder, add, remove, or rewrite items when the implementation reveals a better plan. Check an item only when its behavior is implemented and its relevant tests pass. Keep the Decision Record synchronized with decisions made during those cycles.

## Decision record rules

Preserve durable decisions rather than transient implementation detail. Record the chosen approach and enough rationale to distinguish it from meaningful alternatives.

Do not include specific file paths or ordinary code snippets in the Decision Record because they become stale quickly. If a prototype produced a small state machine, schema, type shape, or similar artifact that captures a decision more precisely than prose, include only the decision-rich fragment and identify it as coming from the prototype.

Update an existing spec in place when it follows the same ticket. Preserve checked items and prior decisions; amend them visibly when reality changes instead of silently replacing the working history.
