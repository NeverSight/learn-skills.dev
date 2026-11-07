---
name: mage-character-muse
description: |
  Discover and refine a character from a starter image with Mage: keep what
  works, change the face or details step by step with presets or plain words,
  pick the best take, and save it as a reusable @handle. The Character
  Builder: Muse app as a skill, on Mango 3 by default. Use when: "muse",
  "explore looks from this image", "refine this character", "same person but
  make the face softer", "try different faces on this character", "iterate on
  this portrait until it's right", "make her look more mature", "I like this
  look but can't describe it". NOT for: building a character from a trait list
  (mage-character-builder), saving a finished photo as it is
  (mage-characters), a turnaround sheet (mage-character-sheet), or copying a
  real person.
license: MIT
compatibility: Requires the Mage connector (https://mcp.mage.space/mcp) and a Mage account with Gems.
metadata:
  author: mage-space
  version: "0.0.0" # x-release-please-version
---

# Mage Character Muse

Start from an image that is close, then steer it: change the face with a preset or describe the change, compare the takes, and save the one that is right. This is the [Character Builder: Muse app](https://www.mage.space/apps/character-builder-muse) as a skill: the same two stages, face presets and models, run through the Mage connector.

## Before you start

1. **Mage tools:** `get_model`, `estimate_cost`, `generate`, `get_request`, `search_creations`, `list_characters`, `create_character`, and `create_upload` for local files. If they are missing, ask the user to connect Mage (Claude: Customize → Connectors → Add custom connector, `https://mcp.mage.space/mcp`; Claude Code: `/mcp` to sign in if the Mage plugin is installed, otherwise `claude mcp add --transport http mage https://mcp.mage.space/mcp`; others: https://www.mage.space/mcp), then wait.
2. **Inputs are links:** https URLs of the files themselves, data URLs under about 3 MB, uploads from disk (`create_upload`, when you can run commands), or earlier Mage results. Files attached to the chat never reach Mage: ask for a direct link.
3. **Rights.** Only build characters from images the user has the right to use, and never to copy a real person.

## UX rules

1. Don't ask for what the request already gives. Ask for everything that is missing in one compact question, then wait.
2. Send the app's prompt below word for word. Fill in only the marked slots; don't rewrite, translate, or add to it.
3. Always state the model and the price in Gems. A single image can start with its price in the same message; a batch waits for a yes.
4. Keep a short numbered list of the takes so far (starter, take 1, take 2, …) so the user can say which to continue from.
5. Deliver the link with a one-line label (model, size or length, Gems spent). No prompts, ids, or JSON. Reply in the user's language. Links last 30 days.

## Stage 1: Explore (pick a starter)

The character starts from one image. Ask for it if the request has none:

- an image link or a file on disk,
- one of the user's saved creations (find it with `search_creations`), or
- an earlier Mage result in this conversation.

The app also offers a gallery of starter images; the connector doesn't expose it. With no image at all, make one first with `mage-character-builder` and come back.

## Stage 2: Refine

Each step sends the **selected image** and one prompt, and adds the result to the takes.

- **Selected image:** the starter at first. After that, whichever take the user chose to continue from; by default the newest result.
- **Prompt:** either
  - a **face preset** from `references/faces.md` (Cute, Chiseled, Elegant, Soft, Sharp, Doll, Rough, Freckled, Mature), sent as the prefix, a blank line, and the preset's text; or
  - the user's own description of the change: their sentence alone, without the link or the request around it. Nothing is added to it, not even the presets' prefix, so if the outfit or setting should hold, the user has to say so.

If the request gives neither, list the nine presets in one line and ask.

## Settings

- Model: Mango 3 (`mango`, `model_id: "mango-v3"`) at `resolution: "2K"` for quality. When the user wants speed or a lower price, Mango 3 Turbo (`model_id: "mango-v3-turbo"`). Other models the app offers: `references/models.md`.
- `aspect_ratio`: always `4:5`. The app crops the selected image to 4:5 around its center first; when you can run commands and the image is more than about 5% away from 4:5, crop it the same way (`magick in.jpg -gravity center -crop 4:5 +repage out.jpg`) and upload the crop. Otherwise send it as it is.

## Run

```json
{
  "model_id": "mango-v3",
  "resolution": "2K",
  "aspect_ratio": "4:5",
  "image": "<the selected image>",
  "prompt": "<preset or the user's description>"
}
```

1. `get_model` for the architecture, once per conversation, to confirm its fields and options.
2. `estimate_cost` with the exact config. Say the model and the price in Gems. One image can start in the same message; more than one waits for a yes.
3. `generate` with a new UUID as `idempotency_key`, then `get_request` with `wait_seconds: 120` until the status is `completed`, `failed`, or `cancelled`.

To try several presets at once, run one generation per preset from the same selected image, quote the total, and wait for a yes.

## Check and deliver

Deliver each take with a number and a label (`take 3 · freckled`). If you can see it, say in a few words what changed and whether the outfit and setting held. Then ask: continue from this take, go back to another, or save.

## Save

When the user picks a take:

1. Ask for a name. The handle is derived from it unless the user picks one (1–15 lowercase letters, digits, `_` or `-`, starting with a letter; it can't change later).
2. `create_character` with `name`, `image` (the take's URL), and the optional `handle`.
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

- `references/faces.md`: the face prefix and the nine presets, word for word.
- `references/models.md`: every model the app offers for this, with ids and resolutions.
