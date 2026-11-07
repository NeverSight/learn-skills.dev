---
name: iphone-duo-layout
description: Implement or review fold-aware SwiftUI and UIKit content layouts for iPhone Duo using reserved regions (fold divisions and camera occlusions), ArrangementView or UIArrangementViewController split and overlay arrangements, size classes, and asymmetric safe areas. Use when content or controls collide with the fold or the inner camera, a two-pane or media layout must adapt as the device folds, opens, closes, or rotates, or navigation, selection, and scroll state are lost during those changes.
license: MIT
---

# iPhone Duo layout

Read [layout evidence](references/layout.md) before choosing a Duo-specific container. The arrangement and reserved-region APIs need the iOS 27.1 SDK. With an older SDK, improve the existing resizing behavior and document the deferred adoption; do not insert unresolvable symbols behind runtime availability checks.

## Choose the right boundary

Identify whether the problem belongs to navigation, the relationship between two content panes, or an individual custom control. Keep navigation responsible for routes and selection, outside any arrangement. Keep the content container responsible for pane presentation. A layout change should not restart a network task or create a second document model.

Inventory persistent state before moving view boundaries. Keep models at a stable owner, preserve item IDs, and avoid assigning identity from transient geometry. For imperative layout, recompute from the current view's bounds and insets; verify coordinate conversions when an overlay lives elsewhere in the hierarchy.

## Adapt only what needs adaptation

Start with the system container that fits the content; alerts, menus, sheets, and split views already move around the fold. Use an arrangement only when the layout already resembles one: side by side or stacked maps to split, layered maps to overlay. For a custom layout, query reserved regions instead of recreating a fold from guessed angles, midpoints, or physical dimensions.

- Filter regions on `isActive` for current avoidance. Use `.includeInactive` only to plan, for example to prefer an even number of grid columns.
- Region frames already include their margins. Keep all geometry in one coordinate space, and check right-to-left layout.
- Move only what must move to stay visible and easy to tap. Scrolling content can cross the fold; critical touch targets should not sit in it.

Make the narrow fallback explicit: when one pane is hidden, provide a way to reach it and preserve its state. Test at intermediate sizes, with a keyboard, and with large text. Avoid a feedback loop where measuring a child changes its parent size indefinitely.

## Verify the user's task

Exercise a realistic transition while editing, playing media, or navigating. Check selection, focus, scroll continuity, and operation count alongside visual placement. Test existing non-Duo targets too.

Report the chosen container, state owner, fallback behavior, actual SDK and build result, and runtime evidence. Keep documentation-only guidance distinct from code compiled and exercised in the user's project.
