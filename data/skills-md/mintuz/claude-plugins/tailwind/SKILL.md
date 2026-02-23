---
name: tailwind
description: WHEN building design systems or component libraries with Tailwind CSS; covers design tokens, CVA patterns and dark mode.
---

# Prerequisites

- Load the `web:css` skill for CSS Best Practices.
- Load the `web:react` skill for React Best Practices.
- Load the `web:typescript` skill for TypeScript Best Practices.
- load the `web:web-design` skill for Design Best Practices.

# Tailwind Design System

Build production-ready design systems with Tailwind CSS, including design tokens, component variants, responsive patterns, and accessibility.

## Quick Reference

| Topic                               | Guide                                             |
| ----------------------------------- | ------------------------------------------------- |
| Tailwind config, global CSS, tokens | [setup.md](references/setup.md)                   |
| CVA pattern with type-safe variants | [cva-components.md](references/cva-components.md) |
| Animation utilities and Dialog      | [animations.md](references/animations.md)         |
| Utility functions (cn, focusRing)   | [utilities.md](references/utilities.md)           |
| Do's and Don'ts for maintainability | [best-practices.md](references/best-practices.md) |

## When to Use This Skill

- Creating a component library with Tailwind
- Implementing design tokens and theming
- Building responsive and accessible components
- Standardizing UI patterns across a codebase
- Migrating to or extending Tailwind CSS

## Core Concepts

### Design Token Hierarchy

```
Brand Tokens (abstract)
    └── Semantic Tokens (purpose)
        └── Component Tokens (specific)

Example:
    blue-500 → primary → button-bg
```

### Component Architecture

```
Base styles → Variants → Sizes → States → Overrides
```

## When to Use Each Guide

### Setup

Use [setup.md](references/setup.md) when you need:

- Initial Tailwind configuration
- CSS variable setup for theming
- Design token structure
- Global styles foundation

### CVA Components

Use [cva-components.md](references/cva-components.md) when you need:

- Type-safe component variants
- Button, Badge, or similar components
- Standardized variant APIs
- Reusable component patterns

### Animations

Use [animations.md](references/animations.md) when you need:

- Entry/exit animations
- Dialog or modal transitions
- Tailwind CSS Animate utilities
- State-based animations

### Utilities

Use [utilities.md](references/utilities.md) when you need:

- Class name composition (cn function)
- Common utility patterns
- Focus ring, disabled state helpers

### Best Practices

Use [best-practices.md](references/best-practices.md) for:

- Guidance on semantic naming
- Do's and Don'ts
- Accessibility requirements
- Performance considerations

## Quick Decision Trees

### Where should colors be defined?

```
Is this a one-off color?
├── Yes → Use arbitrary value sparingly (e.g., bg-[#abc123])
└── No → Is it semantic (primary, destructive)?
    ├── Yes → Add to semantic tokens in setup.md
    └── No → Is it a brand color?
        ├── Yes → Add to theme.extend.colors
        └── No → Use existing Tailwind color
```

## Installation

```bash
# Required packages
yarn add tailwindcss postcss autoprefixer
yarn add class-variance-authority clsx tailwind-merge
yarn add tailwindcss-animate
```

## Resources

- [Tailwind CSS Documentation](https://tailwindcss.com/docs)
- [CVA Documentation](https://cva.style/docs)
- [shadcn/ui](https://ui.shadcn.com/)
- [Radix Primitives](https://www.radix-ui.com/primitives)
