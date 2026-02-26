---
name: gh-issue-to-pr
description: Implement GitHub issues end to end using GitHub CLI and git, from cloning a repository (and forking only when needed) to opening a pull request. Use when asked to pick up a specific issue from GitHub and deliver a ready-to-review PR with linked issue context, commits, validation notes, and a pre-PR quality pass via $code-review.
---

# GitHub Issue To PR

Execute a reliable issue-implementation workflow for repositories hosted on GitHub using `gh` and `git`.

## Required Inputs

- `owner/repo` (upstream repository)
- `issue_number`
- Local parent directory for clones

## Workflow

1. Verify environment and read issue context.
2. Clone the target repository and fork only when owner is not current user.
3. Create an issue-specific branch.
4. Implement changes and run relevant checks.
5. Commit local changes.
6. Run `$code-review` on the branch diff and address material findings.
7. Push branch to `origin`.
8. Open a PR with issue linkage.

## Step 1: Verify and Load Context

Run:

```bash
gh auth status
gh issue view <issue_number> --repo <owner/repo> --json number,title,body,labels,assignees,url
```

Parse acceptance criteria, constraints, and edge cases from the issue before coding.

## Step 2: Clone and Conditionally Fork

Detect current GitHub login and repository owner:

```bash
gh auth status
gh api user -q .login
```

If `<owner>` from `<owner/repo>` is equal to current login:

```bash
cd <parent_dir>
gh repo clone <owner/repo>
cd <repo_name>
```

Use `origin` as the base remote for fetch/rebase/push.

If `<owner>` is different from current login, fork first:

```bash
cd <parent_dir>
gh repo fork <owner/repo> --clone --remote=true
cd <repo_name>
```

In fork mode, ensure:
- `origin` -> personal fork
- `upstream` -> original `<owner/repo>`

If `upstream` is missing in fork mode:

```bash
git remote add upstream https://github.com/<owner/repo>.git
```

## Step 3: Create Branch

Detect default branch:

```bash
gh repo view <owner/repo> --json defaultBranchRef -q .defaultBranchRef.name
```

If running in fork mode, branch from latest `upstream/<default_branch>`:

```bash
git fetch upstream
git checkout -B <default_branch> upstream/<default_branch>
git checkout -b issue-<issue_number>-<short-slug>
```

If running in owner mode (no fork), branch from latest `origin/<default_branch>`:

```bash
git fetch origin
git checkout -B <default_branch> origin/<default_branch>
git checkout -b issue-<issue_number>-<short-slug>
```

## Step 4: Implement Issue

- Keep scope strictly aligned with issue requirements.
- Avoid unrelated refactors unless required to complete the issue.
- Add or update tests for behavior changes.
- Run project checks (lint/test/build) relevant to changed code.

Capture key verification results for PR description.

## Step 5: Commit Locally

Use clear, issue-linked commits:

```bash
git add -A
git commit -m "Fix #<issue_number>: <short summary>"
```

If there are multiple logical changes, split into separate commits.

## Step 6: Run `$code-review` Before PR

Invoke `$code-review` on the diff between `<default_branch>` and `issue-<issue_number>-<short-slug>`.

Review expectations:
- Report findings with severity and file/line evidence.
- Treat `P0` and `P1` findings as blockers.
- Resolve blocker findings and rerun relevant checks.
- For unresolved `P2`/`P3`, document rationale in the PR body.

## Step 7: Push Branch

Push only after local checks and blocker review findings are resolved:

```bash
git push -u origin issue-<issue_number>-<short-slug>
```

## Step 8: Create Pull Request

If running in fork mode, open PR from `<your-github-login>:issue-...` to upstream:

```bash
gh pr create \
  --repo <owner/repo> \
  --head <your-github-login>:issue-<issue_number>-<short-slug> \
  --base <default_branch> \
  --title "Fix #<issue_number>: <short summary>" \
  --body "<problem/solution/testing summary>"
```

If running in owner mode, open PR from branch in the same repository:

```bash
gh pr create \
  --repo <owner/repo> \
  --head issue-<issue_number>-<short-slug> \
  --base <default_branch> \
  --title "Fix #<issue_number>: <short summary>" \
  --body "<problem/solution/testing summary>"
```

PR body must include:
- Issue link and closing keyword (`Closes #<issue_number>`)
- Summary of what changed
- Testing/validation performed
- `$code-review` summary (blockers fixed, remaining risks if any)
- Known limitations or follow-ups (if any)

## Failure Handling

- Missing permissions to fork/push: report exact `gh`/`git` error and stop.
- Issue lacks clear acceptance criteria: summarize ambiguity and request clarification before implementation.
- Failing checks: do not create PR until failures are addressed or explicitly documented and accepted.
- Unresolved `$code-review` blockers (`P0`/`P1`): do not create PR.

## Output Contract

Return:
- Repo URL and fork URL (if fork was created)
- Branch name
- Commit SHA(s)
- PR URL
- Short test/check summary
- `$code-review` outcome summary (fixed blockers + any accepted residual risks)
