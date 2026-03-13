---
name: ui-design
description: Practical UI design principles for developers and non-designers. Use when creating web interfaces, components, dashboards, landing pages, or any visual design work. Covers hierarchy, spacing, typography, color, depth, and polish. Based on Refactoring UI methodology.
tags: [design, frontend]
---

# UI Design Skill

Practical design principles for creating professional, polished user interfaces without formal design training.

## Core Philosophy

Design is not about artistic talent—it's about making deliberate decisions. Focus on these fundamentals:

1. **Visual hierarchy** - Guide attention to what matters
2. **Spacing systems** - Create consistent rhythm
3. **Constraint-based design** - Limit choices to speed decisions

## Starting a Design

### Feature First, Not Layout

Never start with the shell (navbar, sidebar). Start with actual functionality:

- Design the core feature first (e.g., search form, not the page layout)
- The shell emerges from feature needs, not vice versa

### Progressive Fidelity

1. **Sketch first** - Use low-fidelity to explore ideas fast
2. **Grayscale second** - Force hierarchy through spacing, contrast, size
3. **Color last** - Add color only after hierarchy is established

### Design the Minimum

- Don't design features you won't build yet
- Expect implementation to be hard—design the smallest useful version
- Work in cycles: design → build → iterate

## Hierarchy

**The most important skill.** When everything competes for attention, nothing stands out.

### Establish Hierarchy With

- **Size** - But don't rely on it alone
- **Weight** - 400-500 for normal, 600-700 for emphasis. Avoid <400 for UI text
- **Color** - Dark for primary, grey for secondary, lighter grey for tertiary

### De-emphasize to Emphasize

When the main element doesn't stand out, don't add more to it—reduce emphasis on competing elements.

### Labels

- Often unnecessary—format and context communicate meaning (email, phone, price)
- Combine with values: "12 left in stock" not "In stock: 12"
- When needed, de-emphasize labels (smaller, lighter, lower contrast)

### Actions

- **Primary** - Solid, high contrast background
- **Secondary** - Outline or lower contrast background
- **Tertiary** - Style like links
- Destructive ≠ always red and bold. Use hierarchy first, confirm with bold styling.

## Spacing & Layout

### White Space

Start with too much, then remove. Elements need breathing room.

### Spacing System

Use a constrained scale where adjacent values differ by ~25%:

```
4, 8, 12, 16, 24, 32, 48, 64, 96, 128, 192, 256, 384, 512
```

Base on 16px (browser default). Don't nitpick between 120px and 125px—grab from your scale.

### Layout Principles

- **Don't fill the screen** - If you need 600px, use 600px
- **Grids are overrated** - Not everything should be fluid. Sidebars often work better with fixed widths.
- **Relative sizing doesn't scale** - Large elements shrink faster than small ones on small screens
- **Avoid ambiguous spacing** - More space _around_ groups than _within_ them

## Typography

### Type Scale

Hand-pick a constrained set:

```
12, 14, 16, 18, 20, 24, 30, 36, 48, 60, 72
```

Use px or rem, never em (nesting breaks the system).

### Line Length

45-75 characters per line (20-35em). Constrain paragraphs even in wide layouts.

### Line Height

- **Inversely proportional to font size** - Taller for small text, shorter for large
- **Proportional to line length** - Wider content needs taller line-height
- Headlines at large sizes can use line-height: 1

### Alignment

- Left-align most text
- Center only headlines or short blocks (<3 lines)
- Right-align numbers in tables

### Letter Spacing

- Tighten for large headlines
- Increase for ALL CAPS text

## Color

### Use HSL

Hue (0-360°), Saturation (0-100%), Lightness (0-100%). More intuitive than hex/RGB.

### Build a Palette

You need far more than 5 colors:

- **Greys** - 8-10 shades. Start dark grey (not pure black), end white.
- **Primary** - 5-10 shades for buttons, links, active states
- **Accents** - Semantic colors (red=destructive, yellow=warning, green=success)

### Creating Shades

1. Pick base color (good for button background)
2. Pick darkest (for text on light bg) and lightest (for tinted backgrounds)
3. Fill gaps: 100, 200, 300, 400, 500, 600, 700, 800, 900

### Advanced Techniques

- **Increase saturation** as lightness moves away from 50%
- **Rotate hue** toward bright hues (60°, 180°, 300°) to lighten, dark hues (0°, 120°, 240°) to darken
- **Saturate greys** with blue (cool) or yellow/orange (warm)

### Colored Backgrounds

Don't use grey text on colored backgrounds—hand-pick a color with same hue, adjusted saturation/lightness.

### Accessibility

- 4.5:1 contrast for normal text, 3:1 for large text
- Flip contrast: dark text on light colored background instead of white on dark
- Never rely on color alone—add icons, patterns, or contrast differences

## Depth & Shadows

### Light Source

Light comes from above. Raised elements: lighter top edge, shadow below. Inset elements: shadow at top, lighter bottom edge.

### Shadow System

Define 5 shadows from subtle to dramatic:

- **Small** - Buttons, subtle elevation
- **Medium** - Dropdowns, cards
- **Large** - Modals, dialogs

### Two-Part Shadows

1. Large, soft shadow (direct light source)
2. Tight, dark shadow (ambient light blocked underneath)

### Flat Design Depth

- Lighter = closer, darker = further
- Solid shadows (no blur) work for flat aesthetics
- Overlap elements to create layers

## Images

### Quality Matters

Bad photos ruin good designs. Use professional photography or quality stock (Unsplash).

### Text Over Images

- Add semi-transparent overlay
- Lower image contrast and adjust brightness
- Add subtle text shadow (large blur, no offset)

### Sizing

- Don't scale icons up (they look chunky) or down (they look muddy)
- Don't shrink full screenshots—use partial screenshots or simplified illustrations
- Control user-uploaded images with fixed containers (background-size: cover)

## Finishing Touches

### Supercharge Defaults

- Replace bullets with icons
- Promote quotes into visual elements
- Style links distinctively
- Use custom checkboxes/radios with brand colors

### Add Polish

- **Accent borders** - Top of cards, side of alerts, under headlines
- **Background decoration** - Color changes, subtle patterns, geometric shapes
- **Empty states** - Design them! Include illustrations and clear CTAs.

### Reduce Borders

Use instead:

- Box shadows
- Different background colors
- Extra spacing

### Think Outside the Box

Dropdowns can have columns, icons, sections. Tables can combine columns and add hierarchy. Radio buttons can be selectable cards.

## Reference Files

For deeper guidance:

- [Hierarchy & Spacing](references/hierarchy-spacing.md) - Visual hierarchy, spacing systems, layout
- [Typography & Color](references/typography-color.md) - Type scales, font selection, color systems
- [Depth & Polish](references/depth-polish.md) - Shadows, images, finishing touches
