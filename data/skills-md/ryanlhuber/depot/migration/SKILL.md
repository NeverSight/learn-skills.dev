---
name: migration
description: "Plans and carries out a move between technical states, such as a framework, dependency, schema, API, or infrastructure change, in reversible steps with compatibility, data integrity, ordering, and rollback defined. Use when a system must change from one state to another. Not for ordinary feature delivery with no state change."
disable-model-invocation: true
---

# Migration

## Purpose
Move a system from its current state to a target state without breaking users, losing data, or leaving no way back.

## When to use
- Use when: a framework, dependency, schema, API, data store, or infrastructure must change from one state to another.
- Do not use when: the work is a normal feature or fix with no state change, or the target state is undefined (settle it first).

## Inputs
- Required: the current state, the target state, and the systems affected.
- Optional: compatibility constraints, deployment order, data volumes, rollback needs, and a window for the change.
- Assumptions: if the affected surfaces cannot be listed, the migration is not ready to start.

## Process
1. Inventory every affected surface: code, data, configuration, callers, and dependents.
2. Break the move into steps that are each small, verifiable, and independently reversible where possible. Prefer an overlap period (add the new, move over, remove the old) to a single cutover.
3. For each step, state the compatibility guarantee, the data-integrity risk, and where it must sit in the deployment order.
4. Define validation after each step and the rollback for it. Name any step that cannot be rolled back.
5. Implement or plan the steps, and record what must be cleaned up afterward.

## Rules and heuristics
- Required: never run a destructive or irreversible step (dropping data, deleting the old path, a live cutover) without explicit authorization and a verified rollback or backup.
- Required: a step with no rollback and unresolved risk is a blocker; report it rather than proceeding.
- Required: never report validation as run or passing unless it was. Prefer a dry run first.
- Recommended: avoid a big-bang cutover unless the reason is stated.

## Checks
- Every affected surface appears in a step.
- Every step has validation and a rollback, or is flagged as irreversible.
- Deployment order and data handling are stated.

## Output
Return: the step plan or implementation, the risk register, the validation plan, the rollback notes, and the cleanup list.

## Completion criteria
- Each step can be executed, checked, and, where possible, undone by someone who did not write the plan.
- Irreversible steps are named and gated on explicit authorization.
