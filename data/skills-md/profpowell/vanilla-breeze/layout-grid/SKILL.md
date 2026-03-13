---
name: layout-grid
description: Design-focused grid layout system with fluid scaling, responsive columns, and resolution-independent patterns. Use when creating page layouts, card grids, or multi-column designs.
allowed-tools: Read, Write, Edit
---

# Layout Grid Skill

This skill covers design grid systems for page layout—fluid, resolution-independent grids that scale proportionally across all viewport sizes without fixed breakpoints.

## Philosophy

Layout grids should:
1. **Scale fluidly** - No fixed pixel values; use relative units throughout
2. **Work at any resolution** - Single grid system, not breakpoint-specific grids
3. **Maintain proportions** - Gutters and margins scale with content
4. **Support composition** - Enable both rigid alignment and flexible content areas

---

## Fluid Grid Token System

Define grid properties as fluid custom properties that scale between viewport bounds.

### Core Grid Tokens

```css
@layer tokens {
  :root {
    /* ==================== GRID FOUNDATION ==================== */

    /* Viewport bounds for fluid calculations */
    --grid-min-width: 20rem;   /* 320px - mobile */
    --grid-max-width: 90rem;   /* 1440px - large desktop */

    /* Content max-width (readable area) */
    --content-max-width: 75rem;  /* 1200px */

    /* ==================== FLUID GUTTER ==================== */

    /* Gutter scales from 1rem to 2rem based on viewport */
    --grid-gutter: clamp(1rem, 0.5rem + 2vw, 2rem);

    /* ==================== FLUID MARGIN ==================== */

    /* Page margin scales from 1rem to 4rem */
    --grid-margin: clamp(1rem, -0.5rem + 6vw, 4rem);

    /* ==================== COLUMN SYSTEM ==================== */

    --grid-columns: 12;

    /* Single column width (fluid) */
    --grid-column-width: calc(
      (100% - (var(--grid-columns) - 1) * var(--grid-gutter)) / var(--grid-columns)
    );
  }
}
```

### The Fluid Scaling Formula

Fluid values use `clamp()` with a calculated preferred value:

```
clamp(min, preferred, max)
preferred = min + (max - min) × viewport-factor
viewport-factor = (100vw - min-viewport) / (max-viewport - min-viewport)
```

Simplified pattern:

```css
/* Scale from 1rem (320px) to 2rem (1440px) */
--value: clamp(1rem, calc(0.5rem + 1.5vw), 2rem);
```

---

## Page Layout Container

### The Fluid Container

```css
@layer layout {
  /* Main content container */
  body > * {
    --_container-width: min(
      var(--content-max-width),
      100% - var(--grid-margin) * 2
    );

    width: var(--_container-width);
    margin-inline: auto;
  }

  /* Full-bleed sections */
  [data-layout="full"] {
    width: 100%;
    padding-inline: var(--grid-margin);
  }

  /* Wide sections (larger than content, not full) */
  [data-layout="wide"] {
    --_container-width: min(
      var(--grid-max-width),
      100% - var(--grid-margin) * 2
    );
  }
}
```

### Named Grid Areas for Page Layout

```css
@layer layout {
  body {
    display: grid;
    grid-template-columns:
      [full-start] var(--grid-margin)
      [wide-start] minmax(0, 1fr)
      [content-start] min(var(--content-max-width), 100%)
      [content-end] minmax(0, 1fr)
      [wide-end] var(--grid-margin)
      [full-end];
    grid-template-rows: auto 1fr auto;
  }

  /* Content aligns to content area */
  body > * {
    grid-column: content;
  }

  /* Full-bleed elements span full width */
  body > [data-layout="full"] {
    grid-column: full;
  }

  /* Wide elements extend past content */
  body > [data-layout="wide"] {
    grid-column: wide;
  }
}
```

---

## Responsive Card Grids

### Auto-Fit Pattern (Recommended)

Cards flow into available columns automatically:

```css
@layer components {
  card-grid {
    display: grid;
    grid-template-columns: repeat(
      auto-fit,
      minmax(min(100%, 18rem), 1fr)
    );
    gap: var(--grid-gutter);
  }
}
```

**How it works:**
- `auto-fit` creates as many columns as fit
- `minmax(min(100%, 18rem), 1fr)` ensures cards are at least 18rem but stretch to fill space
- `min(100%, 18rem)` prevents overflow on narrow viewports

### Auto-Fill vs Auto-Fit

| Property | Behavior | Use When |
|----------|----------|----------|
| `auto-fit` | Collapses empty tracks | Cards should stretch to fill row |
| `auto-fill` | Keeps empty tracks | Maintain consistent column widths |

```css
/* auto-fit: cards stretch */
grid-template-columns: repeat(auto-fit, minmax(15rem, 1fr));

/* auto-fill: consistent widths, may leave gaps */
grid-template-columns: repeat(auto-fill, minmax(15rem, 1fr));
```

### Constrained Column Count

Limit maximum columns while staying fluid:

```css
card-grid {
  --_min-card-width: 18rem;
  --_max-columns: 4;

  display: grid;
  grid-template-columns: repeat(
    auto-fit,
    minmax(
      max(
        var(--_min-card-width),
        calc((100% - var(--grid-gutter) * (var(--_max-columns) - 1)) / var(--_max-columns))
      ),
      1fr
    )
  );
  gap: var(--grid-gutter);
}
```

---

## Explicit Column Grids

### 12-Column Grid

```css
@layer layout {
  [data-grid="12"] {
    display: grid;
    grid-template-columns: repeat(12, 1fr);
    gap: var(--grid-gutter);
  }

  /* Span utilities */
  [data-span="1"] { grid-column: span 1; }
  [data-span="2"] { grid-column: span 2; }
  [data-span="3"] { grid-column: span 3; }
  [data-span="4"] { grid-column: span 4; }
  [data-span="5"] { grid-column: span 5; }
  [data-span="6"] { grid-column: span 6; }
  [data-span="7"] { grid-column: span 7; }
  [data-span="8"] { grid-column: span 8; }
  [data-span="9"] { grid-column: span 9; }
  [data-span="10"] { grid-column: span 10; }
  [data-span="11"] { grid-column: span 11; }
  [data-span="12"] { grid-column: span 12; }
}
```

### Responsive Column Spans

Use container queries for component-level responsiveness:

```css
@layer components {
  feature-grid {
    container-type: inline-size;
    display: grid;
    grid-template-columns: repeat(12, 1fr);
    gap: var(--grid-gutter);
  }

  feature-grid > * {
    grid-column: span 12;  /* Full width by default */
  }

  @container (min-width: 30rem) {
    feature-grid > * {
      grid-column: span 6;  /* Half width */
    }
  }

  @container (min-width: 50rem) {
    feature-grid > * {
      grid-column: span 4;  /* Third width */
    }

    feature-grid > :first-child {
      grid-column: span 8;  /* Featured item wider */
    }
  }
}
```

---

## Subgrid for Alignment

Subgrid enables nested elements to align with parent grid tracks.

### Card Grid with Aligned Content

```css
@layer components {
  /* Parent defines the column structure */
  product-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(min(100%, 18rem), 1fr));
    /* Define row tracks for card internals */
    grid-auto-rows: auto 1fr auto;  /* image, content, actions */
    gap: var(--grid-gutter);
  }

  /* Cards span 3 rows and inherit row tracks */
  product-card {
    display: grid;
    grid-row: span 3;
    grid-template-rows: subgrid;
    gap: var(--size-m);
  }

  product-card img { grid-row: 1; }
  product-card .content { grid-row: 2; }
  product-card .actions { grid-row: 3; }
}
```

### Form Alignment with Subgrid

```css
@layer components {
  form {
    display: grid;
    grid-template-columns: max-content 1fr;
    gap: var(--size-m);
  }

  form-field {
    display: grid;
    grid-column: span 2;
    grid-template-columns: subgrid;
  }

  form-field label {
    grid-column: 1;
  }

  form-field input,
  form-field select {
    grid-column: 2;
  }
}
```

---

## Asymmetric Layouts

### Content + Sidebar

```css
@layer layout {
  [data-layout="sidebar"] {
    display: grid;
    grid-template-columns: 1fr min(20rem, 30%);
    gap: var(--grid-gutter);
  }

  /* Responsive: stack on narrow */
  @container (max-width: 50rem) {
    [data-layout="sidebar"] {
      grid-template-columns: 1fr;
    }
  }
}
```

### Golden Ratio Split

```css
@layer layout {
  [data-layout="golden"] {
    display: grid;
    /* 1.618:1 ratio */
    grid-template-columns: 1.618fr 1fr;
    gap: var(--grid-gutter);
  }
}
```

### Feature + Gallery

```css
@layer layout {
  [data-layout="feature-gallery"] {
    display: grid;
    grid-template-columns: 2fr 1fr 1fr;
    grid-template-rows: 1fr 1fr;
    gap: var(--grid-gutter);
  }

  [data-layout="feature-gallery"] > :first-child {
    grid-row: span 2;
  }
}
```

---

## Fluid Gap Scaling

### Gap Token Scale

```css
:root {
  /* Gaps scale with viewport */
  --gap-xs: clamp(0.25rem, 0.125rem + 0.5vw, 0.5rem);
  --gap-sm: clamp(0.5rem, 0.25rem + 1vw, 1rem);
  --gap-md: clamp(1rem, 0.5rem + 2vw, 2rem);
  --gap-lg: clamp(1.5rem, 0.75rem + 3vw, 3rem);
  --gap-xl: clamp(2rem, 1rem + 4vw, 4rem);
}
```

### Using Gap Tokens

```css
card-grid {
  gap: var(--gap-md);
}

section-grid {
  gap: var(--gap-lg);
}

icon-grid {
  gap: var(--gap-sm);
}
```

---

## Resolution-Independent Patterns

### Using Proportional Units

| Unit | Use For | Example |
|------|---------|---------|
| `fr` | Flexible column widths | `1fr 2fr 1fr` |
| `%` | Proportional within container | `max-width: 80%` |
| `vw/vh` | Viewport-relative | `width: 50vw` |
| `cqi/cqw` | Container-relative | `width: 50cqi` |
| `rem` | Root-relative sizing | `gap: 1.5rem` |
| `ch` | Character-based width | `max-width: 65ch` |

### Never Use Fixed Pixels For:
- Column widths
- Gutters and gaps
- Margins and padding
- Container max-widths (use `rem` instead)

### Pixel-Safe Uses:
- Border widths (`1px`, `2px`)
- Box shadows
- Fine visual details

---

## Common Layout Patterns

### Holy Grail Layout

```css
body {
  display: grid;
  grid-template:
    "header header header" auto
    "nav    main   aside" 1fr
    "footer footer footer" auto
    / minmax(10rem, 15rem) 1fr minmax(10rem, 20rem);
  min-height: 100vh;
  gap: var(--grid-gutter);
}

header { grid-area: header; }
nav { grid-area: nav; }
main { grid-area: main; }
aside { grid-area: aside; }
footer { grid-area: footer; }

/* Stack on mobile */
@media (max-width: 60rem) {
  body {
    grid-template:
      "header" auto
      "nav"    auto
      "main"   1fr
      "aside"  auto
      "footer" auto
      / 1fr;
  }
}
```

### Magazine Layout

```css
article-layout {
  display: grid;
  grid-template-columns:
    [full-start] 1fr
    [main-start] minmax(0, 65ch)
    [main-end] 1fr
    [full-end];
  gap: var(--grid-gutter);
}

article-layout > * {
  grid-column: main;
}

article-layout > figure,
article-layout > blockquote {
  grid-column: full;
}
```

### Masonry-Style (CSS Grid Approximation)

```css
masonry-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(min(100%, 15rem), 1fr));
  grid-auto-rows: 1rem;
  gap: var(--grid-gutter);
}

masonry-grid > * {
  /* Items span variable rows based on content */
  grid-row: span var(--rows, 10);
}
```

Note: True masonry requires JavaScript to calculate `--rows` or wait for CSS `masonry` property support.

---

## Integration with Container Queries

### Component-Level Grid Responsiveness

```css
@layer components {
  dashboard-widget {
    container-type: inline-size;
    display: grid;
    gap: var(--size-m);
  }

  /* Single column by default */
  dashboard-widget {
    grid-template-columns: 1fr;
  }

  /* Two columns when widget is wide enough */
  @container (min-width: 25rem) {
    dashboard-widget {
      grid-template-columns: 1fr 1fr;
    }
  }

  /* Three columns with sidebar */
  @container (min-width: 45rem) {
    dashboard-widget {
      grid-template-columns: 2fr 1fr 1fr;
    }
  }
}
```

---

## Debug Grid Overlay

Visualize grid during development:

```css
/* Add to :root for development */
:root {
  --debug-grid: 0;
}

[data-grid],
[data-layout] {
  position: relative;
}

[data-grid]::before,
[data-layout]::before {
  content: "";
  position: absolute;
  inset: 0;
  pointer-events: none;
  background: repeating-linear-gradient(
    90deg,
    oklch(60% 0.15 250 / 0.1) 0,
    oklch(60% 0.15 250 / 0.1) var(--grid-column-width),
    transparent var(--grid-column-width),
    transparent calc(var(--grid-column-width) + var(--grid-gutter))
  );
  opacity: var(--debug-grid);
  z-index: 9999;
}
```

Toggle with: `document.documentElement.style.setProperty('--debug-grid', '1')`

---

## Checklist

When implementing grid layouts:

### Tokens
- [ ] Grid gutter uses `clamp()` for fluid scaling
- [ ] Page margin scales with viewport
- [ ] No fixed pixel values for layout dimensions
- [ ] Content max-width defined in `rem`

### Grid Structure
- [ ] Use `auto-fit`/`auto-fill` for card grids
- [ ] `minmax()` includes `min(100%, value)` to prevent overflow
- [ ] Named grid areas for page layout
- [ ] `fr` units for flexible column widths

### Responsiveness
- [ ] Container queries for component-level changes
- [ ] Media queries only for page-level layout shifts
- [ ] Single grid system works across all viewports
- [ ] Test at arbitrary widths, not just standard breakpoints

### Alignment
- [ ] Subgrid used for nested element alignment
- [ ] Consistent gap tokens throughout
- [ ] Items align to baseline grid where appropriate

## Related Skills

- **css-author** - @layer organization, container queries, @scope
- **typography** - Baseline grid, vertical rhythm
- **responsive-images** - Images in grid contexts
- **progressive-enhancement** - CSS-only responsive patterns
