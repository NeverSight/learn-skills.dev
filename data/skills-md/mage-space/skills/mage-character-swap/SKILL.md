---
name: mage-character-swap
description: |
  Replace the whole person in an image with a different character using Mage,
  keeping the scene, pose, action, and expression. The Character Swap app as a
  skill, on Mango 3 by default. Use when: "character swap", "replace the
  person in this image with this character", "put my character into this
  scene", "swap the subject", "same shot but with this person instead", "the
  face swap left a seam". NOT for: changing only the face (mage-face-swap),
  only the clothes (mage-outfit-swap), a person in a video
  (mage-video-character-swap), a new pose or a new scene (mage-generate with
  the character), or using a real person's likeness without their consent.
license: MIT
compatibility: Requires the Mage connector (https://mcp.mage.space/mcp) and a Mage account with Gems.
metadata:
  author: mage-space
  version: "0.0.0" # x-release-please-version
---

# Mage Character Swap

Replace the subject of an image with a different character, keeping the pose, action, expression, and scene. This is the [Character Swap app](https://www.mage.space/apps/character-swap) as a skill: the same prompt and models, run through the Mage connector.

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

1. **The scene image:** the photo whose composition and pose stay.
2. **The replacement character:** an image of the character to put in. A saved character works too: use its image URL from `list_characters`.

## Settings

- Model: Mango 3 (`mango`, `model_id: "mango-v3"`) at `resolution: "2K"` for quality. When the user wants speed or a lower price, Mango 3 Turbo (`model_id: "mango-v3-turbo"`). Other models the app offers: `references/models.md`.
- `aspect_ratio`: the model's option closest to the source image's width ÷ height, as the app does. Measure the file when you can run commands; otherwise judge it from the image, or ask. Use the first image's shape.

## Prompt

Send exactly this:

```
Replace the subject in the first image with the character from the second image. Keep the pose, action, and expression consistent with the first image.
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

If you can see the result: the new character should hold the original pose and the light on them should match the room. Retry once on a hard failure. If you can't see images, say the result needs the user's review. Deliver the link.

It keeps the composition, so it also keeps the pose: for a different pose, generate a new image with `mage-generate`. If the light on the new subject doesn't match, use `mage-relight`.

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
