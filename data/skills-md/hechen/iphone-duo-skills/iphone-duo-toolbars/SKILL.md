---
name: iphone-duo-toolbars
description: Adapt SwiftUI and UIKit navigation bars, toolbars, tab bars, sheets, custom controls, and overflow menus for the vertical bar on iPhone Duo without losing essential actions or labels. Use when bars do not move to the side, items disappear or overflow, text-only or custom-view items stay horizontal, a screen should keep horizontal bars, or you need axisBehavior, visibilityPriority, toolbarVerticalEdge or verticalBarEdge, toolbarVerticalBehavior or preferredVerticalBarBehavior, or vertical bar compression.
license: MIT
---

# iPhone Duo toolbars

Read [toolbar evidence](references/toolbars.md). The axis, edge, compression, and opt-out APIs need the iOS 27.1 SDK. Preserve the current deployment target and keep a working horizontal-bar path.

## Inventory actions by meaning

For each screen, list navigation, completion and cancellation, frequent actions, status-bearing items, and infrequent actions. Trace each to the owning navigation container. Only bars owned by a navigation stack, split view, tab view, or navigation controller move to the vertical axis; find hand-built `UIToolbar`, `UINavigationBar`, and `UITabBar` instances and wide custom views before changing placements.

Decide which information is necessary to understand an action. Give each item both a title and a symbol: the vertical bar shows symbols, overflow shows both, and text-only or custom-view items stay horizontal. A changing price or meaningful status may need visible text and can stay horizontal on purpose. Keep the action's enabled state, shortcut, confirmation behavior, and target consistent between the bar and overflow.

## Adapt and prioritize

Use the system behavior first, then tune only demonstrated problems. Put Back or Close at the top, then prominent actions such as Done, using the semantic placements. Keep related items in groups instead of spacing them by hand. Do not mark every item high priority: identify the action the user must keep under space pressure, and choose whether the toolbar or the tab bar compresses first.

For a custom control, define a usable compact representation or leave it in a suitable horizontal location. Read the vertical bar edge instead of assuming the right side. Avoid shrinking text or touch targets merely to fit. Opt out of the vertical bar only for a screen better served by horizontal bars, such as a full-screen player or a non-scrolling calculator-style layout, and keep that choice stable instead of toggling it with view state.

## Verify

Open the keyboard and overflow menu; enter selection or editing mode; present and dismiss a sheet on each display; navigate back; try Split View on both sides. Check that Save, Done, Close, or the equivalent task exit remains discoverable. Repeat with long localized titles, large text, and right-to-left content.

Return the action inventory, placement decisions, source and SDK evidence, and screenshots or interaction results for the constrained states. Report any unresolved overflow or accessibility issue explicitly.
