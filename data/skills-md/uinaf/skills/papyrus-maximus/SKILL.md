---
name: papyrus-maximus
description: "Project documentation that stays alive. Read before starting work, update after finishing. Covers project setup, specs, architecture diagrams, and execution plans. Use when starting a project, writing a spec, checking existing docs, updating docs after changes, or when someone says \"set up docs\", \"create a plan\", \"audit docs\", or \"init project\"."
---

# papyrus-maximus

Project documentation that stays useful. For humans and agents.

## Structure

```
project/
  README.md          ← humans: what is this, how to run it
  AGENTS.md          ← agents: project rules, stack, commands
  CLAUDE.md          ← symlink → AGENTS.md
  docs/
    ARCHITECTURE.md  ← how the system works (diagrams > text)
    *.md             ← guides, references, anything useful
    plans/           ← specs, execution plans, living docs
```

That's it. No nested agent zones. No session notes folder.

## File Roles

### README.md
For humans. High-level only.

| Section | Content |
|---------|---------|
| What | One paragraph — what does this do? |
| Getting Started | Clone, install, run. Copy-pasteable. |
| Usage | Key commands / API surface |
| Contributing | How to dev, test, deploy |

No architecture. No internal module descriptions. No detailed folder trees.

### AGENTS.md
For coding agents. Under 150 lines.

| Section | Content |
|---------|---------|
| Stack | Languages, frameworks, key deps |
| Commands | Build, test, lint, deploy — exact commands |
| Conventions | Naming, patterns, gotchas |
| Architecture | One sentence + "see docs/ARCHITECTURE.md" |

If it's growing past 150 lines, move content to `docs/`.

### docs/ARCHITECTURE.md
How the system is built. **Diagram-first, text-second.**

Use mermaid diagrams liberally:
- System context → who talks to what (C4 level 1)
- Component diagram → major modules and boundaries (C4 level 2)
- Sequence diagrams → key flows
- State diagrams → lifecycle of important entities

```markdown
## System Context

\```mermaid
graph LR
  User --> App
  App --> DB[(PostgreSQL)]
  App --> Queue[Redis]
  Worker --> Queue
  Worker --> ExtAPI[External API]
\```

## Components

| Component | Responsibility | Talks to |
|-----------|---------------|----------|
| API | HTTP handlers, auth | DB, Queue |
| Worker | Background jobs | Queue, ExtAPI |
| CLI | Admin commands | DB |

## Key Flows

\```mermaid
sequenceDiagram
  User->>API: POST /order
  API->>DB: insert order
  API->>Queue: enqueue process_order
  Worker->>Queue: dequeue
  Worker->>ExtAPI: submit
  Worker->>DB: update status
\```
```

Rules:
- **Diagrams > text.** If you can draw it, draw it.
- **Tables > paragraphs.** Component lists, config options, API surfaces.
- **Pseudocode > real code.** `process(order) → validate → enqueue → respond` beats a 30-line function that'll change next week.
- **No folder trees.** They go stale immediately. Describe capabilities and boundaries instead.
- **Mention modules by name**, not by path. "The worker module handles..." not "src/worker/index.ts handles..."

### docs/*.md — Other Material
Anything useful for humans or agents:
- **GUIDE.md** — walkthrough for common tasks
- **API.md** — endpoint reference
- **DEPLOYMENT.md** — how to ship it
- **DECISIONS.md** — notable past decisions (lightweight ADR: what, why, when — no template ceremony)

### docs/plans/*.md — Specs & Execution Plans

Filename convention: `kebab-case-slug.md` (e.g. `kalshi-hardening-2026-02-23.md`, `loss-reduction-2026-02-23.md`). No SHOUTING. Date suffix for at-a-glance staleness detection.
Living documents. Specs before code. Updated as work progresses.

```markdown
# [Feature Name]

## Goal
One sentence.

## Context
Why now? What's the current state? What's wrong with it?

## Design

\```mermaid
graph LR
  ...
\```

| Decision | Choice | Why |
|----------|--------|-----|
| Storage | SQLite | Single machine, no need for Postgres |
| Auth | API key | Internal tool, simplicity wins |

## Pseudocode
\```
on_request(order):
  validate(order.fields)
  enriched = fetch_market_data(order.ticker)
  if enriched.price > order.limit: reject("above limit")
  queue.push(enriched)
  return accepted(order.id)
\```

## Tasks
- [x] Design approved
- [ ] Implement core handler
- [ ] Add validation
- [ ] Write tests
- [ ] Update ARCHITECTURE.md

## Open Questions
- How to handle partial fills? → decided: treat as separate orders
```

Rules:
- **Spec first, code second.** Don't start implementation without an approved plan.
- **Keep them alive.** Check off tasks, update decisions, close questions.
- **Delete when done.** Completed plans can be archived or removed. They served their purpose.
- **One plan per feature/initiative.** Don't combine unrelated work.

## Writing Principles

| Principle | Instead of | Write |
|-----------|-----------|-------|
| Show, don't describe | "The system uses a pub/sub pattern for async communication between services" | A mermaid diagram showing the flow |
| Tables over lists | A bullet list of 8 config options with descriptions | A table with columns: option, type, default, description |
| Pseudocode over real code | A 40-line Go function | `validate → enrich → enqueue → respond` |
| Capabilities over paths | "src/internal/worker/handler.go processes jobs" | "The worker processes background jobs from the queue" |
| Short sentences | "The system is designed to handle the processing of incoming orders by first validating them and then..." | "Orders are validated, then queued for processing." |

## Lifecycle

### Before Work
Read `AGENTS.md`, `docs/ARCHITECTURE.md`, and any relevant `docs/plans/*.md`. Understand what exists before changing anything.

### After Work
Update what changed:
- New component? Update `docs/ARCHITECTURE.md` diagram.
- Finished a plan task? Check it off in `docs/plans/*.md`.
- New convention or gotcha? Add to `AGENTS.md`.
- Plan fully done? Delete or archive it.

### Keeper Mode
When invoked explicitly as papyrus-maximus:

1. **Ensure structure** — AGENTS.md exists, CLAUDE.md symlinked, `docs/` and `docs/plans/` exist
2. **Audit** — are docs accurate? Do diagrams match reality? Any stale plans?
3. **Fix** — update what you can. Create missing diagrams. Trim bloat.
4. **Flag** — report what needs human attention
5. **Trim** — AGENTS.md under 150 lines. README under 80 lines. Move overflow to `docs/`.
