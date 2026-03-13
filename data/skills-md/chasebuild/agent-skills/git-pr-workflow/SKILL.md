---
name: git-pr-workflow
description: Prepare and submit pull requests with clean history, passing checks, and review-ready context. Use when asked to open, prepare, or finalize a PR.
---

# Git PR Workflow

Prepare PRs that are easy to review, safe to merge, and fully validated.

## Required Sequence

1. Confirm branch intent and scope.
2. Ensure commits are atomic (`git-atomic-commit`) and messages are conventional (`git-conventional-commit`).
3. Run `git-run-checks` on latest branch state.
4. Rebase or merge mainline according to project policy.
5. Push branch and open PR with a concise summary, test evidence, and risk notes.

## PR Description Checklist

- Problem statement
- What changed and why
- Screenshots/logs when relevant
- Validation performed (commands + outcomes)
- Risks and rollback plan
- Follow-up tasks (if any)

Use `./scripts/pr-checklist.sh` to generate a markdown template.

## Review Readiness Rules

- No unrelated diffs.
- No failing or skipped mandatory checks.
- No unresolved TODOs that hide correctness risk.
- Commit history tells a coherent story.

## Boris-Inspired Operating Rules

- Keep implementation minimal and focused on stated goal.
- Use parallelism only for independent workstreams.
- Verify continuously and surface uncertainty explicitly.

## Claude Mapping (Optional)

- Map this workflow to `/pr-prepare` and `/pr-submit` commands when command files are supported.
- Hook pre-push to run the same check command used in `git-run-checks`.
