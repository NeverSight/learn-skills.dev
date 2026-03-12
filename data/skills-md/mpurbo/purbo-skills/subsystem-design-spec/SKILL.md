---
name: subsystem-design-spec
description: >
  Use when creating or iterating on a detailed per-subsystem technical design
  specification from a system spec, before starting OpenSpec workflow. Triggers:
  "design spec", "subsystem spec", "write the spec for S1", "phase breakdown",
  "implementation phases", "mid-level spec", "technical design". Encodes
  opinionated progressive phase discipline with FP progression and contract
  boundaries. Do NOT use for high-level system specs (use brainstorming) or for
  OpenSpec artifacts (use openspec directly).
---

# Subsystem Design Spec

A **Subsystem Design Spec** is the bridge between a high-level System Spec and
OpenSpec's change workflow. It takes one subsystem from the system-level
architecture and produces a comprehensive, implementation-ready specification
with opinionated progressive phases.

**Core principle:** Define contracts and phases before any code exists. Each phase
is independently testable, contract-bounded, and follows FP progression:
types -> pure functions -> effects -> composition.

## When to Use

- A System Spec (high-level) exists with subsystems identified
- You're ready to deep-dive on one subsystem before starting OpenSpec
- You're creating the second+ subsystem spec and need convention consistency

**Do NOT use for:**
- High-level system specs (use `superpowers:brainstorming`)
- OpenSpec artifacts (proposal, design, tasks) — OpenSpec handles those
- Specs that don't decompose into implementation phases

## Process

### Step 1: Load Conventions

Before writing anything, check for a project conventions file:

```
Search: docs/conventions.md, docs/spec-conventions.md
```

**If conventions file exists:** Load it. It contains established naming patterns,
section structure, phase coding, and cross-subsystem contracts. Skip scanning
individual specs — the conventions file is the single source of truth.

**If no conventions file exists:** Scan for prior subsystem specs:

```
Search: docs/**/*-spec*.md, docs/**/*-design*.md, docs/prd/**/*.md
```

If prior specs are found, extract conventions from them:
- **Section structure and depth** — which sections, how detailed
- **Phase coding scheme** — e.g., S1.1, S1.2 (carry forward S2.1, S2.2, etc.)
- **Naming patterns** — design decisions (D1, D2...), user stories (US-{n}), acceptance criteria (AC-{n}.{y})
- **Cross-subsystem contracts** — types, traits, or schemas already defined
- **Phase granularity** — typical size estimates, task counts per phase

Present extracted conventions to the user before proceeding. Follow-on subsystem
specs MUST maintain consistency with established conventions.

### Step 2: Reference the System Spec

Load the parent System Spec section for this subsystem. Extract:
- **Subsystem purpose** and boundaries
- **Input/output contracts** with adjacent subsystems
- **Technology choices** already decided at system level
- **Architecture principles** (FP-first, immutability, etc.)

### Step 3: Guide Document Creation

Create the subsystem design spec iteratively with the user. The document follows
this structure (all sections required unless marked optional):

```markdown
# S{n} {Subsystem Name} — Subsystem Design Spec

**Version:** x.y
**Status:** Draft
**Date:** YYYY-MM-DD
**Parent Spec:** [System Spec Name](path) (Section N, S{n})

---

## 1. Overview
### 1.1 Goals
### 1.2 Non-Goals

## 2. Architecture
### 2.1 Component Diagram (mermaid)
### 2.2 Key Design Decisions
    D1 — {Title}: rationale, tradeoffs
    D2 — {Title}: rationale, tradeoffs
    ...

## 3. User Stories
    US-1: {Story} with AC-1.1, AC-1.2, ...
    US-2: {Story} with AC-2.1, AC-2.2, ...
    ...

## 4. Detailed Design
    Per-component subsections with behavior, schemas, flows

## 5. Output Contract
    Data schemas, file structures, API contracts, column definitions,
    constraints — the interface downstream consumers depend on

## 6. Error Handling
    Exit codes, error categories, handling strategy per category

## 7. Testing Strategy
    ### 7.1 Unit Tests — what's covered, key scenarios
    ### 7.2 Integration Tests — with mocks, full flows
    ### 7.3 End-to-End Tests — opt-in, real external services

## 8. Performance Considerations

## 9. Future Considerations (out of scope for v1)

## 10. Dependencies
    ### 10.1 Packages/Crates
    ### 10.2 External Dependencies

## 11. Implementation Phases
    (See Phase Design Discipline below)

## 12. Acceptance Summary
    Numbered list of acceptance conditions

## Appendices (optional)
    Reference material, API response structures, etc.
```

### Step 4: Apply Phase Design Discipline (Section 11)

This is the core opinionated section. Each phase must satisfy:

- **Independently testable** — verifiable with mocks, no prior phase fully needed
- **Contract-bounded** — exposes explicit types/traits/interfaces for downstream
- **Reviewable** — a human can review the phase's OpenSpec output in <=30 minutes
- **Sized for OpenSpec** — each phase becomes one OpenSpec change with <=8 tasks

#### Phase Template

```markdown
### S{n}.{m}: {Phase Name}

**Scope:** What this phase delivers — concrete, verifiable
**Size estimate:** ~N files, ~N lines
**Contracts consumed:** Prior phase contracts (or "None")
**Contracts exposed:**
- Type/trait/interface names and signatures
**Gate:** Exact command to verify (e.g., `cargo build && cargo test`)
**Verification:** How a human reviewer manually verifies this phase works
  beyond the gate command — what to inspect, what to run, what output to expect.
  This becomes the reviewer's checklist during the human review checkpoint.
**Review tier:** gate-only | spot-check | full-review (see Review Tiers below)
**Dependencies:** Which prior phases, and what specifically (contracts only)
```

#### Phase Ordering — FP Progression

1. **Phase 1 — always:** Domain types, core traits/interfaces, project scaffolding.
   No business logic. Only the type-level skeleton.
2. **Early phases (parallel-safe):** Config parsing, state management, I/O
   utilities, rate limiting — independent modules consuming Phase 1 types.
3. **Middle phases:** Pure-core logic, then effects/IO at boundaries.
   Concrete trait implementations (e.g., data source providers).
4. **Final phase:** Integration wiring, CLI/main entry point, dependency assembly.
   The imperative shell.

#### Phase Design Checklist

Before finalizing phases:

- [ ] Phase 1 defines ALL shared types and trait contracts
- [ ] Phases 2..N-1 are maximally independent (parallelizable where possible)
- [ ] Each phase has <=8 OpenSpec tasks (split if more)
- [ ] Contract types are defined BEFORE implementation that uses them
- [ ] Phase N can be tested with mocks even if Phase N-1 isn't implemented
- [ ] No phase has hidden coupling to another phase's internals
- [ ] Each phase has a concrete gate command
- [ ] Each phase has a verification section describing how to manually test it
- [ ] Each phase has a review tier assigned (gate-only, spot-check, full-review)
- [ ] Phase dependency graph is included showing parallelization opportunities

#### Phase Dependency Graph

Include a text diagram showing phase dependencies:

```
S{n}.1 (Types & Contracts)
 |-- S{n}.2 (Component A)
 |-- S{n}.3 (Component B)      <- parallel with S{n}.2
 |-- S{n}.4 (Component C)      <- parallel with S{n}.2, S{n}.3
 |    |
 |    |-- S{n}.5 (Provider X)  <- depends on S{n}.4
 |
 |-- S{n}.6 (Orchestration)    <- depends on S{n}.2-S{n}.4 contracts
      |
      --- S{n}.7 (CLI Wiring)  <- depends on all

Parallelizable: S{n}.2, S{n}.3, S{n}.4 can proceed in parallel after S{n}.1.
```

#### Review Tiers

Each phase is assigned a review tier that determines how much human attention it
needs at the checkpoint. This prevents the human from becoming the bottleneck in
a large system with many phases.

| Tier | When to Use | What Happens at Checkpoint |
|------|-------------|---------------------------|
| **gate-only** | Scaffolding, boilerplate, type definitions, infrastructure. Low risk, mechanical output. | Gate command passes → auto-proceed. Human is notified but doesn't need to act. |
| **spot-check** | Well-constrained phases with clear contracts. Moderate risk. | Human glances at the diff, verifies gate passed, proceeds unless something looks off. |
| **full-review** | Orchestration, business logic, external integrations, security-sensitive code. High risk. | Human reads the diff, runs verification guide, thinks about edge cases before proceeding. |

**Guidelines for assigning tiers:**
- Phase 1 (types & scaffolding): **gate-only** — if it compiles and tests pass,
  the types are correct
- Pure utility phases (rate limiting, CSV writer): **spot-check** — contracts
  constrain the implementation, quick glance suffices
- External integration phases (API clients, data sources): **full-review** —
  HTTP behavior, error handling, and edge cases need human judgment
- Orchestration / composition phases: **full-review** — this is where subtle
  bugs hide
- CLI / wiring phases: **spot-check** — mechanical assembly of already-reviewed
  components

### Step 5: Produce Conventions File

After the first subsystem spec is complete and reviewed, produce (or update) a
lightweight conventions file at `docs/conventions.md`. This file is the single
source of truth for subsequent subsystems — they read this instead of scanning
all prior specs.

```markdown
# Project Conventions

## Naming
- Subsystem codes: S1 (Downloader), S2 (DB Sync), S3 (Stream Ingest), ...
- Phase codes: S{n}.{m} (e.g., S1.1, S1.2)
- Design decisions: D{n} — {Title} with rationale
- User stories: US-{n} with acceptance criteria AC-{n}.{y}

## Document Structure
<list the section structure established in the first subsystem spec>

## Phase Design
- Ordering: types -> pure functions -> effects -> composition
- Max tasks per phase: 8
- Each phase exposes contracts consumed/exposed
- Phase dependency graph required

## Established Contracts
<list cross-subsystem contracts defined so far>
- S1 output: CSV files at data/{market}/{ticker}/{resolution}.csv (Section 5)
- S1 types in sati-contracts: OhlcvBar, TickerInfo, Resolution, CsvRecord
```

**Update this file** after each subsystem spec is finalized. Add new
cross-subsystem contracts and any convention refinements. Keep it under 50 lines.

### Step 6: Review and Iterate

Present the draft spec to the user. Iterate on:
- Phase boundaries — are they clean? Any hidden coupling?
- Contract completeness — are all inter-phase interfaces explicit?
- Design decisions — are tradeoffs documented?
- Size estimates — realistic for the scope?

## Naming Conventions

| Element | Format | Example |
|---------|--------|---------|
| Subsystem code | S{n} | S1, S2, S3 |
| Phase code | S{n}.{m} | S1.1, S1.2, S2.3 |
| Design decision | D{n} | D1, D2, D3 |
| User story | US-{n} | US-1, US-2 |
| Acceptance criterion | AC-{story}.{criterion} | AC-1.1, AC-1.2, AC-3.4 |
| Spec file | {project}-s{n}-{name}-v{version}.md | sati-s1-downloader-v1.md |

## Anti-Rationalization Table

| Thought | Reality |
|---------|---------|
| "The system spec is detailed enough" | System specs define boundaries. Design specs define internals. Different levels. |
| "I'll figure out phases during implementation" | Phases defined after coding starts are retrofitted, not designed. Contracts leak. |
| "These two phases are too small, I'll combine them" | Small phases are a feature. They enable focused review and parallel work. |
| "The contract is obvious, no need to write it" | Explicit contracts enable mock testing and subsystem isolation. Write it. |
| "I'll add the dependency graph later" | The graph exposes parallelization. Without it, phases are assumed sequential. |
| "This subsystem is simple, skip the full structure" | Simple subsystems still need contracts, phases, and testing strategy. |
| "I'll just follow the same structure as last time" | Read the existing specs and extract conventions explicitly. Memory drifts. |
