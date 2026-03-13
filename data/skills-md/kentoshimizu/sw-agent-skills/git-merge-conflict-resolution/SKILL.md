---
name: git-merge-conflict-resolution
description: "Resolve Git merge/rebase conflicts with explicit intent tracking and post-resolution verification. Use when conflicts occur and intent-preserving resolution is required before integration; do not use for CI workflow design or application behavior implementation."
---

# Git Merge Conflict Resolution

## Overview
Use this skill to resolve conflicts without silently dropping behavior from either side.

## Scope Boundaries
- Use this skill when the task matches the trigger condition described in `description`.
- Do not use this skill when the primary task falls outside this skill's domain.

## Shared References
- Semantic conflict triage:
  - `references/semantic-conflict-triage.md`

## Templates And Assets
- Resolution log template:
  - `assets/conflict-resolution-log-template.md`
- Verification checklist:
  - `assets/conflict-verification-checklist.md`

## Inputs To Gather
- Conflicted files and conflict types.
- Intent of each conflicting change set.
- Required tests and high-risk behavioral paths.
- Domain-owner contacts for ambiguous semantic conflicts.

## Deliverables
- Conflict resolution decisions with rationale.
- File-level intent mapping for resolved hunks.
- Verification evidence for resolved behavior.

## Workflow
1. Classify conflicts by behavioral impact and risk.
2. Resolve textual conflicts while preserving intent from both sides.
3. Log rationale in `assets/conflict-resolution-log-template.md`.
4. Validate with `assets/conflict-verification-checklist.md`.
5. Escalate unresolved semantic ambiguity using `references/semantic-conflict-triage.md`.

## Quality Standard
- Every resolved hunk has explicit intent rationale.
- No conflict markers remain.
- Affected behaviors are re-verified by tests/manual checks.
- High-risk semantic merges receive domain-owner review.

## Failure Conditions
- Stop when change intent cannot be reconstructed confidently.
- Stop when semantic correctness cannot be verified post-resolution.
- Escalate when domain arbitration is needed for ambiguous merges.
