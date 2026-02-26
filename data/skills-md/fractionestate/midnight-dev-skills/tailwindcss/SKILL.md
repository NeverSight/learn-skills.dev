---
name: tailwindcss
description: >-
  Utility-first CSS styling with Tailwind CSS v4. Use when styling components, configuring themes,
  responsive design, or building design systems. Triggers on Tailwind, CSS, styling, theming, or
  responsive design questions.
---

# Tailwind CSS v4

Tailwind CSS v4 introduces CSS-first configuration, OKLCH colors, and improved performance.
This skill provides comprehensive patterns for building modern UIs.

## Core Concepts

### CSS-First Configuration

Tailwind v4 uses CSS variables and `@theme` directive instead of `tailwind.config.js`:

```css
/* app.css */
@import 'tailwindcss';

@theme {
  /* Colors using OKLCH for better perceptual uniformity */
  --color-primary-50: oklch(0.97 0.01 250);
  --color-primary-100: oklch(0.93 0.03 250);
  --color-primary-500: oklch(0.55 0.2 250);
  --color-primary-900: oklch(0.25 0.1 250);

  /* Typography */
  --font-family-sans: 'Inter', system-ui, sans-serif;
  --font-family-mono: 'JetBrains Mono', monospace;

  /* Spacing scale */
  --spacing-18: 4.5rem;
  --spacing-128: 32rem;

  /* Border radius */
  --radius-xl: 1rem;
  --radius-2xl: 1.5rem;

  /* Shadows */
  --shadow-soft: 0 2px 15px -3px oklch(0 0 0 / 0.1);

  /* Animations */
  --animate-fade-in: fade-in 0.3s ease-out;
}

@keyframes fade-in {
  from {
    opacity: 0;
    transform: translateY(-4px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
```

### New Variant Syntax

```html
<!-- Container queries -->
<div class="@container">
  <div class="@sm:grid-cols-2 @lg:grid-cols-3">
    <!-- Responsive to container, not viewport -->
  </div>
</div>

<!-- New `not-*` variants -->
<div class="not-first:mt-4">...</div>
<div class="not-last:border-b">...</div>

<!-- Group/Peer with named groups -->
<div class="group/sidebar">
  <div class="group-hover/sidebar:visible">...</div>
</div>

<!-- `has-*` for parent selection -->
<div class="has-[:checked]:bg-blue-100">
  <input type="checkbox" />
</div>
```

## Component Patterns

### Card Component

```html
<div
  class="rounded-2xl bg-white p-6 shadow-soft
            ring-1 ring-black/5
            dark:bg-gray-900 dark:ring-white/10"
>
  <h3 class="text-lg font-semibold text-gray-900 dark:text-white">Card Title</h3>
  <p class="mt-2 text-gray-600 dark:text-gray-400">Card description text</p>
</div>
```

### Button Variants

```html
<!-- Primary -->
<button
  class="rounded-lg bg-primary-500 px-4 py-2
               font-medium text-white
               hover:bg-primary-600
               focus-visible:outline-2 focus-visible:outline-offset-2
               focus-visible:outline-primary-500
               active:scale-[0.98] transition-all"
>
  Primary Button
</button>

<!-- Secondary -->
<button
  class="rounded-lg bg-gray-100 px-4 py-2
               font-medium text-gray-900
               hover:bg-gray-200
               dark:bg-gray-800 dark:text-white dark:hover:bg-gray-700"
>
  Secondary Button
</button>

<!-- Outline -->
<button
  class="rounded-lg border border-gray-300 px-4 py-2
               font-medium text-gray-700
               hover:bg-gray-50
               dark:border-gray-600 dark:text-gray-300 dark:hover:bg-gray-800"
>
  Outline Button
</button>
```

### Form Input

```html
<div>
  <label class="block text-sm font-medium text-gray-700 dark:text-gray-300"> Email </label>
  <input
    type="email"
    class="mt-1 block w-full rounded-lg border-gray-300
           shadow-sm focus:border-primary-500 focus:ring-primary-500
           dark:border-gray-600 dark:bg-gray-800 dark:text-white
           invalid:border-red-500 invalid:ring-red-500"
    placeholder="you@example.com"
  />
</div>
```

## Responsive Design

### Breakpoint Reference

- `sm`: 640px
- `md`: 768px
- `lg`: 1024px
- `xl`: 1280px
- `2xl`: 1536px

### Mobile-First Grid

```html
<div
  class="grid grid-cols-1 gap-6
            sm:grid-cols-2
            lg:grid-cols-3
            xl:grid-cols-4"
>
  <!-- Items -->
</div>
```

### Container Queries

```html
<div class="@container">
  <article class="flex flex-col @md:flex-row @md:items-center gap-4">
    <img class="w-full @md:w-48 rounded-lg" />
    <div class="flex-1">
      <h2>Title</h2>
      <p class="hidden @lg:block">Extended description</p>
    </div>
  </article>
</div>
```

## Animation Patterns

### Hover Effects

```html
<a class="group relative inline-block">
  <span class="relative z-10">Hover me</span>
  <span
    class="absolute inset-0 -z-10 scale-x-0 bg-primary-100
               transition-transform origin-left
               group-hover:scale-x-100 rounded-lg"
  />
</a>
```

### Loading States

```html
<!-- Spinner -->
<div
  class="animate-spin h-5 w-5 border-2 border-primary-500
            border-t-transparent rounded-full"
/>

<!-- Skeleton -->
<div class="animate-pulse space-y-3">
  <div class="h-4 bg-gray-200 rounded w-3/4" />
  <div class="h-4 bg-gray-200 rounded w-1/2" />
</div>

<!-- Shimmer -->
<div class="relative overflow-hidden bg-gray-200 rounded">
  <div
    class="absolute inset-0 -translate-x-full
              bg-gradient-to-r from-transparent via-white/50 to-transparent
              animate-[shimmer_2s_infinite]"
  />
</div>
```

## Dark Mode

```html
<!-- System preference -->
<html class="dark:bg-gray-950">
  <!-- With dark mode toggle -->
  <html class="dark">
    <body class="bg-white text-gray-900 dark:bg-gray-950 dark:text-gray-100"></body>
  </html>
</html>
```

```css
@theme {
  /* Semantic color tokens */
  --color-surface: white;
  --color-on-surface: oklch(0.2 0 0);
}

@media (prefers-color-scheme: dark) {
  @theme {
    --color-surface: oklch(0.15 0 0);
    --color-on-surface: oklch(0.9 0 0);
  }
}
```

## Accessibility

### Focus Styles

```html
<button
  class="focus:outline-none
               focus-visible:ring-2
               focus-visible:ring-primary-500
               focus-visible:ring-offset-2"
>
  Accessible Button
</button>
```

### Screen Reader Only

```html
<span class="sr-only">Navigation menu</span>
```

### Motion Preferences

```html
<div class="animate-bounce motion-reduce:animate-none">Respects reduced motion</div>
```

## References

- [references/theming.md](references/theming.md) - Theme customization
- [references/components.md](references/components.md) - Component library
- [references/responsive.md](references/responsive.md) - Responsive patterns

## Assets

- [assets/globals.css](assets/globals.css) - Global CSS template
