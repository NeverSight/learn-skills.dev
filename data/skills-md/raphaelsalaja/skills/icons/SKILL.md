---
name: icons
description: Draws missing icons in the project's own style, measured from every icon the set already has and built to morph, then shows the set on one sheet.
---

# Icons

This skill draws the icons a project's set is missing, in that set's own style. Every new glyph is measured against the whole set, written to animate and morph, then shown on one sheet.

## Nothing is drawn until the set is measured

The spec is exact. The sheet measures it from every icon the set already has, and each new glyph follows it. A guessed stroke, radius or grid is a finding.

Run it for `draw an icon for`, `we need a ... icon`, `custom icons` or `the set doesn't have a`. Also run it for `match our icons`, `filled version`, `animate this icon`, `morph`, `icon sheet` or `this icon looks off next to the others`.

Which glyphs to draw belongs to `scope`. Searching the set first belongs to `reuse`. Optical nudges belong to `alignment`. The curve, duration and reduced-motion fallback of any icon animation belong to `motion`. Accessible names belong to `defaults`. Visible labels belong to `copy`. Contrast belongs to `color`.

## 1. Draw only what the set lacks

Run `reuse` first. Search the icon package, the icon folder or the map that holds inline icons, and draw a glyph only when it is absent. A second copy of a glyph the set has is `icons-only-missing`.

Add the glyph where the set lives, beside its siblings. A new icon left in a feature file is `icons-in-the-package`. A missing glyph added there is not a finding in `reuse`.

## 2. Measure the whole set

Copy [sheet.html](sheet.html) to `.icons/<set>/index.html`, an ignored folder and never the source tree. Write `sheet.js` beside it with every existing icon, as its header comment shows, then open it.

Mark logos and brand marks `brand: true`. They are never measured, redrawn or restyled.

The sheet derives the spec from every existing icon on the most common viewBox. It records the stroke, caps, joins, radii, grid step, padding, round overshoot and ink coverage per kind. Copy Spec gives `icon-spec.md`, saved beside the icons.

Drawing before `icon-spec.md` exists, or from a spec measured by hand, from a sample or from memory, is `icons-measure-the-spec`. With fewer than 3 icons on one viewBox, stop and ask for the reference set.

An existing icon off the spec shows as an outlier. List it in the report and leave it, because redrawing it is a separate ask under `scope`.

## 3. Draw on the set's grid

Put every anchor point on the spec's grid step, while curve handles stay free. Use `currentColor` and never a literal colour. A coordinate off the step or a hex stroke is `icons-on-the-grid`.

Within the step, keep straight stroke edges on whole pixels. A 2 stroke centres on whole pixels and a 1 stroke on half pixels. A 1.5 stroke centres on a quarter, so its outer edge lands on a whole pixel.

When the set ships a separate drawing per size, draw every size and run one sheet per size.

When the set's icons are only rects on whole pixels, the set is pixel-style. Draw each glyph as a text grid first, then convert that grid to rects. A pixel icon begun as smooth paths is `icons-pixel-grid-first`. Pixel sets skip step 5 and swap with the cross-fade in `motion`.

## 4. Correct what the eye sees

Separate parts sit at least one stroke width apart, and never under 1px. Two strokes that merge into one blot at 16px are `icons-open-gaps`.

Round shapes may pass the padding by the spec's round overshoot and no further. Arrows and play shapes take the nudge in `alignment`, drawn into the coordinates. A circle drawn at a square's size cites `alignment-visual-weight`, and a play icon centred on its box cites `alignment-optical-glyph`.

## 5. Write every new icon in the morph form

Every new icon animates and morphs into every other new icon of its kind. Each one is the same number of `path` elements, and each path is an absolute `M` followed by the same number of explicit `C` segments.

The sheet sets both counts from the most complex new icon and shows them as Morph Form. Pad a shorter path with zero-length segments at its end.

Two icons that are one shape turned, such as back and forward, share one drawing. The swap rotates the whole icon instead of moving points, and the sheet marks the pair Spins.

A straight segment is a cubic whose handles sit on its own ends. A closed stroke returns to its start point instead of using `Z`. An unused path collapses to one point on another stroke, where it stays hidden.

Each path starts at its topmost anchor, leftmost on a tie. Order the paths longest first, so large strokes morph into large strokes. To morph into an existing icon, add that icon's morph form as a new icon with the same ink.

An optimiser that merges paths or converts shapes breaks the form, so turn off `mergePaths` and `convertShapeToPath` for these files. A `circle`, `rect`, `line`, `Z`, relative command or path count off the morph form is `icons-morph-form`.

## 6. Build outline and filled from one skeleton

Outline and filled variants share one skeleton and one morph form. The filled form fills the outline's own paths and keeps its silhouette. Inner detail becomes a counter at least 1px wide, and narrower counters are dropped. A filled icon redrawn from scratch is `icons-one-skeleton`. A fill cannot morph, so outline and filled swap with the cross-fade in `motion`.

## 7. Lint every icon against the spec

The sheet lints each new icon for viewBox, stroke, caps where ends are open, joins where corners exist, grid, padding, radii and more than 3 decimals. It also rejects transforms, ids, classes, inline styles, masks and clip paths.

Ink coverage compares outline with outline and filled with filled, inside the range the set already spans. A kind the set lacks shows `Not Verified` and is judged on the sheet. Each miss is `icons-lint-the-spec`.

## 8. Read the set on one sheet

The sheet sorts by name, so new glyphs sit among old ones, and badges each new one. Style, Size and Dark Tiles at the top set what the grid shows.

Pixels rasterises each icon at its native size, one device pixel per unit, and enlarges it three times. Soft or doubled edges there are a grid problem.

Weight blurs the 48px icons by 2px, so only weight remains. A new glyph that reads darker or lighter than its neighbours there is too dense or too thin.

Morph plays each new icon into the next of its kind on the curve in `motion`. A morph that twists, crosses itself or flashes a dot has its paths out of order.

Clicking an icon opens its dialog. Its Morph tab chains any icons under the stage, pasted ones included, and says whether each step spins, morphs as drawn or needs converting.

A converted preview is the sheet's own guess, not the form that ships. Prompts copies the fix, the redraw or the morph-form request for the agent to apply.

A sheet written from scratch, or icons checked one at a time, is `icons-one-sheet`. Fix every finding and reopen it until Findings is empty.

## 9. Match the project's icon component

Generate components on the project's existing icon API, including its props and file shape. Keep each path its own element, so a caller can animate `d` or draw the stroke on. A one-off component with its own props, or a decorative icon with no `aria-hidden`, is `icons-match-the-api`.

Add a hover, active or swap animation only when the user asks, and run it through `motion`. An icon that is the only content of a control cites `defaults-name-icon-buttons`. Contrast cites `color-ui-contrast`.

## The pair

Every check is a pair. The broken line sits beside the line that replaces it.

| Rule | Broken | Replacement |
| --- | --- | --- |
| `icons-only-missing` | A new `SearchIcon` when the set has one | The set's `SearchIcon` |
| `icons-in-the-package` | `ReceiptIcon` in a feature folder | `ReceiptIcon` beside its siblings in the set |
| `icons-measure-the-spec` | A spec measured by hand from 3 icons | `icon-spec.md` copied from the sheet, then the path |
| `icons-on-the-grid` | `M5 2.3` with `stroke="#111"` on a 0.25 step | `M5 2.25` with `stroke="currentColor"` |
| `icons-pixel-grid-first` | A pixel glyph drawn as smooth paths | A text grid converted to rects |
| `icons-open-gaps` | Two 1.5 strokes 0.5 apart | The strokes 1.5 apart |
| `icons-morph-form` | `<circle r="4.5" />` beside `<path d="M10.5 10.5l3 3" />` | 3 paths, each `M` and 5 `C` segments |
| `icons-one-skeleton` | A filled icon drawn as a new path | The outline's paths filled |
| `icons-lint-the-spec` | `transform="translate(0.5 0.5)"` on a 2px stroke | The spec's stroke and padding, no transform |
| `icons-one-sheet` | The new icon screenshotted alone at 24px | `sheet.html` copied, only `sheet.js` written |
| `icons-match-the-api` | A feature-file `svg` with its own size prop | The project's icon component, `aria-hidden` when decorative |

## Reporting

**Severity.** `HIGH` is a glyph drawn with no spec, or a duplicate of a glyph the set already has. `MEDIUM` is an off-grid icon, a pixel set drawn as paths, closed gaps, a failed lint, an icon off the morph form or a second skeleton. `MEDIUM` is also a missing sheet, a file outside the set or a component off the project's API. `LOW` is a morph that twists or flashes on the sheet.

**Format.** One finding per root cause:

```
file:line - [rule-id] what is wrong
```

Then a `Rule | Count | Severity` summary and the existing outliers as a separate list. `Block` when any `HIGH` remains, `Approve` otherwise. When the miss is the work and not a file, cite `request 2 - [rule-id]`. Mark a sheet you could not render as `Not verified`.
