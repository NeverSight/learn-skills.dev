---
name: gemini-tts
description: Generate speech from text using Google Gemini TTS. Use when creating voiceovers, narration, podcasts, or any text-to-speech task. Supports 70+ languages, style/emotion control via natural language prompts, and 30 prebuilt voices. Trigger on "Gemini TTS", "Google TTS", "voiceover", "narration", "text to speech", "speech generation".
license: MIT
compatibility: Requires Node.js 18+, ffmpeg, and internet access. Set GEMINI_API_KEY env var.
metadata: {"openclaw": {"requires": {"env": ["GEMINI_API_KEY"]}, "primaryEnv": "GEMINI_API_KEY"}}
---

# Gemini Text-to-Speech

Generate natural, expressive speech from text using Google Gemini TTS. Supports 70+ languages, 30 prebuilt voices, and style control via natural language prompts and audio tags.

> **Requirements:** Node.js 18+, ffmpeg, `@google/genai` npm package, `GEMINI_API_KEY` env var.

## Available Scripts

- **`scripts/generate-tts.mjs`** — All-in-one TTS generator with single-request consistency, silence-based splitting, and automatic trimming.

## Quick Start

### Single text to speech

```bash
npm install @google/genai
GEMINI_API_KEY=your-key node scripts/generate-tts.mjs \
  --text "Hello, welcome to our product!" \
  --output-dir public/vo \
  --voice Kore
```

### Multi-segment voiceover (consistent voice)

Create a `segments.json`:

```json
[
  { "id": "intro", "text": "Welcome to our product launch." },
  { "id": "features", "text": "Here are the three features you will love." },
  { "id": "close", "text": "Get started today at our website." }
]
```

Run:

```bash
GEMINI_API_KEY=your-key node scripts/generate-tts.mjs \
  --segments segments.json \
  --output-dir public/vo \
  --voice Kore \
  --director-notes "Tone: Warm, confident, inspiring. Style: Professional narrator with a vocal smile. Accent: Neutral American English. Pacing: Moderate."
```

Output (JSON to stdout):

```json
{
  "success": true,
  "segments": [
    { "id": "intro", "file": "public/vo/vo-intro.mp3", "duration": 3.25 },
    { "id": "features", "file": "public/vo/vo-features.mp3", "duration": 4.10 },
    { "id": "close", "file": "public/vo/vo-close.mp3", "duration": 2.80 }
  ],
  "totalDuration": 10.15,
  "fullAudioFile": "public/vo/vo-full.wav"
}
```

### Script Options

| Flag | Default | Description |
|------|---------|-------------|
| `--segments FILE` | — | JSON file with `[{id, text}]` segment definitions |
| `--text TEXT` | — | Single text to generate (alternative to `--segments`) |
| `--output-dir DIR` | — | Output directory for audio files (required) |
| `--voice NAME` | `Kore` | Prebuilt voice name (see Voices table) |
| `--model NAME` | `gemini-3.1-flash-tts-preview` | Gemini TTS model ID |
| `--director-notes TEXT` | — | Performance guidance: style, pacing, accent, breathing, articulation. Does not control gender/age (use `--voice` for that). |
| `--retries N` | `3` | Max retry attempts for API errors |
| `--trim` / `--no-trim` | `--trim` | Trim silence from segment boundaries |
| `--format FORMAT` | `mp3` | Output format: `mp3` or `wav` |

### Exit Codes

| Code | Meaning |
|------|---------|
| 0 | Success |
| 1 | Missing required arguments or env vars |
| 2 | API error after retries exhausted |
| 3 | ffmpeg not installed or processing failed |
| 4 | File I/O error |

## How It Works (Multi-Segment)

Gemini TTS does NOT guarantee voice consistency across separate API requests. The script solves this by:

1. Combining all segments into ONE prompt with `[3 second pause]` markers between them
2. Generating a single continuous audio file in one API call
3. Detecting silence gaps with ffmpeg `silencedetect` using adaptive thresholds (starts at noise=-35dB, d=1.5s, progressively relaxes). If an exact match is found, uses it directly. If a threshold jump occurs (too few → too many), regenerates audio with faster speech pacing to make inter-segment pauses more distinct, then retries detection.
4. Splitting at silence midpoints into individual segment files
5. Trimming residual silence padding (~1.5s per side) from each segment, keeping 0.15s breathing room

## Models

| Model | Best For |
|-------|----------|
| `gemini-3.1-flash-tts-preview` | Latest, most controllable, 200+ audio tags (default) |
| `gemini-2.5-flash-preview-tts` | Fast, good quality, general use |
| `gemini-2.5-pro-preview-tts` | Highest quality, complex performances |

## Voices

30 prebuilt voices:

| Voice | Gender | Character | Pitch |
|-------|--------|-----------|-------|
| Achernar | Female | Soft | Higher |
| Achird | Male | Friendly | Lower middle |
| Algenib | Male | Gravelly | Lower |
| Algieba | Male | Smooth | Lower |
| Alnilam | Male | Firm | Lower middle |
| Aoede | Female | Breezy | Middle |
| Autonoe | Female | Bright | Middle |
| Callirrhoe | Female | Easy-going | Middle |
| Charon | Male | Informative | Lower |
| Despina | Female | Smooth | Middle |
| Enceladus | Male | Breathy | Lower |
| Erinome | Female | Clear | Middle |
| Fenrir | Male | Excitable | Lower middle |
| Gacrux | Female | Mature | Middle |
| Iapetus | Male | Clear | Lower middle |
| Kore | Female | Firm | Middle |
| Laomedeia | Female | Upbeat | Higher |
| Leda | Female | Youthful | Higher |
| Orus | Male | Firm | Lower middle |
| Puck | Male | Upbeat | Middle |
| Pulcherrima | Male | Forward | Middle |
| Rasalgethi | Male | Informative | Middle |
| Sadachbia | Male | Lively | Lower |
| Sadaltager | Male | Knowledgeable | Middle |
| Schedar | Male | Even | Lower middle |
| Sulafat | Female | Warm | Middle |
| Umbriel | Male | Easy-going | Lower middle |
| Vindemiatrix | Female | Gentle | Middle |
| Zephyr | Female | Bright | Higher |
| Zubenelgenubi | Male | Casual | Lower middle |

## Director's Notes (`--director-notes`)

Performance guidance for the selected voice. Define only what matters — overspecifying limits the model's creativity and can worsen results.

The three most common directions are Style, Pacing, and Accent, but you can include any custom instructions relevant to the performance.

- **Style** — Emotional quality and delivery character. Be descriptive: `"Infectious enthusiasm — the listener should feel part of something exciting"` works better than just `"energetic"`. You can layer characteristics and use voiceover industry terms like "vocal smile".
- **Pacing** — Overall speed and rhythm variation. Can range from `"Speak as fast as possible"` to `"Incredibly slow and liquid, words bleed into each other, zero urgency"`.
- **Accent** — Be specific. `"British English as heard in Croydon, England"` works much better than `"British accent"`.

```bash
--director-notes "Style: Enthusiastic and sassy GenZ beauty YouTuber. Pacing: Extremely fast, rapid delivery like short-form video influencers. Accent: Southern California valley girl from Laguna Beach."
```

## Audio Tags

Inline `[brackets]` in segment text for per-word control. Override director-notes locally.

`[whispers]` `[shouting]` `[excited]` `[serious]` `[short pause]` `[laughs]` `[very fast]` `[very slow]` `[sarcastic]` `[curious]`

Creative tags work too: `[like dracula]`, `[whispering conspiratorially]`

Example: `"[excited] This changes everything! [short pause] Let me show you how."`

## References

- [Prompting Guide](references/prompting-guide.md) — Advanced prompt engineering for style, emotion, and accent
