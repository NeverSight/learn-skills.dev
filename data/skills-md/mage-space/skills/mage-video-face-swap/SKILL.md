---
name: mage-video-face-swap
description: |
  Swap a face into a video with Mage: the new identity (face, hair, skin,
  neck) is applied in every frame while the original pose, motion,
  expressions, lip movements, clothing, and background stay. The Video Face
  Swap app as a skill, on Cherry 2 Pro by default. Use when: "video face
  swap", "swap the face in this video", "put my character's face on this
  clip", "put my face in this video", "replace her face in the footage", "the
  face drifted in this clip, fix it". NOT for: face swaps in a still image
  (mage-face-swap), replacing the whole person with body and outfit
  (mage-video-character-swap), other video edits (mage-video-editor), lip sync
  to audio (mage-lipsync), or putting a real person into a video without their
  consent.
license: MIT
compatibility: Requires the Mage connector (https://mcp.mage.space/mcp) and a Mage account with Gems.
metadata:
  author: mage-space
  version: "0.0.0" # x-release-please-version
---

# Mage Video Face Swap

Replace the face and hair of the person in a video with another identity, keeping the performance: pose, motion, expressions, and lip movements. This is the [Video Face Swap app](https://www.mage.space/apps/video-face-swap) as a skill: the same prompt and models, run through the Mage connector.

## Before you start

1. **Mage tools:** `get_model`, `estimate_cost`, `generate`, `get_request`, `list_characters`, and `create_upload` for local files. If they are missing, ask the user to connect Mage (Claude: Customize → Connectors → Add custom connector, `https://mcp.mage.space/mcp`; Claude Code: `/mcp` to sign in if the Mage plugin is installed, otherwise `claude mcp add --transport http mage https://mcp.mage.space/mcp`; others: https://www.mage.space/mcp), then wait.
2. **Inputs are links:** https URLs of the files themselves, data URLs under about 3 MB, uploads from disk (`create_upload`, when you can run commands), or earlier Mage results. Files attached to the chat never reach Mage: ask for a direct link. A page that plays a video (YouTube, Instagram, a Drive preview) is not a file.
3. **The clip's length matters.** Each model accepts a range of clip lengths, and the price depends on the clip's length. Measure it when you can run commands (`ffprobe -v error -show_entries format=duration -of csv=p=0 clip.mp4`); otherwise ask the user how long it is. `estimate_cost` measures a clip that is a `create_upload` URL or an earlier Mage result, and answers `requires_media_measurement` for a clip on another host: upload it with `create_upload` to price it.
4. **Consent.** Harmful deepfakes are forbidden on Mage. Only use a real person's face, body, or voice with that person's permission, and never to deceive, harass, or sexualize. When the user hasn't said whose likeness it is, state this rule in one line with the price instead of questioning them; if they say they lack permission, stop. The user also needs permission for the footage itself.

## UX rules

1. Don't ask for what the request already gives. Ask for everything that is missing in one compact question, then wait.
2. Send the app's prompt below word for word. Fill in only the marked slots; don't rewrite, translate, or add to it.
3. Always quote the model and the price in Gems and wait for a yes before generating.
4. Deliver the link with a one-line label (model, size or length, Gems spent). No prompts, ids, or JSON. Reply in the user's language. Links last 30 days.

## Inputs

Both are required. Ask for whichever is missing.

1. **The video:** one clip, MP4, MOV, or WebM, with the person clearly visible. 4–30 seconds on the default model; other models differ (`references/models.md`).
2. **The face to swap in:** a clear, front-facing image. Either an image link, or a saved character by `@handle` (`list_characters` shows them; build one with `mage-character-builder` or save one with `mage-characters`).

## Prompt

The app's swap prompt:

```
Replace the face and hair of the person in the video with the identity from the reference image.

Modify the entire head region (face, skin, ears, hair, hairstyle, hair color, and visible neck) to match the subject in the reference image in every frame, while preserving the original pose, motion, facial expressions, lip movements, camera angle, framing, and composition of the video.

Replace the hairstyle completely — use the hair length, texture, color, and styling from the reference image throughout the video.

Keep skin tone, texture, and color fully harmonized across the entire head and neck so the swapped face blends naturally with the body in every frame. Match the lighting direction, shadows, motion blur, and color grading of the video.

Seamlessly blend edges between the replaced area and the rest of each frame. Keep the background, clothing, other subjects, and all remaining visual content identical to the source video.
```

On a Cherry model, which is the default, the app puts that whole prompt inside this wrapper, in the slot. Send it the same way:

```
Use the provided reference video as the source of truth. Recreate its visual content as closely and faithfully as possible from beginning to end.

Preserve the shot sequence, timing, camera angle, camera movement, framing, composition, subject identity, poses, actions, body movement, facial expressions, environment, background, lighting, color grading, and visual style of the reference video.

Apply only the following requested change:
<the change>

Make the minimum changes necessary to fulfill the request. Everything not explicitly mentioned in the requested change must remain consistent with the reference video. Do not restage the scene, reinterpret the action, alter the camera or motion, add or remove unrelated subjects or objects, or introduce unrelated visual changes unless the request explicitly requires it.
```

- **Image reference:** send the wrapped prompt, with the image in `image`.
- **Saved character:** don't send `image`. Add one line after the whole wrapped prompt, separated by a blank line, so Mage attaches the character: `Reference: @handle`. The prompt still says "the reference image"; the character's image is that reference, as in the app.
- **Models outside the Cherry line** get the swap prompt alone, without the wrapper.

## Settings

- Model: Cherry 2 Pro (`cherry`, `model_id: "cherry-2-pro"`), Mage's default for video. When the user asks for another model, use it.
- `resolution`: `480p`, the cheapest. Offer `720p` or `1080p` with the price when the user wants a final.
- Leave `duration` and `aspect_ratio` out: on Cherry 2 Pro the output follows the clip's length and shape.
- `use_character_voices: false`.
- The clip must be 4 to 30 seconds long. For a shorter clip, say so and offer Lemon, which takes 1 to 15 seconds.

Other models the app offers (Lemon, the other Cherry models, Plum, Plum Max, Berry), with their clip limits, fields, and settings: `references/models.md`. Read it before using any model but Cherry 2 Pro.

## Run

```json
{
  "model_id": "cherry-2-pro",
  "resolution": "480p",
  "videos": [
    "<the clip>"
  ],
  "image": "<the reference image>",
  "use_character_voices": false,
  "prompt": "<the wrapped prompt>"
}
```

1. `get_model` for the architecture, once per conversation, to confirm its fields, options, and rules.
2. `estimate_cost` with the exact config. Tell the user the model, resolution, length, and price in Gems, and **wait for a yes**. Video is expensive and the price climbs with resolution and length.
3. `generate` with a new UUID as `idempotency_key`, then `get_request` with `wait_seconds: 120`, repeated quietly until the status is `completed`, `failed`, or `cancelled`. Video takes minutes.

`duration` and `resolution` are strings, written exactly as `get_model` lists them (`"4"`, `"480p"`, and on Plum `"768P"`).

## Check and deliver

Deliver the link with the model, resolution, length, and Gems. Tell the user to watch the whole clip: a swap that looks right in one frame can break during fast motion, profile turns, or when something passes in front of the face. Shorter clips with a steady subject hold up best. If the head shape or the outfit also needs to change, use `mage-video-character-swap`.

## Errors

| Code | What to do |
|---|---|
| `insufficient_gems` | Give the price and the balance; Gems are added at https://www.mage.space/api?tab=billing. |
| `invalid_config` | The message names the field, value, or `@handle`. Fix it from `get_model` and retry with a new key. |
| `content_blocked` | Mage's policy or the model's filter refused it. Never try to slip past a filter. |
| `too_many_requests` | 20 generations are already running. Wait, then submit again. |
| `generation_failed` | Usually transient and refunded. Retry once with a new key. |
| `requires_media_measurement` | The clip is on a host `estimate_cost` can't measure. Upload it with `create_upload` and price again. |

## References

- `references/models.md`: every model the app offers for this, with clip limits, fields, settings, the Cherry wrapper prompt, and audio.
