---
name: linear-comments
description: Manage issue comments - list, create, update, delete. Use when reading or posting comments on issues.
allowed-tools: Bash
---

# Comments

```bash
# List comments on an issue
linear-cli cm list ISSUE_ID
linear-cli cm list SCW-123 --output json

# Create a comment
linear-cli cm create ISSUE_ID -b "Looks good, merging!"

# Update a comment
linear-cli cm update COMMENT_ID -b "Updated text"

# Delete a comment
linear-cli cm delete COMMENT_ID --force
```

## Flags

| Flag | Purpose |
|------|---------|
| `-b BODY` | Comment body text |
| `--output json` | JSON output |
| `--force` | Skip delete confirmation |

## Exit Codes

`0`=Success, `1`=Error, `2`=Not found, `3`=Auth error
