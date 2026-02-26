---
name: rebase
description: Perform a non-interactive interactive git rebase. Use when the user asks to rebase, squash, reorder, drop, or rename commits.
model: haiku
allowed-tools: Bash(git:*), Bash(*/git-rebase-non-interactive.js:*)
---

# Interactive Rebase

Use the `git-rebase-non-interactive.js` script located in this skill's directory.

## Usage

```bash
<skill-path>/git-rebase-non-interactive.js HEAD~N << 'EOF'
pick abc123 Message
drop def456 Message to remove
fixup ghi789 Merge into previous
pick jkl012 Another message
exec git commit --amend -m "New message to rename"
EOF
```

## Available Actions

- `pick`: keep the commit as-is
- `drop`: remove the commit
- `fixup`: merge into the previous commit (keep the previous commit's message)
- `squash`: merge into the previous commit (combine both messages)
- `exec git commit --amend -m "..."`: rename the commit just above

## Workflow

1. Run `git log --oneline` to see the commits
2. Build the todo list with the desired actions
3. Run the command with a heredoc
