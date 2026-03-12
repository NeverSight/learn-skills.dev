---
name: blueprint-ui
description: Build landing pages and web UIs using a dark blueprint/wireframe aesthetic with sharp edges, connected sections, dashed outlines, measurement annotations, and technical typography. Use when creating marketing sites, landing pages, or product pages.
---

# Blueprint / Wireframe UI Design System

Build web pages using a technical blueprint aesthetic: dark background, sharp edges, connected sections with shared borders, dashed outlines, measurement annotations, and monospace labels.

## Core Principles

1. **No rounded corners.** Everything is sharp-edged. Never use `rounded-*` classes.
2. **Connected sections.** Sections share borders and flow into each other via `border-x border-border` on a shared max-width container. No floating cards with gaps.
3. **Dashed outlines** for content boundaries, illustration placeholders, and measurement guides.
4. **Section labels** — small monospace uppercase labels positioned over section borders (e.g., "Hero", "Features", "CLI").
5. **Measurement annotations** — thin dashed lines with monospace dimension labels (e.g., "48px", "grid: 3 cols", "max-width: 672px") placed between sections or elements.
6. **Dot grid background** on the page body.
7. **Numbered elements** — cards and list items get small monospace counters like "01", "02", "03".

## Color Palette

```
Background:     #0a0a0a
Surface:        #111111
Border:         #1e1e1e
Border bright:  #333333
Text primary:   #e8e8e8
Text muted:     #666666
Text dim:       #525252  (labels, annotations, counters)
Accent:         #f59e0b  (amber — CTAs, highlights, output text)
Accent alt:     #ea580c  (orange — hover states, secondary accent)
```

## Typography

- **Body**: Inter (sans-serif)
- **Code / labels / annotations**: JetBrains Mono (monospace)
- **Section headers**: Two-tone — first line white, second line muted
- **Section labels**: 10px monospace, uppercase, letter-spacing 0.1em, `text-dim`, positioned over borders with background color punch-through
- **Measurement text**: 9px monospace, `text-dim`

## Component Patterns

### Section container
Sections are wrapped in `border-x border-border` on the shared `max-w-6xl` container. Internal content uses `border-b border-dashed border-border` as a bottom separator. Each section has a `.section-label` positioned at the top.

```html
<section class="relative border-x border-border">
  <span class="section-label">Features</span>
  <div class="border-b border-dashed border-border px-8 pt-16 pb-16 md:px-16 md:pt-24 md:pb-24">
    <!-- content -->
  </div>
</section>
```

### Feature cards (connected grid)
Cards share borders in a grid. No gaps, no rounded corners. Each card gets a monospace counter.

```html
<div class="grid border border-border md:grid-cols-3">
  <div class="border-b border-border p-6 md:border-b-0 md:border-r md:p-8">
    <div class="mb-3 font-mono text-[10px] uppercase tracking-widest text-dim">01</div>
    <h3>Title</h3>
    <p class="text-muted">Description</p>
  </div>
  <!-- more cards... last card has no border-r -->
</div>
```

### Terminal block
Sharp corners, square traffic-light dots with borders, monospace content.

```html
<div class="border border-border">
  <div class="flex items-center gap-2 border-b border-border px-4 py-2.5">
    <span class="h-2.5 w-2.5 border border-[#ff5f57] bg-[#ff5f57]/20"></span>
    <span class="h-2.5 w-2.5 border border-[#febc2e] bg-[#febc2e]/20"></span>
    <span class="h-2.5 w-2.5 border border-[#28c840] bg-[#28c840]/20"></span>
    <span class="ml-2 font-mono text-[10px] text-dim">terminal</span>
  </div>
  <div class="p-5 font-mono text-xs leading-[1.8] md:p-6 md:text-sm">
    <p><span class="text-dim">$</span> <span class="text-text">command here</span></p>
    <p class="text-amber">output here</p>
  </div>
</div>
```

### Buttons
Sharp-edged, monospace uppercase text, border-based. Two variants:

```html
<!-- Primary (filled) -->
<a class="border border-amber bg-amber px-5 py-2 font-mono text-xs font-medium text-bg hover:bg-transparent hover:text-amber">
  GET STARTED
</a>

<!-- Secondary (outline) -->
<a class="border border-border px-5 py-2 font-mono text-xs font-medium text-muted hover:border-text hover:text-text">
  GITHUB
</a>
```

### Measurement annotation
Dashed lines with a centered dimension label between elements.

```html
<div class="flex items-center gap-2">
  <div class="h-px flex-1 border-t border-dashed border-dim"></div>
  <span class="measure">48px</span>
  <div class="h-px flex-1 border-t border-dashed border-dim"></div>
</div>
```

### Illustration placeholder
Dashed border box with monospace dimension label.

```html
<div class="flex h-48 items-center justify-center border border-dashed border-border">
  <span class="font-mono text-[10px] text-dim">[ 400 x 300 ]</span>
</div>
```

### Carousel (horizontal scroll)
Connected cards with shared borders in a scrollable container. Square arrow buttons.

```html
<div class="carousel flex gap-0 overflow-x-auto scroll-smooth border border-border">
  <div class="flex min-w-[300px] flex-col border-r border-border">
    <!-- card content -->
  </div>
  <!-- more cards... -->
</div>
```

### Nav
Fixed, sharp, blurred backdrop, monospace wordmark.

```html
<nav class="fixed top-0 z-50 w-full border-b border-border bg-bg/90 backdrop-blur-md">
  <div class="mx-auto flex max-w-6xl items-center justify-between px-6 py-4">
    <a class="font-mono text-lg font-semibold">brand</a>
    <!-- links + CTA -->
  </div>
</nav>
```

### Footer
Single border box at the bottom, monospace text, minimal.

## Required CSS

```css
@import "tailwindcss";

@theme {
  --color-bg: #0a0a0a;
  --color-surface: #111111;
  --color-border: #1e1e1e;
  --color-border-bright: #333333;
  --color-text: #e8e8e8;
  --color-muted: #666666;
  --color-dim: #525252;
  --color-amber: #f59e0b;
  --color-orange: #ea580c;
  --font-sans: "Inter", ui-sans-serif, system-ui, sans-serif;
  --font-mono: "JetBrains Mono", ui-monospace, monospace;
}

html {
  background-color: var(--color-bg);
  color: var(--color-text);
  font-family: var(--font-sans);
}

.dot-grid {
  background-image: radial-gradient(circle, var(--color-border) 1px, transparent 1px);
  background-size: 24px 24px;
}

.section-label {
  font-family: var(--font-mono);
  font-size: 10px;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  color: var(--color-dim);
  position: absolute;
  top: -8px;
  left: 12px;
  background: var(--color-bg);
  padding: 0 6px;
}

.measure {
  font-family: var(--font-mono);
  font-size: 9px;
  color: var(--color-dim);
  letter-spacing: 0.05em;
}

.carousel::-webkit-scrollbar { display: none; }
.carousel { -ms-overflow-style: none; scrollbar-width: none; }
```

## Tech Stack

- **Astro** (static output) with `@tailwindcss/vite` plugin
- **Tailwind CSS v4** — theme defined in CSS `@theme`, no `tailwind.config.js`
- **Google Fonts**: Inter + JetBrains Mono
- **No JS frameworks**. Pure Astro components. Vanilla JS only for interactions like carousels.
- **bun** as package manager

## When building a page

1. Wrap everything in a `.dot-grid` container
2. Use a single `max-w-6xl` centered main with `border-x border-border` on each section
3. Add `.section-label` to every section
4. Use connected grids (shared borders, no gaps) for cards
5. Add 1-2 measurement annotations per page for the blueprint feel
6. Keep all corners sharp — zero border-radius
7. Use the two-tone heading pattern for section headers
8. Terminal blocks use square traffic-light dots
9. All small labels and counters in monospace
