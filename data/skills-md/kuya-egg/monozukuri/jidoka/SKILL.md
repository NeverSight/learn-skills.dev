---
name: jidoka
description: "Debug software by making failures visible, reproducing them, finding contributing causes, and adding durable regression protection. Use for bugs, failing tests, incidents, regressions, flaky behavior, and unexplained production errors."
---

# Jidoka

Jidoka is the stop-the-line discipline: when a meaningful defect appears, make
it visible and understand it before allowing more work or releases to build on
it. It is a Japanese-inspired engineering metaphor for quality at the source,
not a promise that every minor imperfection stops all work forever.

## Use this skill when

- a test, build, type check, migration, or invariant fails;
- behavior is incorrect, flaky, slow, or unexplained;
- a regression or production incident needs diagnosis;
- an existing workaround hides a recurring problem; or
- a fix is tempting but the cause is not yet understood.

## Outcome

Produce a verified root-cause fix with:

- a tight reproduction or a clear explanation of why reproduction is blocked;
- observations separated from hypotheses;
- experiments that distinguish plausible causes;
- the contributing cause and why the system allowed it;
- the narrowest safe fix;
- regression protection or durable diagnostic evidence; and
- explicit results and residual risk.

## Workflow

### 1. Stop and frame

State the failure, impact, affected boundary, and current known-good or
known-bad evidence. Do not start with a broad refactor or a preferred theory.

### 2. Reproduce

Create one reliable command, test, fixture, request, or observation that fails
for the actual problem. If the failure is intermittent, capture the smallest
useful signal and improve the feedback loop before guessing.

### 3. Observe

Read the error, inputs, state transitions, logs, traces, timing, and related
code. Instrument only what distinguishes hypotheses. Treat symptoms as clues,
not causes.

### 4. Test hypotheses

List plausible causes and run the cheapest experiment that can eliminate one.
Change one relevant variable at a time. Stop using a hypothesis when evidence
contradicts it.

### 5. Find the contributing cause

Ask why the failure occurred and why existing tests, types, constraints,
observability, or review did not catch it. Use Five Whys when it exposes a
missing guardrail; do not use it to invent blame or a single simplistic cause.

### 6. Fix and protect

Make the smallest fix at the right boundary. Add a regression test, invariant,
diagnostic, or process guardrail that would fail if the problem returns.

### 7. Verify the stop is over

Rerun the reproduction, targeted checks, and broader checks appropriate to the
risk. Confirm that the fix does not mask an adjacent failure.

## Autonomous correction boundary

During the edit phase, fix compile errors, test failures, and minor defects
introduced by your own change when the intended behavior is clear. Stop for
human input only when requirements or architecture are ambiguous, a new
authorization is required, a destructive action is involved, or the evidence
reveals a conflict that cannot be resolved safely.

## Evidence standard

Do not claim root cause from a plausible code reading alone. Show the failing
case before the fix, the result after the fix, and the checks that cover the
changed boundary. Every verification claim must be traceable to an executed
command, observed result, or authoritative evidence.

## Boundaries

- Do not suppress a failing check to restore green status.
- Do not patch only the symptom when the cause is observable.
- Do not perform unrelated cleanup while the feedback loop is broken.
- Do not declare “cannot reproduce” without recording what was tried and what
  evidence is missing.
- Do not leave a known high-impact defect invisible because it was inherited.

## Handoff

Report the failure, cause, fix, regression protection, verification, and any
remaining uncertainty. Use `poka-yoke` for stronger prevention, `andon` for
diagnostics, or `hansei` when the failure reveals a process or system gap.

If a referenced skill is not installed, apply its named lens inline instead of
trying to invoke it.
