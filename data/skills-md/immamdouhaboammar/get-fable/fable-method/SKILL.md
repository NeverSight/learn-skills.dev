---
name: fable-method
description: A step-by-step problem-solving loop (classify the ask, define done, gather evidence, decide, act surgically, verify by observation, report outcome-first). Use when the user says "/fable-method", "use the fable method", or "approach this like Fable", or proactively when starting any multi-step task that no task-specific skill covers. Subcommands - plan (stop after the plan), audit (grade finished work against the loop), report (rewrite an answer outcome-first).
version: 1.0.0
pack: core
inputs:
  - task_description
requires:
  - codebase_access
  - domain_adapters
produces:
  - verified_solution
  - execution_evidence
gates:
  - fit_gate_passed
  - observation_verified
fallback: fable-execute
mutatesWorkspace: true
parallelSafe: false
neural_links:
  precursors:
    - get-fable
  continuations:
    - fable-judge
    - fable-verify
  lateral_peers:
    - fable-plan
    - fable-execute
  recovery: fable-recover
---

# The Fable Method

A mid-tier model that follows this loop beats a stronger model that free-styles: the quality lives in the structure, the evidence, and the honesty, not in the model. The loop is self-contained. Follow it literally.

## Purpose

Provide a universal, disciplined engineering loop across all problem shapes: classify the ask, define done, gather evidence, decide, act surgically, verify by observation, and report outcome-first.

## When to Use

- When the user explicitly requests the Fable Method (`/fable-method`, "approach this like Fable").
- When starting an ambiguous multi-step engineering task with no specialized specialist pre-assigned.
- When executing structured planning (`/fable-method plan <task>`).
- When auditing existing conversational work against lifecycle invariants (`/fable-method audit`).

## When NOT to Use

- Trivial one-line edits where the change is obvious and self-contained (execute directly).
- Purely autonomous background long-polling or test loops (use `fable-loop`).
- Multi-host installation and setup procedures (use `fable-release` or installer).

## Inputs

- `task_description`: The problem prompt, specification, or bug report.
- `domain_adapter`: Optional sector adapter (`references/domains/*`) for non-code domains.

## Expected Outputs

- `verified_solution`: Surgically implemented changes matching the specification.
- `execution_evidence`: Observable evidence proving the solution works as intended.

## Procedure

1. **Triviality Gate**: If the task is one file, under ~10 lines, with no new behavior and known edit, execute directly and confirm with one check.
2. **Fit Gate**: Determine where the answer lives: in reachable sources (run loop), in unknown external techniques (research first), or only in inference (flag low-confidence).
3. **Step 0 — Classify the Ask**:
   - Question / assessment: Report findings, change nothing.
   - Task: Implement and verify.
   - Plan-first: Produce plan and wait for approval if scope is ambiguous or actions are irreversible.
4. **Step 1 — Define Done**: Explicitly declare what completion looks like and how it will be verified.
5. **Step 2 — Gather Evidence**: Open sources, read relevant code, check authoritative docs before modifying state.
6. **Step 3 — Decide**: Formulate the minimal viable plan.
7. **Step 4 — Act Surgically**: Modify only the necessary lines with zero collateral drift.
8. **Step 5 — Verify by Observation**: Run the code, execute the test, observe the side effect.
9. **Step 6 — Report Outcome-First**: State the outcome in the first sentence.

## Decision Rules

- Plan-First Priority: If any irreversible action, destructive command, or ambiguous scope is present, plan-first supersedes task execution.
- Scope Gate: Do not touch files outside the bounded problem domain.
- Evidence Gate: A task is not done until fresh passing machine evidence is observed.

## Tool Policy

- Execute shell commands to run compilers, linters, and test runners.
- Use targeted file reading and editing tools.
- Consult domain adapters in `references/domains/` when handling non-coding tasks (marketing, ops, finance, devops).

## Evidence Requirements

- Direct terminal outputs from test runners or build tools.
- Line references to source code confirming bug mechanism and repair.

## Failure Handling

- If a step fails, diagnose the failure mechanism rather than blindly retrying the same operation.
- If two consecutive failures occur, immediately route to `fable-recover`.

## Completion Criteria

- All criteria defined in Step 1 ("Define Done") are satisfied.
- Fresh passing test evidence captured.
- Final report delivered outcome-first with zero fluff.
