---
name: elevenlabs
description: "Complete ElevenLabs AI audio platform: text-to-speech (TTS), speech-to-text (STT/Scribe), voice cloning, voice design, sound effects, music generation, dubbing, voice changer, voice isolator, and conversational voice agents. Use when working with audio generation, voice synthesis, transcription, audio processing, or building voice-enabled applications. Triggers: generate speech, clone voice, transcribe audio, create sound effects, compose music, dub video, change voice, isolate vocals, build voice agent, ElevenLabs API/SDK/CLI/MCP."
---

# ElevenLabs AI Audio Platform

Complete guide to ElevenLabs' audio AI capabilities: speech synthesis, transcription, voice cloning, sound effects, music generation, dubbing, and conversational voice agents.

## Quick Reference

| Capability | API/Tool | Use Case |
|-----------|----------|----------|
| **Text-to-Speech** | `text_to_speech` | Generate lifelike speech from text |
| **Speech-to-Text** | `speech_to_text` | Transcribe audio with Scribe v2 |
| **Voice Cloning** | `voice_clone` | Clone voices from audio samples |
| **Voice Design** | `text_to_voice` | Create voices from text descriptions |
| **Sound Effects** | `text_to_sound_effects` | Generate SFX from prompts |
| **Music** | `compose_music` | Generate studio-grade music |
| **Dubbing** | Dubbing API | Translate video/audio (32 languages) |
| **Voice Changer** | `speech_to_speech` | Transform voice while preserving emotion |
| **Voice Isolator** | `isolate_audio` | Remove background noise |
| **Voice Agents** | Agents CLI/API | Build conversational AI agents |

## Setup

### API Key
```bash
# Environment variable
export ELEVENLABS_API_KEY="your-api-key"

# Or in .env file
ELEVENLABS_API_KEY=your-api-key
```

### SDK Installation
```bash
# Python
pip install elevenlabs

# TypeScript/Node
npm install elevenlabs
```

### MCP Server (for Claude Code, Cursor, etc.)
```json
{
  "mcpServers": {
    "ElevenLabs": {
      "command": "uvx",
      "args": ["elevenlabs-mcp"],
      "env": {
        "ELEVENLABS_API_KEY": "your-api-key"
      }
    }
  }
}
```

## Text-to-Speech (TTS)

Convert text to lifelike speech. See [references/tts-models.md](references/tts-models.md) for model details.

### Python SDK
```python
from elevenlabs.client import ElevenLabs
from elevenlabs import play

client = ElevenLabs(api_key="your-api-key")

audio = client.text_to_speech.convert(
    text="Hello world!",
    voice_id="JBFqnCBsd6RMkjVDRZzb",  # George
    model_id="eleven_multilingual_v2",
    output_format="mp3_44100_128"
)
play(audio)
```

### MCP Tool
```
mcp__ElevenLabs__text_to_speech
- text: "Your text here"
- voice_name: "Rachel" (or voice_id)
- model_id: "eleven_multilingual_v2"
- stability: 0.5, similarity_boost: 0.75
- speed: 1.0 (range: 0.7-1.2)
```

### Model Selection
| Model | Latency | Languages | Best For |
|-------|---------|-----------|----------|
| `eleven_multilingual_v2` | ~500ms | 29 | High quality, long-form |
| `eleven_flash_v2_5` | ~75ms | 32 | Real-time, agents |
| `eleven_turbo_v2_5` | ~250ms | 32 | Balanced quality/speed |
| `eleven_v3` (alpha) | Higher | 70+ | Emotional, dramatic |

## Speech-to-Text (Scribe)

Transcribe audio with 90+ language support. See [references/stt-scribe.md](references/stt-scribe.md) for details.

### Python SDK
```python
result = client.speech_to_text.convert(
    file=open("audio.mp3", "rb"),
    model_id="scribe_v2",
    diarize=True  # Speaker detection
)
print(result.text)
```

### MCP Tool
```
mcp__ElevenLabs__speech_to_text
- input_file_path: "/path/to/audio.mp3"
- diarize: true (speaker detection)
- language_code: "eng" (or auto-detect)
```

### Features
- **90+ languages** with word-level timestamps
- **Speaker diarization** (up to 48 speakers)
- **Keyterm prompting** (bias toward specific words)
- **Entity detection** (names, numbers, dates)
- **Realtime mode** (~150ms latency)

## Voice Cloning

### Instant Voice Clone (MCP)
```
mcp__ElevenLabs__voice_clone
- name: "My Voice"
- files: ["/path/to/sample1.mp3", "/path/to/sample2.mp3"]
- description: "Professional male voice"
```

### Requirements
- **Instant**: 30+ seconds of clean audio
- **Professional**: 30+ minutes for hyper-realistic clones
- Creator plan or higher required

## Voice Design

Create entirely new voices from text descriptions.

### MCP Tool
```
mcp__ElevenLabs__text_to_voice
- voice_description: "A warm, friendly male voice with a slight British accent,
  perfect for audiobook narration"
```

Creates 3 voice previews to choose from. Use `create_voice_from_preview` to save.

## Sound Effects

Generate cinematic sound effects from text. See [references/sound-effects.md](references/sound-effects.md).

### MCP Tool
```
mcp__ElevenLabs__text_to_sound_effects
- text: "Heavy wooden door creaking open slowly"
- duration_seconds: 3.0 (0.5-30 seconds)
- loop: false
```

### Prompting Tips
- **Simple**: "Glass shattering on concrete"
- **Sequences**: "Footsteps on gravel, then a metallic door opens"
- **Musical**: "90s hip-hop drum loop, 90 BPM"

## Music Generation

Generate studio-grade music. See [references/music-generation.md](references/music-generation.md).

### MCP Tool
```
mcp__ElevenLabs__compose_music
- prompt: "Upbeat electronic track with driving synths, 120 BPM"
- music_length_ms: 60000 (10s-5min)
```

### Features
- Complete control over genre, style, structure
- Vocals or instrumental
- Multilingual lyrics
- Edit sections individually

## Dubbing

Translate audio/video while preserving speaker identity. See [references/dubbing.md](references/dubbing.md).

- **32 languages** supported
- Preserves emotion, timing, tone
- Speaker separation (up to 9 speakers)
- Files up to 1GB / 2.5 hours via API

## Voice Changer (Speech-to-Speech)

Transform any voice while preserving performance nuances.

### MCP Tool
```
mcp__ElevenLabs__speech_to_speech
- input_file_path: "/path/to/recording.mp3"
- voice_id: "target_voice_id"
```

- Preserves whispers, laughs, emotional cues
- 29 languages supported
- Billed at 1000 chars/minute

## Voice Isolator

Remove background noise from recordings.

### MCP Tool
```
mcp__ElevenLabs__isolate_audio
- input_file_path: "/path/to/noisy_audio.mp3"
```

- Supports audio and video files
- Files up to 500MB / 1 hour

## Conversational Voice Agents

Build and deploy voice-enabled AI agents. See [references/voice-agents.md](references/voice-agents.md) for comprehensive guide.

### CLI Quick Start
```bash
# Install
npm install -g @elevenlabs/cli

# Initialize and authenticate
elevenlabs agents init
elevenlabs auth login

# Create agent
elevenlabs agents add "Support Bot" --template customer-service

# Deploy
elevenlabs agents push
```

### Templates
| Template | Use Case |
|----------|----------|
| `customer-service` | Professional support, low temp |
| `assistant` | General purpose, balanced |
| `voice-only` | Voice interactions only |
| `text-only` | Text conversations only |
| `minimal` | Quick prototyping |

### Agent Tools
- **Server Tools**: Webhook API calls
- **Client Tools**: Frontend events
- **MCP Tools**: Model Context Protocol servers
- **System Tools**: transfer_to_number, agent_transfer, end_call

## Voice Library

### Search Voices (MCP)
```
mcp__ElevenLabs__search_voices
- search: "professional narrator"
- sort: "name" | "created_at_unix"
```

### Search Public Library
```
mcp__ElevenLabs__search_voice_library
- search: "deep male"
- page_size: 10
```

### Popular Voice IDs
| Voice | ID | Style |
|-------|-----|-------|
| Rachel | 21m00Tcm4TlvDq8ikWAM | Neutral, professional |
| Adam | pNInz6obpgDQGcFmaJgB | Deep, warm |
| Bella | EXAVITQu4vr4xnSDxMaL | Soft, gentle |

Browse: [elevenlabs.io/voice-library](https://elevenlabs.io/voice-library)

## Account & Billing

### Check Subscription
```
mcp__ElevenLabs__check_subscription
```

### List Models
```
mcp__ElevenLabs__list_models
```

## Reference Documentation

| Topic | File |
|-------|------|
| TTS Models & Parameters | [references/tts-models.md](references/tts-models.md) |
| Speech-to-Text (Scribe) | [references/stt-scribe.md](references/stt-scribe.md) |
| Sound Effects Prompting | [references/sound-effects.md](references/sound-effects.md) |
| Music Generation | [references/music-generation.md](references/music-generation.md) |
| Voice Agents (CLI/API) | [references/voice-agents.md](references/voice-agents.md) |
| Agent Prompting Guide | [references/agent-prompting.md](references/agent-prompting.md) |
| Dubbing Guide | [references/dubbing.md](references/dubbing.md) |

## Pricing & Limits

- **TTS**: Per character (Flash models 50% cheaper)
- **STT**: Per hour of audio
- **Sound Effects**: 40 credits/second when duration specified
- **Music**: Per generation
- See: [elevenlabs.io/pricing](https://elevenlabs.io/pricing)

### Concurrency Limits (by plan)
| Plan | Multilingual v2 | Flash/Turbo | STT |
|------|-----------------|-------------|-----|
| Free | 2 | 4 | 8 |
| Starter | 3 | 6 | 12 |
| Creator | 5 | 10 | 20 |
| Pro | 10 | 20 | 40 |
| Scale | 15 | 30 | 60 |
