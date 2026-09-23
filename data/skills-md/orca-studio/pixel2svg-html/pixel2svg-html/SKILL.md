---
name: pixel2svg-html
description: "Convert raster logos (PNG/JPG/WebP/screenshots) into clean, smooth, minimal-complexity SVG plus standalone JS-rendered HTML, using a lowest-complexity-first fitting workflow with overlay QA, edge smoothness as the primary hard gate, IoU optimized as high as reasonably possible without a fixed global threshold, Bezier audits, and a default 10-iteration budget. Use when asked to vectorize, trace, recreate, fit, or convert a logo image into SVG/HTML and no animation is requested. If the user asks for atomic motions, tuners/controllers, a main animation, or a logo animation showcase HTML, use pixel2motion instead. v2: also covers closed/self-intersecting variable-width ribbon fitting (centerline scaffold + edge snap) and a wordmark font-matching protocol (ink-weight ratio)."
---

# Pixel2SVG-HTML (v2)

Turn a raster logo into:

- `logo.svg` — minimal, smooth, editable vector
- `logo.html` — standalone HTML that recreates the SVG via JavaScript DOM calls
- `final_render.png`, `html_render.png`, overlay iterations + `overlay_progress_strip.png`
- path-audit artifacts when smoothness was a concern; resumable fit state in `outputs/fit_work/`

This skill is static/vector-first. If the requested HTML needs atomic motions, playback tuners/controllers, or a main logo animation, switch to `pixel2motion`; do not force animation delivery through this static skill.

The governing rule is **lowest smooth complexity that passes visual QA**. Do not maximize pixel-fit by default: start with the simplest editable geometry that can explain the mark, escalate only when an overlay shows a structural mismatch. Edge smoothness is the primary hard gate for ordinary logos. IoU is a required diagnostic and should be pushed as high as practical, but there is no fixed global IoU threshold; a slightly lower IoU can pass when the residuals are visually minor and explained.

## Complexity Ladder

Use the first level that matches the source well enough:

1. **Primitives**: circles, ellipses, rects, lines, simple arcs, transforms.
2. **Primitive composites**: boolean-like combinations of a few primitives or masks.
3. **Few-curve analytic paths**: a small number of cubic segments for smooth ribbons, swooshes, C-marks, leaves, waves, shields. For closed and/or self-intersecting variable-width ribbons (∞ marks, scripts) — where two open boundaries don't exist — use the centerline-scaffold recipe: `references/ribbon-fitting.md` + `scripts/fit_ribbon_centerline.py` (playbook §8; the source-pixel edge snap is what reconciles it with playbook §3).
4. **Smoothed outline paths**: more knots only where the source has real shape changes; preserve G1 tangent continuity, no noisy handle flips.
5. **Trace-derived paths**: only for irregular silhouettes where simpler geometry fails (`scripts/raster_logo_trace.py` as measurement/starter). Trace output is a measurement aid, never automatically final art. Smooth or refit before delivery.

If a higher-complexity version improves only antialiasing or minor pixel coverage, keep the lower one. If a lower-complexity version has wrong endpoints, width profile, center, silhouette, negative space, or visibly stair-stepped edges, move up one level or refit with smooth curves. Prefer live SVG `<text>` for wordmarks unless exact letterforms are required. Decide the provisional complexity from the source itself and record the reason.

## Smoothness And Fit Gate

IoU must not hide bad vector craft. A smooth logo source must ship as smooth vector geometry; the final SVG fails if intended smooth edges visibly stair-step, chatter, use pixel-grid orthogonal runs, contain noisy trace knots, or look like a bitmap mask at 200-400% zoom, even when IoU is numerically high.

- Pixel-grid contours from threshold masks are acceptable only as starter measurements or for genuinely pixel-art logos.
- Smooth parts should use primitives, arcs, ellipses, or cubic paths with the lowest complexity that preserves silhouette, width profile, extrema, and negative space.
- Compute and record IoU every iteration, but do not use a fixed global pass/fail value. Optimize IoU upward after smoothness and structural correctness are protected.
- A slightly lower-IoU result may pass when the overlay is visually faithful and residuals are explainable as deliberate smoothing, antialiasing, font substitution, or raster-source artifacts.
- If a lower-IoU smooth candidate ships over a higher-IoU jagged candidate, explicitly state that tradeoff and why the residuals are acceptable.
- Save smoothness evidence when the source has curves: a zoomed crop, path audit artifact, or render that makes edge quality inspectable.
- Binary-mask metrics over GRADIENT-filled parts (gold beads, glossy dots) inflate pixel diffs even when the part is visually faithful — the threshold cuts the gradient at a different isoline than the source's. Judge such parts structurally (center/radius/extent) and visually, and name the artifact when reporting.

**Structure the SVG semantically** even though no animation is planned: one element (or `<g>`) per visual part with stable ids (`#mark`, `#dot`, `#wordmark`). It costs nothing, makes the SVG editable, and keeps it upgradeable to an animated version later.

## Wordmark Font Matching (live `<text>`)

When shipping live `<text>` instead of traced letterforms (the default unless exact letterforms are required):

1. **Enumerate fonts actually installed** (`ls /System/Library/Fonts*`, `fc-list`) before testing candidates. Never trust name-based stacks: two "different" families scoring *identical* wordmark IoU means both silently fell back to the same font.
2. Per candidate, **auto-tune `font-size` to the source cap height** (2–3 render→measure→rescale iterations against the wordmark ink bbox), baseline pinned to the measured source baseline.
3. Rank by wordmark-region IoU **and ink-weight ratio** (rendered ink px ÷ source ink px). A weight ratio ≈ 1.0 with slightly lower IoU usually looks more faithful than a higher-IoU family with 1.2× heavier strokes — weight mismatch reads instantly, letterform differences read slowly. (Field case: Baskerville ratio 1.04 / IoU 0.535 visibly beat Times 1.26 / 0.540.)
4. Lock geometry cross-platform: `textLength="<measured width>" lengthAdjust="spacingAndGlyphs"` + `text-anchor` + measured baseline; order the family stack best-first with graceful fallbacks; document the substitution as a known residual.

## Workflow

1. **Measure first.** Locate the exact source file; record image size, mode, alpha, foreground colors, background. Extract per-part data: masks by color, centers/radii, edge samples. Read `references/fitting-playbook.md` BEFORE writing any fit code — it encodes the expensive lessons (windowed feature search, perpendicular width correction, boundary-from-source-pixels, G1 repair strategies, bridge segments, smooth correction models).

2. **Choose the first fitting strategy** from the ladder. Primitives for dots and geometric marks; stroke paths only for truly constant width; **filled outlines for ribbons or any variable-width stroke**; tracing as measurement, not final art.

3. **Generate a low-complexity first artifact.**
   - SVG with a correct `viewBox`; per-part ids.
   - Render + overlay + metrics in one command:
     `python3 scripts/render_overlay.py logo.svg source.png --out outputs/fit_iterations/01_first_overlay.png --render-out outputs/final_render.png`
   - Keep every fit script, sampled data, and parameter set in `outputs/fit_work/` from iteration 1 — never in `/tmp`.

4. **Inspect with multimodal vision.** Centers, radii, endpoints, width profile, extrema, negative space, silhouette, and edge smoothness. IoU is a supporting metric, not the whole judgment and not a fixed global gate. A high-IoU result still fails if it has structural mismatches, noisy handles, visible bumps, wrong negative space, or pixel-stair edges. Track pixel counts (`src_only_px`, `render_only_px`) and boundary RMS as supporting diagnostics. For smooth curves, run `scripts/svg_path_audit.py`; verify flagged joins by computing turn angles from the control points and classify intentional corners (tip caps, designed points) separately from kinks — only undesigned joins >8° are failures, and they are failures **even at high IoU**.

5. **Iterate — one change per iteration, 10 iterations max by default.**
   - Prefer moving/retuning a few knots over adding knots; if a path looks bumpy, reduce knots and re-fit macro curves.
   - When a local area is wrong, add local complexity only there (e.g. a short bridge segment across a curvature spike — see playbook §4).
   - Apply at most one smooth feedback-correction round (playbook §5); further rounds chase noise.
   - Save an overlay snapshot per iteration: `NN_name_overlay.png`, with metrics recorded.
   - The two stop triggers are evaluated after every iteration, and whichever arrives first ends the fitting loop: **accepted fit** (smoothness, structural, and visual checks pass, with IoU pushed as high as practical) or **10 iterations attempted**.

6. **Budget exhausted or acceptance reached → evaluate and ship/report.**
   - Acceptance reached early: finish immediately.
   - Budget exhausted: stop refining and select the best candidate. Rank candidates with a combined scorecard: (1) smoothness gate pass, (2) no structural mismatch, (3) IoU and pixel deltas, (4) boundary RMS / local residuals, (5) fewest audit kinks and tangent issues, (6) visual overlay verdict, (7) lowest editable complexity. A clean-but-slightly-loose fit beats a tighter fit with a visible kink; an invisible kink may ship only as a disclosed known issue.
   - Build the HTML deliverable: `python3 scripts/svg_to_js_html.py logo.svg --out logo.html --title "..."` — then render it in a real browser, save `html_render.png`, and visually compare against the SVG render (fail on blank, clipped, mis-scaled, or divergent output). The user-facing HTML preview should display the logo at **0.7x of the SVG's intrinsic width** (`width * 0.7`, still capped by the viewport) to leave breathing room.
   - Build `overlay_progress_strip.png` (source + current-run overlays + final render only).
   - In the final message, report the shipped iteration's quality honestly (metrics + known residuals, e.g. "IoU 0.97; sub-pixel boundary residue at the valley, antialiasing-scale"). If the IoU is lower than an alternative or visibly loose, explain the reason; if residuals are not acceptable, state that the current run is a preview, keep the fit state resumable, and offer continued refinement from `outputs/fit_work/`.

## Bundled Scripts

```bash
# measurement / starter trace (inspect & simplify; never final art by default)
python3 scripts/raster_logo_trace.py source.png --out outputs

# render + cyan overlay + IoU metrics in one step (headless Chrome; set CHROME_BIN if needed)
python3 scripts/render_overlay.py logo.svg source.png \
  --out outputs/fit_iterations/02_refined_overlay.png \
  --render-out outputs/final_render.png --report outputs/fit_metrics.json

# closed / self-intersecting variable-width ribbons: centerline scaffold +
# auto-recenter + source edge snap; emits outline + centerline path d + report
# (incl. each exclusion's arc fractions — the split-cut parameters pixel2motion needs)
python3 scripts/fit_ribbon_centerline.py source.png --seeds seeds.json --out-dir outputs/ribbon_fit

# Bezier smoothness audit before accepting complex smooth paths
python3 scripts/svg_path_audit.py logo.svg --out-svg outputs/bezier_segments.svg --report outputs/bezier_audit.json

# JS-rendered standalone HTML deliverable
python3 scripts/svg_to_js_html.py logo.svg --out logo.html --title "Vectorized Logo"

# end-of-run progress strip
python3 scripts/overlay_progress_strip.py --source source.png --dir outputs/fit_iterations \
  --pattern "*overlay*.png" --final-image outputs/final_render.png --out outputs/overlay_progress_strip.png
```

Environment notes: Pillow/numpy via a venv when system Python is externally managed (`python3 -m venv .venv && .venv/bin/pip install pillow numpy`); rendering and HTML screenshots use headless Chrome — no rasterizer or Playwright required (`"$CHROME" --headless=new --screenshot=... --window-size=WxH file://...`).

## Practical Heuristics

- If a path looks bumpy, first reduce knots and re-fit macro curves; do not add more points.
- For smooth ribbons, compare both boundaries separately; a centerline stroke may be wrong even when it seems close. Never build outlines by offsetting a G1 centerline (playbook §3).
- Keep endpoints under colored circles or masks intentional; butt caps under the covering shape, no protruding round caps.
- For a circular C-mark: fit center, inner/outer radii, start/end angles; encode as one arc-based path.
- For a dot: `<circle>` with flat fill unless the source shows a gradient.
- For baked-in checkerboards: threshold foreground by darkness/saturation; exclude the checkerboard from final output.
- For solid backgrounds: infer the background color from image borders.

## Acceptance Criteria

Completion requires evidence, not claims:

- SVG exists and renders; standalone HTML exists, recreates the SVG via JavaScript DOM calls, and has been executed in a real browser with `html_render.png` inspected and matching the SVG render in scale, position, color, clipping.
- Final overlay viewed; `overlay_progress_strip.png` shows source → current-run overlays → final render.
- Report final IoU and pixel deltas, but do not apply a fixed global IoU pass/fail value. IoU should be as high as practical after preserving smoothness and structural correctness. If a lower-IoU result passes, explain exactly why the residuals are acceptable.
- Smooth marks pass the path audit (no undesigned joins >8°), or the kink is disclosed as a known issue under budgeted delivery.
- No structural mismatch: wrong center, scale, endpoint, width profile, spacing, negative space, or silhouette.
- Remaining differences are explainable as antialiasing, deliberate smoothing, or acceptable font substitution.
- **Budgeted delivery**: if the 10-iteration budget ran out, best-of-run may be packaged when smoothness, structure, and visual QA pass and residuals are disclosed. If residuals are not acceptable, label it as a preview, keep the fit state resumable from `outputs/fit_work/`, and offer continued refinement.

IoU is mandatory to report but not a fixed-threshold gate. A high-IoU result fails if the geometry is unnecessarily complex, visibly bumpy, stair-stepped, or built from noisy traced handles.

## References

- `references/fitting-playbook.md` — field-tested fitting strategies: measurement, feature windows, boundary-from-source fitting, G1 repair & bridge segments, feedback corrections, iteration discipline, environment pragmatics.
- `references/ribbon-fitting.md` — closed/self-intersecting variable-width ribbons (centerline scaffold + measured recenter + source edge snap), pitfall table, wordmark font-matching protocol.

## v2 changelog

Hardened from a production run (calligraphic ∞ ribbon, width 2→28px, one self-crossing, occluding gold bead, serif wordmark):

- New `scripts/fit_ribbon_centerline.py` + `references/ribbon-fitting.md`: the centerline-scaffold recipe for closed/self-intersecting ribbons (seeded Catmull-Rom → normal-direction midpoint/width measurement → arclength-spaced control rebuild, converges in 2–3 passes → sub-pixel edge snap to source pixels). Measured pitfalls encoded: stride-based rebuild inflates control counts; heavy width smoothing curve-cuts caps ~1.5px; hairline tapers must not be snapped; exclusion gaps interpolate circularly. The report emits each exclusion's arc fractions — exactly the cut parameters a downstream split draw-on needs.
- Wordmark font-matching protocol: enumerate installed fonts (identical IoU across names = silent fallback), tune size to cap height, rank by ink-weight ratio alongside IoU, lock width with `textLength`.
- Gradient-vs-threshold artifact rule: binary-mask diffs over gradient fills are not shape errors; judge structurally and name the artifact.
