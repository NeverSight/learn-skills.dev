---
name: github-review
description: "Automated PR code review skill. Collects context through ghx, performs standards-based analysis, and publishes one structured review with optional inline comments."
---

# GitHub Review Skill

`github-review` focuses on review quality and publishing rules.  
Context acquisition details are owned by `ghx`.

## Prerequisites

- `gh` CLI authentication is required.
- Prefer `ghx` for context and publish operations.
- `GITHUB_TOKEN`/`GH_TOKEN` needs permissions to read PR data and publish reviews/comments.

## Runtime Paths

- `GITHUB_OUTPUT_DIR`: output artifacts directory (caller-provided preferred; otherwise temp dir).
- `GITHUB_CONTEXT_DIR`: context directory (default `${GITHUB_OUTPUT_DIR}/github-context`).

## Inputs (Manifest-First)

Required input:
- `${GITHUB_CONTEXT_DIR}/manifest.json` from `ghx context collect`.

Optional inputs:
- Any context artifact listed as `status=present` in `manifest.json`.

This skill must not assume fixed context filenames.  
Use `manifest.artifacts[]` (`id`, `path`, `status`, `description`) to determine available context.

## Workflow

### 1. Collect context

Preferred:
- `skills/ghx/scripts/ghx.sh context collect <pr_ref>`

Fallback:
- Direct `gh` commands only if `ghx` is unavailable; still produce equivalent manifest contract.

### 2. Perform review

Generate:
- `${GITHUB_OUTPUT_DIR}/review.md`
- `${GITHUB_OUTPUT_DIR}/review.json`
- `${GITHUB_OUTPUT_DIR}/summary.md`
- Optional `${GITHUB_OUTPUT_DIR}/manifest.json` (execution metadata)

### 3. Publish review

Preferred:
- `skills/ghx/scripts/ghx.sh review publish --pr=<owner/repo#num> --body-file=review.md --comments-file=review.json`

Fallback:
- Direct GitHub API only when primary publish clearly failed.

## Review Standards

### Scope and priority

Review focus order:
1. Correctness bugs
2. Security/safety issues
3. Performance/scalability risks
4. API compatibility and error handling
5. High-impact maintainability issues

### Incremental-first

- Prioritize newly introduced changes (new commits and new diff hunks).
- Expand scope only when needed to validate correctness or safety.

### Historical deduplication

- Check existing review threads/comments before raising findings.
- Do not repeat already-raised issues unless there is new evidence or changed impact.
- If re-raising, explain the delta briefly.

### Keep signal high

- Avoid low-value style nitpicks unless they affect behavior/maintainability.
- Keep feedback concise, specific, and actionable.
- Prefer fewer high-impact findings over exhaustive noise.

## Output Contract

### `review.md`

Human-readable review summary containing:
- conclusion-first summary
- key findings ordered by severity
- actionable recommendations

### `review.json`

Structured inline findings:

```json
[
  {
    "path": "path/to/file.go",
    "line": 42,
    "severity": "error|warn|nit",
    "message": "Issue description",
    "suggestion": "Optional concrete fix"
  }
]
```

Severity semantics:
- `error`: must-fix before merge
- `warn`: should-fix
- `nit`: optional improvement

### `summary.md`

Short execution summary:
- reviewed ref/head
- context coverage summary from manifest
- number of findings and publish outcome
- explicit degradation/failure reason when context is insufficient

## Degradation Rules

- If core review artifacts are missing (for example `pr_metadata`, `diff` and `files` both unavailable), do not fabricate certainty.
- Either:
  - produce summary-only review with explicit limitations and no inline comments, or
  - fail with clear reason in `summary.md`.

## Publishing Guardrails

- Publish at most one review per execution round.
- A successful primary publish is terminal; do not run alternate publish paths.
- Before fallback publish, check whether an equivalent Holon review already exists for the same head SHA and skip if present.

## Configuration

- `DRY_RUN=true`: preview only.
- `MAX_INLINE=N`: cap inline comments.
- `POST_EMPTY=true`: allow posting empty review.

## Notes

- `github-review` defines review standards and output expectations.
- `ghx` defines context collection structure and artifact semantics.
