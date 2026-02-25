---
name: design-system
description: 'Builds scalable design systems with tokens, theming, and component architecture. Use when creating design token hierarchies, theming systems, component variant patterns, or accessibility foundations. Use for design tokens, CVA variants, dark mode, multi-brand theming, Radix headless UI, Storybook documentation, and governance.'
license: MIT
metadata:
  author: oakoss
  version: '1.0'
  source: 'https://designtokens.org'
user-invocable: false
---

# Design System

## Overview

Single source of truth for visual consistency at scale — a shared language between design and engineering. Covers token architecture, theming infrastructure, component API patterns, accessibility compliance, and governance workflows.

Design systems are not component libraries alone. They unify tokens, patterns, documentation, and contribution processes so teams build once and maintain once.

## Quick Reference

| Area                | Pattern                                 | Key Points                                                           |
| ------------------- | --------------------------------------- | -------------------------------------------------------------------- |
| Token hierarchy     | Primitive > Semantic > Component        | Never reference primitives in components; semantic layer is themable |
| Dark mode           | Swap semantic tokens via `data-theme`   | Use off-white/dark-gray, not pure white/black                        |
| Multi-brand theming | Override semantic tokens per brand      | Apply via CSS custom properties at runtime                           |
| Tailwind v4         | `@theme` block in CSS (no config file)  | CSS-first configuration replaces `tailwind.config.js`                |
| CVA variants        | `cva()` for variant + size combinations | Type-safe with `VariantProps`; pair with `cn()` utility              |
| Compound components | `Modal.Header`, `Modal.Body` sub-parts  | Composition over configuration; shared context for implicit state    |
| Headless UI         | Radix primitives + Tailwind classes     | Accessibility built-in; bring your own styles                        |
| Focus management    | `focus-visible:ring-2` on all controls  | 2px solid outline with offset; visible on keyboard only              |
| Reduced motion      | `prefers-reduced-motion` media query    | Near-zero duration for all transitions and animations                |
| Style Dictionary    | JSON tokens to CSS/iOS/Android          | `outputReferences: true` preserves token chain                       |
| Storybook           | Stories + autodocs + a11y addon         | Visual documentation with accessibility audit built in               |
| Governance          | Semver for tokens and components        | Breaking = removed props/tokens; minor = new additions               |

## Common Mistakes

| Mistake                                       | Correct Pattern                                                          |
| --------------------------------------------- | ------------------------------------------------------------------------ |
| Primitive tokens in components (`blue-500`)   | Reference semantic tokens (`interactive-primary`) that map to primitives |
| Skipping focus states on interactive elements | Add `focus-visible:ring-2` on every button, link, and input              |
| Body text set to `gray-400`                   | Use `gray-600` or darker to meet 4.5:1 WCAG AA contrast                  |
| Circular token references between layers      | Tokens flow one direction: primitive > semantic > component              |
| Ignoring `prefers-reduced-motion`             | Wrap all animations in a reduced-motion media query                      |
| Using `scale()` transforms for hover          | Use `translateY(-1px)` and shadow changes to avoid layout shift          |
| Hardcoded hex/px values in component files    | All visual values come from semantic or component tokens                 |
| Deep CSS nesting for theme overrides          | Override CSS custom properties at the semantic layer                     |
| Theme flash on page load (FOUC)               | Inject synchronous theme script in `<head>` before body renders          |
| Flat token list without layers                | Organize into primitive, semantic, and component tiers                   |

## Delegation

- **Audit codebase for hardcoded values that should be tokens**: Use `Explore` agent
- **Migrate a component library to a token-based design system**: Use `Task` agent
- **Plan a multi-brand theming architecture**: Use `Plan` agent
- **Review accessibility compliance across components**: Use `Task` agent

> If the `motion` skill is available, delegate animation token integration and motion design patterns to it.

## References

- [Design Tokens](references/design-tokens.md) — three-layer hierarchy, CSS custom properties, TypeScript definitions, naming conventions
- [Theming](references/theming.md) — dark mode, theme provider, multi-brand, Tailwind v4, SSR flash prevention
- [Color and Typography](references/color-and-typography.md) — 60-30-10 rule, contrast requirements, type scale, fluid typography
- [Component Architecture](references/component-architecture.md) — CVA variants, compound components, headless UI, polymorphic rendering
- [Accessibility](references/accessibility.md) — WCAG compliance, keyboard navigation, ARIA patterns, screen reader testing
- [Motion and Layout](references/motion-and-layout.md) — animation tokens, reduced motion, spacing grid, elevation system
- [Tooling](references/tooling.md) — Style Dictionary, Storybook, component testing, visual regression
- [Governance](references/governance.md) — versioning, deprecation, contribution workflow, component lifecycle
- [Troubleshooting](references/troubleshooting.md) — common issues, dark mode fixes, token sprawl, pre-delivery checklist
