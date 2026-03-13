---
name: code-review
description: Perform comprehensive software code reviews focused on correctness, regressions, security, reliability, performance, and test quality. Use when asked to review pull requests, commits, branches, patches, or source files and deliver prioritized findings with severity, concrete impact, and file/line references.
---

# Code Review

## Overview

Execute a rigorous, risk-first code review workflow and produce actionable findings.
Prioritize bugs and behavior regressions over style preferences.

## Required Inputs

- Review target: PR, commit range, branch diff, or specific files
- Project context: language/framework, runtime, and critical flows (if known)
- Scope constraints: full review or focused areas (security, performance, API, tests)

If context is missing, infer from repository and changed files, then state assumptions.

## Workflow

1. Define review boundaries.
2. Build a risk map from touched components and data flows.
3. Inspect code paths for correctness and regression risks.
4. Validate non-functional risks (security, reliability, performance).
5. Evaluate tests and observability coverage.
6. Report findings ordered by severity.

## Step 1: Define Review Boundaries

- Read the diff first, then open surrounding code for context.
- Distinguish change types: feature, bugfix, refactor, migration, dependency bump, config-only.
- Identify high-impact zones: auth, payments, data persistence, concurrency, caching, error handling, external integrations.

## Step 2: Build a Risk Map

- Trace entry points to side effects:
  - API request -> validation -> business logic -> DB/queue/cache updates
  - Background job/scheduler -> idempotency/locking/retry paths
  - UI event -> API calls -> state transitions -> user-visible behavior
- Flag unsafe changes early:
  - Contract changes without versioning or migration path
  - Data model changes without backfill/migration rollback plan
  - Removed guards or authorization checks

## Step 3: Inspect for Defects and Regressions

Use [references/review-checklist.md](references/review-checklist.md) for a complete checklist.

Focus on:
- Logic errors and broken invariants
- Off-by-one or boundary mistakes
- Incorrect null/empty/error handling
- Race conditions, deadlocks, and ordering issues
- Inconsistent read/write behavior and transaction boundaries
- Backward compatibility and API/schema mismatches

Use [references/language-risk-cues.md](references/language-risk-cues.md) for language-specific bug patterns.

## Step 4: Validate Security, Reliability, and Performance

- Security:
  - AuthN/AuthZ enforced on all protected paths
  - Input validation and output encoding are preserved
  - Secrets and sensitive data are not exposed in logs/errors
- Reliability:
  - Retries are bounded and idempotent
  - Timeouts/circuit breakers are set for network calls
  - Failure paths avoid partial writes and silent corruption
- Performance:
  - Query counts, complexity, and N+1 risks are understood
  - Unbounded loops, allocations, or payload growth are avoided
  - Caching invalidation behavior remains correct

## Step 5: Evaluate Tests and Operability

- Verify tests cover changed behavior and critical failure modes.
- Confirm regressions are reproducible by tests where possible.
- Check logging, metrics, tracing, and alerting impact for changed code paths.
- Mark missing tests as findings when risk is material.

## Severity Model

- `P0`: Critical bug/security/data-loss risk; likely production incident.
- `P1`: High-impact correctness/reliability issue with significant user or business impact.
- `P2`: Medium-risk defect or regression risk; should be fixed before merge when practical.
- `P3`: Low-risk improvement, maintainability concern, or clarity gap.

If uncertain, prefer lower confidence rather than inflated severity.

## Output Contract

Report findings first, ordered by severity, with this structure:

1. `[Px]` concise title
2. Why this is a problem (impact and failure mode)
3. Evidence with file and line reference
4. Recommended fix direction

Then include:
- Open questions/assumptions
- Brief change summary
- Residual risks or testing gaps

If no material issues are found, explicitly say so and list residual risks/test gaps.

## Review Discipline

- Do not block on style-only issues unless explicitly requested.
- Do not invent missing context; state assumptions.
- Prefer concrete, reproducible reasoning over speculative criticism.
- Keep suggestions actionable and scoped to the reviewed change.
