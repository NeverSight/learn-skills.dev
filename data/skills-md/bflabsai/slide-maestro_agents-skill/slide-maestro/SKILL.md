---
name: slide-maestro
description: "The definitive slide presentation skill. Fuses design intelligence, viewport-safe HTML engineering, data visualization, copywriting formulas, and 100+ style presets. Triggers on: slides, presentation, deck, pitch, keynote, talk, webinar, apresentação, criar apresentação, converter pptx."
tags: [design, slides, presentation, html, deck, pitch, data-visualization, chartjs, copywriting, animation, frontend]
related_skills: [claude-design, popular-web-designs, webdesign-pro-max, frontend-design, canvas-design]
---

# Slide Maestro

The definitive slide presentation skill. One workflow — from blank canvas to production-ready HTML deck.

Fuses: frontend-design (Claude native), frontend-slides (ECC), claude-design, webdesign-pro-max (100+ palettes, 57 font pairings), ckm:slides (Chart.js data viz + copywriting formulas).

## Design Thinking — Before You Code

Every great deck starts with a decision, not a template.

### 1. Purpose
What problem does this solve? Who watches it, in what context?

### 2. Tone — Pick an Extreme
- **Impressed/Confident**: Bold Signal, Electric Studio, Dark Botanical
- **Excited/Energized**: Creative Voltage, Neon Cyber, Split Pastel
- **Calm/Focused**: Notebook Tabs, Paper and Ink, Swiss Modern
- **Inspired/Moved**: Dark Botanical, Vintage Editorial, Pastel Geometry
- **Luxury/Refined**: Monochrome with gold accent, editorial serif
- **Brutalist/Raw**: High-contrast, oversized type, grid-breaking

### 3. Differentiation
What is the ONE thing someone will remember? Design toward that.

### 4. Content State
- Finished copy → go straight to design
- Rough notes → structure first, then style
- Topic only → outline → copy → design

---

## When to Use

- New presentation from topic/notes → Full workflow
- PPT/PPTX conversion → Extract with python-pptx → style → build HTML
- Existing HTML deck improvement → enhance layout/motion/typography/data
- Data-driven slides with charts → Chart.js integration
- Marketing/pitch deck → copywriting formulas + brand tokens
- Conference talk → large-screen readability + animation

---

## Workflow

### Step 1: Discover Content
Ask only what is needed:
- Purpose: pitch, teaching, conference, internal, marketing
- Length: short (5-10), medium (10-20), long (20+)
- Content state: finished copy, rough notes, topic only
- Brand constraints: colors, fonts, logos

### Step 2: Discover Style
If user knows preset → use it directly. Otherwise:
1. Ask what feeling the deck should create
2. Generate 3 single-slide preview files in `.slide-maestro-previews/`
3. Each preview: self-contained, shows typography/color/motion
4. Let user pick or mix elements

### Step 3: Structure the Narrative
Copywriting formulas:
- **PAS** (Problem → Agitation → Solution) for pain-point decks
- **AIDA** (Attention → Interest → Desire → Action) for pitch decks
- **SCQA** (Situation → Complication → Question → Answer) for strategic decks
- **Star → Chain → Hook** for narrative-driven decks

Slide position strategy:
- Opening (1-3): Hook with bold statement, question, or striking visual
- Middle: Alternate data, story, proof. Vary layout every 2-3 slides
- Closing: Strong CTA, memorable takeaway, contact/next steps

### Step 4: Build
Output: `presentation.html` or `[name].html`
Required: semantic sections, viewport-fit CSS base, CSS variables, navigation controller, Intersection Observer, reduced-motion support.

### Step 5: Enforce Viewport Fit (HARD GATE)
Every slide MUST fit in one viewport. No exceptions.
- `height: 100vh; height: 100dvh; overflow: hidden`
- All type/spacing scales with `clamp()`
- Content does not fit → split into more slides
- Never shrink text below readable sizes
- Never allow scrollbars inside a slide

### Step 6: Validate
Check at: 1920x1080, 1280x720, 768x1024, 375x667, 667x375

### Step 7: Deliver
- Delete temporary previews unless user wants them
- Summarize: file path, preset, slide count, customization points
- Open with: `xdg-open file.html` (Linux) / `open file.html` (macOS)

---

## MANDATORY Viewport-Fit CSS Base

Copy this into every presentation. Theme on top.

```css
html, body { height: 100%; overflow-x: hidden; margin: 0; padding: 0; }
html { scroll-snap-type: y mandatory; scroll-behavior: smooth; }

.slide {
    width: 100vw; height: 100vh; height: 100dvh;
    overflow: hidden; scroll-snap-align: start;
    display: flex; flex-direction: column; position: relative;
}

.slide-content {
    flex: 1; display: flex; flex-direction: column;
    justify-content: center; max-height: 100%;
    overflow: hidden; padding: var(--slide-padding);
}

:root {
    --title-size: clamp(1.5rem, 5vw, 4rem);
    --h2-size: clamp(1.25rem, 3.5vw, 2.5rem);
    --h3-size: clamp(1rem, 2.5vw, 1.75rem);
    --body-size: clamp(0.75rem, 1.5vw, 1.125rem);
    --small-size: clamp(0.65rem, 1vw, 0.875rem);
    --slide-padding: clamp(1rem, 4vw, 4rem);
    --content-gap: clamp(0.5rem, 2vw, 2rem);
    --element-gap: clamp(0.25rem, 1vw, 1rem);
}

.card, .container, .content-box { max-width: min(90vw, 1000px); max-height: min(80vh, 700px); }
.grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(min(100%, 250px), 1fr)); gap: clamp(0.5rem, 1.5vw, 1rem); }
img, .image-container { max-width: 100%; max-height: min(50vh, 400px); object-fit: contain; }

@media (max-height: 700px) { :root { --slide-padding: clamp(0.75rem, 3vw, 2rem); --content-gap: clamp(0.4rem, 1.5vw, 1rem); --title-size: clamp(1.25rem, 4.5vw, 2.5rem); } }
@media (max-height: 600px) { :root { --slide-padding: clamp(0.5rem, 2.5vw, 1.5rem); --title-size: clamp(1.1rem, 4vw, 2rem); --body-size: clamp(0.7rem, 1.2vw, 0.95rem); } .nav-dots, .keyboard-hint, .decorative { display: none; } }
@media (prefers-reduced-motion: reduce) { *, *::before, *::after { animation-duration: 0.01ms !important; transition-duration: 0.2s !important; } html { scroll-behavior: auto; } }
```

---

## Content Density Limits

- **Title**: 1 heading + 1 subtitle + optional tagline
- **Content**: 1 heading + 4-6 bullets or 2 paragraphs
- **Feature grid**: 6 cards max
- **Data/Chart**: 1 chart + title + 1-2 takeaways
- **Code**: 8-10 lines max
- **Quote**: 1 quote + attribution
- **Image**: 1 image constrained by viewport
- **Comparison**: 2 columns max, 3 items per column

---

## Typography Rules

- Choose fonts that are beautiful, unique, unexpected
- Pair distinctive display + refined body
- NEVER: Inter, Roboto, Arial, system-ui (unless intentionally editorial)
- Minimum 24px at 1920x1080
- Type as hierarchy before boxes/icons/color
- Max 2 font families, 3 weights

### Font Pairing Suggestions
- **Bold/Confident**: Archivo Black + Space Grotesk
- **Clean/Agency**: Manrope variable (single family, weight contrast)
- **Editorial/Serif**: Playfair Display + Source Serif Pro
- **Tech/Precise**: JetBrains Mono headings + DM Sans body
- **Luxury/Refined**: Cormorant Garamond + Montserrat Light
- **Playful**: Bricolage Grotesque + Plus Jakarta Sans

---

## Color System

- CSS custom properties for all colors
- Dominant colors + sharp accents beat timid even palettes
- Avoid: purple gradient on white, blue CTA on gray
- Prefer oklch for harmonious palettes
- Contrast: 4.5:1 body text, 3:1 large text (WCAG AA)
- Semantic tokens: `--bg`, `--surface`, `--ink`, `--muted`, `--accent`, `--danger`, `--success`

---

## Animation and Motion

- CSS-only by default; JS only for complex state
- One orchestrated page load with staggered reveals beats scattered micro-interactions
- Duration: 150-300ms micro, 400ms max transitions
- Use transform/opacity only — never animate width/height/top/left
- Easing: ease-out enter, ease-in exit
- Stagger items 30-50ms
- Exit 60-70% of enter duration
- Always respect prefers-reduced-motion

### Reveal Pattern
```js
const observer = new IntersectionObserver((entries) => {
    entries.forEach((entry, i) => {
        if (entry.isIntersecting) {
            entry.target.style.animationDelay = `${i * 80}ms`;
            entry.target.classList.add('revealed');
        }
    });
}, { threshold: 0.3 });
document.querySelectorAll('.slide [data-reveal]').forEach(el => observer.observe(el));
```

---

## Data Visualization (Chart.js)

Use Chart.js CDN for data slides.

### Chart Selection
- Trend over time → Line
- Comparison → Bar
- Proportion (≤5) → Donut
- Correlation → Scatter/Bubble
- Distribution → Histogram

### Template
```html
<script src="https://cdn.jsdelivr.net/npm/chart.js@4"></script>
<canvas id="chart1" style="max-height: 50vh;"></canvas>
<script>
new Chart(document.getElementById('chart1'), {
    type: 'bar',
    data: { labels: ['Q1','Q2','Q3','Q4'], datasets: [{ label: 'Revenue', data: [12,19,8,15], backgroundColor: 'var(--accent)', borderRadius: 6 }] },
    options: { responsive: true, maintainAspectRatio: false, plugins: { legend: { display: false } } }
});
</script>
```

Rules: 1 chart/slide, key takeaway as text, label axes, accessible colors, tooltips, reduced-motion support.

---

## Navigation Controller

```js
class SlideMaestro {
    constructor() { this.slides = document.querySelectorAll('.slide'); this.current = 0; this.init(); }
    init() {
        document.addEventListener('keydown', e => {
            if (e.key === 'ArrowDown' || e.key === ' ' || e.key === 'PageDown') this.next();
            if (e.key === 'ArrowUp' || e.key === 'PageUp') this.prev();
            if (e.key === 'Home') this.goTo(0);
            if (e.key === 'End') this.goTo(this.slides.length - 1);
        });
        let ty = 0;
        document.addEventListener('touchstart', e => ty = e.touches[0].clientY);
        document.addEventListener('touchend', e => { const d = ty - e.changedTouches[0].clientY; if (Math.abs(d) > 50) d > 0 ? this.next() : this.prev(); });
        this.createProgress();
    }
    next() { this.goTo(Math.min(this.current + 1, this.slides.length - 1)); }
    prev() { this.goTo(Math.max(this.current - 1, 0)); }
    goTo(i) { this.slides[i].scrollIntoView({ behavior: 'smooth' }); this.current = i; this.updateProgress(); }
    createProgress() { const b = document.createElement('div'); b.style.cssText = 'position:fixed;top:0;left:0;height:3px;background:var(--accent);transition:width .3s;z-index:9999'; document.body.appendChild(b); this.progressBar = b; this.updateProgress(); }
    updateProgress() { this.progressBar.style.width = ((this.current + 1) / this.slides.length * 100) + '%'; }
}
new SlideMaestro();
```

---

## PPT/PPTX Conversion

1. Use python3 + python-pptx to extract text, images, notes
2. If unavailable: `pip install python-pptx`
3. Preserve slide order, speaker notes, extracted assets
4. After extraction → same style-selection workflow
5. Cross-platform (Python, not macOS-only)

---

## Anti-Slop Rules

NEVER:
- Generic purple gradients on white
- Inter/Roboto/Arial/system fonts
- Bullet walls (>6 = split the slide)
- Scrolling code blocks
- Startup-gradient templates
- Fake metrics or placeholder testimonials
- Emoji as structural icons
- "Insights", "Growth", "Scale" without content
- Rainbow palettes
- Glassmorphism by default

DO:
- Bold, intentional aesthetic direction
- Distinctive typography per deck
- Atmospheric backgrounds (gradients, noise, geometry, grain)
- Meaningful animation
- Sparse slides solved with layout/rhythm/scale
- Real content or clearly marked placeholders

---

## Variation Rules

Offer 3 options minimum:
1. **Conservative** — lowest risk
2. **Strong-fit** — best interpretation
3. **Divergent** — novel, pushes boundaries

When user picks → consolidate. Do not leave as pile of options.

---

## Deck Rules

- Default: 1920x1080, 16:9
- Fixed canvas scaled to fit viewport
- Keyboard + touch + wheel navigation
- localStorage slide persistence
- 1-2 background colors max
- Text 24px+ at 1920x1080

---

## Accessibility

- Semantic: main, section, nav
- Contrast 4.5:1 minimum
- Keyboard-only nav
- prefers-reduced-motion
- Alt text for images
- Color never sole indicator
- Visible focus states
- Aria-labels for icon-only controls

---

## Pre-Delivery Checklist

- Runs from local file in browser
- Every slide fits viewport
- Style is distinctive, not generic
- Animation is meaningful
- Reduced motion respected
- No Inter/Roboto
- WCAG AA contrast
- Verified at 1920x1080 and 375x667

---

## Reference Files

- **Style Presets** → `references/style-presets.md`
- **Copywriting Formulas** → `references/copywriting-formulas.md`
- **Layout Patterns** → `references/layout-patterns.md`
- **Slide Strategies** → `references/slide-strategies.md`
- **HTML Template** → `references/html-template.md`
