---
name: transcript
description: "Download or transcribe text from any audio/video source. For YouTube URLs, fetches subtitles (manual preferred, then auto-generated, then Whisper fallback). For any audio/video file, transcribes directly with faster-whisper — generating plain text, SRT/VTT subtitles, JSON, or timestamped segments. Supports batch processing and translation. Trigger keywords: transcribe, transcript, download transcript, get captions, get subtitles, extract text from video, convert audio to text, YouTube transcript, generate subtitles, transcribe podcast, audio to text, video to text."
agent_created: true
---

# Transcript — Universal Audio/Video to Text

> Fetch YouTube transcripts via yt-dlp, or transcribe any audio/video file with OpenAI Whisper.

## Routing

```
User input:
  ├── YouTube URL? → Read references/youtube-transcript.md and follow its workflow
  └── Audio/video file? → Read references/whisper-transcription.md and follow its workflow
```

**Always ask the user before large downloads** (audio files, Whisper models). Clean up temporary files when done.

