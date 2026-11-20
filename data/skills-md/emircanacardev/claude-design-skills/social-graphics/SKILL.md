---
name: social-graphics
description: Designs social media graphics at exact platform sizes, including feed posts, carousels, story and reel covers, and video thumbnails, with safe zones, readable thumbnail text, consistent templates, and correct export settings, delivered as HTML and CSS or SVG layouts. Use when asked to make an Instagram post or carousel, a YouTube thumbnail, a LinkedIn or X image, or a story graphic. Not for presentation decks, which is slide-design.
---

# Social Graphics

Produces platform-ready social visuals at exact pixel sizes, with text inside the safe zones and a reusable template, as HTML/CSS or SVG that exports cleanly to image files.

## When to use
- "Make an Instagram carousel / post about X."
- YouTube thumbnails, Reel, TikTok, or Shorts covers, and Story graphics.
- LinkedIn or X post images, announcement cards, quote cards.
- Setting up a consistent template set for a series or brand.
- Adapting one piece of content to several platforms and aspect ratios.

## Workflow
1. Confirm platform, format, message, and brand inputs (colors, fonts, logo from brand-identity if available). If no platform is given, default to an Instagram portrait post at 1080×1350 and say so.
2. Pick the exact canvas from the size list below and mark the safe zones before placing anything.
3. Write the copy: one message per graphic, 3–5 words on thumbnails and covers. Longer explanation belongs in the caption.
4. Choose one focal point (a face, product, number, or headline) and build the hierarchy around it: focal subject, headline, supporting line, small brand mark.
5. For carousels, outline first: slide 1 is the hook, then one point per slide, and the last slide is the call to action (save, share, follow, visit). Keep margins, numbering, and a recurring element consistent so the slides read as a set.
6. Build it as a template: tokens for color, type, and spacing; fixed text positions; named content slots.
7. Test small: view at about 25% scale and on a phone; check legibility, contrast, and crop previews.
8. Export at the exact size with the settings below.

## Rules
**Sizes (px)**
- Instagram feed: portrait 1080×1350 (4:5, preferred) or square 1080×1080.
- Stories, Reels, TikTok, YouTube Shorts: 1080×1920 (9:16).
- YouTube thumbnail: 1280×720 (16:9), under 2 MB.
- LinkedIn feed: 1200×627 landscape or 1080×1350 portrait. X/Twitter: 1600×900 (16:9).

**Safe zones**
- 9:16 vertical: keep text and faces out of roughly the top 250px and bottom 350–400px, where platform UI and captions overlay, and away from the right edge, where action buttons sit.
- Instagram profile grid previews crop feed posts to 3:4, centered by default: about 34px off each side of a 1080×1350 post and 135px off each side of a 1080×1080 post. Keep essential content out of those strips.
- Keep at least 60px of margin from every edge on feed graphics.

**Thumbnails and covers**
- One focal subject, 3–5 words, high contrast, and type large enough to read with the image shown about 160px wide.
- The text complements the video title rather than repeating it.
- Keep text out of the bottom-right corner of YouTube thumbnails, where the duration badge sits.

**Text and type**
- Photo-led graphics keep text to a small share of the area; text-led graphics (quotes, tips) use one headline and at most 2 supporting lines per slide.
- At most 2 typefaces; about 32px minimum for body text on a 1080px-wide canvas.
- Text contrast at least 4.5:1; text over photos gets a scrim or solid panel.

**Export**
- PNG for text-heavy graphics and flat color; JPG at high quality (around 80–90) for photo-heavy images; sRGB color profile; exact canvas size.
- Name files by platform, ratio, and order: `ig-carousel-4x5-01.png`.

## Output
- HTML/CSS with one fixed-size element per graphic (for example `.slide { width: 1080px; height: 1350px; }`), or standalone SVG with a matching `viewBox`. Tokens as CSS custom properties; no new dependencies unless asked.
- An optional safe-zone overlay toggled by a class and hidden for export.
- Copy for each slide and a caption outline.
- Export steps: render at the exact viewport with a device scale factor of 1 (for example, a headless browser screenshot), then save as PNG or JPG.

## Avoid
- Designing at one ratio and letting each platform crop it.
- Text in the vertical-video UI zones or under the YouTube duration badge.
- Long sentences on thumbnails and several competing focal points.
- Low-contrast text on busy photos without a scrim.
- Carousel slides with shifting margins, fonts, or colors.
- Other creators' images, logos, or trademarked characters used without rights.

## Final check
- [ ] Canvas size matches the platform exactly.
- [ ] Text and faces sit inside the safe zones; the 3:4 grid crop was checked.
- [ ] Thumbnail or cover text is 3–5 words and legible at small size.
- [ ] Carousels have a hook slide, one point per slide, and a CTA slide.
- [ ] Text contrast is at least 4.5:1; at most 2 typefaces.
- [ ] Export format, sRGB profile, and file size limits (YouTube under 2 MB) are met.
