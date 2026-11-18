---
name: voice-direction
description: Directs voiceover like a voice director, casting the voice, marking up the script for performance, and writing prompts and settings for TTS models like ElevenLabs. Use when the user wants a voiceover, narration audio, TTS, an AI voice, ElevenLabs prompts, audio tags, voice casting or design, expressive delivery, pronunciation fixes, or says the AI voice sounds flat, robotic, overacted or inconsistent.
license: MIT
metadata:
  version: "0.1.0"
  status: beta
  category: production
  pack: creator-skills
---

# Voice Direction

Voice decides whether a script feels human. A great script read flat sounds like AI slop; an average script read like a real person telling you something sounds alive. You're the voice director: you cast, you mark up the script, you run the takes, and you stop chasing a take that isn't coming.

## The floor

1. **Cast before you prompt.** Decide who this voice is (age, texture, energy, attitude, the relationship to the listener) before picking a voice ID.
2. **Direct the intention, not the sound.** "Telling a friend something you can't believe happened" beats "excited voice".
3. **Fewer tags, better placed.** One delivery cue per clause at most. A tag carries forward until the next one. Over-tagging makes the model overact. [verified for ElevenLabs v3/v4, see model card]
4. **Write for the model's ears.** Spell out numbers, dates, abbreviations and symbols. Respell names that get mangled.
5. **Generate in chunks** (a scene or paragraph), not the whole script and not word by word. Chunks keep tone consistent and make retakes cheap.
6. **One variable per retake.** Change the tag, *or* the punctuation, *or* the setting, *or* the voice. Never all at once.
7. **Three-strike rule.** If a line fails three retakes, stop. Rewrite the line, split it, or change approach. Looping on the same prompt burns credits and patience.
8. **Check freshness.** Before using model-specific features, check the `verified:` date on the model card. Older than 60 days: re-read the official docs first.

## Procedure

1. **Read the script** (production format) and the bible. Note the profile's energy and the target wpm.
2. **Write the casting brief** (below). If a voice is locked in the bible, use it and skip to step 4.
3. **Audition** with the protocol in [references/audition-protocol.md](references/audition-protocol.md): 3 voices × 2 settings on the same 20-second excerpt, labeled blind, user ranks.
4. **Mark up the script** for the chosen model ([references/tts-markup.md](references/tts-markup.md)): normalization, pacing punctuation, audio tags where delivery matters.
5. **Produce the VO pack** (below): chunked text, settings, and notes per chunk.
6. **Review takes** against the direction notes. Retake with one change at a time, three strikes max per line.
7. **Lock it.** Write voice ID, model, settings, tag vocabulary and pronunciation fixes into `.creator/bible.md` under `audio.voiceover` so every future episode sounds the same.

## Casting brief

```markdown
## Casting: <project>
Who: <e.g., a 35-year-old history nerd who tells stories at bars; amused, never smug>
Relationship to listener: <friend | teacher | insider | narrator from above>
Texture: <warm, slightly gravelly, close-mic, not radio-polished>
Energy: <punchy, fast but clear>     Pace: <~170 wpm>     Accent: <neutral American | ...>
Range needed: <deadpan → disbelief → quiet on the deaths>
Avoid: <announcer voice, upward inflection on every line, breathy ASMR>
```

## VO pack (output)

```markdown
## VO pack: <title>
Model: eleven_v4 (verified 2026-10-19)    Voice: <name / id>    Settings: <per model card>
Pronunciations: Purity → "PURE-ih-tee"

### Chunk 1 · HOOK (0:00–0:03)
Direction: deadpan, like stating the weather. Let "molasses" land.
Text:
In nineteen nineteen... a wave of molasses killed twenty-one people.

### Chunk 2 · SETUP
Direction: friendly, a bit amused.
Text:
[amused] The tank was fifty feet tall. And it leaked. From day one.
```

## Direction vocabulary (works for humans and models)

| Note | Means |
|---|---|
| "Tell one person" | Intimate, conversational; kills announcer voice |
| "Throw it away" | Casual, underplayed; good for dry jokes |
| "Lean in" | Quieter, closer, conspiratorial |
| "Land it" / "button it" | Finish the line with weight, falling pitch |
| "Punch the word" | Stress one word (CAPS can do this in some TTS models) |
| "Let it breathe" | Pause after; the silence does the work |
| "Smile through it" | Warmth in the voice without laughing |
| "Don't sell it" | Stop overacting; trust the line |

## References

| File | Read when |
|---|---|
| [references/elevenlabs.md](references/elevenlabs.md) | Using ElevenLabs: models, audio tags, settings, limits (dated model card) |
| [references/tts-markup.md](references/tts-markup.md) | Preparing script text for any TTS: numbers, names, pacing, tags |
| [references/audition-protocol.md](references/audition-protocol.md) | Casting a voice; running expression experiments; logging results |
