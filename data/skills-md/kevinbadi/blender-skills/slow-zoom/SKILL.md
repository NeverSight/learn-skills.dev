---
name: slow-zoom
description: Cinematic slow push-in zoom toward a hero detail on the product. Creates a reveal effect.
---

## Slow Zoom Camera Animation

Camera slowly pushes in from a wide establishing shot to a tight close-up on a hero detail (logo, texture, feature). Includes subtle dolly zoom (focal length shift) for cinematic compression.

## When to Use

- User wants a "reveal" or "hero shot"
- User says "zoom in", "push in", "close-up on the logo", "cinematic reveal"
- Highlighting a specific detail or feature on the product

## Prerequisites

- **Blender MCP**: Connected
- **3D model**: Already imported in the Blender scene
- **Output folder**: `~/Desktop/Blender Videos/`
- **ffmpeg**: Installed

## Parameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| `duration` | `5` | Video length in seconds |
| `fps` | `24` | Frames per second |
| `start_distance` | `4.0` | Starting camera distance |
| `end_distance` | `1.8` | Ending camera distance (close-up) |
| `start_height` | `3.0` | Starting camera height |
| `end_height` | `1.2` | Ending camera height |
| `start_lens` | `35` | Starting focal length (wide) |
| `end_lens` | `65` | Ending focal length (tight) |
| `focus_point` | `(0,0,0.1)` | Point to zoom toward (e.g. logo center) |
| `transparent_bg` | `true` | Transparent background |

## Flow

### Step 1: Identify Focus Point

Ask user what detail to zoom into, or default to object center. Use `AskUserQuestion` if unclear.

### Step 2: Set Up Camera

```python
import bpy, math

# Focus target
bpy.ops.object.empty_add(type='PLAIN_AXES', location=FOCUS_POINT)
tgt = bpy.context.active_object
tgt.name = 'ZoomTarget'

# Camera
bpy.ops.object.camera_add(location=(START_X, -START_DISTANCE, START_HEIGHT))
cam = bpy.context.active_object
cam.name = 'SlowZoomCam'
cam.data.lens = START_LENS

track = cam.constraints.new(type='TRACK_TO')
track.target = tgt
track.track_axis = 'TRACK_NEGATIVE_Z'
track.up_axis = 'UP_Y'

bpy.context.scene.camera = cam
```

### Step 3: Animate Push-In

```python
import bpy

TOTAL_FRAMES = DURATION * FPS
scene = bpy.context.scene
scene.frame_start = 1
scene.frame_end = TOTAL_FRAMES
scene.render.fps = FPS

# Start wide
cam.location = (1.5, -START_DISTANCE, START_HEIGHT)
cam.keyframe_insert(data_path='location', frame=1)
cam.data.lens = START_LENS
cam.data.keyframe_insert(data_path='lens', frame=1)

# End tight
cam.location = (0.3, -END_DISTANCE, END_HEIGHT)
cam.keyframe_insert(data_path='location', frame=TOTAL_FRAMES)
cam.data.lens = END_LENS
cam.data.keyframe_insert(data_path='lens', frame=TOTAL_FRAMES)

# Keep default BEZIER interpolation for smooth ease in/out
```

### Step 4: Lighting + Render

Use the same golden hour lighting setup as turntable skill. Render as PNG sequence with Cycles, encode with ffmpeg to ProRes 4444.

```bash
ffmpeg -y -framerate 24 \
  -i "~/Desktop/Blender Videos/slowzoom_frames/%04d.png" \
  -c:v prores_ks -profile:v 4444 -pix_fmt yuva444p10le \
  "~/Desktop/Blender Videos/slow_zoom.mov"
```

## Tips

- The focal length shift (35mm to 65mm) creates a subtle dolly zoom / Hitchcock effect
- BEZIER interpolation gives smooth ease-in/out — don't use LINEAR for this animation
- Offset the start position slightly on X (e.g. 1.5) for a more cinematic diagonal approach
