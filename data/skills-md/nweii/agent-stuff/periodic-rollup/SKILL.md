---
name: periodic-rollup
description: "Roll up vault content into consolidated notes. History rollup: compile periodic note mentions of a project/topic into a Histories note. Periodic rollup: synthesize child note descriptions into a parent periodic note's description."
argument-hint: "[[Project or topic]] [timespan] | [periodic note title]"
metadata:
  author: nweii
  version: "1.0.0"
  internal: true
---

# Vault rollups

Today's daily note: !`obsidian daily:path`

Two operations for aggregating periodic note content into consolidated artifacts. Determine which to run based on what's asked:

| Operation       | When to use                                                                            | Reference                                                      |
| --------------- | -------------------------------------------------------------------------------------- | -------------------------------------------------------------- |
| History rollup  | "Roll up history for [[Project]]", "compile mentions of [[Topic]]"                     | [references/history-rollup.md](references/history-rollup.md)   |
| Periodic rollup | "Roll up my weekly", "summarize this quarter", "generate description for [[2026-W07]]" | [references/periodic-rollup.md](references/periodic-rollup.md) |

If $ARGUMENTS is provided, use it to identify the project, topic, or periodic note to target. If ambiguous between the two operations, ask before proceeding.

## Shared workflow

Both operations follow the same pattern:

1. **Gather** — Search for source notes using obsidian CLI or MCP vault search
2. **Synthesize** — Process gathered content according to the operation's rules
3. **Write** — Produce or update the output note

## Shared principles

- Preserve source wikilinks back to origin notes for traceability
- Respect the hierarchy: daily → weekly → quarterly → yearly
- Preserve detail in archives; don't summarize what should be kept verbatim
- Update `related` properties bidirectionally when creating new notes
