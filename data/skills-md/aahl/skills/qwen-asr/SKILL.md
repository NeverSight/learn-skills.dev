---
name: qwen-asr
description: Transcribe audio files using Qwen ASR. Use when the user sends voice messages and wants them converted to text.
---

# Qwen ASR
Transcribe an audio file (wav/mp3/ogg...) to text using Qwen ASR. No configuration or API key required.

## Usage
```shell
uv run scripts/main.py -f audio.wav
cat audio.wav | uv run scripts/main.py > transcript.txt
```
