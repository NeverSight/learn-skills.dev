---
name: agent-mail
displayName: Agent Mail (Alias)
description: >-
  Backward-compatible alias for the canonical clawmail protocol. Use when older
  prompts mention 'agent-mail'. For full, current coordination rules load the
  `clawmail` skill.
version: 1.0.0
author: joel
tags:
  - coordination
  - alias
  - protocol
---

# Agent Mail (Alias)

This skill is kept for compatibility with older prompts and habits.

**Canonical source of truth is now `skills/clawmail/SKILL.md`.**

## Use This Skill When
- a prompt explicitly asks for `agent-mail`
- you need to bridge old instructions to current protocol

## Current Rules (summary)
1. Mail access in pi goes through **`joelclaw mail`** (wrappers are fine).
2. Check inbox before starting shared work.
3. Announce scope (`Starting:`), reserve paths, send status updates, release locks.
4. Include file paths and task context in every coordination message.

## Immediate Redirect
Load and follow:
- `skills/clawmail/SKILL.md`

## Related
- ADR-0172: Agent Mail via MCP Agent Mail
- `joelclaw mail --help`
