---
name: share-memory
description: |
  Project-scoped shared memory for AI coding agents (Claude Code + Codex) via one AI_MEMORY/ per project. Use when the user says "init memory", "update memory", "sync memory", "memory status", "consolidate memory", "repair memory", "migrate memory", "更新记忆", "共享记忆", when AI_MEMORY/ is missing in a project that should have it, or to record completed work for the other agent.
  Do NOT use for: general chat memory, non-project shared state, one-off summaries, cross-project personal preferences, writing-materials archiving, or read-only audits. If the user forbids writing ("don't modify anything", "read-only audit", "only write the report"), auto-write is paused — do not write AI_MEMORY/ and say so at the end.
---

# ShareMemory Skill

Sets up and maintains a file-based shared memory (`AI_MEMORY/`) that Claude Code and Codex both read/write in the same project, so each agent sees the other's decisions and changes.

This skill is installable on both platforms (same folder, same SKILL.md):
- Claude Code: `~/.claude/skills/share-memory/` (personal) or `<project>/.claude/skills/share-memory/` (project)
- Codex: `~/.agents/skills/share-memory/`

AGENT_NAME: use `Claude` when running as Claude Code, `Codex` when running as Codex.
After init, the rules live in the project's `MEMORY_PROTOCOL.md` — that file (not this skill) is the source of truth for day-to-day behavior.

Memory model:
- `SYNC_LOG.md` + `archive/` are daily handoff history, with at most one block per date.
- `PROJECT.md`, `DECISIONS.md`, `TASKS.md`, and `LEARNINGS.md` are current views.
- Boot layer: `AGENTS.md` carries the shared agent-neutral rules; `CLAUDE.md` imports it via `@AGENTS.md` and adds Claude-only notes. All skill-managed boot content lives inside `<!-- SHAREMEMORY:START -->` / `<!-- SHAREMEMORY:END -->` marker blocks.
- Before ANY write inside `AI_MEMORY/` (incl. creating or archiving files), acquire `AI_MEMORY/.write.lock` per the protocol.
- Use the protocol's file-routing cadence before writing: prefer existing files, write only facts that help the next project agent, and refresh `PROJECT.md` / `LEARNINGS.md` when durable context would otherwise be missed.

Determine the operation from the user's intent: **init**, **update**, **status**, **consolidate**, **repair**, or **migrate**.

**Intent routing (first-trigger decision table):**

| User says / situation | Operation | Pre-check |
|---|---|---|
| "init memory", first time in project, `AI_MEMORY/` missing | **init** | If `AI_MEMORY/` already populated → status instead (idempotent) |
| "update memory", "sync memory", "更新记忆", "同步记忆", record progress | **update** | Must have `AI_MEMORY/` initialized |
| "memory status", "状态", "what changed" | **status** | Read-only — never writes |
| "consolidate memory", "压缩记忆" | **consolidate** | Acquire write lock first |
| "repair memory", boot files broken, lint fails | **repair** | Acquire write lock; back up files before fixing |
| "migrate memory", protocol version mismatch | **migrate** | User must explicitly consent; acquire write lock |

**Mandatory stop points** (halt and ask user before proceeding):
- Creating or replacing boot files/marker blocks without an explicit `init memory`, `repair memory`, or consented `migrate memory` request
- Enabling git or running `git init`
- Removing a `.write.lock` that is NOT yet stale (younger than the TTL; stale locks past the TTL auto-reclaim — no stop needed)
- Migrating protocol version
- Any publishing-channel operation

**Read-only vs auto-write rule:** When the user imposes a write restriction (e.g. "only write this report", "don't modify anything", "read-only audit"), auto-write of decisions / task-completion log bullets is PAUSED for the entire session. At the end, state: "Per user restriction, memory was not updated." The user can later lift the restriction by saying "update memory" explicitly.

**Project-helpfulness routing check** (run before `update`, after significant task completion, and before long handoff):

| If this changed | Write / refresh |
|---|---|
| Project goal, scope, architecture, workflow, install path, public contract | `PROJECT.md` and/or `DECISIONS.md` |
| Skill behavior, memory protocol, rule/schema, boot template, lint gate, or install/publish contract | `DECISIONS.md`; refresh `PROJECT.md` Long-Term Memory if startup would be stale |
| Active work now needs a next action, blocker, owner, continuation state, or completion mark | `TASKS.md` automatically if handoff would be incomplete; otherwise only on `update memory` |
| Confirmed bug cause, validation trap, release gotcha, repeated failure mode | `LEARNINGS.md` automatically if reusable; otherwise skip |
| Long-Term Memory would be stale for a fresh agent | rewrite `PROJECT.md` Long-Term Memory |
| Only today's handoff changed | one compact `SYNC_LOG.md` bullet |

Current protocol version shipped by this skill: **v1.3**.

## Marker block rules (used by init, repair, migrate)

For each boot file (`AGENTS.md`, `CLAUDE.md`):
- File doesn't exist → create it from this skill's `templates/project/`.
- File exists, no `SHAREMEMORY` block → back it up (`<file>.bak.YYYYMMDD-HHMMSS`), then INSERT the template's block (top of `CLAUDE.md` so the import loads first; end of `AGENTS.md`).
- File exists with a block → back it up, then REPLACE the block content with the template's. Never touch user content outside the markers.
- Never plain-append: repeated runs must never produce a second block.

## Operations

Full step-by-step for every operation lives in `references/operations.md` — **read the relevant section there before executing**. Quick map:

- **init** — detect project state (skip if already initialized); ask language + git; bootstrap the lock helper, acquire the init lock, create the boot/memory files, lint/commit if enabled, then release.
- **update** — run the helpfulness routing check; touch only files that truly changed; route accepted architecture / dependency / skill behavior / memory protocol / rule/schema / boot template / lint gate / install/publish contract decisions → `DECISIONS.md`; one `SYNC_LOG.md` bullet per file; lint; commit if `Git: enabled`.
- **status** — read-only; report AGENT_NAME, last writer, project state, active tasks, latest 1-2 daily blocks, lock state + last boot receipt (`scripts/memory_lock.sh status`), lint result, and protocol-version drift.
- **consolidate** — merge/dedup, rewrite `PROJECT.md` Long-Term (≤30 lines, re-read first), move overflow + old daily blocks to `archive/`, lint.
- **repair** — fix missing `@AGENTS.md` import / broken marker blocks / missing files / stale lock; restore scripts from `templates/project/`; lint and report what was fixed.
- **migrate** — version upgrade with user consent; rebuild marker blocks + restore protocol/scripts from `templates/project/`; carry forward all entries; bump `CONFIG.md` version; lint.

## Failure modes

On any conflict — lock held, permission denied, git missing, protocol mismatch, missing template, lock race, or a user write-restriction — **stop or degrade exactly per the table in `references/operations.md`. Never bypass the lock or write while a restriction is in effect.**

## Always

- Sign entries `### [YYYY-MM-DD HH:MM] [AGENT_NAME] Title` — timestamp from `date "+%Y-%m-%d %H:%M"`, never guessed.
- Telegraphic style, ≤3 lines per entry, language per `CONFIG.md`. Write only facts that change what a future agent should do. NEVER write secrets into memory.
- Cross-agent state lives in `AI_MEMORY/` only — never rely on Claude auto memory or any agent-private store for facts the other agent needs.
- At the end of meaningful work, run the project-helpfulness routing check before deciding whether to update memory; avoid durable entries when a compact `SYNC_LOG.md` bullet is enough.
- Decisions, dependency changes, rule/protocol contract changes, handoff-critical task state, confirmed reusable lessons, and task-completion log bullets are AUTO-written per protocol §5 even when this skill isn't invoked.
