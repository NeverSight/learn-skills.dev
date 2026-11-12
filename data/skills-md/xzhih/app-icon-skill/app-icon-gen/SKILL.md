---
name: app-icon-gen
description: Use when creating, repairing, converting, packaging, or verifying app icons for any platform from briefs, references, brand marks, SVG/logo/text assets, generated concepts, or existing icons; use the optional Apple adapter when Icon Composer output is requested.
disable-model-invocation: true
---

# App Icon Gen

Create reusable cross-platform icon source assets from a JSON spec. The normal route is semantic layered authoring: a small set of meaningful SVG/base-shape layers or deliberately clean PNG fallback layers, rounded preview assets, unrounded app/source assets, and verification evidence. Apple Icon Composer packaging is an optional adapter, not the default contract.

This skill may export rendered PNGs with Icon Composer's bundled `ictool` when it is locally available on macOS. It does not prove app integration or final platform rendering beyond those exported PNG files.

## Hard Contract

For every new or repaired icon, use one generation root: the user-facing delivery directory.

- `target_platforms` is optional metadata. Accept the user's platform labels without inferring, expanding, or rejecting non-Apple platforms.
- Always deliver reusable SVG/PNG source assets first. After reviewing them, ask whether the user wants a native platform export; do not claim a native Android, Windows, Web, tvOS, or visionOS package without its dedicated adapter.
- Request Apple packaging with an Apple target (`iOS`, `iPadOS`, `macOS`, or `watchOS`) or an Apple `deliverable_type`. Only then create a `.icon` bundle and optional `apple/` renders.
- When `watchOS` is requested through the Apple adapter, review the circular crop and 1088px Default render separately.
- Write the current spec at `<delivery>/tmp/work/spec.json` before generation.
- When a user source image/vector or selected generated concept exists, keep exactly one visible source evidence file at `<delivery>/<delivery-name>.origin.png` or `<delivery>/<delivery-name>.origin.svg`; put unselected candidates under `<delivery>/tmp/work/`.
- Put every intermediate artifact under `<delivery>/tmp/work/` as it is created: masks, threshold tests, extracted foregrounds, traced candidates, comparison images, notes, and repair scratch.
- Generate with `author-icon --spec <delivery>/tmp/work/spec.json --out <delivery>`.
- Reruns may overwrite generated root files, `layers/`, `.icon/`, `apple/`, and `tmp/reports/`; they must preserve existing `tmp/work/` except for replacing `tmp/work/spec.json` with the current spec, and preserve `.origin.png`/`.origin.svg` unless the selected source changes.
- Do not generate a full package in another directory and reorganize or copy it into the delivery directory.
- Do not patch generated `layers/`, `.icon/Assets`, or `icon.json`; update the spec and regenerate.

Normal delivery layout:

```text
<delivery>/
  <delivery-name>.preview.svg
  <delivery-name>.preview.png
  <delivery-name>.svg
  <delivery-name>.png
  <delivery-name>.origin.png or <delivery-name>.origin.svg  # when source evidence exists
  <Name>.icon/                        # optional Apple adapter
  apple/                              # optional Apple renders
    iOS/{Default,Dark,TintedLight,TintedDark,ClearLight,ClearDark}.png
    macOS/{Default,Dark,TintedLight,TintedDark,ClearLight,ClearDark}.png
    watchOS/Default.png
  layers/
  tmp/
    reports/
    work/
      spec.json
```

The visible delivery root must stay limited to `.svg`, `.png`, `.preview.svg`, `.preview.png`, `.origin.png`, `.origin.svg`, `.icon`, `apple/`, `layers/`, and `tmp/`.

## Workflow

1. Inspect supplied sources before asking questions: attachments, paths, app metadata, existing assets, screenshots, SVG/logo files, `.icon` bundles, and project-local source vectors.
2. Choose one route: source conversion, generated concept, direct semantic authoring, or existing package refinement. Record target platforms only when they are known.
3. Read only the route-specific references below.
4. Write or update `<delivery>/tmp/work/spec.json`; keep layers in bottom-to-top visual order. If source evidence exists, copy the selected source or concept to `<delivery>/<delivery-name>.origin.png` or `<delivery>/<delivery-name>.origin.svg`.
5. Generate directly into the delivery directory. The generic SVG/PNG assets are always written. When the Apple adapter is requested and Icon Composer.app's `ictool` is available, it additionally writes Apple renders under `apple/`.
6. Run `verify`; add `--reference` when a reference image exists. Normalize the reference first only when its canvas/size/mask differs from the preview canvas.
7. Inspect generated preview/app assets at full size and 64px plus the applicable verification evidence. If an Apple adapter exists, also inspect `.icon/Assets`, `icon.json`, and any requested Apple renders. Record `visual-review.json` when a human decision is needed; do not treat missing optional platform exports as a generic failure.
8. If verification or inspection fails, repair the spec, regenerate, and verify again.

Run commands from the skill directory, or use an absolute `--prefix` to `scripts/`. Node package metadata lives in `scripts/package.json`; do not run `npm install` at the skill root.

```bash
npm --prefix scripts ci

delivery="/absolute/path/to/my-icon"
mkdir -p "$delivery/tmp/work"

npm --prefix scripts run author-icon -- \
  --spec "$delivery/tmp/work/spec.json" \
  --out "$delivery"

npm --prefix scripts run verify -- --out "$delivery"
```

With a reference:

```bash
npm --prefix scripts run verify -- \
  --out "$delivery" \
  --reference "/absolute/path/to/reference.png"
```

Use absolute paths for script inputs and outputs.

`author-icon` refuses to replace a non-empty directory it does not own. It refreshes only leaf files in the previous style report's validated `generated_files` ownership manifest, fails closed when that manifest disagrees with the safe report-derived file set, removes generated directories only after they become empty, and preserves other files even when they sit inside `layers/`, `.icon/`, or `apple/`. Clean an unowned directory outside this workflow only after inspecting it yourself.

## Verification Evidence Ladder

Do not repair or switch routes from side-by-side and mean delta alone. Choose evidence by failure type and use it before changing the spec:

- Whole-icon likeness: inspect `reference-side-by-side.png` first for overall style, scale, mass, and obvious drift.
- Geometry, placement, proportion, and layer alignment: inspect `reference-overlay.png` before deciding a foreground is shifted, too small/large, or the wrong shape.
- Color, background, glow, shadow, antialiasing, and material drift: inspect `reference-diff.png` and the verifier diagnostics before changing fills or adding/removing material.
- Rounded app-mask/frame drift: treat `frame_or_rounded_mask_residual_dominated` as frame normalization evidence rather than foreground shape failure; inspect the interior diff before repairing the mark.
- Severe local mismatch: read `local_sample_gate`, `local_samples`, and `tile_heatmap`; translate hotspots into a concrete repair hypothesis instead of treating them as another score.
- Smooth symbolic marks, mascots, loops, ribbons, and brand-like contours: use overlay/diff plus bbox/centroid or `shape-facts` when the visual error is ambiguous.
- Simple SVG primitives: run `geometry-audit` on the affected layer after repair; a numeric pass does not excuse wobbly curves, bad tangents, or path noise.
- PNG fallback: inspect the isolated PNG asset and `png_layer_hygiene`; reference mean success is not enough.

Repair order for reference-driven work: geometry/placement first, then scale/proportion, then color/background, then renderer/material differences. Only choose PNG fallback after the relevant SVG route has failed with evidence from overlay/diff/local diagnostics or isolated asset inspection; for clean separable silhouettes, the relevant SVG route includes component-level traced SVG before PNG fallback.

## Reference Routing

- `references/source-requirements.md`: provenance, identity risk, source classification, background route, and PNG fallback risk.
- `references/concept-prompts.md`: no source artwork exists and image generation or direct concept authoring is needed.
- `references/semantic-icon-design.md`: JSON design contract shared by no-reference image generation and direct semantic authoring.
- `references/style-directions.md`: SVG-convertible style directions for `semantic_icon_design`.
- `references/semantic-authoring.md`: JSON spec structure, `semantic_review`, `source_analysis`, layer order, text, and PNG fallback decisions.
- `references/cookbook.md`: route is ambiguous or the icon matches a known family such as geometric marks, letterforms, text, material references, or overlapping plates.
- `references/icon-composer.md`: `.icon` structure, fill formats, Icon Composer material boundaries, asset formats, and `icon.json`.
- `references/verification.md`: verifier behavior, reference comparison, visual-review sidecars, batch summaries, and review gates.
- `references/optimization-methods.md`: geometry polish, bitmap extraction, shape diagnostics, localized repair, or foreground cleanup.
- `references/failure-modes.md`: dirty PNGs, wrong semantics, preview/fill drift, source-vector needs, path repair, or misleading numeric passes.
- `references/golden-examples.md`: small known-good specs and anti-patterns.
- `examples/semantic-image-prompts/README.md`: index of no-reference image prompt examples; read only the matching example file after choosing a style direction.

## Completion Gate

Complete only when all applicable checks are true:

- Required root assets, `layers/`, `tmp/reports/style-report.json`, and `tmp/work/spec.json` exist. `.icon/` and `apple/` exist only when the Apple adapter was requested.
- When a source/reference/generated concept drove the package, `<delivery-name>.origin.png` or `<delivery-name>.origin.svg` exists at the delivery root and is not imported into `.icon/Assets`.
- Preview SVG/PNG are the rounded local visual contract; root SVG/PNG are the unrounded app/source canvas.
- An Apple adapter, when requested, contains clean `.icon/Assets` rather than a single flattened app icon unless the accepted route is a documented PNG fallback.
- `svg_material_warnings` and package `warnings` are empty. Every `png_layer_hygiene` entry passes the edge/residue checks; the array may be non-empty for legitimate clean PNG assets.
- For reference matching, side-by-side, overlay, and diff were generated and inspected; overlay/diff/local diagnostics were used to justify any repair or route change; mean delta, `visual_delta_gate`, and `local_sample_gate` either pass the route target or the accepted semantic tradeoff is recorded.
- No simple background is duplicated into `.icon/Assets`; no preview-only rim, glow, bevel, shadow, highlight, border, or mask artifact is imported as source material.

Do not widen completion into Icon Composer import, app integration, publication, or platform-specific final rendering unless the user explicitly asks for that.

Final response must include the delivery path, generic source assets, target-platform metadata when supplied, optional adapter outputs, source evidence when applicable, and the preview/assets actually inspected. Ask before claiming or attempting a native export not supported by an installed adapter.
