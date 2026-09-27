---
name: blender-cameras
description: Set up Blender cameras with cinematic intent — focal length, depth of field (f-stop / focus object), composition (rule of thirds, leading lines), animated cameras (orbit, dolly, push-in), tracking constraints. Use whenever the user asks to "set up the camera", "frame the shot", "make it look cinematic / hero / portrait / wide-angle / telephoto", "add depth of field", "orbit the camera", or any composition/framing request. Make sure to use this skill even if the user does not say "camera" — also covers "hero shot", "close-up", "from above", "shallow focus", "85mm portrait look".
when_to_use: Any camera placement, framing, focal length, DoF, or animated camera setup in Blender.
allowed-tools: Read Bash mcp__blender__execute_blender_code mcp__blender__get_scene_info mcp__blender__get_object_info
---

# Blender Cameras

Set up cameras with the same decisions a real cinematographer makes: focal length for feel, f-stop for focus, composition for storytelling.

## Focal length cheat sheet

| Length | Feel | Use |
|--------|------|-----|
| 14–24mm | Very wide, distorted | Architecture, claustrophobic interiors, exaggerated perspective |
| 28–35mm | Wide, "documentary" | Establishing shots, environments |
| **50mm** | Neutral (≈ human eye) | Default storytelling |
| **85mm** | Short telephoto | Portraits, character close-ups (flattering) |
| 100–135mm | Telephoto | Hero product shots, isolated subjects |
| 200mm+ | Long tele | Wildlife, surveillance look, heavy compression |

**Quick rule**: 85mm for intimacy, 24mm for spectacle, 50mm for neutral.

## Aperture / f-stop

| f-stop | DoF | Use |
|--------|-----|-----|
| f/1.2–2.0 | Razor thin | Hero portraits, dreamy |
| f/2.8 | Shallow | Standard portrait |
| f/4 | Moderate | Two subjects in frame |
| f/5.6–8 | Medium-deep | Group portraits, environments |
| f/11+ | Very deep | Landscape, "everything sharp" |

## Recipes

### Recipe 0 — Bbox-aware hero camera (preferred for orchestrator chains)

Use this when you have a specific subject. Computes the subject's bounding box, places camera at a distance that fits the subject in ~80% of the frame vertically, and aims via Track-To.

```python
import bpy, math
from mathutils import Vector

# Choose subject — all meshes named GEO-* by default, or pass a specific list
subject_meshes = [o for o in bpy.data.objects if o.type == 'MESH' and o.name.startswith('GEO-')]
if not subject_meshes:
    raise RuntimeError("No subject meshes found (looking for GEO- prefix)")

# World-space bbox
deps = bpy.context.evaluated_depsgraph_get()
all_verts = []
for o in subject_meshes:
    eo = o.evaluated_get(deps); em = eo.to_mesh()
    for v in em.vertices:
        all_verts.append(o.matrix_world @ v.co)
    eo.to_mesh_clear()
xs = [v.x for v in all_verts]; ys = [v.y for v in all_verts]; zs = [v.z for v in all_verts]
center = Vector(((min(xs)+max(xs))/2, (min(ys)+max(ys))/2, (min(zs)+max(zs))/2))
height = max(zs) - min(zs)
width = max(xs) - min(xs)
biggest = max(height, width)

# Frame fit: at distance D, vertical frame = D × (sensor_h / focal). Solve for D.
focal_mm = 60        # 60mm gives a flattering not-too-wide hero shot
sensor_h_mm = 24     # full-frame
frame_per_meter = sensor_h_mm / focal_mm   # 0.4 m vertical frame per metre of distance
target_fill = 0.80
camera_distance = biggest / (frame_per_meter * target_fill)

# Camera positioned in front (negative Y) with slight X offset for a 3/4 angle
cam_pos = Vector((center.x + camera_distance * 0.3, center.y - camera_distance, center.z))

# Empty for tracking
empty_name = 'Empty-camera_target'
empty = bpy.data.objects.get(empty_name) or bpy.data.objects.new(empty_name, None)
if empty.name not in [o.name for o in bpy.context.collection.objects]:
    bpy.context.collection.objects.link(empty)
empty.location = center

# Camera
cam_data = bpy.data.cameras.new('CAM-hero')
cam_data.lens = focal_mm
cam_data.dof.use_dof = True
cam_data.dof.aperture_fstop = 4.0
cam_data.dof.focus_object = subject_meshes[0]   # focus on first/main subject

cam = bpy.data.objects.new('CAM-hero', cam_data)
bpy.context.collection.objects.link(cam)
cam.location = cam_pos

track = cam.constraints.new('TRACK_TO')
track.target = empty
track.track_axis = 'TRACK_NEGATIVE_Z'
track.up_axis = 'UP_Y'

bpy.context.scene.camera = cam
print(f"camera:bbox_aware center={tuple(round(v,2) for v in center)} dist={camera_distance:.2f}m focal={focal_mm}mm")
```

For elongated vertical subjects (sword, flag, candle): biggest dimension is height; the framing math fits height to 80% of vertical frame, which is what you want.

For wide horizontal subjects (car, table): biggest is width; it fits width to 80% of vertical frame too which over-zooms — for those, swap to `frame_per_meter_h = (sensor_h_mm * aspect_ratio) / focal_mm` or adjust target_fill down.

### Recipe 1 — Hero portrait camera (85mm + shallow DoF)

```python
import bpy, math

subject = bpy.data.objects.get('GEO-subject')   # change to your subject

# Camera
cam_data = bpy.data.cameras.new('CAM-hero')
cam = bpy.data.objects.new('CAM-hero', cam_data)
bpy.context.collection.objects.link(cam)
bpy.context.scene.camera = cam

cam.location = (3, -4, 1.6)
cam_data.lens = 85
cam_data.sensor_width = 36

# Depth of field
cam_data.dof.use_dof = True
cam_data.dof.aperture_fstop = 2.8
if subject:
    cam_data.dof.focus_object = subject

# Track-to constraint (auto-aim at subject)
if subject:
    track = cam.constraints.new('TRACK_TO')
    track.target = subject
    track.track_axis = 'TRACK_NEGATIVE_Z'
    track.up_axis = 'UP_Y'

print('camera:CAM-hero set')
```

### Recipe 2 — Wide environmental establishing shot (24mm)

```python
import bpy, math

cam_data = bpy.data.cameras.new('CAM-establish')
cam = bpy.data.objects.new('CAM-establish', cam_data)
bpy.context.collection.objects.link(cam)
bpy.context.scene.camera = cam

cam.location = (8, -10, 2.5)
cam.rotation_euler = (math.radians(80), 0, math.radians(35))

cam_data.lens = 24
cam_data.sensor_width = 36
cam_data.dof.use_dof = False

print('camera:CAM-establish (24mm wide)')
```

### Recipe 3 — Product hero (100mm + macro DoF)

```python
import bpy, math

subject = bpy.data.objects.get('GEO-product')

cam_data = bpy.data.cameras.new('CAM-product')
cam = bpy.data.objects.new('CAM-product', cam_data)
bpy.context.collection.objects.link(cam)
bpy.context.scene.camera = cam

cam.location = (0.4, -1.5, 0.2)   # close-in
cam_data.lens = 100
cam_data.sensor_width = 36
cam_data.dof.use_dof = True
cam_data.dof.aperture_fstop = 2.0
if subject:
    cam_data.dof.focus_object = subject

if subject:
    track = cam.constraints.new('TRACK_TO')
    track.target = subject
    track.track_axis = 'TRACK_NEGATIVE_Z'
    track.up_axis = 'UP_Y'

print('camera:CAM-product (100mm hero)')
```

### Recipe 4 — Composition guides (rule-of-thirds overlay)

```python
import bpy

cam_data = bpy.data.cameras['CAM-hero']
cam_data.show_composition_thirds = True
cam_data.show_composition_golden = False
cam_data.show_composition_center = False
print('composition:thirds_on')
```

These overlays show in viewport only; no effect on render.

### Recipe 5 — Orbit camera animation (10-second 360° turntable)

```python
import bpy, math

target = bpy.data.objects.get('GEO-subject')

# Empty as pivot
pivot = bpy.data.objects.new('Empty-orbit_pivot', None)
bpy.context.collection.objects.link(pivot)
if target:
    pivot.location = target.location

# Camera child of pivot
cam_data = bpy.data.cameras.new('CAM-orbit')
cam = bpy.data.objects.new('CAM-orbit', cam_data)
bpy.context.collection.objects.link(cam)
cam.parent = pivot
cam.location = (0, -5, 0.5)
cam.rotation_euler = (math.radians(85), 0, 0)
cam_data.lens = 50

bpy.context.scene.camera = cam

# Animate pivot's Z rotation: 0 → 360° over frames 1..240 (10s @ 24fps)
pivot.rotation_euler = (0, 0, 0)
pivot.keyframe_insert('rotation_euler', frame=1)
pivot.rotation_euler = (0, 0, math.radians(360))
pivot.keyframe_insert('rotation_euler', frame=240)

# Set linear interpolation for constant orbit speed
if pivot.animation_data and pivot.animation_data.action:
    for fc in pivot.animation_data.action.fcurves:
        for kp in fc.keyframe_points:
            kp.interpolation = 'LINEAR'

print('camera:CAM-orbit (10s turntable)')
```

### Recipe 6 — Push-in / dolly (camera moves forward, no zoom)

```python
import bpy

cam = bpy.data.objects['CAM-hero']

# Start position
cam.location = (3, -8, 1.6)
cam.keyframe_insert('location', frame=1)

# End position (closer to subject)
cam.location = (3, -4, 1.6)
cam.keyframe_insert('location', frame=120)
print('camera:dolly_5s')
```

A push-in (physical move forward) is visually distinct from a zoom (focal length change). Use push-ins for cinematic feel, zooms for surveillance/news look.

## Composition rules — enforce via positioning

1. **Rule of thirds**: place the subject at one of the 4 intersection points, not center.
2. **Headroom**: leave ~10% empty above the head.
3. **Nose room**: if subject faces left, leave space on the left for them to "look into".
4. **Foreground/midground/background**: three depth layers feel more cinematic.

## Sensor sizes

| Sensor | Width (mm) | Notes |
|--------|-----------|-------|
| Full frame DSLR / 35mm cinema | 36 | Default |
| APS-C | 22.5 | 1.5–1.6× crop |
| Super 35 | 24.89 | Most cinema |
| Micro Four Thirds | 17.3 | Mirrorless |
| iPhone 15 Pro | 9.8 | Smartphone reference |

Set with `cam_data.sensor_width = 36`.

## Common pitfalls

| Symptom | Fix |
|---------|-----|
| Distorted face on portrait | Use 50mm+ for human subjects |
| Subject blurred, background sharp | Set `dof.focus_object` to the subject |
| Camera dead-center on subject | Apply rule of thirds; offset subject |
| Orbit camera tilts wildly | Use Track-To constraint, not manual rotation |
| Camera below ground in animation | Add Floor constraint or check Z keyframes |
| DoF very slow in Cycles | Acceptable for finals; viewport may use simpler approximation |

## When to load `references/overview.md`

Load when:
- Cinematic effects beyond defaults: anamorphic, lens flares, vignette
- Multi-camera scenes (camera markers for editing)
- Camera shake / handheld noise
- Stereo / VR camera setup

The reference covers: full focal length theory, aperture/f-stop tables, composition guides, sensor variants for matching real cameras (iPhone, cinema, DSLR), animated camera patterns, cinematic effects.
