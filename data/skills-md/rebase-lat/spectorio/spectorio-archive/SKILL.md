---
name: spectorio-archive
description: Finalize a change with changelog entry and move to archive. Use when the user says archive, finalize, close out, or finish a change.
compatibility: opencode, claude-code, cursor, codex, windsurf, copilot
license: MIT
metadata:
  version: "0.1.3"
  part-of: spectorio workflow (final step of propose → apply → archive)
---

# Spectorio Archive — Finalize a Change

Strictness per `conventions.md` §6 in the `spectorio` router skill: default
warn-and-confirm on gaps (validation failure still refuses); STRICT BLOCK only
when `strict_archive=true`.

## Guide

Follow `archive.md`: workspace `spectorio/references/archive.md` when present,
else the installed `spectorio` router skill's copy (`../spectorio/references/archive.md` from here).
`spectorio-validate` clean first; mismatch on sync-verify → report diff, STOP.

Summary when done: archived path, sync status, changelog entry.

Voice throughout: act as the expert developer/product owner in `persona.md` (same workspace-first resolution as the guide above).
