---
name: spectorio-sync
description: Merge a change's delta specs into living specs without archiving. Use when the user says sync, merge specs, update main specs, or when a parallel change builds on these specs.
compatibility: opencode, claude-code, cursor, codex, windsurf, copilot
license: MIT
metadata:
  version: "0.1.3"
  part-of: spectorio workflow (merge deltas; change stays active)
---

# Spectorio Sync — Merge Deltas Without Archiving

Merge delta specs into living specs; the change stays active. Use when main specs should update before archiving, when a parallel change builds on these specs, or to review the merged result first.

## Guide

Follow `sync.md`: workspace `spectorio/references/sync.md` when present,
else the installed `spectorio` router skill's copy (`../spectorio/references/sync.md` from here).
Confirm `spectorio-validate` is clean first; mismatch → report the diff, STOP.

Next: `spectorio-archive` when finished, or `spectorio-apply` if code must catch up.

Voice throughout: act as the expert developer/product owner in `persona.md` (same workspace-first resolution as the guide above).
