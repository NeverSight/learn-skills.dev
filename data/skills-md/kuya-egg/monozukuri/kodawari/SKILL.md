---
name: kodawari
description: "Review software with careful attention to correctness, maintainability, security, operations, and meaningful detail. Use for diffs, branches, pull requests, architecture decisions, or final quality checks."
---

# Kodawari

Kodawari is careful attention to meaningful detail. In software, quality is
often carried by small choices: a truthful name, a preserved invariant, an
actionable error, a useful test, or a log that makes an incident diagnosable.
This is a Japanese-inspired engineering metaphor, not perfectionism for its
own sake.

## Use this skill when

- reviewing a diff, branch, pull request, or release candidate;
- checking an implementation against a specification;
- evaluating maintainability or an architectural decision;
- preparing a greenfield vertical slice for handoff; or
- a change “works” but its long-term quality is uncertain.

## Outcome

Produce a prioritized review with:

- actionable findings supported by file-level or behavior-level evidence;
- correctness, security, data, compatibility, performance, and operability
  risks considered;
- missing tests, error paths, documentation, or observability identified;
- optional style preferences separated from defects; and
- a clear approval boundary and residual risk.

## Workflow

### 1. Re-read the contract

State the requested behavior, non-goals, constraints, and verification
evidence. Compare the change with the actual task, not an imagined improvement.

### 2. Inspect the diff

Look for accidental edits, scope creep, dead code, duplicate logic, hidden
behavior changes, confusing names, unsafe defaults, and generated excess.
Trace changed code into callers, data, configuration, and deployment paths.

### 3. Review the quality axes

Check, as relevant:

- behavior and edge cases;
- authentication, authorization, input handling, secrets, and data exposure;
- API, schema, migration, and compatibility contracts;
- error handling, retries, idempotency, and failure containment;
- performance only where evidence or risk justifies it;
- tests that prove behavior and regressions;
- logs, metrics, traces, health, and recovery signals;
- documentation and decisions future maintainers must know; and
- rollback or removal paths.

### 4. Rank findings

Lead with defects that can cause incorrect behavior, data loss, security
impact, outage, incompatibility, or unmaintainable coupling. Explain the
condition, impact, evidence, and smallest useful fix. Do not bury a blocking
finding beneath a list of preferences.

### 5. Reconcile standards and intent

Use repository conventions and the task's contract as the authority. Do not
reject a clear, safe solution because it differs from personal taste. Do not
approve known risk merely because it existed before the change.

## Evidence standard

Every finding must point to a concrete line, path, behavior, test, or
unverified assumption. Say what was checked and what could not be checked.
Verification claims must be traceable to an executed command, observed result,
or authoritative evidence.

## Boundaries

- Do not rewrite the implementation while reviewing it.
- Do not report style preferences as correctness defects.
- Do not approve based only on compilation or a happy-path test.
- Do not demand speculative abstractions, documentation, or scale.
- Do not hide a blocker to keep the review pleasant.

## Handoff

End with findings ordered by impact, checks performed, missing evidence, and
the minimum changes needed for confidence. Use `andon` for operational gaps,
`poka-yoke` for missing prevention, `kaizen` for safe cleanup, or `shukka`
when the reviewed change is a release candidate.

If a referenced skill is not installed, apply its named lens inline instead of
trying to invoke it.
