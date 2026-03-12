---
name: together-audio
description: Text-to-speech (TTS) and speech-to-text (STT) via Together AI. TTS models include Orpheus, Kokoro, Cartesia Sonic, Rime, MiniMax with REST, streaming, and WebSocket support. STT models include Whisper and Voxtral. Use when users need voice synthesis, audio generation, speech recognition, transcription, TTS, STT, or real-time voice applications.
---

# Together Audio (TTS & STT)

## Overview

Together AI provides text-to-speech and speech-to-text capabilities.

**TTS** — Generate speech from text via REST, streaming, or WebSocket:
- Endpoint: `/v1/audio/speech`
- WebSocket: `wss://api.together.xyz/v1/audio/speech/websocket`

**STT** — Transcribe audio to text:
- Endpoint: `/v1/audio/transcriptions`

## Installation

```shell
# Python (recommended)
uv init  # optional, if starting a new project
uv add together
```

```shell
# or with pip
pip install together
```

```shell
# TypeScript / JavaScript
npm install together-ai
```

Set your API key:

```shell
export TOGETHER_API_KEY=<your-api-key>
```

## TTS Quick Start

### Basic Speech Generation

```python
from together import Together
client = Together()

response = client.audio.speech.create(
    model="canopylabs/orpheus-3b-0.1-ft",
    input="Today is a wonderful day to build something people love!",
    voice="tara",
    response_format="mp3",
)
response.stream_to_file("speech.mp3")
```

```typescript
import Together from "together-ai";
import { Readable } from "stream";
import { createWriteStream } from "fs";

const together = new Together();

async function generateAudio() {
  const res = await together.audio.create({
    input: "Today is a wonderful day to build something people love!",
    voice: "tara",
    response_format: "mp3",
    sample_rate: 44100,
    stream: false,
    model: "canopylabs/orpheus-3b-0.1-ft",
  });

  if (res.body) {
    const nodeStream = Readable.from(res.body as ReadableStream);
    const fileStream = createWriteStream("./speech.mp3");
    nodeStream.pipe(fileStream);
  }
}

generateAudio();
```

```shell
curl -X POST "https://api.together.xyz/v1/audio/speech" \
  -H "Authorization: Bearer $TOGETHER_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model":"canopylabs/orpheus-3b-0.1-ft","input":"Hello world","voice":"tara","response_format":"mp3"}' \
  --output speech.mp3
```

### Streaming Audio (Low Latency)

```python
response = client.audio.speech.create(
    model="canopylabs/orpheus-3b-0.1-ft",
    input="The quick brown fox jumps over the lazy dog",
    voice="tara",
    stream=True,
    response_format="raw",
    response_encoding="pcm_s16le",
)
response.stream_to_file("speech.wav", response_format="wav")
```

```typescript
import Together from "together-ai";

const together = new Together();

async function streamAudio() {
  const response = await together.audio.speech.create({
    model: "canopylabs/orpheus-3b-0.1-ft",
    input: "The quick brown fox jumps over the lazy dog",
    voice: "tara",
    stream: true,
    response_format: "raw",
    response_encoding: "pcm_s16le",
  });

  const chunks = [];
  for await (const chunk of response) {
    chunks.push(chunk);
  }

  console.log("Streaming complete!");
}

streamAudio();
```

### WebSocket (Lowest Latency)

```python
import asyncio, websockets, json, base64

async def generate_speech():
    url = "wss://api.together.ai/v1/audio/speech/websocket?model=hexgrad/Kokoro-82M&voice=af_alloy"
    headers = {"Authorization": f"Bearer {api_key}"}

    async with websockets.connect(url, additional_headers=headers) as ws:
        session = json.loads(await ws.recv())
        await ws.send(json.dumps({"type": "input_text_buffer.append", "text": "Hello!"}))
        await ws.send(json.dumps({"type": "input_text_buffer.commit"}))

        audio_data = bytearray()
        async for msg in ws:
            data = json.loads(msg)
            if data["type"] == "conversation.item.audio_output.delta":
                audio_data.extend(base64.b64decode(data["delta"]))
            elif data["type"] == "conversation.item.audio_output.done":
                break
```

## TTS Models

| Model | API String | Endpoints | Price |
|-------|-----------|-----------|-------|
| Orpheus 3B | `canopylabs/orpheus-3b-0.1-ft` | REST, Streaming, WebSocket | $15/1M chars |
| Kokoro | `hexgrad/Kokoro-82M` | REST, Streaming, WebSocket | $4/1M chars |
| Cartesia Sonic 2 | `cartesia/sonic-2` | REST | $65/1M chars |
| Cartesia Sonic | `cartesia/sonic` | REST | - |
| Rime Arcana v3 Turbo | `rime-labs/rime-arcana-v3-turbo` | REST, Streaming, WebSocket | DE only |
| MiniMax Speech 2.6 | `minimax/speech-2.6-turbo` | REST, Streaming, WebSocket | DE only |

## TTS Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| `model` | string | TTS model (required) | - |
| `input` | string | Text to synthesize (required) | - |
| `voice` | string | Voice ID (required) | - |
| `response_format` | string | `mp3`, `wav` (default), `raw`, `mulaw` | `wav` |
| `stream` | bool | Enable streaming (raw format only) | false |
| `response_encoding` | string | `pcm_f32le`, `pcm_s16le`, `pcm_mulaw`, `pcm_alaw` for raw | - |
| `language` | string | Language of input text: en, de, fr, es, hi, it, ja, ko, nl, pl, pt, ru, sv, tr, zh | "en" |
| `sample_rate` | int | Audio sample rate (e.g., 44100) | - |

### List Available Voices

```python
response = client.audio.voices.list()
for model_voices in response.data:
    print(f"Model: {model_voices.model}")
    for voice in model_voices.voices:
        print(f"  - {voice.name}")
```

**Key voices:** Orpheus: `tara`, `leah`, `leo`, `dan`, `mia`, `zac`. Kokoro: `af_alloy`, `af_bella`, `am_adam`, `am_echo`. See [references/tts-models.md](references/tts-models.md) for complete voice lists.

## STT Quick Start

### Transcribe Audio

```python
response = client.audio.transcriptions.create(
    model="openai/whisper-large-v3",
    file=open("audio.mp3", "rb"),
)
print(response.text)
```

```typescript
import Together from "together-ai";

const together = new Together();

const transcription = await together.audio.transcriptions.create({
  file: "path/to/audio.mp3",
  model: "openai/whisper-large-v3",
  language: "en",
});
console.log(transcription.text);
```

```shell
curl -X POST "https://api.together.xyz/v1/audio/transcriptions" \
  -H "Authorization: Bearer $TOGETHER_API_KEY" \
  -F model="openai/whisper-large-v3" \
  -F file=@audio.mp3
```

### STT Models

| Model | API String |
|-------|-----------|
| Whisper Large v3 | `openai/whisper-large-v3` |
| Voxtral Mini 3B | `mistralai/Voxtral-Mini-3B-2507` |

## Delivery Method Guide

- **REST**: Batch processing, complete audio files
- **Streaming**: Real-time apps where TTFB matters
- **WebSocket**: Interactive/conversational apps, lowest latency

## Resources

- **Complete voice lists**: See [references/tts-models.md](references/tts-models.md)
- **STT details**: See [references/stt-models.md](references/stt-models.md)
- **TTS script**: See [scripts/tts_generate.py](scripts/tts_generate.py) — REST, streaming, and WebSocket TTS (v2 SDK)
- **STT script**: See [scripts/stt_transcribe.py](scripts/stt_transcribe.py) — transcribe, translate, diarize with CLI flags (v2 SDK)
- **TTS script (TypeScript)**: See [scripts/tts_generate.ts](scripts/tts_generate.ts) — minimal OpenAPI `x-codeSamples` extraction for TTS/voices (TypeScript SDK)
- **STT script (TypeScript)**: See [scripts/stt_transcribe.ts](scripts/stt_transcribe.ts) — minimal OpenAPI `x-codeSamples` extraction for transcription/translation (TypeScript SDK)
- **Official docs**: [Text-to-Speech](https://docs.together.ai/docs/text-to-speech)
- **Official docs**: [Speech-to-Text](https://docs.together.ai/docs/speech-to-text)
- **API reference**: [TTS API](https://docs.together.ai/reference/audio-speech)
- **API reference**: [STT API](https://docs.together.ai/reference/audio-transcriptions)
