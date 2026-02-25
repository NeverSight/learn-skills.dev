---
name: watch-youtube
description: Watch and analyze YouTube videos using Gemini's video understanding API. Pass any YouTube URL to get summaries, timestamps, Q&A, or detailed analysis of video content — audio and visual.
---

# Watch YouTube

Use Google's Gemini API to actually *watch* YouTube videos and answer questions about them.

## How It Works

Gemini processes both audio and visual streams of YouTube videos at 1 FPS. You pass a URL + prompt, it returns analysis.

## When to Use

- User shares a YouTube URL and wants a summary, transcript, or analysis
- User asks "what did they say about X in this video?"
- User wants timestamps of key moments
- User wants to compare multiple videos (up to 10 per request with Gemini 2.5+)

## When NOT to Use

- Private or unlisted videos (only public videos work)
- User just wants the video link or metadata

## Setup

Requires `GOOGLE_API_KEY` environment variable. Get one free at https://aistudio.google.com/apikey

## Usage

Run the script:
```bash
GOOGLE_API_KEY="$GOOGLE_API_KEY" python3 ~/.openclaw/workspace/skills/watch-youtube/watch.py "<youtube_url>" "<prompt>"
```

### Examples

**Summarize:**
```bash
watch.py "https://www.youtube.com/watch?v=VIDEO_ID" "Summarize this video in 5 bullet points"
```

**Timestamps:**
```bash
watch.py "https://www.youtube.com/watch?v=VIDEO_ID" "List the key moments with timestamps"
```

**Q&A:**
```bash
watch.py "https://www.youtube.com/watch?v=VIDEO_ID" "What tools or products did they mention?"
```

**Specific section:**
```bash
watch.py "https://www.youtube.com/watch?v=VIDEO_ID" "What happens at 05:30?" 
```

## Limits

- **Free tier:** 8 hours of YouTube video per day
- **Paid tier:** No limit
- **Max videos per request:** 10 (Gemini 2.5+)
- **Max video length:** ~1 hour (1M context), ~3 hours (low res)
- **~300 tokens per second** of video

## Models

- `gemini-2.5-flash` — fast, cheap, good for most use cases
- `gemini-2.5-pro` — deeper analysis, longer videos
- `gemini-3-flash-preview` — latest, best quality
