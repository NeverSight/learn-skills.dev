---
name: video-scene-analyzer
description: Analyze video files by detecting scene boundaries and generating structured production metadata as JSON. Use when asked to analyze scenes in a video, detect scene changes, generate scene-level metadata (camera angles, color tone, tempo, transitions, text overlays), catalog visual assets, or produce a structured JSON breakdown of video content. Includes bundled videx script for frame extraction (requires ffmpeg/ffprobe). Outputs analysis.json with per-scene content summaries, production/direction tags, and a cross-scene asset library.
---

# Video Scene Analyzer

Detect scene boundaries in video files and generate structured JSON with content summaries, production tags, and a visual asset library per scene.

## Prerequisites

Requires `ffmpeg` and `ffprobe`. Verify:

```bash
ffmpeg -version && ffprobe -version
```

If missing, inform the user and stop.

This skill bundles its own `videx` script at `scripts/videx` (relative to SKILL.md). Resolve the full path:

```bash
VIDEX="$(dirname "$(realpath "<path-to-SKILL.md>")")/scripts/videx"
```

## Workflow Overview

Two-pass process:

1. **Pass 1 -- Overview**: Extract low-res frames, read them all, identify scene boundaries
2. **Pass 2 -- Deep-dive**: Extract high-res frames per scene, generate detailed metadata
3. **Output**: Write `analysis.json` + conversation summary

## Pass 1: Overview Scan

### Step 1: Get video metadata

```bash
ffprobe -v error -show_entries format=duration,size -show_entries stream=codec_name,width,height,r_frame_rate -of default=noprint_wrappers=1 <video>
```

Record duration, resolution, fps for the output JSON.

### Step 2: Extract overview frames

Choose interval based on duration:

| Duration | Interval | Command |
|----------|----------|---------|
| < 5 min | 2s | `$VIDEX overview <video> 2 320 0.5` |
| 5-30 min | 5s | `$VIDEX overview <video> 5 320 0.5` |
| > 30 min | 10s | `$VIDEX overview <video> 10 320 0.5` |

Use triplet=0.5 (wider spread) to make transitions visible.

### Step 3: Read all overview frames

Read every `_b` (center) frame chronologically using the Read tool. Read in batches of 20-30 if many frames.

For timestamps where the `_b` frame looks like a transition (blur, blend, fade), also read the `_a` and `_c` frames.

### Step 4: Detect scene boundaries

Compare consecutive `_b` frames. A **scene boundary** exists when:

- **Hard cut**: Completely different content between consecutive frames
- **Dissolve/fade**: Frame shows blending or fade to/from black/white
- **Major change**: Same subject but clearly different setting, angle, or composition

Heuristic: **when uncertain, prefer splitting**. Users can merge; they cannot split what was missed.

Record for each boundary:
- Approximate timestamp (midpoint between the two sample points)
- Transition type (cut, dissolve, fade-to-black, fade-from-black, fade-to-white, fade-from-white, wipe)

The first frame always starts Scene 1. The last sample point ends the final scene (use video duration).

### Step 5: Report scene list

Show the user a scene list before proceeding:

```
Scene 1: 0:00 - 0:04 (cut)
Scene 2: 0:04 - 0:07 (dissolve)
...
```

Ask if they want to adjust boundaries or proceed.

## Pass 2: Scene Deep-Dive

### Step 6: Extract scene frames

For each scene, extract at 1280px:

```bash
$VIDEX range <video> <start>-<end> --triplet=0.2
```

Short scenes (< 2s): add `--fps=5`
Long scenes (> 30s): default 2fps is fine.

### Step 7: Analyze each scene

Read all extracted frames for the scene. Determine:

**Content summary**: 2-4 sentences. Subjects, actions, setting, props, visible text.

**Production tags**:

| Tag | Values |
|-----|--------|
| `camera_angle` | eye-level, low-angle, high-angle, bird's-eye, dutch-angle, over-the-shoulder, pov |
| `shot_size` | extreme-wide, wide, medium-wide, medium, medium-close-up, close-up, extreme-close-up |
| `camera_movement` | static, pan-left, pan-right, tilt-up, tilt-down, zoom-in, zoom-out, dolly-in, dolly-out, tracking, handheld, crane, steadicam |
| `color_tone` | warm, cool, neutral, desaturated, high-contrast, low-contrast, monochrome, neon, pastel, earth-tones |
| `lighting` | natural, artificial, high-key, low-key, backlit, side-lit, top-lit, silhouette, mixed |
| `tempo` | static, slow, moderate, fast, frenetic |

**Text overlay**:
- `placement`: none, lower-third, centered, top, full-screen, watermark
- `content`: actual text visible, or null

**Transitions**:
- `in`: how scene begins (none for first scene)
- `out`: how scene ends (none for last scene)

If a tag changes mid-scene, use the dominant value and note the change in `notes`.

### Step 7b: Build asset library

While analyzing scenes, catalog every distinct visual asset across the entire video. For each asset, record:

| Field | Description |
|-------|-------------|
| `id` | Kebab-case unique identifier (e.g., `student-summer`, `logo-brand`) |
| `type` | `character`, `background`, `icon`, `ui-screen`, `photo`, `product`, `logo`, `decoration`, `text-graphic`, `effect` |
| `label` | Human-readable one-line description with key visual traits |
| `style` | `anime-illustration`, `flat-design`, `realistic-photo`, `3d-render`, `hand-drawn`, `typography`, `mixed` |
| `appears_in` | Array of scene numbers where this asset appears |

Guidelines:
- Characters with costume changes get separate entries (e.g., `student-summer`, `student-winter`)
- Same icon in multiple scenes = one entry with all scene numbers
- Only list distinctive backgrounds (skip generic white/black)
- `label` should be concise but include enough detail to identify the asset (color, pose, size, distinguishing features)

See `references/schema.md` for the full type reference and examples.

### Step 8: Write analysis.json

Assemble the complete JSON per the schema in `references/schema.md`.

Write to: `./videx-out/<video-name>/analysis.json`

### Step 9: Conversation summary

After writing JSON, provide:

1. Total scenes and video duration
2. One-line summary per scene with timestamps
3. Asset library summary (total count, type breakdown)
4. Notable production patterns across the video

## Edge Cases

- **< 10 seconds**: Use 1-second interval. Single scene is valid.
- **> 1 hour**: Use 10-second intervals. Read overview frames in batches.
- **Static content (slideshow/screencast)**: Slide changes = scene boundaries. Note `camera_movement: static`.
- **Ambiguous boundaries**: Prefer splitting over merging.

## Output Location

```
./videx-out/<video-name>/
├── overview/          (Pass 1)
├── range_*/           (Pass 2)
└── analysis.json      (final output)
```
