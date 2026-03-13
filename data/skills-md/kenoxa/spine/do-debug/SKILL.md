---
name: do-debug
description: >
  Diagnose and fix bugs through structured 4-phase debugging.
  Use when facing failing tests, crashes, regressions, or unexpected behavior.
  Do NOT use when the problem is unclear scope or missing requirements — use /do-plan instead.
argument-hint: "[error, failing test, or symptom]"
---

Diagnose root cause and fix through four phases: observe → pattern → hypothesis → harden.

## Phases

### 1. Observe and Capture

- Reproduce deterministically. Capture exact error, steps, environment, and variance.
- Record what is known vs unknown before editing any code.

### 2. Pattern Analysis

- Compare failing path with a known-good reference (code, commit, or contract).
- Identify mismatches in assumptions, data shape, config, ordering, boundaries.
- Narrow to the smallest collision zone that explains the failure.

### 3. Hypothesis Testing

- One hypothesis at a time: `I expect X because Y proves Z`.
- Change one variable per test. Log: hypothesis, test, result, next move.
- Failed hypothesis → return to Observe/Orient, not forward. This is a loop.

### 4. Implement and Harden

- Apply the smallest fix that resolves the confirmed root cause.
- Harden to make the bug class impossible, not just fix the symptom:
  - Entry validation
  - Domain invariants
  - Environment guardrails
  - Regression test coverage
- Verification claims require current-run command evidence (E3).
- Semantic regression from the fix → re-enter Phase 1. Non-semantic failure (lint, format) → fix inline.

## Escalation into Root-Cause Chain

When root cause remains unclear after Phase 2, or the same failure pattern spans multiple modules:
chain "why" questions, each grounded in observed evidence. Stop when the cause is actionable.
Branching unknowns → return to Phase 1.

## Unsticking Patterns

- **Simplification cascade**: strip non-essential parts until failure is obvious.
- **Collision-zone narrowing**: reduce to smallest interacting component set that still fails.
- **Inversion check**: validate assumptions by forcing opposite conditions.
- **Boundary stress**: test near limits to expose hidden conditions.

## Escalation

- After 3 failed hypotheses: escalate with concrete evidence and attempted alternatives.
- Architectural uncertainty or repeated cross-module failures: re-enter planning (`/do-plan`) before broader changes.

## Anti-Patterns

- Skipping reproduction because the fix "seems obvious"
- Bundling speculative edits across multiple subsystems
- Suppressing errors to force green checks
- Stopping at symptom relief when the source trigger is unknown
- Claiming completion without current-run verification evidence
