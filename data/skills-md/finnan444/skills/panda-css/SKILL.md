---
name: panda-css
description: Build styles with Panda CSS. Use when creating, editing, or reviewing any code that uses Panda CSS — css(), cva(), sva(), recipes, patterns, tokens, semantic tokens, config, theming, or JSX styled components. Supports React, Vue, Svelte, Solid, and any framework with PostCSS.
---

# Panda CSS

Reference Panda CSS LLM-optimized docs before writing or reviewing Panda CSS code.

## Docs Sources

First fetch `https://panda-css.com/llms.txt` — this is the index of all available LLM docs.

Then fetch the relevant section-specific docs based on the task:

| Section | URL | When to use |
|---------|-----|-------------|
| Full docs | `https://panda-css.com/llms-full.txt` | General reference, broad tasks |
| Overview | `https://panda-css.com/llms.txt/overview` | Setup, installation, framework integrations |
| Concepts | `https://panda-css.com/llms.txt/concepts` | css(), recipes (cva/sva), patterns, conditions, cascade layers, style merging, JSX style context |
| Theming | `https://panda-css.com/llms.txt/theming` | Tokens, semantic tokens, text styles, layer styles, animation styles |
| Utilities | `https://panda-css.com/llms.txt/utilities` | Style properties, shorthands, spacing, sizing, typography, effects, gradients, focus ring |
| Customization | `https://panda-css.com/llms.txt/customization` | Custom conditions, utilities, patterns, presets, config functions, theme overrides |
| Guides | `https://panda-css.com/llms.txt/guides` | Migration, dynamic styling, debugging, advanced patterns |
| References | `https://panda-css.com/llms.txt/references` | CLI commands, panda.config.ts options, full config reference |

Use WebFetch to retrieve the correct reference **before starting any task**.
If the index lists different section URLs, follow the index and ignore the table above.

## Usage

1. Fetch `llms.txt` index to check for any new/updated doc URLs.
2. Confirm Panda CSS is installed by checking for `@pandacss/dev` in `package.json`/lockfiles. If missing, pause and alert the user before proceeding.
3. Note the installed Panda version (v0 vs v1+). If docs don’t match the installed major version, flag it before continuing.
4. In monorepos or multiple apps, inspect the relevant package path or ask the user which app to target.
5. Check for `panda.config.ts` (or `.js`/`.mjs`) to understand tokens, recipes, patterns, and framework config. If absent, ask whether to scaffold a minimal config.
6. Fetch the matching section-specific docs for the task at hand (reuse a cached copy during the session unless `llms.txt` changed).
7. Read the relevant sections for the features needed.
8. Write or review code following the documented patterns.
