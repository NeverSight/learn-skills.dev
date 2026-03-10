---
name: resolve-git-conflicts
description: >
  Resolve merge and rebase conflicts with safe recovery strategies.
  Covers identifying conflict sources, reading conflict markers,
  choosing resolution strategies, and continuing or aborting operations
  safely. Use when a git merge, rebase, cherry-pick, or stash pop reports
  conflicts, when a git pull results in conflicting changes, or when you
  need to safely abort and restart a failed merge or rebase operation.
license: MIT
allowed-tools: Read Write Edit Bash Grep Glob
metadata:
  author: Philipp Thoss
  version: "1.0"
  domain: git
  complexity: intermediate
  language: multi
  tags: git, merge-conflicts, rebase, conflict-resolution, version-control
---

# Resolve Git Conflicts

Identify, resolve, and recover from merge and rebase conflicts.

## When to Use

- A `git merge` or `git rebase` reports conflicts
- A `git cherry-pick` cannot apply cleanly
- A `git pull` results in conflicting changes
- A `git stash pop` conflicts with current working tree

## Inputs

- **Required**: Repository with active conflicts
- **Optional**: Preferred resolution strategy (ours, theirs, manual)
- **Optional**: Context about which changes should take priority

## Procedure

### Step 1: Identify the Conflict Source

Determine what operation caused the conflict:

```bash
# Check current status
git status

# Look for indicators:
# "You have unmerged paths" — merge conflict
# "rebase in progress" — rebase conflict
# "cherry-pick in progress" — cherry-pick conflict
```

The status output tells you which files have conflicts and what operation is in progress.

**Expected:** `git status` shows files listed under "Unmerged paths" and indicates the active operation.

**On failure:** If `git status` shows a clean tree but you expected conflicts, the operation may have already been completed or aborted. Check `git log` for recent activity.

### Step 2: Read Conflict Markers

Open each conflicting file and locate the conflict markers:

```
<<<<<<< HEAD
// Your current branch's version
const result = calculateWeightedMean(data, weights);
=======
// Incoming branch's version
const result = computeWeightedAverage(data, weights);
>>>>>>> feature/rename-functions
```

- `<<<<<<< HEAD` to `=======`: Your current branch (or the branch you're rebasing onto)
- `=======` to `>>>>>>>`: The incoming changes (the branch being merged or the commit being applied)

**Expected:** Each conflicting file contains one or more blocks with `<<<<<<<`, `=======`, and `>>>>>>>` markers.

**On failure:** If no markers are found but files show as conflicting, the conflict may be a binary file or a deleted-vs-modified conflict. Check `git diff --name-only --diff-filter=U` for the full list.

### Step 3: Choose a Resolution Strategy

**Manual merge** (most common): Edit the file to combine both changes logically, then remove all conflict markers.

**Accept ours** (keep current branch's version):

```bash
# For a single file
git checkout --ours path/to/file.R
git add path/to/file.R

# For all conflicts
git checkout --ours .
git add -A
```

**Accept theirs** (keep incoming branch's version):

```bash
# For a single file
git checkout --theirs path/to/file.R
git add path/to/file.R

# For all conflicts
git checkout --theirs .
git add -A
```

**Expected:** After resolution, the file contains the correct merged content with no remaining conflict markers.

**On failure:** If you chose the wrong side, re-read the conflicting version from the merge base. During a merge, `git checkout -m path/to/file` re-creates the conflict markers so you can try again.

### Step 4: Mark Files as Resolved

After editing each conflicting file:

```bash
# Stage the resolved file
git add path/to/resolved-file.R

# Check remaining conflicts
git status
```

Repeat for every file listed under "Unmerged paths".

**Expected:** All files move from "Unmerged paths" to "Changes to be committed". No conflict markers remain in any file.

**On failure:** If `git add` fails or markers remain, re-open the file and ensure all `<<<<<<<`, `=======`, and `>>>>>>>` lines are removed.

### Step 5: Continue the Operation

Once all conflicts are resolved:

**For merge**:

```bash
git commit
# Git auto-populates the merge commit message
```

**For rebase**:

```bash
git rebase --continue
# May encounter more conflicts on subsequent commits — repeat steps 2-4
```

**For cherry-pick**:

```bash
git cherry-pick --continue
```

**For stash pop**:

```bash
# Stash pop conflicts don't need a continue — just commit or reset
git add .
git commit -m "Apply stashed changes with conflict resolution"
```

**Expected:** The operation completes. `git status` shows a clean working tree (or moves to the next commit during rebase).

**On failure:** If the continue command fails, check `git status` for remaining unresolved files. All conflicts must be resolved before continuing.

### Step 6: Abort if Needed

If resolution is too complex or you chose the wrong approach, abort safely:

```bash
# Abort merge
git merge --abort

# Abort rebase
git rebase --abort

# Abort cherry-pick
git cherry-pick --abort
```

**Expected:** Repository returns to the state before the operation started. No data loss.

**On failure:** If abort fails (rare), check `git reflog` to find the commit before the operation and `git reset --hard <commit>` to restore it. Use with caution — this discards uncommitted changes.

### Step 7: Verify Resolution

After the operation completes:

```bash
# Verify clean working tree
git status

# Check that the merge/rebase result is correct
git log --oneline -5
git diff HEAD~1

# Run tests to confirm nothing is broken
# (language-specific: devtools::test(), npm test, cargo test, etc.)
```

**Expected:** Clean working tree, correct merge history, tests pass.

**On failure:** If tests fail after resolution, the merge may have introduced logical errors even though syntax conflicts are resolved. Review the diff carefully and fix.

## Validation

- [ ] No conflict markers (`<<<<<<<`, `=======`, `>>>>>>>`) remain in any file
- [ ] `git status` shows a clean working tree
- [ ] The merge/rebase history is correct in `git log`
- [ ] Tests pass after conflict resolution
- [ ] No unintended changes were introduced

## Common Pitfalls

- **Blindly accepting one side**: `--ours` or `--theirs` discards the other side entirely. Only use when you are certain one version is completely correct.
- **Leaving conflict markers in code**: Always search the entire file for remaining markers after editing. A partial resolution breaks the code.
- **Amending during rebase**: During an interactive rebase, do not `--amend` unless the rebase step specifically calls for it. Use `git rebase --continue` instead.
- **Losing work on abort**: `git rebase --abort` and `git merge --abort` discard all resolution work. Only abort if you want to start over.
- **Not testing after resolution**: A syntactically clean merge can still be logically wrong. Always run tests.
- **Force-pushing after rebase**: After rebasing a shared branch, coordinate with collaborators before force-pushing, as it rewrites history.

## Related Skills

- `commit-changes` - committing after conflict resolution
- `manage-git-branches` - branch workflows that lead to conflicts
- `configure-git-repository` - repository setup and merge strategies
