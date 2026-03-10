---
name: xiaoyuzhou-transcribe
description: Download a Xiaoyuzhou (小宇宙) episode from a public URL and generate subtitles (.srt) plus transcript (.txt) using faster-whisper. Use when a user provides a xiaoyuzhoufm episode URL and wants full transcript text with timestamps, or needs to convert the audio into SRT/TXT files.
---

# Xiaoyuzhou Transcribe

## Overview

Generate SRT and TXT transcripts from a Xiaoyuzhou episode URL by downloading the audio and running faster-whisper locally. Use the bundled script to keep the workflow deterministic and repeatable.

## Quick Start

- Install dependency: `python3 -m pip install -U faster-whisper`
- Run: `python3 scripts/xiaoyuzhou_transcribe.py "<episode-url>" --output-dir .`
- Expect outputs: `xiaoyuzhou-<eid>.mp3`, `xiaoyuzhou-<eid>.srt`, `xiaoyuzhou-<eid>.txt`

## Workflow

- Fetch the episode page and parse `__NEXT_DATA__` to locate the audio URL.
- Download the audio (resume supported) unless `--audio-path` is provided.
- Transcribe audio with faster-whisper and write SRT + TXT.

## Script Usage

`scripts/xiaoyuzhou_transcribe.py` accepts:

- `--output-dir`: write outputs to a specific directory
- `--model`: whisper model size (`tiny` by default; use `base` or `small` for higher accuracy)
- `--language`: force a language code or allow auto-detect
- `--audio-path`: transcribe a local audio file instead of downloading
- `--force-download`: re-download the audio even if it exists
- `--no-vad`: disable VAD filtering if segments are too aggressive

## Notes

- If the episode is private or requires login, the script cannot access it.
- Xiaoyuzhou does not expose public transcripts for many episodes; this workflow generates subtitles via speech-to-text instead.
