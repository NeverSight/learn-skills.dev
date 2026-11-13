---
name: design-tokens-theming
description: Use when setting up a design system — color, typography, and spacing scales as CSS variables, the shadcn/ui theme, and dark mode. Covers semantic tokens, Tailwind wiring, and consistent theming across components.
---

# Design Tokens & Theming

## Overview

A SaaS UI looks "designed" when every color, space, and font size comes from a **small, named scale** — not arbitrary values sprinkled per component. Define tokens once as CSS variables, expose them through Tailwind, and let dark mode be a swap of variable values, not a rewrite of class names.

## When to use

- Starting a new app and deciding colors/spacing/typography.
- Components use raw hex codes or one-off pixel values.
- You need dark mode or multi-brand theming.

## Semantic tokens (the key idea)

Name tokens by **role**, not by hue. `--primary`, `--muted`, `--destructive` — not `--blue-500`. Roles let you re-theme without touching components. shadcn/ui uses exactly this convention:

```css
/* globals.css */
:root {
  --background: 0 0% 100%;
  --foreground: 240 10% 3.9%;
  --primary: 240 5.9% 10%;
  --primary-foreground: 0 0% 98%;
  --muted: 240 4.8% 95.9%;
  --muted-foreground: 240 3.8% 46.1%;
  --destructive: 0 84.2% 60.2%;
  --border: 240 5.9% 90%;
  --radius: 0.5rem;
}
.dark {
  --background: 240 10% 3.9%;
  --foreground: 0 0% 98%;
  --primary: 0 0% 98%;
  --primary-foreground: 240 5.9% 10%;
  --muted: 240 3.7% 15.9%;
  --muted-foreground: 240 5% 64.9%;
  --border: 240 3.7% 15.9%;
}
```

Store HSL channels (no `hsl(...)` wrapper) so Tailwind can add opacity: `hsl(var(--primary) / 0.5)`.

## Wire tokens into Tailwind

```ts
// tailwind.config.ts
export default {
  darkMode: "class",
  theme: {
    extend: {
      colors: {
        background: "hsl(var(--background))",
        foreground: "hsl(var(--foreground))",
        primary: { DEFAULT: "hsl(var(--primary))", foreground: "hsl(var(--primary-foreground))" },
        muted: { DEFAULT: "hsl(var(--muted))", foreground: "hsl(var(--muted-foreground))" },
        border: "hsl(var(--border))",
      },
      borderRadius: { lg: "var(--radius)", md: "calc(var(--radius) - 2px)" },
    },
  },
};
```

Now `bg-primary text-primary-foreground` works in both themes automatically.

## Dark mode toggle

Use `next-themes` (or a tiny class toggler) and `darkMode: "class"`. Never hard-code `dark:` colors when a semantic token already flips — `bg-background` beats `bg-white dark:bg-zinc-950`.

## Scales to standardize

- **Spacing:** stick to Tailwind's 4px scale (`p-2`, `gap-4`, `space-y-6`). Avoid `p-[13px]`.
- **Typography:** a 5–6 step type scale (`text-sm`→`text-3xl`); set `text-muted-foreground` for secondary text.
- **Radius/shadow:** one `--radius` token; 2–3 shadow steps.

## Pitfalls

- **Raw hex/px values** per component → inconsistent UI that can't be re-themed.
- **`dark:` overrides everywhere** instead of flipping tokens once.
- **Naming tokens by color** (`--blue`) instead of role (`--primary`).
- **Wrapping `hsl()` in the variable** — breaks Tailwind opacity modifiers.
- **Too many shades** — a bloated palette is harder to keep consistent than a tight one.

## Hand-off

A token layer that `responsive-layout`, `accessible-components`, and every component skill build on — change a value once, the whole app re-themes.
