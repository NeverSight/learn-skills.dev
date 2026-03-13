---
name: ffmpeg-toolkit
description: >-
  Video and audio processing with FFmpeg. Covers transcoding, resizing, trimming,
  speed adjustment, compression, audio extraction, concatenation, cropping,
  thumbnails, and probing. References available for codec/filter lookup, audio
  processing, streaming formats, Remotion integration, and platform export.
---

# FFmpeg Toolkit

## Transcode

```bash
# Convert to MP4 (H.264 + AAC)
ffmpeg -i input.mov -c:v libx264 -preset medium -crf 23 \
       -c:a aac -b:a 128k output.mp4

# Convert to WebM (VP9 + Opus)
ffmpeg -i input.mp4 -c:v libvpx-vp9 -crf 30 -b:v 0 \
       -c:a libopus -b:a 128k output.webm
```

## Resize

```bash
# Specific dimensions
ffmpeg -i input.mp4 -vf "scale=1920:1080" output.mp4

# Aspect-ratio preserve with padding (letterbox/pillarbox)
ffmpeg -i input.mp4 -vf "scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2" output.mp4

# Crop to fill (no black bars)
ffmpeg -i input.mp4 -vf "scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080" output.mp4

# Scale to width, auto height
ffmpeg -i input.mp4 -vf "scale=1280:-2" output.mp4

# Scale to percentage (50%)
ffmpeg -i input.mp4 -vf "scale=iw/2:ih/2" output.mp4
```

## Trim and Cut

```bash
# Cut from timestamp + duration (re-encode recommended for accuracy)
ffmpeg -i input.mp4 -ss 00:00:30 -t 00:00:15 -c:v libx264 -c:a aac output.mp4

# Cut from start to end timestamp
ffmpeg -i input.mp4 -ss 00:00:30 -to 00:00:45 -c:v libx264 -c:a aac output.mp4

# Stream copy (faster, but may lose frames at non-keyframe cut points)
ffmpeg -i input.mp4 -ss 00:00:30 -t 00:00:15 -c copy output.mp4

# Fast seek for large files (put -ss before -i)
ffmpeg -ss 00:10:00 -i large_video.mp4 -t 00:05:00 -c copy clip.mp4
```

**Note:** Re-encoding is recommended for trimming. Stream copy (`-c copy`) can silently drop video if the seek point doesn't align with a keyframe.

## Speed Adjustment

```bash
# 2x speed (video and audio)
ffmpeg -i input.mp4 -filter_complex "[0:v]setpts=0.5*PTS[v];[0:a]atempo=2.0[a]" \
       -map "[v]" -map "[a]" output.mp4

# 0.5x speed (slow motion)
ffmpeg -i input.mp4 -filter_complex "[0:v]setpts=2.0*PTS[v];[0:a]atempo=0.5[a]" \
       -map "[v]" -map "[a]" output.mp4

# Video only (no audio)
ffmpeg -i input.mp4 -filter:v "setpts=0.5*PTS" -an output.mp4

# Extreme slow motion (0.25x) - chain atempo filters (each limited to 0.5-2.0)
ffmpeg -i input.mp4 -filter_complex "[0:v]setpts=4.0*PTS[v];[0:a]atempo=0.5,atempo=0.5[a]" \
       -map "[v]" -map "[a]" output.mp4
```

**Calculate speed factor:**
- To fit X seconds into Y seconds: `speed = X / Y`
- setpts multiplier = `1 / speed` (e.g., 3x speed = `setpts=0.333*PTS`)
- atempo value = `speed` (e.g., 3x speed = `atempo=3.0`)
- Extreme speed audio (>2x): chain atempo filters, e.g. 4x = `atempo=2.0,atempo=2.0`

*For Remotion playbackRate vs FFmpeg speed decisions, see [remotion.md](remotion.md).*

## Compress

```bash
# Good quality, smaller file (CRF 23 is default, lower = better)
ffmpeg -i input.mp4 -c:v libx264 -crf 23 -preset medium -c:a aac -b:a 128k output.mp4

# Aggressive compression for web preview
ffmpeg -i input.mp4 -c:v libx264 -crf 28 -preset fast -c:a aac -b:a 96k output.mp4

# Target file size (e.g., ~10MB for 60s video = ~1.3Mbps)
ffmpeg -i input.mp4 -c:v libx264 -b:v 1300k -c:a aac -b:a 128k output.mp4
```

*For platform-specific size targets, see [platform-export.md](platform-export.md).*

## Extract and Convert Audio

```bash
# Extract to MP3
ffmpeg -i input.mp4 -vn -acodec libmp3lame -q:a 2 output.mp3

# Extract to AAC
ffmpeg -i input.mp4 -vn -acodec aac -b:a 192k output.m4a

# Extract to WAV (uncompressed)
ffmpeg -i input.mp4 -vn output.wav

# Extract audio from specific time range
ffmpeg -i video.mp4 -ss 00:01:00 -t 00:00:30 -vn audio.mp3

# M4A to MP3
ffmpeg -i input.m4a -codec:a libmp3lame -qscale:a 2 output.mp3

# Adjust volume
ffmpeg -i input.mp3 -filter:a "volume=1.5" output.mp3
```

## Crop

```bash
# Arbitrary crop (width:height:x:y)
ffmpeg -i input.mp4 -vf "crop=640:480:100:50" output.mp4

# Center crop to 16:9
ffmpeg -i input.mp4 -vf "crop=ih*16/9:ih" output.mp4
```

## Concatenate

```bash
# Create file list
echo "file 'clip1.mp4'" > list.txt
echo "file 'clip2.mp4'" >> list.txt
echo "file 'clip3.mp4'" >> list.txt

# Concatenate (same codec/resolution)
ffmpeg -f concat -safe 0 -i list.txt -c copy output.mp4

# Concatenate with re-encoding (different sources)
ffmpeg -f concat -safe 0 -i list.txt -c:v libx264 -c:a aac output.mp4
```

## Fade

```bash
# Video fade in first 1s, fade out last 1s (adjust st= for your duration)
ffmpeg -i input.mp4 -vf "fade=t=in:st=0:d=1,fade=t=out:st=9:d=1" -c:a copy output.mp4

# Audio fade
ffmpeg -i input.mp4 -af "afade=t=in:st=0:d=1,afade=t=out:st=9:d=1" -c:v copy output.mp4
```

## Overlay and Composition

```bash
# Watermark (bottom-right corner)
ffmpeg -i video.mp4 -i watermark.png \
       -filter_complex "overlay=W-w-10:H-h-10" output.mp4

# Text overlay
ffmpeg -i input.mp4 -vf "drawtext=text='Hello World':fontsize=24:fontcolor=white:x=10:y=10" output.mp4

# Picture-in-Picture
ffmpeg -i main.mp4 -i overlay.mp4 \
       -filter_complex "[1:v]scale=320:-1[pip];[0:v][pip]overlay=W-w-10:H-h-10" output.mp4

# Side by side
ffmpeg -i left.mp4 -i right.mp4 \
       -filter_complex "[0:v]scale=640:-1[l];[1:v]scale=640:-1[r];[l][r]hstack" output.mp4
```

## Thumbnails and Screenshots

```bash
# Single screenshot at timestamp
ffmpeg -i video.mp4 -ss 00:00:10 -vframes 1 thumbnail.jpg

# Best quality thumbnail
ffmpeg -i video.mp4 -ss 00:00:10 -vframes 1 -q:v 2 thumbnail.jpg

# Generate thumbnails every N seconds
ffmpeg -i video.mp4 -vf "fps=1/10" thumbnails_%03d.jpg

# Thumbnail sprite sheet
ffmpeg -i video.mp4 -vf "fps=1/5,scale=160:-1,tile=5x5" sprite.jpg

# GIF from video (simple)
ffmpeg -i input.mp4 -vf "fps=10,scale=480:-1" output.gif

# GIF from video (palette for better quality + smaller size)
ffmpeg -i input.mp4 -vf "fps=10,scale=480:-1,split[s0][s1];[s0]palettegen[p];[s1][p]paletteuse" output.gif
```

## Probe (ffprobe)

```bash
# Full JSON info
ffprobe -v quiet -print_format json -show_format -show_streams input.mp4

# Duration in seconds
ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 input.mp4

# Resolution
ffprobe -v error -select_streams v:0 -show_entries stream=width,height -of csv=p=0 input.mp4

# Codec name
ffprobe -v error -select_streams v:0 -show_entries stream=codec_name -of default=noprint_wrappers=1:nokey=1 input.mp4

# Frame count
ffprobe -v error -select_streams v:0 -count_frames -show_entries stream=nb_read_frames -of csv=p=0 input.mp4
```

## Batch Processing

```bash
# Convert all MP4s to WebM
for f in *.mp4; do
    ffmpeg -i "$f" -c:v libvpx-vp9 -crf 30 -c:a libopus "${f%.mp4}.webm"
done

# Resize all images in directory
for f in *.jpg; do
    ffmpeg -i "$f" -vf "scale=1280:-1" "resized_$f"
done

# Extract audio from multiple videos
for f in *.mp4; do
    ffmpeg -i "$f" -vn -c:a mp3 -b:a 192k "${f%.mp4}.mp3"
done
```

## Common Errors

| Error | Cause | Fix |
|-------|-------|-----|
| "height not divisible by 2" | Odd dimensions | Add `-vf "scale=trunc(iw/2)*2:trunc(ih/2)*2"` |
| Video won't play in browser | Missing web flags | Use `-movflags faststart -pix_fmt yuv420p -c:v libx264` |
| Audio out of sync after speed change | Mismatched filters | Use `filter_complex` with both `setpts` and `atempo` |
| File too large | Low compression | Increase CRF (23->28) or reduce resolution |
| "No such file" | Wrong input path | Check path, use quotes for spaces |
| "Invalid data" | Corrupted input | Re-download or re-record source |
| "encoder not found" | Missing codec | Install FFmpeg with full codecs |
| Output 0 bytes | Silent failure | Check full ffmpeg output (`-v error`) |

## Quality Guidelines

| Use Case | CRF | Preset | Notes |
|----------|-----|--------|-------|
| Archive/Master | 18 | slow | Best quality, large files |
| Production | 20-22 | medium | Good balance |
| Web/Preview | 23-25 | fast | Smaller files |
| Draft/Quick | 28+ | veryfast | Fast encoding |

Preset spectrum (faster = larger files, quicker encoding):
`ultrafast` > `superfast` > `veryfast` > `faster` > `fast` > `medium` > `slow` > `slower` > `veryslow`

## References

- [reference.md](reference.md) - Codec, filter, and format lookup tables (video/audio filters, codecs, CRF range, containers, input/output options)
- [audio-processing.md](audio-processing.md) - Advanced audio: normalization, noise reduction, frequency filters, merging audio tracks
- [streaming-and-hwaccel.md](streaming-and-hwaccel.md) - HLS/DASH streaming and hardware acceleration (NVENC, VideoToolbox, QuickSync)
- [remotion.md](remotion.md) - Remotion integration: asset preparation, speed decisions, `<OffthreadVideo>` notes
- [platform-export.md](platform-export.md) - Social media export optimization (YouTube, Twitter/X, LinkedIn, Instagram, TikTok, web embed)
