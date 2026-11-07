---
name: huashu-design-html-native
description: HTML-native design skill for AI coding agents — high-fidelity prototypes, slides, animations, and MP4 export with 20 design philosophies and 5-dimension critique
triggers:
  - make a design for this
  - create an iOS app prototype
  - build a presentation slide deck
  - generate an animation and export MP4
  - do a design critique or review
  - create an infographic or data visualization
  - suggest design directions or styles
  - export this design as PPTX or GIF
---

# Huashu Design — HTML-Native Design Skill

> Skill by [ara.so](https://ara.so) — Daily 2026 Skills collection.

Huashu Design turns natural-language requests into deliverable designs — interactive prototypes, animated slides, motion exports, and infographics — entirely in HTML/CSS/JS, no Figma or GUI required. Install it once into your agent; from then on say what you want and receive a finished file.

---

## Installation

```bash
npx skills add alchaincyf/huashu-design
```

Compatible with Claude Code, Cursor, Codex, OpenClaw, Hermes, and any agent that reads `SKILL.md`.

---

## What It Produces

| Output | Format | Typical Time |
|--------|--------|-------------|
| Interactive prototype (App/Web) | Single-file HTML, iPhone/Android bezel, clickable | 10–15 min |
| Presentation deck | HTML (browser) + editable PPTX (real text boxes) | 15–25 min |
| Timeline animation | MP4 (25/60 fps) + GIF (palette-optimized) + BGM | 8–12 min |
| Design variants | 3+ side-by-side, Tweaks panel, localStorage | 10 min |
| Infographic / data viz | Print-quality, CSS Grid, exportable PDF/PNG/SVG | 10 min |
| Design direction advice | 5 schools × 20 philosophies, 3 directions + demos | 5 min |
| 5-dimension expert critique | Radar chart + Keep/Fix/Quick Wins list | 3 min |

---

## Repository Structure

```
huashu-design/
├── SKILL.md                  # Agent-facing spec (the real instructions)
├── assets/
│   ├── animations.jsx        # Stage + Sprite + Easing + interpolate APIs
│   ├── ios_frame.jsx         # iPhone 15 Pro bezel (Dynamic Island, Home bar)
│   ├── android_frame.jsx
│   ├── macos_window.jsx
│   ├── browser_window.jsx
│   ├── deck_stage.js         # HTML slide engine
│   ├── deck_index.html       # Multi-file deck assembler
│   ├── design_canvas.jsx     # Side-by-side variant display
│   ├── showcases/            # 24 prebuilt examples (8 scenes × 3 styles)
│   └── bgm-*.mp3             # 6 scene-matched background tracks
├── references/
│   ├── animation-pitfalls.md
│   ├── design-styles.md      # 20 design philosophies detail
│   ├── slide-decks.md
│   ├── editable-pptx.md
│   ├── critique-guide.md
│   └── video-export.md
├── scripts/
│   ├── render-video.js       # HTML → MP4 via Playwright
│   ├── convert-formats.sh    # MP4 → 60fps interpolation + GIF
│   ├── add-music.sh          # Mux BGM into MP4
│   ├── export_deck_pdf.mjs
│   ├── export_deck_pptx.mjs
│   └── html2pptx.js          # DOM computedStyle → real PPTX objects
└── demos/                    # 9 capability demos (c*/w* series)
```

---

## Core Concepts

### 1. Junior Designer Workflow (Default Mode)

The agent never starts blind. Before any task it:

1. Shows a one-shot question list — waits for batch answers before touching code
2. Writes `assumptions`, `placeholders`, and `reasoning` comments inside the HTML
3. Shows an early skeleton (even gray boxes) — gets approval
4. Fills content → generates variations → adds Tweaks panel — shows each step
5. Runs Playwright visual check before final delivery

### 2. Brand Asset Protocol (Mandatory for Named Brands)

When the task involves a specific brand (Stripe, Linear, Anthropic, your company):

| Step | Action |
|------|--------|
| 1 · Ask | Does the user have brand guidelines? |
| 2 · Search | `<brand>.com/brand`, `brand.<brand>.com`, `<brand>.com/press` |
| 3 · Download | SVG file → full page HTML → product screenshot color-pick (three fallbacks) |
| 4 · Extract | `grep` all `#xxxxxx` from assets, rank by frequency, filter black/white/gray |
| 5 · Lock spec | Write `brand-spec.md` + CSS custom properties; all HTML uses `var(--brand-*)` |

**Never guess brand colors from memory.** Always extract from downloaded assets.

```css
/* brand-spec.md output example */
:root {
  --brand-primary:   #635BFF;   /* Stripe violet — freq: 847 */
  --brand-secondary: #0A2540;   /* Stripe navy   — freq: 312 */
  --brand-accent:    #00D924;   /* Stripe green  — freq: 89  */
}
```

### 3. Design Direction Advisor (Fallback)

Triggered when the request is too vague to start. The agent:

- Picks **3 directions from different schools** out of 5 schools × 20 philosophies
- Returns each with: representative works, mood keywords, reference designers
- Generates 3 parallel visual demos for the user to choose
- Then enters the Junior Designer main flow

The 5 schools and 20 philosophies live in `references/design-styles.md`. Examples:

| School | Philosophies (subset) |
|--------|----------------------|
| Modernist Functionalism | Swiss Grid, Bauhaus Utility, Dieter Rams Reduction |
| Emotional Expressionism | Memphis Color, Brutalist Raw, Maximalist Baroque |
| Digital Native | Glassmorphism, Neumorphism, Cyberpunk Neon |
| Cultural Fusion | Wabi-Sabi, Bauhaus East, Art Nouveau Revival |
| Systems Thinking | Material Design, IBM Carbon, Apple HIG |

### 4. Motion Design Engine

The animation system uses four composable primitives from `assets/animations.jsx`:

```js
// Stage: defines total duration and canvas
const stage = useStage({ duration: 5000, width: 1920, height: 1080 });

// Sprite: a timed element (appears at t=500ms, lasts 2000ms)
const logo = useSprite({ start: 500, duration: 2000 });

// interpolate: map time → value with easing
const x = interpolate(stage.t, [0, 1000], [−200, 0], Easing.easeOutExpo);
const opacity = interpolate(stage.t, [0, 500], [0, 1], Easing.linear);

// Render
return (
  <div style={{
    transform: `translateX(${x}px)`,
    opacity,
    ...logo.style,   // visibility gating included
  }}>
    {children}
  </div>
);
```

### 5. Anti-AI-Slop Rules

Avoid the visual least-common-denominator:

- ❌ Purple gradients, emoji icons, left border-accent cards, SVG-drawn human faces, Inter as display font
- ✅ `text-wrap: pretty`, CSS Grid layouts, curated serif display fonts, `oklch()` color space, actual whitespace

---

## Starter Patterns

### iOS App Prototype

```html
<!-- Uses assets/ios_frame.jsx internally -->
<!-- Agent generates a self-contained HTML file like this: -->

<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>AI Pomodoro — Prototype</title>
  <style>
    :root {
      --ios-width: 393px;
      --ios-height: 852px;
      --brand-primary: #FF3B30;
    }

    body {
      display: flex;
      justify-content: center;
      align-items: center;
      min-height: 100vh;
      background: #1a1a1a;
      font-family: -apple-system, BlinkMacSystemFont, "SF Pro Display", sans-serif;
    }

    .device {
      width: var(--ios-width);
      height: var(--ios-height);
      background: #000;
      border-radius: 54px;
      box-shadow:
        0 0 0 2px #3a3a3a,
        0 0 0 6px #1a1a1a,
        0 40px 80px rgba(0,0,0,0.8);
      overflow: hidden;
      position: relative;
    }

    /* Dynamic Island */
    .dynamic-island {
      position: absolute;
      top: 12px;
      left: 50%;
      transform: translateX(-50%);
      width: 126px;
      height: 37px;
      background: #000;
      border-radius: 20px;
      z-index: 100;
    }

    /* Screen states */
    .screen { display: none; width: 100%; height: 100%; }
    .screen.active { display: flex; flex-direction: column; }

    /* Navigation */
    [data-go] { cursor: pointer; }
  </style>
</head>
<body>
  <div class="device">
    <div class="dynamic-island"></div>

    <!-- Screen: Home -->
    <div class="screen active" id="screen-home">
      <div style="flex:1; display:flex; flex-direction:column; align-items:center;
                  justify-content:center; padding: 60px 32px 0; background:#fff;">
        <div style="font-size:72px; font-weight:700; color:var(--brand-primary);
                    font-variant-numeric:tabular-nums;">25:00</div>
        <div style="margin-top:8px; color:#6e6e73; font-size:17px;">Focus Session</div>
        <button data-go="screen-running"
          style="margin-top:48px; background:var(--brand-primary); color:#fff;
                 border:none; border-radius:50%; width:80px; height:80px;
                 font-size:32px; cursor:pointer;">▶</button>
      </div>
    </div>

    <!-- Screen: Running -->
    <div class="screen" id="screen-running">
      <div style="flex:1; display:flex; flex-direction:column; align-items:center;
                  justify-content:center; padding:60px 32px 0; background:#fff;">
        <div style="font-size:72px; font-weight:700; color:var(--brand-primary);">24:59</div>
        <button data-go="screen-home"
          style="margin-top:48px; background:#f2f2f7; color:#000;
                 border:none; border-radius:20px; padding:16px 40px;
                 font-size:17px; cursor:pointer;">Stop</button>
      </div>
    </div>
  </div>

  <script>
    // State-driven navigation
    document.querySelectorAll('[data-go]').forEach(el => {
      el.addEventListener('click', () => {
        document.querySelectorAll('.screen').forEach(s => s.classList.remove('active'));
        document.getElementById(el.dataset.go)?.classList.add('active');
      });
    });
  </script>
</body>
</html>
```

### HTML Slide Deck

```html
<!-- Single-file deck with keyboard navigation -->
<!DOCTYPE html>
<html>
<head>
  <style>
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body { background: #0a0a0a; font-family: "Inter", sans-serif; }

    .deck { width: 100vw; height: 100vh; }
    .slide {
      display: none;
      width: 100%;
      height: 100%;
      padding: 80px;
      flex-direction: column;
      justify-content: center;
    }
    .slide.active { display: flex; }

    /* Progress bar */
    .progress {
      position: fixed;
      bottom: 0; left: 0;
      height: 3px;
      background: var(--accent, #635BFF);
      transition: width 0.3s ease;
    }
  </style>
</head>
<body>
  <div class="deck">
    <div class="slide active" style="background:#0a0a0a; color:#fff;">
      <h1 style="font-size:clamp(2rem,6vw,5rem); font-weight:800; line-height:1.1;
                 text-wrap:pretty;">The Future of AI Design</h1>
      <p style="margin-top:24px; font-size:1.25rem; color:#888;">May 2026</p>
    </div>

    <div class="slide" style="background:#fff; color:#0a0a0a;">
      <h2 style="font-size:3rem; font-weight:700;">Key Insight</h2>
      <p style="margin-top:32px; font-size:1.5rem; line-height:1.6;
                max-width:60ch; text-wrap:pretty;">
        Design tools are disappearing. The interface is the conversation.
      </p>
    </div>
  </div>

  <div class="progress" id="progress"></div>

  <script>
    const slides = document.querySelectorAll('.slide');
    let current = 0;

    function go(n) {
      slides[current].classList.remove('active');
      current = Math.max(0, Math.min(n, slides.length - 1));
      slides[current].classList.add('active');
      document.getElementById('progress').style.width =
        `${((current + 1) / slides.length) * 100}%`;
    }

    document.addEventListener('keydown', e => {
      if (e.key === 'ArrowRight' || e.key === ' ') go(current + 1);
      if (e.key === 'ArrowLeft') go(current - 1);
    });

    go(0);
  </script>
</body>
</html>
```

### Tweaks Panel (Design Variants)

```html
<script>
  // Parameterized design system with localStorage persistence
  const TWEAKS = {
    colorScheme: { options: ['midnight', 'warm', 'ocean'], default: 'midnight' },
    typeScale:   { options: ['compact', 'comfortable', 'spacious'], default: 'comfortable' },
    density:     { options: ['dense', 'balanced', 'airy'], default: 'balanced' },
  };

  const themes = {
    midnight: { '--bg': '#0a0a0a', '--fg': '#ffffff', '--accent': '#635BFF' },
    warm:     { '--bg': '#faf6f0', '--fg': '#1a1208', '--accent': '#d4793a' },
    ocean:    { '--bg': '#f0f7ff', '--fg': '#0a1628', '--accent': '#0066cc' },
  };

  function applyTweak(key, value) {
    localStorage.setItem(`tweak-${key}`, value);
    if (key === 'colorScheme') {
      Object.entries(themes[value]).forEach(([prop, val]) =>
        document.documentElement.style.setProperty(prop, val));
    }
  }

  // Restore on load
  Object.keys(TWEAKS).forEach(key => {
    const saved = localStorage.getItem(`tweak-${key}`) || TWEAKS[key].default;
    applyTweak(key, saved);
  });
</script>
```

### Video Export Pipeline

```bash
# 1. Render HTML animation to MP4
node scripts/render-video.js \
  --input  ./animation.html \
  --output ./out/animation.mp4 \
  --fps    25 \
  --duration 10000

# 2. Upscale to 60fps with frame interpolation
bash scripts/convert-formats.sh \
  --input  ./out/animation.mp4 \
  --fps    60 \
  --output ./out/animation-60fps.mp4

# 3. Export palette-optimized GIF
bash scripts/convert-formats.sh \
  --input  ./out/animation.mp4 \
  --format gif \
  --width  800 \
  --output ./out/animation.gif

# 4. Add background music
bash scripts/add-music.sh \
  --video ./out/animation.mp4 \
  --audio ./assets/bgm-cinematic.mp3 \
  --output ./out/animation-final.mp4
```

```js
// render-video.js uses Playwright internally
const { chromium } = require('playwright');

async function renderVideo({ input, output, fps = 25, duration = 10000 }) {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1920, height: 1080 } });

  await page.goto(`file://${path.resolve(input)}`);

  // Frame-by-frame capture
  const frames = [];
  const totalFrames = Math.ceil((duration / 1000) * fps);

  for (let i = 0; i < totalFrames; i++) {
    await page.evaluate(t => window.__seekTo?.(t), (i / fps) * 1000);
    frames.push(await page.screenshot({ type: 'png' }));
  }

  await browser.close();
  // Encode frames → MP4 via ffmpeg
  await encodeFrames(frames, output, fps);
}
```

### PPTX Export (Real Text Boxes)

```bash
# Export HTML deck to editable PowerPoint
node scripts/export_deck_pptx.mjs \
  --input  ./deck.html \
  --output ./deck.pptx

# Export to PDF (vector)
node scripts/export_deck_pdf.mjs \
  --input  ./deck.html \
  --output ./deck.pdf
```

The `html2pptx.js` converter reads `getComputedStyle()` on every DOM element and maps CSS properties to real PowerPoint text boxes, shapes, and images — output is editable in PowerPoint/Keynote, not an image dump.

### 5-Dimension Expert Critique

Ask: *"Do a 5-dimension design critique of this file"*

The agent scores 0–10 on:

| Dimension | What It Checks |
|-----------|---------------|
| Philosophical Consistency | Does the design commit to one visual language? |
| Visual Hierarchy | Can a stranger scan and know what matters in 3 seconds? |
| Detail Execution | Spacing, kerning, alignment — are they precise? |
| Functionality | Does every element earn its place? |
| Innovation | Is there a distinctive creative choice? |

Output: SVG radar chart + structured `Keep / Fix / Quick Wins` list with actionable steps.

---

## Prompt Examples That Work Well

```
# Prototype
"Make a clickable iOS prototype for an AI journaling app — 4 core screens"

# Slide deck
"Create a 10-slide pitch deck for a B2B SaaS product, suggest 3 style directions"

# Animation
"Animate this product launch sequence, 30 seconds, export MP4 with music"

# Infographic
"Visualize this dataset as a magazine-quality infographic, export PNG 300dpi"

# Critique
"Critique this design file across all 5 dimensions and give me a fix list"

# Vague request (triggers advisor)
"I need something that looks premium for my fintech app"
```

---

## Troubleshooting

**Agent generates generic purple-gradient AI slop**
The skill's anti-slop rules are in `SKILL.md`. Make sure `npx skills add` completed — check that `SKILL.md` is referenced in your agent's config. Re-run the install.

**Brand colors look wrong**
The brand asset protocol requires live extraction. Tell the agent: *"Re-run the brand asset protocol for [Brand] — download the SVG from their press page and grep the hex values."*

**MP4 export fails**
Playwright must be installed: `npx playwright install chromium`. FFmpeg must be on PATH: `brew install ffmpeg` / `apt install ffmpeg`.

**PPTX text shows as images not text boxes**
Use `html2pptx.js`, not screenshot-based export. Check that the slide HTML uses semantic elements (`<h1>`, `<p>`, `<span>`) — the converter maps element types to PPTX object types.

**Animation is choppy at 25fps**
Run the 60fps interpolation step in `convert-formats.sh`. For real-time smoothness, set `requestAnimationFrame` timing in the HTML source and verify the `--fps 60` flag in the render call.

**Tweaks panel doesn't persist across sessions**
The panel uses `localStorage`. Verify the HTML is served from the same origin across sessions — `file://` paths that differ by absolute path will miss the stored values. Use a local dev server: `npx serve .`

---

## Design Philosophies Quick Reference

20 philosophies live in `references/design-styles.md`. A fast selection guide:

| Goal | Reach for |
|------|-----------|
| Corporate trust / enterprise | IBM Carbon, Swiss Grid, Material Design |
| Consumer delight / warmth | Memphis Color, Bauhaus Utility, Art Nouveau Revival |
| Tech credibility / startup | Neumorphism (refined), Cyberpunk Neon (restrained), Brutalist Raw |
| Editorial / media | Swiss Grid, Maximalist Baroque, Wabi-Sabi |
| Luxury / premium | Dieter Rams Reduction, Japanese Minimalism, Art Deco Revival |

Always pick directions from **different schools** to give the client a genuine choice.

---

## Key Constraints

- No layer-editable PPTX-to-Figma round-trip
- No 3D, physics simulation, or particle systems
- Completely blank-brand designs land at ~60–65/100; provide any brand asset to push toward 80+
- MP4 export requires local Playwright + FFmpeg
