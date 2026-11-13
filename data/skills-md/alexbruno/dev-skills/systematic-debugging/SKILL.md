---
name: systematic-debugging
description: >-
  Investigate bugs and failures through disciplined root-cause analysis before
  writing fixes. Use this skill when diagnosing failing tests, runtime errors,
  regressions, or unexpected behavior—before proposing or applying any code
  changes.
---

# Systematic Debugging

Find and prove the **root cause** before changing any production code. Never guess, apply shotgun patches, or silence errors to make symptoms disappear.

## Core Rule

**No fix without a confirmed root cause.** Every bug fix must follow: **Reproduce -> Isolate -> Prove Root Cause -> Regression Test -> Fix -> Verify**.

## Debugging Process

### 1. Reproduce Reliably

- Capture exact reproduction steps, inputs, environment conditions, and expected vs. actual behavior.
- If the failure cannot be reproduced yet, gather logs, traces, or state snapshots first—do not speculate.

### 2. Isolate & Form Hypotheses

- Narrow the failure boundary (recent changes via `git diff`/`git log`, failing inputs, or call paths via `codebase-indexing` if active).
- Form **one concrete, testable hypothesis** at a time about why the failure occurs.
- Test the hypothesis with targeted observation (logs, minimal reproduction, or debugger/test run).

### 3. Confirm & Document Root Cause

- Confirm the exact mechanism causing the bug with direct evidence.
- If `workflow/SPEC.md` is active for this bug fix, record the reproduction steps and confirmed root cause there before planning the fix.

### 4. Write a Failing Regression Test First

- Create an automated test (or reproducible check) that fails for the **exact** reason of the bug.
- Verify it fails before applying the fix so you know the test actually catches the regression.

### 5. Fix the Root Cause & Verify

- Apply the minimal, clean fix that addresses the root cause—not a workaround around the symptom.
- Run the regression test and the full relevant test suite to confirm no regressions were introduced.

## Anti-Patterns to Avoid

- **Shotgun debugging**: Changing multiple unrelated things at once hoping one works.
- **Symptom masking**: Catching and ignoring exceptions, adding arbitrary retries/sleeps, or loosening assertions to pass tests.
- **Speculative fixes**: Editing code before you can explain *why* it failed.
