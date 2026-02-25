---
name: blitzreels-carousels-tiktok
description: Create TikTok carousel projects (still slides + text overlays) via the BlitzReels API.
---

# BlitzReels Carousels (TikTok)

This skill is a convenience wrapper around `blitzreels-carousels` with TikTok defaults:

- `platform: "tiktok"`
- Recommended aspect ratio: `9:16`
- Safe area preset: `tiktok_9_16`

Use it when the user explicitly wants a TikTok photo-mode carousel.

## TikTok Platform-Specific Guidelines

### Danger Zones (Absolute Pixels @ 1080x1920)

**AVOID these areas:**
- **Right edge**: Rightmost 120px (share/like/comment/profile buttons)
- **Bottom**: Bottom 450px (username, caption, sound name, CTA button)
- **Top**: Top 80px (status bar, back button, camera/search icons)

### Safe Text Positioning

**Normalized Coordinates (0-1 scale):**
- **Top-center safe**: `position_x: 0.45, position_y: 0.18` (offset left to avoid right UI)
- **Middle-left safe**: `position_x: 0.35, position_y: 0.5` (body text)
- **Bottom safe (max)**: `position_x: 0.45, position_y: 0.65` (before caption zone)

**Best Practices:**
- Always offset text slightly left (`position_x: 0.45` instead of `0.5`)
- Use `position: "top"` preset for hook slides
- Keep text within center 70% of width (avoid left/right 15% edges)

### Caption & Hashtag Strategy

**Captions:**
- First 125 characters visible without "more" tap
- Lead with hook/question (don't repeat slide 1 text)
- Use emojis for visual breaks (max 3-4 per caption)

**Hashtags:**
- Mix broad (1M+ views) + niche (10K-100K views) + branded
- Example: `#entrepreneur #startuptips #businessgrowth #YourBrand`
- Place at end of caption or first comment

### Visual Consistency Patterns

**Color Palette:**
- High-contrast backgrounds (black, white, bold gradients)
- Consistent brand colors across all slides
- TikTok users prefer vibrant, eye-catching palettes

**Typography:**
- Bold sans-serif fonts (Montserrat Bold, Poppins Bold)
- 64-80px for titles, 48-56px for body
- Always enable 6px text stroke (black on white or vice versa)

**Slide Timing:**
- 3 seconds per slide (TikTok's photo mode default)
- Keep total carousel under 15 seconds (3-5 slides)

## Quickstart

```bash
export BLITZREELS_API_KEY="br_live_xxxxx"

bash scripts/tiktok.sh \
  --name "My TikTok Carousel" \
  --slide-duration 3 \
  --images "https://.../1.jpg|https://.../2.jpg|https://.../3.jpg" \
  --titles "Hook|Point|CTA"
```

## Full Workflow Example

**Goal**: Create a 3-slide TikTok carousel about productivity tips.

**Step 1: Prepare slide backgrounds** (use Canva, Figma, or AI generation)
- Slide 1: Bold gradient (red → purple)
- Slide 2: Minimalist white background
- Slide 3: Dark background with subtle pattern

**Step 2: Run script**
```bash
bash scripts/tiktok.sh \
  --name "Productivity Hacks Carousel" \
  --slide-duration 3 \
  --images "https://i.imgur.com/slide1.jpg|https://i.imgur.com/slide2.jpg|https://i.imgur.com/slide3.jpg" \
  --titles "5 Productivity Hacks\nThat Actually Work|1. Time blocking\n2. 2-minute rule\n3. Batch similar tasks|Save this & follow\nfor more tips 🚀"
```

**Step 3: Verify layout**
```bash
bash scripts/blitzreels.sh GET "/projects/${PROJECT_ID}/context?mode=timeline"
```

**Step 4: Export slideshow**
```bash
export BLITZREELS_ALLOW_EXPENSIVE=1
bash scripts/blitzreels.sh POST "/projects/${PROJECT_ID}/export" '{"resolution":"1080p","format":"mp4"}'
```

**Step 5: Upload to TikTok**
- Use TikTok's native photo mode upload
- Add caption: "Which one do you struggle with most? 👇"
- Add hashtags: `#productivity #productivitytips #worksmart #tiktokcarousel`
- Post at peak times (7-9 AM, 12-1 PM, 7-9 PM user's timezone)

