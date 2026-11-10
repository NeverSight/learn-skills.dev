---
name: revit-workflow
description: Plan and review safe Autodesk Revit, pyRevit, Revit API, and Dynamo workflows. Use for Revit model automation, parameter/schedule/sheet operations, family or element data workflows, transaction-safe scripting, dry runs, and verification plans.
---

# Revit Workflow

Use this skill for Revit-specific automation and review. Keep general CAD/BIM strategy in `cad-bim-automation`; activate this skill when the task depends on Revit concepts, pyRevit, Dynamo, or the Revit API.

## Start with the environment

Record what is known before proposing implementation:

- Revit release and project type.
- Host: Revit API add-in, pyRevit, Dynamo, external automation, or manual workflow.
- Model scope: local, central/workshared, linked, cloud-hosted, family, or template.
- Target categories, views, sheets, schedules, parameters, families, and element IDs when available.
- Whether the operation is read-only or mutating.

Leave unknown values as `UNKNOWN`. Do not invent API members, parameter identifiers, units, or version-specific behavior.

## Safety contract

1. Prefer a read-only inventory or dry run before mutation.
2. Never overwrite the only copy of a model, family, export, or generated schedule.
3. Scope mutations to explicit element sets and report the proposed count first.
4. Treat worksharing ownership, design options, groups, links, pinned elements, and read-only parameters as possible blockers.
5. Use the host's supported transaction model for mutations; do not imply that partial writes are safe when the runtime cannot guarantee them.
6. Separate Revit facts observed in the project from assumptions and external documentation.
7. Require competent human review for regulated design conclusions.

## Workflow

### 1. Define the invariant

State what must remain true after the operation: element count, unique IDs, parameter schema, sheet numbering, family placement, geometry, or another measurable condition.

### 2. Inventory

Produce a compact preflight table with target scope, candidate count, exclusions, blockers, and unknowns. For write operations, identify a reversible output or backup strategy.

### 3. Choose the smallest automation surface

Prefer the least complex surface that reliably satisfies the task:

- Native Revit UI for one-off deterministic edits.
- Dynamo for graph-friendly parameter/data transformations that benefit from visual inspection.
- pyRevit for repeatable team tools and lightweight Python-driven workflows.
- Revit API add-ins for compiled, maintainable integrations requiring deeper API control.

Do not claim one surface is universally superior.

### 4. Plan mutations

Describe selection/filter logic, validation gates, transaction boundaries, failure handling, and output logging before code or graph construction. For parameter writes, preserve storage type and unit semantics.

### 5. Verify

After execution, compare before/after counts and the invariant. Sample changed elements by stable identifiers where possible. Report skipped and failed elements separately from successful changes.

## Output contract

For implementation plans, return:

1. **Environment and assumptions**
2. **Preflight inventory**
3. **Proposed workflow**
4. **Mutation/transaction boundaries**
5. **Verification and rollback**
6. **Unknowns requiring confirmation**

For reviews of existing scripts or graphs, prioritize data-loss risks, transaction correctness, version assumptions, element filtering, parameter/unit handling, and observable verification.

## Boundaries

Do not present Autodesk API details as current unless they are verified against the relevant Revit release documentation or the user's inspected environment. Do not encode office-specific standards or jurisdictional rules as universal Revit behavior.
