---
name: alignment
description: Measures a running page for edges, gaps, centring and radii that miss by a pixel or two, then judges visual weight and returns a numbered report with proof.
disable-model-invocation: true
---

# Alignment

This skill checks a running page for things that are out of line or out of balance. It measures the rendered ink, confirms each finding in a zoomed screenshot and returns a numbered report.

## Measured to the pixel, judged by eye

Lines, gaps, centres and radii are measured, never estimated. A miss of 1–4px is a finding, because it reads as a mistake while a 16px indent reads as intent. Visual weight has no number, so it is judged from the screenshot and shown as a crop.

Opening the running result belongs to `verify`. Comparing against a named reference belongs to `match`. Forcing hover, open and error states belongs to `lab`. Moving a fix into the shared component belongs to `reuse`. Rendering every width belongs to `viewports`.

## 1. Open the shipped render

Open the page at the viewport it ships at, with a device scale factor of 2. Check each theme and each state the user named. Reasoning from the CSS about where things should land is `alignment-measure-the-render`.

## 2. Run the measurement

Read the spacing scale from the project's tokens first. Run [measure.js](measure.js) in the page through the browser's evaluate call, passing the scale as `window.__alignmentOptions = { scale }`.

It returns findings with a rule, the element, the measured values and a rectangle. Treat each as a candidate until step 3 confirms it.

## 3. Check the lines

Crop each candidate from the 2x screenshot and count the pixels. Drop any finding the pixels do not show.

Text, icons and controls that start a column share one x. A title 2px right of its description is `alignment-shared-edge`.

Repeated siblings sit at one gap. A list spaced 8, 8 then 12px is `alignment-even-gaps`. A deliberate group break is at least twice the gap.

Every padding, gap and margin is a step on the project's scale. A 6px padding on a 4px scale is `alignment-on-scale`.

## 4. Check the centres

Text in a control centres on its cap height and baseline, not its line box. Ink sitting 2px low in a button is `alignment-ink-centre`. Trim the box with `text-box: trim-both cap alphabetic` or balance the padding.

An icon beside a label centres on the label's cap height. An icon centred on the line box and sitting 1px low is `alignment-icon-with-label`.

Play icons, arrows and triangles carry their weight on one side. A play icon centred by its box that looks shifted left is `alignment-optical-glyph`. Nudge it and name the value, such as `--play-nudge: 1px`.

A nested surface's radius is the outer radius minus the inset. A 16px panel inside a 16px card at 8px inset is `alignment-concentric-radius`, and it takes 8px.

## 5. Judge the weight

Look at the screenshot at 1x and name what the eye lands on first. Compare icon strokes with the text's stem weight, filled icons beside outline icons and circles drawn the same size as squares.

Circles and triangles need roughly 10% more size than a square to read as equal. A 2px icon stroke beside 1.5px text stems is `alignment-visual-weight`.

## 6. Report with proof

Copy [report.html](report.html) to `.alignment/<page>/index.html`, an ignored folder and never the source tree. Save the 2x screenshot beside it and write `report.js` in the shape its header comment shows, then open it.

The report draws the numbered outlines and cuts each zoomed crop from that screenshot, so write data only. A report with its own markup or crops cut by hand is `alignment-shipped-report`. A finding with no measurement and no rect is `alignment-annotated-proof`.

## 7. Fix only when asked

The report is the deliverable. When the user asks for fixes, change the token or primitive behind each finding. Rerun the script and the screenshot, then report what cleared.

## The pair

Every check is a pair. The broken line sits beside the line that replaces it.

| Rule | Broken | Replacement |
| --- | --- | --- |
| `alignment-measure-the-render` | "The flex container centres it" | Measured in the running page at 2x |
| `alignment-shared-edge` | Title inset 2px from its description | Both start on one ink line |
| `alignment-even-gaps` | Rows at 8, 8 and 12px | Rows at 8, 8 and 8px |
| `alignment-on-scale` | `padding: 6px` on a 4px scale | `padding: 8px` |
| `alignment-ink-centre` | Label ink 2px low in its button | `text-box: trim-both cap alphabetic` |
| `alignment-icon-with-label` | Icon centred on the line box | Icon centred on the cap height |
| `alignment-optical-glyph` | Play icon centred by its box | Play icon nudged `1px` right, named |
| `alignment-concentric-radius` | 16px panel in a 16px card at 8px inset | 8px panel radius |
| `alignment-visual-weight` | 2px icon stroke beside 1.5px stems | Stroke matched to the text weight |
| `alignment-annotated-proof` | "The button looks a bit off" | Finding 3, 1.8px low, with the crop |
| `alignment-shipped-report` | Crops cut by hand into a page written from scratch | `report.html` copied, only `report.js` written |

## Reporting

**Severity.** `HIGH` is a miss visible at 1x on a primary surface, such as a heading column or a primary button. `MEDIUM` is a 1–2px miss, uneven gaps, a radius mismatch, a weight imbalance or a hand-built report. `LOW` is an off-scale value that still renders aligned.

**Format.** One finding per root cause, numbered to match the overlay:

```
1. file:line - [rule-id] what is wrong (measured values)
```

Cite the element from the script when the source line is not found. Then a `Rule | Count | Severity` summary. `Block` when any `HIGH` remains, `Approve` otherwise. Mark canvas, image and cross-origin content as `Not verified`.
