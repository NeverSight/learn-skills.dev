---
name: recon
description: "Map codebase topology, module seams, and execution call chains."
---

# recon — Codebase Topology & Architecture Cartography Engine

## Domain Rubric

### 1. Cartography Dimensions

- **Topography & Module Seams**: Entrypoints, schemas, data models, and architectural boundaries between subsystems.
- **Key Execution Flows**: Sequential call chains tracing runtime dispatch from intake to terminal state persistence with exact code pointers (`file:///path/to/file#L<N>`).
- **System Invariants & Gotchas**: Transaction boundaries, state lifecycles, hidden side-effects, or specification drift.

### 2. Exploration Guardrails (What to Ignore)

- Focus strictly on architectural transitions and module seams; forbid cataloging trivial leaf utilities, transient test fixtures, or dumping raw directory listings.

## Canonical Output Contract

```markdown
# Codebase Cartography: <Subsystem / Target Scope>

## 1. Topography & Architectural Seams
- **Entrypoints**: <Primary intake points, commands, public APIs, or event consumers with file pointers>
- **Core Contracts & Schemas**: <Key interfaces, data types, state schemas, or governing specifications>
- **Module Boundaries**: <Key directories/packages and their distinct architectural responsibilities>

## 2. Key Execution Flows
### Flow: <Primary Flow Name, e.g., Data Intake / Transformation / Render Pipeline>
1. `<Symbol>` ([<file>#L<N>](file:///path/to/file#L10)) ── <Trigger or input intake>
2. `<Symbol>` ([<file>#L<N>](file:///path/to/file#L50)) ── <Intermediate dispatch, orchestration, or validation>
3. `<Symbol>` ([<file>#L<N>](file:///path/to/file#L90)) ── <Core state transition, persistence, or terminal execution>
*(Add secondary flow if distinct execution path exists)*

## 3. Invariants & Gotchas
- **Invariants (Must Preserve)**: <Core rules, transaction boundaries, or state lifecycles that cannot be broken>
- **Gotchas (Watch Out)**: <Hidden side-effects, spec drift, or surprising couplings; state 'None observed' if clean>
```

### Routing

- Caller requests a change whose direction is settled and execution paths/mutation boundaries are clear → (via /changeset).
- Discovered architectural tensions, trade-offs, or multiple viable implementation paths → (via /clarify).

## Execution Protocol

### Phase 1: Macro Anchor Grounding

1. Ingest target subsystem or codebase scope.
2. Scout high-level architectural anchors (entrypoints, key schemas, router boundaries) using file and symbol tools.
3. Establish anchor coordinates before deep inspection.

### Phase 2: Scale-Adaptive Cartography

1. Evaluate target scope scale:
   - *In-Turn Execution* (< 10 files or single cohesive module): Trace call flows against discovered anchors directly in-turn to eliminate subagent latency and token overhead.
   - *Subagent Fan-Out* (broad codebase or cross-layer scopes): Launch concurrent `research` subagents dynamically scaled to partitioned layers or caller-declared budget (Role: `Cartography Scout (<Layer>)`). Seed each with target boundary, discovered anchors, and Canonical Output Contract (offload extensive traces to `.agents/scratch/recon-<layer>-dossier.md`).

### Phase 3: Synthesis & Turn-Halt Gate (Fan-in)

1. Reconcile findings into the Canonical Output Contract with pointers to any offloaded dossiers.
2. Present the completed cartography into the conversation stream and halt turn immediately.

