---
name: taste-web-performance
description: |
  Core Web Vitals discipline for agent-built pages: LCP, CLS, INP budgets, font loading that doesn't shift layout, images that don't bloat, CSS/JS that doesn't block. A designed page that loads like a template is half a page. Use when generating or auditing any web page or component. Stack on the design-taste core skill.
triggers:
  - "performance"
  - "core web vitals"
  - "lcp"
  - "cls"
  - "inp"
  - "page speed"
  - "optimization"
  - "lighthouse"
  - "font loading"
  - "image optimization"
---

# taste-web-performance

> Speed is part of the design. A hero that paints in 900ms with a shifted headline is a broken hero.

## 1. THE BUDGETS (Write These Down First)

Target p75 on mobile hardware (the median phone, not your Mac):

- **LCP < 2.5s** — the hero text or hero image must be the largest contentful element and must paint fast.
- **CLS < 0.1** — no element moves after it's first painted. Every font, image, and ad-sized box is a CLS risk.
- **INP < 200ms** — no click waits on a long task; no JS does heavy work on the main thread at interaction time.
- **Total page weight ≤ 1.5MB** for a marketing page; a "simple" page should ship under 500KB.
- State the budget in the build notes — a page without a stated budget is a page without a plan.

## 2. FONT LOADING (The #1 Agent Failure)

- **Never more than two font families, never more than ~4 styles** (the design-taste skills already cap this — enforce it in code).
- `font-display: swap` on all webfonts, and the text must not shift when the font lands: reserve the space or accept ≤ 3px movement.
- `preload` the hero font face (woff2 only); load the rest lazily or from the correct `unicode-range` subsets.
- No `@import` in CSS (render-blocking), no font loading scripts that block first paint, no loading fonts the page doesn't use on the current route.
- If the pack's display font is decorative, consider system-font fallback for everything below the hero — the headline is where the font earns its weight.

## 3. IMAGES (Every One Gets a Decision)

- Every image: explicit `width`/`height` (or `aspect-ratio`) — the CLS fix that costs nothing.
- Format: AVIF/WebP at runtime, PNG only for real transparency, never a 2MB JPEG on a marketing page.
- `srcset`/`sizes` for responsive delivery; `loading="lazy"` for everything below the fold, `fetchpriority="high"` for the LCP image.
- Decorative imagery is CSS (gradients, noise, patterns) — an agent that "solves" a background with a 400KB image has failed the design, not just the budget.
- Hero images are cropped at the correct aspect ratio in the markup, not squeezed by CSS.

## 4. CSS & JS DELIVERY

- CSS: one file, or per-route critical CSS; no framework stylesheet for a 2-section page, no purged-out-of-the-box utility soup.
- JS: `defer` everything that isn't interactive-critical; no framework for a static page (a landing page has no business shipping React).
- No synchronous third-party scripts (chat widgets, analytics) in the critical path; analytics loads after interaction if it loads at all.
- Animations run on transform/opacity only (see taste-motion); anything animating `top/width/box-shadow` on scroll is a jank generator, not a feature.

## 5. THE VERIFY RITUAL (Always Run It)

1. Build, then run Lighthouse on a throttled profile (mobile, Slow 4G) — not on a localhost Mac.
2. Report the three vitals + weight. Any budget miss gets fixed or gets a written reason.
3. Re-check after any image/font change — those are the two things that regress silently.
4. `prefers-reduced-motion` and offline-safe fonts are not optional extras; they're part of the contract.

## 6. CHECKLIST (Fail the Page If…)

- [ ] Any font loaded without `swap` + dimensioned text, or more than two families.
- [ ] Any image without dimensions, without format decision, or lazy-loading the hero.
- [ ] Any layout shift visible on reload (test it; shifts lie about themselves).
- [ ] Any render-blocking script/stylesheet, `@import`, or framework shipped to a static page.
- [ ] Page weight or vitals over budget with no stated reason.
- [ ] No Lighthouse run logged for the page.
- [ ] The page looks designed but behaves like 2015.