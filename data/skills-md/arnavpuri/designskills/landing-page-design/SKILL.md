---
name: landing-page-design
description: >
  Full, multi-section marketing and conversion pages: section order (hero, social proof,
  features, how it works, testimonials, pricing, FAQ, final CTA, footer), CTA strategy,
  and page-level performance. Use when the user asks to "build a landing page", "create a
  homepage", "design a marketing page", "make a product page", "build a SaaS landing page",
  "create a signup page", or any marketing/conversion-focused web page. For only the
  above-the-fold block use hero-section; for individual cards use card-design; for app
  screens and general components use ui-design.
license: MIT
---

# Landing Page Design

## Before You Start: Load Design Context

1. **Read `.agents/design-context.md`** (written by the `design-context` skill). If it is missing, look for tokens in `tailwind.config.*` or `:root` CSS variables. If nothing exists, use the defaults (Primary `#2563EB`, Secondary `#7C3AED`, Accent `#F59E0B`, Tailwind gray neutrals, Inter for headings and body, Minimal style) and **tell the user defaults were used** — suggest running `design-context`.
2. **Map tokens to CSS variables once**, then use only the variables: `--color-primary`, `--color-primary-light`, `--color-primary-dark`, `--color-secondary`, `--color-accent`, `--color-neutral-50`…`--color-neutral-900`, `--color-success`/`-warning`/`-error`, `--font-heading`, `--font-body`, `--font-mono`, `--radius`, and the 4px-base spacing scale.
3. **Tailwind:** expose the same variables (v3 `theme.extend`, v4 `@theme`) as `primary`, `primary-light`, `primary-dark`, `secondary`, `accent`, `neutral-*`, `font-heading`, `font-body`. The `indigo-*` / `gray-*` classes in the examples below are placeholders for these tokens.
4. **Figma:** if the user gives a Figma URL, pull it with the Figma MCP (`get_design_context`, `get_screenshot`) and match it; it overrides the context file for that design.
5. Ask or infer: what is the product, who is the audience, and what is the **single** desired action? Use the context's tone for copy and its style archetype to pick the hero pattern and section backgrounds.

---

## 1. Section Framework

Every high-converting landing page follows this flow. You can reorder or omit sections, but this is the proven sequence:

```
1. Hero          — Value prop + primary CTA (above the fold)
2. Social Proof  — Logos, stats, or trust badges
3. Features      — What it does (benefits, not features)
4. How It Works  — 3-step simplicity
5. Testimonials  — Real humans saying real things
6. Pricing       — Clear tiers with obvious recommendation
7. FAQ           — Overcome objections
8. Final CTA     — Repeat the primary action
9. Footer        — Links, legal, secondary nav
```

### Spacing Between Sections
- Use `py-20 md:py-28 lg:py-32` for major sections (full spacing scale in section 11).
- Alternate between white and subtle gray (`bg-gray-50`) backgrounds.
- Use a `max-w-7xl mx-auto px-4 sm:px-6 lg:px-8` container for all content.

---

## 2. Hero Patterns

The hero is the first section of the page. This is the default; for split, video, and minimal-typography variants, background techniques, and LCP details, use the **hero-section** skill.

### Pattern A: Centered Hero (Best for SaaS)
```html
<section class="relative overflow-hidden bg-white pt-24 pb-20 sm:pt-32 sm:pb-28">
  <div class="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 text-center">
    <!-- Optional: Badge / announcement -->
    <div class="inline-flex items-center gap-2 rounded-full bg-indigo-50 px-3 py-1 text-sm
      font-medium text-indigo-700 ring-1 ring-indigo-600/10 mb-8">
      <span class="h-1.5 w-1.5 rounded-full bg-indigo-600"></span>
      Now in public beta
    </div>

    <h1 class="text-4xl sm:text-5xl lg:text-6xl font-extrabold tracking-tight text-gray-950
      max-w-4xl mx-auto leading-[1.1]">
      The faster way to build
      <span class="text-indigo-600">beautiful products</span>
    </h1>

    <p class="mt-6 text-lg sm:text-xl text-gray-600 max-w-2xl mx-auto leading-relaxed">
      Ship production-ready interfaces in minutes. Stop fighting CSS and start
      delighting your users.
    </p>

    <div class="mt-10 flex flex-col sm:flex-row items-center justify-center gap-4">
      <a href="#" class="w-full sm:w-auto bg-indigo-600 text-white px-8 py-3.5 rounded-xl
        font-semibold text-lg hover:bg-indigo-500 transition-colors shadow-lg
        shadow-indigo-600/25">
        Start free trial
      </a>
      <a href="#" class="w-full sm:w-auto text-gray-700 px-8 py-3.5 rounded-xl font-semibold
        text-lg hover:bg-gray-100 transition-colors flex items-center justify-center gap-2">
        <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20" aria-hidden="true"><!-- play icon --></svg>
        Watch demo
      </a>
    </div>

    <!-- Trust signals -->
    <p class="mt-8 text-sm text-gray-500">No credit card required. Free for up to 3 projects.</p>
  </div>
</section>
```

### Other Hero Patterns
Split (text + product visual), video background, and animated heroes live in **hero-section**. Whatever the pattern, the hero image is the LCP element: never `loading="lazy"`, always `fetchpriority="high"` plus `width`/`height`.

---

## 3. Social Proof Section

### Logo Bar
```html
<section class="bg-gray-50 py-12 border-y border-gray-100">
  <div class="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
    <p class="text-center text-sm font-medium text-gray-500 mb-8">
      Trusted by 2,000+ teams worldwide
    </p>
    <div class="flex flex-wrap items-center justify-center gap-x-12 gap-y-6
      grayscale opacity-60 hover:grayscale-0 hover:opacity-100 transition-all">
      <!-- Logos: SVG preferred, max-h-8, auto width -->
      <img src="/logos/stripe.svg" alt="Stripe" width="112" height="28" class="h-7 w-auto" loading="lazy" />
      <img src="/logos/vercel.svg" alt="Vercel" width="112" height="28" class="h-7 w-auto" loading="lazy" />
      <!-- ... more logos -->
    </div>
  </div>
</section>
```

### Stats Counters
```html
<div class="grid grid-cols-2 lg:grid-cols-4 gap-8 text-center">
  <div>
    <div class="text-4xl font-extrabold text-gray-950">10K+</div>
    <div class="mt-1 text-sm text-gray-500">Active users</div>
  </div>
  <div>
    <div class="text-4xl font-extrabold text-gray-950">99.9%</div>
    <div class="mt-1 text-sm text-gray-500">Uptime SLA</div>
  </div>
  <!-- ... -->
</div>
```

---

## 4. Feature Sections

### Bento Grid (Modern, Visual)
```html
<section class="py-20 bg-white">
  <div class="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
    <div class="text-center mb-16">
      <h2 class="text-3xl sm:text-4xl font-bold text-gray-950">Everything you need</h2>
      <p class="mt-4 text-lg text-gray-600 max-w-2xl mx-auto">
        A complete toolkit for modern teams.
      </p>
    </div>
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
      <!-- Featured card (spans 2 cols) -->
      <div class="md:col-span-2 bg-gradient-to-br from-indigo-600 to-purple-700
        rounded-2xl p-8 text-white min-h-[300px] flex flex-col justify-end">
        <h3 class="text-2xl font-bold">AI-powered insights</h3>
        <p class="mt-2 text-white/90">Automatically surface what matters most.</p>
      </div>
      <!-- Regular cards -->
      <div class="bg-gray-50 rounded-2xl p-8 min-h-[300px] flex flex-col justify-end">
        <div class="w-10 h-10 rounded-lg bg-indigo-100 text-indigo-600 flex items-center
          justify-center mb-4" aria-hidden="true"><!-- icon --></div>
        <h3 class="text-lg font-bold text-gray-950">Real-time sync</h3>
        <p class="mt-2 text-gray-600">Changes appear instantly across all devices.</p>
      </div>
    </div>
  </div>
</section>
```

### Alternating Rows (Classic, Detailed)
- Odd rows: text left, image right.
- Even rows: image left, text right.
- Each row highlights one feature with a heading, description, and visual.

### Icon Grid (Simple, Scannable)
- 3 or 4 columns of icon + heading + short description.
- Icons should be consistent style (outline or filled, not mixed).

---

## 5. CTA Design

### Primary CTA Rules
- **Size**: Minimum 48px tall, 200px+ wide. Larger than any other button on the page.
- **Color**: Highest contrast element on the page. Primary brand color.
- **Copy**: Action-oriented verb. "Start free trial" > "Submit". "Get started" > "Sign up".
- **Urgency**: Optional, but effective. "Start free — no credit card required."
- **Repetition**: Primary CTA appears at least 3 times: hero, mid-page, bottom.

### Sticky CTA (Mobile)
```html
<!-- Add pb-24 to <body> on mobile so the bar never covers the footer -->
<div class="fixed bottom-0 inset-x-0 bg-white/90 backdrop-blur-lg border-t
  border-gray-200 px-4 pt-4 pb-[calc(1rem+env(safe-area-inset-bottom))] sm:hidden z-50">
  <a href="#" class="block w-full bg-indigo-600 text-white text-center py-3.5
    rounded-xl font-semibold text-lg">
    Start free trial
  </a>
</div>
```

### Secondary CTA Patterns
- Ghost button (outline) next to primary.
- Text link with arrow: `Learn more ->`.
- Never two equally-weighted CTAs side by side.
- Use `<a>` for CTAs that navigate and `<button>` for ones that open a modal or submit.

---

## 6. How It Works

### Three-Step Pattern
```html
<section class="py-20 bg-gray-50">
  <div class="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
    <h2 class="text-3xl font-bold text-center text-gray-950 mb-16">
      Get started in minutes
    </h2>
    <div class="grid md:grid-cols-3 gap-12">
      <div class="text-center">
        <div class="w-12 h-12 rounded-full bg-indigo-100 text-indigo-600 font-bold
          text-lg flex items-center justify-center mx-auto">1</div>
        <h3 class="mt-4 text-lg font-semibold text-gray-950">Connect your data</h3>
        <p class="mt-2 text-gray-600">Import from 50+ sources with one click.</p>
      </div>
      <!-- Steps 2 and 3 follow same pattern -->
    </div>
  </div>
</section>
```

Keep it to 3 steps. If your process has more, simplify or group.

---

## 7. Testimonials

### Card Grid
```html
<div class="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
  <div class="bg-white rounded-2xl p-6 shadow-sm border border-gray-100">
    <div class="flex gap-1 text-amber-400 mb-4" role="img" aria-label="Rated 5 out of 5">
      <!-- 5 star icons, each aria-hidden="true" -->
    </div>
    <blockquote class="text-gray-700 leading-relaxed">
      "This completely changed how our team works. We shipped 3x faster in the
      first month."
    </blockquote>
    <div class="mt-4 flex items-center gap-3">
      <img src="/avatars/sarah.jpg" alt="" width="40" height="40" loading="lazy" class="w-10 h-10 rounded-full" />
      <div>
        <div class="font-semibold text-gray-950 text-sm">Sarah Chen</div>
        <div class="text-gray-500 text-sm">CTO, Acme Corp</div>
      </div>
    </div>
  </div>
</div>
```

### Rules
- Real photos, real names, real companies.
- Include role/title for authority.
- Star ratings add visual credibility.
- Highlight specific outcomes ("3x faster", "saved 20 hours/week").

---

## 8. Pricing Section

### Three-Tier Pattern
- **Free/Basic** — anchor price, limited features.
- **Pro** (recommended) — highlighted with border, badge, or shadow. Most features.
- **Enterprise** — "Contact sales", unlimited everything.

### Design Rules
- Highlight the recommended plan with `ring-2 ring-indigo-600` and `lg:scale-105` (no scaling on mobile — it causes overflow when cards stack).
- Use a "Most Popular" badge.
- Annual/monthly toggle with savings callout — a real `<button role="switch" aria-checked>` or radio group, not a styled `<div>`.
- Feature list: checkmarks for included, dashes or X for excluded.
- Price: large number, small period (e.g., **$29**/mo).

---

## 9. Trust Signals

Place these throughout the page, not just in one section:
- **Security badges**: SSL, SOC 2, GDPR
- **Money-back guarantee**: "30-day full refund, no questions asked"
- **Support**: "24/7 support" or "Avg. response time: 2 hours"
- **Social proof**: "Join 10,000+ teams" near CTA buttons
- **Press logos**: "As seen in TechCrunch, Forbes..."

---

## 10. Performance Priorities

### Above-the-Fold (LCP Optimization)
- Hero image/video poster is the likely LCP element: `fetchpriority="high"`, explicit `width`/`height`, never `loading="lazy"`.
- Preload only if the image is discovered late (CSS background, JS-rendered, `<picture>`).
- Inline critical CSS for the hero section. Don't fade the headline in from `opacity: 0` — it delays LCP.
- Targets (Core Web Vitals, 75th percentile): LCP ≤ 2.5s, INP ≤ 200ms, CLS ≤ 0.1.

```html
<link rel="preload" href="/hero-image.webp" as="image" fetchpriority="high" />
```

### Below-the-Fold
- Lazy-load all images: `loading="lazy"`.
- Use `srcset` for responsive images.
- Defer non-critical JS.
- Use `content-visibility: auto` with `contain-intrinsic-size: auto 800px` on far-down sections (without the size hint the scrollbar jumps).
- Give every image `width`/`height` (or `aspect-ratio`) to prevent layout shift.

```html
<img
  src="/feature.webp"
  srcset="/feature-400.webp 400w, /feature-800.webp 800w, /feature-1200.webp 1200w"
  sizes="(max-width: 768px) 100vw, 50vw"
  width="1200" height="800"
  loading="lazy"
  alt="Feature description"
  class="rounded-2xl"
/>
```

---

## 11. Conversion-Focused Spacing & Flow

### Visual Flow Rules
1. **F-pattern** for text-heavy pages (eyes scan top-left to right, then down-left).
2. **Z-pattern** for minimal pages (eyes zigzag across the page).
3. **Each section answers one question** then guides to the next.
4. **White space is a feature** — cramped pages feel untrustworthy.

### Section Spacing Scale
- Between major sections: `py-20 md:py-28 lg:py-32`
- Between subsections: `py-12 lg:py-16`
- Between heading and content: `mb-12 lg:mb-16`
- Between content items: `gap-6 lg:gap-8`

---

## Verify: Render and Check

Don't hand over code you haven't looked at. After generating it:
1. Screenshot it at mobile and desktop widths, e.g. `npx playwright screenshot --full-page --viewport-size=390,844 file://$PWD/index.html mobile.png`, then again with `--viewport-size=1440,900` (or point at the dev server URL).
2. Open both images and check: no horizontal scroll or clipped/overlapping text, hierarchy reads at a glance, brand tokens are applied, images load at the right aspect ratio.
3. Tab through once: every interactive element gets a visible focus ring, in a logical order.
4. Check the 390px screenshot shows the headline and primary CTA without scrolling, and the sticky CTA does not cover content. Run Lighthouse (`npx lighthouse <url> --only-categories=performance,accessibility`) if a server is running.
5. Fix what you find and re-screenshot before reporting done.

---

## Landing Page Checklist

- [ ] Single clear CTA (repeated 3+ times)
- [ ] Hero LCP image uses `fetchpriority="high"`, has width/height, is not lazy-loaded
- [ ] Social proof within first scroll
- [ ] Benefits over features in copy
- [ ] Mobile-optimized (sticky CTA, stacked layout)
- [ ] Core Web Vitals: LCP ≤ 2.5s, INP ≤ 200ms, CLS ≤ 0.1
- [ ] Animations respect `prefers-reduced-motion`; text meets 4.5:1 contrast
- [ ] Rendered and screenshotted at 390px and 1440px (see Verify)
- [ ] No competing navigation (minimal header on landing pages)
