---
name: spec-lifecycle
description: Manages feature spec lifecycle from creation to archival. Use when creating, updating, or completing feature specs in .context/specs/.
version: 1.0.0
---

# Spec Lifecycle

Manages the state machine for feature specs in `.context/specs/`. Keeps the active specs directory clean and ensures completed work is properly archived.

## When to Use This Skill

- Creating a new feature spec
- Updating spec status during development
- Completing and archiving a feature spec
- Reviewing active specs for staleness

## Spec States

```
┌──────────┐     ┌──────────────┐     ┌───────────┐     ┌──────────┐
│ Created  │────▶│ In Progress  │────▶│ Completed │────▶│ Archived │
└──────────┘     └──────────────┘     └───────────┘     └──────────┘
     │                  │                                      ▲
     │                  ▼                                      │
     │           ┌──────────┐                                  │
     └──────────▶│ Blocked  │──────────────────────────────────┘
                 └──────────┘
```

| State | Marker | Location |
|---|---|---|
| Created | `Status: [ ] Not Started` | `.context/specs/` |
| In Progress | `Status: [/] In Progress` | `.context/specs/` |
| Blocked | `Status: [!] Blocked` | `.context/specs/` |
| Completed | `Status: [x] Completed` | `.context/specs/` |
| Archived | *(moved)* | `.context/specs/.archive/` |

## Operations

### Create a Spec
1. Copy `.context/specs/_template.md` to `.context/specs/feat-{name}.md` or `fix-{name}.md`
2. Fill in: Goal, User Story, Requirements
3. Set status to `[ ] Not Started`
4. Set priority and date

**Naming convention:**
- Features: `feat-{short-description}.md` (e.g., `feat-user-auth.md`)
- Bug fixes: `fix-{short-description}.md` (e.g., `fix-payment-timeout.md`)
- Performance: `perf-{short-description}.md` (e.g., `perf-query-optimization.md`)

### Start Work on a Spec
1. Change status marker from `[ ]` to `[/]`
2. Update the `Last Updated` field
3. Ensure the Implementation Plan section is filled in

### Complete a Spec
1. Change status marker from `[/]` to `[x]`
2. Update the `Last Updated` field
3. Verify all acceptance criteria are checked `[x]`
4. **Trigger `context-sync`** to update `project.md`

### Archive a Spec
1. Move the completed spec file to `.context/specs/.archive/`
2. Remove any references to it from active documentation

```bash
git mv .context/specs/feat-{name}.md .context/specs/.archive/
```

## Staleness Detection

A spec is considered **stale** if:
- Status is `[/] In Progress` for more than 14 days without updates
- Status is `[ ] Not Started` for more than 30 days
- Status is `[!] Blocked` with no blocker description

When detected, report:

```
⚠️ STALE SPECS DETECTED:
- feat-dashboard-api.md — In Progress for 21 days (last updated: 2026-01-28)
- fix-cache-invalidation.md — Not Started for 35 days

Recommended action: Review and update or archive these specs.
```

## Dashboard View

When asked for spec status, produce:

```
📋 SPEC DASHBOARD
─────────────────
Active:    2 specs
Blocked:   0 specs
Completed: 1 spec (pending archive)
Archived:  8 specs

ACTIVE SPECS:
  [/] feat-user-auth.md      — Priority: High — 5 days in progress
  [ ] feat-dashboard-api.md  — Priority: Medium — Not started

PENDING ARCHIVE:
  [x] fix-payment-timeout.md — Completed 3 days ago
```
