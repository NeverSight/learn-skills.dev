---
name: transcribing-youtube
description: Downloads YouTube videos, transcribes audio via OpenAI Whisper, and produces summaries stored locally. Covers yt-dlp download, audio extraction, transcription, caching, and summarization. Use when a YouTube link is shared and the user wants a transcript or summary
---

# Transcribing YouTube

Download audio from YouTube videos using yt-dlp, transcribe with OpenAI Whisper API, and summarize the content.
Transcriptions and summaries are cached in a `transcriptions/` folder to avoid redundant API calls.

## Reference Files

| File | Read When |
|------|-----------|
| `references/installation.md` | Phase 0 reports a missing dependency (yt-dlp, ffmpeg, or API key) |
| `references/troubleshooting.md` | Download fails, transcription errors, codec issues, or rate limiting |

## Prerequisites

`OPENAI_API_KEY`, `yt-dlp`, `ffmpeg`. Phase 0 checks all three and `references/installation.md` covers install steps if anything is missing.

All `scripts/` paths are **relative to the skill directory** — resolve to absolute paths before running.

## Workflow Checklist

```
- [ ] Phase 0: Verify prerequisites
- [ ] Phase 1: Check cache for existing transcription
- [ ] Phase 2: Download audio
- [ ] Phase 3: Transcribe audio
- [ ] Phase 4: Summarize transcription
- [ ] Phase 5: Save and report
```

## Phase 0: Verify Prerequisites

Run these checks. If anything is `MISSING`, read `references/installation.md` and install it before proceeding.

```bash
python -c "
import os, shutil
from pathlib import Path
key = os.environ.get('OPENAI_API_KEY', '')
if not key:
    env = Path('.env')
    if env.exists():
        for line in env.read_text().splitlines():
            if line.strip().startswith('OPENAI_API_KEY'):
                key = line.partition('=')[2].strip().strip('\"').strip(\"'\")
print('OPENAI_API_KEY:', 'OK' if key else 'MISSING')
print('yt-dlp:', 'OK' if shutil.which('yt-dlp') else 'MISSING')
print('ffmpeg:', 'OK' if shutil.which('ffmpeg') else 'MISSING')
"
```

Then ensure dependencies and output directory are ready:
```bash
pip install -r <skill-dir>/scripts/requirements.txt
mkdir -p transcriptions
```

## Phase 1: Check Cache

Before downloading anything, check if this video has already been transcribed.

The download script extracts the video ID from the URL. Check for existing files:

```bash
ls transcriptions/<VIDEO_ID>_transcript.txt 2>/dev/null && echo "CACHED" || echo "NEW"
```

Extract the video ID from common URL formats:
- `https://www.youtube.com/watch?v=VIDEO_ID` — the `v` parameter
- `https://youtu.be/VIDEO_ID` — the path segment
- `https://www.youtube.com/shorts/VIDEO_ID` — the path after `shorts/`

If cached:
- Read the existing transcript from `transcriptions/<VIDEO_ID>_transcript.txt`
- Read the existing summary from `transcriptions/<VIDEO_ID>_summary.txt` (if it exists)
- Skip to Phase 4 if only the transcript exists (to regenerate summary), or Phase 5 if both exist
- Ask the user if they want to re-transcribe (e.g., if the previous result was poor)

## Phase 2: Download Audio

Download audio only (no video) to minimize bandwidth and storage.

```bash
python scripts/download_audio.py --url "YOUTUBE_URL" --output-dir transcriptions
```

The script:
- Downloads the best available audio stream
- Converts to mp3 (Whisper accepts it and it's ~10x smaller than WAV)
- Splits files larger than 25MB into chunks (Whisper API limit)
- Outputs metadata: title, duration, video ID, file path(s)
- Names files as `<VIDEO_ID>.mp3` (or `<VIDEO_ID>_chunk_001.mp3` etc. if split)

**Output format:**
```
VIDEO_ID: dQw4w9WgXcQ
TITLE: Rick Astley - Never Gonna Give You Up
DURATION: 213
FILES: transcriptions/dQw4w9WgXcQ.mp3
STATUS: OK
```

If the video is longer than 3 hours, warn the user — transcription will be expensive and slow.
Ask for confirmation before proceeding.

## Phase 3: Transcribe Audio

Transcribe the downloaded audio using OpenAI's Whisper API.

```bash
python scripts/transcribe_audio.py --input transcriptions/<VIDEO_ID>.mp3 --output transcriptions/<VIDEO_ID>_transcript.txt
```

The script:
- Sends audio to OpenAI Whisper API (`whisper-1` model)
- Handles chunked files automatically (concatenates results)
- Saves raw transcript text to the output file
- Includes timestamps if `--timestamps` flag is passed

**For chunked audio** (files that were split in Phase 2):
```bash
python scripts/transcribe_audio.py --input-dir transcriptions --video-id <VIDEO_ID> --output transcriptions/<VIDEO_ID>_transcript.txt
```

This mode auto-discovers all `<VIDEO_ID>_chunk_*.mp3` files and transcribes them in order.

**Output:**
```
WORDS: 3847
DURATION_SECONDS: 213
OUTPUT: transcriptions/dQw4w9WgXcQ_transcript.txt
STATUS: OK
```

After transcription completes, **clean up audio files** to save disk space:
```bash
rm transcriptions/<VIDEO_ID>.mp3 transcriptions/<VIDEO_ID>_chunk_*.mp3 2>/dev/null
```

## Phase 4: Summarize Transcription

Read the transcript file and produce a summary. This is done by you (the agent), not a script.

**Audience:** Write for a smart, knowledgeable reader. Don't pad with filler or restate the obvious.
Focus on genuinely valuable insights, novel arguments, and actionable information.
Omit trivial details, pleasantries, sponsor reads, advertisements, and anything a thoughtful person could infer from context.
If the video references specific tools, websites, repos, or resources that viewers would find useful, mention them.
For tutorials and how-to content, preserve specific values, thresholds, and step sequences — these are the primary value.

1. Read `transcriptions/<VIDEO_ID>_transcript.txt`
2. Produce a summary that includes:
   - **Title** of the video
   - **Key points** — bulleted list of the most substantive ideas, arguments, or takeaways. Scale with content length: a 10-minute video might warrant 3-5 bullets, a 2-hour podcast might need 15-20. Each bullet should convey real information, not vague topic labels. Prefer "X works because Y" over "Discusses X"
   - **Detailed summary** — length should scale with the content. A short video gets a paragraph or two; a long podcast gets as many paragraphs as needed to do justice to the material. Lead with the core thesis or most important insight. Prioritize novel or non-obvious information over background context the reader likely already knows
   - **Notable quotes** — direct quotes that are especially insightful, surprising, or well-stated. Include as many as are genuinely worth preserving — could be 1 for a short video, could be 10+ for a rich long-form conversation. Skip generic motivational filler
   - **Metadata** — duration, word count, date transcribed
3. Save to `transcriptions/<VIDEO_ID>_summary.txt`

**Summary format:**
```markdown
# Video Summary: <TITLE>

**Source:** <YOUTUBE_URL>
**Duration:** <DURATION>
**Transcribed:** <DATE>
**Words:** <WORD_COUNT>

## Key Points

- Point 1
- Point 2
- ...

## Summary

<paragraphs scaled to content length>

## Notable Quotes

> "Quote 1"

> "Quote 2"
```

## Phase 5: Save and Report

1. Confirm all files are saved:
   - `transcriptions/<VIDEO_ID>_transcript.txt` — full transcript
   - `transcriptions/<VIDEO_ID>_summary.txt` — summary
2. Clean up any remaining temporary audio files
3. Report to the user:
   - Video title and duration
   - Key points from the summary
   - File paths for transcript and summary
   - Note that cached transcriptions will be reused for this video ID

## Anti-Patterns

| Avoid | Do Instead |
|-------|------------|
| Downloading full video | Download audio only (`-x` flag) — much smaller |
| Sending files over 25MB to Whisper | Split into chunks before transcribing |
| Re-downloading already transcribed videos | Check cache by video ID first |
| Keeping audio files after transcription | Delete WAV files to save disk space |
| Transcribing 3+ hour videos without asking | Warn user about cost and get confirmation |
| Using youtube-dl (unmaintained) | Use yt-dlp (actively maintained fork) |
| Hardcoding API keys in scripts | Load from env var or .env file |
| Summarizing without reading the full transcript | Always read the complete transcript before summarizing |
| Generating summary in a script | Use the agent (Claude) for summarization — better quality |

## Dependency Note

This skill requires `yt-dlp`, `openai`, and `ffmpeg`. Phase 0 checks availability; `references/installation.md` handles the rest. The only manual step for the user is providing `OPENAI_API_KEY`.
