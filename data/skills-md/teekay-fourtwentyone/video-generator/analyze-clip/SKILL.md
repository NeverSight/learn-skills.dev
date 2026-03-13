---
name: analyze-clip
description: Analyze video clips for quality issues, timing problems, and dialogue accuracy. Use when checking generated videos, validating clips, finding black frames, freeze frames, or audio sync issues.
allowed-tools: Read, mcp__video-generator__*
context: fork
agent: general-purpose
---

# Analyze Clip

Comprehensive video clip analysis using the MCP tools.

## Quick Start

Use the `analyze_clip_unified` tool:

```
Tool: analyze_clip_unified
Args: { "videoPath": "data/video/clip.mp4" }
```

## What It Detects

| Signal | Source | Purpose |
|--------|--------|---------|
| Scene changes | ffmpeg scene detection | Visual discontinuities |
| Black frames | ffmpeg blackdetect | Fades, dead regions |
| Freeze frames | ffmpeg freezedetect | Static frames, AI artifacts |
| Speech segments | Whisper | Audio activity |
| Dialogue match | Comparison | Validate generated speech |

## With Dialogue Context

```
Tool: analyze_clip_unified
Args: {
  "videoPath": "data/video/clip.mp4",
  "context": {
    "dialogue": [
      {"speaker": "marcus", "text": "Hello there"}
    ]
  }
}
```

## Available Analysis Tools

| Tool | Purpose |
|------|---------|
| `analyze_clip_unified` | Full analysis (scenes, black, freeze, audio) |
| `transcribe` | Whisper transcription only |
| `analyze_audio_timeline` | Speech/silence detection |
| `analyze_dialogue_clip` | Compare expected vs actual dialogue |

## Interpreting Results

- `recommended_action`: 'use_as_is', 'trim', 'review', or 'regenerate'
- `trim_recommendation`: Suggested start/end times
- `anomalies`: Issues found (with severity)

See `.claude/rules/agents.md` for full response schema.
