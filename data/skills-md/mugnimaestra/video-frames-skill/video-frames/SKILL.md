---
name: video-frames
description: Extract frames from video files using ffmpeg for AI/LLM analysis. Use when (1) the user asks to analyze, describe, or summarize a video file, (2) the user wants to extract frames or screenshots from a video, (3) the user provides a video file (.mp4, .mov, .avi, .mkv, .webm, etc.) and asks questions about its visual content, (4) the user wants to identify scenes, objects, or events in a video, (5) the user wants timestamps overlaid on extracted frames for temporal reference. Converts video into JPEG frames that can be attached to LLM prompts as images. Requires ffmpeg on PATH. Supports scene-change detection, model-aware optimization (Claude/OpenAI/Gemini), quality presets (efficient/balanced/detailed/ocr), grayscale and high-contrast OCR mode, and automatic FPS calculation via --max-frames.
---

# Video Frames

Extract frames from video files using ffmpeg, producing JPEG images optimized for LLM vision analysis. Supports multiple frame-selection strategies (fixed FPS, scene detection, target frame count), quality presets, model-aware dimension optimization, and OCR enhancements.

## Prerequisites

ffmpeg and ffprobe must be installed and on PATH:

```bash
brew install ffmpeg  # macOS
```

## Workflow

1. Receive a video file path from the user
2. Run `scripts/extract_frames.py` to extract JPEG frames
3. Parse the JSON output for frame paths, resolution, and token estimates
4. Read the extracted frames as image attachments for analysis
5. Answer the user's question about the video content
6. Clean up temp directories when done

## Quick Start

The simplest invocation -- extracts 1 frame/second at balanced quality:

```bash
python3 scripts/extract_frames.py video.mp4
```

For most use cases, use `--max-frames` to let the script auto-calculate FPS:

```bash
python3 scripts/extract_frames.py video.mp4 --max-frames 30
```

This is the **preferred approach** over manually setting `--fps`, since it adapts to any video length and keeps the frame count predictable.

## Presets

Four quality presets control resolution, JPEG quality, and image processing:

| Preset      | Max dim | Quality | Extras                              | Best for                   |
| ----------- | ------- | ------- | ----------------------------------- | -------------------------- |
| `efficient` | 768px   | 5       | --                                  | Bulk frames, long videos   |
| `balanced`  | 1024px  | 3       | --                                  | General analysis (default) |
| `detailed`  | 1568px  | 2       | --                                  | Fine detail, small objects |
| `ocr`       | 1568px  | 1       | grayscale + high contrast + sharpen | Text/document extraction   |

```bash
# Long video, keep costs low
python3 scripts/extract_frames.py long_video.mp4 --max-frames 20 --preset efficient

# Need to read text in a screencast
python3 scripts/extract_frames.py screencast.mp4 --max-frames 40 --preset ocr
```

Quality (1=best, 31=worst) and max dimension can be overridden independently:

```bash
python3 scripts/extract_frames.py video.mp4 --preset balanced --quality 1 --max-dimension 1568
```

## Scene-Change Detection

Instead of extracting at a fixed rate, detect visual scene changes and extract one frame per scene. This is ideal for videos with distinct segments (presentations, edited footage, tutorials).

```bash
python3 scripts/extract_frames.py video.mp4 --scene-threshold 0.3
```

- `--scene-threshold` (float, 0.0-1.0): Sensitivity. Lower = more sensitive, detects smaller changes. Start with `0.3` (the default when the flag is used).
- `--min-scene-interval` (float, default: 1.0): Minimum seconds between detected scenes. Prevents burst detections during rapid cuts.

**Note:** `--fps` and `--scene-threshold` are mutually exclusive. `--max-frames` can only be used with `--fps` mode, not scene detection.

```bash
# Presentation with clear slide transitions
python3 scripts/extract_frames.py presentation.mp4 --scene-threshold 0.2

# Action footage -- less sensitive, min 2s apart
python3 scripts/extract_frames.py action.mp4 --scene-threshold 0.5 --min-scene-interval 2.0
```

## Model-Aware Optimization

Use `--target-model` to resize frames to dimensions that align with a specific model's tile boundaries, minimizing wasted tokens:

| Model       | Max dim | Rationale                                      |
| ----------- | ------- | ---------------------------------------------- |
| `claude`    | 1568px  | Max native resolution before auto-resize       |
| `openai`    | 768px   | Aligned to 512px tile grid (shortest side 768) |
| `gemini`    | 768px   | Aligned to 768px tile boundaries               |
| `universal` | 768px   | Sweet spot across all models (default)         |

```bash
# Optimized for Claude -- maximum detail
python3 scripts/extract_frames.py video.mp4 --max-frames 30 --target-model claude

# Optimized for GPT-4o -- efficient tile packing
python3 scripts/extract_frames.py video.mp4 --max-frames 30 --target-model openai
```

`--target-model` sets the max dimension unless `--max-dimension` is explicitly provided (CLI override takes priority).

See `references/llm-image-specs.md` for detailed token formulas, tile calculations, and optimal dimension tables for each model.

## OCR and Grayscale Mode

For videos containing text (screencasts, presentations, documents, terminal recordings):

```bash
# Full OCR pipeline via preset
python3 scripts/extract_frames.py screencast.mp4 --preset ocr --max-frames 40

# Manual OCR flags (can combine with any preset)
python3 scripts/extract_frames.py video.mp4 --grayscale --high-contrast
```

- `--grayscale`: Converts frames to grayscale. Reduces file size ~60% with no OCR accuracy loss.
- `--high-contrast`: Applies `contrast=1.3, brightness=0.05` to improve text/background separation.
- The `ocr` preset enables both flags **plus** unsharp-mask sharpening at 1568px, quality 1 (best JPEG).

## Advanced Options

### FPS Selection Guide

When using `--fps` directly instead of `--max-frames`:

| Video length | Recommended fps | Rationale                               |
| ------------ | --------------- | --------------------------------------- |
| < 30s        | 2-5             | Short clip, capture detail              |
| 30s - 5min   | 1               | Good balance of coverage vs frame count |
| 5min - 30min | 0.5             | Avoid excessive frames                  |
| > 30min      | 0.1 - 0.2       | Sample key moments only                 |

Keep total frame count under ~50 for optimal LLM context usage. Formula: `duration_seconds * fps = frame_count`.

Prefer `--max-frames` over manual FPS -- it auto-calculates the right rate and clamps to 0.05-30.0 FPS.

### Timestamp Overlay

```bash
python3 scripts/extract_frames.py video.mp4 --timestamps --max-frames 30
```

Overlays the source filename and `hh:mm:ss` timestamp in the bottom-right corner of each frame (white text on semi-transparent black box). Use when the user needs to reference specific moments in the video.

### All CLI Options Reference

| Option                 | Type   | Default    | Description                                                        |
| ---------------------- | ------ | ---------- | ------------------------------------------------------------------ |
| `video_path`           | pos.   | (required) | Path to the video file                                             |
| `--fps`                | float  | 1.0        | Frames per second (mutually exclusive with `--scene-threshold`)    |
| `--scene-threshold`    | float  | --         | Scene-change sensitivity 0.0-1.0 (mutually exclusive with `--fps`) |
| `--min-scene-interval` | float  | 1.0        | Min seconds between scene-change frames                            |
| `--max-frames`         | int    | --         | Auto-calculate FPS to produce ~N frames                            |
| `--preset`             | choice | balanced   | `efficient` / `balanced` / `detailed` / `ocr`                      |
| `--max-dimension`      | int    | --         | Override max pixel dimension (longest edge)                        |
| `--quality`            | int    | --         | JPEG quality 1-31 (1=best, 31=worst)                               |
| `--target-model`       | choice | --         | `claude` / `openai` / `gemini` / `universal`                       |
| `--grayscale`          | flag   | off        | Convert to grayscale                                               |
| `--high-contrast`      | flag   | off        | Boost contrast for text readability                                |
| `--timestamps`         | flag   | off        | Overlay filename + timestamp on frames                             |
| `--output-dir`         | string | temp dir   | Output directory for extracted frames                              |

## Output JSON Structure

The script prints JSON to stdout with the following structure:

```json
{
  "output_dir": "/tmp/video_frames_abc123/",
  "frames": ["/tmp/video_frames_abc123/frame_00001.jpg", "..."],
  "preset": "balanced",
  "resolution": { "width": 1024, "height": 576 },
  "token_estimate": {
    "frame_count": 30,
    "per_frame": {
      "claude": 787,
      "openai_high": 765,
      "openai_low": 85,
      "openai_patch": 934,
      "gemini": 258
    },
    "total": {
      "claude": 23610,
      "openai_high": 22950,
      "openai_low": 2550,
      "openai_patch": 28020,
      "gemini": 7740
    }
  },
  "summary": {
    "video_duration_seconds": 120.5,
    "extraction_method": "max_frames",
    "scene_changes_detected": null,
    "frames_extracted": 30,
    "estimated_total_tokens": {
      "claude": 23610,
      "openai_high": 22950,
      "openai_low": 2550,
      "openai_patch": 28020,
      "gemini": 7740
    }
  }
}
```

Use `token_estimate.total` to verify the frame set fits within model context limits before attaching frames to a prompt.

> **Note:** `openai_high` and `openai_low` are for legacy models (GPT-4o, GPT-4.1). `openai_patch` is for newer models (gpt-5.4+, gpt-5-mini, o4-mini). See `references/llm-image-specs.md` for details.

On error, JSON with an `"error"` key is printed to stderr and the script exits with code 1.

## After Extraction

1. Parse the JSON output to get the list of frame paths from `frames`
2. Check `token_estimate.total` to ensure the frames fit within context limits
3. Read each frame image using the Read tool (they are JPEG files)
4. Analyze the frames to answer the user's question
5. Clean up: delete the output directory when done if it was a temp dir
