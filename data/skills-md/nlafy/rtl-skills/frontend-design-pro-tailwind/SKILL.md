---
name: frontend-design-pro-tailwind
description: Design and implement professional, polished, official-looking frontend interfaces using Tailwind CSS latest/v4, JavaScript/TypeScript, React/Next.js, and modern design-system practices. Use this skill when the user asks for UI design, landing pages, dashboards, SaaS interfaces, admin panels, forms, tables, responsive layouts, RTL/LTR multilingual UI, Arabic interfaces, visual polish, redesigns, component systems, Tailwind classes, design tokens, or frontend-only improvements. Focuses exclusively on frontend presentation, UX quality, accessibility, responsive behavior, Tailwind v4 CSS-first tokens, formal visual style, and production-ready component composition. Do not use this skill for backend, database, API, DevOps, or server architecture work.
---

# Frontend Design Pro + Tailwind Skill

This skill is a frontend-only playbook for building **professional, official, polished interfaces** with Tailwind CSS latest/v4 and modern JavaScript/TypeScript frameworks.

It is optimized for:

- Official government, enterprise, SaaS, and corporate UI
- Arabic-first and multilingual RTL/LTR products
- Next.js, React, TypeScript, JSX/TSX, and plain Tailwind components
- Formal dashboards, landing pages, auth screens, forms, tables, and settings pages
- Design-system consistency, accessibility, responsiveness, and visual refinement

## Scope

Use this skill for frontend UI work only:

- Layout and composition
- Visual hierarchy
- Typography
- Color systems
- Tailwind v4 tokens
- Responsive design
- RTL/LTR UI behavior
- Component polish
- Accessibility and interaction states
- Motion and transitions
- Empty/loading/error states
- Formal design quality

Do not use this skill for backend logic, database schemas, server permissions, authentication internals, deployment, infrastructure, or API design except when the frontend shape depends on it.

## Required references

Read the relevant reference before generating or modifying code:

| Task | Reference |
|---|---|
| Tailwind v4 setup, `@theme`, CSS-first tokens | `references/tailwind-v4-system.md` |
| Formal/official visual design rules | `references/official-ui-style.md` |
| RTL/LTR, Arabic UI, logical utilities, chevrons | `references/rtl-ltr-ui.md` |
| Layout, spacing, grids, containers | `references/layout-composition.md` |
| Typography hierarchy and Arabic text | `references/typography.md` |
| Color, elevation, borders, shadows | `references/color-elevation.md` |
| Components: buttons, cards, inputs, nav, tables | `references/component-patterns.md` |
| Responsive and mobile-first rules | `references/responsive-design.md` |
| Accessibility and keyboard states | `references/accessibility.md` |
| Motion, microinteractions, loading states | `references/motion-states.md` |
| Final review checklist | `references/final-ui-audit.md` |

## Core principles

### 1. Formal first, not flashy first

Professional UI should look trustworthy, quiet, structured, and intentional. Avoid excessive gradients, neon colors, exaggerated shadows, over-rounded cards, random glassmorphism, and decorative clutter unless the product explicitly asks for a playful style.

Default aesthetic:

- Clean light background
- Clear typography
- Generous but disciplined spacing
- Subtle borders
- Soft shadows only where elevation is meaningful
- High contrast content
- Calm primary color
- Minimal motion
- Strong alignment

### 2. Tailwind v4 CSS-first design tokens

Use Tailwind latest/v4 conventions by default:

```css
@import "tailwindcss";

@theme {
  --font-sans: var(--font-geist-sans), system-ui, sans-serif;
  --font-arabic: var(--font-ibm-plex-arabic), system-ui, sans-serif;

  --color-background: oklch(0.99 0.003 250);
  --color-foreground: oklch(0.19 0.018 260);
  --color-surface: oklch(1 0 0);
  --color-muted: oklch(0.96 0.006 250);
  --color-muted-foreground: oklch(0.48 0.025 260);
  --color-border: oklch(0.90 0.010 250);
  --color-primary: oklch(0.48 0.15 255);
  --color-primary-foreground: oklch(0.99 0.003 250);
  --color-ring: oklch(0.60 0.14 255);

  --radius-xs: 0.375rem;
  --radius-sm: 0.5rem;
  --radius-md: 0.75rem;
  --radius-lg: 1rem;
  --radius-xl: 1.25rem;
}
```

Use semantic classes such as `bg-background`, `text-foreground`, `bg-surface`, `border-border`, `text-muted-foreground`, `bg-primary`, and `text-primary-foreground` instead of scattering hard-coded palettes everywhere.

### 3. RTL-ready by default

Use logical Tailwind utilities from the first draft:

- `ms-*`, `me-*` instead of `ml-*`, `mr-*`
- `ps-*`, `pe-*` instead of `pl-*`, `pr-*`
- `start-*`, `end-*` instead of `left-*`, `right-*`
- `text-start`, `text-end` instead of `text-left`, `text-right`
- `border-s`, `border-e` instead of `border-l`, `border-r`
- `rounded-s-*`, `rounded-e-*` instead of `rounded-l-*`, `rounded-r-*`
- Prefer `gap-*` over `space-x-*`

Directional SVG icons do not flip automatically. Raw `ChevronRight` and `ChevronLeft` are banned for navigation. Use semantic wrappers from `assets/directional-icons.tsx`.

### 4. Component systems over one-off styling

Prefer a small set of reusable primitives:

- `Button`
- `Input`
- `Textarea`
- `SelectTrigger`
- `Card`
- `Badge`
- `PageHeader`
- `Section`
- `DataTableShell`
- `EmptyState`
- `StatCard`

Do not generate a unique button style for every screen. Use variants and sizes.

### 5. Accessibility is part of visual quality

Every interactive element must include:

- Visible focus state
- Disabled state
- Hover/active state where appropriate
- Sufficient contrast
- Correct semantic element (`button`, `a`, `label`, `input`)
- Keyboard usability
- `aria-hidden="true"` for decorative icons

### 6. Mobile-first, responsive without breakpoint chaos

Start with mobile. Add breakpoints only when layout needs them:

- `sm` for minor spacing/typography changes
- `md` for two-column layouts
- `lg` for desktop navigation and dashboards
- `xl` for wide enterprise layouts

Avoid many breakpoints on one element unless there is a clear reason.

### 7. Use states deliberately

For every important surface, define:

- Loading state
- Empty state
- Error state
- Success state
- Disabled state
- Skeleton state if data has known structure

Never leave a blank white area while data loads.

## Frontend design workflow

When asked to create or improve UI:

1. Identify product tone: official, enterprise, SaaS, government, financial, healthcare, education, or consumer.
2. Define visual system: typography, spacing scale, radius, borders, shadows, color tokens.
3. Choose layout structure: header, sidebar, content width, section rhythm, responsive behavior.
4. Build reusable primitives first.
5. Compose the screen from primitives.
6. Add accessibility, focus, hover, disabled, loading, empty, and error states.
7. Run the final UI audit.

## Default page structure

Prefer this hierarchy:

```tsx
<main className="min-h-dvh bg-background text-foreground">
  <section className="mx-auto w-full max-w-7xl px-4 py-6 sm:px-6 lg:px-8">
    <PageHeader />
    <div className="mt-6 grid gap-6">
      {/* content */}
    </div>
  </section>
</main>
```

For RTL/LTR-safe spacing:

```tsx
<Button>
  <span>Details</span>
  <ForwardChevron className="ms-2" />
</Button>
```

Not:

```tsx
<Button>
  Details
  <ChevronRight className="ml-2" />
</Button>
```

## Formal design defaults

Use these defaults unless the user provides a brand guide:

- Background: near-white, not pure gray-heavy
- Cards: white/surface with `border border-border`
- Radius: `rounded-xl` for cards, `rounded-lg` for buttons/inputs
- Shadow: minimal, usually `shadow-sm`; prefer borders for structure
- Typography: `text-sm` body, `text-base` primary content, `text-2xl` to `text-4xl` headings
- Spacing: `gap-4`, `gap-6`, `py-6`, `py-10`, `py-16`
- Primary action: one strong button per section
- Secondary actions: outline/ghost variants
- Navigation: clear active state, not only color-based

## Forbidden by default

Avoid unless explicitly requested:

- Random gradients on every card
- Glassmorphism for official apps
- Neon colors
- Heavy drop shadows
- Excessive animation
- Tiny low-contrast text
- Inconsistent spacing
- Hard-coded physical RTL-breaking classes
- Raw chevrons for navigation
- Divs acting as buttons
- Placeholder-only labels in forms
- Unlabeled icon buttons

## Final answer requirements when generating code

When returning UI code:

1. Provide production-ready code.
2. Use Tailwind v4-friendly classes and semantic tokens.
3. Use logical RTL-safe classes.
4. Include accessibility states.
5. Explain the visual design choices briefly.
6. State any intentional exceptions.
7. Never claim the UI is professional or RTL-safe unless the final audit passes.

## Assets

Reusable templates are included:

- `assets/globals.css` — Tailwind v4 theme tokens for formal UI
- `assets/primitives.tsx` — Button, Card, Input, Badge, PageHeader, EmptyState
- `assets/directional-icons.tsx` — RTL/LTR-safe icon wrappers
- `assets/professional-page-shell.tsx` — formal app/page layout
- `assets/dashboard-template.tsx` — official dashboard example
- `assets/landing-page-template.tsx` — professional landing page example
- `assets/form-template.tsx` — accessible form pattern
