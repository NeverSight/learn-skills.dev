---
name: mage-scene-builder
description: |
  Build a video scene with two characters using Mage: two character images or
  saved @handles, plus a ready-made multi-shot scene (boxing match, wedding,
  dinner date, dance battle, kissing, mafia meeting, late night drive, beach
  episode, morning together) or the user's own prompt, with both identities
  kept in every shot. The Scene Builder app as a skill, on Cherry 2 Pro by
  default. Use when: "scene builder", "a scene with these two characters",
  "make these two have dinner", "put @a and @b in a boxing match",
  "two-character video", "dialogue scene between my characters", "a wedding
  video of these two". NOT for: one character alone (mage-generate), a
  scripted drama or series (mage-short-drama), a music performance
  (mage-music-video), a talking head (mage-lipsync), product videos
  (mage-ugc-video), or real people without their consent.
license: MIT
compatibility: Requires the Mage connector (https://mcp.mage.space/mcp) and a Mage account with Gems.
metadata:
  author: mage-space
  version: "0.0.0" # x-release-please-version
---

# Mage Scene Builder

Give it two characters and a scene, and get a short video of them together, each one recognizable. This is the [Scene Builder app](https://www.mage.space/apps/scene-builder) as a skill: the same presets, prompt template and models, run through the Mage connector.

## Before you start

1. **Mage tools:** `get_model`, `estimate_cost`, `generate`, `get_request`, `list_characters`, and `create_upload` for local files. If they are missing, ask the user to connect Mage (Claude: Customize → Connectors → Add custom connector, `https://mcp.mage.space/mcp`; Claude Code: `/mcp` to sign in if the Mage plugin is installed, otherwise `claude mcp add --transport http mage https://mcp.mage.space/mcp`; others: https://www.mage.space/mcp), then wait.
2. **Inputs are links:** https URLs of the files themselves, data URLs under about 3 MB, uploads from disk (`create_upload`, when you can run commands), or earlier Mage results. Files attached to the chat never reach Mage: ask for a direct link.
3. **Consent.** Harmful deepfakes are forbidden on Mage. Only use a real person's face, body, or voice with that person's permission, and never to deceive, harass, or sexualize. When the user hasn't said whose likeness it is, state this rule in one line with the price instead of questioning them; if they say they lack permission, stop. Both characters must be adults.

## UX rules

1. Don't ask for what the request already gives. Ask for everything that is missing in one compact question, then wait.
2. Send the app's prompt below word for word. Fill in only the marked slots; don't rewrite, translate, or add to it.
3. Always quote the model and the price in Gems and wait for a yes before generating.
4. A preset is sent word for word with only the two character slots filled. A custom prompt is sent as the user wrote it.
5. Deliver the link with a one-line label (model, size or length, Gems spent). No prompts, ids, or JSON. Reply in the user's language. Links last 30 days.

## Inputs

1. **Character one** and **character two** (both required): each an image link, or a saved character by `@handle`. Their order is the order the scene uses them.
2. **The scene:** one of the presets, or the user's own prompt. If the request gives neither, list the presets in one line and ask.

Presets: Boxing Match, Wedding, Dinner Date, Dance Battle, Kissing, Mafia Meeting, Late Night Drive, Beach Episode, Morning Together.

## Prompt

**A preset:** read `references/presets.md`, take the preset's text, and fill its two slots as the table there says: a saved character becomes `@handle`, an image becomes `the character from Image 1` or `the character from Image 2`.

**A custom prompt:** send the user's description of the scene, without the links or the request around it. It has to say who is who, so if it doesn't name the characters, put this line first, then a blank line, then their text, and show the user the line you added: `Use <character one> and <character two> as the two characters.`, with each slot filled as for a preset (`@handle`, or `the character from Image 1` / `Image 2`).

## Settings

- Model: Cherry 2 Pro (`cherry`, `model_id: "cherry-2-pro"`), Mage's default for video. When the user asks for another model, use it.
- `resolution`: `480p`. `duration`: `"4"`. `aspect_ratio`: `16:9`.
- Character images, in order, go in `image` and `additional_images`. Saved characters are mentions only and take no image field.

Four seconds is short for a four-shot preset, so the model compresses it. Offer `8`, `10`, or `15` seconds with the price when the user wants the whole scene to play out. Other models the app offers (Cherry Pro, Cherry, Raspberry, Lemon): `references/models.md`.

## Run

Two images:

```json
{
  "model_id": "cherry-2-pro",
  "resolution": "480p",
  "duration": "4",
  "aspect_ratio": "16:9",
  "image": "<character one's image>",
  "additional_images": [
    "<character two's image>"
  ],
  "prompt": "<the filled preset or the custom prompt>"
}
```

With one saved character and one image, send only the image, in `image`. With two saved characters, send no image fields.

1. `get_model` for the architecture, once per conversation, to confirm its fields, options, and rules.
2. `estimate_cost` with the exact config. Tell the user the model, resolution, length, and price in Gems, and **wait for a yes**. Video is expensive and the price climbs with resolution and length.
3. `generate` with a new UUID as `idempotency_key`, then `get_request` with `wait_seconds: 120`, repeated quietly until the status is `completed`, `failed`, or `cancelled`. Video takes minutes.

`duration` and `resolution` are strings, written exactly as `get_model` lists them (`"4"`, `"480p"`, and on Plum `"768P"`).

## Check and deliver

Deliver the link with the model, resolution, length, and Gems. Two is the limit. Physical interaction between two generated people is the hardest case in video, so expect more retries than a single-subject clip: if faces merge or limbs distort, offer one retry.

## Errors

| Code | What to do |
|---|---|
| `insufficient_gems` | Give the price and the balance; Gems are added at https://www.mage.space/api?tab=billing. |
| `invalid_config` | The message names the field, value, or `@handle`. Fix it from `get_model` and retry with a new key. |
| `content_blocked` | Mage's policy or the model's filter refused it. Never try to slip past a filter. |
| `too_many_requests` | 20 generations are already running. Wait, then submit again. |
| `generation_failed` | Usually transient and refunded. Retry once with a new key. |

## References

- `references/presets.md`: the nine scene presets, word for word, and how to fill their character slots.
- `references/models.md`: every model the app offers for scenes, with ids, resolutions, durations, and ratios.
