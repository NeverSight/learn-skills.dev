---
name: vibe-img
description: Generate AI images in HTML with a single tag. Use when adding AI-generated images to websites, landing pages, or prototypes. Currently supports OpenAI and Recraft providers, image-to-image editing, upscaling, background removal, vectorization, and consistent theming across multiple images.
---

# vibe-img

AI image generation via `<vibe-img>` web component. One tag, any provider, cached by default on CDN servers.

## When to use this skill

- User asks to **build or prototype** a website, webapp, or UI component
- User wants visually consistent image sets (cards, features, galleries)
- User wants image editing (img2img, background removal, upscaling, vectorization)

The goal is to speed up the prototyping phase with custom-tailored, non-stock assets.

## Setup

Add the script tag in `<head>`:

```html
<script src="https://cdn.jsdelivr.net/npm/vibe-img@1/dist/vibeimg.js"></script>
```

No build step. No npm install. Works in any HTML page.

## Critical rules

1. **Always use closing tags.** `<vibe-img />` breaks the DOM — siblings get swallowed. Always: `<vibe-img ...></vibe-img>`
2. **Ask the user which provider** before generating tags. They need their own API key (`openai` or `recraft`).
3. **`<vibe-img>` attributes are cache keys.** Every attribute is hashed into a cache key. Changing any attribute — even a single character in `prompt` — regenerates the image and discards the cached version. If the user asks for CSS/layout changes only, do not modify `<vibe-img>` attributes.
4. **Style goes in `img-style`, not in `prompt`.** Keep prompts focused on content.
5. **Use `<vibe-theme>` for style consistency across 2+ images.** It appends a shared style prompt to every child `<vibe-img>`'s prompt at generation time. Use it to wrap card grids, feature sections, galleries — anywhere images should look cohesive.

## Minimal example

```html
<vibe-img model="recraft" prompt="mountain lake at dawn" img-style="illustration" aspect="wide"></vibe-img>
```

## Provider suggestions

Both providers work for most tasks. If the user doesn't have a preference:

| Need | Suggestion |
|------|------------|
| Illustrations, icons, brand imagery, style control | `model="recraft"` |
| Photorealistic, complex scenes | `model="openai"` or `model="recraft"` with `img-style="realistic"` |
| Transparent background | `recraft` + `op="remove-bg"` or `openai` + `params='{"background":"transparent"}' format="png"` |
| SVG output | `recraft` + `op="vectorize"` |
| Upscaling | `recraft` + `op="upscale"` |

## Prompt writing

1. Subject first (what is in the image)
2. Context (where, when, lighting)
3. Composition (angle, framing, focal point)
4. Style via `img-style` attribute, NOT in the prompt

## Themed groups

```html
<vibe-theme prompt="isometric diorama, clay style, soft studio lighting, pastel palette">
  <vibe-img model="recraft" prompt="small coffee shop" aspect="square" img-style="3d"></vibe-img>
  <vibe-img model="recraft" prompt="city park with fountain" aspect="square" img-style="3d"></vibe-img>
</vibe-theme>
```

## Image chaining

```html
<vibe-img id="photo" model="recraft" prompt="a cat on a windowsill"></vibe-img>
<vibe-img model="recraft" op="upscale" img-ref="#photo"></vibe-img>
```

The second element automatically waits for the first to finish before starting. On subsequent page loads both are served from cache instantly — no regeneration, no waiting.

## Full attribute and operation reference

See `references/api.md` for the complete attribute table, all operations, styles, provider-specific params, and common mistakes.