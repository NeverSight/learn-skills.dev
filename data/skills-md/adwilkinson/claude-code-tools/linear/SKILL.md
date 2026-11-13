---
name: linear
author: Andrew Wilkinson (github.com/ADWilkinson)
description: Manage Linear tasks and issues. Use when the user mentions Linear, tasks, issues, tickets, backlog, sprints, or wants to create/view/update work items.
allowed-tools:
  - Bash
  - Read
  - Write
  - mcp__linear__list_issues
  - mcp__linear__get_issue
  - mcp__linear__create_issue
  - mcp__linear__update_issue
  - mcp__linear__list_comments
  - mcp__linear__create_comment
  - mcp__linear__list_teams
  - mcp__linear__get_user
---

# Linear Task Manager

Simple Linear integration for daily task management.

## Tool Selection Strategy

**IMPORTANT: Prefer Linear MCP tools when available.**

1. **Check for MCP first**: If `mcp__linear__*` tools are available, use them directly
2. **Fall back to CLI**: Only use the bash script if MCP tools are unavailable

### Using MCP Tools (Preferred)

When MCP tools are available, use them directly:

```
# List my tasks
mcp__linear__list_issues with assignee="me", state type != "completed" or "canceled"

# Get issue details
mcp__linear__get_issue with id="ISSUE-ID"

# Create issue
mcp__linear__create_issue with title, team, assignee="me"

# Update issue state
mcp__linear__update_issue with id, state="Done" or "In Progress"

# Add comment
mcp__linear__create_comment with issueId, body
```

### Using CLI Fallback

Only use when MCP is unavailable.

## Setup (CLI Fallback Only)

The CLI requires an API key. Check if configured:

```bash
[ -n "$LINEAR_API_KEY" ] && echo "Linear configured" || echo "Set LINEAR_API_KEY in your shell profile"
```

If not configured, tell the user to add to `~/.zshrc`:
```bash
export LINEAR_API_KEY="lin_api_..."
```

Get key from: Linear → Settings → Security & access → Personal API keys

## CLI Operations (Fallback)

### View My Tasks

```bash
npx tsx ~/.claude/skills/linear/scripts/linear.ts my-tasks
npx tsx ~/.claude/skills/linear/scripts/linear.ts my-tasks --label "frontend"
```

### View In Progress

```bash
npx tsx ~/.claude/skills/linear/scripts/linear.ts in-progress
```

### View Backlog

```bash
npx tsx ~/.claude/skills/linear/scripts/linear.ts backlog
npx tsx ~/.claude/skills/linear/scripts/linear.ts backlog --label "tech-debt"
```

### View All Team Tasks

```bash
npx tsx ~/.claude/skills/linear/scripts/linear.ts team-tasks
npx tsx ~/.claude/skills/linear/scripts/linear.ts team-tasks --label "urgent"
```

### Search Issues

```bash
npx tsx ~/.claude/skills/linear/scripts/linear.ts search "rebrand"
npx tsx ~/.claude/skills/linear/scripts/linear.ts search "auth" --label "security"
```

### Create Task (Assigned to Me)

```bash
npx tsx ~/.claude/skills/linear/scripts/linear.ts create "Task title" --assignee me
```

### Create Backlog Item (Unassigned)

```bash
npx tsx ~/.claude/skills/linear/scripts/linear.ts create "Task title"
```

### Complete a Task

```bash
npx tsx ~/.claude/skills/linear/scripts/linear.ts done ISSUE-ID
```

### Start Working on Task

```bash
npx tsx ~/.claude/skills/linear/scripts/linear.ts start ISSUE-ID
```

### View Specific Issue

```bash
npx tsx ~/.claude/skills/linear/scripts/linear.ts show ISSUE-ID
```

### Add Comment

```bash
npx tsx ~/.claude/skills/linear/scripts/linear.ts comment ISSUE-ID "Comment text"
```

## Filtering

All list commands support the `--label` flag for filtering:

```bash
# Filter my tasks by label
my-tasks --label "frontend"

# Search with label filter
search "bug" --label "critical"

# Team tasks with label
team-tasks --label "reskin"
```

Label matching is case-insensitive and partial (e.g., `--label front` matches "frontend").

## State Conventions

| Scenario | State |
|----------|-------|
| Assigned to me | Todo |
| Unassigned | Backlog |
| Started work | In Progress |
| Completed | Done |

## Natural Language Mapping

| User says | Action |
|-----------|--------|
| "show my tasks" / "what's on my plate" | `my-tasks` |
| "what am I working on" | `in-progress` |
| "show my backlog" | `backlog` |
| "show all team tasks" | `team-tasks` |
| "search for rebrand tasks" | `search "rebrand"` |
| "find frontend issues" | `my-tasks --label "frontend"` |
| "create task: X" / "add task X" | `create "X" --assignee me` |
| "add to backlog: X" | `create "X"` |
| "done with X" / "complete X" / "finished X" | `done X` |
| "start X" / "working on X" | `start X` |
| "show X" / "details on X" | `show X` |

## Output Format

Task lists show a clean table with issue count:

```
ID         | Title                                              | State        | Priority
-----------|----------------------------------------------------|--------------|---------
ENG-123    | Fix login bug causing session timeout              | In Progress  | High
ENG-124    | Update documentation for new API endpoints         | Todo         | Medium

2 issues found.
```

Team tasks and search results include an Assignee column.

## Error Handling

If LINEAR_API_KEY is missing, respond with setup instructions.
If an issue ID doesn't exist, say so clearly.
If the API fails, show the error and suggest checking the API key.
