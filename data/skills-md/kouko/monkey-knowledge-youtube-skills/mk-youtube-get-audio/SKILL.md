---
name: mk-youtube-get-audio
description: Download YouTube video audio file. Use when user wants to extract audio or download music/podcast from a video.
license: MIT
metadata:
  version: 1.1.1
  author: kouko
  tags:
    - youtube
    - audio
    - download
compatibility:
  claude-code: ">=1.0.0"
---

# YouTube Audio Download

Download video audio file (best available format, no conversion).

## Quick Start

```
/mk-youtube-get-audio <URL> [output_dir] [browser] [--force]
```

## Parameters

| Parameter | Required | Default | Description |
|-----------|----------|---------|-------------|
| URL | Yes | - | YouTube video URL |
| output_dir | No | /tmp/monkey_knowledge/youtube/audio | Output directory for audio file |
| browser | No | auto | Browser for cookies (chrome, firefox, safari, edge, brave) |
| --force | No | false | Force re-download even if cached file exists |

## Examples

- `/mk-youtube-get-audio https://youtube.com/watch?v=xxx` - Download with auto cookie fallback
- `/mk-youtube-get-audio https://youtube.com/watch?v=xxx ~/Music` - Save to custom directory
- `/mk-youtube-get-audio https://youtube.com/watch?v=xxx /tmp chrome` - Use Chrome cookies

## How it Works

1. Execute: `{baseDir}/scripts/audio.sh "<URL>" "<output_dir>" "<browser>"`
2. First attempt: download without authentication
3. If failed: retry with browser cookies (auto-detect or specified)
4. Parse JSON output to get file path

```
┌─────────────────────────────┐
│   First attempt (no auth)   │
└──────────────┬──────────────┘
               │
       ┌───────┴───────┐
       │               │
    Success         Failed
       │               │
       ▼               ▼
   [Return]    ┌─────────────────────┐
               │ Retry with cookies  │
               │ chrome → firefox →  │
               │ safari → edge →     │
               │ brave               │
               └──────────┬──────────┘
                          │
                  ┌───────┴───────┐
                  │               │
               Success         Failed
                  │               │
                  ▼               ▼
              [Return]        [Error]
```

## Output Format

Success:
```json
{
  "status": "success",
  "file_path": "/tmp/monkey_knowledge/youtube/audio/20091025__VIDEO_ID.m4a",
  "file_size": "5.2M",
  "cached": false,
  "video_id": "dQw4w9WgXcQ",
  "title": "Video Title",
  "channel": "Channel Name",
  "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
  "duration_string": "3:32"
}
```

**Cache hit** (returns existing file):
```json
{
  "status": "success",
  "file_path": "/tmp/monkey_knowledge/youtube/audio/20091025__VIDEO_ID.m4a",
  "file_size": "5.2M",
  "cached": true,
  ...
}
```

Error:
```json
{
  "status": "error",
  "message": "Download failed (tried with and without cookies)"
}
```

## Filename Format

Files use unified naming with date prefix: `{YYYYMMDD}__{video_id}.{ext}`

Example: `20091025__dQw4w9WgXcQ.m4a`

## Browser Cookie Fallback

When download fails (e.g., member-only or age-restricted content), the script automatically:

1. Tries each browser: chrome → firefox → safari → edge → brave
2. For Chrome: tries all profiles (Default, Profile 1, Profile 2, ...)
3. Uses first successful browser/profile combination

Supported browsers:

| Browser | Parameter | Chrome Profile Support |
|---------|-----------|------------------------|
| Chrome | `chrome` | Yes (auto-detect all profiles) |
| Firefox | `firefox` | Default profile only |
| Safari | `safari` | Default profile only |
| Edge | `edge` | Default profile only |
| Brave | `brave` | Default profile only |

## Use Cases

- Download audio for speech-to-text when video has no subtitles
- Podcast or music download
- Member-only or age-restricted content (with browser cookies)

## Notes

- **File caching**: If audio file already exists for this video, it will be reused (returns `cached: true`)
- **Force refresh**: Use `--force` flag to re-download even if cached file exists
- Uses system yt-dlp/jq if available, otherwise auto-downloads on first run
- No ffmpeg required (uses best available format without conversion)
- Output format depends on source (typically m4a, webm, or opus)
- Cookie fallback only activates when initial download fails
- Using cookies may risk YouTube account suspension - use secondary account if needed

## Next Step

After downloading the audio, invoke `/mk-youtube-audio-transcribe` with the `file_path` from the output:

```
/mk-youtube-audio-transcribe <file_path> [model] [language]
```

**Tip**: If you know the video's language from `/mk-youtube-get-info`, pass it as the language parameter for better model auto-selection (e.g., `zh` → belle-zh, `ja` → kotoba-ja).
