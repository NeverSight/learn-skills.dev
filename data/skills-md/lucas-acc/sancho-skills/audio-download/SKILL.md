---
name: audio-download
description: Download audio from YouTube and Twitter/X links
metadata:
  openclaw:
    emoji: 🎵
    requires:
      bins: ["yt-dlp", "ffmpeg"]
    install:
      - id: "brew-yt-dlp"
        kind: "brew"
        formula: "yt-dlp"
        bins: ["yt-dlp"]
        label: "Install yt-dlp (brew)"
      - id: "pip-yt-dlp"
        kind: "pip"
        command: "pip install yt-dlp"
        bins: ["yt-dlp"]
        label: "Install yt-dlp (pip)"
      - id: "brew-ffmpeg"
        kind: "brew"
        formula: "ffmpeg"
        bins: ["ffmpeg"]
        label: "Install ffmpeg (brew)"
---

# Audio Download Skill

Download audio from YouTube and Twitter/X links using yt-dlp.

## Supported Platforms

- **YouTube**: Videos, Shorts, playlists
- **Twitter/X**: Posts with video/audio content

## Supported Audio Formats

- MP3 (most compatible)
- M4A (AAC audio)
- WAV (uncompressed)
- FLAC (lossless)
- OGG (Vorbis/Opus)

## Quality Options

- `0` or `best` - Best quality available
- `1` - High quality (~192kbps for MP3)
- `2` - Medium quality (~128kbps for MP3)
- `3` - Low quality (~64kbps for MP3)
- `worst` - Lowest quality available

## Basic Usage

### Download from YouTube

```bash
# Download as MP3 (best quality)
yt-dlp -x --audio-format mp3 --audio-quality 0 -o "~/Downloads/audio/%(title)s.%(ext)s" "<YOUTUBE_URL>"

# Download YouTube Shorts as M4A
yt-dlp -x --audio-format m4a --audio-quality 0 -o "~/Downloads/audio/%(title)s.%(ext)s" "<SHORTS_URL>"
```

### Download from Twitter/X

```bash
# Download audio from tweet as MP3
yt-dlp -x --audio-format mp3 --audio-quality 0 -o "~/Downloads/audio/%(title)s.%(ext)s" "<TWITTER_URL>"
```

### Common Options

```bash
# List available formats (without downloading)
yt-dlp -F "<URL>"

# Download specific format code
yt-dlp -f <FORMAT_CODE> -o "~/Downloads/audio/%(title)s.%(ext)s" "<URL>"

# Download with metadata/thumbnail
yt-dlp -x --audio-format mp3 --embed-metadata --embed-thumbnail -o "~/Downloads/audio/%(title)s.%(ext)s" "<URL>"
```

## Python Helper Script

For batch operations or playlists, use the helper script:

```bash
# Basic download
python {baseDir}/scripts/download.py "<URL>"

# Specify format and output directory
python {baseDir}/scripts/download.py "<URL>" --format mp3 --output ~/Downloads/audio

# Download with specific quality
python {baseDir}/scripts/download.py "<URL>" --format m4a --quality best

# Download first 3 items from playlist only
python {baseDir}/scripts/download.py "<PLAYLIST_URL>" --playlist-items 3
```

## Output Template Variables

Use these variables in the `-o` output template:

- `%(title)s` - Video title
- `%(uploader)s` - Channel/username
- `%(upload_date)s` - Upload date (YYYYMMDD)
- `%(duration)s` - Duration in seconds
- `%(id)s` - Video ID
- `%(ext)s` - File extension

Example with custom naming:
```bash
yt-dlp -x --audio-format mp3 -o "~/Downloads/audio/%(uploader)s - %(title)s [%(id)s].%(ext)s" "<URL>"
```

## Troubleshooting

### Update yt-dlp

If downloads fail, update yt-dlp to the latest version:

```bash
# If installed via brew
brew upgrade yt-dlp

# If installed via pip (ensure conda environment is activated)
conda activate default
pip install -U yt-dlp
```

### Common Issues

**"ffmpeg not found"**: Install ffmpeg - it's required for audio format conversion.

**"Video unavailable"**: Some videos may be region-restricted or require authentication.

**Slow downloads**: Add `--concurrent-fragments 5` to download multiple fragments in parallel.
