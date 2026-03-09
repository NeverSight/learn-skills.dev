---
name: linear-milestones
description: Manage project milestones - create, update, track target dates. Use when planning project deliverables.
allowed-tools: Bash
---

# Milestones

```bash
# List milestones for a project
linear-cli ms list -p "My Project"
linear-cli ms list -p "My Project" --output json

# Get milestone details
linear-cli ms get MILESTONE_ID

# Create a milestone
linear-cli ms create "Beta Release" -p "My Project"
linear-cli ms create "GA" -p PROJ --target-date 2025-06-01

# Update a milestone
linear-cli ms update MILESTONE_ID --target-date +2w
linear-cli ms update MILESTONE_ID --name "Renamed"

# Delete a milestone
linear-cli ms delete MILESTONE_ID --force
```

## Flags

| Flag | Purpose |
|------|---------|
| `-p PROJECT` | Project name/ID |
| `--target-date DATE` | Target date (YYYY-MM-DD or +Nw) |
| `--name NAME` | Milestone name |
| `--output json` | JSON output |

## Exit Codes

`0`=Success, `1`=Error, `2`=Not found, `3`=Auth error
