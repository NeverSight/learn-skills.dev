---
name: peer-review
description: Run AI-powered code review of changes by delegating to codex in review mode. Use when the user asks to "review my code", "peer review", "review changes", "review the diff", "review uncommitted changes", or "review against main".
---

# Peer Review

AI-powered code review of changes. Delegates to `/codex` in review mode by default.

## Usage

Determine what to review based on context:

- **Uncommitted changes**: run `/codex` with `--uncommitted`
- **Against a base branch**: run `/codex` with `--base <branch>`
- **Specific commit**: run `/codex` with `--commit <sha>`

Pass `--title` when reviewing a feature branch or PR to give the reviewer context.

Capture and return the full review output.
