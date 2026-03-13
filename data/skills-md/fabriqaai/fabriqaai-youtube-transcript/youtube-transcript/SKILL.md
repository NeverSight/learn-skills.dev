---
name: youtube-transcript
description: Retrieve YouTube transcripts without MCP using a Python CLI tool. Use when a user asks for full transcript text or available transcript languages from a YouTube URL or video ID. For summaries, key points, or quotes, use AI summarization (prefer a sub-agent when available) to save main-context tokens.
---

# YouTube Transcript Skill

Use this skill to fetch transcripts and transcript languages with a standalone Python CLI tool (no MCP server).

## Prerequisites

Install dependency:

```bash
python3 -m pip install youtube-transcript-api
```

## Package Knowledge: `youtube-transcript-api`

Teach and apply these package facts when reasoning about failures or writing code:

- Package role:
- fetch transcript text for a YouTube video
- list available transcript languages
- detect generated vs manual captions

- Common API patterns across versions:
- static-style: `YouTubeTranscriptApi.get_transcript(video_id, languages=[...])`
- class list: `YouTubeTranscriptApi.list_transcripts(video_id)`
- instance-style (newer variants): `api = YouTubeTranscriptApi(); api.list(video_id); api.fetch(video_id, languages=[...])`

- Typical transcript item fields:
- `text`
- `start`
- `duration`

- Typical language fields:
- `language_code`
- `language`
- `is_generated`

- Common exception names you should expect and map:
- `InvalidVideoId`
- `TranscriptsDisabled`
- `NoTranscriptFound`
- `VideoUnavailable`
- `TooManyRequests`
- `CouldNotRetrieveTranscript`

- Reliability guidance:
- try requested language first, then fallback to first available language
- for AI summary workflows, prefer transcript retrieval with `--include-timestamps false`
- keep tool output structured JSON so downstream AI agents can parse reliably

## Core Contract

This skill provides transcript retrieval. Summary and analysis must be done by AI.

- Use the CLI for data retrieval (`transcript`, `languages`).
- Do summary/key points/quotes using an AI agent.
- Prefer sub-agent summarization when available to preserve main-context space.

## Workflow

1. Extract a YouTube URL or 11-character video ID.
2. Decide output type:
- Full transcript requested: fetch transcript and return it.
- Summary requested: fetch transcript first, then summarize with AI.
3. Context-saving rule for summary:
- If sub-agents are available, run transcript retrieval + summarization in a sub-agent.
- If sub-agents are unavailable, summarize in the current agent after retrieval.
4. For long videos, prefer transcript fetch with `--include-timestamps false` unless timestamps are explicitly requested.

## Sub-Agent Guidance

When available, use this flow:

1. Sub-agent runs transcript fetch command.
2. Sub-agent summarizes transcript based on user intent.
3. Sub-agent returns concise summary (and optional key quotes).
4. Main agent returns the synthesized result without dumping full raw transcript unless the user asks.

## Commands

Get transcript with timestamps:

```bash
python3 youtube_transcript_tool.py \
  --mode transcript \
  --url "https://www.youtube.com/watch?v=VIDEO_ID" \
  --lang en \
  --include-timestamps true
```

Get transcript as plain text (recommended for summarization):

```bash
python3 youtube_transcript_tool.py \
  --mode transcript \
  --url "VIDEO_ID" \
  --include-timestamps false
```

List available transcript languages:

```bash
python3 youtube_transcript_tool.py \
  --mode languages \
  --url "https://youtu.be/VIDEO_ID"
```

## Output Contract

Default output is JSON (`--json true`).

Success payload:
- `ok: true`
- includes `mode`, `video_id`, and mode-specific payload

Error payload:
- `ok: false`
- `error.code`
- `error.message`
- `error.hint`

Use `--json false` for readable text output.

## Error Handling Guidance

When the tool fails, surface the hint directly and suggest one practical next step:

- `invalid_video_id`: check URL format or use raw 11-char ID
- `transcripts_disabled`: captions disabled by publisher
- `no_transcript`: try another language or auto-generated captions
- `video_unavailable`: video is private/deleted/restricted
- `rate_limited`: retry later or from a different network
- `dependency_missing`: install `youtube-transcript-api`

## Defaults

- `--lang en`
- `--include-timestamps true`
- `--json true`
