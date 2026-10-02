---
name: ai-voice-humanizer
description: Make AI-generated voiceovers sound realistic and human using ElevenLabs. Use when creating AI voiceovers, formatting scripts for text-to-speech, generating voiceovers with ElevenLabs, editing AI voice in a DAW/NLE, dubbing videos to other languages, or anytime the user wants to make AI voice sound less robotic and more natural. Also use when the user mentions "AI voice," "voiceover," "ElevenLabs," "TTS," "text to speech," "voice clone," "dubbing," or "realistic AI audio."
---

# AI Voice Humanizer

Make AI voiceovers sound indistinguishable from human speech. Based on proven techniques from professional YouTube creators generating hundreds of AI voiceovers.

## The 4 Elements of Realistic AI Voice

Every realistic-sounding AI voice nails these four things:

1. **Tone variation** -- Change between monotonous and excited. Flat = robotic. Dynamic = human.
2. **Strategic pauses** -- Don't cut all pauses. Pause on important points for impact and naturalness.
3. **Word emphasis** -- Stress key words to create rhythm and conviction.
4. **Human-written scripts** -- AI-written scripts make even the best AI voice sound robotic. Viewers can tell.

## Voice Setup (ElevenLabs)

### Voice Selection (3 options)

| Method | When to use | How |
|--------|-------------|-----|
| **Clone your voice** | Want your own voice but AI-generated | Voices > Clone a Voice > Instant Voice Clone. Upload a sample. Professional clone needs 30+ min sample. |
| **Voice library** | Want a pre-made voice fast | Browse the voice library and pick one |
| **Custom voice design** | Want a unique branded voice nobody else has | Voices > Create a Voice > Voice Design. Describe the voice in natural language. |

Custom voice design prompt example:
> "A young man in his 20s, american accent, speaking with quirky but charismatic style. Speaks with a lot of emotions and variances in his speech, changes the tone and speed continuously throughout the speech."

Reduce guidance slider for more creative variation.

### Model Selection

Use **V2 model** (Eleven Multilingual v2). V3 is newer but can alter voice identity unpredictably.

### V2 Slider Settings

- **Speed**: Increase slightly
- **Stability**: Reduce (lower = more expressive, more human)
- **Similarity**: ~70%
- **Style exaggeration**: Increase (adds expressiveness)

## Script Formatting for ElevenLabs

This is where most of the humanization happens. See [references/script-formatting.md](references/script-formatting.md) for the full formatting guide with before/after examples.

Quick reference:

| Technique | Markup | Effect |
|-----------|--------|--------|
| Emphasis | `ALL CAPS` | Stresses the word |
| Excitement | `!` or `!!` | Energetic, excited delivery |
| Disappointment/confusion | `...` (3 dots) | Slower, uncertain tone |
| Natural pause | `...` or `,` | Brief pause in speech |

**Before:** `We tested this for six months. The results were not what we expected.`
**After:** `We tested this for SIX months! The results... were not what we EXPECTED!!`

## The Secret Sauce: Small-Batch Generation

**Never paste your entire script and hit generate.** This creates an uncanny AI pattern that listeners can feel even if they can't articulate it.

### The technique:

1. Select **2-4 sentences** from your script
2. Apply formatting (caps, punctuation, ellipses)
3. Generate the voiceover
4. Use the **2 free regenerations** -- download ALL versions (original + 2 regens)
5. Move to the next 2-4 sentences and repeat

### Why this works:

Each generation produces slightly different tone and speed. Real humans never speak with perfectly consistent delivery. By generating in small batches and getting multiple takes, you create natural tonal variation that eliminates the uncanny AI pattern.

## Editing Workflow

See [references/editing-workflow.md](references/editing-workflow.md) for the full post-production pipeline.

Key steps:
1. Import all generated clips into your NLE (Premiere Pro, DaVinci, etc.)
2. **Choose best takes** per section -- listen to all versions, pick what fits context
3. **Frankenstein technique** -- chop best parts from different generations of the same sentence and splice them together
4. **Cut dead air** between sentences, but keep intentional pauses at important moments
5. **EQ processing** -- high-pass filter, reduce echo-y frequencies, apply voice preset
6. Don't use built-in speed changers (they distort pitch even with "maintain pitch" on)

## Dubbing Videos to Other Languages

See [references/dubbing-workflow.md](references/dubbing-workflow.md) for the step-by-step dubbing pipeline.

Key insight: Only ~20% of YouTube's 2.5B users speak English. Adding 5 more languages reaches ~50% of YouTube. Creators who dub (MrBeast, Mark Rober) see 2-3x view/subscriber growth.

Quick workflow:
1. Export voiceover-only MP3 and music+SFX-only MP3 separately
2. ElevenLabs > Dubbing tab > upload voiceover > select target language
3. Align dubbed track with original timing in your editor
4. Apply EQ preset, export audio
5. Upload to YouTube Studio under Languages > add dubbed audio track
6. Translate title + description

## Voice Presets (FFmpeg)

This skill includes a CLI script that applies a set of voice processing chains with FFmpeg. No Premiere Pro or other DAW required.

**Processing chain adapted from Isaac's (ISAACVERSE) Premiere presets.**

```bash
# Apply the voice enhancer (the main one for AI voiceover production)
python3 scripts/voice_preset.py input.wav voice-enhancer

# List all available presets
python3 scripts/voice_preset.py --list

# Preview the FFmpeg command without running
python3 scripts/voice_preset.py input.wav movie-trailer --dry-run
```

Run this from the skill's own directory, or prefix the script with the install path (for example `<path-to-skill>/scripts/voice_preset.py`). Requires FFmpeg on your PATH.

### Available presets

**Useful (production):**

| Preset | What it does |
|--------|-------------|
| `voice-enhancer` | Compression + noise gate + EQ (HP 34Hz, +1.1dB@75Hz, -0.9dB@246Hz, +4dB shelf@15kHz) |
| `movie-trailer` | Limiter + amp + compression + de-ess + dual EQ (deep, broadcast quality) |
| `deeper-voice` | Pitch down 5 semitones |
| `echo` | Studio reverb (60/40 dry/wet) |
| `muffled` | -17.5dB high shelf at 7kHz (through-the-wall) |
| `noise-remover` | Gate + high-pass |
| `phone-call` | Telephone bandpass (300-3400Hz, +4.6dB@1638Hz) |

**Fun (creative effects):** `90s`, `alien-voice`, `chipmunk`, `inner-monologue`, `pilot-voice`, `robot-voice`, `villain-voice`

For complete extracted Premiere Pro parameter values, see [references/premiere-pro-presets-raw.md](references/premiere-pro-presets-raw.md).

## YouTube Monetization

YouTube allows AI voices and monetization of AI-voiced content, as long as the content itself is original (not compilations).
