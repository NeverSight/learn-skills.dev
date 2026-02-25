---
name: design-system
description: |
    Use when building or maintaining a design system — the coordinated set of design tokens, component libraries, documentation, and tooling that ensures visual and behavioral consistency across products.
    USE FOR: design system architecture, choosing token formats vs component frameworks, connecting Figma to code, design-to-development workflows, multi-platform consistency
    DO NOT USE FOR: specific token authoring (use design-tokens), Figma workflows (use figma), component cataloging (use storybook), token transformation (use style-dictionary), cross-framework components (use mitosis)
license: MIT
metadata:
  displayName: "Design System"
  author: "Tyler-R-Kendrick"
compatibility: claude, copilot, cursor
references:
  - title: "W3C Design Tokens Community Group"
    url: "https://www.w3.org/community/design-tokens/"
  - title: "Design Tokens Specification"
    url: "https://www.designtokens.org/"
---

# Design System

## Overview
A design system is the single source of truth for an organization's UI — combining design tokens, component libraries, documentation, and tooling into a cohesive ecosystem. It ensures consistency, accelerates development, and bridges the gap between design and engineering.

## Architecture Layers
```
┌─────────────────────────────────────────────────┐
│  Design (Figma)                                 │
│  Variables, components, styles, auto-layout     │
├─────────────────────────────────────────────────┤
│  Tokens (W3C DTCG / Style Dictionary)           │
│  Color, typography, spacing, elevation, motion  │
├─────────────────────────────────────────────────┤
│  Components (React, Vue, Angular, Web Comp.)    │
│  Buttons, inputs, modals, cards, layouts        │
├─────────────────────────────────────────────────┤
│  Documentation (Storybook)                      │
│  Stories, usage guidelines, interaction tests   │
└─────────────────────────────────────────────────┘
```

## Design-to-Code Pipeline
```
Figma Variables ──► W3C DTCG JSON ──► Style Dictionary ──► CSS / SCSS / iOS / Android
                                                            │
Figma Components ──► Code Connect / Mitosis ──────────────► React / Vue / Angular / Svelte
                                                            │
                                                            ▼
                                                        Storybook
                                                  (catalog + interaction tests)
```

## Token Architecture
Design tokens are the atomic values of a design system — colors, spacing, typography, elevation, motion. They flow through three tiers:

| Tier | Example | Purpose |
|------|---------|---------|
| **Global** | `blue-500: #3b82f6` | Raw palette values |
| **Alias / Semantic** | `color-primary: {blue-500}` | Intent-based references |
| **Component** | `button-bg: {color-primary}` | Scoped to a specific component |

## Component Strategy

### Single-Framework
Build components in one framework (e.g., React) and use Storybook for documentation and testing.

### Multi-Framework
Use an intermediary format to target multiple frameworks from a single source:
- **Mitosis** — JSX subset that compiles to React, Vue, Angular, Svelte, Solid, etc.
- **Web Components** — Framework-agnostic custom elements usable everywhere
- **Stencil** — Web Component compiler with lazy loading and SSR

## Key Tools
| Tool | Role |
|------|------|
| **Figma** | Visual design, variables, prototyping, Dev Mode |
| **W3C Design Tokens** | Vendor-neutral token format (DTCG spec) |
| **Style Dictionary** | Transform tokens into platform-specific outputs |
| **Storybook** | Component catalog, docs, visual/interaction testing |
| **Mitosis** | Write-once component compiler for multiple frameworks |
| **Tokens Studio** | Figma plugin for managing tokens in DTCG format |
| **Chromatic** | Visual regression testing for Storybook stories |

## File Structure
```
design-system/
  tokens/
    global/
      colors.tokens.json      # W3C DTCG format
      typography.tokens.json
      spacing.tokens.json
    semantic/
      theme-light.tokens.json
      theme-dark.tokens.json
  style-dictionary.config.mjs  # Token build pipeline
  src/
    components/
      Button/
        Button.tsx             # Component implementation
        Button.stories.tsx     # Storybook stories
        Button.test.tsx        # Unit / interaction tests
  .storybook/
    main.ts
    preview.ts
```

## Best Practices
- Define tokens in W3C DTCG format for vendor neutrality — avoid locking into a single tool's proprietary format.
- Use three-tier token architecture (global → semantic → component) so themes only override the semantic layer.
- Use Style Dictionary to transform tokens into every platform your products target (CSS, SCSS, iOS, Android, Compose).
- Catalog every component in Storybook with args, docs, and play-function interaction tests.
- Use Figma Variables synced to your token files — Tokens Studio or Code Connect bridges the gap.
- For multi-framework orgs, evaluate Mitosis or Web Components before duplicating component code per framework.
- Automate visual regression testing with Chromatic or Percy in CI.
- Version your design system as a package — consumers should pin to semver releases.
