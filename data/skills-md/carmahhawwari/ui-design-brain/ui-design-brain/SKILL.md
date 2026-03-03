---
name: ui-design-brain
description: Generate production-grade UI using real component patterns and best practices from 60+ documented interface components. Use when the user asks to build web interfaces, pages, dashboards, forms, navigation, or any UI — ensures modern, minimal, SaaS-quality output grounded in design system conventions rather than generic AI patterns.
license: Complete terms in LICENSE.txt
---

# UI Design Brain

This skill provides a curated knowledge base of 60+ UI component patterns sourced from [component.gallery](https://component.gallery) and enriched with best practices, layout guidance, and usage rules. It replaces generic guessing with real design-system knowledge when generating interfaces.

**Before writing any UI code**, consult this skill to select the right components and follow their best practices. Read [components.md](components.md) for the full reference.

## When to Use This Skill

Apply whenever the user asks to build, design, or generate:
- Web pages, landing pages, marketing sites
- SaaS dashboards, admin panels, settings pages
- Forms, data tables, navigation structures
- Modals, drawers, popovers, or overlay patterns
- Any React, HTML/CSS, or Tailwind UI component

## Design Philosophy

Every generated interface should feel **modern, minimal, and production-ready** — not like a template.

### Core Principles

1. **Restraint over decoration.** Fewer elements, highly refined. White space is a feature.
2. **Typography carries hierarchy.** Pair a distinctive display font with a clean body font. Maximize weight contrast between headings and labels.
3. **One strong color moment.** Neutral palette first (warm off-whites, near-blacks, muted mid-tones). Introduce one confident accent. If it could appear on a poster or book cover, it's probably timeless.
4. **Spacing is structure.** Use an 8 px grid. Tighter gaps group related elements; generous gaps let hero content breathe.
5. **Accessibility is non-negotiable.** WCAG AA contrast minimums. Focus indicators. Semantic HTML. Keyboard navigation.
6. **No generic AI aesthetics.** Avoid: purple-on-white gradients, Inter/Roboto defaults, evenly-spaced card grids, and cookie-cutter layouts. Every interface should feel designed for its specific context.

### Quality Bar

The output should match what you'd expect from a senior product designer at a top SaaS company:
- Clean visual rhythm with intentional asymmetry
- Obvious interactive affordances (hover, focus, active states)
- Graceful edge cases (empty states, loading, error)
- Responsive without breakpoint artifacts

## Workflow

### Step 1 — Identify Components

Read the user's request and determine which UI components are needed. Reference [components.md](components.md) to find each component by name or alias.

Common mappings:
- "navigation" → Header, Navigation, Breadcrumbs, Tabs
- "form" → Form, Text input, Select, Checkbox, Radio button, Button
- "data display" → Table, Card, List, Badge, Avatar
- "feedback" → Alert, Toast, Modal, Spinner, Progress bar, Empty state
- "input" → Text input, Textarea, Select, Combobox, Datepicker, File upload, Slider
- "overlay" → Modal, Drawer, Popover, Tooltip, Dropdown menu

### Step 2 — Apply Best Practices

For each component in the interface, follow its best practices from the reference. Key rules that apply broadly:

**Layout**
- Single-column forms — faster to scan
- Consistent vertical lanes in repeated rows (lists, tables)
- Fixed-width slots for icons and actions, even when empty
- Cards: media → title → meta → action hierarchy

**Interaction**
- Buttons: verb-first labels ("Save changes", not "Submit"), one primary per section
- Modals: always provide X, Cancel, and Escape; trap focus; return focus on close
- Toasts: auto-dismiss 4–6 s, allow manual dismiss, stack newest on top
- Toggles: immediate effect only — use checkboxes in forms that require Save

**Typography & Spacing**
- Strict heading hierarchy (h1 → h2 → h3), one h1 per page
- Minimum 44 px touch targets on mobile
- Labels above inputs (vertical forms) or beside (horizontal)
- Placeholder text as format hint, never as label replacement

**States**
- Empty states: illustration + helpful headline + primary CTA
- Loading: skeleton screens > spinners (show after 300 ms delay)
- Validation: inline on blur, not on every keystroke
- Disabled elements: visually distinct but still readable

### Step 3 — Choose a Design Direction

Select the style preset that best matches the user's intent, or ask if unclear:

**Modern SaaS** (default)
- Neutral palette, one strong accent
- 8 px grid, generous white space
- Clean, professional, spacious

**Apple-level Minimal**
- Near-monochrome, warm grays
- Large type hierarchy, tight tracking on display text
- Abundant white space, micro-interactions (150–250 ms ease-out)

**Enterprise / Corporate**
- Information-dense, well-defined regions
- Compact spacing scale (4/8/12/16/24 px)
- Robust form handling, fully keyboard-navigable

**Creative / Portfolio**
- Bold, expressive, strong visual personality
- Asymmetric layouts, dramatic scale contrast
- Editorial typography, vivid accent colors

**Data Dashboard**
- Data-dense, optimised for scannability
- Consistent vertical alignment across rows
- Clear metric hierarchy: KPI → trend → detail

### Step 4 — Generate Code

Write production-ready code following these rules:

```
Stack:       React + Tailwind CSS (unless user specifies otherwise)
Spacing:     Tailwind spacing scale (p-2, gap-4, etc.) on an 8px grid
Colors:      CSS variables or Tailwind config for palette consistency
Typography:  Tailwind text utilities; expressive font pairings via Google Fonts
States:      Implement hover, focus, active, disabled for all interactive elements
Responsive:  Mobile-first; test at 375, 768, 1440 px
Accessibility: Semantic HTML, ARIA where needed, focus management
```

## Component Quick Reference

Below are the 15 most commonly needed components. For the full 60+ component reference with best practices, aliases, and layout examples, see [components.md](components.md).

| Component | When to use | Key rule |
|-----------|------------|----------|
| **Button** | Trigger actions | Verb-first labels; one primary per section |
| **Card** | Represent an entity | Media → title → meta → action; shadow OR border, not both |
| **Modal** | Focused attention | Trap focus; X + Cancel + Escape to close |
| **Navigation** | Page/section links | 5–7 items max; clear active state |
| **Table** | Structured data | Sticky header; right-align numbers; sortable columns |
| **Tabs** | Switch panels | 2–7 tabs; active indicator; accordion on mobile |
| **Form** | Collect input | Single column; labels above; inline validation on blur |
| **Toast** | Brief confirmation | Auto-dismiss 4–6 s; undo action for destructive ops |
| **Alert** | Important status | Semantic colors + icon; max 2 sentences |
| **Drawer** | Secondary panel | Right for detail, left for nav; 320–480 px desktop |
| **Search input** | Find content | Cmd/Ctrl+K shortcut; debounce 200–300 ms |
| **Empty state** | No data | Illustration + headline + CTA; positive framing |
| **Skeleton** | Loading placeholder | Match actual layout shape; shimmer animation |
| **Badge** | Status/metadata label | 1–2 words; pill shape for status; limited color palette |
| **Dropdown menu** | Action/nav options | 7±2 items; destructive actions last in red |

## Anti-Patterns to Avoid

Never generate these — they signal generic, low-quality UI:

- **Rainbow badges** — every status a different bright color with no semantic meaning
- **Modal inside modal** — use a page or drawer for complex flows
- **Disabled submit with no explanation** — always indicate what's missing
- **Spinner for predictable layouts** — use skeleton screens instead
- **"Click here" links** — link text must describe the destination
- **Hamburger menu on desktop** — use visible navigation when space allows
- **Auto-advancing carousels** — let users control navigation
- **Placeholder-only form fields** — always use visible labels
- **Equal-weight buttons** — establish primary/secondary/tertiary hierarchy
- **Tiny text (< 12 px)** — body text minimum 14 px, prefer 16 px
