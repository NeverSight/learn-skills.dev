---
name: frontend-tailwind-best-practices
description: Tailwind CSS patterns and conventions for frontend apps. Use when writing component styles, layouts, or working with CSS classes.
---

# Tailwind CSS Best Practices

Styling patterns and conventions for frontend applications. Contains 10 rules covering layout utilities, affordances, color schemes, responsive design, and className handling.

## When to Apply

Reference these guidelines when:

- Writing component styles with Tailwind
- Creating layouts (stacks, grids, centering)
- Handling responsive design
- Working with color schemes
- Merging className props

## Rules Summary

### Layout Utilities (CRITICAL)

#### layout-stack-utilities - @rules/layout-stack-utilities.md

Use custom stack utilities instead of flex classes.

```tsx
// Bad
<div className="flex flex-col gap-4">
<div className="flex flex-row gap-4">

// Good
<div className="v-stack gap-4">
<div className="h-stack gap-4">
```

Available utilities:

- `v-stack` - Vertical stack (flex column)
- `h-stack` - Horizontal stack (flex row)
- `v-stack-reverse` - Reversed vertical stack
- `h-stack-reverse` - Reversed horizontal stack
- `z-stack` - Overlapping stack (grid-based, centers children on top of each other)
- `center` - Center content both horizontally and vertically
- `spacer` - Flexible spacer that fills available space
- `circle` - Perfect circle with aspect-ratio 1/1

#### layout-prefer-gaps - @rules/layout-prefer-gaps.md

Use `gap-*` on parents instead of child margins.

```tsx
// Bad
<div>
  <Item className="mb-4" />
  <Item className="mb-4" />
</div>

// Good
<div className="flex flex-col gap-4">
  <Item />
  <Item />
</div>
```

#### layout-responsive-stacks - @rules/layout-responsive-stacks.md

Switch layout direction at breakpoints.

```tsx
// Mobile: vertical, Desktop: horizontal
<div className="v-stack lg:h-stack gap-4">
  <main className="grow">...</main>
  <aside className="shrink-0 lg:w-80">...</aside>
</div>

// Mobile: horizontal, Desktop: vertical
<div className="h-stack md:v-stack">
```

### Color Schemes (CRITICAL)

#### color-schemes - @rules/color-schemes.md

Use class-based color schemes with a custom `dark` variant.

```tsx
<button className="rounded-full bg-gray-900 px-4 py-2 text-white dark:bg-gray-100 dark:text-gray-900">
  Toggle
</button>
```

### className Handling (CRITICAL)

#### classname-cn-utility - @rules/classname-cn-utility.md

Always use `cn()` to merge classNames in components.

```tsx
import { cn } from "~/lib/cn";

function Button({ className, variant }: Props) {
  return (
    <button
      className={cn(
        "base-classes",
        {
          "variant-primary": variant === "primary",
          "variant-secondary": variant === "secondary",
        },
        className, // external className always last
      )}
    />
  );
}
```

#### classname-prop-types - @rules/classname-prop-types.md

Use proper types for className props.

```tsx
import type { ClassName, ClassNameRecord } from "~/lib/cn";

// Single element
type Props = {
  className?: ClassName;
};

// Multiple elements
type Props = {
  className?: ClassNameRecord<"root" | "label" | "input">;
};

// Usage
<Input className={{ root: "w-full", label: "font-bold" }} />;
```

### Affordances (HIGH)

#### affordance-classes - @rules/affordance-classes.md

Define element-agnostic visual patterns that compose with utilities.

```tsx
<label className="ui-button" htmlFor="document-upload">
  Choose file
</label>
```

### Responsive Design (MEDIUM)

#### responsive-breakpoints - @rules/responsive-breakpoints.md

Use responsive prefixes with Tailwind defaults.

```tsx
// Standard breakpoints (min-width)
<div className="px-4 md:px-8 lg:px-12">

// Show/hide with standard breakpoints
<div className="hidden md:block">Desktop only</div>
<div className="md:hidden">Mobile only</div>
```

#### responsive-text - @rules/responsive-text.md

Scale text responsively.

```tsx
// Responsive font size
<h1 className="text-2xl md:text-3xl lg:text-4xl">

// Responsive line height with text
<p className="text-sm leading-5 md:text-base md:leading-6">
```

#### responsive-capabilities - @rules/responsive-capabilities.md

Design for input capabilities (pointer/hover) instead of device labels.

```tsx
<button className="h-10 w-10 pointer-coarse:h-12 pointer-coarse:w-12">
  <Icon />
</button>
```

## Anti-Patterns

| Don't                              | Do                     |
| ---------------------------------- | ---------------------- |
| `flex flex-col`                    | `v-stack`              |
| `flex flex-row`                    | `h-stack`              |
| `flex items-center justify-center` | `center`               |
| `bg-gray-100`                      | `bg-neutral-100`       |
| `bg-[#hex]`                        | Use design tokens      |
| `className="..."` without `cn()`   | `cn("...", className)` |
| Inline `style` for responsive      | Tailwind prefixes      |

## Key Files

| File                      | Purpose                          |
| ------------------------- | -------------------------------- |
| `tailwind.config.js`      | Config, custom utilities, colors |
| `app/styles/global.css`   | Color scheme CSS variables       |
| `app/styles/tailwind.css` | Additional utilities             |
| `app/utils/cn.ts`         | className merge utility          |
