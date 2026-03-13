---
name: pan-3d-transition
description: Create 3D pan/swivel transition effects for videos using Remotion. Use when user asks to add 3D transitions, create swivel effects, or add video transitions.
---

# 3D Pan Transition

## Goal
Create 3D rotating "swivel" transition effects for videos using Remotion rendering.

## Scripts
- `./scripts/insert_3d_transition.py` - Insert transition into video

## Usage

```bash
python3 ./scripts/insert_3d_transition.py input.mp4 output.mp4 \
  --insert-at 3 \
  --duration 5 \
  --teaser-start 60 \
  --bg-image .tmp/bg.png
```

## Parameters
| Argument | Default | Description |
|----------|---------|-------------|
| `--insert-at` | 3 | Where to insert (seconds) |
| `--duration` | 5 | Transition duration |
| `--teaser-start` | 60 | Where to sample content from |
| `--bg-image` | none | Background image |

## How It Works
1. Extracts frames from later in video
2. Creates 3D rotating animation via Remotion
3. Splits video: intro, transition, main
4. Concatenates with audio preserved

## Dependencies
```bash
cd video_effects && npm install
```

## Output
Video with swivel teaser inserted at specified position.

---

## Schema

### Inputs
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `input_video` | file_path | Yes | Input video file |
| `insert_at` | integer | No | Where to insert teaser (seconds, default: 3) |
| `duration` | integer | No | Transition duration (seconds, default: 5) |
| `teaser_start` | integer | No | Where to sample content from (seconds, default: 60) |
| `bg_image` | file_path | No | Background image path |

### Outputs
| Name | Type | Description |
|------|------|-------------|
| `output_video` | file_path | Video with 3D transition inserted |

### Composable With
Skills that chain well with this one: `video-edit`

### Cost
Free locally (Remotion + FFmpeg)
