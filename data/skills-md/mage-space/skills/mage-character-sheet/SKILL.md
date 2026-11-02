---
name: mage-character-sheet
description: |
  Turn one image of a character into a full character reference sheet with
  Mage: a face close-up, front, three-quarter, side, and back full-body views,
  and hair, outfit, and accessory details on one wide canvas, ready to save as
  a character. The Character Sheet app as a skill, on Mango 3 by default.
  Use when: "character sheet", "reference sheet", "model sheet", "turnaround
  of this character", "front side and back views", "make a sheet so my
  character stays consistent", "character design sheet from this image".
  NOT for: one new camera angle of a scene (mage-angles), designing the
  character in the first place (mage-character-builder, mage-character-muse),
  saving a plain portrait (mage-characters), or sheets of real people without
  consent.
license: MIT
compatibility: Requires the Mage connector (https://mcp.mage.space/mcp) and a Mage account with Gems.
metadata:
  author: mage-space
  version: "0.0.0" # x-release-please-version
---

# Mage Character Sheet

Make a character reference sheet from a single image, then save it as a character so every later generation has the face, the body from four sides, and the outfit to draw on. This is the [Character Sheet app](https://www.mage.space/apps/character-sheet) as a skill: the same prompt, layout, model, and defaults, run through the Mage connector.

## Before you start

1. **Mage tools:** `get_model`, `estimate_cost`, `generate`, `get_request`, `list_characters`, `create_character`, and `create_upload` for local files. If they are missing, ask the user to connect Mage (Claude: Customize → Connectors → Add custom connector, `https://mcp.mage.space/mcp`; Claude Code: `/mcp` to sign in if the Mage plugin is installed, otherwise `claude mcp add --transport http mage https://mcp.mage.space/mcp`; others: https://www.mage.space/mcp), then wait.
2. **Inputs are links:** https URLs of the files themselves, data URLs under about 3 MB, uploads from disk (`create_upload`, when you can run commands), or earlier Mage results. Files attached to the chat never reach Mage: ask for a direct link.
3. **Rights.** Only make a sheet of a real person with that person's consent.

## UX rules

1. Don't ask for what the request already gives. Ask for everything that is missing in one compact question, then wait.
2. Send the app's prompt below word for word. Fill in only the marked slots; don't rewrite, translate, or add to it.
3. Always state the model and the price in Gems. A single image can start with its price in the same message; a batch waits for a yes.
4. Deliver the link with a one-line label (model, size or length, Gems spent). No prompts, ids, or JSON. Reply in the user's language. Links last 30 days.

## Inputs

1. **One image of the character.** A saved character works too: use its image URL from `list_characters`.
2. **Details (optional):** changes or additions to apply in every panel ("add a red scarf", "her eyes are green"). Don't ask for them; use them when given.

## Prompt

Send exactly this:

```
Create a character reference sheet of the character in this image on one wide canvas with a plain light gray background.
Center: a square column as tall as the canvas. Its top two-thirds is a large close-up portrait of the character's face and shoulders, facing the camera with a neutral expression, centered in the column. Its bottom third is a row of three close-up detail panels of the character's hair, outfit, and most distinctive accessory or feature.
Left side: two full-body views of the character, head to toe, side by side: front view and three-quarter view.
Right side: two full-body views of the character, head to toe, side by side: side profile view and back view.
Every full-body view shows the character standing in a relaxed neutral pose, all at the same scale.
Keep the same character in every panel: same face, age, skin tone, body type, hairstyle, hair color, eye color, outfit, colors, and accessories as in the image.
Match the art style of the image. If the image is a photo, make every panel a photo.
Use even, soft lighting in every panel. Leave clean gray space between panels. The sheet is purely visual: only the character panels on the plain background.
```

With details, add one more line directly after it, joined by a single newline. `<details>` is what the user asked for as a phrase with no final period ("add a red pocket square" becomes `a red pocket square`):

```
Add these details to the character in every panel. Where they differ from the image, follow these details: <details>
```

## Settings

- Model: Mango 3 (`mango`, `model_id: "mango-v3"`) at `resolution: "2K"` for quality. When the user wants speed or a lower price, Mango 3 Turbo (`model_id: "mango-v3-turbo"`). Other models the app offers: `references/models.md`.
- `aspect_ratio`: always `16:9`. The layout puts the face in a centered square column, so a square crop of the sheet is a face avatar; that only works at 16:9.

## Run

```json
{
  "model_id": "mango-v3",
  "resolution": "2K",
  "aspect_ratio": "16:9",
  "image": "<the character image>",
  "prompt": "<the prompt above>"
}
```

1. `get_model` for the architecture, once per conversation, to confirm its fields and options.
2. `estimate_cost` with the exact config. Say the model and the price in Gems. One image can start in the same message; more than one waits for a yes.
3. `generate` with a new UUID as `idempotency_key`, then `get_request` with `wait_seconds: 120` until the status is `completed`, `failed`, or `cancelled`.

## Check and deliver

If you can see the sheet: the face portrait is in the center with three detail panels under it, two full-body views are on each side (front and three-quarter, then side and back), it is the same character in every panel, and there is no text. Retry once on a hard failure. If you can't see images, say the result needs the user's review. Deliver the link.

## Save as a character

Offer it after delivering: the sheet is what keeps the character consistent across generations.

1. Ask for a name. The handle is derived from it unless the user picks one (1–15 lowercase letters, digits, `_` or `-`, starting with a letter; it can't change later).
2. `create_character` with `name`, `image` (the sheet's URL), and the optional `handle`.
3. Reply "Saved @handle. Mention @handle in any prompt to use them."

## Errors

| Code | What to do |
|---|---|
| `insufficient_gems` | Give the price and the balance; Gems are added at https://www.mage.space/api?tab=billing. |
| `invalid_config` | The message names the field, value, or `@handle`. Fix it from `get_model` and retry with a new key. |
| `content_blocked` | Mage's policy or the model's filter refused it. Never try to slip past a filter. |
| `too_many_requests` | 20 generations are already running. Wait, then submit again. |
| `generation_failed` | Usually transient and refunded. Retry once with a new key. |
| `handle_taken` | Suggest another handle, or leave it out to derive one. |

## References

- `references/models.md`: every model the app offers for this, with ids and resolutions.
