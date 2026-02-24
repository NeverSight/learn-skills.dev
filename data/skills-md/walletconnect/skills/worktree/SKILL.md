---
name: worktree
description: Manages git worktree lifecycle - create, list, remove, cleanup, prune, lock/unlock. Use when user mentions 'worktree', 'parallel branch work', 'cleanup worktrees', or needs to work on multiple branches simultaneously.
user-invocable: true
---

# Git Worktree Manager

Manages the full lifecycle of git worktrees: creation, monitoring, cleanup, and maintenance.

## Subcommands

| Command | Alias | Description |
|---------|-------|-------------|
| `/worktree create <name>` | `/worktree <name>` | Create new worktree with conventional branch naming |
| `/worktree list` | `/worktree ls` | Show all worktrees with status and branch info |
| `/worktree remove <path>` | `/worktree rm` | Remove worktree + cleanup branches |
| `/worktree cleanup` | - | Interactive batch removal of multiple worktrees |
| `/worktree prune` | - | Remove stale worktree references |
| `/worktree lock <path>` | - | Prevent worktree from being auto-pruned |
| `/worktree unlock <path>` | - | Allow worktree to be pruned again |

**Default**: No subcommand or unrecognized arg = `create`

## When to use
- Creating isolated workspace for new feature/fix
- Viewing all active worktrees across a repo
- Cleaning up after merging PRs
- Removing abandoned/stale worktrees
- Protecting important worktrees on portable storage

## When not to use
- Simple branch switching (use `git checkout`)
- Temporary file exploration (use `git stash` or read-only)
- Submodule management (different concept)

---

## Subcommand: create

Creates new worktree in sibling directory with conventional commit branch naming.

### Workflow

1. **Get name**: From args or ask user (e.g., "alerts", "fix-login")

2. **Prompt for type**: Use AskUserQuestion
   - Header: "Commit type"
   - Options: feat, fix, chore, docs, refactor, test, perf, ci

3. **Construct branch**: `{type}/{name}` (e.g., `feat/alerts`)

4. **Determine path**:
   - Get repo name from remote/directory
   - Path: `../{repo}-{type}-{name}` (slashes → hyphens)

5. **Create**:
   ```bash
   git worktree add -b {branch} {path}
   ```

6. **Confirm**: Show branch name, path, and `cd` command

### Error handling
- Branch exists → offer to use existing or suggest new name
- Directory exists → warn and ask to proceed or rename
- Dirty working tree → warn but allow (worktree add works regardless)

---

## Subcommand: list

Shows all worktrees with status information.

### Workflow

1. **Run**: `git worktree list -v`

2. **Parse and display**:
   - Path
   - Branch name (or "detached HEAD")
   - Status flags: locked, prunable, bare
   - Commit SHA (short)

3. **Enhance** (optional): For each worktree, show:
   - Uncommitted changes count: `git -C {path} status --porcelain | wc -l`
   - Ahead/behind upstream: `git -C {path} rev-list --left-right --count @{u}...HEAD`

### Example output
```
Worktrees for my-project:
  /path/to/main          [main]           clean, up-to-date
  /path/to/feat-alerts   [feat/alerts]    3 uncommitted, 2 ahead
  /path/to/old-feature   [fix/old]        prunable (directory missing)
```

---

## Subcommand: remove

Removes single worktree with full branch cleanup.

### Workflow

1. **Identify target**: From args or show list and ask

2. **Check status**:
   ```bash
   git -C {path} status --porcelain
   ```
   - If uncommitted changes → warn and confirm force removal

3. **Get branch name** for cleanup:
   ```bash
   git -C {path} branch --show-current
   ```

4. **Remove worktree**:
   ```bash
   git worktree remove {path}        # clean
   git worktree remove -f {path}     # if uncommitted changes
   git worktree remove -ff {path}    # if locked
   ```

5. **Delete local branch**:
   ```bash
   git branch -d {branch}    # safe (fails if unmerged)
   git branch -D {branch}    # force (if user confirms)
   ```

6. **Offer remote branch deletion** (AskUserQuestion):
   - Check if remote exists: `git ls-remote --heads origin {branch}`
   - If yes, ask: "Delete remote branch too?"
   - If yes: `git push origin --delete {branch}`

7. **Confirm**: Summarize what was removed

### Safety checks
- Never remove main worktree (the original repo)
- Warn if branch has unpushed commits
- Warn if PR is still open for this branch

---

## Subcommand: cleanup

Interactive batch removal of multiple worktrees.

### Workflow

1. **List all worktrees**: `git worktree list --porcelain`

2. **Filter candidates**:
   - Exclude main worktree
   - Flag: prunable, merged branches, old (no commits in 2+ weeks)

3. **Present selection** (AskUserQuestion with multiSelect):
   - Header: "Cleanup"
   - Question: "Which worktrees should be removed?"
   - Options: List each non-main worktree with status

4. **For each selected**: Run `remove` workflow

5. **Run prune**: `git worktree prune -v`

6. **Summary**: Show what was cleaned up

---

## Subcommand: prune

Removes stale worktree administrative files.

### Workflow

1. **Preview**: `git worktree prune -n -v`

2. **If stale entries found**:
   - Show what will be pruned
   - Confirm with user

3. **Prune**: `git worktree prune -v`

4. **Report**: Show removed entries

### When to use
- After manually deleting worktree directories
- After moving worktree without `git worktree move`
- Periodic maintenance

---

## Subcommand: lock / unlock

Protects worktree from automatic pruning.

### Lock workflow

1. **Identify worktree**: From args or list and ask

2. **Prompt for reason** (optional):
   - "Why lock this worktree?" (e.g., "portable drive", "long-running experiment")

3. **Lock**:
   ```bash
   git worktree lock --reason "{reason}" {path}
   # or without reason:
   git worktree lock {path}
   ```

4. **Confirm**: Show locked status

### Unlock workflow

1. **Identify worktree**: From args or list locked ones

2. **Unlock**: `git worktree unlock {path}`

3. **Confirm**: Show unlocked status

---

## Validation checklist

- [ ] Correct subcommand identified from args
- [ ] Branch naming follows `{type}/{name}` convention
- [ ] Worktree path is sibling directory, not nested
- [ ] No uncommitted changes lost without warning
- [ ] Local branch deleted only after worktree removal
- [ ] Remote branch deletion is opt-in, not automatic
- [ ] Main worktree protected from removal
- [ ] Prune only runs after user confirmation

---

## Examples

### Example 1: Create
```
User: /worktree queue-alerts
Claude: [asks commit type] → User: feat
Claude: Created worktree
  Branch: feat/queue-alerts
  Path: ../my-project-feat-queue-alerts
  Run: cd ../my-project-feat-queue-alerts
```

### Example 2: List
```
User: /worktree list
Claude: Worktrees for my-project:
  /Users/me/my-project              [main]           clean
  /Users/me/my-project-feat-alerts  [feat/alerts]    2 uncommitted
  /Users/me/my-project-fix-bug      [fix/bug-123]    prunable
```

### Example 3: Remove with cleanup
```
User: /worktree remove ../my-project-feat-alerts
Claude: Worktree has 2 uncommitted changes. Force remove?
User: yes
Claude: [asks about remote branch deletion] → User: yes
Claude: Removed:
  - Worktree: ../my-project-feat-alerts
  - Local branch: feat/alerts
  - Remote branch: origin/feat/alerts
```

### Example 4: Interactive cleanup
```
User: /worktree cleanup
Claude: [shows multiselect with 3 worktrees]
User: [selects 2]
Claude: Removed 2 worktrees, pruned 1 stale entry
  - feat/old-feature (merged)
  - fix/abandoned (no remote)
```

---

## Notes

- Worktrees share git objects but have separate working directories
- Each worktree can have different branch checked out simultaneously
- Locked worktrees survive `git gc` and won't be auto-pruned
- Use `git worktree move` to relocate (not manual mv)
- See WORKFLOWS.md for detailed step-by-step procedures

---

## Evaluation Prompts

### Test 1: Activation - create (should trigger)
```
User: /worktree new-dashboard
Expected: Skill activates, asks for commit type, creates worktree
```

### Test 2: Activation - list (should trigger)
```
User: /worktree list
Expected: Skill activates, runs git worktree list, shows formatted output
```

### Test 3: Activation - cleanup (should trigger)
```
User: /worktree cleanup
Expected: Skill activates, lists worktrees with multiselect, processes removals
```

### Test 4: Activation - natural language (should trigger)
```
User: I need to clean up my old worktrees
Expected: Skill activates with cleanup subcommand context
```

### Test 5: Non-activation (should NOT trigger)
```
User: How do I switch to a different branch?
Expected: Normal response about git checkout/switch, NOT worktree skill
```

### Test 6: Non-activation (should NOT trigger)
```
User: Delete the feature-x branch
Expected: Normal git branch -d advice, NOT worktree removal
```

### Test 7: Edge case - remove main worktree
```
User: /worktree remove .
Expected: Skill refuses with clear error "Cannot remove main worktree"
```

### Test 8: Edge case - remove with uncommitted changes
```
User: /worktree remove ../project-feat-wip
Context: Worktree has uncommitted changes
Expected: Warning shown, asks for confirmation before force removal
```

### Test 9: Edge case - no worktrees to cleanup
```
User: /worktree cleanup
Context: Only main worktree exists
Expected: "No worktrees available for cleanup" message
```
