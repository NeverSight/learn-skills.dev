---
name: "gitlab-issue"
description: "GitLab issue operations. ALWAYS use this skill when user wants to: (1) list issues, (2) view issue details, (3) create new issues, (4) update/close/reopen issues, (5) add comments/notes to issues."
version: "1.0.0"
author: "GitLab-Assistant-Skills"
license: "MIT"
allowed-tools: ["Bash", "Read", "Glob", "Grep"]
---

# Issue Skill

Issue operations for GitLab using the `glab` CLI.

## Quick Reference

| Operation | Command | Risk |
|-----------|---------|:----:|
| List issues | `glab issue list` | - |
| View issue | `glab issue view <id>` | - |
| Create issue | `glab issue create` | ⚠️ |
| Update issue | `glab issue update <id>` | ⚠️ |
| Close issue | `glab issue close <id>` | ⚠️ |
| Reopen issue | `glab issue reopen <id>` | ⚠️ |
| Delete issue | `glab issue delete <id>` | ⚠️⚠️ |
| Add note | `glab issue note <id>` | ⚠️ |

**Risk Legend**: - Safe | ⚠️ Caution | ⚠️⚠️ Warning | ⚠️⚠️⚠️ Danger

## When to Use This Skill

**ALWAYS use when:**
- User wants to work with issues
- User mentions "issue", "bug", "task", "ticket" or related terms
- User wants to track or manage work items

**NEVER use when:**
- User wants bulk operations on 10+ issues (use gitlab-bulk instead)
- User is only searching/filtering issues (use gitlab-search instead)

## Available Commands

### List Issues

```bash
glab issue list [options]
```

**Options:**
| Flag | Description |
|------|-------------|
| `-a, --assignee=<user>` | Filter by assignee (use @me for yourself) |
| `--author=<user>` | Filter by author |
| `-l, --label=<labels>` | Filter by comma-separated labels |
| `-m, --milestone=<milestone>` | Filter by milestone |
| `-s, --state=<state>` | Filter by state: opened, closed, all (default: opened) |
| `-c, --closed` | Get only closed issues |
| `--all` | Get all issues |
| `-P, --per-page=<n>` | Number of items per page |
| `--confidential` | Filter to only confidential issues |
| `--search=<query>` | Search issues by title/description |

**Examples:**
```bash
# List all open issues
glab issue list

# List issues assigned to you
glab issue list --assignee=@me

# List closed issues
glab issue list --closed

# List issues with specific label
glab issue list --label=bug

# List issues in a milestone
glab issue list --milestone="Release 1.0"

# Search issues
glab issue list --search="login bug"

# Get all issues (paginated)
glab issue list --all
```

### View Issue Details

```bash
glab issue view <id> [options]
```

**Options:**
| Flag | Description |
|------|-------------|
| `-w, --web` | Open issue in browser |
| `-c, --comments` | Show issue comments |
| `-s, --system-logs` | Show system activities |

**Examples:**
```bash
# View issue in terminal
glab issue view 42

# Open issue in browser
glab issue view 42 --web

# View with comments
glab issue view 42 --comments
```

### Create Issue

```bash
glab issue create [options]
```

**Options:**
| Flag | Description |
|------|-------------|
| `-t, --title=<title>` | Issue title |
| `-d, --description=<desc>` | Issue description |
| `-a, --assignee=<users>` | Comma-separated assignees |
| `-l, --label=<labels>` | Comma-separated labels |
| `-m, --milestone=<milestone>` | Milestone title |
| `--confidential` | Create as confidential |
| `--weight=<n>` | Issue weight (0-9) |
| `-w, --web` | Open in browser after creation |
| `-y, --yes` | Skip confirmation prompts |

**Examples:**
```bash
# Create issue with title
glab issue create -t "Fix login bug"

# Create issue with full details
glab issue create -t "Add dark mode" -d "Implement dark mode toggle" -l "enhancement,ui"

# Create issue with milestone and assignee
glab issue create -t "Release prep" -m "Release 2.0" -a "@me"

# Create confidential issue
glab issue create -t "Security vulnerability" --confidential

# Create and open in browser
glab issue create -t "New feature" --web
```

### Update Issue

```bash
glab issue update <id> [options]
```

**Options:**
| Flag | Description |
|------|-------------|
| `-t, --title=<title>` | Update title |
| `-d, --description=<desc>` | Update description |
| `-a, --assignee=<users>` | Update assignees |
| `--unassign` | Remove all assignees |
| `-l, --label=<labels>` | Add labels |
| `--unlabel=<labels>` | Remove labels |
| `-m, --milestone=<milestone>` | Set milestone |
| `--confidential` | Mark as confidential |
| `--public` | Mark as public |
| `--lock-discussion` | Lock discussion |
| `--unlock-discussion` | Unlock discussion |

**Examples:**
```bash
# Update title
glab issue update 42 -t "Updated title"

# Add labels
glab issue update 42 -l "priority,reviewed"

# Remove labels
glab issue update 42 --unlabel="needs-review"

# Change assignee
glab issue update 42 -a "username"

# Add to milestone
glab issue update 42 -m "Sprint 5"
```

### Close/Reopen Issue

```bash
# Close issue
glab issue close <id>

# Reopen issue
glab issue reopen <id>
```

### Delete Issue

```bash
glab issue delete <id>
```

**Warning:** This permanently deletes the issue. Use with caution.

### Add Note/Comment

```bash
glab issue note <id> -m "<message>"
```

**Examples:**
```bash
# Add comment
glab issue note 42 -m "Working on this now"

# Add closing comment
glab issue note 42 -m "Fixed in !123"
```

### Subscribe/Unsubscribe

```bash
# Subscribe to issue notifications
glab issue subscribe <id>

# Unsubscribe
glab issue unsubscribe <id>
```

## Common Workflows

### Workflow 1: Triage Issues

```bash
# 1. List unassigned issues
glab issue list --assignee=""

# 2. View issue details
glab issue view 42

# 3. Assign and label
glab issue update 42 -a "developer" -l "bug,priority"
```

### Workflow 2: Work on Issue

```bash
# 1. Find assigned issues
glab issue list --assignee=@me

# 2. View details
glab issue view 42

# 3. Create branch and work
git checkout -b fix/issue-42

# 4. Add progress note
glab issue note 42 -m "Started work on this"

# 5. Close when MR is merged
glab issue close 42
```

### Workflow 3: Quick Bug Report

```bash
# Create issue with all details
glab issue create \
  -t "Login fails with special characters" \
  -d "Steps to reproduce:
1. Enter username with @ symbol
2. Click login
3. Error: 500

Expected: Login succeeds" \
  -l "bug,login"
```

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| Authentication failed | Invalid/expired token | Run `glab auth login` |
| Issue not found | Invalid ID or no access | Verify ID with `glab issue list` |
| Permission denied | Insufficient rights | Check project permissions |
| Cannot close | Issue is locked | Request unlock from maintainer |

## Related Documentation

- [Safeguards](../shared/docs/SAFEGUARDS.md)
- [Quick Reference](../shared/docs/QUICK_REFERENCE.md)
