---
name: chrisai-doctor
description: Use when the user explicitly asks to diagnose, verify, inspect, troubleshoot, update, upgrade, pull, install, or sync ChrisAI skills, repository state, validation, or agent adapter targets.
license: MIT
---

# ChrisAI Doctor

Use this skill for explicit ChrisAI maintenance requests. Prefer diagnostics
before mutation, and prefer read-only checks unless the user explicitly asks for
repair, update, install, or sync.

## Workflows

- Use `workflows/health-inspection.md` when the user asks to diagnose, verify,
  inspect, check health, or troubleshoot a ChrisAI installation, version,
  repository checkout, skill validation failure, or agent adapter sync state
  without necessarily changing files.
- Use `workflows/update-and-sync.md` when the user explicitly asks to update,
  upgrade, pull, install, or sync ChrisAI skills from the canonical repository,
  or asks how to update ChrisAI for Codex, Claude Code, or OpenCode.

Do not run sync, update, pull, install, repair, tag, push, or release commands
unless the user explicitly requests that operation.
