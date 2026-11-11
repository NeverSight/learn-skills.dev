---
name: android-ui-layout-content
description: Design, implement, or audit Android screen layouts and content for phones, tablets, foldables, and resizable windows. Use for pane composition, adaptive navigation placement, grids, insets, keyboard overlap, orientation, immersive content, and image behavior.
license: Apache-2.0
---
# Android layout and content

Design around the task and available window, not a fixed phone screenshot. Prioritize continuity, readable content, and reachable actions.

## Work from content to adaptation

1. Identify the primary task, content hierarchy, main action, supporting information, and persistent state. Inspect existing spacing tokens and screen structure.
2. Choose list-detail, feed, or supporting-pane composition when it fits. Record what each pane owns and what must remain visible.
3. Specify compact and expanded behavior, then resolve intermediate widths and short heights. Include resizing while a task is in progress.
4. Define constraints: margins, minimum usable pane width, content maximum width, scroll ownership, image crop, and pinned controls. Express dimensions in dp and type in sp.
5. Resolve system bars, cutouts, gesture regions, captions, hinges, and the on-screen keyboard separately from aesthetic spacing.
6. Validate the rendered configurations relevant to the change. Keep design-only conclusions separate from runtime results.

## Read by problem

- Starting a screen, grouping, units, or content hierarchy: [composition](references/composition.md).
- Choosing panes and changing navigation presentation: [adaptive layouts](references/adaptive-layouts.md).
- Keyboard obstruction, double padding, system bars, or immersive mode: [insets and immersion](references/insets-and-immersion.md).
- Rotation, small cover screens, hinges, or tabletop: [postures](references/postures.md).
- Image cropping, asset handoff, or visual effects: [images and graphics](references/images-and-graphics.md).
- Concrete design decisions and an acceptance matrix: [recipes and validation](references/recipes-and-validation.md).

## Essential constraints

- Use the current app window dimensions. Device labels such as "tablet" cannot determine layout alone.
- Width is a starting point; compact height, enlarged text, keyboard, and hinge occlusion may change a proposed multi-pane solution.
- Additional width should improve composition, not stretch every button, field, paragraph, or card.
- Keep backgrounds and scrolling content edge-to-edge while protecting actionable and essential content. Know which container consumes each inset.
- Preserve selected item, draft, filters, scroll, and playback where relevant when panes appear or disappear. Resizing is not a new user navigation action.
- Avoid portrait locks as a layout workaround. Keep short windows usable through reflow and intentional scrolling.
- Use 48 dp minimum touch targets and scalable text; do not shrink controls to force a screenshot to fit.

## Handoff

For each affected window configuration, describe visible panes, navigation component, content limits, scrolling/pinning, image behavior, and state continuity. Name concrete failure cases and show the rendered result if implementation is in scope.

For destination hierarchy and Back semantics, also read [patterns](../android-ui-patterns/SKILL.md). For detailed accessibility or system bar behavior, read [foundations](../android-ui-foundations/SKILL.md).

Source baseline: [Layout basics](https://developer.android.com/design/ui/mobile/guides/layout-and-content/layout-basics), reviewed 2026-10-04. References contain topic-specific sources. Check current APIs against installed libraries before coding.
