---
name: mage-ad-multiplier
description: |
  Turn one ad into many independent variations with Mage: new talent,
  wardrobe, setting, background, color story, or headline, while the product,
  brand, layout, and every untouched element stay exactly as they were.
  Works on static image ads (Mango 3, GPT Image 2.5 Flare for headline
  changes) and on video ads (Cherry 2 Pro edits that keep motion, framing,
  cuts, timing, and audio). Use when: "make variations of this ad",
  "multiply this ad", "ad variants", "creative testing", "A/B test
  versions", "new talent / new model in this ad", "change the setting",
  "10 headline variants", "refresh this creative", "same ad with different
  people". NOT for: resizing an ad for placements (use mage-ad-resizer),
  translating an ad (mage-ad-localizer), creating a first ad from a product
  photo (mage-product-photoshoot ad_creative_pack), or UGC videos from
  scratch (mage-ugc-video).
license: MIT
compatibility: Requires the Mage connector (https://mcp.mage.space/mcp) and a Mage account with Gems.
metadata:
  author: mage-space
  version: "0.0.0" # x-release-please-version
---

# Mage Ad Multiplier

Make independent variations of one ad for creative testing. Each variation changes only what was asked and keeps the rest of the ad identical: product, logo, layout, untargeted text, and for video the motion, framing, cuts, timing, and audio.

## Before you start

1. **Mage tools:** `get_model`, `estimate_cost`, `generate`, `get_request`, and `create_upload` for local files. If they are missing, ask the user to connect Mage (Claude: Customize → Connectors → Add custom connector, `https://mcp.mage.space/mcp`; Claude Code: `/mcp` to sign in if the Mage plugin is installed, otherwise `claude mcp add --transport http mage https://mcp.mage.space/mcp`; others: https://www.mage.space/mcp), then wait.
2. **The ad is a link:** an https URL of the image or video file, a data URL under about 3 MB, or an upload from disk (`create_upload`, needed for most videos). Files attached to the chat never reach Mage.

## UX rules

1. Ask at most one question: which elements to vary, when the request doesn't say. Offer the axes below as options.
2. Every variation is its own generation from the original ad, never an edit of another variation, so they stay independent.
3. Quote the total Gems and wait for a yes. Video variations are priced by the source clip's length, measured on submit; give the per-second rate from `estimate_cost` or a range, and say so.
4. Deliver labeled links (what changed), nothing else. Links expire after 30 days.
5. Never change the product, the logo, the offer, prices, legal text, or any text the user didn't ask to change.

## Variation axes

| Axis | Changes | Keeps |
|---|---|---|
| Talent | The person: age, look, ethnicity, style (or a saved `@character`) | Pose, framing, gesture, product interaction |
| Wardrobe | Clothing and accessories | Person, pose, setting |
| Setting | The location or interior | Person, pose, product, framing |
| Background | Backdrop color or texture only | Everything in the foreground |
| Color story | Palette of set dressing and grade | Product and brand colors |
| Season | Seasonal props, light, and weather | Product, layout |
| Headline | Only the headline text | Everything else, including other text |
| Remix | Two axes together (talent + wardrobe, setting + season) | The rest |

Recipes per axis: `references/variation-axes.md`.

## Static ads

1. Pass the original ad in `image`; refer to it as `@image1`. Add a saved `@character` or an outfit `@reference` if the user wants a specific person or look.
2. Model: Mango 3 (`mango`, `mango-v3`) for image changes; it keeps the rest of the image in place. For headline-only variations, GPT Image 2.5 Flare (`gpt_image_2`, `gpt-image-2.5-flare`) renders text most reliably. Match the original's `aspect_ratio`; `resolution: "2K"`.
3. One prompt per variation from the axis recipe: the change, then the lock list.
4. Headline variants: write the headlines first (short, distinct angles: benefit, urgency, social proof, curiosity, offer) and show them with the price in one message; generate after the user approves or edits them.

## Video ads

1. The source clip goes in `videos` (one clip) on Cherry 2 Pro (`cherry`, `cherry-2-pro`); keep its `aspect_ratio`, and set `duration` to the clip's length rounded up to an allowed value. Lemon (`lemon`) edits at a lower price when the user wants cheaper drafts.
2. Prompt: the change in one or two sentences, then: "Keep the original motion, camera moves, framing, cuts, timing, product, logo, on-screen text, and audio."
3. `estimate_cost` answers `requires_media_measurement` for a video input: the price is set by the clip's length when it's submitted. Quote from a probe or the user's clip length, and say it's approximate.

## Workflow

1. Get the ad and the axes (and headlines, for headline variants).
2. `get_model` for the model(s), `estimate_cost`, quote the total, wait for a yes.
3. `generate` every variation (new UUID `idempotency_key` each), then `get_request` (`wait_seconds: 120`) on each.
4. Check each result if you can see it: the product, logo, and untouched text must match the original. Regenerate a variation once if not.

## Deliver

```text
4 variations ready:
- Talent · young runner: https://…
- Wardrobe · winter layers: https://…
- Setting · rooftop at dusk: https://…
- Headline · "Run the city": https://…
```

Offer the next step once: resize the winners for every placement (`mage-ad-resizer`) or localize them (`mage-ad-localizer`).

## References

- `references/variation-axes.md`: prompt recipes and lock lists for every axis, static and video.
