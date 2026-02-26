---
name: tailwind-css
description: Set up and use Tailwind CSS v4 only with Next.js (App Router), Vite, or CLI; no tailwind.config.js—theme via @theme in CSS. Use when styling with Tailwind, configuring Tailwind, installing Tailwind, utility classes, @theme, @layer, @utility, or when the user mentions Tailwind CSS or Tailwind v4.
---

# Tailwind CSS (v4)

## Overview

Tailwind CSS is a utility-first CSS framework. Style by combining single-purpose classes in markup.

**We use Tailwind v4 only.** There is no `tailwind.config.js`, `tailwind.config.ts`, or `tailwind.config.mjs`. Configuration is done in CSS via `@import "tailwindcss"` and the `@theme` directive, plus the Vite or PostCSS plugin.

- **Entry**: One main CSS file with `@import "tailwindcss";`
- **Build**: `@tailwindcss/vite` (Vite) or `@tailwindcss/postcss` (Next.js)
- **Theme**: `@theme { ... }` in that same CSS file (or imported CSS). No JS config.

**Core principle**: Prefer utility classes in markup; extend with `@theme` and custom CSS when needed. Never suggest or create `tailwind.config.*` or `content`/`theme` in a config file.

---

## Installation

### Next.js (App Router, 15+)

1. Create project (if needed): `npx create-next-app@latest my-project --typescript --eslint --app`
2. Install: `npm install tailwindcss @tailwindcss/postcss postcss`
3. Create `postcss.config.mjs` in project root:

```js
const config = {
  plugins: {
    "@tailwindcss/postcss": {},
  },
};
export default config;
```

4. In `./app/globals.css`:

```css
@import "tailwindcss";
```

5. Run: `npm run dev`

Use `className` in React/TSX (e.g. in `app/page.tsx`):

```tsx
export default function Home() {
  return (
    <h1 className="text-3xl font-bold underline">
      Hello world!
    </h1>
  );
}
```

Ensure `app/globals.css` is imported in `app/layout.tsx` (Create Next App does this by default).

### Vite (React, Vue, Qwik, etc.)

1. Install: `npm install tailwindcss @tailwindcss/vite`
2. In `vite.config.ts`:

```ts
import tailwindcss from '@tailwindcss/vite'

export default defineConfig({
  plugins: [tailwindcss(), /* ... */],
})
```

3. Main CSS (e.g. `src/index.css`): `@import "tailwindcss";`

### Tailwind CLI (standalone)

1. Install: `npm install tailwindcss @tailwindcss/cli`
2. Main CSS: `@import "tailwindcss";`
3. Build: `npx @tailwindcss/cli -i ./src/input.css -o ./src/output.css --watch`

---

## Using Tailwind

- Use **utility classes** in markup: `className` in React/Next.js, `class` in Qwik/Vue.
- Prefer design tokens (theme) over arbitrary values when possible.
- Group related utilities for readability (layout → spacing → typography → colors → effects).

Examples: `text-3xl font-bold underline`, `flex items-center gap-4`, `p-6 rounded-xl bg-white shadow-lg`, `max-w-sm mx-auto`.

---

## Theme: @theme only (no config file)

**Only in CSS.** Use `@theme` in the same file as `@import "tailwindcss"` (or in CSS imported by it).

### Extending the default theme

```css
@import "tailwindcss";

@theme {
  --font-display: "Satoshi", "sans-serif";
  --breakpoint-3xl: 120rem;
  --color-avocado-500: oklch(0.84 0.18 117.33);
  --ease-fluid: cubic-bezier(0.3, 0, 0, 1);
}
```

Use: `font-display`, `3xl:`, `bg-avocado-500`, `ease-fluid`.

### Overriding defaults

Redefine a variable inside `@theme` to override:

```css
@theme {
  --breakpoint-sm: 30rem;
}
```

### Theme variable namespaces (quick reference)

| Namespace       | Use for                         | Examples                    |
|----------------|----------------------------------|-----------------------------|
| `--color-*`    | Colors                           | `bg-*, text-*, border-*`    |
| `--font-*`     | Font family                      | `font-sans`, `font-mono`     |
| `--text-*`     | Font size                        | `text-xl`, `text-base`      |
| `--font-weight-*` | Font weight                  | `font-bold`                 |
| `--breakpoint-*`  | Responsive variants           | `sm:`, `md:`, `lg:`         |
| `--spacing-*`  | Spacing/sizing                    | `p-4`, `gap-2`, `m-6`       |
| `--radius-*`   | Border radius                    | `rounded-lg`                |
| `--shadow-*`   | Box shadow                       | `shadow-md`                  |
| `--ease-*`     | Transition timing                | `ease-out`                  |
| `--animate-*`  | Animations                       | `animate-spin`               |

### Referencing other variables

Use `@theme inline` when a token should reference another variable:

```css
@theme inline {
  --font-sans: var(--font-inter);
}
```

### Custom keyframes

Define keyframes inside `@theme` so they are used by `--animate-*`:

```css
@theme {
  --animate-fade-in-scale: fade-in-scale 0.3s ease-out;
  @keyframes fade-in-scale {
    0% { opacity: 0; transform: scale(0.95); }
    100% { opacity: 1; transform: scale(1); }
  }
}
```

For more theme options (overriding full namespaces, custom theme, sharing across projects), see [reference.md](reference.md).

---

## Custom styles

### Plain CSS

Add any custom CSS in the same file as `@import "tailwindcss"` or in imported files:

```css
@import "tailwindcss";

.my-custom-style {
  /* ... */
}
```

### Base layer

Use `@layer base` for element defaults:

```css
@layer base {
  h1 { font-size: var(--text-2xl); }
  h2 { font-size: var(--text-xl); }
}
```

### Component layer

Use `@layer components` for reusable component-like classes (override with utilities when needed):

```css
@layer components {
  .card {
    background-color: var(--color-white);
    border-radius: var(--radius-lg);
    padding: var(--spacing-6);
    box-shadow: var(--shadow-xl);
  }
}
```

### Custom utilities: @utility

Simple utility:

```css
@utility content-auto {
  content-visibility: auto;
}
```

Complex (e.g. scrollbar hidden):

```css
@utility scrollbar-hidden {
  &::-webkit-scrollbar {
    display: none;
  }
}
```

### Custom variants: @variant

Use `@variant` inside custom CSS:

```css
.my-element {
  background: white;
  @variant dark {
    background: black;
  }
}
```

Or register a named variant with `@custom-variant`:

```css
@custom-variant theme-midnight (&:where([data-theme="midnight"] *));
```

Then use: `theme-midnight:bg-black`.

---

## Arbitrary values and properties

- **Arbitrary value**: `top-[117px]`, `bg-[#bada55]`, `text-[22px]`, `lg:top-[344px]`.
- **CSS variable in arbitrary value**: `fill-(--my-brand-color)` (shorthand for `fill-[var(--my-brand-color)]`).
- **Arbitrary property**: `[mask-type:luminance]`, `[--scroll-offset:56px]`.
- **Whitespace in value**: Use underscore `_` for space, e.g. `grid-cols-[1fr_500px_2fr]`.
- **Ambiguity**: Use a type hint: `text-(length:--my-var)` vs `text-(color:--my-var)`.

---

## Compatibility

- **Browsers**: Tailwind v4 targets modern browsers (Chrome 111+, Safari 16.4+, Firefox 128+). Some utilities use newer features; avoid those if you need older support.
- **Preprocessors**: Do not use Tailwind with Sass/Less/Stylus in the same pipeline; use Tailwind as the main styling layer.

---

## Quick reference

| Task          | Action |
|---------------|--------|
| Entry         | One CSS file with `@import "tailwindcss";` |
| Next.js       | `@tailwindcss/postcss` in `postcss.config.mjs`, no Tailwind config file |
| Vite          | `tailwindcss()` from `@tailwindcss/vite` |
| Theme         | `@theme { ... }` in CSS only |
| Base styles   | `@layer base { ... }` |
| Components    | `@layer components { ... }` |
| Custom util   | `@utility name { ... }` |
| Custom variant| `@custom-variant name (selector);` |

---

## Common mistakes

- **Wrong attribute**: React/Next use `className`; Qwik/Vue use `class`.
- **Missing import**: The file with `@import "tailwindcss"` must be the one loaded by the app (e.g. in root layout).
- **Config file**: Do not create or suggest `tailwind.config.js`, `tailwind.config.ts`, or any `tailwind.config.*`. Do not suggest `content: []`, `theme: {}`, or plugins in a JS config. Tailwind v4 uses only CSS (`@import "tailwindcss"` + `@theme`) and the Vite/PostCSS plugin.

---

## Additional resources

- [reference.md](reference.md) — Theme options, official doc links, default theme summary.
- Official: [Tailwind CSS v4 Docs](https://tailwindcss.com/docs) — Installation, theme, adding custom styles, compatibility.
