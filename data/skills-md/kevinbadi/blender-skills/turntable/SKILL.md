---
name: turntable
description: 360-degree turntable camera orbit around a 3D product. Classic product showcase animation.
---

## Turntable Camera Animation

Orbits the camera 360 degrees around the product for a clean product showcase. Starts front-facing and loops seamlessly.

## When to Use

- User wants a product turntable / spin video
- User says "rotate around", "orbit", "showcase all angles", "turntable"
- Default go-to for product showcase videos

## Prerequisites

- **Blender MCP**: Connected (blender-mcp addon on port 9876)
- **3D model**: Already imported in the Blender scene
- **Output folder**: `~/Desktop/Blender Videos/` (create if needed)
- **ffmpeg**: Installed for video encoding

## Parameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| `duration` | `5` | Video length in seconds |
| `fps` | `24` | Frames per second |
| `camera_distance` | `4.5` | Distance from object center |
| `camera_height` | `2.0` | Camera height above object |
| `camera_lens` | `50` | Focal length in mm |
| `transparent_bg` | `true` | Transparent background |
| `output_format` | `mov` | `mov` (ProRes 4444 w/ alpha) or `webm` (VP9 alpha) |

## Flow

### Step 1: Detect Front Face

Render 4 low-res test frames from different camera positions to find the front of the product. Ask the user which angle is the front.

```python
import bpy, math
from mathutils import Vector

obj = bpy.data.objects['<OBJECT_NAME>']
bbox = [obj.matrix_world @ Vector(c) for c in obj.bound_box]
center = sum(bbox, Vector()) / 8

RADIUS = 4.5
HEIGHT = 2.0

# Create temp camera
bpy.ops.object.camera_add()
cam = bpy.context.active_object
cam.name = 'TempCam'
bpy.context.scene.camera = cam

# Add track constraint to center
bpy.ops.object.empty_add(type='PLAIN_AXES', location=center)
target = bpy.context.active_object
target.name = 'TempTarget'

cam.constraints.new(type='TRACK_TO').target = target

# Render 4 angles
positions = {
    'front': (center.x, center.y - RADIUS, HEIGHT),
    'right': (center.x + RADIUS, center.y, HEIGHT),
    'back': (center.x, center.y + RADIUS, HEIGHT),
    'left': (center.x - RADIUS, center.y, HEIGHT),
}
for label, pos in positions.items():
    cam.location = pos
    bpy.context.scene.render.filepath = f'<OUTPUT>/facing_{label}.png'
    bpy.ops.render.render(write_still=True)
```

Show all 4 images to the user and ask which is the front.

### Step 2: Set Up Camera Rig

```python
import bpy, math

# Create target empty at object center
bpy.ops.object.empty_add(type='PLAIN_AXES', location=(0, 0, 0))
target = bpy.context.active_object
target.name = 'TurntableTarget'

# Create camera at front-facing position (determined from Step 1)
# Default front = -Y axis
bpy.ops.object.camera_add(location=(0, -CAMERA_DISTANCE, CAMERA_HEIGHT))
cam = bpy.context.active_object
cam.name = 'TurntableCamera'
cam.data.lens = 50

# Track to target
track = cam.constraints.new(type='TRACK_TO')
track.target = target
track.track_axis = 'TRACK_NEGATIVE_Z'
track.up_axis = 'UP_Y'

# Parent camera to target for orbit
bpy.ops.object.select_all(action='DESELECT')
cam.select_set(True)
target.select_set(True)
bpy.context.view_layer.objects.active = target
bpy.ops.object.parent_set(type='OBJECT', keep_transform=True)

bpy.context.scene.camera = cam
```

### Step 3: Animate 360 Rotation

```python
import bpy, math

TOTAL_FRAMES = DURATION * FPS  # e.g. 5 * 24 = 120

scene = bpy.context.scene
scene.frame_start = 1
scene.frame_end = TOTAL_FRAMES
scene.render.fps = FPS

target = bpy.data.objects['TurntableTarget']
target.rotation_euler = (0, 0, 0)
target.keyframe_insert(data_path='rotation_euler', frame=1)
target.rotation_euler = (0, 0, math.radians(360))
target.keyframe_insert(data_path='rotation_euler', frame=TOTAL_FRAMES + 1)

# IMPORTANT: Linear interpolation for constant speed
# Blender 5.1 uses layered actions:
action = target.animation_data.action
strip = action.layers[0].strips[0]
for cb in strip.channelbags:
    for fc in cb.fcurves:
        for kp in fc.keyframe_points:
            kp.interpolation = 'LINEAR'
```

### Step 4: Set Up Lighting

```python
import bpy, math

# Warm sunset lighting on LIGHTS only (not on materials/world)
bpy.ops.object.light_add(type='AREA', location=(3, -3, 4))
k = bpy.context.active_object; k.name='GoldenKey'
k.data.energy = 2000; k.data.size = 3.0
k.data.color = (1.0, 0.78, 0.45)
k.rotation_euler = (math.radians(45), 0, math.radians(25))

bpy.ops.object.light_add(type='AREA', location=(-3, -2, 3))
f = bpy.context.active_object; f.name='WarmFill'
f.data.energy = 1000; f.data.size = 5.0
f.data.color = (1.0, 0.75, 0.4)
f.rotation_euler = (math.radians(40), 0, math.radians(-30))

bpy.ops.object.light_add(type='AREA', location=(0, 0, 5))
oh = bpy.context.active_object; oh.name='OverheadWash'
oh.data.energy = 800; oh.data.size = 8.0
oh.data.color = (1.0, 0.92, 0.75)

bpy.ops.object.light_add(type='AREA', location=(0, 4, 2))
r = bpy.context.active_object; r.name='WarmRim'
r.data.energy = 800; r.data.size = 3.0
r.data.color = (1.0, 0.65, 0.3)
r.rotation_euler = (math.radians(-40), 0, math.radians(180))

bpy.ops.object.light_add(type='AREA', location=(4, 0, 0.5))
sw = bpy.context.active_object; sw.name='SideGlow'
sw.data.energy = 600; sw.data.size = 2.0
sw.data.color = (1.0, 0.8, 0.5)
sw.rotation_euler = (math.radians(5), 0, math.radians(90))
```

### Step 5: Render

```python
import bpy, os

scene = bpy.context.scene
scene.render.resolution_x = 1920
scene.render.resolution_y = 1080
scene.render.film_transparent = True
scene.render.engine = 'CYCLES'  # better metallic reflections
scene.cycles.samples = 64
scene.cycles.use_denoising = True
scene.cycles.device = 'GPU'
scene.render.image_settings.file_format = 'PNG'
scene.render.image_settings.color_mode = 'RGBA'

# Neutral world for subtle reflections (not colored)
if not scene.world:
    scene.world = bpy.data.worlds.new("World")
scene.world.use_nodes = True
bg = scene.world.node_tree.nodes.get('Background')
bg.inputs['Color'].default_value = (0.95, 0.95, 0.95, 1)
bg.inputs['Strength'].default_value = 0.3

frames_dir = os.path.expanduser('~/Desktop/Blender Videos/turntable_frames/')
os.makedirs(frames_dir, exist_ok=True)
scene.render.filepath = frames_dir

bpy.ops.render.render(animation=True)
```

### Step 6: Encode Video

MCP will timeout during render. Poll frames directory until all frames exist, then encode:

```bash
# ProRes 4444 with alpha (transparent)
ffmpeg -y -framerate 24 \
  -i "~/Desktop/Blender Videos/turntable_frames/%04d.png" \
  -c:v prores_ks -profile:v 4444 -pix_fmt yuva444p10le \
  "~/Desktop/Blender Videos/turntable.mov"
```

## Blender 5.1 Notes

- Render engine enum: `BLENDER_EEVEE` (not `BLENDER_EEVEE_NEXT`)
- No FFMPEG output format — render PNG sequence + encode with ffmpeg
- Layered actions API: `action.layers[0].strips[0].channelbags` to access fcurves
- `film_transparent = True` for transparent background
- Warm color goes on the LIGHTS, not on the world/materials
