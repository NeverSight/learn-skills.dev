---
name: OpenAI Whisper
description: 使用Whisper命令行工具进行本地语音转文字（无需API密钥）。
homepage: https://openai.com/research/whisper
metadata: {"clawdbot":{"emoji":"🎙️","requires":{"bins":["whisper"]},"install":[{"id":"brew","kind":"brew","formula":"openai-whisper","bins":["whisper"],"label":"Install OpenAI Whisper (brew)"}]}}
---

# Whisper (CLI)

Use `whisper` to transcribe audio locally.

Quick start
- `whisper /path/audio.mp3 --model medium --output_format txt --output_dir .`
- `whisper /path/audio.m4a --task translate --output_format srt`

Notes
- Models download to `~/.cache/whisper` on first run.
- `--model` defaults to `turbo` on this install.
- Use smaller models for speed, larger for accuracy.
