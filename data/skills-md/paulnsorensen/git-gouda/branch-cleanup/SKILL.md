---
license: MIT
name: branch-cleanup
description: >
  Report stale git branches with a keep, archive, or delete recommendation, and propose
  enabling delete-branch-on-merge. Use for "clean up stale branches", "delete merged
  branches", "delete branch on merge", "which branches are dead", or /branch-cleanup.
  Checks age, author, ahead/behind counts, merged status, open pull requests, and ruleset
  protection, then prints exact deletion commands that require explicit per-batch
  authorization before any push. Do NOT use for local git worktree management (worktree
  add, list, or prune) — that stays out of scope. One-time repository merge defaults and
  branch-protection rulesets belong to /gh-bootstrap; this skill reads and reports on that
  state but does not set it up.
---

# branch-cleanup

Report stale remote branches and propose safe deletion. Never delete a branch without
explicit authorization for that batch.

## What this skill is NOT for

- Local git worktree management (`git worktree add`, `list`, `prune`) — out of scope.
- One-time repository merge-default and branch-protection setup — use `/gh-bootstrap`.
  This skill only reads `delete_branch_on_merge` and existing rulesets; it proposes
  turning the setting on but the write happens through `gh api -X PATCH`, the same
  endpoint `/gh-bootstrap` uses in its step 2.

## Protocol

### 1. Check delete-branch-on-merge

```bash
REPO="$(gh repo view --json nameWithOwner --jq '.nameWithOwner')"
gh api "repos/$REPO" --jq '.delete_branch_on_merge'
```

If `false`, propose enabling it and explain the effect: GitHub deletes a branch's remote
ref automatically once its pull request merges. Ask for explicit authorization before
running the `gh api -X PATCH repos/{owner}/{repo} -F delete_branch_on_merge=true` write —
see `/gh-bootstrap` step 2 for the full merge-defaults `PATCH`, which this skill does not
duplicate.

### 2. Report stale branches

Run the bundled script from the repository root:

```bash
python3 "$BRANCH_CLEANUP_HELPER" --days 90 --github "$REPO"
```

Resolve `BRANCH_CLEANUP_HELPER` from the loaded `SKILL.md` directory
(`scripts/stale_branches.py`), resolving symlinks first. For each remote branch the script
reports:

- Last commit date and author (`git log -1`).
- Ahead/behind counts against the default branch (`git rev-list --left-right --count`).
- Merged status (`git branch -r --merged <default>`).
- Whether an open pull request targets the branch (`gh pr list --head <branch> --state
  open --json number`), when `--github` is passed.
- Whether a ruleset protects the branch (`gh api repos/{owner}/{repo}/rules/branches/
  {branch}`), when `--github` is passed.

The output is a table sorted by age (oldest first) with a `recommendation` column of
`keep`, `archive`, or `delete`. See `references/policy.md` for the exact classification
rule.

### 3. Local hygiene

Report-only, no deletion:

```bash
git fetch --prune
git branch --merged <default>
```

List the locally merged branches for the user. Do not delete local branches without the
same per-batch authorization required in step 4.

### 4. Deletion is never automatic

For every branch classified `delete`, print the exact command:

```bash
git push origin --delete <branch>
```

Always exclude the default branch, any protected branch, and any branch with an open pull
request from deletion — the script enforces this by classifying those branches `keep`
regardless of age. Require explicit user authorization before running any printed command,
and confirm the authorized batch matches the printed list exactly.

### 5. Optional scheduled report workflow

Copy `assets/stale-branch-report.yml` to `.github/workflows/stale-branch-report.yml` if the
user wants a recurring report. It only writes a job summary — it never deletes a branch.
`actions/checkout` is pinned by SHA.

### 6. Verify

Re-run the script and confirm the printed table matches the branches actually present on
the remote (`git branch -r`). Confirm no `delete` recommendation includes the default
branch, a protected branch, or a branch with an open pull request.

## Cross-references

- `/gh-bootstrap` — one-time repository merge defaults and branch-protection rulesets.
- `/prek` — local pre-commit hook checks, unrelated to branch lifecycle.
- `/oss-hygiene` — broader repository health, including community-standards files.
