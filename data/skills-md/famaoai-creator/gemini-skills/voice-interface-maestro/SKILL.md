---
name: voice-interface-maestro
description: Converts text responses into spoken audio (TTS). Supports multiple voice personas (Professional, Energetic, Calm) and secure configuration via the Personal Tier.
status: implemented
category: Strategy & Leadership
last_updated: '2026-02-13'
tags:
  - gemini-skill
---

# Voice Interface Maestro

This skill gives the agent a literal voice.

## Capabilities

### 1. Text-to-Speech Synthesis

- Converts Markdown text into audio files (`.mp3`).
- Removes code blocks and URLs before speaking to ensure natural flow.

### 2. Persona-Based Voice Selection

- Automatically selects the best voice based on the context (e.g., uses "Calm" voice if `biometric-context-adapter` detects stress).
- Loads API keys and Voice IDs from `knowledge/personal/voice/config.json`.

## Usage

- "Read this summary to me."
- "Speak the results of the security audit using the 'Professional' voice."

## Knowledge Protocol

- Adheres to `knowledge/voice/persona_definitions.md`.
