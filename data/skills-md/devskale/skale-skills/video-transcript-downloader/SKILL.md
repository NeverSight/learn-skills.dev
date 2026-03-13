---
name: video-transcript-downloader
description: Download videos, audio, subtitles, and clean paragraph-style transcripts from YouTube and any other yt-dlp supported site. Transcripts are saved to file by default. Use when asked to “download this video”, “save this clip”, “rip audio”, “get subtitles”, “get transcript”, or to troubleshoot yt-dlp/ffmpeg and formats/playlists.
---

# Video Transcript Downloader

`./scripts/vtd.js` can:

- Print a transcript as a clean paragraph (timestamps optional).
- Download video/audio/subtitles.

Transcript behavior:

- YouTube: fetch via `youtube-transcript-plus` when possible.
- Otherwise: pull subtitles via `yt-dlp`, then clean into a paragraph.

## Setup

Run the installation script to set up dependencies (including `yt-dlp` in a virtual environment):

```bash
./install.sh
```

## Transcript (default: save to current directory)

Transcripts are saved to `./YYYY-MM-DD_title-short.md` (current directory) by default. This is the intended behavior for all transcript requests unless `--no-file` is explicitly requested.

**Note for AI Agent:** When you run the `transcript` or `search` command, the script will output the path to the saved file. Your task is complete once the file is saved. Simply provide the file path to the user. Do not ask if they want to save it; it has already been saved.

```bash
./scripts/vtd.js transcript --url 'https://…'
./scripts/vtd.js transcript --url 'https://…' --lang en
./scripts/vtd.js transcript --url 'https://…' --timestamps
./scripts/vtd.js transcript --url 'https://…' --keep-brackets
./scripts/vtd.js transcript --url 'https://…' --no-file  # Print to console instead
```

## Search

Search for videos and download transcripts (default limit: 1). Auto-detects "top N" in query. Transcripts are saved to file by default.

```bash
./scripts/vtd.js search "top 3 ai videos on reinforcement learning"
./scripts/vtd.js search "nextjs tutorial" --limit 5
./scripts/vtd.js search "..." --no-file --timestamps
```

## Download video / audio / subtitles

```bash
./scripts/vtd.js download --url 'https://…' --output-dir ~/Downloads
./scripts/vtd.js audio --url 'https://…' --output-dir ~/Downloads
./scripts/vtd.js subs --url 'https://…' --output-dir ~/Downloads --lang en
```

## Formats (list + choose)

List available formats (format ids, resolution, container, audio-only, etc):

```bash
./scripts/vtd.js formats --url 'https://…'
```

Download a specific format id (example):

```bash
./scripts/vtd.js download --url 'https://…' --output-dir ~/Downloads -- --format 137+140
```

Prefer MP4 container without re-encoding (remux when possible):

```bash
./scripts/vtd.js download --url 'https://…' --output-dir ~/Downloads -- --remux-video mp4
```

## Notes

- Default transcript output is a single paragraph. Use `--timestamps` only when asked.
- Bracketed cues like `[Music]` are stripped by default; keep them via `--keep-brackets`.
- By default, transcripts are saved to the current directory (`./`).
  - **Agent behavior:** If the script outputs a file path, the transcript is already saved. Inform the user of the location.
  - Use `--no-file` to print to stdout instead if User requests it.
  - Pass extra `yt-dlp` args after `--` for `transcript` fallback, `download`, `audio`, `subs`, `formats`.

```bash
./scripts/vtd.js formats --url 'https://…' -- -v
```

## Troubleshooting (only when needed)

- Missing `yt-dlp` / `ffmpeg`:

Run `./install.sh` to fix missing `yt-dlp`. For `ffmpeg` (required for audio conversion):

```bash
brew install ffmpeg
```

- Verify:

```bash
./scripts/vtd.js --help
```
