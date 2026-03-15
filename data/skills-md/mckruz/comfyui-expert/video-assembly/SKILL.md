---
name: video-assembly
description: Assemble final video from generated clips, audio, and assets using FFmpeg or Remotion. Handles concatenation, audio mixing, transitions, titles, and export. Use when combining multiple production outputs into a final deliverable.
user-invocable: true
metadata: {"openclaw":{"emoji":"🎞️","os":["darwin","linux","win32"],"requires":{"bins":["ffmpeg"]}}}
---

# Video Assembly

Combines outputs from video and voice pipelines into final deliverable videos.

## Two Assembly Modes

### Mode 1: FFmpeg (Simple, Fast)

Best for: Concatenation, audio mixing, basic transitions, format conversion.

No dependencies beyond FFmpeg (pre-installed on most systems).

### Mode 2: Remotion (Complex Compositions)

Best for: Animated captions, data visualizations, complex motion graphics, React-based templates.

Uses existing `remotion-best-practices` skill for guidance.

## FFmpeg Operations

### Concatenate Video Clips

```bash
# Create file list
echo "file 'clip1.mp4'" > filelist.txt
echo "file 'clip2.mp4'" >> filelist.txt
echo "file 'clip3.mp4'" >> filelist.txt

# Concatenate (same codec/resolution)
ffmpeg -f concat -safe 0 -i filelist.txt -c copy output.mp4

# Concatenate (different codecs/resolutions - re-encode)
ffmpeg -f concat -safe 0 -i filelist.txt -vf "scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2" -c:v libx264 -crf 19 output.mp4
```

### Add Audio to Video

```bash
# Replace audio
ffmpeg -i video.mp4 -i audio.wav -c:v copy -c:a aac -map 0:v:0 -map 1:a:0 output.mp4

# Mix audio (keep original + add music)
ffmpeg -i video.mp4 -i music.mp3 -filter_complex "[0:a][1:a]amix=inputs=2:duration=first:dropout_transition=3" -c:v copy output.mp4

# Add audio with volume control
ffmpeg -i video.mp4 -i bgm.mp3 -filter_complex "[1:a]volume=0.3[bg];[0:a][bg]amix=inputs=2:duration=first" -c:v copy output.mp4
```

### Add Subtitles

```bash
# Burn subtitles (SRT file)
ffmpeg -i video.mp4 -vf "subtitles=subs.srt:force_style='FontName=Arial,FontSize=24,PrimaryColour=&HFFFFFF,OutlineColour=&H000000,Outline=2'" -c:a copy output.mp4

# Burn subtitles (ASS file for styled)
ffmpeg -i video.mp4 -vf "ass=subs.ass" -c:a copy output.mp4
```

### Transitions Between Clips

```bash
# Crossfade (2 second transition)
ffmpeg -i clip1.mp4 -i clip2.mp4 -filter_complex \
  "[0:v]trim=0:5,setpts=PTS-STARTPTS[v0]; \
   [1:v]trim=0:5,setpts=PTS-STARTPTS[v1]; \
   [v0][v1]xfade=transition=fade:duration=2:offset=3[outv]" \
  -map "[outv]" output.mp4
```

### Extract/Manipulate Frames

```bash
# Extract frames
ffmpeg -i video.mp4 -vf "fps=1" frames/frame_%04d.png

# Create video from frames
ffmpeg -framerate 24 -i frames/frame_%04d.png -c:v libx264 -crf 19 -pix_fmt yuv420p output.mp4

# Speed up/slow down
ffmpeg -i video.mp4 -filter:v "setpts=0.5*PTS" -filter:a "atempo=2.0" fast.mp4   # 2x speed
ffmpeg -i video.mp4 -filter:v "setpts=2.0*PTS" -filter:a "atempo=0.5" slow.mp4   # 0.5x speed
```

### Format Conversion

```bash
# MP4 (H.264) - universal compatibility
ffmpeg -i input.mov -c:v libx264 -crf 19 -preset medium -c:a aac -b:a 192k output.mp4

# WebM (VP9) - web delivery
ffmpeg -i input.mp4 -c:v libvpx-vp9 -crf 30 -b:v 0 -c:a libopus output.webm

# GIF (short clips)
ffmpeg -i input.mp4 -vf "fps=15,scale=480:-1:flags=lanczos" -loop 0 output.gif
```

### Quality Presets

| Use Case | CRF | Resolution | Notes |
|----------|-----|------------|-------|
| Master/Archive | 15-17 | Original | Large files, best quality |
| YouTube Upload | 18-20 | 1920x1080 | Good balance |
| Social Media | 20-23 | 1080x1920 (vertical) | Smaller files |
| Preview/Draft | 25-28 | 1280x720 | Quick review |

## Assembly Pipeline

### Standard Video

```
1. Gather clips from comfyui-video-pipeline outputs
2. Gather audio from comfyui-voice-pipeline outputs
3. Normalize audio levels (-16 LUFS for YouTube)
4. Trim/arrange clips to match script timing
5. Add transitions between clips (if multiple)
6. Add background music (optional, lower volume)
7. Add subtitles (if applicable)
8. Export in target format
```

### Talking Head Video

```
1. Lip-synced video from comfyui-voice-pipeline
2. Add intro/outro (if applicable)
3. Add lower thirds or name cards
4. Add background music at -20dB below speech
5. Normalize speech to -16 LUFS
6. Export
```

### Tutorial/Walkthrough

```
1. Screen recordings + talking head overlay
2. Use Remotion for animated annotations
3. Add chapter markers
4. Add subtitles (auto-generate from audio)
5. Export with chapters embedded
```

## Audio Normalization

```bash
# Normalize to -16 LUFS (YouTube standard)
ffmpeg -i input.mp4 -af "loudnorm=I=-16:TP=-1.5:LRA=11" -c:v copy output.mp4

# Two-pass normalization (more accurate)
ffmpeg -i input.mp4 -af loudnorm=I=-16:TP=-1.5:LRA=11:print_format=json -f null -
# Read measured values, then:
ffmpeg -i input.mp4 -af "loudnorm=I=-16:TP=-1.5:LRA=11:measured_I=-20:measured_TP=-2:measured_LRA=8:measured_thresh=-30" -c:v copy output.mp4
```

## Remotion Integration

For complex compositions, delegate to `remotion-best-practices` skill.

**Use Remotion when:**
- Animated text/captions needed
- Data visualizations in video
- Complex motion graphics
- Programmatic/template-based video generation
- React-based UI elements as video overlays

**Pass to Remotion:**
- Clip paths and timings
- Text content and styles
- Animation specifications
- Output format requirements

## Output Checklist

Before marking assembly as complete:

- [ ] Audio levels normalized (-16 LUFS for YouTube)
- [ ] No audio clipping (peak below -1.5 dB)
- [ ] Resolution matches delivery target
- [ ] Frame rate is consistent throughout
- [ ] No black frames at cuts
- [ ] Subtitles are timed correctly (if applicable)
- [ ] File size is reasonable for delivery platform
- [ ] Metadata is correct (title in filename)

## Reference

- `references/workflows.md` - Video output format settings
- `remotion-best-practices` skill - Complex composition guidance
