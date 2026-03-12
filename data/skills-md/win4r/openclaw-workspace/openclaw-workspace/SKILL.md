---
name: openclaw-workspace
description: Use when maintaining or optimizing OpenClaw workspace files — AGENTS.md, TOOLS.md, SOUL.md, USER.md, IDENTITY.md, HEARTBEAT.md, BOOT.md, MEMORY.md, and related checklists and memory files. Covers workspace auditing, token budget analysis, new agent workspace setup from scratch, memory distillation, and cross-file consistency reviews.
---

# OpenClaw Workspace Skill

## Overview

OpenClaw workspace files form the agent's "soul and memory" — they are injected into the system prompt on every turn (or on relevant turns), giving the agent its identity, behavioral rules, environmental knowledge, and long-term memory. Managing these files well is critical: bloat wastes tokens, redundancy creates confusion, and stale content leads to bad decisions.

**Token budget:** 20,000 chars per file, ~150,000 chars total across all bootstrap files.

## File Inventory

| File | Purpose | Loaded When | Sub-agents? |
|------|---------|-------------|-------------|
| `AGENTS.md` | Boot sequence, checklists, behavioral rules | Every turn (all agents) | Yes |
| `SOUL.md` | Persona, tone, values, continuity philosophy | Every turn (all agents) | Yes |
| `TOOLS.md` | Env-specific notes (SSH, TTS, cameras, devices) | On-demand reference (part of bootstrap set) | Yes |
| `USER.md` | Human profile, preferences, relationship context | Every turn (all agents) | Yes |
| `IDENTITY.md` | Name, emoji, avatar, self-description | Every turn | Yes |
| `HEARTBEAT.md` | Periodic check tasks and health routines | Every heartbeat turn | Depends |
| `BOOT.md` | Startup actions (requires `hooks.internal.enabled`) | On gateway startup | No |
| `BOOTSTRAP.md` | First-time onboarding script — delete after use | New workspaces only | No |
| `MEMORY.md` | Long-term curated facts and iron-law rules | Main sessions only | No |
| `memory/YYYY-MM-DD.md` | Daily session logs | Loaded per AGENTS.md boot sequence | No |
| `checklists/*.md` | Step-by-step ops guides | Referenced in AGENTS.md, loaded on demand | No |

**Security rule:** MEMORY.md must NEVER be loaded in group chats or sub-agent sessions — it contains private context that should not leak.

For full details on each file's design, anti-patterns, and section structure, see [references/workspace-files.md](references/workspace-files.md).

## Workspace Paths

| Path | Purpose |
|------|---------|
| `~/.openclaw/workspace/` | Default workspace for main agent |
| `~/.openclaw/workspace-<profile>/` | Per-profile workspace (multiple agents) |
| `~/.openclaw/workspace/vendor/OpenClaw-Memory/` | Vendor-managed base files (synced from upstream) |
| `~/.openclaw/workspace/checklists/` | Checklist files referenced from AGENTS.md |
| `~/.openclaw/workspace/memory/` | Daily session logs |
| `~/.openclaw/workspace/docs/` | On-demand documentation (NOT auto-loaded) |

Config key: `agents.defaults.workspace` or per-agent `agents.list[].workspace`.

## Workflow: Audit Existing Workspace

Use when workspace files may be bloated, stale, or redundant.

1. **Read all active files** — AGENTS.md, SOUL.md, TOOLS.md, USER.md, IDENTITY.md, HEARTBEAT.md, BOOT.md, MEMORY.md
2. **Check character counts:**
   ```bash
   wc -c ~/.openclaw/workspace/AGENTS.md
   wc -c ~/.openclaw/workspace/SOUL.md
   wc -c ~/.openclaw/workspace/TOOLS.md
   wc -c ~/.openclaw/workspace/USER.md
   wc -c ~/.openclaw/workspace/IDENTITY.md
   wc -c ~/.openclaw/workspace/MEMORY.md
   # Or all at once:
   wc -c ~/.openclaw/workspace/*.md
   ```
3. **Flag files over 10,000 chars** — prime candidates for trimming or offloading to `docs/`
4. **Check for redundancy** — same fact in SOUL.md and AGENTS.md? Same tool note in TOOLS.md and MEMORY.md?
5. **Check for staleness** — outdated SSH hosts, old tool names, deprecated rules, historical context that's no longer needed
6. **Check MEMORY.md discipline** — should contain curated facts, lessons learned, decisions, and critical rules — not raw session summaries or task-specific notes
7. **Propose targeted edits** — trim, move to docs/, or restructure

See [references/optimization-guide.md](references/optimization-guide.md) for specific optimization strategies.

## Workflow: Set Up New Workspace

Use when creating a workspace for a new agent from scratch.

**File creation order** (matters for boot sequence to work):

1. `SOUL.md` — persona and values first; everything else follows from identity
2. `AGENTS.md` — boot sequence, safety rules, checklist table
3. `IDENTITY.md` — name, emoji, avatar
4. `USER.md` — human profile and preferences (main agent only)
5. `TOOLS.md` — environment-specific notes (add as you discover env details)
6. `MEMORY.md` — start minimal; only truly universal iron laws
7. `HEARTBEAT.md` — periodic health checks (optional, add when needed)
8. `BOOT.md` — startup hooks (optional, only if `hooks.internal.enabled = true`)
9. `BOOTSTRAP.md` — first-run onboarding (optional; delete after first successful startup)

**Minimal viable workspace:** AGENTS.md + SOUL.md + TOOLS.md. Everything else is optional.

**BOOTSTRAP.md note:** If creating a BOOTSTRAP.md, include a self-deletion instruction at the end:
```
## Final Step
Delete this file: exec `rm ~/.openclaw/workspace/BOOTSTRAP.md`
```

## Workflow: Memory Distillation

Use periodically (weekly or monthly) to keep MEMORY.md lean.

1. **Read all recent daily logs:** `memory/YYYY-MM-DD.md` files from the past period
2. **Identify candidates for promotion to MEMORY.md:**
   - Rules violated more than once (recurring mistakes)
   - Hard-won discoveries that aren't in skills docs
   - Env-specific facts that should always be in context (not left to memory_search recall)
3. **Check what's already in MEMORY.md** — avoid duplicates
4. **Draft additions** — use iron-law format: concise, action-oriented, unambiguous
5. **Archive old daily logs** — move files older than 30 days to `memory/archive/` or delete
6. **Check MEMORY.md total size** — keep under 10,000 chars; if larger, review for rules that are now stable enough to move to a skill's SKILL.md instead

**Do NOT put in MEMORY.md:**
- Long narratives or session summaries
- Things already covered in skill docs
- Anything specific to a single past task
- Episodic or task-specific memories (store those via memory_search/SQLite instead)

## Workflow: Add or Update a Checklist

Use when adding a new high-risk operation type or updating an existing checklist.

1. **Create or edit** `checklists/<operation-name>.md`
2. **Structure:**
   ```markdown
   # Checklist: <Operation Name>

   ## Pre-flight
   - [ ] Step 1
   - [ ] Step 2

   ## Execution
   - [ ] Step 3

   ## Verification
   - [ ] Confirm outcome
   - [ ] Log result in memory
   ```
3. **Register in AGENTS.md** — add a row to the checklists table:
   ```markdown
   | <Operation description> | `checklists/<filename>.md` |
   ```
4. **Keep checklists short** — if a checklist exceeds ~50 lines, it's probably trying to be documentation; move narrative content to `docs/` and keep only the actionable steps

## Workflow: Update TOOLS.md

Use when adding a new tool, device, or environment capability.

**TOOLS.md = environment-specific cheat sheet.** It should contain:
- SSH hosts and common commands for this specific machine
- TTS provider, voice IDs, and any quirks
- Camera IDs or device names for this setup
- Node device IDs or names
- Any local aliases or shortcuts that aren't obvious

**Do NOT put in TOOLS.md:**
- General skill documentation (use skill SKILL.md files)
- Things that are the same across all environments
- Installation instructions (use docs/)

**Format conventions:**
```markdown
# TOOLS.md - Local Notes

## SSH
- Main server: `ssh user@hostname`

## TTS
- Provider: Edge
- Voice: zh-CN-XiaoxiaoNeural

## Cameras
- Living room: node-id `abc123`, device `camera-0`
```

## Common Issues

### File exceeds token limit
**Symptom:** File is over 20,000 chars; OpenClaw may truncate it.
**Fix:** Audit for content that belongs in `docs/` (loaded on demand) instead of the bootstrap file. Move detailed references, historical context, and long examples out. Keep only what needs to be on every turn.

### MEMORY.md leaking to groups
**Symptom:** Agent shares private context in group chats or Discord.
**Fix:** Ensure MEMORY.md boot step in AGENTS.md is gated: "Main session only: Read MEMORY.md". Verify the agent's boot sequence explicitly checks session type before loading.

### Boot sequence not loading files
**Symptom:** Agent doesn't know about content in SOUL.md, USER.md, or MEMORY.md at session start.
**Fix:** Check that AGENTS.md boot sequence explicitly names each file to read. The agent won't auto-load files — it follows the boot sequence instructions in AGENTS.md. Verify `hooks.internal.enabled = true` in config if using BOOT.md.

### MEMORY.md growing too large
**Symptom:** File approaches or exceeds 10,000 chars; reading it on every turn wastes significant context.
**Fix:** Run memory distillation workflow. Move stable rules that have been incident-free for months into relevant skill SKILL.md files. Delete rules that are no longer relevant.

### Workspace changes not taking effect
**Symptom:** Agent still uses old content after editing a workspace file.
**Fix:** Workspace files are read at session start per the boot sequence. Restart the gateway or start a new session for changes to take effect.

## Reference Files

| Reference | Coverage |
|-----------|---------|
| [workspace-files.md](references/workspace-files.md) | Deep-dive on each file: purpose, design principles, anti-patterns, section structure |
| [optimization-guide.md](references/optimization-guide.md) | Token efficiency strategies, audit commands, distillation process |
