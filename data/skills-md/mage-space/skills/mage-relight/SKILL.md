---
name: mage-relight
description: |
  Relight a photo with Mage: a new light source from a chosen direction, soft
  or hard, at a chosen brightness and color, with the content and composition
  unchanged. The Relight app as a skill, on Mango 3 by default. Use when:
  "relight this photo", "change the lighting", "light it from the left", "add
  a rim light from behind", "warm golden light", "make the light softer",
  "dramatic side lighting", "match the lighting after a swap", "this looks
  flat, give it direction". NOT for: changing what is in the image
  (mage-inpaint or mage-refine), a new camera angle (mage-angles), relighting
  a video (mage-video-editor), or product scenes from scratch
  (mage-product-photoshoot).
license: MIT
compatibility: Requires the Mage connector (https://mcp.mage.space/mcp) and a Mage account with Gems.
metadata:
  author: mage-space
  version: "0.0.0" # x-release-please-version
---

# Mage Relight

Change the direction, hardness, brightness, and color of the light in an image, and nothing else. This is the [Relight app](https://www.mage.space/apps/relight) as a skill: the same controls, prompt and models, run through the Mage connector.

## Before you start

1. **Mage tools:** `get_model`, `estimate_cost`, `generate`, `get_request`, and `create_upload` for local files. If they are missing, ask the user to connect Mage (Claude: Customize → Connectors → Add custom connector, `https://mcp.mage.space/mcp`; Claude Code: `/mcp` to sign in if the Mage plugin is installed, otherwise `claude mcp add --transport http mage https://mcp.mage.space/mcp`; others: https://www.mage.space/mcp), then wait.
2. **Inputs are links:** https URLs of the files themselves, data URLs under about 3 MB, uploads from disk (`create_upload`, when you can run commands), or earlier Mage results. Files attached to the chat never reach Mage: ask for a direct link.

## UX rules

1. Don't ask for what the request already gives. Ask for everything that is missing in one compact question, then wait.
2. Send the app's prompt below word for word. Fill in only the marked slots; don't rewrite, translate, or add to it.
3. Always state the model and the price in Gems. A single image can start with its price in the same message; a batch waits for a yes.
4. Deliver the link with a one-line label (model, size or length, Gems spent). No prompts, ids, or JSON. Reply in the user's language. Links last 30 days.

## Inputs

1. **The image** to relight.
2. **The light.** Four controls, each with the app's default. Map what the user said onto them and ask only if the request gives no direction at all.

| Control | Values | Default |
|---|---|---|
| Direction | A height and a side, in 45° steps: see below | front, level |
| Light type | soft, or hard | soft |
| Brightness | 0 to 100 | 75 |
| Color | Any color | white |

## Build the prompt

```
Relight this image with a new <light type> light source coming from the <direction>. The light brightness is <brightness>% and the light color is <color>. Preserve all content, subjects, and composition of the original image. Only change the lighting.
```

Fill the four slots exactly as the app does:

- **`<light type>`:** `soft, diffused` or `hard, directional`.
- **`<direction>`:** height then side. Left and right are as seen in the image; front is the camera's side of the subject and back is behind them. Straight above is `top` and straight below is `bottom`, with no side. Otherwise prefix the side with `upper` (light 45° above), `lower` (45° below), or nothing (level):

  | Side | Text |
  |---|---|
  | In front of the subject | `front` |
  | Front, toward the right | `front right` |
  | The right | `right` |
  | Behind, toward the right | `back right` |
  | Behind | `back` |
  | Behind, toward the left | `back left` |
  | The left | `left` |
  | Front, toward the left | `front left` |

  So a high light from the front left is `upper front left`, and a rim light from behind is `back`.
- **`<brightness>`:** the number, 0 to 100 (the prompt adds the `%`).
- **`<color>`:** one of the app's named colors when it fits: `white`, `black`, `red`, `green`, `blue`, `yellow`, `orange`, `warm orange`, `warm golden yellow`, `cool sky blue`. For any other color write `the color #RRGGBB` with its hex code as given; the sentence then reads "the light color is the color #12A5B0", which is how the app writes it.

Example: "warm, hard light from the upper left" becomes "Relight this image with a new hard, directional light source coming from the upper left. The light brightness is 75% and the light color is warm orange. …"

## Settings

- Model: Mango 3 (`mango`, `model_id: "mango-v3"`) at `resolution: "2K"` for quality. When the user wants speed or a lower price, Mango 3 Turbo (`model_id: "mango-v3-turbo"`). Other models the app offers: `references/models.md`.
- `aspect_ratio`: the model's option closest to the source image's width ÷ height, as the app does. Measure the file when you can run commands; otherwise judge it from the image, or ask.

## Run

```json
{
  "model_id": "mango-v3",
  "resolution": "2K",
  "aspect_ratio": "<closest to the image>",
  "image": "<the image>",
  "prompt": "<the filled prompt>"
}
```

1. `get_model` for the architecture, once per conversation, to confirm its fields and options.
2. `estimate_cost` with the exact config. Say the model and the price in Gems. One image can start in the same message; more than one waits for a yes.
3. `generate` with a new UUID as `idempotency_key`, then `get_request` with `wait_seconds: 120` until the status is `completed`, `failed`, or `cancelled`.

For several looks from one image, change one control per generation, quote the total, and wait for a yes.

## Check and deliver

If you can see the result: the shadows on the subject agree with the shadows in the background, and the content is unchanged. Retry once on a hard failure. If you can't see images, say the result needs the user's review. Deliver the link with the light as its label (`hard · upper left · warm orange`).

Relight works with what is there and can't recover detail the exposure lost. A strong change of direction can look wrong when the old shadows still show in reflections or on the ground.

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
