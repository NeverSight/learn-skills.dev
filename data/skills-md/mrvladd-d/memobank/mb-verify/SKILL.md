---
name: mb-verify
description: >
  Verify one TASK-* against acceptance criteria and record reproducible evidence.
---

# mb-verify — Verifier loop (acceptance → evidence → verdict)

- **What it does:** checks a completed task against acceptance criteria and records the result with evidence.
- **Use it when:** implementation is done and you want an explicit PASS, FAIL, or partial verdict.
- **Input:** `TASK_ID`, acceptance criteria sources, and the task protocol files.
- **Output:** `verification.md`, evidence artifacts, updated task state, and follow-up bugs when criteria fail.

## Goal
Independent-ish verification so we don’t “trust without verify”.

## Inputs
- `TASK_ID` (e.g. `TASK-123`)
- Links to acceptance criteria:
  - `.memory-bank/features/FT-*` and/or
  - `.memory-bank/requirements.md` (REQ IDs)
- Link to protocol plan: `.protocols/<TASK_ID>/plan.md`

## Preconditions
- Implementation is done and gates were run (or failures recorded).

## Required outputs
- Update (or create) `.protocols/<TASK_ID>/verification.md` using:
  - `./references/shared-protocols-verification-template.md`
- Store evidence in `.tasks/<TASK_ID>/`:
  - logs, screenshots, videos, reproduction steps

## Process

### 1) Prime only what you need
Read:
- `.protocols/<TASK_ID>/context.md`
- `.protocols/<TASK_ID>/plan.md`
- `.protocols/<TASK_ID>/progress.md`
- acceptance criteria source docs

### 2) Verify acceptance criteria
For each AC / REQ:
- run the smallest meaningful check
- prefer deterministic checks (tests/CLI) over “looks OK”
- record what you did and link the evidence

If the task changes UI or browser behavior:
- prefer Playwright / agent-browser / CDP-driven verification
- capture screenshots/videos/traces when useful
- store artifacts in `.tasks/<TASK_ID>/`
- do not use “I clicked around manually” as the main evidence when browser automation is available

### 3) Verdict
If anything fails:
- set `VERDICT: FAIL`
- create a bug doc in `.memory-bank/bugs/BUG-<short>.md`
- add a follow-up TASK in backlog (if needed)
- mark current task as `failed`
- block downstream dependents until the bug/follow-up is resolved

If all pass:
- `VERDICT: PASS`

### 4) Sync statuses
- Update RTM lifecycle in `.memory-bank/requirements.md` (if used)
- If the feature/epic doc tracks `lifecycle`, sync it there too
- Mark task done (or blocked) in `.memory-bank/tasks/backlog.md`

## Definition of done
- `verification.md` exists and is evidence-backed.
- PASS tasks have updated RTM/backlog.
- FAIL tasks have a bug doc and next steps.
