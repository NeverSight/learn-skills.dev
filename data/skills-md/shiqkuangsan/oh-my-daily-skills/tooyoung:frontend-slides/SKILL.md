---
name: tooyoung:frontend-slides
description: "Create viewport-fitted HTML slide presentations with 8 curated visual themes. Single-file output, system font fallbacks, scroll-snap navigation. Trigger: make slides, create presentation, 做 PPT, 做幻灯片, slidedeck, pitch deck, HTML slides"
metadata:
  version: "1.0.1"
---

# Frontend Slides

Create beautiful, single-file HTML slide presentations. Each slide fills exactly one viewport — no scrolling within slides, no build tools, no frameworks. Inspired by [zarazhangrui/frontend-slides](https://github.com/zarazhangrui/frontend-slides).

**Output:** One `.html` file containing all CSS, JS, and slide content inline.

**Font strategy:** Every theme specifies a Google Fonts / Fontshare web font AND a system font fallback stack. Web fonts enhance — they are **not required**. Presentations must look good offline.

> **Reference files** contain complete code templates. Load them on-demand — only read what you need for the current task.

## Core Principles

1. **One slide = one viewport.** `100dvh`, `overflow: hidden`, `scroll-snap-align: start`. Content that overflows → split into more slides.
2. **All sizes use `clamp()`.** No fixed `px`/`rem` for typography or spacing. Everything scales with the viewport.
3. **Content density limits are hard rules.** See the table below — never exceed them.
4. **Single-file output.** Fonts via CDN `<link>`, everything else inline. No external CSS/JS files.
5. **Respect `prefers-reduced-motion`.** All animations must have a reduced-motion fallback.

## Viewport Fitting (Single Source of Truth)

This section is THE authority on viewport rules. Reference files do not repeat these — they assume this CSS is always present.

### Required Base CSS

```css
*,
*::before,
*::after {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

html {
  scroll-snap-type: y mandatory;
  scroll-behavior: smooth;
  height: 100%;
}

body {
  font-family: var(--font-body);
  background: var(--bg-primary);
  color: var(--text-primary);
  overflow-x: hidden;
  height: 100%;
}

.slide {
  width: 100vw;
  height: 100vh;
  height: 100dvh;
  overflow: hidden;
  scroll-snap-align: start;
  display: flex;
  flex-direction: column;
  position: relative;
}

.slide-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: center;
  max-height: 100%;
  overflow: hidden;
  padding: var(--slide-padding);
}
```

### Required CSS Variables

```css
:root {
  /* Typography — MUST use clamp() */
  --title-size: clamp(1.5rem, 5vw, 4rem);
  --h2-size: clamp(1.25rem, 3.5vw, 2.5rem);
  --h3-size: clamp(1rem, 2.5vw, 1.75rem);
  --body-size: clamp(0.75rem, 1.5vw, 1.125rem);
  --small-size: clamp(0.65rem, 1vw, 0.875rem);

  /* Spacing — MUST use clamp() */
  --slide-padding: clamp(1rem, 4vw, 4rem);
  --content-gap: clamp(0.5rem, 2vw, 2rem);
  --element-gap: clamp(0.25rem, 1vw, 1rem);

  /* Animation */
  --ease-out-expo: cubic-bezier(0.16, 1, 0.3, 1);
  --duration-normal: 0.6s;
}
```

### Responsive Breakpoints

```css
/* Short viewports (< 700px height) */
@media (max-height: 700px) {
  :root {
    --slide-padding: clamp(0.75rem, 3vw, 2rem);
    --content-gap: clamp(0.4rem, 1.5vw, 1rem);
    --title-size: clamp(1.25rem, 4.5vw, 2.5rem);
    --h2-size: clamp(1rem, 3vw, 1.75rem);
  }
}

/* Very short (< 600px height) */
@media (max-height: 600px) {
  :root {
    --slide-padding: clamp(0.5rem, 2.5vw, 1.5rem);
    --content-gap: clamp(0.3rem, 1vw, 0.75rem);
    --title-size: clamp(1.1rem, 4vw, 2rem);
    --body-size: clamp(0.7rem, 1.2vw, 0.95rem);
  }
  .nav-dots,
  .keyboard-hint,
  .decorative {
    display: none;
  }
}

/* Landscape phones (< 500px height) */
@media (max-height: 500px) {
  :root {
    --slide-padding: clamp(0.4rem, 2vw, 1rem);
    --title-size: clamp(1rem, 3.5vw, 1.5rem);
    --h2-size: clamp(0.9rem, 2.5vw, 1.25rem);
    --body-size: clamp(0.65rem, 1vw, 0.85rem);
  }
}

/* Narrow viewports (< 600px width) */
@media (max-width: 600px) {
  :root {
    --title-size: clamp(1.25rem, 7vw, 2.5rem);
  }
  .grid {
    grid-template-columns: 1fr;
  }
}

/* Reduced motion */
@media (prefers-reduced-motion: reduce) {
  *,
  *::before,
  *::after {
    animation-duration: 0.01ms !important;
    transition-duration: 0.2s !important;
  }
  html {
    scroll-behavior: auto;
  }
}
```

## Content Density Limits

Hard maximums per slide type. **If content exceeds → split into multiple slides.**

| Slide Type   | Maximum Content                                      |
| ------------ | ---------------------------------------------------- |
| Title        | 1 heading + 1 subtitle + optional tagline            |
| Content      | 1 heading + 4–6 bullets OR 1 heading + 2 paragraphs  |
| Feature Grid | 1 heading + 6 cards max (2×3 or 3×2)                 |
| Code         | 1 heading + 8–10 lines of code max                   |
| Quote        | 1 quote (max 3 lines) + attribution                  |
| Two-Column   | 1 heading + 2 columns, each ≤ 4 bullets              |
| Image        | 1 heading + 1 image (`max-height: min(50vh, 400px)`) |

## Slide Types

Seven standard types. See `references/slide-components.md` for complete HTML/CSS templates.

| Type         | Class            | Use For                                |
| ------------ | ---------------- | -------------------------------------- |
| Title        | `.title-slide`   | Opening slide, section dividers        |
| Content      | `.content-slide` | Bullet points, paragraphs              |
| Code         | `.code-slide`    | Code snippets with syntax highlighting |
| Feature Grid | `.grid-slide`    | Feature cards, comparisons             |
| Quote        | `.quote-slide`   | Testimonials, key statements           |
| Two-Column   | `.two-col-slide` | Side-by-side comparisons               |
| Image        | `.image-slide`   | Screenshots, diagrams, photos          |

## Theme Collection

8 curated themes across 3 categories. Each theme includes CSS variables, font pairings with system fallbacks, layout guidance, and signature element CSS.

### Dark Themes → `references/themes-dark.md`

| Theme            | Vibe                    | Signature                                            |
| ---------------- | ----------------------- | ---------------------------------------------------- |
| Bold Signal      | Confident, high-impact  | Colored card on dark gradient, large section numbers |
| Creative Voltage | Energetic, retro-modern | Electric blue + neon yellow, halftone textures       |
| Dark Botanical   | Elegant, sophisticated  | Soft gradient circles, warm gold/pink accents        |

### Light Themes → `references/themes-light.md`

| Theme             | Vibe                      | Signature                                             |
| ----------------- | ------------------------- | ----------------------------------------------------- |
| Notebook Tabs     | Editorial, tactile        | Paper card with colored tabs, binder holes            |
| Pastel Geometry   | Friendly, approachable    | Rounded card with vertical pills on right edge        |
| Vintage Editorial | Witty, personality-driven | Geometric shapes, bold bordered CTAs, serif headlines |

### Specialty Themes → `references/themes-specialty.md`

| Theme          | Vibe              | Signature                                         |
| -------------- | ----------------- | ------------------------------------------------- |
| Neon Cyber     | Futuristic, techy | Particle backgrounds, neon glow, grid patterns    |
| Terminal Green | Developer, hacker | Scan lines, blinking cursor, monospace everything |

## Font Fallback Strategy

Every theme has two font stacks — **web** (CDN) and **system** (offline).

| Theme             | Web Font                      | System Fallback                                    |
| ----------------- | ----------------------------- | -------------------------------------------------- |
| Bold Signal       | Archivo Black / Space Grotesk | Impact, Arial Black / system-ui                    |
| Creative Voltage  | Syne / Space Mono             | Trebuchet MS / Courier New, monospace              |
| Dark Botanical    | Cormorant / IBM Plex Sans     | Georgia, Times New Roman / system-ui               |
| Notebook Tabs     | Bodoni Moda / DM Sans         | Didot, Georgia / system-ui                         |
| Pastel Geometry   | Plus Jakarta Sans             | system-ui, -apple-system                           |
| Vintage Editorial | Fraunces / Work Sans          | Georgia, Palatino / system-ui                      |
| Neon Cyber        | Clash Display / Satoshi       | system-ui, -apple-system                           |
| Terminal Green    | JetBrains Mono                | "SF Mono", "Cascadia Code", "Fira Code", monospace |

When web fonts fail to load, the presentation must still look intentional — system fallbacks are chosen to preserve the theme's character.

## Creation Workflow

1. **User provides:** topic, audience, optional theme preference
2. **Choose theme:** match audience/mood to theme vibe (see table above)
3. **Load references:**
   - Always: `references/slide-template.md` (HTML skeleton)
   - Always: the relevant `references/themes-*.md` (for chosen theme)
   - As needed: `references/slide-components.md` (for specific slide types)
   - As needed: `references/animation-recipes.md` (for advanced effects)
4. **Plan slides:** outline each slide with type + key content (respect density limits)
5. **Generate:** single HTML file using the skeleton, theme CSS, and component patterns
6. **Verify:** every slide fits viewport, no overflow, animations have reduced-motion fallback

## CSS Gotchas

### Negating CSS Functions

```css
/* WRONG — silently ignored, no console error: */
right: -clamp(28px, 3.5vw, 44px);
margin-left: -min(10vw, 100px);

/* CORRECT — wrap in calc(): */
right: calc(-1 * clamp(28px, 3.5vw, 44px));
margin-left: calc(-1 * min(10vw, 100px));
```

Browsers silently discard declarations with `-` before `clamp()`, `min()`, `max()`.

### Image Constraints

```css
.slide-image {
  max-width: 100%;
  max-height: min(50vh, 400px);
  object-fit: contain;
  border-radius: 8px;
}

.slide-image.screenshot {
  border: 1px solid rgba(255, 255, 255, 0.1);
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
}
```

### Grid Auto-Fit

```css
.grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(min(100%, 250px), 1fr));
  gap: clamp(0.5rem, 1.5vw, 1rem);
}
```

## Effect-to-Feeling Guide

| Feeling      | Techniques                                                               |
| ------------ | ------------------------------------------------------------------------ |
| Dramatic     | Slow fade-ins (1–1.5s), scale 0.9→1, dark bg + spotlight, parallax       |
| Techy        | Neon glow, particle canvas, grid patterns, monospace, glitch effects     |
| Playful      | Bouncy easing, large border-radius, pastels, floating animations         |
| Professional | Subtle fast animations (200–300ms), clean sans-serif, minimal decoration |
| Calm         | Very slow subtle motion, high whitespace, muted palette, serif type      |
| Editorial    | Strong type hierarchy, pull quotes, grid-breaking layouts, serif + sans  |

## DO NOT USE

- `position: fixed` for slides (breaks scroll-snap)
- Fixed `px` / `rem` for typography or spacing (use `clamp()`)
- `vh` without `dvh` fallback (mobile address bar issues)
- `overflow: auto/scroll` on `.slide` (breaks one-slide-per-viewport rule)
- Google Fonts `@import` in CSS (use `<link>` in `<head>` for performance)
- More than 6 feature cards per grid slide
- Code blocks longer than 10 lines per slide

## References

| File                   | Contents                                          | When to Load                            |
| ---------------------- | ------------------------------------------------- | --------------------------------------- |
| `slide-template.md`    | Complete HTML/CSS/JS skeleton with navigation     | Always — every presentation starts here |
| `slide-components.md`  | 7 slide type HTML templates                       | Always — for building individual slides |
| `themes-dark.md`       | Bold Signal, Creative Voltage, Dark Botanical     | When using a dark theme                 |
| `themes-light.md`      | Notebook Tabs, Pastel Geometry, Vintage Editorial | When using a light theme                |
| `themes-specialty.md`  | Neon Cyber, Terminal Green                        | When using a specialty theme            |
| `animation-recipes.md` | Reveal, stagger, typewriter, particle effects     | When advanced animations are needed     |
