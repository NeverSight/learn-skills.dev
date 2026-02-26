---
name: voice-command-listener
description: Captures microphone input and transcribes it into text commands. Uses SoX for recording and OpenAI Whisper for high-accuracy transcription to control the agent via voice.
status: implemented
category: Interface & AI
last_updated: '2026-02-13'
tags:
  - gemini-skill
---

# Voice Command Listener

This skill allows you to control the Gemini Ecosystem with your voice.

## Capabilities

### 1. Voice Recording

- Uses `sox` (Sound eXchange) to capture audio from the default microphone.
- Records until silence is detected or a specific key is pressed (Ctrl+C).

### 2. Transcription (Whisper)

- Sends the recorded `.wav` or `.mp3` file to the OpenAI Whisper API.
- Returns the transcribed text, ready to be piped into other skills.

## Usage

- "Listen to my command." (Starts recording)
- "Transcribe this audio file and execute it as a prompt."

## Prerequisites

- `sox` installed (`brew install sox`).
- OpenAI API Key configured in `knowledge/personal/voice/config.json`.

## Knowledge Protocol

- Adheres to `knowledge/tech-stack/macos/voice_control_guide.md`.
