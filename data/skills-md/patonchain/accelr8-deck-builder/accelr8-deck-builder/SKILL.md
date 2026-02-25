---
name: accelr8-deck-builder
description: Create beautiful slide decks as shareable webpages. Use when asked to make presentations, pitch decks, or slides. Generates images with nanobanana, removes backgrounds automatically. Exports to PDF.
---

# ACCELR8 Deck Builder

Create slide decks as standalone HTML files. Share as a link. Export as PDF with one click.

## Quick Start

1. Read `references/template.html` — this is your starting point
2. Create a new HTML file, copy the template contents
3. Add slides using the layout classes below
4. Generate images using the asset workflow
5. Open in browser to present or export

## The Asset Workflow

When slides need images, use this three-step process:

### 1. Generate with Background Removal

```bash
python ~/accelr8-deck-builder/scripts/generate_asset.py \
  --prompt "a confident businesswoman presenting" \
  --output speaker.png \
  --remove-bg
```

This generates the image AND removes the background automatically.

### 2. Generate without Background Removal

For backgrounds, gradients, full-bleed images:

```bash
python ~/accelr8-deck-builder/scripts/generate_asset.py \
  --prompt "abstract gradient, warm orange to deep purple, minimal, 16:9" \
  --output hero-bg.png
```

### 3. Remove Background from Existing Image

```bash
python ~/accelr8-deck-builder/scripts/generate_asset.py \
  --input photo.jpg \
  --output photo-clean.png \
  --remove-bg
```

### Prompt Guidelines for Clean Cutouts

When generating images for background removal, include:
- "isolated on white background"
- "product photography style"
- "clean edges"
- "studio lighting"

The script adds these automatically when `--remove-bg` is used.

**Examples:**

```bash
# Person for split slide
--prompt "professional man in suit, confident pose" --remove-bg

# Product shot
--prompt "modern laptop, front view, floating" --remove-bg

# Icon/object
--prompt "golden trophy, 3D render" --remove-bg

# Abstract shape (no bg removal needed)
--prompt "flowing abstract ribbons, blue and purple gradient"
```

## Template

Read `references/template.html` for the complete working template. Copy it to start a new deck.

The template includes:
- All CSS styles embedded
- PDF export with progress indicator
- Presentation mode
- All slide layouts ready to use

## Slide Layouts

Each slide is a `<section class="slide slide--TYPE">`:

### Title Slide
```html
<section class="slide slide--title">
    <p class="label">Category</p>
    <h1>Main Title</h1>
    <p>Subtitle text</p>
</section>
```

### Content Slide
```html
<section class="slide slide--content">
    <h2>Slide Title</h2>
    <p>Body text here.</p>
    <ul>
        <li>Point one</li>
        <li>Point two</li>
        <li>Point three</li>
    </ul>
</section>
```

### Bullets Slide (Large)
```html
<section class="slide slide--bullets">
    <h2>Key Points</h2>
    <ul>
        <li>First major point</li>
        <li>Second major point</li>
        <li>Third major point</li>
    </ul>
</section>
```

### Split Slide (Text + Image)

Perfect for transparent PNGs:

```html
<section class="slide slide--split">
    <div>
        <p class="label">Label</p>
        <h2>Title</h2>
        <p>Description text.</p>
    </div>
    <div>
        <img src="speaker.png" alt="Speaker" crossorigin="anonymous">
    </div>
</section>
```

### Quote Slide
```html
<section class="slide slide--quote">
    <blockquote>
        "Quote text here."
        <cite>— Attribution</cite>
    </blockquote>
</section>
```

### Image Slide (Full Bleed)
```html
<section class="slide slide--image">
    <img src="hero.png" alt="Description" crossorigin="anonymous">
    <figcaption>Optional caption</figcaption>
</section>
```

### Section Divider
```html
<section class="slide slide--section">
    <p class="label">Part One</p>
    <h2>Section Title</h2>
</section>
```

### Code Slide
```html
<section class="slide slide--code">
    <h2>Example</h2>
    <pre><code>const x = 1;</code></pre>
</section>
```

### End Slide
```html
<section class="slide slide--end">
    <h2>Thank You</h2>
    <p>contact@example.com</p>
</section>
```

## Components

Use inside any slide:

```html
<!-- Two columns -->
<div class="columns">
    <div>Left</div>
    <div>Right</div>
</div>

<!-- Three columns -->
<div class="columns-3">
    <div>One</div>
    <div>Two</div>
    <div>Three</div>
</div>

<!-- Card -->
<div class="card">
    <h3>Title</h3>
    <p>Content</p>
</div>

<!-- Numbered step -->
<div class="icon-row">
    <span class="badge">1</span>
    <div>
        <h3>Step</h3>
        <p>Description</p>
    </div>
</div>
```

## Workflow Example

Creating a pitch deck:

```bash
# 1. Copy template
cp ~/accelr8-deck-builder/references/template.html ./pitch-deck.html

# 2. Generate hero background
python ~/accelr8-deck-builder/scripts/generate_asset.py \
  --prompt "abstract gradient, dark blue to purple, minimal, 16:9" \
  --output hero-bg.png

# 3. Generate team photo cutout
python ~/accelr8-deck-builder/scripts/generate_asset.py \
  --prompt "diverse startup team, casual professional, standing together" \
  --output team.png \
  --remove-bg

# 4. Generate product shot
python ~/accelr8-deck-builder/scripts/generate_asset.py \
  --prompt "modern SaaS dashboard on laptop screen, floating, 3D render" \
  --output product.png \
  --remove-bg

# 5. Edit pitch-deck.html, add slides, reference images

# 6. Open in browser, present or export PDF
open pitch-deck.html
```

## Features

- **Present button** — Fullscreen mode (or press P)
- **Export PDF** — Downloads PDF automatically, each slide = one page
- **Arrow keys** — Navigate in presentation mode
- **Escape** — Exit presentation

## Design Rules

1. One idea per slide
2. Maximum 6 bullet points
3. Use transparent PNGs for people/products on split slides
4. Full-bleed images for emotional impact
5. Section dividers every 3-4 slides
6. End with clear call to action

## Requirements

- Python 3.8+
- nanobanana skill (for image generation)
- rembg (auto-installed on first use)
- GEMINI_API_KEY environment variable

---

Read `references/template.html` for the complete working template.
