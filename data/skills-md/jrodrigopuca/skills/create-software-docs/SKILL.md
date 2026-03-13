---
name: create-software-docs
description: Orchestrate project documentation generation from codebase analysis using specialized sub-skills for scope analysis, architecture, development guides, ADRs, runbooks, APIs, data models, glossary, known issues, validation, and cleanup. | Orquesta la generación de documentación de proyecto desde el análisis del código usando sub-skills especializadas para alcance, arquitectura, guía de desarrollo, ADRs, runbooks, API, modelo de datos, glosario, problemas conocidos, validación y limpieza.
license: MIT
metadata:
  author: jrodrigopuca
  version: "1.5"
---

# Software Project Documentation Orchestrator

Generate or update structured project documentation by coordinating specialized documentation sub-skills.

For lightweight version history and maintenance notes, see [CHANGELOG.md](CHANGELOG.md).

## Overview

This skill is the **orchestrator** for project documentation. It does not try to author every document directly. Instead, it:

1. resolves the documentation `{scope}`
2. gathers shared evidence
3. decides whether to generate, update, or reconcile documentation
4. decides which sub-skills are applicable
5. executes them in the right order
6. consolidates output under `{scope}/docs/`
7. validates consistency before finishing

The orchestrator is responsible for hierarchy, activation order, and global quality rules.

It is also responsible for coordinating artifact handoffs between sub-skills using the shared handoff contract.

## Operation Modes

This skill should support three operating modes:

- `generate` — create documentation that does not yet exist for the selected `{scope}`
- `update` — refresh existing documentation while preserving still-valid content
- `reconcile` — align existing documentation with current repository evidence when drift, staleness, or partial inconsistency is detected

Default behavior:

- use `generate` when `{scope}/docs/` does not exist or is effectively empty
- use `update` when documentation already exists and the goal is to refresh only impacted content
- use `reconcile` when existing documentation appears inconsistent, partially stale, or unevenly maintained

## Output Convention

All generated files must live under `{scope}/docs/`, where `{scope}` is:

- the repository root for a single-project repo
- the selected app root in a monorepo
- the selected package root in a monorepo
- the selected service root in a multi-service repository

Never write documentation outside the selected `{scope}`.

## Available Sub-skills

Use these sub-skills as building blocks:

- `sub-skills/analyze-project-scope/`
- `sub-skills/create-project-overview/`
- `sub-skills/create-architecture-docs/`
- `sub-skills/create-development-guide/`
- `sub-skills/create-adrs/`
- `sub-skills/create-runbooks/`
- `sub-skills/create-data-model-docs/`
- `sub-skills/create-api-docs/`
- `sub-skills/create-glossary/`
- `sub-skills/create-known-issues/`
- `sub-skills/validate-generated-docs/`
- `sub-skills/cleanup-and-review-docs/`

## Operating Rules

These rules are mandatory across all sub-skills:

1. **Do not invent facts.** Only document behavior, structure, commands, integrations, and architecture that are directly observable in the repository.
2. **Differentiate evidence from inference.** Mark reconstructed statements as **Inferred**. Mark low-confidence statements as **Needs confirmation**.
3. **Prefer omission over speculation.** If a section is unsupported, omit it or mark it explicitly.
4. **Cite repository evidence.** Every generated document must include a short **Sources inspected** section.
5. **Respect scope boundaries.** Do not mix evidence from outside the selected `{scope}` unless you clearly label it as external context.
6. **Keep cross-document consistency.** Names, modules, diagrams, and paths must agree across all docs.
7. **Validate before finishing.** Run the validation sub-skill before final cleanup and review.
8. **Polish before delivery.** Run cleanup and review before considering the documentation complete.

## Orchestration Policy

Use [references/orchestration-policy.md](references/orchestration-policy.md) for planning-time policy.

That reference defines:

- context loading and lazy-loading boundaries by stage
- downgrade rules when context, time, or repository size are constrained
- validation levels: `minimal`, `standard`, and `full`
- known-issues tracking modes: `compact` and `full`
- the fast path for `simple` projects

Default policy summary:

- load only the files needed for the current stage
- keep scope analysis and core docs mandatory when downgrading
- use `standard` validation by default
- use `compact` known-issues tracking for simple or minimal workflows unless stronger continuity needs exist
- use the simple-project fast path only when scope analysis clearly supports it

## Orchestrator Workflow

### 1. Resolve Scope

Call `sub-skills/analyze-project-scope/` first.

The scope analysis must determine:

- scope root
- scope type: repository, app, package, or service
- operation mode: `generate`, `update`, or `reconcile`
- project complexity: simple, medium, or complex
- main technologies
- major modules and entry points
- evidence inventory
- whether existing docs already exist under `{scope}/docs/`
- applicable document types

If the repository is partial, document the missing context explicitly.

### 2. Inspect Existing Documentation When Present

If documentation already exists under `{scope}/docs/`, inspect it before rewriting anything.

At minimum:

- identify which generated docs already exist
- determine which documents are still valid and mostly reusable
- determine which sections are stale, missing, or contradicted by repository evidence
- preserve valid content whenever safe
- avoid full regeneration when only specific sections or files need updates

### 3. Build the Generation or Update Plan

Based on scope analysis, decide which documents to generate.

In `update` or `reconcile` mode, decide which documents to:

- leave unchanged
- partially update
- substantially rewrite
- mark as obsolete or remove if they no longer fit the selected scope

#### Always generate

- `{scope}/docs/project-overview.md`
- `{scope}/docs/architecture.md`
- `{scope}/docs/development-guide.md`

#### Generate if applicable

- `{scope}/docs/decisions/NNN-title.md`
- `{scope}/docs/runbooks/*.md`
- `{scope}/docs/data-model.md`
- `{scope}/docs/api-reference.md`
- `{scope}/docs/glossary.md`
- `{scope}/docs/known-issues.md`

### 4. Execute Sub-skills in Order

Use this staged order unless there is a strong scope-specific reason to change it:

1. `analyze-project-scope`
2. sequential core docs:
   - `create-project-overview`
   - `create-architecture-docs`
   - `create-development-guide`
3. optional document batch:
   - `create-data-model-docs` if persistent data exists
   - `create-api-docs` if an API exists
   - `create-runbooks` if deployments or operations exist
   - `create-glossary` if domain language is non-trivial
4. `create-adrs`
5. `validate-generated-docs`
6. `cleanup-and-review-docs`
7. `create-known-issues` if there are unresolved, accepted, deferred, or clarification-worthy issues

Parallelization rule:

- the optional document batch may run in parallel only after scope analysis and the three core docs have stabilized the main terminology, structure, and boundaries
- parallelize only the sub-skills that are actually applicable and whose evidence is mostly independent
- prefer sequential execution when the scope is small, context is tight, or cross-document terminology is still unstable
- if optional docs run in parallel, merge and reconcile their artifacts before validation

Validation rule:

- select `minimal`, `standard`, or `full` validation before running `validate-generated-docs`, following [references/orchestration-policy.md](references/orchestration-policy.md)
- if cleanup or known-issues generation performs meaningful structural edits, run `validate-generated-docs` once more
- if cleanup makes only editorial or formatting changes, a `minimal` final pass is enough

In `update` or `reconcile` mode, run only the sub-skills needed for impacted documentation areas, but always keep scope analysis, validation, and cleanup in the loop.

### 4.1 Fast Path for Simple Projects

If scope analysis classifies the project as `simple`, apply the fast path defined in [references/orchestration-policy.md](references/orchestration-policy.md).

### 4.2 Coordinate Handoffs

Use the shared handoff contract to coordinate the workflow:

- consume the `Scope Analysis Artifact` from `analyze-project-scope`
- pass scope, evidence, and planning data into document-producing sub-skills
- when optional document sub-skills run in parallel, pass the same scope artifact and stable naming baseline into each of them
- pass `Document Generation Artifact` outputs into `validate-generated-docs`
- pass the `Validation Artifact` into `cleanup-and-review-docs`
- pass the `Validation Artifact` and `Cleanup Artifact` into `create-known-issues` when persistent issues remain worth tracking
- pass the selected known-issues tracking mode into `create-known-issues`
- request a final validation pass when cleanup or known-issues generation reports meaningful edits

In `update` or `reconcile` mode, also pass forward the knowledge of which documents already existed and which sections were intentionally preserved.

When validation is run below `full`, pass forward the selected validation level and any deferred checks so cleanup, known-issues generation, and final review do not assume deeper coverage than what actually happened.

When coordinating `knownIssueCandidates`, apply this boundary:

- keep ordinary validation findings in validation output if they do not need long-term tracking
- keep editorial or easy structural fixes in cleanup work when they can be resolved in the same pass
- send only persistent, evidence-backed, track-worthy issues into `create-known-issues` as input for the `Known Issues Document Artifact`

### 5. Update Scope README

After generation and validation, add or update a `## Documentation` section in the README that belongs to the selected `{scope}`.

In `update` or `reconcile` mode, preserve valid README links and only change what is required by the refreshed documentation set.

## Activation Rules

### `analyze-project-scope`

Always run.

### `create-project-overview`

Always run.

In `update` or `reconcile` mode, update only the impacted sections when the existing overview is still mostly valid.

### `create-architecture-docs`

Always run.

In `update` or `reconcile` mode, prefer section-level updates when the existing architecture doc still matches the current codebase broadly.

### `create-development-guide`

Always run unless the scope is purely documentary and has no executable development workflow.

### `create-adrs`

Run when you can identify important, hard-to-reverse, or cross-cutting technical decisions.

### `create-runbooks`

Run when the repository shows evidence of deployment, migration, operations, workers, queues, jobs, or incident handling.

### `create-data-model-docs`

Run when persistent data is present: ORM models, migrations, schemas, entity definitions, or database configuration.

### `create-api-docs`

Run when the scope exposes an API: routes, controllers, resolvers, RPC handlers, OpenAPI specs, or similar.

### `create-glossary`

Run when the scope uses domain-specific language, acronyms, bounded contexts, or internal terminology.

### `create-known-issues`

Run when validation, cleanup, or scope analysis surfaces unresolved issues, accepted limitations, deferred work, monitoring items, or clarification gaps worth preserving in documentation.

Do not run it for transient editorial noise or for minor findings that were fully fixed during validation and cleanup.

Use `compact` tracking by default for `simple` scopes or downgraded workflows, and `full` tracking for `complex`, `reconcile`, or history-sensitive cases.

### `validate-generated-docs`

Always run before final cleanup, and run again after cleanup if needed.

In `update` or `reconcile` mode, also verify that preserved content still matches repository evidence.

Choose the validation level explicitly:

- `minimal` for fast-path or downgraded runs
- `standard` by default
- `full` for complex, high-risk, or heavily preserved documentation sets

### `cleanup-and-review-docs`

Run after validation when documentation is intended for delivery, review, or long-term maintenance.

In `update` or `reconcile` mode, preserve valid existing phrasing when it remains accurate and consistent.

## Conflict Resolution

If sub-skills produce overlapping or conflicting information:

1. prefer direct evidence over inference
2. prefer the more specialized sub-skill over the more general one
3. if the conflict cannot be resolved, mark it as **Needs confirmation**
4. fix links and naming inconsistencies before finalizing

## Shared References

Use the shared references when they apply:

- [references/templates.md](references/templates.md)
- [references/diagrams.md](references/diagrams.md)
- [references/contracts/document-subskill.md](references/contracts/document-subskill.md)
- [references/contracts/non-document-subskill.md](references/contracts/non-document-subskill.md)
- [references/orchestration-policy.md](references/orchestration-policy.md)
- [references/contracts/update-reconcile-guidance.md](references/contracts/update-reconcile-guidance.md)
- [references/contracts/rules-and-checklists.md](references/contracts/rules-and-checklists.md)
- [references/contracts/sub-skill-handoffs.md](references/contracts/sub-skill-handoffs.md)
- the shared quality checklist in `references/quality-checklist.md`

Sub-skills may also have local references that specialize these shared materials.

## Completion Checklist

Before finalizing, verify:

- [ ] `{scope}` is explicit
- [ ] output files are inside `{scope}/docs/`
- [ ] every document includes evidence or sources inspected
- [ ] inferred statements are labeled
- [ ] diagrams reflect the real code structure
- [ ] runbook commands are evidenced by repository artifacts
- [ ] README links point to generated docs inside the selected scope
- [ ] the validation sub-skill has been run
- [ ] the validation artifact is specific enough to drive cleanup and re-validation
- [ ] cleanup and review has been completed for deliverable documentation
- [ ] cleanup output makes unresolved items and follow-up actions explicit when they remain
- [ ] known issues were documented when unresolved or accepted limitations remain
- [ ] existing valid documentation was preserved when operating in `update` or `reconcile` mode
- [ ] stale or contradicted sections were updated, removed, or explicitly marked
