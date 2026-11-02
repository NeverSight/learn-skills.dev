---
name: mage-youtube-thumbnail
description: |
  High-click-through YouTube thumbnails and vertical video covers with Mage:
  a truthful information-gap concept, up to three faces kept identical to
  their photos, an optional logo, bold punchy lighting, controlled variants
  (different emotions or takes), a headline baked in on request, and
  surgical follow-up edits. Mango 3 renders, GPT Image 2.5 Flare adds text.
  Use when: "YouTube thumbnail", "thumbnail for my video", "MrBeast-style
  thumbnail", "clickable thumbnail", "Shorts cover", "Reels cover",
  "Instagram video cover", "podcast episode cover", "make my face look
  shocked in the thumbnail". Chain after mage-faceless-video or any video
  once its topic is known. NOT for: making the video itself (use
  mage-generate or mage-faceless-video), product catalog photos
  (mage-product-photoshoot), or ads (mage-ad-multiplier).
license: MIT
compatibility: Requires the Mage connector (https://mcp.mage.space/mcp) and a Mage account with Gems.
metadata:
  author: mage-space
  version: "0.0.0" # x-release-please-version
---

# Mage YouTube Thumbnail

Design a thumbnail that makes people click and tells the truth about the video. Render it with Mango 3, keep faces identical to their photos, and make only the edits asked for afterwards.

## Before you start

1. **Mage tools:** `get_model`, `estimate_cost`, `generate`, `get_request`, `list_characters`, and `create_upload` for local files. If they are missing, ask the user to connect Mage (Claude: Customize → Connectors → Add custom connector, `https://mcp.mage.space/mcp`; Claude Code: `/mcp` to sign in if the Mage plugin is installed, otherwise `claude mcp add --transport http mage https://mcp.mage.space/mcp`; others: https://www.mage.space/mcp), then wait.
2. **Faces and logos are links:** https URLs of the files, data URLs under about 3 MB, uploads from disk (`create_upload`), or saved `@character` handles. Files attached to the chat never reach Mage.

## UX rules

1. Don't ask for what the brief already says. Ask one compact question only when a missing choice changes the result: usually who appears.
2. **Truthful.** The thumbnail may exaggerate but must honestly represent the video. Never invent outcomes, numbers, people, or screenshots.
3. **People:** 0–3. If the concept needs a person and no face was given, ask: the user (send a photo or `@handle`), someone else they provide, or a generic generated person. Never pick silently. Only use someone's face with their consent.
4. A style-reference thumbnail is for analysis only: describe its energy, layout, palette, and emotion, but never pass it to Mage or copy its people.
5. No text in the image unless asked. When asked, 2–4 words.
6. Deliver links with short labels (`shock · close-up`). No prompts, ids, or JSON. Hard cap: 16 generations per request.

## Intake

- The video's title or topic, and the promise the thumbnail can make.
- Who appears (see rule 3), and each person's emotion.
- Optional: logo (flat, or turned into a 3D object), headline text, a style-reference thumbnail.
- Ratio: `16:9` for YouTube (default), `9:16` for Shorts and Reels, `4:5` for Instagram feed.
- One final, or a variant set (about four when alternatives would help).

Emotion ladder when the user wants N emotions without naming them: shock, hype, awe, laugh, fear, smug, confusion, determination.

## Concept

Read `references/thumbnail-frameworks.md`. Brainstorm at least five truthful concepts across the frameworks, then pick the one with the strongest information gap, one focal subject, and the least clutter. It must read in under a second at about 120 px wide.

## Render

Mango 3 (`mango`, `mango-v3`), `resolution: "2K"`. Face photos go in `image` and `additional_images` in character order, then the logo; saved people can be `@handle`s instead. Assemble the prompt in this order:

1. **Frame:** "Bold, punchy YouTube-thumbnail image, poster-grade, photoreal and high-impact, not a muted movie still, <ratio>, one continuous shot with no split screen." For `9:16`, add "faces in the upper two-thirds".
2. **Scene:** the chosen concept, exactly.
3. **Text:** "No text, no readable UI, no watermark." (Headlines are added in a later step.)
4. **Subjects:** large, foreground, chest-up or closer, filling 40–60% of the frame. Per person: "CHARACTER N: the person from @imageK. Identity lock: reproduce this exact person with a photographic match, same bone structure, eyes, nose, lips, jawline, skin tone, hairline, and hair. Do not beautify or restyle the face. Expression: <emotion phrase>." End with "All faces crisply sharp."
5. **Key elements:** only the props that create the information gap.
6. **Logo:** "The logo from @imageK, exact shapes, colors, and letterforms, away from faces."
7. **Composition:** one hero on a power third, clear scale hierarchy, strong subject–background separation.
8. **Background:** vivid, high-contrast color field or environment, soft vignette.
9. **Lighting on people:** "Thumbnail lighting rig: strong key light sculpting the face, soft fill, bright rim light tracing hair and shoulders."
10. **Grade:** vivid, glossy, saturated, deep blacks, crisp highlights. Tone it down only for a calm or premium brief.

For a variant set, one generation per concept or emotion, same references and settings; vary only that one line. Quote the total Gems first and wait for a yes.

## Check

If you can see the results: faces match their photos, no stray text, the emotion and hero read at thumbnail size, the concept is true to the video. Retry a hard failure at most twice. If you can't see images, say the results need the user's review.

## Edits

Use the picked result's URL as the only image, Mango 3, same ratio, and change one thing:

```
Change ONLY <the person's expression to: <phrase> / the background to: … /
the rim light color to: …>. Keep identity, face, hair, pose, clothing, logo,
composition, and lighting exactly the same.
```

Each accepted edit becomes the source for the next. Never regenerate the whole composition for a small request.

## Headline text

When asked, bake 2–4 words onto the picked result with GPT Image 2.5 Flare (`gpt_image_2`, `gpt-image-2.5-flare`), the result in `image`:

```
Add the headline "<TEXT>" to @image1: huge, ultra-bold condensed sans-serif in
all caps, white with a thick black outline and a hard drop shadow, in the
<free corner / bottom third>, never covering a face. Change nothing else.
```

Check it letter by letter.

## Deliver

Return each passing link with a label (`shock · close-up`), the ratio, and whether it's clean or has text. Links expire after 30 days.

## References

- `references/thumbnail-frameworks.md`: 16 concept frameworks and the rules that make thumbnails work.
