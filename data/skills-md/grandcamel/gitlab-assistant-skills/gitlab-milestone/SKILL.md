---
name: "gitlab-milestone"
description: "GitLab milestone operations. ALWAYS use this skill when user wants to: (1) list milestones, (2) create new milestones, (3) manage sprints or iterations."
version: "1.0.0"
author: "GitLab-Assistant-Skills"
license: "MIT"
allowed-tools: ["Bash", "Read", "Glob", "Grep"]
---

# Milestone Skill

Milestone management operations for GitLab using the `glab` CLI.

## Quick Reference

| Operation | Command | Risk |
|-----------|---------|:----:|
| List milestones | `glab milestone list` | - |
| Create milestone | `glab milestone create <title>` | ⚠️ |

**Risk Legend**: - Safe | ⚠️ Caution | ⚠️⚠️ Warning | ⚠️⚠️⚠️ Danger

## When to Use This Skill

**ALWAYS use when:**
- User wants to manage project milestones
- User mentions "milestone", "sprint", "iteration", "release planning"
- User wants to organize work into time-boxed periods

**NEVER use when:**
- User wants to assign milestones to issues (use gitlab-issue)
- User wants to create releases (use gitlab-release)

## Available Commands

### List Milestones

```bash
glab milestone list [options]
```

**Options:**
| Flag | Description |
|------|-------------|
| `-s, --state=<state>` | Filter by state: active, closed, all |
| `-P, --per-page=<n>` | Results per page |
| `--all` | Get all milestones |

**Examples:**
```bash
# List active milestones
glab milestone list

# List all milestones including closed
glab milestone list --state=all

# List closed milestones
glab milestone list --state=closed

# List with more results
glab milestone list --per-page=50
```

### Create Milestone

```bash
glab milestone create <title> [options]
```

**Options:**
| Flag | Description |
|------|-------------|
| `-d, --description=<desc>` | Milestone description |
| `--due-date=<date>` | Due date (YYYY-MM-DD format) |
| `--start-date=<date>` | Start date (YYYY-MM-DD format) |

**Examples:**
```bash
# Create simple milestone
glab milestone create "Sprint 1"

# Create with description
glab milestone create "Q1 Release" \
  -d "Features planned for Q1 2024 release"

# Create with dates
glab milestone create "Sprint 5" \
  --start-date=2024-02-01 \
  --due-date=2024-02-14 \
  -d "Two-week sprint"

# Create release milestone
glab milestone create "v2.0.0" \
  --due-date=2024-03-15 \
  -d "Major version 2.0 release"
```

## Common Workflows

### Workflow 1: Sprint Planning

```bash
# 1. Create new sprint milestone
glab milestone create "Sprint 12" \
  --start-date=2024-03-01 \
  --due-date=2024-03-14 \
  -d "Sprint 12 goals:
- Complete authentication feature
- Fix critical bugs
- Improve test coverage"

# 2. Assign issues to milestone
glab issue update 101 -m "Sprint 12"
glab issue update 102 -m "Sprint 12"
glab issue update 103 -m "Sprint 12"

# 3. View sprint issues
glab issue list --milestone="Sprint 12"
```

### Workflow 2: Release Planning

```bash
# 1. List current milestones
glab milestone list

# 2. Create release milestone
glab milestone create "Release 1.5" \
  --due-date=2024-04-01 \
  -d "Version 1.5 release including:
- New dashboard
- Performance improvements
- Bug fixes from user feedback"

# 3. Associate issues
glab issue list --label="release-1.5" | while read issue; do
  glab issue update $issue -m "Release 1.5"
done
```

### Workflow 3: Review Sprint Progress

```bash
# 1. List sprint milestones
glab milestone list --state=active

# 2. Check open issues in sprint
glab issue list --milestone="Sprint 12" --state=opened

# 3. Check closed issues
glab issue list --milestone="Sprint 12" --state=closed

# 4. Check MRs in sprint
glab mr list --milestone="Sprint 12"
```

## Milestone Naming Conventions

Common patterns for milestone names:

| Pattern | Example | Use Case |
|---------|---------|----------|
| Sprint N | Sprint 1, Sprint 2 | Agile sprints |
| YYYY-QN | 2024-Q1, 2024-Q2 | Quarterly planning |
| vX.Y.Z | v1.0.0, v2.1.0 | Version releases |
| YYYY-MM | 2024-03, 2024-04 | Monthly cycles |
| Feature Name | "User Authentication" | Feature-based milestones |

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| Authentication failed | Invalid/expired token | Run `glab auth login` |
| Milestone not found | Wrong name or closed | Check with `glab milestone list --state=all` |
| Invalid date | Wrong format | Use YYYY-MM-DD format |
| Permission denied | Not maintainer | Need maintainer+ role |

## Related Documentation

- [Safeguards](../shared/docs/SAFEGUARDS.md)
- [Quick Reference](../shared/docs/QUICK_REFERENCE.md)
