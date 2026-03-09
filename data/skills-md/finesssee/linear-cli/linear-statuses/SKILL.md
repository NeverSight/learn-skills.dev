---
name: linear-statuses
description: View and manage workflow states. Use when checking or configuring issue statuses for a team.
allowed-tools: Bash
---

# Statuses

```bash
# List all statuses for a team
linear-cli st list -t ENG
linear-cli st list -t ENG --output json

# Get status details
linear-cli st get "In Progress" -t ENG

# Update a workflow state
linear-cli st update STATE_ID --name "Reviewing" --color "#3B82F6"
```

## Flags

| Flag | Purpose |
|------|---------|
| `-t TEAM` | Team key (required) |
| `--name NAME` | Status name |
| `--color HEX` | Status color |
| `--output json` | JSON output |

## Exit Codes

`0`=Success, `1`=Error, `2`=Not found, `3`=Auth error
