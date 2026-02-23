---
name: etsy-listing-generator
description: Generate Etsy listing images from HTML templates using Playwright. Supports single and batch rendering with customizable title, subtitle, badge text, and product images. Use when creating Etsy product listing images, mockups, or running batch generation for multiple products (e.g., puppet printables, digital downloads). Works with any HTML template that uses PRODUCT_IMAGE_URL, TITLE_TEXT, SUBTITLE_TEXT, BADGE_LEFT_TEXT placeholders.
---

# Etsy Listing Image Generator

Generate professional Etsy listing images from HTML templates via Playwright screenshot rendering.

## Quick Start — Single Image

```bash
node scripts/render.mjs <template> <image-url> <title> <subtitle> <badge> <output>
```

Example:
```bash
node scripts/render.mjs \
  assets/puppet-listing.html \
  "http://localhost:3021/api/output/moses-characters.png" \
  "Bible Story Puppet Printables" \
  "Moses & The Exodus" \
  "12 ELEMENTS + 4 BACKGROUNDS" \
  output/moses-listing.png
```

## Quick Start — Batch

Create a JSON file with an array of objects:
```json
[
  { "file": "http://localhost:3021/api/output/moses-characters.png", "subtitle": "Moses & The Exodus" },
  { "file": "http://localhost:3021/api/output/david-characters.png", "subtitle": "David & Goliath" }
]
```

Run:
```bash
node scripts/render.mjs --batch assets/puppet-listing.html stories.json output/listings/
```

## Batch JSON Fields

| Field | Required | Default | Description |
|-------|----------|---------|-------------|
| `file` / `image` / `url` | Yes | — | Product image URL (HTTP or file://) |
| `title` | No | "Bible Story Puppet Printables" | Large top text on banner |
| `subtitle` / `name` | No | — | Smaller bottom text on banner |
| `badge` | No | "12 ELEMENTS + 4 BACKGROUNDS" | Left badge text |
| `output` | No | Auto from subtitle | Output filename |

## Template Placeholders

Templates are plain HTML files. The renderer replaces these strings:

- `PRODUCT_IMAGE_URL` → product/character image
- `TITLE_TEXT` → large banner text
- `SUBTITLE_TEXT` → smaller banner text  
- `BADGE_LEFT_TEXT` → left pill badge
- `INSTANT DOWNLOAD` → right badge (hardcoded, edit HTML to change)

## Template Design — Current Base (puppet-listing.html)

- **1400×2000px** portrait format
- White background, sage green (#4D6840) bottom banner
- Gold pill badges (top-left: custom, top-right: INSTANT DOWNLOAD)
- Poppins font throughout
- Product image uses `object-fit: cover; object-position: center center`
- Subtle TheSunDaisy watermark

## Creating New Templates

Copy `assets/puppet-listing.html` and modify. Key CSS to adjust:

- `.canvas` width/height — canvas dimensions
- `.banner` height — green section size
- `.product-area` top/bottom — image boundaries
- `.badge` styling — pill badge appearance
- `.title` / `.subtitle` — typography

Keep the placeholder strings (`PRODUCT_IMAGE_URL`, etc.) for the renderer to replace.

## Serving Local Images

If product images are local files, either:
1. Serve via Image Forge backend: copy to `/projects/image-forge/output/` → accessible at `http://localhost:3021/api/output/filename.png`
2. Use `file://` URLs (must be absolute paths)
3. Start any local HTTP server in the image directory

## Dependencies

- Node.js
- Playwright (`npx playwright install chromium` if not installed)
