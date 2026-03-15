---
name: frontend-docs-context7
description: Use this skill when users ask for frontend library/framework usage, APIs, best practices, or examples (e.g. Vue, Vite, React, Tailwind). Always fetch up-to-date docs with Context7.
metadata:
  author: IceyWu
  homepage: https://github.com/IceyWu
  version: "0.1.0"
  source: https://github.com/IceyWu/skills
---

# Frontend Docs via Context7

Use this skill for documentation-driven questions, not for run/open/preview workflows.

## 1. Trigger

Apply this skill when user asks about package/framework:

- usage patterns
- API details
- best practices
- migration/version differences
- code examples from official docs

## 2. Required Flow

1. Call `mcp_io_github_ups_resolve-library-id` with the library name.
2. Call `mcp_io_github_ups_get-library-docs` with the resolved ID.
3. Answer based on fetched docs; avoid relying only on memory.

## 3. Scope Notes

- Prefer this skill for frontend ecosystem docs (Vue/Vite/React/Tailwind and related tools).
- If the request is actually about running/opening/debugging a project, use `frontend-dev-tools` instead.
