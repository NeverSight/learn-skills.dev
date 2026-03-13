---
name: performance-analyzer
description: CSS performance analysis covering bundle size, selector complexity, render-blocking resources, critical CSS, and optimization strategies. Use when CSS performance is slow or bundle size is too large.
allowed-tools: Read, Grep, Glob, Bash
---

# Performance Analyzer Skill

This skill analyzes CSS performance and identifies optimization opportunities. I'll examine bundle size, selector efficiency, render performance, and suggest specific improvements to make your CSS faster.

## What I Analyze

### Bundle Analysis
- Total CSS file size
- Unused CSS percentage
- Duplicate rules
- Minification potential
- Compression ratios

### Selector Performance
- Selector complexity
- Expensive selectors
- Over-specific rules
- Selector matching speed

### Render Performance
- Render-blocking CSS
- Critical CSS opportunities
- Paint/layout triggers
- Animation performance

### Loading Strategy
- CSS delivery method
- Code splitting potential
- Async loading opportunities
- Caching strategy

## Performance Metrics

### Key Indicators

**First Contentful Paint (FCP)**
- When first content appears
- Target: < 1.8s

**Largest Contentful Paint (LCP)**
- When main content visible
- Target: < 2.5s

**Cumulative Layout Shift (CLS)**
- Visual stability
- Target: < 0.1

**CSS Bundle Size**
- Total downloaded CSS
- Target: < 50KB gzipped for initial load

**Unused CSS**
- Percentage not used on page
- Target: < 20% unused

## Bundle Size Analysis

### File Size Audit

```bash
# Check CSS file sizes
ls -lh dist/*.css

# Example output:
# styles.css        250KB (uncompressed)
# styles.min.css    180KB (minified)
# styles.min.css.gz  45KB (gzipped)
```

### Optimization Potential

```
Original:     250KB (100%)
Minified:     180KB (72%)  - Remove whitespace, comments
Gzipped:      45KB  (18%)  - Compression
Unused removed: 30KB (12%)  - Remove unused CSS
Optimized:    30KB  (12%)  - Final target

Potential savings: 88%
```

### Bundle Composition

```
Analyze what's in your bundle:

Vendor CSS (Bootstrap, etc.):  120KB (48%)
Component styles:               80KB (32%)
Utility classes:                30KB (12%)
Global styles:                  20KB (8%)

Recommendations:
1. Remove unused Bootstrap components
2. Use PurgeCSS for utilities
3. Split vendor from custom CSS
```

## Selector Performance

### Expensive Selectors

```css
/* ❌ VERY SLOW - Universal selector with pseudo */
*:hover {
  cursor: pointer;
}

/* ❌ SLOW - Descendant with universal */
.container * {
  box-sizing: border-box;
}

/* ❌ SLOW - Complex attribute selectors */
[class^="icon-"][class$="-large"] {
  font-size: 2rem;
}

/* ❌ SLOW - Deep nesting */
.nav ul li a span.icon {
  color: blue;
}

/* ✓ FAST - Single class */
.icon-large {
  font-size: 2rem;
}

/* ✓ FAST - Low specificity */
.nav-icon {
  color: blue;
}
```

### Selector Complexity Scoring

```
Complexity Score (Lower is better):

Single class:              1 point (.button)
Element selector:          1 point (div)
Class + element:           2 points (div.button)
Descendant:                +1 per level (.nav .item .link = 3)
Pseudo-class:              +1 (:hover)
Attribute:                 +2 ([type="text"])
Complex attribute:         +3 ([class*="btn-"])
Universal:                 +5 (*)

Target: Average < 5 points per selector
```

### Refactoring Examples

```css
/* BEFORE: Complexity 8 */
.container .sidebar nav ul li a:hover {
  color: blue;
}
/* Score: 1 + 1 + 1 + 1 + 1 + 1 + 1 + 1 = 8 */

/* AFTER: Complexity 2 */
.sidebar-link:hover {
  color: blue;
}
/* Score: 1 + 1 = 2 */

/* BEFORE: Complexity 10 */
div[class^="card-"][class$="-featured"]:not(.disabled) {
  border: 2px solid gold;
}
/* Score: 1 + 3 + 3 + 2 + 1 = 10 */

/* AFTER: Complexity 1 */
.card--featured {
  border: 2px solid gold;
}
/* Score: 1 */
```

## Render Performance

### Properties That Trigger Reflow (Layout)

```css
/* ❌ EXPENSIVE - Triggers layout recalculation */
.animated {
  animation: move 1s;
}

@keyframes move {
  from { left: 0; width: 100px; }
  to { left: 100px; width: 200px; }
}

/* These properties trigger layout:
 * width, height, padding, margin, border
 * top, right, bottom, left
 * font-size, line-height
 * display, position, float
 */
```

### Properties That Trigger Paint

```css
/* ⚠️ MODERATE - Triggers repaint */
.animated {
  animation: fade 1s;
}

@keyframes fade {
  from { background: red; }
  to { background: blue; }
}

/* These properties trigger paint:
 * color, background, box-shadow
 * border-radius, border-style
 * visibility, outline
 */
```

### Compositor-Only Properties (FAST)

```css
/* ✓ OPTIMAL - GPU accelerated */
.animated {
  animation: slide 1s;
}

@keyframes slide {
  from { transform: translateX(0); opacity: 0; }
  to { transform: translateX(100px); opacity: 1; }
}

/* These are compositor-only:
 * transform (translate, rotate, scale)
 * opacity
 */
```

### Animation Performance Comparison

```css
/* ❌ POOR PERFORMANCE */
@keyframes slideIn {
  from { left: -100px; }    /* Triggers layout */
  to { left: 0; }
}

/* Performance impact:
 * - Recalculates layout (expensive)
 * - Repaints (expensive)
 * - Composites (cheap)
 * Total: ~50ms per frame
 * Result: Janky animation < 60fps
 */

/* ✓ GOOD PERFORMANCE */
@keyframes slideIn {
  from { transform: translateX(-100px); }  /* Compositor only */
  to { transform: translateX(0); }
}

/* Performance impact:
 * - Composites (cheap)
 * Total: ~1-2ms per frame
 * Result: Smooth animation @ 60fps
 */
```

## Critical CSS Strategy

### What is Critical CSS?

CSS required for above-the-fold content. Should be inlined in `<head>` to eliminate render-blocking requests.

### Critical CSS Identification

```css
/* CRITICAL - Above the fold */
/* Inline these in <head> */

/* Reset */
*, *::before, *::after {
  box-sizing: border-box;
}

body {
  margin: 0;
  font-family: system-ui;
}

/* Header (visible immediately) */
.header {
  display: flex;
  padding: 1rem;
  background: white;
}

.logo {
  font-size: 1.5rem;
}

.nav {
  display: flex;
  gap: 1rem;
}

/* Hero section (above fold) */
.hero {
  min-height: 400px;
  padding: 4rem 2rem;
  background: #f0f0f0;
}

.hero-title {
  font-size: 3rem;
  margin: 0;
}

/* NON-CRITICAL - Load async */
/* Footer, modals, below-fold content */
```

### Implementation

```html
<!DOCTYPE html>
<html>
<head>
  <!-- INLINE CRITICAL CSS -->
  <style>
    /* Critical CSS here (< 14KB) */
    *, *::before, *::after { box-sizing: border-box; }
    body { margin: 0; font-family: system-ui; }
    .header { /* ... */ }
    .hero { /* ... */ }
  </style>

  <!-- PRELOAD FULL STYLESHEET -->
  <link rel="preload" href="/styles.css" as="style">

  <!-- LOAD FULL STYLESHEET ASYNC -->
  <link rel="stylesheet" href="/styles.css" media="print" onload="this.media='all'">
  <noscript><link rel="stylesheet" href="/styles.css"></noscript>
</head>
<body>
  <!-- Content -->
</body>
</html>
```

## CSS Loading Optimization

### Loading Strategy Analysis

```css
/* ❌ POOR - Single large bundle, render-blocking */
<link rel="stylesheet" href="/styles.css">  <!-- 250KB -->

/* Issues:
 * - Blocks rendering until entire file downloads
 * - Contains unused CSS
 * - No prioritization
 */

/* ✓ BETTER - Critical CSS inline + async full */
<style>/* Critical CSS */</style>
<link rel="preload" href="/styles.css" as="style">
<link rel="stylesheet" href="/styles.css" media="print" onload="this.media='all'">

/* Benefits:
 * - Immediate rendering with critical CSS
 * - Non-blocking full stylesheet load
 * - Faster FCP
 */

/* ✓ BEST - Critical inline + route-based splitting */
<style>/* Critical CSS */</style>
<link rel="preload" href="/common.css" as="style">
<link rel="preload" href="/page.css" as="style">
<link rel="stylesheet" href="/common.css" media="print" onload="this.media='all'">
<link rel="stylesheet" href="/page.css" media="print" onload="this.media='all'">

/* Benefits:
 * - Only loads CSS needed for current page
 * - Common styles cached across pages
 * - Optimal bundle size
 */
```

### HTTP/2 Considerations

```html
<!-- With HTTP/2, can load multiple files efficiently -->
<link rel="stylesheet" href="/reset.css">      <!-- 2KB -->
<link rel="stylesheet" href="/typography.css"> <!-- 5KB -->
<link rel="stylesheet" href="/layout.css">     <!-- 8KB -->
<link rel="stylesheet" href="/components.css"> <!-- 15KB -->

<!-- Advantages:
  * Better caching (only changed files re-download)
  * Parallel loading
  * Selective loading possible
-->
```

## Optimization Tools

### Analysis Tools

```bash
# CSS Stats - Analyze CSS complexity
npx cssstats styles.css > stats.json

# Coverage - Find unused CSS (Chrome DevTools)
# DevTools → Coverage → Record → Reload

# Lighthouse - Performance audit
lighthouse https://example.com --only-categories=performance

# Bundle analyzer
npx webpack-bundle-analyzer stats.json
```

### Optimization Tools

```bash
# Minification - Remove whitespace
npx cssnano styles.css styles.min.css

# PurgeCSS - Remove unused CSS
npx purgecss --css styles.css --content '**/*.html' --output dist/

# Critical - Extract critical CSS
npx critical index.html --base dist --inline > optimized.html

# Compression - Gzip/Brotli
gzip -9 styles.css          # Gzip
brotli -q 11 styles.css     # Brotli (better)
```

## Performance Budget

### Set Targets

```yaml
# performance-budget.yml

# Bundle sizes
css-total: 50KB        # Total CSS (gzipped)
css-critical: 14KB     # Inline critical CSS
css-vendor: 20KB       # Third-party CSS

# Metrics
first-contentful-paint: 1.8s
largest-contentful-paint: 2.5s
cumulative-layout-shift: 0.1

# Code quality
unused-css: 20%         # Max unused CSS
avg-selector-depth: 3   # Max avg nesting
specificity-avg: 30     # Max avg specificity
```

### Monitor & Enforce

```bash
# Add to CI/CD pipeline
npm run build
npm run analyze-bundle

# Check if bundle exceeds budget
if [ $(stat -f%z dist/styles.css.gz) -gt 51200 ]; then
  echo "❌ CSS bundle exceeds 50KB limit"
  exit 1
fi
```

## Performance Checklist

### Bundle Size
- [ ] Minified CSS (cssnano, clean-css)
- [ ] Gzip/Brotli compression enabled
- [ ] Unused CSS removed (PurgeCSS)
- [ ] Duplicate rules eliminated
- [ ] Bundle size < 50KB (gzipped)

### Selectors
- [ ] Average depth < 3 levels
- [ ] No universal selectors in production
- [ ] Complex attribute selectors removed
- [ ] BEM or similar flat methodology

### Rendering
- [ ] Animations use transform/opacity only
- [ ] No layout-triggering properties in animations
- [ ] will-change used appropriately (and removed)
- [ ] contain property used where appropriate

### Loading
- [ ] Critical CSS inlined (< 14KB)
- [ ] Non-critical CSS loaded async
- [ ] CSS split by route/feature
- [ ] HTTP caching configured

### Monitoring
- [ ] Performance budget set
- [ ] Lighthouse CI configured
- [ ] Bundle size tracked
- [ ] Metrics monitored

## Example Analysis Report

**Input**: Analyze `styles.css` (250KB)

**Report**:

```markdown
# CSS Performance Analysis

## Bundle Size 🔴
- **Uncompressed**: 250KB
- **Minified**: 180KB (28% savings)
- **Gzipped**: 45KB (82% total savings)
- **Status**: ❌ Exceeds 50KB budget

### Recommendations:
1. Remove unused CSS (estimated 70KB savings)
2. Split vendor CSS (Bootstrap) from custom
3. Implement code splitting by route

## Selector Performance ⚠️
- **Average depth**: 4.2 levels
- **Complex selectors**: 23 found
- **Universal selectors**: 5 found

### Top Issues:
1. `.container * { }` - Universal descendant (line 45)
2. `#nav ul li a span` - 5 levels deep (line 234)
3. `[class*="btn-"]:not(.disabled)` - Complex attribute (line 567)

### Recommendations:
1. Refactor to BEM methodology
2. Replace universal selectors with specific classes
3. Flatten deeply nested selectors

## Render Performance ✓
- **Layout-triggering animations**: 2 found
- **Paint-heavy properties**: 15 instances
- **Compositor-only**: 8 animations

### Issues:
1. `@keyframes slideIn` uses `left` property (line 890)
   - **Fix**: Use `transform: translateX()`

2. `.animated` animates `width` (line 923)
   - **Fix**: Use `transform: scaleX()`

## Critical CSS ⚠️
- **Above-fold CSS**: ~35KB
- **Currently inline**: 0KB
- **Render-blocking**: Yes

### Recommendations:
1. Extract critical CSS (header, hero, navigation)
2. Inline critical CSS (target < 14KB)
3. Load remaining CSS async

## Priority Actions:
1. 🔴 **HIGH**: Remove unused CSS (↓ 70KB)
2. 🟠 **MEDIUM**: Inline critical CSS (improve FCP by ~1s)
3. 🟡 **LOW**: Refactor selectors (improve maintainability)

## Expected Impact:
- Bundle size: 250KB → 50KB (80% reduction)
- FCP: 3.2s → 1.5s (53% improvement)
- LCP: 4.5s → 2.2s (51% improvement)
```

## Just Ask!

Request performance analysis:
- "Analyze this CSS file for performance"
- "Find expensive selectors"
- "Identify critical CSS"
- "Check my animation performance"
- "Suggest bundle optimizations"

I'll provide actionable optimization recommendations!
