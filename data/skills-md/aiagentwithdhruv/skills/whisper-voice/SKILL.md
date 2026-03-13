---
name: whisper-voice
description: Native macOS menu bar app for live voice-to-text with auto-type using WhisperKit on Apple Silicon
---

# Whisper Voice — Live Speech-to-Text Mac App

## Goal
Build and run a native macOS menu bar app that captures live microphone audio, transcribes it offline using WhisperKit (on Apple Silicon), and auto-types the text wherever the cursor is.

## Inputs

| Name | Type | Required | Description |
|------|------|----------|-------------|
| model_size | string | No | Whisper model: tiny, base (default), small |
| language | string | No | "en" (default) or "hi" for Hindi mode |
| chunk_duration | float | No | Seconds per audio chunk (default: 3.0) |

## Process

### 1. Build the app
```bash
cd AiwithDhruv_Voice/WhisperAiwithDhruv
swift build
```

### 2. Run the app
```bash
swift run WhisperAiwithDhruv
# Or open in Xcode: open Package.swift → Cmd+R
```

### 3. First launch setup
1. Grant microphone permission when prompted
2. Grant Accessibility in System Settings → Privacy → Accessibility
3. Wait for model download (~140MB for base model)

### 4. Usage
- **Cmd+Shift+Space** — Toggle recording on/off
- Click mic icon in menu bar for controls
- Speak — text auto-types at cursor position
- Toggle Hindi mode for Hindi/Hinglish input

## Outputs

| Name | Type | Description |
|------|------|-------------|
| transcribed_text | string | Live transcribed text typed at cursor |
| history | array | Last 50 transcription entries in menu bar |

## Edge Cases
- **No mic**: Shows error in menu bar dropdown
- **Accessibility denied**: Auto-type disabled, manual copy from history
- **Silence**: VAD skips silent chunks (energy-based threshold)
- **Hallucinations**: Filters common Whisper artifacts ("Thank you.", "...")
- **Model not downloaded**: Shows download progress bar

## Environment
- macOS 14+ (Sonoma)
- Apple Silicon (M1/M2/M3/M4)
- Xcode 15+ (for building)
- No API keys needed (fully offline)

## Schema

### Inputs
| Name | Type | Required | Description |
|------|------|----------|-------------|
| model_size | string | No | tiny / base / small |
| language | string | No | en / hi |
| chunk_duration | float | No | 2.0 - 8.0 seconds |
| silence_threshold | float | No | 0.002 - 0.05 |

### Outputs
| Name | Type | Description |
|------|------|-------------|
| transcription | string | Live text output |
| auto_typed | boolean | Whether text was injected at cursor |

### Credentials
| Name | Source |
|------|--------|
| None | Fully offline, no API keys |

### Composable With
`video-edit` (add transcription captions), `send-telegram` (send transcriptions to phone)

### Cost
Free — runs entirely on-device. Model download is one-time (~140MB for base).
