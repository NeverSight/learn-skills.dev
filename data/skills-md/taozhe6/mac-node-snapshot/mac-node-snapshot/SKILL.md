---
name: mac-node-snapshot
description: A robust, permission-friendly method to capture macOS screens via OpenClaw screen.record. Ideal for headless environments or ensuring capture reliability.
---

# mac-node-snapshot

## Overview
Uses node screen.record to record a 1-second clip and extract a high-quality PNG frame. This workflow bypasses common screencapture permission issues and ensures a reliable image return.

## Quick start (single command, no scripts)
All paths are **relative** to `{skill}`.

```bash
mkdir -p "{skill}/tmp" \
&& openclaw nodes screen record --node "<node>" --duration 1000 --fps 10 --no-audio --out "{skill}/tmp/snap.mp4" \
&& ffmpeg -hide_banner -loglevel error -y -ss 00:00:00 -i "{skill}/tmp/snap.mp4" -frames:v 1 "{skill}/tmp/snap.png"
```

## When to use (trigger phrases)
Use this skill when the user asks:
- "Take a screenshot"
- "What is on my screen?"
- "Capture the screen"
- "Screenshot via screen.record"

## Notes
- Requirements: `ffmpeg` (ask before installing).
- If the frame is **black**, ask the user to **wake the screen** and retry.
- Use `read` on `{skill}/tmp/snap.png` to attach it to the reply.

## Troubleshooting
- **screen_record fails (node disconnected):** check `nodes status`, ensure OpenClaw app is running/paired.
- **screenRecording false:** must grant Screen Recording in System Settings; cannot be bypassed.
- **Black frame:** screen may be asleep/locked; ask the user to wake and retry.
