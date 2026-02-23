---
name: web-design
description: WHEN refining UI layout, typography, color, or polish; NOT code implementation; provides concise principles for intentional, legible design.
---

# Web Design

Focus on clear hierarchy, generous spacing, and restrained styling to make interfaces feel intentional.

## Visual Hierarchy & Focus

- Group related elements by proximity and aligned edges; avoid scattered, evenly-spaced elements that compete for attention.
- Add hierarchy with weight before color: `font-weight: 600` and size changes beat random accent colors.
- Reduce noise: fewer borders; use spacing, background tints, or subtle dividers instead of heavy outlines.

## Layout & Spacing

- Use a consistent scale (4px or 8px).
- Make vertical rhythm obvious: larger gaps between sections than between labels/inputs.
- Set max widths for readability (e.g. `max-width: 1280px` for pages, `68-70ch` for text blocks).
- Pad clickable areas generously (12–16px vertical, 16–24px horizontal) so touch targets feel confident.

## Typography

- Pick one font family; use weight/size/letter-spacing for contrast instead of juggling many fonts.
- Define a small scale of text styles (e.g., `32/40`, `24/32`, `18/28`, `16/24`, `14/20`) and reuse them.
- Use letter-spacing for uppercase labels; use color to de-emphasize metadata instead of shrinking excessively.

```css
.eyebrow {
  text-transform: uppercase;
  letter-spacing: 0.08em;
  font-size: 12px;
  color: #6c7280;
}
```

## Color & Contrast

- Start with neutrals; let a single accent color carry primary actions. Avoid pure black/white—use softened grays for warmth.
- Build palettes by lightening/darkening the same hue; use low-saturation tints for surfaces and bolder shades for actions.
- Ensure contrast for text on tints; add a subtle border when a tinted panel touches a white background.
- Use color for meaning (success/info/warn/danger) plus an icon or text so color-blind users are covered.

## Depth, Shape & Elevation

- Prefer soft, diffuse shadows for elevation; combine slight offset with low opacity blur. Avoid harsh, opaque drop shadows.
- Keep radii consistent (e.g., 8–12px across inputs, cards, modals). Match inner elements to the parent radius.
- Separate stacked surfaces with either a light border or a faint shadow but not both.

## Components That Feel Designed

- Buttons: one clear primary, a low-emphasis secondary (ghost/text), and a destructive variant. Use consistent padding and radius.
- Forms: pair clear labels with inputs; avoid placeholder-as-label; show inline validation close to the field; use generous vertical spacing.
- Lists/tables: increase row height, soften alternating backgrounds, and highlight the primary cell with weight/color.
- Icons: keep stroke weight consistent; pair icons with labels unless the meaning is universal. Balance visual weight with padding.

## States, Feedback & Empty Space

- Design hover, active, focus, loading, error, and success states. A primary button should have at least hover + active + disabled styles.
- Use skeletons or subtle shimmer for loading instead of spinners alone; provide friendly empty states with a short “what to do next.”
- Clarify errors with color, icon, and text; reserve red for errors and use calmer hues for neutral info.
- Give content room to breathe—whitespace is a design tool, not wasted space.

## Compositional Polish

- Use consistent gaps, radii, shadows, and border colors across the entire UI to create harmony.
- Replace visual clutter (dividers, lines, boxes) with spacing and alignment; let one strong anchor (title or primary action) lead.
- When stacking elements on images, add a dark or light overlay to keep text legible.
