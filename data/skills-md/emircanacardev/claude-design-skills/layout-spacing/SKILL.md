---
name: layout-spacing
description: Sets up layout and spacing foundations with a 4 or 8 point spacing scale, proximity-based grouping, alignment rules, a 12-column grid with gutters, container max-widths, vertical section rhythm and density modes, and decides when to use flexbox versus CSS grid. Use when asked to fix spacing, balance a layout or set up a grid, or when a screen looks cramped, too airy or misaligned. Not for breakpoint behavior; use responsive-design.
---

# Layout and Spacing

Produces a spacing scale and grid that every element snaps to, with grouping that makes the structure readable at a glance, delivered as tokens plus layout CSS and a value-by-value fix list.

## When to use
- "The spacing feels random", "too cramped" or "too much white space"
- Elements do not line up across sections or cards
- Setting up a page grid, gutters and container widths
- Adding compact and comfortable density options
- Deciding between flexbox and grid for a component

## Workflow
1. Inventory spacing values in use (margin, padding, gap) and count unique values. Identify the content type: marketing (airy), app (balanced), data tool (dense).
2. Choose the base: 8pt with 4pt half-steps for most products; strict 4pt for dense tools.
3. Map every existing value to the nearest scale step and list the changes.
4. Define relationships: within an element < between related items < between groups < between sections.
5. Define the grid: columns, gutters and outer margins per breakpoint, plus container max-widths.
6. Define section rhythm tokens for vertical spacing.
7. Implement with gap on flex and grid containers, then verify alignment edges.
8. If density modes are needed, swap semantic spacing tokens per mode via design-tokens.

## Rules
**Scale**
- Steps (px): 0, 4, 8, 12, 16, 20, 24, 32, 40, 48, 64, 80, 96, 128. A 2px step exists only for hairline optical fixes.
- Component internals use 4px multiples; layout spacing uses 8px multiples.
- Space between groups is at least 2× the space within them. Typical: label to input 4–8px, field to field 16–24px, card to card 16–24px, section to section 64–128px on desktop and 48–64px on mobile.
- A container's padding is greater than or equal to the gap between its children (e.g. card padding 24px, inner gap 12–16px).
- Buttons: 8–12px vertical and 16–24px horizontal padding, height 36–48px; 44px minimum on touch.

**Grid and containers**
- 12 columns on desktop (divisible by 2, 3, 4 and 6); 4 columns on mobile, 8 on tablet.
- Gutters: 16px mobile, 24px tablet, 24–32px desktop. Outer margins ≥16px on mobile.
- Container max-widths: reading 640–720px (about 65ch), app content 1200–1280px, wide 1440px. Always keep padding-inline ≥16px.
- Keep each section to 3–4 alignment edges; align text baselines and icon centers across adjacent elements.

**Flex vs grid**
- Grid for two-dimensional layouts and anything that must align across rows: page shells, card grids, forms with a label column.
- Flex for one-dimensional runs sized by content: toolbars, button groups, nav rows, tag lists.
- Card grids without breakpoints: grid-template-columns: repeat(auto-fill, minmax(min(100%, 280px), 1fr)).
- Use gap instead of child margins; use logical properties (padding-inline, margin-block) for RTL readiness.

**Density**
- Compact is about 0.75× comfortable spacing. Table rows: 32px compact, 40px default, 48px comfortable.
- Density never shrinks targets below 24×24px, or below 44px on touch.

## Output
- Spacing tokens as CSS custom properties plus semantic aliases (stack, inline, inset, section), or a Tailwind spacing mapping if the project uses Tailwind.
- Grid and container CSS.
- Fix list for the screen in question: element, old value → new value.

```css
:root {
  --space-1: 0.25rem; --space-2: 0.5rem; --space-3: 0.75rem; --space-4: 1rem;
  --space-6: 1.5rem;  --space-8: 2rem;   --space-12: 3rem;   --space-16: 4rem;
  --space-section: clamp(3rem, 2rem + 5vw, 8rem);
}
.container { max-width: 75rem; margin-inline: auto; padding-inline: clamp(1rem, 4vw, 2rem); }
.grid-12 { display: grid; grid-template-columns: repeat(12, minmax(0, 1fr)); gap: var(--space-6); }
```

## Avoid
- Off-scale values (13px, 22px, 37px)
- Equal spacing everywhere, which removes grouping cues
- Child margins that double up or collapse at container edges
- Nested containers that each add padding, producing double gutters
- Fixed heights on text containers
- Centering everything to dodge alignment decisions
- Full-width text blocks on wide screens

## Final check
- [ ] Every spacing value is on the scale
- [ ] Within-group < between-group < between-section spacing
- [ ] At most 3–4 alignment edges per section
- [ ] Container max-width set; mobile side margins ≥16px
- [ ] No horizontal overflow at 320px (see responsive-design)
- [ ] Targets ≥24×24px, 44px on touch
