---
name: haro-docs
description: Manage project documentation structure using the Atomic Content Blocks model. Use when the user wants to initialize a documentation structure for a new project, organize existing documentation, aggregate complete documents (BRD, PRD, SAD, FSD...) from existing content blocks, critically review a problem/file via subagent reviewers, or manage project knowledge memory via remember/knowledge. Run /haro-docs with no args to scan the project and pick the next action. Before acting on any command, read its commands/*.md file fully — never act from memory.
---

# Haro Docs — Documentation Structure Skill

## 1. Overview

`haro-docs` organizes project documentation as **Atomic Content Blocks**: every small section is a separate markdown file, written exactly once (Single Source of Truth), then flexibly assembled into complete documents (BRD, PRD, SAD, FSD...).

- **Standardization:** every project has an identical documentation structure.
- **Atomicity:** each block is an independent object — easy to track and version.
- **Flexibility:** output documents are just different "Views" over the same blocks (see `shared/structure.md`).
- **Knowledge memory:** project facts live as small domain-scoped files under `.haro-docs/knowledge/` and are loaded selectively like RAG — no vector DB (see `commands/knowledge.md`).
- **Two states:** every doc file is `UPDATING` (in progress, reference-only) or `RELEASED` (final, must-follow). Status lives only in `.haro-docs/config/status.yaml` — doc files carry no status themselves.

## 2. Workspace `.haro-docs/`

The skill stores all configuration and state in `.haro-docs/` at the project root.
Single-file YAMLs live together in `config/`; each multi-file feature (`knowledge/`, `reviews/`, `elicitation/`) manages itself through its own `index.yaml`. YAML files are the single source for everything the agent looks up; Markdown payloads carry YAML frontmatter.

```
.haro-docs/
├── config/
│   ├── project.yaml     # Project profile: type, audience, doc-root, language settings, version
│   ├── schema.yaml      # Approved folder tree + aggregation matrix (version lives in project.yaml)
│   ├── agents.yaml      # Review subagent ("đệ tử") configuration — see commands/review.md (§10)
│   └── status.yaml      # Single source of doc status: UPDATING | RELEASED (see commands/generate.md (§6))
├── knowledge/           # Project knowledge memory — selective RAG (see commands/knowledge.md (§4))
│   ├── index.yaml       # Lookup source: file | domain | summary | tags | updated — read this, not the payloads
│   ├── business-*.md
│   ├── technical-*.md
│   ├── team-*.md
│   └── common-*.md
├── elicitation/         # Interim Q&A for generate (see commands/generate.md (§6))
│   ├── index.yaml       # Lookup: target | file | updated | open_gaps — one entry per Q&A file
│   └── <sanitized-path>.md
└── reviews/             # Saved review reports (see commands/review.md (§10))
    ├── index.yaml       # Lookup: id | topic | verdict | reviewers | date — appended on every save
    └── RR-YYYYMMDD-HHmmss-<slug>.md
```

> **Important:** `config/project.yaml` records the **doc-root** — the documentation location chosen by the user during `init`. Every command (`generate`, `remember`, `knowledge`) reads this config first. Never guess the doc-root.

> **Read order (every command):** `config/project.yaml` → `config/schema.yaml` → `config/status.yaml` → `knowledge/index.yaml` → selectively load only the matching payload files. See the command's workflow file for details.

> **Knowledge RAG:** Before any `init` or `generate` turn that needs project context, read `.haro-docs/knowledge/index.yaml` (if it exists), then selectively load only the knowledge files whose domain/tags match the task. Knowledge counts as ground truth when it conflicts with scanned defaults. See commands/knowledge.md (§4).

> **Elicitation & Status:** `generate` stores interim Q&A in `.haro-docs/elicitation/` (located via its `index.yaml`) and marks each doc file `UPDATING | RELEASED` in `.haro-docs/config/status.yaml` (single source — doc files carry no status). See commands/generate.md (§6).

> **Reviews:** `review` appends one entry per saved report to `.haro-docs/reviews/index.yaml` and reads it first to skip already-reviewed topics. See commands/review.md (§10).

> **Language settings:** `config/project.yaml` also records the **reply language** (`language.response`) and the **documentation language** (`language.documentation`). These are the single source of truth for all communication and content decisions — see shared/authoring.md (§9). If they are empty or missing, ask the user before running any command.

> ## MANDATORY ROUTING — READ BEFORE ACTING (no exceptions)
>
> This file is only the router. The normative workflow for each command lives in its workflow file (table below).
>
> 1. Match the user's command to exactly one table row.
> 2. Read that workflow file **fully, before any other tool call or answer** — the no-args dashboard (§3 below) is the only workflow that runs directly from this file.
> 3. If you notice you are about to act, answer, or create anything without the workflow open, **STOP and read it first**. Acting from memory, habit, or a previous session instead of the workflow is a workflow violation: **the workflow always wins over memory**, even when you are confident. This applies equally to small/weak models — when in doubt, re-read.

## Command index

| Command | When to use | Read first (fully, before acting) |
|---------|-------------|-----------------------------------|
| `/haro-docs` (no args) | Scan project, show dashboard, pick next action | — (runs from §3 below) |
| `/haro-docs init <description>` | Initialize the documentation structure for a new project | `commands/init.md` |
| `/haro-docs generate` | Build next doc (guided Q&A) | `commands/generate.md` + `shared/authoring.md` when writing |
| `/haro-docs generate <file>` | Focus on a specific file | `commands/generate.md` + `shared/authoring.md` when writing |
| `/haro-docs review <topic\|file>` | Critically review a problem/file via subagent reviewer(s) | `commands/review.md` |
| `/haro-docs remember <free text>` | Record knowledge (analyze → confirm → save) | `commands/knowledge.md` |
| `/haro-docs knowledge` | Open hub picker (list / remember / reindex / clean) | `commands/knowledge.md` |
| `/haro-docs knowledge --reindex` | Rebuild the knowledge index from payload frontmatter + compact | `commands/knowledge.md` |
| `/haro-docs knowledge --clean` | List stale/irrelevant knowledge, confirm per row, then remove | `commands/knowledge.md` |
| `/haro-docs config [agents\|conventions\|language]` | Manage config via hub picker | `commands/config.md` |

## Authoring rules (summary — full text in `shared/authoring.md`)

- Single Source of Truth: write once, assemble — never duplicate.
- Conversation uses `language.response`, doc content uses `language.documentation` (`en` | `vi` | `vi-en`); if missing, ask first.
- Write current state as the first version — no change-log phrasing, no version history in bodies (git owns versions).
- `RELEASED` means final and must-follow; `UPDATING` means reference-only.

## 3. Command `/haro-docs` (no args) — Project Scan + Status Dashboard + Action Picker

When the user runs `/haro-docs` with no arguments, or with arguments that do not match any configured command, do NOT execute a workflow. Instead run a **deep read-only scan** and show the dashboard + action picker:

1. **Deep scan (read-only)** —
   - If `.haro-docs/config/project.yaml` and `.haro-docs/config/schema.yaml` exist: read `docroot`, `language.*`, `version`; list the actual folder tree under doc-root (for each of `00-common` → `99-assets` show exists/missing, file count, and UPDATING/RELEASED breakdown from `.haro-docs/config/status.yaml`; paths missing from the map count as UPDATING).
   - If not initialized: show `Not initialized` and display the standard tree from shared/structure.md (§8) as preview.
   - Check knowledge: if `.haro-docs/knowledge/index.yaml` exists, show `Knowledge: N files` and the first 5 entries; otherwise show `Knowledge: (empty)`.
   - Check reviews: if `.haro-docs/reviews/index.yaml` exists, show `Reviews: N (latest verdict)`; otherwise show `Reviews: (none)`.
   - Check elicitation: if `.haro-docs/elicitation/index.yaml` exists, show `Elicitation: N open`; otherwise show `Elicitation: (none)`.
   - Check agents config: if `.haro-docs/config/agents.yaml` exists, show `Agents: <ids> (default: <id>)`; otherwise show `Agents: (default inline critic)`.
   - Scan the repo lightly: README (business domain, key features), top-level source tree + tech stack signals (package.json / requirements / go.mod / pom.xml / Cargo.toml...), code scale estimate, docs files lying outside doc-root (if any).
   - Synthesize a **Project Note**: 5–8 lines on current state — initialized?, doc-root, docs coverage (% RELEASED), biggest gaps (top-3 empty folders/files), tech stack, knowledge depth.
2. **Show command summary:**

   | Command | When to use | Example |
   |---------|-------------|---------|
   | `/haro-docs init <description>` | Initialize structure (12 folders) | `/haro-docs init E-commerce Next.js + PostgreSQL` |
   | `/haro-docs generate` | Build next doc in order (guided Q&A) | `/haro-docs generate` |
   | `/haro-docs generate <file>` | Focus on a specific file | `/haro-docs generate 02-business/01-value-prop.md` |
   | `/haro-docs review <topic\|file>` | Critically review a problem/file via subagent reviewer(s) | `/haro-docs review Should we use microservices?` |
   | `/haro-docs remember <free text>` | Record knowledge (analyze → confirm → save) | `/haro-docs remember STID is my company` |
   | `/haro-docs knowledge` | Open hub picker (list / remember / reindex / clean) | `/haro-docs knowledge` |
   | `/haro-docs knowledge --reindex` | Rebuild index + compact small files | `/haro-docs knowledge --reindex` |
   | `/haro-docs knowledge --clean` | Remove stale/irrelevant knowledge | `/haro-docs knowledge --clean` |
   | `/haro-docs config [agents\|conventions\|language]` | Manage skill config via hub picker (subagents, conventions, language) | `/haro-docs config` |

3. **Show Aggregation Matrix (compact)** — BRD/PRD/SAD/FSD source folders from shared/structure.md (§7).
4. **Action picker (popup)** — after the dashboard, always ask the user what to do next (use the agent's question/picker tool when available, otherwise a numbered list). Pre-suggest **2–3 smart recommendations** based on the scan, e.g.:
   - Not initialized → recommend `init`.
   - `01-overview` / `02-business` empty → recommend `generate <that file>`.
   - Many files `RELEASED` but no recent review → recommend `review <topic>`.
   - Knowledge empty → recommend `remember <seed facts>`.
   The user may pick a suggestion or name any other command. Once picked, follow the MANDATORY ROUTING above: read that command's workflow file fully before acting. Do NOT auto-run side effects without that command's normal confirmations.
5. **Do not create any file or write to any file.** If the first token is unknown (e.g. `/haro-docs foo`), prefix the dashboard with `Unknown command 'foo'. Valid: init, generate, review, remember, knowledge, knowledge --reindex, knowledge --clean, config.` and suggest the closest match. Also handle `help`, `--help`, `-h` as aliases for this dashboard. Matching is case-insensitive, trim whitespace.
