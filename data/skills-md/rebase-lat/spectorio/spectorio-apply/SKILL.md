---
name: spectorio-apply
description: Implement tasks from a spectorio change top-to-bottom. Use when the user says apply, implement, build it, or work through tasks.
compatibility: opencode, claude-code, cursor, codex, windsurf, copilot
license: MIT
metadata:
  version: "0.1.3"
  part-of: spectorio workflow (implementation half of propose → apply → archive)
---

# Spectorio Apply — Implement Tasks

Preconditions: `spectorio-validate` clean; proposal + specs (or `skip_specs=true`) + tasks exist; design present or skipped with reason. Motion/verification/learning/update never block. Gaps → STOP.

## Guide

Follow `apply.md`: workspace `spectorio/references/apply.md` when present,
else the installed `spectorio` router skill's copy (`../spectorio/references/apply.md` from here).

Report completed-this-session + overall `N/M`; suggest `spectorio-verify` (not archive) when done.

Voice throughout: act as the expert developer/product owner in `persona.md` (same workspace-first resolution as the guide above).
