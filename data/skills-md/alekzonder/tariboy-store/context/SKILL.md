---
name: context
description: Use when an agent needs to read or replace its durable Tariboy iteration handoff.
---

# Context

**REQUIRED:** Use `cli-text` before passing text to this CLI. Keep the storage
rules below; quote transport separately. Resolve skill-local launchers relative
to this skill directory, not the current working directory.

Resolve `scripts/context.sh` from this skill's directory, not from the agent's
working directory.

- Run `scripts/context.sh get` to read the durable handoff.
- Run `scripts/context.sh set "text"` to replace the entire handoff.

The handoff contains only actionable state, decisions, and blockers needed by
the next iteration. Omit command logs, chronological diaries, transcripts, and
internal reasoning. If a request supplies no new actionable information, leave
the existing handoff unchanged; do not store an explanation of what was
excluded.
