---
name: mage-ad-resizer
description: |
  Adapt a static ad to every placement with Mage: square feed, portrait feed,
  Stories and Reels, landscape video and display, wide banners, and
  Pinterest. Recomposes the layout for each aspect ratio instead of cropping,
  extends the background, keeps every word, the product, and the logo, and
  respects each platform's safe zones. GPT Image 2.5 Flare for ads with
  text, Mango 3 for image-only ads. Use when: "resize this ad", "make this
  ad 9:16", "adapt for Stories", "all ad sizes", "placements", "1:1 4:5
  9:16", "make a banner version", "reformat for TikTok / Meta / Pinterest /
  YouTube / Google Display". NOT for: new creative variations (use
  mage-ad-multiplier), translations (mage-ad-localizer), video ads, or
  cropping a photo without an ad layout (mage-generate).
license: MIT
compatibility: Requires the Mage connector (https://mcp.mage.space/mcp) and a Mage account with Gems.
metadata:
  author: mage-space
  version: "0.0.0" # x-release-please-version
---

# Mage Ad Resizer

Re-lay out one static ad for every placement. Each size is recomposed from the original, not cropped: text reflows, the background extends, and the product and logo stay intact and in focus.

## Before you start

1. **Mage tools:** `get_model`, `estimate_cost`, `generate`, `get_request`, and `create_upload` for local files. If they are missing, ask the user to connect Mage (Claude: Customize → Connectors → Add custom connector, `https://mcp.mage.space/mcp`; Claude Code: `/mcp` to sign in if the Mage plugin is installed, otherwise `claude mcp add --transport http mage https://mcp.mage.space/mcp`; others: https://www.mage.space/mcp), then wait.
2. **The ad is a link:** an https URL of the image file, a data URL under about 3 MB, or an upload from disk with `create_upload`. Files attached to the chat never reach Mage.

## UX rules

1. Default to the three core placements (`1:1`, `4:5`, `9:16`) when the user doesn't list sizes; ask only if the platform is unclear.
2. Transcribe every word of the ad's text before generating and reuse it verbatim; show the transcription with the price so the user can correct it.
3. Quote the total Gems and wait for a yes.
4. Deliver links labeled by placement. Links expire after 30 days.
5. Never add, remove, or reword text, and never change the product, logo, or offer.

## Placements

| Placement | Aspect | Layout |
|---|---|---|
| Feed square (Meta, LinkedIn, X) | `1:1` | Headline top, product center, CTA bottom |
| Feed portrait (Instagram, Facebook) | `4:5` | Same as square with more vertical breathing room |
| Stories, Reels, TikTok, Shorts | `9:16` | Keep the top ~14% and bottom ~20% free of text and logo (app UI covers them); stack headline, product, CTA in the middle band |
| Pinterest | `2:3` | Tall, product-led, headline in the top half |
| YouTube thumbnail, display landscape, X/LinkedIn link | `16:9` | Product on one side, text on the other |
| Wide web banner, email header | `21:9` | Product on the right third, text on the left, lots of background |

Other Mage ratios (`3:2`, `5:4`, `2:3`, `9:21`) are available for custom slots. Exact pixel sizes (for example 1080×1920) come from resizing the 2K output afterwards; the aspect ratio is what matters here.

## Workflow

1. **Read the ad.** List its text (every line, verbatim), the product, the logo, the CTA, the background, and the visual hierarchy.
2. **Choose the model.** GPT Image 2.5 Flare (`gpt_image_2`, `gpt-image-2.5-flare`) when the ad has text; it renders words most reliably. Mango 3 (`mango`, `mango-v3`) for image-only ads. `resolution: "2K"`.
3. **Prompt each size**, with the original in `image`:

   ```
   Recompose the ad in @image1 as a <aspect> <placement> ad. Reuse exactly the
   same text, word for word: "<line 1>", "<line 2>", "<CTA>". Keep the product,
   its label, and the logo identical and prominent. <Layout for this placement
   from the table.> Extend the background naturally in the same style; do not
   stretch, crop, or distort the product. Same fonts, colors, and visual
   hierarchy as the original.
   ```

4. **Price, generate, wait:** `get_model`, `estimate_cost` per size, quote the total, `generate` each (new UUID `idempotency_key`), `get_request` with `wait_seconds: 120`.
5. **Check** each result if you can see it: every word spelled as in the original, nothing cut off, the product undistorted, text clear of the safe zones on `9:16`. Regenerate once if not.

## Deliver

```text
Resized for 3 placements:
- 1:1 feed: https://…
- 4:5 feed: https://…
- 9:16 Stories and Reels: https://…
```

Offer once to localize the set (`mage-ad-localizer`) or make variations of the winner (`mage-ad-multiplier`).

## Errors

- **Text changed or misspelled:** regenerate with Flare and the transcription quoted line by line; shorten nothing.
- **Product squashed or cut off:** add "the whole product visible, same proportions" and give it a larger share of the frame.
- **`invalid_config`:** the aspect ratio isn't offered by the model; check `get_model`.
