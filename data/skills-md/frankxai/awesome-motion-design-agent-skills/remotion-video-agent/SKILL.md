---
name: remotion-video-agent
description: Use when creating or editing Remotion videos, programmatic explainers, motion graphics, MP4 renders, GIF renders, social cutdowns, or React-authored video templates.
---

# Remotion Video Agent

## Workflow

1. Confirm the composition format: aspect ratio, duration, FPS, destination, and voice/music requirements.
2. Break the video into scenes with frame ranges.
3. Build scenes as React components with deterministic timing.
4. Use Remotion helpers for interpolation, sequencing, audio, static files, and rendering.
5. Prefer MP4 for delivery. Use GIF only for previews or documentation.
6. Render and inspect before final delivery.

## Useful Defaults

- 30 FPS for general video.
- 60 FPS only when motion quality requires it.
- 1080x1920 for vertical social.
- 1920x1080 for YouTube/demo.
- 1200x630 or 1600x900 for launch preview loops.

## QA

- No text cut off.
- No scene timing dead air.
- Motion supports the script.
- Assets are licensed or owned.
- Audio levels are not clipped.
- GIF exports are size-conscious.

