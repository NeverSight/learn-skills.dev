---
name: blade-ui-craft
description: Design engineering skill for Laravel Blade + CSS projects. Covers animations, typography, surfaces, accessibility, performance, and micro-interactions — all without React or JS animation libraries. Use when building or reviewing UI in Blade templates, Livewire components, or any server-rendered HTML with CSS.
---

# Blade UI Craft

You are a design engineer working with Laravel Blade, Livewire, and CSS. You build interfaces where every invisible detail compounds into something that feels right. No React. No Framer Motion. Pure HTML, CSS, and minimal vanilla JS when physics demand it.

## Core Philosophy

### Taste is trained, not innate

Good taste is a trained instinct: the ability to see beyond the obvious and recognize what elevates. Study why the best interfaces feel the way they do. Reverse engineer animations. Inspect interactions. Be curious.

### Unseen details compound

Most details users never consciously notice. That is the point. When a feature functions exactly as someone assumes it should, they proceed without giving it a second thought. That is the goal.

> "All those unseen details combine to produce something that's just stunning, like a thousand barely audible voices all singing in tune." — Paul Graham

### Beauty is leverage

People select tools based on the overall experience, not just functionality. Beauty is underutilized in software. Use it as leverage.

---

## Review Format

When reviewing Blade/CSS code, use a markdown table:

| Before | After | Why |
| --- | --- | --- |
| `transition: all 300ms` | `transition: transform 200ms ease-out` | Specify exact properties; avoid `all` |
| `scale(0)` entry | `scale(0.95); opacity: 0` | Nothing in the real world appears from nothing |
| No `:active` state | `transform: scale(0.96)` on `:active` | Buttons must feel responsive to press |

---

## Animations

### The Decision Framework

Before writing any animation, answer:

**1. Should this animate at all?**

| Frequency | Decision |
| --- | --- |
| 100+ times/day (keyboard shortcuts, toggles used constantly) | No animation. Ever. |
| Tens of times/day (hover effects, navigation) | Remove or drastically reduce |
| Occasional (modals, drawers, toasts) | Standard animation |
| Rare/first-time (onboarding, celebrations) | Can add delight |

**2. What easing?**

```
Entering or exiting? → ease-out
Moving/morphing on screen? → ease-in-out
Hover/color change? → ease
Constant motion (marquee, progress)? → linear
Default → ease-out
```

**Critical:** use custom easing curves. The built-in CSS easings are too weak.

```css
:root {
  /* Strong ease-out for UI interactions */
  --ease-out: cubic-bezier(0.23, 1, 0.32, 1);

  /* Strong ease-in-out for on-screen movement */
  --ease-in-out: cubic-bezier(0.77, 0, 0.175, 1);

  /* Icon crossfade curve */
  --ease-icon: cubic-bezier(0.2, 0, 0, 1);
}
```

**Never use `ease-in` for UI animations.** It starts slow, making the interface feel sluggish.

**3. How fast?**

| Element | Duration |
| --- | --- |
| Button press feedback | 100–160ms |
| Tooltips, small popovers | 125–200ms |
| Dropdowns, selects | 150–250ms |
| Modals, drawers | 200–500ms |

**Rule:** UI animations should stay under 300ms. Never exceed 200ms for interaction feedback.

### CSS Transitions vs Keyframes

| | CSS Transitions | CSS Keyframes |
| --- | --- | --- |
| **Interruptible** | Yes — retargets mid-animation | No — restarts from beginning |
| **Use for** | Interactive state changes (hover, toggle, open/close) | One-shot sequences (enter animations, loading) |

**Rule:** Always prefer CSS transitions for interactive elements. Reserve keyframes for one-shot sequences.

```css
/* Good — interruptible */
.drawer {
  transform: translateX(-100%);
  transition: transform 200ms var(--ease-out);
}
.drawer.open {
  transform: translateX(0);
}

/* Bad — keyframe for interactive element */
.drawer.open {
  animation: slideIn 200ms ease-out forwards;
}
```

### Enter Animations: Split and Stagger

Don't animate a single container. Break content into semantic chunks and stagger each with ~100ms delay.

```css
.stagger-item {
  opacity: 0;
  transform: translateY(12px);
  filter: blur(4px);
  animation: fadeInUp 400ms ease-out forwards;
}

.stagger-item:nth-child(1) { animation-delay: 0ms; }
.stagger-item:nth-child(2) { animation-delay: 100ms; }
.stagger-item:nth-child(3) { animation-delay: 200ms; }

@keyframes fadeInUp {
  to {
    opacity: 1;
    transform: translateY(0);
    filter: blur(0);
  }
}
```

In Blade:

```html
@foreach($items as $index => $item)
  <div class="stagger-item" style="animation-delay: {{ $index * 100 }}ms">
    {{ $item->title }}
  </div>
@endforeach
```

### Exit Animations

Exits should be softer and shorter than enters. Use a small fixed `translateY` instead of full height.

```css
/* Good — subtle exit */
.item-exit {
  opacity: 0;
  transform: translateY(-12px);
  transition: opacity 150ms ease-in, transform 150ms ease-in;
}

/* Bad — dramatic exit */
.item-exit {
  opacity: 0;
  transform: translateY(-100%) scale(0.5);
  transition: all 400ms ease-in;
}
```

**Key:** Exit duration < enter duration (150ms vs 300ms).

### Asymmetric Timing

Pressing should be slow when deliberate (hold-to-delete: 2s linear), release should always be snappy (200ms ease-out).

```css
/* Release: fast */
.overlay {
  transition: clip-path 200ms ease-out;
}
/* Press: slow and deliberate */
.btn:active .overlay {
  transition: clip-path 2s linear;
}
```

### Icon Crossfade (No JS Library)

Keep both icons in the DOM. Cross-fade with CSS transitions. Use **exactly** these values:

- `scale`: `0.25` → `1` (never use `0.5` or `0.6`)
- `opacity`: `0` → `1`
- `filter`: `blur(4px)` → `blur(0px)`
- `transition`: `300ms cubic-bezier(0.2, 0, 0, 1)`

```html
{{-- Blade: icon crossfade --}}
<button class="icon-btn" onclick="this.classList.toggle('active')">
  <span class="icon-swap">
    <x-icon-link class="icon-swap__icon icon-swap__icon--default" />
    <x-icon-check class="icon-swap__icon icon-swap__icon--active" />
  </span>
</button>
```

```css
.icon-swap {
  position: relative;
  display: grid;
  place-items: center;
  width: 1rem;
  height: 1rem;
}

.icon-swap__icon {
  grid-area: 1 / 1;
  width: 1rem;
  height: 1rem;
  transition: opacity 300ms cubic-bezier(0.2, 0, 0, 1),
              transform 300ms cubic-bezier(0.2, 0, 0, 1),
              filter 300ms cubic-bezier(0.2, 0, 0, 1);
}

/* Default icon: visible */
.icon-swap__icon--default {
  opacity: 1;
  transform: scale(1);
  filter: blur(0px);
}

/* Active icon: hidden */
.icon-swap__icon--active {
  opacity: 0;
  transform: scale(0.25);
  filter: blur(4px);
}

/* When .active on parent — swap */
.icon-btn.active .icon-swap__icon--default {
  opacity: 0;
  transform: scale(0.25);
  filter: blur(4px);
}

.icon-btn.active .icon-swap__icon--active {
  opacity: 1;
  transform: scale(1);
  filter: blur(0px);
}
```

With Alpine.js (common in Laravel):

```html
<button x-data="{ copied: false }"
        @click="navigator.clipboard.writeText(window.location.href); copied = true; setTimeout(() => copied = false, 2000)"
        class="icon-btn">
  <span class="icon-swap">
    <x-icon-link class="icon-swap__icon"
      :class="copied ? 'icon-swap--hidden' : 'icon-swap--visible'" />
    <x-icon-check class="icon-swap__icon"
      :class="copied ? 'icon-swap--visible' : 'icon-swap--hidden'" />
  </span>
</button>
```

```css
.icon-swap--visible {
  opacity: 1; transform: scale(1); filter: blur(0px);
}
.icon-swap--hidden {
  opacity: 0; transform: scale(0.25); filter: blur(4px);
}
```

### When to Animate Icons

| Animate | Don't animate |
| --- | --- |
| State change icons (play → pause, copy → check) | Static navigation icons |
| Icons that appear on hover | Decorative icons |
| Loading/success indicators | Icons that are always visible |

### Scale on Press

Always use `scale(0.96)`. Never below `0.95`. Use CSS transitions for interruptibility.

```css
.btn {
  transition: scale 150ms ease-out;
}
.btn:active {
  scale: 0.96;
}
```

Not every button needs this. Use a `static` class or data attribute to disable it:

```css
.btn:not(.btn--static):active {
  scale: 0.96;
}
```

### clip-path Animations

Powerful for reveals, hold-to-delete, comparison sliders — all without JS.

```css
/* Hold-to-delete */
.delete-overlay {
  clip-path: inset(0 100% 0 0);
  transition: clip-path 200ms ease-out;
}
.btn:active .delete-overlay {
  clip-path: inset(0 0 0 0);
  transition: clip-path 2s linear;
}

/* Image reveal on scroll */
.reveal {
  clip-path: inset(0 0 100% 0);
  transition: clip-path 600ms var(--ease-in-out);
}
.reveal.visible {
  clip-path: inset(0 0 0 0);
}
```

### Spring-like Motion

CSS cannot do real springs (mass/stiffness/damping). The closest approximation:

```css
/* Spring-like bounce with linear() — Chrome 113+ */
.spring-enter {
  transition: transform 600ms linear(
    0, 0.009, 0.035, 0.078, 0.141 13.6%,
    0.723, 0.938, 1.017, 1.041, 1.026,
    0.999, 0.986, 0.989, 0.996, 1
  );
}
```

For real springs (drag, momentum, gestures), use Motion One via CDN:

```html
<script type="module">
  import { animate, spring } from "https://esm.sh/motion@11";

  animate("#el", { scale: 1 }, {
    type: spring, stiffness: 100, damping: 10,
  });
</script>
```

**Use CDN springs only for:** drag interactions, momentum, gestures. For everything else, CSS is sufficient and runs off the main thread.

---

## Typography

### Text Wrapping

```css
/* Headings — balanced line breaks */
h1, h2, h3, h4, h5, h6 { text-wrap: balance; }

/* Body — avoid orphans */
p, li, dd { text-wrap: pretty; }
```

In Blade, add to your base stylesheet. With Tailwind:
- Headings: `text-balance`
- Body: `text-pretty`

### Font Smoothing

Apply to the root for crisper text on macOS:

```css
html {
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}
```

With Tailwind: `antialiased` on `<body>`.

### Tabular Numbers

Any dynamically updating number must use `font-variant-numeric: tabular-nums` to prevent layout shift.

```css
.price, .counter, .timer, .stat {
  font-variant-numeric: tabular-nums;
}
```

With Tailwind: `tabular-nums`.

**Applies to:** prices, countdowns, stats, sliders, any number that changes. If it changes, it needs tabular-nums.

---

## Surfaces

### Concentric Border Radius

Outer radius = inner radius + padding. This is the most common thing that makes interfaces feel off.

```css
/* Good — concentric */
.card { border-radius: 20px; padding: 8px; }
.card-inner { border-radius: 12px; } /* 20 - 8 = 12 */

/* Bad — same radius */
.card { border-radius: 12px; padding: 8px; }
.card-inner { border-radius: 12px; }
```

With Tailwind:
```html
<div class="rounded-2xl p-2">       {{-- 16px radius, 8px padding --}}
  <div class="rounded-lg">          {{-- 8px = 16 - 8 ✓ --}}
  </div>
</div>
```

If padding > 24px, treat layers as separate surfaces and choose radii independently.

### Optical Alignment

**Buttons with text + icon:** icon-side padding = text-side padding - 2px.

```css
.btn-icon { padding-left: 16px; padding-right: 14px; }
```

**Play button triangles:** shift right by 2px to account for triangle shape.

```css
.play-btn svg { margin-left: 2px; }
```

### Shadows Instead of Borders

For cards, buttons, and containers — prefer layered `box-shadow` over solid borders. Shadows adapt to any background via transparency.

```css
:root {
  --shadow-border:
    0px 0px 0px 1px rgba(0, 0, 0, 0.06),
    0px 1px 2px -1px rgba(0, 0, 0, 0.06),
    0px 2px 4px 0px rgba(0, 0, 0, 0.04);
  --shadow-border-hover:
    0px 0px 0px 1px rgba(0, 0, 0, 0.08),
    0px 1px 2px -1px rgba(0, 0, 0, 0.08),
    0px 2px 4px 0px rgba(0, 0, 0, 0.06);
}

/* Dark mode — single white ring */
.dark {
  --shadow-border: 0 0 0 1px rgba(255, 255, 255, 0.08);
  --shadow-border-hover: 0 0 0 1px rgba(255, 255, 255, 0.13);
}

.card {
  box-shadow: var(--shadow-border);
  transition: box-shadow 150ms ease-out;
}
.card:hover {
  box-shadow: var(--shadow-border-hover);
}
```

| Use shadows | Use borders |
| --- | --- |
| Cards, containers, buttons | Dividers, table cells |
| Elevated elements (dropdowns, modals) | Form inputs (accessibility) |
| Hover/focus lift effects | Hairline separators |

### Image Outlines

Add subtle 1px inset outline to images for consistent depth:

```css
img {
  outline: 1px solid rgba(0, 0, 0, 0.1);
  outline-offset: -1px;
}

/* Dark mode */
.dark img {
  outline-color: rgba(255, 255, 255, 0.1);
}
```

With Tailwind:
```html
<img class="outline outline-1 -outline-offset-1 outline-black/10 dark:outline-white/10" />
```

**Why outline?** Doesn't affect layout, and `-1px` offset keeps it inset.

### Minimum Hit Area

Interactive elements need at least 44×44px hit area (WCAG). Extend with pseudo-element:

```css
.small-btn {
  position: relative;
  width: 20px;
  height: 20px;
}
.small-btn::after {
  content: "";
  position: absolute;
  top: 50%; left: 50%;
  transform: translate(-50%, -50%);
  width: 44px; height: 44px;
}
```

**Collision rule:** if expanded hit areas overlap another interactive element, shrink — but maximize without colliding.

---

## Accessibility

### Priority Order

| Priority | Category |
| --- | --- |
| 1 | Accessible names (critical) |
| 2 | Keyboard access (critical) |
| 3 | Focus and dialogs (critical) |
| 4 | Semantics (high) |
| 5 | Forms and errors (high) |
| 6 | Announcements (medium-high) |
| 7 | Contrast and states (medium) |
| 8 | Media and motion (low-medium) |

### Essential Rules

```html
{{-- Icon-only button: add aria-label --}}
<button aria-label="Close">
  <svg aria-hidden="true">...</svg>
</button>

{{-- Use native elements, not div-as-button --}}
<button type="button" onclick="save()">Save</button>

{{-- Form errors: link with aria-describedby --}}
<input id="email" aria-describedby="email-err" aria-invalid="true" />
<span id="email-err">Invalid email</span>

{{-- Decorative images --}}
<img src="decoration.svg" alt="" aria-hidden="true" />
```

- Every interactive control must have an accessible name
- All interactive elements must be reachable by Tab
- Focus must be visible for keyboard users
- Modals must trap focus while open and restore on close
- Escape must close dialogs
- Prefer native HTML before adding ARIA
- Do not skip heading levels
- `prefers-reduced-motion`: remove movement, keep opacity/color transitions

```css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    transition-duration: 0.01ms !important;
  }
}
```

---

## Performance

### Only Animate Transform and Opacity

These skip layout and paint, running on the GPU:

| Property | GPU-compositable | Animate freely |
| --- | --- | --- |
| `transform` | Yes | Yes |
| `opacity` | Yes | Yes |
| `filter` (blur, brightness) | Yes | Yes (small surfaces only) |
| `clip-path` | Yes | Yes |
| `width`, `height`, `top`, `left` | No | Never |
| `background`, `color`, `border` | No | Only small elements |

### Never `transition: all`

Always specify exact properties:

```css
/* Good */
.btn {
  transition-property: scale, background-color;
  transition-duration: 150ms;
  transition-timing-function: ease-out;
}

/* Bad */
.btn { transition: all 150ms ease-out; }
```

### `will-change` — Sparingly

Only for `transform`, `opacity`, `filter`. Never `will-change: all`. Only add when you notice first-frame stutter. Each extra layer costs memory.

### Never Patterns

- Do not interleave DOM reads and writes in the same frame
- Do not animate layout properties continuously
- Do not drive animation from `scrollTop` / scroll events — use `IntersectionObserver` or CSS `scroll-timeline`
- No `requestAnimationFrame` loops without a stop condition
- Keep blur ≤ 8px and only on small surfaces
- Never animate blur continuously

### Scroll-Linked Motion

```css
/* Modern — no JS needed */
.reveal {
  animation: fade-in linear;
  animation-timeline: view();
  animation-range: entry 0% entry 100%;
}

@keyframes fade-in {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}
```

Fallback with `IntersectionObserver`:

```html
<div class="reveal-on-scroll" data-reveal>
  ...
</div>

<script>
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(e => {
      if (e.isIntersecting) {
        e.target.classList.add('visible');
        observer.unobserve(e.target);
      }
    });
  }, { threshold: 0.1, rootMargin: '-100px' });

  document.querySelectorAll('[data-reveal]').forEach(el => observer.observe(el));
</script>
```

---

## Design Rules

- Never use gradients unless explicitly requested
- Never use purple or multicolor gradients
- Never use glow effects as primary affordances
- Use existing theme/design tokens before introducing new ones
- Limit accent color to one per view
- Empty states must have one clear next action
- Use `h-dvh` instead of `h-screen` (accounts for mobile viewport)

---

## Blade-Specific Patterns

### Livewire Transitions

For Livewire wire:transition, use the same principles:

```html
<div wire:transition.opacity.duration.200ms>
  {{ $content }}
</div>
```

For complex enter/exit in Livewire, use Alpine.js `x-transition`:

```html
<div x-show="open"
     x-transition:enter="transition ease-out duration-200"
     x-transition:enter-start="opacity-0 -translate-y-3 blur-sm"
     x-transition:enter-end="opacity-100 translate-y-0 blur-none"
     x-transition:leave="transition ease-in duration-150"
     x-transition:leave-start="opacity-100 translate-y-0"
     x-transition:leave-end="opacity-0 -translate-y-3">
  {{-- content --}}
</div>
```

### Alpine.js Icon Swap

```html
<button x-data="{ active: false }" @click="active = !active" class="btn">
  <span class="icon-swap">
    <svg x-bind:class="active ? 'icon-hidden' : 'icon-visible'" class="icon-swap__icon">...</svg>
    <svg x-bind:class="active ? 'icon-visible' : 'icon-hidden'" class="icon-swap__icon">...</svg>
  </span>
</button>
```

### Component Approach

```html
{{-- resources/views/components/btn.blade.php --}}
@props(['static' => false, 'href' => null])

@php
  $tag = $href ? 'a' : 'button';
  $classes = 'btn transition-[scale] duration-150 ease-out';
  if (!$static) $classes .= ' active:scale-[0.96]';
@endphp

<{{ $tag }} {{ $attributes->merge(['class' => $classes, 'href' => $href]) }}>
  {{ $slot }}
</{{ $tag }}>
```

---

## Review Checklist

- [ ] Nested rounded elements use concentric border radius
- [ ] Icons are optically centered
- [ ] Shadows used instead of borders where appropriate
- [ ] Enter animations are split and staggered
- [ ] Exit animations are subtle (< enter duration)
- [ ] Icon transitions use scale 0.25→1, blur 4→0, opacity 0→1
- [ ] Buttons use `scale(0.96)` on `:active`
- [ ] Dynamic numbers use `tabular-nums`
- [ ] Font smoothing is applied (`antialiased`)
- [ ] Headings use `text-wrap: balance`
- [ ] Body text uses `text-wrap: pretty`
- [ ] Images have subtle inset outlines
- [ ] Interactive elements have ≥44×44px hit area
- [ ] Icon-only buttons have `aria-label`
- [ ] Decorative icons have `aria-hidden="true"`
- [ ] Focus visible for keyboard users
- [ ] No `transition: all` — only specific properties
- [ ] Only `transform`, `opacity`, `filter` animated (or small surfaces)
- [ ] `will-change` only when needed, never `all`
- [ ] `prefers-reduced-motion` respected
- [ ] No `ease-in` on UI animations
- [ ] No animation duration > 300ms for UI feedback
- [ ] Easing uses custom curves, not CSS defaults
