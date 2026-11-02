---
name: mage-face-swap
description: |
  Swap a face from one image onto the person in another with Mage: the whole
  head (face, hair, skin, neck) is replaced while the pose, expression,
  clothing, and background stay. The Face Swap app as a skill, on Mango 3 by
  default. Use when: "face swap", "swap faces", "put this face on that photo",
  "put my face on this picture", "replace the face in this image", "fix the
  face in this one image so it matches the others". NOT for: swapping a face
  in a video (mage-video-face-swap), replacing the whole person including body
  and outfit (mage-character-swap), changing only clothes (mage-outfit-swap),
  or putting a real person into anything without their consent.
license: MIT
compatibility: Requires the Mage connector (https://mcp.mage.space/mcp) and a Mage account with Gems.
metadata:
  author: mage-space
  version: "0.0.0" # x-release-please-version
---

# Mage Face Swap

Put the face and hair from one image onto the person in another, keeping the pose, expression, clothing, and background. This is the [Face Swap app](https://www.mage.space/apps/face-swap) as a skill: the same prompt and models, run through the Mage connector.

## Before you start

1. **Mage tools:** `get_model`, `estimate_cost`, `generate`, `get_request`, `list_characters`, and `create_upload` for local files. If they are missing, ask the user to connect Mage (Claude: Customize → Connectors → Add custom connector, `https://mcp.mage.space/mcp`; Claude Code: `/mcp` to sign in if the Mage plugin is installed, otherwise `claude mcp add --transport http mage https://mcp.mage.space/mcp`; others: https://www.mage.space/mcp), then wait.
2. **Inputs are links:** https URLs of the files themselves, data URLs under about 3 MB, uploads from disk (`create_upload`, when you can run commands), or earlier Mage results. Files attached to the chat never reach Mage: ask for a direct link.
3. **Consent.** Harmful deepfakes are forbidden on Mage. Only use a real person's face, body, or voice with that person's permission, and never to deceive, harass, or sexualize. When the user hasn't said whose likeness it is, state this rule in one line with the price instead of questioning them; if they say they lack permission, stop.

## UX rules

1. Don't ask for what the request already gives. Ask for everything that is missing in one compact question, then wait.
2. Send the app's prompt below word for word. Fill in only the marked slots; don't rewrite, translate, or add to it.
3. Always state the model and the price in Gems. A single image can start with its price in the same message; a batch waits for a yes.
4. Deliver the link with a one-line label (model, size or length, Gems spent). No prompts, ids, or JSON. Reply in the user's language. Links last 30 days.

## Inputs

Both are required. Ask for whichever is missing.

1. **The image to change:** the photo whose scene and body stay.
2. **The face to use:** a clear, front-facing image of the new face. A saved character works too: use its image URL from `list_characters`.

## Settings

- Model: Mango 3 (`mango`, `model_id: "mango-v3"`) at `resolution: "2K"` for quality. When the user wants speed or a lower price, Mango 3 Turbo (`model_id: "mango-v3-turbo"`). Other models the app offers: `references/models.md`.
- `aspect_ratio`: the model's option closest to the source image's width ÷ height, as the app does. Measure the file when you can run commands; otherwise judge it from the image, or ask. Use the first image's shape.

## Prompt

Send exactly this:

```
Replace the face and hair of the person in the first image with the identity from the second image.

Modify the entire head region (face, skin, ears, hair, hairstyle, hair color, and visible neck) to match the subject in the second image, while preserving the original pose, expression, camera angle, and composition of the first image.

Replace the hairstyle completely — use the hair length, texture, color, and styling from the second image. Do not retain any hair features from the first image.

Ensure skin tone, texture, and color are fully harmonized across the entire head and neck so it blends naturally with the body. Match lighting direction, shadows, and color grading to the first image.

Seamlessly blend edges between the replaced area and the original image. Do not alter the background, clothing, or framing.
```

## Run

```json
{
  "model_id": "mango-v3",
  "resolution": "2K",
  "aspect_ratio": "<closest to the first image>",
  "image": "<first image>",
  "additional_images": [
    "<second image>"
  ],
  "prompt": "<the prompt above>"
}
```

The order matters: the prompt calls `image` "the first image" and `additional_images[0]` "the second image".

1. `get_model` for the architecture, once per conversation, to confirm its fields and options.
2. `estimate_cost` with the exact config. Say the model and the price in Gems. One image can start in the same message; more than one waits for a yes.
3. `generate` with a new UUID as `idempotency_key`, then `get_request` with `wait_seconds: 120` until the status is `completed`, `failed`, or `cancelled`.

## Check and deliver

If you can see the result: check the hairline and jaw, where a swap shows first, and that skin tone matches the neck and body. Retry once on a hard failure. If you can't see images, say the result needs the user's review. Deliver the link.

Face Swap changes the head only, so the head shape stays. For very different face shapes, strong angles, or a visible seam, use `mage-character-swap`. If the light on the new face doesn't match the room, use `mage-relight`.

## Errors

| Code | What to do |
|---|---|
| `insufficient_gems` | Give the price and the balance; Gems are added at https://www.mage.space/api?tab=billing. |
| `invalid_config` | The message names the field, value, or `@handle`. Fix it from `get_model` and retry with a new key. |
| `content_blocked` | Mage's policy or the model's filter refused it. Never try to slip past a filter. |
| `too_many_requests` | 20 generations are already running. Wait, then submit again. |
| `generation_failed` | Usually transient and refunded. Retry once with a new key. |

## References

- `references/models.md`: every model the app offers for this, with ids and resolutions.
