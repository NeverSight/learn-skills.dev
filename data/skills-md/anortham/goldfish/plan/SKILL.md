---
name: plan
description: Create and manage persistent plans in Goldfish memory — for tracking multi-session strategic direction
allowed-tools: mcp__goldfish__plan
---

# Plan — Persistent Strategic Plans

## The Golden Rule

Plans capture strategic direction that must survive across sessions. When you start multi-session work or make architectural decisions, SAVE A PLAN. When work is done, MARK IT COMPLETE. Stale plans are worse than no plans.

## When to Create a Plan

### MANDATORY:
- **Starting multi-session work** — save a plan NOW with goals and approach
- **After architectural decisions** — save a plan NOW so future sessions know the direction
- **After brainstorming/design sessions** — capture the approved design as a plan

### Good habit:
- When starting a new feature that will span multiple sessions
- When the user describes a project direction or roadmap
- When you need to track progress across context compactions

## How to Create a Plan

```
mcp__goldfish__plan({
  action: "save",
  title: "Auth System Overhaul",
  content: "## Goals\n\n- Migrate from session tokens to JWT...\n\n## Approach\n\n...\n\n## Tasks\n\n- [ ] Task 1\n- [ ] Task 2",
  tags: ["feature", "auth"],
  activate: true
})
```

### Plan Content Structure

Structure your plan content with clear sections:

1. **Goals** — what are we trying to achieve?
2. **Approach** — how are we going to do it?
3. **Tasks** — checklist of deliverables (use `- [ ]` / `- [x]`)
4. **Constraints** — anything we need to avoid or work around

### Key Parameters

- **activate: true** — ALWAYS set this unless you have a specific reason not to. The active plan shows at the top of every `recall()` response, keeping future sessions oriented.
- **tags** — categorize for search. Use consistent tags across checkpoints and plans.
- **id** — auto-generated from title. Only override if you need a specific slug.

## Managing Plan Lifecycle

### Check current plans
```
mcp__goldfish__plan({ action: "list" })
```

### Update a plan (add progress, change scope)
```
mcp__goldfish__plan({
  action: "update",
  id: "auth-system-overhaul",
  updates: {
    content: "## Goals\n\n...(updated content with progress noted)..."
  }
})
```

### Mark a plan complete — NEVER SKIP THIS
```
mcp__goldfish__plan({ action: "complete", id: "auth-system-overhaul" })
```

### Archive a superseded plan
```
mcp__goldfish__plan({
  action: "update",
  id: "old-plan",
  updates: { status: "archived" }
})
```

## The Active Plan

Only ONE plan can be active per workspace. The active plan:
- Appears at the top of every `recall()` response
- Guides all work in the project
- Should reflect the current strategic direction

If priorities shift, either update the active plan or archive it and create a new one.

## Critical Rules

- **ALWAYS activate plans.** An inactive plan is invisible to future sessions.
- **ALWAYS mark plans complete when done.** Stale active plans mislead every future session into thinking work is still in progress.
- **NEVER leave orphaned active plans.** If a plan is done or abandoned, complete or archive it.
- **Update plans as work progresses.** Check off tasks, note scope changes, record decisions.
- **Plans are NOT checkpoints.** Plans are forward-looking strategy. Checkpoints are backward-looking history. Use both.
