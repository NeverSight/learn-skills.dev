---
name: spectorio-propose
description: Draft a change proposal with delta specs, design, and tasks. Use when the user says propose, plan, spec out, design, or names a feature/refactor/migration to specify.
compatibility: opencode, claude-code, cursor, codex, windsurf, copilot
license: MIT
metadata:
  version: "0.1.3"
  part-of: spectorio workflow (planning half of propose → apply → archive)
---

# Spectorio Propose — Planning Artifacts

Create planning artifacts in dependency order. **Planning only means planning only** —
never edit project code; wait for an explicit apply request (`spectorio-apply`).

Preconditions: change scaffolded (`spectorio-new`); `spectorio/onboarding.md` exists
(`spectorio-onboard` otherwise). Vague/risky request? Explore first (`spectorio-motion`).
New dep mid-planning? Amend onboarding first (`spectorio-onboard` Flow B), then resume.

## Guide

Follow `propose.md`: workspace `spectorio/references/propose.md` when present,
else the installed `spectorio` router skill's copy (`../spectorio/references/propose.md` from here).

Next: `spectorio-validate`, then `spectorio-apply` on explicit request.

Voice throughout: act as the expert developer/product owner in `persona.md` (same workspace-first resolution as the guide above).
