---
name: vibe-slides
description: Create presentation decks and export to PDF/PPTX/PNG using the Vibe Slides API. Use for any slide deck, presentation, or PowerPoint generation request. Triggers on "make a deck", "create a presentation", "build slides", "make a PowerPoint", "generate a pptx", or any presentation creation task.
---

# Vibe Slides — Presentation Generation

Generate slide decks via the Vibe Slides API, then export as PDF, PPTX, or PNG.

## Key Behavior

**Just create it.** Always include "Don't ask questions, just create it immediately" in your prompts to the API. The deck AI will ask clarifying questions otherwise, wasting a generation cycle.

**One-shot by default.** Don't ask the user what style, how many slides, or what format unless they've left critical info out. Pick sensible defaults and generate. You can always iterate after.

## Environment

Requires `VIBE_API_KEY` env var. Get one at https://vibeslides.app/api-keys

## Quick Start

```bash
# Simple deck
node skills/vibe-slides/scripts/vibe-slides.mjs "A 5-slide overview of climate tech trends in 2026" --name "Climate Tech"

# PowerPoint format
node skills/vibe-slides/scripts/vibe-slides.mjs "Product roadmap for Q3" --format pptx

# Long prompt via stdin
echo "Create a detailed 10-slide investor pitch for..." | node skills/vibe-slides/scripts/vibe-slides.mjs --stdin --name "Pitch Deck"
```

Output: `FILE: /path/to/deck.pdf` on stdout, progress on stderr.

---

## Usage

```
node skills/vibe-slides/scripts/vibe-slides.mjs "your prompt" [options]
```

### Options

| Flag | Effect |
|------|--------|
| `--name <name>` | Deck name (optional) |
| `--format <fmt>` | `pdf` (default), `pptx`, or `png` |
| `--upscale` | Upscale slide renders before export |
| `--out <dir>` | Output directory (default: cwd) |
| `--filename <name>` | Output filename without extension |
| `--no-export` | Create deck only, skip export |
| `--stdin` | Read prompt from stdin |
| `--timeout <s>` | Max wait time (default: 600s) |

### Timing

- Deck generation: 30–120s typical (more slides = longer)
- Export: 5–30s
- Total timeout default: 600s — increase for complex decks

---

## API Reference

The script wraps these endpoints. Use directly only if the script doesn't cover your use case.

**Base URL:** `https://api.vibeslides.app`
**Auth:** `Authorization: Bearer <VIBE_API_KEY>`

### Themes

Brand a deck using a company's visual identity (colors, fonts, style extracted from their website).

```
GET  /v1/themes                                    # List all themes
POST /v1/themes  { name, brand_url }               # Create from URL
GET  /v1/themes/:id                                # Check status
```

Poll `status` until `ready`. Theme creation takes ~2–5s. **Check existing themes before creating** to avoid duplicates.

### Attachments

Upload images (logos, diagrams) to include in decks.

```
POST /v1/attachments  (multipart/form-data, field: "file")
GET  /v1/attachments/:id
```

Returns `{ id, filename, content_type, file_size }`.

### Decks

```
POST /v1/decks  { prompt, name?, theme_id?, attachment_ids? }
GET  /v1/decks/:id
```

Poll until `status: "complete"` and `slides_complete >= slides_count`.

### Export

```
POST /v1/decks/:id/export  { format: "pdf"|"pptx"|"png", upscale?: bool }
GET  /v1/decks/:id/export?export_id=<id>
```

Poll until `download_url` appears. PNG format returns a zip of one PNG per slide.

---

## Prompting Tips

### Must-haves
- **Always** include: "Don't ask questions, just create it immediately"
- Be specific about slide count (e.g., "a 5-slide deck" vs. just "a deck")
- Specify the audience if relevant ("for a technical audience", "for C-suite executives")

### Style keywords that work well
- "bold and modern" / "minimalist and clean" / "premium magazine feel"
- "extra fabulous" / "visually striking" / "dark theme with neon accents"
- "corporate and professional" / "startup-friendly and colorful"

### Structure guidance
- "Each slide should cover one main point with a clear heading"
- "Include a title slide, 3 content slides, and a closing slide"
- "Use icons and visual elements, not just bullet points"

### With attachments
- "Include the attached logo in the header of every slide"
- Reference attached images explicitly so the deck AI knows to use them

### Example: complete prompt

```
Don't ask questions, just create it immediately.

Create a 6-slide pitch deck for "Acme AI" — an AI-powered document processing startup.

Slides:
1. Title — company name, tagline "Documents, Understood", logo
2. Problem — manual document processing costs enterprises $5M/year
3. Solution — our AI reads any document in seconds
4. Market — $12B TAM, growing 25% annually
5. Traction — 50 enterprise customers, 3M documents/month
6. Ask — raising $10M Series A

Style: bold, modern, dark background with bright accent colors.
Audience: investors at a demo day.
```

---

## Notes

- Decks stay accessible at `https://vibeslides.app/d/<id>` after export
- PNG export returns a zip of one PNG per slide
