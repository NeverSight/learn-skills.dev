---
name: tailwind
description: 'Tailwind CSS v4 patterns and design systems. Use when configuring Tailwind themes, building components, implementing dark mode, using container queries, migrating from v3, integrating shadcn/ui, or fixing build errors. Use for tailwind, css, styling, theme, design-tokens.'
license: MIT
metadata:
  author: oakoss
  version: '1.0'
  source: 'https://tailwindcss.com/docs'
---

# Tailwind CSS (v4+)

## Overview

Tailwind CSS v4 skill covering CSS-first configuration, design tokens, component patterns, shadcn/ui integration, dark mode, container queries, migration from v3, and custom utilities.

**When to use:** Configuring Tailwind themes, building utility-first components, implementing dark mode, using container queries, migrating from v3, integrating shadcn/ui, troubleshooting build errors.

**When NOT to use:** Tailwind v3 legacy projects that will not upgrade, projects using a different styling approach (CSS Modules, styled-components) without plans to adopt Tailwind.

## Quick Reference

| Pattern              | API                                                   | Key Points                                       |
| -------------------- | ----------------------------------------------------- | ------------------------------------------------ |
| CSS-first config     | `@theme { --color-brand: oklch(...); }`               | All config in CSS, no `tailwind.config.js`       |
| Import entry         | `@import "tailwindcss";`                              | Replaces `@tailwind base/components/utilities`   |
| Custom utilities     | `@utility name { ... }`                               | Replaces `@layer utilities`, works with variants |
| Functional utilities | `@utility tab-* { tab-size: --value(--tab-size-*); }` | Accept dynamic values via `--value()`            |
| Plugin loading       | `@plugin "@tailwindcss/typography";`                  | Replaces `require()` in config                   |
| Container queries    | `@container` parent + `@md:` child                    | Built-in, no plugin needed                       |
| Named containers     | `@container/sidebar` + `@md/sidebar:`                 | Scope queries to specific containers             |
| Dark mode variant    | `@custom-variant dark (&:where(.dark, .dark *));`     | Class-based dark mode override                   |
| Theme inline         | `@theme inline { --color-bg: var(--bg); }`            | Inlines values at build, single-theme only       |
| Source detection     | `@source "../node_modules/my-lib";`                   | Explicitly add scan paths                        |
| Reference import     | `@reference "../../app.css";`                         | Use theme in Vue/Svelte scoped styles            |
| Override defaults    | `--color-*: initial;` inside `@theme`                 | Reset a category before redefining               |
| Dynamic values       | `grid-cols-(--my-var)`                                | Use CSS variables in utility values              |
| Text shadows         | `text-shadow-*`                                       | Built-in text shadow utilities                   |
| Starting styles      | `starting:opacity-0`                                  | `@starting-style` variant for entry animations   |
| Masks                | `mask-*`                                              | CSS mask utilities for image/gradient masking    |
| Field sizing         | `field-sizing-content`                                | Auto-sizing textareas and inputs                 |
| Inset shadows        | `inset-shadow-*`, `inset-ring-*`                      | Inner shadow and ring utilities                  |
| User validation      | `user-valid:`, `user-invalid:`                        | Form validation after user interaction           |
| Pointer queries      | `pointer-fine:`, `pointer-coarse:`                    | Target input device precision                    |
| Inert                | `inert:opacity-50`                                    | Style inert elements                             |
| Logical spacing      | `pbs-*`, `pbe-*`, `mbs-*`, `mbe-*`                    | Block-direction padding/margin (v4.2)            |
| Logical sizing       | `inline-*`, `block-*`, `min-inline-*`, `max-block-*`  | Logical width/height utilities (v4.2)            |
| Logical inset        | `inset-s-*`, `inset-e-*`, `inset-bs-*`, `inset-be-*`  | Logical positioning; replaces `start-*`/`end-*`  |
| Logical borders      | `border-bs-*`, `border-be-*`                          | Block-direction border utilities (v4.2)          |
| Font features        | `font-features-['smcp']`                              | OpenType `font-feature-settings` (v4.2)          |
| New color palettes   | `mauve`, `olive`, `mist`, `taupe`                     | Additional neutral palettes (v4.2)               |
| Webpack integration  | `@tailwindcss/webpack`                                | Run Tailwind as a webpack plugin (v4.2)          |
| Color space          | OKLCH                                                 | Default in v4, sRGB fallbacks generated          |

## Common Mistakes

| Mistake                                   | Correct Pattern                                  |
| ----------------------------------------- | ------------------------------------------------ |
| Using `tailwind.config.js` in v4          | Configure via `@theme { ... }` in CSS            |
| `hsl(var(--background))` double-wrap      | Reference directly: `var(--background)`          |
| `:root`/`.dark` inside `@layer base`      | Define at root level, outside any `@layer`       |
| `@apply` with `@layer components` classes | Use `@utility` directive for custom utilities    |
| `@theme inline` for multi-theme switching | Use `@theme` without `inline` for dynamic themes |
| Raw colors like `bg-blue-500` everywhere  | Semantic tokens (`bg-primary`) that auto-adapt   |
| `require()` or `@import` for plugins      | Use `@plugin "package-name";`                    |
| `tailwindcss-animate` in v4               | Use `tw-animate-css` instead                     |
| Missing `@theme inline` with shadcn/ui    | Map all CSS variables in `@theme inline` block   |
| Using `theme('colors.brand')` in CSS      | Use `var(--color-brand)` native CSS variables    |
| Using deprecated `start-*`/`end-*` inset  | Use `inset-s-*`/`inset-e-*` logical utilities    |

## Delegation

- **Class pattern discovery and usage examples**: Use `Explore` agent
- **v3 to v4 migration across multiple files**: Use `Task` agent
- **Design token hierarchy and theming architecture**: Use `Plan` agent

> If the `motion` skill is available, delegate complex animation patterns (spring physics, gestures, scroll-linked) to it.

## References

- [Configuration](references/configuration.md) -- CSS-first config, @theme, @theme inline, @utility, @plugin, @source, @reference, @variant directives
- [Design Tokens](references/design-tokens.md) -- OKLCH token system, brand scales, semantic tokens, shadows, z-index, fluid typography
- [Component Patterns](references/component-patterns.md) -- Layouts, grids, container queries, 3D transforms, subgrid, CVA variants
- [UI Patterns](references/ui-patterns.md) -- Buttons, forms, navigation, cards, typography with variants, states, accessibility
- [Dark Mode](references/dark-mode.md) -- Class-based dark mode, multi-theme systems, ThemeProvider, @custom-variant
- [shadcn/ui Integration](references/shadcn-integration.md) -- Four-step architecture, components.json, tw-animate-css, Vite setup
- [Migration](references/migration.md) -- v3 to v4 migration steps, breaking changes, upgrade tool, common gotchas
- [Troubleshooting](references/troubleshooting.md) -- Common errors, build fixes, CSS layer issues, PostCSS problems
