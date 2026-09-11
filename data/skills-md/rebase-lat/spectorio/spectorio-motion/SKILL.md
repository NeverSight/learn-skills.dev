---
name: spectorio-motion
description: Explore a vague or risky idea with 3-agent synthesis before committing to a plan. Use when the user says explore, think through, motion, or is unsure how to approach a change.
compatibility: opencode, claude-code, cursor, codex, windsurf, copilot
license: MIT
metadata:
  version: "0.1.3"
  part-of: spectorio workflow (optional explore before propose)
---

# Spectorio Motion — Optional Exploration

Recorded exploration: 3 parallel assessments → synthesis → human picks direction.
Skippable — fast path goes straight to `spectorio-propose`. Planning only — do NOT edit project code.

Preconditions: `spectorio/` workspace exists (`spectorio-new` bootstrap otherwise);
`spectorio/onboarding.md` read as constraints.

## Guide

Follow `motion.md`: workspace `spectorio/references/motion.md` when present,
else the installed `spectorio` router skill's copy (`../spectorio/references/motion.md` from here).

Human picks A/B/C/hybrid (or re-motion). Next: `spectorio-propose`.

Voice throughout: act as the expert developer/product owner in `persona.md` (same workspace-first resolution as the guide above).
