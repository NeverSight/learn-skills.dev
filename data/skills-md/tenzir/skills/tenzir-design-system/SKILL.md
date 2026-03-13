---
name: tenzir-design-system
description: >-
  Tenzir frontend design system tokens, component specifications, and brand
  assets. Use when building or styling Tenzir UI, choosing colors or
  typography, implementing standard controls, or using official logos. Also use
  when implementing any web UI that should look like a Tenzir product, or when
  the user asks about Tenzir brand colors, fonts, or component patterns.
---

# Tenzir Design System

Use the shared Tenzir design system when implementing frontend UI.

## Start Here

1. Identify whether the task needs design tokens, a standard component, or a
   logo asset.
2. Load only the reference files needed for the current component or styling
   problem.
3. Prefer design tokens and existing component patterns over bespoke styling.

## Design Tokens

Load these references as needed:

- [typography](references/typography.md)
- [colors](references/colors.md)
- [spacing](references/spacing.md)
- [shadows](references/shadows.md)
- [border radius](references/border-radius.md)

Use the `--tnz-` CSS custom-property prefix for design-system tokens.

## Component References

Load the relevant reference before implementing the component:

- [buttons](references/buttons.md)
- [dropdown](references/dropdown.md)
- [hyperlinks](references/hyperlinks.md)
- [segmented control](references/segmented-control.md)
- [input field](references/input-field.md)
- [search input](references/search-input.md)
- [checkbox](references/checkbox.md)
- [radio button](references/radio-button.md)
- [toggle switch](references/toggle-switch.md)
- [tag](references/tag.md)
- [badge](references/badge.md)
- [tab bar](references/tab-bar.md)
- [toast](references/toast.md)

## Assets

Official logo files live in `assets/logos/`:

- `logo.svg`
- `logo-white.svg`
- `logomark.svg`
- `logomark-white.svg`

Use these assets for Tenzir products and integrations that should follow the
official brand system.
