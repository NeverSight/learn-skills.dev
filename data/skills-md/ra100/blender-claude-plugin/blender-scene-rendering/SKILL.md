---
name: blender-scene-rendering
description: Blender 5.x scene setup, render engines (Cycles/EEVEE), output formats, import/export (FBX/glTF/OBJ/USD/Alembic), linking/appending, color management (AgX/Filmic), view layers, viewport config, and world/environment setup via Python (bpy). Includes 5.1 changes (AVIF, HTJ2K, OpenColorIO 2.5, Light Path in World).
---

# Blender Scene & Rendering Expert

## Overview

This skill provides expert guidance for Blender 5.x scene setup, render configuration, output pipelines, file import/export, linking/appending, viewport settings, and project-level Python automation. The reference files contain the complete settings catalog and Python API patterns.

## MCP-First Approach

Prefer the **official Blender MCP Server** (Blender Lab, Blender 5.1+) for changing render settings, importing files, configuring color management, kicking off renders directly in a running Blender session. Fall back to emitting Python scripts only when the MCP server is not connected.

**Detection:** at session start, look for tools whose names match `execute_blender_code`, `get_objects_summary`, or `search_api_docs` — these belong to the official `blender-mcp` server. If any are present, MCP is available.

**Tools used by this skill:**

- `execute_blender_code` — run `bpy` Python in the live session (primary action)
- `get_objects_summary`, `get_object_detail_summary` — inspect scene state before mutating
- `get_blendfile_summary_datablocks` / `_missing_files` / `_of_linked_libraries` / `_path_info` / `_usage_guess` — inventory the file
- `search_api_docs`, `get_python_api_docs`, `search_manual_docs` — confirm correct API/operator names before calling them
- `get_screenshot_of_window_as_image` / `_as_json`, `get_screenshot_of_area_as_image` — verify visual results
- `jump_to_tab_by_name`, `jump_to_tab_by_space_type`, `jump_to_view3d_object_by_name`, `jump_to_view3d_object_data_by_name` — drive the UI to make changes visible
- `render_thumbnail_to_path`, `render_viewport_to_path` — capture quick visual feedback

**Workflow:** inspect with a `get_*` / `search_*` tool → mutate via `execute_blender_code` → verify with a screenshot or summary tool. Keep code blocks small and idempotent so failures are easy to localize.

Setup: see [docs/blender-mcp-setup.md](../../docs/blender-mcp-setup.md).

## Task Decision Tree

- **"Set up render / configure Cycles or EEVEE"** -> See Render Engine Configuration
- **"Change resolution / output format"** -> See Output Settings
- **"Adjust samples / denoising"** -> See Sampling & Denoising
- **"Color management / Filmic / AgX"** -> See Color Management
- **"Set up world / environment / HDRI"** -> See World & Environment
- **"Import FBX / glTF / OBJ / USD"** -> See Import/Export
- **"Link or append from another .blend"** -> See Linking & Appending
- **"Configure units / frame range / FPS"** -> See Scene Settings
- **"View layers / render passes"** -> See View Layers
- **"Viewport shading / overlays"** -> See Viewport Configuration
- **"Batch render / automate output"** -> See Batch Rendering
- **"Render looks wrong"** -> See Debugging section

## Render Engine Configuration

### Switch to Cycles

```python
import bpy

scene = bpy.context.scene
scene.render.engine = 'CYCLES'

# Device: CPU or GPU
cycles = scene.cycles
cycles.device = 'GPU'

# GPU compute device type
prefs = bpy.context.preferences.addons['cycles'].preferences
prefs.compute_device_type = 'CUDA'  # CUDA, OPTIX, HIP, METAL, ONEAPI
prefs.get_devices()  # Refresh device list
for device in prefs.devices:
    device.use = True  # Enable all available devices
```

### Switch to EEVEE

```python
import bpy

scene = bpy.context.scene
scene.render.engine = 'BLENDER_EEVEE'  # Blender 4.x+/5.x EEVEE

eevee = scene.eevee

# Shadows
eevee.shadow_ray_count = 1
eevee.shadow_step_count = 6

# Ray tracing
eevee.use_raytracing = True
eevee.ray_tracing_method = 'SCREEN'  # SCREEN or FULL

# Emission transparency (for emissive materials that need alpha blending)
# Set per-material: material.surface_render_method = 'BLENDED'

# Ambient Occlusion (baked into lighting in EEVEE)
```

### Workbench (Solid/Preview)

```python
import bpy
bpy.context.scene.render.engine = 'BLENDER_WORKBENCH'
```

## Output Settings

### Resolution & Frame Range

```python
import bpy

render = bpy.context.scene.render

# Resolution
render.resolution_x = 1920
render.resolution_y = 1080
render.resolution_percentage = 100

# Frame range
scene = bpy.context.scene
scene.frame_start = 1
scene.frame_end = 250
scene.frame_step = 1
scene.frame_current = 1

# FPS
render.fps = 24
render.fps_base = 1.0  # Actual FPS = fps / fps_base
```

### Output Format

```python
import bpy

render = bpy.context.scene.render
render.filepath = "//output/render_"  # // = relative to .blend file

# Image format
# Image format
render.image_settings.file_format = 'PNG'  # PNG, JPEG, OPEN_EXR, OPEN_EXR_MULTILAYER, TIFF, BMP, HDR, FFMPEG, AVIF (5.1)
render.image_settings.color_mode = 'RGBA'  # BW, RGB, RGBA
render.image_settings.color_depth = '16'   # 8, 16 (PNG/TIFF), 16/32 (EXR)
render.image_settings.compression = 15     # PNG compression 0-100

# EXR settings
render.image_settings.file_format = 'OPEN_EXR'
render.image_settings.exr_codec = 'DWAA'  # NONE, PXR24, ZIP, PIZ, RLE, ZIPS, DWAA, DWAB
render.image_settings.color_depth = '32'

# Video (FFmpeg)
render.image_settings.file_format = 'FFMPEG'
render.ffmpeg.format = 'MPEG4'        # MPEG4, MKV, WEBM, AVI, QUICKTIME
render.ffmpeg.codec = 'H264'          # H264, MPEG4, WEBM, PNG, HUFFYUV, DNXHD, FFV1
render.ffmpeg.constant_rate_factor = 'MEDIUM'  # NONE, LOSSLESS, PERC_LOSSLESS, HIGH, MEDIUM, LOW, LOWEST
render.ffmpeg.audio_codec = 'AAC'     # NONE, AAC, AC3, FLAC, MP2, MP3, OPUS, PCM, VORBIS
```

### OpenEXR HTJ2K (New in 5.1)
1. New EXR codec: `render.image_settings.exr_codec = 'HTJ2K'`
2. High-throughput JPEG 2000 compression for EXR files
3. Better compression ratios than DWAA/DWAB for multi-layer EXR output

### Video Custom CRF (5.1)
1. FFmpeg `constant_rate_factor` now supports integer values for finer control
2. Example: `render.ffmpeg.constant_rate_factor = 'HIGH'` or set numeric CRF directly

# AVIF format (new in 5.1)
render.image_settings.file_format = 'AVIF'
render.image_settings.avif_compression = 50  # Quality 0-100

## Sampling & Denoising

### Cycles Sampling

```python
import bpy

cycles = bpy.context.scene.cycles

# Render samples
cycles.samples = 256
cycles.use_adaptive_sampling = True
cycles.adaptive_threshold = 0.01    # Lower = higher quality
cycles.adaptive_min_samples = 64

# Viewport samples
cycles.preview_samples = 32
cycles.use_preview_adaptive_sampling = True

# Time limit (0 = disabled)
cycles.time_limit = 0.0

# Seed
cycles.seed = 0
cycles.use_animated_seed = True  # Different seed per frame

# Light paths
cycles.max_bounces = 12
cycles.diffuse_bounces = 4
cycles.glossy_bounces = 4
cycles.transmission_bounces = 12
cycles.volume_bounces = 0
cycles.transparent_max_bounces = 8

# Caustics
cycles.caustics_reflective = False
cycles.caustics_refractive = False

# Clamping (reduce fireflies)
cycles.sample_clamp_direct = 0.0    # 0 = disabled
cycles.sample_clamp_indirect = 10.0
```

### Denoising

```python
import bpy

scene = bpy.context.scene
cycles = scene.cycles

# Render denoising
scene.cycles.use_denoising = True
scene.cycles.denoiser = 'OPENIMAGEDENOISE'  # OPENIMAGEDENOISE or OPTIX
scene.cycles.denoising_input_passes = 'RGB_ALBEDO_NORMAL'  # RGB, RGB_ALBEDO, RGB_ALBEDO_NORMAL
scene.cycles.denoising_prefilter = 'ACCURATE'  # NONE, FAST, ACCURATE

# Viewport denoising
scene.cycles.use_preview_denoising = True
scene.cycles.preview_denoiser = 'OPENIMAGEDENOISE'
scene.cycles.preview_denoising_start_sample = 1
```

## Color Management

### Configure Color Management

```python
import bpy

cm = bpy.context.scene.view_settings
ds = bpy.context.scene.display_settings

# Display device
ds.display_device = 'sRGB'  # sRGB, None

# View transform
cm.view_transform = 'AgX'       # Standard, Filmic, AgX, Raw, False Color
cm.look = 'None'                 # None, AgX - Punchy, AgX - Golden, etc.

# Exposure and gamma
cm.exposure = 0.0
cm.gamma = 1.0

# Sequencer color space
bpy.context.scene.sequencer_colorspace_settings.name = 'sRGB'
```

**Common view transforms:**

| Transform   | Use Case                                           |
| ----------- | -------------------------------------------------- |
| `AgX`       | Default for Blender 4.0+/5.x, wide dynamic range  |
| `Filmic`    | Legacy default, good for photorealistic scenes     |
| `Standard`  | sRGB direct (UI elements, non-photorealistic)      |
| `Raw`       | No transform (data passes, masks)                  |

## World & Environment

### HDRI Environment

```python
import bpy

world = bpy.context.scene.world
if world is None:
    world = bpy.data.worlds.new("World")
    bpy.context.scene.world = world

world.use_nodes = True
nodes = world.node_tree.nodes
links = world.node_tree.links
nodes.clear()

# Background + Environment Texture
bg = nodes.new('ShaderNodeBackground')
env_tex = nodes.new('ShaderNodeTexEnvironment')
env_tex.image = bpy.data.images.load("//hdri/studio.exr")
mapping = nodes.new('ShaderNodeMapping')
tex_coord = nodes.new('ShaderNodeTexCoord')
output = nodes.new('ShaderNodeOutputWorld')

links.new(tex_coord.outputs['Generated'], mapping.inputs['Vector'])
links.new(mapping.outputs['Vector'], env_tex.inputs['Vector'])
links.new(env_tex.outputs['Color'], bg.inputs['Color'])
links.new(bg.outputs['Background'], output.inputs['Surface'])

bg.inputs['Strength'].default_value = 1.0
```

### Solid Color World

```python
import bpy

world = bpy.context.scene.world
world.use_nodes = True
nodes = world.node_tree.nodes
bg = nodes.get('Background')
bg.inputs['Color'].default_value = (0.05, 0.05, 0.05, 1.0)
bg.inputs['Strength'].default_value = 1.0
```

## Import/Export

### Common Import Operations

```python
import bpy

# FBX
bpy.ops.import_scene.fbx(filepath="/path/to/model.fbx")

# glTF / GLB
bpy.ops.import_scene.gltf(filepath="/path/to/model.glb")

# OBJ
bpy.ops.wm.obj_import(filepath="/path/to/model.obj")

# USD
bpy.ops.wm.usd_import(filepath="/path/to/scene.usdc")

# Alembic
bpy.ops.wm.alembic_import(filepath="/path/to/cache.abc")

# STL
bpy.ops.wm.stl_import(filepath="/path/to/model.stl")

# SVG
bpy.ops.import_curve.svg(filepath="/path/to/graphic.svg")
```

### Common Export Operations

```python
import bpy

# FBX
bpy.ops.export_scene.fbx(
    filepath="/path/to/export.fbx",
    use_selection=True,          # Export selected only
    apply_scale_options='FBX_SCALE_ALL',
    axis_forward='-Z',
    axis_up='Y',
    use_mesh_modifiers=True,
    mesh_smooth_type='FACE',
    add_leaf_bones=False,
    bake_anim=True,
)

# glTF / GLB
bpy.ops.export_scene.gltf(
    filepath="/path/to/export.glb",
    export_format='GLB',         # GLB (binary), GLTF_SEPARATE, GLTF_EMBEDDED
    use_selection=True,
    export_apply=True,           # Apply modifiers
    export_animations=True,
    export_draco_mesh_compression_enable=False,
)

# OBJ
bpy.ops.wm.obj_export(
    filepath="/path/to/export.obj",
    export_selected_objects=True,
    apply_modifiers=True,
    export_uv=True,
    export_normals=True,
    export_materials=True,
)

# USD
bpy.ops.wm.usd_export(
    filepath="/path/to/export.usdc",
    selected_objects_only=True,
    export_animation=True,
    export_hair=True,
)

# Alembic
bpy.ops.wm.alembic_export(
    filepath="/path/to/export.abc",
    selected=True,
    start=1,
    end=250,
)

# STL
bpy.ops.wm.stl_export(
    filepath="/path/to/export.stl",
    export_selected_objects=True,
    apply_modifiers=True,
)
```

## Linking & Appending

### Append (Copy into Current File)

```python
import bpy

blend_path = "/path/to/library.blend"

# Append a single object
with bpy.data.libraries.load(blend_path) as (data_from, data_to):
    data_to.objects = ["ObjectName"]

# Link appended objects to active collection
for obj in data_to.objects:
    if obj is not None:
        bpy.context.collection.objects.link(obj)

# Append specific data types
with bpy.data.libraries.load(blend_path) as (data_from, data_to):
    data_to.materials = ["MaterialName"]
    data_to.node_groups = ["NodeGroupName"]
    data_to.collections = ["CollectionName"]
    data_to.worlds = ["WorldName"]
```

### Link (Reference, Stay Connected)

```python
import bpy

blend_path = "/path/to/library.blend"

with bpy.data.libraries.load(blend_path, link=True) as (data_from, data_to):
    data_to.collections = ["CollectionName"]

# Link collection instance to scene
for coll in data_to.collections:
    if coll is not None:
        bpy.context.collection.children.link(coll)

# Make library override (editable linked data)
# Select linked object first
bpy.ops.object.make_override_library()
```

### Reload / Relocate Libraries

```python
import bpy

for lib in bpy.data.libraries:
    lib.reload()  # Reload from disk

# Relocate a library to a new path
# lib.filepath = "/new/path/to/library.blend"
# lib.reload()
```

## Scene Settings

### Units

```python
import bpy

unit = bpy.context.scene.unit_settings
unit.system = 'METRIC'          # NONE, METRIC, IMPERIAL
unit.scale_length = 1.0         # 1.0 = 1 Blender unit = 1 meter
unit.length_unit = 'METERS'     # ADAPTIVE, KILOMETERS, METERS, CENTIMETERS, MILLIMETERS, MICROMETERS
unit.use_separate = True        # Use separate units (e.g., 1m 50cm)
unit.temperature_unit = 'CELSIUS'
```

### Multiple Scenes

```python
import bpy

# Create new scene
new_scene = bpy.data.scenes.new("MyScene")

# Copy scene (Full Copy = independent copy of all data)
bpy.ops.scene.new(type='FULL_COPY')  # NEW, EMPTY, LINK_COPY, FULL_COPY

# Switch active scene
bpy.context.window.scene = bpy.data.scenes["MyScene"]

# Delete scene
bpy.data.scenes.remove(bpy.data.scenes["MyScene"])
```

## View Layers

### Configure View Layers

```python
import bpy

scene = bpy.context.scene

# Create view layer
vl = scene.view_layers.new("MyLayer")

# Enable/disable collections per layer
vl.layer_collection.children["CollectionName"].exclude = True

# Render passes
vl.use_pass_combined = True
vl.use_pass_z = True
vl.use_pass_normal = True
vl.use_pass_diffuse_color = True
vl.use_pass_glossy_color = True
vl.use_pass_emit = True
vl.use_pass_ambient_occlusion = True
vl.use_pass_shadow = True
vl.use_pass_mist = True

# Cryptomatte
vl.use_pass_cryptomatte_object = True
vl.use_pass_cryptomatte_material = True
vl.use_pass_cryptomatte_asset = True
```

## Viewport Configuration

### Viewport Shading

```python
import bpy

# Access 3D viewport shading
for area in bpy.context.screen.areas:
    if area.type == 'VIEW_3D':
        for space in area.spaces:
            if space.type == 'VIEW_3D':
                shading = space.shading

                # Shading type: WIREFRAME, SOLID, MATERIAL, RENDERED
                shading.type = 'MATERIAL'

                # Solid mode options
                shading.light = 'STUDIO'       # STUDIO, MATCAP, FLAT
                shading.color_type = 'MATERIAL' # MATERIAL, SINGLE, OBJECT, RANDOM, VERTEX, TEXTURE

                # Rendered mode options
                shading.use_scene_lights_render = True
                shading.use_scene_world_render = True

                break
```

### Overlays

```python
import bpy

for area in bpy.context.screen.areas:
    if area.type == 'VIEW_3D':
        for space in area.spaces:
            if space.type == 'VIEW_3D':
                overlay = space.overlay

                overlay.show_overlays = True
                overlay.show_floor = True
                overlay.show_axis_x = True
                overlay.show_axis_y = True
                overlay.show_wireframes = False
                overlay.show_face_orientation = False
                overlay.show_stats = True

                break
```

## Batch Rendering

### Render All Cameras

```python
import bpy

scene = bpy.context.scene
original_camera = scene.camera

for obj in bpy.data.objects:
    if obj.type == 'CAMERA':
        scene.camera = obj
        scene.render.filepath = f"//output/{obj.name}_"
        bpy.ops.render.render(write_still=True)

scene.camera = original_camera
```

### Render Multiple Scenes

```python
import bpy

for scene in bpy.data.scenes:
    scene.render.filepath = f"//output/{scene.name}_"
    bpy.ops.render.render(write_still=True, scene=scene.name)
```

### Render Animation

```python
import bpy
bpy.ops.render.render(animation=True)  # Renders full frame range
```

## Debugging

### Render Issues

| Problem                         | Cause                                              | Fix                                                                      |
| ------------------------------- | -------------------------------------------------- | ------------------------------------------------------------------------ |
| Render is black                 | No lights, camera pointing wrong way               | Add light, check camera direction and clipping                           |
| Render is noisy                 | Low samples                                        | Increase `cycles.samples`, enable denoising                              |
| Fireflies (bright pixels)       | Caustics or unbounded light                        | Set `sample_clamp_indirect = 10`, disable caustics                       |
| Colors look washed out          | Wrong color management                             | Set view transform to `AgX` or `Filmic`                                  |
| Colors too saturated/contrasty  | View transform mismatch                            | Try `AgX` with `None` look                                               |
| Export missing textures         | Textures not packed or paths broken                 | `bpy.ops.file.pack_all()` before export, or use `export_format='GLB'`    |
| Import scale wrong              | Unit mismatch between apps                         | Adjust `scale_length` or import scale option                             |
| Linked objects not updating     | Library not reloaded                               | `bpy.data.libraries["lib"].reload()`                                     |
| Viewport slow                   | Too many objects in rendered mode                  | Switch to Solid, reduce subdivision levels, use collection visibility    |
| Missing render passes           | Passes not enabled on view layer                   | Enable passes in View Layer properties                                   |
| EEVEE looks different from Cycles | Engine differences in lighting                   | EEVEE Next with ray tracing enabled closes the gap                       |

## Reference Files

- `references/python_api.md` — Complete Python API patterns for scene/render/I/O operations
- `references/settings_reference.md` — All render engine settings, output formats, color management options, import/export format options

## Blender 5.1 Changes

### OpenColorIO 2.5
1. Blender 5.1 ships with OpenColorIO 2.5
2. Improved color space handling and display transforms
3. Better accuracy for AgX and other view transforms

### Cycles Performance
1. Significant rendering speedups for complex scenes
2. Improved adaptive sampling convergence

### EEVEE Performance
1. Reduced memory usage for screen-space effects
2. Faster ray tracing evaluation

### Light Path in World Nodes
1. Light Path node is now available in World node trees (not just materials)
2. Enables per-light-type effects in environment materials
