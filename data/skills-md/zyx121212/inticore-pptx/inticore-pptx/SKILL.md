---
name: inticore-pptx
description: Generate a user-approved full-slide visual blueprint and recreate it, or directly recreate a supplied PNG/JPG/WebP/screenshot, as a native editable PowerPoint PPTX across Codex, Claude Code, WorkBuddy, Cursor, Gemini CLI, OpenCode, and other filesystem-based agents. Use for 内容先出视觉稿再做PPT, 图片转PPT, 截图转PPT, 1:1重制PPT, 100%像素级还原, 零差异PPT, 原生可编辑PPT, editable PPTX, or when the user rejects a full-slide background image. Preserve approved wording, layout, dimensions, colors, hierarchy, tables, timelines, diagrams, borders, icons, people information, and photographic assets. For pixel-perfect requests, freeze the renderer contract and require the actual PPTX render to pass a strict per-slide zero-pixel-difference comparison without embedding the full reference image.
---

# Inticore PPTX

Create or accept a full-slide visual reference, freeze it after user approval, and rebuild each page as editable PowerPoint objects. Use raster images only for inherently photographic or highly detailed illustration assets.

## Route the request

Choose exactly one entry route:

- **Route A — supplied image:** The user already supplied a slide image or screenshot. Treat it as the approved reference and begin reconstruction unless the user asks to redesign it.
- **Route B — content to blueprint:** The user supplied content, documents, notes, data, or a concept but no approved slide image. Use the runtime's available image-generation capability or the portable blueprint fallback to create full-slide visual blueprints, obtain explicit user approval, freeze the approved blueprints, and only then begin reconstruction.

For Route B, read [references/content-to-blueprint.md](references/content-to-blueprint.md), [references/slide-title-system.md](references/slide-title-system.md), and [references/visual-enhancement-system.md](references/visual-enhancement-system.md) completely before generating any image. After approval, read [references/blueprint-freeze-and-handoff.md](references/blueprint-freeze-and-handoff.md) completely before creating the PPTX. Use the bundled prompts, visual-direction system, approval gates, and handoff records as the complete blueprint workflow.

## Bootstrap the runtime

Before creating files, run `python3 scripts/detect_runtime.py --host <known-host> --json` from this Skill directory and read [references/runtime-selection.md](references/runtime-selection.md) completely. Use `--host auto` only when the active host is genuinely unknown. Then read exactly the matching adapter: [references/runtime-codex.md](references/runtime-codex.md), [references/runtime-workbuddy.md](references/runtime-workbuddy.md), [references/runtime-claude-code.md](references/runtime-claude-code.md), or [references/runtime-portable.md](references/runtime-portable.md).

Prefer a host-provided presentation capability when it can satisfy the native-editability and renderer contract. Read that capability's complete instructions before authoring. Otherwise use the portable PptxGenJS toolchain. Freeze the selected authoring backend, renderer, versions, fonts, color mode, and output dimensions in the task ledger; never switch them silently during pixel comparison.

## Non-negotiable contract

- Never insert the complete reference image as the slide background or a full-slide image.
- A large background asset is allowed only when it is a semantic-content-free atmosphere or scene plate. It must contain no title, copy, chart, timeline, foreground illustration, label, or data object, and it must be independently removable without deleting information.
- Do not add explanations, visual inventions, rewritten copy, inferred content, or stylistic improvements.
- Do not omit, shorten, correct, translate, or paraphrase visible text.
- Keep text editable. Build tables, borders, arrows, timelines, containers, badges, simple icons, and diagrams as native PowerPoint objects.
- Use independent raster assets only for photographs, product renders, portraits, detailed illustrations, or textures that cannot reasonably be recreated as native objects.
- Treat each retained raster as the smallest semantically complete editable unit. A unit must be independently movable, resizable, replaceable, and removable without changing an unrelated neighboring concept. Never retain a full row, timeline strip, multi-panel collage, or grouped illustration band when it can be split into independent milestone, person, product, scene, or icon-level assets.
- Define the final renderer contract before authoring. A strict comparison is invalid if either image is resized, resampled, cropped, padded, or exported by a different renderer after the contract is frozen.
- Before approving a Route B blueprint, verify that every required editable element can be reproduced by the selected PowerPoint renderer. Do not approve geometry that native PowerPoint cannot render, such as a deliberately stretched native doughnut chart, unless the user explicitly accepts a raster or shape-based exception.
- Crop raster assets tightly from the source so they do not contain unrelated text, lines, icons, or neighboring panels.
- Match the source aspect ratio, positions, sizes, colors, alignment, layering, and whitespace exactly. “Visually close,” a high similarity score, or a small average error is not completion.
- In pixel-perfect mode, the frozen reference is immutable ground truth. The only passing result is an actual PPTX render with the same pixel dimensions, `changed_pixels = 0`, and `max_channel_delta = 0` after the declared renderer and color-mode normalization. Never claim “100%,” “zero difference,” or “pixel-perfect” when these conditions are not met.
- Any authoring-backend preview is diagnostic only. The render produced from the exported PPTX by the frozen renderer is authoritative for acceptance.
- Never obtain a zero-difference result by embedding the complete reference as a slide-sized image. Pixel equality and native editability are simultaneous requirements.
- If editable PowerPoint rendering cannot reach zero difference because of an identified renderer, font, or antialiasing limitation, keep the task open or report the exact blocker and residual metrics. Do not silently relax the gate.
- In Route B, never start PPTX reconstruction until the user explicitly approves the displayed full-page blueprint or blueprints.
- After approval, do not reinterpret, improve, simplify, or regenerate the layout. Treat the frozen blueprint and content lock as the only design specification.
- Generated imagery defines composition and visual language, not factual truth. Reconstruct every word, number, table value, label, and source from the approved content lock rather than trusting rasterized generated text.

## Workflow

### 0. Complete Route B blueprint design when required

Skip this step only for Route A.

1. Build an exact content lock from user-provided material. Separate immutable copy/data from design choices. Do not invent facts or fill evidence gaps.
   Before freezing a newly authored Route B title, apply `references/slide-title-system.md`: use a direct topic label that tells the reader what the page covers. Put the takeaway in a subtitle, chart title, metric, or conclusion box instead of turning the page title into a sentence. If the user supplied exact title wording, preserve it unless they explicitly request title editing.
2. If the user supplied a sufficiently specific brand guide, template, or visual reference, use it. Otherwise generate three distinct full-slide 16:9 visual-direction prototypes using the same representative content and show all three images directly in the conversation. Use the selected runtime adapter's blueprint method; do not assume a named image-generation tool exists.
3. Stop for user selection or revision. Do not generate the final deck or PPTX yet.
4. Lock the chosen visual system: canvas, grid, surface colors, typography hierarchy, icon language, chart language, margins, spacing rhythm, page furniture, and target density. Run a native-feasibility review before approval: classify every P0/P1 element as `exact_native`, `native_renderer_risk`, `minimum_raster`, or `contract_conflict`. Resolve every `contract_conflict` in the blueprint stage.
   When charts or atmospheric backgrounds are useful, choose them from `references/visual-enhancement-system.md`. Keep these enhancements optional and blueprint-bound: do not apply them to Route A unless the user requested a redesign, and do not add or restyle them after blueprint approval.
5. Generate one complete 16:9 blueprint per slide. Generate separate images, never a contact sheet or montage. Display every blueprint directly to the user.
6. Apply requested changes as targeted edits with the same blueprint backend while preserving all unmentioned elements. Repeat until the user explicitly approves the blueprint set.
7. Freeze the approved images, prompts, content locks, component inventories, editable-text regions, raster-only candidates, and SHA-256 hashes. Run `scripts/freeze_blueprint.py` to create the immutable handoff manifest.
8. Begin reconstruction only from this frozen package. If the user later requests a design change, return to the blueprint stage, create a new version, obtain approval again, and refreeze.

### 1. Inspect the reference

Open the approved image at original resolution. For Route B, verify that its SHA-256 matches the frozen handoff manifest before measuring it. Record its pixel dimensions and use that aspect ratio for the slide canvas. Identify all visible text and structural regions before writing code.

For a pixel-perfect request, freeze the authoritative PowerPoint renderer, renderer version, font environment, color mode, and exact output width/height before writing slide code. Prove that the renderer can emit those exact dimensions. Do not use a resized render for final comparison; interpolation changes glyphs, rules, gradients, and antialiasing across the whole page.

Sample the actual background and panel fills from several empty pixels in the reference. Do not assume that an apparently white page is `#FFFFFF`: many references use warm white, cool white, paper texture, subtle gradients, or region-specific mattes. Define shared `BG`, `PANEL_BG`, and other region-fill constants from these measurements before placing any cropped assets.

Read [references/background-and-matte.md](references/background-and-matte.md) whenever the page contains cropped raster assets or any near-white background. Use `scripts/sample_matte.py` to record source-region colors and crop-edge colors instead of relying on visual judgment alone. When the source contains paper variation, gradients, faint environmental line art, or background texture, also read [references/background-layer-extraction.md](references/background-layer-extraction.md) completely. Use `scripts/extract_content_free_texture.py` for a measured texture plate and run its contamination audit before admitting the asset.

Create an object inventory:

- editable text boxes;
- native shapes, rules, borders, arrows, tables, charts, timelines, and callouts;
- repeated components and alignment grids;
- raster-only photographic or illustration assets;
- foreground/background layering relationships.

Assign every visible object a P0/P1/P2 registry entry and a rebuild class. Authoring cannot begin while a P0/P1 item is unregistered. Record native-renderer risks separately from missing assets so a chart or font limitation is discovered before the slide is mostly rebuilt.

Read [references/reconstruction-patterns.md](references/reconstruction-patterns.md) when the page contains dense tables, workflows, portraits, product imagery, charts, or complicated icon systems.

Read [references/curves-and-scene-backgrounds.md](references/curves-and-scene-backgrounds.md) completely whenever the reference contains arbitrary curves, dashed trajectories, hand-drawn outlines, room/environment line art, or a decorative background scene. Register semantic curves separately from background-scene strokes. Decompose the page into native surface, content-free texture, independently removable scene plates, and semantic objects before placing foreground content.

For every 1:1, 100%, zero-difference, or pixel-level reconstruction request, read [references/pixel-perfect-reconstruction.md](references/pixel-perfect-reconstruction.md) completely before authoring the slide. Create the reference/render contract and pixel-diff ledger described there.

### 2. Transcribe exactly

For Route A, transcribe every visible word, number, punctuation mark, footnote, header, and label exactly as shown. Zoom or crop the source for inspection when text is small. Do not silently guess illegible copy; ask only when the source truly cannot resolve it.

For Route B, use the frozen content lock as the authoritative text and data source. Use the blueprint only to determine geometry, hierarchy, wrapping intent, styling, and component relationships. Generated-image spelling or numeric artifacts must never overwrite the content lock.

Preserve visible spaces around quotation marks, separators, Latin text, numbers, and Chinese punctuation. Compare the source string and authored string character by character before layout tuning; typography cannot compensate for missing or added characters.

Read [references/typography-and-text-fit.md](references/typography-and-text-fit.md) for every dense slide or whenever the reference and rendered text differ in width, weight, baseline, or line spacing. Use `scripts/measure_text_ink.py` to compare rendered ink bounds and per-line row spans.

### 3. Establish geometry

Use the source pixel coordinate system as the reconstruction coordinate system whenever possible. Set the PowerPoint slide size to the source image width and height or an exact proportional equivalent.

Measure major regions first, then nested objects:

1. page margins, title, header, and footer;
2. primary columns, panels, and tables;
3. internal rows, dividers, nodes, and labels;
4. icons, image crops, fine rules, and decorative details.

Prefer shared constants and helper functions for repeated typography, shapes, rules, and cells.

Treat the visible glyph bounds as the target, not merely the text-box rectangle. Measure the source text's ink bounding box, line tops, line bottoms, and line-to-line intervals. Record font family, explicit typeface, font size, weight, alignment, text-box insets, line spacing, vertical alignment, wrapping, and autofit as independent parameters.

### 4. Prepare raster-only assets

Crop photographs, portraits, product renders, and complex illustrations into separate files under the temporary build directory. Inspect every crop at full size.

Create an asset manifest before placement. For each crop record `asset_id`, semantic owner, source image and pixel box, target slide box, alpha or matte mode, underlying region fill, SHA-256, and the reason it cannot be native. This manifest is the admission list for `ppt/media/`; unexplained media fails QA.

Before cropping, define the asset boundary by semantic ownership rather than rectangular convenience. Ask: “If the user moves or replaces this object, should any neighboring concept move with it?” If the answer is no, split them. For timelines and process diagrams, create one raster asset per milestone or scene; keep dates, captions, connectors, baselines, arrows, containers, and labels as separate native PowerPoint objects. For comparison layouts, create one asset per person, product, or side. A single strip containing several otherwise independent illustrations fails the editable-object requirement even when it contains no text.

After building the PPTX, inspect `ppt/media/` and verify that no composite row or full-region raster survived. The media count and filenames should correspond to the documented minimum semantic units. Record any justified exception in `source-notes.txt`.

Reject a crop when it includes neighboring words, rules, icons, or excessive page background. Adjust the crop or use an appropriate image-editing workflow when clean isolation is impossible.

For every retained crop, sample its empty corner and edge pixels and compare them with the PowerPoint fill directly underneath it. The crop matte and underlying slide/card fill must match closely enough that no rectangular boundary is visible. Prefer transparency for a genuinely isolated object; otherwise preserve the source-region matte and reproduce that exact matte in PowerPoint. Never place a warm-white crop on a pure-white card, or vice versa.

Treat anti-aliased edge halos separately from the crop's broad matte. Removing a background is acceptable only when the subject edge remains clean at full size; otherwise retain the original matte and match the PowerPoint region to it. Do not recolor photographic pixels to force a match.

Document every retained raster asset in `source-notes.txt` and the slide's `[Sources]` speaker-notes block.

### 5. Rebuild with native objects

Implement the slide with the authoring backend frozen during runtime bootstrap. Use `@oai/artifact-tool` only when the Codex adapter and its Presentations capability select it. Use PptxGenJS for the portable path. Do not mix backends within a strict comparison run.

Set the explicit typeface or font face supported by the selected backend for every shared text style. Do not rely on an application default. Set text-box insets explicitly; backend defaults can shift visible glyphs even when object coordinates are correct. Disable automatic shrinking during fidelity reconstruction so it cannot hide a typography mismatch.

Use this priority order:

1. native text boxes for all text;
2. native PowerPoint tables when the reference is tabular, or precisely aligned native cell rectangles when fidelity requires it;
3. native lines, custom paths, shapes, connectors, and simple symbols for diagrams, semantic curves, and icons;
4. native charts when the reference represents data and the data values are readable;
5. independent cropped images only for raster-only assets.

For native charts, build a one-chart renderer proof before committing the slide. Calibrate plot-area bounds, chart-area margins, axis/legend suppression, first-slice angle, hole size, point colors, labels, and aspect behavior against the actual PPTX render. If the approved geometry is impossible for the native chart renderer, do not conceal the conflict with offsets; return to the blueprint or obtain an explicit contract exception.

Create connectors before diagram nodes so arrows remain behind nodes. Keep foreground object order consistent with the reference.

Do not approximate an arbitrary fixed curve with PowerPoint's automatically routed curved connector. Use a native custom path with source-coordinate line segments when the silhouette must remain fixed. Use a curved connector only when attachment and rerouting are part of the intended editability.

### 6. Preview and correct

Export a preview PNG through the selected adapter and inspect it at full-slide size. Compare it with the reference for:

- unexpected text wrapping;
- font substitution;
- missing or changed words;
- incorrect line thickness or color;
- image crops containing foreign content;
- visible rectangular mattes or halos around cropped assets;
- background/panel fills that were assumed rather than sampled from the source;
- panel, column, row, and baseline drift;
- broken layering or hidden objects;
- inconsistent repeated objects.
- text ink bounds that differ from the source despite matching text-box coordinates;
- incorrect text-box insets, line spacing, baseline positions, or font fallback;

Inspect cropped assets at 200% or greater. Sample pixels immediately outside each crop boundary in the rendered preview and compare them with the crop's empty edge pixels. Correct the PowerPoint fill, crop bounds, transparency, or layering whenever a rectangular seam remains.

For each primary title and representative body block, compare the preview's ink bounding box and line spans with the reference. A 1–2 pixel difference is useful only as an intermediate diagnostic target; it is not a passing result in pixel-perfect mode. If the exact font is unavailable, test installed candidates and choose by glyph silhouette, weight, ink width, and ink height before adjusting font size. Do not use font size alone to conceal a wrong typeface.

Replace unstable emoji with native shapes, plain text symbols, or isolated icon assets. Never accept a system emoji that changes color or appearance during export.

### 7. Validate the actual PPTX

Render the exported PPTX with the frozen host renderer or `scripts/render_pptx.py`, inspect every slide individually, and run the adapter's overflow test. Fix all unintended clipping, overlap, wrapping, or displacement before delivery.

Repeat the matte comparison against the actual PPTX render, not only the artifact preview. Office/LibreOffice export can expose seams that were not obvious in the construction preview.

For textured or illustrated backgrounds, record pixel metrics before and after every texture/scene-layer change. Do not flatten large semantic regions by excluding their complete bounding boxes from the texture plate; retain only near-surface pixels across the canvas, then exclude the smallest contaminated region when necessary. An improved changed-pixel percentage is iteration evidence, never a passing result.

Repeat the typography comparison against the actual PPTX render because font substitution and text metrics can change during export. Recheck titles for one-line fit and body blocks for every line's baseline interval.

Run `scripts/compare_slide_pixels.py` against each frozen reference and its corresponding actual PPTX render. Use strict mode for final acceptance. Inspect the generated difference image and bounding box after every failing comparison. Correct the smallest responsible object, rerender the PPTX, and repeat until the strict comparison exits successfully. A deck passes only when every slide passes independently; a montage or deck-level average cannot hide a failing page.

Classify every failure before changing code: `dimension_or_renderer`, `background_or_texture`, `typography`, `geometry`, `matte_or_alpha`, `missing_or_composite_asset`, `layering`, or `native_renderer_limit`. Distinguish font-file/hinting residuals from native line antialiasing residuals with isolated renderer proofs. Do not make global changes in response to a local diff island. If the diff bounding box covers the full slide, fix the renderer/canvas/background contract before moving individual objects.

Use [references/qa-checklist.md](references/qa-checklist.md) for the final pass.

### 8. Deliver cleanly

Place only the final PPTX in the user-facing output directory. Keep previews, inspection NDJSON, crop files, scripts, and rendered QA images in the temporary work directory.

State briefly that the deck is native/editable, that the complete reference or blueprint image was not embedded, and that rendering and overflow checks passed. Cite the final PPTX exactly once.
