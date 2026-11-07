---
name: crane-shot
description: Camera starts low and rises up to reveal the full product. Great for dramatic product reveals on a pedestal.
---

## Crane Shot Camera Animation

Camera begins at a low angle looking up at the product, then smoothly rises to reveal the full product from above. Creates a dramatic unveiling effect.

## When to Use

- User wants a "reveal" or "unveil" shot
- User says "crane", "rise up", "low to high", "dramatic reveal"
- Product on a pedestal or platform

## Parameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| `duration` | `5` | Video length in seconds |
| `fps` | `24` | Frames per second |
| `start_height` | `-0.2` | Starting height (below product level) |
| `end_height` | `3.5` | Ending height (above product) |
| `start_distance` | `3.0` | Starting distance |
| `end_distance` | `4.0` | Ending distance (pulls back as it rises) |

## Flow

### Step 1: Set Up Camera

```python
import bpy, math

bpy.ops.object.empty_add(type='PLAIN_AXES', location=(0, 0, 0.05))
tgt = bpy.context.active_object
tgt.name = 'CraneTarget'

bpy.ops.object.camera_add(location=(1.0, -START_DISTANCE, START_HEIGHT))
cam = bpy.context.active_object
cam.name = 'CraneCam'
cam.data.lens = 45

trk = cam.constraints.new(type='TRACK_TO')
trk.target = tgt
trk.track_axis = 'TRACK_NEGATIVE_Z'
trk.up_axis = 'UP_Y'

bpy.context.scene.camera = cam
```

### Step 2: Animate Crane Movement

```python
TOTAL_FRAMES = DURATION * FPS

scene = bpy.context.scene
scene.frame_start = 1
scene.frame_end = TOTAL_FRAMES
scene.render.fps = FPS

# Start low
cam.location = (1.0, -START_DISTANCE, START_HEIGHT)
cam.keyframe_insert(data_path='location', frame=1)
cam.data.lens = 45
cam.data.keyframe_insert(data_path='lens', frame=1)

# Rise up and pull back
cam.location = (1.5, -END_DISTANCE, END_HEIGHT)
cam.keyframe_insert(data_path='location', frame=TOTAL_FRAMES)
cam.data.lens = 35
cam.data.keyframe_insert(data_path='lens', frame=TOTAL_FRAMES)

# BEZIER for smooth crane motion
```

### Step 3: Render + Encode

Same pipeline — Cycles, PNG sequence, ffmpeg ProRes 4444.

```bash
ffmpeg -y -framerate 24 \
  -i "~/Desktop/Blender Videos/crane_frames/%04d.png" \
  -c:v prores_ks -profile:v 4444 -pix_fmt yuva444p10le \
  "~/Desktop/Blender Videos/crane_shot.mov"
```
