---
name: backlog-manager
description: Manage backlog items across multiple backends (GitHub Issues, Linear, Beads). Configure task_management in .agents.yml.
disable-model-invocation: true
---

# Backlog Manager Skill

## Overview

The backlog manager provides a unified interface for tracking work items across different task management systems. Choose your backend based on team preferences and existing tooling.

**Supported Backends:**

| Backend | Integration | Best For |
|---------|-------------|----------|
| **GitHub** | `gh` CLI | Teams using GitHub Issues |
| **Linear** | MCP server | Teams using Linear |
| **Beads** | `bd` CLI | Dependency-aware workflows, AI agents |

**For simple/solo projects:** Use native Tasks (`TaskCreate`, `TaskList`, `TaskUpdate`) instead of backlog-manager.

## Configuration

Configure your preferred backend in your project's `.agents.yml`:

```yaml
task_management: github  # Options: github, linear, beads

# Workflow labels (for github/linear backends)
workflow_labels:
  - backlog
  - in-progress
  - ready-for-review
  - done

# Beads configuration (when task_management: beads)
# beads_prefix: myapp               # Optional: custom issue prefix
```

**Default:** If no configuration is found, use native Tasks (`TaskCreate`, `TaskList`, `TaskUpdate`) for simple tracking.

## When to Use This Skill

**Create a backlog item when:**
- Work requires more than 15-20 minutes
- Needs research, planning, or multiple approaches considered
- Has dependencies on other work
- Requires approval or prioritization
- Part of larger feature or refactor
- Technical debt needing documentation

**Act immediately instead when:**
- Issue is trivial (< 15 minutes)
- Complete context available now
- No planning needed
- User explicitly requests immediate action
- Simple bug fix with obvious solution

## Core Concepts

### Status Lifecycle

All backends follow this status workflow:

```
pending → ready → complete
```

| Status | Meaning |
|--------|---------|
| **pending** | Needs triage/approval before work begins |
| **ready** | Approved and ready for implementation |
| **complete** | Work finished, acceptance criteria met |

### Priority Levels

| Priority | Meaning |
|----------|---------|
| **p1** | Critical - blocks other work or users |
| **p2** | Important - should be done soon |
| **p3** | Nice-to-have - can wait |

### Core Operations

Each backend implements these operations:

| Operation | Purpose |
|-----------|---------|
| **CREATE** | Add new backlog item |
| **LIST** | Query existing items |
| **UPDATE** | Modify item (status, priority, details) |
| **COMPLETE** | Mark item as done |

## Backend Selection

When this skill is invoked:

1. **Read configuration** from project CLAUDE.md
2. **Load appropriate reference** based on `backend` setting:
   - `github` → `references/github-backend.md`
   - `linear` → `references/linear-backend.md`
   - `beads` → `references/beads-backend.md`
3. **Follow backend-specific instructions** for operations

### Fallback Behavior

If the configured backend is unavailable:
- **GitHub unavailable** (gh not authenticated): Fall back to native Tasks
- **Linear unavailable** (MCP not configured): Fall back to native Tasks
- **Beads unavailable** (bd not installed or not initialized): Fall back to native Tasks
- **Warn user** about the fallback

## Integration with Development Workflows

| Trigger | Flow |
|---------|------|
| Code review findings | Review → Create items → Triage → Work |
| PR comments | Resolve PR → Create items for complex fixes |
| Planning sessions | Brainstorm → Create items → Prioritize → Work |
| Technical debt | Document → Create item → Schedule |
| Feature requests | Analyze → Create item → Prioritize |

## Key Distinctions

**Backlog manager (this skill):**
- Persisted tracking across sessions
- Multiple backend options
- Team collaboration
- Project/sprint planning

**Native Tasks (TaskCreate, TaskList, TaskUpdate):**
- Session task tracking with file persistence (`~/.claude/tasks/`)
- Supports dependencies (`blockedBy`, `blocks`)
- Can be shared across sessions via `CLAUDE_CODE_TASK_LIST_ID` env var
- Use for: in-session progress tracking, subagent coordination, simple task lists
- Different from backlog manager: Tasks are ephemeral coordination, backlog is project planning
