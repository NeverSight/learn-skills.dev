---
name: dioxus-ui-ux
description: "Dioxus UI/UX design intelligence. Specialized guidelines for Dioxus Components, plus 50 styles, 21 palettes, 50 font pairings. Stacks: dioxus, daisyui, shadcn, html-tailwind. Actions: plan, build, create, design, implement, review, fix, improve, optimize. Projects: web app, dashboard, admin panel, SaaS, mobile app. Elements: button, modal, navbar, card, form, chart."
---

# Dioxus UI/UX Skill - Design Intelligence

Comprehensive design guide for Dioxus applications using Dioxus Components. Contains guidelines for component usage, design systems, and general UI/UX best practices.

## When to Apply

Reference these guidelines when:
- Building Dioxus applications with `dioxus-components`
- Designing new UI components or pages
- Choosing color palettes and typography
- Reviewing code for UX issues
- Implementing accessibility requirements

## Quick Reference

### 1. Dioxus Components (CRITICAL)

- `installation` - Use `dx components add` CLI command
- `theming` - Use CSS variables in `dx-components.css`
- `variants` - Use props (enums) for variants, not raw classes
- `structure` - Keep components in `components/` directory
- `primitives` - Use `dioxus-primitives` for custom accessible components

### 2. Accessibility (CRITICAL)

- `color-contrast` - Minimum 4.5:1 ratio for normal text
- `focus-states` - Visible focus rings on interactive elements
- `alt-text` - Descriptive alt text for meaningful images
- `aria-labels` - aria-label for icon-only buttons

### 3. Performance (HIGH)

- `lazy-loading` - Load heavy components lazily if possible
- `assets` - Optimize images and fonts
- `re-renders` - Use `use_memo` and `use_callback` appropriately

## How to Use

Search specific domains using the CLI tool below.

---

## Prerequisites

Check if Python is installed:

```bash
python3 --version || python --version
```

---

## How to Use This Skill

When user requests UI/UX work for Dioxus, follow this workflow:

### Step 1: Analyze User Requirements

Extract key information from user request:
- **Product type**: SaaS, e-commerce, portfolio, dashboard, etc.
- **Style keywords**: minimal, professional, elegant, etc.
- **Stack**: **dioxus** (Primary), daisyui (Components), shadcn (Reference), html-tailwind (Styling)

### Step 2: Generate Design System (REQUIRED)

**Always start with `--design-system`** to get comprehensive recommendations:

```bash
python3 skills/dioxus-ui-ux/scripts/search.py "<product_type> <keywords>" --design-system -p "Project Name"
```

### Step 3: Dioxus Guidelines

Get implementation-specific best practices for Dioxus Components:

```bash
python3 skills/dioxus-ui-ux/scripts/search.py "<component_name>" --stack dioxus
```

**Example:**
```bash
python3 skills/dioxus-ui-ux/scripts/search.py "button" --stack dioxus
```

### Step 4: Supplement with Reference Patterns (Optional)

If Dioxus docs are sparse, check Shadcn patterns:

```bash
python3 skills/dioxus-ui-ux/scripts/search.py "dialog" --stack shadcn
```

### Step 5: General UI Search

For styles, colors, and typography:

```bash
python3 skills/dioxus-ui-ux/scripts/search.py "glassmorphism" --domain style
python3 skills/dioxus-ui-ux/scripts/search.py "fintech" --domain color
```

---

## Search Reference

### Available Stacks

| Stack | Focus | Usage |
|-------|-------|-------|
| `dioxus` | Core Dioxus Components guidelines | `--stack dioxus` |
| `daisyui` | Semantic daisyUI component classes | `--stack daisyui` |
| `shadcn` | Upstream React component patterns | `--stack shadcn` |
| `html-tailwind` | Utility class best practices | `--stack html-tailwind` |

### Available Domains

| Domain | Use For |
|--------|---------|
| `style` | UI styles, visual effects |
| `color` | Color palettes by industry |
| `typography` | Font pairings |
| `chart` | Chart recommendations |
| `ux` | UX best practices |

---

## Pre-Delivery Checklist

Before delivering Dioxus UI code:

### Dioxus Specifics
- [ ] Components installed via CLI (`dx components add`)
- [ ] CSS variables used for theming
- [ ] Variants passed as props, not hardcoded strings
- [ ] `dx-components.css` linked in root

### Visual Quality
- [ ] No emojis used as icons (use SVG)
- [ ] Consistent icon sizing
- [ ] Hover states defined
- [ ] Cursor pointer on interactive elements

### Accessibility
- [ ] Contrast ratio > 4.5:1
- [ ] Images have alt text
- [ ] Interactive elements focusable via keyboard
