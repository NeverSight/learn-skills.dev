---
name: html-ppt-skill
description: Build professional HTML presentations with 36 themes, 31 layouts, 47 animations — pure static HTML/CSS/JS, no build step required.
triggers:
  - create a presentation in HTML
  - make slides with animations
  - build a pitch deck HTML
  - generate HTML PPT with themes
  - create a slideshow with canvas effects
  - make a 小红书 style slide deck
  - scaffold a new HTML presentation
  - add animations to my HTML slides
---

# html-ppt-skill — HTML PPT Studio

> Skill by [ara.so](https://ara.so) — Daily 2026 Skills collection.

A world-class AgentSkill for producing professional HTML presentations using **36 themes**, **14 full-deck templates**, **31 page layouts**, and **47 animations** (27 CSS + 20 canvas FX) — all pure static HTML/CSS/JS, zero build step.

---

## Install

```bash
# Register with your agent runtime
npx skills add https://github.com/lewislulu/html-ppt-skill

# Or clone directly
git clone https://github.com/lewislulu/html-ppt-skill
```

---

## Scaffold a New Deck

```bash
# Create a new deck from the base template
./scripts/new-deck.sh my-talk

# Output: examples/my-talk/index.html (ready to edit)
```

---

## Project Structure (Key Paths)

```
html-ppt-skill/
├── assets/
│   ├── base.css                  # shared tokens + primitives
│   ├── runtime.js                # keyboard nav + presenter + overview
│   ├── themes/*.css              # 36 theme token files
│   └── animations/
│       ├── animations.css        # 27 named CSS animations
│       ├── fx-runtime.js         # auto-init [data-fx] on slide enter
│       └── fx/*.js               # 20 canvas FX modules
├── templates/
│   ├── deck.html                 # minimal starter
│   ├── theme-showcase.html       # all 36 themes (iframe-isolated)
│   ├── layout-showcase.html      # all 31 layouts
│   ├── animation-showcase.html   # 47 animation slides
│   ├── full-decks-index.html     # 14-deck gallery
│   ├── full-decks/<name>/        # 14 scoped multi-slide decks
│   └── single-page/*.html        # 31 layout files with demo data
└── examples/demo-deck/           # complete working deck
```

---

## Minimal Deck Template

Every deck follows this structure — `assets/base.css` + one theme file + `runtime.js`:

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>My Talk</title>
  <!-- Base system -->
  <link rel="stylesheet" href="../../assets/base.css" />
  <!-- Pick ONE theme -->
  <link rel="stylesheet" href="../../assets/themes/tokyo-night.css" />
  <!-- Optional: animations -->
  <link rel="stylesheet" href="../../assets/animations/animations.css" />
</head>
<body>

  <!-- Slide 1: Cover -->
  <section class="slide" data-layout="cover">
    <div class="slide-content">
      <h1 class="animate-on-enter rise-in">My Presentation</h1>
      <p class="animate-on-enter fade-up" style="--delay:0.3s">Subtitle goes here</p>
    </div>
  </section>

  <!-- Slide 2: Bullets -->
  <section class="slide" data-layout="bullets">
    <div class="slide-content">
      <h2>Key Points</h2>
      <ul class="stagger-list">
        <li>First important point</li>
        <li>Second important point</li>
        <li>Third important point</li>
      </ul>
    </div>
  </section>

  <!-- Slide 3: Big Quote -->
  <section class="slide" data-layout="big-quote">
    <div class="slide-content">
      <blockquote class="animate-on-enter zoom-pop">
        "Design is not just what it looks like. Design is how it works."
      </blockquote>
      <cite>— Steve Jobs</cite>
    </div>
  </section>

  <!-- Slide 4: Thanks -->
  <section class="slide" data-layout="thanks">
    <div class="slide-content">
      <h1>Thank You</h1>
      <p>github.com/yourhandle</p>
    </div>
  </section>

  <script src="../../assets/runtime.js"></script>
  <script src="../../assets/animations/fx-runtime.js"></script>
</body>
</html>
```

---

## Themes (36 total)

Swap the single `<link>` to change the entire deck's appearance. All themes live in `assets/themes/*.css`.

```html
<!-- Light / Editorial -->
<link rel="stylesheet" href="assets/themes/minimal-white.css" />
<link rel="stylesheet" href="assets/themes/editorial-serif.css" />
<link rel="stylesheet" href="assets/themes/soft-pastel.css" />
<link rel="stylesheet" href="assets/themes/academic-paper.css" />

<!-- Dark / Moody -->
<link rel="stylesheet" href="assets/themes/tokyo-night.css" />
<link rel="stylesheet" href="assets/themes/dracula.css" />
<link rel="stylesheet" href="assets/themes/catppuccin-mocha.css" />
<link rel="stylesheet" href="assets/themes/gruvbox-dark.css" />
<link rel="stylesheet" href="assets/themes/nord.css" />

<!-- Bold / Design-forward -->
<link rel="stylesheet" href="assets/themes/neo-brutalism.css" />
<link rel="stylesheet" href="assets/themes/glassmorphism.css" />
<link rel="stylesheet" href="assets/themes/cyberpunk-neon.css" />
<link rel="stylesheet" href="assets/themes/memphis-pop.css" />
<link rel="stylesheet" href="assets/themes/vaporwave.css" />

<!-- Business / Professional -->
<link rel="stylesheet" href="assets/themes/corporate-clean.css" />
<link rel="stylesheet" href="assets/themes/pitch-deck-vc.css" />
<link rel="stylesheet" href="assets/themes/swiss-grid.css" />

<!-- Special / Cultural -->
<link rel="stylesheet" href="assets/themes/xiaohongshu-white.css" />
<link rel="stylesheet" href="assets/themes/japanese-minimal.css" />
<link rel="stylesheet" href="assets/themes/terminal-green.css" />
```

Browse all 36 themes live: `open templates/theme-showcase.html`

---

## Layouts (31 total)

Set via `data-layout` on each `<section class="slide">`.

```html
<!-- Structural -->
<section class="slide" data-layout="cover">…</section>
<section class="slide" data-layout="toc">…</section>
<section class="slide" data-layout="section-divider">…</section>
<section class="slide" data-layout="thanks">…</section>
<section class="slide" data-layout="cta">…</section>

<!-- Content -->
<section class="slide" data-layout="bullets">…</section>
<section class="slide" data-layout="two-column">…</section>
<section class="slide" data-layout="three-column">…</section>
<section class="slide" data-layout="big-quote">…</section>
<section class="slide" data-layout="table">…</section>
<section class="slide" data-layout="code">…</section>
<section class="slide" data-layout="diff">…</section>
<section class="slide" data-layout="terminal">…</section>

<!-- Data / Stats -->
<section class="slide" data-layout="stat-highlight">…</section>
<section class="slide" data-layout="kpi-grid">…</section>
<section class="slide" data-layout="chart-bar">…</section>
<section class="slide" data-layout="chart-line">…</section>
<section class="slide" data-layout="chart-pie">…</section>
<section class="slide" data-layout="chart-radar">…</section>

<!-- Diagrams / Process -->
<section class="slide" data-layout="flow-diagram">…</section>
<section class="slide" data-layout="timeline">…</section>
<section class="slide" data-layout="roadmap">…</section>
<section class="slide" data-layout="mindmap">…</section>
<section class="slide" data-layout="arch-diagram">…</section>
<section class="slide" data-layout="process-steps">…</section>
<section class="slide" data-layout="gantt">…</section>

<!-- Comparison -->
<section class="slide" data-layout="comparison">…</section>
<section class="slide" data-layout="pros-cons">…</section>
<section class="slide" data-layout="todo-checklist">…</section>

<!-- Visual -->
<section class="slide" data-layout="image-hero">…</section>
<section class="slide" data-layout="image-grid">…</section>
```

Browse all 31 layouts live: `open templates/layout-showcase.html`

---

## CSS Animations

Add class to any element. Use `--delay` CSS variable for staggering.

```html
<!-- Fade / Entrance -->
<h1 class="animate-on-enter rise-in">Title</h1>
<p class="animate-on-enter fade-up" style="--delay:0.2s">Subtitle</p>
<img class="animate-on-enter zoom-pop" style="--delay:0.4s" src="..." />
<p class="animate-on-enter blur-in">Blurred entrance</p>

<!-- Text Effects -->
<h2 class="typewriter">Typed out text</h2>
<span class="glitch-in">Glitched text</span>
<span class="neon-glow">Glowing text</span>
<span class="shimmer-sweep">Shimmer effect</span>
<div class="gradient-flow">Animated gradient background</div>

<!-- Lists -->
<ul class="stagger-list">
  <li>Appears first</li>
  <li>Appears second</li>
  <li>Appears third</li>
</ul>

<!-- Numbers -->
<span class="counter-up" data-target="1000000">0</span>

<!-- 3D / Advanced -->
<div class="card-flip-3d">…</div>
<div class="cube-rotate-3d">…</div>
<div class="page-turn-3d">…</div>
<div class="perspective-zoom">…</div>

<!-- Scroll / Motion -->
<div class="marquee-scroll">Scrolling ticker text…</div>
<div class="kenburns"><img src="..." /></div>
<div class="parallax-tilt">Tilt on hover</div>
<div class="ripple-reveal">Ripple entrance</div>
<div class="spotlight">Spotlight effect</div>
```

---

## Canvas FX Animations

Add `data-fx` attribute to trigger cinematic canvas effects on slide enter:

```html
<!-- Particle effects -->
<section class="slide" data-layout="cover" data-fx="particle-burst">
  <div class="slide-content">
    <h1>Big Launch</h1>
  </div>
</section>

<!-- Celebration -->
<section class="slide" data-layout="thanks" data-fx="confetti-cannon">
  <div class="slide-content"><h1>Thank You!</h1></div>
</section>

<!-- Tech / Data -->
<section class="slide" data-layout="arch-diagram" data-fx="knowledge-graph">
  <div class="slide-content">…</div>
</section>

<section class="slide" data-fx="neural-net">…</section>
<section class="slide" data-fx="matrix-rain">…</section>
<section class="slide" data-fx="data-stream">…</section>

<!-- Space / Ambient -->
<section class="slide" data-fx="starfield">…</section>
<section class="slide" data-fx="constellation">…</section>
<section class="slide" data-fx="galaxy-swirl">…</section>
<section class="slide" data-fx="orbit-ring">…</section>

<!-- Text FX -->
<section class="slide" data-fx="typewriter-multi">…</section>
<section class="slide" data-fx="word-cascade">…</section>
<section class="slide" data-fx="letter-explode">…</section>
<section class="slide" data-fx="counter-explosion">…</section>

<!-- Visual -->
<section class="slide" data-fx="gradient-blob">…</section>
<section class="slide" data-fx="sparkle-trail">…</section>
<section class="slide" data-fx="shockwave">…</section>
<section class="slide" data-fx="firework">…</section>
<section class="slide" data-fx="chain-react">…</section>
<section class="slide" data-fx="magnetic-field">…</section>
```

`fx-runtime.js` auto-initialises these on slide enter — no extra JS needed.

---

## Full-Deck Templates (14 total)

Pre-built complete decks in `templates/full-decks/<name>/`:

```bash
# Business / Generic
templates/full-decks/pitch-deck/
templates/full-decks/product-launch/
templates/full-decks/tech-sharing/
templates/full-decks/weekly-report/
templates/full-decks/course-module/

# Social / Chinese
templates/full-decks/xhs-post/          # 9-slide 3:4 ratio
templates/full-decks/xhs-white-editorial/
templates/full-decks/xhs-pastel-card/

# Technical / Dark
templates/full-decks/graphify-dark-graph/
templates/full-decks/hermes-cyber-terminal/
templates/full-decks/knowledge-arch-blueprint/

# Specific Styles
templates/full-decks/obsidian-claude-gradient/
templates/full-decks/testing-safety-alert/
templates/full-decks/dir-key-nav-minimal/
```

Each deck uses scoped `.tpl-<name>` CSS — safe to embed multiple decks side-by-side.

Browse all: `open templates/full-decks-index.html`

---

## Common Deck Patterns

### Pitch Deck (VC Style)

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <title>Pitch Deck</title>
  <link rel="stylesheet" href="../../assets/base.css" />
  <link rel="stylesheet" href="../../assets/themes/pitch-deck-vc.css" />
  <link rel="stylesheet" href="../../assets/animations/animations.css" />
</head>
<body>

  <section class="slide" data-layout="cover" data-fx="gradient-blob">
    <div class="slide-content">
      <h1 class="animate-on-enter rise-in">CompanyName</h1>
      <p class="animate-on-enter fade-up" style="--delay:0.3s">
        One-line value proposition
      </p>
      <p class="animate-on-enter fade-up" style="--delay:0.5s">Seed Round · 2026</p>
    </div>
  </section>

  <section class="slide" data-layout="stat-highlight">
    <div class="slide-content">
      <h2>Traction</h2>
      <div class="kpi-row">
        <div class="kpi">
          <span class="counter-up" data-target="50000">0</span>
          <label>Users</label>
        </div>
        <div class="kpi">
          <span class="counter-up" data-target="120">0</span>
          <label>% MoM Growth</label>
        </div>
        <div class="kpi">
          <span>$<span class="counter-up" data-target="2">0</span>M</span>
          <label>ARR</label>
        </div>
      </div>
    </div>
  </section>

  <section class="slide" data-layout="two-column">
    <div class="slide-content">
      <h2>The Problem / Solution</h2>
      <div class="col">
        <h3>😩 Problem</h3>
        <ul class="stagger-list">
          <li>Pain point one</li>
          <li>Pain point two</li>
        </ul>
      </div>
      <div class="col">
        <h3>✅ Solution</h3>
        <ul class="stagger-list">
          <li>How we fix it</li>
          <li>Why we win</li>
        </ul>
      </div>
    </div>
  </section>

  <section class="slide" data-layout="cta" data-fx="confetti-cannon">
    <div class="slide-content">
      <h1>Join Us</h1>
      <p>hello@company.com</p>
    </div>
  </section>

  <script src="../../assets/runtime.js"></script>
  <script src="../../assets/animations/fx-runtime.js"></script>
</body>
</html>
```

### Tech Talk / Engineering

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <title>Tech Sharing</title>
  <link rel="stylesheet" href="../../assets/base.css" />
  <link rel="stylesheet" href="../../assets/themes/tokyo-night.css" />
  <link rel="stylesheet" href="../../assets/animations/animations.css" />
</head>
<body>

  <section class="slide" data-layout="cover" data-fx="neural-net">
    <div class="slide-content">
      <h1 class="neon-glow">How We Scaled to 10M RPS</h1>
      <p>Engineering Deep Dive · 2026</p>
    </div>
  </section>

  <section class="slide" data-layout="code">
    <div class="slide-content">
      <h2>The Bottleneck</h2>
      <pre><code class="language-python">
# Before: naive approach — O(n²) lookup
def find_user(users, uid):
    for user in users:      # 💀 scans entire list
        if user.id == uid:
            return user

# After: hash map — O(1)
user_index = {u.id: u for u in users}
def find_user(uid):
    return user_index.get(uid)  # ⚡ instant
      </code></pre>
    </div>
  </section>

  <section class="slide" data-layout="timeline">
    <div class="slide-content">
      <h2>Migration Roadmap</h2>
      <div class="timeline">
        <div class="timeline-item">
          <span class="date">Q1</span>
          <span class="event">Audit + profiling</span>
        </div>
        <div class="timeline-item">
          <span class="date">Q2</span>
          <span class="event">Hash-map refactor</span>
        </div>
        <div class="timeline-item">
          <span class="date">Q3</span>
          <span class="event">Cache layer + CDN</span>
        </div>
        <div class="timeline-item">
          <span class="date">Q4</span>
          <span class="event">10M RPS achieved ✓</span>
        </div>
      </div>
    </div>
  </section>

  <script src="../../assets/runtime.js"></script>
  <script src="../../assets/animations/fx-runtime.js"></script>
</body>
</html>
```

### 小红书 Style (3:4 ratio)

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8" />
  <title>小红书图文</title>
  <link rel="stylesheet" href="../../assets/base.css" />
  <link rel="stylesheet" href="../../assets/themes/xiaohongshu-white.css" />
  <link rel="stylesheet" href="../../assets/animations/animations.css" />
  <style>
    /* 3:4 aspect ratio for XHS */
    .slide { aspect-ratio: 3 / 4; max-width: 480px; }
  </style>
</head>
<body>

  <section class="slide" data-layout="cover">
    <div class="slide-content">
      <h1 class="animate-on-enter rise-in">5个让你效率翻倍的工具</h1>
      <p class="animate-on-enter fade-up" style="--delay:0.3s">
        📌 收藏备用！
      </p>
    </div>
  </section>

  <section class="slide" data-layout="image-hero">
    <div class="slide-content">
      <div class="tag">工具 01</div>
      <h2>Notion</h2>
      <p>把你的大脑外包给它，笔记 / 任务 / Wiki 一体化</p>
    </div>
  </section>

  <!-- Repeat for tools 2–5 -->

  <section class="slide" data-layout="thanks">
    <div class="slide-content">
      <h2>觉得有用的话</h2>
      <p>💾 收藏 + 👍 点赞 + 💬 评论你用什么工具</p>
    </div>
  </section>

  <script src="../../assets/runtime.js"></script>
</body>
</html>
```

---

## Speaker Notes

Add notes inside `.slide-notes` — revealed by pressing `S`:

```html
<section class="slide" data-layout="bullets">
  <div class="slide-content">
    <h2>Architecture Overview</h2>
    <ul class="stagger-list">
      <li>Service A handles ingestion</li>
      <li>Service B handles processing</li>
    </ul>
  </div>
  <!-- Hidden from audience, shown in presenter overlay -->
  <aside class="slide-notes">
    Mention: Service A uses Kafka. Budget 3 min here. 
    Demo link: internal.company.com/demo
  </aside>
</section>
```

---

## Deep Linking & URL Navigation

Link directly to a slide by appending `#N` or `?slide=N`:

```html
<!-- Link to slide 5 in a shared deck -->
<a href="my-deck/index.html#5">Jump to Architecture slide</a>

<!-- From JS -->
window.location.hash = '3';
```

---

## Keyboard Controls

| Key | Action |
|---|---|
| `← → Space PgUp PgDn` | Navigate slides |
| `Home / End` | First / last slide |
| `F` | Fullscreen |
| `S` | Speaker notes overlay |
| `O` | Slide overview grid |
| `T` | Cycle through themes |
| `A` | Demo animation on current slide |

---

## Render to PNG (Headless Chrome)

```bash
# Single template, default viewport
./scripts/render.sh templates/theme-showcase.html

# Specific deck, 12 slides
./scripts/render.sh examples/my-talk/index.html 12

# Output lands in scripts/verify-output/
ls scripts/verify-output/*.png
```

---

## Browse Showcase Files

```bash
# All 36 themes (each in an isolated iframe)
open templates/theme-showcase.html

# All 31 layouts with real demo data
open templates/layout-showcase.html

# All 47 animations (CSS + canvas FX)
open templates/animation-showcase.html

# All 14 full-deck templates in a gallery
open templates/full-decks-index.html
```

---

## Troubleshooting

**Animations not firing on slide enter**
- Ensure `fx-runtime.js` is loaded after `runtime.js`
- Check `data-fx` value matches a name in `assets/animations/fx/*.js`
- Canvas FX requires a visible `<canvas>` — `fx-runtime.js` injects one automatically if absent

**Theme not applying**
- Only one theme `<link>` should be active at a time
- Theme file must be loaded after `base.css`
- Scoped deck templates use `.tpl-<name>` class on `<body>` — add it when embedding

**Fonts not loading (offline)**
- `fonts.css` loads Noto Sans SC / Noto Serif SC from Google Fonts CDN
- For offline use, download fonts and update `@font-face` paths in `assets/fonts.css`

**3:4 ratio slides look stretched**
- Add `aspect-ratio: 3 / 4` and constrain `max-width` on `.slide` (see XHS example above)
- Default slides are 16:9 widescreen

**Code blocks not highlighted**
- Include highlight.js from CDN: `<script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/highlight.min.js"></script>`
- Call `hljs.highlightAll()` after DOM load

**Chart layouts blank**
- `chart-bar`, `chart-line`, `chart-pie`, `chart-radar` layouts expect Chart.js
- Include: `<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>`
