---
name: nous-branding
description: >-
  Generate images and content consistent with the Nous Research brand identity. Use when
  creating visuals in the Nous / Theia / Hermes ecosystem: a "cyber-classical" style
  blending neo-classical statuary, cyberpunk/industrial grunge, and retro anime
  illustration. Covers official brand color palette, typography (Inter/IBM Plex Sans,
  JetBrains Mono, heavy distressed display faces), the Nous Girl mascot, texture system,
  and image prompt construction. Ships reference images for palette, mascot, and brand
  collage that can be used as img2img inputs. Do not use this skill for unrelated
  requests; route to the nearest named specialist.
license: MIT
compatibility: Compatible with any agent capable of image generation or brand analysis.
  Reference-image workflows (img2img, style transfer, variations) require an API endpoint
  supporting image inputs — use the assets/ images as input.
metadata:
  tags: nous-research, theia, hermes, brand, illustration, mascot, image-generation,
    style-guide, cyber-classical
  sources: https://nousresearch.com, {"Reference image"=>"assets/palette-typography-reference.png"},
    {"Reference image"=>"assets/nous-girl-official.webp (official mascot, 2669×2709)"},
    {"Reference image"=>"assets/nous-girl-style-reference.png"}, {"Reference image"=>"assets/brand-collage-reference.png"},
    https://nousresearch.com/wp-content/uploads/2024/03/NOUS-BRAND-BOOKLET-firstedition_1.pdf
  version: 1.1.0
---

# Nous Branding

Generate images and brand-consistent visual content inspired by **Nous Research** ("The AI accelerator company").

## When not to use

- **Non-Nous design work** — this skill encodes one specific brand system; do
  not apply its palette, textures, mascot, or compliance rules to unrelated
  brands or generic design requests.
- **Official brand representation** — the Nous Girl mascot is not a substitute
  for the logo; use the Nous Research wordmark/symbol for official brand use.

## Reference Images

This skill ships reference images in `assets/` that can be used as visual anchors for img2img, style transfer, image variation, or prompt construction:

| File | Description | Usage |
|------|-------------|-------|
| `assets/palette-typography-reference.png` | Brand identity system card showing the 6-color palette swatches with hex codes, typography specimen (Inter, IBM Plex Sans, JetBrains Mono, heavy display), and classified-dossier layout | Upload as reference for color palette and typography style |
| `assets/nous-girl-official.webp` | Official high-resolution (2669×2709) Nous Girl mascot from nousresearch.com. High-contrast black-and-white retro manga portrait. Three-quarter profile facing left, white headband (primary badge variant). 51% dark / 47% light, pure b&w with no gray. | Primary mascot reference — the single most authentic brand image |
| `assets/nous-girl-official-badge.png` | Official badge portrait from the brand booklet (5760×7454). Shows the Nous Girl in her canonical form: white headband, three-quarter profile, neutral attentive expression, stark black/white manga style. | Use when the badge/primary variant is needed |
| `assets/nous-girl-sketch-sheet.png` | Official character sheet from the brand booklet showing all 4 canonical poses: primary badge, headphone ¾ profile, headphone profile left, and headphone small profile. | Use for pose reference and character consistency |
| `assets/nous-girl-philosophy.png` | Brand philosophy page from the booklet showing the Nous Girl alongside the "decentralization of good design" mission statement. | Use for brand context and philosophy reference |
| `assets/nous-girl-style-reference.png` | Generated reference portrait with "NOUS" on headphones, electric blue accents, and color swatch label | Color-application reference and prompt examples |
| `assets/brand-collage-reference.png` | Cyber-classical brand collage with Theia marble statue, glowing electric blue eye with targeting reticle, system architecture diagram, CRT noise overlay | Multi-panel brand layout and HUD aesthetic reference |

---

## Brand Identity Overview

Nous Research's visual identity is a **three-way fusion**:

| Influence | Expression |
|-----------|-----------|
| **Classical / Greek myth** | Statuary of Theia (Titaness of Sight), marble textures, mythological naming |
| **Cyberpunk / Industrial** | Grunge textures, CRT scan lines, photocopy noise, distressed type, dark palette |
| **Retro Anime / Manga** | The "Nous Girl" mascot, cel-shaded illustration, large expressive eyes, 1970s-80s manga aesthetic |
| **Tech / Brutalist** | Heavy display typography, system diagrams, blueprint-style layouts, monospace code labels |

**Tagline:** "The AI accelerator company"
**Key phrases:** "Advance human rights and freedoms", "Open source language models", "Unrestricted availability and use"
**Vibe:** Intellectual but gritty — a cutting-edge research lab operating in the shadows

---

## Loading Guide

Load references on demand — do not load everything at once.

| File | Load when |
|------|-----------|
| [references/style-lanes.md](references/style-lanes.md) | Choosing a style lane or writing a lane-specific prompt — full lane grammar, prompt cues, example prompts, and the asset-to-lane Reference Catalog |
| [references/visual-system.md](references/visual-system.md) | Constructing or reviewing an image against the visual system — hero + extended palettes, Nous Girl spec and pose variants, typography, texture system, art style |
| [references/post-processing.md](references/post-processing.md) | Delivering any generated image — mandatory post-process modes (`imprint`/`nous`/`standard`) and intensity calibration for `scripts/postprocess.py` |
| [`references/pitfalls.md`](references/pitfalls.md) | Output doesn't match expectations — known failure modes and mitigations |

---

## Image Prompt Templates

### Method 1: Full Brand Portrait

```
A cyber-classical brand identity illustration in the style of Nous Research / Project Theia.
[SUBJECT DESCRIPTION]. High-contrast dramatic lighting with deep near-black background (#00000E).
Electric blue (#3847FF) primary accent. Soft lavender (#BDA6FF) and burnt orange (#D6825A)
secondary accents. Deep teal (#2E706B) shadow tones. Overlaid with risograph grain texture,
photocopy noise, and subtle CRT scan lines. Retro anime cel-shading combined with neo-classical
sculptural forms. Geometric HUD overlay lines in burnt orange. Bold, distressed display typography.
Raw, analog, imperfect finish. No corporate polish.
Palette: #00000E bg, #3847FF accent, #BDA6FF secondary, #D6825A warm, #E6E6E6 text.
```

### Method 2: Nous Girl Mascot

```
High-contrast retro manga anime portrait, 1970s-80s cel-shaded style.
A young woman with large anime eyes, shoulder-length dark hair with blunt
straight-across bangs. White over-ear headphones. Three-quarter profile facing left.
Melancholic introspective expression. Bold heavy outlines. Pure black and white with
no grayscale. [Optional: Electric blue #3847FF hair highlights for color version].
```

### Method 3: Brand System Sheet / Collage

```
Multi-panel brand identity system sheet in Nous Research / Project Theia style.
Grid layout. [Describe panels]. Color palette: #3847FF electric blue, #BDA6FF lavender,
#D6825A burnt orange, #2E706B deep teal, #E6E6E6 off-white, #00000E near-black.
Texture swatches: risograph grain, photocopy noise, CRT scan lines, paper fiber, ink smudge.
Typography: heavy distressed display for titles, Inter/IBM Plex Sans for labels,
JetBrains Mono for technical data. Grunge textures throughout. Dark near-black background.
```

### Method 4: Reference-Image-Driven Generation (Recommended)

**This is the preferred method for generating brand-consistent images.** Use the `scripts/generate-with-ref.py` script which reads your Hermes config, determines the active image provider, and hits the API directly with the reference image as contextual input — bypassing the built-in `image_generate` tool which only supports text prompts.

```
python3 scripts/generate-with-ref.py \
  --prompt "Your prompt describing the desired image" \
  --reference assets/nous-girl-official-badge.png \
  --aspect landscape \
  --quality medium
```

**Features:**
- `--prompt` (required) — image description
- `--reference` (required) — path to a reference image (use `assets/` images from this skill)
- `--aspect` — `landscape` (1536×1024), `portrait` (1024×1536), or `square` (1024×1024)
- `--quality` — `low`, `medium` (default), or `high`
- `--output` — custom output path
- `--dry-run` — preview without executing

**How it works:**
1. Reads `~/.hermes/config.yaml` to find your active image generation provider
2. For **OpenAI**: uses `/v1/images/edits` with multipart upload — the only endpoint that accepts image input with gpt-image-2
3. Automatically crops the reference to square (1024×1024) as required by the edits endpoint
4. Saves output to `~/.hermes/cache/images/`
5. Returns JSON with `image`, `model`, `aspect_ratio`, and `provider`

**Why this matters:** Text-only generation loses the precise manga style, character proportions, and contrast balance of the Nous Girl. Uploading the official badge preserves the specific 1970s–80s cel-shaded ink style.

**Prompting for reference workflows:**
State what to **preserve** from the reference, then what to **add**:
- "Keep the character's white over-ear headphones, white collared shirt, solid black hair with blunt bangs, neutral expression"
- "Maintain the same high-contrast black ink on white manga style"
- Then add the scene details, text, lighting, etc.

### Prompt Formula

```
[STYLE: cyber-classical / Nous Research]
+ [SUBJECT DESCRIPTION]
+ [PALETTE: #00000E bg, #3847FF accent, #BDA6FF, #D6825A]
+ [TEXTURES: risograph grain, photocopy noise, CRT scan lines, paper fiber, ink smudge]
+ [LIGHTING: high-contrast chiaroscuro, dramatic spot, neon edge highlights]
+ [MOOD: intellectual, gritty, underground, calm/attentive]
+ [TYPOGRAPHY: heavy distressed display, Inter/IBM Plex Sans labels, JetBrains Mono code]
```

---

## Post-Processing

Raw AI-generated images are too clean for the Nous aesthetic. **Post-processing is mandatory** after every generation — the raw generated image is never the final deliverable.

```bash
python3 scripts/postprocess.py input.png output.png --mode imprint --intensity 0.7
```

Run it as the final step after any generation method (text-only, img2img, multi-pass, or any provider). For mode selection (`imprint` / `nous` / `standard`) and intensity calibration per output type, load [references/post-processing.md](references/post-processing.md).

---

## API Workflow Notes

| API | Approach |
|-----|----------|
| **DALL-E 3** | Text-only. Use Method 1–3 prompts with hex values. |
| **OpenAI Variations / Edit** | Upload `assets/*.png` as image input. Prompt describes differences. |
| **Midjourney** | `--sref <asset-url>` with `--iw 1.5–2.0`. Include palette hex values in prompt. |
| **ComfyUI** | IPAdapter or Reference-Only ControlNet from assets. Denoise 0.6–0.7. Post-process with grain overlay. |
| **Replicate / SD img2img** | Upload reference. Prompt strength 0.7–0.8. CFG 7. |

---

## What Is NOT On-Brand

Avoid these common anti-patterns:

| Anti-Pattern | Why It's Wrong |
|-------------|----------------|
| **Sad/melancholic expression** | Model defaults to sad for manga characters unless explicitly told "not sad, not crying" |
| **Dark/black headphones** | Nous Girl wears **white** over-ear headphones in all canonical poses |
| **Facial markings (teardrop, tattoos, scars)** | The character has clean, clear skin — no markings whatsoever |
| **Wrong ethnicity (Asian instead of French)** | Model defaults to Asian features for anime style; explicitly state "French Caucasian" |
| **Busy/cluttered compositions** | The brand is restrained — dark background, 1-2 accent colors, 2-3 text elements max |
| **Smooth digital illustration** | The brand is **never** clean — every image needs grain, noise, or analog texture |
| **Cartoon/anime with glossy rendering** | The manga style is stark black ink on white paper — no soft shading, no gradients |
| **Corporate/sterile tech aesthetic** | The finish should feel like an underground research lab, not a SaaS landing page |
| **Over-detailed backgrounds** | Let the subject breathe. Negative space is a feature. |

For a complete list of known failure modes and mitigations, see [`references/pitfalls.md`](references/pitfalls.md).

---

## Brand Compliance Checklist

- [ ] Background is near-black (#00000E) or very dark
- [ ] Electric blue (#3847FF) is used as primary accent
- [ ] At least one grunge texture visibly applied (grain, noise, scan lines, paper, ink)
- [ ] High contrast — dramatic light/dark difference
- [ ] Palette is restricted to the specified colors
- [ ] If mascot appears: white headphones, manga style, neutral attentive expression, three-quarter profile
- [ ] If text appears: heavy distressed display for titles, clean sans for labels, monospace for code
- [ ] No flat/clean/corporate polish — finish is raw and tactile
- [ ] Overall impression: intellectual, gritty, underground research lab

Full color tables, the complete Nous Girl mascot specification with pose variants, typography roles, texture definitions, and art-style attributes live in [references/visual-system.md](references/visual-system.md); lane-specific prompt construction lives in [references/style-lanes.md](references/style-lanes.md).

## Available Scripts

| Script | Purpose | Invocation |
|---|---|---|
| `scripts/generate-with-ref.py` | Reference-image-driven generation: reads the active image provider from `~/.hermes/config.yaml`, uploads the reference via the provider's image-input endpoint (square-cropped), and saves the result as JSON with output path. Run it for any Method 4 generation where brand fidelity matters — it preserves the manga style that text-only prompts lose. Use `--dry-run` first to preview provider and parameters. | `python3 scripts/generate-with-ref.py --prompt "..." --reference assets/nous-girl-official-badge.png --aspect landscape --quality medium` |
| `scripts/postprocess.py` | Mandatory analog post-processing: applies grain/noise/scan-line modes (`standard`, `risograph`, `nous`, `imprint`) at a calibrated intensity. Run it as the final step on every generated image — raw AI output is never the deliverable. Load `references/post-processing.md` to pick mode and intensity. | `python3 scripts/postprocess.py input.png output.png --mode imprint --intensity 0.7` |

## Prerequisites

- Python 3 for both scripts; `postprocess.py` additionally needs an imaging backend (Pillow) available.
- For `generate-with-ref.py`: a configured Hermes image-generation provider in `~/.hermes/config.yaml` (or an explicit `--provider`) whose API accepts image inputs — text-only endpoints cannot do reference-driven generation.
- The bundled reference images in `assets/`, which serve as img2img anchors; pass one via `--reference`.
- An agent or client capable of image generation when working outside the scripts (per `compatibility`).

## Limitations

- This skill encodes one specific brand system — the palette, mascot rules, textures, and compliance checklist here are not general design guidance and must not be applied to other brands (see When not to use).
- The Nous Girl is not a logo substitute; official brand representation requires the wordmark/symbol, not generated mascot art.
- Generated imagery approximates the style even with references: always run the Brand Compliance Checklist before delivering, and consult `references/pitfalls.md` when output drifts (sad expressions, dark headphones, glossy rendering).
- Model/provider behavior changes over time — flag-specific details like endpoint names may drift from what the scripts assume; verify against your configured provider.
