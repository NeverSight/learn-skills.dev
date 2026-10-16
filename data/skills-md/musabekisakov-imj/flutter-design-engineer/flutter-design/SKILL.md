---
name: flutter-design
description: Orchestrate product-aware Flutter UI design and redesign from repository inspection through rendered verification. Use for new Flutter screens, multi-screen flows, major visual redesigns, design-led implementation, or ambiguous Flutter UI requests that require routing across audit, design-system, implementation, motion, accessibility, and visual-QA workflows.
---

# Flutter Design

Design with evidence. Do not jump from a vague request to widget code.

## Workflow

1. Inspect `pubspec.yaml`, Flutter/Dart versions, app structure, theme, routing, state management, reusable widgets, tests, and current git state.
2. Identify the product, primary user, critical action, platform mix, content hierarchy, constraints, and measurable success condition.
3. Classify the work and invoke the smallest useful specialist set:
   - Existing-interface diagnosis: use `$flutter-audit`.
   - Tokens, themes, or component contracts: use `$flutter-design-system`.
   - Approved UI implementation: use `$flutter-implementation`.
   - Transition or interaction motion: use `$flutter-motion`.
   - Accessibility, text scaling, keyboard, or RTL: use `$flutter-accessibility`.
   - Rendered review or golden tests: use `$flutter-visual-qa`.
4. Before implementation, record one explicit visual direction: type character, density, palette behavior, geometry, imagery, and motion character. Read `references/visual-direction.md` and `references/anti-slop.md`.
5. Enumerate data and interaction states: initial, loading, empty, populated, partial, error, offline, disabled, destructive confirmation, and success as applicable.
   For multi-domain dashboards or connected tools, read `references/connected-product-workflows.md` and define the connective model before arranging regions.
6. Define acceptance criteria for compact and expanded layouts, themes, text scaling, and critical interactions.
7. Implement only after direction and states are explicit.
8. Require static checks, rendered evidence, accessibility review, and one refinement pass before completion.

## Gates

- Ask one focused question when missing product context would materially change the design.
- Offer two or three visual approaches when direction is genuinely open; recommend one with product reasoning.
- Preserve existing business behavior unless the user authorizes behavior changes.
- Treat screenshots as evidence. Never claim visual parity or polish without inspecting rendered output.
- Report environmental limits explicitly when rendering or tests are unavailable.

## Output Contract

Lead with the implemented or recommended outcome. State the chosen direction, important interaction decisions, verified viewport/theme combinations, tests run, and unresolved limitations. Avoid narrating routine file operations.
