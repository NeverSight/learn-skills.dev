---
name: team-orch
description: |
  Size-first multi-agent orchestration (team-orch): Atlas/Fable leads and never
  implements; 13 roles / 15 specialists (Opus/Sonnet/Haiku); 7-phase delivery;
  M/L workflow folders only; scope-locked T-NN tasks; fan-out and gates.

  Trigger when the user asks to orchestrate, route a roster, run DEFINE/PLAN/BUILD,
  author PRDs, fan-out specialists, or coordinate an AI team.

  Keywords: team-orch, Atlas, Fable, orchestrate, roster, DEFINE, PLAN, BUILD,
  TEST, REVIEW, SIMPLIFY, SHIP, XS S M L, workflow, tasks.md, fan-out, subagent
version: 1.2.0
license: Apache-2.0
metadata:
  author: famosapp
  stack: cursor-task-subagents, git-worktrees, git-full, optional-temporal
  related_skills: make-it-clear, git-worktrees, git-full, database-design, cavecrew
  primary_coordination: files + Task/subagents
  max_parallel_specialists: 8
  workflow_path: docs/workflow/wf-<YYYY-MM-DD-HHMM>-<slug>/
  sources_synthesized: super-orchestrator-playbook, agent-template, memory-protocol, phases, roster, prd-templates
---

# Team Orch

One Fable brain (**Atlas**), fourteen specialists, seven phases — workflow
folders only for **M/L**; Fable only does what actually requires Fable.
**Non-negotiables override framework fashion.** Size first — then route.

**Announce when activating:** "Using the team-orch skill."

Full playbook: [playbook.md](references/playbook.md). Vague intent →
[make-it-clear](../make-it-clear/SKILL.md).

## When to load which reference

| Need | Read |
|------|------|
| Super Orchestrator Playbook | [playbook.md](references/playbook.md) |
| Hard bans | [non-negotiable.md](references/non-negotiable.md) |
| Size / effort (XS–L) | [effort-ladder.md](references/effort-ladder.md) |
| 7-phase delivery map | [phases.md](references/phases.md) |
| Roster, tiers, routing | [roster.md](references/roster.md) |
| ticket/prd/adr/tasks/progress/report | [prd-templates.md](references/prd-templates.md) |
| Author a specialist agent | [agent-template.md](references/agent-template.md) |
| Index-first MEMORY.md | [memory-protocol.md](references/memory-protocol.md) |
| Topology choice | [patterns.md](references/patterns.md) |
| Generic role mandates | [roles.md](references/roles.md) |
| Message / task / status types | [types-and-layouts.md](references/types-and-layouts.md) |
| Sprint bootstrap & recovery | [sprints.md](references/sprints.md) |
| Shared memory & handoffs | [state-and-memory.md](references/state-and-memory.md) |
| Durable workflows (Temporal) | [durable-workflows.md](references/durable-workflows.md) |
| Pitfalls | [gotchas.md](references/gotchas.md) |
| DO / DON'T | [do-dont.md](references/do-dont.md) |
| Review checklist | [review-checklist.md](references/review-checklist.md) |
| Recipes | [examples.md](references/examples.md) |

---

## Core rules

1. **Size first** — XS/S/M/L before pipeline or fan-out ([effort-ladder.md](references/effort-ladder.md)).
2. **Lead ≠ coder** — Atlas/Fable sizes, routes, gates, synthesizes. **Never** writes production code.
3. **Workflow only for M/L** — `docs/workflow/wf-<YYYY-MM-DD-HHMM>-<slug>/` with all six files before BUILD. **XS/S: never create a workflow.**
4. **Scope lock** — execute only `tasks.md`; honor Out of scope; no hallucinated extras.
5. **Phases, not phase-agents** — Atlas fans existing specialists (‖ or →). Full 7-phase is for **L**, not typos.
6. **Fan-out independent work** — batch spawns in one message; 2–5 clones; builders need disjoint files or worktrees.
7. **Pass reports verbatim** — never paraphrase contracts or diagnoses.
8. **One specialist per concern** — engineer does not review its own code.
9. **Match Claude to job** — Fable lead · Opus judgment · Sonnet builders · Haiku volume. Never escalate coding to Fable.
10. **Context isolation** — Task/subagents + [git-worktrees](../git-worktrees/SKILL.md) `.worktrees/<X>-<Y>/`; one writer per branch.
11. **STOP at checkpoints** — architecture, M/L make-it-clear, review blockers → surface to user.
12. **Human reads the final diff** — SHIP stops before tag/deploy without explicit go-ahead.

---

## Non-negotiable

Full: [non-negotiable.md](references/non-negotiable.md), [playbook.md](references/playbook.md).

| Rule | Requirement |
|------|-------------|
| Size first | XS/S/M/L before route; no XS→L expand or L→XS shrink without reason |
| Lead ≠ coder | Atlas/Fable does not implement feature code |
| Workflow | M/L: six files under `docs/workflow/wf-…/` before BUILD; XS/S: no folder |
| Scope lock | Only `tasks.md`; Out of scope forbidden until ticket/prd updated |
| Isolation | Minimal prompts; no full-history dump; one checkout per branch |
| Verbatim handoff | Pass specialist reports / T-NN blocks without paraphrase |
| Clone memory | Parallel same-id clones are memory-silent; spawner consolidates |
| Human gates | `decision_gate` for prod deploy, data destroy, force-push, release tag |
| Synthesis | Never return raw unsorted multi-agent dumps as the user answer |

---

## Gotchas

Summary — [gotchas.md](references/gotchas.md).

- Full 7-phase or a workflow folder on a typo.
- Skipping recon on L auth/schema; starting M/L BUILD without six files.
- Fable/lead typing the bulk; engineer reviewing its own code.
- Work outside `tasks.md`; `report.md` missing “What was NOT done.”
- Supervisor telephone-game paraphrase; two writers on one branch.
- Parallel clones racing MEMORY.md; Haiku on hard diagnosis.
- Soft orchestrator prompt → lead gets impatient and codes.

---

## Types (“Data Types”)

| Kind | Values / shape |
|------|----------------|
| Effort size | `XS` · `S` · `M` · `L` |
| Phase | `DEFINE` · `PLAN` · `BUILD` · `TEST` · `REVIEW` · `SIMPLIFY` · `SHIP` · `META` |
| Claude tier | `Fable` (lead) · `Opus` · `Sonnet` · `Haiku` |
| Topology | `supervisor` · `swarm` · `hierarchical` · `pipeline` · `consensus` · `dag` · `saga` |
| Orchestration mode | `sequential` · `parallel` · `dag` · `debate` |
| Agent role | roster ids (`team-lead`, `architect`, …) · generic producer/dev/qa |
| Message type | `dispatch` · `status` · `worker_done` · `escalation` · `handoff` · `decision_gate` · `merge_ready` |
| Task status | `pending` · `ready` · `running` · `blocked` · `completed` · `failed` · `in-progress` · `done` |
| Memory layer | `agent` (MEMORY.md) · `working` · `session` · `long-term` |
| Readiness axis | `FEATURE` · `PERFORMANCE` · `SECURITY` · `QUALITY` · `MAINTENANCE` · `DEPLOYMENT` · `DOCUMENTATION` |

Details: [types-and-layouts.md](references/types-and-layouts.md).

---

## Layouts (“Tables / Columns”)

### Workflow (M / L only)

```
docs/workflow/wf-<YYYY-MM-DD-HHMM>-<slug>/
├── ticket.md      # Atlas — intake → Goal Spec
├── prd.md         # architect — in/out, assumptions, DoD
├── adr.md         # architect — this-workflow ADRs (link docs/adr/)
├── tasks.md       # architect — T-NN graph (ONLY executable work)
├── progress.md    # Atlas — live T-NN status
└── report.md      # Atlas — recon + delivery + what was NOT done
```

Timestamp: `date +%Y-%m-%d-%H%M`. Slug: kebab-case. One folder per feature;
`## Phase NN` sections inside the six files — no parallel tree.

### Agent file layout

```
.claude/agents/<id>.md
.claude/agent-memory/<id>/
  MEMORY.md
  mem-YYYY-MM-DD-HHMMSS-*.md
```

### Worker isolation

```
repo/                         # lead / main
repo/.worktrees/<X>-<Y>/      # one writer per branch
```

### Runtime topologies

| Layout | Shape | Use |
|--------|-------|-----|
| Star (Task) | Lead → N workers → synthesize | Default Cursor fan-out |
| Phase group | Lead fans ‖ or → per [phases.md](references/phases.md) | Delivery pipeline |
| Mesh | Peers hand off via files | Cross-cutting exploration |
| Hierarchy | Strategy → plan → execute | Large programs / sprints |
| Debate | Propose → critique → revise | High-stakes decisions |

---

## DO and DON'T

| DO | DON'T |
|----|--------|
| Size first; minimum agents | Full 7-phase / workflow on XS |
| Atlas plans/gates; workers type | Fable implements “to save time” |
| Six files before M/L BUILD | Start coding without `tasks.md` lock |
| Verbatim reports + T-NN packets | Paraphrase contracts/diagnoses |
| Opus for judgment; Haiku for volume | Hard diagnosis on Haiku; coding on Fable |
| Worktrees X-Y; memory-silent clones | Two writers on one branch |
| `report.md` lists what was NOT done | Silent extras / while-I'm-here |

Complete: [do-dont.md](references/do-dont.md).

---

## Examples

See [examples.md](references/examples.md):

1. Size-first route (XS typo vs L feature)
2. DEFINE parallel scout ‖ architect
3. M/L workflow folder + PLAN lock
4. Supervisor fan-out code review
5. BUILD foundations → feature ‖ qa
6. TEST red → debugger → BUILD loop
7. Parallel clones memory-silent
8. Sprint bootstrap / context recovery
9. Optional Temporal sketches

---

## Critical / Recommended / Nits

Full: [review-checklist.md](references/review-checklist.md).

### Critical
Unjustified multi-agent; no isolation; shared branch writers; lead coding; M/L BUILD without six workflow files; work outside `tasks.md`; secrets leaked; unbounded loops; no synthesis; human gate skipped; paraphrase of contracts; parallel clones writing MEMORY.md; XS→L / L→XS mis-size on auth/schema.

### Recommended
Size recorded; XS/S skipped workflow; phase right-sizing; complete delegation packet; agent template completeness; worktree X-Y; `progress.md` current; `report.md` “What was NOT done”; debate on high-stakes; ≤8 parallel; readiness axes for L; Claude tier matched to job.

### Nits
Codenames vs mandates; idle roster bloat; message type labels; confidence scores; cold-start prompt in brief.

---

## Decision workflow (Atlas loop)

1. **SIZE** — XS/S/M/L ([effort-ladder.md](references/effort-ladder.md)).
2. **TICKET** — M/L: mkdir workflow + `ticket.md`. XS/S: skip folder.
3. **INSPECT** — scout/recon when needed (never skip L / auth / new package).
4. **PLAN** — M/L: `prd.md` + `adr.md` + `tasks.md`; lock before BUILD.
5. **DELEGATE** — packet: path + T-NN + files + binary AC + Out of scope + memory mode. Match roster + Claude tier ([roster.md](references/roster.md)).
6. **WAIT** — do not steal the keyboard.
7. **PROGRESS** — M/L: `progress.md` on every status change.
8. **GATE** — TEST green + REVIEW clean (sized); loop to BUILD. Then SIMPLIFY → SHIP.
9. **SYNTH + REPORT** — one verdict; ownership by agent/model; iteration count; human diffs.

Master prompt: [playbook.md](references/playbook.md) §10.
