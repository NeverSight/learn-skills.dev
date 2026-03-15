---
name: voice-mode
description: "Offline-first voice I/O super-skill: speak via say, listen via listen, and run agent-orchestrated duplex dialogue."
metadata:
  version: 1.0.0
---

# Voice Mode (Super-Skill)

## Purpose

This skill unifies voice output and voice input in one place:

- `say` — text-to-speech (TTS)
- `listen` — speech-to-text (STT)
- `duplex mode` — agent orchestration (`say` → `listen`) built on the atomic scripts

Use `say` and `listen` independently, or let the agent combine them into continuous duplex dialogue.
This is an offline-first skill: STT runs locally via `faster-whisper`, and TTS uses local `piper` models after the initial voice download.

## Atomic Commands

### 1) Speak

```bash
say "text to announce"
say --lang ru "<text in Russian>"
# short alias is also supported:
say -l ru "<text in Russian>"
```

### 2) Listen

```bash
listen
```

### 3) Duplex mode (agent orchestration)

```bash
say --lang ru "<spoken reply in the conversation language>"
listen -l ru -d 0 -s 1
```

Duplex mode is not a standalone shell script in this skill. Core protocol remains atomic: `say` then `listen`.
In duplex sessions, prefer `listen -d 0 -s 1`: no hard timeout, stop by user pause.

## Operating Modes

### Mode A: Selective Voice (default)

- Use `say` only for short, high-value moments (greeting, warning, key conclusion).
- Keep code, tables, and long technical details in text.

### Mode B: Full Voice Output (screenless)

When explicitly requested by the user:

1. Use `say` for every response.
2. Speak the entire assistant reply through `say`, not just a short follow-up question.
3. Do not duplicate full spoken content in chat.
4. For code/tables: describe briefly by voice (language, purpose, size), avoid reading raw code line by line.

### Mode C: Voice Input On-Demand

- Call `listen` when the user wants to dictate the next prompt.
- `listen` prints recognized text to stdout.

### Mode D: Duplex Continuous Dialogue (`say` → `listen`)

When the user enables duplex mode (e.g. "turn on duplex", "full voice mode"):

1. Generate the full assistant response first.
2. Speak the full response via `say`.
3. Immediately call `listen -d 0 -s 1` in the same conversation language.
4. Treat recognized text as the next user prompt.
5. Normalize the recognized text and stop when a stop phrase intent is heard: `стоп`, `выключи прослушивание`, `выключи дуплекс`, `stop listening`.

Canonical agent loop:

```text
answer = full assistant reply
say --lang <lang> "<answer>"
heard = listen -l <lang> -d 0 -s 1
if heard matches a stop phrase intent:
  exit duplex mode
```

This is a hands-free conversational flow owned by the agent, not by a dedicated shell helper.
Never keep the substantive reply only in chat while sending a shorter handoff question to speech.

### Mode E: Autonomous Voice Alerts (optional)

Short proactive announcements are allowed for:

- long-running operations,
- critical blockers/security issues,
- required confirmation to proceed safely.

Keep alerts brief and informative.

## Voice Guard + Listen Guard

Before `say`: ask if silence would hide important information. If not, do not speak.

Before `listen`: ask if voice input is actually needed right now. Do not invoke speculatively.

## Language Memory

- Preferred language is stored in `~/.pi_voice_lang`.
- Use short language codes: `ru`, `en`, `de`, ... (not `ru_RU`, `en_US`).
- In duplex mode, keep `say` and `listen -l <lang>` aligned.
- `say` auto-downloads missing Piper model on first use.

## Initialization (Linux & macOS)

Run bootstrap once:

```bash
"${SKILL_DIR}/scripts/_bootstrap"
```

Bootstrap installs to `~/.local/bin`:

- `say`
- `listen`
- `listen-server`

## Platform Support

- Linux: `piper` + `aplay`, `faster-whisper`, `arecord`/`pyaudio`
- macOS: `piper` + `afplay`, `faster-whisper`, `sox`/`pyaudio`
