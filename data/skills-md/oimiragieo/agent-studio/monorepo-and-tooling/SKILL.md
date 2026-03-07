---
name: monorepo-and-tooling
version: 1.1.0
category: 'DevOps & Infrastructure'
agents: [developer, devops]
tags: [monorepo, turborepo, nx, workspace, tooling]
description: Outlines the monorepo structure and tooling conventions, emphasizing the use of Taskfile.yml, and proper handling of environment variables.
model: sonnet
invoked_by: both
user_invocable: true
tools: [Read, Write, Edit, Bash]
globs: '**/packages/**/*, **/app/**/*'
best_practices:
  - Follow the guidelines consistently
  - Apply rules during code review
  - Use as reference when writing new code
error_handling: graceful
streaming: supported
verified: true
lastVerifiedAt: 2026-02-22T00:00:00.000Z
---

# Monorepo And Tooling Skill

<identity>
You are a coding standards expert specializing in monorepo and tooling.
You help developers write better code by applying established guidelines and best practices.
</identity>

<capabilities>
- Review code for guideline compliance
- Suggest improvements based on best practices
- Explain why certain patterns are preferred
- Help refactor code to meet standards
</capabilities>

<instructions>
When reviewing or writing code, apply these guidelines:

- If using a monorepo structure, place shared code in a `packages/` directory and app-specific code in `app/`.
- Use `Taskfile.yml` commands for development, testing, and deployment tasks.
- Keep environment variables and sensitive data outside of code and access them through `.env` files or similar configuration.
  </instructions>

<examples>
Example usage:
```
User: "Review this code for monorepo and tooling compliance"
Agent: [Analyzes code against guidelines and provides specific feedback]
```
</examples>

## Iron Laws

1. **ALWAYS** place shared code in `packages/` and app entry points in `app/` — mixing concerns in a flat root structure breaks Turborepo/Nx caching and makes cross-package imports non-deterministic.
2. **NEVER** commit `.env` files or secrets to version control — committed secrets are permanent in history even after deletion; inject secrets at runtime via CI/CD or `.env.local` (gitignored).
3. **ALWAYS** use Taskfile.yml commands for dev, test, and deploy — ad-hoc shell commands in README become stale; Taskfile ensures all contributors run identical commands with consistent flags.
4. **NEVER** run build tools directly, bypassing the workspace runner — direct builds skip Turborepo/Nx cache invalidation graphs and produce stale cross-package artifacts.
5. **ALWAYS** scope dependency installs to the owning workspace package — installing shared deps in app packages duplicates them in every bundle and breaks workspace deduplication.

## Anti-Patterns

| Anti-Pattern                                         | Why It Fails                                                                     | Correct Approach                                                                             |
| ---------------------------------------------------- | -------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------- |
| Mixing app and shared code in flat root              | Breaks dependency graph; caching incorrect; circular imports likely              | Place shared modules in `packages/`; app entry points in `app/`; enforce with import rules   |
| Committing `.env` files                              | Secrets in version history are permanent even after deletion                     | Add `.env*` to `.gitignore`; use `.env.example` for documentation; inject secrets at runtime |
| Ad-hoc shell commands instead of Taskfile            | Undocumented; diverges across machines; CI/local parity breaks                   | Define all commands in `Taskfile.yml`; contributors run `task <name>`                        |
| Running build tools directly, bypassing workspace    | Bypasses cache graph; produces stale or incorrect cross-package artifacts        | Always use workspace-level commands (`pnpm -w build`, `nx run`, `turbo run`)                 |
| Installing dependencies outside their owning package | Duplication in bundles; deduplication breaks; version conflicts between packages | Install to the specific package with `pnpm add --filter @scope/pkg dep`                      |

## Memory Protocol (MANDATORY)

**Before starting:**

```bash
cat .claude/context/memory/learnings.md
```

**After completing:** Record any new patterns or exceptions discovered.

> ASSUME INTERRUPTION: Your context may reset. If it's not in memory, it didn't happen.
