---
name: linear-cli
description: Instructions for using the Linear CLI to manage issues, projects, teams, and more in Linear
version: 1.0.0
license: MIT
---

# Linear CLI Agent Skill

Use this skill when the user wants to interact with Linear - a project management tool for software teams. The `linear` CLI provides full access to Linear's API for managing issues, projects, teams, cycles, labels, and users.

## When to Use This Skill

Activate this skill when the user:
- Mentions Linear, Linear issues, or Linear tickets
- Wants to create, update, or view issues/tickets
- Asks about project status or progress
- Needs to manage sprints/cycles
- Wants to check their assigned tasks
- Mentions issue identifiers like `TECH-123`, `ENG-456`, etc.

## Prerequisites

The CLI must be authenticated. Check with:
```bash
linear auth status
```

If not authenticated, guide the user to run:
```bash
linear auth login
```

## Command Reference

### Issues (Most Common)

```bash
# List issues with filters
linear issues list --team <TEAM>
linear issues list --team <TEAM> --state "In Progress"
linear issues list --assignee me
linear issues list --project "Project Name"

# View issue details (supports both formats)
linear issues view TECH-123
linear issues view <uuid>

# Create new issue
linear issues create --title "Title" --team TECH
linear issues create --title "Title" --team TECH --description "Details" --priority 2 --assignee me

# Update issue
linear issues update TECH-123 --state "In Progress"
linear issues update TECH-123 --assignee "John Doe"
linear issues update TECH-123 --priority 1

# Add comment
linear issues comment TECH-123 --body "Comment text"

# View comments
linear issues comments TECH-123

# Archive/delete issue
linear issues delete TECH-123
```

### Projects

```bash
linear projects list
linear projects view "Project Name"
linear projects create --name "New Project" --teams TECH,DESIGN
linear projects update "Project Name" --state completed
```

### Teams

```bash
linear teams list
linear teams view TECH
```

### Cycles (Sprints)

```bash
linear cycles list --team TECH
linear cycles current --team TECH
linear cycles view <cycle-id>
linear cycles create --team TECH --starts-at 2024-01-01 --ends-at 2024-01-14
```

### Labels

```bash
linear labels list
linear labels list --team TECH
linear labels create --name "bug" --color "#ff0000"
```

### Users

```bash
linear users list
linear users me
linear users view "User Name"
```

### Workflow States

```bash
linear states list --team TECH
```

## Output Formats

All commands support `--json` for machine-readable output:
```bash
linear issues list --team TECH --json
```

Use `--no-color` to disable colored output.

## Common Patterns

### Find my open issues
```bash
linear issues list --assignee me --state "In Progress"
```

### Create a bug report
```bash
linear issues create --title "Bug: description" --team TECH --priority 2 --labels "bug"
```

### Move issue to done
```bash
linear issues update TECH-123 --state "Done"
```

### Get issue details as JSON for processing
```bash
linear issues view TECH-123 --json
```

### Check current sprint progress
```bash
linear cycles current --team TECH
```

## Priority Levels

- `0` - No priority
- `1` - Urgent
- `2` - High
- `3` - Medium
- `4` - Low

## Tips for Agents

1. **Always check authentication first** before running commands
2. **Use `--json` flag** when you need to parse output programmatically
3. **Team is often required** - ask the user or use `linear teams list` to find available teams
4. **Issue identifiers** (like TECH-123) are preferred over UUIDs for readability
5. **Use `me` as assignee** to refer to the authenticated user
6. **Workflow states vary by team** - use `linear states list --team <TEAM>` to see valid states
