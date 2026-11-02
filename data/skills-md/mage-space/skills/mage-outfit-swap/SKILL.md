---
name: mage-outfit-swap
description: |
  Put the clothing, footwear, and accessories from one image onto the person
  in another with Mage, keeping the person, pose, and scene. The Outfit Swap
  app as a skill, on Mango 3 by default. Use when: "outfit swap", "change her
  outfit to this one", "put this jacket on him", "dress the model in this
  look", "try this outfit on", "same photo, different clothes", "virtual
  try-on of this garment on this person". NOT for: swapping a face
  (mage-face-swap) or the whole person (mage-character-swap), catalog shots of
  a garment with no person to dress (mage-product-photoshoot), or an outfit
  reused across many new images (save it as a reference with mage-characters).
license: MIT
compatibility: Requires the Mage connector (https://mcp.mage.space/mcp) and a Mage account with Gems.
metadata:
  author: mage-space
  version: "0.0.0" # x-release-please-version
---

# Mage Outfit Swap

Dress the person in one image in the outfit from another, keeping their identity, pose, and background. This is the [Outfit Swap app](https://www.mage.space/apps/outfit-swap) as a skill: the same prompt and models, run through the Mage connector.

## Before you start

1. **Mage tools:** `get_model`, `estimate_cost`, `generate`, `get_request`, `list_references`, and `create_upload` for local files. If they are missing, ask the user to connect Mage (Claude: Customize → Connectors → Add custom connector, `https://mcp.mage.space/mcp`; Claude Code: `/mcp` to sign in if the Mage plugin is installed, otherwise `claude mcp add --transport http mage https://mcp.mage.space/mcp`; others: https://www.mage.space/mcp), then wait.
2. **Inputs are links:** https URLs of the files themselves, data URLs under about 3 MB, uploads from disk (`create_upload`, when you can run commands), or earlier Mage results. Files attached to the chat never reach Mage: ask for a direct link.

## UX rules

1. Don't ask for what the request already gives. Ask for everything that is missing in one compact question, then wait.
2. Send the app's prompt below word for word. Fill in only the marked slots; don't rewrite, translate, or add to it.
3. Always state the model and the price in Gems. A single image can start with its price in the same message; a batch waits for a yes.
4. Deliver the link with a one-line label (model, size or length, Gems spent). No prompts, ids, or JSON. Reply in the user's language. Links last 30 days.

## Inputs

Both are required. Ask for whichever is missing.

1. **The subject image:** the person to dress. Identity, pose, and scene stay.
2. **The outfit image:** the clothing to apply, worn or as a flat lay. A saved outfit works too: use its `image_url` from `list_references` with `kind: "outfit"`.

## Settings

- Model: Mango 3 (`mango`, `model_id: "mango-v3"`) at `resolution: "2K"` for quality. When the user wants speed or a lower price, Mango 3 Turbo (`model_id: "mango-v3-turbo"`). Other models the app offers: `references/models.md`.
- `aspect_ratio`: the model's option closest to the source image's width ÷ height, as the app does. Measure the file when you can run commands; otherwise judge it from the image, or ask. Use the first image's shape.

## Prompt

Send exactly this:

```
Transfer the clothing, footwear, and accessories from the second image onto the person in the first image.

Preserve the subject's identity, face, hair, body shape, pose, expression, framing, and background from the first image.

Keep the lighting, shadows, color grading, and scene continuity from the first image so the restyled outfit blends naturally.

Do not replace the person or alter unrelated scene elements. Only change the worn outfit and styling items to match the second image.
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

If you can see the result: check where the garment meets skin, and that the face, hair, pose, and framing are unchanged. When the outfit image shows pieces the source framing can't (shoes or trousers for a waist-up photo), the model may re-pose or pull back to show them. If the framing changed, say so and offer a retry, an outfit image cropped to the pieces that fit the frame, or Mango 3 Turbo, which held the framing in testing. Retry once on a hard failure. If you can't see images, say the result needs the user's review. Deliver the link.

Complex garments, sheer fabric, and unusual layering are harder than a simple silhouette. For the same outfit across a whole series, save it as an outfit reference with `mage-characters` and mention its `@handle` instead of swapping each image.

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
