---
name: video-processing
description: Download videos from YouTube/Facebook, extract audio tracks, transcribe audio to text using faster-whisper, and analyze videos with scene detection, keyframe extraction, and subtitle generation
license: MIT
compatibility: opencode
metadata:
  language: node
  capabilities:
    - video-download
    - audio-extraction
    - speech-transcription
    - scene-detection
    - subtitle-generation
---

## What I do

- **Download Videos** - Fetch videos from YouTube, Facebook, and other platforms
- **Extract Audio** - Pull audio tracks from video files in various formats (MP3, WAV, AAC, etc.)
- **Transcribe Audio** - Convert speech to text with word-level timestamps using faster-whisper (supports Bengali and English)
- **Analyze Videos** - Detect scenes, extract keyframes, generate thumbnails and subtitles

## Commands

### Download a video
```
video download <url> [--output <path>] [--format <mp4|webm>] [--quality <quality>]
```

### Extract audio from video
```
video extract-audio <video> [--output <path>] [--format <mp3|wav|aac>] [--bitrate <kbps>]
```

### Transcribe video to text
```
video transcribe <video> [--output <path>] [--format <json|srt|vtt>] [--language <code>]
```

### Analyze video comprehensively
```
video analyze <video> [--output <path>] [--threshold <0.0-1.0>] [--interval <seconds>]
```

## Requirements

- Node.js 18+
- FFmpeg (system installation required)
- faster-whisper (CTranslate2-based Whisper implementation for faster local transcription)

## Usage examples

```bash
# Download YouTube video
video download "https://youtube.com/watch?v=..." --output ./videos

# Extract MP3 from video
video extract-audio ./video.mp4 --format mp3 --bitrate 320k

# Generate subtitles
video transcribe ./video.mp4 --format srt --language en

# Analyze video with scene detection
video analyze ./video.mp4 --threshold 0.3
```

## When to use me

Use this skill when you need to:
- Save online videos for offline viewing
- Convert video content to audio (podcasts, music)
- Create subtitles or transcripts from video content
- Analyze video structure for editing or highlights
