---
name: tesseract-design
description: Create and revise static visual designs as editable Tesseract compositions and rendered PNGs, including posters, social graphics, slide layouts, diagrams, and web/UI mockups. Use when the requested deliverable is a design image.
---

# Design with Tesseract

Turn the user's brief into static visual designs rendered with `tsrct preview`. Deliver the PNGs as the primary result and keep their editable `.tsrct` sources for revisions. Match the format to the request: a poster, social graphic, slide, diagram, interface mockup, or another composition.

The CLI may send basic usage telemetry for some commands. Read [telemetry](references/telemetry.md) for collected data and opt-out; never enable telemetry on the user's behalf.

## Establish the design

Use the context already provided: the design’s purpose, audience, message or action, intended medium, copy, brand assets, visual references, and requested dimensions or variants. Inspect supplied references and assets. Ask only for missing information that materially changes the design; state reasonable assumptions for open choices and continue. For revisions, preserve the existing direction and scope.

Choose a visual direction tied to the brief and content: type hierarchy, spacing, grid, color, and imagery. Use realistic copy and supplied assets; identify placeholder content rather than inventing customer evidence or claims. Adapt composition and type to each requested format. For web/UI mockups with responsive variants, reflow content for each width instead of shrinking the desktop image.

## Author and preview

1. Resolve this skill's root from the directory containing this `SKILL.md`. Follow [installation](references/installation.md), check the required CLI version once per session, and use its resolved executable path throughout.
2. Follow [static authoring](references/static-authoring.md) to create or revise the portable document, set its actual canvas dimensions, import fonts/images, and save editable layers. Query the installed schemas for the fields needed; never invent APIs or assume browser/CSS behavior.
3. Keep text, shapes, diagram elements, and layout geometry as native editable layers. Use images for photography, logos, and other supplied raster assets. Do not flatten the entire layout into one image. Use named groups where useful for related elements or components.
4. Render a PNG early, open it, and revise the saved composition. Review hierarchy, alignment, spacing, line breaks, clipping, image crops, contrast, and text legibility at the intended viewing size. Inspect large or detailed designs in close-up as well as at an overview scale. A successful render alone does not establish a good design.

## Deliver designs

Render each final design or requested variant with `preview` from its saved source. Use clear names such as `Poster.png`, `Social-square.png`, or `Home-mobile.png`, and show the images inline when supported. Include a clearly labeled link to each final PNG alongside its matching editable `.tsrct` source, even when displaying the PNG inline. Use absolute local paths for these links and state the actual image dimensions. Keep working JSON and useful assets with the project for continuation.

The PNGs are the finished deliverable; no video export, sound pass, or animation is needed. Explain any missing assets, unreviewed output, or renderer limits. For web/UI mockups, distinguish the static design from an implemented website or working interaction. Slides are PNG layouts with editable Tesseract sources; do not imply a PowerPoint or print-production file was delivered.
