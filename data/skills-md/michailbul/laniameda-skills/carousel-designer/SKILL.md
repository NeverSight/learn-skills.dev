---
name: carousel-designer
description: Generate branded LinkedIn carousel slides as a single HTML file + PDF export. Use when asked to build, generate, or iterate on a LinkedIn carousel, social media slide deck, or branded content slides. Produces Tailwind-based HTML (1080x1350px per slide, 7 slides), renders to PDF and PNGs via Playwright, and saves output to dist/.
---

# Carousel Designer

Generate a 7-slide LinkedIn carousel as a single self-contained HTML file using Tailwind CSS CDN. Export to PDF + PNGs via Playwright.

## Output structure

```
<project>/
  src/slides.html      ← single file, all 7 slides
  dist/carousel.pdf
  dist/slides/01.png … 07.png
  package.json         ← { "type": "module", "dependencies": { "playwright": "^1.52" } }
```

## Workflow — follow in order, skip nothing

### Phase 1: Design Intelligence (before writing any HTML)
1. Read `references/REFERENCES.md` — extract layout patterns, type choices, color moments, spacing ratios from listed references. Note which patterns apply to each slide type.
2. Read `references/layout-rules.md` — internalize all 12 rules. These override any general instincts about layout.
3. Read `references/design-standards.md` — lock in the typography scale + quality checklist.
4. Read the brief — map each key point to a slide type and select the right primitive.

### Phase 2: Build
5. Read `assets/linkedin-base.html` — use as skeleton (fonts, tokens, grid/grain, slide counter all pre-wired)
6. Read `assets/components/primitives.html` — copy-paste the right building block per slide
7. Build `src/slides.html`:
   - Start from base template, fill 7 slides
   - Apply layout-rules.md constraints (alignment, scale contrast, negative space)
   - Apply patterns extracted from REFERENCES.md
   - Every element left-aligned unless explicitly specified otherwise
   - Slide counter `"0N / 07"` on every slide

### Phase 3: Render & QA
8. Run `npm install` then `node scripts/render.mjs`
9. Run full quality checklist from `references/design-standards.md`
10. If any check fails: fix and re-render (do not skip)
11. Print: `RENDER_COMPLETE: dist/carousel.pdf + dist/slides/01-07.png`

## Slide map
| # | Type         | Components to use                  |
|---|-------------|-------------------------------------|
| 1 | Cover       | kicker, hero-headline, subtitle, badge-row |
| 2 | Problem     | kicker, section-headline, subtitle  |
| 3 | Stat / Math | kicker, section-headline, metric-card OR equation-block |
| 4 | Stat / Math | kicker, section-headline, metric-card OR equation-block |
| 5 | System      | kicker, section-headline, checklist |
| 6 | Solution    | kicker, section-headline, stack-grid |
| 7 | CTA         | kicker, section-headline, ordered-list, closing-line |

## Fonts (v2 — always include in <head>)
```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Space+Grotesk:wght@400;500;600;700&family=JetBrains+Mono:wght@400;700&display=swap" rel="stylesheet">
```

## Brand tokens (always inline in the `<script>` block)
```js
tailwind.config = {
  theme: { extend: {
    colors: { primary:'#8566AF', secondary:'#BA943B', accent:'#EA3F2C', 'accent-alt':'#FF552E', brand:'#09090B' },
    fontFamily: {
      display: ['"Bebas Neue"', 'Impact', 'sans-serif'],
      body:    ['"Space Grotesk"', '"Helvetica Neue"', 'sans-serif'],
      mono:    ['"JetBrains Mono"', '"SF Mono"', 'monospace'],
    },
  }},
}
```

## Hard rules
- Fonts: Bebas Neue + Space Grotesk + JetBrains Mono via Google Fonts CDN — **never Arial/Inter/Roboto as display**
- Use Tailwind CDN (`<script src="https://cdn.tailwindcss.com"></script>`) — no build step
- Every slide: class `slide`, id `slide-0N`, 1080×1350 via CSS
- Black border: `border-left:12px; border-right:12px; border-top:14px; border-bottom:14px; all #09090b`
- Grid overlay via `::before`, grain via `::after` (see base template)
- `chrome` div: `position:relative; z-index:1; padding:78px 76px; display:flex; flex-direction:column`
- Slide counter `"0N / 07"` on every slide: `absolute bottom-[28px] right-[32px] z-index:2`
- **The Unforgettable Rule**: slide 1 must pass — one element works as a standalone viral image
- **1 idea per slide** — no walls of text
- Accent color (`#EA3F2C`) on ≤1 element per slide
- No placeholder text — real content from brief only
- Print `RENDER_COMPLETE` only after PDF + all PNGs verified to exist

## Reference files — read ALL in Phase 1 before writing HTML
| File | What it contains | When to use |
|------|-----------------|-------------|
| `references/REFERENCES.md` | Design inspiration + brand DNA | Extract layout/type/color patterns before designing |
| `references/layout-rules.md` | 12 explicit design rules | Alignment, scale contrast, spacing, card style, narrative arc |
| `references/design-standards.md` | Typography scale, color rules, quality checklist | Type sizes, color assignments, QA after render |

## Asset files — copy-paste when building
| File | What it contains |
|------|-----------------|
| `assets/linkedin-base.html` | Skeleton: fonts, Tailwind config, grid/grain, slide counter wired up |
| `assets/components/primitives.html` | All primitives: kicker, hero-headline, bleed-headline, section-headline, subtitle, metric-card, equation-block, terminal-block, data-table, stack-grid, checklist, asymmetric-layout, badge-row, closing-line+CTA |
| `scripts/render.mjs` | Playwright render → PDF + PNGs (copy to project root) |
