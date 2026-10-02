---
name: heygen-creative
description: Produce talking-head ad video using HeyGen avatars. Wraps the project's heygen_processor.py to generate avatar-led ads from a script, splitting long audio into chunks and stitching the result. Use when the user wants founder-style, testimonial-style, or "talking-to-camera" ad video without filming a real person.
metadata:
  tags: ads, video, heygen, avatar, talking-head, creative
---

## When to use

- Founder-POV ad ("I built PFC because…")
- Testimonial-style script delivered by a chosen avatar
- Coach-explainer ad ("Three macros. Here's why we ignore the rest.")
- Quick A/B variants on the same script with different avatars / hooks

## Prerequisites

1. **HeyGen API key** — set `HEYGEN_API_KEY` in env.
2. **ffmpeg + ffprobe** on PATH (used to split the audio).
3. **OpenAI key** if you're generating the script's TTS audio with OpenAI
   (alternatively use ElevenLabs or a recorded VO — heygen accepts mp3).
4. **Avatar ID** — pick from HeyGen library or a custom avatar. Default in the
   processor is `Aditya_public_4`. PFC defaults are listed below.

## PFC default avatars

| Persona | Avatar ID | Use for |
|---|---|---|
| Founder voice | `Aditya_public_4` | Founder-POV, "I built this" |
| Female coach | `Brenda_public_3` | Coach-explainer, women's audience |
| Athlete | `Tyler_public_2` | Performance / lifters cohort |

(Update once the user confirms preferred custom avatars.)

## Project layout

```
creative/heygen/
  heygen_processor.py        # copied from Codex-content
  scripts/
    EXP-XXX-founder.md       # narration script
    EXP-XXX-founder.mp3      # rendered TTS audio (input)
ad-assets/heygen/
  EXP-XXX/
    chunks/                  # intermediate
    final.mp4                # stitched output
    manifest.json
```

## Process

1. **Write the script** (max 30s for IG/Reels, max 60s for feed). Hook in the
   first 1.2s. Pull voice rules from `brand-profile.json` (`voice.do_say` /
   `voice.do_not_say`).
2. **Generate TTS audio** (project default = OpenAI `tts-1-hd` voice `alloy`):
   ```bash
   python -m openai.tts ...   # or use the openai-tts skill
   ```
3. **Run the processor**:
   ```bash
   python creative/heygen/run.py \
     --script creative/heygen/scripts/EXP-001-founder.md \
     --audio  creative/heygen/scripts/EXP-001-founder.mp3 \
     --avatar Aditya_public_4 \
     --ratio 9:16 \
     --output ad-assets/heygen/EXP-001/
   ```
4. **The runner**:
   - Splits audio into ≤14s chunks
   - Calls HeyGen `/v2/video/generate` per chunk
   - Polls for completion
   - Stitches outputs with ffmpeg concat
   - Writes `manifest.json` with chunk IDs, durations, and final path
5. **Hand off** to `format-adapter` for dimension/aspect validation, then to
   Remotion if you want overlays (subtitles, three-macro ring chrome).

## Cost guardrail

HeyGen consumes credits per second of generated video. Before running a batch:
- Estimate seconds × $0.30 (rough) and confirm with user above $20.
- Cache TTS audio so we don't regenerate the voice on every avatar swap.

## Failure modes

- **API 401**: missing or stale `HEYGEN_API_KEY`. Set in env.
- **Chunk fails repeatedly**: shrink chunk length to 10s, increase max_retries.
- **Lip-sync drift on stitched video**: ffmpeg concat at chunk boundaries can
  produce pops. Use the `-c copy` mode and ensure all chunks use identical
  resolution + audio codec.
- **Avatar looks off-brand**: switch avatars or fall back to higgsfield Speak.

## Subtitles

Always burn captions for Meta — 85% of feed plays muted. Generate via the
`openai-tts` skill's `--captions` flag or use Whisper word-level timestamps
on the rendered audio, then composite via Remotion (see slideshow skill).
