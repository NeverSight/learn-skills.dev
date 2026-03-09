---
name: tailwind-best-practices
description:
  Stop your AI agent from generating Tailwind CSS v3 code. Rules for v4 syntax, CSS-first config,
  modern utility patterns, and common anti-patterns.
metadata:
  tags: tailwind, css, best-practices, v4
---

## When to use

Use this skill when working with Tailwind CSS code. AI agents are trained on Tailwind v3 data and
consistently generate outdated patterns - wrong config files, deprecated directives, removed
utilities, and verbose class lists. This skill enforces Tailwind CSS v4 patterns.

## Critical Rules

### 1. Use CSS @import Instead of @tailwind Directives

**Wrong (agents do this):**

```css
@tailwind base;
@tailwind components;
@tailwind utilities;
```

**Correct:**

```css
@import "tailwindcss";
```

**Why:** Tailwind v4 removed `@tailwind` directives entirely. Use a standard CSS `@import`
statement.

### 2. Use CSS-First Configuration with @theme

**Wrong (agents do this):**

```js
// tailwind.config.js
module.exports = {
  theme: {
    extend: {
      colors: {
        brand: "#3b82f6",
      },
      spacing: {
        18: "4.5rem",
      },
    },
  },
};
```

**Correct:**

```css
@import "tailwindcss";

@theme {
  --color-brand: #3b82f6;
  --spacing-18: 4.5rem;
}
```

**Why:** Tailwind v4 uses CSS-first configuration with the `@theme` directive. No
`tailwind.config.js` needed for most projects.

### 3. Use @tailwindcss/postcss Plugin

**Wrong (agents do this):**

```js
// postcss.config.mjs
export default {
  plugins: {
    "postcss-import": {},
    tailwindcss: {},
    autoprefixer: {},
  },
};
```

**Correct:**

```js
// postcss.config.mjs
export default {
  plugins: {
    "@tailwindcss/postcss": {},
  },
};
```

**Why:** In v4, `postcss-import` and `autoprefixer` are handled automatically. The plugin is
`@tailwindcss/postcss`, not `tailwindcss`.

### 4. Use Modern Opacity Syntax

**Wrong (agents do this):**

```html
<div class="bg-red-500 bg-opacity-50">
  <div class="text-blue-600 text-opacity-75"></div>
</div>
```

**Correct:**

```html
<div class="bg-red-500/50">
  <div class="text-blue-600/75"></div>
</div>
```

**Why:** The `bg-opacity-*`, `text-opacity-*`, `border-opacity-*`, and `placeholder-opacity-*`
utilities were removed in v4. Use the slash modifier syntax.

### 5. Use CSS Variables for Custom Colors

**Wrong (agents do this):**

```html
<div class="bg-[#3b82f6]"></div>
```

**Correct:**

```css
@theme {
  --color-brand: #3b82f6;
}
```

```html
<div class="bg-brand"></div>
```

**Why:** Arbitrary values (`bg-[#3b82f6]`) should be rare. Define custom colors in `@theme` so
they're reusable and consistent.

### 6. Use Container Queries with @container

**Wrong (agents do this):**

```html
<div class="md:flex-row flex-col"></div>
```

**Correct (when sizing should be based on parent, not viewport):**

```html
<div class="@container">
  <div class="flex flex-col @md:flex-row">
    <!-- Responds to container width, not viewport -->
  </div>
</div>
```

**Why:** Tailwind v4 has built-in container query support. Use `@container` on the parent and
`@sm:`, `@md:`, `@lg:` variants on children for component-level responsive design.

### 7. Use @utility for Custom Utilities

**Wrong (agents do this):**

```css
@layer utilities {
  .content-auto {
    content-visibility: auto;
  }
}
```

**Correct:**

```css
@utility content-auto {
  content-visibility: auto;
}
```

**Why:** Tailwind v4 uses `@utility` directive instead of `@layer utilities` for custom utilities.

### 8. Use Correct Important Modifier

**Wrong (agents do this):**

```js
// tailwind.config.js
module.exports = {
  important: true,
};
```

**Correct:**

```css
@import "tailwindcss" important;
```

**Why:** The `important` option moved from config to the CSS import statement in v4.

### 9. Use Renamed Utilities

**Wrong (agents do this):**

```html
<div class="shadow-sm ring-1 ring-gray-900/5">
  <div class="blur-sm">
    <div class="rounded-sm"></div>
  </div>
</div>
```

**Correct:**

```html
<div class="shadow-xs ring-1 ring-gray-900/5">
  <div class="blur-xs">
    <div class="rounded-xs"></div>
  </div>
</div>
```

**Why:** In v4, `shadow-sm` was renamed to `shadow-xs`, `shadow` to `shadow-sm`, `blur-sm` to
`blur-xs`, `rounded-sm` to `rounded-xs`, etc. The old `-sm` values now map to what was previously
the default.

### 10. Use Modern Gradient Syntax

**Wrong (agents do this):**

```html
<div class="bg-gradient-to-r from-blue-500 to-purple-500"></div>
```

**Correct:**

```html
<div class="bg-linear-to-r from-blue-500 to-purple-500"></div>
```

**Why:** Tailwind v4 renamed `bg-gradient-to-*` to `bg-linear-to-*` and added support for other
gradient types like `bg-conic-*` and `bg-radial-*`.

### 11. Use not-\* Variant for Negation

**Wrong (agents do this):**

```html
<div class="hover:bg-blue-500">
  <!-- No way to style non-hovered state specifically -->
</div>
```

**Correct:**

```html
<div class="not-hover:opacity-75 hover:opacity-100"></div>
```

**Why:** Tailwind v4 added the `not-*` variant for styling elements that do NOT match a condition.

### 12. Use @starting-style for Entry Animations

**Wrong (agents do this):**

```css
.modal {
  opacity: 0;
  transition: opacity 0.3s;
}
.modal.open {
  opacity: 1;
}
```

**Correct:**

```html
<div class="starting:opacity-0 opacity-100 transition-opacity duration-300"></div>
```

**Why:** Tailwind v4 supports `@starting-style` via the `starting:` variant for CSS-only entry
animations without JavaScript.

## Patterns

- Define all custom design tokens in `@theme` blocks
- Use `@import "tailwindcss"` as the single entry point
- Use container queries (`@container` + `@md:`) for component-level responsive design
- Use the slash modifier for opacity: `bg-blue-500/50`, `text-gray-900/75`
- Use `@utility` for custom utilities, `@variant` for custom variants
- Use `bg-linear-to-*` for gradients (not `bg-gradient-to-*`)

## Anti-Patterns

- NEVER create a `tailwind.config.js` unless you need JavaScript-based dynamic config
- NEVER use `@tailwind base/components/utilities` - use `@import "tailwindcss"`
- NEVER use `bg-opacity-*`, `text-opacity-*` - use slash modifier syntax
- NEVER use `@layer utilities` for custom utilities - use `@utility`
- NEVER use `bg-gradient-to-*` - use `bg-linear-to-*`
- NEVER use `postcss-import` or `autoprefixer` with v4 - they're built in
- NEVER use `shadow-sm` when you mean the smallest shadow - it's now `shadow-xs`
