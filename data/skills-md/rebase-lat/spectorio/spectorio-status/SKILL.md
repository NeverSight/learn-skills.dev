---
name: spectorio-status
description: Answer "now what?" for a spectorio project — scan changes, report state, and recommend the next step. Use when the user says status, now what, where were we, next step, resume, or returns to a stale or pending implementation.
compatibility: opencode, claude-code, cursor, codex, windsurf, copilot
license: MIT
metadata:
  version: "0.1.3"
  part-of: spectorio workflow (orientation — read-only, never starts the next step)
---

# Spectorio Status — Now What?

Orientation only: scan the workspace, report per-change state, recommend the next
step. Read-only — never scaffold, plan, implement, or archive. Never start the
recommended step unprompted; state it and wait.

If `spectorio/` workspace is missing → stop and point at `spectorio-new`
bootstrap (or run it when shell access allows). If `spectorio/onboarding.md` is
missing → the recommendation is `spectorio-onboard`.

## Guide

Follow `status.md`: workspace `spectorio/references/status.md` when present,
else the installed `spectorio` router skill's copy (`../spectorio/references/status.md` from here).

Close with a single recommended next command per change (plus a one-line
alternative). Then stop and wait for the human's pick.

Voice throughout: act as the expert developer/product owner in `persona.md` (same workspace-first resolution as the guide above).
