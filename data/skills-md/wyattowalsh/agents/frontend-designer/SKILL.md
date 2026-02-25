---
name: frontend-designer
description: >-
  Build production-grade frontend interfaces with modern React, Tailwind CSS,
  and shadcn/ui. Five modes: scaffold projects, create components, configure
  themes and design tokens, refactor styles, and audit codebases. Encodes best
  practices for React 19 Server Components (framework-dependent), TailwindCSS v4
  CSS-first config, shadcn/ui with Radix primitives, modern CSS (container
  queries, :has(), view transitions, scroll-driven animations), Monaspace
  typography, and Vite 6. Supersedes the frontend-design skill. Use when
  building, styling, theming, or improving any frontend project. NOT for backend
  APIs, database design, DevOps, testing frameworks, state management libraries,
  routing, or full SSR framework setup.
argument-hint: "<mode> [target]"
model: opus
license: MIT
metadata:
  author: wyattowalsh
  version: "1.0.0"
---

# Frontend Designer

Build production-grade frontend interfaces with modern React, TailwindCSS v4, and shadcn/ui. Five modes from project scaffolding to codebase audit.

**Input:** `$ARGUMENTS` — mode keyword + target, natural language UI description, or file path.

---

## Canonical Vocabulary

| Term | Meaning | NOT |
|------|---------|-----|
| **server component** | React component rendered on the server; default in Next.js/Remix App Router | "SSR component" |
| **client component** | React component with `"use client"` directive; runs in the browser | "CSR component" |
| **design token** | CSS custom property holding a design decision (color, spacing, font) | "CSS variable" (too generic) |
| **theme** | Complete set of design tokens configured in `@theme {}` | "skin", "palette" |
| **component** | Reusable UI building block (React component + styles) | "widget", "module" |
| **primitive** | Radix UI base component providing behavior without styling | "base component" |
| **registry** | shadcn/ui component distribution endpoint (local or remote) | "package", "library" |
| **container query** | CSS `@container` rule for component-scoped responsive design | "media query" (page-scoped) |
| **action** | React 19 Server Action: async function executed server-side via form | "API call", "handler" |
| **scaffold** | Create a new project with full stack configuration | "bootstrap", "setup" |
| **refactor** | Modernize existing frontend code to current best practices | "rewrite" |
| **audit** | Read-only analysis of frontend codebase quality and patterns | "review", "scan" |
| **utility class** | Tailwind CSS class mapping to a single CSS declaration | "helper class" |
| **logical property** | CSS property using start/end instead of left/right for RTL | "directional property" |
| **texture healing** | Monaspace technique for adjusting glyph spacing in monospace | — |

---

## Dispatch

Route `$ARGUMENTS` to the appropriate mode:

| `$ARGUMENTS` pattern | Mode | Start at |
|----------------------|------|----------|
| `scaffold <name>` / `init <name>` | **Scaffold** | Mode A |
| `component <name>` / `create <name>` | **Component** | Mode B |
| `theme` / `theme <path>` / `tokens` / `tokens <path>` | **Theme** | Mode C |
| `refactor <path>` / `style <path>` | **Refactor** | Mode D |
| `audit` / `audit <path>` | **Audit** | Mode E |
| Natural language UI description ("build a sidebar", "design a card") | Auto: **Component** | Mode B |
| Path to existing `.tsx`/`.jsx`/`.css` file or directory | Auto: **Refactor** | Mode D |
| Error message / "not working" / "broken" | Auto: **Audit** | Mode E |
| "backend" / "API" / "database" / "DevOps" | **Refuse** | Redirect to relevant skill |
| Empty | **Gallery** | Show modes with example invocations |

### Classification Gate

For ambiguous inputs, disambiguate before routing:

| Signal | Route to |
|--------|----------|
| Error, broken, bug, crash, "doesn't work" | Audit |
| Upgrade, modernize, migrate, update, convert | Refactor |
| Colors, dark mode, tokens, palette, branding | Theme |
| Build, create, design, add, new + UI noun | Component |
| Setup, init, start, new project | Scaffold |
| Mixed signals | Ask user which mode |

---

## Live Documentation (Optional)

Consult live docs **only when**: user reports unexpected behavior, a reference notes a pre-release API, or user asks about features not covered in bundled references.

1. **Context7** — `resolve-library-id` for "tailwindcss", "shadcn-ui", or "react", then `query-docs`.
2. **WebSearch** — `site:tailwindcss.com`, `site:ui.shadcn.com`, or `site:react.dev` for specific topics.
3. If live docs contradict bundled references, **live docs win**.

---

## Mode A: Scaffold

**Goal:** Create a new project with the full modern frontend stack.

**Load:** `references/tailwind-v4.md`, `references/vite-config.md`, `references/shadcn-patterns.md`, `references/typography.md`, `references/aesthetic-guide.md`

### A.1 Framework Selection

Ask or detect:

| Framework | When |
|-----------|------|
| **Vite + React** | SPA, no SSR needed, fastest setup |
| **Next.js App Router** | SSR/SSG, Server Components, production web apps |
| **Remix** | Full-stack, nested routing, progressive enhancement |

Default to **Vite + React** unless user specifies otherwise.

### A.2 Tailwind v4 Setup

CSS-first configuration — no `tailwind.config.js`:

```css
@import "tailwindcss";

@theme {
  --color-primary: oklch(0.6 0.2 260);
  --color-surface: oklch(0.98 0 0);
  --color-surface-dark: oklch(0.15 0 0);
  --font-display: "Your Display Font", serif;
  --font-body: "Your Body Font", sans-serif;
  --font-mono: "Monaspace Neon", monospace;
}
```

### A.3 shadcn/ui Init

```bash
npx shadcn@latest init
```

Configure `components.json` for project structure. Install core components: `button`, `input`, `card`, `dialog`, `dropdown-menu`, `toast`.

### A.4 Typography

- **Code/mono:** Monaspace Neon (or Argon, Krypton, Radon, Xenon per aesthetic)
- **Display:** Distinctive, characterful — never Inter, Roboto, Arial, system-ui
- **Body:** Clean, readable — pair with display font for contrast
- Load `references/typography.md` for @font-face setup and fluid type scale.

### A.5 Aesthetic Direction

Run the design thinking exercise (see Aesthetic Direction section below). Commit to a direction before writing any component code.

### A.6 File Structure

```
src/
  components/ui/     # shadcn/ui components (managed by CLI)
  components/        # Custom project components
  lib/               # Utilities, helpers
  hooks/             # Custom React hooks
  styles/            # Global CSS, @theme, @font-face
  app/ or pages/     # Routes (framework-dependent)
```

---

## Mode B: Component

**Goal:** Design and build a single component with production quality.

**Load:** `references/react-19.md`, `references/shadcn-patterns.md`, `references/modern-css.md`
**Conditional:** Load `references/aesthetic-guide.md` for visual/landing/hero/marketing components. Skip for utility components, forms, data tables.

### B.1 Classify Component

| Context | Default | "use client" needed? |
|---------|---------|---------------------|
| **Next.js / Remix App Router** | Server Component | Only if using hooks, event handlers, or browser APIs |
| **Vite + React** | Client Component | No — `"use client"` is unnecessary, all components are client |

For compound components (e.g., `<Tabs>`, `<Accordion>`): separate server wrapper from client interactive parts.

### B.2 Design Intent

Gather before building:
- **Purpose:** What problem does this solve? Who uses it?
- **Interactions:** Click, hover, drag, keyboard, touch?
- **Responsive behavior:** How does it adapt across container sizes?
- **Accessibility:** Required ARIA roles, keyboard patterns?

### B.3 Primitive Selection

Check if shadcn/ui provides the component or a close base. If interactive (dialog, dropdown, popover, tooltip, tabs, accordion, toggle), **use Radix UI primitives via shadcn/ui** — never build from scratch.

Load `references/shadcn-patterns.md` for CLI commands and customization patterns.

### B.4 Implement

- Style with Tailwind v4 utility classes + CSS custom properties from `@theme {}`
- Responsiveness: use `@container` queries for component-level adaptation, not media queries
- Modern CSS: `:has()` for parent-based styling, view transitions for state changes
- Keep component files focused — extract hooks and utilities to separate files

### B.5 Accessibility

Non-negotiable for every interactive component:
- Keyboard navigation (Tab, Enter, Escape, Arrow keys as appropriate)
- ARIA attributes (roles, labels, descriptions, live regions)
- Focus management (trap in modals, restore on close)
- Color contrast: WCAG AA minimum (4.5:1 text, 3:1 large text/UI)

---

## Mode C: Theme

**Goal:** Configure or reconfigure the project's design token system.

**Load:** `references/tailwind-v4.md`, `references/modern-css.md`, `references/typography.md`

### C.1 Sub-dispatch

If `$ARGUMENTS` contains `tokens`: run token extraction workflow:
1. Grep for hardcoded color values (hex, rgb, hsl) across `.tsx`, `.jsx`, `.css` files
2. Grep for hardcoded spacing/font values not using Tailwind utilities
3. Organize into three layers: **primitive** (raw values) → **semantic** (purpose-named) → **component** (scoped overrides)
4. Generate `@theme {}` block with organized custom properties

### C.2 Color System

Use `oklch` for perceptually uniform color manipulation:

```css
@theme {
  --color-primary: oklch(0.6 0.2 260);
  --color-primary-light: color-mix(in oklch, var(--color-primary) 70%, white);
  --color-primary-dark: color-mix(in oklch, var(--color-primary) 70%, black);
}
```

**contrast-color() is experimental** — Firefox 146+ and Safari TP only. Use manual fallbacks:

```css
/* Fallback for contrast-color() */
--color-on-primary: oklch(1 0 0); /* manually chosen for contrast */
```

### C.3 Dark Mode

CSS custom properties strategy with Tailwind v4:

```css
@custom-variant dark (&:where(.dark, .dark *));
```

Override tokens on the `.dark` selector:

```css
.dark {
  --color-surface: oklch(0.15 0 0);
  --color-text: oklch(0.95 0 0);
}
```

### C.4 Typography Scale

Fluid type scale with `clamp()`:

```css
@theme {
  --text-base: clamp(1rem, 0.5vw + 0.875rem, 1.125rem);
  --text-lg: clamp(1.125rem, 0.75vw + 1rem, 1.25rem);
  --text-xl: clamp(1.25rem, 1vw + 1.125rem, 1.5rem);
}
```

### C.5 RTL Preparation

Audit and convert directional properties to logical equivalents:

| Physical | Logical |
|----------|---------|
| `margin-left` | `margin-inline-start` |
| `padding-right` | `padding-inline-end` |
| `text-align: left` | `text-align: start` |
| `float: right` | `float: inline-end` |

---

## Mode D: Refactor

**Goal:** Modernize existing frontend code to current best practices.

**Load:** `references/tailwind-v4.md`, `references/react-19.md`, `references/modern-css.md`, `references/anti-patterns.md`

### D.1 Pre-scan Checklist

Before any changes, scan the project:

- [ ] Glob for `tailwind.config.js` or `tailwind.config.ts` — v3 legacy config?
- [ ] Grep for `"use client"` count across `.tsx`/`.jsx` files
- [ ] Grep for `@media` vs `@container` ratio — component responsiveness pattern?
- [ ] Grep for hardcoded hex/rgb/hsl color values outside CSS custom properties
- [ ] Grep for `font-family` declarations — are distinctive fonts used or defaults?
- [ ] Check `package.json` for React version, Tailwind version, Vite version

### D.2 Migration Patterns

| From | To | Reference |
|------|----|-----------|
| `tailwind.config.js` | CSS-first `@import "tailwindcss"` + `@theme {}` | `references/tailwind-v4.md` |
| `@media` for component sizing | `@container` queries | `references/modern-css.md` |
| Manual dropdowns/modals | Radix primitives via shadcn/ui | `references/shadcn-patterns.md` |
| Hardcoded colors | Design tokens in `@theme {}` | Mode C |
| Class components | Function components + hooks | `references/react-19.md` |
| Excessive `"use client"` | Server Components where possible (Next.js/Remix only) | `references/react-19.md` |

### D.3 Workflow

1. Present file-by-file migration plan → **user approval gate**
2. Execute changes, one file at a time
3. Verify after each file: build passes, no visual regressions
4. Re-run pre-scan checklist to confirm improvement

---

## Mode E: Audit

**Goal:** Read-only analysis of frontend codebase quality. **Never modify code.**

**Load:** `references/anti-patterns.md`

### E.1 Pre-scan

Run the same checklist as Mode D (§D.1).

### E.2 Score Dimensions

| Dimension | What to check |
|-----------|---------------|
| Stack currency | Tailwind v4 CSS-first? React 19? Latest shadcn/ui? |
| Component patterns | Server vs client split? Radix primitives? Compound components? |
| Design tokens | @theme usage? Hardcoded values? Token layers? |
| CSS modernness | Container queries? :has()? Logical properties? @supports guards? |
| Typography | Distinctive fonts? Monaspace for code? Fluid type scale? |
| Accessibility | ARIA attributes? Keyboard nav? Focus management? Contrast ratios? |

### E.3 Report Format

```markdown
## Frontend Audit Report

### Critical (must fix)
- [finding with evidence]

### Warning (should fix)
- [finding with evidence]

### Suggestion (nice to have)
- [finding with evidence]

### Strengths
- [well-implemented patterns]

### Recommended Actions
- [action] → use `/frontend-designer refactor <path>`
- [action] → use `/frontend-designer theme`
```

---

## Aesthetic Direction

Before building visual components, commit to a bold aesthetic:

**Design Thinking:**
1. **Purpose** — What problem does this interface solve? Who uses it?
2. **Tone** — Pick an extreme and own it: brutalist, maximalist, minimal, editorial, retro-futuristic, organic, luxury, playful, art deco, industrial, soft pastel
3. **Constraints** — Framework, performance budget, accessibility requirements
4. **Differentiation** — What makes this unforgettable? The one thing someone remembers?

**Anti-Slop Rules:**
- NEVER default to Inter, Roboto, Arial, or system fonts
- NEVER use purple gradients on white backgrounds
- NEVER produce cookie-cutter layouts that could come from any AI
- NEVER converge on the same aesthetic across generations — vary themes, fonts, palettes
- Match implementation complexity to vision: maximalism needs elaborate code; minimalism needs precision

Full aesthetic catalog, color theory, motion design, spatial composition: load `references/aesthetic-guide.md`.

---

## Scope Boundaries

**Supersedes:** The `frontend-design` skill. All aesthetic guidance is now here.

**NOT for:**
- Backend APIs, database design, DevOps configuration
- Testing frameworks (Jest, Vitest) — use standard testing patterns
- State management libraries (Zustand, Redux, Jotai) — choose per project needs
- Routing (React Router, TanStack Router) — framework-specific docs
- Full SSR framework setup (Next.js, Remix config beyond React 19 patterns)
- Build tooling, package management — defer to `javascript-conventions`

---

## Reference File Index

Load on demand during the relevant mode. Do NOT load all at once.

| File | Content | Load during |
|------|---------|-------------|
| `references/tailwind-v4.md` | CSS-first config, @theme, @import, Oxide engine, dark mode, container queries, v3→v4 migration | Scaffold, Theme, Refactor |
| `references/shadcn-patterns.md` | CLI commands, components.json, RTL, registries, Radix primitives, compound components, forms | Scaffold, Component |
| `references/react-19.md` | Server vs Client decision tree (framework-dependent), Actions, useActionState, use(), Suspense | Component, Refactor |
| `references/modern-css.md` | Container queries, :has(), @scope, view transitions, scroll-driven animations, anchor positioning, color-mix(), @layer | Component, Theme, Refactor |
| `references/typography.md` | Monaspace superfamily, variable fonts, @font-face, font pairing, fluid type scale with clamp() | Scaffold, Theme, Component (visual) |
| `references/aesthetic-guide.md` | Design thinking, aesthetic catalog, color theory, motion, spatial composition, anti-slop rules | Component (visual/landing/hero), Scaffold |
| `references/vite-config.md` | Vite 6 setup, plugins, CSS handling, asset optimization, env variable security | Scaffold |
| `references/anti-patterns.md` | Detection criteria and fixes for common frontend anti-patterns | Audit, Refactor |

---

## Critical Rules

1. **Never use `tailwind.config.js` in Tailwind v4** — CSS-first with `@import "tailwindcss"` and `@theme {}` exclusively
2. **Framework-aware component model** — In Next.js/Remix: minimize `"use client"`, Server Components are default. In Vite+React: `"use client"` is unnecessary, all components are client
3. **Use Radix primitives via shadcn/ui** for interactive components — never build custom dialogs, popovers, dropdowns, or tooltips from scratch
4. **Design tokens in CSS custom properties** via `@theme {}` — never hardcode colors, spacing, or font values
5. **Container queries for component responsiveness** — media queries for page layout and user preferences (`prefers-color-scheme`, `prefers-reduced-motion`, `hover`, `pointer`)
6. **`@supports` guards for progressive enhancement** — mandatory for `contrast-color()`, anchor positioning, scroll-driven animations, `@scope`
7. **Logical properties for RTL readiness** — `margin-inline-start` not `margin-left`, `padding-block` not `padding-top`
8. **Never default to Inter/Roboto/Arial/system-ui** — select distinctive fonts; Monaspace for code contexts
9. **Accessibility non-negotiable** — keyboard nav, ARIA, focus management, WCAG AA contrast (4.5:1 text, 3:1 large text)
10. **Consult live docs only when needed** — references are stable; fetch Context7/WebSearch only for unexpected behavior or uncovered features
11. **Body stays under 500 lines** — deep technical details go to reference files
12. **Audit mode is read-only** — never modify code in audit mode
