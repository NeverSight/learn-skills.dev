---
name: spacemit-robot-speech
description: SpacemiT Robot SDK speech and audio component workflow for components/multimedia/audio, components/model_zoo/asr, components/model_zoo/vad, components/model_zoo/tts, components/model_zoo/voiceprint, and components/multimedia/audio_process/doa. Use for independent component builds, dependency build ordering, model or demo performance measurement, and C++/Python API integration from API.md, headers, and built binaries.
metadata:
  requires:
    bins: ["bash"]
  sdk:
    module_paths:
      - components/multimedia/audio
      - components/model_zoo/asr
      - components/model_zoo/vad
      - components/model_zoo/tts
      - components/model_zoo/voiceprint
      - components/multimedia/audio_process/doa
    primary_docs:
      - components/multimedia/audio/API.md
      - components/multimedia/audio/package.xml
      - components/multimedia/audio/test.yaml
      - components/model_zoo/asr/API.md
      - components/model_zoo/asr/package.xml
      - components/model_zoo/asr/test.yaml
      - components/model_zoo/vad/API.md
      - components/model_zoo/vad/package.xml
      - components/model_zoo/vad/test.yaml
      - components/model_zoo/tts/API.md
      - components/model_zoo/tts/package.xml
      - components/model_zoo/tts/test.yaml
      - components/model_zoo/voiceprint/API.md
      - components/model_zoo/voiceprint/package.xml
      - components/model_zoo/voiceprint/test.yaml
      - components/multimedia/audio_process/doa/API.md
      - components/multimedia/audio_process/doa/package.xml
      - components/multimedia/audio_process/doa/test.yaml
    build_hint: single_package_first
---

# SpacemiT Robot Speech

## Overview

Use this skill for speech/audio work in SpacemiT Robot SDK. It replaces the separate ASR, VAD, TTS, voiceprint, audio, and DOA module skills with one workflow-oriented entry point.

Always start from the real SDK checkout and the active execution mode from `spacemit-robot-shared`. Build and run actions still follow `spacemit-robot-build`, `spacemit-robot-remote`, and `spacemit-robot-sync`; this skill only adds speech/audio component routing.

## Components

| Area | SDK path | API source |
| --- | --- | --- |
| audio capture/playback/resample | `components/multimedia/audio` | `components/multimedia/audio/API.md` |
| ASR/STT | `components/model_zoo/asr` | `components/model_zoo/asr/API.md` |
| VAD | `components/model_zoo/vad` | `components/model_zoo/vad/API.md` |
| TTS | `components/model_zoo/tts` | `components/model_zoo/tts/API.md` |
| voiceprint / speaker recognition | `components/model_zoo/voiceprint` | `components/model_zoo/voiceprint/API.md` |
| DOA / sound source localization | `components/multimedia/audio_process/doa` | `components/multimedia/audio_process/doa/API.md` |

## Task Routing

- For component build requests, read `references/build-components.md`.
- For model, demo, latency, RTF, throughput, bandwidth, or memory performance requests, read `references/performance.md`.
- For application development, C++/Python API integration, or composing multiple speech components, read `references/api-integration.md`.
- For an empty audio device list, `PortAudio ... Unanticipated host error`, or a capture/playback stream that fails on a real board, read `references/audio-devices.md`.

Read only the reference needed for the user task. Then read the component `API.md`, `package.xml`, `test.yaml`, headers, demos, or binary help text that the reference asks for.

## Rules

- Do not keep separate ASR, VAD, TTS, voiceprint, audio, or DOA skill logic in this repository; this skill is the speech/audio entry.
- Do not invent API shape from memory. Read the component `API.md` first, then headers or bindings when the user asks for implementation.
- Do not conclude that a microphone, speaker, or board is broken from an empty device list alone. Prove the ALSA layer with raw `arecord`/`aplay`, then check what the binary's audio library loads; an empty PortAudio list with working `arecord` is a library/backend problem, not hardware. See `references/audio-devices.md`.
- Do not treat model downloads, real microphones, speakers, or manual hardware smoke as PR-required checks.
- Do not fake model or device performance. If a model, sample, binary, or device is missing, report the missing precondition and the checks already completed.
