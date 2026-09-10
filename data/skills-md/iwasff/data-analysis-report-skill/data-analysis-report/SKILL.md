---
name: data-analysis-report
description: >
  Build polished, production-grade standalone HTML data analysis reports and
  dashboards — from raw data or descriptions. Use this skill whenever the user
  asks to build a data report, analytics dashboard, business analysis page,
  KPI summary, or any multi-section data visualization document. Also trigger for:
  "make a report", "visualize this data", "dashboard for my data", "analysis HTML",
  "退货分析", "数据报告", "仪表盘", "可视化报告". This skill covers the full workflow:
  interviewing the user, choosing a visual style, generating charts with ECharts,
  and delivering a single self-contained HTML file with animations and interactions.
  Always use this skill — don't design data reports from scratch.
---

# Data Analysis Report Skill

A complete workflow and design system for building beautiful, self-contained HTML
data reports. Covers two structural modes (Analysis dashboard, Narrative slides),
five palettes, five UI styles, four typography stacks, and three motion levels —
selectable via the **Style Config** system.

---

## 5-Axis Style System

Every report is defined by exactly five dimensions. The combination is captured in
a **Style Config** block that the user can copy, paste, or generate via the
Phase 0 Artifact.

```
╔═ STYLE CONFIG v3.0 ════════════╗
  Mode       │ analysis
  Palette    │ warm-green
  UI Style   │ solid
  Typography │ serif
  Motion     │ standard
╚════════════════════════════════╝
```

| Axis | Options | File |
|------|---------|------|
| **Mode** | `analysis` · `narrative` | `dimensions/mode.md` |
| **Palette** | `warm-green` · `ocean-blue` · `slate-warm` · `dark-glass` · `ice-glass` | `dimensions/palette.md` |
| **UI Style** | `solid` · `glass` · `minimal` · `editorial` · `glass-round` | `dimensions/ui-style.md` |
| **Typography** | `serif` · `sans` · `mono-heavy` · `glass-round` | `dimensions/typography.md` |
| **Motion** | `subtle` · `standard` · `expressive` | `dimensions/motion.md` |

**Natural combinations (from the five demo files):**

| Demo | Mode | Palette | UI Style | Typography | Motion |
|------|------|---------|----------|------------|--------|
| A | analysis | warm-green | solid | serif | standard |
| B | analysis | ocean-blue | solid | sans | standard |
| C | narrative | dark-glass | glass | sans | expressive |
| D | narrative | slate-warm | editorial | serif | standard |
| E | analysis | ice-glass | glass-round | glass-round | standard |

---

## Phase 0: Style Discovery

### Mandatory first step when style is missing

**If the user has not pasted a complete Style Config block, Phase 0 is mandatory.**
Do not choose defaults, ask direct style questions, or start generating the
report. First provide the Phase 0 Style Selector to the user and wait for the
generated Style Config.

Use the canonical selector file directly:

```
demos/phase0-style-selector.html
```

Deliver that HTML to the user as the Phase 0 artifact/output without modifying
it. In Codex-style local workflows, copy this exact file to the user-facing
outputs directory and link it. In artifact-capable chat workflows, render this
exact file as the HTML artifact.

Tell the user:

> "请先在 Phase 0 Style Selector 里选择报告风格。完成 5 步后，复制页面生成的
> STYLE CONFIG 块发回来；我收到 Config 后再进入数据确认、结构规划和报告生成。"

After providing Phase 0, stop. The next report-generation step begins only
after the user sends back the Style Config.

### Style Config Provided

**When the user pastes a Style Config block**, parse it immediately:

```
Mode       → dimensions/mode.md
Palette    → dimensions/palette.md
UI Style   → dimensions/ui-style.md
Typography → dimensions/typography.md
Motion     → dimensions/motion.md
```

Acknowledge the config, confirm the data topic, and proceed to Phase 1.


---

## Phase 1: Content & Structure

1. **Confirm data** — Ask for data if not yet provided (CSV, JSON, paste numbers, or "use sample data")
2. **Propose structure** — Based on Mode:
   - `analysis`: Cover → Overview KPIs → 3–6 numbered sections → optional Action Plan
   - `narrative`: 6–12 scroll-snap slides, each with a single focused message
3. **Announce the plan** — List section titles and what each contains before coding

Max 5–8 sections for analysis; 6–12 slides for narrative.

---

## Phase 2: Build the Report

Read the relevant dimension files before writing any code:

```
dimensions/mode.md        → layout skeleton (analysis or narrative)
dimensions/palette.md     → :root CSS variables for chosen palette
dimensions/ui-style.md    → card/section CSS rules
dimensions/typography.md  → font imports and type scale
dimensions/motion.md      → animation CSS + JS snippets
```

Then read components:
```
references/components-analysis.md   (if mode = analysis)
references/components-narrative.md  (if mode = narrative)
references/animations.md            (for IntersectionObserver patterns)
```

### File constraints
- Single self-contained `.html` — no external CSS, no npm, no frameworks
- CDN only: Google Fonts + ECharts 5 (`cdn.jsdelivr.net`)
- All CSS and JS inline

### Style Config comment header (mandatory, first line of `<style>`)

```css
/* ─── STYLE CONFIG ───────────────────────────────────────────
   Mode       : [value]
   Palette    : [value]
   UI Style   : [value]
   Typography : [value]   ([font names])
   Motion     : [value]
──────────────────────────────────────────────────────────── */
```

### Sidebar Style Config display (analysis mode)

Inside the sidebar, render the active config as a small `<pre>` block so users
can see what style was applied:

```html
<div class="sb-cfg">
  <div class="sb-cfg-t">STYLE CONFIG</div>
  <pre class="sb-cfg-pre">╔═ STYLE CONFIG v3.0 ════════╗
  Mode       │ analysis
  Palette    │ warm-green
  UI Style   │ solid
  Typography │ serif
  Motion     │ standard
╚════════════════════════════╝</pre>
</div>
```

---

## Core Design Rules

**Cards always lighter than sections.** In solid/minimal/editorial modes, section
backgrounds must be visually distinct from card backgrounds. Test the contrast — if
they look similar, darken the section bg.

**Text must be dark.** Minimum `#3A4430` for body copy in light themes. In Ice Glass:
`#2F414A` for primary, `rgba(47,65,74,.5)` for labels.

**Charts go full-width first.** A chart card spans the full section width.
Below it: 2-column grid — left 2×2 insight strips, right data table.
Never put two charts side-by-side (height mismatch creates whitespace).

**No emoji in UI.** SVG icons only. See `references/components-analysis.md` for the icon library.

**No-data cells are warm.** Heatmap empty cells: `background:#EDE8C0; color:#A3B18A`.
Map no-data: `outOfRange:{color:'#FFFFFF'}`. Never grey.

**Every section element gets `.reveal`.** All section content fades up on scroll.

**Cover replays on return.** Use `.playing` class — cover animations re-trigger
every time the user scrolls back to top.

---

## Checklist Before Delivery

- [ ] Style Config comment in `<style>` header matches requested config
- [ ] All colors from the chosen palette only — no ad-hoc hex values
- [ ] Section backgrounds visually distinct from card backgrounds (solid/minimal/editorial modes)
- [ ] Text contrast meets minimum values for chosen palette
- [ ] Charts full-width; below = 2-col (2×2 insight grid | data table) — analysis mode
- [ ] Every section element has `.reveal` + optional `.delay-N`
- [ ] Cover re-animates on scroll return (`.playing` class) — analysis mode
- [ ] No emoji — SVG icons only
- [ ] `IntersectionObserver` observes Elements not NodeLists
- [ ] Every EChart has `window.addEventListener('resize', () => chart.resize())`
- [ ] Single `.html` file, no external deps except CDN fonts + ECharts
- [ ] **Glass / Glass-Round only**: all `.card` have `backdrop-filter: blur(28px)` + `-webkit-backdrop-filter`
- [ ] **Ice Glass only**: `body` uses `background: ... fixed`, sections transparent, navbar `#2F414A`
- [ ] **Narrative only**: `html` has `scroll-snap-type: y mandatory`, each slide `scroll-snap-align: start; height: 100vh`

---

## Phase 0 Artifact

The canonical Phase 0 artifact is `demos/phase0-style-selector.html`.
Use that file directly whenever Phase 0 is required. The embedded copy below is
legacy reference material only; prefer the demo file so users always receive the maintained selector.

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Report Skill · Phase 0 · Style Selector</title>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Space+Mono:wght@400;700&display=swap" rel="stylesheet">
<style>
:root {
  --bg: #f4f5f7;
  --card: #ffffff;
  --bd: #e2e5ea;
  --bd-sel: #4a7ab5;
  --t1: #1a1f2e;
  --t2: #5a6478;
  --t3: #9aa0ae;
  --acc: #4a7ab5;
  --acc2: #6a9ad5;
  --r: 14px;
  --ff: 'Inter', sans-serif;
  --fm: 'Space Mono', monospace;
}
*, *::before, *::after { margin:0; padding:0; box-sizing:border-box }
body { font-family: var(--ff); background: var(--bg); color: var(--t1); min-height: 100vh; }
.header { background: #1a1f2e; padding: 18px 32px; display: flex; align-items: center; justify-content: space-between; }
.hdr-brand { display: flex; align-items: center; gap: 10px }
.hdr-dot { width: 8px; height: 8px; border-radius: 50%; background: #6a9ad5; animation: dp 2.5s ease-in-out infinite }
@keyframes dp { 0%,100%{opacity:.5} 50%{opacity:1;box-shadow:0 0 8px #6a9ad5} }
.hdr-title { font-family: var(--fm); font-size: 12px; color: rgba(255,255,255,.7); letter-spacing: .12em }
.hdr-step { font-family: var(--fm); font-size: 11px; color: rgba(255,255,255,.35); letter-spacing: .1em }
.progress-wrap { padding: 20px 32px 0; }
.progress-bar { height: 3px; background: var(--bd); border-radius: 2px; overflow: hidden }
.progress-fill { height: 100%; background: linear-gradient(90deg, var(--acc), var(--acc2)); border-radius: 2px; transition: width .5s cubic-bezier(.16,1,.3,1) }
.progress-steps { display: flex; justify-content: space-between; margin-top: 8px }
.ps { font-family: var(--fm); font-size: 10px; color: var(--t3); letter-spacing: .08em; transition: color .3s }
.ps.done { color: var(--acc) }
.ps.active { color: var(--t1); font-weight: 700 }
.main { max-width: 900px; margin: 0 auto; padding: 32px 24px 80px; }
.axis-section { display: none; animation: fadeUp .4s cubic-bezier(.16,1,.3,1) }
.axis-section.active { display: block }
@keyframes fadeUp { from{opacity:0;transform:translateY(16px)} to{opacity:1;transform:translateY(0)} }
.axis-header { margin-bottom: 24px }
.axis-ew { font-family: var(--fm); font-size: 10px; letter-spacing: .2em; text-transform: uppercase; color: var(--acc); display: flex; align-items: center; gap: 8px; margin-bottom: 10px }
.axis-ew::before { content: ''; width: 14px; height: 1px; background: currentColor }
.axis-title { font-size: 22px; font-weight: 800; color: var(--t1); margin-bottom: 6px; letter-spacing: -.02em }
.axis-desc { font-size: 14px; color: var(--t2); line-height: 1.65 }
.option-grid { display: grid; gap: 14px }
.option-grid.cols-2 { grid-template-columns: 1fr 1fr }
.option-grid.cols-3 { grid-template-columns: repeat(3, 1fr) }
.option-grid.cols-4 { grid-template-columns: repeat(4, 1fr) }
.option-grid.cols-5 { grid-template-columns: repeat(5, 1fr) }
.opt-card { background: var(--card); border: 2px solid var(--bd); border-radius: var(--r); padding: 18px 16px; cursor: pointer; transition: border-color .2s, transform .2s cubic-bezier(.34,1.56,.64,1), box-shadow .2s; position: relative; overflow: hidden; user-select: none; }
.opt-card:hover { border-color: var(--bd-sel); transform: translateY(-3px); box-shadow: 0 8px 24px rgba(74,122,181,.12) }
.opt-card.selected { border-color: var(--bd-sel); box-shadow: 0 0 0 3px rgba(74,122,181,.15), 0 8px 24px rgba(74,122,181,.15); transform: translateY(-3px) }
.opt-card.selected::after { content: '✓'; position: absolute; top: 10px; right: 12px; font-family: var(--fm); font-size: 11px; color: var(--acc); font-weight: 700 }
.prev-label { font-family: var(--fm); font-size: 9px; letter-spacing: .12em; text-transform: uppercase; color: var(--t3); margin-bottom: 8px; font-weight: 700 }
.prev-mode { height: 72px; border-radius: 8px; overflow: hidden; margin-bottom: 4px; position: relative }
.prev-mode-analysis { background: #1a2f3a; display: flex }
.pma-sidebar { width: 30%; background: #0f1e26; display: flex; flex-direction: column; gap: 3px; padding: 6px 5px }
.pma-nav { height: 5px; border-radius: 2px; background: rgba(255,255,255,.12) }
.pma-nav.on { background: rgba(91,141,184,.6) }
.pma-content { flex: 1; display: flex; flex-direction: column; gap: 4px; padding: 6px }
.pma-kpi { display: grid; grid-template-columns: repeat(3,1fr); gap: 3px }
.pma-k { height: 14px; border-radius: 3px; background: rgba(255,255,255,.08) }
.pma-chart { flex: 1; border-radius: 3px; background: rgba(255,255,255,.05) }
.prev-mode-narrative { background: #1a1f2e; display: flex; flex-direction: column; justify-content: center; align-items: center; gap: 4px }
.pmn-h { height: 8px; width: 55%; border-radius: 2px; background: rgba(255,255,255,.25) }
.pmn-s { height: 4px; width: 35%; border-radius: 2px; background: rgba(255,255,255,.1) }
.pmn-dots { display: flex; gap: 3px; margin-top: 4px }
.pmn-dot { width: 4px; height: 4px; border-radius: 50%; background: rgba(255,255,255,.15) }
.pmn-dot.on { background: rgba(91,141,184,.8) }
.prev-palette { height: 44px; border-radius: 8px; overflow: hidden; display: flex; margin-bottom: 4px }
.sw { flex: 1 }
.prev-ui { height: 60px; border-radius: 8px; overflow: hidden; margin-bottom: 4px; display: flex; align-items: center; justify-content: center; gap: 6px; padding: 8px }
.ui-card-glass { background: rgba(255,255,255,.3); backdrop-filter: blur(8px); border: 1px solid rgba(255,255,255,.6); border-radius: 10px; padding: 6px 10px; font-size: 10px; color: #2F414A; font-weight: 600 }
.ui-card-solid { background: #F9F3DC; border: 1px solid #C8D9A8; border-radius: 8px; padding: 6px 10px; font-size: 10px; color: #3A4430; font-weight: 600 }
.ui-card-minimal { border: 1.5px solid #9aa0ae; border-radius: 6px; padding: 6px 10px; font-size: 10px; color: #5a6478; font-weight: 600 }
.ui-card-editorial { border-left: 3px solid #C17F4A; padding: 6px 10px 6px 14px; font-size: 10px; color: #2A2A2A; font-weight: 700; font-family: Georgia, serif }
.ui-card-round { background: rgba(255,255,255,.35); border: 1.5px solid rgba(255,255,255,.7); border-radius: 14px; padding: 6px 12px; font-size: 10px; color: #2F414A; font-weight: 600 }
.prev-type { height: 56px; border-radius: 8px; background: #f8f9fb; border: 1px solid var(--bd); display: flex; flex-direction: column; justify-content: center; padding: 0 12px; margin-bottom: 4px; gap: 3px; overflow: hidden }
.type-big { font-size: 20px; font-weight: 800; line-height: 1; color: var(--t1); white-space: nowrap }
.type-small { font-size: 10px; color: var(--t3); font-family: var(--fm) }
.prev-motion { height: 60px; border-radius: 8px; background: #1a1f2e; margin-bottom: 4px; display: flex; align-items: center; justify-content: center; gap: 6px; overflow: hidden; position: relative }
.motion-bar { height: 6px; border-radius: 3px; background: rgba(106,154,213,.5) }
.motion-dot { width: 8px; height: 8px; border-radius: 50%; background: rgba(106,154,213,.7) }
.opt-name { font-size: 13px; font-weight: 700; color: var(--t1); margin-bottom: 3px }
.opt-sub  { font-size: 11px; color: var(--t2); line-height: 1.5 }
.opt-tag  { font-family: var(--fm); font-size: 9px; padding: 2px 7px; border-radius: 100px; background: rgba(74,122,181,.1); color: var(--acc); border: 1px solid rgba(74,122,181,.2); display: inline-block; margin-top: 8px; font-weight: 700; letter-spacing: .04em }
.btn-row { display: flex; gap: 10px; margin-top: 32px; justify-content: flex-end }
.btn { padding: 10px 24px; border-radius: 8px; font-family: var(--ff); font-size: 14px; font-weight: 600; cursor: pointer; border: none; transition: all .2s }
.btn-back { background: var(--card); border: 1.5px solid var(--bd); color: var(--t2) }
.btn-back:hover { border-color: var(--t2); color: var(--t1) }
.btn-next { background: var(--acc); color: #fff; box-shadow: 0 4px 12px rgba(74,122,181,.3) }
.btn-next:hover { background: #3a6aa5; transform: translateY(-1px); box-shadow: 0 6px 16px rgba(74,122,181,.4) }
.btn-next:disabled { background: var(--bd); color: var(--t3); box-shadow: none; transform: none; cursor: not-allowed }
.config-section { display: none; animation: fadeUp .4s cubic-bezier(.16,1,.3,1) }
.config-section.active { display: block }
.config-wrap { background: var(--card); border: 1px solid var(--bd); border-radius: 16px; padding: 28px 32px; margin-bottom: 20px }
.config-title { font-size: 18px; font-weight: 800; color: var(--t1); margin-bottom: 4px }
.config-sub { font-size: 14px; color: var(--t2); margin-bottom: 24px }
.config-pills { display: flex; gap: 8px; flex-wrap: wrap; margin-bottom: 24px }
.cfg-pill { display: flex; align-items: center; gap: 7px; background: var(--bg); border: 1px solid var(--bd); border-radius: 100px; padding: 6px 14px }
.cfg-pill-k { font-family: var(--fm); font-size: 10px; color: var(--t3); letter-spacing: .06em }
.cfg-pill-v { font-family: var(--fm); font-size: 11px; color: var(--t1); font-weight: 700 }
.config-code-wrap { position: relative }
.config-code { background: #1a1f2e; border-radius: 12px; padding: 20px 22px; font-family: var(--fm); font-size: 13px; color: rgba(200,215,235,.8); line-height: 2; white-space: pre; }
.config-code .acc { color: #9bb4cb; font-weight: 700 }
.config-code .dim { color: rgba(200,215,235,.3) }
.copy-btn { position: absolute; top: 12px; right: 12px; background: rgba(255,255,255,.08); border: 1px solid rgba(255,255,255,.12); border-radius: 8px; padding: 5px 12px; font-family: var(--fm); font-size: 10px; color: rgba(200,215,235,.7); cursor: pointer; transition: all .2s; letter-spacing: .06em }
.copy-btn:hover { background: rgba(255,255,255,.14); color: #fff }
.copy-btn.copied { background: rgba(74,122,181,.3); color: #9bb4cb; border-color: rgba(74,122,181,.4) }
.config-hint { font-size: 13px; color: var(--t2); line-height: 1.7; padding: 14px 18px; background: rgba(74,122,181,.06); border: 1px solid rgba(74,122,181,.12); border-radius: 10px }
.config-hint strong { color: var(--acc) }
.restart-btn { display: flex; align-items: center; gap: 8px; background: none; border: 1.5px solid var(--bd); border-radius: 8px; padding: 9px 18px; font-family: var(--ff); font-size: 13px; color: var(--t2); cursor: pointer; transition: all .2s; margin-top: 16px }
.restart-btn:hover { border-color: var(--t2); color: var(--t1) }
@keyframes dp2 { 0%,100%{opacity:.4;transform:scale(1)} 50%{opacity:1;transform:scale(1.3);box-shadow:0 0 8px rgba(106,154,213,.6)} }
</style>
</head>
<body>
<div class="header">
  <div class="hdr-brand">
    <div class="hdr-dot"></div>
    <span class="hdr-title">DATA ANALYSIS REPORT SKILL · PHASE 0</span>
  </div>
  <span class="hdr-step" id="hdr-step">STYLE SELECTOR</span>
</div>
<div class="progress-wrap">
  <div class="progress-bar"><div class="progress-fill" id="prog-fill" style="width:17%"></div></div>
  <div class="progress-steps">
    <span class="ps active" id="ps0">01 · Mode</span>
    <span class="ps" id="ps1">02 · Palette</span>
    <span class="ps" id="ps2">03 · UI Style</span>
    <span class="ps" id="ps3">04 · Typography</span>
    <span class="ps" id="ps4">05 · Motion</span>
    <span class="ps" id="ps5">Config</span>
  </div>
</div>
<div class="main">

<!-- STEP 0: MODE -->
<div class="axis-section active" id="step-0">
  <div class="axis-header">
    <div class="axis-ew">Dimension 01</div>
    <div class="axis-title">报告模式 Mode</div>
    <div class="axis-desc">决定整体布局逻辑 — Analysis 适合「读数据」，Narrative 适合「讲故事」</div>
  </div>
  <div class="option-grid cols-2">
    <div class="opt-card" data-axis="mode" data-val="analysis" onclick="select(this)">
      <div class="prev-label">布局预览</div>
      <div class="prev-mode">
        <div class="prev-mode-analysis">
          <div class="pma-sidebar"><div class="pma-nav on"></div><div class="pma-nav"></div><div class="pma-nav"></div><div class="pma-nav"></div></div>
          <div class="pma-content"><div class="pma-kpi"><div class="pma-k"></div><div class="pma-k"></div><div class="pma-k"></div></div><div class="pma-chart"></div></div>
        </div>
      </div>
      <div class="opt-name">Analysis 分析模式</div>
      <div class="opt-sub">侧边栏导航 + 多 Section + KPI 指标条 + 图表切换，适合数据密集、需要导航跳转的报告</div>
      <span class="opt-tag">退货分析 · 卖点分析 · 月报</span>
    </div>
    <div class="opt-card" data-axis="mode" data-val="narrative" onclick="select(this)">
      <div class="prev-label">布局预览</div>
      <div class="prev-mode">
        <div class="prev-mode-narrative">
          <div class="pmn-h"></div><div class="pmn-s"></div>
          <div class="pmn-dots"><div class="pmn-dot on"></div><div class="pmn-dot"></div><div class="pmn-dot"></div><div class="pmn-dot"></div></div>
        </div>
      </div>
      <div class="opt-name">Narrative 叙事模式</div>
      <div class="opt-sub">全屏 scroll-snap Slide，每页聚焦一个核心内容，读者「翻页」而非滚动，适合作品集、Demo 展示、汇报</div>
      <span class="opt-tag">作品集 · Demo · 对外展示</span>
    </div>
  </div>
  <div class="btn-row"><button class="btn btn-next" id="btn-0" onclick="next(0)" disabled>选择后继续 →</button></div>
</div>

<!-- STEP 1: PALETTE -->
<div class="axis-section" id="step-1">
  <div class="axis-header">
    <div class="axis-ew">Dimension 02</div>
    <div class="axis-title">配色方案 Palette</div>
    <div class="axis-desc">决定整体色调和氛围 — 5 套配色适合不同场景和受众</div>
  </div>
  <div class="option-grid cols-5">
    <div class="opt-card" data-axis="palette" data-val="warm-green" onclick="select(this)">
      <div class="prev-palette"><div class="sw" style="background:#D0986A"></div><div class="sw" style="background:#7EA090"></div><div class="sw" style="background:#EDE8C0"></div><div class="sw" style="background:#F9F3DC"></div><div class="sw" style="background:#293D33"></div></div>
      <div class="opt-name">Warm-Green</div>
      <div class="opt-sub" style="font-size:10px">暖琥珀 + 森林绿，专业朴实</div>
      <span class="opt-tag">默认推荐</span>
    </div>
    <div class="opt-card" data-axis="palette" data-val="ocean-blue" onclick="select(this)">
      <div class="prev-palette"><div class="sw" style="background:#906060"></div><div class="sw" style="background:#5B8DB8"></div><div class="sw" style="background:#D8E8F0"></div><div class="sw" style="background:#F0F8FC"></div><div class="sw" style="background:#1A2F3A"></div></div>
      <div class="opt-name">Ocean-Blue</div>
      <div class="opt-sub" style="font-size:10px">冷蓝 + 近黑，商务清晰</div>
      <span class="opt-tag">对外汇报</span>
    </div>
    <div class="opt-card" data-axis="palette" data-val="slate-warm" onclick="select(this)">
      <div class="prev-palette"><div class="sw" style="background:#C17F4A"></div><div class="sw" style="background:#6A6A5A"></div><div class="sw" style="background:#E8E0CC"></div><div class="sw" style="background:#F4EEE0"></div><div class="sw" style="background:#2A2A2A"></div></div>
      <div class="opt-name">Slate-Warm</div>
      <div class="opt-sub" style="font-size:10px">暖琥珀 + 深灰石，编辑现代</div>
      <span class="opt-tag">品牌报告</span>
    </div>
    <div class="opt-card" data-axis="palette" data-val="dark-glass" onclick="select(this)">
      <div class="prev-palette"><div class="sw" style="background:#7a9ab8"></div><div class="sw" style="background:#9bb4cb"></div><div class="sw" style="background:#2a3248"></div><div class="sw" style="background:#1f2128"></div><div class="sw" style="background:#141820"></div></div>
      <div class="opt-name">Dark-Glass</div>
      <div class="opt-sub" style="font-size:10px">烟蓝 + 近黑暗底，技术展示</div>
      <span class="opt-tag">Portfolio</span>
    </div>
    <div class="opt-card" data-axis="palette" data-val="ice-glass" onclick="select(this)">
      <div class="prev-palette"><div class="sw" style="background:#7DA59C"></div><div class="sw" style="background:#9BB8BC"></div><div class="sw" style="background:#B2CECB"></div><div class="sw" style="background:#DEEAEB"></div><div class="sw" style="background:#2F414A"></div></div>
      <div class="opt-name">Ice-Glass</div>
      <div class="opt-sub" style="font-size:10px">冰蓝渐变底 + 高透玻璃，通透清爽</div>
      <span class="opt-tag">品牌情报</span>
    </div>
  </div>
  <div class="btn-row"><button class="btn btn-back" onclick="back(1)">← 上一步</button><button class="btn btn-next" id="btn-1" onclick="next(1)" disabled>选择后继续 →</button></div>
</div>

<!-- STEP 2: UI STYLE -->
<div class="axis-section" id="step-2">
  <div class="axis-header">
    <div class="axis-ew">Dimension 03</div>
    <div class="axis-title">UI 风格 UI Style</div>
    <div class="axis-desc">决定卡片和组件的设计语言 — 独立于配色，可以自由组合</div>
  </div>
  <div class="option-grid cols-5">
    <div class="opt-card" data-axis="ui" data-val="glass" onclick="select(this)">
      <div class="prev-ui" style="background:linear-gradient(135deg,#4a7a96,#8fb8b4)"><div class="ui-card-glass">Report</div><div class="ui-card-glass">Data</div></div>
      <div class="opt-name">Glass</div>
      <div class="opt-sub" style="font-size:10px">backdrop-filter 毛玻璃，深色背景下通透浮动</div>
      <span class="opt-tag">Dark-Glass 常用</span>
    </div>
    <div class="opt-card" data-axis="ui" data-val="solid" onclick="select(this)">
      <div class="prev-ui" style="background:#7EA090"><div class="ui-card-solid">Report</div><div class="ui-card-solid">Data</div></div>
      <div class="opt-name">Solid</div>
      <div class="opt-sub" style="font-size:10px">实色填充卡片，层次清晰，兼容性最佳</div>
      <span class="opt-tag">默认推荐</span>
    </div>
    <div class="opt-card" data-axis="ui" data-val="minimal" onclick="select(this)">
      <div class="prev-ui" style="background:#f0f0ec"><div class="ui-card-minimal">Report</div><div class="ui-card-minimal">Data</div></div>
      <div class="opt-name">Minimal</div>
      <div class="opt-sub" style="font-size:10px">细边框无填充，极简留白，轻量克制</div>
      <span class="opt-tag">留白风格</span>
    </div>
    <div class="opt-card" data-axis="ui" data-val="editorial" onclick="select(this)">
      <div class="prev-ui" style="background:#E8E0CC"><div class="ui-card-editorial">Report</div><div class="ui-card-editorial">Data</div></div>
      <div class="opt-name">Editorial</div>
      <div class="opt-sub" style="font-size:10px">左侧色条 + 细边框，杂志排版感，字体驱动</div>
      <span class="opt-tag">叙事模式佳</span>
    </div>
    <div class="opt-card" data-axis="ui" data-val="glass-round" onclick="select(this)">
      <div class="prev-ui" style="background:linear-gradient(135deg,#6a9aa6,#CEDFDE)"><div class="ui-card-round">Report</div><div class="ui-card-round">Data</div></div>
      <div class="opt-name">Glass-Round</div>
      <div class="opt-sub" style="font-size:10px">高透白玻璃 + 超大圆角(24px)，圆润通透</div>
      <span class="opt-tag">Ice-Glass 专属</span>
    </div>
  </div>
  <div class="btn-row"><button class="btn btn-back" onclick="back(2)">← 上一步</button><button class="btn btn-next" id="btn-2" onclick="next(2)" disabled>选择后继续 →</button></div>
</div>

<!-- STEP 3: TYPOGRAPHY -->
<div class="axis-section" id="step-3">
  <div class="axis-header">
    <div class="axis-ew">Dimension 04</div>
    <div class="axis-title">字体风格 Typography</div>
    <div class="axis-desc">决定整体气质 — 英文数字和中文字体分别选择最搭配的方案</div>
  </div>
  <div class="option-grid cols-4">
    <div class="opt-card" data-axis="type" data-val="serif" onclick="select(this)">
      <div class="prev-type"><div class="type-big" style="font-family:Georgia,serif">Report</div><div class="type-small">Playfair Display + Noto Serif SC</div></div>
      <div class="opt-name">Serif</div>
      <div class="opt-sub" style="font-size:10px">Playfair Display 英文 + Noto Serif SC 中文，质感与权威并重</div>
      <span class="opt-tag">Warm / Slate 常用</span>
    </div>
    <div class="opt-card" data-axis="type" data-val="sans" onclick="select(this)">
      <div class="prev-type"><div class="type-big" style="font-family:'Inter',sans-serif">Report</div><div class="type-small">Montserrat + Inter + Noto Sans SC</div></div>
      <div class="opt-name">Sans</div>
      <div class="opt-sub" style="font-size:10px">Montserrat 数字 + Inter / Noto Sans SC，现代清晰，最通用</div>
      <span class="opt-tag">默认推荐</span>
    </div>
    <div class="opt-card" data-axis="type" data-val="mono-heavy" onclick="select(this)">
      <div class="prev-type"><div class="type-big" style="font-family:'Space Mono',monospace;font-size:16px">Report</div><div class="type-small">Space Mono 主导 + Noto Sans SC</div></div>
      <div class="opt-name">Mono-Heavy</div>
      <div class="opt-sub" style="font-size:10px">大量使用 Space Mono，技术感和代码感极强</div>
      <span class="opt-tag">技术文档</span>
    </div>
    <div class="opt-card" data-axis="type" data-val="glass-round" onclick="select(this)">
      <div class="prev-type" style="background:linear-gradient(135deg,rgba(107,154,166,.12),rgba(178,206,203,.12))"><div class="type-big" style="font-family:'Montserrat',sans-serif;letter-spacing:-.01em">Report</div><div class="type-small">Montserrat + 幼圆 / YouYuan</div></div>
      <div class="opt-name">Glass-Round</div>
      <div class="opt-sub" style="font-size:10px">Montserrat 圆润几何英文 + 幼圆中文，配合大圆角卡片</div>
      <span class="opt-tag">Ice-Glass 专属</span>
    </div>
  </div>
  <div class="btn-row"><button class="btn btn-back" onclick="back(3)">← 上一步</button><button class="btn btn-next" id="btn-3" onclick="next(3)" disabled>选择后继续 →</button></div>
</div>

<!-- STEP 4: MOTION -->
<div class="axis-section" id="step-4">
  <div class="axis-header">
    <div class="axis-ew">Dimension 05</div>
    <div class="axis-title">动效级别 Motion</div>
    <div class="axis-desc">决定报告的动态层次 — 动效越丰富加载越慢，按场景选择</div>
  </div>
  <div class="option-grid cols-3">
    <div class="opt-card" data-axis="motion" data-val="subtle" onclick="select(this)">
      <div class="prev-motion"><div style="display:flex;flex-direction:column;gap:5px;width:60%"><div class="motion-bar" style="width:80%;opacity:.4"></div><div class="motion-bar" style="width:60%;opacity:.3"></div><div class="motion-bar" style="width:70%;opacity:.35"></div></div></div>
      <div class="opt-name">Subtle 轻淡</div>
      <div class="opt-sub" style="font-size:10px">仅 Scroll Reveal 淡入，无额外动效。加载最快，专注内容</div>
      <span class="opt-tag">内部文档</span>
    </div>
    <div class="opt-card" data-axis="motion" data-val="standard" onclick="select(this)">
      <div class="prev-motion"><div style="display:flex;flex-direction:column;align-items:center;gap:6px"><div style="display:flex;gap:5px"><div class="motion-dot"></div><div class="motion-dot" style="opacity:.6"></div><div class="motion-dot" style="opacity:.4"></div></div><div class="motion-bar" style="width:80px"></div><div style="font-family:'Space Mono',monospace;font-size:9px;color:rgba(106,154,213,.6)">0 → 247</div></div></div>
      <div class="opt-name">Standard 标准</div>
      <div class="opt-sub" style="font-size:10px">Scroll Reveal + ECharts 入场 + Counter 计数器，平衡动效与性能</div>
      <span class="opt-tag">默认推荐</span>
    </div>
    <div class="opt-card" data-axis="motion" data-val="expressive" onclick="select(this)">
      <div class="prev-motion" style="overflow:hidden">
        <canvas id="mini-particles" width="200" height="60" style="position:absolute;inset:0;width:100%;height:100%"></canvas>
        <div style="position:relative;z-index:1;display:flex;flex-direction:column;align-items:center;gap:4px"><div style="font-family:'Space Mono',monospace;font-size:9px;color:rgba(106,154,213,.8)">Expressive</div><div style="display:flex;gap:4px"><div class="motion-dot" style="animation:dp2 1.5s ease-in-out infinite"></div><div class="motion-dot" style="animation:dp2 1.5s ease-in-out .3s infinite;opacity:.7"></div><div class="motion-dot" style="animation:dp2 1.5s ease-in-out .6s infinite;opacity:.5"></div></div></div>
      </div>
      <div class="opt-name">Expressive 全量</div>
      <div class="opt-sub" style="font-size:10px">粒子背景 + Stagger 错落入场 + 全量图表动效 + 旋转装饰</div>
      <span class="opt-tag">Portfolio · Demo</span>
    </div>
  </div>
  <div class="btn-row"><button class="btn btn-back" onclick="back(4)">← 上一步</button><button class="btn btn-next" id="btn-4" onclick="next(4)" disabled>生成 Config →</button></div>
</div>

<!-- CONFIG OUTPUT -->
<div class="config-section" id="step-5">
  <div class="axis-header">
    <div class="axis-ew">Style Config</div>
    <div class="axis-title">配置完成</div>
    <div class="axis-desc">复制下方 Config 块，粘贴到 Claude 对话里，直接开始生成报告</div>
  </div>
  <div class="config-wrap">
    <div class="config-title">你的 Style Config</div>
    <div class="config-sub">5 个维度已选定，Claude 读到此格式后会自动生成对应风格的报告</div>
    <div class="config-pills" id="cfg-pills"></div>
    <div class="config-code-wrap">
      <pre class="config-code" id="cfg-code"></pre>
      <button class="copy-btn" id="copy-btn" onclick="copyConfig()">COPY</button>
    </div>
  </div>
  <div class="config-hint">
    <strong>使用方式：</strong>把上方 Config 块完整复制，开始新对话后告诉 Claude：<br>
    「请使用以下 Style Config 帮我生成报告，数据是……」<br>
    Claude 会自动识别 Config 格式，按选定风格生成单文件 HTML 报告。
  </div>
  <button class="restart-btn" onclick="restart()">
    <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="1 4 1 10 7 10"/><path d="M3.51 15a9 9 0 1 0 .49-3.08"/></svg>
    重新选择
  </button>
</div>

</div>

<script>
const state = { mode:null, palette:null, ui:null, type:null, motion:null };
const keys  = ['mode','palette','ui','type','motion'];
const labels = { mode:'Mode', palette:'Palette', ui:'UI Style', type:'Typography', motion:'Motion' };
function select(el) {
  const axis = el.dataset.axis, val = el.dataset.val;
  document.querySelectorAll(`[data-axis="${axis}"]`).forEach(c=>c.classList.remove('selected'));
  el.classList.add('selected');
  state[axis] = val;
  const stepIdx = keys.indexOf(axis);
  const btn = document.getElementById('btn-'+stepIdx);
  if(btn) btn.disabled = false;
}
function next(stepIdx) {
  document.getElementById('step-'+stepIdx).classList.remove('active');
  const nextStep = stepIdx + 1;
  if(nextStep < 5) { document.getElementById('step-'+nextStep).classList.add('active'); }
  else { buildConfig(); document.getElementById('step-5').classList.add('active'); }
  updateProgress(nextStep);
}
function back(stepIdx) {
  document.getElementById('step-'+stepIdx).classList.remove('active');
  document.getElementById('step-'+(stepIdx-1)).classList.add('active');
  updateProgress(stepIdx-1);
}
function updateProgress(step) {
  const pct = Math.round((step+1)/6*100);
  document.getElementById('prog-fill').style.width = pct+'%';
  const lbs = ['01 · Mode','02 · Palette','03 · UI Style','04 · Typography','05 · Motion','Config'];
  for(let i=0;i<6;i++){
    const el=document.getElementById('ps'+i);
    el.className='ps'+(i<step?' done':i===step?' active':'');
  }
  document.getElementById('hdr-step').textContent = step<5?lbs[step]:'COMPLETE';
}
function buildConfig() {
  document.getElementById('cfg-pills').innerHTML = keys.map(k=>
    `<div class="cfg-pill"><span class="cfg-pill-k">${labels[k].toUpperCase()}</span><span class="cfg-pill-v">${state[k]}</span></div>`
  ).join('');
  document.getElementById('cfg-code').innerHTML =
    `<span class="dim">╔═ STYLE CONFIG v3.0 ════════════╗</span>\n`+
    `  Mode       │ <span class="acc">${state.mode}</span>\n`+
    `  Palette    │ <span class="acc">${state.palette}</span>\n`+
    `  UI Style   │ <span class="acc">${state.ui}</span>\n`+
    `  Typography │ <span class="acc">${state.type}</span>\n`+
    `  Motion     │ <span class="acc">${state.motion}</span>\n`+
    `<span class="dim">╚════════════════════════════════╝</span>`;
}
function copyConfig() {
  const text =
    `╔═ STYLE CONFIG v3.0 ════════════╗\n`+
    `  Mode       │ ${state.mode}\n`+
    `  Palette    │ ${state.palette}\n`+
    `  UI Style   │ ${state.ui}\n`+
    `  Typography │ ${state.type}\n`+
    `  Motion     │ ${state.motion}\n`+
    `╚════════════════════════════════╝`;
  navigator.clipboard.writeText(text).then(()=>{
    const btn=document.getElementById('copy-btn');
    btn.textContent='COPIED ✓'; btn.classList.add('copied');
    setTimeout(()=>{ btn.textContent='COPY'; btn.classList.remove('copied'); },2000);
  });
}
function restart() {
  Object.keys(state).forEach(k=>state[k]=null);
  document.querySelectorAll('.opt-card').forEach(c=>c.classList.remove('selected'));
  document.querySelectorAll('.btn-next').forEach(b=>b.disabled=true);
  document.querySelectorAll('.axis-section,.config-section').forEach(s=>s.classList.remove('active'));
  document.getElementById('step-0').classList.add('active');
  updateProgress(0);
}
(function(){
  const cv=document.getElementById('mini-particles'); if(!cv) return;
  const ctx=cv.getContext('2d');
  const pts=[];
  for(let i=0;i<18;i++) pts.push({x:Math.random()*200,y:Math.random()*60,vx:(Math.random()-.5)*.4,vy:(Math.random()-.5)*.4,r:.5+Math.random(),o:.1+Math.random()*.2});
  function draw(){
    ctx.clearRect(0,0,200,60);
    pts.forEach(p=>{
      p.vx*=.98; p.vy*=.98; p.x+=p.vx; p.y+=p.vy;
      if(p.x<0||p.x>200)p.vx*=-1; if(p.y<0||p.y>60)p.vy*=-1;
      ctx.beginPath(); ctx.arc(p.x,p.y,p.r,0,Math.PI*2);
      ctx.fillStyle=`rgba(106,154,213,${p.o})`; ctx.fill();
    });
    requestAnimationFrame(draw);
  }
  draw();
})();
</script>
</body>
</html>
```
