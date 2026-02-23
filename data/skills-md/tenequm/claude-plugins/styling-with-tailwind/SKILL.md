---
name: styling-with-tailwind
description: Creates UIs using Tailwind CSS utility classes and shadcn/ui patterns. Covers CSS variables with OKLCH colors, component variants with CVA, responsive design, dark mode, and Tailwind v4.2 features. Supports Radix UI and Base UI primitives, CLI 3.0, and visual styles. Use when building interfaces with Tailwind, styling shadcn/ui components, implementing themes, or working with utility-first CSS.
---

# Styling with Tailwind CSS

Build accessible UIs using Tailwind CSS v4 utility classes and shadcn/ui component patterns. **Tailwind v4 uses CSS-first configuration only - never create or modify `tailwind.config.js`/`tailwind.config.ts`.** Supports Radix UI (default) or Base UI as primitive libraries.

## Critical Rules

### No `tailwind.config.js` - CSS-First Only

Tailwind v4 configures everything in CSS. Migrate any JS/TS config:
- `theme.extend.colors` → `@theme { --color-*: ... }`
- `plugins` → `@plugin "..."` or `@utility`
- `content` → `@source "..."`
- `tailwindcss-animate` → `@import "tw-animate-css"`
- `@layer utilities` → `@utility name { ... }`

### Always Use Semantic Color Tokens

```tsx
// CORRECT - respects themes and dark mode
<div className="bg-primary text-primary-foreground">

// WRONG - breaks theming
<div className="bg-blue-500 text-white">
```

Always pair `bg-*` with `text-*-foreground`. Extend with success/warning/info in [theming.md](theming.md).

### Never Build Class Names Dynamically

```tsx
// WRONG - breaks Tailwind scanner
<div className={`bg-${color}-500`}>

// CORRECT - complete strings via lookup
const colorMap = { red: "bg-red-500", blue: "bg-blue-500" } as const
<div className={colorMap[color]}>
```

### cn() Merge Order

Defaults first, consumer `className` last (tailwind-merge last-wins):
```tsx
className={cn(buttonVariants({ variant, size }), className)}  // correct
className={cn(className, buttonVariants({ variant, size }))}  // wrong
```

### Animation Performance

```tsx
// WRONG - transition-all causes layout thrashing
<div className="transition-all duration-300">

// CORRECT - transition only what changes
<div className="transition-colors duration-200">

// CORRECT - respect reduced motion
<div className="motion-safe:animate-fade-in">
```

### `@theme` vs `@theme inline`

- `@theme` - static tokens, overridable by plugins
- `@theme inline` - references CSS variables, follows dark mode changes

```css
@theme { --color-brand: oklch(0.6 0.2 250); }          /* static */
@theme inline { --color-primary: var(--primary); }       /* dynamic */
```

See [components.md](components.md) for more pitfalls and [theming.md](theming.md) for color system reference.

## Core Patterns

### CSS Variables for Theming

shadcn/ui uses semantic CSS variables mapped to Tailwind utilities:

```css
/* globals.css - Light mode */
:root {
  --background: oklch(1 0 0);
  --foreground: oklch(0.145 0 0);
  --primary: oklch(0.205 0 0);
  --primary-foreground: oklch(0.985 0 0);
  --muted: oklch(0.97 0 0);
  --muted-foreground: oklch(0.556 0 0);
  --border: oklch(0.922 0 0);
  --radius: 0.5rem;
}

/* Dark mode */
.dark {
  --background: oklch(0.145 0 0);
  --foreground: oklch(0.985 0 0);
  --primary: oklch(0.922 0 0);
  --primary-foreground: oklch(0.205 0 0);
}

/* Tailwind v4: Map variables */
@theme inline {
  --color-background: var(--background);
  --color-foreground: var(--foreground);
  --color-primary: var(--primary);
}
```

**Usage in components:**
```tsx
// Background colors omit the "-background" suffix
<div className="bg-primary text-primary-foreground">
<div className="bg-muted text-muted-foreground">
<div className="bg-destructive text-destructive-foreground">
```

### Component Authoring Pattern

Components use plain functions with `data-slot` attributes (React 19 - no `forwardRef`):

```tsx
import { cva, type VariantProps } from "class-variance-authority"
import { cn } from "@/lib/utils"

const buttonVariants = cva(
  "inline-flex items-center justify-center gap-2 rounded-md text-sm font-medium transition-colors focus-visible:outline-none focus-visible:ring-1 disabled:pointer-events-none disabled:opacity-50",
  {
    variants: {
      variant: {
        default: "bg-primary text-primary-foreground shadow hover:bg-primary/90",
        destructive: "bg-destructive text-destructive-foreground hover:bg-destructive/90",
        outline: "border border-input bg-background hover:bg-accent",
        ghost: "hover:bg-accent hover:text-accent-foreground",
        link: "text-primary underline-offset-4 hover:underline",
      },
      size: {
        default: "h-9 px-4 py-2",
        sm: "h-8 px-3 text-xs",
        lg: "h-10 px-8",
        icon: "size-9",
      },
    },
    defaultVariants: { variant: "default", size: "default" },
  }
)

// Plain function with React.ComponentProps (not forwardRef)
function Button({
  className,
  variant,
  size,
  ...props
}: React.ComponentProps<"button"> & VariantProps<typeof buttonVariants>) {
  return (
    <button
      data-slot="button"
      className={cn(buttonVariants({ variant, size, className }))}
      {...props}
    />
  )
}

// Usage
<Button variant="outline" size="sm">Click me</Button>
```

**Icon spacing with `data-icon`:**
```tsx
<Button>
  <Spinner data-icon="inline-start" />
  Generating...
</Button>

<Button>
  <CheckIcon data-slot="icon" />
  Save Changes
</Button>
```

### Responsive Design

Mobile-first breakpoints:

```tsx
// Stack on mobile, grid on tablet+
<div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">

// Hide on mobile
<div className="hidden md:block">

// Different layouts per breakpoint
<div className="flex flex-col md:flex-row lg:gap-8">
  <aside className="w-full md:w-64">
  <main className="flex-1">
</div>

// Responsive text sizes
<h1 className="text-3xl md:text-4xl lg:text-5xl">
```

### Container Queries

First-class in Tailwind v4, no plugin needed:

```tsx
<div className="@container">
  <div className="grid gap-4 @sm:grid-cols-2 @lg:grid-cols-3">
    Responds to container width, not viewport
  </div>
</div>

// Named containers
<div className="@container/sidebar">
  <nav className="hidden @md/sidebar:block">
```

### Dark Mode

```tsx
// Use dark: prefix - but prefer semantic colors over manual dark: overrides
<div className="bg-background text-foreground">          // auto dark mode
<div className="bg-white dark:bg-black">                 // manual override

// Use next-themes for toggle: useTheme() → setTheme("dark" | "light")
// Always add suppressHydrationWarning to <html> to prevent flash
```

## Common Component Patterns

### Card

```tsx
<div className="rounded-xl border bg-card text-card-foreground shadow">
  <div className="flex flex-col space-y-1.5 p-6">
    <h3 className="font-semibold leading-none tracking-tight">Title</h3>
    <p className="text-sm text-muted-foreground">Description</p>
  </div>
  <div className="p-6 pt-0">Content</div>
  <div className="flex items-center p-6 pt-0">Footer</div>
</div>
```

### Form Field

```tsx
<div className="space-y-2">
  <label className="text-sm font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70">
    Email
  </label>
  <input
    type="email"
    className="flex h-9 w-full rounded-md border border-input bg-transparent px-3 py-1 text-sm shadow-sm transition-colors placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring disabled:cursor-not-allowed disabled:opacity-50"
  />
  <p className="text-sm text-muted-foreground">Helper text</p>
</div>
```

### Badge

```tsx
const badgeVariants = cva(
  "inline-flex items-center rounded-md border px-2.5 py-0.5 text-xs font-semibold transition-colors",
  {
    variants: {
      variant: {
        default: "border-transparent bg-primary text-primary-foreground shadow",
        secondary: "border-transparent bg-secondary text-secondary-foreground",
        destructive: "border-transparent bg-destructive text-destructive-foreground",
        outline: "text-foreground",
      },
    },
  }
)
```

## Layout Patterns

### Centered Layout

```tsx
<div className="flex min-h-screen items-center justify-center">
  <div className="w-full max-w-md space-y-8 p-8">
    {/* Content */}
  </div>
</div>
```

### Sidebar Layout

```tsx
<div className="flex h-screen">
  <aside className="w-64 border-r bg-muted/40">Sidebar</aside>
  <main className="flex-1 overflow-auto">Content</main>
</div>
```

### Dashboard Grid

```tsx
<div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
  <Card className="col-span-2">Wide card</Card>
  <Card>Regular</Card>
  <Card>Regular</Card>
  <Card className="col-span-4">Full width</Card>
</div>
```

## Accessibility Patterns

### Focus Visible

```tsx
<button className="focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2">
```

### Screen Reader Only

```tsx
<span className="sr-only">Close dialog</span>
```

### Disabled States

```tsx
<button className="disabled:cursor-not-allowed disabled:opacity-50" disabled>
```

## Tailwind v4 Features

### CSS-First Configuration

```css
@import "tailwindcss";

/* Custom utilities (replaces @layer utilities) */
@utility tab-highlight-none {
  -webkit-tap-highlight-color: transparent;
}

/* Custom variants */
@custom-variant pointer-fine (@media (pointer: fine));

/* Source control */
@source inline("{hover:,}bg-red-{50,100,200}");
@source not "./legacy";
```

### @theme Directive

```css
@theme {
  --color-primary: oklch(0.205 0 0);
  --font-sans: "Inter", system-ui;
}

/* With CSS variables (shadcn/ui pattern) */
@theme inline {
  --color-primary: var(--primary);
}
```

### Animation

```css
@import "tw-animate-css";
```

```tsx
<div className="animate-fade-in">
<div className="animate-slide-in-from-top">
```

### v4.1 Features

```tsx
// Text shadows
<h1 className="text-shadow-sm text-4xl font-bold">

// Gradient masks for fade effects
<div className="mask-linear-to-b">Fades to transparent at bottom</div>

// Pointer-aware sizing
<button className="pointer-fine:py-1 pointer-coarse:py-3">

// Form validation after user interaction
<input className="user-valid:border-success user-invalid:border-destructive" />

// Overflow wrap for long strings
<p className="overflow-wrap-anywhere">verylongwordthatneedstowrap</p>
```

### v4.2 Features (February 2026)

```tsx
// Logical block properties (RTL/writing-mode aware)
<div className="pbs-4 pbe-8 mbs-2">
<div className="border-bs-2 border-be">

// Logical sizing (replaces w-*/h-* for logical layouts)
<div className="inline-full block-screen">

// Font feature settings
<p className="font-features-['tnum','liga']">Tabular numbers</p>

// New color palettes: mauve, olive, mist, taupe
<div className="bg-mauve-100 text-olive-900">
```

**Deprecation:** `start-*`/`end-*` deprecated in favor of `inset-s-*`/`inset-e-*`.

## OKLCH Colors

All shadcn/ui colors use OKLCH format: `oklch(lightness chroma hue)`. Lightness 0-1, chroma 0-0.4 (0 = gray), hue 0-360. Base palettes: Neutral, Zinc, Slate, Stone, Gray. See [theming.md](theming.md) for complete palettes and OKLCH reference.

## Best Practices

### Prefer Semantic Colors

```tsx
// Good - uses theme
<div className="bg-background text-foreground">

// Avoid - hardcoded
<div className="bg-white text-black dark:bg-zinc-950">
```

### Group Related Utilities

```tsx
<div className="
  flex items-center justify-between
  rounded-lg border
  bg-card text-card-foreground
  p-4 shadow-sm
  hover:bg-accent
">
```

### Avoid Arbitrary Values

```tsx
// Prefer design tokens
<div className="p-4 text-sm">

// Avoid when unnecessary
<div className="p-[17px] text-[13px]">
```

## Installation & CLI

```bash
# Create new project with visual style + primitive selection
npx shadcn create

# Initialize in existing project
pnpm dlx shadcn@latest init

# Add components
pnpm dlx shadcn@latest add button card form

# Add from community registries
npx shadcn add @acme/button @internal/auth-system

# View/search registries
npx shadcn view @acme/auth-system
npx shadcn search @tweakcn -q "dark"
npx shadcn list @acme

# Add MCP server for AI integration
npx shadcn@latest mcp init

# Update existing components
pnpm dlx shadcn@latest add button --overwrite
```

### Visual Styles

`npx shadcn create` offers 5 built-in visual styles:
- **Vega** - Classic shadcn/ui look
- **Nova** - Compact, reduced padding
- **Maia** - Soft and rounded, generous spacing
- **Lyra** - Boxy and sharp, pairs with mono fonts
- **Mira** - Dense, for data-heavy interfaces

These rewrite component code (not just CSS variables) to match the selected style.

## Troubleshooting

**Colors not updating:** Check CSS variable in globals.css → verify `@theme inline` includes the mapping → clear build cache.

**Dark mode flash on load:** Add `suppressHydrationWarning` to `<html>` tag and ensure ThemeProvider wraps app with `attribute="class"`.

**Found `tailwind.config.js`:** Delete it. Run `npx @tailwindcss/upgrade` to auto-migrate to CSS-first config. All customization belongs in your CSS file via `@theme`, `@utility`, `@plugin`.

**Classes not detected:** Check `@source` directives cover your component paths. Never construct class names dynamically (see Critical Rules).

## Component Patterns

For detailed component patterns see [components.md](components.md):
- **Composition**: asChild pattern, data-slot attributes
- **Typography**: Heading scales, prose styles, inline code
- **Forms**: React Hook Form + Zod, Field component with FieldSet/FieldGroup
- **Icons**: Lucide icons with data-icon attributes
- **Inputs**: OTP, file, grouped inputs
- **Dialogs**: Modal patterns and composition
- **Data Tables**: TanStack table integration
- **Toasts**: Sonner notifications
- **Pitfalls**: cn() order, form defaultValues, dialog nesting, sticky, server/client

## Resources

See [theming.md](theming.md) for complete color system reference:
- `@theme` vs `@theme inline` (critical for dark mode)
- Status color extensions (success, warning, info)
- Z-index scale and animation tokens
- All base palettes (Neutral, Zinc, Slate, Stone, Gray)

## Summary

Key concepts:
- **v4 CSS-first only** - no `tailwind.config.js`, all config in CSS
- **Semantic colors only** - never use raw palette (`bg-blue-500`), always `bg-primary`
- **Always pair** `bg-*` with `text-*-foreground`
- **Never build class names dynamically** - use object lookup with complete strings
- **cn() order** - defaults first, consumer `className` last
- **No `transition-all`** - transition only specific properties
- **`@theme inline`** for dynamic theming, `@theme` for static tokens
- Author components as plain functions with `data-slot` (React 19)
- Apply CVA for component variants
- Use `motion-safe:` / `motion-reduce:` for animations
- Choose Radix UI or Base UI as primitive library

This skill targets Tailwind CSS v4.2 with shadcn/ui. For component-specific examples, see [components.md](components.md). For color system, see [theming.md](theming.md).
