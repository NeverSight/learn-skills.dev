---
name: ffmpeg-video-editor
version: 1.0.0
description: >
  A complete FFmpeg-powered video editing agent. Use this skill whenever the
  user wants to do anything with video or audio files — trimming, cutting,
  transcoding, resizing, concatenating, adding subtitles, overlaying images or
  text, applying color grades or LUTs, normalizing audio levels, creating
  transitions, green-screen compositing, frame extraction, slideshows, or
  exporting for social media (TikTok, Reels, YouTube). Also use it for codec
  questions (H.264, H.265, VP9, AV1, ProRes, FFV1), hardware-accelerated
  encoding (NVIDIA NVENC, Intel QSV, VAAPI, Apple VideoToolbox), and any
  ffmpeg or ffprobe command construction. Even if the user just says "convert
  this video" or "make it smaller" or "add my logo" — reach for this skill.
  Reference documents in references/ cover filters, codecs, transitions, and
  hardware acceleration. Helper scripts in scripts/ handle probing,
  concatenation, and normalization.
author: ffmpeg-video-editor contributors
license: MIT
requirements:
  - ffmpeg >= 6.0
  - ffprobe >= 6.0
tags:
  - video
  - audio
  - ffmpeg
  - transcoding
  - editing
  - color-grading
  - normalization
---

# FFmpeg Video Editor Agent Skill

You are an expert FFmpeg operator. Use this skill to answer any video/audio
editing request by constructing correct `ffmpeg` command lines. Always probe
input files first, then select the appropriate operation category below.

## Probe Input Files

Run `scripts/probe.sh <file>` (make executable first with `chmod +x scripts/*.sh` if needed), or inspect manually:

```bash
ffprobe -v error -show_streams -show_format -of json input.mp4
```

## Trim / Cut

```bash
# Fast stream-copy trim (no re-encode)
ffmpeg -ss 00:01:00 -to 00:02:30 -i input.mp4 -c copy out.mp4

# Precise trim (re-encode around keyframes)
ffmpeg -ss 00:01:00 -i input.mp4 -t 90 -c:v libx264 -crf 18 -c:a aac out.mp4
```

## Transcode

```bash
# H.264 web-safe (pix_fmt ensures broad player compatibility)
ffmpeg -i input.mp4 -c:v libx264 -crf 23 -preset slow \
  -pix_fmt yuv420p -c:a aac -b:a 128k -movflags +faststart out.mp4

# H.265 (smaller files)
ffmpeg -i input.mp4 -c:v libx265 -crf 28 -preset slow \
  -pix_fmt yuv420p -c:a aac -b:a 128k out.mp4

# VP9 for web
ffmpeg -i input.mp4 -c:v libvpx-vp9 -crf 33 -b:v 0 \
  -c:a libopus -b:a 128k out.webm

# AV1 (best compression)
ffmpeg -i input.mp4 -c:v libaom-av1 -crf 35 -cpu-used 4 \
  -c:a libopus -b:a 128k out.mkv
```

See `references/CODECS.md` for full codec comparison.

## Concatenate Files

```bash
# Using helper script
scripts/concat.sh out.mp4 clip1.mp4 clip2.mp4 clip3.mp4

# Manual concat demuxer
printf "file 'a.mp4'\nfile 'b.mp4'\n" > list.txt
ffmpeg -f concat -safe 0 -i list.txt -c copy out.mp4
```

## Scale / Resize

```bash
# Scale to 1920×1080, keep aspect ratio, pad to fill
ffmpeg -i in.mp4 -vf "scale=1920:1080:force_original_aspect_ratio=decrease,\
pad=1920:1080:(ow-iw)/2:(oh-ih)/2:black" out.mp4

# Scale by width only (auto height)
ffmpeg -i in.mp4 -vf "scale=1280:-2" out.mp4
```

## Crop

```bash
# Crop 640×360 starting at (100,50)
ffmpeg -i in.mp4 -vf "crop=640:360:100:50" out.mp4

# Center crop to 1:1 square
ffmpeg -i in.mp4 -vf "crop=min(iw\,ih):min(iw\,ih)" out.mp4
```

## Overlay / Watermark

```bash
# Overlay image (top-right, 10px margin)
ffmpeg -i video.mp4 -i logo.png \
  -filter_complex "[0:v][1:v] overlay=W-w-10:10" out.mp4

# PiP: small video on top of main
ffmpeg -i main.mp4 -i pip.mp4 \
  -filter_complex "[1:v]scale=320:-2[small];[0:v][small]overlay=W-w-10:H-h-10" out.mp4
```

## Draw Text / Titles

```bash
ffmpeg -i in.mp4 -vf \
  "drawtext=text='My Title':fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf\
:fontsize=48:fontcolor=white:x=(w-text_w)/2:y=(h-text_h)/2\
:shadowx=2:shadowy=2" out.mp4
```

## Burn Subtitles

```bash
# SRT subtitles (re-encode required)
ffmpeg -i video.mp4 -vf "subtitles=subs.srt" out.mp4

# ASS/SSA subtitles (preserves styling)
ffmpeg -i video.mp4 -vf "ass=subs.ass" out.mp4
```

## Speed Change

```bash
# 2× speed (video + audio)
ffmpeg -i in.mp4 -vf "setpts=0.5*PTS" -af "atempo=2.0" out.mp4

# 0.5× speed (half speed)
ffmpeg -i in.mp4 -vf "setpts=2.0*PTS" -af "atempo=0.5" out.mp4

# >4×: chain atempo (max 2.0 per filter)
ffmpeg -i in.mp4 -vf "setpts=0.25*PTS" -af "atempo=2.0,atempo=2.0" out.mp4

# <0.5×: chain atempo (min 0.5 per filter)
ffmpeg -i in.mp4 -vf "setpts=4.0*PTS" -af "atempo=0.5,atempo=0.5" out.mp4
```

## Reverse

```bash
ffmpeg -i in.mp4 -vf "reverse" -af "areverse" out.mp4
```

## Transitions (xfade)

```bash
# Dissolve between two clips (1s overlap at t=5)
ffmpeg -i a.mp4 -i b.mp4 \
  -filter_complex "[0:v][1:v]xfade=transition=dissolve:duration=1:offset=5[v];\
[0:a][1:a]acrossfade=d=1[a]" \
  -map "[v]" -map "[a]" out.mp4
```

See `references/TRANSITIONS.md` for all 40+ xfade transition types.

## Audio: Volume & Normalization

```bash
# Adjust volume
ffmpeg -i in.mp4 -af "volume=1.5" out.mp4

# EBU R128 normalization (two-pass)
scripts/normalize-audio.sh in.mp4 out.mp4

# One-pass loudnorm
ffmpeg -i in.mp4 -af "loudnorm=I=-16:TP=-1.5:LRA=11" out.mp4
```

## Audio: Fade In/Out

```bash
# Fade in 2s at start, fade out 3s before end (total 60s)
ffmpeg -i in.mp4 -af "afade=t=in:d=2,afade=t=out:st=57:d=3" out.mp4
```

## Mix / Combine Audio

```bash
# Mix two audio streams
ffmpeg -i video.mp4 -i music.mp3 \
  -filter_complex "[0:a][1:a]amix=inputs=2:duration=first:weights=1 0.3[a]" \
  -map 0:v -map "[a]" -c:v copy out.mp4
```

## Color Grading

```bash
# Brightness/Contrast/Saturation
ffmpeg -i in.mp4 -vf "eq=brightness=0.05:contrast=1.2:saturation=1.3" out.mp4

# Hue shift
ffmpeg -i in.mp4 -vf "hue=h=30:s=1.1" out.mp4

# Apply 3D LUT (.cube)
ffmpeg -i in.mp4 -vf "lut3d=file=lut.cube" out.mp4

# Apply Hald CLUT PNG
ffmpeg -i in.mp4 -i lut.png \
  -filter_complex "[0:v][1:v]haldclut" out.mp4
```

## Chroma Key / Green Screen

```bash
# chromakey (color + similarity + blend)
ffmpeg -i foreground.mp4 -i background.mp4 \
  -filter_complex "[0:v]chromakey=0x00FF00:0.3:0.2[fg];\
[1:v][fg]overlay" out.mp4

# colorkey (simpler, exact color)
ffmpeg -i in.mp4 -vf "colorkey=green:0.3:0.2" out.mp4
```

## Frame Rate Conversion

```bash
# Convert to 30fps
ffmpeg -i in.mp4 -vf "fps=30" out.mp4

# Use motion interpolation (minterpolate)
ffmpeg -i in.mp4 -vf "minterpolate=fps=60:mi_mode=mci" out.mp4
```

## Extract Frames / Create Slideshow

```bash
# Extract one frame per second as PNG
ffmpeg -i in.mp4 -vf "fps=1" frames/%04d.png

# Slideshow from images (3s per image, 30fps output)
ffmpeg -framerate 1/3 -i frames/%04d.png -c:v libx264 -r 30 out.mp4
```

## Stacking / Grid Layout

```bash
# Side by side (hstack)
ffmpeg -i a.mp4 -i b.mp4 -filter_complex "[0:v][1:v]hstack=inputs=2" out.mp4

# Top-bottom (vstack)
ffmpeg -i a.mp4 -i b.mp4 -filter_complex "[0:v][1:v]vstack=inputs=2" out.mp4

# 2×2 grid (xstack)
ffmpeg -i a.mp4 -i b.mp4 -i c.mp4 -i d.mp4 \
  -filter_complex "[0:v][1:v][2:v][3:v]xstack=inputs=4:layout=0_0|w0_0|0_h0|w0_h0" out.mp4
```

## Hardware-Accelerated Encoding

```bash
# NVIDIA NVENC H.264
ffmpeg -hwaccel cuda -i in.mp4 -c:v h264_nvenc -preset p4 -cq 23 out.mp4

# Apple VideoToolbox H.265
ffmpeg -i in.mp4 -c:v hevc_videotoolbox -q:v 60 out.mp4

# Intel QuickSync H.264
ffmpeg -hwaccel qsv -i in.mp4 -c:v h264_qsv -global_quality 23 out.mp4
```

See `references/HARDWARE-ACCEL.md` for full GPU encoding guide.

## Encoding Presets (assets/preset-profiles.json)

When the task maps to a named use case below, read `assets/preset-profiles.json`
and use the `example` field as the ready-made ffmpeg command.

| Profile                  | Codec     | CRF | Use Case              |
|--------------------------|-----------|-----|-----------------------|
| web-optimized            | H.264     | 23  | Browser streaming     |
| high-quality             | H.264     | 18  | Archive / master      |
| social-media-vertical    | H.264     | 23  | 9:16 TikTok/Reels     |
| social-media-square      | H.264     | 23  | 1:1 Instagram         |
| fast-preview             | H.264     | 28  | Proxy / review        |
| lossless-intermediate    | FFV1      | —   | Post-production store |

## Multi-Stream Filter Graph Pattern

```bash
ffmpeg \
  -i input_video.mp4 \
  -i overlay.png \
  -i audio_bed.mp3 \
  -filter_complex "
    [0:v]scale=1920:1080,setsar=1[base];
    [1:v]scale=200:-2,format=rgba,colorchannelmixer=aa=0.8[logo];
    [base][logo]overlay=W-w-20:20[composited];
    [0:a][2:a]amix=inputs=2:weights=1 0.2[audio_mix]
  " \
  -map "[composited]" -map "[audio_mix]" \
  -c:v libx264 -crf 18 -preset slow \
  -c:a aac -b:a 192k \
  -movflags +faststart \
  output.mp4
```

## Common Options Reference

| Flag              | Meaning                                      |
|-------------------|----------------------------------------------|
| `-ss`             | Seek/start time (before `-i` = fast seek)    |
| `-to`             | End time (absolute)                          |
| `-t`              | Duration                                     |
| `-c copy`         | Stream copy (no re-encode)                   |
| `-crf`            | Constant Rate Factor (lower = better)        |
| `-preset`         | Encoder speed/quality tradeoff               |
| `-movflags +faststart` | Move moov atom to front (web streaming) |
| `-vf`             | Video filter chain                           |
| `-af`             | Audio filter chain                           |
| `-filter_complex` | Multi-input/output filter graph              |
| `-map`            | Select output streams explicitly             |
| `-an`             | Drop audio                                   |
| `-vn`             | Drop video                                   |
| `-y`              | Overwrite output without prompt              |

## Debugging Tips

```bash
# Dry-run: print filter graph without encoding
ffmpeg -i in.mp4 -vf "scale=1280:-2" -f null -

# Benchmark encode speed
ffmpeg -benchmark -i in.mp4 -c:v libx264 -f null -

# Show available encoders
ffmpeg -encoders | grep -E "^.V|^.A"

# Show filter options
ffmpeg -help filter=loudnorm
```
