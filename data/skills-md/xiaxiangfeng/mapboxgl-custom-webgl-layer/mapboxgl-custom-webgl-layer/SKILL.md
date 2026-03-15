---
name: mapboxgl-custom-webgl-layer
description: "Build, debug, and optimize mapboxgl `type: 'custom'` layers using raw WebGL. Covers shader setup, buffer pipelines, matrix usage, animation uniforms, precision-safe coordinate handling (RTC/local origin), and multiple geometry types (lines, polygons, points/icons). Use for custom GIS overlays and for fixing jitter, tearing, flicker, or empty rendering issues."
---

# Mapbox GL Custom WebGL Layer

Implement custom Mapbox GL layers with deterministic WebGL lifecycle, stable geometry generation, and precision-safe rendering. Follow the workflow, rules, and checklists below.

## CustomLayerInterface Contract

A custom layer object must conform to the Mapbox `CustomLayerInterface`:

| Property / Method | Required | Description |
|---|---|---|
| `id` | ✅ | Unique layer identifier |
| `type` | ✅ | Must be `'custom'` |
| `renderingMode` | ❌ | `'2d'` (default, no depth) or `'3d'` (shares depth buffer) |
| `onAdd(map, gl)` | ❌ | Called once when layer is added. Initialize shaders, buffers, uniforms here. |
| `render(gl, matrix)` | ✅ | Called every frame. Draw geometry here. Do not assume GL state except blend/depth. |
| `prerender(gl, matrix)` | ❌ | Called before `render` if the layer needs to draw to a texture/FBO first. |
| `onRemove(map, gl)` | ❌ | Called when layer is removed. Delete buffers, programs, textures here. |

### Critical API Notes
1. Mapbox uses **premultiplied alpha** blending. The expected blend state is `gl.blendFunc(gl.ONE, gl.ONE_MINUS_SRC_ALPHA)`. Fragment shaders must output premultiplied colors: `gl_FragColor = vec4(color.rgb * color.a, color.a)`.
2. Do NOT assume any GL state in `render` except that blending and depth are configured for compositing. Set all other state explicitly.
3. Call `map.triggerRepaint()` only when continuous animation is needed.
4. Handle `webglcontextlost` / `webglcontextrestored` events to recreate GPU resources gracefully.

## Workflow
1. Normalize input data into explicit `LineString` / `MultiLineString` / `Polygon` / `MultiPolygon` / `Point` primitives.
2. Construct a custom layer object with `id`, `type: 'custom'`, `renderingMode`, `onAdd`, `render`, and `onRemove`.
3. In `onAdd`: compile/link shaders, cache attribute/uniform locations, allocate buffers, register context-loss listeners.
4. Build geometry on CPU: convert coordinates → Mercator → local offsets. Upload typed arrays with `gl.bufferData`.
5. In `render`: compute `originClip` on CPU, set uniforms (`u_matrix`, `u_originClip`, time, colors), bind buffers, set GL state, draw.
6. Trigger repaint only when animation is active.
7. In `onRemove`: delete buffers, program, textures; remove event listeners.

## Data Preprocessing
1. Parse GeoJSON features, flatten `Multi*` geometries into individual primitives.
2. Convert `[lng, lat]` to Mercator using `mapboxgl.MercatorCoordinate.fromLngLat(lngLat)`.
3. Use `MercatorCoordinate.meterInMercatorCoordinateUnits()` to convert metric widths/offsets to Mercator space.
4. Remove consecutive duplicate points (`dist < epsilon`).
5. Optionally simplify dense polylines (Douglas-Peucker) for performance.

## Precision Rules (RTC Pipeline)
1. Keep geographic coordinates (`lng/lat`) on CPU only.
2. Convert to `MercatorCoordinate` on CPU — values range [0, 1].
3. Pick one local origin (`originMercator`) per geometry batch (e.g. centroid or first point).
4. Store vertex positions as local offsets: `local = mercator - originMercator`.
5. Per frame on CPU: `originClip = matrix * vec4(originMercator.x, originMercator.y, 0, 1)`.
6. In vertex shader: `offsetClip = matrix * vec4(a_pos, 0, 0)` (note `w=0`), then `gl_Position = originClip + offsetClip`.
7. **Never** add large world coordinates and small offsets in GPU math.
8. Use `highp` in vertex shader. Use fragment precision fallback guard:

```glsl
#ifdef GL_FRAGMENT_PRECISION_HIGH
precision highp float;
#else
precision mediump float;
#endif
```

Reference: [precision-playbook.md](references/precision-playbook.md)

## Geometry Rules

### Lines / Path Ribbons
1. Sample centerline in input order (do not reorder points).
2. Compute direction from neighboring samples and derive perpendicular normals.
3. Use miter join with clamp (`miterLimit ≈ 2.0`) and bevel fallback on sharp turns.
4. Build triangle strip or indexed triangle list deterministically.
5. For animated patterns, compute cumulative `lineDistance` on CPU and pass as attribute.
6. Rebuild buffers only when geometry-affecting props change (data, width, offset, join style).

### Polygons
1. Flatten rings from GeoJSON: outer ring + holes.
2. Triangulate using earcut (or equivalent): `earcut(flatCoords, holeIndices, dimensions)`.
3. Convert resulting vertex positions to Mercator local offsets (same RTC pipeline).
4. Use `gl.drawElements(gl.TRIANGLES, ...)` with the earcut index buffer.
5. For extruded polygons (3D), add height attribute and adjust `renderingMode: '3d'`.

### Points / Icons / Symbols
1. For each point, emit a billboard quad (4 vertices, 2 triangles) centered at the point.
2. Pass quad corner offsets as attributes (e.g. `[-1,-1], [1,-1], [1,1], [-1,1]`).
3. In vertex shader, scale quad offsets by desired pixel size / zoom factor.
4. Use texture atlas or SDF (Signed Distance Field) for icon/glyph rendering.
5. For large point counts, consider instancing (`ANGLE_instanced_arrays` extension).

Reference: [common-patterns.md](references/common-patterns.md)

## Render-State Rules
1. Set blend state explicitly: `gl.blendFunc(gl.ONE, gl.ONE_MINUS_SRC_ALPHA)` (premultiplied alpha).
2. Disable depth test for pure 2D overlay layers unless 3D ordering is required.
3. Rebind attribute pointers explicitly every frame — do not rely on preserved state.
4. Avoid hidden global state assumptions between custom layers.
5. Restore any modified GL state if the layer modifies non-standard state (stencil, scissor, etc.).
6. Keep `renderingMode` aligned with intent: `'2d'` for overlays, `'3d'` for depth interaction.

## Performance Rules
1. Use `gl.STATIC_DRAW` for geometry that rarely changes; `gl.DYNAMIC_DRAW` for frequently updated data.
2. Avoid rebuilding geometry or re-uploading buffers every frame.
3. Batch multiple features into a single draw call when possible.
4. Minimize shader uniform uploads — cache values and skip if unchanged.
5. Use `Uint16Array` for index buffers when vertex count ≤ 65535; `Uint32Array` with `OES_element_index_uint` extension otherwise.
6. Consider using VAO (`OES_vertex_array_object`) to reduce per-frame attribute setup cost.

## Debug Sequence
1. Check layer is actually added: `map.getLayer(id)`.
2. Check shader compile/link logs before geometry debugging.
3. Log `indexCount` / `vertexCount`; if zero, fix data normalization or geometry build.
4. If geometry exists but nothing renders, verify attribute locations are not `-1` and draw count > 0.
5. If geometry renders but flickers/jitters, verify RTC pipeline and `w=0` local transform.
6. If colors appear too bright or too dark, check premultiplied alpha output.
7. If spikes or self-intersections appear, tune join strategy (reduce `miterLimit`, use bevel fallback).
8. If visuals disappear on some GPUs, check precision declarations and fragment fallback.
9. If layer disappears after tab switch, handle `webglcontextrestored` event.

Reference: [troubleshooting-checklist.md](references/troubleshooting-checklist.md)

## Output Contract
1. Return implementation changes with concrete file paths and line-level rationale.
2. Explain precision decisions explicitly when touching vertex transforms.
3. Explain blending mode choice (premultiplied alpha).
4. Add a short validation checklist: render visible, zoom/pan stability, no shader errors, context-loss recovery.
