---
name: revision-adversarial
description: Revisa de forma adversarial un Technical Design Document y sus ADRs, buscando activamente huecos, riesgos y decisiones débiles en vez de validarlos. Use when the user asks to challenge, stress-test, get a second opinion on, or adversarially review a technical design document, architecture decisions, or ADRs.
---

# Adversarial Design Review

## Goal

Challenge an existing Technical Design Document (`TECH-DESIGN.md`) and its ADRs, actively hunting
for gaps, unjustified decisions, and unconsidered risks. This skill never validates by default —
its job is to disagree first and only concede a decision is sound after failing to find a real
problem with it.

## Why this matters

Asking the same conversation that produced a design "are you sure about this?" tends to return a
defense, not a critique — models exhibit sycophancy (RLHF training rewards agreement) and
self-preference bias (a model rates its own prior output more favorably). Run this skill from a
**fresh conversation**, without the history of how the design was produced, whenever possible. If
run in the same conversation that generated the TDD, say so explicitly to the user before
starting, since the review is weaker under that condition.

## Required Input

- `TECH-DESIGN.md` and its `adrs/*.md` files — required.
- `PRD.md` and `Design.md`, if present — used to cross-check that no decision contradicts stated
  scope or UI requirements. Not required to run the review, but skipping them narrows it — say so.

## Workflow

1. Read `TECH-DESIGN.md` and every ADR in full.
2. For each ADR, check against this bar — it fails if any of these is missing or weak:
   - Context actually justifies the decision (not generic boilerplate).
   - Alternatives considered are genuinely viable options, not a false choice (two names for the
     same thing does not count).
   - Consequences include at least one real cost or trade-off, not only benefits.
   - The decision is proportional to the project's actual scale — flag both over-engineering and
     under-engineering.
3. Check across documents:
   - Does any decision contradict the PRD's scope or explicit "No alcance"? (if PRD.md available)
   - Does every data-implying element in `Design.md` have coverage in the data model? (if
     Design.md available)
   - Are there missing decision areas entirely — components, data model, API contracts, stack,
     state management, resilience — that the project clearly needs but no ADR addresses?
4. Actively look for what isn't there: unhandled failure modes, missing non-functional
   requirements the PRD implies (performance, concurrency, offline use), and second-order
   consequences of a decision that its own ADR didn't mention.
5. Produce a findings report — do not edit `TECH-DESIGN.md` or any ADR directly. This skill
   reports; the human decides what to change.

## Output

A findings report, ranked most severe first:

- **Crítico** — the design will likely fail or contradict a stated requirement if unaddressed.
- **Advertencia** — a real gap or weak justification, worth fixing before implementation.
- **Sugerencia** — a smaller improvement, not blocking.

Each finding: which ADR or section it targets, the concrete problem, and why it matters — not a
vague "consider reviewing this." If, after genuinely trying, no real issue is found in an area,
say so plainly instead of inventing a minor one to appear thorough.

## Quality Gate

Before returning, silently check:

- Every ADR was actually challenged — none were skipped or rubber-stamped.
- At least one finding names a real trade-off the original ADR missed, or the report explicitly
  states the design held up under scrutiny — never a generic "looks solid" with no specifics.
- No finding is invented just to pad the report.
