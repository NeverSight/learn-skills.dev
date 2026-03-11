---
name: video-processing
description: "Process video files with ffmpeg automation. Use when: compressing videos for upload; extracting audio from video; resizing for social formats; clipping segments; merging multiple videos; generating thumbnails"
license: MIT
metadata:
  author: ClawFu
  version: 1.0.0
  mcp-server: "@clawfu/mcp-skills"
---

# Video Processing

> Automate repetitive video editing tasks using FFmpeg - the industry-standard tool powering YouTube, Netflix, and most video platforms.

## When to Use This Skill

- **Social media optimization** - Resize videos for Instagram (9:16), TikTok, LinkedIn
- **Upload preparation** - Compress large videos to meet platform limits
- **Audio extraction** - Pull audio from webinars, interviews for podcasts
- **Content clipping** - Extract highlights, quotes, or segments
- **Batch processing** - Apply same operations to multiple videos


## What Claude Does vs What You Decide

| Claude Does | You Decide |
|-------------|------------|
| Structures production workflow | Final creative direction |
| Suggests technical approaches | Equipment and tool choices |
| Creates templates and checklists | Quality standards |
| Identifies best practices | Brand/voice decisions |
| Generates script outlines | Final script approval |

## Dependencies

```bash
pip install ffmpeg-python moviepy click
# Also requires ffmpeg installed on system
# macOS: brew install ffmpeg
# Ubuntu: sudo apt install ffmpeg
```

## Commands

### Compress Video
```bash
python scripts/main.py compress video.mp4 --target-mb 10
python scripts/main.py compress video.mp4 --crf 28 --output compressed.mp4
```

### Extract Audio
```bash
python scripts/main.py extract-audio video.mp4 --format mp3
python scripts/main.py extract-audio video.mp4 --format wav --output audio.wav
```

### Resize for Social
```bash
python scripts/main.py resize video.mp4 --format instagram  # 1080x1920 (9:16)
python scripts/main.py resize video.mp4 --format youtube    # 1920x1080 (16:9)
python scripts/main.py resize video.mp4 --format square     # 1080x1080 (1:1)
python scripts/main.py resize video.mp4 --width 1280 --height 720
```

### Clip Segment
```bash
python scripts/main.py clip video.mp4 --start 00:30 --end 01:45
python scripts/main.py clip video.mp4 --start 00:30 --duration 60
```

### Merge Videos
```bash
python scripts/main.py concat video1.mp4 video2.mp4 --output merged.mp4
python scripts/main.py concat ./clips/ --output compilation.mp4
```

### Generate Thumbnail
```bash
python scripts/main.py thumbnail video.mp4 --time 00:30
python scripts/main.py thumbnail video.mp4 --best  # Auto-select best frame
```

## Examples

### Example 1: Prepare Video for Instagram Reels
```bash
# Original: 4K horizontal video, 500MB
python scripts/main.py resize long-video.mp4 --format instagram
python scripts/main.py compress long-video_instagram.mp4 --target-mb 50

# Output: long-video_instagram_compressed.mp4 (1080x1920, <50MB)
```

### Example 2: Extract Podcast from Webinar
```bash
# Extract audio track
python scripts/main.py extract-audio webinar-recording.mp4 --format mp3 --bitrate 192k

# Output: webinar-recording.mp3 (ready for podcast hosting)
```

### Example 3: Create Highlight Reel
```bash
# Extract multiple clips
python scripts/main.py clip interview.mp4 --start 05:30 --end 06:15 --output clip1.mp4
python scripts/main.py clip interview.mp4 --start 12:00 --end 12:45 --output clip2.mp4
python scripts/main.py clip interview.mp4 --start 28:30 --end 29:00 --output clip3.mp4

# Merge into highlight reel
python scripts/main.py concat clip1.mp4 clip2.mp4 clip3.mp4 --output highlights.mp4
```

## Social Media Format Reference

| Platform | Format | Resolution | Max Size | Max Duration |
|----------|--------|------------|----------|--------------|
| Instagram Reels | 9:16 | 1080x1920 | 4GB | 90s |
| Instagram Feed | 1:1 | 1080x1080 | 4GB | 60s |
| TikTok | 9:16 | 1080x1920 | 287MB | 10min |
| YouTube Shorts | 9:16 | 1080x1920 | - | 60s |
| YouTube | 16:9 | 1920x1080 | 256GB | 12h |
| LinkedIn | 1:1/16:9 | 1920x1080 | 5GB | 10min |
| Twitter/X | 16:9 | 1920x1080 | 512MB | 2:20 |

## Performance Tips

1. **GPU acceleration** - FFmpeg uses hardware encoding when available (NVENC, VideoToolbox)
2. **CRF values** - Lower = better quality, larger file. 18-28 typical range
3. **Preset selection** - `ultrafast` for drafts, `slow` for final exports
4. **Two-pass encoding** - Better quality for target bitrate

## Skill Boundaries

### What This Skill Does Well
- Structuring audio production workflows
- Providing technical guidance
- Creating quality checklists
- Suggesting creative approaches

### What This Skill Cannot Do
- Replace audio engineering expertise
- Make subjective creative decisions
- Access or edit audio files directly
- Guarantee commercial success

## Related Skills

- [whisper-transcription](../whisper-transcription/) - Transcribe video audio
- [youtube-downloader](../youtube-downloader/) - Download videos to process
- [image-batch](../image-batch/) - Process video thumbnails

## Skill Metadata


- **Mode**: cyborg
```yaml
category: automation
subcategory: video-processing
dependencies: [ffmpeg-python, moviepy]
difficulty: beginner
time_saved: 5+ hours/week
```
