---
name: audio-transcriber
description: Transcribe audio/video files to text using OpenAI Whisper.
status: implemented
arguments:
  - name: file
    short: f
    type: string
    required: true
  - name: key
    short: k
    type: string
    description: OpenAI API Key
  - name: out
    short: o
    type: string
category: Interface & AI
last_updated: '2026-02-13'
tags:
  - gemini-skill
---

# Audio Transcriber

Transcribe audio/video files to text using OpenAI Whisper.

## Usage

node audio-transcriber/scripts/transcribe.cjs [options]

## Troubleshooting

| Error                                 | Cause                         | Fix                                                                    |
| ------------------------------------- | ----------------------------- | ---------------------------------------------------------------------- |
| `ffmpeg: command not found`           | FFmpeg not installed          | Install: `brew install ffmpeg` (macOS) or `apt install ffmpeg` (Linux) |
| `Cannot find module 'openai'`         | OpenAI SDK not installed      | Run `npm install openai`                                               |
| `OPENAI_API_KEY is not set`           | API key missing               | Set `export OPENAI_API_KEY=sk-...` in your shell                       |
| `Error: 413 Request Entity Too Large` | Audio file exceeds 25MB limit | Split file: `ffmpeg -i input.mp3 -ss 0 -t 600 part1.mp3`               |
| `Unsupported audio format`            | File format not recognized    | Convert to mp3/wav: `ffmpeg -i input.ogg output.mp3`                   |

## Knowledge Protocol

- This skill adheres to the `knowledge/orchestration/knowledge-protocol.md`. It automatically integrates Public, Confidential (Company/Client), and Personal knowledge tiers, prioritizing the most specific secrets while ensuring no leaks to public outputs.
