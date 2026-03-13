---
name: do-plan
description: >
  Structured planning before complex implementation.
  Use this skill whenever the user mentions planning, architecture decisions,
  multi-file changes, migration strategies, or asks to "think through",
  "map out", or "figure out the approach" before coding. Also trigger when
  the task is open-ended, touches 3+ files, or requires evaluating multiple
  approaches. Do NOT use for single-file edits, straightforward bug fixes,
  or when the user already has an approved plan.
argument-hint: "[task description]"
---

Produce a self-sufficient, executable implementation plan through five phases:
discovery → framing → planning → challenge → synthesis.

If requirements are unclear or the solution space is wide open, run `brainstorming` first
to explore alternatives and get user sign-off on direction before entering discovery.

## Phases

Every subagent prompt MUST be self-contained — include all prior-phase context explicitly.

**Subagent dispatch policy**: Each role uses its specialized agent type. Every dispatch prompt MUST include:
- The exact output file path (`.scratch/<session>/<prescribed-filename>.md`)
- The constraint: "Write your complete output to that path. You may read any repository file. Do NOT edit, create, or delete files outside `.scratch/<session>/`. Do NOT run build commands, tests, or destructive shell commands."

| Phase | Agent type | Rationale |
|-------|-----------|-----------|
| Discovery | `@researcher` | Deep evidence gathering with structured E-level output |
| Planning | `@planner` | Angle-committed, no phase re-entry |
| Challenge | `@debater` | Adversarial Socratic dialogue, peer-reactive |

This is a prompt-level constraint, not a platform-enforced restriction. It is adequate for planning workloads where agents have no operational reason to modify source files.

**Session ID**: Generate per SPINE.md Sessions convention. Reuse across all phases of a single do-plan run. Carry forward into do-execute. Append to the session log at each phase boundary (discovery, framing, planning, challenge, synthesis). All output paths below use `<session>` as placeholder.

### 1. Discovery

Map the codebase before planning. Dispatch discovery subagents **in parallel** (`@researcher` type):

| Role | Persona | Output | When |
|------|---------|--------|------|
| `file-scout` | Traces entry points, call graphs, config flags, and change surface | `.scratch/<session>/plan-discovery-file-scout.md` | Always |
| `docs-explorer` | Extracts intended behavior, spec bullets, and ambiguities from documentation | `.scratch/<session>/plan-discovery-docs-explorer.md` | Always |
| `external-researcher` | Checks upstream breaking changes, API gotchas, and version compatibility | `.scratch/<session>/plan-discovery-external-researcher.md` | When touching external dependencies |

**Synthesis**: main thread reads all output files, merges into `discovery_findings`. All claims tagged with evidence level (see [Evidence Levels](#evidence-levels)). Conflicting claims across subagents → prefer higher evidence level; same level → flag for framing.

### 2. Framing

Distill `discovery_findings` into a `planning_brief` all planners share. Fields:

| Field | Content |
|-------|---------|
| `goal` | One-sentence task restatement, disambiguated by discovery |
| `scope` | Confirmed in/out with change surface |
| `constraints` | Hard limits (performance, security, backwards compat, API surface) |
| `key_decisions` | Numbered IDs, A/B/C options, explicit tradeoffs |
| `planner_focus_cues` | E2 pointers to entry points, patterns, tests — no narrative |
| `evidence_manifest` | Artifact paths with why-relevant; planners lazy-load from here |
| `docs_impact` | Classification: `customer-facing`, `internal`, `both`, or `none` — with skip rationale when `none` |

Classify `docs_impact` for every plan. When `none`, record explicit skip rationale in the brief. When `customer-facing` or `both`, changelog updates are in scope — load `use-writing` skill for changelog rules.

No raw dumps — distilled signals only.

Apply the Two-Way Door test to each `key_decision`: reversible decisions get a fast path;
one-way doors (rewrites, migrations, vendor lock-in) require exhaustive analysis. Evaluate
options on: correctness risk, operational complexity, team familiarity, migration cost, blast
radius. Limit to 2–3 options — never present 4+ without narrowing first.

Ask before dispatching planners if any `key_decisions` would materially change scope or risk.
Present context + options first, then prompt the user with short structured questions.

### 3. Planning

Dispatch planners **in parallel** (`@planner` type). Each receives `planning_brief` + `evidence_manifest` and produces an independent plan from a distinct angle:

| Role | Persona | Output |
|------|---------|--------|
| `conservative` | Rejects changes without a working codebase precedent; prefers no-change over novelty when risk is ambiguous | `.scratch/<session>/plan-planning-conservative.md` |
| `thorough` | Enumerates every edge case and failure mode; treats missing boundary coverage as a gap, not an optimization | `.scratch/<session>/plan-planning-thorough.md` |
| `innovative` | Proposes structural improvements when scope allows; must justify each departure from existing patterns with concrete benefit | `.scratch/<session>/plan-planning-innovative.md` |

**Synthesis**: main thread reads all output files, merges into `canonical_plan`. Deduplicate by meaning; rank E3 > E2 > E1 > E0; conflicting E2+ claims on blocking topics → targeted verification pass aiming for E3.

### 4. Challenge

Adversarial review of `canonical_plan`. Blocking findings MUST be E2+; E0-only blocking claims are advisory.

Challenge methodology: expose hidden assumptions, underestimated risks, and uncomfortable truths.
Ask: "Why must it be this way?" "What if that assumption is wrong?" "What are you avoiding?"
Flag over-engineering, under-engineering, and unnecessary abstraction. A blocking finding
requires a better alternative that is project-documented, industry-standard, or demonstrably
lower risk — never block without one.

Useful review lenses: approach correctness (`assumptions`) and non-functional risks (`nfr`: security, perf, scalability).
For visual architecture explanations, use the `visual-explainer` skill.

If blocking findings remain unresolved after asking, dispatch a structured debate **in parallel** (`@debater` type). Each debater receives: `canonical_plan`, unresolved blocking findings, and the full `evidence_manifest`.

| Role | Persona | Output |
|------|---------|--------|
| `thesis-champion` | Defends the canonical plan, steelmans its strengths, rebuts each objection with evidence | `.scratch/<session>/plan-challenge-thesis-champion.md` |
| `counterpoint-dissenter` | Attacks assumptions, surfaces hidden risks, proposes concrete alternatives for each weakness | `.scratch/<session>/plan-challenge-counterpoint-dissenter.md` |
| `tradeoff-analyst` | Weighs both positions, quantifies costs and reversibility, identifies irreversible commitments | `.scratch/<session>/plan-challenge-tradeoff-analyst.md` |

**Synthesis**: main thread reads all output files. Blocking findings that survive the debate (E2+ with no viable alternative surfaced) are incorporated into the plan. Findings resolved by the debate are closed with rationale.

### 5. Synthesis

Main thread only. Sole readiness authority. No subagent dispatch.

1. Assemble final plan using [references/plan-template.md](references/plan-template.md) as scaffold. Write the assembled plan to `.scratch/<session>/plan.md`.
2. Validate all content requirements (see [Plan Requirements](#plan-requirements)).
3. Confirm every blocking finding is incorporated or rejected with explicit rationale.
4. Confirm no open ask-checkpoint decisions without user-deferred evidence.
5. Emit readiness decision.

`semantic` gaps (missing test tasks, unresolved blocking findings, self-sufficiency failure) → re-run from framing.
`non_semantic` gaps (format, evidence shape) → fix inline.

## Evidence Levels

See AGENTS.md for E0–E3 definitions. Blocking claims MUST be E2+.

## Ask Policy

Ask whenever ambiguity materially affects scope, risk, or approach. Two pressure points:

- After discovery, before framing: blocking unknowns that would misdirect planning
- After challenge, before synthesis: contentious findings that remain unresolved

Never carry unresolved decisions silently into synthesis.

## Plan Requirements

Synthesis cannot declare readiness unless the plan includes:

- **Self-sufficiency**: executable without chat history; repo-relative paths; defined terms; decision rationale
- **Test tasks**: explicit for behavior-changing work; includes concrete scenarios (given/when/then), not abstract "add tests" placeholders
- **Edge/failure coverage**: enumeration for low risk; perspective table for medium/high risk
- **Docs tasks**: explicit for user-visible/API/config changes; includes changelog entries when `docs_impact` is `customer-facing` or `both`
- **Completion criteria**: testable acceptance conditions

See [references/plan-template.md](references/plan-template.md) for required sections and scaffold.

## Readiness Declaration

- `Plan is ready for execution.` — STOP. Do not proceed. Await explicit user approval before any execution begins. User approval means a direct confirmation in the next message (e.g. "go", "approved", "proceed") — the readiness declaration itself does not constitute approval.
- `Plan is NOT ready for execution` — followed by specific gaps listed.

## Iteration Cap

5 iterations per request. A reroute from framing through synthesis = one iteration.
On cap: freeze best plan snapshot and request explicit user approval to continue.

## Anti-Patterns

- Skipping challenge for complex scope
- Carrying E0-only objections as blocking findings into synthesis
- Declaring readiness when self-sufficiency contract is unmet
- Silently carrying unresolved `key_decisions` past the ask checkpoint
- Declaring readiness without `docs_impact` classification in the planning brief
