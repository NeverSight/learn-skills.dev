---
name: iopho-analyzing-videos
description: Reverse-engineer videos into .storyboard.md files for AI video regeneration
allowed-tools: Bash(python3 *), Bash(ffmpeg *), Bash(pip *)
user-invocable: true
argument-hint: <video_path> [output_path] [--no-frames] [--model gemini-2.0-flash]
---

# iopho-analyzing-videos — Video → .storyboard.md Reverse Engineering

Analyze a video file and generate a detailed `.storyboard.md` file — a human+AI readable "source code" representation of the video, including scene-by-scene breakdowns, visual descriptions, audio transcripts, and extracted keyframes.

## Prerequisites

!`python3 -c "import google.generativeai; print('google-generativeai: ✓')" 2>/dev/null || echo "google-generativeai: ✗ — install: pip install google-generativeai"`

!`which ffmpeg 2>/dev/null && echo "ffmpeg: ✓ (needed for frame extraction)" || echo "ffmpeg: ✗ — install: brew install ffmpeg"`

!`echo "GEMINI_API_KEY: $([ -n \"$GEMINI_API_KEY\" ] && echo '✓ set' || echo '✗ — set via: export GEMINI_API_KEY=your-key')"`

**Required**: `google-generativeai` + `ffmpeg` + `GEMINI_API_KEY` environment variable.

Get a Gemini API key at https://aistudio.google.com/apikey (free tier available).

## What It Produces

Given a video file, this skill generates:

```
output.storyboard.md    ← YAML frontmatter + scene-by-scene markdown
frames/
  scene-001.jpg         ← Keyframe at midpoint of scene 1
  scene-002.jpg         ← Keyframe at midpoint of scene 2
  ...
```

### .storyboard.md Format

```yaml
---
title: "Video Title"
duration_seconds: 19
resolution: "1920x1080"
style:
  visual_style: "clean, modern, minimalist"
  color_palette: ["#E6E6FA", "#9400D3", "#00BFFF"]
audio:
  has_voiceover: true
  voiceover_language: "en"
content:
  type: "product_demo"
  framework: "PAS"
  key_message: "..."
---

### Scene 1: Hook (0:00 – 0:02, 2s)
**Thumbnail**: ![scene-001](./frames/scene-001.jpg)

#### Visual
- **Shot Type**: wide
- **Camera Movement**: static
- **Subject**: ...
- **Text On Screen**: "..."

#### Audio
- **Voiceover**: "exact transcript"
- **Music**: upbeat, electronic

#### Analysis
- **Narrative Purpose**: ...
- **Sales Element**: problem
- **Transition Out**: cut to →
```

Each scene includes: Visual (shot type, camera, subject, text, graphics), Audio (voiceover, music, SFX), and Analysis (narrative purpose, viewer psychology, sales element).

## Quick Reference

**Analyze a local video**:
```bash
python3 scripts/video_to_storyboard.py "$VIDEO_PATH" "$OUTPUT_PATH"
```

**Analyze without frame extraction**:
```bash
python3 scripts/video_to_storyboard.py "$VIDEO_PATH" "$OUTPUT_PATH" --no-frames
```

**Use a different Gemini model**:
```bash
GEMINI_MODEL=gemini-2.5-flash python3 scripts/video_to_storyboard.py "$VIDEO_PATH"
```

## Execute

Run the analysis pipeline:

```bash
# From $ARGUMENTS: <video_path> [output_path] [--no-frames] [--model MODEL]
#
# Default output: same directory as video, with .storyboard.md extension
# Default model: gemini-2.0-flash
#
# The agent should:
# 1. Verify video file exists
# 2. Check GEMINI_API_KEY is set
# 3. Run the analysis script
# 4. Report: output path, scene count, frame count, token usage

python3 scripts/video_to_storyboard.py "$VIDEO_PATH" "$OUTPUT_PATH"
```

## Pipeline Details

The analysis pipeline works in 4 stages:

```
Stage 1: Upload
  Video file → Gemini File API (supports up to ~1GB)
  Wait for server-side processing

Stage 2: Analyze
  Gemini Flash processes video natively (no frame extraction needed)
  Generates complete .storyboard.md with scene timestamps
  ~$0.001 per short video (< 30s)

Stage 3: Extract Frames
  Parse scene timestamps from generated markdown
  ffmpeg screenshots at each scene midpoint
  Insert thumbnail references into markdown

Stage 4: Output
  Write .storyboard.md file
  Write frames/ directory with keyframe JPGs
  Clean up uploaded file from Gemini
```

## Script Setup

If the analysis script doesn't exist yet, create it:

```bash
# Check if script exists
ls scripts/video_to_storyboard.py 2>/dev/null || echo "Script not found — see references/video_to_storyboard.py for the full implementation"
```

The script requires these Python packages:
```bash
pip install google-generativeai
```

## Cost Estimates

| Video Length | Gemini Flash Cost | Notes |
|-------------|------------------|-------|
| < 30s | ~$0.001 | Short ads, demos |
| 1-5 min | ~$0.01 | Explainers, tutorials |
| 5-15 min | ~$0.03 | Long-form content |
| 15-60 min | ~$0.06-0.15 | Full presentations |

Costs based on Gemini 2.0 Flash pricing. Gemini 2.5 Flash may differ.

## Combine with Other iopho Skills

**Full pipeline — search, download, analyze**:
```
/iopho-searching-videos SaaS explainer under 30s --limit 5
/iopho-getting-videos https://youtube.com/watch?v=BEST_MATCH --mode all --output temp/
/iopho-analyzing-videos temp/video.mp4 temp/output.storyboard.md
```

**Analyze + regenerate with Remotion**:
After generating `.storyboard.md`, use it as a blueprint to recreate the video with Remotion or other video generation tools.

## Tips

- Gemini Flash processes video natively — no need to pre-extract frames
- The `.info.json` from iopho-getting-videos is auto-detected for source URL and title
- Short videos (< 30s) produce the most accurate scene detection
- For longer videos, consider splitting first with `ffmpeg -ss START -to END`
- The generated `.storyboard.md` is both human-readable and machine-parseable
- Use `--no-frames` for faster processing when you don't need keyframe images
