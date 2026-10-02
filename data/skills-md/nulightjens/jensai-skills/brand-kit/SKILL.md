---
name: brand-kit
description: "Generate comprehensive visual brand kits and style guides as self-contained HTML files with companion markdown theme references. Use when the user asks to 'create a brand kit,' 'build a style guide,' 'design a brand system,' 'make a brand guide,' 'create brand guidelines,' or wants to establish or document the visual identity for a brand or project. Also use when the user mentions 'brand kit,' 'style guide,' 'design system,' 'brand guidelines,' 'visual identity,' 'brand standards,' or 'brand book.'"
---

# Brand Kit Generator

Generate production-quality visual brand kits as self-contained HTML files with companion markdown theme documentation. Two deliverables per brand: a visual HTML style guide and a text-based theme reference file.

## Workflow

Building a brand kit involves these steps:

1. Gather brand context (name, style direction, colors, fonts, content)
2. Select style direction preset and customize
3. Build the HTML brand kit (13 sections)
4. Build the companion markdown theme file
5. Open in browser for review

## Step 1: Gather Brand Context

Ask the user for these inputs. If they have existing branding files or HTML, read those first.

**Required:**
- Brand name
- Style direction / mood (see [references/brand-kit-structure.md](references/brand-kit-structure.md) "Style Direction Presets" for common options: Bold Creator, Dark Tech, Premium Modern)
- Primary accent color (hex)
- Font pairing (display + body); suggest Google Fonts pairings if the user has no preference

**Optional (read if provided):**
- Existing brand HTML or landing page to extract patterns from
- Logo files or wordmark specifications
- Brand content (product descriptions, taglines, value props, pricing)
- Competitor references or inspiration screenshots

If the user has an existing theme file (`.md`) or branding HTML, read it and extract all design tokens rather than asking for inputs already defined.

Never invent brand assets. Logos, wordmarks, taglines, and copy must come from files the user provides or from the brand's own site. If a required asset cannot be found, say so and ask instead of substituting a placeholder.

## Step 2: Select Style Direction

Reference [references/brand-kit-structure.md](references/brand-kit-structure.md) for the three preset directions:

- **Bold Creator.** Black bg, one high-contrast signal accent, condensed display font, 2px borders, zero radius, no shadows
- **Dark Tech.** Near-black bg, cool accent, geometric display font, 1px borders, small radius, subtle shadows
- **Premium Modern.** Light bg, vibrant accent, rounded display font, generous radius, layered shadows

Use the preset as a starting point, then customize every token to the specific brand.

## Step 3: Build the HTML Brand Kit

Create a single self-contained HTML file with:
- Embedded CSS (no external stylesheets)
- Google Fonts via CDN `<link>` tags
- No JavaScript dependencies (only a small IntersectionObserver script for nav highlighting)

### HTML Structure

```
Sticky sidebar nav (fixed left, 240px wide)
  └─ Section links with IntersectionObserver active highlighting
Main content (margin-left offset)
  └─ Cover section (brand name, version, metadata)
  └─ 13 guide sections (numbered 01-13)
  └─ Footer
```

### Required Sections (in order)

See [references/brand-kit-structure.md](references/brand-kit-structure.md) for detailed patterns for each section.

| # | Section | Key Elements |
|---|---------|-------------|
| 01 | Logo & Wordmark | Variations grid (primary/mono/reversed), construction rule blocks |
| 02 | Color System | Primary accent hero swatch with opacity variants, functional accent grid, neutral strip |
| 03 | Typography | Font specimen cards with character sets, weight sample rows |
| 04 | Type Hierarchy | Specimen rows: left metadata column + right live rendered sample |
| 05 | Spacing | Token table with accent-colored bars showing relative size |
| 06 | Borders & Surfaces | Border treatment demos, corner do/don't, elevation level cards |
| 07 | Buttons | State rows: default, hover, focus, disabled, loading + anatomy rule blocks |
| 08 | Cards | 3-state grid (default/hovered/featured) + shared-border grid demo |
| 09 | Badges | Badge specimens per category + anatomy rule blocks |
| 10 | Navigation | Live nav bar demo + specification rule blocks |
| 11 | Voice & Copy | 2-column voice card grid with live examples per element type |
| 12 | Do's & Don'ts | Side-by-side visual pairs with green checkmark / red X headers |
| 13 | Motion | Animation rule blocks |

### Critical HTML Patterns

**Sidebar nav with scroll tracking:**
```html
<aside class="sidebar">
  <a href="#section-id">Section Name</a>
</aside>
<script>
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        // Remove active from all, add to matching link
      }
    });
  }, { rootMargin: '-20% 0px -70% 0px' });
</script>
```

**Component state rows.** A flex row of cells, each with a label plus the rendered component:
```html
<div class="component-row">
  <div class="component-cell">
    <div class="component-cell-label">Default</div>
    [component in default state]
  </div>
  <div class="component-cell">
    <div class="component-cell-label">Hover</div>
    [component styled as hover]
  </div>
</div>
```

**Do/Don't pairs.** A 2-column grid with visual examples, not just text:
```html
<div class="do-dont-grid">
  <div class="do-card">
    <div class="do-card-header">✓ DO</div>
    <div class="do-dont-example">[actual correct rendering]</div>
    <div class="do-dont-text">Brief explanation</div>
  </div>
  <div class="dont-card">
    <div class="dont-card-header">✗ DON'T</div>
    <div class="do-dont-example">[actual incorrect rendering]</div>
    <div class="do-dont-text">Brief explanation</div>
  </div>
</div>
```

**Specification rule blocks.** A label plus a content grid:
```html
<div class="rule-block">
  <div class="rule-block-inner">
    <div class="rule-label">PROPERTY NAME</div>
    <div class="rule-content">Value and explanation with <code>code</code> inline</div>
  </div>
</div>
```

### Color Swatch Requirements

Every color swatch MUST show:
- Visual color block (minimum 120px height)
- Color name (display font)
- CSS token name (monospace, accent color)
- Hex value (monospace)
- Usage description (body font, muted color)

Primary accent swatch additionally shows opacity variants as horizontal bands.

### Component State Requirements

Every interactive component MUST show these states visually rendered side by side:
1. **Default.** Resting appearance
2. **Hover.** Color/bg change (render the hover state statically, not via :hover)
3. **Focus.** Outline ring
4. **Disabled.** Reduced opacity, not-allowed cursor
5. **Loading.** Text swap (display font: "LOADING...")

### Do's & Don'ts Requirements

Each pair MUST include an actual visual rendering of both the correct and incorrect version. Minimum 7 pairs covering: corners, shadows, gradients/flat, typography usage, color usage, section backgrounds, copy style.

## Step 4: Build the Companion Theme File

Create a markdown `.md` file alongside the HTML. See [references/theme-file-template.md](references/theme-file-template.md) for the exact template structure.

The theme file must document every design decision explicitly enough that any AI or designer can reproduce the style without seeing the HTML. Include:
- Every CSS custom property with hex, usage, and rules
- Every type scale entry with font, size, weight, spacing, height, color
- Every component's exact specs
- Every anti-pattern with reasoning
- Copy-paste-ready `:root {}` block

## Step 5: Review

Open the HTML file in the browser (`open` on macOS, `xdg-open` on Linux, `start` on Windows). Tell the user both files are ready and summarize the section count and key design decisions.

## Output Files

Place both files in a `themes/` directory within the project:
```
project/
└── themes/
    ├── brand-kit.html          (visual style guide)
    └── [style-name].md         (theme reference)
```

If the user specifies a different output location, use that instead.

## References

- **Section structure and patterns:** [references/brand-kit-structure.md](references/brand-kit-structure.md)
- **Theme markdown template:** [references/theme-file-template.md](references/theme-file-template.md)
