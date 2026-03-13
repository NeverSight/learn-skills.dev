---
name: soniox
description: Integrate Soniox speech-to-text API for real-time and async transcription. Use when working with Soniox WebSocket streaming, Soniox REST transcription, Soniox SDKs (Python, Node, Web), or implementing voice/speech features using Soniox. Triggers on mentions of Soniox API, soniox package, @soniox/node, @soniox/speech-to-text-web, real-time transcription via Soniox, speech-to-text integration, or audio transcription with Soniox.
---

# Soniox Speech-to-Text

Cloud speech-to-text API with real-time WebSocket streaming and async file transcription. Supports 60+ languages, speaker diarization, live translation, and custom vocabulary context.

## API Structure

Two main APIs:

| API | Transport | Model | Use Case |
|-----|-----------|-------|----------|
| Real-Time | WebSocket `wss://stt-rt.soniox.com/transcribe-websocket` | `stt-rt-v4` | Live audio streaming, token-by-token results |
| Async | REST `https://api.soniox.com/v1/` | `stt-async-v4` | Pre-recorded files, batch processing |

Authentication: `Authorization: Bearer <API_KEY>` header (or `api_key` query param for WebSocket).

## Quick Start — Real-Time WebSocket

1. Connect to `wss://stt-rt.soniox.com/transcribe-websocket?api_key=YOUR_KEY`
2. Send JSON config: `{"model": "stt-rt-v4", "audio_format": "pcm_s16le", "sample_rate": 16000}`
3. Stream raw audio bytes
4. Receive JSON tokens: `{"tokens": [{"text": "hello", "is_final": true, "start_ms": 100, "end_ms": 500}]}`
5. Close connection when done

Key token fields: `text`, `is_final` (false=provisional, true=confirmed), `start_ms`, `end_ms`, `confidence`, `speaker` (if diarization enabled), `language` (if language ID enabled).

## Quick Start — Async REST

```bash
# Upload and transcribe
curl -X POST https://api.soniox.com/v1/transcriptions \
  -H "Authorization: Bearer $API_KEY" \
  -F model=stt-async-v4 \
  -F audio_file=@recording.mp3

# Poll for result
curl https://api.soniox.com/v1/transcriptions/{id} \
  -H "Authorization: Bearer $API_KEY"
```

## Configuration Options (Both APIs)

Common parameters sent in start config (real-time) or request body (async):

| Parameter | Type | Description |
|-----------|------|-------------|
| `model` | string | `stt-rt-v4` or `stt-async-v4` |
| `language_hints` | string[] | ISO 639-1 codes to improve accuracy |
| `language_hints_strict` | bool | Restrict recognition to hinted languages |
| `enable_language_identification` | bool | Detect language per token |
| `enable_speaker_diarization` | bool | Label speakers (up to 15) |
| `translation` | object | Translation config: `{"type": "one_way", "target_language": "fr"}` or `{"type": "two_way", "language_a": "en", "language_b": "fr"}` |
| `context` | object | Domain context (see below) |
| `max_endpoint_delay_ms` | int | 500-3000ms, semantic endpoint detection (real-time only) |

### Context Object Format

```json
{
  "context": {
    "general": [
      {"key": "domain", "value": "Healthcare"},
      {"key": "topic", "value": "Medical Consultation"}
    ],
    "text": "Background: Patient discussing cardiac symptoms...",
    "terms": ["myocardial infarction", "stent", "angioplasty"],
    "translation_terms": [
      {"source": "stent", "target": "стент"}
    ]
  }
}
```

Max 8000 tokens.

## Reference Files

Read these based on the specific task:

| File | When to Read |
|------|-------------|
| [references/realtime.md](references/realtime.md) | WebSocket protocol details, token streaming, finalization, keepalive, error codes |
| [references/async-api.md](references/async-api.md) | REST endpoints, file upload, job polling, webhooks, file management |
| [references/features.md](references/features.md) | Languages list, diarization details, context format, models, timestamps |
| [references/sdks.md](references/sdks.md) | Python/Node/Web SDK usage, code patterns, client initialization |
| [references/integrations.md](references/integrations.md) | Direct/Proxy stream patterns, Vercel AI, TanStack, Twilio, n8n, data residency, security |

## Native Swift/macOS Integration

Soniox has no native Swift SDK. For macOS/iOS apps, connect via raw WebSocket:

```swift
// URLSessionWebSocketTask approach
let url = URL(string: "wss://stt-rt.soniox.com/transcribe-websocket?api_key=\(apiKey)")!
let task = URLSession.shared.webSocketTask(with: url)
task.resume()

// Send start config
let config = """
{"model":"stt-rt-v4","audio_format":"pcm_s16le","sample_rate":16000}
"""
task.send(.string(config)) { error in /* handle */ }

// Stream audio bytes from microphone
task.send(.data(audioBuffer)) { error in /* handle */ }

// Receive tokens
func receiveNext() {
    task.receive { result in
        switch result {
        case .success(.string(let json)):
            // Parse tokens from JSON
            break
        case .failure(let error):
            // Handle error
            break
        default: break
        }
        receiveNext() // Continue receiving
    }
}
```

Audio format: Send raw PCM signed 16-bit little-endian at 16kHz mono for best results. The API also auto-detects encoded formats (mp3, ogg, flac, wav, etc.).

## Rate Limits

| Limit | Real-Time | Async |
|-------|-----------|-------|
| Requests/min | 100 | 100 |
| Concurrent | 10 connections | 100 pending jobs |
| Max duration | 300 min/session | — |
| Storage | — | 10GB, 1000 files |
| Total transcriptions | — | 2000 |

## Data Residency

Regional endpoints available:

| Region | Real-Time Endpoint | Async Endpoint |
|--------|-------------------|----------------|
| US (default) | `stt-rt.soniox.com` | `api.soniox.com` |
| EU | `stt-rt.eu.soniox.com` | `api.eu.soniox.com` |
| Japan | `stt-rt-jp.soniox.com` | `api.jp.soniox.com` |
