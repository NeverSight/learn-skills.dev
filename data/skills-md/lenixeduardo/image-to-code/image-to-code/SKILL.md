---
name: image-to-code
description: Reconstruct a responsive webpage or UI from a supplied screenshot, mockup, or image. Use for image-to-code, screenshot-to-React, pixel-perfect implementation, asset extraction, layer decomposition, design-token and typography inspection, icon recovery, and visual QA across mobile, tablet, and desktop. Do not use for a textual feature request without a visual reference.
license: MIT
compatibility: Requires image-capable reasoning and access to a project workspace. Python 3.10+ and Pillow are optional for deterministic cropping/comparison; Playwright is optional for screenshot capture. Image generation, OCR, vector tracing, and font lookup require separate capabilities when needed.
---

# Image to Code — Layer-first Reconstruction

**Author and project creator:** Lenix Eduardo Rotundo de Camargo (GitHub: [@lenixeduardo](https://github.com/lenixeduardo)).

The project attribution above identifies the skill's creator. It does not transfer rights to third-party screenshots, logos, typefaces, or artwork reconstructed using this skill.

Convert a visual reference into working, accessible, responsive UI **without redesigning the source**. Work from large layers to small details. Preserve existing project conventions and user-provided assets. Never report inferred properties as measured facts.

## Portable agent support (v1.5.0)

This is **one Agent Skills bundle** usable by Claude Code, OpenCode, Freebuff/Codebuff, Hermes, Codex, Cursor, Gemini CLI and other agents implementing the standard. Do not fork or simplify the workflow per vendor. See `references/agent-compatibility.md` for verified paths, activation behavior and limitations.

Install into the chosen agent's skills directory with `python scripts/install.py --agent <name> --scope project --project /path/to/app` or `--scope global`. Multiple agents can be installed together with `--agent all`; the installer detects shared `.agents/skills/` targets, doesn't overwrite existing installations without `--force`, preserves backups, and supports `--dry-run` and `--verify`.

Agents must load the **entire installed folder** (not only `SKILL.md`) so relative `references/` and `scripts/` work. Only claim a platform was actually executed end-to-end if its CLI was tested. Installation tests validate the filesystem contract, not model understanding, code quality, or screenshot fidelity.

## Inputs and precedence

1. Locate the reference image(s) and identify the target repository, framework, page route, and existing design system. Inspect the existing project before choosing new dependencies. Default to its current stack; use React/Next.js + TypeScript + CSS/Tailwind only if appropriate and not contradicted by the project.
2. Prioritize user-approved images/assets and explicitly provided instructions over screenshot approximation, then reliable image evidence, then documented responsive inference.
3. If only one viewport is provided, treat its geometry as **observed** only for that viewport. Infer other breakpoints and label them **inferred**; don't claim pixel-perfect fidelity on unseen screens.
4. Never silently replace original branding or subject artwork. If the user explicitly requests recreation, use the two-pass image-to-prompt workflow in `references/reference-guided-regeneration.md`: the screenshot crop is a **visual generation reference only**, not the output. Treat reconstructed detail as generated rather than recovered original pixels.

## Mandatory pipeline (in this order)

### 1. Inventory and normalize

- Record image filename, actual pixel dimensions, device pixel ratio if known, crop status, source viewport if known, and whether the image is a full-page or viewport screenshot.
- If tools are available, run `python scripts/image_inventory.py path/to/reference.png --out artifacts/inventory.json`. Its color samples are candidate values, **not** automatically the intended brand palette.
- Inspect visual references directly; never rely on OCR alone to recover text, fonts, or UI meaning. Document ambiguous details explicitly.

### 2. Decompose layers — back to front

Identify and inventory each meaningful region by bounding box, stacking order, repeat behavior, occlusion, and ownership. Use `references/layer-analysis.md`.

Process strictly:

1. **Background** — solid colors, gradients, texture, noise, overlays, backgrounds by section, fixed/scroll/parallax behavior. Rebuild via CSS where possible; export only genuine isolated raster artwork. Do not treat the complete screenshot as a usable clean background.
2. **Section layout and containers** — page frame, grid/flex, columns, gutters, max-width, alignment, padding, section height, breakpoints and stacking context.
3. **Components** — header/nav, hero, CTA, cards, buttons, fields, galleries, footer; identify states, constraints, focus/hover/tap behavior, ordering, semantics.
4. **Typography** — text hierarchy, candidate font families, weights, sizes, line heights, letter spacing, transformations, wrapping and exact copy. An image alone usually cannot prove the original font family; label confidence and use only legally accessible fonts.
5. **Icons and graphical assets** — preserve original icons or extract them with transparency if truly separable; if recreation is required use coherent SVG geometry and stroke. Don't silently substitute unrelated icons.
6. **Images and illustrations** — identify originals. For explicitly requested regeneration, condition the image generator on **full screenshot + component reference crop + forensic scene prompt** to make a complete text-free scene, then restore exact typography as a second pass. Otherwise extract unobscured pixels. Record crop/focal point/object-fit/art direction.
7. **Foreground microdetails** — separators, borders, shadows, blur, glow, decorative marks, overlays and motion.

Track a layer manifest with observed/inferred/unknown evidence. `scripts/export_layers.py` produces screenshot fragments, never recovered hidden source. In explicit regeneration mode use `scripts/prepare_generation_reference.py` to create a reference crop for the generator; require **both images + detailed scene prompt**. If no image generator exists, report a blocker rather than silently substituting a crop.

### 2.5. Reference-guided TWO-PASS regeneration (mandatory when new image generation is requested)

Follow the complete [reference-guided regeneration protocol](references/reference-guided-regeneration.md). **This is the exact video-demonstrated order:**

1. Analyze the full reference and crop the relevant component **as a generation reference only**. Use `python scripts/prepare_generation_reference.py input.png --box X Y W H --out artifacts/reference/component.png --manifest artifacts/reference/crop.json`.
2. Convert the image to a **forensic prompt grounded in both visual references**: same character/face/eyes/anatomy/paws/pose, coherent environment, built-in glow, precise framing, negative constraints and text-safe region. Do not guess invisible details as if seen. See `examples/catty-hero-scene-prompt.md`.
3. Generate a **clean, complete SCENE first, WITHOUT text, UI, logo, phone, button or status indicators**. Use the full screenshot **and component crop** as reference images attached to the generation call. Do not crop the original pixels as the final scene. Rejected generations are not silently reused.
4. Review the generated scene for subject identity, paws/limbs, lighting integrated in the rendered artwork, no cut seams, no new accessories and no ghost text. Iterate by targeted correction prompts until all gates pass or honestly report the limit. Never claim 100% exact identity just because a prompt is detailed.
5. **SECOND PASS:** restore exact wording, font metrics, sizes and positions from the screenshot. Use accessible **HTML/CSS** for a functional webpage; for a separately requested static poster use a second image-editing pass, preserving the first-stage scene. Do not let typography generation regenerate or change the character.
6. Write `artifacts/regeneration/contract.json` and run `python scripts/validate_generation_cycle.py --file artifacts/regeneration/contract.json --root .`. All six visual checks and final typography positioning must have grounded evidence. The validator checks the contract, not visual correctness itself.

The crop is **never the final asset**, and native luminous ribbons/bloom must **not be duplicated with CSS haze or blurred clones**. Keep the original scene-only render and screenshot references for comparison. This branch of the workflow supersedes crop-only instructions when the user explicitly requests regeneration.

### 3. Produce a reproducible design specification

Before code, write `artifacts/design-spec.json` (see `references/design-spec.schema.json` and `references/spec-guide.md`), plus `artifacts/asset-manifest.json` and `artifacts/assumptions.md`.

Include:

- palette in HEX/RGBA, gradients/stops, opacity, shadows, borders, radii, spacing scale, grid/container widths, z-index;
- each font candidate, fallback, source/license, weights, font size, line height, letter spacing, and text treatment for desktop/tablet/mobile;
- every component's reference bounds, CSS role, states, min/max size, padding, alignment, stacking and behavior;
- every icon/image asset's location or generation requirement, license, transparency, crop and dimensions;
- named breakpoints and behavior rules **for mobile, tablet, desktop**;
- evidence classification (`observed`, `inferred`, `unknown`) and confidence (`high`, `medium`, `low`) for material decisions.

Use fluid CSS (`clamp`, `%`, `minmax`, `aspect-ratio`, `object-fit`) where it matches source evidence. Avoid arbitrary fixed heights and absolute positioning for primary layout; use absolute positioning only for genuinely overlaid elements. Validate spec with `python scripts/validate_spec.py artifacts/design-spec.json`.

### 3.5. Independent visual risk reviews (mandatory for fidelity claims)

Use four dedicated reviewer roles described in `references/visual-review-agents.md`: **icons**, **typography and controls**, **subject integrity**, and **lighting/composition**. Agents with subagent support may run them independently; without that capability, execute them sequentially and do not claim multiple AI agents executed. Use the same viewport and keep evidence files. Detect blurry duplicate glows from image artwork with baked-in highlights and any cropped paw/ear/anatomy. Do not approve an approximate icon, unspecified font, or asset with ghost text.

Before claiming acceptance, write `artifacts/visual-review.json` with these four review entries and run `python scripts/validate_visual_review.py --file artifacts/visual-review.json --root /path/to/project`. Non-pass/unknown status means **not approved** regardless of passing Playwright tests. This gate checks review records, not human judgment quality.

### 4. Export and organize assets — **HARD GATE BEFORE ANY PAGE CODE**

**Order is mandatory: IMAGE → COMPLETE ASSET KIT → VERIFIED MANIFEST → COMPONENT/TYPE SPECS → IMPLEMENTATION → VISUAL QA.**

Do not write JSX, HTML, CSS, layout components, visual mockup markup, or placeholders before the asset kit is assembled and inspected. This applies to a desktop screenshot, mobile mockup, multi-panel image, and pre-existing codebases alike.

1. **First create every required source asset** in the intended layer order: (a) full section background including its genuine visible illumination and textures, (b) isolated subject/character wherever recoverable, (c) logo and wordmark, (d) every custom icon, (e) illustrations and product photographs, (f) complete phone/device mockup **including its visible internal screen UI** and, where appropriate, separately extractable screen items, (g) buttons/badges/decorative graphics only where they cannot be faithfully rendered with CSS.
2. **Audit actual provenance and occlusion.** A flattened screenshot cannot reveal the concealed paw behind a phone, clean background behind text, unseen screen content, or exact licensed font binaries. Mark such detail as unrecoverable or inferred; never assert that a reconstructed layer is the exact hidden original. Preserve approved art rather than redrawing it. A decorative phone raster is not a working phone interface: build separate interactive screen components only when required by the task.
3. **Before any frontend implementation**, publish a local transparent/neutral-background **asset-contact-sheet** showing the logo, background, subject, icons, and device/screen assets. Inspect for ghost text, hard rectangular edges, accidental blurring, clipped paws, incorrect symbols, or missing alpha channels. Correct the assets first; do not push the problem downstream into CSS.
4. Write `artifacts/assets-ready.json` with `stage: assets_before_code`, `required_roles`, `assets` entries `{role,path,status,sha256,provenance}`; status is `extracted`, `reused`, `reconstructed`, or `unrecoverable` (plus reason). Run `python scripts/validate_asset_gate.py --manifest artifacts/assets-ready.json --root /path/to/project` and **do not enter step 5 unless it passes**. If missing assets cannot be recovered, disclose the blocker and obtain a deliberate fallback choice rather than claiming pixel-perfect completion.
5. Record font family candidates, weights, letter spacing and breakpoint geometry as independent specifications **before** implementing typography. A rasterized label embedded in a screenshot is not a legally distributable font or selectable text.

**Mandatory source-asset audit for an existing project:** run `python scripts/audit_project_assets.py --project /path/to/project --out artifacts/project-assets.json` before implementation, and repeat it before acceptance. This catches static references to missing images even if an `onError` fallback makes the page appear visually intact. Missing approved source assets are blockers; do not silently fabricate, replace, or mark the output pixel-perfect.

- Store generated or extracted page assets under the project's preferred static directory (e.g., `public/assets/image-to-code/`), named by function: `hero-background.webp`, `hero-subject.png`, `logo.svg`, `icon-menu.svg`, etc.
- Export raster sources at original fidelity. Don't upscale and claim added detail. Use vector only when the shape is legitimately recoverable. Maintain transparent backgrounds for isolated foreground assets.
- Avoid cropping text into bitmap assets if it should be selectable/accessibly rendered as HTML.
- Use local provided assets first. Respect copyright/license for external fonts/photos/icons, and record asset provenance.
- Where occluded content is impossible to recover, list a missing asset and **do not silently synthesize**.

### 5. Implement with responsive components

- Build semantic, reusable component tree; define theme tokens and typography first, then background, layout, components, icons/images, and microdetails in that order.
- Keep desktop/tablet/mobile behavior explicit in the spec: navigation collapse, card columns, reflow/reorder, image crop, text scaling, touch interaction, modal behavior, overflow, spacing, hidden/visible elements.
- Use breakpoints based on observed design shifts rather than a dogmatic device-size assumption. Default inspection sizes: **390×844**, **820×1180**, **1440×900**; also smoke-test **360, 430, 768, 1024, 1280, 1920px** widths.
- Include keyboard navigation, focus-visible, accessible names, reduced motion, image alt text, layout stability, touch targets and avoidance of horizontal overflow.
- Avoid replacing existing source assets or unrelated project files; scoped edits only. Avoid adding unnecessary frameworks, fonts and icon libraries.

Read `references/responsive-rules.md` and `references/implementation-guide.md` during this step.

### 6. Validate visually; iterate

1. Run project lint/build/tests where available; inspect console and runtime errors. Also run `python -m unittest discover -s tests -v` and `node --test tests/test_capture.mjs` for changes to this skill; these checks verify the tooling, not UI fidelity.
2. Render **desktop, tablet, and mobile screenshots**, plus matching original viewport and intermediate widths, using browser automation, e.g. `node scripts/capture.mjs --url http://localhost:3000 --out artifacts/screenshots --reference-viewport 1179x616 --smoke-widths 360,430,768,1024,1280,1920` after installing Playwright. Record screenshots and `capture-report.json` in the final deliverables; fail quality gates on broken images, JavaScript errors, unlabeled interactive controls, horizontal overflow or missing main landmark. Do not pass `--allow-warnings` for approval. **Embed the required side-by-side boards visibly in the chat** when the interface supports it; never substitute download links for in-chat evidence.
3. For each supplied reference and matching viewport: run `python scripts/audit_visual.py --reference input.png --render artifacts/screenshots/desktop.png --out artifacts/audit/desktop`. Sizes must match; if they do not, correct the viewport rather than silently resize.
4. Review geometry, font rendering, assets, colors, spacing, responsive behavior and interactions manually. Fix the largest divergences, re-capture, and compare again. Treat automated pixel error as a **diagnostic**, not an authoritative visual quality score. See `references/visual-qa.md`.
5. Produce the **mandatory presentation boards** via `scripts/present_results.py`, and show both **directly inside the chat**, not just as downloadable links: mobile + tablet side-by-side; if the source reference is a desktop UI screenshot, original desktop + rebuilt desktop side-by-side. Never use a single giant multi-device collage. If source and render are not the same viewport, disclose the mismatch and recapture before a fidelity claim. Consult `references/presentation-standard.md`.
6. Target **≥9.5/10 on every viewport that has a reference**, with screenshot evidence and the weighted rubric. For inferred breakpoints, report responsive quality separately, not pixel fidelity. If target cannot be reached, report exact deviations and evidence instead of claiming success.

## Mandatory fidelity contract and multi-agent rejection gates (v1.4.0)

**Read [fidelity-gates.md](references/fidelity-gates.md) and run its two specialist reviews plus an independent acceptance review before reporting success.** Use distinct agents when the runtime supports them; otherwise perform three clearly documented separate review passes. Never represent a role-based manual pass as an actually spawned agent.

- **Agent A, UI fidelity:** inspect original icons rather than swapping icon libraries; verify the actual loaded font, computed CSS and glyphs; compare button size/position/padding with independently measured reference XYWH. A larger CTA is a failed gate even if the global screenshot diff is low.
- **Agent B, asset integrity:** preserve the approved original subject and embedded glow as one composite when baked together. Forbid regenerating it, artificial upper/lower blur, extra CSS halos and clipped subject details. Verify extremities (including a cat's paw) as dedicated regions. A cropped screenshot derivative does not count as the lost original.
- **Agent C, acceptance:** review A and B evidence, run browser interactions, independently compare each critical region and check protected asset hashes. Reject altered icons, font fallback, CTA-size deviations, missing details and unverified visual claims.
- **Run the strict contract gate:** `python scripts/audit_fidelity_contract.py --contract artifacts/visual-fidelity.contract.json --project . --out artifacts/audit/fidelity-contract-report.json`. Start from the example JSON and **replace all sample coordinates** with actual measured screenshot regions, add immutable original asset hashes, and enable `require_protected_assets` for pages with approved source art. Do not change thresholds after seeing failures to force acceptance.
- Treat user-reported visual defects as **separate, blocking regression cases**: icon shape, typography, CTA geometry, upper/lower glow boundaries and all visible subject details. Never average a critical failure away in the total score. Do not claim ≥9.5 while any unresolved blocking regression remains.
- Reference and render must be captured at matching viewport/DPR, with fonts/images loaded and relevant states matched. This gate does not substitute for a real browser, human visual review or in-chat evidence boards.

## Required output contract

Return a project-ready implementation, **not just a text prompt**:

- Actual source-code changes and any required extracted assets, or an explicit blocker where tool support is absent.
- `artifacts/design-spec.json`, `artifacts/asset-manifest.json`, **`artifacts/assets-ready.json` (asset-first gate)**, `artifacts/assumptions.md`, and an audit report.
- A concise component tree, font scale in px/rem, design tokens, image/icon manifest, and breakpoint table.
- **Mandatory chat-visible images:** one mobile + tablet side-by-side board; one desktop original + reconstruction side-by-side board when the user supplied a desktop-interface screenshot. For a non-desktop reference, show the desktop preview separately. These must render directly in the conversation, with links only as secondary downloads. Keep both panels readable, labeled, entirely visible and undistorted. Record reference cropping/viewport differences; do not present inferred layouts as faithfully matched.
- Screenshot evidence for mobile/tablet/desktop, test/build outcomes, and a separate score per reference viewport.
- A clear distinction between **confirmed from image**, **inferred for responsiveness**, and **not recoverable**.

Never claim assets were created, screenshots captured, tests passed or a page was deployed unless those outputs actually exist. Do not treat analysis-only completion as completed image-to-code implementation.

## Supporting files

- [Multi-agent installation and compatibility](references/agent-compatibility.md)

- [Layer decomposition and extraction](references/layer-analysis.md)
- [Design spec JSON schema](references/design-spec.schema.json)
- [Spec examples and evidence rules](references/spec-guide.md)
- [Responsive behaviors](references/responsive-rules.md)
- [Implementation rules](references/implementation-guide.md)
- [Visual QA and acceptance](references/visual-qa.md)
- [Mandatory demonstration format](references/presentation-standard.md)

## Acceptance integrity (v1.1.0)

- A tool test passing is not proof of a faithful reconstructed website. A full QA report needs an actual browser render, comparison at matching viewport/DPR and user-visible evidence boards.
- Browser runtime checks include failed/broken images, interactive controls without accessible names, JavaScript console errors, missing `main`, horizontal overflow and failed requests. Investigate rather than blanket ignoring failures.
- In screenshot audits, any excluded dynamic regions must be explicit, limited in scope and **visible as neutral masks** in diagnostics. Never use large masks to hide defective artwork.
- Never assign a perfect 10/10 to the skill or a reconstructed page when end-to-end browser execution is blocked or when referenced viewports and fonts cannot be validated. Document unresolved gaps by severity.

- For desktop screenshot QA, invoke `scripts/present_results.py` with `--require-matching-desktop` to make mismatched dimensions a failed acceptance gate, not just a warning.


## Multi-state pixel-perfect acceptance (v1.6.0 — REQUIRED)

**Do not approve image-to-code merely because expected text exists or the modal opens.** The Catty validation previously passed text/navigation tests while a device frame, character and bottom controls were clipped.

1. Inventory every approved screenshot state (including character expressions, chat steps, bottom navigation, sound controls and original copy). Reproduce **each state** as accessible UI and capture it in a real browser.
2. Compare reference and actual render with `scripts/calibrate_pixel_perfect.py`. Use equally sized images by default. For a multi-screen composite, use `--columns N --normalize-reference` only after explicitly recording the derived dimensions, and never silently resize. Inspect per-state paired PNGs and heatmaps, optional SSIM, RGB MAE and baseline deltas. No diagnostic pixel metric is a 0–10 rating.
3. Configure `scripts/validate_visual_states.mjs` with real viewports, state click sequences, and `mustFit` selectors for the entire phone frame, character/paws, main CTA, bottom controls and other visible critical nodes. An off-screen or clipped element **fails** even if its text is present and all other tests pass.
4. Preserve authentic subject anatomy, full original art lighting and icon styles; match typographic wrap and exact text. Do not replace lost paws with blur/gradients or claim pixels hidden behind text can be recovered without source artwork.
5. Require per-state comparisons alongside the mobile+tablet presentation board. Inspect font/icons, image provenance and viewport inference. If any P0 errors remain, report them and do not claim ≥9.5/10.

See [pixel-perfect QA methodology](references/pixel-perfect-qa.md), [state configuration](examples/visual-states.example.json) and [prioritized TODOs](TODO.md). This is a reproducible code-and-browser validation loop, **not** training of the agent model's weights.


## Advanced project-wide quality gates (v1.7.0)

Before claiming high fidelity, run **independent** checks for masked regional similarity, component layout, font and icon provenance, touch/focus and agent runtime availability. See [advanced QA reference](references/advanced-visual-qa.md) and [remaining TODOs](TODO.md).

- `scripts/advanced_visual_qa.py`: mask-aware SSIM, guarded regions, untouched-reference split-overlay, advisory edge alignment, and reviewer-only CSS suggestions. The global mask maximum is 8%; critical face/CTA areas cannot be masked.
- `scripts/validate_component_geometry.py`: default semantic tolerances (critical 3px, high 5px, normal 9px, decorative 14px), with clipping an unconditional failure.
- `scripts/audit_typography_icons.py`: original licensed font metadata / icon SVG outline-filling-baseline comparison. No source file = unresolved, not magically recovered.
- `scripts/browser_font_audit.py`: effective computed font, line count, size/weight and possible fallback in Chromium; it cannot prove same-metric typeface identity.
- `scripts/browser_compat_qa.py`: actual Chromium device-emulated tap/swipe/focus, WebKit when installed; SKIPPED is never PASS.
- `scripts/probe_agents.py`: lists installed supported coding agent CLIs. Installation paths are not evidence of working agent invocation.
- `scripts/negative_controls.py` and `scripts/benchmark_evidence.py`: measured negative tests and strict 3-independent-project reference coverage gate.
- `scripts/build_state_dashboard.py`: linked local states/heatmaps/interactive overlays with no proprietary uploads.

Do not assign a completed P0 to three separate projects unless each has independently approved, non-derived mobile/tablet/desktop references and real-browser evidence. An image-capable coding agent's autonomous pipeline and original flattened Catty layers also require direct proof. Never upload proprietary screenshots or font files to a public CI artifact.


## Real coding agents, font identity, longitudinal CI (v1.8.0)

1. Prepare native agent skill layouts and isolated runtimes with `python scripts/prepare_cli_environments.py --skill-root . --out artifacts/cli-preflight --check`. Use the **manual** GitHub Actions workflow `CLI runtime environment validation` to try official npm installs on isolated Linux runners. A binary reporting `--version` is **NOT** authenticated agent invocation.
2. Before claiming an *exact* original font, use `scripts/verify_font_identity.py` with a licensed original font file or owner-confirmed SHA-256. Missing original font source MUST be `ORIGINAL_UNAVAILABLE`, regardless of CSS family/weight or visual similarity. Do not commit or distribute font binaries.
3. `scripts/ci_metrics.py` writes sanitized per-job QA counts. `Aggregate Image to Code QA history` downloads only `qa-metrics-*.json` artifacts into local JSON/CSV/Markdown/HTML. Runs lacking artifacts are `N/D` rather than zero; all metrics are diagnostics, not 0–10 fidelity grades.
4. No autonomous end-to-end agent success claim unless a properly authenticated CLI independently reads a new reference, constructs assets/code, runs a browser, performs corrections and exports verified evidence.

Read [CLI/font/metrics setup](references/cli-font-metrics-setup.md), [font manifest](examples/font-source-manifest.example.json) and [remaining TODOs](TODO.md).


## Mandatory polish gates from field tests (Catty · Zouti · GoatVPN)

**Consult [the 32-item field polish register](references/field-polish-findings-2026-10-30.md) before starting and during acceptance.**

- **Recreation default: `NO_SOURCE_SCREENSHOT_CROPS`.** The reference image is analysis/conditioning/comparison material, **not** an exportable page layer. Generate the complete missing scene cleanly, then use real DOM/CSS/SVG for interface, charts and text. An independently supplied original/logo/portrait asset is different from cropping a screenshot and can be reused only when authorized. If a user chooses hybrid mode explicitly, disclose it and score code-only regions separately. A high SSIM achieved by copied screenshot panels is NOT proof of code fidelity.
- **Project/source identity:** pin active project, reference path and digest before every asset-generation or code step. Never substitute another supplied mockup or a generated concept.
- **Scene owner boundaries:** keep enormous outer typography, mesh/globe lighting and decorative waves outside the device/monitor; reconstruct the screen content inside as independent components. No screen-text residues, duplicate bloom, blur patches, or smudged segmentation around subjects.
- **Separate geometry and quality gates:** compare background (including luminance and light directions), icons/fonts/CTAs, subject anatomy, phone/device outline, globe nodes and internal UI. Apply explicit per-project anchors, semantic-region metrics, icon/font provenance and clipping/occlusion checks. Source-asset limitations must remain visible.
- **Evidence and presentation:** only real browser screenshots may be called HTML reconstruction. Original+desktop render must be one side-by-side composite PNG; mobile+tablet must be another single composite with nonoverlapping labels. Without reference mobile/tablet shots, label layouts `INFERRED`, not pixel-perfect.
- **Preview acceptance:** verify standalone HTML with local/served browser modes when supported, and provide ZIP plus a documented HTTP/HTTPS fallback when an app viewer doesn't execute HTML. Never assert that a client supports the preview without checking.
- **Acceptance semantics:** operational checks (e.g., 24/24) and SSIM are diagnostic signals, not a 9.5/10 score. A critical region with poor fidelity blocks approval even if a sourced dashboard/asset yields favorable whole-frame metrics. Record changes and compare before/after by region.

The field register is a **backlog**, not a declaration that these 32 improvements have been implemented.
