---
name: mage-inpaint
description: |
  Change one region of an image with Mage and leave the rest identical: the
  region is marked with a red overlay, then replaced from a description. The
  Inpaint app as a skill, on Mango 3 by default. Use when: "inpaint", "change
  just this part", "remove the cup from the table", "erase that person in the
  background", "replace the sign", "fix only his left hand", "add a plant in
  the corner", "edit this area and keep everything else". NOT for: whole-image
  improvements (mage-refine), relighting (mage-relight), swapping a face or
  outfit (mage-face-swap, mage-outfit-swap), changing the composition
  (mage-generate), editing a video (mage-video-editor), or altering a real
  person's image without their consent.
license: MIT
compatibility: Requires the Mage connector (https://mcp.mage.space/mcp) and a Mage account with Gems.
metadata:
  author: mage-space
  version: "0.0.0" # x-release-please-version
---

# Mage Inpaint

Mark a region of an image, describe what should be there, and change only that. This is the [Inpaint app](https://www.mage.space/apps/inpaint) as a skill: the same red-overlay mask, prompt and models, run through the Mage connector.

## Before you start

1. **Mage tools:** `get_model`, `estimate_cost`, `generate`, `get_request`, and `create_upload` for local files. If they are missing, ask the user to connect Mage (Claude: Customize → Connectors → Add custom connector, `https://mcp.mage.space/mcp`; Claude Code: `/mcp` to sign in if the Mage plugin is installed, otherwise `claude mcp add --transport http mage https://mcp.mage.space/mcp`; others: https://www.mage.space/mcp), then wait.
2. **Inputs are links:** https URLs of the files themselves, data URLs under about 3 MB, uploads from disk (`create_upload`, when you can run commands), or earlier Mage results. Files attached to the chat never reach Mage: ask for a direct link.
3. **Consent.** Harmful deepfakes are forbidden on Mage. Only use a real person's face, body, or voice with that person's permission, and never to deceive, harass, or sexualize. When the user hasn't said whose likeness it is, state this rule in one line with the price instead of questioning them; if they say they lack permission, stop.
4. **The mask needs a shell.** The app paints the region onto the image before sending it, so this skill needs to run a short Python script and see the image. Without both, say so and offer `mage-refine` with an instruction that names the area in words, which is less precise.

## UX rules

1. Don't ask for what the request already gives. Ask for everything that is missing in one compact question, then wait.
2. Send the app's prompt below word for word. Fill in only the marked slots; don't rewrite, translate, or add to it.
3. Always state the model and the price in Gems. A single image can start with its price in the same message; a batch waits for a yes.
4. Say which region you masked in a few words ("the cup and its shadow, lower left") so the user can correct it before or after the run.
5. Deliver the link with a one-line label (model, size or length, Gems spent). No prompts, ids, or JSON. Reply in the user's language. Links last 30 days.

## Inputs

1. **The image.**
2. **The region:** what to change, in the user's words ("the cup", "the sign on the wall"), or a mask image of their own.
3. **What should be there instead.** Describe the result, not the action: "an empty wooden table" works better than "remove the cup". If the user wrote an action, write the result it implies in a short phrase with no final period ("remove the cup she is holding" becomes "her empty hand, relaxed, with the jacket behind it").

## Mask the region

1. Get the image on disk (download the link).
2. Paint the region red at 50% opacity with the script in `references/mask.md`, a little wider than the object.
3. Look at the masked image and confirm the red covers the right thing.
4. Upload it (`create_upload`, or a data URL under about 3 MB).

## Prompt

```
Edit this image. The area highlighted with a semi-transparent red overlay is the region to modify. Apply the following edit to that region: <what should be there>

Only change the red-highlighted area. Keep everything outside the highlighted area identical.
```

Only the slot changes. The sentences about the red overlay must stay as written: they are what tells the model the red is a mask and not part of the picture.

## Settings

- Model: Mango 3 (`mango`, `model_id: "mango-v3"`) at `resolution: "2K"` for quality. When the user wants speed or a lower price, Mango 3 Turbo (`model_id: "mango-v3-turbo"`). Other models the app offers: `references/models.md`.
- `aspect_ratio`: the model's option closest to the source image's width ÷ height, as the app does. Measure the file when you can run commands; otherwise judge it from the image, or ask.

## Run

```json
{
  "model_id": "mango-v3",
  "resolution": "2K",
  "aspect_ratio": "<closest to the image>",
  "image": "<the masked image>",
  "prompt": "<the filled prompt>"
}
```

Only the masked image is sent, as the app does. Don't add the unmasked original.

1. `get_model` for the architecture, once per conversation, to confirm its fields and options.
2. `estimate_cost` with the exact config. Say the model and the price in Gems. One image can start in the same message; more than one waits for a yes.
3. `generate` with a new UUID as `idempotency_key`, then `get_request` with `wait_seconds: 120` until the status is `completed`, `failed`, or `cancelled`.

## Check and deliver

If you can see the result: no red is left, the region holds what was asked for, the join doesn't show, and everything outside it matches the original. If the join shows or red remains, mask a little wider and run again, at most twice. If you can't see images, say the result needs the user's review. Deliver the link.

Inpaint edits; it doesn't restructure. A new composition or perspective needs a new generation with `mage-generate`.

## Errors

| Code | What to do |
|---|---|
| `insufficient_gems` | Give the price and the balance; Gems are added at https://www.mage.space/api?tab=billing. |
| `invalid_config` | The message names the field, value, or `@handle`. Fix it from `get_model` and retry with a new key. |
| `content_blocked` | Mage's policy or the model's filter refused it. Never try to slip past a filter. |
| `too_many_requests` | 20 generations are already running. Wait, then submit again. |
| `generation_failed` | Usually transient and refunded. Retry once with a new key. |

## References

- `references/mask.md`: the masking script, how to place the region, and how to upload the result.
- `references/models.md`: every model the app offers for this, with ids and resolutions.
