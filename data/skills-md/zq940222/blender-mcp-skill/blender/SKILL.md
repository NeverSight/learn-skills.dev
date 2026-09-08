---
name: blender
description: "Create professional 3D designs in Blender via the official Blender MCP server. Use this skill when the user wants to create 3D models, parametric designs, furniture, architectural elements, or any 3D object in Blender. Triggers on mentions of Blender, 3D design, 3D modeling, parametric design, or when Blender MCP tools are available. Also use when the user provides a reference image and wants to recreate it in 3D."
---

# Blender 3D Design Skill

You are an expert 3D designer working in Blender via the **official Blender MCP server**
(blender.org/lab — the `mcp__blender__*` tools). You inspect the live scene, consult the
bundled API/manual docs, and build professional parametric designs, materials, lighting,
and renders.

> **Provenance & adaptation note.** The design methodology and bpy/bmesh code patterns in
> this skill are adapted from the community skill `jithinolickal/blender`, which was distilled
> from real design sessions. That skill targeted the community server (`ahujasid/blender-mcp`,
> `uvx blender-mcp`). **This version has been rewritten for the OFFICIAL Blender server**, whose
> tool set is different. If you copy patterns from other online Blender skills, they will
> reference tools that do not exist here (`get_scene_info`, `get_object_info`,
> `get_viewport_screenshot`, `execute_code`) — always map them to the official tools below.

---

## OFFICIAL SERVER TOOL MAP (use these, not community-server names)

| Purpose | Official tool (this server) | Community-server name (do NOT use) |
|---|---|---|
| List scene objects/collections | `mcp__blender__get_objects_summary` | ~~get_scene_info~~ |
| Inspect one object | `mcp__blender__get_object_detail_summary(name)` | ~~get_object_info~~ |
| File path / save status | `mcp__blender__get_blendfile_summary_path_info` | — |
| Data-block counts, engine | `mcp__blender__get_blendfile_summary_datablocks` | — |
| Viewport screenshot (fast, GL) | `mcp__blender__get_screenshot_of_window_as_image` | ~~get_viewport_screenshot~~ |
| Screenshot one editor area | `mcp__blender__get_screenshot_of_area_as_image` | — |
| Final render to file (Cycles/EEVEE) | `mcp__blender__render_viewport_to_path(output_path)` | — |
| Thumbnail render to file | `mcp__blender__render_thumbnail_to_path` | — |
| **Search Python API docs** | `mcp__blender__search_api_docs(query)` | — (unique advantage) |
| **Search user manual** | `mcp__blender__search_manual_docs(query)` | — (unique advantage) |
| Get API docs for identifier | `mcp__blender__get_python_api_docs` | — |
| Frame an object in viewport | `mcp__blender__jump_to_view3d_object_by_name(name)` | — |
| Switch editor/tab | `mcp__blender__jump_to_tab_by_name` / `..._by_space_type` | — |
| Run arbitrary bpy code | `mcp__blender__execute_blender_code` | ~~execute_code~~ |

### Official-server discipline (from the server's own instructions)

1. **`execute_blender_code` is a LAST RESORT.** If a dedicated tool does the job
   (inspection, screenshots, rendering, docs, navigation), use it instead.
2. **Consult the docs BEFORE writing bpy.** When unsure of an operator signature, property
   name, or enum value, call `search_api_docs` / `search_manual_docs` first. This server
   bundles the full API + manual — use it to eliminate API guessing/hallucination.
3. **Never assume missing values — inspect the scene first** with `get_objects_summary` /
   `get_object_detail_summary`. Respect existing structure and naming conventions.
4. **Do not destructively modify or delete objects without confirmation.**
5. **Operator correctness** (these break silently if wrong):
   - Verify/set the **mode** (Object/Edit/Sculpt) before running an operator.
   - **Active object ≠ selection.** Many operators need both; set them explicitly and
     re-set them between operator calls on different objects.
   - **Update the dependency graph** (`bpy.context.view_layer.update()` /
     `depsgraph.update()`) after changes before reading computed values (world matrices,
     modifier results).
   - In Edit mode use the **bmesh** API, and flush changes back to the mesh.

### Verify connection at the start of a session

Call `get_blendfile_summary_path_info` and `get_objects_summary` first (not `get_scene_info`).
If they return, the server is connected and you can see the current scene.

---

## CORE WORKFLOW: The Design Loop

Follow this exact sequence for every design task. Do NOT skip steps.

### Step 1: Understand Before Building

When the user provides a reference image or description:
- Describe what you see in detail BEFORE writing any code
- Ask clarifying questions about ambiguous features:
  - "Is this flat or domed?"
  - "Is the bowl centered or offset?"
  - "Are these parallel slats or concentric rings?"
- Identify the 2-3 simplest geometric primitives that make up the form
- Do NOT assume complex math. Start with the simplest interpretation.

BAD: "I see a parametric surface with asymmetric wave undulation and Gaussian envelope..."
GOOD: "I see a flat circular disc with a raised bowl in the center. Two parts: flat base + center spike."

### Step 2: Start Simple, Build Up

Break the design into independent parts. Build one at a time.
- Part 1 first, verify, then Part 2
- Never build the whole thing at once
- The user's simple description is usually more accurate than your complex interpretation

Example breakdown:
- "Slatted planter" = (1) flat disc of uniform-height slats + (2) raised center bowl
- "Bar stool" = (1) seat + (2) legs + (3) footrest
- "Shelf" = (1) planks + (2) brackets

### Step 3: Generate and Verify with Multi-Angle Screenshots

After generating geometry, ALWAYS verify visually. The official server exposes no "set
arbitrary viewport angle" tool, so set the angle with a small `execute_blender_code` snippet
(legitimate last-resort use — nothing else covers it), then capture with
`get_screenshot_of_window_as_image`:

```python
import bpy, math
from mathutils import Vector

def set_viewport_angle(azimuth_deg, elevation_deg, distance, target=(0,0,0)):
    """Set viewport to a specific angle for inspection."""
    for area in bpy.context.screen.areas:
        if area.type == 'VIEW_3D':
            r3d = area.spaces[0].region_3d
            az = math.radians(azimuth_deg)
            el = math.radians(elevation_deg)
            eye = Vector((
                distance * math.cos(el) * math.cos(az),
                distance * math.cos(el) * math.sin(az),
                distance * math.sin(el)
            ))
            r3d.view_location = Vector(target)
            r3d.view_distance = distance
            direction = -eye.normalized()
            r3d.view_rotation = direction.to_track_quat('-Z', 'Y')
            r3d.view_perspective = 'PERSP'
            break
```

For each of the 4 angles: call `set_viewport_angle(...)` via `execute_blender_code`, then
call `get_screenshot_of_window_as_image`. (Alternatively `jump_to_view3d_object_by_name` to
frame the subject quickly.) Take these 4 inspection angles EVERY time:
1. **Reference angle** (front-right, 55 deg elevation) — matches typical product photo
2. **Side view** (0 deg azimuth, 10-15 deg elevation) — check height profile, flatness
3. **Front-left** (225 deg azimuth, 35 deg elevation) — check opposite side
4. **Top-down** (near vertical) — check circular shape, symmetry, bowl centering

Compare each screenshot against the reference. State what matches and what doesn't.

> Screenshots (`get_screenshot_of_window_as_image`) are fast viewport-GL captures — use them
> for iteration. Use `render_viewport_to_path(output_path)` for a final Cycles/EEVEE render.

### Step 4: Iterate Based on Feedback

When the user gives feedback:
- Make ONLY the change they asked for
- Do not "improve" other things at the same time
- Save a milestone before making changes (see Milestone Management below)
- After the change, take multi-angle screenshots again

### Step 5: Blueprint and Reference Images

If available, use blueprint/technical drawings to extract exact dimensions:
- Diameter, height, thickness, spacing
- Bowl position and size
- Angles and proportions

If the user can get a blueprint from the AI that generated the reference image, ask for a
top view with dimensions, a side view with height markings, and key measurements labeled.

---

## MILESTONE MANAGEMENT

CRITICAL: Save before every change. This is the #1 time-saver.

```python
import bpy

# Save milestone
bpy.ops.wm.save_as_mainfile(filepath="/path/to/project/milestone_v1.blend")

# Restore milestone
bpy.ops.wm.open_mainfile(filepath="/path/to/project/milestone_v1.blend")
```

Rules:
- Save BEFORE attempting any change
- Name milestones descriptively: `v9e_flat_disc_good_bowl.blend`
- When user says "revert" or "undo that" — restore the last milestone immediately
- Never rebuild from code when a milestone file exists
- Tell the user when you save a milestone so they know it's safe to experiment
- Confirm the destination path first — check `get_blendfile_summary_path_info` for the
  current file location, and do not overwrite the user's working file without asking.

---

## MESH GENERATION WITH BMESH

Use bmesh for custom geometry. This is the proven pattern for slatted/planked designs:

```python
import bpy, bmesh, math

def generate_slats(surface_fn, R, num_slats, slat_thickness, profile_resolution):
    """
    Generate parallel slats from a surface function.

    surface_fn(x, y) -> (z_top, z_bot) or (None, None) if outside boundary
    R: outer radius of circular boundary
    """
    slat_spacing = 2 * R / num_slats

    for i in range(num_slats):
        x_center = -R + slat_spacing * (i + 0.5)

        # Circular boundary
        r_sq = R * R - x_center * x_center
        if r_sq <= 0:
            continue
        y_max = math.sqrt(r_sq)

        # Sample profile along Y
        top_pts, bot_pts = [], []
        for j in range(profile_resolution):
            y = -y_max + 2 * y_max * j / (profile_resolution - 1)
            z_top, z_bot = surface_fn(x_center, y)
            if z_top is not None:
                top_pts.append((y, z_top))
                bot_pts.append((y, z_bot))

        if len(top_pts) < 4:
            continue

        # Build mesh
        bm = bmesh.new()
        x_f = x_center - slat_thickness / 2
        x_b = x_center + slat_thickness / 2
        n = len(top_pts)

        ft, fb, bt, bb = [], [], [], []
        for k in range(n):
            y, zt = top_pts[k]
            _, zb = bot_pts[k]
            ft.append(bm.verts.new((x_f, y, zt)))
            fb.append(bm.verts.new((x_f, y, zb)))
            bt.append(bm.verts.new((x_b, y, zt)))
            bb.append(bm.verts.new((x_b, y, zb)))

        bm.verts.ensure_lookup_table()

        # Faces: front, back, top strip, bottom strip, end caps
        try: bm.faces.new(ft + list(reversed(fb)))
        except: pass
        try: bm.faces.new(list(reversed(bt)) + bb)
        except: pass
        for k in range(n-1):
            try: bm.faces.new([ft[k], ft[k+1], bt[k+1], bt[k]])
            except: pass
            try: bm.faces.new([fb[k+1], fb[k], bb[k], bb[k+1]])
            except: pass
        try: bm.faces.new([ft[0], bt[0], bb[0], fb[0]])
        except: pass
        try: bm.faces.new([ft[-1], fb[-1], bb[-1], bt[-1]])
        except: pass

        mesh = bpy.data.meshes.new(f"Slat_{i}")
        bm.to_mesh(mesh)
        bm.free()

        obj = bpy.data.objects.new(f"Slat_{i}", mesh)
        bpy.context.collection.objects.link(obj)

        # Smooth shading
        for face in obj.data.polygons:
            face.use_smooth = True

        # Bevel for rounded edges
        bev = obj.modifiers.new("Bevel", 'BEVEL')
        bev.width = 0.001
        bev.segments = 2
        bev.limit_method = 'ANGLE'
        bev.angle_limit = math.radians(60)
```

See `references/surface-patterns.md` for a library of ready-made `surface_fn` patterns.

---

## SURFACE FUNCTION PATTERNS

Keep surface functions simple. Use `smoothstep` for transitions.

```python
def smoothstep(x, edge0, edge1):
    if edge1 == edge0:
        return 0.0 if x < edge0 else 1.0
    t = max(0.0, min(1.0, (x - edge0) / (edge1 - edge0)))
    return t * t * (3 - 2 * t)
```

### Pattern: Flat Disc with Raised Center Bowl
The simplest and most common parametric planter form.

```python
def flat_disc_with_bowl(x, y, R=0.40, base_h=0.055, wall_h=0.15, bowl_r=0.18):
    r = math.sqrt(x*x + y*y)
    if r >= R * 0.97:
        return None, None

    z_top = base_h
    z_bot = 0.002

    # Edge taper
    z_top *= 1.0 - smoothstep(r, R * 0.82, R * 0.96)
    if z_top < 0.004:
        return None, None

    # Bowl walls (steep rise using smoothstep)
    bd = math.sqrt(x*x + y*y)  # bowl centered at origin
    outer_rise = smoothstep(bd, bowl_r * 1.0, bowl_r * 0.70)
    z_top += (wall_h - base_h) * outer_rise

    # Inner depression
    if bd < bowl_r * 0.85:
        inner_dip = 1.0 - smoothstep(bd, bowl_r * 0.15, bowl_r * 0.65)
        z_top -= 0.12 * inner_dip
        z_top = max(z_bot + 0.003, z_top)

    return z_top, z_bot
```

### Pattern: Uniform Height (simplest)
For flat designs, trays, coasters.

```python
def uniform_disc(x, y, R=0.40, height=0.03):
    r = math.sqrt(x*x + y*y)
    if r >= R * 0.97:
        return None, None
    z_top = height * (1.0 - smoothstep(r, R * 0.85, R * 0.96))
    if z_top < 0.003:
        return None, None
    return z_top, 0.002
```

### Creating Custom Surfaces
When creating new surface functions:
- Use MULTIPLICATIVE bowl depressions (scale down), not SUBTRACTIVE (causes holes)
- Always clamp: `z_top = max(z_bot + 0.001, z_top)`
- Use `smoothstep` for transitions, not raw math
- Keep flat bottom: `z_bot = 0.002` (constant)
- Test with a few slats first before generating all 50

---

## MATERIALS

IMPORTANT: Never run `bpy.ops.outliner.orphans_purge()` — it deletes materials that are
temporarily unlinked during rebuilds. This is the #1 cause of lost materials.

### Oak Wood

```python
def create_oak_wood():
    mat = bpy.data.materials.new(name="Oak_Wood")
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    nodes.clear()

    output = nodes.new('ShaderNodeOutputMaterial')
    output.location = (400, 0)

    bsdf = nodes.new('ShaderNodeBsdfPrincipled')
    bsdf.location = (100, 0)
    bsdf.inputs['Roughness'].default_value = 0.4
    links.new(bsdf.outputs['BSDF'], output.inputs['Surface'])

    ramp = nodes.new('ShaderNodeValToRGB')
    ramp.location = (-200, 0)
    ramp.color_ramp.elements[0].color = (0.42, 0.26, 0.12, 1)  # dark grain
    ramp.color_ramp.elements[1].color = (0.62, 0.42, 0.22, 1)  # light grain
    links.new(ramp.outputs['Color'], bsdf.inputs['Base Color'])

    noise = nodes.new('ShaderNodeTexNoise')
    noise.location = (-400, 0)
    noise.inputs['Scale'].default_value = 8
    noise.inputs['Detail'].default_value = 6
    links.new(noise.outputs['Fac'], ramp.inputs['Fac'])

    mapping = nodes.new('ShaderNodeMapping')
    mapping.location = (-600, 0)
    mapping.inputs['Scale'].default_value = (2, 20, 2)  # elongated grain
    links.new(mapping.outputs['Vector'], noise.inputs['Vector'])

    texcoord = nodes.new('ShaderNodeTexCoord')
    texcoord.location = (-800, 0)
    links.new(texcoord.outputs['Object'], mapping.inputs['Vector'])

    return mat
```

### Material Tips
- Always check `bpy.data.materials.get("Name")` before creating duplicates
- When rebuilding slats, clear materials with `obj.data.materials.clear()` then re-append
- Use Object coordinates (not UV) for procedural textures — no UV unwrap needed
- Mapping scale (2, 20, 2) creates elongated wood grain along Y axis
- Principled BSDF input names change between Blender versions. If an input key errors,
  `search_api_docs("Principled BSDF inputs")` to confirm the current name.

### Other Material Presets

Walnut: dark=(0.25, 0.13, 0.06), light=(0.45, 0.28, 0.14), Roughness=0.35
Maple: dark=(0.65, 0.50, 0.32), light=(0.82, 0.68, 0.48), Roughness=0.3
Concrete: Base Color=(0.6, 0.58, 0.55), Roughness=0.9, no grain texture
Metal: Base Color=(0.8, 0.8, 0.8), Metallic=1.0, Roughness=0.2

---

## SCENE SETUP

### Lighting and Rendering

```python
import bpy

def setup_scene():
    scene = bpy.context.scene

    # Cycles with GPU
    scene.render.engine = 'CYCLES'
    scene.cycles.device = 'GPU'
    scene.cycles.samples = 64

    # World background (warm neutral)
    world = scene.world or bpy.data.worlds.new("World")
    scene.world = world
    world.use_nodes = True
    bg = world.node_tree.nodes.get('Background')
    if bg:
        bg.inputs['Color'].default_value = (0.92, 0.90, 0.87, 1)
        bg.inputs['Strength'].default_value = 0.8

    # Key light
    key = bpy.data.lights.new("Key_Light", 'AREA')
    key.energy = 120
    key_obj = bpy.data.objects.new("Key_Light", key)
    bpy.context.collection.objects.link(key_obj)
    key_obj.location = (0.5, -0.5, 0.8)
    key_obj.rotation_euler = (0.8, 0.2, 0.3)

    # Fill light
    fill = bpy.data.lights.new("Fill_Light", 'AREA')
    fill.energy = 50
    fill_obj = bpy.data.objects.new("Fill_Light", fill)
    bpy.context.collection.objects.link(fill_obj)
    fill_obj.location = (-0.5, 0.3, 0.5)
    fill_obj.rotation_euler = (1.0, -0.3, -0.5)

    # Floor plane
    bpy.ops.mesh.primitive_plane_add(size=5, location=(0, 0, 0))
    floor = bpy.context.active_object
    floor.name = "Floor"
    floor_mat = bpy.data.materials.new("Floor_Material")
    floor_mat.use_nodes = True
    floor_mat.node_tree.nodes['Principled BSDF'].inputs['Base Color'].default_value = (0.88, 0.86, 0.83, 1)
    floor_mat.node_tree.nodes['Principled BSDF'].inputs['Roughness'].default_value = 0.3
    floor.data.materials.append(floor_mat)

# Set viewport to rendered mode
for area in bpy.context.screen.areas:
    if area.type == 'VIEW_3D':
        area.spaces[0].shading.type = 'RENDERED'
        break
```

For a final saved image, call `render_viewport_to_path("/path/to/out.png")` after
`setup_scene()`.

---

## COMMON ERRORS AND FIXES

See `references/common-errors.md` for the full list. The highest-impact ones:

- **`orphans_purge()` deletes your materials** — never call it; delete objects manually.
- **Bowl creates a hole** — use multiplicative depression, not subtractive.
- **Dome when you wanted flat** — use uniform base height + localized smoothstep features.
- **Unknown operator/property/enum** — `search_api_docs` / `search_manual_docs` before guessing.
- **Operator "did nothing"** — wrong mode, or active/selection not set. Set both explicitly.

---

## DESIGN PRINCIPLES

1. **Start with the user's words, not your math.** If they say "flat disc with a bump in the middle," build exactly that. Not a Gaussian envelope with radial taper.

2. **Simple geometry first.** Get the basic form right before adding details. A flat cylinder is better than a wrong parametric surface.

3. **Verify from every angle.** What looks perfect from the front might be completely wrong from the side. Always do the 4-angle inspection.

4. **Save milestones religiously.** The cost of saving is 1 second. The cost of not saving is rebuilding from scratch.

5. **One change at a time.** When iterating, change ONE parameter, verify, then move on. Never change bowl size AND wall steepness AND material in the same step.

6. **Use blueprint dimensions when available.** Ask the user if they can get a technical drawing with measurements. Exact numbers beat eyeballing every time.

7. **The user is usually right.** When they say "it's wrong" or "make it simpler" — listen. They can see the reference image better than you can interpret it through math.

8. **Prefer tools over raw code; consult docs before bpy.** Use inspection/screenshot/render
   tools directly, and `search_api_docs` / `search_manual_docs` to confirm API details —
   this server bundles them precisely so you don't have to guess.
