---
name: gsd-2-agent-framework
description: Meta-prompting, context engineering, and spec-driven development system for autonomous long-running coding agents
triggers:
  - gsd autonomous agent
  - spec-driven development
  - context engineering coding
  - long running agent task
  - gsd auto mode
  - milestone slice task hierarchy
  - gsd-pi cli agent
  - autonomous coding agent framework
---

# GSD 2 — Autonomous Spec-Driven Agent Framework

> Skill by [ara.so](https://ara.so) — Daily 2026 Skills collection

GSD 2 is a standalone CLI that turns a structured spec into running software autonomously. It controls the agent harness directly — managing fresh context windows per task, git worktree isolation, crash recovery, cost tracking, and stuck detection — rather than relying on LLM self-loops. One command, walk away, come back to a built project with clean git history.

---

## Installation

```bash
npm install -g gsd-pi
```

Requires Node.js 18+. Works with Claude (Anthropic) as the underlying model via the Pi SDK.

---

## Core Concepts

### Work Hierarchy

```
Milestone  →  a shippable version (4–10 slices)
  Slice    →  one demoable vertical capability (1–7 tasks)
    Task   →  one context-window-sized unit of work
```

**Iron rule:** A task must fit in one context window. If it can't, split it into two tasks.

### Directory Layout

```
project/
├── .gsd/
│   ├── STATE.md          # current auto-mode position
│   ├── DECISIONS.md      # architecture decisions register
│   ├── LOCK              # crash recovery lock file
│   ├── milestones/
│   │   └── M1/
│   │       ├── slices/
│   │       │   └── S1/
│   │       │       ├── PLAN.md        # task breakdown with must-haves
│   │       │       ├── RESEARCH.md    # codebase/doc scouting output
│   │       │       ├── SUMMARY.md     # completion summary
│   │       │       └── tasks/
│   │       │           └── T1/
│   │       │               ├── PLAN.md
│   │       │               └── SUMMARY.md
│   └── costs/
│       └── ledger.json   # per-unit token/cost tracking
├── ROADMAP.md            # milestone/slice structure
└── PROJECT.md            # project description and goals
```

---

## Commands

### `/gsd auto` — Primary Autonomous Mode

Run the full automation loop. Reads `.gsd/STATE.md`, dispatches each unit in a fresh session, handles recovery, and advances through the entire milestone without intervention.

```bash
/gsd auto
# or with options:
/gsd auto --budget 5.00        # pause if cost exceeds $5
/gsd auto --milestone M1       # run only milestone 1
/gsd auto --dry-run            # show dispatch plan without executing
```

### `/gsd init` — Initialize a Project

Scaffold the `.gsd/` directory from a `ROADMAP.md` and optional `PROJECT.md`.

```bash
/gsd init
```

Creates initial `STATE.md`, registers milestones and slices from your roadmap, sets up the cost ledger.

### `/gsd status` — Dashboard

Shows current position, per-slice costs, token usage, and what's queued next.

```bash
/gsd status
```

Output example:
```
Milestone 1: Auth System  [3/5 slices complete]
  ✓ S1: User model + migrations
  ✓ S2: Password auth endpoints
  ✓ S3: JWT session management
  → S4: OAuth integration  [PLANNING]
    S5: Role-based access control

Cost: $1.84 / $5.00 budget
Tokens: 142k input, 38k output
```

### `/gsd run` — Single Unit Dispatch

Execute one specific unit manually instead of running the full loop.

```bash
/gsd run --slice M1/S4            # run research + plan + execute for a slice
/gsd run --task M1/S4/T2          # run a single task
/gsd run --phase research M1/S4   # run just the research phase
/gsd run --phase plan M1/S4       # run just the planning phase
```

### `/gsd migrate` — Migrate from v1

Import old `.planning/` directories from the original Get Shit Done.

```bash
/gsd migrate                        # migrate current directory
/gsd migrate ~/projects/old-project # migrate specific path
```

### `/gsd costs` — Cost Report

Detailed cost breakdown with projections.

```bash
/gsd costs
/gsd costs --by-phase
/gsd costs --by-slice
/gsd costs --export costs.csv
```

---

## Project Setup

### 1. Write `ROADMAP.md`

```markdown
# My Project Roadmap

## Milestone 1: Core API

### S1: Database schema and migrations
Set up Postgres schema for users, posts, and comments.

### S2: REST endpoints
CRUD endpoints for all resources with validation.

### S3: Authentication
JWT-based auth with refresh tokens.

## Milestone 2: Frontend

### S1: React app scaffold
...
```

### 2. Write `PROJECT.md`

```markdown
# My Project

A REST API for a blogging platform built with Express + TypeScript + Postgres.

## Tech Stack
- Node.js 20, TypeScript 5
- Express 4
- PostgreSQL 15 via pg + kysely
- Jest for tests

## Conventions
- All endpoints return `{ data, error }` envelope
- Database migrations in `db/migrations/`
- Feature modules in `src/features/<name>/`
```

### 3. Initialize

```bash
/gsd init
```

### 4. Run

```bash
/gsd auto
```

---

## The Auto-Mode State Machine

```
Research → Plan → Execute (per task) → Complete → Reassess → Next Slice
```

Each phase runs in a **fresh session** with context pre-inlined into the dispatch prompt:

| Phase | What the LLM receives | What it produces |
|---|---|---|
| Research | PROJECT.md, ROADMAP.md, slice description, codebase index | RESEARCH.md with findings, gotchas, relevant files |
| Plan | Research output, slice description, must-haves | PLAN.md with task breakdown, verification steps |
| Execute (task N) | Task plan, prior task summaries, dependency summaries, DECISIONS.md | Working code committed to git |
| Complete | All task summaries, slice plan | SUMMARY.md, UAT script, updated ROADMAP.md |
| Reassess | Completed slice summary, full ROADMAP.md | Updated roadmap with any corrections |

---

## Must-Haves: Mechanically Verifiable Outcomes

Every task plan includes must-haves — explicit, checkable criteria the LLM uses to confirm completion. Write them as shell commands or file existence checks:

```markdown
## Must-Haves

- [ ] `npm test -- --testPathPattern=auth` passes with 0 failures
- [ ] File `src/features/auth/jwt.ts` exists and exports `signToken`, `verifyToken`
- [ ] `curl -X POST http://localhost:3000/auth/login` returns 200 with `{ data: { token } }`
- [ ] No TypeScript errors: `npx tsc --noEmit` exits 0
```

The execute phase ends only when the LLM can check off every must-have.

---

## Git Strategy

GSD manages git automatically in auto mode:

```
main
 └── milestone/M1          ← worktree branch created at start
      ├── commit: [M1/S1/T1] implement user model
      ├── commit: [M1/S1/T2] add migrations
      ├── commit: [M1/S1] slice complete
      ├── commit: [M1/S2/T1] POST /users endpoint
      └── ...
 
 After milestone complete:
main ← squash merge of milestone/M1 as "[M1] Auth system"
```

Each task commits with a structured message. Each slice commits a summary commit. The milestone squash-merges to main as one clean entry.

---

## Crash Recovery

GSD writes a lock file at `.gsd/LOCK` when a unit starts and removes it on clean completion. If the process dies:

```bash
# Next run detects the lock and auto-recovers:
/gsd auto

# Output:
# ⚠ Lock file found: M1/S3/T2 was interrupted
# Synthesizing recovery briefing from session artifacts...
# Resuming with full context
```

The recovery briefing is synthesized from every tool call that reached disk — file writes, shell output, partial completions — so the resumed session has context continuity.

---

## Cost Controls

Set a budget ceiling to pause auto mode before overspending:

```bash
/gsd auto --budget 10.00
```

The cost ledger at `.gsd/costs/ledger.json`:

```json
{
  "units": [
    {
      "id": "M1/S1/research",
      "model": "claude-opus-4",
      "inputTokens": 12400,
      "outputTokens": 3200,
      "costUsd": 0.21,
      "completedAt": "2025-01-15T10:23:44Z"
    }
  ],
  "totalCostUsd": 1.84,
  "budgetUsd": 10.00
}
```

---

## Decisions Register

`.gsd/DECISIONS.md` is auto-injected into every task dispatch. Record architectural decisions here and the LLM will respect them across all future sessions:

```markdown
# Decisions Register

## D1: Use kysely not prisma
**Date:** 2025-01-14
**Reason:** Better TypeScript inference, no code generation step needed.
**Impact:** All DB queries use kysely QueryBuilder syntax.

## D2: JWT in httpOnly cookie, not Authorization header
**Date:** 2025-01-14  
**Reason:** Better XSS protection for the web client.
**Impact:** Auth middleware reads `req.cookies.token`.
```

---

## Stuck Detection

If the same unit dispatches twice without producing its expected artifact, GSD:

1. Retries once with a deep diagnostic prompt that includes what was expected vs. what exists on disk
2. If the second attempt fails, **stops auto mode** and reports:

```
✗ Stuck on M1/S3/T1 after 2 attempts
Expected: src/features/auth/jwt.ts (not found)
Last session: .gsd/sessions/M1-S3-T1-attempt2.log
Run `/gsd run --task M1/S3/T1` to retry manually
```

---

## Skills Integration

GSD supports auto-detecting and installing relevant skills during the research phase. Create `SKILLS.md` in your project:

```markdown
# Project Skills

- name: postgres-kysely
- name: express-typescript  
- name: jest-testing
```

Skills are injected into the research and plan dispatch prompts, giving the LLM curated knowledge about your exact stack without burning context on irrelevant docs.

---

## Timeout Supervision

Three timeout tiers prevent runaway sessions:

| Timeout | Default | Behavior |
|---|---|---|
| Soft | 8 min | Sends "please wrap up" steering message |
| Idle | 3 min no tool calls | Sends "are you stuck?" recovery prompt |
| Hard | 15 min | Pauses auto mode, preserves all disk state |

Configure in `.gsd/config.json`:

```json
{
  "timeouts": {
    "softMinutes": 8,
    "idleMinutes": 3,
    "hardMinutes": 15
  },
  "defaultModel": "claude-opus-4",
  "researchModel": "claude-sonnet-4"
}
```

---

## TypeScript Integration (Pi SDK)

GSD is built on the [Pi SDK](https://github.com/badlogic/pi-mono). You can extend it programmatically:

```typescript
import { GSDProject, AutoRunner } from 'gsd-pi';

const project = await GSDProject.load('/path/to/project');

// Check current state
const state = await project.getState();
console.log(state.currentMilestone, state.currentSlice);

// Run a single slice programmatically
const runner = new AutoRunner(project, {
  budget: 5.00,
  onUnitComplete: (unit, cost) => {
    console.log(`Completed ${unit.id}, cost: $${cost.toFixed(3)}`);
  },
  onStuck: (unit, attempts) => {
    console.error(`Stuck on ${unit.id} after ${attempts} attempts`);
    process.exit(1);
  }
});

await runner.runSlice('M1/S4');
```

---

## Custom Dispatch Hooks

Inject custom context into any dispatch prompt:

```typescript
// .gsd/hooks.ts
import type { DispatchHook } from 'gsd-pi';

export const beforeTaskDispatch: DispatchHook = async (ctx) => {
  // Append custom context to every task dispatch
  return {
    ...ctx,
    extraContext: `
## Live API Docs
${await fetchInternalAPIDocs()}
    `
  };
};
```

Register in `.gsd/config.json`:

```json
{
  "hooks": "./hooks.ts"
}
```

---

## Roadmap Reassessment

After each slice completes, GSD runs a reassessment pass that may:

- Re-order upcoming slices based on discovered dependencies
- Split a slice that turned out larger than expected
- Mark a slice as no longer needed
- Add a new slice for discovered work

The LLM edits `ROADMAP.md` in place. You can review diffs with:

```bash
git diff ROADMAP.md
```

To disable reassessment:

```json
{
  "reassessment": false
}
```

---

## Troubleshooting

### Auto mode stops immediately with "no pending slices"
All slices in `ROADMAP.md` are marked `[x]`. Reset a slice: remove `[x]` from its entry and delete `.gsd/milestones/M1/slices/S3/SUMMARY.md`.

### LLM keeps failing must-haves
Check `.gsd/sessions/` for the last session log. Common causes: must-have references wrong file path, or test command needs environment variable. Adjust must-haves in the task's `PLAN.md` and re-run with `/gsd run --task M1/S3/T2`.

### Cost ceiling hit unexpectedly
The research phase on large codebases can be expensive. Set `researchModel` to a cheaper model in config, or reduce codebase index depth.

### Lock file left after clean exit
```bash
rm .gsd/LOCK
/gsd auto
```

### Git worktree conflicts
```bash
git worktree list          # see active worktrees
git worktree remove .gsd/worktrees/M1 --force
/gsd auto                  # recreates cleanly
```

### Session file too large for recovery
If `.gsd/sessions/` grows large, GSD compresses sessions older than 24h automatically. Manual cleanup:
```bash
/gsd cleanup --sessions --older-than 7d
```

---

## Links

- [GitHub: gsd-build/GSD-2](https://github.com/gsd-build/GSD-2)
- [npm: gsd-pi](https://www.npmjs.com/package/gsd-pi)
- [Pi SDK](https://github.com/badlogic/pi-mono)
- [Original GSD v1](https://github.com/gsd-build/get-shit-done)
