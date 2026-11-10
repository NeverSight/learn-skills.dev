---
name: image-to-svg
description: Convert a supplied raster image into editable SVG artwork while preserving its recognizable shapes, layout, colors, and negative space. Use for image-to-SVG conversion, vectorization, or tracing of logos, icons, sketches, and illustrations; not bitmap embedding, raster editing, general screenshot-to-UI implementation, or new artwork merely inspired by an image.
---

# Image to SVG

Reconstruct the supplied image as real vector geometry, using semantic parts and
rendered feedback rather than wrapping a bitmap in an SVG. Fidelity to the source
is the default; redesign or stylization requires the user's direction.
No image-generation model, external API, GPU, or tracing package is required.
This skill includes its own scripts and references; no other skill is required.

For standalone conversion, do not invoke a planning or image-generation skill:
the supplied image establishes the visual direction. Ask only about consequential
source or fidelity ambiguities. When a production workflow supplies a selected
image, optional baseline SVG, and a bounded conversion scope, read
[vector-handoff.md](references/vector-handoff.md). Return a separate candidate;
do not take over art direction or start another production workflow.

## 1. Inspect the actual source

Open the supplied image with an available image-viewing tool before drawing.
Inspect its pixel dimensions, aspect ratio, orientation, transparency, and visible
content. Do not infer shapes from a filename or claim to inspect an inaccessible
attachment. If the source is missing or cannot be viewed, ask for an accessible
image instead of inventing a reconstruction.

Identify the intended artwork separately from any screenshot frame, checkerboard,
or surrounding UI. Preserve the source canvas and background by default; do not
automatically crop whitespace or turn a white background transparent. Ask only
when ambiguity about the target region or fidelity would materially change the
result. Preserve the original and write conversion outputs separately.

## 2. Choose the conversion approach

- **Flat logo, icon, or illustration:** rebuild meaningful shapes with primitives
  and short paths. Prioritize silhouette, cutouts, spacing, and layer order.
- **Line drawing or sketch:** preserve stroke rhythm, junctions, open ends, and
  intentional irregularity; do not turn every stroke into a filled blob.
- **Dense or photographic image:** explain the tradeoff between a simplified
  editable illustration and a high-detail trace. Do not silently substitute a
  stylized result when close reproduction was requested.
- **Explicit automatic tracing:** use a suitable available local tracer, inspect
  its result, and disclose whether the output is contour-editable or semantically
  organized. Do not claim to have run a tracer when drawing paths manually.

Read [conversion-modes.md](references/conversion-modes.md) for tracing, lettering,
photographic sources, and low-resolution edge treatment when relevant.
Do not install heavyweight tracing stacks or upload the source to a conversion
service by default. A task to convert an image does not require generating a new
bitmap. If the input is already SVG, inspect and edit that source instead of
rasterizing and retracing it. Preserve existing IDs and unaffected parts.

## 3. Map the source to editable parts

Use a coordinate system matching the source aspect ratio, commonly
`viewBox="0 0 WIDTH HEIGHT"` with the source pixel dimensions. Keep margins and
landmark positions proportional; never stretch the image to a square to simplify
authoring. Record the target dimensions or crop if the user requested a change.

Identify a small set of recognition-bearing parts, their approximate bounds,
colors, holes, attachment points, and back-to-front order. Separate intentional
detail from compression artifacts or antialiasing. For multipart work, assign
stable IDs such as `bird.body`, `bird.wing`, and `bird.eye` and group related parts.
A separate scene file is useful for complex iterative work, not required for a
simple conversion. When using one, follow the bundled
[scene-model.md](references/scene-model.md) schema so its mappings can be validated.
For a new scene, record observed art direction and semantic parts as a v2 `plan`,
then add actual tags/parents and set `phase: "bound"` after authoring. Reuse supplied
plans and existing IDs; preserve v1 maps without requiring migration. A generated
reference must not override explicit preservation requirements from the handoff.

## 4. Author genuine vector geometry

Create a standalone SVG with the SVG namespace and a finite positive `viewBox`.
Use circles, ellipses, rectangles, and polygons where they fit the reference;
otherwise use purposeful Bézier paths. Place anchors at corners, extrema, and
inflections rather than following every source pixel. Preserve intentional
asymmetry, negative space, overlapping objects, and holes in compound paths.

Keep meaningful parts independently editable, fills and strokes explicit, and
resource references local. Use presentation attributes for compatibility with
the bundled validator. Gradients are appropriate when visible in the
source; they are not a reason to flatten the artwork. Include a useful `title`
and, when needed, `desc` without inventing facts about the image.

Do not use embedded or linked raster images, data-URI bitmaps, `foreignObject`,
scripts, external resources, or one rectangle per pixel to simulate vectorization.
Do not change branding, lettering, color count, or background to make conversion
easier. Disclose approximations and font dependencies rather than promising exact
reproduction from insufficient source detail.

## 5. Validate and compare against the source

Check XML, namespace, viewBox, geometry, duplicate IDs, and local references; also
check that the output contains no raster content. Resolve `SKILL_DIR` to the
directory containing this file, not the current working directory. Read
[tooling.md](references/tooling.md) for the bundled helpers, runtime dependencies,
static-vector profile, and exit codes. Python 3.10+ is required.

```bash
python3 "$SKILL_DIR/scripts/validate_svg.py" converted.svg
python3 "$SKILL_DIR/scripts/render_svg.py" converted.svg --output preview.png --width 768
```

Use `validate_scene.py scene.json` for a plan-only contract check. Add
`--scene scene.json` to SVG validation only after a scene is bound; the command
rejects an unbound plan rather than pretending its mapping was verified. Choose
the preview width for the source or intended display size. Fix validation errors
before rendering, then actually open the PNG alongside the source. Do not strip
unsupported source features just to satisfy the bundled static-vector profile.

Compare at the same aspect ratio, crop, and background, both at source/display
size and zoomed in. Inspect silhouette and landmark alignment first, then holes,
occlusion, spacing, palette, stroke weight, and lettering. Check transparency on
both light and dark backgrounds. A successful parse or render does not establish
visual fidelity, and pixel-error metrics are not a substitute for inspection.

Correct the largest visible discrepancy with a focused edit, revalidate, render,
and inspect again. Preserve the best version. Stop when the brief is satisfied or
after three unproductive correction rounds; report remaining limitations rather
than repeatedly adding detail. Rerender after cleanup or path simplification.
The bundled `measure_svg.py` reports structural complexity; `normalize_svg.py`
only normalizes XML serialization, not geometry. Use `compare_render.py` for
optional pixel measurements, not as a fidelity or design-quality verdict.
If rendering or image viewing is unavailable, explicitly state which checks were
not performed and do not describe the conversion as visually verified.

## Deliver

Return the editable `.svg` and a rendered preview when available. Briefly state
the conversion method, any intentional simplification, text/font treatment when
relevant, and unresolved fidelity or verification limits. Keep source images and
internal iterations out of the deliverable unless requested.
