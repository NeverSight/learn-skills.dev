---
name: marketing-design
description: "Marketing brand-asset generation (raster images via AI): logo design (55 styles, 30 palettes, 25 industries), corporate identity / CIP mockups (50 deliverables - business card, letterhead, signage, packaging, apparel), banner design (22 styles, social/ads/web/print), SVG icon design (15 styles), social photos (multi-platform), and model-agnostic poster prompts. Default image engine is Codex gpt-image-2 (ChatGPT subscription via `codex login`), attaching the brand logo as a reference image for CIP compositing; falls back to Gemini Nano Banana (GEMINI_API_KEY, same key as omnimedia). Actions: design logo, create CIP / brand identity, generate mockups, design banner, generate icon, create social photos, design poster, social media images. Platforms: Facebook, Twitter, LinkedIn, YouTube, Instagram, Pinterest, TikTok, Threads, Google Ads. For HTML/web pages, dashboards, and slide decks, use opendesign instead."
argument-hint: "[design-type] [context]"
license: MIT
metadata:
  author: vanducng
  version: "1.1.0"
---

# Marketing Design

Unified marketing brand-asset skill: logo, CIP, banners, SVG icons, social photos, posters. Generates **raster images** - default engine is **Codex gpt-image-2** (ChatGPT subscription, `codex login`), falling back to **Gemini Nano Banana** (`GEMINI_API_KEY`, the same key `omnimedia` uses). For HTML/web artifacts and slide decks, use `opendesign`.

## Sub-skill Routing

All built-in modules are self-contained (references + scripts + data in this skill). Route HTML artifacts and frontend implementation to the installed repo skills listed below.

| Task | Sub-skill | Details |
|------|-----------|---------|
| Static HTML artifacts, decks, presentations | `vd:opendesign` | Self-contained HTML/CSS artifacts |
| Frontend UI, tokens, shadcn/Tailwind code | `vd:uiuxdesign` | App UI design/build/review/test |
| Full-stack FastAPI + React apps | `vd:fastreact` | Mockup-first app scaffolding |
| Logo creation, AI generation | Logo (built-in) | `references/logo-design.md` |
| CIP mockups, deliverables | CIP (built-in) | `references/cip-design.md` |
| Banners, covers, headers | Banner (built-in) | `references/banner-sizes-and-styles.md` |
| Social media images/photos | Social Photos (built-in) | `references/social-photos-design.md` |
| SVG icons, icon sets | Icon (built-in) | `references/icon-design.md` |
| Posters (event, editorial, marketing) | Poster (built-in) | `references/poster-design.md` |

## Image Generation Backend

Raster generators (`logo`, `cip`) default to **Codex `$imagegen` (gpt-image-2)** on the ChatGPT subscription - no API key. One-time setup: `brew install codex && codex login`. If Codex is unavailable (not installed / not logged in / quota), they **fall back to Gemini** automatically (`export GEMINI_API_KEY=...` from https://aistudio.google.com/apikey, `pip install google-genai pillow`).

| Generator | Default engine | Reference image | Force Gemini | Notes |
|-----------|----------------|-----------------|--------------|-------|
| `logo` | Codex gpt-image-2 | - | `--provider gemini` | `--batch` always uses Gemini (Codex = one image/turn) |
| `cip` | Codex gpt-image-2 | brand logo via `--logo` (attached as `-i` reference) | `--provider gemini` | large `--set` faster on Gemini |
| `icon` | Gemini (SVG **code**, not raster) | - | n/a | Codex can't emit SVG markup |
| `poster` | model-agnostic prompt emitter | - | n/a | prints a prompt for any image model |
| `banner` / social photos | HTML→screenshot | - | n/a | not direct AI image gen |

`--provider`: `codex` (default) · `gemini` (force Nano Banana) · `auto` (codex→gemini). Codex takes 5-30s/image. Reference-image compositing requires codex-cli ≥ 0.137.

## Resolve Paths (run once)

Resolve the skill dir and a Python interpreter once, then reuse `$SKILL` / `$PY` in every command below (works under Claude Code, Codex, or a dev clone).

```bash
SKILL="${CLAUDE_SKILL_DIR:-$(for d in "$HOME/skills/skills/marketing-design" "$HOME/.claude/skills/marketing-design" "$HOME/.agents/skills/marketing-design"; do [ -d "$d" ] && { echo "$d"; break; }; done)}"
PY="$([ -x "$HOME/.claude/skills/.venv/bin/python3" ] && echo "$HOME/.claude/skills/.venv/bin/python3" || echo python3)"
```

## Logo Design (Built-in)

55+ styles, 30 color palettes, 25 industry guides. Default engine: **Codex gpt-image-2** (Gemini fallback).

```bash
# Design brief (start here), then search styles/colors/industries as needed
python3 $SKILL/scripts/logo/search.py "tech startup modern" --design-brief -p "BrandName"
python3 $SKILL/scripts/logo/search.py "minimalist clean" --domain style
python3 $SKILL/scripts/logo/search.py "tech professional" --domain color
python3 $SKILL/scripts/logo/search.py "healthcare medical" --domain industry

# Generate (ALWAYS output logo images with white background)
python3 $SKILL/scripts/logo/generate.py --brand "TechFlow" --style minimalist --industry tech
python3 $SKILL/scripts/logo/generate.py --prompt "coffee shop vintage badge" --style vintage

# Force Gemini Nano Banana (aspect-ratio control, --pro, or variant batch)
python3 $SKILL/scripts/logo/generate.py --brand "TechFlow" --provider gemini --pro
python3 $SKILL/scripts/logo/generate.py --brand "TechFlow" --batch 9 --output-dir ./logos
```

**IMPORTANT:** When scripts fail, try to fix them directly.

After generation, ask whether the user wants an HTML preview gallery. If yes, use `vd:opendesign` for a static gallery artifact.

## CIP Design (Built-in)

50+ deliverables, 20 styles, 20 industries. Default engine: **Codex gpt-image-2** with the brand logo attached as a reference image (`-i`); Gemini Nano Banana fallback (`--model flash` = `gemini-2.5-flash-image`, `--model pro` = `gemini-3-pro-image-preview`).

```bash
# CIP brief (start here)
python3 $SKILL/scripts/cip/search.py "tech startup" --cip-brief -b "BrandName"
python3 $SKILL/scripts/cip/search.py "business card letterhead" --domain deliverable
python3 $SKILL/scripts/cip/search.py "luxury premium elegant" --domain style
python3 $SKILL/scripts/cip/search.py "office reception" --domain mockup

# Mockups (with logo is RECOMMENDED; generate the logo first if none exists)
python3 $SKILL/scripts/cip/generate.py --brand "TopGroup" --logo /path/to/logo.png --deliverable "business card" --industry "consulting"
python3 $SKILL/scripts/cip/generate.py --brand "TopGroup" --logo /path/to/logo.png --industry "consulting" --set
python3 $SKILL/scripts/cip/generate.py --brand "TopGroup" --logo logo.png --deliverable "business card" --model pro
python3 $SKILL/scripts/cip/generate.py --brand "TechFlow" --deliverable "business card" --no-logo-prompt
python3 $SKILL/scripts/cip/generate.py --brand "TopGroup" --logo logo.png --industry "consulting" --set --provider gemini

# HTML presentation from generated mockups
python3 $SKILL/scripts/cip/render-html.py --brand "TopGroup" --industry "consulting" --images /path/to/cip-output
```

## Banner Design (Built-in)

22 art direction styles across social, ads, web, print. Uses the built-in banner reference, this skill's raster generation flow when imagery is needed, and browser/Playwright screenshots for exact-pixel export. Load `references/banner-sizes-and-styles.md` for the complete sizes and styles reference.

Workflow: gather requirements (purpose, platform, content, brand, style, quantity) → research visual references only when the brief lacks direction → design HTML/CSS variants (raster visuals via this skill's image flow when needed) → export via Browser/Playwright/Chrome screenshot at exact dimensions → present options side-by-side and iterate.

### Banner: Quick Size Reference

| Platform | Type | Size (px) |
|----------|------|-----------|
| Facebook | Cover | 820 x 312 |
| Twitter/X | Header | 1500 x 500 |
| LinkedIn | Personal | 1584 x 396 |
| YouTube | Channel art | 2560 x 1440 |
| Instagram | Story | 1080 x 1920 |
| Instagram | Post | 1080 x 1080 |
| Google Ads | Med Rectangle | 300 x 250 |
| Website | Hero | 1920 x 600-1080 |

### Banner: Design Rules

- Safe zones: critical content in central 70-80%
- One CTA per banner, bottom-right, min 44px height
- Max 2 fonts, min 16px body, ≥32px headline
- Text under 20% for ads (Meta penalizes)
- Print: 300 DPI, CMYK, 3-5mm bleed

## Icon Design (Built-in)

15 styles, 12 categories. Gemini 3.1 Pro Preview generates SVG text output (`--list-styles` on the script lists every style).

```bash
python3 $SKILL/scripts/icon/generate.py --prompt "settings gear" --style outlined
python3 $SKILL/scripts/icon/generate.py --prompt "shopping cart" --style filled --color "#6366F1"
python3 $SKILL/scripts/icon/generate.py --name "dashboard" --category navigation --style duotone
python3 $SKILL/scripts/icon/generate.py --prompt "cloud upload" --batch 4 --output-dir ./icons
python3 $SKILL/scripts/icon/generate.py --prompt "user profile" --sizes "16,24,32,48" --output-dir ./icons
```

**Model:** `gemini-3.1-pro-preview` - text-only output (SVG is XML text). No image generation API needed.

## Poster Design (Built-in)

20-30 curated styles × 15-20 palettes × 10-14 layouts × 8-12 textures. Model-agnostic - emits text prompts only. Use any image model (Gemini Nano Banana 2, GPT Image, Imagen, Midjourney).

Three axes (style, palette, texture) locked per call to preserve identity; layout + variation seed randomized to guarantee per-call variety. 5 calls with same `--style` → 5 visibly distinct posters that read as one series.

Load `references/poster-design.md` for the full guide and `references/poster-prompt-engineering.md` for prompt anatomy + model-specific tweaks.

```bash
$PY $SKILL/scripts/poster/search.py --domain style --query "swiss editorial"
$PY $SKILL/scripts/poster/search.py --poster-brief --topic "AI Conference" --query "minimal grid"

$PY $SKILL/scripts/poster/generate.py --topic "AI Conference"
$PY $SKILL/scripts/poster/generate.py --topic "AI Conference" --style "Swiss Editorial Grid" --seed 42
```

Pipe stdout into any image-gen model. For series: same `--style`, different `--seed` values (lock identity, vary composition).

### Poster: Rebuild Knowledge Base

```bash
# Vision analysis (resume-safe; needs GEMINI_API_KEY)
$PY $SKILL/scripts/poster/analyze.py --input-dir /path/to/posters
# Re-cluster + regenerate CSVs
$PY $SKILL/scripts/poster/cluster.py
```

## Social Photos (Built-in)

Multi-platform social image design: HTML/CSS → screenshot export. Uses built-in social templates, brand context from the brief, and Browser/Playwright screenshots. Load `references/social-photos-design.md` for sizes, templates, best practices.

Workflow: parse prompt (subject, platforms, style, brand context) → ideate 3-5 concepts and present concise options → design with brand tokens from the brief, HTML per idea × size → export via Browser or Playwright screenshot at exact px (2x deviceScaleFactor) → visually verify exports, fix layout/styling issues, re-export → report to the injected `Reports:` path and sort outputs under the chosen artifact directory.

### Social Photos: Key Sizes

| Platform | Size (px) | Platform | Size (px) |
|----------|-----------|----------|-----------|
| IG Post | 1080×1080 | FB Post | 1200×630 |
| IG Story | 1080×1920 | X Post | 1200×675 |
| IG Carousel | 1080×1350 | LinkedIn | 1200×627 |
| YT Thumb | 1280×720 | Pinterest | 1000×1500 |

## Workflows

### Complete Brand Package

1. **Logo** → `scripts/logo/generate.py` → Generate logo variants
2. **CIP** → `scripts/cip/generate.py --logo ...` → Create deliverable mockups
3. **Presentation** → use `opendesign` to build the pitch deck (HTML)

### New Design System

1. **Brand assets** (this skill) → Define visual direction and generate marks/mockups
2. **HTML artifact** (`vd:opendesign`) → Explore page/deck direction
3. **Implement** (`vd:uiuxdesign`) → Configure Tailwind, shadcn/ui, and frontend screens
