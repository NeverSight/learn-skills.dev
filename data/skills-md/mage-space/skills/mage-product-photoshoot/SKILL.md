---
name: mage-product-photoshoot
description: |
  Brand-quality product photos from one product image with Mage: studio
  packshots, lifestyle scenes, close-ups with hands, Pinterest pins, hero
  banners, carousels, ad packs, virtual try-on, surreal concept shots, and
  seasonal restyles. Ten modes with built-in photography recipes, the right
  Mage model per mode (Mango 3, Guava 2 Pro, GPT Image 2.5 Flare), and the
  product kept faithful across every variant. Use when: "product photo",
  "product photoshoot", "studio shot", "packshot", "lifestyle image",
  "Pinterest pin", "hero banner", "carousel", "ad creatives", "Meta ads
  images", "virtual try-on", "model wearing my product", "person holding
  my product", "floating/levitating/splash product", "CGI product",
  "Christmas version of my product photo". NOT for: marketplace listing sets
  with compliant main images and A+ modules (use mage-marketplace-cards),
  variants of an existing ad (mage-ad-multiplier), UGC product videos
  (mage-ugc-video), or images with no product (mage-generate).
license: MIT
compatibility: Requires the Mage connector (https://mcp.mage.space/mcp) and a Mage account with Gems.
metadata:
  author: mage-space
  version: "0.0.0" # x-release-please-version
---

# Mage Product Photoshoot

Turn one product photo into a shoot. Pick a mode, ask a few labeled questions, write each variant's prompt from the mode's recipe, and generate every variant with the product locked to the reference.

## Before you start

1. **Mage tools:** `get_model`, `estimate_cost`, `generate`, `get_request`, and `create_upload` for local files. If they are missing, ask the user to connect Mage (Claude: Customize → Connectors → Add custom connector, `https://mcp.mage.space/mcp`; Claude Code: `/mcp` to sign in if the Mage plugin is installed, otherwise `claude mcp add --transport http mage https://mcp.mage.space/mcp`; others: https://www.mage.space/mcp), then wait.
2. **The product image is a link.** An https URL of the file (a store image, a CDN link), a data URL under about 3 MB, or an upload from disk with `create_upload`. Files attached to the chat never reach Mage. A product saved as an `object` reference works by `@handle`.

## UX rules

1. Deliver image links with short labels. No JSON, ids, model internals, or the prompts you wrote.
2. Reply in the user's language; prompts sent to Mage stay in English, except text meant to appear in the image.
3. Ask at most four short questions, as labeled options, in one message. Skip any the context already answers.
4. Quote the total Gems for the set and wait for a yes before generating.
5. Never change the product: shape, color, label, logo, and text stay as in the reference. If the reference is too small or blurry to read, say so and ask for a better one.

## Modes

| Mode | For | Aspect | Model |
|---|---|---|---|
| `product_shot` | Packshot on white, gray, or a colored studio sweep | `1:1` or `4:5` | Mango 3 |
| `lifestyle_scene` | Product in use in a real place: kitchen, gym, desk, outdoors | `4:5` | Mango 3 |
| `closeup_with_person` | Hands holding or applying it, partial face, demonstration | `4:5` | Guava 2 Pro |
| `moodboard_pin` | Vertical, Pinterest-native, styled flat lay or vignette | `2:3` | Mango 3 |
| `hero_banner` | Wide website, email, or campaign header with room for copy | `21:9` or `16:9` | Mango 3 |
| `social_carousel` | 3–10 connected slides with one visual system | `4:5` or `1:1` | Mango 3 (Flare for text slides) |
| `ad_creative_pack` | Static ad variants for Meta, TikTok, Pinterest, Google | `1:1`, `4:5`, `9:16` | GPT Image 2.5 Flare with copy, else Mango 3 |
| `virtual_try_on` | Clothing, jewelry, or accessories worn by a model | `4:5` or `2:3` | Guava 2 Pro |
| `conceptual_product` | Levitating, splash, frozen motion, surreal, sculptural, CGI | `4:5` or `1:1` | Mango 3 |
| `restyle` | New mood, aesthetic, or season for an existing product image | same as source | Mango 3 |

Model ids: Mango 3 is `mango` / `mango-v3`; Guava 2 Pro is `guava` / `guava-2-pro` (at most 3 reference images); GPT Image 2.5 Flare is `gpt_image_2` / `gpt-image-2.5-flare`. Always `resolution: "2K"`. Confirm fields with `get_model`.

### Choosing the mode

Choose by intent, and prefer the more specific mode when two fit:

- clean, white, studio, catalog, Shopify → `product_shot`
- in use, kitchen, outdoor, cafe, gym, "in context" → `lifestyle_scene`
- hands, applying, holding, demonstrating, beauty → `closeup_with_person`
- Pinterest, pin, moodboard → `moodboard_pin`
- hero, banner, header, landing page, email → `hero_banner`
- carousel, slides, swipe → `social_carousel`
- ads, ad pack, paid social, Meta/TikTok ads → `ad_creative_pack`
- worn by a model, try-on, lookbook, on body → `virtual_try_on`
- floating, splash, surreal, CGI, sculptural → `conceptual_product`
- change the vibe or season of an existing image → `restyle`

Tie-breakers: "Pinterest pin on a kitchen counter" → `moodboard_pin`; "hero banner showing it in use" → `hero_banner`; "carousel of it in different scenes" → `social_carousel`.

## Interview

Ask only what's missing, as options:

- **Product photo, "make me photos":** How many? `[1 / 3 / 5]` · Style? `[Clean studio / Lifestyle / Conceptual / With a model]` · Where will they run? `[Shop / Instagram / Pinterest / Ads / Website hero]` · Brand colors to match?
- **Named use case** ("make a hero banner"): only the gaps: how many, the mood or offer, anything to emphasize.
- **No photo:** ask for a link to one (much higher fidelity). If there is none, get the category, packaging, colors, and distinctive details, and generate from the description.
- **Restyle:** aesthetic `[Clean girl / Quiet luxury / Cottagecore / Dark academia / Y2K / Other]` · season `[Holiday / Valentine's / Summer / Halloween / Black Friday / None]`.
- **Try-on:** model archetype (suggest two or three for the audience) · setting `[Studio / Street / Outdoor / Editorial / Home]` · framing `[Full body / Three-quarter / Waist up / Close-up]`.

## Generate

1. Read `references/modes.md` for the chosen mode and write one prompt per variant from its recipe. Vary the listed axes across variants, so no two are paraphrases.
2. Pass the product image in `image` and refer to it as `@image1` in each prompt ("the product from @image1"). Add a second product angle in `additional_images` if the user has one. Brand assets (a logo, a palette swatch) go in `additional_images` too.
3. `get_model` for each model you use, then `estimate_cost` per distinct config; quote the total.
4. Start every variant with `generate` (new UUID `idempotency_key` each), then wait on each with `get_request` (`wait_seconds: 120`).
5. Look at every result if you can see images. Regenerate a variant once if the product changed (wrong label, color, or shape) or text is misspelled.

For a carousel or ad pack, lock the visual system first: write one style line (palette, light, type style, background) and repeat it in every slide.

## Deliver

```text
3 lifestyle shots ready:
- Morning counter: https://…
- Gym bag: https://…
- Desk at golden hour: https://…
```

Mention once that links expire after 30 days. Offer one next step that fits: more variants, a resize (`mage-ad-resizer`), or a video (`mage-ugc-video`).

## Don't

- Write the product's text or logo from memory; copy what's visible in the reference.
- Use Guava 2 Pro with more than 3 images, or GPT Image 2.5 Flare for photoreal people when Guava 2 Pro fits better.
- Generate a set with different aspect ratios unless the user asked for placements.

## References

- `references/modes.md`: the recipe for each mode (prompt template, variation axes, pitfalls).
