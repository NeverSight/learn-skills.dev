---
name: tailwind-ui
description: Use when writing HTML/JSX with Tailwind CSS for common UI patterns like heroes, forms, lists, navbars, modals, cards, or any standard web component
model: haiku
---

# Tailwind UI Templates

## Overview

**Always search templates before writing Tailwind UI code from scratch.**

You have access to 657 hand-crafted Tailwind UI templates in `assets/`. These templates include dark mode, accessibility, polish, and edge case handling that you won't replicate from scratch.

## When to Use

**Use this skill when:**
- Building any common UI component (hero, navbar, form, list, card, modal, etc.)
- Writing HTML/JSX with Tailwind CSS classes
- Need professional-quality, accessible, responsive UI

**Skip for:**
- Minor styling tweaks to existing code
- Non-UI code (logic, data, APIs)

## Template Discovery

### 1. Search the Index

```bash
# Find templates by keyword
grep -i "hero" assets/index.jsonl | jq .

# Browse by category
grep '"category":"marketing"' assets/index.jsonl | jq -r '.subsection' | sort | uniq

# Find specific component type
grep -i "stacked.*list" assets/index.jsonl | jq .
```

### 2. Understand the Hierarchy

```
Category (3): marketing, application-ui, ecommerce
  └─ Section: Page Sections, Elements, Forms, etc.
      └─ Subsection: Hero Sections, Feature Sections, Stacked Lists, etc.
          └─ Component: "Simple centered", "Split with screenshot", etc.
```

### 3. Read the Template

```
assets/code/{version}/{language}/{category}/{subsection}/{slug}.{ext}

Examples:
  assets/code/v4/html/marketing/hero-sections/simple-centered.html
  assets/code/v4/react/application-ui/stacked-lists/with-badges.tsx
  assets/code/v4/vue/ecommerce/product-pages/with-image-grid.vue
```

**Always prefer v4** (latest Tailwind CSS). Use v3 only for legacy projects.

## Usage Modes

| Mode | When | How |
|------|------|-----|
| **Verbatim** | Template matches exactly | Copy template, swap placeholder content |
| **Modify** | Template is close | Start from template, adjust structure/styling |
| **Synthesize** | Need combination | Study 2-3 similar templates, combine patterns |
| **Learn & Create** | No exact match | Find closest templates, extract patterns, apply to novel component |

### When No Exact Template Exists

**Never write truly from scratch.** Even for novel components, find inspiration and patterns in existing templates. This ensures your code is consistent with Tailwind UI conventions even when no template exists.

## Template Qualities to Preserve

Tailwind UI templates include polish you'll lose if writing from scratch:

- **Dark mode**: `dark:` variants throughout
- **Accessibility**: `aria-*` attributes, semantic HTML, focus states
- **Responsive**: Mobile-first with `sm:`, `md:`, `lg:` breakpoints
- **Focus states**: `focus-visible:outline-2 focus-visible:outline-offset-2`
- **Subtle polish**: `text-pretty`, `shadow-xs`, gradient masks, decorative SVGs

## Red Flags

If you catch yourself doing any of these, STOP and search templates:

- "Let me write a quick hero section"
- "I'll just add some Tailwind classes"
- "This is a simple component"
- "I know how to do this"
- "There's no template for this" → Find similar ones and learn patterns!

**657 templates exist. One is probably close, or several can teach you the patterns.**
