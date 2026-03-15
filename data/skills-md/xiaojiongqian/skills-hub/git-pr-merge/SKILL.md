---
name: git-pr-merge
description: >
  Review, validate, and merge a GitHub pull request into a target branch with
  `gh` and `git`. Use when the user asks to merge a PR end-to-end, optionally
  delete the source branch, and optionally use a temporary worktree. Run
  autonomous review first; if blocking issues, unresolved conflicts, failed
  checks, or insufficient docs/tests are found, comment on the PR and stop
  instead of merging.
version: 1.3.0
license: MIT
metadata:
  short-description: Review and merge a GitHub PR safely
---

# Git PR Merge

## Overview

End-to-end pull request merge workflow: review the diff for quality, security, and docs/tests coverage, validate locally on disposable branches or worktrees, finalize with `gh pr merge` when safe, and clean up. Default target is the PR base branch. `dev` may proceed autonomously; `main` requires human confirmation before the final merge.

Prefer Claude as the host when available. Medium and large PRs benefit from Claude's internal review and simplification helpers; other agents should fall back to the bundled sub-agent prompts in this skill.

## Quick start

```text
Merge PR #123
Merge PR #456 with squash and delete the source branch
Review PR #789 targeting main; merge only after I confirm
```

## Inputs

- `pr`: required. PR number, `#123`, or full PR URL.
- `target_branch`: optional. Default the PR `baseRefName` from `gh pr view`. If provided and different from `baseRefName`, treat it as a non-standard target override; review and commenting may proceed, but do not autonomously merge unless a human explicitly confirms the alternate integration flow.
- `merge_strategy`: optional. `merge` | `squash` | `rebase`. Default `merge`.
- `delete_branch`: optional. Default `false`. Applies only when the GitHub merge succeeds and the source branch is not protected.
- `use_worktree`: optional. Default `false`.

## Operating model

- Execute the full flow autonomously once the user requests a merge, except for protected-branch confirmation gates.
- Use `gh pr merge` for the final standard merge so GitHub remains the source of truth for branch protection, merge queues, and merge state.
- Do not pause for routine confirmations during fetch, review, validation, cleanup, or PR comments.
- Stop only when a required input is missing, access is unavailable, a blocking issue is found, or a human confirmation gate is required.
- Never force-push or manually rewrite target-branch history.
- Never delete protected branches such as `main`, `master`, `dev`, or `develop`.
- If the merge flow fails after review has started, leave a traceable PR comment and stop cleanly.
- If the host is non-interactive and the target branch requires human confirmation, stop after review/comment and do not merge.

## Preconditions

1. Confirm repo scope and remotes:
   - `pwd`
   - `git rev-parse --show-toplevel`
   - `git remote -v`
2. Verify GitHub CLI access:
   - `gh auth status`
3. Resolve the PR and capture metadata:
   - `gh pr view <pr> --json number,title,state,isDraft,headRefName,headRefOid,baseRefName,author,mergeable,commits,additions,deletions,body,url`
   - `gh pr checks <pr>`
   - `gh pr diff <pr>`
4. Determine the target branch:
   - If the user specified `target_branch`, use it.
   - Otherwise default to `baseRefName`.
   - If `target_branch != baseRefName`, record that the run is in non-standard target-override mode.
5. Apply target-branch policy:
   - If the target branch is `dev`, continue autonomously after review and validation.
   - If the target branch is `main`, require explicit human confirmation immediately before the final merge.
   - If the target branch is something else and the repo norm is unclear, prefer review/comment only instead of guessing.

Do not continue if the PR is closed, already merged, inaccessible, or still in draft state.

## Review workflow

### Review mode

Choose review depth from total changed lines (`additions + deletions`):

- Small: `< 100`
- Medium: `100-500`
- Large: `> 500`

Always perform:

- code quality review
- security review
- docs and tests completeness review
- impact and regression review

If the host agent supports deeper review helpers or subagents, use them for medium and large PRs. If not, perform the review manually.

### Sub-agent delegation

For medium and large PRs, use sub-agents when available:

- **Code review sub-agent**: Performs the detailed code quality, security, impact, and docs/tests review. Invoke after capturing the PR diff and metadata.
  - Claude: use the `code-reviewer` skill (or the Agent tool with a review prompt).
  - Other agents: use the bundled prompt at `<path-to-skill>/agents/code-reviewer.md` to spawn a sub-agent. Pass the PR diff and metadata as input.
- **Code simplifier sub-agent**: Optional, non-blocking follow-up for duplication, dead code, and unnecessary complexity. Use only after the merge decision is already made, or after a review-only run when the user wants cleanup suggestions.
  - Claude: use the `simplify` skill (or the Agent tool with a simplification prompt).
  - Other agents: use the bundled prompt at `<path-to-skill>/agents/code-simplifier.md` to spawn a sub-agent. Pass the list of changed files and their post-merge content.

For small PRs, sub-agent delegation is optional — inline review is sufficient.

### Required review checks

1. Read the diff and identify the changed modules.
2. Check for obvious bugs, unsafe behavior, sensitive data, and risky edge cases.
3. Check whether docs and tests are adequate for the size and type of change.
4. Distinguish issues introduced by this PR from historical issues that already existed.

### Docs and tests policy

Use three modes:

- Strict mode:
  - for large PRs or obvious feature additions
  - require meaningful design or requirement documentation, either in changed docs, a sufficiently detailed PR body, or linked external docs
  - require tests for new public behavior
- Update mode:
  - for medium PRs
  - require doc/test updates when public behavior, interfaces, or contracts changed
- Consistency mode:
  - for small PRs
  - verify that existing docs and tests still match the new behavior

If docs or tests are clearly insufficient for the chosen mode, do not merge.

### Historical issues

If review finds problems that are clearly outside the PR diff and not introduced by this PR:

- do not block the merge for those issues alone
- optionally create a GitHub issue to track the historical debt
- note it in the PR summary comment

## PR comment discipline

Before posting any PR comment:

1. Inspect recent PR comments from the current actor:
   - `gh api repos/<owner>/<repo>/issues/<pr>/comments?per_page=10`
2. Only post a new comment when there is materially new information, for example:
   - final merge completed
   - blocker set changed
   - mergeability or conflict status changed
   - validation outcome changed
   - PR head SHA changed
   - the previous run had no traceable comment and this run does
3. If the latest merge comment from this workflow already states the same outcome and same actionable blocker set, do not add another comment.

Comment content rules:

- Always include `Execution harness: <claude|codex>` near the top. Use the current host agent identity.
- Keep comments concise and high-signal. Prefer a one-line summary plus only the sections needed to act.
- Do not restate obvious PR context that GitHub already shows on the same page, such as PR title or source/target branches, unless branch targeting itself is the issue.
- Do not dump long command lists or repeat passing checks unless they are directly relevant to the decision.
- Omit any section whose only content would be filler or repeated background.

### Blocking issues

If review finds blocking issues, do all of the following:

1. Add a PR review comment describing:
   - the blocking problem
   - affected files or lines
   - concrete fixes needed
2. If the current user has permission and the repo workflow uses draft PRs, mark the PR back to draft:
   - `gh pr ready <pr> --undo`
   - Skip this step if the current user is not the PR author and does not have maintainer access.
3. Stop without merging.

Use a comment shape like:

```text
## PR merge blocked

**Execution harness**: <claude|codex>
**Summary**: <one-line blocker summary>
**Review mode**: <Small|Medium|Large> (<N> lines changed)

### Blocking issues
- Prefer a short bullet list for 1-2 blockers.
- Use a table only when there are several blockers and the structure adds clarity.

### Next actions
1. specific fix instruction
2. ...
```

## Workspace preparation

Before switching branches:

1. Record the current branch:
   - `git rev-parse --abbrev-ref HEAD`
2. Check for local modifications:
   - `git status --porcelain`
3. If dirty, stash automatically:
   - `git stash push -m "pr-merge-<pr>-auto-stash"`

Restore the stash at the end if one was created.

## Target branch setup

### Default mode

Operate in the current worktree:

```bash
git fetch origin
git checkout <target_branch>
git pull --ff-only origin <target_branch>
```

### Worktree mode

If `use_worktree=true`, use a temporary worktree to avoid disturbing the current checkout:

```bash
temp_dir="/tmp/git-pr-merge-<pr>-$(date +%s)"
git fetch origin
git worktree add "$temp_dir" origin/<target_branch>
cd "$temp_dir"
```

If worktree creation fails, either recover cleanly or fall back to default mode only when it is safe to do so.

## Merge preparation

1. Check out the PR branch locally:
   - `gh pr checkout <pr>`
   - record `source_branch` from `headRefName`
2. Create a disposable validation branch:
   - for `merge` or `squash`:
     - `git checkout -B pr-merge-<pr>-validate origin/<target_branch>`
   - for `rebase`:
     - `git checkout -B pr-merge-<pr>-rebase <source_branch>`
3. Dry-run the integration without publishing it:
   - `merge`: `git merge --no-commit --no-ff <source_branch>`
   - `squash`: use the same local dry-run merge for conflict and regression detection: `git merge --no-commit --no-ff <source_branch>`
   - `rebase`: `git rebase origin/<target_branch>`
4. Run validation only on the disposable branch. Never rebase or merge directly on the real target branch during validation.

If the dry-run setup succeeds, continue to validation.

## Conflict handling

Automatically resolve only conflicts that are clearly mechanical:

- import ordering or duplicated import blocks
- formatting-only and comment-only conflicts
- lockfile or dependency-manifest additions when both sides can be combined mechanically
- simple config-list merges where both entries can safely coexist

For each resolved conflict, record the file, the resolution strategy, and a brief rationale so it can be included in the post-merge comment.

Do not auto-resolve:

- logic or control-flow conflicts
- deletion-vs-modification conflicts
- schema or API contract conflicts
- ambiguous product-behavior conflicts

If a non-mechanical conflict appears:

1. Abort the in-progress validation state:
   - `git merge --abort` or `git rebase --abort`
2. Add a PR review comment listing each unresolved conflict with file paths and a description of why it cannot be auto-resolved.
3. If the current user has permission, mark the PR back to draft:
   - `gh pr ready <pr> --undo`
4. Stop without merging.

## Validation before merge

Run the smallest sufficient validation based on changed modules and repo tooling.

Preferred order:

1. lint or static checks
2. type checks
3. unit or integration tests for affected modules

Detect commands from the project when possible:

- Node: `npm run lint`, `npm run typecheck`, `npm test`, `npm run test:unit`
- Python: `ruff check .` or `flake8`, `mypy`, `pytest`
- Go: `go vet ./...`, `go test ./...`
- Rust: `cargo clippy`, `cargo test`

For monorepos or multi-package projects, prefer running checks only for affected packages or workspaces rather than the entire project. Look for workspace-level scripts (e.g., `nx affected`, `turbo run test --filter=...`, `pnpm --filter`).

If checks fail:

1. capture the failing command and error
2. comment on the PR with the failure summary
3. abort the validation state safely:
   - `git merge --abort` if merge validation is active
   - `git rebase --abort` if rebase validation is active
4. clean up the disposable validation branch or worktree state
5. if the current user has permission, mark the PR back to draft
6. stop without merging

## Finalize merge

Only execute the final merge when all of the following are true:

- review passed
- validation passed
- `target_branch == baseRefName`
- the target-branch policy allows a merge
- the PR head still matches the captured `headRefOid`

If the target branch is `main`:

- ask for explicit human confirmation immediately before running the final merge command
- if the host is non-interactive, skip the merge and leave a review-only summary comment instead

Use GitHub CLI to finalize the standard merge:

- `merge`:
  - `gh pr merge <pr> --merge --match-head-commit <head_sha>`
- `squash`:
  - `gh pr merge <pr> --squash --match-head-commit <head_sha>`
- `rebase`:
  - `gh pr merge <pr> --rebase --match-head-commit <head_sha>`

If `delete_branch=true` and the source branch is not protected, add `--delete-branch`.

This keeps GitHub merge state, merge queues, and branch protections authoritative.

If `target_branch != baseRefName`, do not run `gh pr merge`. Leave a summary comment with the review and validation outcome, state that the PR was not merged on GitHub, and require explicit human follow-up for the alternate target flow.

After the merge command, verify the result:

- `gh pr view <pr> --json state,merged,mergeCommit`
- `git fetch origin <target_branch>`
- `git log origin/<target_branch> -1`

## Post-merge PR comment

Add a summary comment to the PR conversation when the run produces a materially new outcome. The comment must be clear, concise, and information-dense — no filler, every line carries signal.

Use a comment shape like:

```text
## PR merge <result>

**Execution harness**: <claude|codex>
**Mode**: <standard-merge|review-only|target-override>
**Strategy**: <merge|squash|rebase>
**Merge commit**: `<sha>` (or "N/A" if not merged)
**Summary**: <one-line result>

### Review
- Include only if the review found a non-obvious issue or the verdict is not already clear from Summary.

### Validation
- Include only the smallest sufficient validation facts to justify the decision.

### Conflicts
- Include only if conflicts existed or conflict status is the reason for the outcome.

### Cleanup
- Include only if cleanup state matters for follow-up.

### Follow-up
- Include only if a human still needs to act.
```

Never omit the merge result, `Execution harness`, or the validation outcome that justifies the decision.

## Branch cleanup

Delete the source branch only when the GitHub merge succeeds, `delete_branch=true`, and the branch is not protected. Prefer `gh pr merge --delete-branch` over manual remote deletion so GitHub remains the source of truth.

Never delete `main`, `master`, `dev`, or `develop`.

## Cleanup

This skill is responsible for cleaning up resources it created during the merge flow. The source branch is not a resource created by this skill — its lifecycle is controlled by the `delete_branch` input, not by cleanup.

At the end:

- If a temporary worktree was created, always remove it:
  - `git worktree remove "$temp_dir"`
  - If removal fails (e.g., uncommitted files), force-remove with `git worktree remove --force "$temp_dir"` since the worktree is purely temporary and any useful state has already been pushed.
- Restore the original working directory.
- Switch back to the branch that was checked out before the merge flow started.
- Delete disposable validation branches such as `pr-merge-<pr>-validate` or `pr-merge-<pr>-rebase`.
- Pop the auto stash if one was created:
  - `git stash pop`

If stash pop fails due to conflicts, warn the user and leave the stash intact for manual resolution.

## Final report

Report:

- PR number and title
- source and target branches
- merge strategy used
- review result
- docs/tests assessment
- validation commands run
- merge result
- cleanup result
- any follow-up items

## Bundled resources

- `agents/openai.yaml` — OpenAI-compatible agent UI metadata
- `agents/code-reviewer.md` — Sub-agent prompt for code review (used by non-Claude agents)
- `agents/code-simplifier.md` — Optional, non-blocking prompt for post-merge or review-only simplification follow-up
