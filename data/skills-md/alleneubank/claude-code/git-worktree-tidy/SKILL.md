---
name: git-worktree-tidy
description: Fetch latest from origin, prune remote-tracking refs, delete stale local branches and worktrees, and fast-forward important branches. Use when tidying up a worktree-based repo layout.
metadata:
  short-description: Worktree hygiene cleanup
---

# git-worktree-tidy

Routine hygiene for bare-repo + worktree layouts. Fetches origin, prunes
gone branches and orphaned worktrees, and fast-forwards important local
branches.

## When to use

User asks to "fetch prune", "clean up stale branches/worktrees", or
"update main/dev to latest" in a worktree-based repo.

## Hard Rules

- All destructive actions (worktree remove, branch delete) require user
  confirmation. Present the full list and wait.
- Never force-delete a worktree with uncommitted changes without explicit
  approval. Flag dirty worktrees separately.
- Use `--ff-only` when updating branches. If ff-only fails, stop and ask.
- Operate from the `.bare` directory (or repo root) for branch/worktree
  management commands.
- Never infer "merged/shipped" from `git rev-list origin/main..<branch>` or
  `git merge-base --is-ancestor` alone. Squash- and rebase-merges land the
  work under a new SHA, so a fully-shipped branch still shows commits "not in
  main" and a non-ancestor tip. Verify ship status against the forge's PR
  merge state (step 3a) before classifying a gone branch as unmerged.

## Workflow

### 1) Locate the bare root

Determine the bare repo directory:
- If cwd contains `.bare/`, use it
- Otherwise: `git rev-parse --git-common-dir`

All branch and worktree management commands run from this directory.

### 2) Fetch + prune

```bash
git fetch --prune origin
```

Report what was pruned (deleted remote-tracking branches, updated refs).

### 3) Discover stale branches

```bash
git branch -vv | grep ': gone]'
```

Collect branch names whose upstream is gone.

### 3a) Verify ship status (gone upstream ≠ merged)

A deleted upstream ("gone") does NOT prove the work shipped, and git ancestry
is unreliable here: squash- and rebase-merges land the work under a new SHA, so
a fully-shipped branch still shows commits "not in main" and a non-ancestor tip.
Verify against the forge before deleting — gone-but-unmerged branches are the
only ones that lose real work.

For each gone-upstream branch (GitHub example; substitute your forge CLI):

```bash
# Was there a merged PR from this head?
gh pr list --state all --head <branch> \
  --json number,state,mergedAt,mergeCommit \
  --jq '.[] | "#\(.number) \(.state) merged=\(.mergedAt // "no")"'

# If merged, confirm nothing was added to the branch AFTER the merge:
# the local tip should equal the PR head at merge.
gh pr view <pr> --json commits --jq '.commits[-1].oid'   # vs: git rev-parse <branch>
```

Classify each gone branch:
- **Merged (verified)** — a MERGED PR exists AND its head == local tip → shipped,
  safe to delete.
- **At risk** — no merged PR, or the tip has commits dated after the merge
  (`git show -s --format=%ci <tip>`) → genuine unshipped work. Flag it; do not
  delete without explicit approval.

If `gh`/the forge CLI is unavailable, say so and treat unverifiable branches as
**at risk** rather than assuming merged.

### 4) Discover stale worktrees

```bash
git worktree list
git worktree prune --dry-run
```

Cross-reference worktrees against the gone-branch list. Check each stale
worktree for dirty state:

```bash
cd <worktree-path> && git status --short
```

Categorize:
- **Clean + gone**: safe to remove
- **Dirty + gone**: flag for user review
- **Prunable metadata**: orphaned worktree entries (directory already gone)

### 5) Confirm deletions

Present a summary table:

```
Stale worktrees to remove:
  <path> (<branch>) [clean]
  <path> (<branch>) [dirty — N uncommitted changes]

Stale branches:
  <branch>  [merged — PR #N, safe to delete]
  <branch>  [AT RISK — no merged PR / commits after merge; review first]

Prunable worktree metadata:
  <entry>
```

Call out the **at risk** branches explicitly so the user is deciding with the
ship status in front of them. Wait for user confirmation before proceeding.

### 6) Remove stale worktrees

For each confirmed worktree:

```bash
git worktree remove <name>
```

If removal fails (dirty), report and skip unless user approved force.

### 7) Delete stale branches

```bash
git branch -D <branch1> <branch2> ...
```

### 8) Prune worktree metadata

```bash
git worktree prune -v
```

### 9) Update important branches

Identify which branches have dedicated worktrees for `main`, `dev`, or
other important branches (user may specify). For each:

```bash
cd <worktree-path> && git pull --ff-only origin <branch>
```

If ff-only fails, report the divergence and ask for guidance.

### 10) Final status

Show a summary: what was removed, what was updated, any items skipped.
