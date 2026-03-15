---
name: text-to-speech
description: "Produce actual audio output from the computer's speakers using text-to-speech. Use this skill when the user asks to speak, say something out loud, talk, vocalize, read aloud, announce, play audio from text, or produce voice output. Can use OS-native commands (macOS say, Linux espeak) or high-quality API-based TTS (OpenAI). The key point: this MUST produce real sound, not just text."
tags:
  [
    audio,
    speech,
    voice,
    text-to-speech,
    tts,
    vocalization,
    say,
    speak,
    talk,
    read-aloud,
    announce,
    sound,
    auto-generated,
  ]
version: 0.2.0
---

# Skill: text-to-speech

## When to Use

Use this skill when the user asks to:

- Say something out loud / speak / talk
- Read text aloud or announce something
- Generate audio from text
- Create a voice message or spoken output
- Use text-to-speech / TTS
- Produce audible output from the computer speakers

CRITICAL: This skill produces REAL AUDIO from the speakers. NOT just text.

## Input Parameters

| Parameter      | Required | Description                | Example              |
| -------------- | -------- | -------------------------- | -------------------- |
| `text_content` | Yes      | The text to speak out loud | hello I am P-H-P Bot |

## Procedure

1. Extract the text content from the user's request
2. Try the simplest approach first — use the OS built-in TTS:
   - **macOS**: `say "{{TEXT_CONTENT}}"` (zero dependencies, instant)
   - **Linux**: `espeak "{{TEXT_CONTENT}}"` or `spd-say "{{TEXT_CONTENT}}"`
   - Verify it worked (exit code 0)
3. If higher quality is needed or the simple approach fails, escalate:
   - Check for an OpenAI API key: `get_keys` → `search_computer` → `ask_user`
   - Generate speech via API: `curl` the OpenAI TTS endpoint, save to MP3
   - Play the MP3: `afplay` (macOS) or `mpv`/`aplay` (Linux)
4. Confirm to the user that audio was played from the speakers

## Reference Commands

```bash
# Simplest: macOS built-in (try this first)
say "hello I am P-H-P Bot"

# With voice selection
say -v Samantha "hello I am P-H-P Bot"

# Higher quality: OpenAI TTS API → play result
curl -s https://api.openai.com/v1/audio/speech \
  -H "Authorization: Bearer ${OPENAI_API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{"model":"tts-1","input":"hello I am P-H-P Bot","voice":"alloy"}' \
  --output /tmp/speech.mp3 && afplay /tmp/speech.mp3
```

## Example

```
talk out loud and say "hello I am P-H-P Bot"
say "good morning" out loud
speak the following text: welcome to PHP Bot
read this aloud: the quick brown fox
```
