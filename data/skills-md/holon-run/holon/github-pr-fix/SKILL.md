---
name: github-pr-fix
description: "Fix pull requests based on review feedback and CI failures, then publish review replies."
---

# GitHub PR Fix Skill

`github-pr-fix` focuses on remediation: diagnose PR problems, apply fixes, push commits, and publish review replies.

## Prerequisites

- `gh` CLI authentication is required.
- Prefer `ghx` for context collection and publish operations.
- `GITHUB_TOKEN`/`GH_TOKEN` must allow PR read-write operations.

## Runtime Paths

- `GITHUB_OUTPUT_DIR`: output artifacts directory (caller-provided preferred; otherwise temp dir).
- `GITHUB_CONTEXT_DIR`: context directory (default `${GITHUB_OUTPUT_DIR}/github-context`).

## Inputs (Manifest-First)

Required input:
- `${GITHUB_CONTEXT_DIR}/manifest.json` from `ghx context collect`.

Optional inputs:
- Any artifact listed as `status=present` in `manifest.artifacts[]`.

Do not assume fixed `github/*.json` files.  
Resolve available context through artifact metadata (`id`, `path`, `status`, `description`).

## Workflow

### 1. Collect context

Preferred:
- `skills/ghx/scripts/ghx.sh context collect <pr_ref>`

Fallback:
- Direct `gh` collection only when `ghx` is unavailable; still produce equivalent manifest contract.

### 2. Diagnose and prioritize

Prioritize in this order:
1. Build/compile failures
2. Failing tests and runtime regressions
3. Type/import/module errors
4. Lint/style issues
5. Non-blocking refactor suggestions

Use existing review threads/comments to avoid duplicate or stale responses.

### 3. Implement fixes

- Apply minimal targeted fixes for blocking issues first.
- Run relevant verification commands.
- Commit and push before posting review replies.

### 4. Publish review replies

Preferred:
- Use `ghx` publish capabilities for reply workflows.

Fallback:
- Use direct `gh api` reply operations only if `ghx` publish path is unavailable.

### 5. Finalize outputs

Required outputs under `${GITHUB_OUTPUT_DIR}`:
- `summary.md`
- `manifest.json`
- `publish-results.json`

## Remediation Standards

- Do not mark issues fixed without verification evidence.
- If verification is partial, state exact limits and risk.
- Defer non-blocking large refactors with explicit rationale.
- Keep review replies concrete: what changed, where, and any remaining risk.

## Output Contract

### `summary.md`

Must include:
- PR reference and diagnosis summary
- fixes applied
- verification commands and outcomes
- reply publish result summary
- deferred/follow-up items

### `manifest.json`

Execution metadata for this skill, including:
- `provider: "github-pr-fix"`
- PR reference
- fix/reply counters
- `status` (`completed|partial|failed`)

### `publish-results.json`

Publish execution record from `ghx` or equivalent fallback format.

## Completion Criteria

A successful run requires all of the following:
1. Blocking fixes are committed and pushed to the PR branch.
2. `publish-results.json` exists.
3. Reply publish contains no failed required reply action.

If replies are planned but not published, the run is not successful.

## Notes

- This skill defines diagnosis/remediation/reply behavior.
- `ghx` defines context artifact semantics and publish command surfaces.
