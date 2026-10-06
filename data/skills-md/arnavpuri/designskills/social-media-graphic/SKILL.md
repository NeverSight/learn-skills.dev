---
name: social-media-graphic
description: >
  Organic social media graphics (posts, stories, carousels, profile headers/covers) sized for
  Instagram, X/Twitter, LinkedIn, Facebook, Pinterest, and TikTok, with platform safe zones.
  Defaults to Gemini 3.1 Flash image generation; HTML/CSS for templated carousels. Use for
  unpaid feed content; for paid ads use ad-creative-design, for website/email banners use
  banner-design, for YouTube thumbnails and OG images use thumbnail-design.
  Trigger phrases: "create a social media post", "design an Instagram graphic",
  "make a Twitter image", "LinkedIn post graphic", "social media design",
  "Instagram story", "carousel design", "social graphic".
license: MIT
---

# Social Media Graphic Design

Generate platform-perfect social media graphics with correct dimensions, safe zones, and platform-specific design patterns. Default output is a Gemini-generated PNG cropped to exact platform pixels; use HTML/CSS (Step 8) for multi-slide carousels with shared templates or copy-heavy posts.

---

## Step 1: Load Design Context

1. Read `.agents/design-context.md` first -- brand colors (hex), fonts, style archetype
2. If missing, use the `design-context` Default Fallbacks and tell the user defaults were used
3. Social media graphics must be strongly on-brand -- consistency builds recognition

---

## Gemini Image Generation Path

Pipeline/CLI: `image-generation`. Prompt craft, cropping, and text-overlay fallback: `graphic-design` Step 3.

1. Generate at the Gemini ratio from the table below; crop to exact pixels with `--resize WxH`
2. Tell Gemini where the safe zone is ("keep all text in the middle 70% vertically") -- it can't see platform UI
3. Read the output PNG: check every word's spelling, legibility at phone-feed size, and the Step 3 safe zones; fix one issue per follow-up turn

| Target | Gemini `--aspect-ratio` | `--resize` |
|--------|------------------------|-----------|
| IG/FB/LinkedIn square | 1:1 | 1080x1080 |
| IG/FB/LinkedIn portrait | 4:5 | 1080x1350 |
| IG feed 3:4 | 3:4 | 1080x1440 |
| Story / Reel / TikTok cover | 9:16 | 1080x1920 |
| X in-feed | 16:9 | 1200x675 |
| Link card / FB / LinkedIn landscape (1.91:1) | 16:9 | 1200x628 |
| X header (3:1) | 21:9 | 1500x500 |
| LinkedIn personal banner | 4:1 | 1584x396 |
| LinkedIn company cover (~5.9:1) | 8:1 | 1128x191 |
| Facebook page cover | 21:9 | 1640x624 (2x of 820x312) |
| Pinterest pin | 2:3 | 1000x1500 |

### Example Prompts

- **Instagram Post:** "Create a square Instagram post graphic for [brand]. [product] centered on [color] gradient. Bold [font-style] text '[headline]'. Clean, modern aesthetic."
- **Instagram Story:** "Create a vertical story graphic for [brand]. [product/subject] as the focal point with [color scheme] background. Text '[headline]' in the upper-middle, CTA '[action]' above the lower fifth; leave the top and bottom 15% free of text. Trendy, editorial style."
- **LinkedIn Post:** "Create a professional landscape LinkedIn post graphic for [brand]. [topic/statistic] visualized with [chart type or icon]. Headline '[text]' in [font-style]. Corporate blue tones, clean data-driven layout."

---

## Step 2: Identify Platform and Format

### Platform Dimensions Reference

#### Instagram
| Format | Dimensions | Aspect Ratio | Use Case |
|--------|-----------|--------------|----------|
| Feed Post (Square) | 1080 x 1080 | 1:1 | Standard post |
| Feed Post (Portrait) | 1080 x 1350 | 4:5 | Maximum feed real estate |
| Feed Post (3:4) | 1080 x 1440 | 3:4 | Matches the 3:4 profile grid (since 2025) |
| Feed Post (Landscape) | 1080 x 566 | 1.91:1 | Panoramic content |
| Story / Reel Cover | 1080 x 1920 | 9:16 | Full-screen vertical |
| Carousel Slide | 1080 x 1080 or 1080 x 1350 | 1:1 / 4:5 | All slides use the first slide's ratio |
| Profile Picture | 320 x 320 | 1:1 | Circular crop |

#### Twitter / X
| Format | Dimensions | Aspect Ratio | Use Case |
|--------|-----------|--------------|----------|
| In-Feed Image | 1200 x 675 | 16:9 | Standard post image |
| Header / Banner | 1500 x 500 | 3:1 | Profile header |
| Card Image | 1200 x 628 | 1.91:1 | Link preview |

#### LinkedIn
| Format | Dimensions | Aspect Ratio | Use Case |
|--------|-----------|--------------|----------|
| Feed Post | 1200 x 627 | 1.91:1 | Standard post |
| Feed Post (Square) | 1200 x 1200 | 1:1 | Square post |
| Feed Post (Portrait) | 1080 x 1350 | 4:5 | More mobile real estate |
| Personal Profile Banner | 1584 x 396 | 4:1 | Profile background |
| Company Page Cover | 1128 x 191 | ~5.9:1 | Company page |
| Article / Newsletter Cover | 1920 x 1080 | 16:9 | Article header |

#### Facebook
| Format | Dimensions | Aspect Ratio | Use Case |
|--------|-----------|--------------|----------|
| Feed Post | 1080 x 1350 or 1200 x 630 | 4:5 / 1.91:1 | 4:5 wins on mobile; 1.91:1 for link shares |
| Cover Photo | 820 x 312 (upload 1640 x 624) | 2.63:1 | Page cover; mobile shows a 640 x 360 crop |
| Event Cover | 1920 x 1005 | 1.91:1 | Event banner |
| Story | 1080 x 1920 | 9:16 | Story format |

#### Pinterest
| Format | Dimensions | Aspect Ratio | Use Case |
|--------|-----------|--------------|----------|
| Standard Pin | 1000 x 1500 | 2:3 | Optimal engagement |
| Long Pin | 1000 x 2100 | 1:2.1 | Feed crops pins taller than 2:3 -- put the hook in the top 1500px |
| Square Pin | 1000 x 1000 | 1:1 | Alternative format |

#### TikTok
| Format | Dimensions | Aspect Ratio | Use Case |
|--------|-----------|--------------|----------|
| Video Cover | 1080 x 1920 | 9:16 | Profile grid shows a ~3:4 center crop |

---

## Step 3: Apply Safe Zones

Every platform has areas where UI elements overlap the content. Keep critical text and visuals inside these safe zones.

### Instagram Feed Post (1080 x 1080 / 1080 x 1350)
```
Safe zone: 60px padding on all sides
Profile grid shows a 3:4 center crop: on 1:1 keep key content in the central 810px width;
on 4:5 the grid trims ~34px from each side
```

### Instagram / Facebook Story (1080 x 1920)
```
Top safe: 250px from top (~14%: progress bar, profile, close)
Bottom safe: 250px from bottom (~14%: reply bar, CTA sticker)
Left/Right safe: 60px from edges
Content zone: 960w x 1420h centered
```

### Reels / TikTok Cover (1080 x 1920)
```
Top: ~220px clear   Bottom: ~420px clear (caption, audio, CTA)
Right: ~130px clear (like/comment/share rail)
Keep the headline in the center band -- it also survives the 3:4 grid crop
```

### Twitter/X (1200 x 675)
```
Safe zone: 40px padding all sides
Text should be centered -- edges may crop on mobile
Keep key content in center 1120 x 595
```

### LinkedIn (1200 x 627)
```
Safe zone: 50px padding all sides
Bottom-left: avoid -- engagement buttons overlap
Center the main message
```

### Facebook Cover (820 x 312)
```
Desktop shows 820 x 312; mobile shows full height but crops the sides (~555px of 820 visible)
Mobile safe zone: center ~555 x 312
Profile photo can overlap the bottom-left -- keep text centered
```

### Pinterest Pin (1000 x 1500)
```
Keep ~80px clear top and bottom (Save button and icons overlay the corners)
Logo/branding: small, bottom-center or top-left
Headline readable at ~236px feed width
```

---

## Step 4: Platform-Specific Design Trends

### Instagram
- Clean, editorial layouts with generous whitespace
- Muted color palettes with one pop of color
- Consistent carousel templates (same frame, changing content)
- Sans-serif typography dominates
- Photo-forward with text overlays at 60-80% opacity backgrounds
- Rounded corners on inner elements (12-16px radius)

### Twitter / X
- Bold, high-contrast designs (dark mode is common)
- Large readable text -- viewed at small sizes in feed
- Data visualizations and chart-style graphics perform well
- Thread-style sequential graphics
- Minimal decoration, content-forward

### LinkedIn
- Professional, corporate-leaning aesthetic
- Blue tones naturally blend with the platform
- Clean data presentation, statistics, and insights
- Headshot + quote format for thought leadership
- Subtle gradients rather than loud colors

### Facebook
- Warm, approachable design language
- Photo-centric with overlay text
- Event and community-focused layouts
- Cover photos should work with little or no text (the old "20% text rule" was retired in 2020, but text-light images still tend to perform better)
- Groups and communities prefer authentic over polished

### Pinterest
- Vertical format maximizes screen real estate
- Text overlay on lifestyle imagery
- Step-by-step tutorial formats
- List-style pins with clear numbered sections
- Warm, aspirational color palettes
- Bold, readable text at small sizes

### TikTok
- Bold, energetic, trend-driven
- High contrast for small-screen readability
- Emoji and casual typography
- Thumbnail must convey content in under 1 second

---

## Step 5: Template Structures

### Quote Post (Instagram 1080x1080)
```html
<div class="canvas" style="width:1080px;height:1080px;position:relative;overflow:hidden;
  background:linear-gradient(135deg, var(--primary), var(--secondary));
  display:flex;align-items:center;justify-content:center;padding:80px;">

  <div style="text-align:center;">
    <div style="font-size:72px;line-height:1.1;margin-bottom:8px;opacity:0.3;
      font-family:Georgia,serif;">"</div>
    <p style="font-family:var(--font-heading);font-size:42px;font-weight:700;
      color:#fff;line-height:1.3;text-wrap:balance;">
      The quote text goes here, keep it under 120 characters for readability.
    </p>
    <div style="margin-top:40px;display:flex;align-items:center;justify-content:center;gap:12px;">
      <div style="width:40px;height:2px;background:rgba(255,255,255,0.5);"></div>
      <span style="font-family:var(--font-body);font-size:18px;color:rgba(255,255,255,0.8);
        text-transform:uppercase;letter-spacing:0.1em;">Author Name</span>
      <div style="width:40px;height:2px;background:rgba(255,255,255,0.5);"></div>
    </div>
  </div>
</div>
```

### Announcement Post (LinkedIn 1200x627)
```
Layout structure:
- Left 60%: Headline (bold, 48px) + Body text (20px) + CTA badge
- Right 40%: Visual element (icon, illustration, or abstract shape)
- Top bar: Brand color accent line (4px)
- Bottom: Logo + URL in small text
- Background: White or very light neutral
```

### Tip Carousel (Instagram 1080x1080, multi-slide)
```
Slide 1 (Cover):
- Bold headline: "5 Tips for [Topic]"
- Subtext: "Swipe to learn more →"
- Eye-catching gradient or image background
- Brand logo bottom-center

Slides 2-6 (Content):
- Tip number: large, semi-transparent in background (like "01")
- Tip headline: 32px bold
- Tip description: 20px, 2-3 lines max
- Consistent background across all slides
- Progress indicator dots at bottom

Slide 7 (CTA):
- "Found this helpful?"
- Follow CTA + handle
- Share/save prompt
- Brand logo
```

### Before/After (Instagram 1080x1350)
```
Layout:
- Top half: "Before" label + image/state
- Divider: thin line or diagonal cut with label
- Bottom half: "After" label + image/state
- Keep dimensions equal for both halves
- Use subtle color shift (gray/muted for before, vibrant for after)
```

### Data/Stat Post (Twitter 1200x675)
```
Layout:
- Large number: 72-96px, bold, gradient or accent color
- Context line: 24px below the number
- Supporting text: 18px, 2 lines max
- Source attribution: 14px, bottom-right
- Background: clean gradient or subtle pattern
- Brand mark: small, bottom-left
```

---

## Step 6: Carousel Design System

For multi-slide carousels, maintain consistency:

```css
/* Shared carousel variables */
:root {
  --slide-bg: #0F172A;
  --slide-text: #F8FAFC;
  --slide-accent: #6366F1;
  --slide-padding: 80px;
  --slide-radius: 0; /* carousels are edge-to-edge */
}

/* Consistent header bar across slides */
.slide-header {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 4px;
  background: var(--slide-accent);
}

/* Progress indicator */
.progress-dots {
  position: absolute;
  bottom: 40px;
  left: 50%;
  transform: translateX(-50%);
  display: flex;
  gap: 8px;
}
.progress-dots .dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: rgba(255,255,255,0.3);
}
.progress-dots .dot.active {
  background: var(--slide-accent);
  width: 24px;
  border-radius: 4px;
}

/* Swipe hint on first slide */
.swipe-hint {
  position: absolute;
  right: 40px;
  top: 50%;
  transform: translateY(-50%);
  font-size: 14px;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  writing-mode: vertical-rl;
  opacity: 0.6;
}
```

---

## Step 7: Engagement Optimization

### Text Readability Rules
- **Maximum 6 words per line** for headlines on social
- **Maximum 3 lines** for any text block on a social graphic
- **Minimum font size:** 24px for Instagram, 20px for Twitter/LinkedIn
- **Contrast:** white text on dark overlay OR dark text on light overlay, never mid-tone on mid-tone

### Attention-Grabbing Techniques
1. **Asymmetric layouts** -- break the grid slightly for visual tension
2. **One bold color** against a muted palette
3. **Oversized numbers or single words** as anchors
4. **Negative space** that frames the message
5. **Diagonal elements** that create movement
6. **Border or frame** around the canvas edge (8-12px inset)

### Platform-Specific CTAs
- Instagram: "Save this for later", "Share to your story", "Double tap if you agree"
- Twitter: "RT if you agree", "Reply with your take", "Bookmark this thread"
- LinkedIn: "Agree? Share your perspective below", "Follow for more insights"
- Pinterest: "Save this pin", "Click through for the full guide"

---

## Step 8: Code Output Path

When using code instead of Gemini, generate a self-contained HTML file. Include:

1. Correct `width` and `height` on the canvas element
2. Google Fonts loaded via `<link>` tag
3. All colors from design-context
4. CSS custom properties for easy adjustment
5. Comments marking editable sections (text, colors, images)

### Exporting Tips

Include a comment in the output:
```html
<!-- To export as an image (body margin must be 0):
     node <graphic-design>/scripts/render.mjs post.html --size 1080x1080 --out post.png
     (without the graphic-design skill: chromium --headless --hide-scrollbars --window-size=1080,1080 --screenshot=post.png post.html)
     Or DevTools > Cmd+Shift+P > "Capture node screenshot" -->
```

After exporting, Read the PNG and check it the same way as a Gemini output.

---

## Quality Checklist

- [ ] Dimensions exactly match the target platform
- [ ] Text is within safe zones
- [ ] Font size is readable at the platform's display size
- [ ] Brand colors and fonts are applied consistently
- [ ] Visual hierarchy is clear -- one focal point
- [ ] No text-heavy areas (social graphics are visual-first)
- [ ] CTA or action prompt is included where appropriate
- [ ] Output PNG was Read: every word spelled correctly, legible at phone size
- [ ] Code output (if used) is self-contained except fonts
