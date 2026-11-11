---
name: android-ui-foundations
description: Apply Android accessibility, system-bar, terminology, and platform-translation guidance when designing or reviewing mobile UI. Use for inclusive interaction, system UI integration, or adapting an iOS design to Android.
license: Apache-2.0
---
# Android foundations

Preserve the user's task and the product's identity while making the experience work with Android conventions and accessibility services.

## Select the reference

- Accessibility, contrast, touch targets, semantics, and alternate input: [accessibility](references/accessibility.md).
- Status/navigation/caption bars and platform terminology: [system UI and glossary](references/system-ui-and-glossary.md).
- Translating an iOS or shared design system: [platform translation](references/platform-translation.md).

## Apply foundations in context

Inspect the actual screen, user journey, and UI stack. Keep system controls distinct from app controls. Respect system text, theme, motion, and input preferences. Use familiar native semantics without forcing every product into identical styling.

For accessibility, check the affected flow end-to-end: labels, state, focus order, errors, recovery, alternate actions, text scaling, contrast, and touch geometry. An accessible individual button does not prove an accessible journey.

For platform translation, map behavior before replacing visual assets. Review destination hierarchy and distinguish Back, Up, and modal dismissal. Preserve the product's existing brand and content priority.

## Validation and handoff

Provide actionable findings with the affected element or step, user impact, and proposed correction. Measure contrast and geometry where possible. Label source inspection separately from observed TalkBack, keyboard, Voice Access, or Switch Access behavior. Do not call a screen accessible solely because it uses Material components.

For overlap and adaptive layout decisions use [layout](../android-ui-layout-content/SKILL.md); for history and predictive gestures use [patterns](../android-ui-patterns/SKILL.md).

Source baseline: [Android accessibility](https://developer.android.com/design/ui/mobile/guides/foundations/accessibility), reviewed 2026-10-04.
