---
name: ui-from-image
description: Convert one or more webpage/app UI screenshots into a high-fidelity responsive implementation, either as a standalone page or by adapting an existing frontend. Prioritize exact viewport matching, typography/icon audits, explicit spacing and colour matching, browser screenshot comparison, and repeated refinement until no obvious mismatches remain. Handle missing assets by using supplied files, generating missing raster assets with direct image_gen when available, preferably as extractable asset sheets for multiple related assets, or otherwise using placeholders plus a single copy-paste code block containing one standalone generation prompt per remaining asset.
---

## Mission

Treat the provided reference image(s) as the visual source of truth.

Accuracy beats speed. Do not stop at "close enough". The task is not finished when the page merely works; it is finished when the rendered result is a close visual match and there are no obvious mismatches left.

Bias toward more verification passes rather than fewer. If there is a realistic chance that text is wrong, a control is crowded, spacing is fragile, or a layout bug is hidden by one viewport, keep iterating.

Do not describe the result as "good enough", "ready to ship", or equivalent unless all mandatory verification and reporting steps in this skill are complete and no known visible mismatch remains beyond clearly stated minor uncertainty.

## Default output

Unless the repo already dictates another structure, use:
- `index.html`
- `styles.css`
- `script.js`

If adapting an existing frontend/framework, follow the repo's file structure while keeping markup, styling, and behavior as cleanly separated as the framework allows.

## Operating mode

- For standalone work, default to plain HTML/CSS/JS unless the environment already includes a styling system the user wants to keep.
- Reuse the repo's existing Tailwind/DaisyUI setup when present.
- If the repo already has a different established styling system, do not introduce Tailwind/DaisyUI as a competing second system unless the user explicitly asks for it.
- If Tailwind/DaisyUI are already available or explicitly requested, treat them as implementation tools rather than design authority. Override defaults whenever the screenshot differs.
- First achieve fidelity at the exact reference dimensions of the primary screenshot.
- For desktop webpage work, do not treat a narrow mockup or POC screenshot as the final real-page desktop width. After the reference-size pass, prefer adapting the layout to a real desktop viewport around `1900px` wide, allowing roughly `1900px` rather than `1920px` to account for a scrollbar and normal browser chrome.
- Only after the reference-size version is visually close should you derive tablet/mobile behavior.
- When the user supplies a newer or revised screenshot, the latest screenshot becomes the source of truth.

## High-fidelity rules

- Match layout, spacing, typography, line height, letter spacing, colours, borders, border opacity, shadows, gradients, border radius, imagery crop/aspect ratio, and visual hierarchy as closely as possible.
- Use explicit values for widths, heights, max-widths, padding, margin, gap, border radius, font size, line height, tracking, and shadow when defaults are not close enough.
- Treat text fidelity as a layout problem as well as a content problem. If text is clipped, crowded, truncated, wrapped incorrectly, or pushes nearby controls out of alignment, the page is not done.
- Treat data visualizations and proportional graphics as layout-critical UI, not decorative approximations. Chart plot areas, axes, legends, segment widths, map regions, funnels, gauges, timelines, and diagram shapes must match the reference proportions and alignment closely enough that a user would read them as the same interface.
- Treat every visible detail as required, including micro-details:
  - small logos and button icons
  - search icons
  - dropdown carets
  - pagination chevrons
  - active nav underlines / glows
  - status dots
  - bullet colours
  - card icons
  - star/favorite icons
  - divider lines
  - subtle corner radii differences
  - text opacity changes
- Missing a small icon or logo inside a control is a fidelity failure, not a minor omission.
- Do not redesign, simplify, embellish, or "improve" the UI unless required for responsiveness or because the reference is genuinely ambiguous.
- Do not silently rely on DaisyUI typography, button styles, input styles, or spacing scale if they do not match the reference.

## Existing frontend adaptation mode

When working inside an existing frontend or design system:
- Inspect the current codebase before creating new structures.
- Reuse existing layout shells, shared components, utility patterns, typography tokens, spacing scales, breakpoints, icon conventions, and theme variables wherever they can faithfully express the reference.
- Prefer adapting a nearby existing page or section over creating a parallel implementation from scratch.
- Do not introduce duplicate components, conflicting design tokens, or a second styling system unless the user explicitly asks for it.
- If the screenshot conflicts with the established design system, preserve the screenshot's page-level composition while staying as consistent as possible with the current tokens/components, unless the user explicitly says the screenshot should override the current design language.

## Reference intake and breakpoint handling

- Record the exact dimensions of each reference image before coding.
- For the primary fidelity pass, render the page at the exact reference viewport size in CSS pixels whenever possible.
- If the reference desktop image is substantially narrower than a modern desktop viewport, treat that width as a composition/style reference rather than the final real-page desktop width. Preserve the screenshot's structure, hierarchy, spacing intent, and visual language, then expand and validate the actual desktop implementation at about `1900px` viewport width.
- If multiple reference images are provided for desktop/tablet/mobile, treat each as authoritative for its breakpoint.
- If only a desktop reference exists, infer tablet/mobile layouts by preserving hierarchy, ordering, and visual balance without inventing new sections or interactions.
- If text is legible, reproduce it exactly, including punctuation and small helper labels.
- If text is unclear, use the closest reasonable approximation and report the uncertainty.
- If the screenshot shows a cropped region of a page rather than a full page, match the visible region first.

## Viewport honesty and scaling safety

- Treat browser zoom, OS DPI scaling, and device pixel ratio as environmental factors that the implementation must tolerate, not as excuses to distort the layout.
- When Playwright or similar browser automation is available, treat automation-controlled screenshots captured at an explicit viewport size as the primary fidelity reference for comparison.
- Do not treat a headed browser window as the source of truth for pixel fidelity when OS DPI scaling, browser zoom, window chrome, or desktop compositor behavior may affect what the human sees on screen.
- On Windows in particular, assume non-default desktop scaling or browser zoom can make a headed browser visually misleading even when the underlying page layout is correct in CSS pixels.
- If Playwright reports that it opened a `chrome` or `msedge` browser/channel, that is still Playwright-driven verification. Do not describe this as "switching away from Playwright" unless browser automation was actually abandoned.
- Do not use CSS `zoom`, root-level `transform: scale(...)`, synthetic wrapper scaling, or similar viewport hacks to make the implementation screenshot look closer to the reference.
- Do not "fix" width, crowding, or fold-position mismatches by shrinking the entire page or inflating the canvas.
- Solve screenshot mismatches with real layout changes:
  - correct container widths
  - correct grid and flex sizing
  - correct gaps and paddings
  - correct font sizes and line heights
  - correct control heights and intrinsic widths
  - correct responsive breakpoints
- If a browser-specific mismatch appears, first suspect invalid layout assumptions, overflow, or scaling hacks in the implementation before blaming the user's environment.
- If there is a mismatch between a headed browser window and a Playwright screenshot taken at the calibrated viewport, trust the screenshot first for fidelity work and investigate the implementation with additional screenshot passes before attributing the difference to the user's machine.
- When reporting fidelity status, distinguish between:
  - expected reflow differences caused by user/browser zoom preferences, and
  - genuine layout bugs such as horizontal overflow, incorrect width calculations, broken wrapping, or fragile breakpoint behavior.

## Scroll-Resilience Check

For layouts with sticky/fixed sidebars, tool panels, inspectors, menus, or any viewport-height region:
- Verify that every region with content taller than the viewport can be scrolled independently.
- Do not rely on `height: 100vh` alone for fixed/sticky panels; add appropriate `overflow-y: auto` where content may exceed available height.
- Test at least one shorter desktop viewport height or zoom-like condition when the design includes a full-height sidebar or tool panel.
- Confirm lower controls, footer actions, account cards, collapse buttons, and secondary navigation remain reachable.
- Treat unreachable panel content as a functional layout bug, not only a visual mismatch.

## Persistent Navigation And Panel Width

For persistent navigation, sidebars, rails, inspectors, and tool panels:
- Verify expanded labels fit without internal horizontal scrolling at desktop and wide/zoom-like desktop widths.
- Check horizontal overflow inside the panel itself, not only on `document.documentElement`.
- Capture a focused crop of the panel when it contains labels, icons, badges, counters, account controls, collapse buttons, or footer actions.
- Prefer sufficient intrinsic panel width, `nowrap`/ellipsis for labels, independent panel scrolling, and explicit collapsed breakpoints over letting panel content squeeze or create a horizontal scrollbar.
- Verify collapsed or icon-only states do not trigger too early, too late, or only because text no longer fits.
- Treat clipped labels, panel-level horizontal scrollbars, hidden footer controls, and labels colliding with icons/badges as layout failures.

## Data Tables And Panel Footers

For cards, panels, data tables, grids, and list modules:
- Check internal scroll containers, not only page-level overflow. A table or grid can have its own horizontal scrollbar even when the document width is fine.
- Verify footer links, CTAs, pagination, summary rows, and secondary actions remain visually inside the card or panel boundary.
- Capture a focused crop of any table/list panel that has many columns, nowrap text, avatars, badges, row menus, pagination, or a footer CTA.
- Prefer explicit column sizing, table layout rules, responsive row-card alternatives, or intentional horizontal scrolling with visible affordance over accidental overflow.
- Treat accidental internal horizontal scrollbars, clipped row-action icons, stray text ellipses from overflowed action cells, and footer links escaping below the panel border as failures.

## Preflight checklist

Before implementing, explicitly inspect and inventory:

1. Page sections and their order
2. Grid / column structure and approximate width ratios
3. Major containers and card boundaries
4. All text blocks and labels
5. All visible controls and interactive states
6. All icons, logos, badges, chips, status dots, separators, and decorative marks
7. All image assets and background graphics
8. Typography groupings (hero title, body copy, pills, buttons, table headers, table rows, side cards, notices, etc.)
9. Primary, secondary, muted, success, warning, danger, and accent colours
10. Likely responsive intent
11. Any regions where copy length, chip count, or control density make crowding likely
12. Any rows or panels that must remain on one line at the reference breakpoint
13. Every data visualization, including its card bounds, plot-area bounds, axes, labels, gridlines, legends, controls, marker positions, series shapes, and empty padding
14. Every proportional graphic or diagram, including relative segment sizes, taper direction, alignment, labels, fills, strokes, and surrounding whitespace
15. Every navigation or toolbar icon matched item-by-item against the reference, including active states, badge placement, stroke weight, and whether the glyph itself is the same concept

Do not start coding until you have a working mental map of every visually meaningful element.

## Typography audit

Typography is a first-class fidelity target.

- Inspect the repo for existing font sources first:
  - global CSS
  - Tailwind config
  - DaisyUI theme config
  - design tokens
  - existing page components
  - local font files
- If an existing project font matches the reference, use it.
- If the reference appears to use a custom or non-default font and the exact font is unavailable, choose the closest available option and report that limitation explicitly.
- Do not default to generic DaisyUI/body typography without checking.
- Confirm the rendered fallback font, not only the declared `font-family`. A declared first-choice font may not be installed, and an installed font may be visibly wider, narrower, heavier, or softer than the reference.
- Set typography explicitly for each visual group:
  - logo text
  - nav links
  - pills / badges
  - hero heading
  - lead paragraph
  - stat labels
  - stat values
  - helper text
  - filter chips
  - form labels
  - table headers
  - table rows
  - sidebar headings
  - notifications / timestamps
  - primary and secondary buttons
- Check not only font family, but also:
  - size
  - weight
  - line height
  - letter spacing
  - apparent glyph width / character fit
  - case
  - colour / opacity
- Avoid artificial tracking or wide letter spacing unless the reference clearly shows it. Extra tracking on large numbers, headings, table text, or nav labels can make a UI look zoomed-in and can cause avoidable truncation.
- For dense dashboards, forms, tables, navs, and operational UIs, compare whether common labels and values occupy similar horizontal space to the reference. If text looks too wide, try a closer system font stack, remove unnecessary tracking, reduce weight, or adjust group-specific font sizes before changing layout.
- Validate text wrapping and line breaks at the reference width. If a heading or paragraph wraps differently from the screenshot, fix it.
- Validate text integrity for controls and dense UI:
  - no unintended truncation
  - no clipped ascenders/descenders
  - no vertical squashing from incorrect line height or control height
  - no label/helper text collisions
  - no placeholder text overflowing its field

## Iconography and completeness audit

Before declaring the page done, verify that every visually meaningful icon or mark from the reference is represented in the DOM.

This includes:
- logo marks
- sidebar, tab bar, toolbar, and command palette icons
- brand icons inside buttons
- search icons
- dropdown carets
- stat-card icons
- status indicators
- row, table, list, and card action icons
- map / notification bullets
- table favorite icons
- pagination arrows
- close / reset / filter icons
- any subtle inline symbols

Rules:
- Small UI icons count as assets and must not be omitted.
- Navigation icons must be audited item-by-item. A generic placeholder icon is acceptable only when the reference glyph is genuinely unreadable; otherwise match the same visual metaphor, stroke weight, size, and alignment.
- Repeated row-action icons must be audited as a set and individually. Confirm the intended semantics are preserved, such as comment vs edit vs open/external-link vs copy vs delete vs overflow; do not substitute a visually similar control with a different meaning.
- For webpages and web apps, prefer existing repo icons or simple inline SVGs only when the glyph is simple enough to reproduce accurately and a focused visual pass confirms it matches the reference.
- Treat complex icons, detailed pictograms, custom illustrated buttons, branded controls, badges, medals, tabs, toggles, game-like controls, bespoke UI ornaments, textured surfaces, and other visually distinctive UI elements as assets when SVG/code recreation would be fragile or visibly wrong.
- Do not rely on CSS pseudo-elements, borders, or clip-path tricks for icons when the glyph has a recognizable outline, holes, star points, curved arcs, brand-like geometry, or a specific visual metaphor. Use an inline SVG or existing icon component so the icon remains visible and comparable to the reference.
- Do not add a new icon library unless the repo already uses one or the user explicitly asks for it.
- For common brand marks used in UI controls (for example Discord), use a clean inline SVG or existing icon component unless the repo already has an appropriate asset.

## Data Visualization and Diagram Fidelity

Charts, diagrams, and dense analytic graphics need their own explicit pass. Do not collapse them into a generic "looks like a chart" implementation.

For every chart-like region, record and match:
- card size and chart-region size separately
- plot-area width, height, and inset from the card edges
- legend position, legend swatch style, and spacing from the title or plot
- axis label count, axis side, tick label positions, and gridline count
- series colour, stroke width, dash pattern, curvature, marker size, and rough point trajectory
- control placement around the chart, such as segmented buttons, dropdowns, zoom controls, range pills, or toolbars
- summary/footer rows below the plot, including column widths and separator lines

For every proportional graphic, record and match:
- overall bounding box and alignment within its card
- number of segments, their relative heights and widths, and whether they taper, expand, overlap, or step
- label placement inside or outside each segment
- colour order, opacity, borders, shadows, and gaps between segments
- companion labels, callout boxes, legends, or side metrics and their distance from the graphic
- whether text is fully contained in the intended segment or intentionally outside it, with no label spillover, clipping, or crowding

For circular charts such as donuts, pies, gauges, and radial progress indicators:
- Audit center labels separately from the chart shape.
- Match the center label's font size, weight, line height, and vertical alignment against the reference.
- Ensure the label fits comfortably inside the inner circle at the reference viewport and responsive breakpoints.
- Prefer explicit flex/grid centering and line heights for center labels.
- If the center label appears crowded, oversized, off-center, or clipped, fix typography and inner radius before declaring the chart matched.

Implementation guidance:
- Use inline SVG for non-rectangular proportional graphics such as funnels, pyramids, gauges, radial charts, maps, node graphs, complex timelines, and icon-like diagrams unless the reference can be matched exactly with normal layout boxes.
- Avoid approximating complex shapes with stacked divs, pseudo-elements, border triangles, or CSS `clip-path` when segment width, taper angle, separator gaps, or label placement need to be faithful. Those techniques are acceptable only after a screenshot pass proves the geometry and text containment match.
- When an SVG viewBox is used, set explicit width, height, polygon/path coordinates, text anchors, and label positions rather than relying on auto scaling or centered layout alone.

When a chart or diagram looks too narrow, too tall, too centered, too simplified, or visually detached from its surrounding card, treat that as a geometry mismatch. Fix container tracks, plot insets, SVG viewBox/aspect ratio, control widths, and neighbouring column ratios before moving on to responsive work.

## Layout fitting and crowding rules

For the reference breakpoint:
- Recreate the screenshot's composition before making responsive adaptations.
- Do not solve crowding by prematurely redesigning, deleting, shrinking, or reflowing major groups.
- Do not solve crowding by scaling the whole page with CSS or by relying on browser zoom assumptions.
- First exhaust fidelity-preserving options:
  - match the reference viewport size
  - correct container widths and side-column widths
  - tighten or loosen gaps to the measured values
  - use the correct font size and line height
  - use correct control widths and min-widths
  - use the correct track sizing for each grid column instead of evenly distributing everything
  - give dense controls the width they actually need before shrinking neighboring elements
  - use wrapping only where the screenshot already implies wrapping
  - inspect whether the reference actually uses multiple rows
- Only move controls to additional rows at the reference breakpoint if:
  - the screenshot explicitly shows multiple rows, or
  - the user provides a revised screenshot showing the updated structure.
- If controls still feel crowded after a pass, assume the proportions are still wrong and continue iterating. Do not normalize crowding as "good enough."
- For narrower breakpoints, reflow cleanly while preserving hierarchy and visual balance.

## Colour, surface, and effects audit

- Match primary surfaces, secondary surfaces, muted surfaces, borders, glows, shadows, gradients, and text opacities as closely as possible.
- When possible, sample or estimate colours from the reference instead of inventing new values.
- Pay attention to:
  - background gradients
  - subtle border alpha
  - panel transparency
  - hover/active emphasis that is visible in the reference
  - contrast differences between main content and sidebar cards
  - accent colour consistency across badges, live indicators, buttons, and highlights

## Asset handling workflow

### Direct `image_gen` rule

When raster assets are missing and would materially improve the implementation, use the native `image_gen` tool directly by default. Do not require the separate `imagegen` or `imagen` skill to be installed.

After `image_gen` runs, continue the same turn unless the user explicitly requested image-only output. Briefly identify what was generated, provide the saved file path or asset reference when available, assess whether it matches the request, and continue with saving, integration, and verification.

If `image_gen` is unavailable or fails, fall back to placeholders plus one standalone generation prompt per missing asset.

Operational rules for direct `image_gen`:
- Treat generated outputs as project-bound assets when they are used by the implementation. The built-in tool may save under `$CODEX_HOME/generated_images/`; move or copy the selected final into the workspace before referencing it in code.
- Do not rely on a destination-path argument for the built-in tool. Generate first, then move or copy the selected output.
- Do not overwrite existing assets unless the user explicitly asked for replacement. Otherwise create a sibling filename such as `hero-v2.png` or `card-thumbnail-generated.png`.
- For multiple missing raster assets, prefer generating one or more asset sheets rather than one image per asset when the assets are related and can fit cleanly on a single canvas.
- Use multiple asset sheets when the assets are too numerous, visually unrelated, need different styles, need very different aspect ratios, include text-heavy content, or would become too small to extract accurately from one sheet.
- For edits of a local file, inspect it with `view_image` first so it is visible in the conversation context. Label each input image by role, such as edit target, style reference, composition reference, or supporting insert.
- Shape prompts compactly around asset type, purpose in UI, subject/content, composition/framing, style/medium, lighting/mood, colour palette, exact text if any, constraints, and avoid notes. For edits, repeat invariants such as "change only X; keep Y unchanged."
- Do not treat fallback CLI/API controls such as quality, input fidelity, masks, output format, or output path as built-in `image_gen` tool arguments.

When transparency is requested, verify the saved PNG has a real alpha channel before finishing. Inspect metadata or pixels with a tool such as Pillow or .NET `System.Drawing`; a valid transparent PNG should be alpha-capable, such as `RGBA` or `Format32bppArgb`, and representative background pixels such as the corners should have alpha `0`. If the generated file has a rendered checkerboard or solid background, leave it untouched, create a repaired derivative with a clear name such as `*-transparent.png`, and re-verify the repaired output.

### Asset sheet generation and extraction

When several missing raster assets should be generated, default to an asset-sheet workflow:

1. Group compatible assets into a single sheet prompt. Group by shared style, lighting, perspective, medium, and target use. Keep separate sheets for assets that need incompatible styles, fine text, exact brand marks, very different proportions, or large detail.
2. Ask for a clean contact sheet or sprite sheet: one asset per cell, generous gutters, consistent scale, front-facing or clearly framed subjects, no overlaps, no shadows crossing cell boundaries, no labels unless the UI asset itself requires text, and a flat removable background colour that does not appear in the assets.
3. Prefer a high-contrast flat background such as pure magenta, cyan, or another chroma-key colour when transparency is needed. Do not rely on the image model to produce real transparency, and do not request checkerboard transparency.
4. After generation, copy the selected sheet into the workspace, then extract individual assets with a local script, preferably Python Pillow. Leave the original generated sheet untouched.
5. During extraction, crop each cell or detected object, remove the keyed background or edge-connected neutral background, trim transparent padding, add any needed safe padding, and save each asset with a clear filename in the project asset folder.
6. Verify every extracted transparent PNG has an alpha-capable mode such as `RGBA` and representative background/corner pixels with alpha `0`. Visually inspect extracted assets before integrating them.
7. Integrate the extracted individual files, not the full sheet, unless the implementation intentionally uses a sprite sheet.
8. If extraction damages edges or removes internal details, keep the original sheet, repair the extraction mask, or regenerate with clearer spacing/background before using the asset.

Use one asset sheet when the likely generated assets will remain large and separable. Use more than one sheet when a single sheet would make assets small, ambiguous, hard to crop, or stylistically inconsistent.

First, inventory every visible asset required by the page:
- logos
- hero images
- thumbnails / cards
- maps
- avatars
- icons
- custom buttons and button artwork
- custom controls, toggles, tabs, badges, medals, stickers, cursors, handles, knobs, or UI ornaments
- desktop/game/app-specific chrome, HUD pieces, menu plates, inventory slots, tool icons, or decorative interface parts
- illustrations
- background graphics
- any other non-text visual elements

For each asset, choose exactly one path.

### 1) User supplied the asset

- Visually inspect it before use.
- Use it where appropriate.
- Crop, resize, pad, trim, or mask it as needed to match the reference composition.
- Preserve aspect ratio; never distort it.
- Use `object-fit: cover` or `contain` as appropriate.
- If the asset is low-resolution or otherwise imperfect, get as close as possible and note the limitation.

### 2) Asset is missing and should be generated

- Use `image_gen` directly to generate or edit the asset when the tool is available.
- If multiple missing assets can be generated together, use the asset-sheet workflow by default, then extract individual files locally.
- If only one asset is missing, or one asset needs unique composition/detail, generate it individually.
- For webpages and web apps, implement simple UI glyphs as inline SVG or existing repo icons only when they can be matched visually; otherwise generate/extract them as image assets.
- For non-web UI such as desktop apps, game HUDs, menus, inventory screens, launchers, or highly skinned tools, expect many custom UI elements to be image assets unless the code-native recreation is clearly faithful and verified.
- Save generated assets in the repo's existing asset location, or a sensible folder such as `assets/generated/` if no convention exists.
- Update the consuming code or markup to reference the generated asset.
- Validate that each extracted or generated asset fits the layout visually and dimensionally.
- Re-crop, regenerate, or iterate if needed until the asset works in context.
- If `image_gen` is unavailable, generation fails, or extraction cannot be repaired in the current turn, use a clearly labeled placeholder and output one standalone generation prompt for each still-missing asset.

### 3) Asset is missing but should not be generated

Use this path for proprietary brand marks, assets that require exact real-world source material, or cases where the user explicitly asks not to generate images.

- Use a clearly labeled placeholder with the correct approximate dimensions, aspect ratio, border radius, placement, and visual weight.
- If you create or synthesize a temporary stand-in asset yourself instead of a generic placeholder, still treat that asset as missing for reporting purposes.
- Never silently substitute a stand-in, proxy illustration, or synthetic replacement and then omit it from the final missing-assets report.
- Prepare one separate, ready-to-use generation prompt for each missing asset unless the user explicitly asked not to receive prompts.
- Do not collapse multiple still-missing fallback prompts into one combined prompt in the final response. Asset-sheet prompts are for in-turn generation and extraction, not for the final missing-assets fallback block.
- Each prompt must remain standalone, but in the final response all still-missing asset prompts must be grouped together inside one single fenced `text` code block for easy copy/paste into another AI/LLM.
- Separate asset prompts inside that block with a clear divider such as `---`.
- Each prompt must include:
  - asset name / suggested filename
  - purpose in the UI
  - desired subject/content
  - composition / framing
  - style / mood
  - colours / lighting
  - target aspect ratio or dimensions
  - transparency/background requirements if relevant
  - key "avoid" notes

## Asset-specific guidance

- Simple UI icons are not a reason to leave a blank area. For webpages, implement simple glyphs with inline SVG or existing repo icons when they can be visually matched and verified.
- Do not force every icon, button, or custom UI element into inline SVG. Use raster assets when the reference depends on custom illustration, texture, complex geometry, painterly detail, shadows, embossed styling, game/desktop chrome, or another visual treatment that would be unreliable to recreate as code.
- For non-web interfaces, expect custom UI pieces to be generated/extracted image assets more often than inline SVG, unless the existing platform or codebase already provides matching components.
- For repeated icons or shortcut/navigation marks, inspect each rendered icon in screenshot context; a technically present icon that is too faint, clipped, collapsed, or visually unrecognizable still counts as missing.
- For brand logos or proprietary-looking marks that are not provided, use placeholders unless the user explicitly wants a temporary generated stand-in.
- For hero images, thumbnail images, maps, and other prominent visuals, match crop, focal point, aspect ratio, and visual weight as closely as possible.
- If the reference includes repeated thumbnail cards, pay attention to consistent crop and corner radius across all items.

## Implementation workflow

1. Inspect the reference image(s) and build the preflight inventory.
2. If an existing codebase is present, inspect the most relevant pages/components/tokens/icons first and decide what to reuse.
3. Build a first pass that is already visually close.
4. Run or preview the page.
5. Capture an implementation screenshot at the exact reference viewport size.
6. Compare the implementation screenshot against the reference.
7. Make a written mismatch list before editing. Focus on the largest visual errors first, then the micro-details.
8. Repeat screenshot, mismatch list, and fixes until there are no obvious mismatches left.
9. For any chart, map, gauge, timeline, funnel, pyramid, tree, graph, or other analytic visual, do a dedicated visual-primitive pass comparing its bounding box, internal proportions, labels, and controls against the reference before declaring the main layout close.
10. For dense, constrained, high-value, or fragile components, capture focused component screenshots/crops and inspect them at larger scale before relying on full-page judgment. This is mandatory for any component where text, icons, badges, controls, charts, legends, tables, avatars, or action rows must fit inside limited space.
11. Before finishing, do at least one explicit "fragility pass" focused only on:
   - crowded rows
   - clipped or squashed text
   - overlapping elements
   - text, labels, or values that hug a card/control edge without enough padding
   - component boundaries where one card, list, row, popover, or toolbar could grow into the next
   - controls that look too narrow for their content
   - suspiciously tight spacing that may break at slightly different widths
   - fixed-height cards, rows, panels, or sticky regions whose content may overflow, overlap, or become unreachable at higher zoom, DPI scaling, larger fonts, or shorter viewport heights
   - center text inside donuts, pies, gauges, badges, counters, and compact chart labels
12. For repeated UI structures such as card grids, table rows, stat tiles, nav items, or repeated buttons, do one explicit alignment pass and verify that shared baselines, footer rows, button positions, chip rows, and media crops are consistent across siblings.

Do not stop at code edits plus lint/build checks when browser verification is available. Build/test results never replace the required screenshot comparison loop for this skill.

## Mandatory visual verification workflow

When browser and screenshot tools are available, the following passes are mandatory.

If browser tools are available and you have not yet captured and inspected screenshots yourself, you are not done. Do not present the work as finished, ready, or validated. Instead, continue until the screenshot pass is complete or explicitly report the blocking reason you could not perform it.

When a task only changes one dense or visually important region rather than a full page, still capture at least:
- one screenshot showing the changed region in context
- one close screenshot of the changed region itself when tooling supports element or cropped captures

In your final report, never imply that screenshots were checked unless you actually captured and inspected them during the current turn.

In your final report, list the actual visual verification artifacts by category:
- full-page or viewport screenshots inspected
- focused component crops inspected
- scaling/resilience screenshots inspected
- any required visual pass that could not be performed, with the concrete reason

Do not describe component crops, scaling checks, browser checks, or responsive checks as completed unless those exact artifacts were captured and inspected in the current turn.

If the page is too tall to inspect reliably in a single screenshot, capture segmented screenshots that collectively cover the whole page. Prefer top / middle / bottom coverage or more segments as needed. Do not assume unseen lower sections are correct.

For tall pages, the preferred verification pattern is:
- capture one full-page or tallest-practical screenshot artifact when tooling supports it, to understand overall vertical rhythm, section spacing, and macro composition across the whole document
- also capture segmented viewport screenshots that cover the page from top to bottom with intentional scroll positions
- visually inspect the segmented screenshots yourself; do not rely on the full-page artifact alone for lower sections, because tall captures can hide crowding, clipped text, sticky overlaps, or small alignment errors
- make sure the segmented set covers the entire page without leaving unverified gaps between scroll positions
- when a section is especially dense or fragile, add extra local screenshots for that region rather than assuming the nearest segment is sufficient

Treat the full-page screenshot as a macro-composition aid and the segmented screenshots as the authoritative visual inspection set for tall-page fidelity.

### Pass 0 - viewport calibration
- Use the exact primary reference dimensions for the first comparison pass.
- Make sure the page is captured at the correct route/state and comparable scroll position.
- Do not judge fidelity from a different width and then claim a match.
- Keep viewport calibration honest: do not use CSS `zoom`, wrapper scaling, or screenshot-only transforms to force the composition into place.
- Prefer automation screenshots captured at explicit CSS viewport dimensions over visual judgment from a headed browser window.
- If headed mode is used for convenience, use it for interaction/debugging only; do not treat the live window as the authoritative fidelity check when a direct Playwright screenshot is available.

### Pass 1 - macro composition
Check:
- overall page width and margins
- main vs sidebar width ratio
- hero split ratios
- card widths and heights
- chart, diagram, map, media, and table region width ratios inside their cards
- section spacing
- alignment of top nav, hero, filter area, table, and sidebar
- absence of horizontal overflow or suspicious whole-page shrink/stretch behavior
- no rows that appear denser, tighter, or more compressed than the reference

### Pass 2 - typography and copy
Check:
- font family choice
- font size
- weight
- line height
- tracking
- text colour / opacity
- exact copy
- exact line breaks / wrapping
- no truncated, clipped, or visibly squashed text
- no copy mismatches in small labels, helper text, timestamps, badge text, placeholders, or table metadata

### Pass 3 - iconography and control completeness
Check:
- every icon, logo, caret, bullet, dot, and star
- every navigation, sidebar, toolbar, and tab icon matched to the corresponding reference item
- every repeated table/list/card action icon, including whether each glyph has the same semantic meaning as the reference
- button leading/trailing icons
- search icon presence and placement
- inline helper icons
- stat-card icons
- missing micro-details

### Pass 4 - colour and surface treatment
Check:
- gradients
- surface tints
- borders
- border opacity
- shadows
- glows
- pill fills
- badge colours
- table row separators
- muted text tones

### Pass 5 - spacing and fine geometry
Check:
- paddings
- margins
- gaps
- border radii
- chip sizes
- input heights
- button heights
- row heights
- image crop framing
- chart plot-area bounds, axis/gridline placement, series shape, marker placement, legend spacing, and chart-footer geometry
- proportional diagram bounds, segment sizes, taper/step geometry, label placement, and adjacent metric spacing
- proportional diagram text containment: labels must not spill outside their intended segment unless the reference does the same
- icon size inside controls
- card and panel heights, especially when adjacent cards in the same row intentionally have different heights
- internal component vertical balance: charts, donuts, legends, footer links, and CTAs should sit at the same relative height as the reference
- no overlapping layers, clipped corners, or compressed control interiors
- no fields/buttons/selects that are narrower than the reference unless the screenshot clearly shows it
- alignment consistency across repeated components
- matched footer/button baselines across peer cards where the reference implies alignment
- do not force peer cards to equal heights unless the reference shows equal heights; mismatched reference heights are part of the design
- no sibling card or tile whose CTA, stat row, badge row, or title block sits visibly higher or lower than its peers without an explicit reason in the reference

### Pass 5a - component crop checks
For dense, constrained, high-value, or fragile UI regions, capture and inspect focused screenshots of individual components in addition to full-page or segmented screenshots.

Use component-level screenshots for:
- charts, donuts, gauges, maps, funnels, tables, data grids, timelines, and analytic panels
- sticky sidebars, toolbars, inspectors, headers, and filter bars
- persistent navigation panels, sidebars, rails, and tool panels, including expanded labels and collapsed/icon-only states
- table/list panels with footer CTAs, pagination, row actions, nowrap columns, avatars, chips, or badges
- cards, forms, modals, nav bars, sidebars, tab bars, segmented controls, checkout blocks, pricing cards, settings panels, feed/list items, desktop app panes, game HUD panels, and other constrained surfaces
- components with compact typography, badges, chips, counters, avatars, icons, legends, values, timestamps, dates, or action rows
- stacked-card junctions, card-to-card boundaries, sticky-to-content boundaries, and any place where one component's natural height could grow into a neighbour
- any region where text alignment, clipping, overflow, or exact proportional geometry is easy to miss at full-page scale
- any component that looked questionable during the full-page pass

When using Playwright or equivalent browser automation:
- Prefer element screenshots/crops for the component under review.
- Capture the component in context when its surrounding spacing matters.
- Inspect center labels, legends, chip rows, button text, icon alignment, row heights, internal padding, edge clearance, and neighbouring-component separation at component scale.
- Do not rely only on full-page screenshots for small typography or chart-label judgments.
- If a component-level crop reveals an issue, fix it and re-capture that component before declaring the visual pass complete.
- If a component is dense or constrained and no crop was captured, do not claim component-level visual verification in the final report.

### Pass 5b - mobile navigation state checks
For inferred or adapted mobile navigation, capture and inspect the relevant states, not only the default page:
- closed/default mobile navigation state
- open drawer, sheet, menu, overflow, or expanded tab state when present
- one narrow mobile stress width when the nav contains labels, icons, badges, or many destinations

Check that all major destinations remain reachable, active state is clear, labels fit or truncate intentionally, touch targets are usable, the menu trigger is obvious, overlays do not obscure controls incoherently, and drawers/sheets can scroll when their content exceeds the viewport.

### Pass 6 - responsive behavior
After the reference-size version is close:
- for desktop webpages, include a preferred wide-desktop validation pass at about `1900px` viewport width unless the user explicitly asks for a different desktop target
- do not assume the reference screenshot's narrower width is the correct production desktop width; if the screenshot is a POC, translate it into a stable real-page layout at the preferred wide-desktop viewport while keeping its composition and design language
- test tablet and mobile widths
- if feasible, sanity-check at one alternate desktop condition as well, such as a slightly narrower desktop width or a browser zoomed-out view, to catch fragile layout assumptions
- if a user’s environment is known to use non-default zoom or DPI scaling, include one sanity check that approximates that condition when practical
- preserve hierarchy and balance
- avoid overflow, clipped controls, awkward wrapping, and distorted media
- do not let the responsive version drift so far that it no longer resembles the same design language
- when reporting results, distinguish environment-related rendering differences from genuine layout bugs; do not use DPI scaling or browser zoom as a blanket excuse for visible geometry mistakes

### Pass 6a - browser and scaling resilience
For any dense or constrained UI, perform a scaling-resilience pass before final:
- Test one constrained effective desktop width in addition to the reference and normal responsive breakpoints. Prefer a width 5-15% narrower than the reference, or the nearest breakpoint above tablet.
- When practical, test one larger-text or reduced-available-width condition to approximate browser zoom, minimum font-size changes, Windows/macOS display scaling, side panels, or browser-specific font metrics.
- Inspect focused crops for the most constrained components under this stress condition, especially legends, tables, cards, nav bars, toolbars, forms, badges, date/value columns, and stacked-card junctions.
- Treat text wrapping, clipping, edge-hugging, overlap, value truncation, badge crowding, and unexpected component height growth as layout failures.
- Avoid relying on fixed heights, fixed grid rows, or absolute positioning for text-heavy components unless overflow behavior and neighbouring-component separation are verified under the stress condition.
- Prefer natural document flow, `min-height`, independent stacks, container queries, intrinsic sizing, wrapping rules, and earlier breakpoints when a component may become narrow inside a desktop viewport.
- If the stress condition reveals that the reference-faithful layout is too fragile, preserve the design language while choosing the more robust layout; report this as an intentional resilience adjustment.

### Pass 7 - final completeness review
Before finishing, verify:
- every visible section exists
- every visible icon exists
- every visible text label exists
- every important visible control has appropriate basic affordance states or a clearly intentional inert state
- every supplied asset is used correctly
- every generated asset sheet has either been extracted into individual files or intentionally integrated as a sheet/sprite
- every extracted transparent asset has had alpha metadata/pixels verified when transparency is required
- every remaining missing asset has a placeholder and, if needed, an entry in the single asset-prompt code block
- table/list panels have no accidental internal scrollbars, clipped row actions, or footer CTAs outside their container
- no obvious crowding, clipping, overlap, or layout fragility remains in the verified views

Continue iterating beyond these passes if needed. Do not stop at the first working draft.

## Optional helper script

If this skill includes `scripts/compare_screenshots.py` and Python is available, use it after capturing the implementation screenshot at the reference size.

Preferred usage:
`python <path-to-codex-home>/skills/ui-from-image/scripts/compare_screenshots.py path/to/reference.png path/to/implementation.png --out-dir .codex-artifacts/ui-diff`

Notes:
- The helper script lives in the installed skill directory, not the target repo, unless you copied it into the repo yourself.
- Best practice is to compare screenshots at the same dimensions without resizing.
- Use `--fit` only as a fallback when your candidate screenshot size is slightly off and you need a quick diagnostic.
- Use the generated diff images and metrics to locate hot spots, but do not optimize only to the number; visual judgment still matters.

## Responsive requirements

- The result must work cleanly on desktop, tablet, and mobile.
- Avoid overflow, broken wrapping, clipped content, distorted media, and awkward spacing jumps.
- Preserve the desktop composition where possible, then reflow/stack cleanly on smaller screens.
- Keep interactive elements touch-friendly.
- Do not hide important content unless the reference clearly implies it.

## Inferred Mobile Adaptation

When no mobile reference is provided, do not mechanically stack the desktop layout. Design a mobile adaptation that preserves the product hierarchy and visual language while making each component usable on a narrow touch viewport.

For inferred mobile:
- Define the mobile information order before coding.
- Convert dense tables/data grids into row cards, compact summaries, or horizontal scrollers only when that preserves the task.
- Convert persistent sidebars into a deliberate mobile navigation pattern based on the app type. Do not simply hide the sidebar or turn a long desktop nav into an overlong horizontal strip.
- Ensure charts and diagrams remain readable; simplify axes, legends, labels, or provide summary-first cards when needed.
- Avoid extremely long pages when sections can reasonably become tabs, accordions, summaries, or drill-in views without contradicting the reference.
- Verify touch targets, label wrapping, card spacing, sticky headers/nav, and all primary actions.
- Capture mobile viewport screenshots plus focused crops for dense mobile components.
- In the final report, say when mobile was inferred and list intentional structural changes from desktop.

### Mobile navigation substitution

When a desktop sidebar, rail, top nav, inspector nav, or command menu cannot fit on mobile:
- Preserve access to every important desktop destination. A mobile adaptation may prioritize a few common destinations, but the remaining destinations still need a discoverable full menu, drawer, sheet, overflow menu, or equivalent.
- Choose the pattern intentionally: bottom nav for 3-5 primary app areas, top tab/segmented nav for sibling views, drawer or sheet for many destinations, and compact horizontal nav only when all items remain discoverable and usable.
- If using priority shortcuts plus a full menu, keep shortcut count small and make the menu trigger visually obvious.
- If using a drawer/sheet, include a clear title or context, close affordance, scrim or outside-close behavior where appropriate, keyboard close when practical, and scrollability for long lists.
- Verify active states, icon/text alignment, label fit, touch target size, and menu trigger placement in both closed and open states.
- Treat hidden destinations, clipped labels, unreachable drawer items, focusable off-canvas links while closed, and ambiguous menu triggers as mobile navigation failures.

## Behaviour

- Add JS only for visible behaviour implied by the reference.
- If no JS is needed, still create `script.js` with a short comment.
- Do not add unrelated features, animations, or libraries.

## Implied interaction and affordance fidelity

Implement basic interaction states for visible controls when the reference or product context implies they are interactive. Keep behavior local and credible; do not invent unsupported workflows, backend logic, or product capabilities.

For web and app UIs:
- Links should have appropriate hover, focus, visited, or active styling when those states are relevant to the surface.
- Buttons should have hover, active, focus-visible, selected, loading, and disabled states where the reference or control role implies them.
- Dropdowns, selects, segmented controls, tabs, toggles, checkboxes, radio buttons, icon buttons, row menus, command bars, table rows, and list items should have basic local interaction behavior when visibly present or clearly implied.
- Search and filter controls may perform lightweight client-side filtering when visible local data exists.
- Tabs or segmented controls may switch local visible states if the reference implies multiple modes and the content can be represented without inventing product data.
- Menus, popovers, drawers, accordions, and tooltips may open and close when their trigger is present, using plausible visible options only when supported by the screenshot or surrounding product context.
- Do not fake destructive actions, payment flows, authentication, persistence, network calls, notifications, file system access, or complex product workflows unless explicitly requested.

For desktop-style UIs:
- Use native-feeling hover, focus, pressed, selected, disabled, and resize affordances for toolbar buttons, tree rows, menu items, tabs, grid rows, splitters, panes, scroll areas, and form controls.
- Preserve platform conventions for keyboard focus, context menus, dense data grids, disabled controls, window chrome, and status bars.
- Do not make a desktop tool feel like a marketing webpage unless the reference itself is a marketing-style surface.

For game UIs and interactive 3D surfaces:
- Implement menu selection, hover/focus/pressed states, controller/keyboard-friendly navigation cues, basic panel transitions, HUD feedback, and pause/settings navigation when implied.
- Do not invent gameplay systems, inventory effects, combat rules, physics, progression, save/load behavior, or online features unless requested.
- Prioritize readability, selected state, input feedback, stable HUD layout, and non-overlapping overlays.

For any UI surface:
- Every visibly clickable element should either have real local behavior or a clearly correct inert state.
- Cursor, hover, pressed, selected, disabled, focus-visible, drag, resize, and touch states should match the platform and visual style.
- Icon-only buttons need accessible labels or equivalent semantics in code.
- Local state changes must not damage visual fidelity, cause layout jumps, hide required content, or create states that contradict the reference.
- Verify at least one hover, focus, selected, or open state for important controls when automation or UI tooling makes that practical.

## Final report

At the end, briefly report:
1. what was implemented
2. what was reused/adapted vs newly created
3. which supplied assets were used
4. which assets were generated and integrated, including whether they came from individual generations or extracted asset sheets
5. which placeholders remain
6. if any assets are still missing, include exactly one fenced `text` code block containing all remaining asset-generation prompts
7. which visual comparison passes were completed
8. any remaining uncertainties or tiny mismatches
9. if any temporary stand-ins or synthetic replacements were used for missing assets, state that explicitly and list them alongside the missing-assets reporting
10. for extracted transparent assets, whether alpha verification was completed
11. when mobile navigation was inferred, which mobile nav pattern was chosen and which open/closed/narrow-state screenshots were inspected

### Single asset-prompt block rules

- Use exactly one fenced `text` code block for all still-missing asset prompts.
- Omit the block entirely if no asset-generation prompts are needed.
- Do not spread asset prompts across multiple code blocks or normal prose.
- Do not substitute freeform prose prompts, bullet lists, or paraphrased prompt suggestions when this block is required.
- When missing assets remain, copy this structure exactly rather than improvising a different format.
- Inside the block, keep each asset prompt standalone and clearly separated with `---`.
- Start the block with:

Generate each asset below as a separate image file. Do not combine multiple assets into one image.

- Then use this structure for each asset:

---
asset_name: ...
suggested_filename: ...
purpose_in_ui: ...
target_dimensions_or_aspect_ratio: ...
background_requirements: ...
prompt: ...
avoid: ...
---

Before sending the final answer, quickly self-check:
- if any asset is still missing, is there exactly one fenced `text` block
- does every missing asset have its own `asset_name`, `suggested_filename`, `purpose_in_ui`, `target_dimensions_or_aspect_ratio`, `background_requirements`, `prompt`, and `avoid`
- did you avoid adding any extra asset prompts outside that single block

## Definition of done

The task is done only when all of the following are true:

- The rendered page is a close visual match to the reference image(s).
- The primary reference-size screenshot has been matched first before responsive adaptation.
- Desktop/tablet/mobile layouts are coherent and stable.
- At least one additional sanity-check view beyond the primary desktop screenshot has been checked when tooling makes that practical.
- Dense or constrained components have focused screenshots/crops captured and inspected, including neighbouring-component junctions where content growth could cause overlap.
- A scaling/browser-resilience pass has been completed for dense or constrained UI when tooling makes it practical, using a narrower effective width, larger-text approximation, or known user environment condition.
- Persistent navigation, sidebars, rails, inspectors, and tool panels have been checked for internal horizontal overflow, label fit, independent scrolling, and correct expanded/collapsed behaviour when present.
- Mobile navigation substitutions preserve access to all important destinations and have verified closed/open/narrow states when the desktop navigation changes form.
- Data tables, grids, and list panels have been checked for accidental internal scrollbars, clipped row actions, and footer links/CTAs escaping their card boundaries.
- Existing project patterns are reused where appropriate.
- Typography has been explicitly audited for family, rendered fallback, size, weight, line height, letter spacing, and apparent glyph width; it does not merely rely on framework defaults.
- Text is correct and does not appear clipped, truncated, squashed, edge-hugging, overlapping, or incorrectly wrapped in the verified views.
- Card and panel heights, including intentional unequal peer-card heights, have been checked against the reference rather than normalized automatically.
- Iconography and micro-details have been explicitly audited and no obvious small UI elements are missing.
- Data visualizations and proportional diagrams have been explicitly audited for card bounds, internal geometry, labels, controls, and surrounding whitespace.
- Focused component screenshots/crops have been captured and inspected for dense, high-value, or fragile regions when tooling makes that practical.
- Visible interactive controls have appropriate platform-specific affordance states and basic local behavior where the reference or product context implies it, without inventing unsupported workflows.
- Supplied assets are used appropriately.
- Missing raster assets that should be generated have been generated when possible, preferably via asset sheets for compatible groups, extracted into individual files, and integrated.
- Generated/extracted transparent assets have verified real alpha channels when transparency is required.
- Remaining missing assets are represented by accurate placeholders plus standalone generation prompts grouped into one single fenced `text` code block.
- No obvious horizontal overflow, overlapping elements, or crowding-related regressions remain in the verified views.
- Separate HTML/CSS/JS files are used for standalone work, or the implementation is cleanly integrated into the repo's existing structure for framework-based projects.
- If browser tooling was available, the final response accurately states which screenshots were captured and inspected; you must not omit this pass or describe non-visual checks as equivalent.
- If component crops or scaling checks were required, the final response accurately states which ones were captured and inspected; do not imply they were completed from full-page screenshots alone.
- If missing assets remain, the final response uses the exact single-block asset prompt format from this skill rather than an ad hoc alternative.

