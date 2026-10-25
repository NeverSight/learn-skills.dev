---
name: kata
description: "Implement software through small, repeatable, integrated vertical slices with clear exit criteria and honest verification. Use when a design is understood and code needs to be built or changed."
---

# Kata

Kata is a repeatable form practiced until good judgment becomes reliable. In
software, use a small engineering routine: make one behavior real, verify it,
learn from it, and then extend it. This is a Japanese-inspired metaphor for
discipline, not a demand for ceremony.

## Use this skill when

- a requirement and design are sufficiently understood;
- implementing a greenfield vertical slice;
- adding a feature or changing existing behavior;
- translating a decision into reviewable code; or
- AI-generated output needs to be reduced to the smallest correct change.

If the problem is still ambiguous, use `nemawashi`. If the repository or
environment is unknown, use `genchi-genbutsu`. If the design is overbuilt, use
`kanso` first.

## Outcome

Produce a focused, integrated change that:

- implements one observable behavior or structural improvement;
- follows local repository conventions;
- has appropriate tests and failure handling;
- leaves no generated or speculative excess;
- has a clean, explainable diff; and
- includes verification evidence and known residual risk.

## Workflow

### 1. Define the slice

State the behavior, boundary, exit criterion, and files likely to change. Pick
the smallest vertical path that proves the design through real interfaces.
When several slices are queued, take the smallest ready one first and end each
at a verified checkpoint (`monozukuri-core/references/checkpoints.md`).

### 2. Read before editing

Inspect neighboring implementations, callers, types, schemas, tests, and
commands. Reuse existing behavior when it already solves the problem. Do not
invent a parallel convention because it is easier to generate.

### 3. Build the narrow path

Implement the smallest complete behavior. Keep responsibilities cohesive,
names explicit, and invalid states constrained. Add only dependencies and
configuration justified by the requirement.

### 4. Integrate early

Run a focused check as soon as the slice can execute. Expand the slice only
after the current behavior is understood and verified. Prefer several small
integrations to a large batch of partially finished work.

### 5. Review generated work

Read every changed line. Remove wrappers, comments, abstractions, branches,
and configuration that do not serve the slice. Compare the diff with the
original request and inspect adjacent failure paths. Do not reformat untouched
code or apply broad stylistic cleanup that obscures the behavior change.

### 6. Close the slice

Run the relevant tests, type checks, lint, build, migration, or smoke checks.
Record what ran, what passed, what could not run, and what risk remains.

## Evidence standard

Verification must match behavior and risk. A compile-only result does not prove
runtime behavior; a passing happy-path test does not prove failure handling.
Every verification claim must be traceable to an executed command, observed
result, or authoritative evidence. Never report a check as passed unless it was
actually run or directly observed.

## Boundaries

- Do not broaden a slice because an unrelated cleanup is nearby.
- Do not hide incomplete behavior behind a TODO when a smaller complete slice
  is possible.
- Do not call generated code production-ready without reading and verifying it.
- Do not preserve a bad pattern merely because it is old; change it when the
  current slice gives a safe, relevant seam.

## Handoff

End with the changed behavior, files, checks, and residual risk. Use
`poka-yoke` to strengthen tests and boundaries, `kodawari` to review the diff,
or `shukka` when the change is ready for release preparation.

If a referenced skill is not installed, apply its named lens inline instead of
trying to invoke it.
