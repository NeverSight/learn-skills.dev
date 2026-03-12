---
name: video-audio-extractor
description: Extract audio from video files or URLs (including YouTube). Supports MP3, WAV, M4A, FLAC, OGG, and OPUS formats. Can process local video files or download from URLs. For YouTube videos, uses yt-dlp for direct audio extraction when possible.
homepage: https://ffmpeg.org
metadata:
  {
    "openclaw":
      {
        "emoji": "🎵",
        "requires": { "bins": ["ffmpeg", "python3"] },
        "optional": { "bins": ["yt-dlp"] },
        "install":
          [
            {
              "id": "brew",
              "kind": "brew",
              "formula": "ffmpeg",
              "bins": ["ffmpeg"],
              "label": "Install ffmpeg (brew)",
            },
            {
              "id": "pip",
              "kind": "pip",
              "package": "yt-dlp",
              "bins": ["yt-dlp"],
              "label": "Install yt-dlp for YouTube support (pip3 install yt-dlp)",
            },
          ],
      },
  }
---

# Video Audio Extractor

Extract audio from video files or URLs. Supports various output formats including MP3, WAV, M4A, FLAC, OGG, and OPUS.

## Features

- ✅ Extract audio from local video files
- ✅ Download and extract from direct video URLs
- ✅ **YouTube support** - Direct audio extraction (requires yt-dlp)
- ✅ Multiple output formats with quality control
- ✅ Automatic cleanup of temporary files

## Prerequisites

```bash
# Required
brew install ffmpeg

# Optional - for YouTube support
pip3 install yt-dlp
```

## Quick Start

### Extract from local file

```bash
{baseDir}/scripts/extract-audio.py video.mp4
# Creates: video.mp3
```

### Extract from YouTube

```bash
{baseDir}/scripts/extract-audio.py "https://youtube.com/watch?v=..."
```

### Different formats

```bash
{baseDir}/scripts/extract-audio.py video.mp4 -f wav    # WAV format
{baseDir}/scripts/extract-audio.py video.mp4 -f m4a    # Apple format
{baseDir}/scripts/extract-audio.py video.mp4 -f flac   # Lossless
```

## Usage

```
extract-audio.py [-h] [-o OUTPUT] [-f {mp3,wav,m4a,aac,flac,ogg,opus}]
                 [-b BITRATE] [-r SAMPLE_RATE] [--keep-video] [--video-only]
                 input
```

## Options

| Option | Description | Default |
|--------|-------------|---------|
| `input` | Video file path or URL | (required) |
| `-o, --output` | Output audio file path | Auto-generated |
| `-f, --format` | Output format | mp3 |
| `-b, --bitrate` | Audio bitrate | 192k |
| `-r, --sample-rate` | Sample rate (Hz) | Original |
| `--keep-video` | Keep downloaded video | Delete after |
| `--video-only` | Download video without extracting | Disabled |

## Supported Formats

| Format | Codec | Notes |
|--------|-------|-------|
| **MP3** | libmp3lame | Best compatibility |
| **WAV** | pcm_s16le | Uncompressed, large files |
| **M4A** | AAC | Apple ecosystem |
| **FLAC** | FLAC | Lossless compression |
| **OGG** | Vorbis | Open format |
| **OPUS** | Opus | Streaming optimized |

## Examples

### High quality MP3

```bash
{baseDir}/scripts/extract-audio.py video.mp4 -b 320k -r 48000
```

### YouTube to M4A

```bash
{baseDir}/scripts/extract-audio.py "https://youtu.be/xxxxx" -f m4a
```

### Custom output location

```bash
{baseDir}/scripts/extract-audio.py video.mp4 -o ~/Music/my-song.mp3
```

### Download YouTube video (keep it)

```bash
{baseDir}/scripts/extract-audio.py "https://youtube.com/watch?v=..." --video-only --keep-video
```

## YouTube Support

For YouTube videos, the tool uses `yt-dlp` to extract audio directly when possible. This is faster and more efficient than downloading the full video.

### YouTube Limitations

YouTube actively blocks automated downloads. If you encounter errors:

1. **Update yt-dlp**: `pip3 install -U yt-dlp`
2. **Try different URLs** - Some videos have stricter restrictions
3. **Use --video-only** to download the video first, then extract
4. **Browser extension** - Use a YouTube downloader extension, then process the file

### Common YouTube Errors

- **403 Forbidden**: YouTube blocked the request. Try updating yt-dlp or use a different video.
- **Sign in required**: Video requires authentication. Use browser download instead.
- **Timeout**: Video too large or connection slow. Try `--video-only` first.

## Technical Details

- Uses **ffmpeg** for audio extraction
- Uses **yt-dlp** for YouTube downloads
- Downloads to temporary directory, auto-cleanup by default
- Preserves original audio codec when possible
- Progress indicators for long operations
