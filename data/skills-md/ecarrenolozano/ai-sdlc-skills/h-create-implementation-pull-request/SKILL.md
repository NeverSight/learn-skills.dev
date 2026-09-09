---
name: h-create-implementation-pull-request
description: Prepare and create GitHub pull requests for locally committed, validated implementation work after g-implement-repository-work. Use when Codex must inspect implementation commits, group implemented issues into a coherent PR, verify SDLC traceability and local status tracking, draft a PR title/body, require explicit approval before pushing or creating the PR, run gh pr create, report the PR URL, and avoid issue closure, project moves, labels, assignments, merges, or force pushes unless separately approved.
---

# Implementation Pull Request

## Purpose

Create a controlled review handoff after local implementation is complete. Inspect committed work, validate evidence, propose the PR, and perform remote PR creation only after explicit approval.

## Governing Rules

- Work in English.
- Use the exact skill identifier `h-create-implementation-pull-request`.
- Start only after implementation work is locally committed or the user explicitly asks for a PR proposal from local changes.
- Treat commits, `sdlc_docs/trace_workflow.md`, `sdlc_docs/03_implementation/backlog_priority.md`, code-level architecture docs, validation commands, and GitHub issues as authoritative inputs.
- Do not implement product code, rewrite implementation commits, or alter requirements or architecture decisions.
- Do not push, create a PR, comment on issues, close issues, move project cards, assign, label, merge, rebase, force-push, or delete branches without separate explicit approval.
- Avoid GitHub auto-close keywords such as `closes`, `fixes`, or `resolves` unless the user explicitly approves automatic issue closure on merge.
- Prefer one PR per coherent implementation batch. One story per PR is acceptable when independently reviewable; group stories only when they are tightly coupled, small, validated together, and share the same architecture slice.
- Keep skill/tooling changes separate from product implementation PRs unless the user explicitly approves a combined maintenance PR.
- Never claim a command passed unless it was executed and returned the reported result.

## Preconditions

Confirm all of the following before proposing a PR:

1. The repository root, current branch, base branch, and GitHub remote are identified.
2. Local implementation commits exist or local changes are intentionally being proposed.
3. Working tree status is known.
4. Implemented issues are identifiable from commits, local SDLC docs, or explicit user selection.
5. Relevant validation evidence is present or can be rerun.
6. No remote action has been performed in this run without approval.

Use `scripts/inspect_pr_readiness.py` before drafting the proposal.

## Inputs to Inspect

- `git status --short`
- `git branch --show-current`
- `git remote -v`
- commits since the selected base branch
- changed files since the selected base branch
- `sdlc_docs/trace_workflow.md`
- `sdlc_docs/03_implementation/backlog_priority.md` when present
- `sdlc_docs/02_architecture/code-level.md` and per-container code-level maps when implementation changed code
- GitHub issues referenced by commits or SDLC docs

Read `references/pr-policy.md` before deciding PR grouping or remote actions.

## PR Grouping

Classify the candidate PR as one of:

- **Single story PR:** one issue with focused implementation and validation.
- **Coherent batch PR:** multiple tightly related issues in the same architecture slice with shared validation evidence.
- **Maintenance PR:** skill, documentation workflow, tooling, or foundation-only changes.
- **Mixed PR:** product implementation plus skill/tooling/foundation changes. Avoid this unless explicitly approved and justified.

When multiple commits exist, present the grouping rationale and any alternative split before asking for approval.

## Approval Boundaries

### Approval 1: PR Proposal

Before any remote action, show:

- repository, current branch, base branch, and target remote;
- commits included;
- implemented issues and grouping rationale;
- changed-file summary;
- validation evidence and commands to rerun;
- local status-tracking evidence;
- proposed PR title and body;
- issue auto-close behavior, explicitly stating whether auto-close keywords are absent;
- remote actions requested.

Approval applies only to the visible proposal.

### Approval 2: Remote Push and PR Creation

After approval, perform only the approved remote actions:

- push the current branch to the selected remote;
- create the PR with the approved title/body/base/head;
- report the PR URL.

Stop afterward unless the user separately approves issue comments, project moves, labels, assignments, merge, or cleanup.

## Workflow

1. Locate the repository root.
2. Confirm PR creation mode or PR proposal-only mode.
3. Run `scripts/inspect_pr_readiness.py`.
4. Identify current branch, base branch, and remote.
5. Inspect commits and changed files since base.
6. Read local status-tracking docs and code-level architecture docs relevant to the changed files.
7. Identify implemented issues and whether they are locally marked implemented.
8. Inspect GitHub issue state when available, without mutating it.
9. Classify the PR grouping.
10. Run or verify validation commands needed for the included work.
11. Draft the PR title/body using `references/proposal-and-result-patterns.md`.
12. Present the PR proposal and stop for explicit approval.
13. Re-check Git status and branch after approval.
14. Push the current branch only if approved.
15. Create the PR only if approved.
16. Report the PR URL, included commits, validation evidence, and any remote actions skipped.
17. Stop before merge, issue closure, project moves, labels, assignment, or comments unless separately approved.

## Result Format

Use `references/proposal-and-result-patterns.md` for proposal and final result formats.

## References

- Read `references/pr-policy.md` before grouping issues or performing remote actions.
- Read `references/proposal-and-result-patterns.md` before presenting PR proposals or results.

## Scripts

- `scripts/inspect_pr_readiness.py`: inspect local Git, branch, commits, changed files, issue references, and SDLC tracking docs without modifying files or remotes.
- `scripts/run_regression_tests.py`: validate the skill policy, reference files, and readiness inspector.


## Progressive Audit Resources

- Read `references/golden-example/README.md` only when a progressive concrete example is useful.
- Read `references/process_flowchart.md` only for human explanation or audit.
