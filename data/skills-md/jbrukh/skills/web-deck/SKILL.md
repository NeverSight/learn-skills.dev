---
name: web-deck
description: "Build CoinFund-branded web presentations as self-contained HTML files. Supports static (print/PDF) and dynamic (keyboard nav, transitions) modes. Outputs a single versionable HTML file with optional PDF export via Puppeteer. Trigger on: 'web deck', 'web slides', 'html presentation', 'web presentation', or any request for a browser-based slide deck."
---

# Web Deck — CoinFund Web Presentation Builder

Build minimalist, CoinFund-branded slide decks as self-contained HTML files. Each deck is a single `.html` file — no build step, no dependencies, trivially versionable in Git.

## When to Use

Any time the user wants a **web-based** slide deck (HTML/CSS/JS). For `.pptx` output, use the `jake-deck` skill instead. This skill is for browser-native presentations that can also export to PDF.

The user specifies:
1. **Mode**: `static` (print-optimized, no JS) or `dynamic` (keyboard navigation, slide transitions). Default: `dynamic`.
2. **Content**: Slide titles and content, as an outline or bullet points.

## Design System

### Color Palette (CSS Custom Properties)

```css
:root {
  --bg:      #F7F3EE;  /* Warm cream — all slide backgrounds        */
  --text:    #1A1A1A;  /* Near-black — headings, primary body text   */
  --gray:    #7A7A7A;  /* Secondary text, labels                     */
  --ltgray:  #C8C2BA;  /* Divider rules, subtle borders              */
  --white:   #FFFFFF;  /* Title slide background, table headers      */
  --red:     #C0392B;  /* Warnings, risks, negative indicators       */
  --green:   #27AE60;  /* Positive indicators, "ready" status        */
  --blue:    #2C3E50;  /* Section headers, callout boxes             */
}
```

### Typography

All text uses **Nunito** (loaded from Google Fonts, with system-font fallback for offline use).

| Element          | Size   | Weight | Color      |
|------------------|--------|--------|------------|
| Slide title      | 28px   | 700    | `--blue`   |
| Section header   | 16px   | 700    | `--text`   |
| Body text        | 13px   | 400    | `--text`   |
| Labels/secondary | 11px   | 400    | `--gray`   |
| Footnotes        | 10-11px| 400    | `--red` or `--gray` |

### Layout

Slides are **16:9** aspect ratio (960px x 540px base, scaled to fill viewport).

```
┌──────────────────────────────────────────────┐
│  padding-left: 76px (~0.8" equivalent)       │
│  ┌─ Title zone: top 50px ──────────────────┐ │
│  │                                          │ │
│  ├─ Content zone: top 110px ───────────────┤ │
│  │  width: 808px (~8.4" equivalent)        │ │
│  │                                          │ │
│  ├─ Footnote zone: bottom 30px ────────────┤ │
│  └──────────────────────────────────────────┘ │
└──────────────────────────────────────────────┘
```

## Required Slides

### Title Slide (always first)

- Background: `--white` (#FFFFFF), not cream
- CoinFund logo: text wordmark "CoinFund" in 52px Arial bold, color `--text`, centered
- Thin divider line below wordmark: 240px wide, `--text`, centered
- Deck title: 28px Nunito bold, color `--blue`, centered below divider
- Subtitle/date: 14px Nunito, color `--gray`, centered

```html
<section class="slide slide--title">
  <div class="slide__wordmark">CoinFund</div>
  <hr class="slide__divider slide__divider--title">
  <h1 class="slide__deck-title">Deck Title Here</h1>
  <p class="slide__subtitle">March 2026</p>
</section>
```

### End Slide (always last)

- Background: `--bg` (cream)
- "CoinFund" in 36px Nunito bold, color `--blue`, centered
- Gray divider rule centered
- "coinfund.io" in 13px Nunito, color `--gray`, centered

```html
<section class="slide slide--end">
  <div class="slide__end-wordmark">CoinFund</div>
  <hr class="slide__divider slide__divider--end">
  <p class="slide__end-url">coinfund.io</p>
</section>
```

## Content Slide Patterns

Every content slide follows this HTML structure:

```html
<section class="slide">
  <h2 class="slide__title">Slide Title</h2>
  <hr class="slide__accent">
  <div class="slide__body">
    <!-- Content using one of the patterns below -->
  </div>
  <!-- Optional footnote -->
  <footer class="slide__footnote">Footnote text</footer>
</section>
```

### Pattern 1: Header + Body Blocks (default, most common)

For slides with 3-5 topics, each with bold header and description.

```html
<div class="block">
  <div class="block__header">Bold header text</div>
  <div class="block__body">Gray body description text.</div>
</div>
<!-- Repeat for each block. Max 4-5 per slide. -->
```

### Pattern 2: Label-Value Grid

Two-column layout: gray labels left, text values right.

```html
<div class="kv-grid">
  <div class="kv-grid__row">
    <span class="kv-grid__label">Label</span>
    <span class="kv-grid__value">Value text here</span>
  </div>
  <!-- Max 6 rows per slide -->
</div>
```

### Pattern 3: Table

Blue header row with white text, alternating cream/white body rows.

```html
<table class="deck-table">
  <thead>
    <tr><th>Column A</th><th>Column B</th><th>Column C</th></tr>
  </thead>
  <tbody>
    <tr><td>Data</td><td>Data</td><td>Data</td></tr>
    <tr><td>Data</td><td>Data</td><td>Data</td></tr>
  </tbody>
</table>
```

### Pattern 4: Numbered List

Blue number + bold label + body inline.

```html
<ol class="numbered-list">
  <li>
    <span class="numbered-list__label">Item name</span>
    <span class="numbered-list__desc">Description text explaining the item.</span>
  </li>
</ol>
```

### Pattern 5: Callout Box

Light blue-gray fill with left border accent.

```html
<div class="callout">
  <p>Key insight or important note goes here.</p>
</div>
```

## Entrance Animations

In dynamic mode, add `class="reveal"` to any element that should animate in when its slide becomes active. Elements fade up with staggered timing based on their position among siblings.

```html
<section class="slide">
  <h2 class="slide__title reveal">Title animates first</h2>
  <hr class="slide__accent reveal">
  <div class="slide__body">
    <div class="block reveal">This block animates third</div>
    <div class="block reveal">This one fourth (0.08s delay)</div>
  </div>
</section>
```

In static mode, `reveal` has no effect — elements render normally.

## Static vs. Dynamic Mode

### Static Mode (`data-mode="static"`)

- No JavaScript whatsoever
- All slides visible in sequence, separated by CSS page breaks
- Optimized for `Cmd+P` / `Ctrl+P` browser print or Puppeteer PDF export
- Each `<section class="slide">` gets `page-break-after: always`

### Dynamic Mode (`data-mode="dynamic"`)

- Keyboard navigation: Arrow keys, Space, Page Up/Down
- Touch/swipe navigation on mobile and tablet
- Current slide indicator (e.g., "3 / 12") in bottom-right
- Blue progress bar at top of viewport
- Subtle fade transitions between slides (CSS `opacity` + `transition`)
- Staggered entrance animations on `.reveal` elements
- URL hash updates per slide (`#slide-3`) for deep linking
- Press `F` for fullscreen, `Esc` to exit
- Press `P` to toggle overview mode (shows all slides, click to jump)
- `prefers-reduced-motion` automatically disables animations

## HTML Template

The file `template.html` (in the same directory as this SKILL.md) is the complete, working boilerplate for every deck. It includes all CSS (design tokens, patterns 1-5, animations, static/dynamic modes, print styles) and all JS (keyboard/touch nav, overview mode, fullscreen, progress bar, hash deep linking).

### Creating a new deck

Copy the template to start every new deck:

```bash
cp <skill-dir>/template.html deck.html
```

Then:
1. Set `data-mode` on `<html>` to `"dynamic"` or `"static"`
2. Replace `DECK_TITLE_HERE` in `<title>` and `.slide__deck-title`
3. Replace `MONTH YEAR` in `.slide__subtitle`
4. Add content slides between the title and end slides, using the content patterns documented above

**Do not regenerate the boilerplate from memory.** Always copy the template file.

## Live Development Server (MANDATORY)

**ALWAYS serve decks through the dev server.** Never open deck files directly via `file://` — the server provides live reload, the hamburger overlay menu, and PDF export. Without it, the user gets a static file with no interactivity tools.

The dev server is at `serve-deck.mjs` (same directory as this SKILL.md). Zero npm dependencies (Puppeteer auto-installed on first PDF export).

### Starting the server

```bash
node /path/to/skills/web-deck/serve-deck.mjs 3333 /path/to/deck/directory
```

Then open the browser:
```bash
open http://localhost:3333/deck.html
```

**Start the server BEFORE opening the browser.** Use `run_in_background: true` so it persists across edits.

### What the server provides

1. **Live reload** — SSE-based, auto-reloads the browser on every file save. The user sees changes instantly as you edit slides.
2. **Hamburger overlay menu** — always-visible hamburger icon (☰) in the top-right corner with:
   - **Download as PDF** — Puppeteer renders the deck server-side at 960×540px per slide, producing a faithful PDF with all fonts and styles intact. Auto-installs Puppeteer on first use.
   - **⌘P hint** — reminder that browser print also works
3. **Static file serving** — serves the deck and any local assets (images, fonts)

The overlay menu and reload client are **injected at serve time** — they do not exist in the `deck.html` file itself. The deck stays clean and self-contained. This is why the server is mandatory: without it, no hamburger menu, no PDF export, no live reload.

### Workflow

1. User provides outline (slide titles + content bullets) and mode preference (static/dynamic)
2. Copy the template: `cp <skill-dir>/template.html deck.html`
3. Set the mode, title, and subtitle in the copied file
4. Choose the right content pattern for each slide and add content slides
5. **Start the server** (background, one time): `node <skill-dir>/serve-deck.mjs 3333 .` with `run_in_background: true`
6. **Open in browser** (one time): `open http://localhost:3333/deck.html`
7. **Iterate** — use the Edit tool to modify slides. The browser auto-reloads on every save.
8. User clicks the **hamburger menu → Download as PDF** when ready.

### Important: keep the server running

- Start the server with `run_in_background: true` so it persists across edits
- The second argument is the directory to serve (defaults to `.`)
- The server stays alive for the session — no auto-shutdown
- When the session ends or user is done, kill the server: `pkill -f serve-deck` or let it die naturally

## Style Principles

The CoinFund deck style is defined by restraint:

1. **No gradients, drop shadows, or decorative elements.** The CSS `box-shadow` on slides is only for the browser viewport framing, not part of the slide content itself.
2. **Color is semantic.** Blue for structure, red for risk/warnings, green for readiness/positive. Never decorative.
3. **Whitespace does the heavy lifting.** Generous padding, clear spacing between blocks. If it feels crowded, split into two slides.
4. **Max 4-5 content blocks per slide.** Prevents overflow and keeps slides scannable.
5. **Footnotes sit below main content** with a clear gap. Use `slide__footnote` positioned at the bottom.
6. **One accent line per slide.** The short `slide__accent` `<hr>` separates title from content. That's the only decoration.
7. **Terse over verbose.** Bullets should be 1-2 sentences max. The deck is a conversation starter, not a whitepaper.
8. **Uniform style changes.** When the user makes a visual or stylistic change to one slide, apply that change consistently across all slides in the deck.

## Incremental Editing

The live server makes editing feel like a REPL — edit the file, see the result immediately.

Because the deck is a single HTML file:

- **Git-friendly**: each slide is a `<section>` block, so diffs are clean and meaningful
- **Add slides**: insert new `<section class="slide">` blocks between existing ones
- **Reorder**: cut/paste `<section>` blocks
- **Edit content**: modify text within existing sections
- **Style tweaks**: adjust CSS custom properties in `:root` for global changes

When the user asks to edit specific slides, use the Edit tool to modify just the relevant `<section>` blocks. Do not regenerate the entire file for small changes. The live server will auto-reload on every save.

## Overflow Prevention

- **5 blocks max** per slide (Pattern 1)
- **6 rows max** per label-value grid (Pattern 2)
- **7 table rows max** (including header)
- **Footnotes** anchored to `bottom: 20px` via absolute positioning
- If content won't fit, **split into two slides** — never shrink fonts below 10px
