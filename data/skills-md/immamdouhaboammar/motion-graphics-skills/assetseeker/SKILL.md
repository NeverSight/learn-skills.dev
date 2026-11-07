---
name: assetseeker
description: Search free commercial-use creative assets across multiple online sources  -  photos, illustrations, icons, video footage, music, sound effects, and fonts. Use when the user needs to find assets for videos, PPTs, articles, or any content creation. Trigger on phrases like "find me a photo of", "search for icons", "I need background music", "find video footage", "search fonts", "找一张图片", "搜素材", "帮我找图标/视频/音乐/字体". Covers Pexels, Unsplash, Pixabay, Iconify, Freesound, Google Fonts and more  -  with API-backed search where available.
argument-hint: "[asset type] [keyword]"
author: Agents365-ai
category: Content Creation
version: 1.0.0
created: 2026-07-09
updated: 2026-07-09
homepage: https://github.com/Agents365-ai/365-skills
metadata: {"openclaw":{"requires":{"bins":["python3"],"env":["PEXELS_API_KEY"]},"primaryEnv":"PEXELS_API_KEY","emoji":"🔍"}}
---

# Asset Seeker  -  Online Creative Asset Search

## Overview

Search free commercial-use creative assets across the internet from curated, high-quality sources. Covers **photos, illustrations, icons, video footage, music, sound effects, and fonts**  -  all vetted for license safety (CC0 / free commercial use).

Backed by the research from the "创作者素材库大盘点" video  -  every source has been verified for license terms, China accessibility, and API availability.

## When to Use This Skill

Activate when the user needs to find online assets for content creation:

- "Find me a photo of mountains for a video thumbnail"
- "Search for laptop icons in outline style"
- "I need drone footage of city traffic for B-roll"
- "Find calm piano background music"
- "Search for a bold Chinese font for my title"
- "找一张科技感的图片" / "帮我搜个图标" / "有没有免费商用的视频素材"

Do NOT use for: local file search, video editing, or asset management tools (Eagle/Billfish).

## Supported Sources

### Photos

| Source | API | Free Tier | China Access | License |
| -------- | ----- | ----------- | ------------- | --------- |
| **Pexels** (default) | ✅ Photos + Videos | 200 req/hr, 20k/month | ✅ Direct | No attribution required |
| **Unsplash** | ✅ Photos | 50 req/hr (demo) | ✅ Direct | Attribution appreciated |
| **Pixabay** | ✅ Photos + Videos | Free | ✅ Direct | No attribution required |

### Illustrations & Vectors

| Source | API | Notes |
| -------- | ----- | ------- |
| **unDraw** | ❌ | One-click recolor, all free |
| **Storyset** | ❌ (Freepik API paid) | Editable characters + animations |
| **Humaaans / Open Doodles / Open Peeps** | ❌ | Direct download from site |

### Icons

| Source | API | Free Tier | Notes |
|--------|-----|-----------|-------|
| **Iconify** (default) | ✅ Open API | **No key needed** | 200+ icon sets, 300k+ icons |
| **Noun Project** | ✅ | 5,000/month free | Needs OAuth |

### Video Footage

| Source | API | Free Tier | China Access |
| -------- | ----- | ----------- | ------------- |
| **Pexels Video** (default) | ✅ | 200 req/hr, 20k/month | ✅ Direct |
| **Pixabay Video** | ✅ | Free | ✅ Direct |
| **Mixkit** | 🎭 Playwright scraper | Free, no attribution | ✅ Direct |
| **Coverr** | ✅ | Needs application | ✅ Direct |

### Music & Sound Effects

| Source | API | Notes |
| -------- | ----- | ------- |
| **Freesound** (default for SFX) | ✅ | OAuth, community-largest SFX library |
| **Pixabay Music** | ❌ Music API unavailable | Web download only, no attribution |
| **YouTube Audio Library** | ❌ | Manual, some need attribution |

### Fonts

| Source | API | Notes |
|--------|-----|-------|
| **Google Fonts** (default) | ✅ Metadata API | 1,500+ font families, OFL |
| **100font** | ❌ | Best CN free font directory |

## Workflow

### Step 1  -  Understand the request

Determine:

- **Asset type**: photo / icon / video / music / sfx / font / illustration
- **Keywords**: what the user is searching for
- **Style hints**: orientation, color, mood, style

If the type is ambiguous, ask briefly. Otherwise proceed.

### Step 2  -  Check API keys

Run the prerequisite check:

```bash
SKILL_DIR="${SKILL_DIR:-${CLAUDE_SKILL_DIR}}"
python3 "${SKILL_DIR}/scripts/seek_assets.py" sources
```

This lists all available sources and whether their API keys are configured. Without any API key, only **Iconify** (icons) will work  -  tell the user and suggest setting up at least `PEXELS_API_KEY` (free, most versatile).

### Step 3  -  Search

```bash
# Photo search (searches Pexels + Pixabay + Unsplash in parallel when keys are set)
python3 "${SKILL_DIR}/scripts/seek_assets.py" search photo "mountain sunset"

# Icon search (Iconify — always works, no key needed)
python3 "${SKILL_DIR}/scripts/seek_assets.py" search icon "laptop"

# Video search (via Pexels API)
python3 "${SKILL_DIR}/scripts/seek_assets.py" search video "city traffic"

# Video search (via Mixkit Playwright scraper — no API key needed)
python3 "${SKILL_DIR}/scripts/seek_assets.py" search video "sunset" --source mixkit

# Sound effect search
python3 "${SKILL_DIR}/scripts/seek_assets.py" search sfx "whoosh"

# Font search
python3 "${SKILL_DIR}/scripts/seek_assets.py" search font "bold sans-serif"

# Limit results
python3 "${SKILL_DIR}/scripts/seek_assets.py" search photo "cat" --max 10

# Filter by orientation
python3 "${SKILL_DIR}/scripts/seek_assets.py" search photo "landscape" --orientation landscape

# Human-readable output
python3 "${SKILL_DIR}/scripts/seek_assets.py" search icon "arrow" --format text
```

### Step 4  -  Present results

For each result, show:

- Thumbnail/preview URL (when available)
- Source name + license
- Download link or instructions
- Any attribution requirements

For **Iconify**, also show the icon set name and suggest usage (e.g., `<span class="iconify" data-icon="mdi:laptop">`).

### Step 5  -  Download (if needed)

```bash
python3 "${SKILL_DIR}/scripts/seek_assets.py" download <url> --output poster_bg.jpg
```

For sources without direct API download, open the page URL in browser or instruct the user to download manually.

## Commands

### search  -  Find assets

```bash
python3 seek_assets.py search <type> <keyword> [options]
```

Types: `photo`, `icon`, `video`, `music`, `sfx`, `font`

Options:

- `--max N`  -  Results per source (default: 10)
- `--source S`  -  Specific source (e.g., `--source pexels`, `--source iconify`)
- `--orientation landscape|portrait|square`  -  Photo/video orientation
- `--color red|orange|yellow|green|...`  -  Photo color filter (Pexels/Pixabay)
- `--format json|text`  -  Output format (default: json)

### sources  -  List available sources

```bash
python3 seek_assets.py sources
python3 seek_assets.py sources --type photo
```

Shows each source's status: API key configured, free tier limits, China accessibility.

### download  -  Download a single asset

```bash
python3 seek_assets.py download <url> --output <path>
```

## Environment Variables

```bash
# Photo & Video (get free key at pexels.com/api)
export PEXELS_API_KEY="your-pexels-api-key"

# Photo (get free key at unsplash.com/developers)
export UNSPLASH_ACCESS_KEY="your-unsplash-access-key"

# Photo & Video (get free key at pixabay.com/api/docs)
export PIXABAY_API_KEY="your-pixabay-api-key"

# Sound Effects (get key at freesound.org/apiv2/apply)
export FREESOUND_API_KEY="your-freesound-api-key"
# Optional: OAuth token for higher rate limits
export FREESOUND_TOKEN="your-oauth-token"

# Fonts (get key at console.cloud.google.com)
export GOOGLE_FONTS_API_KEY="your-google-fonts-api-key"

# Noun Project icons (get key at thenounproject.com/developers)
export NOUN_PROJECT_KEY="your-noun-project-key"
export NOUN_PROJECT_SECRET="your-noun-project-secret"
```

**Priority order**: At minimum, set `PEXELS_API_KEY` (free, covers photos + videos). Iconify works without any key.

### Get API Keys

| Service | Signup URL | Time to get key |
| --------- | ----------- | ---------------- |
| Pexels | <https://www.pexels.com/api/> | ~2 min |
| Unsplash | <https://unsplash.com/developers> | ~5 min (needs app registration) |
| Pixabay | <https://pixabay.com/api/docs/> | ~2 min |
| Freesound | <https://freesound.org/apiv2/apply/> | ~1 day (manual approval) |
| Google Fonts | <https://console.cloud.google.com/> | ~5 min |

## Requirements

```bash
# Core (stdlib, no pip needed for photos/icons/fonts)
pip install requests

# Optional: for Mixkit Playwright scraper
pip install playwright && python -m playwright install chromium
```

## Manual Sources (no API  -  agent provides direct guidance)

These sources are documented in the skill's knowledge base but have no programmatic API. When the user asks for these types, the agent provides curated recommendations with direct links:

- **Illustrations**: unDraw, Storyset, ManyPixels, DrawKit, IRA Design, Open Doodles
- **Video (no API)**: Mixkit, Coverr, Mazwai, Videvo
- **Music (no API)**: Pixabay Music, YouTube Audio Library, Freepd, Uppbeat
- **Fonts (no API)**: 100font (100font.com), 猫啃网 (maoken.com)
- **Emoji**: Fluent Emoji, Twemoji, OpenMoji, Noto Emoji
- **AI Tools**: remove.bg, Suno, 即梦, 可灵 Kling

When the user needs these, the agent should consult `references/asset_catalog.md` for the full curated list.

## References

- `references/asset_catalog.md`  -  Complete curated source catalog with URLs, licenses, China accessibility, and notes (extracted from the creator-assets research)

## Project Structure

```
assetseeker/
├── SKILL.md                   # This file (in skills/assetseeker/)
├── README.md                  # English README
├── README_CN.md               # Chinese README
├── references/
│   └── asset_catalog.md       # Full curated source catalog
└── skills/
    └── assetseeker/
        ├── SKILL.md
        ├── references/
        │   └── asset_catalog.md
        └── scripts/
            └── seek_assets.py # Main CLI
```

## Related Skills

- **video-podcast-maker**  -  Video production pipeline that consumes these assets
- **imagencn**  -  AI image generation when real photos don't fit the need
