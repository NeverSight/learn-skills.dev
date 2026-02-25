---
name: executing-plans-preflight
description: Use when starting implementation work or executing a plan to run preflight checks before superpowers:executing-plans. Trigger on plan execution kickoff, coding start, or implementation continuation.
license: MIT
metadata:
  author: shihyuho
  version: "1.0.0"
---

# Executing Plans Preflight

Run a preflight gate before implementation so `superpowers:executing-plans` starts only after policy checks pass.

## Overview

- Enforce a deterministic preflight gate before editing files or executing plan tasks.
- Execute gate policy in `references/preflight-gates.md` and stop on blocking failures.
- Read gate details from `references/gates/*.md` as directed by policy.

## Trigger Contract

Trigger this skill when the user asks to:

- implement a plan
- start coding
- refactor/fix/add features
- continue implementation after planning

Common trigger phrases:

- "start implementation"
- "implement this plan"
- "start coding"
- "開始實作"
- "執行計劃"

## Preflight Flow

Core model:

1. Read `references/preflight-gates.md`.
2. Evaluate gates in listed order.
3. For each gate, apply policy rules defined in `references/preflight-gates.md`.
4. Collect evidence and decision (`PASS`/`BLOCK`/`SKIP`).
5. If preflight decision is `BLOCK`, halt plan execution and propose concrete next actions.
6. Ask the user to confirm which suggested action to take.
7. Invoke `superpowers:executing-plans` only after preflight passes.

## Integration with superpowers:executing-plans

**REQUIRED SUB-SKILL ORDER**:

1. Invoke `executing-plans-preflight` first.
2. Complete preflight decision.
3. Invoke `superpowers:executing-plans` only after preflight passes.

**BLOCKING GATE**:

- Do NOT start Task 1 of `superpowers:executing-plans` when preflight decision is `BLOCK`.
- Report every blocking reason before asking user to resolve it.
- Provide suggested remediation actions (with commands when applicable), then require user confirmation for the chosen next step.

When user says "execute plan" or equivalent, run this skill as pre-step and report:

- executed gates
- skipped gates and why
- blocking reasons (if any)
- whether plan execution is allowed or blocked

If blocked, also report:

- suggested remediation actions
- recommended default action
- explicit user confirmation prompt for next step

## Guardrails

- **MUST** run preflight before any plan execution or code edits.
- **MUST** follow gate order and decision semantics in `references/preflight-gates.md`.
- **MUST** read each gate's detail file before evaluating it.
- **MUST** detect git context first and mark git-dependent gates as `SKIP` when not inside a git repository.
- **MUST** report evidence and decision for every evaluated gate.
- **MUST** explicitly gate `superpowers:executing-plans` on preflight result.
- **MUST** propose concrete remediation actions whenever preflight decision is `BLOCK`.
- **MUST** get user confirmation for the next action before resolving blockers.
- **MUST NOT** ignore any listed gate unless its `skip_if` condition is met.
- **MUST NOT** start Task 1 when policy returns blocking result.

## Verification

- Gate policy loaded from `references/preflight-gates.md`.
- Gate commands/checks executed and output interpreted.
- Preflight decision communicated clearly.
- Implementation starts only after preflight passes.
- `superpowers:executing-plans` is invoked only after preflight gate passes.

## References

- `references/preflight-gates.md` - Gate policy and decision semantics
- `references/gates/g1-branch-context.md` - G.1 gate implementation details
- `references/gates/g2-worktree-clean.md` - G.2 gate implementation details
- `references/gates/g3-remote-sync.md` - G.3 gate implementation details
