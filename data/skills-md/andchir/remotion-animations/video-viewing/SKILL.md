---
name: video-viewing
description: Download, view, and analyze video files from direct URLs. Use this skill when the user asks to download, save, view, or analyze video files from direct links (mp4, webm, mkv, avi, mov files). Does NOT support YouTube or other streaming platforms - only direct video file URLs.
---

# Video Viewing and Analysis

Download and analyze video files from direct URLs with frame extraction and metadata retrieval.

## Quick Start

The simplest way to download a video:

```bash
python scripts/download_video.py "https://example.com/video.mp4"
```

This downloads the video to `/mnt/user-data/outputs/` (or current directory if not available).

## Options

### Custom Output Directory

Use `-o` or `--output` to specify a different output directory:

```bash
python scripts/download_video.py "URL" -o /path/to/directory
```

### Custom Filename

Use `-n` or `--name` to specify a custom filename (without extension):

```bash
python scripts/download_video.py "URL" -n my_video
```

### Extract Frames

Use `-f` or `--frames` to extract key frames from the video:

```bash
python scripts/download_video.py "URL" -f
```

This extracts frames at regular intervals and saves them as images for visual analysis.

### Get Video Info

Use `-i` or `--info` to get video metadata without downloading:

```bash
python scripts/download_video.py "URL" -i
```

This displays duration, resolution, codec, frame rate, and file size.

## Complete Examples

1. Download video with default settings:
```bash
python scripts/download_video.py "https://previews.customer.envatousercontent.com/h264-video-previews/dfb637cb-f04e-46dc-99dc-256fa6090958/61509131.mp4"
```

2. Download and extract frames for analysis:
```bash
python scripts/download_video.py "https://example.com/video.mp4" -f
```

3. Get video information only:
```bash
python scripts/download_video.py "https://example.com/video.mp4" -i
```

4. Download to custom directory with custom name:
```bash
python scripts/download_video.py "https://example.com/video.mp4" -o /custom/path -n my_video
```

## How It Works

The skill uses standard Python libraries to:
- Download video files using `requests` with streaming support
- Extract video metadata using `ffprobe` (part of ffmpeg)
- Extract key frames using `ffmpeg`
- Support resume for partially downloaded files

## Viewing Downloaded Videos

After downloading, Claude can analyze the video content by:
1. Extracting frames at key intervals
2. Analyzing the extracted images to describe video content
3. Providing metadata about duration, resolution, and format

## Requirements

The script requires:
- Python 3.7+
- `requests` library (installed automatically)
- `ffmpeg` and `ffprobe` for frame extraction and metadata (optional)

Install ffmpeg on Ubuntu/Debian:
```bash
sudo apt-get install ffmpeg
```

Install ffmpeg on macOS:
```bash
brew install ffmpeg
```

## Important Notes

- Only supports direct video file URLs (not streaming platforms like YouTube)
- Supported formats: mp4, webm, mkv, avi, mov, m4v, wmv, flv
- Large files are downloaded with progress indication
- Frame extraction requires ffmpeg to be installed
- Downloads are saved to `/mnt/user-data/outputs/` by default, or current directory
