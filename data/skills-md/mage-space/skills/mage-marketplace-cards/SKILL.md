---
name: mage-marketplace-cards
description: |
  Marketplace listing images with Mage: a compliant main image on pure white,
  secondary images (infographic, multiple angles, detail, lifestyle, what's in
  the box), and A+ / enhanced brand content modules, generated from one
  product photo with the product kept exact. Mango 3 for product photos, GPT
  Image 2.5 Flare for images with text. Use when: "Amazon listing images",
  "marketplace images", "product listing photos", "main image", "white
  background image", "infographic for my product", "A+ content", "enhanced
  brand content", "secondary images", "listing image set", "Etsy / Walmart /
  Shopify product images". NOT for: brand or social photography without a
  listing context (use mage-product-photoshoot), static ads
  (mage-ad-multiplier), product videos (mage-ugc-video), or images with no
  product (mage-generate).
license: MIT
compatibility: Requires the Mage connector (https://mcp.mage.space/mcp) and a Mage account with Gems.
metadata:
  author: mage-space
  version: "0.0.0" # x-release-please-version
---

# Mage Marketplace Cards

Build a listing's image set from one product photo: the main image, the secondary images, and A+ modules. Every card uses the product image as its reference, and every word on a card comes from the user.

## Before you start

1. **Mage tools:** `get_model`, `estimate_cost`, `generate`, `get_request`, and `create_upload` for local files. If they are missing, ask the user to connect Mage (Claude: Customize → Connectors → Add custom connector, `https://mcp.mage.space/mcp`; Claude Code: `/mcp` to sign in if the Mage plugin is installed, otherwise `claude mcp add --transport http mage https://mcp.mage.space/mcp`; others: https://www.mage.space/mcp), then wait.
2. **Product image:** an https link to the file, a data URL under about 3 MB, or an upload from disk (`create_upload`). Files attached to the chat never reach Mage. A clean front photo works best; a second angle helps the angle cards.

## UX rules

1. Ask at most one short question before quoting: usually the marketplace and the product facts you need for text cards.
2. Never invent facts. Features, ingredients, dimensions, certifications, results, and reviews come only from the user or their listing. With no facts, make image-only cards and say which text cards need input.
3. Quote the total Gems for the set and wait for a yes.
4. Deliver labeled links only; no JSON, ids, or prompts. Mention once that links expire after 30 days.
5. Reply in the user's language; text on cards is in the listing's language.

## Scopes

| Scope | Cards |
|---|---|
| `main` | 1 main image |
| `product-images` | Main + 5 secondary: infographic, multi-angle, detail, lifestyle, what's in the box |
| `aplus` | Main + 7 A+ modules: hero banner, pain points, features, ingredients or materials, results, how to use, endorsement |
| `full-set` | Main + 5 secondary + 7 A+ |

Use a custom subset when the user names specific cards. Drop cards that don't apply (no "ingredients" for a phone case; no "endorsement" without real quotes).

## Cards

| Card | Model | Aspect | Text |
|---|---|---|---|
| `main_image` | Mango 3 | `1:1` | None |
| `infographic` | GPT Image 2.5 Flare | `1:1` | 3–5 short callouts from the user's facts |
| `multi_angle` | Mango 3 | `1:1` | None |
| `detail_shot` | Mango 3 | `1:1` | None |
| `lifestyle` | Mango 3 (Guava 2 Pro if a person is central) | `1:1` | None |
| `whats_in_box` | Mango 3 | `1:1` | None, or item labels via Flare |
| `aplus_hero_banner` | GPT Image 2.5 Flare | `21:9` | Brand line |
| `aplus_pain_points` | GPT Image 2.5 Flare | `16:9` | Problem → solution |
| `aplus_features` | GPT Image 2.5 Flare | `16:9` | 3–4 features |
| `aplus_ingredients` | GPT Image 2.5 Flare | `16:9` | Named ingredients or materials |
| `aplus_efficacy` | GPT Image 2.5 Flare | `16:9` | Only results the user supplies |
| `aplus_how_to_use` | GPT Image 2.5 Flare | `16:9` | 3 steps |
| `aplus_endorsement` | GPT Image 2.5 Flare | `16:9` | Only real quotes the user supplies |

Ids: Mango 3 `mango` / `mango-v3`; Guava 2 Pro `guava` / `guava-2-pro`; GPT Image 2.5 Flare `gpt_image_2` / `gpt-image-2.5-flare`. Use `resolution: "2K"`. Confirm fields with `get_model`.

## Workflow

1. **Marketplace.** Default Amazon. Read `references/marketplace-rules.md` for its main-image rules; other marketplaces are there too.
2. **Facts.** Collect or extract the product name, three to five key features, what's included, and any claims the user can back. Use the user's wording.
3. **Main image first.** Generate it alone, check it against the rules (pure white, product fills about 85% of the frame, no text or props), and fix it before building the rest: every other card reuses the product from the same reference.
4. **The rest.** Write each card from `references/card-recipes.md`. Pass the product image in `image` and call it `@image1`. For consistent A+ modules, write one style line (palette, type style, background) and repeat it in every module.
5. **Price, generate, wait:** `estimate_cost` per distinct config, quote the total, `generate` each card (new UUID `idempotency_key`), `get_request` with `wait_seconds: 120`.
6. **Check.** If you can see the images, verify the product is unchanged and every word is spelled exactly as supplied. Regenerate a card once if not.

## Deliver

```text
Listing images ready:
- Main image: https://…
- Infographic: https://…
- Lifestyle: https://…
```

Say which marketplace rules the main image follows, and list any cards skipped for missing facts.

## References

- `references/marketplace-rules.md`: main-image and A+ rules for Amazon, Walmart, Etsy, eBay, and Shopify.
- `references/card-recipes.md`: the prompt recipe for every card.
