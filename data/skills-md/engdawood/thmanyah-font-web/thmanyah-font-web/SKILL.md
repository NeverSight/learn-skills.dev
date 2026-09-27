---
name: thmanyah-font-web
description: Add the Thmanyah (ثمانية) Arabic font family to web projects via the @dawod/thmanyah-font-web npm package or CDN links, and download the raw .woff2 files when a project needs them locally. Use when the user mentions Thmanyah, ثمانية, @dawod/thmanyah-font-web, or wants Arabic webfonts (Thmanyah Sans, Thmanyah Serif Display, Thmanyah Serif Text) installed, downloaded, or used in HTML, CSS, React, Vue, Next.js, or any frontend stack.
---

# Thmanyah Font Web

Community web package for the Thmanyah (ثمانية) Arabic font family: **3 families × 5 weights = 15 fonts** (300/400/500/700/900), distributed as plain CSS `@font-face` rules. By default the font binaries stream from the jsDelivr CDN at runtime — nothing to download or bundle. The raw `.woff2` files are also individually fetchable if a project must host them itself (see [Downloading the font files](#downloading-the-font-files-agent-friendly)).

- npm package: `@dawod/thmanyah-font-web` (CSS only: `index.css`, `sans.css`, `serif-display.css`, `serif-text.css`)
- Live demo / visual reference: https://engdawod.github.io/thmanyah-font-web/

## Pick a path first

| | Use it online (default) | Download the files |
| --- | --- | --- |
| How | One `<link>` to the CDN stylesheet, or `npm install` | Fetch the 15 `.woff2` files into the project |
| Good for | Almost everything — websites, apps, demos, prototypes | Offline/air-gapped builds, no-external-request policies, desktop apps |
| Cost | Zero setup, ~1.2 MB streamed and cached by the browser | ~1.2 MB in the repo + you write/adapt the `@font-face` CSS |
| Catch | Needs network access to `cdn.jsdelivr.net` | Check the license before self-hosting (bottom of this file) |

Default to online unless the user asks for local files or the environment can't reach a CDN.

## Quick start (CDN — no install)

```html
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@dawod/thmanyah-font-web/index.css" />
```

`index.css` loads all three families. To load only one family, swap the filename: `sans.css`, `serif-display.css`, or `serif-text.css`. unpkg also works: `https://unpkg.com/@dawod/thmanyah-font-web/index.css`.

## Install with a package manager

```bash
npm install @dawod/thmanyah-font-web
```

```js
// JS/TS entry (Vite, webpack, Next.js, …) — all families
import "@dawod/thmanyah-font-web";

// or just one family
import "@dawod/thmanyah-font-web/sans.css";
```

```css
/* Inside a CSS file */
@import "@dawod/thmanyah-font-web";
```

## Using the fonts

Font-family names — always quoted (they contain spaces), always with a fallback:

| Family | CSS `font-family` | Best for |
| --- | --- | --- |
| Thmanyah Sans | `"Thmanyah Sans", sans-serif` | UI, body text |
| Thmanyah Serif Display | `"Thmanyah Serif Display", serif` | Headlines, large titles |
| Thmanyah Serif Text | `"Thmanyah Serif Text", serif` | Long-form reading |

Weights: `300` Light · `400` Regular · `500` Medium · `700` Bold · `900` Black. Set them numerically (`font-weight: 500`) — the keywords `normal`/`bold` only reach 400/700.

```css
body {
  font-family: "Thmanyah Sans", sans-serif;
  font-weight: 400;
}
h1, h2 {
  font-family: "Thmanyah Serif Display", serif;
  font-weight: 700;
}
article p {
  font-family: "Thmanyah Serif Text", serif;
}
```

## Utility classes (available once the CSS is loaded)

- Families: `.font-thmanyah-sans`, `.font-thmanyah-serif-display`, `.font-thmanyah-serif-text`
- Weights: `.font-weight-light` (300), `.font-weight-regular` (400), `.font-weight-medium` (500), `.font-weight-bold` (700), `.font-weight-black` (900)

```html
<h1 class="font-thmanyah-serif-display font-weight-black">عنوان رئيسي</h1>
```

## The full set — all 15 fonts

Every family ships the same five weights. File names follow one pattern:

```
fonts/<family-slug>/woff2/<family-slug>-<Weight>.woff2
```

- `<family-slug>` — `thmanyah-sans` · `thmanyah-serif-display` · `thmanyah-serif-text`
- `<Weight>` — `Light` (300) · `Regular` (400) · `Medium` (500) · `Bold` (700) · `Black` (900)

| # | Family | Weight | File |
| --- | --- | --- | --- |
| 1 | Thmanyah Sans | 300 | `thmanyah-sans/woff2/thmanyah-sans-Light.woff2` |
| 2 | Thmanyah Sans | 400 | `thmanyah-sans/woff2/thmanyah-sans-Regular.woff2` |
| 3 | Thmanyah Sans | 500 | `thmanyah-sans/woff2/thmanyah-sans-Medium.woff2` |
| 4 | Thmanyah Sans | 700 | `thmanyah-sans/woff2/thmanyah-sans-Bold.woff2` |
| 5 | Thmanyah Sans | 900 | `thmanyah-sans/woff2/thmanyah-sans-Black.woff2` |
| 6 | Thmanyah Serif Display | 300 | `thmanyah-serif-display/woff2/thmanyah-serif-display-Light.woff2` |
| 7 | Thmanyah Serif Display | 400 | `thmanyah-serif-display/woff2/thmanyah-serif-display-Regular.woff2` |
| 8 | Thmanyah Serif Display | 500 | `thmanyah-serif-display/woff2/thmanyah-serif-display-Medium.woff2` |
| 9 | Thmanyah Serif Display | 700 | `thmanyah-serif-display/woff2/thmanyah-serif-display-Bold.woff2` |
| 10 | Thmanyah Serif Display | 900 | `thmanyah-serif-display/woff2/thmanyah-serif-display-Black.woff2` |
| 11 | Thmanyah Serif Text | 300 | `thmanyah-serif-text/woff2/thmanyah-serif-text-Light.woff2` |
| 12 | Thmanyah Serif Text | 400 | `thmanyah-serif-text/woff2/thmanyah-serif-text-Regular.woff2` |
| 13 | Thmanyah Serif Text | 500 | `thmanyah-serif-text/woff2/thmanyah-serif-text-Medium.woff2` |
| 14 | Thmanyah Serif Text | 700 | `thmanyah-serif-text/woff2/thmanyah-serif-text-Bold.woff2` |
| 15 | Thmanyah Serif Text | 900 | `thmanyah-serif-text/woff2/thmanyah-serif-text-Black.woff2` |

Each woff2 is ~72–83 KB; all 15 together ~1.2 MB. Only woff2 is distributed (covers every modern browser); the OTF originals are not published anywhere — get them from https://font.thmanyah.com if the user needs desktop/print files.

## Downloading the font files (agent-friendly)

**Prefer the CDN stylesheet above.** Only download binaries when the project genuinely cannot hit a CDN — offline builds, air-gapped environments, or a self-hosting requirement (and see the license note at the bottom before self-hosting).

Base URL — pinned to a commit, so it never changes underneath you:

```
https://cdn.jsdelivr.net/gh/engdawood/thmanyah-font-web@4266a9d/fonts/<family-slug>/woff2/<family-slug>-<Weight>.woff2
```

Single file:

```bash
curl -fL -o thmanyah-sans-Regular.woff2 \
  "https://cdn.jsdelivr.net/gh/engdawood/thmanyah-font-web@4266a9d/fonts/thmanyah-sans/woff2/thmanyah-sans-Regular.woff2"
```

All 15, into a local `fonts/` tree that mirrors the CDN layout:

```bash
BASE="https://cdn.jsdelivr.net/gh/engdawood/thmanyah-font-web@4266a9d/fonts"
for fam in thmanyah-sans thmanyah-serif-display thmanyah-serif-text; do
  mkdir -p "fonts/$fam/woff2"
  for w in Light Regular Medium Bold Black; do
    curl -fL -o "fonts/$fam/woff2/$fam-$w.woff2" "$BASE/$fam/woff2/$fam-$w.woff2"
  done
done
```

PowerShell:

```powershell
$base = "https://cdn.jsdelivr.net/gh/engdawood/thmanyah-font-web@4266a9d/fonts"
foreach ($fam in "thmanyah-sans","thmanyah-serif-display","thmanyah-serif-text") {
  New-Item -ItemType Directory -Force "fonts/$fam/woff2" | Out-Null
  foreach ($w in "Light","Regular","Medium","Bold","Black") {
    Invoke-WebRequest "$base/$fam/woff2/$fam-$w.woff2" -OutFile "fonts/$fam/woff2/$fam-$w.woff2"
  }
}
```

After downloading, verify each file is a real font, not an HTML error page: size should be ~72–83 KB and the first four bytes are `wOF2`.

Then point `@font-face` at the local copies (one block per weight — 15 total):

```css
@font-face {
  font-family: "Thmanyah Sans";
  src: url("/fonts/thmanyah-sans/woff2/thmanyah-sans-Regular.woff2") format("woff2");
  font-weight: 400;
  font-style: normal;
  font-display: swap;
}
```

Faster path: copy the package's own `index.css` and rewrite the CDN prefix to your local path.

```bash
curl -fL "https://cdn.jsdelivr.net/npm/@dawod/thmanyah-font-web/index.css" \
  | sed 's|https://cdn.jsdelivr.net/gh/engdawood/thmanyah-font-web@4266a9d/fonts|/fonts|g' > thmanyah.css
```

Humans can also grab per-weight or per-family zips from the download section of the demo page: https://engdawood.com/ar/projects/thmanyah-fonts-web/

## Arabic / RTL checklist

- Set `lang="ar"` and `dir="rtl"` on `<html>` (or `direction: rtl` in CSS) for Arabic content.
- The CSS already includes `font-display: swap` and Arabic + Latin `unicode-range` — no extra configuration.
- When linking the stylesheet, don't hand-write `@font-face` rules; the package's CDN-pinned ones already cover all 15 fonts. Build font-file URLs only when deliberately downloading, and only from the pinned base URL above.

## Verify it works

1. Load the page → devtools Network tab → filter `woff2`: the requests should return 200 — from `cdn.jsdelivr.net` when online, or from your own `/fonts/` path when self-hosted (a 404 here means the local paths are wrong).
2. Inspect rendered text: the computed `font-family` should be the Thmanyah family, not the fallback.
3. Switch weights (300 → 900) and confirm the rendering actually changes — if every weight looks the same, a `@font-face` block is missing or its `font-weight` is wrong.
