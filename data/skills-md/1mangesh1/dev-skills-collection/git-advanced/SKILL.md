---
name: git-advanced
description: Advanced Git operations including rebase, cherry-pick, bisect, reflog, and recovery. Use when user asks to "rebase branch", "cherry-pick commit", "find bug with bisect", "recover lost commit", "squash commits", "fix git history", "interactive rebase", or any advanced git tasks.
---

# Git Advanced

Advanced Git operations and recovery techniques.

## Interactive Rebase

```bash
# Rebase last N commits
git rebase -i HEAD~5

# Rebase onto branch
git rebase -i main

# Commands in interactive editor:
# pick   = keep commit as-is
# reword = keep commit, edit message
# edit   = pause for amending
# squash = combine with previous commit
# fixup  = combine with previous, discard message
# drop   = remove commit

# Squash last 3 commits into one
git rebase -i HEAD~3
# Change 'pick' to 'squash' for commits 2 and 3

# Abort if something goes wrong
git rebase --abort

# Continue after resolving conflicts
git rebase --continue

# Skip current commit
git rebase --skip
```

## Cherry-Pick

```bash
# Pick single commit
git cherry-pick abc1234

# Pick range of commits
git cherry-pick abc1234..def5678

# Pick without committing (stage only)
git cherry-pick --no-commit abc1234

# Pick from another branch
git cherry-pick feature-branch~3  # 3rd commit from tip

# Resolve conflicts and continue
git cherry-pick --continue

# Abort
git cherry-pick --abort
```

## Bisect

```bash
# Start bisect
git bisect start

# Mark current as bad
git bisect bad

# Mark known good commit
git bisect good v1.0.0

# Git checks out middle commit - test it, then:
git bisect good    # If this commit works
git bisect bad     # If this commit is broken

# Repeat until Git finds the culprit

# End bisect
git bisect reset

# Automated bisect with test command
git bisect start HEAD v1.0.0
git bisect run npm test
# Git automatically finds the first bad commit

# Automated with script
git bisect run ./test-script.sh
# Script must exit 0 (good) or 1 (bad)
```

## Stash

```bash
# Save work in progress
git stash
git stash push -m "work on feature X"

# Stash specific files
git stash push -m "partial" path/to/file.js

# Include untracked files
git stash -u
git stash --include-untracked

# List stashes
git stash list

# Apply stash
git stash pop          # Apply and remove
git stash apply        # Apply and keep
git stash pop stash@{2}  # Specific stash

# View stash contents
git stash show -p stash@{0}

# Create branch from stash
git stash branch new-branch stash@{0}

# Drop stash
git stash drop stash@{0}
git stash clear        # Remove all stashes
```

## Reflog (Recovery)

```bash
# View reflog
git reflog
git reflog show HEAD
git reflog show main

# Each entry shows HEAD position at that point
# HEAD@{0} = current
# HEAD@{1} = previous position

# Recover after hard reset
git reflog
# Find the commit hash before the reset
git reset --hard HEAD@{2}

# Recover deleted branch
git reflog
# Find last commit of deleted branch
git checkout -b recovered-branch abc1234

# Recover after bad rebase
git reflog
# Find the commit before rebase started
git reset --hard HEAD@{5}

# Reflog expires after 90 days (default)
```

## Reset vs Revert

```bash
# Reset (moves HEAD, rewrites history)
git reset --soft HEAD~1    # Undo commit, keep changes staged
git reset --mixed HEAD~1   # Undo commit, keep changes unstaged (default)
git reset --hard HEAD~1    # Undo commit, discard changes

# Revert (creates new commit, safe for shared branches)
git revert abc1234
git revert HEAD~3..HEAD    # Revert range
git revert --no-commit abc1234  # Stage without committing

# Revert a merge commit
git revert -m 1 abc1234   # Keep parent 1 (usually main)
```

## Worktrees

```bash
# Create linked worktree
git worktree add ../project-hotfix hotfix-branch
git worktree add ../project-review origin/feature-branch

# List worktrees
git worktree list

# Remove worktree
git worktree remove ../project-hotfix

# Prune stale worktrees
git worktree prune
```

## Log & History

```bash
# Compact log
git log --oneline --graph --all

# Search commits by message
git log --grep="fix bug"

# Search commits by code change
git log -S "functionName"           # Pickaxe (added/removed)
git log -G "pattern"                # Regex in diff

# Show commits that changed a file
git log --follow -- path/to/file.js

# Show who changed each line
git blame path/to/file.js
git blame -L 10,20 path/to/file.js  # Lines 10-20

# Diff between branches
git diff main..feature
git diff main...feature              # Changes since fork point

# Show files changed between commits
git diff --name-only HEAD~5 HEAD
```

## Cleanup

```bash
# Remove untracked files (dry run first!)
git clean -n              # Preview
git clean -f              # Delete files
git clean -fd             # Delete files and directories
git clean -fx             # Delete ignored files too

# Garbage collection
git gc
git gc --aggressive

# Remove old reflog entries
git reflog expire --expire=30.days --all
```

## Common Workflows

```bash
# Squash merge (clean history)
git checkout main
git merge --squash feature-branch
git commit -m "Add feature X"

# Rebase before merge (linear history)
git checkout feature
git rebase main
git checkout main
git merge feature   # Fast-forward

# Fixup workflow
git commit --fixup=abc1234
git rebase -i --autosquash main
```

## Reference

For recovery techniques and reflog patterns: `references/recovery.md`
