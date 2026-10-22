---
name: flutter-audit
description: Audit existing Flutter interfaces for product hierarchy, visual coherence, interaction quality, adaptive behavior, accessibility, and implementation risks. Use when asked to review, critique, diagnose, assess, or prioritize improvements to Flutter screens or flows; remain read-only unless implementation is explicitly requested.
---

# Flutter UI Audit

Diagnose before prescribing. Keep audit work read-only unless the user requests changes.

## Inspect

1. Read the screen, related state, navigation, theme, shared widgets, and tests.
2. Run the app or inspect screenshots when available. Record viewport, theme, locale, and state for each observation.
3. Evaluate:
   - product goal and primary action;
   - hierarchy, grouping, scan order, density, typography, color, and surface use;
   - navigation, forms, feedback, destructive actions, and recovery;
   - loading, empty, partial, error, offline, and success states;
   - compact and expanded layouts;
   - semantics, focus, text scaling, contrast, touch targets, RTL, and reduced motion;
   - widget boundaries, hard-coded dimensions, rebuild scope, and theme consistency.
4. Read `references/anti-slop.md`, `references/layout-and-density.md`, and `references/visual-qa.md` for applicable checks.
   For multi-domain surfaces, also read `references/connected-product-workflows.md` and verify that the connection is more than adjacent cards.

## Prioritize

Classify findings:

- P0: blocks a core task, creates data loss/security risk, or makes the interface unusable.
- P1: materially harms comprehension, accessibility, completion, or adaptive behavior.
- P2: weakens consistency, polish, or maintainability without blocking the task.
- P3: optional refinement with limited user impact.

For each actionable finding, cite the screen/state and relevant file or rendered evidence. Explain user impact and the smallest credible remedy. Separate facts from visual judgment.

## Deliver

Lead with the highest-impact pattern, not a long checklist. Include strengths that should be preserved, prioritized findings, missing evidence, and a recommended sequence. Do not imply verification for states you did not render or inspect.
