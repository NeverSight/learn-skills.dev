---
name: mage-music-video
description: |
  Make saved characters perform a music video to an audio track with Mage: one
  to three performers sing and dance in sync with up to 15 seconds of music,
  with cinematic camera work and optional reference images for the setting or
  look. The Music Video app as a skill, on Cherry 2 Pro by default. Use when:
  "music video", "make my character sing this song", "make them dance to this
  track", "performance video for my song", "my AI artist performing", "a band
  of my characters playing this", "turn this track into a video". NOT for: a
  single subject speaking a voice clip (mage-lipsync), copying a specific
  dance from a reference video (mage-video-character-swap on that video), a
  narrated explainer (mage-faceless-video), making the music itself
  (mage-generate), or music the user has no right to use.
license: MIT
compatibility: Requires the Mage connector (https://mcp.mage.space/mcp) and a Mage account with Gems.
metadata:
  author: mage-space
  version: "0.0.0" # x-release-please-version
---

# Mage Music Video

Put one to three characters on screen performing a track: singing, dancing, and moving with the music. This is the [Music Video app](https://www.mage.space/apps/music-video) as a skill: the same prompt and models, run through the Mage connector.

## Before you start

1. **Mage tools:** `get_model`, `estimate_cost`, `generate`, `get_request`, `list_characters`, `create_character`, `list_references`, `create_reference`, and `create_upload` for local files. If they are missing, ask the user to connect Mage (Claude: Customize → Connectors → Add custom connector, `https://mcp.mage.space/mcp`; Claude Code: `/mcp` to sign in if the Mage plugin is installed, otherwise `claude mcp add --transport http mage https://mcp.mage.space/mcp`; others: https://www.mage.space/mcp), then wait.
2. **Inputs are links:** https URLs of the files themselves, data URLs under about 3 MB, uploads from disk (`create_upload`, when you can run commands), or earlier Mage results. Files attached to the chat never reach Mage: ask for a direct link.
3. **Rights.** Use music the user has the right to use, and only make a real person perform with that person's consent. Mage's usage rights cover what is generated, not music that wasn't licensed.

## UX rules

1. Don't ask for what the request already gives. Ask for everything that is missing in one compact question, then wait.
2. Send the app's prompt below word for word. Fill in only the marked slots; don't rewrite, translate, or add to it.
3. Always quote the model and the price in Gems and wait for a yes before generating.
4. Deliver the link with a one-line label (model, size or length, Gems spent). No prompts, ids, or JSON. Reply in the user's language. Links last 30 days.

## Inputs

**Performers (1 required, up to 3):** saved characters, by `@handle`. `list_characters` shows them. The app takes characters here, not loose images, so if the user gives a picture of a performer, save it first with `create_character` (free; ask for a name) and use the handle. No character at all? Build one with `mage-character-builder`.

**The track (required):** up to 15 seconds of music.

1. **A saved audio reference:** use its `@handle` (`list_references` with `kind: "audio"`).
2. **A clip (MP3 or WAV link, or a file on disk):** save it with `create_reference` (`kind: "audio"`, `audio`, and a `name` taken from the file name or the user's description), which returns its `@handle`. Mage trims it to 15 seconds, the same limit as the app. Saving is free; tell the user the handle it was saved under.
3. **No audio yet:** offer to generate a track with Seed Audio (`seed_audio`, `duration` `"5"` or `"10"`): give the genre, tempo, instruments, mood, and any sung words in quotes, quote the price, then save the result with `create_reference` as above.

Know the audio's length in seconds: measure it when you can run commands (`ffprobe -v error -show_entries format=duration -of csv=p=0 clip.mp3`), use the `duration` you asked Seed Audio for, or ask. Anything over 15 counts as 15.

**Reference images (optional, up to 3):** a setting, a stage, a prop, or a look. Image links.

**Direction (optional):** setting, wardrobe, or mood, in the user's words, as a sentence of its own ("A neon rooftop at night.").

## Prompt

The app's fixed prompt:

```
Generate a music video of the characters in the reference images performing to the provided audio track.

The characters sing and dance in sync with the music for its full length. Their movements, energy, and expressions follow the rhythm and mood of the track. The camera moves cinematically with dynamic framing, like a professionally shot music video. Each character keeps the exact appearance and identity from their reference image.
```

Build what you send in this order, with a blank line between parts:

1. The fixed prompt, exactly.
2. If the user gave direction: the line `Also follow these custom instructions:` and their direction on the next line, as they wrote it.
3. One line of mentions, so Mage attaches the saved items: `Performers: @one, @two. Audio track: @track-handle` (with one performer, `Performers: @one. Audio track: @track-handle`). The fixed prompt stays plural either way.

The app attaches the characters and the track directly. The connector attaches them from `@handle` mentions, which is the only reason for the last line.

## Settings

- Model: Cherry 2 Pro (`cherry`, `model_id: "cherry-2-pro"`), Mage's default for video. When the user asks for another model, use it.
- `resolution`: `480p`, the cheapest. Offer `720p` or `1080p` with the price when the user wants a final.
- `duration`: the shortest option that covers the track: `"4"`, `"5"`, `"8"`, `"10"`, or `"15"`.
- `aspect_ratio`: `9:16`, a short-form vertical clip.
- `use_character_voices: false`, so the track is the only audio.
- Reference images go in `image` (the first) and `additional_images` (the rest), never `first_image`. Performers are mentions only.

Other models the app offers (Lemon, the other Cherry models, Plum, Plum Max): `references/models.md`.

## Run

```json
{
  "model_id": "cherry-2-pro",
  "resolution": "480p",
  "duration": "<covers the track>",
  "aspect_ratio": "9:16",
  "use_character_voices": false,
  "image": "<optional first reference image>",
  "additional_images": [
    "<optional others>"
  ],
  "prompt": "<fixed prompt>\n\nAlso follow these custom instructions:\n<optional direction>\n\nPerformers: @one, @two. Audio track: @track-handle"
}
```

Leave `image` and `additional_images` out when there are no reference images.

1. `get_model` for the architecture, once per conversation, to confirm its fields, options, and rules.
2. `estimate_cost` with the exact config. Tell the user the model, resolution, length, and price in Gems, and **wait for a yes**. Video is expensive and the price climbs with resolution and length.
3. `generate` with a new UUID as `idempotency_key`, then `get_request` with `wait_seconds: 120`, repeated quietly until the status is `completed`, `failed`, or `cancelled`. Video takes minutes.

`duration` and `resolution` are strings, written exactly as `get_model` lists them (`"4"`, `"480p"`, and on Plum `"768P"`).

## Check and deliver

Deliver the link with the model, resolution, length, and Gems. The movement is generated, so the choreography can't be chosen: for a specific dance, swap the character into a video of that dance with `mage-video-character-swap`. For a longer song, make it in 15-second sections with the same characters and direction.

## Errors

| Code | What to do |
|---|---|
| `insufficient_gems` | Give the price and the balance; Gems are added at https://www.mage.space/api?tab=billing. |
| `invalid_config` | The message names the field, value, or `@handle`. Fix it from `get_model` and retry with a new key. |
| `content_blocked` | Mage's policy or the model's filter refused it. Never try to slip past a filter. |
| `too_many_requests` | 20 generations are already running. Wait, then submit again. |
| `generation_failed` | Usually transient and refunded. Retry once with a new key. |

## References

- `references/models.md`: every model the app offers for music videos, with ids, resolutions, and durations.
