---
name: local-whisper
description: LOCAL voice transcription using OpenAI Whisper. 100% private - audio never leaves your machine. Supports 97+ languages.
homepage: https://github.com/kesslerio/local-whisper-openclaw-skill
metadata: {"openclaw":{"emoji":"🎙️","requires":{"bins":["whisper","ffmpeg"]},"install":[{"id":"pip","kind":"pip","package":"openai-whisper","bins":["whisper"],"label":"Install Whisper (pip)"}]}}
---

# 🎙️ Local Whisper Transcription

100% private voice transcription using OpenAI Whisper. Audio never leaves your machine.

## ⚠️ Important: OpenClaw Configuration Required

This skill must be configured in OpenClaw's `tools.media.audio` to handle incoming voice messages. Without this config, voice messages may cause token overflow errors or be sent to cloud APIs.

Add to `~/.openclaw/openclaw.json`:

```json5
{
  tools: {
    media: {
      audio: {
        enabled: true,
        models: [
          {
            type: "cli",
            command: "node",
            args: ["<skill-path>/transcribe.js", "{{MediaPath}}"]
          }
        ]
      }
    }
  }
}
```

Replace `<skill-path>` with the path to the checked-out skill repository. For a mirrored OpenClaw install, use `~/.openclaw/skills/local-whisper`.

## Quick Start

```bash
# Install dependencies
pip install openai-whisper

# Transcribe audio
node transcribe.js voice.ogg
```

## CLI Options

```
--model <tiny|base|small|medium|large>  Model size (default: small)
--language <lang>                        Language code (default: auto)
--output-dir <dir>                       Output directory
--smart-model                           Auto-select model by file size
--check                                 Verify dependencies
```

## Model Sizes

| Model | Size | Speed | RAM |
|-------|------|-------|-----|
| tiny | 39 MB | ⚡⚡⚡⚡ | ~1GB |
| base | 74 MB | ⚡⚡⚡ | ~1GB |
| small | 244 MB | ⚡⚡ | ~2GB |
| medium | 769 MB | ⚡ | ~5GB |
| large | 1550 MB | 🐢 | ~10GB |

## Documentation

- [Installation Guide](docs/INSTALL.md)
- [Troubleshooting](docs/TROUBLESHOOTING.md)
- [GitHub Repository](https://github.com/kesslerio/local-whisper-openclaw-skill)
