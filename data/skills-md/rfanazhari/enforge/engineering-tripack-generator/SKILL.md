---
name: engineering-tripack-generator
description: >
  Generates or revises the three standard technical documents ("tripack") for feature work
  in a software project: technical-design.md, tactical-strategy.md, and task-plan.md —
  plus an optional decision-log.md capturing business-driven technical decisions
  (readable by PM/PO/tech lead) whenever the input contains them.
  Stack-agnostic — it discovers the project's tech stack, architecture, and conventions
  from CLAUDE.md at the project root and from the codebase itself.
  Use this skill whenever the user wants an implementation plan — for a NEW feature, an ADJUSTMENT
  to an existing feature, or a REVISION of a previously generated tripack (enhance, adjust, or remove
  parts after a requirement change mid-development). Input can be a PRD, FSD, analysis document,
  or a direct feature description — no specific upstream document is required.
  Trigger phrases include: "generate tripack", "buat technical design", "buatkan task plan",
  "generate implementation plan", "buat rencana implementasi", "update tripack",
  "revisi technical design", "ada perubahan requirement", "re-sync doc",
  "adjust tripack", "tripack dari PRD/FSD ini".
  Do NOT use for: small bug fixes, doc reviews without generation, or general architecture questions.
---

# Engineering Tripack Generator

Generates or revises three standard technical documents for planning feature work in any
software project. Output is designed for direct use by engineers and can be reviewed by
a tech lead or PM.

The skill is **stack-agnostic**: it makes no assumptions about language, framework,
architecture, or tooling. Everything project-specific is discovered from `CLAUDE.md`
and the codebase (see Project Context Discovery), and the output templates adapt to
what is found there.

The tripack is the **source of truth** for implementation sessions (vibe coding per task):
task-plan tasks reference technical-design sections, so every task is traceable and
verifiable against the design.

## Project Context Discovery

Before generating anything, discover the actual project context. **Never fill
architecture, reuse, or schema details from assumption.** This step is mandatory
in every mode.

1. Read `CLAUDE.md` at the project root — it is the authoritative source for:
   - Tech stack (language, framework, database, API style — REST/gRPC/GraphQL/etc.)
   - Directory structure and where each kind of code lives
   - Code behavior conventions, patterns, and project-specific rules
   - Tooling (migration tool, codegen, test commands, lint)
2. Verify and complete the picture from the codebase: package/module structure,
   one or two similar existing features/flows as pattern references, interface
   definition files (proto/OpenAPI/GraphQL schema/route definitions), and the
   migrations directory if one exists.
3. Derive the project's **layer/component names** from what you find (e.g.
   handler/service/repository, controller/model/view, or whatever the project uses).
   Use the project's own vocabulary in all output documents — never impose a
   layer structure the project doesn't have.
4. If `CLAUDE.md` is missing or a critical detail is not discoverable, ask the user
   instead of guessing.

## Input

Any of the following, in any combination:

- PRD or FSD from the product team
- An analysis document produced earlier in the conversation or provided as a file
- A direct feature/change description from the user
- For Mode C: the existing tripack files (required) plus the change description

Constraints (e.g. additive only, no DB change, no domain entity change) must be known
before generating. If not stated in the input, **ask the user before proceeding.**

## Modes

Detect the mode from the input and the user's intent. If ambiguous, ask.

### Mode A — New Feature
No related implementation exists yet. Generate a fresh tripack.

### Mode B — Adjustment to an Existing Feature
The feature exists in the codebase, but no tripack (or none is provided).
Before generating, perform an **impact analysis** against the codebase:

- Identify affected components per layer (what is Modified vs Reused as-is)
- Identify affected entities/schema and whether migration is needed
- Identify backward-compatibility risks (API contract, consumers, data)
- Build the reuse map from actual code, not assumption

Then generate a fresh tripack that incorporates the impact analysis.

### Mode C — Revision of an Existing Tripack
A tripack exists and (usually) implementation is partially done, then requirements changed.
**Update, do not regenerate from scratch.** Steps:

1. **Baseline** — compare the existing tripack against the current code state.
   Classify: implemented-and-conforming / implemented-but-deviating /
   not-yet-implemented / code-not-covered-by-design. Ask the user for task
   progress status if it is not evident from task-plan.md checkboxes.
2. **Impact analysis** — map the new change onto the tripack: which design sections
   change, which entities/schema are affected (migration from the *current actual*
   schema, not the originally planned one), which completed work becomes invalid,
   and whether the change contradicts earlier decisions (flag contradictions —
   let the user decide which wins).
3. **Update technical-design.md** — the resulting doc must be fully self-consistent:
   a new reader should understand the current design without knowing its history.
   Record the change in the **Revision History** section (what changed, why).
4. **Update tactical-strategy.md** — adjust reuse map, net-new inventory, testing
   and rollout/rollback as needed.
5. **Regenerate task-plan.md for remaining work only** —
   - Preserve completed tasks and their `[x]` status if still valid
   - Mark invalidated tasks as `~~obsolete~~` with a one-line reason (do not delete)
   - Insert **reconciliation tasks first**: align already-written code (including
     schema migration) with the revised design, before any new-feature tasks

## Output

Three files:

1. `technical-design.md`
2. `tactical-strategy.md`
3. `task-plan.md`
4. `decision-log.md` — **optional, conditional**: generate only when the input or
   analysis surfaces technical decisions driven by business decisions/constraints
   (see "When to generate decision-log.md" below). Never create it as an empty
   formality. Its audience is PM / product manager / tech lead — see the template
   for tone rules.

Save to the output directory specified by the user. If none is specified:
save next to the input file if the input is a file; otherwise ask
(suggest `./docs/<feature-name>/` as the default).

---

## Output Templates

The templates below are the baseline structure. **Adapt terminology and sections to
the project discovered in Project Context Discovery** — use the project's actual
layer names, and rename/omit sections that don't apply (noted per section).

### File 1: technical-design.md

```
# Technical Design: [feature name]

## 1. Overview
[Brief description of the feature and its context]

### Goals
- [what this delivers]

### Non-Goals
- [explicitly out of scope]

## 2. API / Interface Contract Changes
[Adapt to the project's API style: gRPC/proto changes, REST endpoints & OpenAPI,
GraphQL schema, event/message contracts, CLI commands, or public library API]
[If none: "No contract changes required"]

## 3. Data Model & Schema Changes
[If none: "No schema changes required"]
- Affected entities and final schema (per the project's DB and migration tooling)
- Migration plan: forward migration + rollback path
- Impact on existing data (backfill, defaults, data loss risk)

## 4. Component Breakdown
[Use the project's actual layers/components as rows — discovered, not assumed]

| Layer/Component | Status | Justification |
|-----------------|--------|---------------|
| [project's layer 1] | New / Modified / Reused as-is | ... |
| [project's layer 2] | New / Modified / Reused as-is | ... |

### Detail per component
[For each New or Modified component: explain what changes and why]

## 5. Flow Sequence
[Step-by-step from entry point to result — request/response, event handling,
job execution, or whatever fits the feature]
1. [step 1]
2. [step 2]

## 6. Request / Response (or Input / Output)
[Diff or full spec of new input and output vs existing if changed]

## 7. Error Handling
[New errors added, their propagation path]

## 8. Constraints Checklist
- [ ] [constraint 1 from input]
- [ ] [constraint 2 from input]

## 9. Risks & Open Questions
[Implementation risks, unresolved questions]

## 10. Revision History
| Version | Date | Change | Reason |
|---------|------|--------|--------|
| v1 | [date] | Initial design | — |
```

### File 2: tactical-strategy.md

```
# Tactical Strategy: [feature name]

## 1. Implementation Strategy
[Additive-only / breaking change / mixed — and the chosen approach]

## 2. Code Reuse Map
| Component | Location | Used for |
|-----------|----------|----------|
| [function/class/module name] | [package/file] | [purpose] |

## 3. Net-New Code Inventory
| Item | Layer/Component | Type | Notes |
|------|-----------------|------|-------|
| [name] | [component] | [contract/handler/service/etc.] | ... |

## 4. Branching / PR Strategy
[Recommendation: one large PR or split, safe merge order; commit per task]

## 5. Testing Strategy
[Use the project's test framework and commands from CLAUDE.md]

### Unit Tests
- [what to unit test, focus on new logic]

### Integration Tests
- Happy path: [scenario]
- Error cases: [scenario per new error]

### Regression Tests
- [existing endpoints or flows that must still pass]

## 6. Rollout & Rollback
- Rollout: [feature flags, phased rollout, monitoring to add]
- Rollback: [trigger conditions, how to revert code and migrations safely]
```

### File 3: task-plan.md

```
# Task Plan: [feature name]

## Legend
- ID: T1, T2, ... (stable — never renumber on revision)
- Complexity: S (< 2h) | M (2–4h) | L (> 4h)
- Status: [ ] Todo | [~] In Progress | [x] Done | ~~obsolete~~
- ref: technical-design.md section this task implements
- DoD: definition of done (verifiable)

## Tasks

### Reconciliation (Mode C only — must be done first)
- [ ] T1. [align existing code/schema with revised design] — [Component] — [S/M/L]
      — depends: none — ref: design §X — DoD: [criteria]

### Sequential (must be done in order)
- [ ] T2. [Task title] — [Component] — [S/M/L] — depends: T1 — ref: design §X
      — DoD: [e.g. tests pass, lint clean, endpoint callable]

### Parallel (can be done simultaneously)
- [ ] T5. [Task title] — [Component] — [S/M/L] — depends: none — ref: design §Y
      — DoD: [criteria]

## Dependency Graph
T1 → T2 → T3
T5 (parallel, after T1)
```

### File 4 (optional): decision-log.md

**When to generate decision-log.md:** only when the input (PRD/FSD/analysis/user
statements) or the impact analysis reveals technical decisions that are *driven by
business decisions or constraints* — e.g. a product rule shaping where logic lives,
a deadline forcing a simplification, a compliance/regulatory requirement dictating
architecture, a pricing/tier decision shaping access control. Pure technical
trade-offs (library choice, internal patterns) do NOT belong here — they stay in
technical-design.md Justifications. If no business-driven decision exists, do not
create the file, and say so in the final summary.

**Audience & tone:** written for PM / product manager / tech lead. Business-first
ordering, plain language, no unexplained jargon. A PM must be able to read every
entry without an engineer translating.

```
# Decision Log: [feature name]

Technical decisions in this feature that exist because of business decisions or
constraints. Each entry records why, what it means for the product, and when it
should be revisited.

## D1: [short decision title, plain language]
- **Business driver:** [the business decision/constraint that triggered this,
  and who decided it — e.g. "Feature is premium-only (decided by PM, PRD §2)"]
- **Technical decision:** [what was chosen, explained in plain language]
- **What this means for the product:** [observable consequence for users/business —
  e.g. "free users get a clear upgrade prompt instead of an error"]
- **Alternatives considered:** [briefly, and why rejected — fair, no strawman]
- **Trade-offs accepted:** [honest, including the negative ones]
- **Revisit when:** [the business condition that should trigger re-evaluating this —
  e.g. "if the feature opens to all tiers" / "after launch deadline passes"]
- **Status:** active | superseded by D[x] (on [date], reason)
```

Decision IDs (D1, D2, ...) are stable and referenceable from technical-design.md
(e.g. "caching skipped — see decision-log D2") and from Component Breakdown
Justifications.

---

## How It Works

1. **Discover project context** (CLAUDE.md + codebase) — see Project Context Discovery.
   This determines the vocabulary and structure of everything generated below.
2. **Detect the mode** (A/B/C) and confirm constraints with the user if not stated.
3. **Analyze** — Mode B: impact analysis against the codebase.
   Mode C: baseline + impact analysis against the existing tripack and code.
4. **Generate/update technical-design.md** — architectural decisions: what is new,
   what is reused, why, and where each net-new component lives. Justify placement.
5. **Generate/update tactical-strategy.md** — execution: reuse, net-new, safe order.
   Testing must cover happy path + every new error + regression.
6. **Generate/update task-plan.md** — granular tasks, each independently verifiable
   and completable in one implementation session. Every task has: stable ID, title,
   component, complexity, dependency, design-section ref, and DoD.
7. **Generate/update decision-log.md if applicable** — during analysis (step 3),
   note every technical decision with a business driver; if any exist, write them
   to decision-log.md. In Mode C: check whether the new change contradicts any
   active decision — if so, surface it to the user, and on confirmation mark the
   old entry `superseded by D[x]` (never delete it) and add the new entry.
8. **Save the files** and summarize: mode used, key decisions, whether a
   decision-log was produced (and why not, if skipped), open questions.

## Rules

- **All output documents must be written in English**, regardless of conversation language
- Use the project's own layer/component names and conventions as discovered from
  CLAUDE.md and the codebase — never impose a structure the project doesn't have
- Do not write implementation code — design and planning only
- Never fill the reuse map, component status, or schema details from assumption —
  verify against the codebase first
- If there are blocking open questions (from the input or discovered during analysis),
  flag them to the user before generating
- In Mode C, never silently drop prior decisions: contradictions between old and new
  requirements must be surfaced, and history is preserved via Revision History,
  ~~obsolete~~ task markers, and `superseded` decision-log entries
- decision-log.md is conditional: create it only when business-driven technical
  decisions exist; keep its language accessible to PM/PO (plain language, no
  unexplained jargon), unlike the other three files which target engineers
- Task IDs are stable across revisions — add new IDs, never renumber
- Complexity estimates (S/M/L) are rough — engineers must still validate
