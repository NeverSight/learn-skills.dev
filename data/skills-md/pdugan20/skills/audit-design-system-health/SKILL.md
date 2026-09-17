---
name: audit-design-system-health
license: MIT
description: Audit one or more code repositories for design-system drift, hardcoded visual decisions, inconsistent token or primitive use, overlapping UI components, missing system capabilities, and enforceable rules. Produce a prioritized read-only health and consolidation report grounded in source and rendered evidence. Do not use for aligning one component, UI ideation, greenfield system creation, Figma-only audits, or automatic refactoring.
---

# Audit Design-System Health

## Core outcome

Turn broad repository signals into a defensible, read-only account of design-system coherence. Identify what should converge, what should remain intentionally different, what the system cannot yet express, and which stable rules deserve automation.

## Frame the audit

1. Read repository instructions, inspect dirty work, and name the repositories, platforms, and UI surfaces in scope. Do not modify files, install tools, or change CI during the audit.
2. Record the user's decision goal and known concerns. Do not require a formal design-system team, Figma library, or governance model when the system is encoded informally in product code.
3. State the evidence budget: broad static inventory plus representative semantic and rendered samples. Avoid exhaustive builds or renders unless they would change a material conclusion.
4. Use upstream Figma auditing when the request is Figma-only. If Figma is one authority among several, audit code here and clearly attribute any Figma evidence gathered through an available upstream capability.

## Map the implemented system

Locate and rank actual authorities:

- instructions, design documents, selected specifications, and migration notes;
- theme and token definitions, style entry points, platform adapters, and feature palettes;
- shared primitives, component exports, variants, and representative feature surfaces;
- previews, Storybook, development galleries, visual fixtures, and screenshots;
- lint rules, tests, accessibility checks, visual regression, and CI policy.

Record conflicts and adapters instead of pretending there is one canonical file. Separate general UI semantics from brand assets, data palettes, generated files, authored content, visualizations, emergency fallbacks, and intentional experiments.

## Gather and normalize signals

Read [references/signals-and-enforcement.md](references/signals-and-enforcement.md), then choose only the relevant stack guidance.

1. Run repository-native checks first. Use scoped source searches to inventory literal colors, spacing, type, shape, elevation, motion, raw platform controls, token usage, variants, and likely duplicated structures.
2. Exclude definitions and legitimate special domains before counting. Group equivalent values and aliases, then trace representative uses to semantic context.
3. Treat search matches and duplication scores as leads, never findings. Do not claim coverage percentages without a known denominator and repeatable extraction method.
4. Inspect history when it can distinguish deliberate divergence, independent duplication, migration residue, or a selected design decision.

## Test consolidation candidates

Cluster components using role, rendered structure, imports, styling, names, and source similarity. For every candidate compare:

- semantic role and ownership;
- content and state model;
- interaction and navigation behavior;
- accessibility contract and platform behavior;
- visual structure and allowed variants;
- dependency direction, migration cost, and likely API pressure.

Choose `merge`, `extract a smaller primitive`, `share tokens only`, `document the distinction`, `retire after migration`, or `no action`. Similar appearance or duplicated lines alone do not justify consolidation.

## Classify and prioritize

Assign each material finding one class:

- **Accidental drift:** A stable repository rule is bypassed without a semantic reason.
- **Intentional exception:** A departure serves brand, data, platform, content, error recovery, or selected product intent.
- **System gap:** A recurring legitimate need lacks a suitable token, primitive, variant, or documented pattern.
- **Consolidation candidate:** Multiple implementations may share a component, smaller primitive, or contract after the semantic test above.
- **Uncertain:** Evidence, rendering, denominator, or product intent is insufficient; name the discriminating check.

Prioritize with judgment: user and accessibility impact, spread, drift risk, evidence confidence, migration cost, and reversibility. Do not hide those dimensions behind a synthetic health score.

## Recommend enforcement selectively

Recommend automation only when the rule is stable, machine-detectable with low false positives, has a clear replacement or repair path, and has an explicit exception policy. Match the mechanism to the claim:

- lint or typed APIs for deterministic source rules;
- component, interaction, and accessibility tests for behavior;
- focused visual regression for stable rendered contracts;
- duplication reports for discovery, not hard failure thresholds;
- documentation or review guidance for product-intent judgments.

Describe the rule, scope, exclusions, migration prerequisite, owner, and whether it should begin as informational or blocking. Do not configure it during the audit.

## Report

Return:

1. scope, method, sampling, commands, and limitations;
2. an implemented source-of-truth map;
3. ranked findings with class, confidence, exact evidence, impact, and smallest action;
4. consolidation clusters with the semantic comparison and recommended disposition;
5. an enforcement matrix with false-positive and migration boundaries;
6. a staged remediation order that separates low-risk cleanup, system additions, migrations, and later enforcement;
7. intentional exceptions and unresolved checks that should not become backlog noise.

Do not redesign, refactor, install tooling, change policy, or claim compliance as part of the audit. Route a later bounded component correction to `align-ui-to-design-system`; substantial approved remediation should be planned and implemented separately.
