---
name: asc-screenshots
description: Use when building App Store screenshot pages, generating exportable marketing screenshots for iOS apps or iPad apps, or creating programmatic screenshot generators with Next.js. Triggers on app store, screenshots, marketing assets, html-to-image, device mockup, frameme, asc-client, asc-screenshots.
---

# App Store Screenshots Generator

## Overview

Build a Next.js page that renders App Store screenshots for **iPhone and iPad** as **advertisements** (not UI showcases) and exports them via `html-to-image` at Apple's required resolutions. Uses [FrameMe](https://github.com/joshluongo/frameme) to composite app screenshots into official Apple device bezels with pixel-perfect accuracy (including Dynamic Island). Screenshots are the single most important conversion asset on the App Store.

## Core Principle

**Screenshots are advertisements, not documentation.** Every screenshot sells one idea. If you're showing UI, you're doing it wrong — you're selling a *feeling*, an *outcome*, or killing a *pain point*.

## Step 1: Ask the User These Questions

Before writing ANY code, ask the user all of these. Do not proceed until you have answers:

### Required

1. **App screenshots** — "Where are your app screenshots? (PNG files of actual device captures)"
2. **App icon** — "Where is your app icon PNG?"
3. **Brand colors** — "What are your brand colors? (accent color, text color, background preference)"
4. **Font** — "What font does your app use? (or what font do you want for the screenshots?)"
5. **Feature list** — "List your app's features in priority order. What's the #1 thing your app does?"
6. **Number of slides** — "How many screenshots do you want? (Apple allows up to 10)"
7. **Style direction** — "What style do you want? Examples: warm/organic, dark/moody, clean/minimal, bold/colorful, gradient-heavy, flat. Share App Store screenshot references if you have any."
8. **Devices** — "Which devices did you capture screenshots on? (e.g. iPhone 17 Pro, iPhone 17 Pro Max, iPad Pro 11", iPad Pro 13", etc.)"

### Optional

9. **Localization** — "Do you want screenshots in multiple languages? If so, which languages? (e.g. English, German, French). You'll get a language switcher in the preview to toggle between them."
10. **Project location** — "Do you want to keep the screenshot generator project permanently so you can come back to make changes or add languages later? If so, where should I create it? (e.g. inside your app's repo)"
11. **Component assets** — "Do you have any UI element PNGs (cards, widgets, etc.) you want as floating decorations? If not, that's fine — we'll skip them."
12. **Additional instructions** — "Any specific requirements, constraints, or preferences?"

### Derived from answers (do NOT ask — decide yourself)

Based on the user's style direction, brand colors, and app aesthetic, decide:
- **Background style**: gradient direction, colors, whether light or dark base
- **Decorative elements**: blobs, glows, geometric shapes, or none — match the style
- **Dark vs light slides**: how many of each, which features suit dark treatment
- **Typography treatment**: weight, tracking, line height — match the brand personality
- **Color palette**: derive text colors, secondary colors, shadow tints from the brand colors

**IMPORTANT:** If the user gives additional instructions at any point during the process, follow them. User instructions always override skill defaults.

## Step 2: Set Up the Project

### Requirements

- **Node.js 18+**
- **FrameMe** — required for pixel-perfect device framing (including Dynamic Island). Install by building from source:
  ```bash
  git clone https://github.com/joshluongo/frameme.git /tmp/frameme
  cd /tmp/frameme && swift build -c release
  strip .build/release/frameme
  cp .build/release/frameme /usr/local/bin/frameme
  ```
  If the user doesn't have FrameMe, ask them to install it before proceeding.

### Detect Package Manager

Check what's available, use this priority: **bun > pnpm > yarn > npm**

```bash
# Check in order
which bun && echo "use bun" || which pnpm && echo "use pnpm" || which yarn && echo "use yarn" || echo "use npm"
```

### Scaffold (if no existing Next.js project)

```bash
# With bun:
bunx create-next-app@latest . --typescript --app --src-dir --no-eslint --import-alias "@/*"
bun add html-to-image jszip

# With pnpm:
pnpx create-next-app@latest . --typescript --app --src-dir --no-eslint --import-alias "@/*"
pnpm add html-to-image jszip

# With yarn:
yarn create next-app . --typescript --app --src-dir --no-eslint --import-alias "@/*"
yarn add html-to-image jszip

# With npm:
npx create-next-app@latest . --typescript --app --src-dir --no-eslint --import-alias "@/*"
npm install html-to-image jszip
```

### File Structure

```
project/
├── public/
│   ├── app-icon.png            # User's app icon
│   ├── framed/                 # FrameMe output (device-framed screenshots)
│   │   ├── iphone/
│   │   │   ├── en/             # Per-locale if localized UI screenshots
│   │   │   │   ├── home_framed.png
│   │   │   │   └── ...
│   │   │   └── de/             # (if single language, skip locale dirs)
│   │   │       └── ...
│   │   └── ipad/
│   │       └── ...
│   └── screenshots/            # Raw app screenshots (before framing)
│       ├── iphone/
│       │   ├── en/
│       │   │   ├── home.png
│       │   │   └── ...
│       │   └── de/
│       │       └── ...
│       └── ipad/
│           └── ...
├── src/app/
│   ├── copy.json               # Localized copy (editable without touching code)
│   ├── layout.tsx              # Font setup
│   └── page.tsx                # The screenshot generator (single file)
└── package.json
```

If the app UI is the same across languages (only marketing text changes), skip the locale subdirectories — all languages share the same framed device images.

**The generator is `page.tsx` + `copy.json`.** No routing, no extra layouts, no API routes. All text lives in `copy.json` so the user can update copy without editing components.

### Font Setup

```tsx
// src/app/layout.tsx
import { YourFont } from "next/font/google"; // Use whatever font the user specified
const font = YourFont({ subsets: ["latin"] });

export default function Layout({ children }: { children: React.ReactNode }) {
  return <html><body className={font.className}>{children}</body></html>;
}
```

## Step 2.5: Frame Screenshots with FrameMe

Before building the page, composite each raw screenshot into its device bezel using FrameMe. This produces pixel-perfect device images with the Dynamic Island, rounded corners, and bezel fully intact.

### Device Bezels

The skill includes official Apple bezels (co-located with this SKILL.md). Use the bezel that matches the device the user captured screenshots on:

| Bezel file | Device | Image size |
|------------|--------|------------|
| `iphone-17-pro.png` | iPhone 17 Pro (6.1") | 1350×2760 |
| `iphone-17-pro-max.png` | iPhone 17 Pro Max (6.9") | 1470×3000 |
| `ipad-pro-11.png` | iPad Pro 11" M4 | 1880×2640 |
| `ipad-pro-13.png` | iPad Pro 13" M4 | 2300×3000 |

### Frame All Screenshots

Based on the user's answer to question #8, select the matching bezel:

```bash
SKILL_DIR="<path to this skill's directory>"

# Frame screenshots per locale (en is required, others optional)
for LANG in en de fr; do
  # iPhone (pick the matching bezel)
  mkdir -p public/framed/iphone/$LANG
  frameme "$SKILL_DIR/iphone-17-pro.png" public/screenshots/iphone/$LANG/*.png --output public/framed/iphone/$LANG
  # OR: frameme "$SKILL_DIR/iphone-17-pro-max.png" ...

  # iPad (pick the matching bezel)
  mkdir -p public/framed/ipad/$LANG
  frameme "$SKILL_DIR/ipad-pro-11.png" public/screenshots/ipad/$LANG/*.png --output public/framed/ipad/$LANG
  # OR: frameme "$SKILL_DIR/ipad-pro-13.png" ...
done
```

If the app UI doesn't change across languages (only marketing text differs), frame once under `en/` — the Device component's `onError` fallback will use English images for all locales.

FrameMe automatically:
- Detects the screen area from the bezel's alpha channel
- Creates a per-scanline mask (handles Dynamic Island, rounded corners)
- Composites the screenshot behind the bezel
- Outputs `filename_framed.png`

### Important Notes

- **Match the bezel to the capture device** — using a mismatched bezel will cause clipping or misalignment
- FrameMe does NOT resize — the screenshot should match the bezel's screen area
- The framed images are what the page.tsx will reference — the user sees the final device appearance in the ad layouts

## Step 3: Plan the Slides

### Screenshot Framework (Narrative Arc)

Adapt this framework to the user's requested slide count. Not all slots are required — pick what fits:

| Slot | Purpose | Notes |
|------|---------|-------|
| #1 | **Hero / Main Benefit** | App icon + tagline + home screen. This is the ONLY one most people see. |
| #2 | **Differentiator** | What makes this app unique vs competitors |
| #3 | **Ecosystem** | Widgets, extensions, watch — beyond the main app. Skip if N/A. |
| #4+ | **Core Features** | One feature per slide, most important first |
| 2nd to last | **Trust Signal** | Identity/craft — "made for people who [X]" |
| Last | **More Features** | Pills listing extras + coming soon. Skip if few features. |

**Rules:**
- Each slide sells ONE idea. Never two features on one slide.
- Vary layouts across slides — never repeat the same template structure.
- Include 1-2 contrast slides (inverted bg) for visual rhythm.

## Step 4: Write Copy FIRST

Get all headlines approved before building layouts. Bad copy ruins good design.

### The Iron Rules

1. **One idea per headline.** Never join two things with "and."
2. **Short, common words.** 1-2 syllables. No jargon unless it's domain-specific.
3. **3-5 words per line.** Must be readable at thumbnail size in the App Store.
4. **Line breaks are intentional.** Control where lines break with `<br />`.

### Three Approaches (pick one per slide)

| Type | What it does | Example |
|------|-------------|---------|
| **Paint a moment** | You picture yourself doing it | "Check your coffee without opening the app." |
| **State an outcome** | What your life looks like after | "A home for every coffee you buy." |
| **Kill a pain** | Name a problem and destroy it | "Never waste a great bag of coffee." |

### What NEVER Works

- **Feature lists as headlines**: "Log every item with tags, categories, and notes"
- **Two ideas joined by "and"**: "Track X and never miss Y"
- **Compound clauses**: "Save and customize X for every Y you own"
- **Vague aspirational**: "Every item, tracked"
- **Marketing buzzwords**: "AI-powered tips" (unless it's actually AI)

### Copy Process

1. Write 3 options per slide using the three approaches
2. Read each at arm's length — if you can't parse it in 1 second, it's too complex
3. Check: does each line have 3-5 words? If not, adjust line breaks
4. Present options to the user with reasoning for each
5. If localized: translate approved headlines into all requested languages. Respect the tone/formality of each language. Line breaks may need adjusting per language — German and French text is often longer than English.

### Reference Apps for Copy Style

- **Raycast** — specific, descriptive, one concrete value per slide
- **Turf** — ultra-simple action verbs, conversational
- **Mela / Notion** — warm, minimal, elegant

## Step 5: Build the Page

### Architecture

```
page.tsx
├── Constants (IPHONE_W, IPHONE_H, IPAD_W, IPAD_H, design tokens)
├── LOCALES (code, label, asc locale code for App Store Connect)
├── ASC_DEVICE (maps "iphone" → "APP_IPHONE_67", "ipad" → "APP_IPAD_PRO_3GEN_129")
├── COPY (imported from copy.json — localized strings per language, keyed by slide name)
├── Device component (renders a pre-framed device image — just an <img>)
├── Caption component (label + headline)
├── Decorative components (blobs, glows, shapes — based on style direction)
├── Screenshot1..N components (one per slide, with iPhone and/or iPad variants)
├── SCREENSHOTS array (registry, with device type tag)
├── ScreenshotPreview (ResizeObserver scaling + hover export)
└── ScreenshotsPage (grid + toolbar with language switcher + device filter + Export/Export All Languages)
```

### Export Sizes (Largest Only — Apple auto-scales to smaller displays)

App Store Connect accepts the largest screenshot size per device and automatically scales it for smaller displays. Only generate:

```typescript
// iPhone 6.9" — covers all iPhone sizes
const IPHONE_W = 1320;
const IPHONE_H = 2868;

// iPad 13" — covers all iPad sizes
const IPAD_W = 2064;
const IPAD_H = 2752;
```

### Rendering Strategy

Each screenshot is designed at full export resolution. Two copies exist:

1. **Preview**: CSS `transform: scale()` via ResizeObserver to fit a grid card
2. **Export**: Offscreen at `position: absolute; left: -9999px` at true resolution

If both iPhone and iPad are requested:
- **Separate sections**: Render iPhone and iPad in distinct sections with device headers (`<h2>iPhone</h2>`, `<h2>iPad</h2>`), each with its own grid. Do NOT mix them in a single grid.
- **Device filter**: The toolbar includes an All / iPhone / iPad toggle that shows/hides sections.
- Each section filters `SCREENSHOTS.filter(s => s.device === "iphone")` etc.

### Localization

If the user wants multiple languages, store all copy in a separate `copy.json` file so the user can edit text without touching code:

```
src/app/copy.json
```

```json
{
  "en": {
    "iphone-hero": { "headline": "Spam texts,<br/>silenced.", "pills": ["Smart", "Private"] },
    "iphone-privacy": { "label": "On-device AI", "headline": "Completely<br/>private.", "sub": "..." }
  },
  "de": {
    "iphone-hero": { "headline": "Spam-SMS,<br/>verstummt.", "pills": ["Intelligent", "Datenschutz"] },
    "iphone-privacy": { "label": "KI auf dem Gerät", "headline": "Vollständig<br/>privat.", "sub": "..." }
  }
}
```

Import and type-cast it in `page.tsx`:

```typescript
import COPY_JSON from "./copy.json";
const COPY = COPY_JSON as Record<Locale, Record<string, SlideCopy>>;
```

Each slide component receives the current locale and looks up its copy from `COPY[locale][slideName]`. The toolbar includes a **language switcher** (`<select>` dropdown) that updates a shared `locale` state. Options show `{label} ({code})` (e.g. "English (en)") and are sorted alphabetically by label. This lets the user preview all slides in any language before exporting.

When exporting, include the locale in filenames: `01-iphone-hero-en-1320x2868.png`, `01-iphone-hero-de-1320x2868.png`. The "Export All" button exports the **currently selected language**. If the user wants all languages, they switch and export each.

**Localized device images:** If app screenshots differ per language (e.g. localized UI), organize framed images by locale: `public/framed/iphone/en/`, `public/framed/iphone/de/`, etc. Slide components use the current locale in the path: `src={`/framed/iphone/${locale}/iPhone-01_framed.png`}`. English (`en`) is the required default — all other languages are optional and fall back to English if the image is missing (via `onError` on the Device component).

### Device Component

Since FrameMe produces complete device-framed images (bezel + screenshot composited together), the device component is just an `<img>` tag — no CSS clipping, no screen offset calculations, no border-radius hacks:

```tsx
function Device({ src, alt, style }: {
  src: string; alt: string; style?: React.CSSProperties;
}) {
  return (
    <img
      src={src}
      alt={alt}
      style={style}
      draggable={false}
      onError={(e) => {
        // Fall back to English if localized image is missing
        const img = e.currentTarget;
        const enSrc = img.src.replace(/\/(?!en\/)[a-z]{2}\//, "/en/");
        if (img.src !== enSrc) img.src = enSrc;
      }}
    />
  );
}
```

The framed images already contain the device bezel with the Dynamic Island, rounded corners, and screen content composited pixel-perfectly. The transparent areas around the device allow it to sit naturally on any background. The `onError` fallback ensures missing locale-specific images gracefully degrade to English.

### Typography (Resolution-Independent)

All sizing relative to canvas width W (use `IPHONE_W` or `IPAD_W` depending on device):

| Element | Size | Weight | Line Height |
|---------|------|--------|-------------|
| Category label | `W * 0.028` | 600 (semibold) | default |
| Headline | `W * 0.09` to `W * 0.1` | 700 (bold) | 1.0 |
| Hero headline | `W * 0.1` | 700 (bold) | 0.92 |

### Device Placement Patterns

Vary across slides — NEVER use the same layout twice in a row:

**Centered device** (hero, single-feature):
```
bottom: 0, width: "82-86%", translateX(-50%) translateY(12-14%)
```

**Two devices layered** (comparison):
```
Back: left: "-8%", width: "65%", rotate(-4deg), opacity: 0.55
Front: right: "-4%", width: "82%", translateY(10%)
```

**Device + floating elements** (only if user provided component PNGs):
```
Cards should NOT block the device's main content.
Position at edges, slight rotation (2-5deg), drop shadows.
If distracting, push partially off-screen or make smaller.
```

### iPad-Specific Layout Notes

iPad screenshots have a **landscape-ish aspect ratio** (2064×2752, closer to 3:4 vs iPhone's ~1:2.2). This affects layouts:

- The device image is wider relative to the canvas — use **narrower widths** (70-78% instead of 82-86%) to avoid crowding
- **Captions may need to sit above the device** rather than beside it, since the wider device leaves less horizontal space
- Two-device layouts work best with **smaller scaling** and more overlap
- iPad's larger visible screen area means the app UI is more readable — lean into showing the content

### "More Features" Slide (Optional)

Dark/contrast background with app icon, headline ("And so much more."), and feature pills. Can include a "Coming Soon" section with dimmer pills.

## Step 6: Export

### Why html-to-image, NOT html2canvas

`html2canvas` breaks on CSS filters, gradients, drop-shadow, backdrop-filter, and complex clipping. `html-to-image` uses native browser SVG serialization — handles all CSS faithfully.

### Export Implementation

```typescript
import { toPng } from "html-to-image";

// CRITICAL: el must be the slide component's root div (position: relative),
// NOT the offscreen wrapper. Use ref on wrapper, then ref.firstElementChild.
// toPng must capture the element that owns the positioned children.
const wrapper = el.parentElement!;

// Before capture: move wrapper on-screen
wrapper.style.left = "0px";
wrapper.style.opacity = "1";
wrapper.style.zIndex = "-1";

const opts = { width: W, height: H, pixelRatio: 1, cacheBust: true };

// CRITICAL: Double-call trick — first warms up fonts/images, second produces clean output
await toPng(el, opts);
const dataUrl = await toPng(el, opts);

// After capture: move wrapper back off-screen
wrapper.style.left = "-9999px";
wrapper.style.opacity = "";
wrapper.style.zIndex = "";
```

Use `W = IPHONE_W, H = IPHONE_H` for iPhone slides and `W = IPAD_W, H = IPAD_H` for iPad slides.

**Offscreen container setup**: The wrapper div is `position: absolute; left: -9999px` with `fontFamily` set. The ref should resolve to the slide's root div inside it (via `firstElementChild`), not the wrapper itself:
```tsx
ref={(el) => { if (el?.firstElementChild) exportRefs.current.set(i, el.firstElementChild as HTMLDivElement); }}
```

### Key Rules

- **Double-call trick**: First `toPng()` loads fonts/images lazily. Second produces clean output. Without this, exports are blank.
- **On-screen for capture**: Temporarily move to `left: 0` before calling `toPng`.
- **Offscreen wrapper**: Use `position: absolute; left: -9999px` (not `fixed`). Do NOT set `width`/`height` on the wrapper — let the slide component define its own dimensions.
- **No resizing needed**: Each slide is already at the exact export resolution. No canvas scaling step.
- **Zip export (asc-client compatible)**: Two export buttons. "Export ({LOCALE})" exports the current language. "Export All Languages" loops through every locale (sets state, waits for re-render, captures). Both create a zip compatible with [asc-client](https://github.com/keremerkan/asc-client). Structure:
  ```
  en-US/APP_IPHONE_67/01_hero.png
  en-US/APP_IPAD_PRO_3GEN_129/01_hero.png
  de-DE/APP_IPHONE_67/01_hero.png
  ```
  Device type mapping: `iphone → APP_IPHONE_67`, `ipad → APP_IPAD_PRO_3GEN_129`. Each locale entry needs an `asc` field for the App Store Connect locale code (e.g. `{ code: "en", label: "English", asc: "en-US" }`). Files are ordered alphabetically so use zero-padded prefixes: `01_name.png`.
- **Single-click export**: Downloads individual PNGs with device in filename: `01-iphone-hero-en-1320x2868.png`.
- 300ms delay between sequential exports.
- Set `fontFamily` on the offscreen container.
- Use `String(index + 1).padStart(2, "0")` for numbering.

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| All slides look the same | Vary device position (center, left, right, two-device, no-device) |
| Decorative elements invisible | Increase size and opacity — better too visible than invisible |
| Copy is too complex | "One second at arm's length" test |
| Floating elements block the device | Move off-screen edges or above the device |
| Plain white/black background | Use gradients — even subtle ones add depth |
| Too cluttered | Remove floating elements, simplify to device + caption |
| Too simple/empty | Add larger decorative elements, floating items at edges |
| Headlines use "and" | Split into two slides or pick one idea |
| No visual contrast across slides | Mix light and dark backgrounds |
| Export is blank | Use double-call trick; move element on-screen before capture |
| Export has empty top, content at bottom | `toPng` must target the slide's root div (has `position: relative`), not the offscreen wrapper |
| FrameMe not installed | Build from source: clone repo, `swift build -c release`, copy binary to PATH |
| Framed image looks wrong | Ensure raw screenshot matches the bezel's screen resolution |
