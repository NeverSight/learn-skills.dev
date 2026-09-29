---
name: hyperframes-media
description: Prepare Fish official-API narration, OpenAI word timestamps, and reviewed user-supplied local music/SFX for HyperFrames. Also covers captions, optional stock APIs and background removal. No private service, browser-session proxy, voice, or music library is bundled.
---

# HyperFrames media

Use [fish-audio-api](../fish-audio-api/SKILL.md) for narration and [media-use](../media-use/SKILL.md) to ingest reviewed local assets. This package supplies workflows and code; users supply accounts, permitted voices, music, sound effects, images and video.

## Requirements and scope

Node >=22.20 and FFmpeg/ffprobe must be on PATH. Read [requirements](references/requirements.md) before generation. The engine loads the video project's `.env`; existing environment values win. Fish uses its official API with `FISH_API_KEY` and `FISH_REFERENCE_ID`. Word timing uses OpenAI `whisper-1` with `OPENAI_API_KEY`, or an explicitly configured OpenAI-compatible `WHISPER_API`.

The shared engine performs one POST per requested narration line and one transcription POST. Neither is automatically retried. It preflights both API configurations before creating voice audio. A whole `--only tts` rerun creates narration again; use the scaffolded paragraph pipeline for cached/surgical revisions. All generated audio needs listening review.

## Shared engine

```sh
node <MEDIA_DIR>/scripts/audio.mjs --request audio_request.json --hyperframes . --out audio_meta.json --only tts
node <MEDIA_DIR>/scripts/audio.mjs --request audio_request.json --hyperframes . --out audio_meta.json --only bgm,sfx
```

The second command needs no API credentials. It preserves and validates any existing voice metadata. Example request (all files shown must be supplied by the user):

```json
{
  "lang": "zh",
  "fish": {
    "transport": "official-api",
    "request": { "normalize": true, "prosody": { "speed": 1 } }
  },
  "lines": [
    { "id": "s0", "text": "这是一段待审听的旁白。", "sfx": [
      { "name": "confirmation", "path": "library/confirmation.wav", "offset_s": 0.2 }
    ] }
  ],
  "bgm": { "path": "library/underscore.wav", "source": "reviewed-local", "volume": 0.18 }
}
```

`fish.reference_id` and `fish.model` are optional project overrides; no personal voice is supplied. `fish.request` uses official API fields, such as top-level `temperature`, `top_p`, `normalize` and `prosody`. The adapter owns text, reference ID and WAV format. It rejects credential-like fields and website `backend` configuration.

Output freezes `assets/voice/<id>.wav` and returns `voices[].words` as `{id,text,start,end}`. `voice_id`, `fish_model` and `fish_transport` describe the resolved non-secret profile. API keys and error bodies are never persisted. A transcription failure stops delivery with the voice WAV still on disk; do not invent word timing or claim captions are synchronized.

BGM/SFX come only from explicit local paths or the user's project manifest. Missing/non-audio files produce anomalies and are skipped; they never trigger search, generation or a fallback library. Review every anomaly before final delivery. Frozen files have content hashes so repeated filenames do not overwrite unrelated sources.

## Discovery and approval

In a scaffolded project, use `npm run audio:discover -- --type sfx --query "confirmation"`. No review catalogs are included. Install `media-use` in `.agents/skills`, or set `MEDIA_USE_SKILL_DIR` to that skill directory; set `MEDIA_CATALOG` or pass `--catalog` for your own workspace-local catalog. Empty search results mean the user must supply or select media. Catalog membership is not approval: audition, record source/license/hash and a review note, then ingest the exact bytes through `media-use`.

## Reference guide

| Need | Read |
|---|---|
| Accounts, environment and optional tools | [requirements](references/requirements.md) |
| Fish request configuration | [tts](references/tts.md) |
| Words and timing | [transcription](references/transcribe.md), [TTS to captions](references/tts-to-captions.md) |
| Caption authoring and cleanup | [authoring](references/captions/authoring.md), [transcript handling](references/captions/transcript-handling.md) |
| Local music and sound effects | [BGM](references/bgm.md), [SFX](references/sfx.md) |
| Audition, gain matching, revisions | [audio review](references/audio-review-and-revision.md) |
| Optional stock APIs | [stock media](references/stock-media-apis.md) |
| Optional background-removal tooling | [background removal](references/remove-background.md) |

API credentials do not replace the user's authorization for generation. Stay within the requested scope, preview a short sample, preserve original audio and keep listening/review decisions distinct from technical validation.
