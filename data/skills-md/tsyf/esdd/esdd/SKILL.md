---
name: esdd
description: Exhaustive Spec-Driven Development (ESDD) — grill the user into an INVEST-checked product spec, derive quality attributes via QAW and a ranked utility tree, design the architecture with Attribute-Driven Design, stress-test it with ATAM, and decompose everything into a Taskwarrior task graph with C4 + PlantUML diagrams and three-level MADR ADRs, where every task is sized under a 100k-token budget and assigned to an agent or a human. Use this skill whenever the user mentions ESDD or "exhaustive spec-driven development", asks for a "spec", "proposal", or "design doc" for a feature, wants a feature broken into tasks/tickets for agents, mentions INVEST, QAW, utility tree, ADD, ATAM, ADRs, Taskwarrior-based planning, or wants a feature's architecture planned thoroughly before coding — even if they never say "ESDD".
---

# ESDD — Exhaustive Spec-Driven Development

ESDD turns "build me X" into a verified architecture and a graph of
agent-sized tasks. It fuses Matt Pocock's grill → spec → tickets flow
(ticket → **task**, blocking edges → Taskwarrior `depends`) with OpenSpec's
proposal/design artifacts and the ATAM/ADD/QAW method family, executed
through sub-agents so the orchestrator's context stays lean.

## What one spec produces

```
.esdd/specs/<slug>/
├── proposal.md       product spec, INVEST-checked      (Phase 1)
├── utility-tree.md   drivers, ASRs, ranked QAS          (Phases 2–3)
├── design.md         ADD architecture + ATAM findings   (Phases 4–5)
├── diagrams/*.puml   C4 + sequence/class/activity/state/ER
├── adrs/NNNN-*.md    spec-level MADR ADRs
└── matrix.md         blocking-edge matrix (generated)
```

Plus, per spec, in Taskwarrior: one **index task** (`+spec`, holds the
`adrs` UDA) and a task graph under `project:<ws>.<proj>.<slug>`.

## Hard rules

1. **Token budget**: every actionable task targets ≤100k estimated tokens;
   100–140k must be split; >140k is a hard stop needing the human's
   written sign-off. Enforced by `esdd estimate` and `esdd verify`.
2. **The orchestrator owns all human contact.** Grilling, validations,
   sign-offs happen in the main session via questions. Sub-agents receive
   briefs and return file paths; if a sub-agent hits a question only the
   human can answer, it stops and reports the question rather than
   guessing (pause-and-return).
3. **Sub-agents do the verbose work** — drafting docs, authoring diagram
   source, walking scenarios — so their output streams never bloat the
   orchestrator's context.
4. **ADR discipline**: three levels — global `~/.esdd/adrs/`, directory
   `.esdd/adrs/`, spec `.esdd/specs/<slug>/adrs/`. MADR format. The
   narrowest applicable ADR wins. Accepted ADRs are only overturned by a
   newer ADR that marks the old one `deprecated` — never silently.
5. **Slugs** are lowercase-hyphen only; no dots (dots are Taskwarrior's
   project separator).
6. **Interfaces before tasks**: a design.md Interface entry exists before
   any task touching it is created.

## CLI quick reference (`esdd`, in `scripts/` of this skill)

| Command | Purpose |
|---------|---------|
| `esdd init [--graph-nav X]` | scaffold `.esdd/`; X ∈ codegraph, graphify, falkordb, neo4j, custom, none |
| `esdd doctor` | check workspace, taskwarrior, env |
| `esdd env set GRAPH_NAV X` | configure code navigation aid |
| `esdd tw -- <args>` | task(1) against nearest `.esdd/tasks` (with UDAs injected) |
| `esdd spec new <slug> --project <p>` | scaffold spec + index task |
| `esdd spec list` | specs and artifact status |
| `esdd adr new --level global\|directory\|spec --title "T"` | MADR ADR with correct numbering |
| `esdd adr list` | all three levels with status |
| `esdd matrix --spec <slug> [--out f]` | blocking-edge matrix + cycle detection |
| `esdd estimate --spec <slug> [--set]` | token estimates from `touches` |
| `esdd verify --spec <slug>` | handoff gate |
| `esdd phase <name> --spec <slug> [--done]` | track phase; names: product, qaw, tree, add, atam, handoff |

## Workflow

Phases run standalone: entering at any phase is fine if its inputs exist
(`esdd phase <name>` checks prerequisites). Normally run 0→6 per spec.

### Phase 0 — Init

- If `esdd` commands fail with "no .esdd found", ask the human whether to
  run `esdd init` at the current directory.
- Read `.esdd/env`; if `GRAPH_NAV` is `unconfigured`, ask the human which
  code-navigation aid to use (codegraph | graphify | falkordb | neo4j |
  custom | none) and `esdd env set GRAPH_NAV <choice>`. Every later phase
  that explores code checks this first: graph aid when configured, plain
  read/grep when not. The skill never requires the tool.
- Load ADR context, cheapest first: list global + directory ADR titles and
  statuses (`esdd adr list`); read in full only those plausibly relevant
  to the feature at hand. Record which ADRs are in play — ADD Step 4
  must cite them.
- Read the shared `.esdd/design.md` if it exists (C4 Level 1–2 boundary).

### Phase 1 — Product (INVEST)

1. `esdd spec new <slug> --project <proj>` (derive slug and project from
   the human's ask; confirm both).
2. Grill the human per `references/invest.md` until proposal.md's Open
   Questions section is empty. This is the longest human loop in ESDD —
   do not rush it; every later phase inherits its precision.
3. Draft proposal.md in a sub-agent (brief below), present to the human
   for sign-off, then write the file.
4. `esdd phase product --done --spec <slug>`.

### Phase 2 — QAW

1. `esdd phase qaw --spec <slug>`; read `references/qaw.md`.
2. Elicit drivers; brainstorm ASRs with the human (round-robin, capture
   verbatim, then structure). Exit when the human twice answers "nothing
   missing" to the read-back.
3. A sub-agent can structure raw notes into the ASR table; the
   brainstorm itself stays with the orchestrator.
4. Write the drivers + ASR sections of `utility-tree.md`.

### Phase 3 — Utility tree

1. Read `references/utility-tree.md`. For each ASR, draft QAS with all
   six parts and measurable response measures — a sub-agent drafts, the
   orchestrator validates with the human.
2. Propose BV/TR rankings **with one-line rationales**; the human
   confirms or overrides each. Never rank silently.
3. Write the tree; `esdd phase tree --done --spec <slug>`.
4. >12 QAS means the ASR list wasn't distilled — merge and demote.

### Phase 4 — ADD (the design loop)

Read `references/add.md`, `references/c4-plantuml.md`, and
`references/taskwarrior.md`. Then iterate the five steps; the loop unit is
one ranked QAS:

1. Review inputs, state design purpose (two sentences, citing drivers).
2. Propose the iteration goal from the top unaddressed QAS; human confirms.
3. Choose elements to refine.
4. Choose design concepts; each cites a QAS or an ADR. Contradicting an
   accepted ADR ⇒ new superseding ADR, old marked `deprecated`.
5. Instantiate: update design.md (Overview + Interfaces), delegate
   diagrams to a sub-agent, `esdd adr new --level spec` per significant
   choice, decompose into tasks (batch `task import`, briefs as first
   annotations, `depends` for blocking edges), refresh
   `esdd matrix --spec <slug> --out matrix.md`, then ask the human which
   tasks they want to own (`worker:human`). Run
   `esdd estimate --spec <slug> --set`.
6. Loop until the human declares the architecture complete. Keep each
   iteration's design purpose in the Iteration Goals Log — ATAM uses it.

### Phase 5 — ATAM

Read `references/atam.md`.

1. Sub-agent walks each QAS through the design (highest BV×TR first),
   marking achieved / addressed / at-risk.
2. Classify findings with the templates: risks, non-risks, sensitivities,
   tradeoffs — each risk cites its causing ADR or is sent back as an
   unmade decision.
3. Human reviews severity: **blocks goal** → new ADD iteration ("mitigate
   <risk>"); **needs mitigation** → hand off only with explicit human
   acceptance (recorded as a task); **watch** → listed, move on.
4. Cluster into risk themes; record all of it in design.md's ATAM
   section. `esdd phase atam --done --spec <slug>`.

### Phase 6 — Handoff

Read `references/token-budget.md`.

1. `esdd estimate --spec <slug> --set`; split every SPLIT verdict; hard
   stops need the human's written sign-off in the task's annotations.
2. `esdd matrix --spec <slug>` — no cycles.
3. `esdd verify --spec <slug>` must pass: one index task, `adrs` UDA in
   sync with files on disk, every actionable task has an estimate and a
   worker, dependencies resolve.
4. Present the summary: spec list, task counts by status, the blocking-
   edge critical path, and the **human work order** (their `worker:human`
   tasks). Workable blockers-first: `esdd tw -- next` is the agent queue.

## Sub-agent briefs

Two standard briefs cover most delegation. Keep them lean; the whole
point is context isolation.

**Drafter** (proposal sections, QAS drafts, ADR drafts, design.md text):

```
Write <artifact> for spec '<slug>' at <path>. Read only:
  - .esdd/specs/<slug>/proposal.md (sections: ...)
  - .esdd/specs/<slug>/utility-tree.md (ASR-n ...)
  - .esdd/adrs/000N-*.md (only: ...)
Requirements: <bulleted, e.g. "every QAS has a numeric response measure">
Do not ask questions; if blocked, list the blocking questions in your
final report instead of guessing. Return: the file path written and a
5-line summary. Do not paste the file contents.
```

**Diagrammer** (all .puml authoring):

```
Create <diagrams list> under .esdd/specs/<slug>/diagrams/ for spec
'<slug>'. Style: esdd/assets/base-theme.puml + C4-PlantUML <level>
includes (see references/c4-plantuml.md). Element names MUST match
design.md exactly: <list>. One diagram per file, <n>-<kind>-<name>.puml.
Return: paths + one line each on what the diagram shows. No file content.
```

**Analyst** (ATAM walkthrough, decomposition drafts):

```
Analyze <QAS list / iteration goal> against .esdd/specs/<slug>/design.md
+ diagrams/. Produce <format per references/atam.md>. Cite elements and
ADRs by name. Return: the file path written + the top-5 findings as a
bullet list. No full prose.
```

## Degradation

- No Taskwarrior binary: `esdd tw` fails loudly. Proceed markdown-only —
  track tasks in `specs/<slug>/tasks.md` as a fallback table, and note in
  handoff that the graph was never materialized.
- Graph nav absent/unusable: grep/read. Never block a phase on it.
- PlantUML can't render: the source files are still the spec; note the
  unrendered state in design.md.
