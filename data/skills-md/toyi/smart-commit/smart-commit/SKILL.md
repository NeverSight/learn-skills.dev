---
name: smart-commit
description: >
  Analyzes all uncommitted changes, groups them by theme (directory, semantic content, timestamps),
  and creates multiple focused commits. Use /smart-commit to create all commits automatically,
  or /smart-commit step to approve each commit one by one.
user_invocable: true
allowed-tools: Read, Bash(git *), Bash(stat *), AskUserQuestion
---

## Context

- Current git status: !`git status`
- Current git diff (staged and unstaged): !`git diff HEAD`
- Recent commits (style reference): !`git log --oneline -15`
- Current branch: !`git branch --show-current`

## Your task

You are a smart commit organizer. You analyze all uncommitted changes in the repository, group them into coherent thematic commits, and create them one by one.

**Arguments:**
- No argument → Automatic mode (create all commits without asking)
- `step` → Step-by-step mode (present each commit for approval before creating it)

## Workflow

### Step 0: Check CLAUDE.md for Directives

Before doing anything else, read the project's `CLAUDE.md` file (if it exists) and look for any instructions related to `smart-commit` behavior (commit style overrides, excluded paths, grouping preferences, custom constraints, etc.). Any directives found there take precedence over the defaults in this skill.

### Step 1: Detect Commit Style

Analyze the 15 recent commits from the context above. Identify the commit message format:
- Conventional commits (`feat:`, `fix:`, `chore:`, etc.)
- Prefixed (`[Feature]`, `[Fix]`, etc.)
- Plain descriptive
- Any other pattern

You MUST reproduce this exact style for all new commits.

### Step 2: Collect All Changes

Parse `git status --porcelain` output to get every changed file:
- Staged files (A, M, D in first column)
- Unstaged modifications (M in second column)
- Untracked files (??)
- Deleted files (D)
- Renamed files (R)

First, unstage everything to start fresh:
```
git reset HEAD -- .
```

Then run:
```
git status --porcelain
```

### Step 3: Get File Timestamps

For all modified/untracked files (not deleted), get their modification timestamps:
```
stat -c '%Y %n' <file1> <file2> ...
```

For large file lists, batch the stat calls.

### Step 4: Group Changes by Theme

Create thematic groups using these signals (in priority order):

1. **Primary — Directory path**: Files in the same directory or directory tree are likely related. Group files sharing a common parent directory.

2. **Secondary — Semantic analysis**: Read the diff content for each file. Files with related changes (same feature, same domain concept) should be grouped together even if in different directories.

3. **Tertiary — Temporal proximity**: Files modified within 5 minutes of each other AND sharing the same theme should be in the same commit.

**Hunk-level splitting (partial file commits):**

When a single file contains changes that belong to different themes (e.g. a controller file where you added a new endpoint AND fixed a bug in an existing one), you MUST split it:

1. Run `git diff <file>` to get the full diff
2. Identify individual hunks (each `@@ ... @@` block)
3. Analyze each hunk's content semantically to determine which theme it belongs to
4. Assign each hunk to the appropriate group

To stage only specific hunks of a file, create a temporary patch file and apply it:
```
git diff <file> > /tmp/full.patch
```
Then manually extract the relevant hunks (keeping the diff header + only the target `@@` blocks) into a partial patch and apply:
```
git apply --cached /tmp/partial.patch
```

After staging partial hunks for a commit, verify with `git diff --cached <file>` that only the intended changes are staged.

**Important:** After committing a partial file, the remaining unstaged hunks of that file are still available for the next group. Always re-run `git diff <file>` before processing the next group to see what's left.

**Grouping rules:**
- Each group gets a descriptive commit message in the detected style
- A single file CAN belong to multiple groups if its hunks are thematically different
- Deleted files are grouped by their former path
- Renamed files: both old and new paths go in the same group
- Binary files are grouped by path + timestamp only (no diff analysis, no splitting)
- If there are 50+ files, be more aggressive in grouping (broader themes)
- If changes are all in one theme, it's fine to have just one commit
- If all hunks in a file belong to the same theme, stage the whole file normally with `git add` (no need to split)

**Output format** (internal, for your use):
```
Group 1: "commit message here"
  - path/to/file1.ext (modified)
  - path/to/file2.ext (new)
  - path/to/file3.ext (partial — hunks 1,3)

Group 2: "commit message here"
  - path/to/file3.ext (partial — hunk 2)
  - path/to/file4.ext (deleted)
```

### Step 5: Check for Conflicts

Before starting commits, check for merge conflicts:
```
git diff --check
```

If conflicts are found, STOP and report them to the user. Do not proceed with any commits.

### Step 6: Execute Commits

#### Automatic Mode (default, no argument)

For each group:
1. Stage the files (whole files with `git add`, partial files with `git apply --cached`)
2. Commit with the generated message
3. Move to next group

No user interaction needed.

#### Step-by-step Mode (argument: `step`)

For each group, in logical order:

1. Display the group to the user:
```
### Commit N/Total: <commit message>

Files:
- path/to/file1.ext (modified)
- path/to/file2.ext (new)
- path/to/file3.ext (partial — 2/5 hunks)
```

For partial files, also show the specific diff hunks that will be included so the user can verify the split makes sense.

2. Use `AskUserQuestion` to ask the user:
   - "Approve this commit?" with options:
     - **Yes** — Stage files and commit
     - **Edit message** — Let the user provide a different commit message
     - **Skip** — Skip this group entirely (files remain uncommitted)

3. If approved:
   - For whole files: `git add <file1> <file2> ...`
   - For deleted files: `git add <deleted-file>` (git add handles deletions)
   - For partial files (specific hunks only):
     a. Extract the diff header + target hunks into a patch file
     b. `git apply --cached /tmp/smart-commit-partial.patch`
     c. Verify with `git diff --cached <file>` that only intended hunks are staged
   - Commit: `git commit -m "<message>"`
   - Confirm success and move to next group

4. If the user chooses "Edit message":
   - Ask for the new message
   - Stage and commit with the new message

5. If skipped, move to the next group.

### Step 7: Final Summary

After all groups are processed, display:

```
## Smart Commit Summary

### Commits Created
1. <hash-short> <commit message> (N files)
2. <hash-short> <commit message> (N files)
...

### Skipped
- N files remain uncommitted

### Current Status
```

Then run `git status` to show the final state.

## Constraints

- NEVER add "Generated by Claude..." or "Co-Authored-By: Claude..." to commit messages
- NEVER push to remote — only local commits
- NEVER run linters
- NEVER commit without asking in step-by-step mode
- NEVER modify file contents — only stage and commit existing changes
- Pass commit messages using HEREDOC format to preserve special characters:
  ```
  git commit -m "$(cat <<'EOF'
  commit message here
  EOF
  )"
  ```
