---
name: tailwindcss
description: Tailwind CSS v4 setup, theme variables, content sources, custom styles, and Vite/PostCSS/CLI integration. Use when styling with utility classes, configuring theme or content, or integrating Tailwind in a build pipeline.
metadata:
  author: Anthony Fu
  version: "2026.2.6"
  source: Generated from https://github.com/tailwindlabs/tailwindcss and https://tailwindcss.com/docs, scripts at https://github.com/antfu/skills
---

# Tailwind CSS

> Skill is based on Tailwind CSS v4.1, generated at 2026-02-06.

Tailwind CSS is a utility-first CSS framework. v4 is configured in CSS via `@theme` and `@source` (no `tailwind.config.js`). Supports Vite, PostCSS, and CLI.

## Core References

| Topic | Description | Reference |
|-------|-------------|-----------|
| Installation | Vite, PostCSS, and CLI setup; CSS entry | [core-installation](references/core-installation.md) |
| Theme | @theme, design tokens, namespaces, extending/overriding | [core-theme](references/core-theme.md) |
| Content & sources | Class detection, @source, base path, safelist | [core-content-sources](references/core-content-sources.md) |
| CLI | Build command, --input, --output, --watch, --minify | [core-cli](references/core-cli.md) |

## Features

| Topic | Description | Reference |
|-------|-------------|-----------|
| Custom styles | Arbitrary values, @layer, @utility, @custom-variant | [features-custom-styles](references/features-custom-styles.md) |

## Integrations

| Topic | Description | Reference |
|-------|-------------|-----------|
| Vite plugin | @tailwindcss/vite options (optimize, minify) | [integrations-vite](references/integrations-vite.md) |
| PostCSS plugin | @tailwindcss/postcss options (base, optimize, transformAssetUrls) | [integrations-postcss](references/integrations-postcss.md) |

## Quick reference

**CSS entry (all setups):**
```css
@import "tailwindcss";
```

**Theme and sources in CSS:**
```css
@theme { --color-mint-500: oklch(0.72 0.11 178); }
@source "../node_modules/@acme/ui";
```

**Vite:** `plugins: [tailwindcss()]` · **PostCSS:** `plugins: { '@tailwindcss/postcss': {} }` · **CLI:** `npx @tailwindcss/cli -i input.css -o output.css --watch`
