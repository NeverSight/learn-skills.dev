---
name: youtube-scribe
description: Turn a YouTube URL into a readable full-sentence transcript (no timestamps) plus a TL;DR summary saved beside it. Use when the user provides a YouTube URL or asks to transcribe, summarize, or get a TL;DR of a YouTube video.
license: MIT
compatibility: Requires the baoyu-youtube-transcript skill (install separately) and bun or npx.
metadata:
  version: "1.0.0"
  openclaw:
    requires:
      anyBins:
        - bun
        - npx
---

# YouTube Scribe

Given a YouTube URL, produce a readable transcript and a TL;DR.

This skill's directory is referred to as `{baseDir}`. It contains
`scripts/yt-transcript`, a thin wrapper around the separate
**baoyu-youtube-transcript** engine.

## Prerequisites

The engine is a separate skill and is not bundled. If it is missing, the wrapper
prints the install command and stops. Install it once with:

```
npx skills add JimLiu/baoyu-skills --skill baoyu-youtube-transcript -g
```

`bun` (preferred) or `npx` is required to run the engine.

## Steps

1. Extract the YouTube URL from the user's request.
2. Run the wrapper from this skill's directory, single-quoting the URL
   (`?` is a shell glob):

   ```
   {baseDir}/scripts/yt-transcript '<youtube-url>'
   ```

   If `{baseDir}` cannot be resolved but `yt-transcript` is on `PATH`, that works too.

   Useful flags: `--out-dir <dir>` (default `./transcripts`), `--languages en,zh`
   (priority order), `--refresh` (ignore engine cache).
   If the engine is missing, show the install command the wrapper prints and stop.
3. The command prints the transcript file path (last line of stdout). Read that file.
4. Write `summary.md` in the same directory as the transcript:
   - `# TL;DR` — 3-6 bullets capturing what the video actually says.
   - `## Key points` — the main arguments in order.
   - `## Notable details` — specific facts, numbers, and names worth knowing.
   Base it on the transcript content, **not** the video description.
   If `summary.md` already exists, leave it untouched and say so (do not overwrite).
5. Reply in chat with the TL;DR bullets and both file paths
   (`transcript.md` and `summary.md`). Do not paste the whole transcript unless asked.

## Rules

- Never run the engine's `--speakers` mode; it emits raw per-chunk SRT (a few words per
  timestamp) and is unreadable. The wrapper already avoids it.
- If the transcript is too long for one pass, read it in ranges, summarize each range,
  then combine — do not truncate.
- If the command fails, show the error verbatim and stop.
