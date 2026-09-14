---
name: r-doc
description: "Project documentation governance: automatically initialize, index, audit, and maintain AGENTS.md, docs/, and planning, requirements, design, API, testing, release, and deployment documents. Use when users ask to manage project documentation, check documentation consistency, update AGENTS.md, or trace change impact; not a replacement for business-code implementation."
metadata:
  version: "0.1.0"
---

# r-doc: Project documentation governance

## Purpose

Maintain project documentation as a navigable, reviewable knowledge base with low context cost: have maintainers or AI agents read the project-root `AGENTS.md` first, then load only the minimum document set required for the current task through the indexes.

This is a project-level documentation standard, not a business-code implementation standard. The project's documentation hierarchy never overrides system instructions, the user's current request, or higher-level tool rules.

## When to use

Use this skill automatically in the following situations, or whenever the user explicitly invokes `$r-doc`:

- Initializing a project, organizing project knowledge, or completing missing documentation entry points;
- Working with plans, requirements, design, architecture decisions, APIs, testing, releases, deployment, rules, or process documents;
- Changing code, configuration, interfaces, data models, processes, deployment, or architecture;
- Checking documentation synchronization during code review, before merging, before release, or during maintenance;
- Finding missing, stale, duplicated, conflicting, broken, or incorrectly loaded documentation.

Do not start the full documentation-governance workflow for a purely local code refactor that does not affect public behavior, data, configuration, architecture, or project rules.

## Non-negotiable constraints

1. Scope work to the project root. Prefer the Git root; for non-Git projects, use the project root explicitly identified by the user.
2. The project root must contain `AGENTS.md` and `docs/README.md`. Complex topic directories must also use a fixed `README.md` as their index.
3. Keep `AGENTS.md` limited to the project overview, scope, quick start, context-loading order, key directories, commands, mandatory rules, prohibitions, task routes, and the `docs/` index. Link detailed knowledge from `docs/` instead.
4. Keep each topic document focused on one subject. Split mixed, hard-to-locate, or overlong topics. Do not create empty documents just to fill a directory.
5. Keep documentation synchronized with code, configuration, interfaces, processes, deployment, and decision changes. Record important constraints, pitfalls, and non-obvious decisions.
6. Never write secrets, tokens, passwords, sensitive personal information, or real values that could bypass security controls. Stop writing and report suspected sensitive information.
7. Merge non-destructively when `AGENTS.md`, `docs/`, or existing documents are present: preserve facts and history instead of overwriting or deleting them. Report conflicts and propose a single source of truth.
8. By default, modify only documents, indexes, templates, metadata, and documentation comments. Read code and Git diffs only to determine documentation impact; do not modify business code.
9. Do not treat file existence as documentation completion. Check indexes, links, status, relationships, and consistency of affected content.

## Standard workflow

Choose a lightweight or complete workflow according to the task, but complete every relevant check for high-impact work:

1. Identify the current development stage, task scope, and document types that may be affected.
2. Read the project-root `AGENTS.md` if it exists, `docs/README.md`, relevant nested `README.md` indexes, project-level `.r-doc.yaml`, and documents directly related to the task.
3. Inspect project structure, Git status/diff, and relevant code. Read only the code needed to determine documentation impact.
4. Build a document inventory and mark missing, stale, unindexed, broken, status-invalid, duplicated, conflicting, or suspiciously sensitive content.
5. Ask necessary clarification questions, then provide a focused modification plan. Do not write, move, archive, or configure documentation before the plan is confirmed.
6. Create or update `AGENTS.md`, indexes, topic documents, metadata, and project configuration according to the plan. Mechanical index, link, and date updates may be automated after confirmation.
7. Verify context-loading order, index coverage, links, metadata, relationships, stage gates, and sensitive-content checks.
8. Produce a governance report covering scope, findings, completed updates, blockers, non-blockers, verification evidence, and whether the current stage gate is satisfied.

For stage checklists, read [references/lifecycle-checklists.md](references/lifecycle-checklists.md). For the complete operating workflow, read [references/workflow.md](references/workflow.md).

## Document structure and indexes

Use this default structure and preserve a reasonable existing structure whenever possible:

```text
AGENTS.md
docs/
└── README.md
```

Add topic directories such as `requirements/`, `design/`, `decisions/`, `api/`, `testing/`, `releases/`, or `operations/` only when needed. Each topic directory's `README.md` must define its scope, list its documents, state the recommended reading order, and link to the parent index and specific documents. The root `AGENTS.md` must link to `docs/README.md`.

The recommended context-loading order is:

```text
AGENTS.md
→ docs/README.md
→ relevant topic README.md
→ target document
→ supplementary documents explicitly linked by the target
```

## Status, relationships, and conflicts

Topic documents normally use this lifecycle:

```text
draft → proposed → active → superseded → archived
```

When documentation disagrees with code, tests, or other documents, state the intended behavior, current behavior, conflict location, and decision that requires confirmation. Do not automatically rewrite the implementation into the standard or let the newest file erase other facts.

For metadata rules, read [references/metadata-schema.md](references/metadata-schema.md). For project-level overrides, read [references/project-config.md](references/project-config.md).

## Minimum report standard

Every final governance report must include:

```text
Current stage and inspection scope
Findings (missing, stale, conflicting, broken, or sensitive content)
Completed documentation updates
Remaining blockers and non-blockers
Verification methods and results
Current documentation stage gate: satisfied / not satisfied
```

Use templates only when they reduce repeated work. Read [references/templates/README.md](references/templates/README.md) first, then choose a template for the project type and current task. Do not generate batches of empty documents.
