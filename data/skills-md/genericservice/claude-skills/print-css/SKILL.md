---
name: print-css
description: Write production-ready print stylesheets. Covers @page rules, page breaks, visibility, color management, typography, images, links, tables, and framework-specific gotchas for Next.js/React/Tailwind. Use when the user asks to add print styles, make a page printable, or create a print-friendly layout.
version: 1.0.0
---

# Print CSS

You are a print stylesheet specialist. You write `@media print` styles that make web pages look intentional on paper -- not like someone hit Cmd+P on a web page.

## When to Use This Skill

- User asks to "make this printable" or "add print styles"
- Building a page that will be printed (invitations, tickets, reports, invoices)
- Creating a "Save as PDF" version of a web page
- Fixing broken print layouts

## Print Stylesheet Skeleton

Every print stylesheet follows this structure, in order:

```css
@media print {
  /* 1. Page setup */
  @page { size: letter; margin: 0.5in 0.6in; }

  /* 2. Force color reproduction */
  * {
    -webkit-print-color-adjust: exact !important;
    print-color-adjust: exact !important;
  }

  /* 3. Base typography */
  body {
    background: white !important;
    color: #1a1a1a !important;
    font-size: 10.5pt;
    line-height: 1.6;
  }

  /* 4. Kill web-only elements */
  nav, .no-print, footer, .cookie-banner { display: none !important; }

  /* 5. Kill animations */
  *, *::before, *::after {
    animation: none !important;
    transition: none !important;
  }

  /* 6. Flatten layouts */
  /* ... framework-specific resets ... */

  /* 7. Page break control */
  h1, h2, h3 { page-break-after: avoid; break-after: avoid-page; }
  tr, img, blockquote { page-break-inside: avoid; break-inside: avoid-page; }
  p { orphans: 3; widows: 3; }

  /* 8. Images */
  img { max-width: 100%; max-height: 3in; }

  /* 9. Links */
  a[href^="http"]::after { content: " (" attr(href) ")"; font-size: 0.8em; }
  a[href^="#"]::after { content: ""; }

  /* 10. Tables */
  thead { display: table-header-group; }
  tfoot { display: table-footer-group; }
}
```

---

## @page Rules

```css
@page {
  size: letter;            /* or: A4, 210mm 297mm, landscape */
  margin: 0.5in 0.6in;    /* top/bottom  left/right */
}

@page :first {
  margin-top: 1in;        /* extra space for cover page */
}
```

**Available sizes:** `letter` (8.5x11in), `A4` (210x297mm), `A3`, `A5`, `legal`, or explicit dimensions.

**Gotchas:**
- @page margin support is limited across browsers. Use padding on body/wrapper as fallback.
- DevTools print emulation does not show @page effects. Must check actual print preview (Cmd+P).
- Cannot set background-color at the page level reliably.

---

## Page Break Control

Use **both** legacy and modern properties for maximum browser support:

```css
/* Prevent breaking inside an element */
.card, tr, figure {
  page-break-inside: avoid;
  break-inside: avoid-page;
}

/* Force a break before a section */
.chapter {
  page-break-before: always;
  break-before: page;
}

/* Prevent a break right after a heading */
h1, h2, h3 {
  page-break-after: avoid;
  break-after: avoid-page;
}
```

### Orphans and Widows

Prevent stranded lines at page boundaries:

```css
p {
  orphans: 3;   /* minimum lines at bottom of page */
  widows: 3;    /* minimum lines at top of next page */
}
```

**Gotchas:**
- `page-break-inside: avoid` does not work reliably on flex or grid containers. Switch to `display: block` in print.
- Overusing `break-inside: avoid` can push content to the next page unpredictably.
- Test with actual content -- short paragraphs behave differently from long ones.

---

## Visibility

### Elements to always hide in print

```css
@media print {
  nav,
  .sidebar,
  .cookie-banner,
  .social-share,
  .comments,
  .ads,
  .chat-widget,
  .search-bar,
  .no-print {
    display: none !important;
  }
}
```

### Print-only elements

```css
.print-only {
  display: none;  /* hidden on screen */
}

@media print {
  .print-only {
    display: block;  /* visible on paper */
  }
}
```

Use `display: none !important` (not `visibility: hidden`) -- visibility preserves layout space and wastes paper.

---

## Colors and Backgrounds

### print-color-adjust

Controls whether the browser can optimize colors for print:

```css
* {
  -webkit-print-color-adjust: exact !important;  /* Safari/older Chrome */
  print-color-adjust: exact !important;           /* standard */
}
```

- `exact` -- preserves declared colors (even if ink-heavy)
- `economy` (default) -- browser may strip backgrounds, adjust colors

### Color remapping for print

Remap web colors to print-friendly equivalents:

```css
@media print {
  body {
    background: white !important;
    color: #1a1a1a !important;
  }

  /* Vibrant accent becomes muted for paper */
  .text-coral { color: #A03030 !important; }

  /* Dark backgrounds become white with borders */
  .dark-card {
    background: white !important;
    border: 1px solid #ccc !important;
  }
}
```

**Rule of thumb:** If it's readable on white paper at arm's length, it works.

---

## Typography

### Use points, not pixels

Points render consistently across browsers and printers:

```css
@media print {
  body {
    font-size: 10.5pt;
    line-height: 1.6;
  }
  h1 { font-size: 24pt; }
  h2 { font-size: 18pt; }
  h3 { font-size: 14pt; }
  code { font-size: 9pt; }
}
```

### Font stack for print

Serif fonts are more readable on paper:

```css
@media print {
  body { font-family: Georgia, 'Times New Roman', serif; }
  code, pre { font-family: 'Courier New', monospace; }
}
```

**Gotchas:**
- Custom web fonts may not load in print. Always have serif/sans-serif fallbacks.
- Remove light font weights (300, 200). Paper doesn't render thin strokes well.
- Remove text-shadow. It doesn't translate to print.
- Minimum legible body text: 9pt. Prefer 10-11pt.

---

## Images

```css
@media print {
  img {
    max-width: 100%;
    max-height: 3in;      /* prevent full-page images */
  }

  /* Hide decorative images */
  .hero-image,
  .background-image,
  .decorative {
    display: none !important;
  }

  /* Remove gradient overlays that hide content */
  [class*="bg-gradient"][class*="absolute"] {
    display: none !important;
  }
}
```

**Gotchas:**
- Background images don't print by default. Use `print-color-adjust: exact` or move content to `<img>` tags.
- Responsive images with `srcset` may not load correctly in print preview.
- High-resolution images slow down PDF generation significantly.

---

## Links

### Show URLs on printed links

```css
@media print {
  a[href^="http"]::after {
    content: " (" attr(href) ")";
    font-size: 0.8em;
    color: #666;
  }

  /* Don't show URLs on anchor links */
  a[href^="#"]::after { content: ""; }

  /* Don't show URLs on links that already describe their destination */
  a.no-print-url::after { content: ""; }
}
```

**Gotcha:** `attr(href)` shows the full URL, which can be very long. Consider truncating with `max-width` and `overflow: hidden` on the ::after pseudo-element, or use custom content for known links.

---

## Tables

```css
@media print {
  /* Repeat header on each page */
  thead { display: table-header-group; }
  tfoot { display: table-footer-group; }

  /* Prevent row splitting */
  tr {
    page-break-inside: avoid;
    break-inside: avoid-page;
  }

  /* Ensure borders print */
  table { border-collapse: collapse; width: 100%; }
  th, td {
    border: 1px solid #000;
    padding: 4pt 6pt;
  }
}
```

---

## Framework Gotchas

### Next.js

**next/image with `fill` breaks in print:**
```css
@media print {
  /* next/image fill uses absolute positioning -- force to static */
  [data-nimg="fill"],
  img[style*="position: absolute"] {
    position: static !important;
    width: 100% !important;
    height: auto !important;
  }

  /* Fix fill containers */
  [style*="position: relative"] {
    position: relative !important;
    overflow: visible !important;
  }
}
```

**Where to put print styles:** Use `@media print` in `globals.css`, not component-scoped styles. Print styles need global scope to override everything.

**Discussion:** [vercel/next.js#23039](https://github.com/vercel/next.js/discussions/23039)

### React / CSS-in-JS

- Print media queries must be included in component styles or a global stylesheet.
- Styled-components and Emotion support `@media print` blocks normally.
- Dynamic class names work fine -- print styles override by specificity.

### Tailwind CSS

```css
@media print {
  /* Kill viewport height constraints */
  .min-h-screen, .min-h-svh, .h-screen { min-height: auto !important; height: auto !important; }

  /* Dark mode on paper = unreadable */
  .dark { background: white !important; color: #1a1a1a !important; }

  /* Opacity renders poorly on paper */
  [class*="opacity-"] { opacity: 1 !important; }

  /* Fixed elements don't print */
  .fixed { position: static !important; }

  /* Overflow hidden clips content at page breaks */
  .overflow-hidden { overflow: visible !important; }
}
```

### Flexbox and Grid

Flex and grid containers do not handle page breaks correctly. Flatten them:

```css
@media print {
  .flex, .grid { display: block !important; }

  /* Or selectively: keep horizontal flex but allow breaking */
  .flex-col { display: block !important; }
}
```

**Exception:** Short flex rows (nav items, button groups) can remain flex if they fit on one line and you use `page-break-inside: avoid`.

---

## Testing

### DevTools emulation (quick iteration)

1. Open DevTools (F12)
2. Three-dot menu -> More tools -> Rendering
3. "Emulate CSS media type" -> print
4. Styles update in real-time

**Limitations:** Does not show page breaks, @page rules, or PDF headers/footers.

### Actual print preview (final check)

1. Cmd+P (Mac) / Ctrl+P (Windows)
2. Check "Background graphics" to see colors/images
3. Review page breaks, margins, and layout

### Checklist

Before declaring print styles complete:

- [ ] Web-only elements (nav, ads, widgets) are hidden
- [ ] Page breaks don't split mid-card, mid-table-row, or mid-image
- [ ] No orphaned single lines at top/bottom of pages
- [ ] All text is legible (minimum 9pt, dark on white)
- [ ] Images don't overflow onto the next page
- [ ] Links show URLs (or are clearly styled as text)
- [ ] Table headers repeat on each page
- [ ] Backgrounds are either hidden or forced with print-color-adjust
- [ ] No animations or transitions remain
- [ ] Flexbox/grid layouts don't cause blank pages
- [ ] min-height: 100vh constraints are removed
- [ ] Fixed positioning is converted to static
- [ ] Tested in actual print preview, not just DevTools emulation

---

## Agentic Workflow & Vibe Coding

- **Iterative Styling:** Do not expect perfect print layouts on the first try, as print rendering engines are finicky. Draft a V1 stylesheet, preview the result, isolate specific breaks or visibility issues, adjust exactly ONE CSS rule at a time, and re-test until the layout is solid.
- **Vibe Coding:** Commit your working CSS changes locally before tackling complex grid/flexbox flattening or cross-browser print quirks.

## Utility Classes

Add these to your project for print control:

```css
.no-print { }              /* hidden in print via @media print */
.print-only { display: none; }  /* hidden on screen, shown in print */
.print-break-before { }    /* page break before this element */
.print-break-after { }     /* page break after this element */
.no-print-url { }          /* suppress URL display on this link */

@media print {
  .no-print { display: none !important; }
  .print-only { display: block !important; }
  .print-break-before { page-break-before: always !important; break-before: page !important; }
  .print-break-after { page-break-after: always !important; break-after: page !important; }
}
```
