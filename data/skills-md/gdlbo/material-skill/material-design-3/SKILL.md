---
name: material-design-3
description: Design, implement, or review Material 3 and Material 3 Expressive interfaces for Android Compose, Android Views, Wear OS, and the web. Use for Material Design, M3, Material You, adaptive Material layouts, Material-focused Android UI modernization, or Material web component work; do not apply it to a non-Material design unless the user asks to adopt Material
---

# Material Design 3

Build a coherent product interface with Material 3 semantics, components, tokens, interaction states, and platform behavior. The target is not a screen that merely looks vaguely Material. It must behave like a good Android or web product and use expression only where it improves hierarchy or comprehension.

## Resolve the Context First

Before changing UI, inspect enough of the project to answer:

- Which target is in scope: Android Compose, Android Views, Wear OS, or web?
- Which Material libraries and versions are already present?
- Is the requested API stable, experimental, or unavailable on that target?
- Which theme, components, navigation model, spacing conventions, and assets already exist?
- What is the screen's primary task, primary action, content hierarchy, and state model?
- Which compact, medium, expanded, desktop, foldable, and input scenarios matter?

Preserve established product identity and architecture. Prefer the existing theme and reusable components unless the task explicitly requests a redesign or migration. Never upgrade a dependency, opt into an alpha release, or migrate Views to Compose as an incidental styling change.

## Read the Relevant Reference

- For visual hierarchy, color, typography, shape, elevation, layout, and component choice, read [references/design-foundations.md](references/design-foundations.md).
- For Android libraries, Compose implementation, theming, system UI, and Views boundaries, read [references/android.md](references/android.md).
- When Material 3 Expressive is requested or materially useful, read [references/expressive.md](references/expressive.md).
- For responsive/adaptive behavior, accessibility, keyboard, focus, and verification, read [references/adaptive-accessibility.md](references/adaptive-accessibility.md).
- For HTML, CSS, web components, Angular Material, or another web framework, read [references/web.md](references/web.md).
- When selecting or upgrading dependencies, validating API availability, or citing guidance, read [references/sources.md](references/sources.md) and refresh version-sensitive facts from the official source.

Read only the references needed for the current target.

## Design Rules

### Establish hierarchy before decoration

1. Identify the one primary task and the minimum set of supporting actions.
2. Group content through alignment, spacing, typography, and background roles first.
3. Add a container only when it clarifies ownership, interaction, selection, or scrolling behavior.
4. Use component emphasis variants to express action priority.
5. Add expressive shape, color, or motion only after the basic hierarchy works.

### Use Material roles, not arbitrary values

- Consume `MaterialTheme` roles or Material web system tokens instead of scattering literal colors, shapes, type sizes, or elevations.
- Map content to semantic roles such as `surface`, `surfaceContainer`, `primary`, `onSurfaceVariant`, `outlineVariant`, and `error`.
- Keep light, dark, dynamic color, contrast, and disabled states coherent.
- Reuse the product spacing rhythm. Use isolated custom values only when content or a platform constraint justifies them.

### Keep surfaces quiet

- Do not wrap every section, row, metric, or control in an outlined card.
- Do not nest cards or stack several decorative containers around the same content.
- Do not repeat the same ownership, grouping, or emphasis with nested containers or surfaces. As a review heuristic, allow no more than one nested authored explicit container per three meaningful content units (`1:3`) inside a parent surface.
- When a content unit needs its own boundary and the parent's `1:3` budget would be exceeded, promote it to a sibling standalone container or surface instead of nesting it. Keep authored explicit containment to at most two levels from the region surface to that unit; framework internals and layout-only nodes do not count.
- Do not use outlines when spacing, a surface-role change, or one divider communicates the boundary.
- Use an official outlined component and its default border tokens only when a persistent boundary is part of that component's role. Do not add a second outline around the component or its parent.
- Use `outline` for boundaries needed to identify a component or state and `outlineVariant` only for lower-emphasis, nonessential separation. Never use a decorative low-contrast stroke as the sole focus, error, selection, or control-boundary cue.
- Do not use shadows as decoration. Reserve shadow elevation for actual overlap, modal separation, or a floating element whose depth must be legible.
- Prefer tonal elevation and surface-container roles for ordinary hierarchy.
- Avoid gradients, glow, blur, glass effects, and ornamental borders unless the product or supplied reference explicitly requires them.
- Do not make the default palette transparent, translucent, or "liquid glass." Material surfaces should have stable, readable color roles rather than letting wallpaper, imagery, or lower layers bleed through.
- Do not use `backdrop-filter`, frosted panels, alpha-heavy surface fills, translucent borders, or glass-like highlights to manufacture depth.
- Do not place important text, controls, forms, or navigation over a transparent image treatment when a stable themed surface would improve readability.
- If translucency is genuinely required for a system surface, media overlay, immersive viewer, or supplied brand reference, keep it localized, preserve semantic contrast, test light/dark and dynamic color, and provide a solid fallback.
- Do not apply the same large corner radius to every surface. Shape should communicate component family, grouping, state, or emphasis.
- Do not turn operational screens into landing pages, add oversized hero copy, or create empty space merely to appear premium.

### Use components for their intended jobs

- Give the highest-emphasis filled action to the main completion action; use tonal, outlined, or text variants for decreasing emphasis.
- Use a FAB only for a frequent, screen-level primary action. Do not add one just because it is recognizable as Material.
- Use cards for discrete, heterogeneous, independently actionable content. Prefer lists or unframed sections for dense homogeneous content.
- Use chips for compact attributes, filters, selections, or suggestions, not as generic buttons or decorative labels.
- Use tabs for peer views inside one destination, not for global navigation.
- Use dialogs for short blocking decisions, sheets for contextual choices or supporting tasks, and full screens for complex flows.
- Keep destructive actions explicit, separated from routine actions, and confirm only when recovery is difficult.

### Make every state intentional

Cover enabled, pressed, focused, hovered where applicable, selected, disabled, loading, empty, error, offline, and success states that the workflow can actually reach. Do not communicate state through color alone. Preserve content and layout stability during asynchronous changes.

### Treat loading and forms as product states

- Choose progressive loading, skeletons, inline progress, or a simple indicator based on how much structure/content is known and how long the operation can take.
- Prefer stable placeholders that match the final geometry over a centered spinner that hides the entire screen.
- Reveal content progressively when independent regions are ready; do not block usable content behind unrelated work.
- Keep submit, validation, autosave, upload, and retry states explicit and recoverable.
- Keep form labels, supporting text, errors, required state, focus, keyboard/IME behavior, and action hierarchy visible in the design contract.
- Never disable the whole form without explaining what is happening or preserving safe navigation/cancellation.

## Material 3 Expressive Gate

Material 3 Expressive is a deliberate emphasis system, not a decoration pass.

- Use standard Material 3 by default for dense, repetitive, or highly utilitarian workflows.
- Use expressive motion, shape contrast, flexible typography, and new expressive components for prominent moments where they improve attention, feedback, or emotional tone.
- Keep recurring utility interactions calmer than key transitions or hero interactions.
- Do not morph every control, animate every size change, or use the shape library as background ornament.
- Verify the exact API in the installed library. Respect `ExperimentalMaterial3ExpressiveApi` and release-channel boundaries.
- If the existing project is on stable Material 3 and Expressive requires alpha APIs, present the dependency/API tradeoff before changing the release channel.

## Implementation Workflow

1. Inspect the rendered path, theme, shared components, dependencies, and target screen sizes.
2. Write a compact UI contract: content priority, navigation, primary action, components, states, and adaptive transformations.
3. Select the official component or the smallest accessible custom composition when no suitable component exists.
4. Implement theme roles and layout structure before polish.
5. Add interaction behavior, semantics, system insets, focus order, and state restoration.
6. Apply expression selectively and remove any outline, shadow, container, or animation that does not communicate something.
7. Verify at relevant window sizes and with realistic content, not only an ideal preview.

When modifying an existing screen, make the narrowest responsible change. Do not replace the app's design language wholesale unless requested.

## Required Verification

For a visible UI change, compilation alone is not visual proof.

- Run the smallest relevant compile, lint, or framework check.
- Inspect the exact requested target and viewport. For phone/tablet layouts, include a compact phone and every other affected window class; for Wear, widgets, and web, use their target-specific configurations instead.
- Check long localized text, large font scale, dark theme, dynamic/custom color, loading, empty, and error content as applicable.
- On applicable Android phone/tablet screens, check edge-to-edge insets, IME overlap, gesture regions, rotation/resizing, and state continuity.
- On web, check keyboard navigation, visible focus, hover, reduced motion, zoom, and narrow/wide layouts.
- Confirm 48dp Android touch targets and platform-appropriate web hit targets.
- Confirm contrast and meaning without relying on color alone.
- Confirm containers do not duplicate a boundary or exceed the `1:3` containment budget or two-level authored nesting limit.
- Confirm meaningful borders and state or focus indicators remain distinguishable in every supported theme and state; a decorative stroke must not carry required meaning.
- Confirm there are no clipped labels, overlapping controls, accidental nested scrolling regions, or layout jumps.

Use screenshots or previews for visual comparison when the environment supports them. State clearly which device/browser scenarios were actually observed.

## Review Output

When reviewing or handing off work, report:

- the chosen Material libraries and whether any API is experimental;
- the hierarchy and adaptive behavior implemented;
- accessibility and system-UI behavior covered;
- checks that actually ran and screen sizes actually inspected;
- remaining device, browser, migration, or dependency risks.

Do not claim Material 3 Expressive, adaptive, accessible, or visually verified behavior from naming, dependency presence, or compilation alone.
