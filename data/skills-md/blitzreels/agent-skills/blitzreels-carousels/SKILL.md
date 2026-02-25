---
name: blitzreels-carousels
description: Create TikTok/Instagram carousel projects (still slides + text overlays) via the BlitzReels API.
---

# BlitzReels Carousels (TikTok + Instagram)

This skill focuses on creating **still-slide carousel projects**: each slide is typically a full-screen image with text on top.

Key idea: model a carousel as a normal BlitzReels project, with:

- `project_type: "carousel"`
- Slide backgrounds uploaded as **image media assets**
- Slides laid out as **timeline media items** (one per slide segment)
- Text placed as **text overlays** aligned to each slide’s time window

## Important Limitations (Current Public API)

- The public OpenAPI spec currently does not expose a ZIP export of per-slide images. Treat carousels as a **slideshow video**: image-per-slide on the timeline + timed text overlays + `mp4` export.
- **Safe area presets are metadata only** — they don't auto-position text. You must manually set `position_x`/`position_y` (see Safe Area Positioning section below).

Always validate what's available via OpenAPI:

- `https://www.blitzreels.com/api/openapi.json`

## Platform Presets

### TikTok (Photo Mode)
- Aspect ratio: `9:16` ✅
- `safe_area_preset`: `tiktok_9_16` (metadata only — manual positioning required)

### Instagram Feed Carousel
- Aspect ratio: `4:5` ✅ (now supported as of 2026-02-12)
- `safe_area_preset`: `instagram_4_5` (metadata only — manual positioning required)

Instagram square is also common:
- Aspect ratio: `1:1` ✅
- `safe_area_preset`: `instagram_1_1` (metadata only — manual positioning required)

## Carousel Project Support

As of 2026-02-12, the public API now supports:
- ✅ `project_type: "carousel"` — creates a carousel-specific project
- ✅ `carousel_settings` (JSONB) — stores platform, safe area preset, slide count, etc.
- ✅ `aspect_ratio: "4:5"` — Instagram portrait format now supported

## Workflow (Manual Carousel Assembly)

1. Create a carousel project (`POST /projects`)
2. Upload slide background images (`POST /projects/{id}/media` with `url` or presigned upload)
3. Insert each image on the timeline (`POST /projects/{id}/timeline/media`) at `start_seconds = slideIndex * slideDuration`
4. Add text overlays for each slide (`POST /projects/{id}/text-overlays`) with matching `start_seconds` and `duration_seconds`
5. Fetch context to confirm layout (`GET /projects/{id}/context?mode=timeline`)
6. Export an `mp4` slideshow video (`POST /projects/{id}/export` with `format:"mp4"`)

## Workflow (One-Call Generation)

This repo includes `scripts/generate.sh` for an experimental one-call carousel generator, but it is not currently part of the public OpenAPI spec. Prefer the manual assembly flow above.

## Quickstart (Script)

This skill includes `scripts/carousel.sh` which creates a carousel project and inserts slide images + optional per-slide titles.

```bash
export BLITZREELS_API_KEY="br_live_xxxxx"
export BLITZREELS_ALLOW_EXPENSIVE=1  # only needed if you export a video preview

# TikTok: 3 slides (URLs) + titles
bash scripts/carousel.sh \
  --platform tiktok \
  --name "My TikTok Carousel" \
  --slide-duration 3 \
  --images "https://.../1.jpg|https://.../2.jpg|https://.../3.jpg" \
  --titles "Hook line|Main point|CTA"

# Instagram feed: 4:5
bash scripts/carousel.sh \
  --platform instagram \
  --aspect 4:5 \
  --name "My IG Carousel" \
  --images "https://.../1.jpg|https://.../2.jpg"
```

## API Endpoints Used

| Method | Path | Purpose |
|--------|------|---------|
| POST | `/projects` | Create a project (carousel fields may be ignored if not supported) |
| POST | `/projects/{id}/media` | Upload/import slide background images |
| POST | `/projects/{id}/timeline/media` | Insert images into the timeline (one segment per slide) |
| POST | `/projects/{id}/text-overlays` | Add slide text overlays (time-windowed) |
| GET | `/projects/{id}/context?mode=timeline` | Inspect timing + overlay placement |
| POST | `/projects/{id}/export` | Export slideshow `mp4` (expensive) |

## Export Slideshow (MP4)

```bash
export BLITZREELS_ALLOW_EXPENSIVE=1

# Slideshow video
bash scripts/blitzreels.sh POST "/projects/${PROJECT_ID}/export" '{"resolution":"1080p","format":"mp4"}'
```

## Marketing Slide Structure

Carousels perform best when structured for social media consumption:

**3-Slide Formula (TikTok):**
1. **Hook (Slide 1)**: Attention-grabbing statement or question (e.g., "3 Mistakes Killing Your Startup")
2. **Value (Slide 2)**: Core insight or key points
3. **CTA (Slide 3)**: Clear next step (e.g., "Save This Post" / "Follow for More")

**5-Slide Formula (Instagram Feed):**
1. **Hook**: Compelling title/question
2-4. **Key Points**: 3 actionable insights (one per slide)
5. **CTA + Recap**: Summary + follow/save/comment prompt

**Template Patterns:**
- Educational: "How to [X]" → Steps 1-3 → Recap
- Listicle: "[N] Ways to [X]" → Point 1 → Point 2 → Point 3 → Summary
- Storytelling: Problem → Struggle → Solution → Result → CTA

## Readability Rules (CRITICAL)

**Character & Line Limits:**
- **Max 40 chars/line** (mobile readable at thumb-scrolling speed)
- **Max 4 lines/slide** (avoid visual clutter)
- Break long text into multiple slides rather than cramming

**Contrast & Legibility:**
- **WCAG AA minimum**: 4.5:1 contrast ratio (text vs background)
- **Always enable text stroke**: 6px black stroke on white text (or vice versa)
- Use web contrast checkers: [WebAIM Contrast Checker](https://webaim.org/resources/contrastchecker/)

**Font Sizing:**
- **Titles**: 64-80px (hook slides, CTAs)
- **Body text**: 48-64px (key points)
- **Minimum**: 48px (anything smaller risks illegibility on mobile)

**Typography Best Practices:**
- Bold fonts (700+ weight) for better mobile readability
- Center-aligned text for carousels (easier to scan)
- Sans-serif fonts (Inter, Montserrat, Poppins) over serif

## Safe Area Positioning (Platform-Specific)

The API supports `carousel_settings.safe_area_preset`, but you must manually position text to respect UI danger zones.

### TikTok Photo Mode (`9:16`)

**Danger Zones (Absolute Pixels @ 1080x1920):**
- **Right edge**: Avoid rightmost 120px (share/like/comment buttons)
- **Bottom**: Avoid bottom 450px (username, caption overlay, sound)
- **Top**: Avoid top 80px (status bar, back button)

**Safe Positioning (Normalized Coords):**
- **Top-center safe**: `position_x: 0.5, position_y: 0.18` (hook slides)
- **Middle-left safe**: `position_x: 0.35, position_y: 0.5` (body text, avoids right UI)
- **Bottom safe**: `position_x: 0.5, position_y: 0.65` (max safe before captions)

**TikTok Best Practices:**
- Always offset text slightly left (`position_x: 0.45` instead of `0.5`) to avoid right-side buttons
- Use `position: "top"` preset for simplicity
- Test with TikTok watermark/UI overlay in mind

### Instagram Feed Carousel (`4:5` or `1:1`)

**Danger Zones (Absolute Pixels @ 1080x1350 for 4:5):**
- **Bottom**: Avoid bottom 420px (username, caption preview, action buttons)
- **Edges**: Keep text 80px from all edges (safe margins)

**Safe Positioning (Normalized Coords):**
- **Top-center safe**: `position_x: 0.5, position_y: 0.15` (titles)
- **Middle-center safe**: `position_x: 0.5, position_y: 0.45` (body text)
- **Bottom safe (max)**: `position_x: 0.5, position_y: 0.6` (before caption zone)

**Instagram Best Practices:**
- Center all text (Instagram's feed is symmetrical)
- Use consistent vertical positioning across all slides (e.g., always `position_y: 0.18`)
- Leave generous bottom margin (users expect captions below)

### Square Format (`1:1`)

**Danger Zones (Absolute Pixels @ 1080x1080):**
- **Bottom**: Avoid bottom 380px (captions, profile link)
- **Edges**: 80px margins on all sides

**Safe Positioning:**
- **Top-center**: `position_x: 0.5, position_y: 0.15`
- **Middle-center**: `position_x: 0.5, position_y: 0.5`

## Text Overlay Mandate (CRITICAL)

**ALWAYS use `POST /projects/{id}/text-overlays` for carousel text.**

**NEVER use motion graphics or motion code for slide text** — those tools are for:
- Animated lower thirds (video editing)
- Dynamic charts/graphs
- Complex multi-layer compositions

**Why text overlays for carousels:**
- Optimized for static text rendering
- Direct control over positioning, stroke, alignment
- No unnecessary animation overhead
- Consistent with per-slide timing model

**API Call Pattern:**
```bash
bash scripts/blitzreels.sh POST "/projects/${PROJECT_ID}/text-overlays" '{
  "text": "Your slide text here\nMax 40 chars/line",
  "start_seconds": 0,
  "duration_seconds": 3,
  "position_x": 0.5,
  "position_y": 0.18,
  "style": {
    "font_size": 64,
    "font_weight": "700",
    "text_align": "center",
    "color": "#ffffff",
    "text_stroke_enabled": true,
    "text_stroke_color": "#000000",
    "text_stroke_width_px": 6
  }
}'
```

## Complete Examples

### Example 1: TikTok Entrepreneurship Carousel (3 Slides)

**Topic**: "3 Mistakes Killing Your Startup"

**Slide 1 (Hook):**
- Text: "3 Mistakes Killing\nYour Startup"
- Duration: 3s
- Position: `position_x: 0.45, position_y: 0.18` (top-left-of-center)
- Style: 72px, bold, white text, 6px black stroke

**Slide 2 (Value):**
- Text: "1. Building without users\n2. Ignoring metrics\n3. Perfectionism"
- Duration: 3s
- Position: `position_x: 0.35, position_y: 0.5`
- Style: 56px, bold

**Slide 3 (CTA):**
- Text: "Save this for later ↓\nFollow for more tips"
- Duration: 3s
- Position: `position_x: 0.45, position_y: 0.18`
- Style: 64px, bold

**Script:**
```bash
bash scripts/tiktok.sh \
  --name "Startup Mistakes Carousel" \
  --slide-duration 3 \
  --images "https://example.com/slide1.jpg|https://example.com/slide2.jpg|https://example.com/slide3.jpg" \
  --titles "3 Mistakes Killing\nYour Startup|1. Building without users\n2. Ignoring metrics\n3. Perfectionism|Save this for later ↓\nFollow for more tips"
```

### Example 2: Instagram Educational Carousel (5 Slides)

**Topic**: "How Photosynthesis Works"

**Slide 1 (Hook):**
- Text: "How Photosynthesis\nWorks (Explained)"
- Position: `position_x: 0.5, position_y: 0.15` (top-center)

**Slides 2-4 (Steps):**
- Slide 2: "Step 1: Light Absorption\nChloroplasts capture sunlight"
- Slide 3: "Step 2: Water Splitting\nH2O breaks into H + O2"
- Slide 4: "Step 3: Sugar Formation\nCO2 + H → Glucose"

**Slide 5 (Recap):**
- Text: "Light → Water → Sugar\nSave for biology class!"

**Script:**
```bash
bash scripts/instagram.sh \
  --aspect 4:5 \
  --name "Photosynthesis Explained" \
  --slide-duration 3 \
  --images "url1|url2|url3|url4|url5" \
  --titles "How Photosynthesis\nWorks (Explained)|Step 1: Light Absorption\nChloroplasts capture sunlight|Step 2: Water Splitting\nH2O breaks into H + O2|Step 3: Sugar Formation\nCO2 + H → Glucose|Light → Water → Sugar\nSave for biology class!"
```

## API Validation & Drift Prevention

Before starting carousel work, validate that required endpoints exist:

```bash
# Validate API endpoints
bash scripts/validate-api.sh
```

**Required Endpoints:**
- `POST /projects` (carousel project creation)
- `POST /projects/{id}/media` (slide background upload)
- `POST /projects/{id}/timeline/media` (slide sequencing)
- `POST /projects/{id}/text-overlays` (text placement)
- `GET /projects/{id}/context` (layout inspection)
- `POST /projects/{id}/export` (mp4 slideshow export)

**OpenAPI Spec Reference:**
- Live spec: `https://www.blitzreels.com/api/openapi.json`
- Always check spec before assuming endpoint availability

## Safe Area Guidance (Practical)

The API supports `carousel_settings.safe_area_preset`, but the preset is **metadata** today.
To "respect safe areas" in practice:

- Keep critical text away from the extreme edges.
- On TikTok, avoid the **right side** (UI buttons) and the **bottom** (captions/CTA overlays).
- Prefer using `position: "top"` or `position: "center"` for text overlays, or set normalized `position_x`/`position_y` (0..1) conservatively.
