---
name: flutter-implementation
description: Implement approved, production-quality Flutter interfaces with adaptive layout, complete states, project-native architecture, accessibility, and proportionate verification. Use when visual direction and behavior are sufficiently defined and the user asks to build, change, polish, or refactor Flutter UI code.
---

# Flutter UI Implementation

Implement the approved experience inside the host project's conventions.

## Before Editing

1. Confirm the visual direction, behavior, state matrix, and acceptance criteria. If absent and choices are material, return to `$flutter-design`.
2. Inspect neighboring screens, theme, routing, state management, generated code rules, test style, and current worktree changes.
3. Read only the relevant references: `references/flutter-architecture.md`, `references/adaptive-layouts.md`, `references/navigation-and-input.md`, and `references/states-and-feedback.md`.
   Read `references/connected-product-workflows.md` when one surface combines multiple domains or data sources.

## Implement

- Separate orchestration, domain state, and presentational widgets at boundaries that remain understandable in one file view.
- Prefer constraints and layout primitives over device-name checks or fixed coordinates.
- Reuse semantic theme roles and established components.
- Preserve callbacks, validation, analytics, navigation, persistence, and backend contracts.
- Implement all applicable loading, empty, partial, error, offline, disabled, destructive, and success states.
- Make focus, semantics, keyboard behavior, touch targets, text scaling, RTL, and reduced motion part of the implementation.
- Keep animations interruptible and avoid expensive work inside build/layout/paint paths.
- Preserve unrelated user changes in a dirty worktree.

## Verify

1. Run the project's formatter, analyzer, and relevant unit/widget/golden tests.
2. Render representative compact and expanded layouts, supported themes, and critical states.
3. Invoke `$flutter-accessibility` and `$flutter-visual-qa` for visually important work.
4. Refine material findings, then rerun affected checks.

## Deliver

Lead with what changed for the user. List key files, behavior preserved, checks run, rendered combinations inspected, and remaining environmental limitations.
