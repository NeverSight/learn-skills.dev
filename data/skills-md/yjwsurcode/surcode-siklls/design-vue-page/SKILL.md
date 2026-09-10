---
name: design-vue-page
description: >
  Generate production-ready Vue 3 Single File Components (SFC) from descriptions, design mockups, images, or URLs.
  Use this skill whenever the user wants to: build a Vue 3 page or component, convert a design/mockup/screenshot into Vue code,
  generate a UI from a description, create a Vue page with dynamic data, or scaffold a Vue component with proper reactivity.
  Trigger even if the user says things like "make me a Vue page", "convert this design to Vue", "build this UI in Vue",
  "write a Vue component for...", "I have a Figma/design/screenshot, turn it into Vue", or any variation of Vue/UI generation.
  Always use this skill for Vue 3 code generation tasks — do not rely on general knowledge alone.
---

# design-vue-page Skill

Generate high-quality, immediately runnable Vue 3 SFC code from user descriptions, design images, URLs, or detailed specs.

---

## Core Principles

1. **Static text → reactive variables** (highest priority)
2. **Pixel-faithful but adaptive layout** when design assets are provided
3. **No hardcoded lists** — always use `v-for` with `:key`
4. **Full SFC output** — `<template>` + `<script setup>` + `<style scoped>`
5. **Overflow safety** — handle text overflow and avoid unintended scroll
6. **Self-check report** — append a brief checklist after the code

---

## Step-by-Step Generation Process

### Step 1: Analyze Input

Determine what the user has provided:

| Input type | Action |
|---|---|
| Text description only | Extract UI elements, infer data structure |
| Design image/screenshot | Extract colors, spacing, font sizes, layout structure pixel-by-pixel |
| Figma / URL | Fetch and analyze the page structure and visual design |
| Combination | Use image as source of truth, description fills gaps |

If an image is provided, carefully extract:
- Color values (exact hex if possible)
- Font sizes and weights
- Padding/margin/gap values (estimate in px or rem)
- Border radius, box shadows
- Layout type (flex, grid, absolute)
- Component hierarchy

### Step 2: Define Data Model

Before writing template code, design the data layer:

```js
// All static UI text → extracted as variables
const pageTitle = ref('Dashboard Overview')
const submitLabel = ref('Submit')

// All list/repeated data → arrays of objects
const items = ref([
  { id: 1, name: 'Item A', status: 'active' },
  { id: 2, name: 'Item B', status: 'pending' },
])

// User interaction state → reactive refs
const isLoading = ref(false)
const selectedId = ref(null)
const formData = reactive({ name: '', email: '' })
```

**Rule**: No string literals in `<template>` except inside `v-for` source arrays or computed values. Every piece of visible text must trace back to a `ref`, `reactive`, `computed`, or `const`.

### Step 3: Write Template

Rules for template:
- Use semantic HTML (`<section>`, `<header>`, `<main>`, `<article>`, `<nav>`, `<footer>`)
- All repeated UI blocks → `v-for` with `:key="item.id"` (never use index as key unless truly no ID)
- Conditional blocks → `v-if` / `v-show`
- Event handlers → `@click`, `@input`, `@submit.prevent`
- Bind all text with `{{ variable }}` or `:prop="variable"`

### Step 4: Write Styles (scoped)

Rules for styles:
- Always `<style scoped>`
- Use CSS custom properties for repeated values (colors, radii, shadows)
- Layout must be **responsive by default**:
  - Prefer `flexbox` or `CSS Grid`
  - Use `max-width` + `width: 100%` on containers
  - Use `min-width: 0` on flex children to prevent overflow
  - Use relative units (`%`, `rem`, `vw/vh`) alongside `px` for fixed elements
- Text overflow safety (apply wherever text might be long):
  ```css
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  /* OR for multi-line: */
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  word-break: break-word;
  ```
- Avoid `position: fixed` or `overflow: hidden` on body/root unless intentional
- No hardcoded `height` on text containers — use `min-height` instead

### Step 5: Self-Check Report

After the code block, append a **Self-Check Report** as a comment or markdown section:

```
<!-- Self-Check Report
✅ All static text extracted to reactive variables
✅ Lists use v-for with :key (no hardcoded repeated blocks)
✅ Layout is responsive (flex/grid, relative units)
✅ Text overflow handled (ellipsis / word-break applied)
✅ No unintended scroll or fixed-position overlap
✅ Full SFC: <template> + <script setup> + <style scoped>
⚠️ [Any known limitations or assumptions made]
-->
```

---

## Output Format

Always output a single, complete, runnable `.vue` file:

````vue
<template>
  <!-- semantic, accessible HTML -->
  <!-- all text from variables -->
  <!-- lists use v-for -->
</template>

<script setup>
import { ref, reactive, computed } from 'vue'

// --- Text / Label Variables ---
const pageTitle = ref('...')

// --- Data ---
const items = ref([...])

// --- State ---
const isLoading = ref(false)
</script>

<style scoped>
/* CSS custom properties */
/* responsive layout */
/* text overflow safety */
</style>

<!-- Self-Check Report
✅ ...
-->
````

---

## Design Fidelity Rules (when image/URL provided)

- Extract and use **exact hex colors** from the design
- Reproduce **box shadows** accurately: `box-shadow: 0 2px 8px rgba(0,0,0,0.12)`
- Match **border-radius** values
- Estimate and apply **padding/gap** values (convert visual spacing to rem/px)
- Reproduce **font-weight** and **font-size** hierarchy
- If the design shows a fixed-width desktop layout, wrap it in a responsive container:
  ```css
  .page-wrapper {
    max-width: 1200px;
    width: 100%;
    margin: 0 auto;
    padding: 0 16px;
    box-sizing: border-box;
  }
  ```
- **Never** produce a pixel-fixed layout that breaks on mobile unless the user explicitly requests desktop-only

---

## Common Pitfalls to Avoid

| Pitfall | Fix |
|---|---|
| Hardcoded text in template | Move all strings to `ref()` variables |
| Repeated `<li>` or `<div>` blocks | Replace with `v-for` |
| `overflow: hidden` on wrong element | Only clip on the intended container |
| `height: 100vh` on inner scroll container | Use `min-height` or `flex: 1` |
| Missing `:key` on `v-for` | Always add `:key="item.id"` |
| Text breaking layout | Add `word-break: break-word` or `min-width: 0` to flex children |
| Long nav items causing overflow | Use `flex-wrap: wrap` or `overflow-x: auto` |

---

## Reference Files

- `references/vue3-patterns.md` — Common Vue 3 composition API patterns and idioms
- `references/tailwindcss-advanced-layouts.md` — Advanced Tailwind CSS layout techniques: CSS Grid (holy grail, auto-fill/fit, subgrid), Flexbox patterns, container queries, sticky/fixed positioning, scroll snap, aspect ratio, multi-column, fluid sizing with clamp, and print styles

- `references/responsive-css.md` — Responsive layout recipes and overflow safety patterns


Read these when you need more detailed patterns beyond what's in this file.