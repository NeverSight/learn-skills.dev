---
name: kami-document-design
description: Design system and AI skill for generating beautiful warm-parchment documents (resumes, slides, one-pagers, portfolios, letters, white papers) with a consistent editorial aesthetic.
triggers:
  - make me a resume
  - build a slide deck
  - create a one-pager
  - write a white paper
  - design a portfolio
  - generate a recommendation letter
  - turn this into a polished document
  - 帮我排版一份文档
---

# Kami Document Design Skill

> Skill by [ara.so](https://ara.so) — Daily 2026 Skills collection.

Kami (紙, かみ) is an aesthetic constraint system for professional printed documents. It produces warm parchment canvas output across six document types, with Chinese and English variants, using a single ink-blue accent and editorial typography tuned for print.

## What Kami Does

Kami is not a UI framework — it is a visual language applied to documents you actually want to read. It gives AI agents a strict design spec so every generated document shares the same signature: parchment background, ink-blue accent, serif for authority, sans for utility, tight editorial whitespace.

**Six document types:**
- **One-Pager** — compact company/product intro, single page
- **Long Doc / White Paper** — multi-section research or analysis
- **Letter** — recommendation, cover, formal correspondence
- **Portfolio** — project showcase, multi-page
- **Resume / CV** — founder or professional CV
- **Slides** — keynote-style deck, 4–8 slides

Each type has a Chinese variant and an English variant. Kami selects the correct variant based on the language you write in.

## Installation

**Claude Code (recommended):**
```bash
npx skills add tw93/kami -a claude-code -g -y
```

**Codex:**
```bash
npx skills add tw93/kami -a codex -g -y
```

**Claude Desktop:**
1. Download the ZIP from [Releases](https://github.com/tw93/kami/releases)
2. Open Customize → Skills → "+" → Create skill
3. Upload the ZIP

The skill auto-triggers on natural language — no slash command needed.

## Design Tokens (Hard Rules)

| Element | Value | Rule |
|---|---|---|
| Canvas | `#f5f4ed` | Warm parchment, never pure white |
| Accent | `#1B365D` | Ink blue only, no second chromatic hue |
| Neutrals | Yellow-brown undertone | No cool blue-grays |
| Serif weight | `500` | Never bold — single weight is the signature |
| Title line-height | `1.1–1.3` | Tight |
| Dense body | `1.4–1.45` | Captions, labels |
| Reading body | `1.5–1.55` | Paragraphs — never `1.6+` |
| Shadows | Ring or whisper only | No hard drop shadows |
| Tag backgrounds | Solid hex only | `rgba()` triggers WeasyPrint double-rectangle bug |

**Fonts:**
- **Chinese:** TsangerJinKai02 (serif) + Source Han Sans (sans). TsangerJinKai is free for personal use; commercial use requires a license from [tsanger.cn](https://tsanger.cn).
- **English:** Newsreader (serif, OFL) + Inter (sans, OFL)

## HTML Document Structure

All Kami output is self-contained HTML rendered to PDF (via WeasyPrint or browser print). The canonical structure:

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Document Title</title>
  <style>
    /* ─── Tokens ─────────────────────────────────── */
    :root {
      --canvas:   #f5f4ed;
      --ink:      #1B365D;
      --ink-mid:  #2c4a7a;
      --ink-soft: #4a6fa5;
      --muted:    #8a7f6e;
      --border:   #d4cfc4;
      --white:    #ffffff;
    }

    /* ─── Reset ──────────────────────────────────── */
    *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

    /* ─── Page ───────────────────────────────────── */
    @page {
      size: A4;
      margin: 18mm 16mm;
    }

    body {
      background: var(--canvas);
      color: var(--ink);
      font-family: 'Newsreader', 'Georgia', serif;
      font-size: 10.5pt;
      line-height: 1.52;
      -webkit-print-color-adjust: exact;
      print-color-adjust: exact;
    }

    /* ─── Typography ─────────────────────────────── */
    h1 {
      font-size: 22pt;
      font-weight: 500;
      line-height: 1.15;
      letter-spacing: -0.02em;
      color: var(--ink);
    }
    h2 {
      font-family: 'Inter', 'Helvetica Neue', sans-serif;
      font-size: 7.5pt;
      font-weight: 600;
      letter-spacing: 0.12em;
      text-transform: uppercase;
      color: var(--muted);
      margin-bottom: 6pt;
    }
    h3 {
      font-size: 11pt;
      font-weight: 500;
      line-height: 1.3;
      color: var(--ink);
    }
    p {
      font-size: 10pt;
      line-height: 1.52;
      color: #3d3427;
    }
    .sans {
      font-family: 'Inter', 'Helvetica Neue', sans-serif;
    }
  </style>
</head>
<body>
  <!-- document content here -->
</body>
</html>
```

## Document Type Examples

### Resume (English)

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <title>Resume – Jane Smith</title>
  <style>
    :root {
      --canvas: #f5f4ed; --ink: #1B365D; --muted: #8a7f6e;
      --border: #d4cfc4; --accent-bg: #1B365D;
    }
    @page { size: A4; margin: 16mm 18mm; }
    *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      background: var(--canvas);
      color: var(--ink);
      font-family: 'Newsreader', Georgia, serif;
      font-size: 10pt;
      line-height: 1.52;
      -webkit-print-color-adjust: exact;
      print-color-adjust: exact;
    }

    /* Header */
    .header {
      border-bottom: 1.5pt solid var(--ink);
      padding-bottom: 10pt;
      margin-bottom: 14pt;
      display: flex;
      justify-content: space-between;
      align-items: flex-end;
    }
    .header h1 {
      font-size: 20pt;
      font-weight: 500;
      line-height: 1.1;
      letter-spacing: -0.02em;
    }
    .header .contact {
      font-family: 'Inter', sans-serif;
      font-size: 8pt;
      color: var(--muted);
      text-align: right;
      line-height: 1.6;
    }

    /* Section */
    .section { margin-bottom: 14pt; }
    .section-label {
      font-family: 'Inter', sans-serif;
      font-size: 7pt;
      font-weight: 600;
      letter-spacing: 0.14em;
      text-transform: uppercase;
      color: var(--muted);
      border-bottom: 0.5pt solid var(--border);
      padding-bottom: 3pt;
      margin-bottom: 8pt;
    }

    /* Entry */
    .entry { margin-bottom: 9pt; }
    .entry-header {
      display: flex;
      justify-content: space-between;
      align-items: baseline;
    }
    .entry-title {
      font-size: 10.5pt;
      font-weight: 500;
    }
    .entry-date {
      font-family: 'Inter', sans-serif;
      font-size: 8pt;
      color: var(--muted);
    }
    .entry-sub {
      font-family: 'Inter', sans-serif;
      font-size: 8.5pt;
      color: var(--muted);
      margin-bottom: 3pt;
    }
    .entry ul {
      padding-left: 13pt;
      font-size: 9.5pt;
      line-height: 1.48;
      color: #3d3427;
    }

    /* Tags */
    .tags { display: flex; flex-wrap: wrap; gap: 4pt; margin-top: 3pt; }
    .tag {
      background: #1B365D;
      color: #f5f4ed;
      font-family: 'Inter', sans-serif;
      font-size: 7pt;
      font-weight: 500;
      padding: 2pt 6pt;
      border-radius: 2pt;
    }
    .tag-light {
      background: #d4cfc4;
      color: #1B365D;
      font-family: 'Inter', sans-serif;
      font-size: 7pt;
      font-weight: 500;
      padding: 2pt 6pt;
      border-radius: 2pt;
    }
  </style>
</head>
<body>

  <div class="header">
    <div>
      <h1>Jane Smith</h1>
      <p style="font-family:Inter,sans-serif;font-size:9pt;color:#8a7f6e;margin-top:3pt;">
        Staff Engineer · Platform Infrastructure
      </p>
    </div>
    <div class="contact">
      jane@example.com<br>
      github.com/janesmith<br>
      San Francisco, CA
    </div>
  </div>

  <div class="section">
    <div class="section-label">Experience</div>

    <div class="entry">
      <div class="entry-header">
        <span class="entry-title">Staff Engineer</span>
        <span class="entry-date">2021 – Present</span>
      </div>
      <div class="entry-sub">Stripe · Platform Infrastructure</div>
      <ul>
        <li>Led migration of payment routing layer to event-driven architecture, reducing p99 latency by 34%.</li>
        <li>Designed the internal developer platform serving 600+ engineers across 12 product teams.</li>
        <li>Mentored 5 senior engineers through promotion cycles to staff level.</li>
      </ul>
    </div>

    <div class="entry">
      <div class="entry-header">
        <span class="entry-title">Senior Software Engineer</span>
        <span class="entry-date">2018 – 2021</span>
      </div>
      <div class="entry-sub">Airbnb · Search & Discovery</div>
      <ul>
        <li>Built the real-time availability indexing pipeline handling 2M events/minute.</li>
        <li>Shipped personalized ranking model that lifted booking conversion by 8%.</li>
      </ul>
    </div>
  </div>

  <div class="section">
    <div class="section-label">Skills</div>
    <div class="tags">
      <span class="tag">Go</span>
      <span class="tag">Rust</span>
      <span class="tag">Kubernetes</span>
      <span class="tag">Kafka</span>
      <span class="tag">PostgreSQL</span>
      <span class="tag-light">System Design</span>
      <span class="tag-light">Technical Leadership</span>
    </div>
  </div>

</body>
</html>
```

### One-Pager (Chinese)

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8" />
  <title>公司介绍</title>
  <style>
    :root { --canvas: #f5f4ed; --ink: #1B365D; --muted: #8a7f6e; --border: #d4cfc4; }
    @page { size: A4; margin: 14mm 16mm; }
    *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      background: var(--canvas);
      color: var(--ink);
      font-family: 'TsangerJinKai02', 'Source Han Serif SC', 'Songti SC', 'SimSun', serif;
      font-size: 10pt;
      line-height: 1.52;
      -webkit-print-color-adjust: exact;
      print-color-adjust: exact;
    }

    .hero {
      text-align: center;
      padding: 18pt 0 14pt;
      border-bottom: 1.5pt solid var(--ink);
      margin-bottom: 16pt;
    }
    .hero h1 {
      font-size: 24pt;
      font-weight: 500;
      letter-spacing: 0.05em;
      line-height: 1.2;
    }
    .hero .tagline {
      font-family: 'Source Han Sans SC', 'PingFang SC', sans-serif;
      font-size: 10pt;
      color: var(--muted);
      margin-top: 5pt;
    }

    .grid { display: grid; grid-template-columns: 1fr 1fr; gap: 14pt; }
    .block { padding: 10pt; background: #edeade; border-radius: 3pt; }
    .block-label {
      font-family: 'Source Han Sans SC', sans-serif;
      font-size: 7pt;
      font-weight: 600;
      letter-spacing: 0.12em;
      text-transform: uppercase;
      color: var(--muted);
      margin-bottom: 5pt;
    }
    .block p {
      font-size: 9.5pt;
      line-height: 1.5;
      color: #3d3427;
    }

    .metric-row {
      display: flex;
      justify-content: space-around;
      margin: 14pt 0;
      padding: 10pt;
      border-top: 0.5pt solid var(--border);
      border-bottom: 0.5pt solid var(--border);
    }
    .metric { text-align: center; }
    .metric .num {
      font-size: 20pt;
      font-weight: 500;
      color: var(--ink);
      line-height: 1.1;
    }
    .metric .label {
      font-family: 'Source Han Sans SC', sans-serif;
      font-size: 8pt;
      color: var(--muted);
    }
  </style>
</head>
<body>

  <div class="hero">
    <h1>公司名称</h1>
    <p class="tagline">一句话描述公司核心价值主张</p>
  </div>

  <div class="metric-row">
    <div class="metric">
      <div class="num">300万+</div>
      <div class="label">注册用户</div>
    </div>
    <div class="metric">
      <div class="num">98%</div>
      <div class="label">续约率</div>
    </div>
    <div class="metric">
      <div class="num">42个</div>
      <div class="label">覆盖城市</div>
    </div>
  </div>

  <div class="grid">
    <div class="block">
      <div class="block-label">产品</div>
      <p>核心产品描述，聚焦用户痛点与解决方案，控制在三句话以内。</p>
    </div>
    <div class="block">
      <div class="block-label">市场</div>
      <p>目标市场规模与增长空间，TAM/SAM 数据，竞争格局简述。</p>
    </div>
    <div class="block">
      <div class="block-label">商业模式</div>
      <p>收入来源、定价策略、毛利结构，一段话说清楚。</p>
    </div>
    <div class="block">
      <div class="block-label">团队</div>
      <p>核心团队背景亮点，行业经验与过往成就，简洁有力。</p>
    </div>
  </div>

</body>
</html>
```

### Inline SVG Diagram — Architecture

```html
<!-- Architecture diagram: fits inside any Kami document -->
<svg xmlns="http://www.w3.org/2000/svg" width="480" height="200" viewBox="0 0 480 200">
  <rect width="480" height="200" rx="4" fill="#edeade"/>

  <!-- Node style: ink-blue fill, parchment text -->
  <rect x="20"  y="80" width="90" height="36" rx="3" fill="#1B365D"/>
  <text x="65"  y="103" text-anchor="middle" fill="#f5f4ed"
        font-family="Inter,sans-serif" font-size="9" font-weight="500">Client</text>

  <rect x="195" y="80" width="90" height="36" rx="3" fill="#1B365D"/>
  <text x="240" y="103" text-anchor="middle" fill="#f5f4ed"
        font-family="Inter,sans-serif" font-size="9" font-weight="500">API Gateway</text>

  <rect x="370" y="80" width="90" height="36" rx="3" fill="#1B365D"/>
  <text x="415" y="103" text-anchor="middle" fill="#f5f4ed"
        font-family="Inter,sans-serif" font-size="9" font-weight="500">Service</text>

  <!-- Arrows -->
  <line x1="110" y1="98" x2="193" y2="98" stroke="#1B365D" stroke-width="1.5"
        marker-end="url(#arr)"/>
  <line x1="285" y1="98" x2="368" y2="98" stroke="#1B365D" stroke-width="1.5"
        marker-end="url(#arr)"/>

  <defs>
    <marker id="arr" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto">
      <path d="M0,0 L0,6 L8,3 z" fill="#1B365D"/>
    </marker>
  </defs>
</svg>
```

### Inline SVG Diagram — Quadrant

```html
<!-- 2×2 quadrant matrix -->
<svg xmlns="http://www.w3.org/2000/svg" width="320" height="280" viewBox="0 0 320 280">
  <rect width="320" height="280" rx="4" fill="#edeade"/>

  <!-- Axes -->
  <line x1="160" y1="20"  x2="160" y2="240" stroke="#d4cfc4" stroke-width="1"/>
  <line x1="20"  y1="140" x2="300" y2="140" stroke="#d4cfc4" stroke-width="1"/>

  <!-- Quadrant labels -->
  <text x="85"  y="38"  text-anchor="middle" font-family="Inter,sans-serif"
        font-size="8" fill="#8a7f6e">Low Effort · High Impact</text>
  <text x="245" y="38"  text-anchor="middle" font-family="Inter,sans-serif"
        font-size="8" fill="#8a7f6e">High Effort · High Impact</text>
  <text x="85"  y="258" text-anchor="middle" font-family="Inter,sans-serif"
        font-size="8" fill="#8a7f6e">Low Effort · Low Impact</text>
  <text x="245" y="258" text-anchor="middle" font-family="Inter,sans-serif"
        font-size="8" fill="#8a7f6e">High Effort · Low Impact</text>

  <!-- Data points -->
  <circle cx="90"  cy="80"  r="6" fill="#1B365D"/>
  <text   x="98"   y="84"   font-family="Inter,sans-serif" font-size="8" fill="#1B365D">Quick win</text>
  <circle cx="220" cy="70"  r="6" fill="#2c4a7a"/>
  <text   x="228"  y="74"   font-family="Inter,sans-serif" font-size="8" fill="#1B365D">Big bet</text>
</svg>
```

## Prompt Patterns (What to Say)

The skill auto-triggers. Just describe your need naturally:

```
make a one-pager for my startup Acme — B2B SaaS for logistics, $2M ARR, 
Series A raise, targeting US mid-market. Include 3 key metrics.

---

build me a 6-slide deck for my talk on distributed tracing.
Include an architecture diagram and a quadrant comparing approaches.

---

write a recommendation letter from a CTO recommending Sarah Chen 
for a senior ML role. Formal, warm, two pages.

---

帮我做一份 Kaku 项目的作品集，6 页，中文，突出技术亮点和用户数据。

---

generate an Elon Musk style resume — founder CV, 2 pages, 
chronological, English.
```

## Critical Rules for Generation

When generating any Kami document, the agent **must** enforce:

1. **Never use `rgba()` for tag/badge backgrounds** — use solid hex. WeasyPrint renders `rgba()` as a double rectangle.
2. **Never use `font-weight: bold` or `700` on serif headings** — lock at `500`.
3. **Never use `line-height: 1.6` or higher** on any element.
4. **Never use pure white (`#ffffff`) as the page background** — always `#f5f4ed`.
5. **Never introduce a second chromatic color** — the only accent is `#1B365D`. Variations are `#2c4a7a` (mid) and `#4a6fa5` (soft).
6. **Always set** `-webkit-print-color-adjust: exact; print-color-adjust: exact;` on `body` so backgrounds survive PDF export.
7. **Always use `@page` with A4 margins** unless the document type is Slides (use 16:9 or letter-landscape).
8. **Slides layout:** use `width: 254mm; height: 143mm;` per slide with `page-break-after: always`.

## Rendering to PDF

**Browser (recommended for demos):**
```
File → Print → Save as PDF
Margins: None or Minimum
Background graphics: ✓ enabled
```

**WeasyPrint (CI/server):**
```bash
pip install weasyprint
weasyprint document.html document.pdf
```

**Node (Puppeteer):**
```js
const puppeteer = require('puppeteer');

async function htmlToPdf(htmlPath, pdfPath) {
  const browser = await puppeteer.launch();
  const page = await browser.newPage();
  await page.goto(`file://${htmlPath}`, { waitUntil: 'networkidle0' });
  await page.pdf({
    path: pdfPath,
    format: 'A4',
    printBackground: true,   // critical for parchment canvas
    margin: { top: '0', right: '0', bottom: '0', left: '0' },
  });
  await browser.close();
}
```

## Slide Deck Structure

```html
<style>
  @page { size: 254mm 143mm; margin: 0; }
  body  { margin: 0; padding: 0; background: #f5f4ed; }

  .slide {
    width: 254mm;
    height: 143mm;
    background: #f5f4ed;
    padding: 12mm 14mm;
    page-break-after: always;
    overflow: hidden;
    position: relative;
    -webkit-print-color-adjust: exact;
    print-color-adjust: exact;
  }
  .slide:last-child { page-break-after: avoid; }

  /* Accent bar — left edge signature element */
  .slide::before {
    content: '';
    position: absolute;
    left: 0; top: 0; bottom: 0;
    width: 3pt;
    background: #1B365D;
  }
</style>

<div class="slide">
  <h1 style="font-size:28pt;font-weight:500;line-height:1.15;margin-top:16mm;">
    Talk Title
  </h1>
  <p style="font-family:Inter,sans-serif;font-size:11pt;color:#8a7f6e;margin-top:8pt;">
    Subtitle or speaker name · Date
  </p>
</div>

<div class="slide">
  <h2 style="font-family:Inter,sans-serif;font-size:7pt;letter-spacing:.12em;
             text-transform:uppercase;color:#8a7f6e;margin-bottom:10pt;">
    Section 01
  </h2>
  <h3 style="font-size:16pt;font-weight:500;line-height:1.25;margin-bottom:10pt;">
    Slide Heading
  </h3>
  <ul style="font-size:10pt;line-height:1.5;color:#3d3427;padding-left:14pt;">
    <li>First key point with specific data or claim</li>
    <li>Second key point — concrete, not abstract</li>
    <li>Third key point — end with implication</li>
  </ul>
</div>
```

## Reference Files

| File | Purpose |
|---|---|
| `references/design.md` | Full design spec (Chinese) |
| `references/design.en.md` | Full design spec (English) |
| `CHEATSHEET.md` | Quick token reference (Chinese) |
| `CHEATSHEET.en.md` | Quick token reference (English) |
| `assets/demos/` | PDF + PNG demo outputs for all 6 types |

## Troubleshooting

**Backgrounds missing in PDF export:**
→ Add `-webkit-print-color-adjust: exact; print-color-adjust: exact;` to `body`. Enable "Background graphics" in browser print dialog.

**Tags render as double rectangles:**
→ Replace any `rgba()` background with a solid hex value. This is a known WeasyPrint bug.

**Chinese text falls back to system font:**
→ Embed TsangerJinKai02 via `@font-face` or ensure the font is installed system-wide. Source Han Sans SC is a safe fallback.

**Serif headings look too heavy:**
→ Check `font-weight` — must be `500`, not `600`, `700`, or `bold`.

**Line-height feels airy / not editorial:**
→ Titles must be `1.1–1.3`. Body must be `1.5–1.55`. Remove any `line-height: 1.6+`.

**Second color crept in:**
→ Audit for any non-neutral color. Only `#1B365D`, `#2c4a7a`, `#4a6fa5` are chromatic. Everything else must be the warm neutral ramp (`#f5f4ed` → `#edeade` → `#d4cfc4` → `#8a7f6e` → `#3d3427` → `#1B365D`).
