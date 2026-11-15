---
name: android-design-explore
description: >
  Explore Android app ideas as live Compose proposals in the previewer app before implementation, without
  changing app code. Use to brainstorm phone, tablet, desktop, or Wear OS app screens, mock up redesign
  alternatives, or compare and iterate on visual directions in chat. Not for Wear tiles, watch faces, or widgets.
  Builds on the android-design skill, which owns every design decision.
---

# Visual design exploration

Follow the `android-design` skill for every design decision: its design questions, components, theming, layout, and the screen check's questions. This skill owns the workflow. Each run is one shot: brief in, one proposal written, checked, shown, then stop. Phone, foldable, tablet, desktop, and Wear OS app screens are in scope; Wear tiles, watch faces, and widgets are not. Where Wear differs, the **Wear OS** section below says how.

A proposal is a data file that the previewer app, a native macOS window, draws with real Compose Material 3 components and redraws on every save. You check it through the app's layout tree; the user judges taste in the window.

## Requirements

macOS, with the previewer app installed and registered as an MCP server named `android_design_preview`. Call its `status` tool first. When its tools are unavailable, stop, give the user the setup steps in [references/setup.md](references/setup.md), and wait.

## Brief

When there is an app, read its relevant screens, theme, assets, and any existing `DESIGN.md` and `design/` proposals first. Answer `android-design`'s design questions in the reply.

- Pick one seed: the brand color, or a content color from the subject (a dish, an album, a trip), never the app's default `#6750A4`.
- When the screen is a hero moment (the hero question in `android-design`'s design questions), layer three or more tactics (its Hero moments section) and name them.
- Keep app code and dependencies unchanged.
- Use representative, non-sensitive data and assets. Use image generation only for assets inside a proposal, never as a substitute for one.

Make several proposals only when the user asks. Each is its own file, a distinct composition (not a recoloring) with its own seed in its `theme`, and at least one is a hero.

## Files

Work in the app's repository root, or the folder the user names. Never write into this skill's own repository.

- `DESIGN.md` at the root holds the shared design system. Create it when missing, with the chosen seed, faces, and named styles. Change it only when the direction changes what every proposal shares; a direction's own look goes in its proposal's `theme`.
- `design/<slug>.proposal.json` holds one proposal.

Both are ordinary tracked files; committing them follows the project's own workflow. Tell the user the proposal's absolute path.

## Write

1. Call `get_catalog` (its tool description says what it returns). It is the only component vocabulary: a component it lacks is out of reach, so build the idea from `Box`, `Row`, `Column`, `Text`, and `Shape`, or leave it out.
2. Read `references/proposal-format.md`, then write `DESIGN.md` and the proposal, compactly as its "Writing it compactly" section says.

The proposal carries these design rules; `proposal-format.md` gives the syntax for each, and its [Component rules](references/proposal-format.md#component-rules) section holds the rules for tabs, carousels, overlays, choices, toolbars, menus, app bars, and badges:

- The screen has one primary action, marked as primary, and it leads its peers as `android-design`'s Emphasis and hierarchy section describes.
- It adapts at 600 and 840 dp: `navigation.destinations` draws a bar at compact and a rail from medium up, and a list's detail screen opens beside the list at expanded widths.
- Text truncates on purpose, with an ellipsis. Button, chip, and navigation labels fit on one line.

## Check

For a proposal, this step replaces the rendering in `android-design`'s screen check. Answer its questions from the `check_proposal` layout summaries and errors (and `get_tree` when they are not enough), not from pixels. The one exception is step 6: two renders per screen once the checks pass. `render_view` is the only way to see the UI: never capture the screen, control the window, or ask the user for a screenshot.

1. Call `open_proposal` with the proposal's absolute path. It loads the file, watches it, shows the window, and returns validation errors. Fix them and call `status`, which reports validation errors only, never render findings: an empty `errors` with the proposal open means the file is valid.
2. Call `check_proposal`. One call checks every screen at every view and returns each view's errors and `layout` summary; its tool description gives the format. A view equal to an earlier one is `{"same": "<view>"}`: read the earlier one. `notes` are info findings that never fail a view; read them. `colors` gives each role's hex for light and dark: judge fills from it (`android-design`'s one-strong-fill cap, under Color), not from role names.
3. Fix every error once, then call `check_proposal` again. An `overflow` error names a node laid out wider than its parent or the view (a row that needs more width than its cell); narrow it, wrap it, or let it scroll. A `corner-clipped` error names a text or control that reaches into the rounded corner of a `Card` or a styled container, which cuts it off; give the container `padding`. Report anything still failing instead of looping.
4. Confirm the adaptation from the `layout` summaries: each larger view reveals what your adaptation answer promised, such as a second pane, a rail, or more regions. A larger view with the phone's regions only spread wider fails.
5. Call `get_tree` only when a summary or an error is not enough; its tool description says what it returns.
6. Once `check_proposal` passes or its remaining errors are on your report list, call `render_view` twice for each screen: once at `light` and once at `desktop` (`watch` and `watch-large` for Wear). Look for what the tree cannot show: an icon that does not fit its meaning, an asset that reads poorly, a screen that looks crowded or empty. Fix what you find, confirm the fix with `check_proposal`, and do not render again. When the picture disagrees with the tree (a padding, color, or bound the tree reports that the picture does not show), do not change the proposal to match the picture: report it as a possible previewer bug.

The step is done when `check_proposal` passes or each remaining error is on the list you report, the adaptation is confirmed, and each screen was rendered at both views.

## Show

Call `show_preview`: `open_proposal` already showed the window, so this brings it back and to the front if the user closed it since. Say in one line what the proposal is, name the tactics a hero layers, list any unresolved findings, what the proposal could not express ([Limits](references/proposal-format.md#limits)), and report "visual quality judged from the layout tree, confirmed with two renders per screen". Then stop and wait for the user's reply.

## Revise

Edit the same proposal with the user's feedback; the window redraws on save. Repeat the check on the screens you changed. The revision replaces the old version; keep no copies.

## Approve and port

Approval is the user saying so in chat. Report the approved proposal's path and that `references/compose-mapping.md` is the porting table. An explore-only request ends there: do not implement. A build request (the `android-design` skill sends design-focused builds of new apps, screens, and redesigns here first) continues to the port. Approval never authorizes library version changes.

The port follows the requesting project's planning, branch, verification, and review rules:

1. Call `export_kotlin` for the screens to port. Its Kotlin is the first draft, not finished code.
2. Fit it to the app's conventions and library versions with `references/compose-mapping.md`.
3. Render the result with the `compose-preview` skill and compare it with the proposal's trees at the same views.

Report components the mapping marks unverified, and anything it lacks, instead of inventing a Compose equivalent. If the design cannot be preserved with the app's dependencies, ask.

## Wear OS

A Wear proposal follows the same workflow. `android-design` `references/wear-os.md` owns the design rules, and [proposal-format.md](references/proposal-format.md#wear-os) owns the file format (catalog id, views, `Screen`, `primary`, `large`).

- **Its own file.** One surface per proposal: write `design/<slug>-wear.proposal.json` beside the phone one.
- **Adaptation check:** the Wear size override applies from 225dp, so the check is "fits and reads at both watch sizes, and the large one shows more value, never less".
- **Shared `DESIGN.md`:** its seed and color roles apply to Wear; its typography is replaced by Roboto Flex.
- **Findings:** fix `round-edge-clipped` (control or text cut by the round edge on a fixed screen) with percentage-style margins or a smaller layout.
- **Port:** the same three steps. `export_kotlin` writes Wear Compose: a `WearAppTheme` with the previewer's exact colors, `AppScaffold` and `ScreenScaffold`, and Navigation 3 with swipe to dismiss. Render the port at both round sizes (204 and 227dp).

## Delete

When the user asks, remove `design/<slug>.proposal.json`. Keep `DESIGN.md` unless the user asks to remove it too.
