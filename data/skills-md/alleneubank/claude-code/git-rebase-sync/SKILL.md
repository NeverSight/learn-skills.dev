---
name: git-rebase-sync
description: Use when syncing a feature branch onto the latest origin base branch via git rebase.
metadata:
  short-description: Rebase branch sync
---

# git-rebase-sync

Use this skill when you need to sync a feature branch onto the latest `origin/{base_branch}` via **git rebase**, including **conflict resolution** with explicit clarification questions when intent is ambiguous.

## Goals
- Rebase the current branch onto a specified base branch (often the repo default branch like `dev` or `main`).
- Resolve conflicts deliberately, without guesswork.
- Keep safety rails: backup ref, confirmations before history-rewriting commands, and safe pushing.

## Hard Rules
- Do not create or switch to a different feature branch. Operate on the current branch name unless I explicitly ask otherwise.
- Before any history-rewriting command (`git rebase ...`, `git push --force*`), print the exact command(s) you will run and wait for my confirmation.
- Create a local backup ref (prefer an annotated tag) before starting the rebase. Do not push backup refs unless I explicitly ask.
- Prefer `git push --force-with-lease`, never plain `--force`.
- If the correct conflict resolution is unclear, stop and ask a targeted question. Do not invent product behavior.

## Workflow

### 1) Identify base + branch
- Determine the current branch:
  - `git branch --show-current`
- Determine the base branch you will rebase onto:
  - If not provided, use GitHub default branch:
    - `gh repo view --json defaultBranchRef --jq '.defaultBranchRef.name'`
- Fetch latest:
  - `git fetch origin`

### 2) Preflight safety checks
- Ensure the working tree is clean and there is no operation in progress:
  - `git status`
- If `git status` indicates an in-progress merge/rebase/cherry-pick, stop and ask what to do (abort vs continue).

### 3) Create a local backup ref (do not push)
- Create an annotated tag at current `HEAD`:
  - `git tag -a {branch_name}-rebase-backup-$(date +%Y%m%d-%H%M%S) -m "pre-rebase backup" HEAD`
- Record the tag name as `{backup_ref}` for recovery.

### 4) Choose rebase mode (normal vs preserve merges)
- Check whether the branch contains merge commits:
  - `git rev-list --count --merges origin/{base_branch}..HEAD`
- If merge commits exist, ask whether to preserve them (`--rebase-merges`) or flatten them (plain rebase).

### 5) Detect stacked branches (will they follow the rebase?)
Other local branches may point at intermediate commits in the range being rewritten (`origin/{base_branch}..HEAD`) — common with phased `NN-description` stacks. A plain rebase rewrites those commits and **orphans** the stacked branches on the old, pre-rebase commits (along with every open PR built on them). `--update-refs` (the default in step 6) moves them onto the rewritten commits instead. Enumerate them so you can report what the rebase will carry along:

```bash
# Branches pointing into the range being rewritten — these get orphaned by a
# plain rebase and require --update-refs to follow the rewrite.
cur=$(git branch --show-current)
git for-each-ref --format='%(refname:short)' refs/heads | while read -r br; do
  [ "$br" = "$cur" ] && continue
  if git merge-base --is-ancestor "$br" HEAD \
     && ! git merge-base --is-ancestor "$br" origin/{base_branch}; then
    echo "stacked: $br ($(git rev-parse --short "$br"))"
  fi
done
```

- Report the detected stacked branches to me before rebasing.
- A branch that is **checked out in another worktree** is skipped by `--update-refs` (git will not move a checked-out branch); flag these so I can verify them manually after the rebase.

### 6) Run the rebase (requires confirmation)
- Default to `--update-refs` so any stacked branch pointing into the rewritten range follows the rewrite instead of being orphaned.
- Print the exact command you intend to run, then wait for confirmation:
  - Default:
    - `git rebase --update-refs origin/{base_branch}`
  - With merge preservation:
    - `git rebase --rebase-merges --update-refs origin/{base_branch}`
- To make this the permanent default without the flag: `git config --global rebase.updateRefs true`.

### 7) Conflict handling loop
When conflicts happen:
1. Collect context:
   - `git status`
   - Identify conflicted files (from status output).
2. For each conflicted file:
   - Open the file and understand the surrounding code and intent.
   - Prefer minimal, mechanical conflict resolutions:
     - Keep upstream changes unless the feature branch deliberately supersedes them.
     - Re-run generators (lockfiles, codegen) instead of hand-editing when appropriate.
   - If intent is ambiguous, ask a single targeted question, for example:
     - "Should we keep the new upstream behavior X, or keep the feature behavior Y?"
     - "Is this file generated and safe to regenerate, or do you want manual resolution?"
3. Apply the resolution, then stage only resolved files:
   - `git add <file...>`
4. Continue:
   - `git rebase --continue`
5. If you reach a point where resolution is too risky/unclear:
   - Stop and ask; optionally propose aborting the rebase.

Helpful commands during conflicts:
- Inspect current conflict hunks: `git diff`
- See the commit being replayed: `git show`
- If you need to back out: `git rebase --abort` (this is safe and should be preferred over destructive resets)

### 8) Post-rebase verification
- Show the new commit range:
  - `git log --oneline --decorate origin/{base_branch}..HEAD`
- Confirm each stacked branch from step 5 moved onto the rewritten range. `git rebase --update-refs` prints an "Updated the following refs with --update-refs" summary; the moved branch refs should also appear as decorations on the new commits in the log above. Note any that did **not** move (e.g. checked out in another worktree) for manual handling.
- Run appropriate repo checks (tests, typecheck, lint) if available.

### 9) Push updated branch(es) (requires confirmation)
- If the branch already exists on origin, rebasing rewrites history, so pushing requires force-with-lease.
- `--update-refs` only moves **local** refs. A normal `git push` updates the current branch only — each stacked branch (from step 5) that also exists on origin must be force-pushed **individually**.
- Print the exact command(s) and wait for confirmation:
  - Current branch:
    - `git push --force-with-lease origin HEAD:{branch_name}`
  - Each moved stacked branch that exists on origin (repeat per branch):
    - `git push --force-with-lease origin {stacked_branch}`
- Any branch skipped because it is checked out in another worktree was not moved — verify it before pushing.

## Recovery
- If something goes wrong, use `{backup_ref}` to restore the pre-rebase state.
- Do not run destructive commands (e.g., `git reset --hard`) unless I explicitly confirm after you show the exact command.
