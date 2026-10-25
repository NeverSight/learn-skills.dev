---
name: monozukuri-blueprint
description: "Author a greenfield build blueprint in four gated stages — business logic, tech stack, logic-to-stack mapping, and a phase plan — each requiring explicit user approval before the next. Use when building a new project or a substantial new subsystem from scratch; run by monozukuri-core for greenfield tasks."
user-invocable: false
---

# Monozukuri blueprint

This skill turns a framed idea into four approved artifacts and an ordered
phase plan. It does no implementation — it sets direction and order so each
phase can then be built under its own playbook.

## Use this skill when

- building a new project from scratch;
- adding a substantial standalone subsystem;
- the router selected the `greenfield` playbook; or
- the user asks for a build plan or blueprint.

## Do not use when

- the work changes an existing flow — that is `feature`;
- the work is a one-off script; or
- the request is a pure question.

## Prerequisite

`nemawashi` has run, or its output already exists. Blueprint consumes the
framed intent, users, and constraints; it does not re-ask them.

## The gate

After producing each stage's artifact, stop. Present it, say what the next
stage will do, and wait for explicit approval. A later stage may send you
back to revise an earlier artifact; re-approve the changed artifact before
resuming. Never begin a stage while the previous one is unapproved.

See `monozukuri-core/references/blueprint.md` for the full gate protocol and
for what a strong artifact at each stage looks like.

## Stages

### Stage 1 — business logic

- produces: `.monozukuri/blueprint/01-business-logic.md`
- contains: domains, actors and roles, entities and their relationships,
  business rules, primary flows, state transitions, invariants, and notable
  edge cases — in plain language.
- refuses: any technology, framework, or datastore choice; naming a library.
- template: `monozukuri-core/references/templates/blueprint/business-logic.md`

### Stage 2 — tech stack

- produces: `.monozukuri/blueprint/02-tech-stack.md`
- contains: language and runtime, framework(s), datastore(s), infra and
  deploy target, and key libraries — each with a one-line "why this — over
  what", derived from a stage-1 need, `kanso` applied.
- refuses: a choice stage 1 does not justify; components added "for later".
- template: `monozukuri-core/references/templates/blueprint/tech-stack.md`

Significant choices — those whose later reversal would touch many modules or
the data model — also become ADRs under `.monozukuri/decisions/`.

### Stage 3 — logic to stack map

- produces: `.monozukuri/blueprint/03-logic-to-stack-map.md`
- contains: one row per stage-1 element (actor, domain, entity, rule, flow,
  state) mapped to exactly one home in the stack; orphans and unused
  components listed explicitly.
- refuses: leaving any stage-1 element unmapped.
- template: `monozukuri-core/references/templates/blueprint/logic-to-stack-map.md`

### Stage 4 — phase plan

- produces: `.monozukuri/blueprint/04-phase-plan.md`
- contains: ordered phases, each with `intent` (one line), `affected`
  (areas or files), `prereqs` (earlier phase ids and named external
  dependencies, or "none"), `playbook`, and `risk`. Phase 1 is a vertical
  slice through real boundaries; later phases run smallest first within
  prereq order (`monozukuri-core/references/checkpoints.md`).
- refuses: step-by-step task lists; a phase whose prereqs are not satisfiable
  by earlier phases.
- template: `monozukuri-core/references/templates/blueprint/phase-plan.md`

## Outcome

Four approved artifacts in `.monozukuri/blueprint/`, and a phase plan whose
phases each name a `playbook` (`feature | refactor | migration | release`)
and a `risk` tier (`low | medium | high | critical`).

## Handoff

After stage 4 approval, start phase 1. Its `playbook` and `risk` are already
set, so the router's classify step is already answered: go straight to that
playbook, render its Definition of Done from `definition-of-done.md` for the
stated risk tier, and execute. The detailed task list for the phase comes
from `spec-driven-implementation` / `writing-plans` at that point, not from
blueprint. Re-run `monozukuri-router` only if a phase proves misclassified.

If a referenced skill is not installed, apply its named lens inline instead
of trying to invoke it.
