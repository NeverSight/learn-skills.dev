---
name: presentation-qa
description: Audit PowerPoint, PDF, Keynote export, or fixed-canvas HTML presentations for storyline, evidence, visual hierarchy, readability, clipping, overlap, asset failures, consistency, and delivery readiness. Use for final review, pre-send checks, slide critiques, or regression QA; diagnose first and only modify the deck when the user also asks for fixes.
license: MIT
metadata:
  short-description: Evidence-backed presentation audit and delivery QA
---

# Presentation QA

Review the rendered artifact, not only its object model or source code. A deck can be structurally valid and still fail because of wrapping, font substitution, crop changes, broken assets, or weak narrative.

## Scope first

Confirm the active file, output format, audience, presentation setting, approved copy, brand constraints, locked elements, and whether the task is review-only or includes fixes. Review requests do not authorize rewriting, editing, publishing, or sending the deck.

## Required workflow

### 1. Inventory

Record page count, dimensions, fonts, linked assets, hidden slides, notes, comments, animations, and expected outputs. Preserve the original; use a named working copy if fixes are requested.

### 2. Render every slide

Render all pages at a consistent 16:9 or source-native size. Build a contact sheet for sequence review, then inspect each slide at full resolution. If the deck has a reference image or baseline, normalize dimensions before comparison.

### 3. Audit in layers

Review in this order:

1. **Purpose and storyline:** audience, decision, opening promise, title sequence, conclusion, and call to action.
2. **Evidence:** source coverage, numeric reconciliation, chart integrity, assumptions, and unsupported claims.
3. **Slide hierarchy:** one message per slide, reading order, dominant proof, density, and whitespace.
4. **Layout mechanics:** clipping, overlap, alignment, wrapping, off-canvas elements, and inconsistent spacing.
5. **Typography and visuals:** font substitution, type scale, contrast, crops, icon consistency, and image quality.
6. **Delivery behavior:** links, media, animations, navigation, PDF export, and file portability.

Use [references/qa-rubric.md](references/qa-rubric.md) for severity and acceptance criteria.

### 4. Separate findings from fixes

For each issue, provide:

- slide number and location;
- severity;
- observable problem;
- why it matters;
- recommended fix;
- evidence such as a render, measurement, or source check.

Do not rewrite copy merely to make it fit. If the fix changes meaning, positioning, numbers, or approved wording, call it out separately.

### 5. Regression after fixes

If editing is authorized, re-render changed slides and nearby pages. Confirm page count, slide order, locked elements, untouched pages, fonts, assets, and final export. Compare before and after under the same rendering conditions.

## Mechanical checks

When the format permits, check:

- text and meaningful-object bounding boxes;
- text-to-text overlap candidates;
- objects beyond the slide canvas;
- missing or zero-dimension images;
- font availability and substitution;
- low-resolution raster assets at rendered size;
- chart labels, axes, legends, and units;
- broken links and runtime or console errors;
- notes, comments, hidden slides, and document metadata.

Treat automated overlap results as candidates and confirm visually; intentional labels, badges, and overlays can be valid.

## Delivery report

Lead with release readiness: `READY`, `READY WITH MINOR FIXES`, or `NOT READY`. Then list P0–P2 issues, a concise slide-by-slide table, validation performed, and remaining limitations. Do not bury a blocking issue in general design feedback.
