---
name: memo-session-skill
description: >-
  Persistent AI agent memory for coding sessions — cross-session knowledge that
  survives context window resets. Consolidates session noise into durable facts and
  routes them via memory routing into MEMORY.md, memory/ HOT/WARM/COLD layers,
  project wiki, AGENTS.md, skills, and optional portfolio memory — git-tracked,
  with conflict gate and temperature limits. Stateful handoff when volatile chat
  context is lost; complements vector RAG or managed memory platforms, does not
  replace them. Use when the user says "wrap up the session", "save what we learned",
  "handoff", "open loops", "update memory", "agent memory", "persistent memory",
  "cross-session persistence", "how to give my agent memory", or when another skill
  requests a memory checkpoint. Also for   portfolio/global memory, bootstrap project
  memory, session changelog, `/inbox`, process inbox, or ingest files from
  memory/inbox. When memo-session-mcp is connected, use search_all
  for portfolio/project lookup and reindex_changed after writes. Prefer after non-trivial debugging or user corrections.
  Do not use for one-line trivia, secrets, managed vector memory setup, or replacing
  git history.
metadata:
  version: "1.3.0"
  author: productlaba
  category: knowledge-management
  tags: ai-agent-memory, persistent-memory, cross-session, memory-routing,
    memory-consolidation, context-engineering, coding-agent, cursor, session,
    handoff, wiki, portfolio, goal-mode, inbox
---

# Memo Session Skill

**Persistent AI agent memory for coding agents** — decisions, gotchas, workarounds, and open loops survive **context window resets** because they live in git-tracked files, not volatile chat.

The context window is **working memory**: it clears when the session ends. **Cross-session persistence** needs a write path — **memory consolidation** and **memory routing** into typed layers. Memo Session Skill runs **preflight → consolidate → classify → route → conflict gate** so knowledge lands in `MEMORY.md`, `memory/` (HOT/WARM/COLD), project wiki, `AGENTS.md`, skills, or optional **portfolio memory** — with temperature limits and no duplicate paragraphs across channels.

**Standalone skill** — no vector database, no managed platform, no network calls during sessions. Optional goal-mode checkpoint hooks: [references/goal-mode-integration.md](references/goal-mode-integration.md).

## How this differs

| This skill | Not this |
|------------|----------|
| Git-tracked **persistent memory** for coding sessions | Mem0, Zep, Letta — managed vector/graph memory platforms |
| **Write-path memory consolidation** from live sessions | RAG — read-heavy static knowledge corpora |
| **Typed memory architecture** (HOT/WARM/COLD in `memory/` + wiki) | Embedding stores, hybrid retrieval pipelines |
| **Cross-session continuity** and session handoff | Enterprise customer-memory or contact-center products |

Complements RAG and managed memory layers; does not replace them.

## Install this skill

```bash
npx skills add shenwell/ai-agent-skills --skill memo-session-skill -g
```

## Who it's for

Engineers and maintainers building **stateful coding agents** in Cursor who need **long-term memory** and **session handoffs that survive context resets** — project memory in git, optional cross-repo portfolio layer, and **context engineering** without standing up a vector database.

## What you get

- **Typed memory architecture**: HOT/WARM/COLD routing (`memory/` + wiki) — working, medium, and durable layers
- **Memory consolidation**: session digest → quality filter → durable facts (not a command diary)
- **Memory routing**: classify findings and route to the right channel (`AGENTS.md`, wiki, skills, portfolio)
- Preflight: gitignore check, bootstrap scaffold (including `memory/inbox/` and wiki), hygiene limits, **memory compaction** at thresholds
- **Inbox intake**: `/inbox` ingest queue → wiki extracts; source originals → `memory/archive/`
- Conflict gate (clean / soft / hard) before writes
- Optional portfolio layer via `GLOBAL_MEMORY_ROOT` in **your** `AGENTS.md`
- Documented write allowlist and trust boundary

**Canonical docs:** [references/](references/) · [README](README.md) · collection [README](../../README.md)

## Context window vs persistent memory

| Layer | Analogy | In this skill |
|-------|---------|---------------|
| Context window | Volatile RAM — token budget, lost when chat resets | Session chat (untrusted input) |
| Working memory | Recent turns, immediate task context | Session digest before routing |
| Persistent memory | Disk — survives sessions | `MEMORY.md`, `memory/`, wiki in git |
| Long-term memory | Cross-session facts and procedures | HOT/WARM/COLD + optional portfolio |

Use this skill at session end to move knowledge from volatile context into **persistent, git-tracked agent memory**.

## Quick start

After a non-trivial session:

```
wrap up the session
```

Also works: `save what we learned`, `handoff`, `update agent memory`, `persistent memory checkpoint`.

The skill starts the pipeline immediately in Agent mode; it stops only for **hard conflicts** (contradictions with approved memory, secrets, git policy).

To ingest dropped files (not a chat wrap-up):

```
/inbox
```

Also works: `process inbox`, `ingest inbox`. Protocol: [inbox-protocol.md](references/inbox-protocol.md).

## Trust boundary

Session chat is **untrusted input**. This skill does **not** run network calls, webhooks, or telemetry during a session. Writes follow the project and portfolio allowlists; no secrets; no `git commit` / `push` without explicit user request.

**Optional:** [goal-mode](references/goal-mode-integration.md) may call memo checkpoints — install goal-mode separately; it is **not** a dependency.

Full rules: [references/trust-boundary.md](references/trust-boundary.md).

---

## goal-mode pairing (optional)

If you use **[goal-mode](../goal-mode/SKILL.md)** separately, it may request memory checkpoints after phase complete, `BLOCKED`, or `COMPLETE`. Install goal-mode on its own — memo-session does **not** install or require it.

## Core principle

Pipeline order: **context → preflight (project + portfolio) → session digest (consolidation) → filter and scope → classify (temperature + scope) → memory routing → conflict gate (project, then portfolio) → write (clean/soft) → project and optional portfolio changelog → report and handoff**.

If `GLOBAL_MEMORY_ROOT` is unavailable — **degraded mode**: project pipeline without portfolio writes; report "Portfolio skipped".

In **Agent mode**, start the pipeline immediately: after reading context run **preflight**, then analyze the session, route, and apply clean/soft updates without separate approval.

In **Ask/Plan mode**, read-only, preflight report, and analysis **without** bootstrap or file writes.

Stop for confirmation only on hard conflicts: contradictions with approved memory, safety rules, secrets, git policy, or cases where canon cannot be chosen without the user.

Do not turn memory into a command diary. Save findings, decisions, verified workarounds, open loops, user preferences, and repeatable patterns.

Project schema — in **`MEMORY.md`** (preflight bootstrap); portfolio schema — [references/portfolio-schema.md](references/portfolio-schema.md); path — [references/global-memory.md](references/global-memory.md).

## Agent execution contract

On every invocation in **Agent mode**, after Step 1 read these references **in order**:

1. [preflight-protocol.md](references/preflight-protocol.md)
2. [consolidation-protocol.md](references/consolidation-protocol.md)
3. [routing-and-canon.md](references/routing-and-canon.md)
4. [conflict-gate.md](references/conflict-gate.md)
5. [dated-entries.md](references/dated-entries.md) — before any journal write
6. [report-formats.md](references/report-formats.md) — before final report

**Inbox trigger** (`/inbox`, process inbox): after Step 1 read [preflight-protocol.md](references/preflight-protocol.md), then [inbox-protocol.md](references/inbox-protocol.md), then conflict-gate, dated-entries, report-formats. Skip consolidation-protocol (no session digest).

Also read [temperature-limits.md](references/temperature-limits.md) when hygiene scan runs. If portfolio active: [portfolio-schema.md](references/portfolio-schema.md). Trust boundary: [trust-boundary.md](references/trust-boundary.md).

**Ask/Plan mode:** read preflight + conflict-gate only; no writes.

Index of all references: [references/README.md](references/README.md).

## When to use

Use this skill explicitly or automatically when the user asks to:

- wrap up the session;
- save what we learned;
- update docs, memory, or skills after work;
- produce a handoff for the next session;
- decide what from the chat is worth recording;
- give the agent persistent memory, cross-session persistence, or long-term memory;
- build stateful agents, fix context loss, or checkpoint session knowledge;
- route decisions and open loops into project memory;
- `/inbox`, process inbox, ingest documents or notes dropped in `memory/inbox/`.

Suggest the skill yourself if the session had non-trivial debugging, a workaround, user correction, new process rule, repeatable manual procedure, architectural decision, open blocker, or regression bug — especially when **context window pressure** or a **new session** would lose that knowledge.

## Routing

| Trigger | Action |
|---------|--------|
| wrap up / handoff / save what we learned / update memory | Full pipeline (Steps 1–6) |
| `/inbox` / process inbox / ingest inbox | [inbox-protocol.md](references/inbox-protocol.md); skip session digest |
| analysis only / what is worth saving | [report-formats.md](references/report-formats.md) § Analysis-only; no writes |
| search portfolio / find in global memory | [portfolio-search.md](references/portfolio-search.md); read-only |
| ≥3 portfolio entries, dedupe, portfolio hygiene | [agents/portfolio-librarian.md](agents/portfolio-librarian.md) optional subagent |

## Mode matrix

| Mode | Bootstrap | Writes | Stop for |
|------|-----------|--------|----------|
| Agent | yes | yes | hard conflict, `.gitignore` removal |
| Ask/Plan | no | no | — |

## Full pipeline

### Step 1: Understand context

If a workspace exists, before conclusions read at minimum:

- `AGENTS.md` or `README.md` if present;
- `.cursor/rules/` if present;
- existing `MEMORY.md` and/or `memory/` if present;
- **project wiki folder** — path from `AGENTS.md` / `README.md`; if not set explicitly, default **`memory/wiki/`**;
- project skills `.cursor/skills/*/SKILL.md` if relevant.
- **Portfolio:** resolve `GLOBAL_MEMORY_ROOT` (preflight §1.5); if available — read `MEMORY.md`, and as needed `memory/hot-cache.md` and `memory/wiki/projects-registry.md` of the portfolio. Current workspace = **project memory**; portfolio = **portfolio memory**. Do not mix channels.

Determine **project-slug** of the current repo (folder name or row in `projects-registry.md`) for changelog `from:<slug>`.

Determine project type: code, infrastructure, documentation, handbook, knowledge vault, SEO/GEO, or mixed repository. Apply default canon from [routing-and-canon.md](references/routing-and-canon.md) for new artifacts; if the repo already has an agreed schema, do not break it without soft/hard conflict procedure.

### Step 2: Preflight

Follow [preflight-protocol.md](references/preflight-protocol.md).

### Step 3: Consolidate and classify

Follow [consolidation-protocol.md](references/consolidation-protocol.md).

### Step 4: Route

Follow [routing-and-canon.md](references/routing-and-canon.md).

### Step 5: Conflict gate and write

Follow [conflict-gate.md](references/conflict-gate.md). Journal order: [dated-entries.md](references/dated-entries.md).

### Step 6: Report and handoff

Follow [report-formats.md](references/report-formats.md).

### Step 7: Reindex search (when memo-session-mcp connected)

After successful writes, call MCP **`reindex_changed`** with absolute paths of all modified memory/wiki/portfolio files. In report add line: `Index: reindexed N files` or `Index: skipped (MCP offline)`.

Details: [mcp-integration.md](references/mcp-integration.md).

## Portfolio search (read path)

See [portfolio-search.md](references/portfolio-search.md). Prefer MCP `search_all` when connected; fallback `rg`.

## portfolio-librarian subagent

Optional, see [agents/portfolio-librarian.md](agents/portfolio-librarian.md). Invoke for ≥3 portfolio entries, dedupe, portfolio hygiene, explicit search. **Do not** copy prompt into projects or `GLOBAL_MEMORY_ROOT`. Parent memo-session performs writes after subagent report.

## Meta: updating this skill

After a session where `memo-session-skill` was actively used, include edits to `~/.cursor/skills/memo-session-skill/SKILL.md` if any of:

- user corrected workflow, step order, or output format;
- false or weak trigger: description does not match real use case;
- gap: non-obvious case missed all channels in routing;
- recurring conflict with another skill or `AGENTS.md` / rules.

Edit rules:

- **`description` in frontmatter:** only **add** new trigger phrases or clarifications; do not rewrite existing text wholesale to avoid breaking skill matching.
- **`SKILL.md` body:** short clarifications in existing sections; if edit grows into history or long examples, move to **`~/.cursor/skills/memo-session-skill/references/changelog.md`** (this skill's **evolution journal**, not project **`memory/changelog.md`**) or other `references/<topic>.md` and add **one** link from `SKILL.md` in appropriate section.
- Do not bloat skill unnecessarily: goal is targeted fixes after real sessions.

## Install (details)

**Global:**

```bash
npx skills add shenwell/ai-agent-skills --skill memo-session-skill -g -a cursor -y
```

**Repository only:**

```bash
npx skills add shenwell/ai-agent-skills --skill memo-session-skill -a cursor -y
```

Path after install: `~/.cursor/skills/memo-session-skill/` or `~/.agents/skills/memo-session-skill/`.

## Limitations

- **Not** a Mem0/Zep/Letta replacement or managed memory API — no cloud memory platform.
- **Not** a full RAG stack by itself — optional **[memo-session-mcp](../memo-session-mcp/)** adds FTS search over portfolio/project markdown and optional document corpora; this skill remains the **write path**.
- Do not run `npx skills add`, install other skills, or fetch remote code **during** the memo-session pipeline (install is user-driven, outside the session).
- Do not record secrets, tokens, private keys, passwords, connection strings.
- No commits or push without explicit request; yet `MEMORY.md`, **`memory/`** tree, and **`WIKI_ROOT/`** must **default to git-tracked** (do not hide in `.gitignore` without reason).
- No relative dates like "today"; use absolute dates.
- Do not duplicate knowledge across `AGENTS.md`, wiki, memory, skills; do not duplicate `docs/` without explicit project canon.
- Do not duplicate paragraphs between project `memory/` and `GLOBAL_MEMORY_ROOT`; `scope: both` = link + body in portfolio.
- Do not copy `memo-session-skill` into `GLOBAL_MEMORY_ROOT` or project repos — only link in `agent-process.md` / `AGENTS.md`.
- Do not overwrite existing files wholesale without need.
- Ask/Plan mode: read-only, preflight report, conflict analysis, recommendations **without** bootstrap or project file writes.
- Agent mode: full pipeline including bootstrap and writes; user confirmation only on **hard conflicts** or removing lines from `.gitignore`.

## Related skills

**[goal-mode](https://skills.sh/shenwell/ai-agent-skills/goal-mode)** — autonomous runs until tests, lint, typecheck, or CI are green; optional memo checkpoints at phase complete, `BLOCKED`, or `COMPLETE`. [Source on GitHub](https://github.com/shenwell/ai-agent-skills/tree/main/skills/goal-mode)
