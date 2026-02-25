---
name: platforma-guidelines
description: Guidance for building backend Go applications with github.com/platforma-dev/platforma. Use when asked to design Platforma project structure, choose or combine Platforma packages (application, database, httpserver, auth, queue, scheduler), explain or run framework-native CLI commands, or provide practical integration examples and migration/run workflows.
---

# Platforma Guidelines

Use this skill to deliver accurate, practical Platforma backend guidance with minimal theory and directly usable commands/snippets.

## Triage Checklist

1. Identify request type: project structure, CLI usage, package integration, or troubleshooting.
2. Confirm target outcome: scaffold app, add package, fix runtime behavior, or explain command workflow.
3. Open only the reference file(s) needed for the request.

## Reference Routing

- Use `references/consumer-project-structure.md` for app folder layout and file responsibilities.
- Use `references/cli-commands.md` for framework-native CLI commands and runtime command semantics.

## Workflow

1. Restate the requested outcome in Platforma backend terms.
2. Select the smallest set of packages needed (`application`, `database`, `httpserver`, `auth`, `queue`, `scheduler`).
3. Provide minimal runnable code with exact imports and registration order.
4. Provide exact commands and explicit execution sequence (`migrate` before `run` when migrations exist).
5. Call out one or two high-impact pitfalls relevant to the task.

## Rules

- Prefer source code, package docs and repository docs as source of truth over assumptions.
