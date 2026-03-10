---
name: retro
description: "Run, write, generate, record, save, persist, and synthesize agent retrospectives and lessons learned after completing tasks. Self-assess session quality, identify mistakes, extract reusable patterns, and update persistent LESSONS.md files using the retrieve-verify loop. Auto-trigger setup: install OpenCode plugin hooks, Claude Code Stop hooks, and Cline TaskComplete hooks so retros fire automatically when all todos complete. Works with session_read (OpenCode), context-window reconstruction (Claude Code, Cursor, Gemini CLI), and compaction pipelines. Use when finishing a task, at session end, when asked to reflect, review, debrief, or write a post-mortem, or when setting up automatic retro triggers."
license: MIT
metadata:
  version: 2.0.0
  author: jeff
  audience: developers, agents
  workflow: retrospective, self-improvement, lessons-learned
---

## Quick Start

**Prerequisites:** Write access to `~/.agents/lessons/` (create if absent). Git configured.

**When to run:** At session end · when asked to "reflect", "debrief", "post-mortem", or "write lessons" · auto-triggered when all todos complete.

**Output file:** `~/.agents/lessons/LESSONS.md` (universal, cross-tool).

**Tools needed:** Read, Write, Bash · `session_read` (OpenCode only) · `retro-lessons.sh` (parser/retrieval)

---

## What I Do

- Run structured self-assessments using the Sailboat+Forward rubric (Wind / Anchor / Rocks / Next)
- Write v2 LESSONS.md entries with Trigger/Action/Scope retrieval headers
- Retrieve and inject relevant past lessons before high-risk operations (the retrieve-verify loop)
- Audit whether injected lessons were Applied, Violated, or Irrelevant
- Compact LESSONS.md when it exceeds 20 entries; promote 3+ occurrence patterns to AGENTS.md
- Set up auto-trigger hooks (OpenCode plugin, Claude Code Stop hook, Cline TaskComplete hook)

---

## The Loop

The v2 retro skill runs a five-phase **reflect → store → retrieve → inject → verify** loop.

1. **Reflect** — assess the session via `session_read` transcript (OpenCode) or context-window reconstruction (all other tools). Identify correction loops, tool failures, and user redirects. Ask the human up to 3 targeted questions before writing. See [references/session-read.md](references/session-read.md).

2. **Store** — append a v2 entry to `~/.agents/lessons/LESSONS.md`, increment `<!-- retro:entries:N -->`. If N+1 > 20, run compaction. Check whether any theme appears 3+ times; if so, promote to `AGENTS.md`. See [references/compaction.md](references/compaction.md) and [references/promotion.md](references/promotion.md).

3. **Retrieve** — at session start, run `retro-lessons.sh retrieve --recent 5`. Before high-risk ops (git-push, git-commit, file-deletion, deployment, secrets-handling), run `retro-lessons.sh retrieve --operation <op>`. See [references/retrieval.md](references/retrieval.md).

4. **Inject** — format retrieved lessons into a compact `## Relevant Lessons` block (≤500 tokens, ≤5 bullets) and place in context before acting. Each bullet: `- **[tag]**: Action (Trigger: trigger)`. See [references/injection.md](references/injection.md).

5. **Verify** — after writing the Sailboat rubric, append an `> Audit:` block classifying each injected lesson as **Applied**, **Violated**, or **Irrelevant**. Violations generate a new reinforcing entry. See [references/audit.md](references/audit.md).

---

## Entry Format

v2 entries have an 8-line structure — heading + 3 retrieval headers + 4 Sailboat fields:

```markdown
## YYYY-MM-DD HH:MM | tag1 tag2
> Trigger: <when this lesson applies>
> Action: <what to do differently>
> Scope: <file-path-glob, operation-type, or general>
**Wind 🌬️:** <what went well>
**Anchor ⚓:** <what went wrong>
**Rocks 🪨:** <risks/unknowns>
**Next 🧭:** <concrete next action>
```

SYNTHESIZED variant: `## SYNTHESIZED — <title> | tag1 tag2` + same 3 headers + freeform body.

Full validation rules and examples → [references/schema.md](references/schema.md).

---

## Using the Parser

`skills/retro/scripts/retro-lessons.sh` — subcommands:

```bash
retro-lessons.sh inject                        # session-start: top 5 lessons → ## Relevant Lessons block
retro-lessons.sh retrieve --operation git-push # pre-risk: targeted retrieval by op type
retro-lessons.sh retrieve --tag planning       # retrieve by tag
  retro-lessons.sh validate                      # check LESSONS.md file health
retro-lessons.sh count                         # show entry count
```

Default file: `~/.agents/lessons/LESSONS.md`. Pass a path as the last argument to override.

---

## Tool Detection

| Tool | Method | Quality |
|------|--------|---------|
| OpenCode | `session_read` — full transcript | Excellent |
| Claude Code | Context-window reconstruction | Good |
| Cursor / Gemini CLI | Context-window reconstruction | Medium |

When `session_read` is unavailable, note in the entry: `> Reconstructed from context window (session_read unavailable)`.

Setup for auto-trigger (hooks + AGENTS.md snippet) → [references/auto-trigger.md](references/auto-trigger.md).

---

## References

| Reference | Content |
|-----------|---------|
| [references/schema.md](references/schema.md) | v2 entry format, tag rules, scope conventions, validation rules |
| [references/retrieval.md](references/retrieval.md) | When/how to retrieve — session-start vs pre-risk, retrieval algorithm, zero-match fallback |
| [references/injection.md](references/injection.md) | Injection format, two-layer injection, 500-token budget, anti-patterns |
| [references/audit.md](references/audit.md) | 5-phase audit protocol — Applied/Violated/Irrelevant, violations → new entries |
| [references/compaction.md](references/compaction.md) | Compact when N>20 — archive, pattern detection, SYNTHESIZED output |
| [references/promotion.md](references/promotion.md) | Promote 3+ occurrence patterns to AGENTS.md / CLAUDE.md |
| [references/migration.md](references/migration.md) | v1-to-v2 migration guide |
| [references/session-read.md](references/session-read.md) | `session_read` usage in OpenCode, graceful degradation |
| [references/auto-trigger.md](references/auto-trigger.md) | Hook setup for OpenCode, Claude Code, Cline; AGENTS.md snippet |
| [scripts/retro-lessons.sh](scripts/retro-lessons.sh) | Bash parser: validate, retrieve, inject, count, migrate subcommands |

---

## Common Errors

| Error | Fix |
|-------|-----|
| Wrong LESSONS.md path | Check `~/.agents/` exists; it takes priority over all tool-specific paths |
| v1 entry (no Trigger/Action/Scope) | Run `retro-lessons.sh migrate` to upgrade to v2 format |
| Token budget exceeded at injection | Trim to ≤5 bullets; oldest entries trimmed first |
| Compaction triggered but <20 entries | Check `<!-- retro:entries:N -->` counter — may be miscounted; use `retro-lessons.sh count` |
| Audit markers missing | Note `> Audit: no injection markers found; best-effort recall used.` |

---

## Examples

```
User: "run retro"
Agent: assesses session → injects lessons → writes v2 entry → audits → appends to LESSONS.md

User: "compact lessons"
Agent: synthesizes 20+ entries → writes SYNTHESIZED blocks → resets counter → promotes patterns

User: "we're done, reflect on what happened"
Agent: session_read (OpenCode) or context-window → Sailboat rubric → Audit block → LESSONS.md
```

---

## Related Skills

- `skill-helper` — improve this skill
- `markdown-editor` — format LESSONS.md and `.retro/` archives
