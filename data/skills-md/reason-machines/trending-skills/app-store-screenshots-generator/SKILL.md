---
name: app-store-screenshots-generator
description: Generate production-ready App Store screenshots for iOS apps using AI agents, Next.js, and html-to-image
triggers:
  - build app store screenshots
  - generate marketing screenshots for my iOS app
  - create exportable screenshot assets for the app store
  - make app store screenshots with AI
  - generate promotional screenshots for my iPhone app
  - create app store marketing images
  - build screenshot generator for iOS app
  - automate app store screenshot creation
---

# App Store Screenshots Generator

> Skill by [ara.so](https://ara.so) — Daily 2026 Skills collection.

A skill for AI coding agents (Claude Code, Cursor, Windsurf, Codex, etc.) that generates production-ready App Store screenshots for iOS apps. It scaffolds a Next.js project, designs advertisement-style slides, and exports PNGs at all required Apple resolutions.

## What This Skill Does

- Asks about your app's brand, features, and style preferences before building anything
- Scaffolds a minimal Next.js + TypeScript + Tailwind project
- Designs each screenshot as an **advertisement** (not a UI showcase)
- Writes compelling copy using proven App Store copywriting patterns
- Renders screenshots with a built-in iPhone mockup frame
- Exports PNGs at all 4 Apple-required sizes (6.9", 6.5", 6.3", 6.1")
- Supports multi-locale screenshot sets, RTL-aware layouts, and reusable theme presets

## Install

### Using npx skills (recommended)

```bash
# Install for current project
npx skills add ParthJadhav/app-store-screenshots

# Install globally (available across all projects)
npx skills add ParthJadhav/app-store-screenshots -g

# Install for a specific agent
npx skills add ParthJadhav/app-store-screenshots -a claude-code
```

### Manual install

```bash
git clone https://github.com/ParthJadhav/app-store-screenshots ~/.claude/skills/app-store-screenshots
```

## Usage

Once installed, just describe what you need:

```
> Build App Store screenshots for my habit tracker.
  The app helps people stay consistent with simple daily routines.
  I want 6 slides, clean/minimal style, warm neutrals, and a calm premium feel.
```

The agent will ask clarifying questions about brand colors, fonts, features, style direction, number of slides, and locales before generating anything.

## Project Structure

The skill scaffolds this layout:

```
project/
├── public/
│   ├── mockup.png              # iPhone frame with transparent screen area
│   ├── app-icon.png            # Your app icon
│   ├── screenshots/            # App screenshots (optionally nested by locale)
│   │   ├── en/
│   │   ├── de/
│   │   └── ar/
│   └── screenshots-ipad/       # Optional iPad screenshots
├── src/app/
│   ├── layout.tsx              # Font setup
│   └── page.tsx                # Entire screenshot generator (single file)
├── package.json
└── next.config.ts
```

**The entire generator lives in a single `page.tsx` file.** Run the dev server, open the browser, and click any screenshot to export it as a PNG.

## Core page.tsx Pattern

```tsx
// src/app/page.tsx — minimal scaffold pattern
"use client";

import { toPng } from "html-to-image";
import { useRef, useState } from "react";

// --- Design tokens / theme presets ---
const THEMES = {
  "clean-light": {
    bg: "#F6F1EA",
    fg: "#171717",
    accent: "#5B7CFA",
    font: "Inter",
  },
  "dark-bold": {
    bg: "#0B1020",
    fg: "#F8FAFC",
    accent: "#8B5CF6",
    font: "Inter",
  },
  "warm-editorial": {
    bg: "#F7E8DA",
    fg: "#2B1D17",
    accent: "#D97706",
    font: "Playfair Display",
  },
} as const;

type ThemeKey = keyof typeof THEMES;

// --- Export sizes (width x height in px) ---
const EXPORT_SIZES = {
  "6.9": { w: 1320, h: 2868 },
  "6.5": { w: 1284, h: 2778 },
  "6.3": { w: 1206, h: 2622 },
  "6.1": { w: 1125, h: 2436 },
} as const;

// --- Slide data ---
const SLIDES = [
  {
    id: 1,
    headline: "Track Every Habit,\nEvery Day",
    subheadline: "Build streaks that stick",
    screenshot: "/screenshots/en/home.png",
    layout: "phone-right", // varies per slide: phone-left | phone-right | phone-center
  },
  {
    id: 2,
    headline: "See Your Progress\nAt a Glance",
    subheadline: "Beautiful weekly summaries",
    screenshot: "/screenshots/en/stats.png",
    layout: "phone-left",
  },
  // ... more slides
];

// --- Screenshot canvas (designed at 6.9" — 1320x2868) ---
function ScreenshotSlide({
  slide,
  theme,
  slideRef,
}: {
  slide: (typeof SLIDES)[0];
  theme: (typeof THEMES)[ThemeKey];
  slideRef: React.RefObject<HTMLDivElement>;
}) {
  return (
    <div
      ref={slideRef}
      style={{
        width: 1320,
        height: 2868,
        background: theme.bg,
        color: theme.fg,
        fontFamily: theme.font,
        position: "relative",
        overflow: "hidden",
      }}
    >
      {/* Headline */}
      <div
        style={{
          position: "absolute",
          top: 180,
          left: 80,
          right: 80,
          fontSize: 96,
          fontWeight: 800,
          lineHeight: 1.1,
          whiteSpace: "pre-line",
        }}
      >
        {slide.headline}
      </div>

      {/* Subheadline */}
      <div
        style={{
          position: "absolute",
          top: 520,
          left: 80,
          fontSize: 48,
          color: theme.accent,
          fontWeight: 500,
        }}
      >
        {slide.subheadline}
      </div>

      {/* iPhone mockup + app screenshot */}
      <div
        style={{
          position: "absolute",
          bottom: 0,
          right: slide.layout === "phone-right" ? 0 : "auto",
          left: slide.layout === "phone-left" ? 0 : "auto",
        }}
      >
        {/* App screenshot inside mockup */}
        <div style={{ position: "relative", width: 660, height: 1430 }}>
          <img
            src={slide.screenshot}
            style={{
              position: "absolute",
              top: 28,
              left: 24,
              width: 612,
              borderRadius: 52,
            }}
            alt=""
          />
          {/* Mockup frame sits on top */}
          <img
            src="/mockup.png"
            style={{ position: "absolute", inset: 0, width: "100%" }}
            alt=""
          />
        </div>
      </div>
    </div>
  );
}

// --- Export helper ---
async function exportSlide(
  ref: React.RefObject<HTMLDivElement>,
  slideId: number,
  size: keyof typeof EXPORT_SIZES,
  locale: string,
  themeName: string
) {
  if (!ref.current) return;

  const { w, h } = EXPORT_SIZES[size];
  const scale = w / 1320; // designed at 1320px wide

  const dataUrl = await toPng(ref.current, {
    width: w,
    height: h,
    style: { transform: `scale(${scale})`, transformOrigin: "top left" },
  });

  const link = document.createElement("a");
  link.download = `slide-${slideId}-${locale}-${themeName}-${size}in.png`;
  link.href = dataUrl;
  link.click();
}

// --- Main page ---
export default function ScreenshotGenerator() {
  const [activeTheme, setActiveTheme] = useState<ThemeKey>("clean-light");
  const [activeLocale, setActiveLocale] = useState("en");
  const slideRefs = useRef<React.RefObject<HTMLDivElement>[]>(
    SLIDES.map(() => ({ current: null } as React.RefObject<HTMLDivElement>))
  );

  const theme = THEMES[activeTheme];

  return (
    <div style={{ padding: 40, background: "#111", minHeight: "100vh" }}>
      {/* Controls */}
      <div style={{ display: "flex", gap: 16, marginBottom: 40 }}>
        {(Object.keys(THEMES) as ThemeKey[]).map((t) => (
          <button
            key={t}
            onClick={() => setActiveTheme(t)}
            style={{
              padding: "8px 16px",
              background: activeTheme === t ? "#fff" : "#333",
              color: activeTheme === t ? "#000" : "#fff",
              border: "none",
              borderRadius: 8,
              cursor: "pointer",
            }}
          >
            {t}
          </button>
        ))}

        {/* Bulk export all slides at all sizes */}
        <button
          onClick={async () => {
            for (const [i, slide] of SLIDES.entries()) {
              for (const size of Object.keys(EXPORT_SIZES) as (keyof typeof EXPORT_SIZES)[]) {
                await exportSlide(
                  slideRefs.current[i],
                  slide.id,
                  size,
                  activeLocale,
                  activeTheme
                );
              }
            }
          }}
          style={{
            padding: "8px 16px",
            background: theme.accent,
            color: "#fff",
            border: "none",
            borderRadius: 8,
            cursor: "pointer",
            marginLeft: "auto",
          }}
        >
          Export All
        </button>
      </div>

      {/* Slides */}
      <div style={{ display: "flex", flexDirection: "column", gap: 40 }}>
        {SLIDES.map((slide, i) => (
          <div key={slide.id}>
            <ScreenshotSlide
              slide={slide}
              theme={theme}
              slideRef={slideRefs.current[i]}
            />
            {/* Per-slide export buttons */}
            <div style={{ display: "flex", gap: 8, marginTop: 12 }}>
              {(Object.keys(EXPORT_SIZES) as (keyof typeof EXPORT_SIZES)[]).map(
                (size) => (
                  <button
                    key={size}
                    onClick={() =>
                      exportSlide(
                        slideRefs.current[i],
                        slide.id,
                        size,
                        activeLocale,
                        activeTheme
                      )
                    }
                    style={{
                      padding: "6px 12px",
                      background: "#222",
                      color: "#fff",
                      border: "1px solid #444",
                      borderRadius: 6,
                      cursor: "pointer",
                      fontSize: 13,
                    }}
                  >
                    Export {size}"
                  </button>
                )
              )}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
```

## Multi-Locale Setup

Organize screenshots under locale folders and swap the base path:

```
public/screenshots/
├── en/home.png
├── de/home.png
└── ar/home.png   ← RTL locale
```

```tsx
// Locale-aware copy dictionary
const COPY: Record<string, Record<number, { headline: string; subheadline: string }>> = {
  en: {
    1: { headline: "Track Every Habit,\nEvery Day", subheadline: "Build streaks that stick" },
    2: { headline: "See Your Progress\nAt a Glance", subheadline: "Beautiful weekly summaries" },
  },
  de: {
    1: { headline: "Jede Gewohnheit\nIm Blick", subheadline: "Baue Serien auf, die halten" },
    2: { headline: "Fortschritt auf\neinen Blick", subheadline: "Wöchentliche Übersichten" },
  },
  ar: {
    1: { headline: "تتبع كل عادة\nكل يوم", subheadline: "ابنِ سلاسل تدوم" },
    2: { headline: "اطّلع على تقدمك\nدفعة واحدة", subheadline: "ملخصات أسبوعية جميلة" },
  },
};

// RTL-aware canvas wrapper
function LocaleCanvas({ locale, children }: { locale: string; children: React.ReactNode }) {
  const isRTL = ["ar", "he", "fa"].includes(locale);
  return (
    <div dir={isRTL ? "rtl" : "ltr"} style={{ textAlign: isRTL ? "right" : "left" }}>
      {children}
    </div>
  );
}
```

## Dependencies (package.json)

```json
{
  "dependencies": {
    "next": "^14.0.0",
    "react": "^18.0.0",
    "react-dom": "^18.0.0",
    "html-to-image": "^1.11.11"
  },
  "devDependencies": {
    "typescript": "^5.0.0",
    "@types/react": "^18.0.0",
    "@types/node": "^20.0.0",
    "tailwindcss": "^3.4.0",
    "autoprefixer": "^10.4.0",
    "postcss": "^8.4.0"
  }
}
```

## Starting the Dev Server

The skill auto-detects your package manager (bun preferred):

```bash
# bun (preferred)
bun install && bun dev

# pnpm
pnpm install && pnpm dev

# yarn
yarn && yarn dev

# npm
npm install && npm run dev
```

Then open [http://localhost:3000](http://localhost:3000) to view the screenshot generator.

## Export Sizes Reference

| Display | Width | Height | Notes |
|---------|-------|--------|-------|
| 6.9" | 1320px | 2868px | Design base size |
| 6.5" | 1284px | 2778px | Scale: 0.973 |
| 6.3" | 1206px | 2622px | Scale: 0.914 |
| 6.1" | 1125px | 2436px | Scale: 0.852 |

> **Note:** Use a 6.1" simulator to capture your initial app screenshots — this avoids resolution adjustments later.

## Design Principles the Agent Follows

1. **Screenshots are ads, not docs** — each slide sells one idea
2. **One-second rule** — headline must be readable at App Store thumbnail size
3. **Vary layouts** — no two adjacent slides share the same phone placement (`phone-left` / `phone-right` / `phone-center`)
4. **Style is user-driven** — no hardcoded colors; everything flows from theme tokens
5. **First slide = strongest benefit** — not the most complex feature

## Quality Checklist

Before exporting, verify each slide:

- [ ] Headline communicates exactly one idea in ~1 second
- [ ] First slide leads with the strongest user benefit (not a feature)
- [ ] Adjacent slides use different phone placement layouts
- [ ] Decorative elements support the message, not obscure the UI
- [ ] Text and framing look correct after scaling to smallest export size (6.1")
- [ ] RTL locales have `dir="rtl"` set and layouts feel native (not mechanically mirrored)

## Example Prompts

```text
# Habit tracker
Build App Store screenshots for my habit tracker.
The app helps people stay consistent with simple daily routines.
I want 6 slides, clean/minimal style, warm neutrals, and a calm premium feel.

# Finance app
Generate App Store screenshots for my personal finance app.
Main strengths: fast expense capture, clear monthly trends, shared budgets.
Sharp modern style, high contrast, 7 slides.

# Multi-locale + themes
Build App Store screenshots for my language learning app.
I need English, German, and Arabic screenshot sets.
Use two themes: clean-light and dark-bold.
Make Arabic slides feel RTL-native, not just translated.
```

## Troubleshooting

**html-to-image exports blank or white images**
- Ensure all images are served from `/public` (same origin). Cross-origin images block canvas export.
- Add `crossOrigin="anonymous"` to `<img>` tags if loading from a CDN.
- Check the browser console for CORS errors.

**Mockup frame not aligning with screenshot**
- The included `mockup.png` has pre-measured transparent screen area. Use `position: absolute` with the app screenshot behind the frame, not inside it.
- Use `top: 28px, left: 24px` as the starting offset for a 660px-wide mockup.

**Export scaling looks blurry**
- Always design at 1320×2868 (6.9" base) and scale down — never design small and scale up.
- Pass explicit `width` and `height` to `toPng()` with the correct scale transform.

**Font not loading in exports**
- Load fonts via `next/font` or a `<style>` tag inside the canvas div, not just in `layout.tsx`.
- Call `document.fonts.ready` before triggering `toPng()`.

```tsx
// Wait for fonts before export
await document.fonts.ready;
const dataUrl = await toPng(ref.current, { width: w, height: h });
```

**Simulator screenshots wrong resolution**
- Always capture from the **6.1" simulator** as the starting point to minimize later adjustments.

## Requirements

- Node.js 18+
- One of: bun, pnpm, yarn, or npm
- Claude Code, Cursor, Windsurf, Codex, or any agent that reads skill files
