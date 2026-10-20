---
name: thumbnail-design
description: >
  YouTube thumbnails, video/podcast/course covers, blog headers, and Open Graph (link-preview)
  images via Gemini 3.1 Flash image generation (default) or HTML/CSS. Optimized for high
  contrast, small-size readability, and click-through rate. Use when the image represents a
  video, episode, or article; for feed posts use social-media-graphic, for paid ads use
  ad-creative-design.
  Trigger phrases: "design a thumbnail", "YouTube thumbnail", "video thumbnail",
  "article header image", "OG image", "create a thumbnail", "blog header",
  "video cover image".
license: MIT
---

# Thumbnail Design

Create high-impact thumbnails optimized for clicks and readability at small sizes. Covers YouTube thumbnails, article headers, OG images, and video covers.

---

## Step 1: Load Design Context

1. Read `.agents/design-context.md` first -- brand colors (hex), fonts, style archetype
2. If missing, use the `design-context` Default Fallbacks and tell the user defaults were used
3. Thumbnails prioritize readability and impact over strict brand guidelines -- but brand colors create channel recognition

---

## Gemini Image Generation Path

Pipeline/CLI: `image-generation`. Prompt craft, cropping, and text-overlay fallback: `graphic-design` Step 3.

1. Generate at the Gemini ratio in the Step 2 table; crop with `--resize WxH` (e.g. `--aspect-ratio 16:9 --resize 1280x720`)
2. Real people: pass their photo with `--image` and say "keep this person's face and identity unchanged". Don't invent likenesses of real people
3. Read the output PNG, then check it shrunk: `python -c "from PIL import Image; Image.open('thumb.png').resize((168,94), Image.LANCZOS).save('thumb_small.png')"` and Read `thumb_small.png`. Text must still be readable and the face expression visible. Fix one issue per follow-up turn

### Example Prompts

- **YouTube Thumbnail:** "Create a YouTube thumbnail (16:9). [subject] on the left side with [expression/pose]. Bold text '[title]' in [color] with dark outline on the right. [background style]. High contrast, readable at small size."
- **Article Header:** "Create a landscape article header image. Abstract [color palette] gradient background. Title '[headline]' in bold white sans-serif, centered. Subtle geometric shapes. Clean, editorial feel."
- **OG Image:** "Create a landscape Open Graph image for [brand/site]. Keep all text inside the central 80%. Logo top-left, title '[text]' large and centered, tagline below in lighter weight. [brand color] gradient background. Professional, shareable."

---

## Step 2: Identify Format and Dimensions

| Format | Dimensions | Aspect Ratio | Gemini ratio | Notes |
|--------|-----------|--------------|--------------|-------|
| YouTube Thumbnail | 1280 x 720 | 16:9 | 16:9 | Min 640px wide; JPG/PNG under 2 MB; must read at 168x94 |
| YouTube Shorts Cover | 1080 x 1920 | 9:16 | 9:16 | Shelf shows a center crop -- keep text mid-frame |
| Article Header / Hero | 1200 x 630 | 1.91:1 | 16:9 + crop | Blog post header |
| OG Image (Open Graph) | 1200 x 630 | 1.91:1 | 16:9 + crop | Link previews on FB, LinkedIn, Slack, X |
| X large-image card | 1200 x 628 | ~1.91:1 | 16:9 + crop | X can crop toward 2:1 -- keep margins |
| Podcast Cover | 3000 x 3000 | 1:1 | 1:1 (4K) | Apple: 1400-3000px square, JPG/PNG, RGB |
| Course Thumbnail | 1280 x 720 (Udemy min 750 x 422) | 16:9 | 16:9 | Udemy, Skillshare |
| Vimeo Thumbnail | 1280 x 720 | 16:9 | 16:9 | Same as YouTube |

---

## Step 3: Thumbnail Composition Principles

### The 3-Second Rule
A thumbnail must communicate its message in under 3 seconds. If someone cannot understand the topic at a glance, the thumbnail fails.

### Readability at Small Sizes
YouTube thumbnails display as small as 168x94 pixels in the sidebar. Test every design mentally at that size.

Rules:
- Maximum 5-7 words of text
- Font size minimum: 60px at 1280x720 (equivalent to ~8px at sidebar size)
- No thin fonts -- use bold or black weights only
- High contrast between text and background (always)
- No small details that vanish at reduced size

### The Three-Element Maximum
The best thumbnails have at most 3 visual elements:
1. A face or focal image
2. Bold text (2-5 words)
3. A supporting visual element (icon, arrow, emoji, product)

More than 3 elements creates clutter.

---

## Step 4: Click-Worthy Composition Frameworks

### Curiosity Gap
Show enough to intrigue but not enough to satisfy. The viewer must click to learn more.

```
Layout:
- Left side: Expressive face (surprise, shock, excitement)
- Right side: Bold text with ONE missing piece
- Example: "I tried [PRODUCT] for 30 days..." with shocked face
- Use "?" or "..." to create open loops
```

### Before / After
Show transformation. The contrast drives clicks.

```css
.before-after {
  display: grid;
  grid-template-columns: 1fr 1fr;
  height: 100%;
}
.before {
  background: #E5E7EB; /* muted, desaturated */
  filter: grayscale(30%);
  display: flex;
  align-items: center;
  justify-content: center;
}
.after {
  background: linear-gradient(135deg, var(--primary), var(--accent));
  display: flex;
  align-items: center;
  justify-content: center;
}
.divider-arrow {
  position: absolute;
  left: 50%;
  top: 50%;
  transform: translate(-50%, -50%);
  font-size: 64px;
  z-index: 10;
  /* Large arrow pointing right: → */
}
```

### Numbers / Lists
Numbers grab attention. "7 Tips", "$10K", "100 Days".

```
Layout:
- Giant number: 120-200px, bold, gradient or accent color
- Supporting text: 36-48px next to or below number
- Background: clean gradient, not busy
- Optional icon related to the topic
```

### Reaction / Emotion
Human faces expressing emotion are the highest-performing thumbnail element.

```
Layout:
- Face/headshot: 60% of frame, positioned left or right
- Expressive emotion: surprise, excitement, disbelief, joy
- 2-3 words of text on the opposite side
- Colored border or glow behind the face to separate from background
```

### Versus / Comparison
Two things side by side with "VS" in the middle.

```css
.versus {
  display: grid;
  grid-template-columns: 1fr auto 1fr;
  align-items: center;
  height: 100%;
}
.vs-badge {
  font-size: 72px;
  font-weight: 900;
  color: var(--accent);
  text-shadow: 0 0 30px rgba(var(--accent-rgb), 0.5);
  z-index: 2;
}
.side-a { background: linear-gradient(135deg, #1a1a2e, #16213e); }
.side-b { background: linear-gradient(135deg, #2d1b00, #462300); }
```

---

## Step 5: Text Treatment for Thumbnails

### Maximum Impact Text

```css
/* Primary thumbnail text */
.thumb-text {
  font-family: 'Inter', 'Arial Black', sans-serif;
  font-size: 80px;
  font-weight: 900;
  color: #FFFFFF;
  text-transform: uppercase;
  line-height: 0.95;
  letter-spacing: -0.02em;

  /* Always add stroke + shadow for readability over any background */
  -webkit-text-stroke: 3px rgba(0, 0, 0, 0.8);
  paint-order: stroke fill;
  text-shadow:
    4px 4px 0 rgba(0, 0, 0, 0.9),
    0 0 20px rgba(0, 0, 0, 0.5);
}

/* Accent word highlight */
.thumb-text .highlight {
  color: var(--accent);
  -webkit-text-stroke-color: rgba(0, 0, 0, 0.9);
}
```

### Text Background Techniques

```css
/* Solid pill behind text */
.text-pill {
  display: inline-block;
  background: var(--primary);
  padding: 8px 24px;
  border-radius: 8px;
  font-weight: 800;
  font-size: 48px;
}

/* Angled highlight bar */
.text-bar {
  display: inline-block;
  background: var(--accent);
  padding: 8px 20px;
  transform: skewX(-5deg);
}
.text-bar span {
  display: inline-block;
  transform: skewX(5deg); /* counter-skew for straight text */
}

/* Blurred backdrop */
.text-backdrop {
  background: rgba(0, 0, 0, 0.6);
  backdrop-filter: blur(8px);
  padding: 12px 24px;
  border-radius: 8px;
}
```

---

## Step 6: Face and Emotion Techniques

### Face Cutout with Glow
```css
.face-container {
  position: relative;
  z-index: 2;
}
.face-container img {
  /* Remove background in advance or use object-fit */
  height: 100%;
  object-fit: contain;
  object-position: bottom;
  filter: drop-shadow(0 0 30px rgba(var(--primary-rgb), 0.6));
}
/* Glow ring behind face */
.face-container::before {
  content: '';
  position: absolute;
  width: 80%;
  height: 80%;
  top: 10%;
  left: 10%;
  border-radius: 50%;
  background: radial-gradient(circle, rgba(var(--primary-rgb), 0.4), transparent 70%);
  z-index: -1;
}
```

### Emoji Accents (When No Face Available)
Use oversized emojis as visual anchors when no photo is available:

```css
.emoji-accent {
  font-size: 120px;
  position: absolute;
  /* Slight rotation adds energy */
  transform: rotate(-10deg);
  filter: drop-shadow(4px 4px 0 rgba(0,0,0,0.3));
}
```

---

## Step 7: Color Psychology for Thumbnails

| Color | Association | Best For |
|-------|-------------|----------|
| **Red** (#EF4444) | Urgency, excitement, danger | Breaking news, warnings, hot takes |
| **Yellow** (#EAB308) | Attention, optimism, energy | Tips, positive content, highlights |
| **Blue** (#3B82F6) | Trust, calm, professionalism | Tutorials, educational, tech |
| **Green** (#22C55E) | Growth, success, money | Finance, results, positive outcomes |
| **Orange** (#F97316) | Energy, creativity, warmth | Creative content, DIY, food |
| **Purple** (#8B5CF6) | Premium, mystery, wisdom | Luxury, deep dives, advanced topics |
| **Black** (#000000) | Power, elegance, sophistication | Dramatic reveals, premium content |
| **White** (#FFFFFF) | Clean, minimal, modern | Minimalist channels, Apple-style |

### Contrast Pairings That Pop
- Yellow text on dark blue background
- White text on deep red or purple
- Black text on bright yellow
- Cyan accent on dark background
- Red accent on dark gray/charcoal

---

## Step 8: YouTube-Specific Optimization

### Sidebar Readability Test
The thumbnail will appear at roughly 168x94px in the sidebar. At this size:
- Only bold, high-contrast text is readable
- Faces must be large enough to show expression
- Details vanish -- keep it simple
- The overall color scheme must be distinct from surrounding thumbnails

### Overlay Zones
YouTube overlays the video duration in the bottom-right corner (dark pill with white text), a red watch-progress bar along the bottom edge for watched videos, and hover icons (Watch Later, Add to queue) in the top-right. Keep critical content out of all three.

```css
/* Duration overlay safe zone */
.youtube-safe {
  /* Avoid content in this area */
  position: absolute;
  bottom: 0;
  right: 0;
  width: 120px;
  height: 40px;
  /* This zone is covered by YouTube's duration badge */
}
```

### Channel Consistency
Create a thumbnail system with recurring elements:
- Consistent background color or gradient per series
- Same font treatment across all thumbnails
- Recurring layout structure (face left + text right, or vice versa)
- Brand color as a signature element (colored border, text highlight)

---

## Step 9: Article Header / OG Image Design

### OG Image Requirements
- Dimensions: 1200 x 630 (recommended by most platforms); declare them with `og:image:width` / `og:image:height` meta tags
- File size: under 1MB for fast loading (platform caps are higher, e.g. 5-8MB)
- Use an absolute HTTPS URL in `og:image`; add `twitter:card` = `summary_large_image` for X
- Text: readable when scaled to ~600x315 (half size in some feeds)
- Avoid text in the outer 10% margins (may be cropped)

### Article Header Layout
```css
.article-header {
  width: 1200px;
  height: 630px;
  position: relative;
  display: flex;
  align-items: center;
  padding: 60px 80px;
  background: linear-gradient(135deg, #0F172A, #1E293B);
  overflow: hidden;
}

.article-header .title {
  font-family: var(--font-heading);
  font-size: 56px;
  font-weight: 800;
  color: #F8FAFC;
  line-height: 1.15;
  max-width: 700px;
  text-wrap: balance;
}

.article-header .meta {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-top: 24px;
  font-size: 18px;
  color: rgba(248, 250, 252, 0.7);
}

.article-header .brand {
  position: absolute;
  bottom: 40px;
  right: 60px;
  font-size: 20px;
  font-weight: 700;
  color: var(--primary);
}

/* Decorative accent */
.article-header::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 6px;
  background: linear-gradient(90deg, var(--primary), var(--accent));
}
```

---

## Step 10: Output and Export

Generate as self-contained HTML with fixed dimensions:

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@700;800;900&display=swap" rel="stylesheet">
  <style>
    body { margin: 0; padding: 0; display: flex; justify-content: center; align-items: center;
           min-height: 100vh; background: #1a1a1a; }
    .thumbnail {
      width: 1280px;
      height: 720px;
      position: relative;
      overflow: hidden;
      /* ... design styles ... */
    }
  </style>
</head>
<body>
  <div class="thumbnail">
    <!-- Thumbnail content -->
  </div>
</body>
</html>
<!-- Export (window size = canvas size, so the centered canvas fills the frame exactly):
     node <graphic-design>/scripts/render.mjs thumb.html --size 1280x720 --out thumb.png
     (without the graphic-design skill: chromium --headless --hide-scrollbars --window-size=1280,720 --screenshot=thumb.png thumb.html) -->
```

Then Read the PNG and run the same 168x94 shrink test as for Gemini output.

---

## Quality Checklist

- [ ] Output PNG was Read at full size and shrunk to 168x94px -- text spelled right and readable
- [ ] Maximum 5-7 words of text
- [ ] 3 or fewer visual elements
- [ ] High contrast text (stroke + shadow for safety)
- [ ] Clear focal point that communicates the topic
- [ ] Bottom-right corner, bottom edge, and top-right are clear (duration badge, progress bar, hover icons)
- [ ] Colors are distinct from platform UI (avoid pure white or YouTube red)
- [ ] Brand consistency with other thumbnails in the series
- [ ] Emotional hook -- face, number, or curiosity element
- [ ] Design-context colors and fonts are applied where appropriate
