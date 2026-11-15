---
name: darija-word-captions
description: Word-by-word captions that stay in sync with speech that switches between Moroccan Darija, Arabic, French and English. Transcribes with a speech-to-text model, times every word with local forced alignment (WhisperX + wav2vec2), then renders the captions with HyperFrames or Remotion. Use when someone asks for word-by-word, karaoke-style or synced captions on a Darija or mixed-language talking video.
---

# Darija word-by-word captions

Accurate captions need two models:
1. **Speech-to-text** writes the words.
2. **Forced alignment** gives every word the time it starts and ends.

Then an editing tool styles and renders the captions on the video.

Rules that keep the result accurate:
- Darija and Arabic stay in **Arabic script**. English and French stay in **Latin script**, exactly as spoken. Never translate, never transliterate.
- Timing comes **only** from acoustic alignment. Never spread words evenly across a sentence and never guess times. A word that cannot be aligned is reported, not invented.
- The displayed words never change to make alignment easier. Use pronunciation aliases instead (step 3).

---

## Prerequisites

Install once:

| Need | Install |
|---|---|
| Python 3.10+ | python.org or `brew install python` |
| FFmpeg | `brew install ffmpeg` (macOS) · `sudo apt install ffmpeg` (Linux) |
| WhisperX (runs the alignment models) | `pip install whisperx==3.8.6` |
| Node.js 18+ (for the editing tool) | nodejs.org or `brew install node` |

Alignment models (downloaded automatically on first run, then cached):

| Language | Model |
|---|---|
| Darija / Arabic | `jonatasgrosman/wav2vec2-large-xlsr-53-arabic` (Hugging Face) |
| French | `jonatasgrosman/wav2vec2-large-xlsr-53-french` (Hugging Face) |
| English | `WAV2VEC2_ASR_BASE_960H` (torchaudio, WhisperX's English default) |

Speech-to-text, pick one:

| Option | Model | Access |
|---|---|---|
| Gemini Flash | `gemini-3.1-flash-lite` | Gemini API key (cheap, fast) |
| Gemini 3.5 Transcribe | `gemini-3.5-transcribe` | Gemini API key |
| Microsoft | `MAI-Transcribe-2` | Azure Speech key + region |
| Local, free | `atlasia/moulsot.v0.3` (made for Darija) | Hugging Face; needs a GPU or an Apple Silicon Mac |

Editing tool, pick one (both are agent skills):

| Tool | Install the agent skill |
|---|---|
| HyperFrames (HTML → video) | `npx skills add heygen-com/hyperframes` |
| Remotion (React → video) | `npx skills add remotion-dev/skills` |

API keys go in environment variables (for example `GEMINI_API_KEY`). Never paste a key into a file you share.

---

## Workflow

### 0. The script
The alignment script is `scripts/align_words.py`, next to this SKILL.md. Run it from there.

### 1. Prepare the audio
```bash
ffmpeg -i input.mp4 -vn -ac 1 -ar 16000 audio.wav
```
Optional: trim long pauses first (`silencedetect`), and apply any speed change to the audio **before** transcribing, so every timestamp is on the final clock.

Cut the audio into chunks of 10–30 seconds at pauses (`ffmpeg -af silencedetect=noise=-35dB:d=0.3`). Never cut inside a word. Record each chunk's start and end.

### 2. Transcribe each chunk
Ask the model for a **verbatim** transcript. A cleaned transcript drops fillers and repetitions, then no longer matches the audio, and alignment fails.

Prompt that works with Gemini:
> Transcribe ONLY this audio chunk exactly as spoken. The speaker mixes Moroccan Darija with English and occasional French. Write Darija in Arabic script and English or French in Latin letters. Do NOT transliterate English into Arabic. Keep every audible word, filler and repetition. Return JSON: segments [{start, end, text}] with short 2–5 second clauses, plus uncertain [{start, end, heard, reason}].

Re-transcribe any unclear window on its own, and fix names and brand spellings by hand.

### 3. Write transcript.json
```json
{
  "audio": "audio.wav",
  "provider": "gemini-3.1-flash-lite",
  "latin_default": "en",
  "aliases": {
    "24": "ربعة وعشرين",
    "OpenAI": "أوبن إيآي",
    "captions": "كابشنز"
  },
  "segments": [
    {"start": 0.0, "end": 4.4, "text": "هاد الـ captions كتبع كل كلمة"},
    {"start": 4.4, "end": 9.1, "spans": [
      {"lang": "ar", "text": "وقالو ليك"},
      {"lang": "fr", "text": "c'est pas encore disponible"}
    ]}
  ]
}
```
- `segments`: the chunk windows from step 1 with their text.
- `spans`: use them when one segment mixes French and English, so each run gets the right model.
- `aliases`: how a word **sounds**, for alignment only. The caption still shows the original word. Give every number an alias. In Darija speech, also give English and French words an Arabic-script alias: Darija speakers pronounce them with a Darija accent, and the Arabic model then places them well. The script cross-checks them with the native English or French model and keeps the stronger match.

### 4. Align
```bash
python scripts/align_words.py transcript.json --out captions/
```
Outputs:
- `captions/words.json`: every word with `start`, `end`, `score`, `lang`, `method`
- `captions/issues.json`: words to check (unaligned, overlaps, low confidence)
- `captions/evidence.json`: raw aligner output

If the script asks for aliases, add them and run it again. Fix every entry in `issues.json` before rendering. Wrong transcript text is the usual cause.

### 5. Render the captions
Give `words.json` to HyperFrames or Remotion and build one caption element per word (or per short group). Each one shows from its `start` and hides at the next word's `start`.

Display tips:
- **Mixed-direction text:** put the line in a right-to-left container, and keep consecutive English words in one left-to-right group (`<bdi dir="ltr">even in English</bdi>`). If every word is a separate inline block, the English comes out in reverse order.
- Standalone articles such as `الـ` can merge into the next word's caption, so no caption is only "الـ".
- Keep captions and video on the same clock. If you cut or speed up the video, apply the same change to the timestamps.

### 6. Check before you publish
Watch the opening, the middle, the end and every language switch. Say clearly whether a human has listened to the result. Automated checks do not prove that every word is right.

---

## Setup prompt

Paste this to your agent together with this file:

> I'm giving you a skill file, SKILL.md, for word-by-word captions on videos where I speak Moroccan Darija mixed with English and French.
> 1. Install it: `npx skills add benmouad-ai/darija-word-captions`, or put the folder in `~/.claude/skills/darija-word-captions/` (Claude Code) or your Codex skills folder.
> 2. Make sure `scripts/align_words.py` sits next to SKILL.md (it comes with the install).
> 3. Check and install the prerequisites: Python, FFmpeg, `pip install whisperx==3.8.6`, Node.js. Tell me what you installed.
> 4. Ask me which speech-to-text option I want (Gemini Flash, Gemini 3.5 Transcribe, Microsoft MAI-Transcribe-2, or local Moulsot) and how to provide the API key safely, as an environment variable.
> 5. Ask me which editing tool I want (HyperFrames or Remotion) and install its agent skill.
> 6. Run the full workflow on a short test clip (`test.mp4`) and show me `issues.json` and a rendered preview before we do a real video.
