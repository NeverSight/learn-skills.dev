---
name: reference-to-3d
description: Reconstruct Blender models from supplied reference sheets, branding templates, texture atlases, orthographic front/side/back/top views, or mascot/logo art where visual fidelity to the source is more important than a plausible generated object. Use when the user says the model must match a template, wireframe, texture pack, character sheet, mascot sheet, or brand asset exactly; also use after feedback like "does not look like the reference", "fit the texture 1:1", "wrong number of visible parts", or "compare against the template". Requires Blender MCP plus local Python with Pillow/OpenCV/numpy; pairs with blender-uv-texturing, wireframe-to-3d, blender-modeling, blender-materials, and blender-export.
when_to_use: User supplies reference images/templates/texture atlases/orthographic views and wants a model matching them, or repeated visual mismatch feedback requires a reference-locked corrective loop.
allowed-tools: Read Bash Glob Grep mcp__blender__execute_blender_code mcp__blender__get_scene_info mcp__blender__get_object_info mcp__blender__get_viewport_screenshot
---

# Reference-to-3D Reconstruction

This skill is for **source-locked modeling**: the reference asset is the contract. Do not generate a plausible object from memory and then decorate it. Extract measurements, part counts, silhouettes, and UV regions from the supplied files first, then build the Blender model to satisfy those measurements.

## 1:1 reconstruction upgrade

When the user requires true 1:1 matching, chain these skills instead of attempting another plausible modeling pass:

1. `reference-analysis-validator` for manifest, masks, part counts, overlay gates.
2. `orthographic-registration` for front/side/back/top coordinate agreement.
3. `contour-to-mesh` for silhouette-derived structural meshes.
4. `atlas-uv-fitting` for per-part texture/UV fitting.
5. `mascot-logo-reconstruction` as the full orchestrator for brand mascot/logo work.

Do not export a final asset until the validation JSON and overlay render pass the manifest thresholds.

## Triggered failure mode

If the user says the output does not match the templates/textures/wireframes, stop regular `text-to-blender` generation and enter this workflow. Repeated plausible-but-wrong renders usually mean the missing step is **reference analysis**, not another modeling iteration.

## Source-of-truth hierarchy

1. **Front template / front wireframe**: primary silhouette, visible part count, face/feature positions, brand read.
2. **Texture atlas**: exact part shapes, color/material boundaries, decals, lightmap/aura intent.
3. **Side/back/top views**: depth, stacking order, thickness, backside forms. They must not change the locked front projection.
4. **User feedback**: hard constraints; promote it into validation gates.

## Mandatory preflight checklist

Before Blender modeling, write a small `reference_manifest.json` with:

```json
{
  "source_files": [],
  "primary_view": "front",
  "expected_primary_parts": {"count": null, "labels": []},
  "structural_parts": [],
  "decorative_parts": [],
  "texture_regions": [],
  "validation_thresholds": {
    "front_mask_iou_min": 0.90,
    "bbox_center_tolerance_px": 12,
    "part_count_exact": true
  }
}
```

If the expected part count is unclear, derive it from the reference sheet with the analyzer and show the user the uncertainty instead of guessing.

## Pipeline

### 1. Inventory and classify sources

Classify each provided asset:

- `front_template`: hero brand image or front wireframe.
- `side_view`, `back_view`, `top_view`: orthographic depth references.
- `texture_atlas`: basecolor / albedo atlas containing pieces.
- `decal`: transparent face/expression or detail layer.
- `emissive`, `roughness`, `bump`, `normal`, `lightmap`: material maps.
- `aura/background`: optional visual context, not structural body geometry.

### 2. Analyze images locally

Use `scripts/template_analyzer.py` for first-pass component extraction:

```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/template_analyzer.py   --image /path/to/front_reference.png   --out /tmp/front_analysis.json   --mode edges  # use bright_on_dark/dark_on_bright/alpha when cleaner
```

The analyzer returns components with area, perimeter-derived score, bbox, centroid, contour, and approximate class hints. Use `--mode edges` for faint grey wireframes and Otsu modes for clean masks/atlases. Treat this as measurement input, not final authority.

### 3. Lock the front reference in Blender

Create a front reference plane or Image Empty in the same orthographic camera used for validation. Prefix it `REF_` and exclude it from export. Official Blender docs describe Image Empties as reference images/blueprints and support front/back depth, opacity, orthographic-only display, and axis-aligned display.

### 4. Build geometry from source contours

For each structural part:

1. Convert the 2D contour to front-view X/Z coordinates.
2. Generate a quad strip/grid inside that contour.
3. Assign Project-from-View-style UVs based on front X/Z bounds or exact atlas region.
4. Add only shallow Y-depth/crown/extrusion after the front silhouette is locked.
5. Keep part names semantic: `GEO-subject_part_top`, `GEO-subject_face_shell`, etc.

Do not radial-duplicate a mascot unless the reference is truly radial. Logos often have occlusion, intentional asymmetry, and a fixed visible part count.

### 5. Multi-view registration

- Front X/Z is locked first.
- Side view controls Y/Z depth envelope only.
- Top view controls X/Y spread only.
- Back view controls hidden/backside geometry and validation, not front silhouette.

If views disagree, keep the front brand read and document the conflict.

### 6. UV and texture mapping

Chain-load `blender-uv-texturing` when any texture pack is provided. For atlas-driven parts:

- crop or map per atlas region; do not project the whole atlas onto every part;
- front-facing hero surfaces use front-projected UVs;
- side/back surfaces use side/back UV islands, procedural fill, or baked colors;
- alpha decals need transparent material settings and must not introduce black planes;
- lightmaps are optional realtime helpers and should not be connected as emission unless specified.

### 7. Validation gates before export

Always produce:

- `front_preview.png`
- `front_overlay_reference.png`
- `front_mask_validation.json`
- `side_preview.png`
- `back_preview.png`
- `top_preview.png`

Use `scripts/silhouette_validator.py`:

```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/silhouette_validator.py   --reference /tmp/reference_mask.png   --render /tmp/render_mask.png   --out /tmp/validation.json
```

Refuse final export if:

- primary part count differs from manifest;
- front-mask IoU is below threshold;
- face/feature centroid is outside tolerance;
- optional aura/decorations are included in the base GLB by mistake.

## Blender code patterns

### Reference plane in front-view X/Z

```python
import bpy

def create_reference_plane(name, image_path, width, height, y=0.2, alpha=0.35):
    img = bpy.data.images.load(image_path, check_existing=True)
    mat = bpy.data.materials.new('MAT-' + name)
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    bsdf = nodes.get('Principled BSDF')
    tex = nodes.new('ShaderNodeTexImage')
    tex.image = img
    mat.node_tree.links.new(tex.outputs['Color'], bsdf.inputs['Base Color'])
    mat.node_tree.links.new(tex.outputs['Alpha'], bsdf.inputs['Alpha'])
    bsdf.inputs['Alpha'].default_value = alpha
    mat.blend_method = 'BLEND'
    verts = [(-width/2,y,-height/2),(width/2,y,-height/2),(width/2,y,height/2),(-width/2,y,height/2)]
    mesh = bpy.data.meshes.new(name + 'Mesh')
    mesh.from_pydata(verts, [], [(0,1,2,3)])
    mesh.update()
    uv = mesh.uv_layers.new(name='UV')
    for li, uvco in zip(mesh.polygons[0].loop_indices, [(0,0),(1,0),(1,1),(0,1)]):
        uv.data[li].uv = uvco
    obj = bpy.data.objects.new('REF-' + name, mesh)
    bpy.context.collection.objects.link(obj)
    obj.data.materials.append(mat)
    obj.hide_render = True
    return obj
```

### Validation print contract

```python
print('VALIDATE expected_primary_parts=', expected, 'actual=', actual)
print('VALIDATE front_locked=True reference_overlay_rendered=True')
if actual != expected:
    raise RuntimeError('Part-count mismatch; refusing export')
```

## When to stop and ask for human input

Ask for a correction only after generating evidence, e.g. an overlay image or JSON showing ambiguity. Do not ask vaguely. Example: “The analyzer finds N prominent structural components plus M faint background/decorative shapes. Should the GLB include only the structural components?”

## Sources distilled

- Blender Manual: Image Empties for reference images/blueprints; front/back display, opacity, orthographic and axis-aligned controls.
- Blender Manual: Trace Image to Grease Pencil works best from manually prepared black/white images and controlled resolution.
- Blender Manual: Shrinkwrap moves vertices to a target surface and is useful after silhouette lock for conforming secondary details.
- Blender Manual: UV/Image Texture and Project-from-View-style workflows require UV maps and material nodes for renders/exports.
- OpenCV docs: contour moments, area, perimeter, bounding boxes, template matching.
- scikit-image docs: SSIM for image similarity when pixel-MSE is not perceptually meaningful.
