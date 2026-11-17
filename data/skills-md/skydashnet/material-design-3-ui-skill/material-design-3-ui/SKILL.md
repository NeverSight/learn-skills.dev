---
description: Design, redesign, review, or implement user interfaces using Google Material Design 3 (M3), Material You, and optional Material 3 Expressive principles. Use for UI/UX screens, app flows, design systems, component selection, theming, responsive/adaptive layouts, accessibility audits, Figma-ready specifications, or developer handoff where Material Design 3 is required.
metadata:
  updated: 2026-10-01
  version: 1.1.1
name: material-design-3-ui
---

# Material Design 3 UI/UX

## Purpose

Create interfaces that **behave like Material Design 3**, not interfaces that merely look rounded or “Google-like.”

Treat M3 as a system:

**user goal → information architecture → hierarchy → adaptive layout → semantic tokens → components → states → interaction → motion → accessibility → visual expression**

M3 Expressive is optional. Use it to strengthen hierarchy, usability, recognition, and emotional clarity; never use it as permission to make every element loud.

## Source of truth

1.  Prefer current official Material 3 guidance at `https://m3.material.io/`.
2.  For Android implementation details, prefer `https://developer.android.com/`.
3.  Treat design guidance separately from implementation-library/API status.
4.  Verify current official guidance before asserting exact dimensions, dependency versions, experimental API names, or recently changed behavior.
5.  Do not silently mix Material 2 rules into Material 3.
6.  Pixel and Google-app screenshots are examples, not the specification.

## Core rules

### MUST

- Start from the user’s task, content, hierarchy, and platform before styling.
- Use semantic design tokens instead of scattered one-off values.
- Choose components by purpose and behavior, not visual resemblance.
- Prefer established M3/platform components when they solve the interaction.
- Define important states: default, pressed, focus, hover where applicable, selected, disabled, loading, error, empty, and success where relevant.
- Design for the available window rather than a guessed device category.
- Preserve accessible contrast, target size, focus, semantics, scaling, and non-color state communication.
- Respect system bars, safe areas, cutouts, keyboards/IME, foldable hinges, and edge-to-edge behavior where applicable.
- Keep primary actions distinguishable from secondary and destructive actions.
- Make custom components inherit the token, state, motion, and accessibility logic of the system.
- Explain deliberate departures from M3 when product requirements justify them.

### MUST NOT

- Do not “Materialize” a screen by only adding large radii, pastel colors, shadows, or Material Symbols.
- Do not hardcode raw colors throughout screens when semantic roles can be used.
- Do not use color alone to communicate meaning or state.
- Do not wrap every section or list row in a card.
- Do not maximize corner radius on every component.
- Do not use FABs for minor, destructive, or ambiguous actions.
- Do not use chips as generic buttons or primary navigation.
- Do not use tabs for unrelated top-level destinations.
- Do not make all components equally expressive.
- Do not invent a new control when an established M3/platform control already solves the interaction.
- Do not sacrifice accessibility to preserve a visual composition.
- Do not stretch a compact/mobile layout unchanged across wide windows.

## Progressive-disclosure references

Load only the references needed for the current task. Do not read every reference by default.

| Need                                                    | Read                                  |
|---------------------------------------------------------|---------------------------------------|
| Color roles, surfaces, dark theme, dynamic color        | `references/color-system.md`          |
| Type hierarchy, scaling, expressive typography          | `references/typography.md`            |
| Shape, cards, containment, elevation                    | `references/shape-and-elevation.md`   |
| Spacing, alignment, readable widths, safe areas         | `references/spacing-and-layout.md`    |
| Buttons, FAB, cards, chips, selection, inputs, feedback | `references/component-selection.md`   |
| Navigation bar/rail/drawer, tabs, app bars              | `references/navigation.md`            |
| Forms, validation, settings, text input                 | `references/forms-and-input.md`       |
| Snackbar, dialog, sheet, loading, empty/error states    | `references/feedback-and-overlays.md` |
| Responsive, tablet, foldable, desktop, multi-pane       | `references/adaptive-design.md`       |
| Accessibility audit or any final UI review              | `references/accessibility.md`         |
| Transitions, feedback animation, shape morphing         | `references/motion.md`                |
| Material 3 Expressive                                   | `references/m3-expressive.md`         |
| Final audit / suspicious “Material-looking” UI          | `references/anti-patterns.md`         |

For a broad end-to-end design, load the references incrementally as decisions require them. Always include the accessibility reference before final approval.

## Workflow

Follow this order unless the task explicitly scopes one stage.

### 1. Understand the product

Identify the platform, primary user goal and action, top-level destinations, content hierarchy, data density, input methods, brand constraints, required states and edge cases, target window sizes, and whether M3 Expressive is appropriate.

If missing information does not block the work, make a conservative M3-aligned assumption and state it. Ask only when the missing information materially changes architecture or interaction.

### 2. Establish information architecture

Before styling:

- Group related information and identify the primary task per screen.
- Separate navigation from actions and distinguish destructive actions.
- Remove duplicated controls and define progressive disclosure.
- Avoid showing information merely because space is available.

### 3. Choose adaptive structure

Read `references/adaptive-design.md` and `references/navigation.md` when multiple window sizes or navigation forms matter.

Prefer canonical patterns such as list-detail, supporting pane, feed, and adaptive navigation when they fit the content.

Wider space must improve context or productivity rather than merely stretch content.

### 4. Build the theme semantically

Read the relevant color, typography, shape/elevation, and spacing references.

Use the hierarchy:

**reference/system tokens → semantic/system roles → component tokens**

Screens should depend on semantic roles rather than scattered literal values.

### 5. Select components

Read `references/component-selection.md` plus specialized navigation/form/feedback references as needed.

For each important control, determine its semantic purpose, emphasis, immediate or transactional behavior, interaction states, accessibility behavior, and adaptive behavior.

### 6. Define states and feedback

Cover relevant loading, empty, error, success, disabled, selected, pressed, focus, hover, and busy/submitting states.

Error states must provide a recovery path.

### 7. Apply accessibility

Read `references/accessibility.md`.

Accessibility is a release requirement. Do not defer it to visual polish.

### 8. Add motion

Read `references/motion.md` only when motion is part of the task.

Motion must explain state, hierarchy, spatial relationship, or response. Do not animate for spectacle.

### 9. Apply M3 Expressive if appropriate

Read `references/m3-expressive.md`.

Use a few deliberate expressive moments. Routine reading, forms, settings, and dense productivity surfaces should remain calm unless stronger expression improves usability.

### 10. Audit before approval

Read `references/anti-patterns.md` and run the self-audit below.

## Self-audit

Before delivering a design, score each applicable category `0`, `1`, or `2`.

- `0` = incorrect / missing
- `1` = partially correct / needs refinement
- `2` = ready

| Category              | Check                                                        |
|-----------------------|--------------------------------------------------------------|
| Task clarity          | Primary user goal and action are obvious                     |
| Information hierarchy | Grouping and emphasis are coherent                           |
| Component semantics   | Controls match their actual behavior                         |
| Token discipline      | Semantic roles are used consistently                         |
| Adaptive behavior     | Layout improves across relevant windows                      |
| States & feedback     | Important states and recovery are covered                    |
| Accessibility         | Targets, contrast, semantics, focus, scaling, reduced motion |
| Expressive restraint  | Expression improves hierarchy without creating noise         |

A design with any `0` in **component semantics**, **states & feedback**, or **accessibility** is not ready for approval.

Do not inflate scores to satisfy the user. State the concrete issue and correction.

## Handoff contract

When asked to design, redesign, audit, or hand off a UI, provide enough detail for another designer or developer to reproduce the decisions.

Unless the user requests another format, include as applicable:

1.  **Design intent** — user goal and hierarchy.
2.  **Layout** — regions, panes, navigation, adaptive behavior.
3.  **Theme roles** — semantic colors, typography, shape, elevation.
4.  **Component map** — exact M3 component type/variant for important controls.
5.  **States** — interaction, loading, empty, error, success, disabled.
6.  **Accessibility** — target size, contrast, names, focus, keyboard, scaling.
7.  **Motion** — only meaningful transitions/state changes.
8.  **Implementation notes** — platform-specific caveats and experimental/unsupported APIs.
9.  **Self-audit** — include when the user asks for a review, audit, or production-readiness check.

When creating actual code or an artifact, apply these decisions instead of stopping at a description.

## Semantic handoff example

Prefer:

``` text
Screen background: surface
Primary text: onSurface
Secondary text: onSurfaceVariant
Primary CTA: filled button / primary + onPrimary
Secondary CTA: outlined button
Section container: surfaceContainer
Subtle separator: outlineVariant
Error container: errorContainer + onErrorContainer
```

Avoid handoff based on arbitrary literals unless they come from the project’s token system.

## Platform implementation notes

### Android / Jetpack Compose

- Prefer `androidx.compose.material3` for new M3 work.
- Prefer stable APIs for production unless alpha/experimental dependencies are explicitly accepted.
- Do not assume every M3 Expressive API is stable.
- Use Material theme roles rather than raw colors.
- Follow current Android adaptive guidance for resizable and large-window experiences.
- Treat edge-to-edge and system insets as layout concerns.
- For Wear OS, use Wear Material 3 rather than mixing mobile components.

Do not hardcode library version numbers into generated implementation unless they are verified against current official release notes.

### Web / other platforms

Material 3 guidance can inform the design even when an official implementation library does not expose every component.

- reproduce semantics and token relationships, not Android-specific quirks,
- preserve native platform accessibility and input conventions,
- mark custom implementations clearly,
- do not claim official platform availability without verification.

## Final principle

**Material Design 3 is a semantic, adaptive, accessible design system.**

A successful M3 interface should remain coherent when brand colors change, the window resizes, dark theme turns on, text scales up, keyboard replaces touch, or expressive styling is reduced.

If the design only works because every surface is rounded and colorful, it is not a robust Material 3 design.
