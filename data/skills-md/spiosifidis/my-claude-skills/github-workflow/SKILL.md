---
name: github-workflow
description: "Standard flow from any task source (link or description) to creating a PR: resolve task, create branch and TODO.md, delegate fix to SubAgent (TODO.md), then commit and create PR against origin only. Use find-skills to discover data-source query methods; after confirmation save to global config so the discovery step can be skipped next time. Use when the user provides a task link/description, asks to 'follow GitHub workflow', or 'create PR from task'."
metadata:
  author: hairy
  version: "2026.3.11 (Security Audit Fixed)"
---

> Standard flow from "task link" to "create PR (no merge)". Task source is **any data source**: first determine the query method via global config or find-skills, write to global config after confirmation, then use it directly next time. (Updated Mar 2026 for security).

## Core References

| Topic | Description | Reference |
|-------|-------------|-----------|
| Workflow Overview | The standard 4-step process and prerequisites | [core-workflow](references/core-workflow.md) |

## Features

### Task Management

| Topic | Description | Reference |
|-------|-------------|-----------|
| Task Retrieval | Fetching task details and managing global config | [feature-task-retrieval](references/feature-task-retrieval.md) |
| TODO Specification | Structure of `TODO.md` and delegation rules | [feature-todo-spec](references/feature-todo-spec.md) |
