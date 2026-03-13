---
name: adk-cheatsheet
description: >
  MUST READ before writing or modifying ADK agent code.
  ADK API quick reference for Python — agent types, tool definitions,
  orchestration patterns, callbacks, and state management.
  Includes an index of all ADK documentation pages.
  Do NOT use for creating new projects (use adk-scaffold).
metadata:
  author: Google
  version: 0.2.0
  managed-by: adk-skills-setup
---

# ADK Cheatsheet

> **Python only for now.** This cheatsheet currently covers the Python ADK SDK.
> Support for other languages is coming soon.

## Reference Files

| File | Contents |
|------|----------|
| `references/python.md` | Python ADK API quick reference — agents, tools, auth, orchestration, callbacks, plugins, state, artifacts, context caching/compaction, session rewind |
| `references/docs-index.md` | ADK docs index (fetched from llms.txt at setup time) — titles and WebFetch URLs. If missing, fetch directly: `WebFetch: https://google.github.io/adk-docs/llms.txt`. **Gemini CLI tip:** use `curl` instead of WebFetch for faster doc fetches. |

Read `references/python.md` for the full API quick reference.

> **Creating a new agent project?** Use `/adk-scaffold` instead — this skill is for writing code in existing projects.
