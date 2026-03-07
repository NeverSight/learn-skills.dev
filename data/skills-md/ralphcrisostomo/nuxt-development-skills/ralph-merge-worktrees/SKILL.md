---
name: ralph-merge-worktrees
description: "Analyze completed Ralph worktree branches, build a smart merge priority queue, and sequentially squash-merge them into main with worktree cleanup. Use this skill whenever the user wants to merge ralph worktrees, merge completed features, clean up finished ralph branches, process the ralph merge queue, or asks about which ralph branches are ready to merge. Triggers on: merge worktrees, ralph merge, merge completed branches, ralph cleanup, merge queue, which branches are done, squash ralph branches."
model: opus
user-invocable: true
---

# Ralph Merge Worktrees

Analyze completed Ralph worktree PRDs, build a dependency-aware merge queue, and sequentially squash-merge each branch into main — removing the worktree after each successful merge.

## Overview

Ralph worktrees live at `.claude/worktrees/ralph/<feature>/` with PRDs at `scripts/ralph/prd.json` inside each worktree. A worktree is "completed" when every user story in its PRD has `passes: true`. This skill finds all completed worktrees, determines the safest merge order, presents the plan for approval, and then executes it one branch at a time.

## Step 1: Scan and Identify Completed Worktrees

Read every `.claude/worktrees/ralph/*/scripts/ralph/prd.json` file. For each PRD:

1. Parse the JSON — extract `branchName`, `description`, and `userStories[]`
2. A worktree is **completed** when ALL stories have `passes: true`
3. Skip any worktree whose PRD has at least one story with `passes: false`
4. Also skip worktrees that don't have a `prd.json` (malformed or empty)

If no completed worktrees are found, tell the user and stop.

## Step 2: Analyze Each Completed Branch

For each completed worktree, gather merge intelligence:

```bash
# From the main repo root, diff the branch against main
git diff main...<branchName> --stat
git diff main...<branchName> --name-only
git log main..<branchName> --oneline
```

Collect for each branch:
- **Files changed** — the full list of modified/added/deleted files
- **Change categories** — classify files into buckets:
  - `terraform` — anything under `terraform/` (infra, resolvers, functions, lambda)
  - `types` — anything under `types/`
  - `graphql` — anything under `app/graphql/`
  - `services` — anything under `services/`
  - `composables` — anything under `app/composables/`
  - `components` — anything under `app/components/`
  - `pages` — anything under `app/pages/`
  - `layouts` — anything under `app/layouts/`
  - `content` — anything under `content/`
  - `config` — root config files (`nuxt.config.ts`, `terraform-scaffold.config.ts`, etc.)
  - `other` — everything else
- **Commit count** — number of commits on the branch
- **Story count** — total user stories in the PRD
- **File count** — total files changed
- **Overlap matrix** — which files are touched by multiple branches (potential conflict zones)

## Step 3: Build the Priority Queue

Rank branches for merge order using these heuristics (most important first):

### 3a. Dependency Layer Ordering

Merge bottom-up through the stack so downstream features inherit upstream changes:

1. **Infrastructure first** — branches that primarily touch `terraform/`, `types/`, `services/`, `config` (schema, tables, resolvers, types)
2. **Data/API layer** — branches focused on `app/graphql/`, `app/composables/` (client-side data plumbing)
3. **UI layer last** — branches primarily touching `app/components/`, `app/pages/`, `app/layouts/`, `content/`

Determine the "primary layer" by whichever category has the most changed files. If a branch spans multiple layers, it belongs to the **lowest** layer it touches (infra > api > ui).

### 3b. Within the Same Layer

When two branches are in the same layer, break ties using:

1. **Less file overlap first** — branches that share fewer files with other pending branches get merged first (lower conflict risk after merge)
2. **Smaller changeset first** — fewer files changed = less risk, gets quick wins merged early, and the larger branch can rebase more easily if needed
3. **Fewer commits first** — proxy for scope/complexity

### 3c. Special Cases

- If a branch only touches `content/` files (e.g., legal pages, markdown), it's very low-risk — can go anywhere in the queue, but default to early since it won't conflict with code changes
- If a branch touches `terraform-scaffold.config.ts` or `terraform/envs/staging/main.tf`, prefer merging it early — other branches may have stale copies of these high-contention files

## Step 4: Present the Merge Plan

Show the user the proposed merge queue in a clear table format:

```
Ralph Merge Queue — N completed branches ready

Priority | Branch                          | Stories | Files | Layer        | Reason
---------|--------------------------------|---------|-------|--------------|------------------
1        | ralph/legal-pages              | 6/6     | 8     | content      | Content-only, low risk
2        | ralph/post-creation            | 12/12   | 34    | infra+ui     | Core data model, merge early
3        | ralph/like-thread-post-comment  | 8/8     | 15    | infra+ui     | Depends on thread model
...

File overlap warnings:
- terraform/envs/staging/main.tf: touched by 3 branches (post-creation, chat-and-messaging, like-thread-post-comment)
- terraform/envs/staging/schema.graphql: touched by 4 branches

Proceed with merge queue? (y/n)
```

Wait for user confirmation before proceeding. If the user wants to reorder or skip branches, adjust the queue accordingly.

## Step 5: Execute the Merge Queue

For each branch in the queue, in order:

### 5a. Pre-merge Check

```bash
# Ensure main is clean and up to date
git checkout main
git status --porcelain
```

If there are uncommitted changes on main, stop and alert the user.

### 5b. Squash-Merge via /squash

Invoke the `/squash` skill with the branch name. This handles:
- Pre-flight checks (branch exists, has diverged from main)
- `git merge --squash <branchName>`
- Delegates commit to `/commit` (Conventional Commits, Co-Authored-By trailer)
- Post-merge verification
- Local branch cleanup (`git branch -d/-D`)

If the squash-merge **fails due to conflicts**:
1. `git merge --abort`
2. Report which files conflicted
3. **Skip this branch** — move it to the end of the queue or remove it
4. Ask the user: "Branch X has conflicts. Skip it and continue with the next branch, or stop the queue?"
5. Continue or stop based on the user's answer

### 5c. Remove the Worktree

After a successful merge and branch deletion:

```bash
# Remove the git worktree
git worktree remove .claude/worktrees/ralph/<feature-name>

# If worktree remove fails (dirty), force it since we already merged
git worktree remove --force .claude/worktrees/ralph/<feature-name>
```

Verify the worktree directory is gone. If the directory still exists after `git worktree remove`, it may need manual cleanup — warn the user but continue.

### 5d. Prune and Report

```bash
git worktree prune
```

Log the result:
```
[1/N] ralph/legal-pages — merged and worktree removed
[2/N] ralph/post-creation — merged and worktree removed
[3/N] ralph/chat-and-messaging — SKIPPED (merge conflict in schema.graphql)
...
```

### 5e. Continue to Next Branch

Move to the next branch in the queue. Each subsequent merge benefits from the prior merges already being on main, which reduces drift.

## Step 6: Final Summary

After processing the entire queue:

```
Ralph Merge Complete
--------------------
Merged:  5 branches
Skipped: 1 branch (conflicts)
Remaining worktrees: 3 (incomplete PRDs)

Skipped branches (need manual resolution):
- ralph/chat-and-messaging: conflict in terraform/envs/staging/schema.graphql

Remaining incomplete worktrees:
- ralph/follow-and-unfollow (4/10 stories)
- ralph/test-coverage (0/8 stories)
- ralph/implement-reporting (2/6 stories)
```

If any branches were skipped due to conflicts, suggest next steps:
1. Go into the skipped worktree
2. `git rebase main` to incorporate the newly merged changes
3. Resolve conflicts
4. Re-run `/ralph-merge-worktrees` to merge the remaining completed branches

## Important Notes

- Always get user confirmation before starting the merge queue — this is a destructive operation (worktree removal)
- Each merge builds on the last — if branch 2 conflicts, branches 3+ might have different conflict profiles than predicted. Re-check is automatic since we run `/squash` which does pre-flight
- The skill reads PRD files from the worktree directories, not from main — each worktree has its own copy
- Worktree paths use the feature name without the `ralph/` prefix: `.claude/worktrees/ralph/post-creation/` for branch `ralph/post-creation`
- After all merges complete, run `bun run lint` on main to verify the combined codebase is healthy
- Quote file paths with spaces in all git/bash commands (the project path contains spaces)
