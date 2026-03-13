---
name: YouTube Transcript Extractor
description: Extracts timestamped transcripts from YouTube videos for translation, summarization, and content creation.
---

# YouTube Transcript Extractor

## What You Get

- **Terminal Output**: Prints the transcript with `[HH:MM:SS]` timestamps.
- **Local File**: Writes `youtube_transcript_{video_id}.txt` in the **current working directory**.
  - Includes the source video URL and the full transcript content.

## Requirements

- Python 3.9+ (Recommended)
- Network environment that can access YouTube transcript APIs.
- Python Dependencies:
  - `youtube-transcript-api`

## Quick Start

### Step 1: (Optional) Create a Virtual Environment

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -U pip
```

### Step 2: Install Dependencies

```bash
python -m pip install youtube-transcript-api
```

### Step 3: Extract Transcript

Run from the repository root (recommended for the clearest path):

```bash
python skills/youtube-transcript-extractor/scripts/get_youtube_transcript.py "https://www.youtube.com/watch?v=IDSAMqip6ms"
```

- The transcript will be saved to `youtube_transcript_{video_id}.txt` in the current working directory.

## Step 4: Convert Transcript to Reader-Friendly Markdown

Output `youtube_transcript_{video_id}.md`. Note: Ensure the content is not altered or truncated.
