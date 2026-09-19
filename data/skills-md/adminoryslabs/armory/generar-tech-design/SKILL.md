---
name: generar-tech-design
description: Genera el Technical Design Document + ADRs (formato MADR) + criterios de aceptación de un proyecto, entrevistando al usuario decisión por decisión a partir de su PRD (y opcionalmente su Design.md o un repo existente). Use when the user asks to generate, draft, or create a technical design document, system architecture, or architecture decision records (ADRs) for a project, greenfield or brownfield.
---

# Technical Design Document Generator (Interactive)

## Goal

Produce a production-grade Technical Design Document (TDD) and its supporting Architecture
Decision Records (ADRs, MADR format) — thorough enough to guide real implementation and
traceable enough to justify itself to a future maintainer. This is not a light draft generator.

**This skill is conversational, not one-shot.** Never generate the full TDD in a single pass. Walk
the user through each architecture decision one at a time, present real alternatives with
trade-offs, ask which one they choose (or if they have a different idea), and only then write the
ADR reflecting their actual decision. An ADR the agent decided alone, without the user's input, is
a failure of this skill.

## Input

- `PRD.md` — **required**. Problem, users, scope, product-level acceptance criteria. If missing,
  stop and ask for it — do not fabricate PRD content, only architecture decisions belong to this
  skill.
- `Design.md` — **optional but desirable**. If present, use it as a primary input for data model
  decisions: the concrete data the interface implies (a discount field, a status badge, a filter)
  often reveals model requirements the PRD alone doesn't. If absent, proceed without it and note
  in `TECH-DESIGN.md` that no Design.md was available — do not block on it.

## Step 0 — Project type

Before anything else, ask the user: is this **greenfield** (from scratch) or **brownfield**
(existing codebase)?

- **Greenfield:** proceed directly to the Workflow below — no prior constraints to reconcile.
- **Brownfield:** ask for the path(s) to the existing repo(s)/components and any existing
  documentation (`README`, `CLAUDE.md`, prior ADRs or tech design docs). Read them before making
  any decision. Existing choices are not blank slates:
  - If a decision area is already settled by the existing code (e.g., the stack is already Node.js
    and Postgres), write its ADR with `Estado: Aceptado (heredado)`, documenting the existing
    choice as the Decision and skipping the interview for that area — unless the user explicitly
    wants to reconsider it, in which case treat it as a normal new decision but note in
    Consequences that it changes an established choice.
  - Never propose an architecture decision that silently contradicts what the existing repo(s)
    already do. If a new requirement from the PRD conflicts with the existing architecture, surface
    the conflict to the user explicitly instead of resolving it unilaterally.

## Workflow

1. Read `PRD.md` (required), `Design.md` (if present), and — for brownfield — the existing repo(s)
   and docs identified in Step 0.
2. Determine the decision areas that apply to this project from `assets/decision-areas.md`
   (components/repos, data model, API contracts, tech stack per component, state management,
   resilience/error handling, plus anything the PRD forces that isn't on that list). For brownfield
   projects, mark which areas are already settled per Step 0.
3. For each **new** decision area (not already settled by an inherited choice), **one at a time**:
   a. State the context: why this decision is needed, quoting what the PRD/Design.md implies.
   b. Present 2-3 real alternatives with concrete trade-offs (not a false choice — each option must
      be genuinely viable for this project).
   c. Ask the user which one they choose, or whether they have a different option in mind. Wait
      for the answer before continuing.
   d. Write the ADR immediately using `assets/adr-template.md`: the chosen option as Decision, the
      others as Alternatives considered (with the reason they were not chosen), and Consequences
      that include at least one real trade-off of the choice made, not only benefits.
4. After all decisions are recorded, derive acceptance criteria per key flow in the PRD, at a more
   granular level than the PRD's own criteria. Confirm with the user before finalizing if any
   criterion required a judgment call.
5. Assemble `TECH-DESIGN.md` from `assets/tech-design-template.md`, referencing every ADR by
   number, including inherited ones.
6. Write to disk:
   - `TECH-DESIGN.md` at the project root.
   - `adrs/0001-{slug}.md`, `adrs/0002-{slug}.md`, ... one file per decision (new or inherited),
     numbered sequentially in the order they were recorded.

## Quality Gate

Before closing, silently check:

- Every ADR has Context, Decision, Consequences with at least one real cost or trade-off, and — for
  new decisions — at least one rejected Alternative. Inherited ADRs (`Aceptado (heredado)`) are
  exempt from the alternatives requirement, since they document what already exists.
- No architecture decision contradicts the PRD's "No alcance" section, or the existing brownfield
  codebase, without that conflict being surfaced to the user first.
- Every UI element in `Design.md` (when available) that implies data has a corresponding data
  model decision.
- Acceptance criteria are verifiable, not vague adjectives.
- Every new decision in `TECH-DESIGN.md` was actually answered by the user — not filled in solo by
  the agent because a question was skipped.

## References

- `assets/decision-areas.md` — which decisions to walk through, and when to add ones not listed.
- `assets/adr-template.md` — MADR-lite format for each ADR, including the inherited-decision state.
- `assets/tech-design-template.md` — the TDD document that assembles and references the ADRs.
