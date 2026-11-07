---
name: detect-stack
description: Analyze a codebase to detect its language, framework, conventions, and CI gates. Run this on first use in a project to generate stack context that all coding principle skills reference. Use when the user says "detect stack," "analyze this project," or "what's this codebase using."
metadata:
  version: 1.0.0
---

# Detect Stack

Analyze the current codebase and generate `.agents/stack-context.md`. Run this on first use in a project, or when the stack context is missing or stale.

## What to Detect

Scan the project root for these signals:

**Language** — Count file extensions (`.rs`, `.py`, `.ts`, `.go`, `.swift`, `.java`, `.rb`, `.cs`, `.ex`, etc.). Primary = most files. Note secondary languages.

**Framework** — Read the package manifest:
- `Cargo.toml` → check `[dependencies]` for axum, actix, rocket, sqlx, diesel, tokio
- `package.json` → check for react, next, svelte, express, fastify, prisma
- `go.mod` → check for gin, echo, fiber, chi, sqlc
- `pyproject.toml` / `requirements.txt` → check for django, flask, fastapi, sqlalchemy
- `Gemfile` → check for rails, sinatra
- `Package.swift` → check for Vapor; scan for SwiftUI imports
- `mix.exs` → check for phoenix, ecto

**Tests** — Look for test directories, test file naming patterns, test config files.

**CI gates** — Scan `.github/workflows/`, `.gitlab-ci.yml`, etc. for blocking checks (format, lint, type check, test).

**Conventions** — Check for `CLAUDE.md`, `AGENTS.md`, `CONTRIBUTING.md`. Note directory structure and naming patterns.

## Output

Write `.agents/stack-context.md` — keep it short (under 40 lines):

```markdown
# Stack Context

Generated: YYYY-MM-DD

## Stack
- **Language**: [primary] [version if pinned]
- **Framework**: [web framework], [db layer]
- **Build**: [build tool]
- **Test**: [test command + framework]
- **Lint**: [linter] [CI gate: yes/no]
- **Format**: [formatter] [CI gate: yes/no]

## Secondary Languages
- [language] ([what it's used for])

## Conventions
- Error handling: [pattern]
- Module structure: [pattern]
- Naming: [pattern]
- Tests: [where they live, how they're organized]

## CI Gates
- [list of blocking checks]
```

## Stack-Specific Principle Application

After writing the stack context, **do not generate static reference files**. Instead:

1. Use your built-in knowledge of the detected language/framework to apply each coding principle idiomatically
2. If you need specific framework API details, use **context7 MCP** (`resolve-library-id` then `query-docs`) to pull live documentation
3. If context7 doesn't cover it, use **web search** as fallback

The coding principle skills are language-agnostic by design. You are the bridge between the principles and the stack.

## When to Re-Run

- `.agents/stack-context.md` doesn't exist
- Major dependency changes (new framework, language version bump)
- Project structure significantly changes
- Context file is older than 30 days
