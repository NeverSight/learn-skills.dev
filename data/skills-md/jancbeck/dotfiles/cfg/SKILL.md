---
name: cfg
description: Sync dotfiles - pull, resolve conflicts, commit changes, and push
disable-model-invocation: true
---

# Dotfiles Sync

Manage dotfiles using the bare git repo technique with the `config` alias.

The `config` alias is defined as:
```
alias config='/usr/bin/git --git-dir=$HOME/.cfg/ --work-tree=$HOME'
```

## Workflow

### Step 1: Pull and Rebase
```bash
config pull --rebase
```

If this fails with conflicts:
- Show the user which files have conflicts
- Read the conflicted files and help resolve them
- After resolution, run `config add <file>` for each resolved file
- Continue with `config rebase --continue` or drop the stash if needed

### Step 2: Check Status
```bash
config status
```

Show the user:
- How many commits ahead/behind of origin
- Any modified files not yet staged

### Step 2.5: Check for Untracked Files
Since `showUntrackedFiles` is disabled, manually check key directories for new files:
```bash
config ls-files --others --exclude-standard ~/.claude/skills/
```

If any untracked files are found, ask the user if they want to add them.

### Step 3: Show Diff
If there are unstaged changes:
```bash
config diff
```

Summarize what changed in each file concisely.

### Step 4: Commit (if changes exist)
If there are changes to commit:
1. Stage all modified tracked files: `config add -u`
2. Draft a concise commit message based on the diff
3. Commit with:
```bash
config commit -m "$(cat <<'EOF'
<commit message>

Co-Authored-By: Claude <noreply@anthropic.com>
EOF
)"
```

### Step 5: Push
If there are commits to push:
```bash
config push
```

### Step 6: Summary
Report final status:
- Commits pushed (if any)
- Current sync state with origin
