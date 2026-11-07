---
name: ui-design
description: >
  Core UI patterns for components and app screens: tokens, visual hierarchy, interactive
  states, forms, navigation, feedback states, accessibility, and responsive rules. Use when
  the user asks to "design a UI", "build a component", "create an interface", "style a form",
  "make it look good", "improve the design", "add hover states", "make it accessible", or any
  general UI work. This is the base the other UI skills build on; prefer landing-page-design
  for full marketing pages, hero-section for only the above-the-fold block, card-design for
  cards, dashboard-design for data-dense admin views, mobile-ui-design for touch-first
  screens, dark-mode for theming, and email-design for HTML email.
license: MIT
---

# UI Design Patterns

## Before You Start: Load Design Context

1. **Read `.agents/design-context.md`** (written by the `design-context` skill). If it is missing, look for tokens in `tailwind.config.*` or `:root` CSS variables. If nothing exists, use the defaults (Primary `#2563EB`, Secondary `#7C3AED`, Accent `#F59E0B`, Tailwind gray neutrals, Inter for headings and body, Minimal style) and **tell the user defaults were used** — suggest running `design-context`.
2. **Map tokens to CSS variables once**, then use only the variables: `--color-primary`, `--color-primary-light`, `--color-primary-dark`, `--color-secondary`, `--color-accent`, `--color-neutral-50`…`--color-neutral-900`, `--color-success`/`-warning`/`-error`, `--font-heading`, `--font-body`, `--font-mono`, `--radius`, and the 4px-base spacing scale.
3. **Tailwind:** expose the same variables (v3 `theme.extend`, v4 `@theme`) as `primary`, `primary-light`, `primary-dark`, `secondary`, `accent`, `neutral-*`, `font-heading`, `font-body`. The `indigo-*` / `gray-*` classes in the examples below are placeholders for these tokens.
4. **Figma:** if the user gives a Figma URL, pull it with the Figma MCP (`get_design_context`, `get_screenshot`) and match it; it overrides the context file for that design.
5. Let the **style archetype** set radius, shadow depth, and how much of section 9 (trends) to use — Minimal and Corporate use none of it.

---

## 1. Component Design Principles (Atomic Design)

Build UI in layers. Never start with a full page — start with the smallest pieces.

### Hierarchy
1. **Tokens** — colors, spacing, radii, shadows, typography scale
2. **Atoms** — button, input, badge, avatar, icon
3. **Molecules** — search bar (input + button), form field (label + input + error), card header (avatar + name + timestamp)
4. **Organisms** — navigation bar, hero section, comment thread, pricing table
5. **Templates** — page layouts composed of organisms
6. **Pages** — templates with real data

### Rules
- Every component gets its own set of CSS custom properties scoped to its root.
- Prefer composition over configuration. A `Card` with `children` beats a `Card` with 15 props.
- Components should be stateless by default. Lift state up.

```css
/* Token layer — values come from .agents/design-context.md (defaults shown) */
:root {
  --color-primary: #2563EB;
  --color-surface: #FFFFFF;
  --radius-md: 0.75rem;
  --shadow-sm: 0 1px 2px oklch(0% 0 0 / 0.05);
  --space-1: 0.25rem;
  --space-2: 0.5rem;
  --space-3: 0.75rem;
  --space-4: 1rem;
  --space-6: 1.5rem;
  --space-8: 2rem;
  --space-12: 3rem;
  --space-16: 4rem;
}
```

**Canonical spacing scale (all UI skills):** 4px base — 4, 8, 12, 16, 24, 32, 48, 64px (Tailwind `1, 2, 3, 4, 6, 8, 12, 16`). Don't use off-scale values.

---

## 2. Visual Hierarchy Framework

Control where the eye goes. Rank every element by importance and apply these levers:

| Lever | High Emphasis | Medium Emphasis | Low Emphasis |
|-------|--------------|-----------------|--------------|
| **Size** | 2rem+ heading | 1rem body | 0.75rem caption |
| **Weight** | 700–800 bold | 500 medium | 400 regular |
| **Color** | Primary or high-contrast text | Muted text (neutral-600) | Subtle text (neutral-500 — lightest gray that still passes 4.5:1 on white) |
| **Spacing** | More whitespace around it | Standard spacing | Tighter spacing |
| **Position** | Top-left or center | Mid-page | Bottom or sidebar |

### The Squint Test
Blur your eyes or zoom out to 25%. If you can still identify the primary action and main heading, your hierarchy works.

### Tailwind Implementation
```html
<!-- High emphasis -->
<h1 class="text-4xl font-extrabold tracking-tight text-gray-950">
  Ship faster with AI
</h1>

<!-- Medium emphasis -->
<p class="mt-4 text-lg text-gray-600 max-w-2xl">
  Build production-ready components in minutes, not hours.
</p>

<!-- Low emphasis -->
<span class="text-xs text-gray-500 uppercase tracking-wide">
  Updated 2 hours ago
</span>
```

---

## 3. Interactive States

Every interactive element needs all five states. No exceptions.

### State Definitions
```css
.btn-primary {
  /* Default */
  background: var(--color-primary);
  color: white;
  border-radius: var(--radius-md);
  padding: var(--space-2) var(--space-4);
  font-weight: 600;
  transition: background-color 150ms ease, box-shadow 150ms ease, transform 150ms ease, filter 150ms ease;

  /* Hover — subtle lift or brightness shift */
  &:hover {
    filter: brightness(1.1);
    box-shadow: 0 4px 12px oklch(0% 0 0 / 0.15);
    transform: translateY(-1px);
  }

  /* Active — pressed feel */
  &:active {
    transform: translateY(0);
    filter: brightness(0.95);
    box-shadow: var(--shadow-sm);
  }

  /* Focus — visible ring for keyboard users */
  &:focus-visible {
    outline: 2px solid var(--color-primary);
    outline-offset: 2px;
  }

  /* Disabled — dimmed, no hover/active effects (don't add pointer-events: none — it hides the not-allowed cursor) */
  &:disabled {
    opacity: 0.5;
    cursor: not-allowed;
    transform: none;
    box-shadow: none;
    filter: none;
  }
}
```

### Tailwind Shorthand
```html
<button class="bg-indigo-600 text-white px-4 py-2 rounded-lg font-semibold
  hover:bg-indigo-500 hover:-translate-y-0.5 hover:shadow-lg
  active:translate-y-0 active:bg-indigo-700
  focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600
  disabled:opacity-50 disabled:cursor-not-allowed disabled:pointer-events-none
  transition-all duration-150">
  Click me
</button>
```

---

## 4. Feedback Patterns

### Loading States
- **Skeleton screens** over spinners. Show the shape of content that's coming.
- Use `motion-safe:animate-pulse` on placeholder blocks, and mark the region `aria-busy="true"` with an sr-only "Loading…" label.
- Show loading inline near the action that triggered it.

```html
<!-- Skeleton card -->
<div class="motion-safe:animate-pulse space-y-3" aria-busy="true">
  <span class="sr-only">Loading…</span>
  <div class="h-48 bg-gray-200 rounded-xl"></div>
  <div class="h-4 bg-gray-200 rounded w-3/4"></div>
  <div class="h-4 bg-gray-200 rounded w-1/2"></div>
</div>
```

### Success State
- Green accent, checkmark icon, brief confirmation text.
- Announce it with `role="status"` (polite live region). Auto-dismiss after 5+ seconds, and never auto-dismiss messages that contain an action.

### Error State
- Red accent, descriptive message, recovery action.
- Never just say "Error." Say what went wrong and what to do.
- Don't rely on red alone: pair it with an icon and text; use `role="alert"` for errors that appear after submit.

### Empty State
- Illustration or icon, explanation, primary action to fix it.
```html
<div class="text-center py-16">
  <svg class="mx-auto h-12 w-12 text-gray-400" aria-hidden="true"><!-- inbox icon --></svg>
  <h3 class="mt-4 text-lg font-semibold text-gray-900">No messages yet</h3>
  <p class="mt-2 text-sm text-gray-500">Start a conversation to see messages here.</p>
  <button type="button" class="mt-6 bg-indigo-600 text-white px-4 py-2 rounded-lg">
    New message
  </button>
</div>
```

---

## 5. Navigation Patterns

### Sidebar Navigation
- Width: 240–280px desktop, collapsible to 64px (icon-only).
- Group items by category with subtle section headers.
- Active item: filled background, bold text, left accent bar, and `aria-current="page"`.

### Top Navigation
- Fixed/sticky at top. Height: 56–64px.
- Logo left, nav links center or left, actions right.
- Mobile: collapse to hamburger at `md` breakpoint.

### Tabs
- Use for switching views within the same context.
- Active tab: bottom border (2–3px) in primary color + bold text. Use `role="tablist"`/`role="tab"` with `aria-selected` and arrow-key navigation (or plain links if each tab is its own URL).
- Never more than 7 tabs. Use dropdown overflow for more.

### Breadcrumbs
- Use `/` or `>` separator.
- Current page is not a link, just text.
- Truncate middle items on long paths.

---

## 6. Form Design

### Rules
1. **Labels above inputs** — not floating, not inline. Always visible.
2. **One column** — multi-column forms reduce completion rate.
3. **Group related fields** with subtle section dividers.
4. **Inline validation** — validate on blur, not on every keystroke.
5. **Error messages below the field**, in red, with specific guidance.
6. **Primary action left-aligned** at form bottom. Secondary action as text link.

```html
<div class="space-y-1.5">
  <label for="email" class="block text-sm font-medium text-gray-700">
    Email address
  </label>
  <input
    type="email"
    id="email"
    class="block w-full rounded-lg border border-gray-300 px-3 py-2
      text-gray-900 placeholder:text-gray-400
      focus:border-indigo-500 focus:ring-2 focus:ring-indigo-500/20
      transition-colors"
    placeholder="you@example.com"
    autocomplete="email"
    aria-describedby="email-error"
  />
  <!-- On error: remove `hidden` and set aria-invalid="true" on the input -->
  <p id="email-error" class="text-sm text-red-600 hidden">Please enter a valid email address.</p>
</div>
```

---

## 7. Accessibility as Design

Accessibility is not an afterthought. It is a design constraint applied from the start.

### Contrast
- **Normal text**: 4.5:1 minimum contrast ratio (WCAG 2.2 AA).
- **Large text** (≥24px regular, or ≥18.66px bold): 3:1 minimum.
- **Non-text UI** (input borders, icons, focus rings, chart marks): 3:1 against adjacent colors.
- Placeholder text is not a label and should still meet 4.5:1 if it carries information.
- Use oklch color space for perceptually uniform contrast adjustments.

### Focus Indicators
- Never remove `outline` without replacing it.
- Use `focus-visible` (not `focus`) to avoid showing rings on mouse click.
- Ring: 2px solid, offset 2px, primary color, with 3:1 contrast against the background.
- Focused elements must not be hidden behind sticky headers/footers (WCAG 2.4.11) — add `scroll-padding-top` equal to the header height.

### Target Size
- WCAG 2.5.8 (AA): pointer targets at least **24×24 CSS px** (or spaced so a 24px circle doesn't overlap a neighbour).
- Platform guidance for touch: **44×44pt** (Apple HIG), **48×48dp** (Material). Use 44px+ for primary touch targets.

### Semantic Structure
- One `<h1>` per page.
- Headings in order (`h1` > `h2` > `h3`). Never skip levels.
- Use `<nav>`, `<main>`, `<aside>`, `<footer>` landmarks.
- Buttons for actions, links for navigation. Never `<div onclick>`.
- `aria-label` on icon-only buttons.

### Motion
```css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
    scroll-behavior: auto !important;
  }
}
```

---

## 8. Responsive Breakpoint Strategy

### Breakpoints (Tailwind defaults — canonical for all UI skills)
| Name | Width | Target |
|------|-------|--------|
| `sm` | 640px | Large phones landscape |
| `md` | 768px | Tablets |
| `lg` | 1024px | Small laptops |
| `xl` | 1280px | Desktops |
| `2xl` | 1536px | Large screens |

### Mobile-First Rules
- Start with the mobile layout. Add complexity at larger breakpoints.
- Stack columns on mobile, side-by-side on `md`+.
- Navigation becomes hamburger below `md`.
- Font sizes scale up: `text-2xl md:text-4xl lg:text-5xl`.
- Generous touch padding on mobile: `p-4`, tighten on desktop: `lg:p-2`.

### Container Queries (Modern CSS)
```css
.card-container {
  container-type: inline-size;
}

@container (min-width: 400px) {
  .card {
    display: grid;
    grid-template-columns: 200px 1fr;
  }
}
```

---

## 9. Modern UI Trends

### Glassmorphism
```css
.glass {
  background: oklch(100% 0 0 / 0.1);
  backdrop-filter: blur(16px) saturate(180%);
  border: 1px solid oklch(100% 0 0 / 0.15);
  border-radius: 1rem;
}
```
Glass only works over a busy background — check text contrast against the *lightest* area behind it, and give a solid fallback: `@supports not (backdrop-filter: blur(1px)) { .glass { background: oklch(20% 0.02 265 / 0.9); } }`.

### Bento Grid
```css
.bento {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  grid-auto-rows: minmax(200px, auto); /* fixed 200px rows clip long content */
  gap: 1rem;
}
@media (max-width: 767px) { .bento { grid-template-columns: 1fr; } .bento .featured { grid-column: auto; grid-row: auto; } }
.bento .featured {
  grid-column: span 2;
  grid-row: span 2;
}
```

### Aurora / Mesh Gradient Background
```css
.aurora {
  background: linear-gradient(135deg, oklch(85% 0.15 280), oklch(80% 0.2 320), oklch(75% 0.18 200));
  background-size: 400% 400%;
  animation: aurora-shift 8s ease infinite;
}
@keyframes aurora-shift {
  0%, 100% { background-position: 0% 50%; }
  50% { background-position: 100% 50%; }
}
```

---

## 10. Advanced CSS Techniques

### `:has()` — Parent Selector
```css
/* Highlight form group when input is focused */
.form-group:has(input:focus-visible) {
  background: oklch(97% 0.01 265);
  border-color: var(--color-primary);
}

/* Card changes layout when it contains an image */
.card:has(img) {
  grid-template-rows: 200px 1fr;
}
```

### Subgrid
```css
.card-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1.5rem;
}
.card {
  display: grid;
  grid-template-rows: subgrid;
  grid-row: span 3; /* header, body, footer align across cards */
}
```

### Scroll-Driven Animations
```css
/* Progressive enhancement: only where supported and motion is OK */
@supports (animation-timeline: view()) {
  @media (prefers-reduced-motion: no-preference) {
    .fade-in {
      animation: fade-in linear both;
      animation-timeline: view();
      animation-range: entry 0% entry 100%;
    }
  }
}
@keyframes fade-in {
  from { opacity: 0; transform: translateY(2rem); }
  to { opacity: 1; transform: translateY(0); }
}
```

---

## Verify: Render and Check

Don't hand over code you haven't looked at. After generating it:
1. Screenshot it at mobile and desktop widths, e.g. `npx playwright screenshot --full-page --viewport-size=390,844 file://$PWD/index.html mobile.png`, then again with `--viewport-size=1440,900` (or point at the dev server URL).
2. Open both images and check: no horizontal scroll or clipped/overlapping text, hierarchy reads at a glance, brand tokens are applied, images load at the right aspect ratio.
3. Tab through once: every interactive element gets a visible focus ring, in a logical order.
4. Check every state you built (hover, focus, disabled, loading, empty, error) at least once, and run a contrast check on muted text.
5. Fix what you find and re-screenshot before reporting done.

---

## Quick Reference: Design Checklist

Before shipping any UI component, verify:

- [ ] Visual hierarchy is clear (squint test passes)
- [ ] All interactive elements have hover, active, focus-visible, and disabled states
- [ ] Color contrast meets WCAG 2.2 AA (4.5:1 text, 3:1 large text and UI components)
- [ ] Targets are ≥24×24px (44px+ for primary touch targets)
- [ ] Rendered and screenshotted at 390px and 1440px (see Verify)
- [ ] Focus order is logical (tab through the page)
- [ ] Responsive at all breakpoints (320px to 1920px)
- [ ] Loading, empty, and error states are designed
- [ ] Spacing uses the 4px-base scale (4, 8, 12, 16, 24, 32, 48, 64)
- [ ] Typography scale is limited to 4–6 sizes
- [ ] Motion respects `prefers-reduced-motion`
- [ ] Semantic HTML is used (landmarks, headings, button vs. link)
