---
name: screenshot-to-code
description: Reproduces a user interface from a screenshot as semantic, responsive code by inventorying regions, estimating spacing on a 4 and 8 px grid, extracting colors and type into tokens, then comparing the result side by side and listing deviations. Use when asked to recreate this screen, convert a screenshot to HTML or React, or rebuild a UI from an image. Only for UIs the user owns or has rights to. Not for rough sketches, which is wireframe-to-hifi.
---

# Screenshot to Code

Produces faithful, maintainable front-end code from a screenshot of a UI the user owns or is licensed to reproduce, plus a list of where the result differs and why.

## When to use
- "Recreate this screen in React" or "turn this screenshot into HTML/CSS."
- Rebuilding a legacy product's UI in a new stack when only screenshots remain.
- Converting an exported mockup (PNG) into code without access to the design file.
- Matching an existing internal page so a new page fits in.

## Workflow
1. Confirm rights. Proceed when the UI is the user's own product, a client's with permission, or an openly licensed template. If it is clearly someone else's product, offer an original layout that borrows only the general structure, and say so. Replace third-party logos, brand marks, and copyrighted photos or illustrations with labeled placeholders.
2. Establish scale: detect the device pixel ratio (a 2880px-wide capture of a laptop browser is probably @2x, so halve every measurement) and note the viewport width the screenshot represents.
3. Inventory regions top to bottom: header, nav, main, aside, sections, cards, footer, overlays. Assign each a semantic element and list the components inside.
4. Measure sizes and gaps in CSS px, then snap to a 4/8 grid (15 becomes 16, 22 becomes 24) unless the source clearly uses another system. Record container max-width and column structure.
5. Extract colors from flat interior areas, not anti-aliased edges or compression artifacts; merge near-identical values into one token. Extract type: family, sizes, weights, line heights, letter-spacing.
6. Build in order: tokens (CSS custom properties or Tailwind config), layout (grid and flex), components, then content. Use the real text from the screenshot.
7. Make it responsive: decide how the layout collapses below the captured width and state those assumptions (see responsive-design).
8. Compare: render at the source viewport width, view side by side or overlaid at 50% opacity, fix mismatches, and list what remains.

## Rules
**Fidelity**
- Match layout, spacing, type scale, and color within the snap tolerance; consistency matters more than exact pixels.
- Text in the screenshot is real text in the code, never an image of text.
- Icons come from an open icon set with a matching style, or inline SVG placeholders; name the set used.
- Never embed a font the user has no license for; use the closest open alternative behind one font variable so the real font can be swapped in.

**Code quality**
- Semantic HTML: headings in order, `<button>` for actions, `<a>` for navigation, lists for lists, a `<label>` for every input.
- No absolute positioning for page layout; flex and grid let content grow.
- Spacing, color, and type come from tokens, not repeated literals.
- Add states a screenshot cannot show (hover, focus-visible, disabled, loading) with sensible defaults, marked as inferred.

**Rights and accessibility**
- Third-party logos become a neutral box labeled "Logo"; photos become aspect-correct placeholders with alt text describing the intended content.
- Do not transfer another company's distinctive brand styling to a different product.
- If the source fails WCAG 2.2 AA contrast (4.5:1 text, 3:1 UI components), flag it and offer a corrected token instead of copying the failure silently.

## Output
- Code: semantic HTML + CSS custom properties, or React + Tailwind if the project already uses it; no new dependencies unless asked.
- Token block: colors, type, spacing, radius, and shadows extracted from the screenshot.
- Region inventory: | Region | Element | Components | Notes |
- Deviation list: what differs, why (unknown font, inferred state, placeholder, accessibility fix), and how to close the gap.

## Avoid
- Using @2x measurements without dividing by the pixel ratio.
- Dozens of one-off colors sampled from anti-aliased pixels.
- Fixed heights that break with longer text or translations.
- Clickable divs instead of buttons and links.
- Using the screenshot or its crops as background images to fake fidelity.
- Reproducing third-party logos, trademarks, or copyrighted imagery.

## Final check
- [ ] Rights are confirmed or explicitly assumed; third-party assets are placeholders.
- [ ] Measurements are normalized to CSS px and snapped to the grid.
- [ ] Colors and type are consolidated into tokens.
- [ ] Structure is semantic, inputs are labeled, and keyboard focus is visible.
- [ ] Side-by-side comparison was done at the source viewport width.
- [ ] Layout holds at narrower widths and with longer text.
- [ ] The deviation list is delivered.
