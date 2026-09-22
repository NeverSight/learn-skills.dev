---
name: baselinedocs-init
description: Create the first adaptive baseline documentation pack for a new task, feature, initiative, or coordinated multi-domain workflow. Use explicitly when no suitable pack exists and the user wants durable planning and operational memory from the start.
---

# Baseline Docs Init

Create the first factual, resumable documentation state.

## Inputs

Infer when safe:

- topic, business outcome, constraints, and task list
- `docs_dir`, defaulting to `docs/baseline`
- kebab-case `prefix`
- single-domain or multi-domain scope

Read `references/pack-contract.md` in full before creating or editing any pack file, every time. It is the only definition of which document owns which content; do not infer that from a filename, from an earlier session, or from memory.

Read `references/report-style.md` in full before reporting to the user, every time. It governs how a pack element is named in conversation; an identifier stated without its meaning is a question the user has to ask.

## Workflow

1. Confirm that no suitable pack already exists.
2. Inspect current code, canonical docs, repository state, and explicit decisions.
3. Choose the layout:
   - one pack for a bounded domain
   - an initiative index plus directly linked domain packs for dependent multi-domain work
4. Create the three core documents.
5. Add `sourcecode` and `useguide` only when their roles are applicable.
6. Write roadmap phases with dependencies, acceptance criteria, verification gates, and one exact next action.
7. Record unresolved decisions only when evidence and business context do not support a safe choice.
8. Mark every claim as implemented, planned, unverified, or decided as appropriate.

## Writing Rules

- Write English documentation unless the repository requires another language.
- Keep task history separate from reusable wiki guidance.
- Record final evidence instead of every attempt.
- Use Mermaid v8.8.0-compatible syntax when a diagram materially improves understanding.
- Never present build, formatting, or static inspection as proof of live integration behavior.

## Output

Create the pack rather than returning only a chat plan. Report paths, open risks, and the first executable step.

## Boundaries

Use `baselinedocs-save` when work is already underway and the user wants a durable capture. Use lifecycle skills for later sync, audit, maintenance, or wiki extraction.
