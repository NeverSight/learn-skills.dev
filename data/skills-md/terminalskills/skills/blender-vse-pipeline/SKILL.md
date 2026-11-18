---
name: blender-vse-pipeline
description: >-
  Automate video editing in Blender's Video Sequence Editor with Python. Use
  when the user wants to add video, image, or audio strips, create transitions,
  apply effects, build edit timelines, batch assemble footage, estimate render
  times, or script any VSE workflow from the command line.
license: Apache-2.0
compatibility: >-
  Requires Blender 5.0+ (strips API; 4.x used scene.sequence_editor.sequences).
  FFmpeg codecs included with Blender. Run: blender --background --python script.py
metadata:
  author: terminal-skills
  version: "1.2.0"
  category: automation
  tags: "blender, video-editing, vse, timeline, pipeline"
  repository: https://projects.blender.org/blender/blender
---

# Blender VSE Pipeline

## Overview

Automate video editing with Blender's Video Sequence Editor (VSE) using Python. Add and arrange strips (video, image, audio), create transitions, apply effects, assemble edits from file lists, and render final video — all headlessly from the terminal. Run on Blender 5.0.1 and checked against the 5.1 release notes and the current (5.2) Python API reference.

Blender 5.0 renamed the VSE API: `Sequence` became `Strip`, `scene.sequence_editor.sequences` became `.strips`, `sequences_all` became `.strips_all`, and `new_effect` takes `length`, `input1`, `input2` instead of `frame_end`, `seq1`, `seq2`. The `TRANSFORM` effect strip is gone; every image or movie strip now has `strip.transform` and `strip.crop`.

The strip timing properties were renamed a second time in Blender 5.1. This skill uses the 5.0 names because they exist in every 5.x release; the 5.1+ names raise `AttributeError` on 5.0.x (verified on 5.0.1).

| Meaning | 5.0 and later (used here) | 5.1 and later only |
|---|---|---|
| first timeline frame | `frame_final_start` | `left_handle` |
| end frame | `frame_final_end` | `right_handle` |
| length on the timeline | `frame_final_duration` | `duration` |
| trim from start / end | `frame_offset_start` / `frame_offset_end` | `left_handle_offset` / `right_handle_offset` |
| frame where the source begins | `frame_start` | `content_start` |

The 5.0 names are deprecated from 5.1 and planned for removal in 6.0 (5.1 Python API release notes). For a script that must run on 5.0 and on 6.0, pick the name at run time, for example `getattr(s, "left_handle", None)` with a fallback to `s.frame_final_start`.

## Instructions

### 1. Initialize the sequence editor

```python
import bpy

scene = bpy.context.scene
if not scene.sequence_editor:
    scene.sequence_editor_create()
strips = scene.sequence_editor.strips
scene.frame_start = 1
scene.frame_end = 250
scene.render.fps = 24
```

### 2. Add strips

```python
# Video strip
clip_a = strips.new_movie(name="Clip_A", filepath="/srv/footage/interview_cam_a.mp4", channel=1, frame_start=1)
clip_a.frame_offset_start = 24   # trim start (skip 1 sec at 24 fps)
clip_a.frame_offset_end = 48     # trim end

# Second clip on another channel, overlapping the end of Clip_A (used by the transitions below)
clip_b = strips.new_movie(name="Clip_B", filepath="/srv/footage/interview_cam_b.mp4", channel=2,
                          frame_start=clip_a.frame_final_end - 24)

# Image strip (hold for duration)
img = strips.new_image(name="Title_Card", filepath="/srv/footage/title_card.png", channel=2, frame_start=1, fit_method='FIT')
img.frame_final_duration = 72  # 3 seconds at 24fps

# Image sequence
import glob
img_files = sorted(glob.glob("/srv/renders/shot_010/frame_*.png"))
img_seq = strips.new_image(name="Render", filepath=img_files[0], channel=1, frame_start=1)
for f in img_files[1:]:
    img_seq.elements.append(f.split("/")[-1])

# Audio strip with fade in/out
audio = strips.new_sound(name="Music", filepath="/srv/audio/theme_music.mp3", channel=3, frame_start=1)
audio.volume = 0.0
audio.keyframe_insert(data_path="volume", frame=1)
audio.volume = 0.6
audio.keyframe_insert(data_path="volume", frame=24)
audio.volume = 0.6
audio.keyframe_insert(data_path="volume", frame=audio.frame_final_end - 48)
audio.volume = 0.0
audio.keyframe_insert(data_path="volume", frame=audio.frame_final_end)
```

### 3. Transitions and effects

```python
# Cross dissolve (strips must overlap and be on different channels)
cross = strips.new_effect(
    name="CrossDissolve", type='GAMMA_CROSS', channel=3,
    frame_start=clip_b.frame_final_start, length=24,
    input1=clip_a, input2=clip_b
)

# Color strip (solid background)
color = strips.new_effect(name="BlackBG", type='COLOR', channel=1, frame_start=1, length=48)
color.color = (0, 0, 0)

# Text overlay
text = strips.new_effect(name="Title", type='TEXT', channel=4, frame_start=1, length=72)
text.text = "Harbor Cities, Episode 3"
text.font_size = 80
text.color = (1, 1, 1, 1)
text.location = (0.5, 0.5)       # relative position in the frame
text.anchor_x = 'CENTER'         # text box anchor relative to location
text.anchor_y = 'CENTER'
text.alignment_x = 'CENTER'      # alignment of lines inside the box
text.use_shadow = True

# Speed control
speed = strips.new_effect(name="SlowMo", type='SPEED', channel=5,
    frame_start=clip_a.frame_final_start, length=clip_a.frame_final_duration, input1=clip_a)
speed.speed_control = 'MULTIPLY'     # default STRETCH fits the input to the strip length
speed.speed_factor = 0.5

# Transform (position, scale, rotation) is a property of image/movie strips
clip_a.transform.scale_x = 1.2
clip_a.transform.scale_y = 1.2
clip_a.transform.offset_x = 40       # pixels
clip_a.crop.min_x = 20               # crop left edge by 20 px
```

### 4. Render the final video

```python
scene = bpy.context.scene
scene.render.filepath = "/tmp/final_edit.mp4"
scene.render.image_settings.media_type = 'VIDEO'   # Blender 5.0+: choose the media type first, or 'FFMPEG' is not a valid file_format
scene.render.image_settings.file_format = 'FFMPEG'
scene.render.ffmpeg.format = 'MPEG4'
scene.render.ffmpeg.codec = 'H264'
scene.render.ffmpeg.audio_codec = 'AAC'
scene.render.ffmpeg.audio_bitrate = 192
scene.render.resolution_x = 1920
scene.render.resolution_y = 1080

# Auto-set frame range from strips
all_strips = scene.sequence_editor.strips_all
if all_strips:
    scene.frame_start = min(s.frame_final_start for s in all_strips)
    scene.frame_end = max(s.frame_final_end for s in all_strips)

bpy.ops.render.render(animation=True)
```

## Examples

### Example 1: Assemble an edit from a shot list

**User request:** "Build a timeline from video clips with crossfades between them"

```python
import bpy, os

clips = ["/srv/footage/shot_01.mp4", "/srv/footage/shot_02.mp4", "/srv/footage/shot_03.mp4", "/srv/footage/shot_04.mp4"]
crossfade_frames = 12

scene = bpy.context.scene
scene.render.fps = 24
if not scene.sequence_editor:
    scene.sequence_editor_create()
strips = scene.sequence_editor.strips
current_frame = 1
prev_strip = None

for i, clip_path in enumerate(clips):
    if prev_strip and crossfade_frames > 0:
        current_frame -= crossfade_frames
    strip = strips.new_movie(
        name=os.path.splitext(os.path.basename(clip_path))[0],
        filepath=clip_path, channel=1 + (i % 2), frame_start=current_frame
    )
    if prev_strip and crossfade_frames > 0:
        strips.new_effect(name=f"Fade_{i}", type='GAMMA_CROSS', channel=3,
            frame_start=current_frame, length=crossfade_frames,
            input1=prev_strip, input2=strip)
    current_frame += strip.frame_final_duration
    prev_strip = strip

scene.frame_start = 1
scene.frame_end = current_frame
```

### Example 2: Batch add text overlays from data

**User request:** "Add text titles at specific timecodes"

```python
import bpy

titles = [("Introduction", 0, 3), ("Chapter 1", 15, 4), ("Chapter 2", 120, 4), ("Conclusion", 300, 5)]
scene = bpy.context.scene
fps = scene.render.fps
if not scene.sequence_editor:
    scene.sequence_editor_create()
strips = scene.sequence_editor.strips

for text_content, start_sec, dur_sec in titles:
    start_frame = int(start_sec * fps) + 1
    text = strips.new_effect(name=text_content[:20], type='TEXT', channel=5,
        frame_start=start_frame, length=int(dur_sec * fps))
    text.text = text_content
    text.font_size = 60
    text.color = (1, 1, 1, 1)
    text.location = (0.5, 0.15)
    text.anchor_x = 'CENTER'
    text.alignment_x = 'CENTER'
    text.use_shadow = True
```

## Guidelines

- Always call `scene.sequence_editor_create()` if `scene.sequence_editor` is `None`.
- Use `strips.new_movie()`, `new_image()`, `new_sound()`, `new_effect()`. Avoid `bpy.ops.sequencer.*` in background mode.
- Cross dissolves need strips on different channels with overlapping frames. Alternate channels (1, 2, 1, 2).
- `frame_offset_start` / `frame_offset_end` trim content without moving the strip; `frame_final_start` is where the strip starts on the timeline. From Blender 5.1 these are deprecated aliases of `left_handle_offset` / `right_handle_offset` and `left_handle` (see the table in the Overview).
- For audio fades, keyframe `strip.volume` — no built-in fade effect in VSE.
- Do not script strip modifiers (`strip.modifiers.new(...)`, e.g. `BRIGHT_CONTRAST`, `COLOR_BALANCE`): on Blender 5.0.1 it crashes Blender in `--background` mode for every modifier type and strip type (verified), so grade footage in the compositor or in the editor UI instead.
- Render long edits as image sequences first, then assemble with ffmpeg.
- Set resolution to match source footage to avoid scaling artifacts, or pass `fit_method` (`FIT`, `FILL`, `STRETCH`, `ORIGINAL`) when adding image and movie strips.
- The container default of `scene.render.ffmpeg.format` is MKV; set `MPEG4` explicitly for `.mp4` output. `ffmpeg.constant_rate_factor` controls quality.
- VSE processes channels bottom-to-top — higher channels layer on top.
