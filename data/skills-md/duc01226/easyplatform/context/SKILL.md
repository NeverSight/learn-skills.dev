---
name: context
description: '[Planning] Load current project development context'
---

# Load Project Context

Load current development context to help with subsequent tasks.

## Git Status

```bash
git status --short
git branch --show-current
```

## Recent Activity

```bash
# Recent commits
git log --oneline -5

# Uncommitted changes
git diff --stat
```

## Project Structure Reminder

**Backend Services:**

- `TextSnippet` - Example application service
- `Accounts` - Authentication & authorization

**Frontend Apps:**

- `playground-text-snippet` - Example frontend application

**Key Libraries:**

- `platform-core` - Base components (PlatformComponent, stores)
- `apps-domains` - Business domain (APIs, models, validators)
- `platform-core` - UI components & utilities

## Development Patterns

**Backend:** Clean Architecture + CQRS + Entity Events
**Frontend:** Angular 19 + Nx + PlatformVmStore

## Current Session Focus

Based on the git status, identify:

- What files are being worked on
- What feature/fix is in progress
- Any uncommitted changes that need attention

Summarize the current state to help with subsequent tasks.

## IMPORTANT Task Planning Notes

- Always plan and break many small todo tasks
- Always add a final review todo task to review the works done at the end to find any fix or enhancement needed
