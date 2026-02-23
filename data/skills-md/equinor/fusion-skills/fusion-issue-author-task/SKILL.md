---
name: fusion-issue-author-task
description: Draft and update task issues with checklist-first decomposition, dependency-aware sequencing, repository-valid labels, and explicit publish confirmation.
license: MIT
metadata:
  version: "0.1.1"
  orchestrator: "fusion-issue-authoring"
  role: "subordinate"
  tags:
    - github
    - issue-authoring
    - task
  mcp:
    required:
      - github
---

# Author Task Issue

## Dependency

Requires `fusion-issue-authoring` as the top-level orchestrator for classification, shared gates, and publish flow.

## When to use

Use this skill for planning, research, specification, migration, testing, documentation, or other enablement work.

## When not to use

Do not use this skill when the request is clearly a bug, feature, or user-story issue.

## Required inputs

- Task objective and scope
- Dependency and ordering constraints

## Instructions

1. Confirm routed type is `Task`.
2. Start with a concise checklist of small tasks when request is broad.
3. For multi-issue requests, define logical order and blockers before drafting.
4. Draft locally in `.tmp/TASK-<context>.md`.
5. Use appropriate task template variant (planning/research/spec/testing/documentation/generic).
6. Include dependency notes and blocker mapping in the draft.
7. Return draft summary for orchestrator review/publish flow.

Template fallback:
- `skills/fusion-issue-author-task/assets/issue-templates/task.md`
- `skills/fusion-issue-author-task/assets/issue-templates/task.planning.md`
- `skills/fusion-issue-author-task/assets/issue-templates/task.research.md`
- `skills/fusion-issue-author-task/assets/issue-templates/task.spec.md`
- `skills/fusion-issue-author-task/assets/issue-templates/task.ux.md`
- `skills/fusion-issue-author-task/assets/issue-templates/task.testing.md`
- `skills/fusion-issue-author-task/assets/issue-templates/task.documentation.md`

## Expected output

- Checklist (for broad task requests)
- Draft file path in `.tmp/`
- Dependency plan (order + blockers)
- Task-specific decomposition summary

## Safety & constraints

Never create contradictory dependency links.
Always model sequencing before adding blockers.
Do not perform mutation directly; mutation stays in `fusion-issue-authoring`.
