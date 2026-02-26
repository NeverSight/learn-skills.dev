---
name: nativewind
description: Use Tailwind CSS to style React Native components across web and native
metadata:
  author: Hairy
  version: "2026-02-26"
  source: Generated from https://github.com/nativewind/website, scripts located at https://github.com/hairyf/skills
---

> Skill is based on NativeWind v5 (Tailwind CSS v4), generated at 2026-02-26.

NativeWind compiles Tailwind CSS for React Native: `className` on components, StyleSheet.create on native and reuse of the Tailwind stylesheet on web. It supports media/container queries, pseudo-classes (hover, focus, active), platform variants (ios:, android:, native:, web:), dark mode, and custom theme/utilities via CSS-first config.

## Core References

| Topic | Description | Reference |
|-------|-------------|-----------|
| Setup | CSS file, Metro withNativewind, PostCSS, app entry, optional lightningcss pin | [core-setup](references/core-setup.md) |
| Configuration | CSS-first config, @theme, @source, nativewind/theme, custom utilities/variants | [core-config](references/core-config.md) |
| v5 Tailwind foundation | Built on Tailwind v4, CSS-first, web vs native support | [core-v5-tailwind-foundation](references/core-v5-tailwind-foundation.md) |
| v5 Units | px, %, vw/vh, rem, em on native; dp vs px; rem sizing | [core-v5-units](references/core-v5-units.md) |
| v5 Functions & directives | @import, @theme, @utility; var(), calc(), env(), color-mix(); RN functions | [core-v5-functions-directives](references/core-v5-functions-directives.md) |
| v5 Style specificity | Order of precedence, !important, merging className and style | [core-v5-style-specificity](references/core-v5-style-specificity.md) |

## Features

| Topic | Description | Reference |
|-------|-------------|-----------|
| Styling components | className usage, custom vs third-party, styled() / cssInterop / remapProps, nativeStyleToProp | [features-styling](references/features-styling.md) |
| Platform & responsive | Platform variants, units, breakpoints, safe-area utilities | [features-platform](references/features-platform.md) |
| v5 Responsive | Breakpoints on native, media queries, platform media, reactive updates | [features-v5-responsive](references/features-v5-responsive.md) |
| States & dark mode | hover/focus/active, disabled/empty, group modifiers, dark:, data attributes | [features-states](references/features-states.md) |
| v5 States & pseudo-classes | Detailed pseudo-class table, selection/placeholder, group, ltr/rtl | [features-v5-states-pseudo](references/features-v5-states-pseudo.md) |
| v5 Third-party guide | When className isn't passed, multiple style props, dynamic mapping @prop | [features-v5-third-party-guide](references/features-v5-third-party-guide.md) |
| Theming & colors | @theme tokens, vars() for runtime CSS variables, color behavior | [advanced-theme](references/advanced-theme.md) |

## API (v5)

| Topic | Description | Reference |
|-------|-------------|-----------|
| withNativewind | Metro wrapper options (globalClassNamePolyfill, typescriptEnvPath) | [api-with-nativewind](references/api-with-nativewind.md) |
| styled | Third-party components, nativeStyleToProp, multiple className props | [api-styled](references/api-styled.md) |
| vars & runtime variables | vars(), VariableContextProvider, useUnstableNativeVariable | [api-vars-runtime](references/api-vars-runtime.md) |
| cssInterop / remapProps | Legacy API (deprecated; use styled) — migration reference | [api-css-interop-remap](references/api-css-interop-remap.md) |

## Advanced

| Topic | Description | Reference |
|-------|-------------|-----------|
| Migrate v4 → v5 | Steps, breaking changes, deprecations | [advanced-migrate-v4](references/advanced-migrate-v4.md) |

## Best Practices

| Topic | Description | Reference |
|-------|-------------|-----------|
| Correctness & debugging | Explicit light/dark, colors on Text not View, cache, DEBUG, verifyInstallation | [best-practices-performance](references/best-practices-performance.md) |
| v5 Deprecations | useColorScheme → RN, cssInterop/remapProps → styled, @prop modifier | [best-practices-v5-deprecations](references/best-practices-v5-deprecations.md) |
