---
name: banner-design
description: >
  Banner graphics for owned channels: website hero/section banner images, email header
  images, event and conference banners, sidebar house promos, and announcement bars, via
  Gemini 3.1 Flash image generation (default) or HTML/CSS. Covers standard sizes, Gemini
  ratios and cropping, CTA placement, responsive art direction, and email constraints. For
  paid display/IAB ads use ad-creative-design; for a coded above-the-fold section use
  hero-section; for a full email template use email-design.
  Trigger phrases: "design a banner", "create a website banner", "hero banner image",
  "email header", "event banner", "promotional banner", "web banner",
  "sidebar banner", "announcement bar", "Eventbrite banner".
license: MIT
---

# Banner Design

Design website banners, email headers, event banners, and hero sections. Covers standard dimensions, static and animated approaches, CTA hierarchy, responsive scaling, and seasonal/promotional frameworks.

---

## Step 1: Load Design Context

1. Read `.agents/design-context.md` first -- brand colors (hex), fonts, style archetype
2. If missing, use the `design-context` Default Fallbacks and tell the user defaults were used
3. Banners are high-visibility brand touchpoints -- strict adherence to brand guidelines

---

## Gemini Image Generation Path

Pipeline/CLI: `image-generation`. Prompt craft, cropping, and text-overlay fallback: `graphic-design` Step 3.

1. Generate at the Gemini ratio in the Step 2 tables, then `--resize WxH` (e.g. `--aspect-ratio 21:9 --resize 1440x600`). Export web/email banners at 2x (e.g. 2880x1200, 1200x400) and display at 1x for sharp retina rendering
2. Web heroes crop differently per breakpoint: keep the subject centered with clear space for text, or generate a separate 4:5 mobile version
3. For web and email, prefer generating the visual without text and setting headline + CTA as live HTML text (accessible, editable, and still visible when email images are blocked)
4. Read the output PNG: check spelling, legibility at the displayed size, and that the text area is clean. Fix one issue per follow-up turn

### Example Prompts

- **Hero Banner:** "Create a wide website hero banner for [brand]. [product/service] visual on the right, headline '[text]' on the left in [font-style]. [color] gradient background. CTA button '[action]'. Modern, bold layout."
- **Email Header:** "Create a wide email header banner for [brand]. [campaign theme] with [color palette]. Logo centered at top, headline '[text]' below. Simple, clean design that renders in all email clients."
- **Event Banner:** "Create a wide event banner for [event name]. [style] background with [decorative elements]. Event name '[text]' prominently displayed. Date '[date]' and location '[venue]' below. [mood/tone]."

---

## Step 2: Identify Banner Type and Dimensions

### Website Banners

| Type | Dimensions | Gemini ratio | Use Case |
|------|-----------|--------------|----------|
| Hero Banner (Full Width) | 1440 x 600 | 21:9 | Homepage hero, above the fold |
| Hero Banner (Tall) | 1440 x 800 | 16:9 | Full-viewport hero section |
| Section Banner | 1440 x 400 | 4:1 | Interior page section divider |
| Sidebar Banner | 300 x 250 or 300 x 600 | 5:4 / 9:16 | House promo (paid placements: ad-creative-design) |
| Notification Bar | Full width x 48px | Top-of-page announcement |
| Cookie/Consent Bar | Full width x 80px | Bottom notification |

### Email Banners

| Type | Dimensions | Gemini ratio | Notes |
|------|-----------|--------------|-------|
| Email Header | 600 x 200 | 21:9 | Standard email width |
| Email Hero | 600 x 300 | 16:9 | Full-width email hero |
| Email Banner | 600 x 150 | 4:1 | Compact promotional |

Email constraints: 600px wide (up to ~640), tables for layout, inline CSS, web fonts only render in some clients (Apple Mail, iOS) so always declare an Arial/Helvetica fallback, every image needs alt text, and key copy should be live text because many clients block images by default.

### Event / Promotional Banners

| Type | Dimensions | Gemini ratio | Use Case |
|------|-----------|--------------|----------|
| Event Banner (Wide) | 1200 x 400 | 21:9 | Event page header |
| Meetup Banner | 1200 x 675 | 16:9 | Meetup.com event cover |
| Eventbrite Banner | 2160 x 1080 | 16:9 | Eventbrite event cover (2:1) |
| Conference Banner | 1920 x 600 | 4:1 | Conference website hero |

---

## Step 3: Hero Banner Composition

### Layout Patterns

#### Split Hero (Content Left, Visual Right)
Grid `1fr 1fr`, min-height 600px, 80px padding, 60px gap. Content side: eyebrow (14px uppercase, brand color), headline (`clamp(36px, 4vw, 56px)`, weight 800, `text-wrap: balance`), description (18px, muted), CTA group (flex, 16px gap).

#### Centered Hero (Text over Background)
Flex column centered, min-height 600px, 80px padding. Background image with gradient overlay for legibility. Headline `clamp(40px, 5vw, 72px)` white, max-width 800px.

#### Asymmetric Hero (Off-Center Focal Point)
Grid `55% 45%`. Content side with padding 80px. Visual side with `clip-path: polygon(10% 0, 100% 0, 100% 100%, 0% 100%)`.

#### Full-Bleed Visual Hero (Minimal Text)
Background image cover, min-height 80vh, `align-items: flex-end`. Gradient scrim `::after` for text legibility (0->0.7 black from bottom). Content at z-index 2, max-width 600px, white text.

---

## Step 4: CTA Placement and Hierarchy

### Primary + Secondary CTA Pattern

Use a flex container (`gap: 16px; flex-wrap: wrap`). Primary CTA: solid brand-color background, white text, 14px 28px padding, 8px radius, shadow. Secondary CTA: transparent bg, neutral border (1.5px), same size. Both: `font-weight: 600`, hover with `translateY(-1px)` or bg fill.

### CTA Placement Rules
- **Hero banner:** CTA below the headline + description, left-aligned
- **Centered banner:** CTA centered, below description
- **Sidebar banner:** CTA at the bottom, full-width
- **Notification bar:** CTA inline with text, right side
- **Email banner:** CTA as a large button, centered

---

## Step 5: Animated Banner Techniques

### Animation Techniques

- **Parallax**: scroll container with `perspective: 1px; height: 100vh; overflow-y: auto`; background layer `transform: translateZ(-1px) scale(2)` (scale = 1 + depth / perspective)
- **Animated gradient**: `background-size: 600% 600%`, animate `background-position` over 12s
- **Floating shapes**: Absolute circles at 0.08 opacity, each with unique translate/rotate keyframes (7-10s duration)
- **Text reveal**: Wrap words in `<span>` with `inline-block`, animate `translateY(100%) -> 0` with staggered 0.1s delays
- **Typing effect**: `white-space: nowrap; width: 0`, animate width with `steps()`, add blinking cursor via `border-right`
- Wrap all motion in `@media (prefers-reduced-motion: no-preference)` and keep the headline readable in the first frame

---

## Step 6: Responsive Banner Techniques

### Fluid Scaling
- Use `clamp()` for min-height, padding, font-size: e.g., `font-size: clamp(28px, 4vw, 64px)`
- At 768px breakpoint: stack split grids to `1fr`, center text, reorder visual above text with `order: -1`
- Swap background images per breakpoint: mobile (default), tablet (768px), desktop (1200px)

---

## Step 7: Seasonal and Promotional Frameworks

### Sale / Discount Banner
Red gradient bg (`135deg, #DC2626, #991B1B`), centered layout. Discount number at `clamp(60px, 10vw, 120px)` weight 900. Add diagonal stripe decoration with `repeating-linear-gradient(-45deg)` at 0.03 opacity.

### Product Launch Banner
Dark bg (`#0F172A` to `#1E293B`), centered text. Pill eyebrow badge (uppercase, 13px, brand color with translucent bg/border). Headline `clamp(36px, 5vw, 64px)` white. Add spotlight glow `::after` with `radial-gradient` centered above.

### Event Countdown Banner
Brand-color bg, centered. Countdown units in flex row (24px gap). Each unit: large number (48px/800, `tabular-nums`, dark translucent bg), small label below (12px uppercase). Separators between units.

### Notification / Announcement Bar
Full-width, brand-color bg, flex centered, 10px 20px padding. Text 14px/500, links underlined bold. Close button absolute right.

### Seasonal Themes

| Season/Event | Colors | Elements | Mood |
|-------------|--------|----------|------|
| **Spring** | Greens, pinks, yellows | Flowers, leaves, butterflies | Fresh, renewal |
| **Summer** | Blues, oranges, bright yellow | Sun, waves, palm trees | Energetic, warm |
| **Fall** | Oranges, reds, browns | Leaves, pumpkins, warm tones | Cozy, harvest |
| **Winter** | Blues, whites, silvers | Snowflakes, frost, evergreen | Crisp, festive |
| **Black Friday** | Black, gold, red | Bold typography, price tags | Urgency, luxury |
| **New Year** | Gold, black, champagne | Confetti, fireworks, sparkle | Celebration |
| **Valentine's** | Reds, pinks, rose gold | Hearts, flowers, soft gradients | Romantic, warm |

---

## Step 8: Hero vs Sidebar Banner Patterns

### Hero Banner Best Practices
- Full viewport width, 50-80vh height
- One clear headline, one clear CTA
- Background: gradient, image with overlay, or animated
- Content area max-width: 1200-1440px, centered
- Mobile: stack vertically, reduce heading size
- Load time: optimize background images, use CSS gradients where possible

### Sidebar Banner Best Practices
- Fixed width (usually 300px)
- Taller formats (300x600) outperform shorter (300x250)
- Content must be fully visible without scrolling
- Clear border/separation from page content
- Minimal text: headline + CTA only
- Strong visual contrast from the surrounding page

Sidebar banner pattern: 300x600px, flex column, brand gradient bg, 32px 24px padding, white text. Logo top, visual center (flex:1), headline 22px/700, body 14px at 0.85 opacity, CTA at bottom (`margin-top: auto`, white bg, brand-color text, centered).

---

## Step 9: Email Header Specifics

Email HTML has severe constraints. Use this approach:

Use table-based layout, max 600px, inline styles only. Font: `Arial, Helvetica, sans-serif`. Structure: outer `<table>` with gradient bg, logo `<img>` centered, `<h1>` (28px bold white), `<p>` (16px white 0.9 opacity), CTA as nested table with white bg + brand-color text link.

### Email Design Rules
- Use `Arial, Helvetica, sans-serif` (web fonts unreliable in email)
- Background images: always set `background-color` as fallback (Outlook ignores bg images)
- Max width 600px, design for 320px mobile
- Images: always set `width`, `height`, `alt`, `display:block`
- Avoid CSS shorthand; use longhand properties
- Test in Litmus or Email on Acid

---

## Quality Checklist

- [ ] Banner dimensions match the target placement (Gemini output cropped with `--resize`)
- [ ] Output PNG / rendered screenshot was Read: text spelled correctly and legible at display size
- [ ] Clear visual hierarchy: Headline > Description > CTA
- [ ] CTA is prominent and action-oriented
- [ ] Brand colors and fonts from design-context applied
- [ ] Text contrast: 4.5:1 normal, 3:1 large (>=24px or >=18.66px bold), measured over the busiest part of the image (add a scrim if needed)
- [ ] Responsive: scales well from mobile to desktop
- [ ] Animations are smooth and not distracting
- [ ] Load performance: CSS gradients preferred over heavy images
- [ ] Email banners use table layout and inline styles
- [ ] Seasonal/promotional banners match the occasion's visual language
- [ ] Self-contained HTML/CSS output
