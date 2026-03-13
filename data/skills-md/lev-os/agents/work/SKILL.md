---
name: work
description: Unified lifecycle/process router. Concurrent FSM that discovers context, refines goals, maintains handoffs and entity state, routes to specialist skills, and uses `.lev/pm/*` as the canonical lifecycle surface. Includes spec-alignment workflow and PM-first template contracts.
version: 3.4.0
extends: []
related_skills:
  - lev-research
  - lev-cdo
  - ux
  - lev-learn
  - workflow
  - lev-portable
skill_type: workflow
category: process-lifecycle
primitive_owner: work
tools:
  - lev CLI
  - tracker CLI (br | bd | td)
  - cm CLI
  - cass CLI
  - skill-discovery CLI
  - jq
storage:
  lifecycle_root: ".lev/pm/"
  scratch_root: ".lev/scratch/"
  canonical_artifacts:
    report: ".lev/pm/reports/"
    proposal: ".lev/pm/proposals/"
    design: ".lev/pm/designs/"
    spec: ".lev/pm/specs/"
    plan: ".lev/pm/plans/"
    handoff: ".lev/pm/handoffs/"
    decision: ".lev/pm/decisions/"
    validation_report: ".lev/pm/validation-reports/"
---

# Work: FSM Lifecycle Router (v3)

**One entry point for all work.** Concurrent FSM with PLANNING and EXECUTION phases. Guard scoring runs constantly (not as a gate). DISCOVER runs interview, memory prefetch, prior art, and search concurrently. Canonical lifecycle artifacts live under `.lev/pm/*`. The free-form exception is `.lev/scratch/`.

```
                       PLANNING PHASE                                               EXECUTION PHASE
  ┌───────────────────┐   ┌───────┐   ┌──────────┐   ┌─────────┐   ┌──────┐   ┌─────────┐   ┌──────────┐   ┌──────┐   ┌───────┐
  │     DISCOVER      │──▶│ ALIGN │──▶│ RESEARCH │──▶│ PROPOSE │──▶│ SPEC │──▶│ EXECUTE │──▶│ VALIDATE │──▶│ EMIT │──▶│ LEARN │
  │   (concurrent)    │   └───────┘   └──────────┘   └─────────┘   └──────┘   └─────────┘   └──────────┘   └──────┘   └───────┘
  │                   │    north star   deeper code    CDO graph     BDD +      spawn         layer-dep      close      cm outcome
  │ ┌──────────────┐  │   ALIGN gate    analysis       5-role        contracts  team/agents   strictness     files      cm reflect
  │ │ Interview(fg)│  │    classify     C1-C4 map      think         accept.    inline        gates          update     br learning
  │ │ PriorArt(bg) │  │    layers       DoR compl.     proposal      criteria   cm add                      status     cass index
  │ │ Search  (bg) │  │    alignment                   file                    (learn)
  │ └──────────────┘  │    verdict
  │                   │
  │ ╔════════════════╗│    Guard is NOT a step -- it scores 6 categories every turn.
  │ ║ GUARD(constant)║│    <=30% -> PASS | 30-60% -> ASK inline | >60% -> interview skill
  │ ╚════════════════╝│
  └───────────────────┘
```

---

## On Load: Do This Immediately (Hard Contract)

1. Detect tracker backend (`bd > br > td > none`).
2. Resolve active workstream name from user request.
3. Open or create active handoff file in `.lev/pm/handoffs/`.
4. Record or confirm the long-term goal, done condition, roadmap, and current execution slice in the handoff.
5. Initialize or update entity matrix.
6. Initialize or update a tracker only for the current execution slice.
7. Append current tick (`Tn`) with objective and first evidence.

If step 3 fails, stop implementation work and create the handoff first.

## Storage Boundary (Hard Contract)

The handoff is the canonical planning artifact.

Store in the handoff:
- long-term goal
- done condition
- roadmap
- deferred work
- evolving decisions
- open questions
- why the current execution slice exists

Trackers (`bd`, `br`, `td`) are execution-plane only.

Store in the tracker:
- the current execution slice
- active implementation task
- blockers on the current slice
- validation or closeout status
- evidence links

Never store long-term plans, end-state framing, or multi-session roadmaps in tracker title, description, or comments unless the user explicitly asks for duplication.

Before every tracker write, check:
1. Is this only about the current execution slice?
2. Would this still be valid if the long-term plan changed?

If either answer is "no", write it to the handoff instead.

## PM Artifact Map (Hard Contract)

Template-backed lifecycle artifacts map 1:1 to `.lev/pm/*`:

| Artifact | Path | Template |
|----------|------|----------|
| Report | `.lev/pm/reports/` | `templates/report.md` |
| Proposal | `.lev/pm/proposals/` | `templates/proposal.md` |
| Design | `.lev/pm/designs/` | `templates/design.md` |
| Spec | `.lev/pm/specs/` | `templates/spec.md` |
| Plan | `.lev/pm/plans/` | `templates/plan.md` |
| Handoff | `.lev/pm/handoffs/` | `templates/handoff.md` |
| Decision | `.lev/pm/decisions/` | `templates/decision.md` |
| Validation Report | `.lev/pm/validation-reports/` | `templates/validation-report.md` |

The skill is self-documenting. Do not rely on companion README files for the contract.

## Scratch Boundary (Hard Contract)

`/.lev/scratch/` is the free-form exception outside the PM lifecycle tree.

Use scratch for:
- early theories
- partial notes
- temporary fragments
- speculative material not yet ready to become a PM artifact

Do not treat `.lev/scratch/` as canonical planning state. Promote out of scratch into a PM artifact when the content becomes durable.

## Template Loading (Hard Contract)

Always load:
- `templates/handoff.md`

Load as needed:
- `templates/report.md`
- `templates/proposal.md`
- `templates/design.md`
- `templates/spec.md`
- `templates/plan.md`
- `templates/decision.md`
- `templates/validation-report.md`

## Template Authoring Rules (Hard Contract)

Every structured PM template must begin with a `How To Fill This Out` section.

That section must:
- explain the purpose of the template
- explain the purpose of each major section
- include good/bad examples
- explicitly allow uncertainty markers

Allowed uncertainty markers:
- `[tbd]`
- `[unknown]`
- `[theory]`
- `[maybe: ..., confidence: ##%]`

## Quick Start

Use `$work` when you want one entry point for lifecycle-aware work:

```bash
work "analyze the current auth system"
work "design the new onboarding flow"
work "write a spec for deterministic callbacks"
work "plan the next implementation slice"
work "create a handoff for this session"
```

The first move is always:
1. open or update the handoff
2. capture or refine the goal/done condition/roadmap/current slice
3. update the entity matrix
4. route into the correct lifecycle behavior

## Common Usage Patterns

### Pattern 1: Research / Analysis

Use when you need to gather evidence or understand current state.

Examples:
- `work "analyze the current API architecture"`
- `work "research validation-gate patterns"`
- `work "scan the codebase for lifecycle drift"`

Typical output:
- active handoff updated
- report artifact in `.lev/pm/reports/`

### Pattern 2: Design / Proposal

Use when you need to shape a solution, compare options, or define an interaction/system direction.

Examples:
- `work "design the callback routing surface"`
- `work "propose a PM-first docs promotion workflow"`
- `work "architect the work-mvp boundary"`

Typical output:
- active handoff updated
- proposal or design artifact in `.lev/pm/proposals/` or `.lev/pm/designs/`

### Pattern 3: Spec

Use when you need an SDLC behavioral contract.

Examples:
- `work "spec the deterministic execution boundary"`
- `work "spec callback lifecycle semantics"`

Typical output:
- active handoff updated
- spec artifact in `.lev/pm/specs/`

### Pattern 4: Plan / Current Execution Slice

Use when you need the concrete slice that is being executed right now.

Examples:
- `work "plan the bugfix slice for handoff sharding"`
- `work "plan the next implementation slice for work-mvp"`

Typical output:
- active handoff updated
- plan artifact in `.lev/pm/plans/`
- tracker updated only for the current execution slice

### Pattern 5: Session Continuity

Use when you need to checkpoint or close a session.

Examples:
- `work "create a handoff for the work skill pass"`
- `work "close this session and capture next steps"`

Typical output:
- handoff updated in `.lev/pm/handoffs/`
- decisions promoted if warranted
- closeout/validation artifacts updated if the slice is done

## Example Lifecycle

```text
User request
  -> $work loads/updates handoff
  -> goal + done condition + roadmap captured
  -> entity matrix updated
  -> DISCOVER
  -> ALIGN
  -> RESEARCH
  -> PROPOSE / DESIGN
  -> SPEC or PLAN
  -> EXECUTE
  -> VALIDATE
  -> EMIT updated PM artifact
  -> LEARN / closeout
```

Concrete example:
1. `work "research the current callback boundary"`
   -> `.lev/pm/reports/...`
2. `work "design the callback routing surface"`
   -> `.lev/pm/designs/...`
3. `work "spec the callback execution contract"`
   -> `.lev/pm/specs/...`
4. `work "plan the next implementation slice"`
   -> `.lev/pm/plans/plan-impl-...`
5. `work "create a handoff"`
   -> `.lev/pm/handoffs/...`

## Troubleshooting

### "I don't know what stage this is"

Start with:
- active handoff
- current execution slice
- current artifact
- entity matrix state

If still unclear:
- route to DISCOVER and gather more evidence
- do not skip straight to execution

### "The tracker is getting roadmap text"

That is a contract violation.

Move long-term framing back into the handoff and keep the tracker scoped to the current execution slice only.

### "I have an idea but it's not ready for PM"

Use `.lev/scratch/` first.
Promote to a PM artifact only when it becomes durable enough to track through the lifecycle.

### "This seems like design, spec, and plan at once"

Separate them:
- design = broad direction
- spec = SDLC behavioral contract
- plan = current execution slice

## Canonical Naming (Hard Contract)

Use this filename format for handoffs:

`{YYYYMMDD}-{workstream}-{component}-{slug}-session-{N}.md`

Examples:
- `20260301-work-skill-core-reconstruction-session-1.md`
- `20260301-sdlc-docs-gates-audit-session-3.md`

Rules:
- `session-1` only when `predecessor: null`.
- Continue an existing stream with `session-{N+1}`.
- Do not start a new `session-1` for the same active stream unless explicitly requested.

## Required Handoff Frontmatter

```yaml
---
status: active | paused | completed
workstream: <slug>
component: <slug>
slug: <slug>
session: <N>
created_at: YYYY-MM-DD
predecessor: <filename.md | null>
confidence: 0.0-1.0
decisions_start: D<N>
---
```

## Required Handoff Sections

Every active handoff must contain:

1. `You Are Here`
2. `Next Agent Brief`
3. `Roadmap To Goal`
4. `Timeline` (tick log)
5. `Decisions Log`
6. `Open Questions`
7. `Entity Matrix`
8. `Meta`

### Required Next Agent Brief Fields

Every `Next Agent Brief` must state:
- `Long-Term Goal`
- `Done Condition`
- `Current Execution Slice`
- `Why This Slice Now`
- `Out of Scope This Session`

## Decision Promotion (Hard Contract)

Decisions stay in the handoff by default.

Promote a decision to `.lev/pm/decisions/` only when it is:
- architectural
- reusable across sessions or workstreams
- policy-setting
- likely to be cited outside the originating handoff

Promoted decisions must:
- link back to the source handoff
- preserve the original rationale
- note whether the handoff copy is now superseded by the promoted ADR

## Handoff Sharding (Hard Contract)

Update the handoff incrementally during the session. Before sharding, prune or compress irrelevant or resolved checkpoints first.

Shard to `session-{N+1}` when one or more of these conditions hold after consolidation:
- soft line cap: around 500 lines and unresolved context is still dense
- hard line cap: around 700 lines
- checkpoint pressure: another checkpoint would exceed 15
- entity pressure: more than 5 actively tracked entities
- complexity pressure: more than 3 major lifecycle phases or more than 2 major domain pivots
- depth pressure: entity-map or timeline growth makes recovery harder than a successor shard

Rules:
- `session-1` only when `predecessor: null`
- successor shards must link to the predecessor
- the old shard keeps historical breadcrumbs
- the new shard starts with compressed context, current entity state, and active next steps

## Roadmap To Goal (Hard Contract)

The handoff must contain a rolling roadmap from current state to the done condition.

### Scope

- The roadmap is a projection of remaining work, not a requirement to invent 10 steps.
- Maximum projection is 10 steps.
- If fewer than 10 steps remain, only list the real remaining steps.
- If remaining steps = 0, the work is in a done-candidate state and must enter reflection before close.

### Required format

```md
## Roadmap To Goal

**Goal**: <one-sentence end state>
**Done Condition**: <deterministic completion test>
**Remaining Steps**: <0-10>

### Step 1: <current execution slice>
- <1-10 concrete bullets>
- <only this step gets full detail>
- <include validation or exit criteria when useful>

### Steps 2-5 (Optional)

#### Step 2: <next phase>
- <1-3 bullets if needed>

#### Step 3: <next phase>
- <1-3 bullets if needed>

#### Step 4: <next phase>
- <1-3 bullets if needed>

#### Step 5: <next phase>
- <1-3 bullets if needed>

### Steps 6-10 (Optional)
6. <one-line future step>
7. <one-line future step>
8. <one-line future step>
9. <one-line future step>
10. <one-line future step>
```

### Rules

- Only Step 1 may contain detailed execution bullets.
- Steps 2-5 are optional and medium-granularity only.
- Steps 6-10 are optional and one-line only.
- Do not invent filler steps to reach 10.
- Tracker items may only represent `Step 1` unless a later step is explicitly pulled forward into the current execution slice.
- When Step 1 completes, shift the roadmap forward and rewrite the new Step 1 in detail.
- When the goal or done condition changes, update the roadmap in the handoff before changing tracker scope.
- Later sessions should refine the goal and done condition when they become clearer; do not preserve session-1 wording if the work is now better understood.

## Task Tracker Adapter (bd | br | td)

The work skill is backend-agnostic for task tracking. Detect which tool is available and route through the adapter. **Preference order: bd > br > td.**

### Detection

```bash
# Prefer bd (Go, auto-commit) > br (Rust, non-invasive) > td (Python, lightweight)
command -v bd && TRACKER=bd || { command -v br && TRACKER=br || { command -v td && TRACKER=td || TRACKER=none; }; }
```

### Operation Map

| Operation | bd (preferred) | br (supported) | td (lightweight) |
|-----------|---------------|-------------|------------------|
| **create** | `bd create --title="..." --type=task` | `br create --title="..." --type=task` | `td add "..."` |
| **list** | `bd list --status=open` | `br list --status=open` | `td` / `td -g {group}` |
| **search** | `bd search "{kw}"` | `br search "{kw}"` | N/A (grep local) |
| **show** | `bd show {id}` | `br show {id}` | `td {id}` |
| **update** | `bd update {id} --status=X` | `br update {id} --status=X` | `td {id} edit` |
| **close** | `bd close {id}` | `br close {id}` | `td {id} complete` |
| **deps** | `bd dep add {p} {c}` | `br dep add {p} {c}` | N/A |
| **ready** | `bd ready` | `br ready` | N/A |
| **sync** | `bd sync` (auto-git) | `br sync --flush-only` + manual git | N/A (local SQLite) |
| **epic** | `bd epic {id}` | `br epic {id}` | N/A (use groups: `td -g {epic}`) |

### Behavioral Differences

- **bd sync** auto-commits and pushes — no manual git needed
- **br sync** exports JSONL only — you must `git add .beads/ && git commit` manually
- **td** has no sync/deps/ready — degrade gracefully (skip dep gates, no ready filtering)

### Degradation Rules

When `td` is the only backend:
- Skip dependency-based gates (no `dep` support)
- Skip `ready` filtering (list all open instead)
- Map groups to epics (`td -g {epic-name}`)
- Search falls back to `td` + grep

When no tracker is available (`TRACKER=none`):
- Continue without task integration; note in artifact
- Prior art check skips BD/tracker queries

### Tracker Write Rules (Hard Contract)

- Tracker title names the current execution slice, not the full program.
- Tracker description describes only what will be executed in this slice.
- Tracker may link to the handoff path for context.
- Tracker must not duplicate long-term roadmap text from the handoff.
- If tracker text starts reading like a roadmap, stop and move that text to the handoff.

---

## Responsibility Boundary

- `lev` owns CLI/protocol routing only.
- `work` owns lifecycle-stage logic and artifact contracts.
- `lev-builder` owns build/migrate execution patterns.

Do not place artifact-format instructions in command shims. Keep format contracts in this skill and its templates.

---

## Entity Lifecycle (7 States + Discarded Branch)

```
ephemeral → captured → classified → crystallizing → crystallized → manifesting → completed
    ↓           ↓          ↓             ↓               ↓              ↓            ↓
 [scratch] [report]   [report]      [proposal or    [spec or       [handoff]    [validation /
                                      design]        plan]                         promoted decisions]
                                       ↘ discarded
```

| Stage | Canonical Artifact | Sub-Skills | Keywords |
|-------|--------------------|-----------|----------|
| **ephemeral** | None (brainstorm) | Inline | "explore", "brainstorm", "understand" |
| **captured** | `.lev/pm/reports/` | `lev get`, `lev-research` | "get", "research", "analyze", "scan", "find", "lookup", "read", "ls" |
| **classified** | `.lev/pm/reports/` + handoff updates | `work` ALIGN gate, `lev-portable` | "classify", "align", "categorize" |
| **crystallizing** | `.lev/pm/proposals/` or `.lev/pm/designs/` | `lev-cdo`, `lev-learn`, `thinking-parliament`, `ux` | "design", "propose", "architect", "learn", "guide me" |
| **crystallized** | `.lev/pm/specs/` or `.lev/pm/plans/` | `work`, tracker | "plan", "implement", "specify", "bugfix", "chore" |
| **manifesting** | `.lev/pm/handoffs/` + active PM artifact | Team coordination, tracker | "working on", "in progress" |
| **completed** | `.lev/pm/validation-reports/` + optional `.lev/pm/decisions/` promotion | `work` close/reflect | "done", "finished", "closed" |
| **discarded** | tombstone link | `work` guard + validation | "discard", "drop", "reject" |

`.lev/scratch/` is the free-form pre-artifact area. It is not a PM artifact class.

---

## Shortcuts

| Key | Action | Route |
|-----|--------|-------|
| `(l)` | Start learn interview | `learn [context]` |
| `(p)` | Start proposal | `work --stage=crystallizing` |
| `(u)` | Show update diff | `work --stage=update` |
| `(s)` | Browse skills | skills-db query (inline) |
| `(d)` | Design/UX hub | `ux` hub |

---

## Operational Command Constellation

These are agent <-> human operational commands and aliases. Map them to root primitives, not ad-hoc flows.

Canonical source for CLI alias + FSM stage + schema handler mapping:
- `~/.agents/skills/work/references/command-matrix.md`

| Command / Alias | Primitive | Route | Notes |
|-----------------|-----------|-------|-------|
| `work` | lifecycle | `work` | DISCOVER -> ALIGN -> route |
| `plan` | execution slice | `work` -> PLAN | Canonical execution artifact under `.lev/pm/plans/` |
| `spec` | sdlc-variant | `work` -> SPEC | SDLC behavioral spec under `.lev/pm/specs/` |
| `propose` | proposal | `work` -> PROPOSE | CDO graph deliberation |
| `design` | design | `work` -> PROPOSE | Design artifact under `.lev/pm/designs/` |
| `tracker` | execution tracking | tracker (br/bd/td) | Task graph + status |
| `check` | validation | `work` VALIDATE | Alignment, DoR, drift |
| `go` | execute | `work` -> EXECUTE | Start manifesting |
| `handoff` | continuity | `work` EMIT | Canonical checkpoint output |
| `exit` | session close | `work` EMIT -> LEARN | Emit handoff + learn ceremony |
| `learn` | guided intake | `lev-learn` via DISCOVER | Interview loop (foreground track) |
| `align` | alignment | `work` -> ALIGN gate | North star check, drift detection |
| `workflow` | workflow mgmt | `workflow` | List/create/run workflow skills |
| `skill` | skill ops | `skill-builder` or skill lookup | Build/discover/install path |
| `ask`, `wiz` | wizard mode | `interview` via DISCOVER | Guard >60% routes here automatically |
| `scan`, `security` | assurance | `work` VALIDATE | Can route to specialist security skills |
| `daemon`, `daemons` | runtime ops | `lev-core` | Operational status/health |
| `reflect` | learning | `work` LEARN | cm reflect + update closeout artifacts |

### External Context Primitive

Use `lev get` as the root external context-gathering primitive.

Compatibility note: if `lev get` is not available in the current CLI build, use `lev find` as a temporary alias.

Aliases that resolve here:
- `ls`, `read`, `search`, `find`, `lookup`, `scan`, `research`, `prior art`

Progressive depth:
- `context` -> current conversation/workspace state
- `fs` -> filesystem and local artifacts
- `tracker` -> task graph and open work (br/bd/td)
- `artifacts` -> `.lev/pm/*` lifecycle artifacts
- `research` -> external sources

---

## Quick-Keyword Artifact/Action Glossary

| Keyword(s) | Stage | Artifact | Action |
|------------|-------|----------|--------|
| "get", "research", "analyze", "scan", "find", "lookup", "read", "ls" | captured | report | DISCOVER -> `lev get` (or `lev-research` for deep mode) |
| "align", "north star", "drift", "classify" | classified | report + handoff | ALIGN gate (embedded) |
| "design", "propose", "architect" | crystallizing | proposal or design | PROPOSE -> `lev-cdo` + `ux` when relevant |
| "learn", "guide me", "unstuck" | crystallizing | proposal or design | DISCOVER interview track -> PROPOSE |
| "specify" | crystallized | spec | SPEC -> SDLC behavioral contract |
| "plan", "implement", "bugfix", "chore" | crystallized | plan | PLAN -> current execution slice |
| "working on", "in progress", "handoff", "exit" | manifesting | handoff | EXECUTE -> EMIT |
| "done", "finished", "closed" | completed | validation report + optional decisions | EMIT -> LEARN |
| "reflect", "learnings", "retro" | completed (post-close) | handoff/meta | LEARN -> `cm reflect` + update closeout |

---

## FSM States: PLANNING PHASE

### DISCOVER -- Concurrent Context Gathering

DISCOVER is the entry point. It runs four tracks concurrently with a constant guard scoring function. All findings update the active handoff and, when durable enough, a report artifact under `.lev/pm/reports/`.

```
/work "{idea}"
    │
    ▼
DISCOVER (concurrent, not sequential)
├── Interview (foreground)
│   └── Ask user questions, rolling bg research per question
├── Memory Prefetch (background)
│   └── cm context + cass search (workspace-first, global fallback)
├── Prior Art (background)
│   └── br search, lev get, cass search, tracker list
├── Search (background)
│   └── Codebase grep, online search, skill discovery
└── Guard (constant -- runs every turn, not a pre-step)
    ├── Score 6 categories: Objective, Scope, Constraints, Environment,
    │   Dependencies, Success Criteria
    ├── Each scored: MISSING (full weight) | PARTIAL (half) | PRESENT (0)
    ├── Weights: Objective (20%), Scope (20%), Constraints (15%),
    │   Environment (15%), Dependencies (15%), Success Criteria (15%)
    │
    ├── Score <=30%  -> PASS (sufficient, advance to ALIGN)
    ├── Score 30-60% -> ASK (structured questions inline)
    └── Score >60%   -> route to interview skill (wizard-mode)
```

**Confidence formula:**

```
base_confidence = 1.0 - (guard_score / 100)
layer_modifier: Site/Structure -0.1, Skin/Services +0.0, Space +0.05, Stuff +0.1
think_modifier: agreement >80% +0.1, 50-80% +0.0, <50% -0.1
final = base + layer_modifier + think_modifier
```

**Memory prefetch** runs as part of DISCOVER before heavy research fan-out:

| Step | Command | Policy |
|------|---------|--------|
| Procedural recall | `cm context "{kw}" --workspace "$PWD" --limit 3 --history 1 --json` | Workspace-first |
| Episodic recall | `cass search "{kw}" --workspace "$PWD" --json --limit 5 --max-content-length 180` | Workspace-first |
| Global fallback | retry without `--workspace` only if low-signal workspace hits | Fail-open |
| Injection budget | summarize to short bullets with provenance links | Keep compact |

Low-signal criteria (default): generic prompt, zero thinking signal, empty/weak workspace hits.

**Skill discovery** runs as part of the Search background track:

| Priority | Source | Path |
|----------|--------|------|
| 1 | Project-local skills | `.claude/skills/`, `.agents/skills/` in project |
| 2 | Global canonical skills | `~/.agents/skills/` |
| 3 | Skills DB | `~/.agents/skills-db/` (use `~/.agents/lev-skills.sh discover`) |
| 4 | POC skills | `~/lev/workshop/poc/skills/` |
| 5 | Polymath skills | `~/lev/workshop/intake/cc-polymath/skills/` |

**Lookup Tool:** Use `~/.agents/lev-skills.sh discover "{kw}"` as the shared local discovery entrypoint. Use raw `grep` only for debugging.

**Prior art search** runs as part of the PriorArt background track:

| Source | Search Method |
|--------|--------------|
| Tracker store | `br search "{kw}"` ; `br list --label-any "{kw}"` |
| Tracker tasks | `$TRACKER list --status=open \| grep -i "{kw}"` ; `$TRACKER search "{kw}"` |
| Codebase & docs | `lev get "{kw}" --scope=all --depth=research` |
| CASS index | `cass search "{kw}" --robot --limit 10` |
| Existing skills | `lev get "{kw}" --scope=knowledge --depth=fs --pattern="SKILL.md"` |

**If substantial prior art found**, present findings and ask:
1. Review existing work?
2. Extend existing work?
3. Proceed with new work anyway?

**Flexible ordering:** Steps have dependency gates, not fixed sequence. If prior art returns empty fast, skip ahead. If interview reveals complexity, loop back. Guard score dropping below 30% unblocks ALIGN regardless of other tracks.

**Skip guard when:** Explicit file paths provided, multi-turn context established, `--no-guard` flag, or resuming from saved session.

**Output:** updated handoff + report artifact with discovery results, guard scores, and skill manifest.

### ALIGN -- North Star Alignment

Check project alignment before deeper work. This is an embedded `work` gate. Use `lev-align` only for standalone deep-dive audits.

```
ALIGN:
├── North star exists?
│   ├── YES -> Compare current state to north star
│   │   └── Drift type? (Stale Docs | Product Pivot | Coverage Gap | Status Drift | Path Drift)
│   └── NO -> Deep research codebase -> define north star -> capture in handoff + report
├── Classify layers (lev-portable):
│   ├── Stewart Brand shearing layers: Site | Structure | Skin | Services | Space Plan | Stuff
│   ├── Depth: L0 (overview) -> L1 (structure) -> L2 (details) -> L3 (runtime)
│   └── Persistence: System graph (permanent) vs CDO graph (ephemeral)
└── Output: alignment verdict (aligned | drift | gap)
```

| Layer | Timescale | Risk | Examples |
|-------|-----------|------|----------|
| Site | Decades | High | DB schema, core model |
| Structure | 30-50y | High | Auth, API contracts |
| Skin | 20y | Medium | UI framework, design system |
| Services | 7-15y | Medium | CI/CD, monitoring |
| Space Plan | 3-7y | Lower | Routes, features |
| Stuff | Daily | Lowest | Copy, env vars |

**If no alignment data exists**, capture project context in the active handoff and a report artifact.

**Execution tiers** (determined by layer classification):

| Classification | Tier | Pattern |
|---|---|---|
| Stuff + L3 + CDO | Direct | Just do it |
| Space Plan + L2 | Brief | 5-bullet spec -> execute |
| Skin/Services + L1-L2 | Standard | Plan -> execute -> review |
| Structure + L1 | Deliberate | Proposal -> approval -> execute -> review |
| Site + L0-L1 | Formal | Proposal -> approval -> phases -> multi-gate review |

### RESEARCH -- Deep Analysis

Deeper investigation informed by DISCOVER results and ALIGN verdict. Runs only when the task warrants it (skipped for Stuff/Space Plan tier).

| Activity | Method | Output |
|----------|--------|--------|
| Code analysis | Read files, trace dependencies | Understanding of current state |
| Content review | Review prior art artifacts | Context for proposal |
| Design review | Architecture patterns, anti-patterns | Alignment assessment |
| C1-C4 mapping | Site/Structure layer analysis | Impact assessment |
| DoR completion | Fill remaining guard categories | Ready for PROPOSE |

**Save to:** `.lev/pm/reports/` and update the active handoff.

**Skip when:** Guard score <=30% at DISCOVER exit AND layer is Stuff/Space Plan (tier Direct or Brief).

### PROPOSE -- Solution Design

Draft a proposal using CDO graph deliberation. Uses 5-role Think (from lev-portable).

```
PROPOSE:
├── Think deliberation (5 roles, layer-weighted):
│   ├── Advocate, Critic, Systems Thinker, Pragmatist, Wild Card
│   ├── Layer weighting: Site/Structure -> heavy Critic + Systems Thinker
│   │                    Stuff -> heavy Pragmatist + Wild Card
│   ├── Devil's advocate trigger when >70% agreement
│   └── Light mode (>=0.80 confidence): Advocate + Critic only
├── Draft proposal or design artifact
├── If ephemeral -> inline response + optional scratch note
├── If prior art exists -> extend, don't duplicate
├── Surface discovered skills:
│   ├── Pull skill manifest from DISCOVER Search track report
│   ├── If design/UX keywords detected -> propose loading `ux` hub
│   ├── Query local skills runtime: ~/.agents/lev-skills.sh discover "{topic}" --json
│   └── Include in dashboard footer (inline, does NOT block FSM)
```

**Save to:** `.lev/pm/proposals/` or `.lev/pm/designs/`, plus active handoff updates.

**Team structure** (determined here, not in a separate PLAN step):

| Complexity | Signals | Strategy | Tool |
|-----------|---------|----------|------|
| Simple | Single file, one skill | Direct execution | None |
| Medium | 2-3 files, multiple skills | Parallel subagents | Task tool, 2-4 agents |
| Complex | Multi-file, cross-cutting | Formal team | TeamCreate + Task tool |

### SPEC -- Behavioral Specification

Crystallize the proposal or design into a spec or a plan, depending on intent:

- `spec` = SDLC behavioral contract under `.lev/pm/specs/`
- `plan` = current execution slice under `.lev/pm/plans/`

Use `spec` when defining target behavior and contracts.
Use `plan` when defining the current implementation / bugfix / research slice.

Specs must include: BDD scenarios (Given/When/Then), contracts, acceptance criteria, and validation boundaries.
Plans must include: goal, done condition, execution steps, dependencies, and validation for the current slice.

#### PROPOSE Dashboard Footer

Every PROPOSE output ends with a structured footer. This is a display convention (not a gate). The agent renders it as markdown; the user responds with a number or letter shortcut.

```
---
🔨 **Work:** {stage} | 🎯 {layer} | 📊 Guard: {score}%

**Skills loaded:** {loaded_list}
**Available:** {available_count} more via skills-db

🪄 **Next:**
1. [s] Skills — browse/load from skills-db
2. [r] Research — deepen with lev-research
3. [p] Prior art — review tracker items and PM artifacts
4. Proceed to SPEC
5. All of the above
6. ⬅️ Back to DISCOVER

#### PM Artifact Promotion Path

The live lifecycle stays in `.lev/pm/*`.

Promotion rules:
1. Reports stay in `.lev/pm/reports/` unless later mined into proposals or decisions.
2. Proposals and designs may be promoted to `docs/_inbox/` when ready for manual review.
3. Specs remain operationally canonical in `.lev/pm/specs/` until explicitly promoted.
4. Plans remain operational in `.lev/pm/plans/` and do not promote directly to canonical docs.
5. Decisions may be promoted from the handoff to `.lev/pm/decisions/` when they become durable.

---

### SPEC ALIGNMENT — Hardening Pass Workflow

When `/work` detects a spec-alignment context (handoff with conflicts, hardening pass, spec rewrite request), it enters this sub-workflow instead of the standard PROPOSE→SPEC flow.

```
SPEC ALIGNMENT LOOP
┌──────────┐   ┌─────────┐   ┌───────────┐   ┌─────────┐   ┌──────────┐   ┌────────────┐
│ ANALYZE  │──▶│ CAPTURE │──▶│ INTERVIEW │──▶│ REWRITE │──▶│ PLAN     │──▶│ SCHEDULE   │
│ (agents) │   │(handoff)│   │ (1-by-1)  │   │ (spec)  │   │(gaps)    │   │ (tracker)  │
└──────────┘   └─────────┘   └───────────┘   └─────────┘   └──────────┘   └────────────┘
```

#### Phase 1: ANALYZE

Launch 1-3 read-only agents per spec cluster to identify:
- spec-vs-reality conflicts
- spec-vs-spec conflicts
- missing sections
- cross-references and open questions

#### Phase 2: CAPTURE

Update the handoff with:
- numbered conflicts
- user direction and decisions
- open questions
- cross-cutting themes

#### Phase 3: INTERVIEW

Present conflicts to the user and log decisions immediately in the handoff.

#### Phase 4: REWRITE

Update specs to describe the TARGET system based on user decisions.

#### Phase 5: PLAN CREATE

For each approved implementation gap, create a plan artifact under `.lev/pm/plans/`:
- `plan-bugfix-*` for behavior mismatches or regressions
- `plan-chore-*` for cleanup or migration slices
- `plan-impl-*` for implementation slices

#### Phase 6: SCHEDULE

Once the plan is approved, create or update the tracker for the current execution slice only.

---

### Aviation System Rules (Hardening Standards)

These rules apply to ALL specs in aviation/safety-critical projects. Enforce during SPEC ALIGNMENT and VALIDATE.

1. **No silent errors.** Every error must be logged, surfaced, or routed to clarification. No `except: pass`. No swallowed exceptions. No empty catch blocks.
2. **No uncontrolled fallbacks.** Fallbacks must be explicit, tested, and tightly scoped (like poc/cleanup strategy profiles). AI agents are terrible at implicit fallbacks — be hyper-vigilant.
3. **Everything is config-driven.** Magic numbers → config. Thresholds → config. Strategy toggles → config. Retry limits → config. Defaults are sane, overrides are explicit.
4. **One engine per concern.** Don't build parallel implementations of the same thing. One validation engine (strategy-driven, used at multiple pipeline points). One clarification mechanism (through session FSM). One telemetry system.
5. **Capture everything.** Every pipeline stage must emit structured telemetry: input, output, latency, decisions, errors. Audio files, transcripts, corrections, intent outputs — all persisted.
6. **Sweep for violations.** Periodically scan codebase for silent errors, swallowed exceptions, uncontrolled fallbacks. Eventually automate as CI gate.

---

#### FlowMind Naming Structure & Config Keys

The `work` skill recognizes specific configuration keys for identifying specs and promoting them:

| Key | Value Pattern | Purpose |
|-----|---------------|---------|
| `naming_structure` | `flowmind` | Enforce `spec-{module}.md` naming |
| `filename_mask` | `core-*-mask` | Regex for validating core filenames |
| `spec_target` | `docs/specs/` | Target directory for promotion |

Example Config (`.lev/config.yaml`):
```yaml
work:
  naming_structure: flowmind
  filename_mask: "spec-.*\\.md"
  spec_target: "docs/specs/"
```
---
```

Shortcut behavior:
- [s] -> ~/.agents/lev-skills.sh discover "{topic}" --json, present results, offer to cat SKILL.md
- [r] -> route to lev-research with current context
- [p] -> br search "{topic}" + cass search "{topic}"

---

## FSM States: EXECUTION PHASE

> **Note:** ROUTE and MANIFESTING are sub-operations within the EXECUTION PHASE, not distinct FSM states. The FSM states are the 7 states (+ discarded branch) in the diagram above. ROUTE selects which skill to invoke; MANIFESTING describes the handoff contract format.

### ROUTE -- Sub-Skill Routing

| Stage | Primary Skill | Secondary Skills | When |
|-------|--------------|------------------|------|
| **ephemeral** | None | `thinking-parliament` | Meta questions only |
| **captured** | `lev get` | `lev-research`, `deep-research` | Progressive context gathering |
| **captured** | `lev-research` | None | Deep research mode |
| **crystallizing** | `lev-learn` | `lev-cdo` | Guided intake when user invokes learn mode |
| **crystallizing** | `lev-cdo` | `thinking-parliament`, `work` alignment gate | Strategic design |
| **crystallizing** | `ux` | `lev-cdo`, `work` template routing | Product/design/UX shaping before spec |
| **crystallized** | `work` | tracker | Template-driven spec or plan authoring |
| **manifesting** | tracker | `work` handoff contract | Task tracking/coordination + handoff emission |
| **completed** | `work` | `cm`, `cass` | Closeout, reflection, and optional decision promotion |

Routing logic:
- `captured` + simple query → `lev get`; deep ambiguity or broad unknowns → `lev-research`
- explicit `learn` intent or underspecified request needing guided intake → `lev-learn` (proposal + handoff)
- `crystallizing` + product/design/UX framing needed → `ux` hub (routes to design-os, pencil, or pipeline)
- `crystallizing` + needs adversarial validation → `thinking-parliament` + `lev-cdo`; else → `lev-cdo`
- `crystallized` → route to the correct PM template (`spec`, `plan`, `design`, `proposal`) and tracker
- `manifesting` → tracker + mandatory handoff contract output

### MANIFESTING -- Handoff Contract (Required)

When emitting `handoff.md`, follow the checkpoint format contract below. This is the canonical handoff schema for continuity.

1. Write `3-15` checkpoints in chronological order.
2. For each checkpoint, use exactly one block type:
   - `⚡ CHECKPOINT Progress`
   - `📋 Code Context`
   - `📋 User feedback / ADR created`
3. Across checkpoints, include:
   - files worked on
   - files loaded into context
   - what was learned and why it matters
4. End with both:
   - `System Prompt for Next Agent`
   - `Context Confidence Score`
5. File location:
   - `.lev/pm/handoffs/{YYYYMMDD}-{workstream}-{component}-{slug}-session-{N}.md`
6. Template source:
   - `~/.agents/skills/work/templates/handoff.md`
7. Handoff must include:
   - `You Are Here`
   - `Next Agent Brief`
   - `Roadmap To Goal`
   - `Timeline`
   - `Decisions Log`
   - `Open Questions`
   - `Entity Matrix`
   - `Meta`
8. Promote non-ephemeral decisions to `.lev/pm/decisions/` when the promotion rule is met.
9. Shard the handoff when the documented sharding signals are hit and pruning no longer restores clarity.

### EXECUTE -- Spawn Workers

Based on PROPOSE and ROUTE outputs:

1. **Direct execution:** Load matched skill inline, execute in current context
2. **Ephemeral subagents:** Spawn via Task tool with skill content injected into prompt
   - Each agent gets: task description + inlined skill content + workspace context
   - Instruct agents to return manifest of files touched + executive brief
3. **Formal team:** Create team config, spawn via TeamCreate + Task tool
   - Assign workstreams with skill-to-agent mapping
   - Set dependency ordering between workstreams

#### Inline Learning Capture

During execution, immediately capture learnings that survive context compaction:

| Trigger | Command | Category |
|---------|---------|----------|
| Bug fixed | `cm add "{description}" --category bug --json` | bug |
| Gotcha discovered | `cm add "{description}" --category {cat} --json` | architecture, testing, tooling |
| Performance issue | `cm add "{description}" --category performance --json` | performance |
| Security concern | `cm add "{description}" --category security --json` | security |

Categories: `bug`, `performance`, `architecture`, `testing`, `security`, `workflow`, `tooling`

**Why inline:** Context compaction loses session details. `cm add` persists immediately to the playbook, surviving any compaction event.

### VALIDATE -- Quality Gates

> Full per-gate definitions (layer modulation, confidence routing, failure actions): `./references/gates.md`

#### Gate A: Preflight (before execute)

Must have:
- active handoff
- objective stated
- long-term goal recorded in handoff
- done condition recorded in handoff
- `Roadmap To Goal` present, with Step 1 matching the current execution slice
- at least one evidence reference

If a tracker exists:
- tracker scope matches the execution slice only

Else: block execution.

#### Gate Summary Matrix

| Gate | Transition | Severity | FORMAL Checks | DIRECT Checks | Confidence Skip |
|------|-----------|----------|---------------|---------------|-----------------|
| `gate:discover-align` | DISCOVER -> ALIGN | MANDATORY | 5/5 (strict) | 1/5 | >= 0.90 auto-pass |
| `gate:align-research` | ALIGN -> RESEARCH | CRITICAL | 7/7 | 2/7 | >= 0.90 skip to 3 |
| `gate:research-propose` | RESEARCH -> PROPOSE | MANDATORY | 6/6 | 1/6 | >= 0.90 skip to 1 |
| `gate:propose-spec` | PROPOSE -> SPEC | CRITICAL | 7/7 + human | 1/7 | >= 0.90 skip to 2 |
| `gate:spec-execute` | SPEC -> EXECUTE | CATASTROPHIC | 16/16 + human | 3/16 | Never fully skip |
| `gate:execute-validate` | EXECUTE -> VALIDATE | MANDATORY | 8/8 | 2/8 | >= 0.90 skip to 3 |
| `gate:validate-emit` | VALIDATE -> EMIT | CRITICAL | 10/10 + human | 1/10 | >= 0.90 layer-min |
| `gate:emit-learn` | EMIT -> LEARN | WARNING | 6/6 | 2/6 | >= 0.90 skip to 2 |

#### Confidence Routing Table

| Confidence | Gate Behavior |
|------------|---------------|
| >= 0.90 | Skip INFO + WARNING gates; execute MANDATORY+ only |
| 0.80 - 0.89 | Standard: all gates at their declared severity |
| 0.60 - 0.79 | All gates fire + deliberation mode (Think 5-role) required before PROPOSE |
| < 0.60 | All gates + extended checks + human review required before SPEC |

#### Backtracking Table

| Gate Failure | Backtrack To | Condition |
|-------------|-------------|-----------|
| `gate:discover-align` | DISCOVER | Insufficient context — re-interview or re-search |
| `gate:align-research` | ALIGN or DISCOVER | Misclassification or missing north star |
| `gate:research-propose` | RESEARCH | Insufficient depth — deepen analysis |
| `gate:propose-spec` | PROPOSE or RESEARCH | Think disagreement or alignment drift |
| `gate:spec-execute` | SPEC or PROPOSE | Missing sections or invalid contracts |
| `gate:execute-validate` | EXECUTE | Incomplete work — finish remaining items |
| `gate:validate-emit` | EXECUTE or VALIDATE | Test failures or visual validation failure |
| `gate:emit-learn` | EMIT (retry) | Write failure — never blocks LEARN |

**Max backtrack depth:** 3 consecutive failures at the same gate before escalating to human review.

#### CATASTROPHIC gate:spec-execute (Inlined — Never Skip)

The spec completeness gate has 16 checks and **cannot be degraded or bypassed** by any mechanism (confidence, layer, user override):

| # | Check | Pass Condition |
|---|-------|---------------|
| 1 | Spec file exists | `.lev/pm/specs/` contains the active spec artifact |
| 2 | Executive summary | Present and <= 3 paragraphs |
| 3 | Context defined | Existing state AND target state documented |
| 4 | BDD scenarios | Given/When/Then covering primary flows |
| 5 | Input/Processing/Output | I/P/O triples defined per scenario |
| 6 | Dependencies declared | All external deps with versions/contracts |
| 7 | Integration points | All integration boundaries documented |
| 8 | Breaking changes | Explicitly noted (even if "none") |
| 9 | Recommended skills | Execution skills listed |
| 10 | Team structure | Team + workstreams if complexity > Simple |
| 11 | Unit test cases | Test cases defined |
| 12 | Integration tests | Integration test scenarios |
| 13 | E2E verification | E2E verification command specified |
| 14 | Success criteria | Measurable criteria with acceptance thresholds |
| 15 | BD tasks created | Spec decomposed into BD epics/tasks |
| 16 | Rollback plan | How to undo if execution fails |

**Layer modulation:** FORMAL = all 16 + human sign-off; DIRECT = checks 1, 3, 14 only. See `./references/gates.md` for full per-tier breakdown.

**Failure:** CATASTROPHIC BLOCK. List every failing check with remediation. Return to SPEC. After 3 consecutive failures, escalate to human. Never auto-waive. Never skip. Never degrade severity.

#### Gate C: Validate Before Close

Must have:
- validation evidence recorded
- open blockers listed or resolved
- next action clear, or explicit `done confirmed` from Done Candidate Protocol
- reflection completed if work is in done-candidate state

Else: block close.

### EMIT -- Create or Update PM Artifact

Create or update the stage-appropriate PM artifact and keep the active handoff in sync.

| Stage | Canonical Path | Action |
|-------|----------------|--------|
| captured | `.lev/pm/reports/` | Create or update report |
| crystallizing | `.lev/pm/proposals/` or `.lev/pm/designs/` | Create or update proposal/design |
| crystallized | `.lev/pm/specs/` or `.lev/pm/plans/` | Create or update spec/plan |
| manifesting | `.lev/pm/handoffs/` | Update handoff |
| completed | `.lev/pm/validation-reports/` | Create validation report or closeout evidence |

Always update the active handoff when emitting any PM artifact.

### LEARN -- Session Close Ceremony

Final FSM step. Reflects on the session, records outcomes, updates the handoff, and optionally promotes durable decisions.

**Triggers:** Session end, `/handoff`, `/exit`, explicit `learn` close request.

#### Steps

1. **Record outcomes** for rules used this session:
   ```bash
   cm outcome {success|failure|mixed} {bullet-ids} --session $SESSION --json
   ```

2. **Add new learnings** not captured inline during EXECUTE:
   ```bash
   cm add "{learning}" --category {category} --json
   ```

3. **Reflect on session** (extract patterns):
   ```bash
   cm reflect --days 1 --json --dry-run
   # Review proposed rules. If good:
   cm reflect --days 1 --json
   ```

4. **Promote durable decisions** from the handoff if needed:
   - create ADR-style documents in `.lev/pm/decisions/`
   - link back to the source handoff

5. **Index session** for future search:
   ```bash
   cass index
   ```

#### Skip Conditions

- Ephemeral/brainstorm sessions (no learnings to record)
- Session < 5 minutes (insufficient depth)
- User flag: `--no-learn`

#### Session Close Checklist

1. Final handoff update (entity matrix, decisions, ticks, open questions).
2. Mark session status (`active` or `completed`).
3. Record next concrete action in `Next Agent Brief`.
4. If code changed, run applicable validations and record evidence.
5. Verify tracker text still describes only the execution slice; move any long-term framing back to the handoff.

## Done Candidate Protocol (Hard Contract)

"Done" must be deterministic.

A workstream is not done because implementation appears complete.
A workstream is done only when the done condition is satisfied and the reflection pass finds no material gaps.

### Trigger

Run this protocol whenever:
- `Remaining Steps = 0`, or
- the agent believes the current workstream may be complete

### Required reflection

Before marking a handoff `completed`, the agent must:

1. Review the current handoff.
2. Review all predecessor handoffs in the same workstream.
3. Produce a full status report and alignment check against:
   - goal
   - done condition
   - roadmap
   - decisions log
   - open questions
   - validation evidence
4. Record:
   - lessons learned
   - gaps or misses discovered during reflection
   - whether any pattern, command, template, or rule should be promoted into a skill or AGENTS.md
5. Decide:
   - `done confirmed`, or
   - `not done`

### If reflection finds gaps

- Do not close the workstream.
- Update the handoff roadmap with the newly discovered remaining steps.
- Re-enter the lifecycle at the appropriate stage.
- Record a tick explaining why the done-candidate failed.

### If reflection confirms done

- Mark the handoff `completed`.
- Record the deterministic evidence that satisfied the done condition.
- Record any skill-promotion or process-promotion recommendations.

### Rule

Assume reflection will often find something.
The purpose of the done protocol is to reveal misses before close, not to justify closing.

---

## Integration Points

### Lev Master Router

| Keywords | Route |
|----------|-------|
| get, search, find, lookup, read, ls, prior art | `lev get` |
| plan, design, build, research, analyze | **work** |
| learn, guide me, unstuck | **work** (`lev-learn` mode) |
| ask, wiz, wizard | **work** (`learn`/interview mode) |
| align, check, scan, security | **work** (validation gates) |
| workflow, workflows | `workflow` (create/list/run only) |
| execute, do it, run | **work** (routes to execute path; `work-mvp` is phase 2 execution binding) |
| install, setup, daemon, daemons | lev-core |

### Tracker Integration (br/bd/td)

- trackers represent the current execution slice only
- specs and plans may link to tracker items
- prior art checks may query the tracker
- completion closes slice-scoped tracker items only

### Team Mode

- Detect `variant.json` `swarmModeEnabled: true` or team keywords
- Use template-driven decomposition and explicit subagent routing
- Keep the handoff and entity matrix as the orchestration spine

---

## Error Handling

| Error | Severity | Response |
|-------|----------|----------|
| Confidence < 0.7 | WARN | Prompt user to clarify: research / design / spec / plan / handoff |
| Tracker not available | INFO | Continue without task integration; note in the handoff |
| Template missing | ERROR | Block artifact creation until the correct PM template exists |
| Tracker-plan boundary violated | ERROR | Rewrite tracker to execution-slice scope, record correction in handoff |
| Spec validation fail | CATASTROPHIC | Block manifesting transition; list missing sections |
| Done claimed without reflection | ERROR | Run Done Candidate Protocol, update roadmap if gaps found, block close |
| Skill discovery empty | INFO | Proceed with inline execution; no skill injection |
| `learn` helper missing | WARN | Run inline interview loop in `work`; still emit proposal + handoff |
| CM/CASS not available | INFO | Skip LEARN ceremony; note in output |

---

## Configuration

| Env Var | Default | Purpose |
|---------|---------|---------|
| `LEV_PM_REPORTS` | `.lev/pm/reports/` | Report output dir |
| `LEV_PM_PROPOSALS` | `.lev/pm/proposals/` | Proposal output dir |
| `LEV_PM_DESIGNS` | `.lev/pm/designs/` | Design output dir |
| `LEV_PM_SPECS` | `.lev/pm/specs/` | Spec output dir |
| `LEV_PM_PLANS` | `.lev/pm/plans/` | Plan output dir |
| `LEV_PM_HANDOFFS` | `.lev/pm/handoffs/` | Handoff output dir |
| `LEV_PM_DECISIONS` | `.lev/pm/decisions/` | Decision output dir |
| `LEV_PM_VALIDATION_REPORTS` | `.lev/pm/validation-reports/` | Validation report output dir |
| `LEV_SCRATCH` | `.lev/scratch/` | Free-form scratch area |

**Stage override:** `work --stage={ephemeral|captured|crystallizing|crystallized|manifesting}`

---

## Principles

1. **Progressive Disclosure** -- Start simple, add complexity as needed
2. **Fail Gracefully** -- Degrade when dependencies missing, don't block
3. **Validate Early** -- Check spec, prior art, alignment before proceeding
4. **Route, Don't Duplicate** -- Delegate to specialists, don't re-implement
5. **Context-Aware** -- Use workspace, artifacts, BD state for decisions
6. **Specs Drive Tests** -- Behavioral specs produce testable contracts
7. **Teams Scale Work** -- Match execution strategy to task complexity
8. **Learn Continuously** -- Capture learnings inline during execution; ceremony at session close

---

## Relates

### Master Router
- **Lev Master Router** (`lev/SKILL.md`) -- Routes all lev-* skills and work skill. Parent skill that dispatches to this skill for work requests.

### Related Skills
- `lev-research` -- Orchestrated research (DISCOVER + RESEARCH stages)
- `lev-cdo` -- Strategic design playbook (PROPOSE stage)
- `lev-learn` -- Guided interview intake to proposal (DISCOVER foreground track)
- `lev-align` -- Optional standalone drift-audit deep dive (ALIGN defaults to embedded work gate)
- `lev get` backend (`lev-find` legacy alias) -- Semantic context gather (DISCOVER background track)
- `br` / `bd` / `td` -- Task tracking via adapter (SPEC -> EXECUTE)
- `cm` -- Collective memory playbook (EXECUTE inline + LEARN ceremony)
- `cass` -- Content-addressable session search (DISCOVER + LEARN)

### Templates & References
- `./templates/report.md`
- `./templates/proposal.md`
- `./templates/design.md`
- `./templates/spec.md`
- `./templates/plan.md`
- `./templates/handoff.md`
- `./templates/decision.md`
- `./templates/validation-report.md`
- `./references/gates.md` — Full per-gate definitions (layer modulation, confidence routing, failure actions)

---

**Status:** v3.4.0 -- PM-first lifecycle contract, 1:1 `.lev/pm` template mapping, handoff bootstrap + sharding + decision promotion, `plan` restored as canonical execution artifact

## Technique Map
- **Role definition** - Clarifies operating scope and prevents ambiguous execution.
- **Context enrichment** - Captures required inputs before actions.
- **Output structuring** - Standardizes deliverables for consistent reuse.
- **Step-by-step workflow** - Reduces errors by making execution order explicit.
- **Edge-case handling** - Documents safe fallbacks when assumptions fail.

## Technique Notes
These techniques improve reliability by making intent, inputs, outputs, and fallback paths explicit. Keep this section concise and additive so existing domain guidance remains primary.

## Prompt Architect Overlay
### Role Definition
You are the prompt-architect-enhanced specialist for work, responsible for deterministic execution of this skill's guidance while preserving existing workflow and constraints.

### Input Contract
- Required: clear user intent and relevant context for this skill.
- Preferred: repository/project constraints, existing artifacts, and success criteria.
- If context is missing, ask focused questions before proceeding.

### Output Contract
- Provide structured, actionable outputs aligned to this skill's existing format.
- Include assumptions and next steps when appropriate.
- Preserve compatibility with existing sections and related skills.

### Edge Cases & Fallbacks
- If prerequisites are missing, provide a minimal safe path and request missing inputs.
- If scope is ambiguous, narrow to the highest-confidence sub-task.
- If a requested action conflicts with existing constraints, explain and offer compliant alternatives.
