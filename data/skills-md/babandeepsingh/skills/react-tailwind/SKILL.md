---
name: react-tailwind
description: Opinionated assistant for installing and configuring Tailwind CSS in React projects, then revamping components using Tailwind utility classes and semantic design tokens. Use when working on React (CRA, Vite, Next.js, Remix, plain SPA) and you need guidance on Tailwind setup, dependency selection and installation order, configuration, semantic theme design, and common UI recipes (forms, data tables, navigation, modals, layout).
---

## Purpose

Use this skill to turn a React project into a well-structured Tailwind-driven UI, or to refactor an existing Tailwind setup into cleaner, token-based styling and reusable patterns.

You are helping with:

- Installing and wiring Tailwind into React toolchains
- Planning and managing dependencies (Tailwind + plugins + component libraries)
- Designing a semantic token layer in `tailwind.config` (colors, spacing, typography, radii, shadows)
- Refactoring components from ad-hoc CSS to Tailwind utility classes
- Applying proven UI recipes (forms, data tables, navigation, modals, layout primitives)

Always assume the user wants practical, copy-pastable steps plus concrete component examples.

## Detect the React + Build Setup

Before giving commands or code, detect how the app is built and tailor instructions:

- **If `package.json` has `react-scripts`**: treat as Create React App.
- **If `vite` appears in devDependencies or scripts**: treat as Vite React.
- **If `next` appears**: treat as Next.js (App Router if `app/` exists, Pages Router otherwise).
- **If `react-scripts`/`vite`/`next` are absent**: treat as generic React SPA using webpack or similar; provide framework-agnostic guidance.

When uncertain, default to **Vite-like** Tailwind setup and clearly say how to adapt:

- Explain which config file to update (`tailwind.config.js`, `postcss.config.js`, entry CSS).
- Show the commands as `npm` and `yarn` variants when useful.

## Installation & Configuration Workflow

Follow this sequence whenever setting up Tailwind in a React project:

1. **Add dependencies**
   - Core: `tailwindcss postcss autoprefixer`
   - For dark mode and theming, rely on Tailwind core; only add UI libraries (e.g. `@headlessui/react`, `@heroicons/react`, Radix, etc.) if the user wants prebuilt patterns.
   - Prefer devDependencies for build-time packages.
2. **Initialize Tailwind**
   - Run the recommended init command for the detected toolchain (e.g. `npx tailwindcss init -p`).
   - Ensure both `tailwind.config.*` and `postcss.config.*` are created or updated.
3. **Configure the `content` paths**
   - Include all React source roots, e.g.:
     - `./index.html` (if Vite)
     - `./src/**/*.{js,ts,jsx,tsx}`
     - `./app/**/*.{js,ts,jsx,tsx,mdx}` and/or `./pages/**/*.{js,ts,jsx,tsx}` for Next.js.
   - Avoid overly broad globs that include `node_modules` or build outputs.
4. **Wire Tailwind into CSS**
   - Create or update a global CSS file (e.g. `src/index.css`, `src/globals.css`, `app/globals.css`) containing:
     - `@tailwind base;`
     - `@tailwind components;`
     - `@tailwind utilities;`
   - Ensure this CSS is imported once at the app entry point (`main.tsx`, `_app.tsx`, `layout.tsx`, etc.).
5. **Verify integration**
   - Instruct the user to add a simple test utility (e.g. `className="text-red-500"`) and confirm it renders correctly.
   - If it fails, inspect:
     - Missing `content` paths
     - CSS not imported
     - Conflicting CSS frameworks (e.g. Bootstrap) and advise migration or coexistence approach.

When installing additional UI libraries (e.g. Tailwind UI, Headless UI, Radix), always:

- Add them **after** Tailwind core is working.
- Check and mention peer dependencies (e.g. React version, `@floating-ui`).
- Keep the installation commands and import locations explicit.

## Tailwind Config & Semantic Tokens

Aim to design a **semantic theme layer** instead of scattering raw brand colors and spacing everywhere.

When editing `tailwind.config.*`:

- **Keep `theme.colors` and `theme.extend.colors` organized by semantic purpose**, not literal brand hex names.
- Use neutral + primary/secondary + feedback scales:

```js
// Example shape – adapt values and names to user brand
theme: {
  extend: {
    colors: {
      bg: {
        canvas: '#020617',
        subtle: '#0b1120',
        elevated: '#020617'
      },
      border: {
        subtle: '#1e293b',
        strong: '#475569',
        focus: '#38bdf8'
      },
      text: {
        primary: '#e5e7eb',
        secondary: '#9ca3af',
        muted: '#6b7280',
        danger: '#fecaca'
      },
      primary: {
        DEFAULT: '#38bdf8',
        foreground: '#0f172a',
        soft: '#0ea5e9'
      },
      danger: {
        DEFAULT: '#ef4444',
        subtle: '#fee2e2'
      },
      success: {
        DEFAULT: '#22c55e',
        subtle: '#dcfce7'
      }
    },
    borderRadius: {
      sm: '0.375rem',
      md: '0.5rem',
      lg: '0.75rem',
      xl: '1rem'
    },
    boxShadow: {
      soft: '0 1px 2px 0 rgba(15,23,42,0.35)',
      raised: '0 10px 30px rgba(15,23,42,0.6)'
    }
  }
}
```

Guidelines:

- Prefer **purpose-based names** (`bg.canvas`, `text.secondary`, `border.focus`) over raw brand names.
- Map existing CSS variables (if present) into Tailwind theme keys to preserve behavior.
- For dark/light modes:
  - Prefer Tailwind `dark` class strategy (`darkMode: 'class'`).
  - Teach the user to toggle a `dark` class on `html`/`body`/root using React state or a small theme hook.

Whenever you introduce or change tokens, also show **one or two component snippets** that use them so the user sees concrete usage.

## Component Revamp Workflow

When the user wants to "revamp" or "modernize" components with Tailwind:

1. **Audit the component**
   - Ask for or inspect the existing JSX + CSS.
   - Identify:
     - Layout primitives (stack, grid, sidebar, card)
     - Typography hierarchy (headings, labels, body text)
     - Interactive elements (buttons, links, inputs)
2. **Design the Tailwind structure**
   - Replace layout CSS with Tailwind primitives (`flex`, `grid`, `gap`, `space-y-*`, `max-w-*`, `overflow-*`).
   - Map CSS variables or design tokens to Tailwind theme keys.
   - Encapsulate repeated patterns in small reusable components (e.g. `Button`, `Card`, `Input`, `Modal`).
3. **Refactor incrementally**
   - Start with **one component at a time** (e.g. a single form, a card list).
   - Keep behavior and props stable; change only the JSX structure and classes.
4. **Extract shared building blocks**
   - Once you see repeated class combinations, suggest:
     - React components with `className` extension hooks.
     - Utility functions for composing class names (e.g. `clsx`, `cva`).
5. **Review accessibility**
   - Ensure roles, aria attributes, and focus rings are preserved or improved.
   - Demonstrate focus styles using semantic border/focus tokens.

Always provide **before/after** snippets when possible: old JSX/CSS vs. Tailwind-powered JSX.

## Common UI Recipes

Use these patterns as starting points and adapt tokens to the user’s theme. Prefer semantic Tailwind tokens (e.g. `bg-bg-elevated`, `text-text-secondary`) if available; otherwise fall back to typical defaults.

### Forms

Goals: consistent spacing, clear label/input alignment, accessible focus styles, helpful error text.

Form pattern:

- Wrap each field in a vertical stack with small `gap`.
- Use labels with `htmlFor`, consistent typography.
- Use inputs with:
  - Full-width `w-full`
  - Semantic background, border, and focus tokens
  - Rounded corners and subtle shadows where appropriate

When refactoring, ensure:

- Error states use semantic danger tokens (e.g. `border-danger`, `text-danger`).
- Disabled states lower opacity and remove hover styles.

### Data Tables

Goals: readable rows, good density control, clear sorting/selection affordances.

Table pattern:

- Use a wrapper for scroll: `overflow-x-auto` with responsive padding.
- Table base: `min-w-full divide-y divide-border-subtle`.
- Headers:
  - Background with subtle contrast (e.g. `bg-bg-subtle`).
  - Uppercase or small-caps with tracking if desired.
  - Use `text-text-secondary` for less visual noise.
- Rows:
  - `divide-y divide-border-subtle`.
  - Hover: `hover:bg-bg-subtle/60`.
  - Selected: `bg-primary/5 border-l-2 border-primary`.

For actions within rows, recommend:

- Inline icon buttons with accessible labels.
- Clear spacing (`space-x-2`) and hit area (`p-1.5`–`p-2`).

### Navigation (Top bar + Sidebar)

Navigation layout:

- Use a shell layout with:
  - Top bar: `flex items-center justify-between h-14 px-4 border-b border-border-subtle bg-bg-elevated`.
  - Sidebar (optional): `hidden md:flex md:w-64 md:flex-col border-r border-border-subtle bg-bg-subtle`.
  - Main: `flex-1 overflow-y-auto p-4 md:p-6`.

Nav items:

- Base: `flex items-center gap-2 rounded-md px-2.5 py-2 text-sm font-medium`.
- Default text: `text-text-secondary`.
- Active: `bg-bg-elevated text-text-primary`.
- Hover: `hover:bg-bg-elevated/70 hover:text-text-primary`.

Prefer grouping navigation into arrays of config objects (label, icon, href, active) and mapping to JSX; this makes it easier to restyle later.

### Modals / Dialogs

For accessible modals:

- Recommend a headless or primitive-based library (e.g. `@headlessui/react` or Radix Dialog) when possible.
- If implemented manually, insist on:
  - ARIA roles (`role="dialog"`, `aria-modal="true"`).
  - Focus trapping and escape-key handling.
  - Background overlay with opacity.

Styling:

- Overlay: `fixed inset-0 bg-black/60 backdrop-blur-sm`.
- Container: `fixed inset-0 flex items-center justify-center px-4`.
- Panel:
  - `w-full max-w-lg rounded-lg bg-bg-elevated shadow-raised p-6`
  - Use tokenized colors and spacing.

Buttons inside modals should reuse the app’s primary/secondary button components rather than ad-hoc classes.

## Dependency Management & Installation Order

When the user asks to "set up Tailwind" or "add Tailwind components", explicitly lay out the order of operations:

1. **Ensure React + bundler dependencies are already installed** (React, ReactDOM, framework-specific tooling).
2. **Install Tailwind + PostCSS + Autoprefixer** as devDependencies.
3. **Initialize Tailwind config + PostCSS config**.
4. **Wire Tailwind CSS into the app entry point** and verify.
5. **Introduce a component library or headless primitives**, if requested:
   - Install library.
   - Import styles if needed (some libraries include base CSS).
   - Show how to integrate with Tailwind classes and the theme tokens.
6. **Refactor existing components incrementally**, starting with:
   - Buttons and typography.
   - Forms.
   - Layout shells (nav, sidebar, main content).
   - Data-heavy views (tables, lists, detail panels).

Always keep the `package.json` in sync with your recommendations (devDependencies vs dependencies) and highlight any required Node or React versions when relevant.

## Common Pitfalls & How to Handle Them

When debugging Tailwind + React setups, check for these issues:

- **Classes not applying**
  - `content` globs not matching file paths or extensions.
  - CSS file with `@tailwind` directives not imported anywhere.
  - Build cache; suggest restarting dev server or clearing cache.
- **Production build is unstyled or partially styled**
  - Wrong `content` paths causing aggressive purging.
  - Classes constructed dynamically in ways Purge cannot detect; recommend:
    - Using canonical class names in code.
    - Extracting variant class maps instead of building full strings from arbitrary input.
- **Conflicts with other frameworks**
  - Legacy global CSS (e.g. Bootstrap) overriding Tailwind; suggest:
    - Removing conflicting imports over time.
    - Namespacing legacy CSS where possible.
- **Inconsistent design**
  - Repeated ad-hoc colors/spacings; suggest:
    - Consolidating into Tailwind semantic tokens.
    - Refactoring repeated class groups into shared components.

When you fix or diagnose an issue, give a short checklist the user can re-run next time (e.g. "verify config paths, CSS import, and dev server restart").

