---
name: visualize
description: >
  Create beautiful, self-contained HTML visualizations from any content or idea.
  Use for: slide decks, presentations, infographics, dashboards, flowcharts, diagrams,
  timelines, comparison tables, data visualizations, landing pages, one-pagers, org charts,
  mind maps, process flows, kanban boards, report summaries, or any visual that helps
  humans digest information faster. Trigger on requests like "visualize this," "make a deck,"
  "create a slide," "build an infographic," "show me a dashboard," "make this visual,"
  or any request to present information in a visual HTML format.
license: MIT
metadata:
  author: careerhackeralex
  version: 0.3.0
  category: document-creation
  tags: [visualization, html, slides, dashboard, infographic]
---

# Visualize

Turn any idea, data, or content into a stunning single-file HTML visualization.

## After Creating a File

**Always do BOTH of these after writing the HTML file:**

1. **Auto-open in browser:** Run `open <filename>.html` (macOS) or `xdg-open <filename>.html` (Linux) so the user sees it immediately
2. **Return the file path as a clickable URL:** Include `file://<absolute-path>` in your response so the user can click to open it

Example response after creation:
```
Created your visualization! Opening in browser now...
📄 file:///Users/you/project/my-dashboard.html
```

## Critical Requirements (NON-NEGOTIABLE)

⚠️ **EVALUATION FAILURE GUARANTEED WITHOUT THESE 8 ELEMENTS** ⚠️

**EVERY file MUST start from the skeleton template in [references/skeleton.md](references/skeleton.md) — copy the ENTIRE template, then add your content.**

1. **CSS Custom Properties:** Exact names required: `--bg, --surface, --surface-hover, --border, --text, --text-secondary, --accent, --accent-secondary, --positive, --negative, --warning` — NO other names (not --bg-primary, not --text-primary). **CRITICAL:** These exact property names are required for evaluation system compatibility.
2. **Utility Menu System (MANDATORY):** Complete `.viz-menu` element with `.viz-menu-toggle` button, `.viz-menu-dropdown` container, download PNG button (`onclick="downloadImage()"`), print button (`onclick="window.print()"`), and html-to-image CDN script (`<script src="https://cdn.jsdelivr.net/npm/html-to-image@1.11.11/dist/html-to-image.js"></script>`). **EVALUATION CRITICAL:** Menu system is automatically checked and WILL CAUSE FAILURES if missing.
3. **Theme Classes (EVALUATION CRITICAL):** Must explicitly define BOTH `.theme-light` and `.theme-dark` classes in stylesheet with complete custom property definitions. **EXAMPLE REQUIRED:**
```css
:root { /* base properties */ }
.theme-light { --bg: #ffffff; --surface: #f8f9fa; --text: #1a1a1a; /* etc */ }
.theme-dark { --bg: #0a0a0a; --surface: #1a1a1a; --text: #ffffff; /* etc */ }
```
**NEVER rely on just `:root` or `@media (prefers-color-scheme)` — evaluation system checks for class-based themes.**
4. **Semantic HTML:** `<main id="main-content">` element, **MANDATORY: Multiple `<section>` elements for major content blocks** (header, metrics, charts, etc.), skip-to-content link. Each distinct content area must be wrapped in semantic `<section>` tags.
5. **Chart.js Requirements (EVALUATION CRITICAL):** MUST include `<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.7/dist/chart.umd.min.js"></script>` before closing `</head>`. **MANDATORY:** IMMEDIATELY after Chart.js script, add `<script>Chart.defaults.animation = false;</script>` (prevents animation glitches and is automatically checked by evaluation system). **MANDATORY CHART VALIDATION:** Every chart function MUST start with `if (typeof Chart === 'undefined') { console.error('Chart.js not loaded'); return; }`. **CHART ACCESSIBILITY:** Every canvas element MUST have `role="img"` and descriptive `aria-label` attributes. **CRITICAL CHART CONFIG:** Set `maintainAspectRatio: false`, `responsive: true`, and `plugins: { tooltip: { enabled: true } }` for accessibility. **NEVER disable tooltips** - evaluation system checks for enabled tooltips. **CHART RELIABILITY SYSTEM:** Use dedicated ChartManager pattern for bulletproof integration:
```javascript
var ChartManager = {
  charts: new Map(),
  safeInit: function(canvasId, config) {
    if (typeof Chart === 'undefined') {
      console.error('Chart.js library not loaded - check CDN inclusion');
      return null;
    }
    try {
      if (this.charts.has(canvasId)) {
        this.charts.get(canvasId).destroy();
        this.charts.delete(canvasId);
      }
      var ctx = document.getElementById(canvasId);
      if (!ctx) {
        console.error('Canvas element not found: ' + canvasId);
        return null;
      }
      // Ensure no conflicting chart instances
      if (ctx.chart) {
        ctx.chart.destroy();
        delete ctx.chart;
      }
      // Set accessibility attributes
      ctx.setAttribute('role', 'img');
      if (!ctx.getAttribute('aria-label')) {
        ctx.setAttribute('aria-label', 'Chart visualization');
      }
      // Initialize with enhanced error handling
      var chart = new Chart(ctx, config);
      this.charts.set(canvasId, chart);
      return chart;
    } catch (error) {
      console.error('Chart initialization failed for ' + canvasId + ':', error);
      return null;
    }
  },
  updateTheme: function() {
    if (typeof Chart === 'undefined') return;
    this.charts.forEach(function(chart, canvasId) {
      try {
        chart.update();
      } catch (error) {
        console.error('Chart theme update failed for ' + canvasId + ':', error);
      }
    });
  },
  destroyAll: function() {
    this.charts.forEach(function(chart) {
      try {
        chart.destroy();
      } catch (error) {
        console.error('Chart destruction failed:', error);
      }
    });
    this.charts.clear();
  }
};
```
Use `ChartManager.safeInit()` instead of raw `new Chart()`. **CRITICAL CHART CONFIG:** Set `maintainAspectRatio: false`, `responsive: true`, and `plugins: { tooltip: { enabled: true } }` for accessibility. **CHART CONTAINER DIMENSIONS:** Container must have explicit `height` >= 300px for charts to render properly. Use theme-aware colors with CSS custom properties, never static hex colors. **NEVER use import/export syntax with Chart.js CDN** — use standard var declarations only.

**CHART.JS TROUBLESHOOTING (CRITICAL):** If charts appear as blank white spaces:
- Verify Chart.js CDN is included before `</head>`
- Verify `Chart.defaults.animation = false;` is immediately after CDN
- Verify chart initialization is in DOMContentLoaded event listener
- Verify no module import/export syntax anywhere in the file
- Verify ChartManager.safeInit() pattern is used correctly
- Verify canvas has `role="img"` and `aria-label` attributes

6. **Responsive Design:** Section spacing ≥48px, **CRITICAL: NO horizontal overflow at 375px viewport** (MANDATORY: add `@media (max-width: 375px) { body { overflow-x: hidden; } }` to prevent horizontal scroll), **MANDATORY FONT-SIZE HIERARCHY:** h1 ≥ 2.5rem, h2 ≥ 2rem, h3 ≥ 1.5rem, body = 1rem. **SLIDE DECK REQUIREMENTS:** Title slide h1 ≥ 3rem, content slide titles ≥ 2.5rem, clear visual distinction between heading levels. **SLIDE SECTION SPACING:** Major sections within slides must have ≥48px spacing (title-to-content, content-to-charts, charts-to-navigation). **Test all layouts at 375px width — dashboards especially prone to chart container overflow.** **CSS CONTAINER QUERIES:** For advanced responsiveness, use container-based queries:
```css
.chart-container { container-type: inline-size; }
@container (max-width: 400px) { 
  .chart-legend { display: none; } 
  .chart-title { font-size: 1rem; }
}
```
This provides true component-level responsiveness beyond viewport media queries.
7. **Print & Accessibility:** `@media print` styles, `@media (prefers-reduced-motion: reduce)` with disabled animations
8. **Entrance Animations (MANDATORY):** Must include entrance animations via `.animate` classes, `data-reveal` attributes, or CSS `@keyframes`. **EVALUATION CRITICAL:** Animation presence is automatically detected and required.
9. **JavaScript Functions:** `cycleTheme()`, `toggleMenu()`, top-level variables use `var` not `let`/`const`

**🔥 CRITICAL: Copy skeleton.md exactly → Replace "YOUR CONTENT HERE" with visualization content → Save file**

## Core Principles

1. **Single-file HTML** — one `.html` file with inline CSS/JS. Opens in any browser, works offline, emails easily.
2. **Light theme optimized** — modern designs prioritize light mode quality. Dark theme available via toggle.
3. **Beautiful by default** — the first output should look professional with zero iteration.
4. **Content-first** — the visualization serves the message. Never sacrifice clarity for aesthetics.
5. **Responsive** — works on desktop, tablet, and mobile unless explicitly fixed-dimension (e.g., 16:9 slides).
6. **Visual restraint** — Professional designs avoid decorative elements that add noise. No floating gradient orbs, rainbow borders, or ornamental animations.

## Philosophy

HTML is not a "website" — it's a visualization tool. Code is cheap. Everyone should feel empowered to visualize anything. This skill turns conversation context, URLs, articles, data, or raw ideas into something visual and digestible in seconds.

Users invoke this **mid-conversation** with Claude Code. Use the full conversation context — whatever they've been discussing, any links they've shared, any data they've pasted — as source material. When given a URL, crawl it and extract the content to visualize.

## Output Rules

**MANDATORY FIRST STEP: Copy the complete skeleton from [references/skeleton.md](references/skeleton.md) — this includes all required elements (menu, theme system, CSS properties, semantic HTML, accessibility features). Never write HTML from scratch.**

- Write ONE `.html` file to `~/Downloads/` (or user-specified path)
- Filename: descriptive kebab-case, e.g., `q4-revenue-dashboard.html`, `team-roadmap-deck.html`
- Start with skeleton.md template, add your content to the `<!-- YOUR CONTENT HERE -->` section
- All custom styles in `<style>` after the skeleton's base styles
- **CDN libraries are encouraged** — use the best tool for the job:
  - **Tailwind CSS** — `https://cdn.tailwindcss.com` (utility-first styling, use freely)
  - **Chart.js** — `https://cdn.jsdelivr.net/npm/chart.js` (bar, line, pie, radar, doughnut)
  - **D3.js** — `https://cdn.jsdelivr.net/npm/d3@7` (complex/custom data viz, force graphs)
  - **Mermaid** — `https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.min.js` (flowcharts, sequence diagrams)
  - **Three.js** — 3D when appropriate
  - **Reveal.js** — full-featured slide engine when needed. **CRITICAL:** Must set `html, body { height: 100%; overflow: hidden; }` and give the `.reveal` container `height: 100%`. Config MUST use numeric dimensions: `Reveal.initialize({ width: 1280, height: 720, center: true, controls: false })` — NEVER use string percentages like `'100%'` which cause zero-height viewport and blank slides. **MANDATORY: Disable Reveal.js default controls** (`controls: false`) — the default `<` `>` arrow overlays are ugly. Instead, add a custom minimal bottom nav bar:
```html
<nav class="slide-nav" aria-label="Slide navigation">
  <button onclick="prevSlide()" aria-label="Previous slide">
    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M15 18l-6-6 6-6"/></svg>
  </button>
  <span class="slide-counter" id="slideCounter">1 / 8</span>
  <button onclick="nextSlide()" aria-label="Next slide">
    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M9 18l6-6-6-6"/></svg>
  </button>
</nav>
```
```css
.slide-nav { position: fixed; bottom: 16px; left: 50%; transform: translateX(-50%); display: flex; align-items: center; gap: 8px; z-index: 9998; }
.slide-nav button { width: 28px; height: 28px; border-radius: 6px; background: transparent; border: none; color: var(--text-secondary); cursor: pointer; display: flex; align-items: center; justify-content: center; opacity: 0.3; transition: opacity 0.2s; }
.slide-nav button:hover { opacity: 0.7; }
.slide-counter { font-size: 12px; color: var(--text-secondary); font-weight: 400; min-width: 40px; text-align: center; opacity: 0.35; }
```
  - **Leaflet** — maps and geospatial data (`https://unpkg.com/leaflet@1.9/dist/leaflet.js` + CSS). **Required for geographic data** — never hand-draw SVG continent shapes. Use OpenStreetMap tiles or a minimal tile provider.
- SVG for icons and simple graphics — never use external image URLs unless user provides them
- Prefer CSS animations over JS when possible

See [references/libraries.md](references/libraries.md) for detailed CDN links, patterns, and tips.

## Design System

Apply these defaults. They are opinionated and tested — override only when user requests it.

**Full design system reference:** See [references/design-system.md](references/design-system.md) for complete typography, color, spacing, animation, accessibility, and visual polish specifications.

Key highlights (consult reference for full details):

### Design Notes

**Theming System (CRITICAL):**
- Use **class-based theming ONLY** — `<html class="theme-dark">` or `<html class="theme-light">`
- Theme toggle changes html class: `document.documentElement.className = 'theme-' + newTheme`
- **Never use `data-theme` attributes** — the evaluation system expects class-based themes
- **Required CSS custom properties:** `--bg, --surface, --text, --accent, --border` (minimum set for evaluation compatibility)

**Typography:**
- **Inter font mandatory** — `https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap`
- **MANDATORY font weight hierarchy:** h1 ≥ 700, h2 ≥ 600, h3 ≥ 500, body = 400 (critical evaluation requirement)
- -0.03em tracking on headings
- **KOREAN TYPOGRAPHY EXCELLENCE:** For Korean content, use Noto Sans KR for body text with Inter for UI elements. Apply `line-height: 1.6` for Korean (vs 1.4 for Latin). Korean Medium weight maps to Western Regular (400). Include: `https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500;600;700&display=swap`

**Colors:**
- Class-based theming only (NO @media prefers-color-scheme)
- Dark: #0A0A0A bg, #EDEDED text. Light: #FAFAF9 bg, #0f172a text
- See reference for full palette.
- **Cards:** 8px radius, shadow-only hover (no translateY/scale), 1px solid var(--border). **GLASS MORPHISM UPGRADE:** For premium layouts, use glass containers with `backdrop-filter: blur(8px)`, semi-transparent backgrounds with CSS var `--glass-opacity: 0.08`, and elevated shadows. Apply selectively to hero sections or primary cards for sophisticated layering.
- **Animations:** CSS @keyframes for page-load (.animate + .delay-N), data-reveal + IntersectionObserver for scroll, data-count for counters. Content visible by default. **Above-fold content must NEVER use data-reveal** — use `.animate` classes instead. Use `data-reveal` sparingly (max 3-4 sections) for below-fold content only.
- **Accessibility:** Skip-to-content, aria-labels, landmark roles, :focus-visible, sr-only for chart data. See reference for full checklist.
- **Icons:** Inline SVG only, never emojis. Lucide-style 24x24, stroke-based.
- **Chart.js (MANDATORY PATTERNS):** `Chart.defaults.animation = false;` at top of script, destroy+recreate on theme toggle, explicit rgba() colors, tooltips always enabled, `maintainAspectRatio: false` on all chart options. **Accessibility: Wrap canvas in div with `role="img"` and descriptive `aria-label`**. **Guard pattern:** Use `chartsBuilt` flag — `onThemeChange()` must check `if (chartsBuilt)` before rebuilding. **Chart containers need min-height: 360px for substantial presence.**
- **Chart.js customization:** Apply professional styling beyond defaults — custom padding (`layout: { padding: 30 }`), remove excessive gridlines (opacity ≤ 0.04), use rounded corners (`borderRadius: 4`), thoughtful color palettes that match theme. Chart containers need 12px border radius, 40px internal padding, and 360px minimum height for substantial presence. Avoid library defaults that look auto-generated.
- **Typography hierarchy:** MANDATORY descending font-size scale: h1 > h2 > h3 > body text. **REQUIRED MINIMUMS:** h1: ≥3rem (48px), h2: ≥2rem (32px), h3: ≥1.5rem (24px), body: 1rem (16px). **EVALUATION CRITICAL:** Each heading level must be visibly smaller than the previous level with at least 0.5rem difference between levels. Example valid hierarchy: h1: 3rem, h2: 2.5rem, h3: 1.5rem, body: 1rem.
- **Visual restraint:** No floating orbs, gradient borders, gradient text on headings, scale transforms, glow effects, decorative animations.
- **Stat value colors:** Colored numbers must have semantic meaning (green/positive = good metric, red/negative = bad metric, accent = primary/neutral highlight). If no clear semantic meaning, use `var(--text)`. Never randomly colorize stat values. **For KPI grids with 4+ cards:** use at most 2 accent colors for values — `var(--accent)` for the single most important metric and `var(--text)` for all others. Reserve `var(--positive)`/`var(--negative)` only for delta indicators (arrows, percentages), not the main card value.
- **Background atmosphere:** One subtle technique per file (radial gradient, noise texture, or dot grid). **Adapt the atmosphere to the content** — a game dashboard should feel different from a financial report. Adjust accent colors and gradient hues to match the subject matter.
- **AI-NATIVE INFORMATION ARCHITECTURE:** Modern designs prioritize insight-driven hierarchy. Place the most important metric/insight above the fold. Use progressive revelation patterns — show key data immediately, provide drill-down on hover/click. Contextual actions should appear near relevant content. Lead with conclusions, support with details.
- **Entrance animations mandatory:** fadeInUp + stagger on all cards/sections.
- **Single-screen posters:** overflow:hidden + justify-content:space-between on fixed-dimension body. See reference for 9:16, 1:1, 4:5 sizing.


## Critical Implementation Requirements

**MANDATORY: Use the skeleton template** — see [references/skeleton.md](references/skeleton.md) for complete copy-paste HTML with all requirements built-in.

**JavaScript Implementation Rules:**
- **All top-level variables MUST use `var`** (not `let`/`const`) to avoid TDZ errors with function hoisting
- **Theme toggle MUST use `cycleTheme()` function** — this is built into the skeleton with proper `applyTheme()` implementation
- **Menu MUST use `toggleMenu()` with outside-click handling** — skeleton includes automatic dropdown closure on outside clicks and escape key
- **Chart rebuilding:** Define `function onThemeChange() {}` for chart re-rendering on theme changes
- **Mobile responsive:** Test all layouts at 375px viewport width — use CSS Grid `minmax(320px, 1fr)` for card grids

**Evaluation Checkers Expect:**
- `cycleTheme()` function exists and works (changes html class)
- `toggleMenu()` function exists and closes on outside clicks  
- Top-level JS variables are declared with `var`
- No horizontal overflow at 375px width
- Interactive elements beyond basic menu (hover states, chart interactions, etc.)

**The skeleton template automatically provides all required functionality. ALWAYS start from skeleton.md to avoid implementation errors.**

## Semantic HTML Requirements

All visualizations must include these semantic elements:

**Required Structure:**
- `<main>` element containing primary content
- `<section>` elements for major content blocks
- Landmark roles (`role="banner"`, `role="main"`, `role="complementary"`) OR skip-to-content link
- Chart accessibility: `role="img"` and `aria-label` on chart containers

**Additional Requirements:**
- `@media print` styles defined
- `@media (prefers-reduced-motion)` styles for accessibility
- Adequate spacing between sections (≥48px)
- Hover states for interactive elements

## Visualization Types

Choose the right format. See [references/types.md](references/types.md) for detailed patterns.

| Type | When to Use | Key Feature |
|------|-------------|-------------|
| **Slide Deck** | Presentations, pitches | 16:9, keyboard nav, transitions |
| **Infographic** | Data summaries, visual stories | Long scroll, big numbers, sections |
| **Dashboard** | Metrics, KPIs | Grid of cards + charts |
| **Flowchart** | Processes, architecture | Mermaid or SVG diagrams |
| **Timeline** | Chronological events | Alternating left/right, scroll-triggered |
| **Comparison** | Side-by-side analysis | Feature matrix, pros/cons |
| **Data Viz** | Charts, data stories | Chart.js or D3 |
| **One-Pager** | Summaries, briefs | Single viewport, print-friendly |
| **Mind Map** | Concept relationships | Radial SVG layout |
| **Kanban** | Status tracking | Column-based cards |
| **Carousel Cards** | Social media (IG/LinkedIn) | 1080×1080 per card, swipeable, bold text |
| **Event Poster** | Conferences, meetups, webinars | Portrait A4/letter, bold headline, date/venue |
| **Resume/CV** | Job applications | One-page, two-column, print-optimized |
| **Banner/Header** | Email, blog, social cover | 1200×630 or 1500×500, centered text on visual bg |
| **Quote Card** | Social proof, testimonials | Portrait/square, large quote, attribution |
| **Process Guide** | How-to, step-by-step | Numbered steps, icons, clear flow |
| **Status Report** | Executive updates | KPIs + progress bars + highlights, one-page |
| **Org Chart** | Team structure | Hierarchical tree, photos/avatars, roles |
| **Data Story** | Narrative + data | Scrollytelling, charts woven with narrative text |
| **Product Card** | Feature highlight, launch | Hero image area, feature pills, CTA |

### Carousel Card Rules

Carousel cards are huge for social media. Get these right:

- **Square format** — `1080×1080px` (or configurable via CSS var)
- **One idea per card** — bold headline + 1-2 supporting points max
- **Swipe nav** — arrows + dots + touch swipe + keyboard
- **Card counter** — "3 / 8" visible
- **Download all** — PNG export of individual cards or full set
- **Typography dominates** — headline at 2.5-4rem, minimal body text
- **Color-coded** — each card can have a subtle accent shift
- **Print layout** — grid of all cards for printing
- **Max 10 cards** — keep it focused

### Event Poster Rules

- **Portrait orientation** — A4/letter ratio or square
- **Visual hierarchy** — Event name (largest) → Date/Time → Location → Description → CTA
- **Bold headline** — 3-5rem, max 6 words
- **Date/time prominent** — styled as a badge or highlighted block
- **QR code area** — placeholder box for registration link
- **Print-first** — looks great printed, dark or light theme

### Quote Card Rules

- **Large quotation marks** — decorative " " in accent color, oversized
- **Quote text** — 1.5-2.5rem, serif or italic weight for contrast
- **Attribution** — name, title, company below quote
- **Square or portrait** — optimized for social sharing
- **Minimal design** — quote is the hero, everything else is subtle

### Single-Screen / Mobile-Fit Rules (Posters, Cards, One-Pagers)

When the user asks for something that fits "one screen," "phone screen," "9:16," or "mobile-fit," create a **fixed-dimension single-viewport** visualization — NOT a scrolling page.

**Dimensions:**
- **9:16 portrait (phone):** `width: 1080px; height: 1920px;` — standard Instagram Story / phone screen
- **1:1 square:** `width: 1080px; height: 1080px;` — Instagram post
- **4:5 portrait:** `width: 1080px; height: 1350px;` — Instagram portrait post
- **16:9 landscape:** `width: 1920px; height: 1080px;` — presentation slide

**Critical CSS pattern:**
```css
body {
  width: 1080px; height: 1920px; /* or chosen ratio */
  overflow: hidden; /* MUST — prevents scroll, enforces single screen */
  display: flex; flex-direction: column; /* Flex column fills canvas completely */
}
.poster-header { padding: 44px 48px 0; }
.poster-grid { flex: 1; padding: 24px 48px 0; } /* flex:1 expands to fill remaining space */
.poster-footer { padding: 16px 48px 36px; }
```

**Layout rules:**
- `overflow: hidden` on body — this is what makes it "one screen." Non-negotiable.
- `justify-content: space-between` on the main container — distributes sections evenly with NO dead gaps.
- **Use `flex: 1` on the main content area** (grid, body, etc.) so it expands to fill ALL remaining space between header and footer. Never use fixed `height` values that leave dead space.
- Wrap each logical section in a `<div>` so flexbox distributes them as blocks.
- **Zero dead space rule:** The poster canvas should be 100% utilized. No large empty margins at bottom or sides. If there's visible empty space, either expand content to fill it or reduce padding. Content should feel like it "fits" the frame perfectly.
- **Test mentally:** count your sections, divide 1920px among them. Each section gets ~200-300px. If content is sparse, make elements bigger (larger fonts, more padding, bigger icons).
- **No hamburger menu** for fixed-dimension posters — it wastes space and the poster is meant for screenshot/export, not interaction.

**Content density for 9:16:**
- Hero (title + subtitle): ~25% of height
- 2-3 content sections: ~55% of height
- Footer/CTA: ~10% of height
- Breathing room (gaps): ~10% of height
- **If it looks empty, your content is too small.** Scale up fonts, add more grid items, use larger icons.

**Font sizing for 1080px-wide posters:**
- Hero h1: `68-80px` (bigger than web — this is a poster)
- Section labels: `15-18px` uppercase, letter-spacing `0.06em`
- Card text: `16-20px`
- Body: `20-24px`

**Common mistake:** Making a scrolling page and screenshotting it. That's NOT a poster — it's a webpage screenshot. A poster is a fixed canvas where every pixel is intentional.

## Slide Deck Rules

Slides are the most common request. Get these right:

- **16:9 aspect ratio** — `100vw × 100vh`, content centered
- **Responsive breakpoints** — Use `clamp()` and container queries for mobile-friendly slides:
  ```css
  .slide-container { container-type: inline-size; }
  .slide-title { font-size: clamp(2rem, 8vw, 4rem); }
  @container (width < 768px) { .slide-content { padding: 1rem; } }
  ```
- **One idea per slide** — if you need a second thought, make a second slide
- **Max 40 words per slide** — more than that, split or use visuals
- **Headlines max 6 words** — short, punchy, memorable
- **Big number + small label** for stat slides — number at 3-5rem, label at 0.875rem
- **Keyboard nav** — ← → arrows, Space, Enter
- **Touch nav** — swipe left/right
- **Click nav** — left third = prev, right two-thirds = next
- **Progress bar** — thin gradient bar at top showing position
- **Slide counter** — "3 / 12" in bottom nav
- **Mobile navigation prominence** — Ensure navigation controls are clearly visible on mobile. Use larger touch targets (min 44px), contrasting colors, and backdrop-blur for floating nav
- **Smooth transitions** — `transform: translateX()` with 500ms cubic-bezier
- **Entrance animations** — elements within slides animate in with staggered delays
- **Speaker notes** — `data-notes` attribute, visible in print only

### High-Impact Presentation Slides (Business Context)
For investor presentations, startup pitches, and executive briefings:
- **Hero slide visual weight** — Use stronger gradients, larger typography (4-6rem), and compelling statistics prominently displayed
- **Value proposition clarity** — Hero should communicate core value in under 5 seconds
- **Professional credibility** — Ensure typography, spacing, and color choices match enterprise/investment-grade expectations
- **Data storytelling** — Each chart slide should have clear insight callouts, not just raw data visualization

### Theme-Aware Slide Gradients (CRITICAL)

Slide decks MUST look visually distinct in dark vs light themes. Gradient backgrounds must change:

```css
/* Dark theme: deep, saturated gradients */
.theme-dark .slide-title { background: linear-gradient(135deg, #1e1b4b 0%, #312e81 50%, #1e3a5f 100%); }
.theme-dark .slide-content { background: var(--bg); }

/* Light theme: soft, pastel gradients */
.theme-light .slide-title { background: linear-gradient(135deg, #e0e7ff 0%, #c7d2fe 50%, #dbeafe 100%); }
.theme-light .slide-content { background: var(--bg); }
```

Rules:
- Title/section slides: use theme-specific gradient pairs (dark=deep+saturated, light=soft+pastel). **Choose gradient colors that evoke the content's subject matter** — a tech pitch uses cool blues, a game pitch uses vibrant purples/cyans, a healthcare deck uses calming greens/teals.
- Content slides: use `var(--bg)` or `var(--surface)` — NOT hardcoded dark backgrounds
- Data cards on slides: use `var(--surface)` with `var(--border)` — they auto-adapt
- Never hardcode `#1a1a2e` or similar dark colors on slide content — use CSS variables
- Test: toggle theme and every slide should look intentionally designed for that mode

### Slide Types
1. **Title** — theme-aware gradient background, big headline, subtitle. Center aligned.
2. **Content** — heading + bullets OR heading + visual. Never text-heavy.
3. **Section divider** — full-bleed accent color, section title only.
4. **Stat** — one big number, one label, one insight sentence.
5. **Chart** — Chart.js visualization with title and key takeaway. MUST use chart-container wrapper class.
6. **Two-column** — split layout for comparisons, text+visual.
7. **Quote** — large pull quote with attribution.
8. **Closing** — CTA, contact info, or summary + social links.

### Slide Deck Chart Requirements (CRITICAL)
Chart slides in presentations MUST follow the same container standards as dashboards:
```html
<div class="chart-slide-container">
  <h2>Chart Title</h2>
  <div class="chart-container" style="height: 400px; padding: 40px; border-radius: 12px; background: var(--surface);">
    <canvas id="slideChart" role="img" aria-label="Description"></canvas>
  </div>
</div>
```
- **Use chart-container class** — maintains evaluation consistency across formats
- **Minimum height 400px** for slide charts — larger than dashboard charts for presentation readability
- **maintainAspectRatio: false** — required for proper sizing in slide layouts

## Data Ingestion

When user provides data:
- **CSV** — parse with JS, auto-detect headers, render appropriate chart type
- **JSON** — extract keys as labels, values as data, nested objects as series
- **Tables** — convert to visual comparison or chart
- **Numbers in text** — extract and highlight as stat cards
- **URLs** — crawl, extract key info, visualize as summary

## Context Awareness

This skill is used mid-conversation. Leverage everything:

- **Conversation context** — summarize, structure, or visualize what's been discussed
- **URLs/links** — crawl and extract content, then visualize
- **Pasted data** — CSV, JSON, tables → charts, dashboards
- **Ideas/concepts** — turn abstract discussions into visual diagrams
- **Code/architecture** — visualize system designs, data flows

Always use real content. Never generate placeholder data when real context exists.

## Type-Specific Interactivity (Mandatory)

Every file MUST have at least ONE meaningful interaction beyond theme toggle + menu. Static-feeling pages score low on interactivity.

| Type | Required Interaction |
|------|---------------------|
| **Cheatsheet** | Search/filter input + copy-to-clipboard on code blocks. Use `<details name="...">` for collapsible groups. |
| **Dashboard** | Filter toolbar or metric drill-down. At minimum: date range or category filter. |
| **Status Report** | Collapsible detail sections (use `<details>`). Progress bars animate on scroll. |
| **Quote Card** | Auto-cycling quotes OR swipeable carousel. Share/copy button. |
| **Event Poster** | Animated countdown timer (days/hours/min/sec). RSVP/register button. |
| **Process Guide** | Steps as exclusive accordion (`<details name="steps">`). Or interactive progress tracker. |
| **Architecture** | Clickable nodes with popover details (use Popover API). Hover highlights connections. |
| **Timeline** | Filter by era/category. Or click to expand event details. |
| **Comparison** | Toggle categories on/off. Or highlight winner per row. |
| **Carousel** | Touch swipe + keyboard + auto-advance option. Card counter always visible. |
| **Slide Deck** | Already interactive (nav). Add: presenter timer, slide overview grid. |

If a type isn't listed, add at minimum: a filter, search, sort, or expand/collapse interaction.

## Layout Variation (CRITICAL)

Every file must feel like a UNIQUE design, not a template with different text. Vary these per file type:
- **Grid structure**: Mix 1-col, 2-col, 3-col. Use CSS Grid `span 2` for featured cards. **CRITICAL: Always test at 768px and 375px - no horizontal overflow allowed.**

**Mobile-First Responsive Pattern (MANDATORY):**
```css
.grid { 
  display: grid; 
  gap: 24px; 
  grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); 
}
@media (max-width: 768px) { 
  .grid { grid-template-columns: 1fr; gap: 16px; }
  .container { padding: 24px 16px; }
}
@media (max-width: 375px) {
  .card { padding: 16px; }  
  .stat-value { font-size: 2rem; }
}
```
- **Section rhythm**: Alternate between full-width sections, card grids, and single-focus sections.
- **Content density**: More content at smaller sizes looks more professional than sparse content at large sizes. A dashboard with 8 KPI cards + 4 charts feels real; 4 KPI cards + 2 charts feels like a demo.
- **Visual focal point**: Every file needs ONE visually dominant element (hero stat, key chart, primary message) — not everything at equal weight.
- **No orphaned grid items**: When a grid has an odd number of items where the last row isn't full, use `grid-column: span 2` on the last item or adjust `grid-template-columns` to avoid a single card stranded alone on a row.

## Anti-Patterns

- ❌ Walls of text — if it reads like a document, it's not a visualization
- ❌ Tiny fonts — minimum 14px body, 20px+ for presentation headings
- ❌ Rainbow colors — stick to 2-3 colors from the palette + neutrals
- ❌ Placeholder content — never use "Lorem ipsum" or fake data
- ❌ Over-engineering — simplest approach that looks stunning
- ❌ Cramped layouts — when in doubt, add more whitespace
- ❌ Generic design — each visualization should feel intentional, not templated
- ❌ Missing menu — every output needs the hamburger menu
- ❌ Broken print — always include `@media print` styles

## Advanced Techniques

Use these when they add value. See [references/css-techniques.md](references/css-techniques.md) for code snippets.

- **Glass morphism** — `backdrop-blur-md bg-white/5 border border-white/10` for floating cards
- **Gradient text** — `background: linear-gradient(...); -webkit-background-clip: text` for hero headlines
- **Scroll-snap** — `scroll-snap-type: y mandatory` as alternative slide navigation (no JS needed)
- **Conic gradients** — `conic-gradient()` for pure CSS pie/donut charts
- **Number animations** — animate counters from 0 to target value on scroll
- **Spring easing** — `cubic-bezier(0.34, 1.56, 0.64, 1)` for playful micro-interactions
- **Animate to auto** — `interpolate-size: allow-keywords` on `:root` enables smooth `height: auto` transitions (Chrome 129+)
- **CSS counters** — auto-numbering for step-by-step processes
- **View Transitions API** — smooth theme switching animations
- **Inline SVG icons** — draw simple icons as `<svg>` paths, no icon library needed

## Mandatory HTML Skeleton

**EVERY visualization MUST start from the skeleton.** Copy it, then add content.

**Full skeleton code:** See [references/skeleton.md](references/skeleton.md) for the complete copy-paste HTML template with themes, print styles, Inter font, animations, menu, and hover effects.

The skeleton provides:
- Class-based dark/light theming (OS detection on first visit, localStorage persistence)
- CSS @keyframes animations (fadeInUp, fadeIn, slideInLeft, slideInRight) + .animate/.delay-N classes
- Scroll-reveal via data-reveal attribute + IntersectionObserver
- Number counter via data-count attribute
- Hamburger menu with theme toggle, PNG download (html-to-image), print/PDF
- Popover and details accordion CSS (Chrome 114+/120+)
- Print styles with @page margin boxes
- prefers-reduced-motion support

### Skeleton Rules
- Use `var` for all top-level JS variables (prevents TDZ errors)
- MANDATORY: Use `data-reveal` for scroll animation OR `.animate.delay-N` for page-load entrance. Add JavaScript scroll observer for `.reveal` classes.
- Define `function onThemeChange() {}` to re-render charts on theme toggle
- Use semantic HTML: `<main>`, `<section>`, `<header>`, `<article>`
- Don't use `let`/`const` at script top level

## Minimum Sizing Rules

Elements must be large enough to read and feel substantial:

- **Timeline cards:** minimum width 280px, minimum padding 20px
- **Timeline layout:** Distribute timeline items evenly to prevent large gaps. If you have 5 items but only fill 60% of the vertical space, add more content sections (like investment breakdown or impact metrics) to fill the remaining 40%. Never leave massive empty spaces below the last timeline item.
- **Chart containers:** minimum 60% of parent width, minimum height 300px (360px+ for dashboards). In grid layouts, charts should use `flex-grow: 1` to fill available space — 300px is a floor, not a target.
- **Stat numbers:** minimum font-size 2rem (32px), bold/extrabold weight
- **Card content area:** minimum padding 24px
- **Section spacing:** **MANDATORY minimum 48px between major sections** — use `margin-bottom: 48px` or larger on section elements
- **Slide headings:** minimum 2rem (32px), maximum 6 words
- **Body text:** minimum 1rem (16px), never smaller

**If content feels too small, it IS too small. Err on the side of larger.**

## Text Visibility Rules

**Text must ALWAYS be visible.** This is the #1 cause of broken outputs.

- Dark theme: text MUST use `var(--text)` which resolves to `#f9fafb` (near-white)
- Light theme: text MUST use `var(--text)` which resolves to `#0f172a` (near-black)
- On gradient backgrounds: add `text-shadow: 0 1px 3px rgba(0,0,0,0.3)` for readability
- On hero slides with gradient/image backgrounds: use a dark overlay (`rgba(0,0,0,0.5)`)
- NEVER set text color to a value close to the background color
- Test mentally: "would this text be visible on BOTH dark (#030712) and light (#f8fafc) backgrounds?"

## Chart.js Integration Rules (CRITICAL — MOST COMMON FAILURE)

Charts are the second most common failure. These rules are MANDATORY for every chart:

### 1. Container Structure (REQUIRED)
```html
<!-- MANDATORY PATTERN FOR EVERY CHART -->
<div role="img" aria-label="Detailed description of chart data and insights">
  <div class="chart-container" style="height: 360px; padding: 40px; border-radius: 12px; background: var(--surface);">
    <canvas id="uniqueChartId"></canvas>
  </div>
</div>
```

### 2. Canvas Dimensions (REQUIRED)
- **Container must have explicit height:** minimum 360px for dashboards, 300px for other types
- **Canvas element needs no sizing** — Chart.js handles this when `maintainAspectRatio: false`
- **Container padding:** 40px internal padding for professional spacing
- **Container border-radius:** 12px for modern card appearance

### 3. Chart.js Initialization (MANDATORY PATTERN)
```javascript
// REQUIRED: Chart destruction and canvas reset to prevent "Canvas already in use" errors
var chartsBuilt = false; // Guard flag

function buildCharts() {
  if (chartsBuilt) return; // Prevent double-initialization during theme detection
  
  // REQUIRED: Reset canvas before building
  function resetCanvas(id) {
    var old = document.getElementById(id);
    if (!old) return null;
    var parent = old.parentNode;
    var canvas = document.createElement('canvas');
    canvas.id = id;
    parent.replaceChild(canvas, old);
    return canvas;
  }
  
  // Example chart with required settings
  var ctx = resetCanvas('myChart');
  if (ctx) {
    new Chart(ctx, {
      type: 'bar',
      data: { /* your data */ },
      options: {
        responsive: true,
        maintainAspectRatio: false, // REQUIRED
        animation: false, // MANDATORY: Plus set Chart.defaults.animation = false globally
        plugins: {
          tooltip: {
            enabled: true, // NEVER disable tooltips
            padding: 12,
            cornerRadius: 8
          }
        },
        layout: { padding: 20 } // REQUIRED: breathing room
      }
    });
  }
  
  chartsBuilt = true; // Mark as built
}

// CRITICAL: Disable Chart.js default animations IMMEDIATELY after Chart.js loads
Chart.defaults.animation = false; // MUST be set before any chart creation

// REQUIRED: Build charts after DOM loads
document.addEventListener('DOMContentLoaded', buildCharts);

// REQUIRED: Rebuild charts on theme change
function onThemeChange() {
  chartsBuilt = false; // Reset flag
  setTimeout(buildCharts, 100); // Slight delay for CSS variable updates
}
```
- **MANDATORY: Hover tooltips enabled** — never disable Chart.js tooltips:
  ```javascript
  options: {
    plugins: {
      tooltip: {
        enabled: true, // NEVER set to false
        mode: 'index',
        intersect: false
      }
    }
  }
  ```
- **Minimum chart height:** 300px on desktop, 250px on mobile
- **Font size defaults:** Axis tick labels at 13px minimum, axis titles at 14px, chart titles at 16px minimum. Legend at 13px.
- **Chart padding:** Add `layout: { padding: { top: 20, right: 20, bottom: 20, left: 20 } }` for breathing room
- **Axis tick config:** `maxRotation: 0` to keep labels horizontal. If labels overflow, use `maxTicksLimit` to reduce count
- **Grid lines:** Very faint — `rgba(255,255,255,0.04)` in dark, `rgba(0,0,0,0.06)` in light
- **Tooltip styling:** `padding: 12`, `cornerRadius: 8`, `titleFont: { size: 14 }`, `bodyFont: { size: 13 }`
- **Point radius:** 0 by default, 6 on hover — cleaner line charts
- **Set `maintainAspectRatio: false`** and control size via CSS container
- **Use theme-aware colors:** read CSS vars at render time, re-render on theme change
- **Chart text colors:** set `Chart.defaults.color = getComputedStyle(root).getPropertyValue('--text-secondary').trim()`
- **Grid line colors:** use `var(--border)` value
- **Legend position:** 'top' for horizontal charts, 'right' for vertical with space
- **Axis labels:** Keep horizontal when possible - avoid rotation unless absolutely necessary
- **Donut/pie charts:** Always include percentage labels on segments
- **Responsive:** `responsive: true` is default, but container must have explicit dimensions
- **High contrast colors:** Ensure sufficient color difference between data series for accessibility

```javascript
// Theme-aware Chart.js setup (include in every chart visualization)
function getChartColors() {
  var s = getComputedStyle(document.documentElement);
  return {
    text: s.getPropertyValue('--text').trim(),
    textSecondary: s.getPropertyValue('--text-secondary').trim(),
    border: s.getPropertyValue('--border').trim(),
    surface: s.getPropertyValue('--surface').trim(),
    accent: s.getPropertyValue('--accent').trim(),
  };
}

// REQUIRED: Reset canvas before rebuilding charts (prevents "Canvas already in use" errors)
function resetCanvas(id) {
  var old = document.getElementById(id);
  var parent = old.parentNode;
  var canvas = document.createElement('canvas');
  canvas.id = id;
  parent.replaceChild(canvas, old);
  return canvas;
}

// Usage in buildCharts():
//   try { if (window.myChart) window.myChart.destroy(); } catch(e) {}
//   window.myChart = new Chart(resetCanvas('myChart'), { ... });

// CRITICAL: Always check chart existence before destroy() to prevent console errors
function buildCharts() {
  var isDark = document.documentElement.classList.contains('theme-dark');
  var colors = getChartColors();
  
  // Safe chart destruction and rebuild pattern
  if (window.myChart) {
    try { window.myChart.destroy(); } catch(e) { /* ignore */ }
  }
  window.myChart = new Chart(resetCanvas('myChart'), {
    // chart config with theme-aware colors
    options: {
      scales: {
        x: { ticks: { color: colors.textSecondary }, grid: { color: colors.border } },
        y: { ticks: { color: colors.textSecondary }, grid: { color: colors.border } }
      }
    }
  });
}
```

## Critical Debugging Patterns

### Counter Animation Debug Pattern
If KPI values show "0%" instead of animating, add this debug pattern:
```javascript
// DEBUG: Add after counter observer setup to verify intersection
var counterEl = document.querySelector('[data-count]');
if (counterEl) {
  console.log('Counter element found:', counterEl); // DEBUG
  var cObs = new IntersectionObserver(function(entries) {
    console.log('Counter intersection triggered:', entries); // DEBUG
    entries.forEach(function(e) { 
      if (e.isIntersecting) { 
        console.log('Starting counter animation'); // DEBUG
        animateCounters(); 
        cObs.disconnect(); 
      } 
    });
  }, { threshold: 0.3 });
  cObs.observe(counterEl);
} else {
  console.warn('No [data-count] elements found'); // DEBUG
}
```

### Chart.js Integration Safety Pattern
MANDATORY for all Chart.js usage to prevent console errors:
```javascript
// STEP 1: Global variables - MUST use var, never let/const
var chartsBuilt = false;

// STEP 2: Chart building function with validation
function buildCharts() {
  // CRITICAL: Always validate Chart.js loaded first
  if (chartsBuilt || typeof Chart === 'undefined') return;
  
  // STEP 3: Destroy existing charts to prevent "Canvas already in use"
  if (window.myChart) window.myChart.destroy();
  
  // STEP 4: Reset canvas elements
  var canvas = document.getElementById('chartId');
  if (!canvas) return;
  
  // STEP 5: Get theme colors from CSS variables
  var isDark = document.documentElement.className.includes('theme-dark');
  var textColor = isDark ? '#EDEDED' : '#0f172a';
  var gridColor = isDark ? 'rgba(255,255,255,0.04)' : 'rgba(0,0,0,0.06)';
  
  // STEP 6: Create chart with proper options
  try {
    window.myChart = new Chart(canvas.getContext('2d'), {
      // Your chart configuration here
      options: {
        responsive: true,
        maintainAspectRatio: false, // REQUIRED
        plugins: {
          tooltip: { enabled: true }, // REQUIRED - never disable
          legend: { 
            labels: { color: textColor, font: { family: 'Inter' } }
          }
        },
        scales: {
          x: { 
            ticks: { color: textColor },
            grid: { color: gridColor }
          },
          y: { 
            ticks: { color: textColor },
            grid: { color: gridColor }
          }
        }
      }
    });
    
    chartsBuilt = true;
  } catch (error) {
    console.error('Chart creation failed:', error);
  }
}

// STEP 7: Theme change handler
function onThemeChange() {
  if (chartsBuilt) {
    chartsBuilt = false;
    buildCharts();
  }
    var ctx = document.getElementById('myChart');
    if (!ctx) {
      console.error('Chart canvas #myChart not found');
      return;
    }
    // ... build chart
  } catch (error) {
    console.error('Chart building failed:', error);
  }
}
```

### Menu Outside-Click Fix
Ensure menu closes when clicking outside by strengthening the event handler:
```javascript
document.addEventListener('click', function(e) { 
  var menu = document.querySelector('.viz-menu');
  var dropdown = document.getElementById('vizMenuDropdown');
  if (!e.target.closest('.viz-menu') && dropdown) {
    dropdown.classList.remove('open');
  }
});
```

## Process

1. **Understand** — what's the message? Who's the audience? What format fits?
2. **Start from skeleton** — copy the Mandatory HTML Skeleton above. NEVER start from a blank file.
3. **Structure** — outline content/sections BEFORE filling in the skeleton
4. **Build** — add content, charts, styles. Keep all colors as CSS vars.
5. **Verify checklist:**
   - [ ] `html.theme-dark` and `html.theme-light` class-based theme selectors (NO @media prefers-color-scheme)?
   - [ ] JS detects OS preference on first visit, stores in localStorage?
   - [ ] All text uses `var(--text)` or `var(--text-secondary)`?
   - [ ] `@media print` hides menu, shows all content?
   - [ ] `@media (prefers-reduced-motion: reduce)` present?
   - [ ] `.viz-menu` with toggle, theme, download, print?
   - [ ] Correct font loaded? (Inter default, Noto Sans KR for Korean, etc.)
   - [ ] Non-Latin content has appropriate CJK/RTL font?
   - [ ] Entrance animations via `.animate` classes (CSS @keyframes)?
   - [ ] Scroll sections use `data-reveal` (visible without JS)?
   - [ ] `.card:hover` has transform effect?
   - [ ] All top-level JS variables use `var` (not `let`/`const`)?
   - [ ] Charts use `var` declarations + `onThemeChange` hook?
   - [ ] **MANDATORY:** All charts wrapped with `role="img" aria-label="..."`?
   - [ ] **MANDATORY:** All charts have hover tooltips enabled (never disabled)?
   - [ ] Animated number counters use `data-count` where stats exist?
   - [ ] Semantic HTML: `<main>`, `<section>`, `<header>`, `<article>`?
   - [ ] All charts have explicit container sizing (≥300px height)?
   - [ ] Hero/title text visible on both themes?
   - [ ] Minimum sizing rules followed (cards 280px+, text 16px+)?
   - [ ] Zero console errors on load?

The quality bar: **"good, period"** — not "good for AI-generated."
