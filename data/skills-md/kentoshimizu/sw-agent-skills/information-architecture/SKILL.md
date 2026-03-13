---
name: information-architecture
description: "Information architecture workflow for navigation structure, content hierarchy, and labeling clarity across product surfaces. Use when content/navigation structure is unclear and teams need explicit hierarchy and taxonomy decisions before screen-level design; do not use for backend data-model or deployment pipeline decisions."
---

# Information Architecture

## Overview
Use this skill to make product information structures findable, scalable, and consistent across surfaces.

## Scope Boundaries
- Use this skill when the task matches the trigger condition described in `description`.
- Do not use this skill when the primary task falls outside this skill's domain.

## Shared References
- Navigation depth and labeling rules:
  - `references/navigation-depth-and-labeling-rules.md`

## Templates And Assets
- Sitemap template:
  - `assets/sitemap-template.md`
- Taxonomy glossary template:
  - `assets/taxonomy-glossary-template.csv`
- IA validation checklist:
  - `assets/ia-validation-checklist.md`

## Inputs To Gather
- Content inventory and navigation pain points.
- User mental models and primary task priorities.
- Localization constraints and terminology rules.
- Product growth expectations affecting hierarchy scale.

## Deliverables
- Hierarchy and sitemap definition.
- Taxonomy and labeling rules with ownership.
- Navigation risks and ambiguity log.
- Discoverability validation results.

## Workflow
1. Audit current hierarchy and duplicate pathways.
2. Draft hierarchy in `assets/sitemap-template.md`.
3. Define taxonomy in `assets/taxonomy-glossary-template.csv`.
4. Validate labels with `references/navigation-depth-and-labeling-rules.md`.
5. Run `assets/ia-validation-checklist.md` against key user tasks.

## Quality Standard
- Hierarchy is navigable without unnecessary depth.
- Labels are clear across supported locales.
- Critical tasks are discoverable in predictable steps.
- Taxonomy ownership is defined for future changes.

## Failure Conditions
- Stop when taxonomy terms conflict across core surfaces.
- Stop when navigation choices cannot explain task findability.
- Escalate when critical tasks remain undiscoverable after redesign.
