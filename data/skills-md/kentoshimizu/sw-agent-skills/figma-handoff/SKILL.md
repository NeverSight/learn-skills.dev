---
name: figma-handoff
description: "Design-to-engineering handoff workflow for packaging implementation-ready Figma specifications, assets, and acceptance criteria. Trigger when approved Figma designs must be translated into engineering-ready handoff materials (specs, assets, states, acceptance criteria) before implementation starts; do not use for backend data-model or deployment pipeline decisions."
---

# Figma Handoff

## Overview
Use this skill to produce implementation-ready handoff artifacts that reduce ambiguity between design and engineering.

## Scope Boundaries
- Use this skill when the task matches the trigger condition described in `description`.
- Do not use this skill when the primary task falls outside this skill's domain.

## Shared References
- Handoff quality gates:
  - `references/figma-handoff-quality-gates.md`

## Templates And Assets
- Handoff package template:
  - `assets/figma-handoff-package-template.md`
- Asset inventory template:
  - `assets/figma-asset-inventory-template.csv`
- Acceptance checklist:
  - `assets/figma-acceptance-checklist-template.md`

## Inputs To Gather
- Finalized Figma frames, components, and variants.
- Token, interaction, and responsive behavior specs.
- Accessibility and localization constraints.
- Engineering constraints and implementation boundaries.

## Deliverables
- Handoff package with scope, states, and implementation notes.
- Asset inventory with source mapping and export spec.
- Acceptance checklist for engineering sign-off.
- Explicit open issues and follow-up owners.

## Workflow
1. Lock design source versions and confirm in-scope artifacts.
2. Build handoff package using `assets/figma-handoff-package-template.md`.
3. Export and register assets in `assets/figma-asset-inventory-template.csv`.
4. Add acceptance checks with `assets/figma-acceptance-checklist-template.md`.
5. Validate readiness against `references/figma-handoff-quality-gates.md`.

## Quality Standard
- Handoff scope is versioned, complete, and unambiguous.
- States, variants, and interactions are implementation-ready.
- Accessibility and localization constraints are explicit.
- Engineering owner can implement without inferred design intent.

## Failure Conditions
- Stop when source designs are not version-locked.
- Stop when required assets/spec details are missing.
- Escalate when implementation constraints conflict with design assumptions.
