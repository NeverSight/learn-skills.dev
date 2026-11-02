---
name: mage-lipsync
description: |
  Make the subject of a single image speak an audio clip with Mage: lip
  movements sync to the audio with natural expressions, and the look, framing,
  and setting of the image stay. Takes a portrait or a saved character, plus a
  voice clip of up to 15 seconds (or generates one with Seed Audio). The
  Lipsync app as a skill, on Cherry 2 Pro by default. Use when: "lip sync",
  "lipsync", "make this photo talk", "make her say this audio", "talking head
  from this image", "animate this portrait to my voiceover", "give my
  character a voice and make them speak". NOT for: characters singing and
  dancing to music (mage-music-video), a spokesperson product video
  (mage-ugc-video), dubbing or editing an existing video (mage-video-editor),
  or putting words in a real person's mouth without their consent.
license: MIT
compatibility: Requires the Mage connector (https://mcp.mage.space/mcp) and a Mage account with Gems.
metadata:
  author: mage-space
  version: "0.0.0" # x-release-please-version
---

# Mage Lipsync

Turn one image and one audio clip into a talking video: the subject's mouth follows the audio, and everything else about the image holds. This is the [Lipsync app](https://www.mage.space/apps/lipsync) as a skill: the same prompt and models, run through the Mage connector.

## Before you start

1. **Mage tools:** `get_model`, `estimate_cost`, `generate`, `get_request`, `list_characters`, `list_references`, `create_reference`, and `create_upload` for local files. If they are missing, ask the user to connect Mage (Claude: Customize → Connectors → Add custom connector, `https://mcp.mage.space/mcp`; Claude Code: `/mcp` to sign in if the Mage plugin is installed, otherwise `claude mcp add --transport http mage https://mcp.mage.space/mcp`; others: https://www.mage.space/mcp), then wait.
2. **Inputs are links:** https URLs of the files themselves, data URLs under about 3 MB, uploads from disk (`create_upload`, when you can run commands), or earlier Mage results. Files attached to the chat never reach Mage: ask for a direct link.
3. **Consent.** Harmful deepfakes are forbidden on Mage. Only use a real person's face, body, or voice with that person's permission, and never to deceive, harass, or sexualize. When the user hasn't said whose likeness it is, state this rule in one line with the price instead of questioning them; if they say they lack permission, stop.

## UX rules

1. Don't ask for what the request already gives. Ask for everything that is missing in one compact question, then wait.
2. Send the app's prompt below word for word. Fill in only the marked slots; don't rewrite, translate, or add to it.
3. Always quote the model and the price in Gems and wait for a yes before generating.
4. Deliver the link with a one-line label (model, size or length, Gems spent). No prompts, ids, or JSON. Reply in the user's language. Links last 30 days.

## Inputs

Both are required. Ask for whichever is missing.

**The subject:** the person or character that speaks, facing the camera with the mouth visible. An image link, or a saved character by `@handle`.

**The audio:** the speech the subject performs, up to 15 seconds.

1. **A saved audio reference:** use its `@handle` (`list_references` with `kind: "audio"`).
2. **A clip (MP3 or WAV link, or a file on disk):** save it with `create_reference` (`kind: "audio"`, `audio`, and a `name` taken from the file name or the user's description), which returns its `@handle`. Mage trims it to 15 seconds, the same limit as the app. Saving is free; tell the user the handle it was saved under.
3. **No audio yet:** offer to generate the line with Seed Audio (`seed_audio`, `duration` `"5"` or `"10"`): quote the words and describe the voice, quote the price, then save the result with `create_reference` as above.

Know the audio's length in seconds: measure it when you can run commands (`ffprobe -v error -show_entries format=duration -of csv=p=0 clip.mp3`), use the `duration` you asked Seed Audio for, or ask. Anything over 15 counts as 15.

**Scene direction (optional):** a new background, outfit, or mood, in the user's words.

## Prompt

The app's fixed prompt:

```
Generate a video of the subject in the reference image speaking the provided audio.

The subject's lip movements sync precisely to the audio for its full length. The subject keeps the exact appearance, framing, lighting, and setting of the reference image. The subject shows natural facial expressions and subtle head movement while speaking. The camera holds steady on the subject.
```

Build what you send in this order, with a blank line between parts:

1. The fixed prompt, exactly.
2. The user's scene direction, if there is any, as a sentence of its own ("She is standing in a sunny park.").
3. One line of mentions, so Mage attaches the saved items: `Audio: @audio-handle` with an image subject, or `Subject: @character-handle. Audio: @audio-handle` with a saved character.

The app attaches the character and the audio directly. The connector attaches them from `@handle` mentions, which is the only reason for the last line.

## Settings

- Model: Cherry 2 Pro (`cherry`, `model_id: "cherry-2-pro"`), Mage's default for video. When the user asks for another model, use it.
- `resolution`: `480p`, the cheapest. Offer `720p` or `1080p` with the price when the user wants a final.
- `duration`: the shortest option that covers the audio: `"4"`, `"5"`, `"8"`, `"10"`, or `"15"`.
- `aspect_ratio`: `9:16`, a talking-head framing.
- `use_character_voices: false`, so the chosen audio is the only voice.
- An image subject goes in `image`, not `first_image` (Blueberry is the one exception: see the reference). A saved character is a mention only.

Other models the app offers (Lemon, the other Cherry models, Plum, Plum Max, Blueberry, Blueberry 2): `references/models.md`.

## Run

```json
{
  "model_id": "cherry-2-pro",
  "resolution": "480p",
  "duration": "<covers the audio>",
  "aspect_ratio": "9:16",
  "use_character_voices": false,
  "image": "<the subject image>",
  "prompt": "<fixed prompt>\n\n<optional scene direction>\n\nAudio: @audio-handle"
}
```

1. `get_model` for the architecture, once per conversation, to confirm its fields, options, and rules.
2. `estimate_cost` with the exact config. Tell the user the model, resolution, length, and price in Gems, and **wait for a yes**. Video is expensive and the price climbs with resolution and length.
3. `generate` with a new UUID as `idempotency_key`, then `get_request` with `wait_seconds: 120`, repeated quietly until the status is `completed`, `failed`, or `cancelled`. Video takes minutes.

`duration` and `resolution` are strings, written exactly as `get_model` lists them (`"4"`, `"480p"`, and on Plum `"768P"`).

## Check and deliver

Deliver the link with the model, resolution, length, and Gems. Tell the user to check the mouth against the audio at full speed. Profiles and covered mouths don't sync well: if the result is off, a front-facing image is the first thing to change.

## Errors

| Code | What to do |
|---|---|
| `insufficient_gems` | Give the price and the balance; Gems are added at https://www.mage.space/api?tab=billing. |
| `invalid_config` | The message names the field, value, or `@handle`. Fix it from `get_model` and retry with a new key. |
| `content_blocked` | Mage's policy or the model's filter refused it. Never try to slip past a filter. |
| `too_many_requests` | 20 generations are already running. Wait, then submit again. |
| `generation_failed` | Usually transient and refunded. Retry once with a new key. |

## References

- `references/models.md`: every model the app offers for lip sync, with ids, resolutions, durations, and what changes on Blueberry.
