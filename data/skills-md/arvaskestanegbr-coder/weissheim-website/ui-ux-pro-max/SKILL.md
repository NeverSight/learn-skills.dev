---
name: ui-ux-pro-max
description: Use this skill for systematic UI/UX design decisions — color palettes, font pairings, layout patterns, accessibility, and design system creation. Activates when designing or auditing any UI component, page, or design system.
---

# UI/UX Pro Max — Design Intelligence

Comprehensive design guide covering 50+ styles, 97 color palettes, 57 font pairings, 99 UX guidelines across 9 technology stacks.

## Rule Priority Tiers

### CRITICAL
**Accessibility**
- Minimum 4.5:1 contrast ratio for normal text, 3:1 for large text
- All interactive elements need visible focus states
- Never rely on color alone to convey meaning
- ARIA labels for icon-only buttons

**Touch & Interaction**
- Minimum touch target: 44×44px
- Tap targets must have 8px spacing between them
- Hover states must not be the only interactive feedback

### HIGH
**Performance**
- Compress all images (WebP preferred)
- Respect `prefers-reduced-motion` for animations
- Lazy-load below-the-fold images
- Avoid layout shifts (CLS)

**Typography**
- Line height: 1.5–1.75 for body text
- Line length: 65–75 characters max
- Never use font-size below 14px for body
- Heading hierarchy must be logical (h1 → h2 → h3)

**Spacing & Layout**
- Use a consistent spacing scale (4px base)
- Breathing room around text blocks: minimum 24px padding
- Consistent alignment — pick a grid and stick to it

### MEDIUM
**Color Systems**
- Define a primary, secondary, and neutral palette
- Reserve accent color for maximum 10–15% of UI
- Background variants: page bg, card bg, subtle bg (3 levels)
- Error, warning, success, info states always defined

**Component Consistency**
- Border radius should be consistent system-wide
- Shadow system: 3 levels (sm, md, lg)
- Button sizes: sm / md / lg with consistent padding ratios

**Forms & Inputs**
- Labels always visible (no placeholder-as-label)
- Error messages inline, below the field
- Success state confirmation after submission
- Disabled states visually distinct

### LOW
**Animation**
- Entrance animations: 200–400ms, ease-out
- Exit animations: 150–250ms, ease-in
- Never animate more than transform + opacity simultaneously
- Page transitions: subtle, not distracting

**Charts & Data**
- Always include a text alternative for charts
- Color-blind safe palettes for data visualization
- Axes and labels always readable at mobile size

## Design System Workflow

1. **Analyze requirements** — product type, target audience, brand tone
2. **Define design tokens** — colors, typography, spacing, shadows, radius
3. **Apply stack guidelines** — Tailwind CSS utilities for each token
4. **Validate against checklist** — accessibility, responsiveness, consistency

## Pre-Delivery Checklist

Before any UI is considered done:

**Visual Quality**
- [ ] Font hierarchy is clear and consistent
- [ ] Color contrast passes WCAG AA
- [ ] Spacing is consistent (no magic numbers)
- [ ] Images are sharp on 2x displays

**Interaction**
- [ ] All buttons have hover + active states
- [ ] Focus states visible for keyboard navigation
- [ ] Loading states for async actions

**Accessibility**
- [ ] All images have alt text
- [ ] Color is not the only differentiator
- [ ] Touch targets ≥ 44px

**Responsiveness**
- [ ] Mobile (375px), tablet (768px), desktop (1280px) tested
- [ ] No horizontal scroll on mobile
- [ ] Font sizes readable without zoom on mobile

## For This Project (WEISSHEIM)

**Stack:** React 18 + TypeScript + Tailwind CSS + shadcn/ui
**Tone:** Premium, clean, trustworthy — German market
**Product colors to integrate:** Himmelblau (#87CEEB range), Beige (#F5F0E8 range), Schwarz
**Conversion goal:** Single CTA — Amazon purchase
**Key UX priority:** Trust signals + friction reduction
