---
name: Layout Designer
slug: layout-designer
description: Expert page layout and grid system design
category: design
complexity: simple
version: "1.0.0"
author: "ID8Labs"
triggers:
  - "layout design"
  - "page layout"
  - "grid system"
  - "design layout"
  - "composition"
tags:
  - layout
  - grid
  - design
  - composition
  - UI
---

# Layout Designer

A layout expert that creates beautiful, functional page compositions using grid systems, spacing, and visual hierarchy principles. This skill combines design theory, responsive design patterns, and modern CSS capabilities to build layouts that work across all devices and content types.

Whether you need a landing page hero, a dashboard interface, or an editorial layout, this skill provides structured approaches to composition that balance aesthetics with usability.

## Core Workflows

### Workflow 1: Landing Page Layout
1. Define page sections:
   - Hero (above fold)
   - Features/Benefits
   - Social proof
   - Pricing/CTA
   - FAQ/Footer
2. Design each section:
   - Choose layout pattern
   - Define grid structure
   - Plan spacing and rhythm
   - Set visual hierarchy
3. Create responsive breakpoints:
   - Mobile: Single column, stacked
   - Tablet: 2-column hybrid
   - Desktop: Full multi-column
4. Specify component placement and sizing
5. Generate HTML/CSS structure

### Workflow 2: Dashboard/App Layout
1. Map information architecture:
   - Navigation (sidebar, top bar, tabs)
   - Primary content area
   - Secondary panels (filters, details)
   - Status/notification areas
2. Choose layout system:
   - Sidebar + content
   - Holy grail (header, 2 sidebars, footer)
   - Split panel
   - Masonry/card grid
3. Define grid and spacing:
   - Base unit (4px, 8px)
   - Column structure
   - Gutter widths
   - Container max-widths
4. Plan responsive behavior:
   - Mobile: Collapsed nav, stacked panels
   - Tablet: Partial collapse
   - Desktop: Full layout
5. Provide Tailwind/CSS Grid code

### Workflow 3: Editorial/Content Layout
1. Understand content:
   - Text-heavy vs. image-heavy
   - Reading length
   - Media types (images, videos, quotes, code)
2. Design reading experience:
   - Optimal line length (60-75 chars)
   - Generous whitespace
   - Clear hierarchy
   - Strategic media placement
3. Choose composition:
   - Single column (blog post)
   - Multi-column (magazine)
   - Asymmetric (editorial)
   - Modular grid (Pinterest-style)
4. Design special elements:
   - Pull quotes
   - Image galleries
   - Sidebars/callouts
   - Author bios
5. Ensure readability across devices

### Workflow 4: Grid System Creation
1. Define requirements:
   - Content types
   - Flexibility needed
   - Breakpoint strategy
2. Create grid specification:
   - Number of columns (12, 16, 24)
   - Gutter width
   - Margin/padding system
   - Container sizes
3. Build spacing scale:
   - Base unit (4px or 8px)
   - Scale progression (0.5, 1, 2, 3, 4, 6, 8, 12, 16, 24, 32)
4. Document layout patterns:
   - Common column combinations
   - Nested grid usage
   - Breakout/bleed patterns
5. Generate framework config

## Quick Reference

| Action | Command/Trigger |
|--------|-----------------|
| Landing page layout | "Design a landing page for [product]" |
| Dashboard layout | "Create dashboard layout for [use case]" |
| Blog/article layout | "Design a blog post layout" |
| Grid system | "Build a grid system for [project]" |
| Fix layout | "Improve the layout of [page/section]" |
| Responsive strategy | "Make this layout responsive" |

## Layout Patterns Library

### Hero Sections

**Full-Width Hero**
- 100vw width, background image/video
- Centered content, max 600px wide
- Prominent H1 + subtitle + CTA
- Best for: SaaS, apps, bold statements

**Split Hero**
- 50/50 image and content
- Image on left or right
- Content: H1, description, form/CTA
- Best for: Product launches, conversions

**Asymmetric Hero**
- 60/40 or 70/30 split
- Creates visual interest
- Diagonal or overlapping elements
- Best for: Creative, agency, portfolio

### Content Sections

**Centered Stack**
- Max-width container (prose, lg, xl)
- Centered content
- Ample vertical spacing
- Best for: Text content, forms

**Card Grid**
- 2-4 columns
- Equal height cards
- Hover states, shadows
- Best for: Features, products, blog grid

**Alternating Rows**
- Image-text, text-image pattern
- Breaks monotony
- Tells visual story
- Best for: Feature showcases, case studies

**Bento Grid**
- Irregular card sizes
- Masonry or CSS Grid
- Visual interest
- Best for: Portfolios, galleries

### App Layouts

**Sidebar Navigation**
```
+-----+----------------+
| Nav |    Content     |
|     |                |
|     |                |
+-----+----------------+
```

**Top Navigation**
```
+---------------------+
|        Nav          |
+---------------------+
|      Content        |
|                     |
+---------------------+
```

**Holy Grail**
```
+---------------------+
|       Header        |
+-----+--------+------+
| L   |  Main  |  R   |
| e   |Content | i    |
| f   |        | g    |
| t   |        | h    |
|     |        | t    |
+-----+--------+------+
|       Footer        |
+---------------------+
```

## Design Principles

**Visual Hierarchy**
- Most important element = largest, highest contrast
- Use size, color, weight, position to guide eye
- F-pattern for text-heavy, Z-pattern for landing pages

**Whitespace**
- Not "empty" space—breathing room
- Groups related elements
- Creates rhythm and flow
- Minimum 1.5x spacing between sections

**Alignment**
- Everything aligns to something
- Strong left edge (for LTR languages)
- Use grid to maintain consistency

**Proximity**
- Related items closer together
- Unrelated items farther apart
- Creates visual relationships

**Balance**
- Symmetrical: Formal, stable
- Asymmetrical: Dynamic, interesting
- Radial: Centered, focused

**Contrast**
- Size, color, shape, texture
- Draws attention
- Creates interest
- Aids scannability

## Best Practices

- **Mobile-first design**: Start small, enhance for larger screens
- **Use consistent spacing**: Stick to 4px or 8px base unit system
- **Limit column variations**: Too many breakpoints = maintenance nightmare
- **Mind the fold**: Key content and CTA above fold, but don't cram
- **Create visual anchors**: Strong elements that guide the eye
- **Use the grid**: Even when breaking it, know you're breaking it
- **Test with real content**: Lorem ipsum hides layout problems
- **Consider reading patterns**: F-pattern, Z-pattern, Gutenberg diagram
- **Embrace whitespace**: Don't fear empty space—it's powerful
- **Maintain aspect ratios**: Images shouldn't distort on different screens
- **Accessible focus flow**: Logical tab order, clear focus states
- **Print styles**: If applicable, test print layouts

## Grid Systems

**12-Column Grid**
- Most common
- Divisible by 2, 3, 4, 6
- Flexible for most layouts
- Used by Bootstrap, Tailwind

**16-Column Grid**
- More granular control
- Good for complex dashboards
- Divisible by 2, 4, 8

**Modular Grid**
- Rows AND columns
- Swiss design heritage
- Best for editorial, magazines

**Baseline Grid**
- Vertical rhythm
- Text aligns to baseline
- Creates harmony
- 8px or 4px common

## Spacing Scale (8px base)

```
0:   0px    (none)
1:   4px    (0.25rem) - tight
2:   8px    (0.5rem)  - base
3:   12px   (0.75rem)
4:   16px   (1rem)    - comfortable
5:   20px   (1.25rem)
6:   24px   (1.5rem)  - loose
8:   32px   (2rem)    - section spacing
10:  40px   (2.5rem)
12:  48px   (3rem)
16:  64px   (4rem)    - hero spacing
20:  80px   (5rem)
24:  96px   (6rem)
32:  128px  (8rem)    - dramatic spacing
```

## Responsive Breakpoints

**Common breakpoints:**
- xs: 0px (base mobile)
- sm: 640px (large mobile)
- md: 768px (tablet)
- lg: 1024px (small desktop)
- xl: 1280px (desktop)
- 2xl: 1536px (large desktop)

**Content-first breakpoints:**
Add breakpoints where YOUR content breaks, not arbitrary device sizes.

## Deliverables Format

```
LAYOUT SPECIFICATION
Project: [Name]
Page: [Landing / Dashboard / Article]

STRUCTURE
[ASCII diagram of layout]

GRID SYSTEM
Columns: 12
Gutter: 24px (1.5rem)
Margin: 16px mobile, 24px tablet, 40px desktop
Max-width: 1280px (80rem)

SECTIONS
1. Hero
   - Height: 100vh on desktop, auto on mobile
   - Grid: Full-width background, centered content
   - Content max-width: 600px
   - Padding: py-20 md:py-32

2. Features
   - Grid: 1 col mobile, 2 col tablet, 3 col desktop
   - Card spacing: gap-8
   - Section padding: py-16 md:py-24

[... more sections ...]

SPACING SYSTEM
Base: 8px
Scale: [0, 0.5, 1, 1.5, 2, 3, 4, 6, 8, 12, 16, 20, 24, 32]
Section spacing: 64px (py-16)
Component spacing: 32px (py-8)

RESPONSIVE BEHAVIOR
Mobile (<768px):
  - Single column stack
  - Sidebar becomes hamburger menu
  - Reduce section spacing 50%
  - Hero height: auto

Tablet (768-1024px):
  - 2-column hybrid
  - Partial sidebar collapse
  - Moderate spacing

Desktop (>1024px):
  - Full multi-column
  - All content visible
  - Maximum spacing

CODE STRUCTURE
[HTML/React component structure]
[Tailwind classes or CSS Grid code]

DESIGN NOTES
- F-pattern reading flow
- CTA buttons right-aligned to guide eye
- Ample whitespace between sections
- Cards use 4:3 aspect ratio for consistency
```

## Tools Integration

- Use **ui-builder** skill for implementing layouts with Tailwind
- Use **Playwright** to test layouts in real browser
- Use **WebSearch** to find layout inspiration
- Use **Midjourney** to generate layout mood boards

## Common Requests

**SaaS Landing Page**: Hero + features grid + pricing + CTA
**Blog**: Centered column + sidebar + featured images
**Portfolio**: Masonry grid + project detail pages
**Dashboard**: Sidebar nav + table/chart grid
**E-commerce**: Product grid + filters + detail view
**Documentation**: Sidebar nav + content + right sidebar TOC
