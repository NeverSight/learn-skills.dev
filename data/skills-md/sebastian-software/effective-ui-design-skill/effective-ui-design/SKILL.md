---
name: effective-ui-design
description: |
  Professional UI design guidelines for accessible, well-structured interfaces. Use when: writing CSS, HTML, or frontend component code; designing websites, apps, dashboards, or any web interface; reviewing or improving existing UI designs; making decisions about colour, typography, layout, spacing, buttons, or forms; ensuring WCAG 2.1 AA accessibility; creating design systems or component libraries. Covers OKLCH colour palettes, 8pt spacing grid, fluid typography with clamp(), container queries, subgrid, form validation patterns, button hierarchy, dark mode, reduced motion, SEO meta tags, and Core Web Vitals.
license: MIT
metadata:
  author: sebastian-software
  version: "1.0"
---

# Effective UI Design

Enforces professional UI design guidelines for accessible, well-structured interfaces. Apply these rules to every UI design decision without exception.

## Quick Reference

| Topic | Reference File |
|-------|---------------|
| Fundamentals | [references/01-fundamentals.md](references/01-fundamentals.md) |
| Less is More | [references/02-less-is-more.md](references/02-less-is-more.md) |
| Colour | [references/03-colour.md](references/03-colour.md) |
| Layout & Spacing | [references/04-layout-spacing.md](references/04-layout-spacing.md) |
| Typography | [references/05-typography.md](references/05-typography.md) |
| Web Fonts | [references/05b-webfonts.md](references/05b-webfonts.md) |
| Copywriting | [references/06-copywriting.md](references/06-copywriting.md) |
| Buttons | [references/07-buttons.md](references/07-buttons.md) |
| Forms | [references/08-forms.md](references/08-forms.md) |
| SEO for Frontend | [references/09-seo.md](references/09-seo.md) |

## Core Principles (ALWAYS Apply)

### 1. Minimise Usability Risks
- Meet WCAG 2.1 level AA accessibility requirements
- Consider users with poor eyesight, low computer literacy, reduced dexterity
- Avoid thin/light grey text, icons without labels, colored headings that look like links

### 2. Have a Logical Reason for Every Design Detail
- Every element must have a purpose that improves usability
- Design using objective logic, not subjective opinion
- Be able to articulate the rationale behind each decision

### 3. Minimise Interaction Cost
- Keep related actions close (Fitts's Law)
- Reduce distractions
- Minimise choices (Hick's Law)
- Use minimum 48pt × 48pt target areas

### 4. Minimise Cognitive Load
- Remove unnecessary styles/information
- Break information into smaller groups
- Use familiar design patterns (Jakob's Law)
- Maintain consistency
- Create clear visual hierarchy

### 5. Create a Design System
- Define predefined colour palette
- Set typography scale
- Use 8pt spacing increments: 8pt, 16pt, 24pt, 32pt, 48pt, 80pt
- Create reusable components

## Critical Rules (NEVER Violate)

### Colour
- Text contrast: minimum 4.5:1 ratio (small text ≤18px)
- Large text/UI elements: minimum 3:1 ratio
- Never rely on colour alone to convey meaning
- Use brand colour ONLY for interactive elements
- Avoid pure black (#000000) on white - use dark grey instead
- Use OKLCH for perceptually uniform palettes; derive variations with relative color syntax
- Use `light-dark()` for theme switching without media query duplication

### Typography
- Use single sans-serif typeface for most interfaces
- UI text (labels, buttons, nav): 14px base
- Body text: 16px base, scale to 18-20px for long-form reading via `clamp()`
- Line height: minimum 1.5 (150%) for body text
- Line length: 40-80 characters per line
- Left-align text (for English)
- Limit font weights: typically 2, max 3 (e.g. Regular 400, Medium 500, Bold 700)

### Layout
- Space elements based on relationship (closer = more related)
- Use 12-column grid for main layout
- Align elements to create neat edges
- Be generous with white space
- Use container queries for component-level responsiveness; media queries for page-level layout
- Use subgrid to align nested content across sibling elements (e.g. card grids)
- Use responsive images (`srcset`, `loading="lazy"`, `aspect-ratio` to prevent layout shift)
- Gate hover effects behind `@media (hover: hover) and (pointer: fine)` — never hide content behind hover
- Use `env(safe-area-inset-*)` with `viewport-fit=cover` for fixed/sticky elements on notched devices

### Icons
- Use SVG icons exclusively — never emoji or icon fonts
- One icon set, used consistently (e.g. Lucide, Heroicons, Phosphor)
- Use `currentColor` to inherit text colour; match stroke width to font weight
- Always pair icons with visible text labels; icon-only buttons need `aria-label`

### Buttons
- Define 3 button weights: Primary, Secondary, Tertiary
- Use single primary button per screen
- Left-align buttons (most important first)
- Button text: verb + noun (e.g., "Save post")
- Minimum size: 48pt × 48pt
- Avoid disabled buttons - validate on submit instead

### Forms
- Single column layout
- Stack labels above inputs
- Mark both required (*) and optional fields
- Match field width to expected input
- Use conventional form field styles
- Display hints above fields (not below)
- Use `:user-valid`/`:user-invalid` for validation that respects interaction timing

### SEO
- Unique `<title>` per page (50-60 chars, primary keyword near the beginning)
- Unique `<meta name="description">` per page (150-160 chars)
- Self-referencing `<link rel="canonical">` on every page
- One `<h1>` per page, logical heading hierarchy (no level skipping)
- Open Graph tags (`og:title`, `og:description`, `og:image`) for social sharing
- JSON-LD structured data for rich results (Article, Product, BreadcrumbList, FAQPage)
- Descriptive, hyphenated image file names and natural alt text
- Meet Core Web Vitals: LCP < 2.5s, INP < 200ms, CLS < 0.1

### Favicons
- Five icons: `favicon.ico` (32×32), `icon.svg` (with dark mode), `apple-touch-icon.png` (180×180), `icon-192.png`, `icon-512.png`
- SVG favicons support `@media (prefers-color-scheme: dark)` for automatic dark mode
- For PWAs: add `manifest.webmanifest` with `icon-192.png`, `icon-mask.png` (512×512, maskable), and `icon-512.png`
- Maskable icons need extra padding — safe zone is a 409×409 circle
- Do not generate multiple PNG sizes, multiple Apple touch icon sizes, or `browserconfig.xml`

## Design Checklist

Before finalizing any UI design:

1. **Accessibility**
   - [ ] All text has 4.5:1+ contrast ratio
   - [ ] UI elements have 3:1+ contrast ratio
   - [ ] Colour is not the only indicator
   - [ ] Target areas are 48pt+ minimum
   - [ ] Text links are underlined
   - [ ] Semantic HTML used (`<nav>`, `<main>`, `<search>`, landmarks)
   - [ ] Icons have visible text labels (or `aria-label` for icon-only buttons)
   - [ ] Images have meaningful `alt` text (empty `alt=""` for decorative)
   - [ ] Skip link present as first focusable element
   - [ ] Viewport meta tag does not disable zoom (`user-scalable=no` / `maximum-scale=1`)
   - [ ] Composite widgets (tabs, toolbars, menus) use single Tab stop with arrow-key navigation

2. **Visual Hierarchy**
   - [ ] Clear order of importance
   - [ ] Primary action is most prominent
   - [ ] Related elements are grouped
   - [ ] Consistent spacing applied

3. **Typography**
   - [ ] 1-2 typefaces (+ optional display/heading typeface)
   - [ ] UI text 14px+, body text 16px+ (18-20px for long-form reading)
   - [ ] Line height 1.5+ for body text
   - [ ] Left-aligned text
   - [ ] 40-80 characters per line

4. **Copywriting**
   - [ ] Concise text (no unnecessary words)
   - [ ] Sentence case used
   - [ ] Plain language (no jargon)
   - [ ] Front-loaded important info
   - [ ] Descriptive button text

5. **Forms**
   - [ ] Single column layout
   - [ ] Labels above inputs
   - [ ] Required/optional fields marked
   - [ ] Field widths match expected input
   - [ ] High contrast borders (3:1+)

6. **SEO**
   - [ ] Unique `<title>` with primary keyword (50-60 chars)
   - [ ] Unique `<meta name="description">` (150-160 chars)
   - [ ] Self-referencing canonical tag
   - [ ] One `<h1>` per page, no heading level skips
   - [ ] Open Graph tags present (`og:title`, `og:description`, `og:image`)
   - [ ] JSON-LD structured data where applicable
   - [ ] Descriptive image file names and alt text
   - [ ] LCP image not lazy-loaded, has `fetchpriority="high"`
   - [ ] Favicons: `favicon.ico`, `icon.svg` (with dark mode), `apple-touch-icon.png`, `icon-192.png`, `icon-512.png`
   - [ ] PWA: `manifest.webmanifest` with `icon-192.png`, `icon-mask.png` (maskable), `icon-512.png`

## Implementation

When creating UI code:

1. Read the relevant reference files for detailed guidelines
2. Apply ALL rules without exception
3. Verify against the checklist above
4. Use the predefined spacing scale (8pt increments)
5. Use the colour palette structure from [references/03-colour.md](references/03-colour.md)
6. Use the Popover API for tooltips, dropdowns, and menus (no JS library needed)
7. Use `@starting-style` for CSS-only entry animations on dialogs and popovers
8. Use the View Transition API for page transitions and shared element animations; always respect `prefers-reduced-motion`

## Colour Palette Template (OKLCH)

```
Brand:         oklch(60% 0.15 hue)     - Interactive elements
Text strong:   oklch(25% 0.02 hue)     - Headings, primary text (4.5:1+)
Text weak:     oklch(45% 0.02 hue)     - Secondary text (4.5:1+)
Stroke strong: oklch(58% 0.02 hue)     - Form borders, icons (3:1+)
Stroke weak:   oklch(92% 0.005 hue)    - Decorative borders
Fill:          oklch(97% 0.003 hue)    - Secondary backgrounds
Background:    oklch(100% 0 0)         - White or near-white
```

## Typography Scale (1.200 Minor Third)

```
Heading 1: 40px / 48px line-height / bold
Heading 2: 32px / 40px line-height / bold
Heading 3: 24px / 32px line-height / bold
Heading 4: 20px / 28px line-height / bold
Body:      16px / 24px line-height / regular
Small:     14px / 20px line-height / regular
```

## Spacing Scale (8pt Grid)

```
XS:  8pt   - Closely related elements
S:   16pt  - Related elements
M:   24pt  - Component padding
L:   32pt  - Grid gutters, section gaps
XL:  48pt  - Large section gaps
XXL: 80pt  - Page section padding
```
