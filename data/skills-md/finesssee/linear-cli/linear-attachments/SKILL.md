---
name: linear-attachments
description: Manage issue attachments - link URLs, create, update, delete. Use when attaching files or links to issues.
allowed-tools: Bash
---

# Attachments

```bash
# List attachments on an issue
linear-cli att list SCW-123
linear-cli att list SCW-123 --output json

# Get attachment details
linear-cli att get ATTACHMENT_ID

# Create attachment
linear-cli att create SCW-123 -T "Design Doc" -u https://example.com

# Link a URL to an issue (shorthand)
linear-cli att link-url SCW-123 https://example.com

# Update attachment
linear-cli att update ATTACHMENT_ID -T "New Title"

# Delete attachment
linear-cli att delete ATTACHMENT_ID --force
```

## Flags

| Flag | Purpose |
|------|---------|
| `-T TITLE` | Attachment title |
| `-u URL` | Attachment URL |
| `--output json` | JSON output |
| `--force` | Skip delete confirmation |

## Exit Codes

`0`=Success, `1`=Error, `2`=Not found, `3`=Auth error
