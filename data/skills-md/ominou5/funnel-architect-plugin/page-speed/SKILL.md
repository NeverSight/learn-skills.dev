---
name: page-speed
description: >
  Page speed optimization guidelines and implementation patterns.
  Ensures all funnel pages meet Core Web Vitals targets for LCP < 2.5s,
  FID < 100ms, and CLS < 0.1.
---

# Page Speed Optimization

Every funnel page must load fast. Slow pages kill conversions — a 1-second delay reduces conversions by 7%.

## Core Web Vitals Targets

| Metric | Target | Impact |
|---|---|---|
| LCP (Largest Contentful Paint) | < 2.5s | Main content visible |
| FID (First Input Delay) | < 100ms | Page is interactive |
| CLS (Cumulative Layout Shift) | < 0.1 | No visual jumping |
| TTFB (Time to First Byte) | < 800ms | Server responds fast |

## Required Optimizations

### 1. Critical CSS Inlining

Inline above-the-fold CSS directly in `<head>` to eliminate render-blocking:

```html
<head>
  <style>
    /* Critical: hero, nav, above-fold layout only */
    .hero { /* ... */ }
    .nav { /* ... */ }
    .cta-primary { /* ... */ }
  </style>
  <!-- Defer the rest -->
  <link rel="preload" href="styles.css" as="style" onload="this.onload=null;this.rel='stylesheet'">
  <noscript><link rel="stylesheet" href="styles.css"></noscript>
</head>
```

### 2. Image Optimization

```html
<!-- Always include width/height to prevent CLS -->
<img
  src="hero.webp"
  alt="Descriptive alt text"
  width="800"
  height="450"
  loading="lazy"
  decoding="async"
>

<!-- Responsive images with srcset -->
<img
  srcset="hero-400.webp 400w, hero-800.webp 800w, hero-1200.webp 1200w"
  sizes="(max-width: 600px) 400px, (max-width: 1000px) 800px, 1200px"
  src="hero-800.webp"
  alt="Descriptive alt text"
  width="800"
  height="450"
  loading="lazy"
>
```

### 3. Font Loading

```css
@font-face {
  font-family: 'BrandFont';
  src: url('brand-font.woff2') format('woff2');
  font-display: swap; /* Always include this */
  font-weight: 400;
}
```

```html
<!-- Preload critical fonts -->
<link rel="preload" href="brand-font.woff2" as="font" type="font/woff2" crossorigin>
```

### 4. Script Loading

```html
<!-- Defer non-critical scripts -->
<script defer src="analytics.js"></script>
<script defer src="interactions.js"></script>

<!-- Async for independent scripts -->
<script async src="third-party-widget.js"></script>

<!-- Never do this -->
<!-- <script src="blocking.js"></script> in <head> -->
```

### 5. Preconnect to Third Parties

```html
<head>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link rel="preconnect" href="https://www.googletagmanager.com">
</head>
```

## Performance Budget

| Resource | Budget |
|---|---|
| Total page weight | < 500KB |
| HTML | < 50KB |
| CSS | < 50KB |
| JavaScript | < 100KB |
| Images (above fold) | < 200KB |
| Fonts | < 100KB |
| Third-party scripts | < 50KB |

## Quick Audit Checklist

- [ ] Viewport meta tag present
- [ ] All images have width/height attributes
- [ ] Below-fold images use `loading="lazy"`
- [ ] No render-blocking scripts in `<head>`
- [ ] `font-display: swap` on all @font-face
- [ ] Critical CSS inlined
- [ ] Third-party origins preconnected
- [ ] No unused CSS/JS shipped
- [ ] Images in WebP/AVIF format
- [ ] Total page weight under 500KB
