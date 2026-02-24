---
name: structural-grid
description: Structural Grid (Exposed Grid / Rail Layout) design system for modern SaaS landing pages. Use when building dark-themed marketing sites, landing pages, or SaaS product pages inspired by Linear, Vercel, Resend, and Planetscale. Provides CSS foundations, section patterns, component recipes, and responsive border logic for the visible-grid aesthetic.
metadata:
  author: nabinkhair42
  version: "1.0.0"
  tags:
    - design-system
    - css
    - tailwind
    - nextjs
    - landing-page
    - saas
---

# Structural Grid Design System

You are implementing a **Structural Grid** (also called "Exposed Grid" or "Rail Layout") design pattern. This is the modern SaaS design pattern used by Linear, Vercel, Resend, Profound, and Planetscale — where the underlying page grid is promoted to a first-class visual element.

## Core Principles

1. **Visible structure** — Vertical rail lines and horizontal dividers are decorative elements, not hidden scaffolding
2. **Content lives inside the grid** — Components blend into the rail structure rather than floating over it
3. **Dashed internal, solid external** — Rail lines and section dividers are solid; internal grid cell dividers are dashed
4. **Alternating visual rhythm** — Sections alternate between default and dot-pattern backgrounds for depth
5. **Minimal containers** — No rounded-xl bordered cards floating inside sections. Content sits directly within the grid
6. **Consistent letter-spacing** — Use `tracking-wide` on all section labels and inline labels. Never mix `tracking-widest` and `tracking-wider`
7. **Every card hovers** — All grid cells get `transition-colors hover:bg-white/[0.02]` for interactive feedback

---

## CSS Foundation

Add these to your global CSS. All measurements derive from a single `--rail-offset` variable.

```css
/* Vertical rail lines */
.page-rails {
  --rail-offset: max(1rem, calc(50% - 36rem)); /* = max-w-6xl centered */
  position: relative;
  overflow-x: clip; /* clip, NOT hidden — hidden breaks position:sticky */
}
.page-rails::before,
.page-rails::after {
  content: '';
  position: absolute;
  top: 0;
  bottom: 0;
  width: 1px;
  background: var(--border);
  pointer-events: none;
  z-index: 1;
}
.page-rails::before { left: var(--rail-offset); }
.page-rails::after { right: var(--rail-offset); }

/* Content bounded to rail edges */
.rail-bounded {
  margin-left: var(--rail-offset);
  margin-right: var(--rail-offset);
}

/* Horizontal section divider between rails */
.section-divider {
  position: relative;
  height: 1px;
  z-index: 2;
}
.section-divider::before {
  content: '';
  position: absolute;
  left: var(--rail-offset, max(1rem, calc(50% - 36rem)));
  right: var(--rail-offset, max(1rem, calc(50% - 36rem)));
  height: 1px;
  background: var(--border);
}

/* Subtle dot pattern for section backgrounds */
.dot-pattern {
  background-image: radial-gradient(rgba(255, 255, 255, 0.04) 1px, transparent 1px);
  background-size: 24px 24px;
}

/* Custom scrollbar — matches dark themes */
* {
  scrollbar-width: thin;
  scrollbar-color: rgba(255, 255, 255, 0.1) transparent;
}
::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: rgba(255, 255, 255, 0.1); border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: rgba(255, 255, 255, 0.2); }
```

### Critical: overflow-x

**Always use `overflow-x: clip` on `.page-rails`, NEVER `overflow-x: hidden`.**
`hidden` creates a new scroll container which breaks `position: sticky` on any descendant.
`clip` clips overflow visually without affecting scroll/sticky behavior.

### Smooth scroll with sticky navbar offset

When using a sticky navbar with anchor links, add to `html`:

```css
html {
  scroll-behavior: smooth;
  scroll-padding-top: 5rem; /* clears the sticky navbar height */
}
```

### Adjusting rail width

Change `36rem` to match your desired max content width:
- `32rem` = 1024px = Tailwind `max-w-5xl`
- `36rem` = 1152px = Tailwind `max-w-6xl` (recommended default)
- `40rem` = 1280px = Tailwind `max-w-7xl`

---

## Page Structure

```tsx
<Navbar />
<div className="page-rails flex flex-col">
  <Hero />
  <div className="section-divider" aria-hidden="true" />
  <SectionA />
  <div className="section-divider" aria-hidden="true" />
  <SectionB />
  <div className="section-divider" aria-hidden="true" />
  <Cta />
</div>
<Footer />
```

Every section is separated by a `section-divider`. The rails run the full height of `.page-rails`. Navbar and Footer sit **outside** `.page-rails`.

### Section IDs

Always add `id` attributes to sections that need anchor links or nav tracking:

```tsx
<section id="features">
<section id="showcase">
<section id="faq">
```

---

## Section Patterns

### 1. Text Header (reusable across sections)

```tsx
<div className="mx-auto w-full max-w-6xl px-6">
  <div className="pb-6 pt-16">
    <p className="text-xs font-medium uppercase tracking-wide text-muted-foreground">
      Section Label
    </p>
    <h2 className="mt-3 text-2xl font-bold tracking-tight sm:text-3xl">
      Section Title
    </h2>
    <p className="mt-2 max-w-md text-base text-muted-foreground">
      Section description text here.
    </p>
  </div>
</div>
```

### 2. Grid with Dashed Internal Dividers

Use `rail-bounded` to align the grid edges with the rails. Apply `border-t border-border` to connect the grid's top edge with the section divider above. Use dashed borders between cells.

**Responsive border logic for a 3-column grid (1 col mobile, 2 col sm, 3 col lg):**

```tsx
<div className="rail-bounded border-t border-border">
  <div className="grid sm:grid-cols-2 lg:grid-cols-3">
    {items.map((item, i) => (
      <div
        key={item.id}
        className={`group px-6 py-8 transition-colors hover:bg-white/[0.02]
          ${i % 3 !== 0 ? "lg:border-l lg:border-dashed lg:border-border" : ""}
          ${i % 2 !== 0 ? "sm:max-lg:border-l sm:max-lg:border-dashed sm:max-lg:border-border" : ""}
          ${i >= 3 ? "lg:border-t lg:border-dashed lg:border-border" : ""}
          ${i >= 2 ? "sm:max-lg:border-t sm:max-lg:border-dashed sm:max-lg:border-border" : ""}
          ${i >= 1 ? "max-sm:border-t max-sm:border-dashed max-sm:border-border" : ""}
        `}
      >
        {/* cell content */}
      </div>
    ))}
  </div>
</div>
```

**Border logic rules:**
- `border-l` (left) = applied to every cell that is NOT the first in its row at that breakpoint
- `border-t` (top) = applied to every cell that is NOT in the first row at that breakpoint
- Use `sm:max-lg:` prefix for tablet-only borders that differ from desktop
- Use `max-sm:` prefix for mobile-only borders
- All internal borders are `border-dashed border-border`
- All grid cells include `group transition-colors hover:bg-white/[0.02]` for hover feedback

### 3. Side-by-Side Layout with Full-Height Dashed Divider

For layouts like text + interactive content, use `items-stretch` so the dashed divider spans the full section height.

```tsx
<section id="section-name" className="relative">
  <div className="dot-pattern absolute inset-0" aria-hidden="true" />
  <div className="relative mx-auto grid w-full max-w-6xl items-stretch gap-0 px-6 lg:grid-cols-[1fr_1.6fr]">
    <div className="py-16 lg:py-24">
      <div className="lg:sticky lg:top-24">
        <p className="text-xs font-medium uppercase tracking-wide text-muted-foreground">Label</p>
        <h2 className="mt-3 text-2xl font-bold tracking-tight sm:text-3xl">Title</h2>
        <p className="mt-4 max-w-sm text-base leading-relaxed text-muted-foreground">Description.</p>
      </div>
    </div>
    <div className="pb-16 lg:border-l lg:border-dashed lg:border-border lg:py-24 lg:pl-8">
      {/* tall content */}
    </div>
  </div>
</section>
```

**Sticky text requirements:**
- Parent `.page-rails` must use `overflow-x: clip` (not `hidden`)
- `items-stretch` on the grid makes both columns match the taller column's height
- Apply padding to children, not the grid itself

### 4. Hero Section

```tsx
<section className="relative flex flex-col items-center px-4 pb-0 pt-24 text-center sm:pt-32">
  <div className="pointer-events-none absolute inset-0 z-0 mx-auto hidden w-full max-w-5xl px-4 sm:block" aria-hidden="true">
    <div className="absolute left-4 top-0 bottom-0 w-px border-l border-dashed border-border" />
    <div className="absolute right-4 top-0 bottom-0 w-px border-r border-dashed border-border" />
  </div>

  <div className="relative z-10 mb-6 inline-flex items-center gap-2 rounded-full border border-white/[0.08] bg-white/[0.04] px-4 py-1.5">
    <span className="size-1.5 rounded-full bg-white/40 animate-pulse" />
    <span className="text-[13px] text-white/60">Badge Text</span>
  </div>

  <h1 className="relative z-10 max-w-2xl text-4xl font-bold tracking-tight sm:text-5xl lg:text-6xl">
    Main headline<br />
    <span className="text-muted-foreground">secondary line</span>
  </h1>

  <p className="relative z-10 mx-auto mt-5 max-w-lg text-base leading-relaxed text-muted-foreground sm:text-lg">
    Subtitle description
  </p>

  <div className="relative z-10 mt-8 flex flex-col items-center gap-3 sm:flex-row">
    <Link href="/pricing" className="inline-flex h-10 items-center gap-2 rounded-lg bg-foreground px-5 text-sm font-medium text-background transition-opacity hover:opacity-80">
      Primary CTA
    </Link>
    <Link href="/#features" className="inline-flex h-10 items-center gap-2 rounded-lg border border-white/[0.1] px-5 text-sm font-medium text-foreground transition-colors hover:bg-white/[0.04]">
      Secondary CTA
    </Link>
  </div>

  <div className="relative hidden w-full self-stretch sm:block" aria-hidden="true">
    <div className="absolute left-0 right-0 border-t border-dashed border-border"
      style={{ marginLeft: "calc(var(--rail-offset) - 1rem)", marginRight: "calc(var(--rail-offset) - 1rem)" }} />
  </div>

  <ProductMockup />
</section>
```

### 5. CTA Section (Bottom)

```tsx
<section>
  <div className="mx-auto flex w-full max-w-6xl flex-col items-center px-6 py-20 text-center sm:py-28">
    <h2 className="text-3xl font-bold tracking-tight sm:text-4xl">Call to action headline</h2>
    <p className="mt-4 max-w-md text-base text-muted-foreground sm:text-lg">Supporting text.</p>
    <div className="mt-8 flex flex-col items-center gap-3 sm:flex-row">
      <Link href="/pricing" className="inline-flex h-11 w-44 items-center justify-center gap-2 rounded-lg bg-foreground text-sm font-medium text-background transition-opacity hover:opacity-80">Primary CTA</Link>
      <Link href="/pricing" className="inline-flex h-11 w-44 items-center justify-center gap-2 rounded-lg border border-white/[0.1] text-sm font-medium text-foreground transition-colors hover:bg-white/[0.04]">Secondary CTA</Link>
    </div>
  </div>
</section>
```

---

## Component Recipes

### Reusable Button Component

```tsx
const base = "inline-flex items-center justify-center gap-2 rounded-lg font-medium disabled:pointer-events-none disabled:opacity-50";

const variants = {
  primary: "bg-foreground text-background shadow-[inset_0_1px_0_rgba(255,255,255,0.25),inset_0_-1px_0_rgba(0,0,0,0.15),0_0_0_1px_rgba(255,255,255,0.2),0_4px_12px_rgba(0,0,0,0.5),0_0_32px_rgba(255,255,255,0.1)] transition-opacity hover:opacity-80",
  outline: "border border-white/[0.1] text-foreground transition-colors hover:bg-white/[0.04]",
  ghost: "text-muted-foreground transition-colors hover:text-foreground",
} as const;

const sizes = {
  sm: "h-9 px-3 text-xs",
  md: "h-10 px-5 text-sm",
  lg: "h-11 px-6 text-sm",
  icon: "size-9 text-sm",
} as const;
```

### Reusable Input Component

```tsx
<input className="h-10 w-full rounded-lg border border-border bg-white/[0.03] px-3 text-sm text-foreground outline-none transition-colors placeholder:text-muted-foreground/50 focus:border-primary/40 focus:ring-1 focus:ring-primary/20" />
```

### Icon Container (Feature Cards)

```tsx
<div className="mb-4 inline-flex size-10 items-center justify-center rounded-xl border border-white/[0.08] bg-white/[0.03] text-white/60 transition-colors group-hover:text-white/90">
  <FeatureIcon size={18} stroke={1.5} />
</div>
```

### Responsive Tables

```tsx
<div className="rail-bounded overflow-x-auto border-t border-border">
  <div className="min-w-[600px]">
    <div className="grid grid-cols-4">{/* table content */}</div>
  </div>
</div>
```

### IntersectionObserver Animation Pattern

```tsx
const observer = new IntersectionObserver(
  ([entry]) => { if (entry.isIntersecting) { setIsVisible(true); observer.disconnect(); } },
  { threshold: 0.3 }
);
```

Staggered entrance:

```tsx
style={{
  opacity: isVisible ? 1 : 0,
  transform: isVisible ? "translateY(0)" : "translateY(8px)",
  transition: `all 0.4s ease ${0.3 + i * 0.1}s`,
}}
```

---

## Design Tokens Reference

| Element | Solid/Dashed | CSS |
|---------|-------------|-----|
| Vertical rails | Solid | `background: var(--border)` |
| Section dividers | Solid | `background: var(--border)` |
| Internal grid dividers | Dashed | `border-dashed border-border` |
| Hero guide lines | Dashed | `border-dashed border-border` |
| Dot pattern | N/A | `radial-gradient` with 4% white opacity |
| Card hover | N/A | `hover:bg-white/[0.02]` |
| Section label | N/A | `text-xs font-medium uppercase tracking-wide` |
| Button primary | N/A | `bg-foreground text-background` + layered shadow |
| Button outline | N/A | `border border-white/[0.1] hover:bg-white/[0.04]` |
| Input field | N/A | `border-border bg-white/[0.03] focus:border-primary/40` |

---

## Common Pitfalls

1. **`overflow: hidden` breaks sticky** — Always use `overflow-x: clip` on the rails container
2. **Grid borders extending past rails** — Use `.rail-bounded` (margin-based) instead of `mx-auto max-w-6xl`
3. **Orphaned grid items on mobile** — Plan item counts around your column counts
4. **Border-left on single-column mobile** — Use `sm:max-lg:border-l` for tablet-only left borders
5. **Section padding on grid parents** — Apply padding to grid children, not the container
6. **Rails not reaching page bottom** — Ensure `.page-rails` wraps all content
7. **Missing `border-border` on dashed dividers** — Always include the color class
8. **Anchor links behind sticky navbar** — Add `scroll-padding-top: 5rem` to `html`
9. **Inconsistent tracking classes** — Standardize on `tracking-wide`
10. **Missing hover states on grid cards** — Every grid cell needs `hover:bg-white/[0.02]`
11. **Both color classes applied at once** — Use a conditional, never both simultaneously
12. **4-column tables on mobile** — Always wrap in `overflow-x-auto` with `min-w-[600px]`
13. **Dashed lines can't reach rails** — Use `calc(var(--rail-offset) - Xrem)` margins
14. **Auth route groups** — Use Next.js `(auth)` route group with shared `layout.tsx`
15. **Component organization** — UI primitives in `components/ui/`, page-specific in `components/{section}/`
