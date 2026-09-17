---
name: align-ui-to-design-system
license: MIT
description: Review one completed UI component or bounded surface against the design system evidenced in its repository, classify accidental deviations, intentional exceptions, system gaps, and uncertainty, then apply only approved corrections. Use for post-build UI conformance or normalization. Do not use for UI ideation, repository-wide audits, exact design translation, or general production hardening.
---

# Align UI to Design System

## Core outcome

Evaluate whether one selected UI surface belongs to the design system that actually exists in its repository without flattening justified product character. Return a bounded, evidence-backed review before changing code unless the user already authorized fixes.

## Set the boundary and mode

1. Read the nearest repository instructions and inspect uncommitted work.
2. Name the component or surface under review, its direct dependencies, and its user-facing job. Do not silently expand to the whole repository.
3. Select the mode from the request:
   - **Review:** Inspect and recommend only. This is the default for review, audit, or “what is off?” requests.
   - **Fix:** Apply findings the user explicitly authorized. A request to align, normalize, or fix the bounded surface authorizes relevant edits, but not a broader system refactor.
4. Preserve the selected product direction. If the user still wants alternatives, use `code-native-ui-ideation` instead.

## Establish repository authority

Use this evidence order and note conflicts rather than inventing certainty:

1. Explicit repository instructions, design documentation, tokens, theme definitions, and shared primitives.
2. Repeated peer components with the same semantic role, including their rendered states when practical.
3. Platform conventions and accessibility behavior.
4. Comments, history, and the component's selected product intent.

Frequency is evidence, not proof. A common pattern can be legacy drift; a rare choice can be intentional. Inspect only enough peers to establish a rule or expose uncertainty.

Record the surface contract before judging it: content, hierarchy, interaction, states, responsive or dynamic-type behavior, accessibility meaning, and any documented intentional departures. Render the component in its existing preview, Storybook, simulator, or browser surface when practical. If rendering is disproportionate or blocked, say which conclusions remain source-only.

## Review the surface

Check only applicable dimensions:

- semantic tokens, typography, color, spacing, shape, elevation, and motion;
- shared primitives, composition patterns, naming, and API shape;
- loading, empty, error, disabled, selected, pressed, focus, and overflow states;
- interaction semantics, target size, keyboard or platform input, and navigation behavior;
- contrast, accessible names, reading order, Dynamic Type or text scaling, reduced motion, and screen-reader behavior;
- responsive layouts, localization, long content, and relevant platform differences.

Do not treat visual sameness as conformance. Compare the component's role and behavior, not only literal values.

## Classify before recommending

Assign every material finding one class:

- **Accidental deviation:** Strong repository evidence establishes a rule, the component breaks it without a role-based reason, and a correction improves coherence or usability.
- **Intentional exception:** The difference supports the component's selected role or product intent while preserving system foundations. Keep it unless the user chooses otherwise.
- **System gap:** A legitimate recurring need cannot be expressed cleanly with current tokens or primitives. Propose the smallest reusable addition separately; do not hide the gap with another one-off or generalize from one occurrence.
- **Uncertain:** Evidence conflicts, rendering is missing, or product intent is unresolved. State the discriminating check or decision needed.

For each material finding report:

1. class and confidence;
2. exact file, line, render, or behavior evidence;
3. the repository rule or component intent it relates to;
4. user or maintenance impact;
5. the smallest justified correction or reason to preserve it.

End a review with an approved-sized recommendation set, not a generic checklist. Separate component fixes from optional system work.

## Apply approved corrections

When edits are authorized:

1. Fix accepted accidental deviations with existing tokens and primitives when they truly fit.
2. Preserve documented intentional exceptions.
3. Add or change a shared token or primitive only when repeated evidence and the user's scope justify system work; otherwise record the gap.
4. Render the changed surface and exercise the affected states and interactions.
5. Run focused repository checks proportional to regression risk.
6. Report applied fixes, preserved exceptions, deferred system gaps, evidence, and any remaining uncertainty.

Do not redesign the surface, audit unrelated components, perform production hardening, or rewrite a repository into a formal design system unless separately requested.
