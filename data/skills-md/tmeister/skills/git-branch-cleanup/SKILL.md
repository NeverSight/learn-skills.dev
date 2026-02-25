---
name: git-branch-cleanup
description: Safely clean merged and stale git branches with explicit confirmations.
---

# Git Branch Cleanup

Use this skill to safely remove merged or stale branches with explicit user confirmation.

## Safety Rules

- Stop if the working tree is not clean.
- Detect the default branch from `origin/HEAD` and fall back to `main`, then `master`.
- Never delete protected branches.
- Never force delete unless the user explicitly approves.

## Workflow

1. **Check repository state**
   - `git status --porcelain`
   - If not clean, ask the user to commit or stash first.

2. **Detect default branch**
   - `git symbolic-ref refs/remotes/origin/HEAD | sed 's@^refs/remotes/origin/@@'`
   - If that fails, try `main`, then `master`.

3. **Define protected branches**
   - Default: `main`, `master`, `develop`, `staging`, `production`, `qa`.
   - Ask the user if any additional branches should be protected.

4. **List merged branches**
   - Local: `git branch --merged <default-branch>`
   - Remote: `git branch -r --merged <default-branch>`
   - Exclude protected branches and the current branch.
   - Present the list and ask for explicit approval to delete.

5. **List stale branches**
   - Show last commit date for each local branch:
     `git for-each-ref --format='%(refname:short) %(committerdate:short)' refs/heads`
   - Ask user for a cutoff (default 30 days).
   - Present the stale list and ask for explicit approval to delete.

6. **Delete with confirmation**
   - Local delete: `git branch -d <branch>`
   - If deletion fails because it is unmerged, ask whether to force delete with `-D`.

7. **Remote cleanup**
   - Prune tracking branches: `git remote prune origin`
   - For remote branches approved for deletion:
     `git push origin --delete <branch>`

8. **Report and recovery**
   - Summarize what was deleted.
   - Provide recovery hint: `git reflog --no-merges --since="2 weeks ago"`.

## Output Format

Provide:

- Default branch detected
- Protected branch list
- Merged branches list (local and remote)
- Stale branches list (local)
- Confirmations collected
- Final summary of deletions
