---
name: agently-session-memory
description: Use when the user needs conversation continuity, memo, or restore-after-restart behavior for a request family, including session ids, chat history, request-side memory boundaries, and session-backed continuity.
---

# Agently Session Memory

Use this skill when the request path already exists but continuity or restore behavior is the main design problem.

## Native-First Rules

- prefer Session-backed continuity before inventing a custom memory layer
- keep request-side chat history and memo boundaries explicit
- separate request memory from workflow runtime state

## Anti-Patterns

- do not use session as a substitute for workflow orchestration state
- do not keep restart-sensitive memory only in transient globals

## Read Next

- `references/overview.md`
