---
name: agent-memory
description: Sets up and drives TencentDB Agent Memory (MemoryCore + MemoryHub + MemoryProxy + MemoryPanel, from AnEntrypoint/agent-memory) -- a persistent, cross-session memory and knowledge system for AI agents. Chat Memory (L0 conversation -> L1 atom -> L2 scenario -> L3 persona), a versioned Skill library extracted from past work, a Wiki + CodeGraph knowledge map over docs and code, and a human-controlled review panel. Use when the user wants an agent team to share and accumulate memory/skills/knowledge across sessions and across multiple agent frameworks (not just this one Claude Code session), when they mention "memory hub", "team memory", "chat memory", "skill library", "wiki", "codegraph", or ask to install/configure/troubleshoot the memory-tencentdb plugin, or when onboarding a new agent into an existing team's accumulated experience. As of gm's tencentdb_backend addition, this system's format can ALSO be gm's own memorize/recall/memorize-fire/memorize-prune backend for an opted-in namespace (see gm.config.json's memory.tencentdb_backend) -- when that's enabled, the verb surface an agent already knows is unchanged; only the storage target moves. Use this skill for the standalone deployment (Docker Compose, panel UI, team review) or when gm's own backend is not what's being asked about.
license: MIT
compatibility: Requires Docker (or Node.js >= 22.16 for source install) to run MemoryCore/MemoryHub/MemoryProxy services locally or self-hosted; a running LLM endpoint (OpenAI-compatible) for extraction/embedding. Panel UI served over HTTP. Verified against AnEntrypoint/agent-memory (published fork of TencentCloud/TencentDB-Agent-Memory).
metadata:
  origin: AnEntrypoint/agent-memory
  upstream: TencentCloud/TencentDB-Agent-Memory
  provenance: published-fork-repackaged-as-skill
allowed-tools: Skill, Read, Write, Bash, WebFetch
---

# agent-memory

TencentDB Agent Memory gives an agent team a shared, growing memory instead of starting cold every session. Two ways it relates to gm's own `memorize-fire`/`recall` (see `wfgy-method`/`gm` skills for that): (1) as a fully standalone system (this skill's main content, below) when the ask spans multiple agent frameworks, multiple team members, or needs a human-reviewable panel; (2) as an opt-in storage backend for gm's own memory verbs (`memory.tencentdb_backend` in `gm.config.json`, disabled by default) -- when a namespace is routed to it, gm's `memorize`/`recall`/`memorize-fire`/`memorize-prune` write file-pointer-indexed content compatible with this system's format instead of gm's default 384-dim md-corpus store, with no change to the verb surface an agent calls. Reach for THIS skill's setup instructions (Docker Compose, panel UI) for the standalone deployment; reach for `gm`'s own docs when the ask is just "make gm's memory use the Tencent-compatible backend."

## What it provides

- **Chat Memory**: retains preferences, facts, decisions, and interaction history per agent. Distilled in layers: L0 raw conversation -> L1 atom -> L2 scenario -> L3 persona.
- **Skill library**: after complex work, an agent can extract a reusable Skill (versioned, with resource files, trigger boundaries, execution steps, validation rules) from its own conversation/tool-call history, then share it with the team after review.
- **Wiki + CodeGraph**: turns docs/specs/runbooks into a linked Wiki; indexes code symbols, files, call relationships, and impact paths into a CodeGraph, both queryable on demand rather than injected wholesale into context.
- **Memory Panel**: a human-controlled review/control surface (not just a dashboard) for what gets promoted, shared, or pruned.

Assets are portable across agent frameworks and shareable across a team -- a new agent or team member can load existing memory instead of relearning from scratch.

## When to use this skill vs. gm's own memory verbs

- Use `agent-memory`'s standalone setup instructions when: the user explicitly names TencentDB/memory-tencentdb/Memory Hub/team memory, wants memory that survives across *different* agent frameworks or team members (not just this session), wants a Skill library extracted from past conversations, or wants a Wiki/CodeGraph over a codebase.
- Use gm's own `memorize`/`recall`/`memorize-fire`/`memorize-prune` verbs (default backend, no setup) for this session's own local recall -- and if the user specifically wants gm's memory to be Tencent-format-compatible without running the standalone services, point them at `gm.config.json`'s `memory.tencentdb_backend` block instead of a full standalone install.

## Setup

### 1. Fastest path: Docker Compose (all three services)

```bash
git clone https://github.com/AnEntrypoint/agent-memory.git
cd agent-memory/deploy/global-images
cp .env.example .env
$EDITOR .env       # fill in LLM params for both the memory group and the proxy group
./start-all.sh     # starts memory-core + memory-hub + proxy; prints a one-liner for Claude Code setup
```

Open the panel at `http://localhost:8125`.

For a standalone Memory Hub, Proxy + Claude Code / CodeBuddy integration, port reference, and teardown, see `INSTALL.md` in the repo (`INSTALL_CN.md` for Chinese).

### 2. OpenClaw plugin install (if the host is OpenClaw, not Claude Code)

```bash
openclaw plugins install @tencentdb-agent-memory/memory-tencentdb
```

Minimal config in `~/.openclaw/openclaw.json`:

```json
{ "memory-tencentdb": { "enabled": true } }
```

Zero-config works for basic capability. Production tuning groups: `capture`, `extraction`, `pipeline`, `recall`, `persona`, `embedding` -- see `references/openclaw-config.md` for the full recommended template and failure-mode notes (embedding four-tuple, retention-day gating, etc.).

### 3. Migrating from an older install (v1.x/v0.x -> v2.0.0+)

Use the migration tool documented at `MemoryCore/scripts/migrate-v2-to-v3/README.md` in the repo. New installs skip this.

### 4. Migrating gm's own memories into the `tencentdb_backend` store

Distinct from #3 above (that's the standalone system's own internal format
evolution). This is for a project that already has gm-native memories
(`.gm/memories/*.md`, written by `memorize`/`memorize-fire` before
`memory.tencentdb_backend` was enabled) and wants them carried over once a
namespace opts into the Tencent-compatible backend, so recall doesn't go
cold on the switch.

Two ways to run this migration -- same underlying write path
(`tencentdb_memory::write_cfg`), pick whichever fits the situation:

- **From within a live agent session**: dispatch the
  `tencentdb-memory-import` verb: `{"source_namespace": "default",
  "dest_namespace": "<routed-namespace>", "kind": "l1"}`. It reads every
  `.md` doc in the source namespace and re-embeds through gm's own 384-dim
  pipeline.
- **Batch/CLI, outside an agent session**: `node
  scripts/migrate-memory-to-tencentdb.mjs --project <path> --namespace
  <ns> [--dry-run] [--archive]`. Same write path, but also applies the
  derivable-state discard filter (git-log-derivable facts, dated audit
  entries, historical framing) the verb does not -- prefer this for a bulk
  migration where discarding superfluous content matters, and the verb for
  a single dispatch from an already-running session.

Both refuse up front unless the destination namespace's resolved
`memory.tencentdb_backend.vectors_db_dims` is exactly `384` -- gm's
embedder cannot produce vectors at any other width, and a namespace
configured for externally-embedded 768-dim content (the default) cannot
safely receive them (recall queries that namespace through the
project-resolved dim, not a per-import override, so a dim mismatch there
is a real defect, not a formality). A project wanting both kinds of
content needs two separate `tencentdb_backend`-routed namespaces, each at
its own dim.

By default this is a one-way copy, not a move: the source `.md` files and
their `rssearch_vectors` index rows are left untouched, so the default
backend keeps working for any namespace not also switched over. Pass
`archive_source: true` (verb) or `--archive` (script) to opt into moving
each successfully-migrated source file to
`.gm/memories-archive-tencentdb/<namespace>/<filename>` instead of leaving
it in place -- content stays inspectable, but the live `.gm/memories/`
corpus no longer duplicates what the new backend now serves.

## Verification (do this before declaring setup done)

1. Confirm version prerequisites: `node -v` (`>=22.16`), and `openclaw --version` (`>=2026.3.13`) if using the OpenClaw plugin path.
2. After start/restart, confirm the service actually came up -- read logs (`[memory-tdai]` prefix for the OpenClaw plugin path, or the relevant container logs for Docker Compose) rather than assuming success from a clean exit code.
3. Confirm the data directory exists and is non-empty (OpenClaw: `~/.openclaw/state/memory-tdai/` containing `conversations/`, `records/`, `scene_blocks/`, `vectors.db`).
4. Run a real round-trip: have 2-3 turns that state memorable facts, start a fresh session, and confirm recall actually surfaces that content (via the panel, or a search tool call such as `tdai_memory_search`/`tdai_conversation_search`). A missing recall on this smoke test means setup is not done -- do not report success from config-file presence alone.

## Common failure modes

- No logs at all: `memory-tencentdb.enabled` not `true`, or the gateway/service was never restarted after config changes.
- Records exist but nothing recalls: `recall.enabled` is false, or `recall.scoreThreshold` is too high.
- No vector results: the `embedding` config is missing one of `apiKey`/`baseUrl`/`model`/`dimensions` -- any single missing field silently degrades to keyword-only mode rather than erroring.
- History disappearing too fast: `l0l1RetentionDays` set too low (1-2) without explicitly enabling `allowAggressiveCleanup`.

## Security

Treat `embedding.apiKey` and any LLM credentials as sensitive -- do not echo them into chat, logs, or screenshots. Prefer environment-variable injection over literal values in config files. When editing config, touch only the `memory-tencentdb`/agent-memory section; do not overwrite unrelated plugin or service config.
