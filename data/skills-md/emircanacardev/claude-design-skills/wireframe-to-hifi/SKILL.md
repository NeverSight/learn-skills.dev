---
name: wireframe-to-hifi
description: Turns a sketch, wireframe, whiteboard photo, or text description into a high-fidelity UI by interpreting the structure, setting type, color, and spacing tokens, mapping elements to components, and polishing hierarchy, states, and alignment, with all assumptions flagged. Use when asked to make a wireframe real, turn a sketch into a design, or build a screen from a rough layout. Not for pixel-matching an existing UI, which is screenshot-to-code.
---

# Wireframe to Hi-Fi

Produces a polished, implementable screen from low-fidelity input, as working code or a detailed spec, with every interpretation and assumption made explicit.

## When to use
- "Turn this sketch into a real UI", with a photo of paper or a whiteboard.
- Balsamiq, Excalidraw, or FigJam wireframes that need visual design.
- Text-only briefs ("a settings page with profile, notifications, and billing").
- Upgrading a working but unstyled prototype.
- Screens listed in a user-flows inventory that now need high-fidelity design.

## Workflow
1. Read the input and write an interpretation list: each region, its likely purpose, and your confidence. Treat squiggles as text, crossed boxes as images, and rough shapes as the nearest standard component. Ask 1–2 questions only if a region's purpose changes the layout; otherwise assume and flag.
2. Name the screen's primary task and rank content: one primary action, two or three secondary, the rest tertiary. Treat sketched sizes as hints, not specs.
3. Reuse the project's tokens and components if they exist. If not, define a minimal set: a type scale (12/14/16/20/24/32), 4px-based spacing (4, 8, 12, 16, 24, 32, 48, 64), neutrals plus one accent plus semantic colors, radius, and elevation (see design-tokens, color-system, typography-system).
4. Map every element to a component (button, input, card, list item, tabs, nav bar, dialog). Note any new component that would be required.
5. Lay out on a grid (see layout-spacing): consistent container width, columns, and spacing from the scale; group related items with proximity before adding borders or boxes.
6. Apply hierarchy with size, weight, and contrast. Only the primary action gets the filled accent style.
7. Add states: hover, focus-visible, active, disabled, loading, empty, error, and long-content behavior (see ui-states). Define the other breakpoint if the input shows only mobile or only desktop (see responsive-design).
8. Polish: align to shared edges, check vertical rhythm, verify contrast, and replace placeholder text with realistic copy (see ux-writing).

## Rules
- Keep the wireframe's information architecture and order unless it causes a clear usability problem; when you change it, say why.
- Every spacing value comes from the scale. No 13px or 27px.
- One typeface is usually enough, two at most; no more than about four text sizes per screen.
- One visually dominant primary action per view.
- Body text at least 16px on web; line length 45–75 characters.
- Touch targets at least 44×44 pt (iOS) or 48×48 dp (Android); 24×24 CSS px is the WCAG 2.2 AA floor.
- Contrast at least 4.5:1 for text and 3:1 for large text, icons, and input borders (WCAG 2.2 AA).
- Use realistic data: real-length names, prices, and dates, including at least one long string.
- Icons come from one set with consistent stroke and size; pair ambiguous icons with text labels.
- Images are aspect-correct placeholders with intended alt text, not random stock photos.
- When the input conflicts with an existing design system, the design system wins; list the conflict.
- A distinctive look is welcome (see distinctive-ui) but never at the cost of hierarchy or contrast.

## Output
- Default: working code in semantic HTML + CSS custom properties, or React + Tailwind if the project already uses it; no new dependencies unless asked. Declare tokens once (`:root` or the Tailwind config).
- On request, a written spec instead: tokens, grid, component list, per-element specs, and states.
- Interpretation table: | Wireframe element | Interpreted as | Confidence | Assumption |
- Assumptions and open questions; anything engineers will need later goes to design-handoff.

## Avoid
- Tracing the sketch's rough proportions literally.
- Adding features or sections that are not in the input; suggest them separately instead.
- Shadows, gradients, and borders on everything instead of spacing and type for hierarchy.
- Lorem ipsum in the final result.
- Delivering only the default state.
- One-off values outside the token set.

## Final check
- [ ] Every wireframe element appears in the interpretation table.
- [ ] Tokens are defined once and used everywhere; spacing sits on the 4px scale.
- [ ] One clear primary action; hierarchy still reads when the screen is blurred.
- [ ] Interactive, loading, empty, and error states exist.
- [ ] Contrast meets WCAG 2.2 AA and focus is visible.
- [ ] Layout works at 360px wide and at desktop width.
- [ ] Assumptions are listed.
