---
name: android-ui-styles
description: Design or audit Android color, themes, typography, shapes, icons, and visual motion direction. Use for Material-based or custom visual systems, dynamic color, dark mode, semantic tokens, and brand adaptation.
license: Apache-2.0
---
# Android styles

Start from the product's actual tokens, brand, and component library. Keep semantic meaning and readability stable across personalization.

## Read by task

- Color roles, dynamic color, contrast, and light/dark choices: [color and themes](references/color-and-themes.md).
- Type, shape, icon consistency, motion, and handoff: [type, shape, icons, and motion](references/type-shape-icons-motion.md).

## Apply style deliberately

Define roles before choosing literal values. Keep one coherent primary theme source; use content-derived colors selectively. Provide a custom fallback if dynamic color is unavailable. Respect system preferences and verify both light and dark variants.

Map existing tokens to component roles rather than scattering hard-coded overrides. A custom system is valid when it serves the product; document what differs from Material and verify accessibility.

Typography and shape should clarify hierarchy. Motion should explain transitions and feedback. Neither should be used to compensate for unclear structure or an inaccessible interaction.

## Deliver and verify

For a theme change, provide affected role mappings, variant behavior, and measured contrast for actual pairs and states. Inspect text scaling, selected/disabled/error states, imagery overlays, and system-bar contrast. Generated palettes or attractive screenshots alone do not prove accessibility.

Keep a small product's theme appropriately small. Do not create a full token framework merely to change one color. Use the project's installed APIs and consult current implementation documentation before generating code.

Sources: [Color](https://developer.android.com/design/ui/mobile/guides/styles/color) and [Themes](https://developer.android.com/design/ui/mobile/guides/styles/themes), reviewed 2026-10-04.
