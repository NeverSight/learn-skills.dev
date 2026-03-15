---
name: tailwind-css
description: This skill should be used when the user asks about "Tailwind CSS", "tailwind-variants", "tv() function", "CSS-first configuration", "Tailwind breaking changes", mentions styling with Tailwind utilities, gradient syntax, or component variants with TypeScript.
---

# Tailwind CSS v4 & tailwind-variants

## Your Role

You are an expert in Tailwind CSS v4. You understand CSS-first configuration, modern utility patterns, and type-safe
component styling with tailwind-variants.

## Reference Documentation

- **Tailwind v4 Rules & Best Practices:** [`./references/tailwind-v4-rules.md`](./references/tailwind-v4-rules.md)
  - Breaking changes, removed/renamed utilities, layout rules, typography, gradients, CSS variables, new v4 features,
    common pitfalls
- **tailwind-variants Patterns:** [`./references/tailwind-variants.md`](./references/tailwind-variants.md)
  - Component variants, slots API, composition, TypeScript integration, responsive variants

## Core Principles

- **Always use Tailwind CSS v4.1+**
- **Do not use deprecated or removed utilities** - Use the replacement
- **Never use `@apply`** - Use CSS variables, the `--spacing()` function, or framework components instead
- **Check for redundant classes** - Remove any classes that aren't necessary

## Configuration Method

Tailwind CSS v4 uses **CSS-only configuration**:

- No `tailwind.config.ts` file needed
- Define theme tokens with `@theme { }` or `@theme static { }`
- Create custom utilities with `@utility { }`
- Define custom variants with `@custom-variant { }`

```css
@import "tailwindcss";

@theme {
  --color-primary: oklch(0.72 0.11 178);
  --spacing-edge: 1.5rem;
}
```

## Critical Breaking Changes (v3 → v4)

### Renamed Utilities

| v3 (deprecated)    | v4 (use instead)   |
| ------------------ | ------------------ |
| `bg-gradient-*`    | `bg-linear-*`      |
| `shadow-sm`        | `shadow-xs`        |
| `shadow`           | `shadow-sm`        |
| `blur-sm`          | `blur-xs`          |
| `blur`             | `blur-sm`          |
| `rounded-sm`       | `rounded-xs`       |
| `rounded`          | `rounded-sm`       |
| `outline-none`     | `outline-hidden`   |
| `ring`             | `ring-3`           |
| `drop-shadow-sm`   | `drop-shadow-xs`   |
| `drop-shadow`      | `drop-shadow-sm`   |
| `backdrop-blur-sm` | `backdrop-blur-xs` |
| `backdrop-blur`    | `backdrop-blur-sm` |

### Removed Utilities

| Deprecated          | Replacement                             |
| ------------------- | --------------------------------------- |
| `bg-opacity-*`      | Use opacity modifier: `bg-black/50`     |
| `text-opacity-*`    | Use opacity modifier: `text-black/50`   |
| `border-opacity-*`  | Use opacity modifier: `border-black/50` |
| `flex-shrink-*`     | `shrink-*`                              |
| `flex-grow-*`       | `grow-*`                                |
| `overflow-ellipsis` | `text-ellipsis`                         |

## Gradient Syntax

**Use v4 gradient syntax:**

```html
<!-- Linear gradients -->
<div class="bg-linear-to-br from-violet-500 to-fuchsia-500"></div>

<!-- Radial gradients -->
<div class="bg-radial-[at_50%_75%] from-sky-200 to-indigo-900"></div>

<!-- Conic gradients -->
<div class="bg-conic-180 from-indigo-600 via-indigo-50 to-indigo-600"></div>

<!-- Deprecated syntax -->
<div class="bg-gradient-to-br ..."></div>
<!-- Wrong! -->
```

## Responsive Design (Mobile-First)

Tailwind is **mobile-first**:

- Default classes (no prefix) apply to all screen sizes
- Breakpoint prefixes (`md:`, `lg:`) apply at that breakpoint **and above**
- **Never use `sm:` for mobile** - it's redundant

```html
<!-- Correct: Mobile first, then scale up -->
<div class="text-sm md:text-base lg:text-lg">
  <div class="flex-col md:flex-row">
    <div class="px-4 md:px-6 lg:px-8">
      <!-- Hide on mobile, show on desktop -->
      <div class="hidden lg:block"></div>
    </div>
  </div>
</div>
```

## Layout Best Practices

### Always use gap for flex/grid spacing

```html
<!-- Don't use space utilities in flex/grid -->
<div class="flex space-x-4">...</div>
<!-- Wrong! -->

<!-- Use gap -->
<div class="flex gap-4">...</div>
<!-- Correct -->
```

### Use `min-h-dvh` instead of `min-h-screen`

`min-h-screen` is buggy on mobile Safari.

### Use `size-*` for equal width/height

```html
<div class="w-10 h-10">...</div>
<!-- Verbose -->
<div class="size-10">...</div>
<!-- Preferred -->
```

## Typography

**Use line-height modifiers, not `leading-*` classes:**

```html
<!-- Don't use separate leading classes -->
<p class="text-base leading-7">...</p>
<!-- Wrong! -->

<!-- Use line-height modifiers -->
<p class="text-base/7">...</p>
<!-- Correct -->
```

## CSS Variables

Tailwind v4 exposes theme values as CSS variables:

```css
.custom-element {
  background: var(--color-red-500);
  padding: var(--spacing-4);
  border-radius: var(--radius-lg);
}
```

Use `--spacing()` function for calculations:

```css
.custom-class {
  margin-top: calc(100vh - --spacing(16));
}
```

## tailwind-variants Quick Start

Type-safe component variants with automatic class conflict resolution:

```typescript
import { tv, type VariantProps } from "tailwind-variants";

const button = tv({
  base: "font-medium rounded-lg transition-colors",
  variants: {
    color: {
      primary: "bg-blue-500 text-white hover:bg-blue-600",
      secondary: "bg-gray-500 text-white hover:bg-gray-600"
    },
    size: {
      sm: "text-sm px-3 py-1.5",
      md: "text-base px-4 py-2",
      lg: "text-lg px-6 py-3"
    }
  },
  defaultVariants: {
    color: "primary",
    size: "md"
  }
});

type ButtonVariants = VariantProps<typeof button>;

// Usage
button(); // Uses defaults
button({ color: "secondary", size: "lg" });
```

**See [`./references/tailwind-variants.md`](./references/tailwind-variants.md) for:**

- Slots API for multi-part components
- Compound variants
- Component composition with `extend`
- TypeScript integration patterns

## Quick Reference

| Topic                  | Pattern                                |
| ---------------------- | -------------------------------------- |
| **Gradients**          | `bg-linear-*`, `bg-radial`, `bg-conic` |
| **Opacity**            | `bg-red-500/50` (not `bg-opacity-*`)   |
| **Line height**        | `text-base/7` (not `leading-*`)        |
| **Spacing**            | Use `gap-*` in flex/grid               |
| **Equal size**         | `size-10` (not `w-10 h-10`)            |
| **Full height**        | `min-h-dvh` (not `min-h-screen`)       |
| **Component variants** | `tv()` from tailwind-variants          |

## Common Tasks

**Creating a component with variants:**

1. Read [`./references/tailwind-variants.md`](./references/tailwind-variants.md) for patterns
2. Use `tv()` for type-safe variants
3. Extract types with `VariantProps<typeof component>`

**Debugging styles:**

1. Check [`./references/tailwind-v4-rules.md`](./references/tailwind-v4-rules.md) for breaking changes
2. Verify gradient syntax (`bg-linear-*`, not `bg-gradient-*`)
3. Check opacity syntax (`bg-red-500/50`, not `bg-opacity-*`)
