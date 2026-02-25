---
name: video-editor
description: Expert guidance for video editing with ffmpeg, encoding best practices, and quality optimization. Use when working with video files, transcoding, remuxing, encoding settings, color spaces, or troubleshooting video quality issues.
---

# Video Editor - FFmpeg & Encoding Expert

Expert guidance for video editing, encoding, and processing with ffmpeg. This skill covers container formats, codecs, encoding best practices, and quality optimization for video production workflows.

## When to Use This Skill

Use this skill when:
- Encoding or transcoding video files
- Converting between container formats (MKV, MP4, etc.)
- Optimizing encoding settings for quality or file size
- Troubleshooting video quality issues
- Working with color spaces and color matrices
- Hardsubbing or softsubbing videos
- Preparing videos for specific platforms or devices
- Understanding why a video looks wrong after processing

## Core Concepts

### Container vs. Codec

**This distinction is critical.** File extensions like `.mkv` or `.mp4` are **container formats** that package already-compressed streams. The actual compression happens through **codecs** like H.264, H.265, VP9, or AV1.

| Concept | What It Is | Examples |
|---------|------------|----------|
| Container | Wrapper that holds video/audio/subtitle streams | MKV, MP4, AVI, MOV, WebM |
| Codec | Algorithm that compresses/decompresses video | H.264, H.265/HEVC, VP9, AV1 |
| Encoder | Software that implements a codec | x264, x265, libvpx, NVENC |

### Remuxing vs. Reencoding

| Operation | What It Does | Quality Impact | Speed |
|-----------|--------------|----------------|-------|
| **Remuxing** | Moves streams between containers without re-compression | None (lossless) | Very fast |
| **Reencoding** | Decodes and re-encodes video with new settings | Always loses quality | Slow |

**Rule of thumb:** If you only need to change the container format, remux. Only reencode when absolutely necessary.

## Quality Principles

### What "Quality" Actually Means

Video quality measures **how closely the output resembles the source**. Every processing step moves the video further from the original. There is no way to add quality - only preserve or lose it.

### Common Misconceptions

| Myth | Reality |
|------|---------|
| Higher resolution = better quality | Resolution is just dimensions; a 720p video can look better than a 4K one |
| Higher bitrate = better quality | Encoder efficiency matters more; same quality at different sizes is possible |
| H.265 is always 50% smaller | Depends on encoder settings; poorly-configured H.265 can be worse than H.264 |
| Hardware encoding is fine for quality | Hardware encoders (NVENC, QuickSync) sacrifice quality for speed |
| AI upscaling improves quality | Upscaling adds artificial detail that wasn't in the source |

### The Encoding Quality Hierarchy

From most to least important:
1. **Encoder settings** (CRF, preset, tuning)
2. **Encoder choice** (x264/x265 vs. hardware encoders)
3. **Codec** (H.265 vs. H.264 vs. VP9)

## Quick Reference: FFmpeg Commands

### Remux (Change Container, No Quality Loss)

```bash
# MKV to MP4 (preserves all streams)
ffmpeg -i input.mkv -c copy output.mp4

# MP4 to MKV
ffmpeg -i input.mp4 -c copy output.mkv
```

### Basic Encoding

```bash
# Encode with x264, copy audio
ffmpeg -i input.mkv -c:a copy -c:v libx264 -preset slower -crf 20 output.mkv

# Encode with x265
ffmpeg -i input.mkv -c:a copy -c:v libx265 -preset slower -crf 22 output.mkv
```

### Quality-Focused Encoding

```bash
# High-quality x264 for animation
ffmpeg -i input.mkv -c:a copy -c:v libx264 -preset slower -crf 18 \
  -x264-params bframes=8 output.mkv

# High-quality x265
ffmpeg -i input.mkv -c:a copy -c:v libx265 -preset slower -crf 20 \
  -x265-params bframes=8 output.mkv
```

## Encoding Settings Deep Dive

### CRF (Constant Rate Factor)

CRF controls quality vs. file size tradeoff. **Lower = higher quality, larger file.**

| CRF Range | Quality Level | Typical Use |
|-----------|---------------|-------------|
| 0 | Lossless | Archival, intermediate |
| 15-18 | Visually lossless | High-quality archival |
| 19-23 | High quality | General use, streaming |
| 24-28 | Medium quality | Web, mobile |
| 29+ | Low quality | Previews, thumbnails |

**Note:** CRF values aren't directly comparable between encoders. x265 CRF 22 ≈ x264 CRF 20.

### Preset

Presets control encoding speed vs. compression efficiency.

| Preset | Speed | File Size | Use When |
|--------|-------|-----------|----------|
| ultrafast | Fastest | Largest | Live streaming |
| fast | Fast | Large | Quick transcodes |
| medium | Moderate | Moderate | Default |
| slow | Slow | Smaller | Quality-focused |
| slower | Very slow | Even smaller | Recommended for quality |
| veryslow | Extremely slow | Smallest | Maximum compression |

**Recommendation:** Use `slower` for quality-focused encoding. The difference between `slower` and `veryslow` is minimal for significant time cost.

### Tune Options

| Tune | Best For |
|------|----------|
| film | Live-action with film grain |
| animation | Cartoons, anime, flat areas |
| grain | Preserve film grain |
| stillimage | Slideshow, static content |
| fastdecode | Playback on weak devices |

```bash
# Animation tuning
ffmpeg -i input.mkv -c:v libx264 -preset slower -crf 20 -tune animation output.mkv
```

## Container-Specific Considerations

### MKV (Matroska)

**Pros:**
- Supports virtually any codec
- Multiple audio/subtitle tracks
- Chapter markers
- Variable frame rate support

**Cons:**
- Less compatible with some devices/software
- Some streaming services don't accept it

### MP4

**Pros:**
- Universal compatibility
- Web-friendly
- Hardware decoder support everywhere

**Cons:**
- Limited subtitle format support
- Stricter codec requirements
- Constant frame rate expected

### Converting MKV to MP4 for Editing Software

Some editing software requires constant frame rate MP4. Use this two-pass approach:

```bash
# Step 1: Initial remux with timescale adjustment
ffmpeg -i input.mkv -c copy -video_track_timescale 24000 intermediate.mp4

# Step 2: Fix timestamps
ffmpeg -i intermediate.mp4 -c copy \
  -bsf:v "setts=dts=1001*round(DTS/1001):pts=1001*round(PTS/1001)" output.mp4
```

## Color Space & Color Management

### Understanding Color Metadata

Videos store colors in YCbCr format with metadata specifying:
- **Color matrix**: How to convert YCbCr to RGB (BT.709, BT.601)
- **Color range**: Limited (16-235) vs. Full (0-255)
- **Chroma location**: Where color samples are positioned

### Common Issues

| Symptom | Likely Cause |
|---------|--------------|
| Washed out colors | Wrong color range (Limited treated as Full) |
| Crushed blacks/blown whites | Wrong color range (Full treated as Limited) |
| Greenish/pinkish tint | Wrong color matrix |
| Colors look "off" after encode | Mismatched color metadata |

### Preserving Color Information

```bash
# Explicitly preserve color metadata
ffmpeg -i input.mkv -c:v libx264 -preset slower -crf 20 \
  -colorspace bt709 -color_primaries bt709 -color_trc bt709 output.mkv
```

## Hardsubbing (Burning In Subtitles)

### Using FFmpeg

```bash
# Hardsub from external subtitle file
ffmpeg -i input.mkv -vf "subtitles=subs.ass" -c:v libx264 -preset slower -crf 20 output.mkv

# Hardsub from embedded subtitle track
ffmpeg -i input.mkv -vf "subtitles=input.mkv:si=0" -c:v libx264 -preset slower -crf 20 output.mkv
```

### Using mpv (Better for Complex Subtitles)

mpv handles complex ASS subtitles (styling, positioning) more accurately:

```bash
mpv --no-config input.mkv -o output.mkv \
  --audio=no \
  --ovc=libx264 \
  --ovcopts=preset=slower,crf=20,bframes=8
```

## What to Avoid

### Tools

| Tool | Problem |
|------|---------|
| Handbrake | Unpredictable settings, hides important options |
| Online converters | Quality loss, privacy concerns |
| "AI upscalers" | Add fake detail, move further from source |
| Windows built-in tools | Poor quality, limited options |

### Practices

| Practice | Why It's Bad |
|----------|--------------|
| Unnecessary sharpening | Adds artifacts, moves from source |
| Upscaling to higher resolution | Doesn't add real detail |
| Multiple reencodes | Quality loss compounds |
| Using NVENC for quality | Hardware encoders prioritize speed over quality |
| Frame rate interpolation | Adds fake frames with artifacts |

## Recommended Tools

### Essential

| Tool | Purpose |
|------|---------|
| [ffmpeg](https://ffmpeg.org/) | Swiss army knife for video processing |
| [MediaInfo](https://mediaarea.net/en/MediaInfo) | Inspect video properties and metadata |
| [mpv](https://mpv.io/) | Superior media player, encoding support |
| [MKVToolNix](https://mkvtoolnix.download/) | GUI for MKV muxing operations |

### Specialized

| Tool | Purpose |
|------|---------|
| [Aegisub](https://aegisub.org/) | Subtitle editing |
| [HandBrake](https://handbrake.fr/) | Simple transcoding (use with caution) |
| [yt-dlp](https://github.com/yt-dlp/yt-dlp) | Download online videos |

## Troubleshooting

### Video Won't Play

1. Check codec support on target device
2. Try remuxing to different container
3. Verify file isn't corrupted: `ffmpeg -v error -i file.mkv -f null -`

### Colors Look Wrong After Encoding

1. Compare color metadata: `mediainfo input.mkv` vs. `mediainfo output.mkv`
2. Check color range (Limited vs. Full)
3. Check color matrix (BT.709 vs. BT.601)
4. Explicitly set color parameters in ffmpeg command

### File Size Too Large

1. Increase CRF (e.g., 20 → 23)
2. Use slower preset for better compression
3. Consider x265 for better efficiency
4. Check if you're unnecessarily encoding (remux instead)

### Encoding Takes Forever

1. Use faster preset (but accept larger file)
2. Check if hardware encoding is acceptable for your use case
3. Ensure source isn't being decoded unnecessarily

### Audio/Video Out of Sync

1. Check source file for sync issues first
2. Use `-async 1` for audio sync correction
3. Try remuxing instead of reencoding

## Examples

### Archive a Blu-ray Rip

```bash
ffmpeg -i input.mkv -c:a copy -c:v libx265 -preset slower -crf 18 \
  -x265-params bframes=8 output.mkv
```

### Prepare for YouTube Upload

```bash
ffmpeg -i input.mkv -c:a aac -b:a 384k -c:v libx264 -preset slower -crf 18 \
  -profile:v high -level 4.2 -pix_fmt yuv420p output.mp4
```

### Quick Preview/Proxy

```bash
ffmpeg -i input.mkv -c:a aac -b:a 128k -c:v libx264 -preset fast -crf 28 \
  -vf scale=640:-2 output.mp4
```

### Extract Audio Only

```bash
# Copy audio stream (no re-encoding)
ffmpeg -i input.mkv -vn -c:a copy output.mka

# Convert to MP3
ffmpeg -i input.mkv -vn -c:a libmp3lame -b:a 320k output.mp3
```

### Trim Without Re-encoding

```bash
# Trim from 1:00 to 2:30
ffmpeg -i input.mkv -ss 00:01:00 -to 00:02:30 -c copy output.mkv
```

## Resources

- [FFmpeg Documentation](https://ffmpeg.org/documentation.html)
- [FFmpeg Wiki](https://trac.ffmpeg.org/wiki)
- [x264 Settings Guide](https://trac.ffmpeg.org/wiki/Encode/H.264)
- [x265 Settings Guide](https://trac.ffmpeg.org/wiki/Encode/H.265)
- [MediaInfo](https://mediaarea.net/en/MediaInfo)
- [mpv Manual](https://mpv.io/manual/stable/)
