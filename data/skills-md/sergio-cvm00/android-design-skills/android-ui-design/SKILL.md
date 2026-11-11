---
name: android-ui-design
description: Plan or review Android phone, tablet, and foldable UI across layout, interaction patterns, visual style, components, accessibility, and system surfaces. Use for cross-cutting design work; use a specialist directly for a focused task.
license: Apache-2.0
---
# Android UI design

Turn a user journey into an Android-appropriate design and a verifiable handoff. These are design skills, not permission to rewrite an app, change authentication, install tools, publish, or alter device settings.

## Establish the design context

Inspect the existing product and design system first. Identify the user's task, primary content, navigation hierarchy, current UI stack (Compose, Views, hybrid, or design-only), supported window configurations, and relevant platform/library versions. Preserve product identity. Ask only for information that changes the solution; label reasonable assumptions.

For a new screen, begin with its content and state model, then layout and navigation, then components and style. For an audit, begin with observed behavior and affected surfaces.

## Route only the relevant work

Sibling skill paths are relative to this file. The complete bundle keeps them available; if a specialist is missing, use the linked official source and report the limitation.

| Need | Read |
| --- | --- |
| Screen structure, responsive behavior, panes, keyboard, edge-to-edge, assets | [android-ui-layout-content](../android-ui-layout-content/SKILL.md) |
| Navigation journeys, Back, onboarding, passkeys, settings, help | [android-ui-patterns](../android-ui-patterns/SKILL.md) |
| Accessibility, system bars, platform translation | [android-ui-foundations](../android-ui-foundations/SKILL.md) |
| Color, theme, type, shape, icons and motion direction | [android-ui-styles](../android-ui-styles/SKILL.md) |
| Choosing component families, states and alternatives | [android-ui-components](../android-ui-components/SKILL.md) |
| Notifications, live updates and picture-in-picture | [android-ui-home-screen](../android-ui-home-screen/SKILL.md) |
| Launcher widget layouts, sizing, configuration and discovery | [android-ui-widgets](../android-ui-widgets/SKILL.md) |

For a normal screen, read layout and patterns only when both apply. Accessibility remains a cross-cutting check, not a reason to load every reference.

## Produce a useful handoff

Adapt the output to the request. For substantive design work, identify:
- The chosen composition and interaction model, with the reason it fits the task.
- Window/pane changes, navigation destinations, Back/Up/dismiss behavior, and state that survives changes.
- Loading, empty, error, unavailable, and recovery states relevant to the flow.
- Accessibility, system UI and input constraints.
- Observed validation, unresolved assumptions, and what requires runtime evidence.

Prefer platform or Material behavior when suitable; customize deliberately. Do not impose a full design system on a small app.

## Source and evidence discipline

This bundle is a practical synthesis of [Android mobile design guidance](https://developer.android.com/design/ui/mobile), reviewed 2026-10-04. References distinguish source recommendations from authored heuristics and examples. Reopen linked implementation documentation before prescribing version-sensitive APIs or SDK behavior. Respect project dependencies; do not automatically upgrade them.

A source link is not proof that an app follows it. A mockup is not proof of TalkBack, predictive Back, keyboard, credential-provider or widget-host behavior. Report each check as observed, proposed, unavailable, or not applicable with a reason. Stay within the user's requested change scope.
