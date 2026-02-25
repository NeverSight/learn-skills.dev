---
name: tailwind-conventions
description: Consistent Tailwind CSS patterns for React/Next.js applications. Use when styling components with Tailwind, adding responsive design, implementing dark mode, or organizing utility classes.
---

# Tailwind CSS Conventions Skill

Consistent patterns for Tailwind CSS in React/Next.js applications.

## Class Organization Order

Always organize classes in this order for readability:

```tsx
className={cn(
  // 1. Layout (position, display, flex/grid)
  "relative flex flex-col",
  // 2. Sizing (width, height, padding, margin)
  "w-full max-w-md p-4 mx-auto",
  // 3. Visual (background, border, shadow)
  "bg-white border border-gray-200 rounded-lg shadow-sm",
  // 4. Typography (font, text, color)
  "text-sm font-medium text-gray-900",
  // 5. States (hover, focus, active, disabled)
  "hover:bg-gray-50 focus:ring-2 focus:ring-blue-500",
  // 6. Responsive (sm:, md:, lg:, xl:)
  "md:flex-row md:p-6",
  // 7. Dark mode
  "dark:bg-gray-800 dark:text-white"
)}
```

## Utility Function (cn)

Use `clsx` + `tailwind-merge` for conditional classes:

```tsx
// lib/utils.ts
import { clsx, type ClassValue } from 'clsx';
import { twMerge } from 'tailwind-merge';

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

// Usage
<div className={cn(
  "base-classes",
  isActive && "active-classes",
  variant === "primary" && "primary-classes"
)} />
```

## Responsive Design

### Mobile-First Approach
```tsx
// Start with mobile, add breakpoints for larger screens
<div className="
  flex flex-col gap-2      // Mobile: stack vertically
  md:flex-row md:gap-4     // Tablet+: horizontal row
  lg:gap-6                 // Desktop: more spacing
" />
```

### Common Breakpoints
- `sm:` - 640px+ (large phones)
- `md:` - 768px+ (tablets)
- `lg:` - 1024px+ (laptops)
- `xl:` - 1280px+ (desktops)
- `2xl:` - 1536px+ (large screens)

### Responsive Typography
```tsx
<h1 className="text-2xl md:text-3xl lg:text-4xl font-bold" />
<p className="text-sm md:text-base" />
```

## Dark Mode

### Using CSS Variables (Recommended)
```css
/* globals.css */
:root {
  --background: 255 255 255;
  --foreground: 10 10 10;
}

.dark {
  --background: 10 10 10;
  --foreground: 255 255 255;
}
```

```tsx
// tailwind.config.ts
theme: {
  extend: {
    colors: {
      background: 'rgb(var(--background) / <alpha-value>)',
      foreground: 'rgb(var(--foreground) / <alpha-value>)',
    }
  }
}

// Usage - no dark: prefix needed
<div className="bg-background text-foreground" />
```

### Using dark: Prefix
```tsx
<div className="
  bg-white text-gray-900
  dark:bg-gray-900 dark:text-white
" />
```

## Component Patterns

### Button Variants
```tsx
const buttonVariants = {
  base: "inline-flex items-center justify-center rounded-md font-medium transition-colors focus:outline-none focus:ring-2 focus:ring-offset-2 disabled:opacity-50 disabled:pointer-events-none",
  variants: {
    primary: "bg-blue-600 text-white hover:bg-blue-700 focus:ring-blue-500",
    secondary: "bg-gray-100 text-gray-900 hover:bg-gray-200 focus:ring-gray-500",
    outline: "border border-gray-300 bg-transparent hover:bg-gray-50 focus:ring-gray-500",
    ghost: "bg-transparent hover:bg-gray-100 focus:ring-gray-500",
    destructive: "bg-red-600 text-white hover:bg-red-700 focus:ring-red-500",
  },
  sizes: {
    sm: "h-8 px-3 text-sm",
    md: "h-10 px-4 text-sm",
    lg: "h-12 px-6 text-base",
  }
};
```

### Card Pattern
```tsx
<div className="rounded-lg border border-gray-200 bg-white shadow-sm dark:border-gray-800 dark:bg-gray-950">
  <div className="p-6">
    <h3 className="text-lg font-semibold">Title</h3>
    <p className="text-sm text-gray-500 dark:text-gray-400">Description</p>
  </div>
</div>
```

### Input Pattern
```tsx
<input className="
  flex h-10 w-full rounded-md border border-gray-300 bg-white px-3 py-2
  text-sm placeholder:text-gray-400
  focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent
  disabled:cursor-not-allowed disabled:opacity-50
  dark:border-gray-700 dark:bg-gray-900
" />
```

## Spacing Conventions

### Consistent Spacing Scale
- `gap-1` / `p-1` = 4px (tight)
- `gap-2` / `p-2` = 8px (compact)
- `gap-4` / `p-4` = 16px (default)
- `gap-6` / `p-6` = 24px (comfortable)
- `gap-8` / `p-8` = 32px (spacious)

### Container Pattern
```tsx
<div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
  {/* Content */}
</div>
```

## Animation

### Transitions
```tsx
// Smooth color/opacity transitions
<button className="transition-colors duration-200" />

// Transform transitions (scale, translate)
<div className="transition-transform duration-200 hover:scale-105" />

// All properties
<div className="transition-all duration-300" />
```

### Built-in Animations
```tsx
<div className="animate-spin" />     // Loading spinner
<div className="animate-pulse" />    // Skeleton loading
<div className="animate-bounce" />   // Attention grabber
<div className="animate-ping" />     // Notification dot
```

## Accessibility

### Focus States
```tsx
// Always visible focus rings
<button className="
  focus:outline-none
  focus:ring-2
  focus:ring-blue-500
  focus:ring-offset-2
" />

// Focus-visible for keyboard only
<button className="
  focus-visible:outline-none
  focus-visible:ring-2
  focus-visible:ring-blue-500
" />
```

### Screen Reader
```tsx
<span className="sr-only">Loading...</span>  // Hidden visually, announced
<div aria-hidden="true" className="..." />   // Decorative, ignored
```

## Layout Patterns

### CSS Grid Layouts
```tsx
// 12-column grid
<div className="grid grid-cols-12 gap-4">
  <div className="col-span-8">Main content</div>
  <div className="col-span-4">Sidebar</div>
</div>

// Auto-fit responsive grid
<div className="grid grid-cols-[repeat(auto-fit,minmax(300px,1fr))] gap-6">
  {items.map(item => <Card key={item.id} />)}
</div>

// Dashboard grid
<div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
  <StatCard />
  <StatCard />
  <StatCard />
  <StatCard />
</div>
```

### Sidebar Layout
```tsx
// Fixed sidebar + scrollable content
<div className="flex h-screen">
  <aside className="w-64 flex-shrink-0 border-r bg-gray-50 overflow-y-auto">
    <nav className="p-4">{/* Nav items */}</nav>
  </aside>
  <main className="flex-1 overflow-y-auto p-6">
    {/* Main content */}
  </main>
</div>

// Collapsible sidebar
<div className="flex h-screen">
  <aside className={cn(
    "flex-shrink-0 border-r bg-gray-50 transition-all duration-300",
    isOpen ? "w-64" : "w-16"
  )}>
    {/* Sidebar content */}
  </aside>
  <main className="flex-1">{/* Content */}</main>
</div>
```

### Form Layouts
```tsx
// Stacked form
<form className="space-y-4 max-w-md">
  <div>
    <label className="block text-sm font-medium mb-1">Email</label>
    <input className="w-full rounded-md border px-3 py-2" />
  </div>
  <div>
    <label className="block text-sm font-medium mb-1">Password</label>
    <input className="w-full rounded-md border px-3 py-2" type="password" />
  </div>
  <button className="w-full bg-blue-600 text-white rounded-md py-2">
    Sign In
  </button>
</form>

// Inline form (search bar)
<form className="flex gap-2">
  <input className="flex-1 rounded-md border px-3 py-2" placeholder="Search..." />
  <button className="px-4 py-2 bg-blue-600 text-white rounded-md">Search</button>
</form>

// Two-column form
<form className="grid grid-cols-1 md:grid-cols-2 gap-4">
  <div>
    <label className="block text-sm font-medium mb-1">First Name</label>
    <input className="w-full rounded-md border px-3 py-2" />
  </div>
  <div>
    <label className="block text-sm font-medium mb-1">Last Name</label>
    <input className="w-full rounded-md border px-3 py-2" />
  </div>
  <div className="md:col-span-2">
    <label className="block text-sm font-medium mb-1">Email</label>
    <input className="w-full rounded-md border px-3 py-2" />
  </div>
</form>
```

### Header/Footer Layout
```tsx
// Sticky header + footer
<div className="min-h-screen flex flex-col">
  <header className="sticky top-0 z-50 border-b bg-white">
    <nav className="mx-auto max-w-7xl px-4 h-16 flex items-center justify-between">
      {/* Nav content */}
    </nav>
  </header>
  <main className="flex-1">
    {/* Page content */}
  </main>
  <footer className="border-t py-8">
    {/* Footer content */}
  </footer>
</div>
```

### Centered Content
```tsx
// Horizontally centered with max-width
<div className="mx-auto max-w-4xl px-4">{/* Content */}</div>

// Vertically and horizontally centered
<div className="min-h-screen flex items-center justify-center">
  <div className="w-full max-w-md">{/* Centered card */}</div>
</div>
```

## Anti-Patterns

- Don't use `@apply` excessively - defeats Tailwind's purpose
- Don't create overly specific custom classes
- Don't fight the spacing scale - use what's provided
- Don't inline complex conditional logic - extract to variables
- Don't forget dark mode when adding colors
- Don't use arbitrary values `[123px]` when scale values exist

---

## Version
- v1.0.0 (2025-12-05): Added YAML frontmatter, initial documented version
