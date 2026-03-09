---
name: linear-done
description: Mark the current branch's issue as Done. Use as a quick shortcut to close the issue you're working on.
allowed-tools: Bash
---

# Done

```bash
# Mark current branch's issue as Done
linear-cli done

# Set to a different status
linear-cli done --status "In Review"
linear-cli done -s "In Progress"
```

Reads the current git branch, extracts the issue ID (e.g. `feat/SCW-123-title` -> `SCW-123`), and updates the issue status.

## Flags

| Flag | Purpose |
|------|---------|
| `-s STATUS` | Status to set (default: "Done") |

## Exit Codes

`0`=Success, `1`=Error, `2`=Not found, `3`=Auth error
