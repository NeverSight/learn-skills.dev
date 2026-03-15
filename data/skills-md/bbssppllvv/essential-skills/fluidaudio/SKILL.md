---
name: fluidaudio
description: >
  Integrate FluidAudio Swift SDK for fully local, on-device audio AI on Apple platforms.
  FluidAudio provides ASR (NVIDIA Parakeet TDT models), speaker diarization, VAD, and TTS —
  all running on Apple Neural Engine via CoreML with zero cloud dependency.
  Use when implementing: (1) offline/local speech-to-text transcription on macOS/iOS,
  (2) real-time streaming ASR with end-of-utterance detection,
  (3) speaker diarization (who spoke when),
  (4) voice activity detection,
  (5) text-to-speech synthesis,
  (6) any FluidAudio SDK integration, FluidInference models, or Parakeet CoreML models.
  Triggers on mentions of FluidAudio, FluidInference, parakeet-tdt, on-device transcription
  with CoreML, local ASR on Apple Silicon, or offline speech recognition for macOS/iOS apps.
---

# FluidAudio SDK

Swift SDK for fully local audio AI on Apple platforms. All inference runs on Apple Neural Engine (ANE) via CoreML — no cloud, no latency, no data leaves the device.

**Repository**: `https://github.com/FluidInference/FluidAudio.git`
**Version**: 0.12.1+
**Platforms**: macOS 14.0+ / iOS 17.0+ (arm64 only, Apple Silicon)

## Quick Start

```swift
import FluidAudio

// ASR — batch transcription
let models = try await AsrModels.downloadAndLoad(version: .v3)  // multilingual, 25 languages
let asr = AsrManager(config: .default)
try await asr.initialize(models: models)
let result = try await asr.transcribe(audioURL)
print(result.text)
```

Models auto-download from HuggingFace on first use, then cache at `~/.cache/fluidaudio/Models/`.

## Installation (SPM)

```swift
dependencies: [
    .package(url: "https://github.com/FluidInference/FluidAudio.git", from: "0.12.1")
]
// Product: "FluidAudio" (core, Apache 2.0) or "FluidAudioTTS" (+ Kokoro TTS, GPL-3.0)
```

## Components & Performance

| Component | Manager | RTFx (M4 Pro) | Key Metric |
|-----------|---------|---------------|------------|
| ASR (batch) | `AsrManager` | ~190x | WER 3.21% |
| ASR (streaming) | `StreamingEouAsrManager` | real-time | 160ms–1.6s EOU latency |
| Diarization (offline) | `OfflineDiarizerManager` | ~150x | DER 13.89% |
| Diarization (online) | `DiarizerManager` | ~150x | DER 17.7% |
| VAD | `VadManager` | ~1000x+ | F1 0.85 |
| TTS (PocketTTS) | `PocketTTS` | — | ~80ms latency |
| TTS (Kokoro) | `KokoroModel` | — | High quality, SSML |

All audio auto-converts to 16kHz mono Float32 via `AudioConverter`.

## Detailed References

Read the appropriate reference file based on your task:

- **ASR (batch + streaming transcription)**: See [references/asr.md](references/asr.md) — models, batch/streaming APIs, configuration, EOU detection, token merging, CLI
- **Speaker diarization**: See [references/diarization.md](references/diarization.md) — offline/online pipelines, Sortformer, configuration, CLI
- **Voice activity detection**: See [references/vad.md](references/vad.md) — batch/streaming VAD, segmentation config, CLI
- **Text-to-speech**: See [references/tts.md](references/tts.md) — PocketTTS vs Kokoro, SSML, licensing
- **Infrastructure (install, models, audio, platform)**: See [references/infrastructure.md](references/infrastructure.md) — SPM/CocoaPods setup, model management, caching, AudioConverter, ANE optimization, package structure

## Key Integration Patterns

### Typical macOS Voice-to-Text App

```swift
import FluidAudio

class TranscriptionService {
    private var asrManager: AsrManager?

    func setup() async throws {
        let models = try await AsrModels.downloadAndLoad(version: .v3)
        let manager = AsrManager(config: .default)
        try await manager.initialize(models: models)
        self.asrManager = manager
    }

    func transcribe(url: URL) async throws -> String {
        guard let manager = asrManager else { throw TranscriptionError.notInitialized }
        let result = try await manager.transcribe(url)
        return result.text
    }
}
```

### Real-Time Streaming with EOU Detection

```swift
let streaming = StreamingEouAsrManager(config: .streaming)
try await streaming.start(models: models)

Task {
    for await update in await streaming.transcriptionUpdates {
        if update.isConfirmed {
            // Final text — safe to paste/display
        } else {
            // Volatile — may change, show as preview
        }
    }
}

// Feed microphone audio
for chunk in microphoneBufferStream {
    await streaming.streamAudio(chunk)
}
let final = try await streaming.finish()
```

### Combined ASR + Diarization

```swift
let samples = try AudioConverter().resampleAudioFile(path: "meeting.wav")

// Transcribe
let asrResult = try await asrManager.transcribe(samples)

// Identify speakers
let diarizer = OfflineDiarizerManager(config: OfflineDiarizerConfig())
try await diarizer.prepareModels()
let diarResult = try await diarizer.process(audio: samples)
```
