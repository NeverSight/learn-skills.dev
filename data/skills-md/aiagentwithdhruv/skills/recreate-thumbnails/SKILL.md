---
name: recreate-thumbnails
description: Face-swap YouTube thumbnails to feature Your Name using AI. Use when user asks to recreate thumbnails, face swap images, generate YouTube thumbnails, or create thumbnail variations.
---

# Recreate YouTube Thumbnails

## Goal
Face-swap YouTube thumbnails to feature Your Name using Gemini image model. The system analyzes face direction, matches reference photos by pose, and generates variations.

## Scripts
- `./scripts/recreate_thumbnails.py` - Main generation script
- `./scripts/analyze_face_directions.py` - Reference photo analyzer

## Quick Start

```bash
# From YouTube video (auto-downloads thumbnail)
python3 ./scripts/recreate_thumbnails.py --youtube "https://youtube.com/watch?v=VIDEO_ID"

# From local thumbnail
python3 ./scripts/recreate_thumbnails.py --source ".tmp/thumbnails/source.jpg"

# Edit pass on generated thumbnail
python3 ./scripts/recreate_thumbnails.py --edit ".tmp/thumbnails/recreated_v3.png" \
  --prompt "Change colors to teal. Change 'AI GOLD RUSH' to 'AGENTIC FLOWS'."
```

## Full Workflow

### Step 1: Build Reference Photo Bank (One-time)

```bash
# Drop 30-40 photos of Nick into raw folder
mkdir -p .tmp/reference_photos/raw

# Analyze and rename with face direction metadata
python3 ./scripts/analyze_face_directions.py
```

Creates files like:
- `nick_yawL30_pitchU10.jpg` — looking 30° left, 10° up
- `nick_yawR45_pitch0.jpg` — looking 45° right, level

### Step 2: Generate Thumbnails

```bash
# From YouTube URL (analyzes face, finds best reference, generates 3 variations)
python3 ./scripts/recreate_thumbnails.py --youtube "VIDEO_URL"

# Custom variation count
python3 ./scripts/recreate_thumbnails.py --source "thumbnail.jpg" -n 5

# Skip direction matching
python3 ./scripts/recreate_thumbnails.py --source "thumbnail.jpg" --no-match
```

### Step 3: Edit & Refine

```bash
# Single edit
python3 ./scripts/recreate_thumbnails.py --edit ".tmp/thumbnails/recreated_v3.png" \
  --prompt "Change colors to teal brand colors."

# Chain multiple edits
python3 ./scripts/recreate_thumbnails.py --edit ".tmp/thumbnails/edited_1.png" \
  --prompt "Make text bigger. Change background to white."
```

## CLI Reference

| Flag | Description |
|------|-------------|
| `--youtube`, `-y` | YouTube video URL |
| `--source`, `-s` | Source thumbnail path or URL |
| `--edit`, `-e` | Image to edit (enables edit mode) |
| `--prompt`, `-p` | Edit instructions (required for edit mode) |
| `--variations`, `-n` | Number of variations (default: 3) |
| `--refs` | Number of reference photos (default: 2) |
| `--no-match` | Skip face direction matching |

## Output Organization

```
.tmp/thumbnails/
├── 20251205/              # Date folder
│   ├── 104016_1.png       # Variation 1
│   ├── 104016_2.png       # Variation 2
│   ├── 104016_3.png       # Variation 3
│   └── 104532_edited.png  # Edit pass
```

## API Details
- **Model:** `gemini-3-pro-image-preview` (Nano Banana Pro)
- **Cost:** ~$0.14-0.24 per generation/edit
- **Latency:** 10-60+ seconds per image
- **Output:** ~1376x768 (close to 16:9)

## Learnings

- 2 reference photos is optimal (1 loses likeness, 3+ causes regeneration)
- Must explicitly request 16:9 format in prompt
- Label images in prompt: "IMAGE 1: Reference, IMAGE 2: Thumbnail"
- "100% exact duplicate except face" instruction works well
- Edit passes work for text, colors, graphs, backgrounds

## Environment
```
NANO_BANANA_API_KEY=your_key
```

---

## Schema

### Inputs
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `youtube_url` | string | No | YouTube video URL (auto-downloads thumbnail) |
| `source` | file_path | No | Source thumbnail image path |
| `variations` | integer | No | Number of variations (default: 3) |
| `edit_image` | file_path | No | Image to edit (enables edit mode) |
| `prompt` | string | No | Edit instructions for edit mode |

### Outputs
| Name | Type | Description |
|------|------|-------------|
| `thumbnails` | array | Generated thumbnail file paths in .tmp/thumbnails/ |

### Credentials
| Name | Source |
|------|--------|
| `NANO_BANANA_API_KEY` | .env |

### Composable With
Skills that chain well with this one: `cross-niche-outliers`, `youtube-outliers`

### Cost
$0.14-0.24 per generation
