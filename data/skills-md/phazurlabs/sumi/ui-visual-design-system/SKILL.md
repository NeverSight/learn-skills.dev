---
name: ui-visual-design-system
description: "Visual design craft: typography scales, color theory (OKLCH, color-mix, light-dark), spacing systems, grids, visual hierarchy, elevation, iconography, and modern CSS (container queries, :has(), subgrid, @layer). Use when setting type and color, fixing hierarchy, or building a visual language."
---

# UI Visual Design System — Visual Excellence Framework

## Visual Design Philosophy

"Good design is as little design as possible. Less, but better — because it concentrates on the essential aspects, and the products are not burdened with non-essentials." — Dieter Rams

Visual design is the language through which interfaces communicate hierarchy, meaning, and emotional tone. Every visual decision — typeface, color, spacing, elevation — either clarifies or obscures the user's path. Pursue clarity ruthlessly.

### Core Principles

1. **Hierarchy is communication** — visual weight directs attention and reveals structure
2. **Consistency breeds trust** — systematic visual rules create predictable, professional interfaces
3. **White space is not empty space** — it is the most powerful tool for grouping, separating, and emphasizing
4. **Restraint over decoration** — every visual element must serve function; remove those that do not
5. **Accessibility is non-negotiable** — visual choices that exclude users are design failures

## Typography System

### Type Scale Design

Build a modular type scale using a consistent ratio. The most common scales:

- **Minor Third (1.200):** Subtle, elegant — suited for content-heavy apps
- **Major Third (1.250):** Balanced — good default for most applications
- **Perfect Fourth (1.333):** Strong contrast — suited for marketing and editorial
- **Augmented Fourth (1.414):** Dramatic — suited for expressive, creative products

**Example scale (Major Third, base 16px):**
```
xs:    10px (0.625rem)
sm:    13px (0.8125rem)
base:  16px (1rem)
lg:    20px (1.25rem)
xl:    25px (1.5625rem)
2xl:   31px (1.9375rem)
3xl:   39px (2.4375rem)
4xl:   49px (3.0625rem)
```

### Typography Best Practices

**Font Selection:**
- Limit to 2 typefaces maximum: one for headings, one for body (or one typeface at different weights)
- Sans-serif for UI elements and body text on screens (Inter, SF Pro, Roboto, Geist)
- Variable fonts reduce file size and enable fluid weight/width adjustment
- Ensure selected fonts support all required character sets and languages

**Readability Rules:**
- Body text: 16px minimum on web, 14px acceptable on desktop apps, never below 12px
- Line height: 1.4-1.6 for body text, 1.1-1.3 for headings
- Line length: 45-75 characters per line (measure) for optimal readability
- Paragraph spacing: 0.5-1.0x the body line height
- Letter spacing: slight increase (+0.01-0.02em) for all-caps text, reduce (-0.01em) for large headings

**Hierarchy Through Typography:**
- Use weight (bold/medium/regular) more than size for subtle hierarchy
- Reserve size jumps for major structural distinctions (page title vs. section heading)
- Color/opacity variation as tertiary hierarchy tool (primary text vs. secondary/caption)
- Limit distinct text styles to 6-8 across the entire application

## Color System

### Color Architecture

**Semantic Color Categories:**
- **Primary:** Brand identity color — used for key actions, active states, links
- **Secondary:** Complementary accent — used for secondary actions, highlights
- **Neutral:** Gray scale — used for text, borders, backgrounds, surfaces
- **Success:** Green spectrum — confirmations, completed states
- **Warning:** Amber/orange spectrum — caution, pending states
- **Error:** Red spectrum — errors, destructive actions, required indicators
- **Info:** Blue spectrum — informational messages, tips

**Color Scale Generation:**
- Generate 10-step scale per color (50-900) for systematic flexibility
- 50 = lightest (background tint), 500 = base value, 900 = darkest (text on light)
- Ensure perceptual uniformity across steps (use OKLCH or CIELAB color space)
- Tools: Leonardo by Adobe, Radix Colors, Tailwind color generator

### Accessibility Color Requirements

**Contrast Ratios (WCAG 2.2):**
- Normal text (<24px): 4.5:1 minimum against background
- Large text (>=24px or >=18.67px bold): 3:1 minimum
- UI components and graphical objects: 3:1 minimum against adjacent colors
- Enhanced (AAA): 7:1 for normal text, 4.5:1 for large text

**Color Independence:**
- Never use color as the sole indicator of meaning — pair with icons, text, or patterns
- Error states: red color + error icon + descriptive text
- Charts and graphs: use patterns, labels, and distinguishable hues (not just red/green)
- Test with color blindness simulators (protanopia, deuteranopia, tritanopia)

### Dark Mode Design

- Do not simply invert colors — redesign the elevation and emphasis model
- Dark mode backgrounds: not pure black (#000) — use desaturated dark grays (#121212-#1E1E1E)
- Reduce color saturation by 10-20% for dark backgrounds to prevent vibration
- Elevated surfaces get lighter in dark mode (opposite of light mode shadow approach)
- Text contrast: use 87% white (not 100%) for primary text on dark backgrounds to reduce eye strain

## Spacing System

### Spacing Scale

Use a base-4 or base-8 scale for consistent spacing:

**Base-4 scale (recommended for dense UIs):**
```
4px, 8px, 12px, 16px, 20px, 24px, 32px, 40px, 48px, 64px, 80px, 96px
```

**Base-8 scale (recommended for spacious UIs):**
```
8px, 16px, 24px, 32px, 48px, 64px, 80px, 96px, 128px
```

### Spacing Application Rules

- **Component internal padding:** 8-16px (compact) or 12-24px (comfortable)
- **Between related elements:** 8-12px (grouping by proximity — Gestalt law)
- **Between unrelated groups:** 24-32px (separation)
- **Section spacing:** 48-80px
- **Page margins:** 16px (mobile), 24-32px (tablet), 48-80px (desktop)

### Layout Grid

- **12-column grid** for maximum flexibility (divisible by 2, 3, 4, 6)
- **Column gutter:** 16-24px (responsive, wider on larger screens)
- **Max content width:** 1200-1440px for readability, centered with side padding
- Use CSS Grid and Flexbox — avoid float-based layouts
- **Subgrid** (CSS subgrid) for component-level alignment to parent grid

## Visual Hierarchy

### The Visual Hierarchy Toolkit (ordered by impact)

1. **Size** — larger elements command attention first
2. **Color/Contrast** — high-contrast and saturated colors draw the eye
3. **Position** — top-left (LTR languages) and center-screen hold priority
4. **Weight** — bolder elements stand out from regular weight
5. **White space** — isolated elements surrounded by space demand attention
6. **Motion** — animated elements capture attention (use sparingly)

### Hierarchy Application

- Every screen should have exactly one primary focal point — the main action or content
- Create clear layers: primary (what to notice), secondary (supporting context), tertiary (background/metadata)
- Squint test: when blurred, the visual structure should remain distinguishable
- Test hierarchy with grayscale rendering to verify it does not rely solely on color

## Elevation and Depth

### Elevation System

```
Level 0: Flat surface (0px shadow) — background, canvas
Level 1: Low (0 1px 3px rgba(0,0,0,0.12)) — cards, tiles
Level 2: Medium (0 4px 6px rgba(0,0,0,0.12)) — dropdowns, popovers
Level 3: High (0 8px 16px rgba(0,0,0,0.12)) — modals, dialogs
Level 4: Highest (0 16px 32px rgba(0,0,0,0.16)) — toasts, floating elements
```

- Higher elevation = closer to user = more important/temporary
- Use elevation consistently: persistent UI at level 0-1, transient UI at level 2-4
- Dark mode: use surface tint (lighter background) instead of shadow for elevation

## Iconography

### Icon Design Rules

- Consistent style: outline OR filled, not mixed (pick one system-wide)
- Minimum touch target: 44x44pt even if icon is visually 24x24
- Always pair icons with text labels in navigation — icons alone are ambiguous
- Standard sizes: 16px (inline), 20px (buttons), 24px (navigation), 32px (feature)
- Consistent stroke width across all icons (typically 1.5-2px at 24px size)

## Routing

For **typography and color in depth** — the type deep dive, the color deep dive,
and the section on making the two work together rather than separately: read
`references/typography-color-mastery.md`.

## Cross-Referencing

- For design token implementation, reference `design-systems-architecture`
- For accessibility requirements, reference `accessibility-inclusive-design`
- For motion and animation, reference `interaction-motion-design`
- For mobile-specific visual design, reference `mobile-ux-design`

## v3.0 Cross-References

The v3.0 upgrade introduces production CSS implementation references, Figma workflow integration, and multi-brand design system architecture that extend visual design systems into implementation and scale.

### Modern CSS Implementation — `component-patterns-code/references/css-modern-patterns.md`

The `component-patterns-code/references/css-modern-patterns.md` reference provides production CSS patterns that implement the visual design system principles above. Key coverage includes: **container queries** for component-level responsive design (replacing media query dependence); **`:has()` selector** for parent-aware styling enabling contextual visual variations; **anchor positioning** for tooltip, popover, and dropdown placement without JavaScript; **view transitions API** for smooth page and state transitions; **OKLCH color space** for perceptually uniform color manipulation (superior to HSL for generating accessible color scales as described in the Color System section); and **`@layer`** for cascade management in multi-team design system environments. Essential for translating visual design specifications into maintainable, modern CSS.

### Figma Design Tool Workflows — `figma-design-tool-workflows`

The `figma-design-tool-workflows` skill covers Figma-specific workflows for visual design system implementation. Includes: Figma variable modes for encoding the spacing scales, type scales, and color systems defined in this skill as structured design tokens; design token extraction pipelines that export Figma variables to Style Dictionary or Tokens Studio formats; and the MCP-powered design-to-code flywheel that maintains synchronization between Figma design system files and production CSS/component libraries. Directly applicable to maintaining visual consistency across design and code.

### Multi-Brand Theming Architecture — `design-systems-architecture/references/maturity-model-multi-brand.md`

The `design-systems-architecture/references/maturity-model-multi-brand.md` reference addresses scaling visual design systems across multiple brands, products, or white-label deployments. Covers multi-tier token architecture (global tokens, brand tokens, component tokens), theme switching strategies, and maturity model stages from single-product design systems through enterprise multi-brand platforms. Essential when the visual design system defined in this skill needs to support brand variants while maintaining structural consistency.

## Key Sources

- Rams, D. "Ten Principles for Good Design"
- Muller-Brockmann, J. "Grid Systems in Graphic Design"
- Material Design 3 color and typography specifications
- Apple Human Interface Guidelines visual design
- W3C WCAG 2.2 contrast requirements
