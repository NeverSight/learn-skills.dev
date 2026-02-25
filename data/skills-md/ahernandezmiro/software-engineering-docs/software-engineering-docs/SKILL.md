---
name: software-engineering-docs
description: Generate and maintain structured software engineering documentation for new or existing applications. Use when asked to create, update, or normalize requirements.md, use_cases.md, specification.md, architecture.md, uml.md, or tests.md from source code and existing docs, and when enforcing consistency and domain boundaries (for example, preventing endpoint-level details in high-level requirements).
---

# Software Engineering Docs

## Overview

Produce consistent, engineering-grade documentation from codebases and existing docs without documenting line-level implementation details. Keep requirements business-focused, keep interfaces and contracts explicit, and keep diagrams aligned with stated system boundaries.

## Workflow Decision

Choose exactly one mode before writing:

1. `full-generation` mode
- Use when docs are missing, incomplete, or untrusted.
- Scan repository context, derive the system model, then generate all required docs.

2. `doc-grounded-retrieval` mode
- Use when docs already exist and the user asks questions or asks for targeted updates.
- Read existing docs first, extract relevant sections, reconcile conflicts, and answer/update with explicit cross-file references.

## Core Rules

1. Do not document implementation internals that should remain in code.
2. Keep functional requirements at capability level. Avoid endpoint URLs, SQL, class names, or handler names in `requirements.md`.
3. Put interface and integration contracts in `specification.md`, not in `requirements.md`.
4. Keep all diagrams and narratives consistent with one shared system model.
5. Use stable IDs across files:
- Functional requirements: `FR-###`
- Non-functional requirements: `NFR-###`
- Use cases: `UC-###`
- Contracts: `CON-###`
- External systems: `SYS-###`

## Step 1: Build Project Context

For existing applications, inspect:

- Product docs (`README`, `docs/`, ADRs)
- Domain model (entities/value objects/events)
- Boundary code (controllers/routes/consumers/producers)
- Integration points (queues, DBs, third-party services)
- Test structure (unit/integration/e2e coverage patterns)

Use `scripts/project_inventory.sh` to collect a fast baseline inventory, then validate findings with targeted file reads.

## Step 2: Build Canonical System Model

Before generating docs, define:

1. Primary actors
2. Internal systems/services and responsibilities
3. External systems and contracts
4. Core domain entities
5. Primary business flows
6. Quality attributes (security, reliability, scalability, observability, performance)

Treat this system model as the single source for all generated documents.

## Step 3: Generate Documentation Set

Use `references/templates.md` and generate documents in this order:

1. `requirements.md`
- Include: goals, scope, `FR-*`, `NFR-*`, constraints, acceptance criteria at capability level.
- Exclude: endpoint paths, payload schemas, table names, framework-specific details.

2. `use_cases.md`
- Include all `UC-*` stories with actor, trigger, preconditions, main flow, alternates, exceptions, success guarantees.
- Include system interaction diagrams (Mermaid sequence/flowchart).

3. `specification.md`
- Include architecture style rationale (for example TDD/DDD/EDA/CQRS where applicable).
- Define high-level operational contracts `CON-*` between systems.
- For each contract include: purpose, inputs/outputs, preconditions, postconditions, failure modes, idempotency/retry notes.

4. `architecture.md`
- Include context/container-level system diagram.
- Include each system responsibility, ownership boundary, and dependency relation.

5. `uml.md`
- Include UML class/domain diagrams for significant entities.
- Include attributes and behavior-level methods only when domain-relevant.
- Omit persistence/ORM/tooling noise.

6. `tests.md` (if applicable)
- Map `FR-*` / `NFR-*` to validation strategy.
- Summarize coverage by test level (unit/integration/e2e/non-functional).
- List critical scenarios and quality gates.

## Step 4: Enforce Consistency Gates

Apply checks from `references/quality-gates.md` before finalizing:

1. Every `FR-*` is covered by at least one `UC-*`.
2. Every `UC-*` maps to one or more `CON-*` or internal operations.
3. Every external interaction in diagrams is represented in `specification.md`.
4. `NFR-*` map to measurable verification notes in `tests.md`.
5. No contradiction in terminology for systems/entities/actors across files.
6. No endpoint-level details in `requirements.md`.

## Step 5: Doc-Grounded Retrieval and Update

When docs already exist and user asks for focused outputs:

1. Read only relevant sections from existing docs first.
2. Build a short trace map (`requirement -> use case -> contract -> test`).
3. Return or update only the needed sections.
4. Preserve existing IDs unless user asks for refactoring.
5. If docs conflict, prefer newest authoritative file and call out the conflict explicitly.

## References

Load only as needed:

- `references/templates.md`
- `references/quality-gates.md`
- `references/diagram-patterns.md`
