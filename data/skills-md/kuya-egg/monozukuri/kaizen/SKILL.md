---
name: kaizen
description: "Improve software continuously through small, safe, behavior-preserving changes that reduce maintenance cost. Use for refactoring, cleanup, technical debt, naming, duplication, dead code, or post-change polish."
---

# Kaizen

Kaizen is continuous improvement. In software, make the codebase a little
clearer, safer, or easier to change whenever a relevant opportunity can be
handled without hiding scope or risk. This is a Japanese-inspired engineering
metaphor, not permission for constant churn.

## Use this skill when

- refactoring an existing area;
- removing duplication, dead paths, or misleading names;
- improving a module while implementing adjacent behavior;
- reducing recurring maintenance cost;
- converting a lesson into a guardrail; or
- deciding whether cleanup belongs in the current change.

## Outcome

Produce a small improvement that:

- has a concrete maintenance, correctness, safety, or clarity benefit;
- preserves behavior unless behavior change is explicit;
- is easy to review and revert;
- has appropriate regression protection; and
- does not turn a focused task into a rewrite.

## Workflow

### 1. Name the waste

Identify the specific pain: misleading language, duplication, dead code,
unclear boundary, missing test, noisy diagnostic, fragile setup, repeated
manual step, or known defect. Explain why it matters now.

### 2. Establish a baseline

Run the narrowest relevant tests, build, type check, benchmark, or behavior
observation before changing structure. If no baseline exists, state the risk.

### 3. Make one small move

Rename, extract, delete, simplify, constrain, document, or automate one clear
improvement. Keep the change local and avoid mixing a behavior change with an
unrelated cleanup unless the cleanup is required for safety.

An adjacent improvement is allowed only when it is directly related to the
task, low risk, independently verifiable, smaller than the primary change,
and unlikely to complicate review or rollback. Otherwise record it as a
concrete follow-up.

### 4. Preserve and verify

Run the baseline checks and inspect the diff. Confirm that the improvement
reduced concepts or risk rather than merely moving complexity elsewhere.

### 5. Record the next step only when real

If more work is needed, record a concrete follow-up with a reason and boundary.
Do not create a vague technical-debt backlog as a substitute for judgment.

## Evidence standard

Show the before-and-after reason the change improves maintainability or safety.
For performance or reliability claims, measure or state that the claim is not
measured.

## Boundaries

- Do not refactor unrelated code because it is aesthetically unpleasant.
- Do not rewrite a stable module without a concrete problem and migration path.
- Do not change behavior silently under the label of cleanup.
- Do not add abstraction unless it removes more complexity than it creates.
- Do not use “leave it better” to bypass the user's scope.
- Do not reformat untouched code or apply broad lint fixes under the name of
  Kaizen.

## Handoff

Report the maintenance problem, improvement, behavior checks, and remaining
opportunities. Use `poka-yoke` for a new guardrail, `kodawari` for review, or
`hansei` when the improvement came from a failure or incident.

If a referenced skill is not installed, apply its named lens inline instead of
trying to invoke it.
