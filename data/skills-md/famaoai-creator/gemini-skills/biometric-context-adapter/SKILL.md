---
name: biometric-context-adapter
description: Infers user stress/energy levels from interaction patterns (typing speed, error rate). Adjusts response verbosity and visualizes mood via a "Niko-Niko Calendar."
status: implemented
category: Interface & AI
last_updated: '2026-02-13'
tags:
  - gemini-skill
---

# Biometric Context Adapter

This skill gives the agent "Emotional Intelligence" to match your pace.

## Capabilities

### 1. Mood Inference

- Analyzes session logs for indicators of stress (e.g., short/abrupt commands, high typo rate) or flow (e.g., rapid, complex instructions).
- Categorizes state into: `Flow`, `Normal`, `Stressed`, `Fatigued`.

### 2. Adaptive Response

- **Stressed/Fatigued**: Returns ultra-concise, yes/no answers.
- **Flow/Normal**: Offers detailed insights and "Devil's Advocate" debates.

### 3. Niko-Niko Calendar

- Generates a visual report (`mood_calendar.md`) showing your emotional trend over the last month.

## Usage

- "How am I doing today? Generate my Niko-Niko calendar."
- "I'm tired. Switch to 'Low Energy Mode'."

## Knowledge Protocol

- Adheres to `knowledge/evolution/biometric_privacy.md`.
