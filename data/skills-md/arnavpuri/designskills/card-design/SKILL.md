---
name: card-design
description: >
  Individual card components and card grids: anatomy, grid/masonry/carousel layouts, hover
  effects, and ready patterns for product, feature, testimonial, blog, expandable, and
  flippable cards plus skeleton loaders. Use when the user asks to "design a card", "build
  card layout", "create a product card", "make a card grid", "design a testimonial card",
  "blog post card", "feature card", "pricing card", or any card-based UI component. For the
  full page section around the cards use landing-page-design; for KPI/stat tiles use
  dashboard-design; for general components use ui-design.
license: MIT
---

# Card Design

## Before You Start: Load Design Context

1. **Read `.agents/design-context.md`** (written by the `design-context` skill). If it is missing, look for tokens in `tailwind.config.*` or `:root` CSS variables. If nothing exists, use the defaults (Primary `#2563EB`, Secondary `#7C3AED`, Accent `#F59E0B`, Tailwind gray neutrals, Inter for headings and body, Minimal style) and **tell the user defaults were used** — suggest running `design-context`.
2. **Map tokens to CSS variables once**, then use only the variables: `--color-primary`, `--color-primary-light`, `--color-primary-dark`, `--color-secondary`, `--color-accent`, `--color-neutral-50`…`--color-neutral-900`, `--color-success`/`-warning`/`-error`, `--font-heading`, `--font-body`, `--font-mono`, `--radius`, and the 4px-base spacing scale.
3. **Tailwind:** expose the same variables (v3 `theme.extend`, v4 `@theme`) as `primary`, `primary-light`, `primary-dark`, `secondary`, `accent`, `neutral-*`, `font-heading`, `font-body`. The `indigo-*` / `gray-*` classes in the examples below are placeholders for these tokens.
4. **Figma:** if the user gives a Figma URL, pull it with the Figma MCP (`get_design_context`, `get_screenshot`) and match it; it overrides the context file for that design.
5. Use the context's `--radius` and shadow style for every card; ask what content goes in the card and what single action it leads to.

---

## 1. Card Anatomy

Every card has up to five zones. Not all are required.

```
+---------------------------+
|        [Media]            |  Image, video, or illustration
+---------------------------+
|  [Header]                 |  Title, subtitle, avatar, badge
|                           |
|  [Body]                   |  Description, content, data
|                           |
|  [Actions]                |  Buttons, links, icons
|  [Metadata]               |  Date, author, tags, stats
+---------------------------+
```

### Base Card Style
```css
.card {
  background: var(--color-surface, #fff);
  border-radius: var(--radius, 1rem);
  border: 1px solid var(--color-neutral-200, oklch(92% 0 0));
  overflow: hidden;
  transition: box-shadow 200ms ease, transform 200ms ease, border-color 200ms ease;
}
```

### Tailwind Base Card
```html
<div class="bg-white rounded-2xl border border-gray-200 overflow-hidden
  shadow-sm hover:shadow-md transition-shadow">
  <!-- content -->
</div>
```

---

## 2. Card Grid Layouts

### Uniform Grid
```html
<div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
  <!-- Equal-sized cards -->
</div>
```

### Featured + Grid
```html
<div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
  <!-- Featured card spans 2 columns -->
  <div class="lg:col-span-2 lg:row-span-2">
    <!-- Large featured card -->
  </div>
  <!-- Smaller cards fill remaining space -->
  <div><!-- card --></div>
  <div><!-- card --></div>
</div>
```

### Masonry Layout (CSS)
```css
.masonry {
  columns: 3;
  column-gap: 1.5rem;
}
.masonry > * {
  break-inside: avoid;
  margin-bottom: 1.5rem;
}

/* Responsive */
@media (max-width: 1024px) { .masonry { columns: 2; } }
@media (max-width: 640px) { .masonry { columns: 1; } }
```

### Horizontal Scroll (Mobile)
```html
<!-- Focusable, labelled region so keyboard users can scroll it.
     (`scrollbar-hide` is not core Tailwind — it needs the tailwind-scrollbar-hide plugin; keep the scrollbar if unsure) -->
<div class="flex gap-4 overflow-x-auto snap-x snap-mandatory scroll-px-4 pb-4 -mx-4 px-4"
  tabindex="0" role="region" aria-label="Featured products">
  <div class="snap-start shrink-0 w-72"><!-- card --></div>
  <div class="snap-start shrink-0 w-72"><!-- card --></div>
  <div class="snap-start shrink-0 w-72"><!-- card --></div>
</div>
```

---

## 3. Hover Effects

### Lift Effect (Subtle, Professional)
```html
<div class="bg-white rounded-2xl border border-gray-200 p-6
  hover:-translate-y-1 hover:shadow-lg transition-all duration-200">
```

### Glow Effect
```html
<div class="bg-white rounded-2xl border border-gray-200 p-6
  hover:border-indigo-300 hover:shadow-[0_0_24px_-4px_rgba(99,102,241,0.25)]
  transition-all duration-300">
```

### Gradient Border Reveal
Two backgrounds: the surface clipped to the padding box, the gradient to the border box behind a transparent border.
```css
.card-gradient-border {
  border: 1px solid transparent;
  border-radius: var(--radius, 1rem);
  background:
    linear-gradient(var(--color-surface, #fff), var(--color-surface, #fff)) padding-box,
    linear-gradient(var(--color-neutral-200, #e5e7eb), var(--color-neutral-200, #e5e7eb)) border-box;
}
.card-gradient-border:hover,
.card-gradient-border:focus-within {
  background:
    linear-gradient(var(--color-surface, #fff), var(--color-surface, #fff)) padding-box,
    linear-gradient(135deg, var(--color-primary), var(--color-accent)) border-box;
}
```

### Content Slide-Up
```html
<div class="group relative bg-white rounded-2xl overflow-hidden border border-gray-200">
  <img src="/image.jpg" alt="" class="w-full h-48 object-cover" />
  <div class="p-6">
    <h3 class="font-bold text-gray-900">Card Title</h3>
    <p class="mt-2 text-gray-600 text-sm">Description text here.</p>
  </div>
  <!-- Actions slide up on hover AND keyboard focus; always visible on touch (no hover) -->
  <div class="absolute bottom-0 inset-x-0 p-4 bg-gradient-to-t from-white via-white
    translate-y-full group-hover:translate-y-0 group-focus-within:translate-y-0
    [@media(hover:none)]:translate-y-0 motion-safe:transition-transform duration-300">
    <button type="button" class="w-full bg-indigo-600 text-white py-2 rounded-lg font-medium">
      View details
    </button>
  </div>
</div>
```

### Image Zoom on Hover
```html
<div class="group rounded-2xl overflow-hidden border border-gray-200">
  <div class="overflow-hidden">
    <img src="/image.jpg" alt="" width="600" height="400" loading="lazy"
      class="w-full h-48 object-cover motion-safe:transition-transform duration-500
        motion-safe:group-hover:scale-110" />
  </div>
</div>
```

---

## 4. Product Card

```html
<div class="group bg-white rounded-2xl border border-gray-200 overflow-hidden
  hover:shadow-lg transition-all duration-200">
  <!-- Image -->
  <div class="relative overflow-hidden">
    <img src="/product.jpg" alt="Product name" width="600" height="448" loading="lazy"
      class="w-full h-56 object-cover motion-safe:group-hover:scale-105 transition-transform duration-500" />
    <!-- Badge (red-600, not red-500: white text needs 4.5:1) -->
    <span class="absolute top-3 left-3 bg-red-600 text-white text-xs font-bold
      px-2.5 py-1 rounded-full">-20%</span>
    <!-- Wishlist button: visible on hover, keyboard focus, and touch devices -->
    <button type="button" aria-label="Add to wishlist" aria-pressed="false"
      class="absolute top-3 right-3 w-11 h-11 bg-white/90 backdrop-blur rounded-full
      flex items-center justify-center text-gray-600 hover:text-red-600
      opacity-0 group-hover:opacity-100 focus-visible:opacity-100
      [@media(hover:none)]:opacity-100 transition-opacity">
      <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
          d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z"/>
      </svg>
    </button>
  </div>

  <!-- Content -->
  <div class="p-4">
    <!-- Category -->
    <span class="text-xs font-medium text-indigo-600 uppercase tracking-wide">Electronics</span>
    <!-- Title -->
    <h3 class="mt-1 font-semibold text-gray-900 line-clamp-2">
      Wireless Noise-Cancelling Headphones Pro Max
    </h3>
    <!-- Rating -->
    <div class="mt-2 flex items-center gap-1.5">
      <div class="flex text-amber-400" role="img" aria-label="Rated 4.5 out of 5">
        <!-- 4.5 stars, each aria-hidden="true" -->
        <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20"><path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z"/></svg>
        <!-- repeat for remaining stars -->
      </div>
      <span class="text-sm text-gray-500">(128<span class="sr-only"> reviews</span>)</span>
    </div>
    <!-- Price -->
    <div class="mt-3 flex items-baseline gap-2">
      <span class="text-xl font-bold text-gray-900"><span class="sr-only">Sale price </span>$249</span>
      <del class="text-sm text-gray-500"><span class="sr-only">Original price </span>$319</del>
    </div>
  </div>

  <!-- Action -->
  <div class="px-4 pb-4">
    <button type="button" class="w-full bg-gray-950 text-white py-2.5 rounded-xl font-medium
      hover:bg-gray-800 active:bg-gray-900 transition-colors">
      Add to cart
    </button>
  </div>
</div>
```

---

## 5. Feature / Benefit Card

```html
<div class="bg-white rounded-2xl border border-gray-200 p-6
  hover:border-indigo-200 hover:shadow-md transition-all duration-200">
  <!-- Icon -->
  <div class="w-12 h-12 rounded-xl bg-indigo-50 text-indigo-600
    flex items-center justify-center">
    <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true">
      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
        d="M13 10V3L4 14h7v7l9-11h-7z"/>
    </svg>
  </div>
  <!-- Content -->
  <h3 class="mt-4 text-lg font-semibold text-gray-900">Lightning Fast</h3>
  <p class="mt-2 text-gray-600 text-sm leading-relaxed">
    Built on edge infrastructure for sub-100ms response times worldwide.
    Your users won't wait.
  </p>
  <!-- Optional link -->
  <a href="#" class="mt-4 inline-flex items-center gap-1 text-sm font-medium
    text-indigo-600 hover:text-indigo-500 transition-colors">
    Learn more
    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
        d="M17 8l4 4m0 0l-4 4m4-4H3"/>
    </svg>
  </a>
</div>
```

---

## 6. Testimonial Card

```html
<div class="bg-white rounded-2xl border border-gray-200 p-6">
  <!-- Stars -->
  <div class="flex gap-0.5 text-amber-400 mb-4" role="img" aria-label="Rated 5 out of 5">
    <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20"><path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z"/></svg>
    <!-- repeat 5x -->
  </div>
  <!-- Quote -->
  <blockquote class="text-gray-700 leading-relaxed">
    "This tool saved our team 20 hours per week. The onboarding was seamless
    and we saw results from day one. Can't imagine going back."
  </blockquote>
  <!-- Author -->
  <div class="mt-6 flex items-center gap-3">
    <img src="/avatar.jpg" alt="" class="w-10 h-10 rounded-full" />
    <div>
      <div class="font-semibold text-gray-900 text-sm">Alex Rivera</div>
      <div class="text-gray-500 text-sm">VP Engineering, Acme Inc</div>
    </div>
  </div>
</div>
```

---

## 7. Blog Post Card

```html
<a href="/blog/post-slug" class="group block bg-white rounded-2xl border border-gray-200
  overflow-hidden hover:shadow-lg transition-shadow duration-200
  focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600">
  <!-- Image -->
  <div class="overflow-hidden">
    <img src="/blog-cover.jpg" alt="" width="600" height="384" loading="lazy"
      class="w-full h-48 object-cover motion-safe:group-hover:scale-105 transition-transform duration-500" />
  </div>
  <!-- Content -->
  <div class="p-5">
    <!-- Meta -->
    <div class="flex items-center gap-2 text-sm text-gray-500 mb-3">
      <span class="bg-indigo-50 text-indigo-700 px-2 py-0.5 rounded-full text-xs font-medium">
        Engineering
      </span>
      <span>5 min read</span>
    </div>
    <!-- Title -->
    <h3 class="font-bold text-gray-900 text-lg group-hover:text-indigo-600
      transition-colors line-clamp-2">
      How We Reduced Our Build Times by 80%
    </h3>
    <!-- Excerpt -->
    <p class="mt-2 text-gray-600 text-sm line-clamp-3 leading-relaxed">
      A deep dive into our migration to incremental builds and how it
      transformed our developer experience across 12 teams.
    </p>
    <!-- Author -->
    <div class="mt-4 flex items-center gap-2">
      <img src="/avatar.jpg" alt="" class="w-6 h-6 rounded-full" />
      <span class="text-sm text-gray-600">Sarah Kim</span>
      <time datetime="2026-03-15" class="text-sm text-gray-500">Mar 15, 2026</time>
    </div>
  </div>
</a>
```

---

## 8. Interactive Cards

### Expandable Card
```html
<details class="group bg-white rounded-2xl border border-gray-200 overflow-hidden">
  <summary class="flex items-center justify-between p-6 cursor-pointer
    list-none hover:bg-gray-50 transition-colors">
    <div>
      <h3 class="font-semibold text-gray-900">Card Title</h3>
      <p class="text-sm text-gray-500 mt-1">Click to expand</p>
    </div>
    <svg class="w-5 h-5 text-gray-400 group-open:rotate-180 transition-transform"
      fill="none" stroke="currentColor" viewBox="0 0 24 24">
      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
        d="M19 9l-7 7-7-7"/>
    </svg>
  </summary>
  <div class="px-6 pb-6 text-gray-600 text-sm leading-relaxed">
    Expanded content appears here. This can contain additional details,
    images, or nested components.
  </div>
</details>
```

### Flippable Card
Use sparingly — hidden content is easy to miss. The flip must also trigger on keyboard focus, and should be a simple swap (no 3D) under reduced motion. Prefer the expandable card when the back holds important content.
```html
<div class="group [perspective:1000px] h-64 w-full">
  <div class="relative h-full w-full motion-safe:transition-transform duration-500
    [transform-style:preserve-3d] group-hover:[transform:rotateY(180deg)]
    group-focus-within:[transform:rotateY(180deg)]">
    <!-- Front -->
    <div class="absolute inset-0 bg-white rounded-2xl border border-gray-200
      p-6 flex flex-col items-center justify-center [backface-visibility:hidden]">
      <div class="w-16 h-16 rounded-2xl bg-indigo-100 text-indigo-600
        flex items-center justify-center text-2xl mb-4">
        <svg class="w-8 h-8" aria-hidden="true"><!-- icon --></svg>
      </div>
      <h3 class="font-bold text-gray-900">Feature Name</h3>
      <p class="mt-2 text-sm text-gray-500 text-center">Hover or focus to learn more</p>
    </div>
    <!-- Back -->
    <div class="absolute inset-0 bg-indigo-600 rounded-2xl p-6
      flex flex-col items-center justify-center text-white text-center
      [backface-visibility:hidden] [transform:rotateY(180deg)]">
      <p class="text-sm leading-relaxed">
        Detailed description of this feature. Includes specific benefits
        and use cases for your team.
      </p>
      <!-- Focusing this link flips the card (group-focus-within) -->
      <a href="#" class="mt-4 bg-white text-indigo-700 px-4 py-2 rounded-lg
        font-medium text-sm">Learn more about Feature Name</a>
    </div>
  </div>
</div>
```

---

## 9. Skeleton Loading States

```html
<!-- Skeleton card mimics the final card structure.
     Put aria-busy="true" + an sr-only "Loading…" on the grid container, not on each card. -->
<div class="bg-white rounded-2xl border border-gray-200 overflow-hidden motion-safe:animate-pulse"
  aria-hidden="true">
  <!-- Image placeholder -->
  <div class="h-48 bg-gray-200"></div>
  <!-- Content placeholders -->
  <div class="p-5 space-y-3">
    <div class="h-3 bg-gray-200 rounded-full w-1/4"></div>
    <div class="h-5 bg-gray-200 rounded-full w-3/4"></div>
    <div class="space-y-2">
      <div class="h-3 bg-gray-200 rounded-full w-full"></div>
      <div class="h-3 bg-gray-200 rounded-full w-5/6"></div>
    </div>
    <div class="flex items-center gap-2 pt-2">
      <div class="w-6 h-6 bg-gray-200 rounded-full"></div>
      <div class="h-3 bg-gray-200 rounded-full w-20"></div>
    </div>
  </div>
</div>
```

### Skeleton Rules
1. Match the exact layout of the real card (same heights, widths, spacing).
2. Use `motion-safe:animate-pulse` on the container (not individual elements).
3. Use `rounded-full` for text placeholders, `rounded-lg` for images.
4. Show 3–6 skeleton cards while loading, matching the expected grid.
5. Transition from skeleton to real content without layout shift.

---

## Verify: Render and Check

Don't hand over code you haven't looked at. After generating it:
1. Screenshot it at mobile and desktop widths, e.g. `npx playwright screenshot --full-page --viewport-size=390,844 file://$PWD/index.html mobile.png`, then again with `--viewport-size=1440,900` (or point at the dev server URL).
2. Open both images and check: no horizontal scroll or clipped/overlapping text, hierarchy reads at a glance, brand tokens are applied, images load at the right aspect ratio.
3. Tab through once: every interactive element gets a visible focus ring, in a logical order.
4. Check cards in a grid with long and short content (equal heights, line-clamp works), and that hover-only content is reachable by keyboard and on touch.
5. Fix what you find and re-screenshot before reporting done.

---

## Card Design Checklist

- [ ] Card has clear visual boundaries (border, shadow, or background contrast)
- [ ] Content hierarchy: media > title > description > actions
- [ ] Hover effect provides feedback (lift, glow, or border change)
- [ ] Interactive cards use a real `<a>` or `<button>` (not `tabindex` on a `<div>`) with a `focus-visible` ring
- [ ] Hover-only content (actions, flip side) also appears on focus and on touch devices
- [ ] Hover motion respects `prefers-reduced-motion`; card images have width/height and `loading="lazy"`
- [ ] Text is truncated with `line-clamp` where needed
- [ ] Grid is responsive (3 cols desktop, 2 tablet, 1 mobile)
- [ ] Loading skeleton matches card layout
- [ ] Images have proper `alt` text and `object-cover`
- [ ] Card links wrap the entire card, or use the stretched-link pattern (`::after { inset: 0 }` on the title link) when the card also contains other buttons — never nest interactive elements inside an `<a>`
- [ ] Rendered and screenshotted at 390px and 1440px (see Verify)
- [ ] Consistent border radius, padding, and spacing across all cards
