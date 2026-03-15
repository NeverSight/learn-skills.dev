---
name: youtube-dl
description: "Download video or extract audio from YouTube and other video sites. Use this skill when the user asks to download a YouTube video, extract audio from a video URL, save a video from the internet, convert a YouTube video to MP3, or download media from supported sites."
tags: [youtube, video, audio, download, yt-dlp, mp3, media, utility]
version: 0.1.0
---

# Skill: youtube-dl

## When to Use

Use this skill when the user asks to:

- Download a YouTube video
- Extract audio from a YouTube video
- Save a video from the internet
- Convert a YouTube video to MP3/audio
- Download video or audio from any supported site
- Get the audio track from a video URL

## Supported Sites

yt-dlp supports 1000+ sites including:

- YouTube, YouTube Music
- Vimeo, Dailymotion
- Twitter/X, Reddit, TikTok
- SoundCloud, Bandcamp
- And many more (run `yt-dlp --list-extractors` for full list)

## Input Parameters

| Parameter | Required | Description                           | Example                         |
| --------- | -------- | ------------------------------------- | ------------------------------- |
| `url`     | Yes      | Video/audio URL                       | https://youtube.com/watch?v=xxx |
| `format`  | No       | `video` (default) or `audio`          | audio                           |
| `quality` | No       | `best` (default), `720`, `480`, `360` | best                            |
| `output`  | No       | Output directory or file path         | ~/Downloads/                    |

## Procedure

1. Get the URL from the user's request
2. Determine if they want video or audio
3. Run the bundled script:

   ```bash
   # Download video (best quality)
   python3 skills/youtube-dl/scripts/download.py "https://youtube.com/watch?v=xxx"

   # Extract audio only (MP3)
   python3 skills/youtube-dl/scripts/download.py "https://youtube.com/watch?v=xxx" --format audio

   # Specific quality
   python3 skills/youtube-dl/scripts/download.py "https://youtube.com/watch?v=xxx" --quality 720

   # Custom output directory
   python3 skills/youtube-dl/scripts/download.py "https://youtube.com/watch?v=xxx" --output ~/Downloads/
   ```

4. The script auto-installs `yt-dlp` if needed
5. Report the downloaded file path and details to the user

## Bundled Scripts

| Script                | Type   | Description                       |
| --------------------- | ------ | --------------------------------- |
| `scripts/download.py` | Python | Download video/audio using yt-dlp |

### Script Usage

```bash
# Download best quality video
python3 scripts/download.py "https://youtube.com/watch?v=dQw4w9WgXcQ"

# Audio only (extracts to best available audio format)
python3 scripts/download.py "https://youtube.com/watch?v=dQw4w9WgXcQ" --format audio

# Specific video quality
python3 scripts/download.py "https://youtube.com/watch?v=dQw4w9WgXcQ" --quality 720

# Custom output location
python3 scripts/download.py "https://youtube.com/watch?v=dQw4w9WgXcQ" --output ~/Music/

# Show video info without downloading
python3 scripts/download.py "https://youtube.com/watch?v=dQw4w9WgXcQ" --info
```

## Example

```
download this youtube video: https://youtube.com/watch?v=xxx
extract the audio from this video
save this video as mp3
download the video in 720p
get the audio from this youtube link
```
