---
name: slides-to-pptx
description: Create stunning, animation-rich HTML presentations from scratch or by converting PowerPoint files, with optional PPTX export via PptxGenJS. Features 12 curated style presets, visual style discovery, viewport-perfect slides, inline editing, and end-to-end content-to-PowerPoint workflow.
---

# Slides to PPTX

Create zero-dependency, animation-rich HTML presentations that run entirely in the browser, with optional PPTX export via PptxGenJS.

## Core Principles

1. **Zero Dependencies** — Single HTML files with inline CSS/JS. No npm, no build tools.
2. **Show, Don't Tell** — Generate visual previews, not abstract choices. People discover what they want by seeing it.
3. **Distinctive Design** — No generic "AI slop." Every presentation must feel custom-crafted.
4. **Viewport Fitting (NON-NEGOTIABLE)** — Every slide MUST fit exactly within 100vh. No scrolling within slides, ever. Content overflows? Split into multiple slides.
5. **Step-by-Step Execution** — You MUST execute this workflow strictly step-by-step. Never jump ahead to the next phase. ALWAYS stop and wait for user input after asking a question.

## Design Aesthetics

You tend to converge toward generic, "on distribution" outputs. In frontend design, this creates what users call the "AI slop" aesthetic. Avoid this: make creative, distinctive frontends that surprise and delight.

Focus on:
- Typography: Choose fonts that are beautiful, unique, and interesting. Avoid generic fonts like Arial and Inter; opt instead for distinctive choices that elevate the frontend's aesthetics.
- Color & Theme: Commit to a cohesive aesthetic. Use CSS variables for consistency. Dominant colors with sharp accents outperform timid, evenly-distributed palettes. Draw from IDE themes and cultural aesthetics for inspiration.
- Motion: Use animations for effects and micro-interactions. Prioritize CSS-only solutions for HTML. Use Motion library for React when available. Focus on high-impact moments: one well-orchestrated page load with staggered reveals (animation-delay) creates more delight than scattered micro-interactions.
- Backgrounds: Create atmosphere and depth rather than defaulting to solid colors. Layer CSS gradients, use geometric patterns, or add contextual effects that match the overall aesthetic.

Avoid generic AI-generated aesthetics:
- Overused font families (Inter, Roboto, Arial, system fonts)
- Cliched color schemes (particularly purple gradients on white backgrounds)
- Predictable layouts and component patterns
- Cookie-cutter design that lacks context-specific character

Interpret creatively and make unexpected choices that feel genuinely designed for the context. Vary between light and dark themes, different fonts, different aesthetics. You still tend to converge on common choices (Space Grotesk, for example) across generations. Avoid this: it is critical that you think outside the box!

## Viewport Fitting Rules

These invariants apply to EVERY slide in EVERY presentation:

- Every `.slide` must have `height: 100vh; height: 100dvh; overflow: hidden;`
- ALL font sizes and spacing must use `clamp(min, preferred, max)` — never fixed px/rem
- Content containers need `max-height` constraints
- Images: `max-height: min(50vh, 400px)`
- Breakpoints required for heights: 700px, 600px, 500px
- Include `prefers-reduced-motion` support
- Never negate CSS functions directly (`-clamp()`, `-min()`, `-max()` are silently ignored) — use `calc(-1 * clamp(...))` instead

**When generating, read `viewport-base.css` and include its full contents in every presentation.**

### Content Density Limits Per Slide

| Slide Type | Maximum Content |
|------------|-----------------|
| Title slide | 1 heading + 1 subtitle + optional tagline |
| Content slide | 1 heading + 4-6 bullet points OR 1 heading + 2 paragraphs |
| Feature grid | 1 heading + 6 cards maximum (2x3 or 3x2) |
| Code slide | 1 heading + 8-10 lines of code |
| Quote slide | 1 quote (max 3 lines) + attribution |
| Image slide | 1 heading + 1 image (max 60vh height) |

**Content exceeds limits? Split into multiple slides. Never cram, never scroll.**

---

## Phase 0: Detect Mode

Determine what the user wants:

- **Mode A: New Presentation** — Create from scratch. Go to Phase 1.
- **Mode B: PPT Conversion** — Convert a .pptx file. Go to Phase 4.
- **Mode C: Enhancement** — Improve an existing HTML presentation. Read it, understand it, enhance. **Follow Mode C modification rules below.**

### Mode C: Modification Rules

When enhancing existing presentations, viewport fitting is the biggest risk:

1. **Before adding content:** Count existing elements, check against density limits
2. **Adding images:** Must have `max-height: min(50vh, 400px)`. If slide already has max content, split into two slides
3. **Adding text:** Max 4-6 bullets per slide. Exceeds limits? Split into continuation slides
4. **After ANY modification, verify:** `.slide` has `overflow: hidden`, new elements use `clamp()`, images have viewport-relative max-height, content fits at 1280x720
5. **Proactively reorganize:** If modifications will cause overflow, automatically split content and inform the user. Don't wait to be asked

**When adding images to existing slides:** Move image to new slide or reduce other content first. Never add images without checking if existing content already fills the viewport.

---

## Phase 1: Content Discovery (New Presentations)

**Detect language from the user's messages and content. Respond in the same language throughout the entire workflow.**

**Ask ALL questions in a single interaction** so the user fills everything out at once:

**Question 1 — Purpose** (header: "Purpose"):
What is this presentation for? Options: Pitch deck / Teaching-Tutorial / Conference talk / Internal presentation

**Question 2 — Length** (header: "Length"):
Approximately how many slides? Options: Short 5-10 / Medium 10-20 / Long 20+

**Question 3 — Content** (header: "Content"):
Do you have content ready? Options: All content ready / Rough notes / Topic only

**Question 4 — Inline Editing** (header: "Editing"):
Do you need to edit text directly in the browser after generation? Options:
- "Yes (Recommended)" — Can edit text in-browser, auto-save to localStorage, export file
- "No" — Presentation only, keeps file smaller

**Remember the user's editing choice — it determines whether edit-related code is included in Phase 3.**

If user has content, ask them to share it.

🛑 **CRITICAL: STOP HERE AND WAIT. You must wait for the user to answer the questions above. DO NOT proceed to Phase 2 or 3 until the user replies.**

### Step 1.2: Image Evaluation (if images provided)

If user selected "No images" → skip to Phase 2.

If user provides an image folder:
1. **Scan** — List all image files (.png, .jpg, .svg, .webp, etc.)
2. **View each image** — Use the Read tool (Claude is multimodal)
3. **Evaluate** — For each: what it shows, USABLE or NOT USABLE (with reason), what concept it represents, dominant colors
4. **Co-design the outline** — Curated images inform slide structure alongside text. This is NOT "plan slides then add images" — design around both from the start (e.g., 3 screenshots → 3 feature slides, 1 logo → title/closing slide)
5. **Confirm** (header: "Outline"): "Does this slide outline and image selection look right?" Options: Looks good / Adjust images / Adjust outline

🛑 **CRITICAL: STOP HERE AND WAIT for the user to confirm the outline before generating any presentation.**

**Logo in previews:** If a usable logo was identified, embed it (base64) into each style preview in Phase 2 — the user sees their brand styled three different ways.

---

## Phase 2: Style Discovery

**This is the "show, don't tell" phase.** Most people can't articulate design preferences in words.

### Step 2.0: Style Path

Ask how they want to choose (header: "Style"):
- "Show me options" (recommended) — Generate 3 previews based on mood
- "I know what I want" — Pick from preset list directly

**If direct selection:** Show preset picker and skip to Phase 3. Available presets are defined in [STYLE_PRESETS.md](STYLE_PRESETS.md).

🛑 **CRITICAL: STOP HERE AND WAIT for the user to choose their style path. DO NOT simulate their choice.**

### Step 2.1: Mood Selection (Guided Discovery)

Ask (header: "Vibe", multiSelect: true, max 2):
What feeling should the audience have? Options:
- Impressed/Confident — Professional, trustworthy
- Excited/Energized — Innovative, bold
- Calm/Focused — Clear, thoughtful
- Inspired/Moved — Emotional, memorable

🛑 **CRITICAL: STOP HERE AND WAIT for the user to select the mood. DO NOT proceed to generating previews until they reply.**

### Step 2.2: Generate 3 Style Previews

Based on mood, generate 3 distinct single-slide HTML previews showing typography, colors, animation, and overall aesthetic. Read [STYLE_PRESETS.md](STYLE_PRESETS.md) for available presets and their specifications.

| Mood | Suggested Presets |
|------|-------------------|
| Impressed/Confident | Bold Signal, Electric Studio, Dark Botanical |
| Excited/Energized | Creative Voltage, Neon Cyber, Split Pastel |
| Calm/Focused | Notebook Tabs, Paper & Ink, Swiss Modern |
| Inspired/Moved | Dark Botanical, Vintage Editorial, Pastel Geometry |

Save previews to `.claude-design/slide-previews/` (style-a.html, style-b.html, style-c.html). Each should be self-contained, ~50-100 lines, showing one animated title slide.

Open each preview automatically for the user.

### Step 2.3: User Picks

Ask (header: "Style"):
Which style preview do you prefer? Options: Style A: [Name] / Style B: [Name] / Style C: [Name] / Mix elements

If "Mix elements", ask for specifics.

🛑 **CRITICAL: STOP HERE AND WAIT for the user to select their preferred style. DO NOT proceed to Phase 3 until they have explicitly made a choice.**

---

## Phase 3: Generate Presentation

Generate the full presentation using content from Phase 1 (text, or text + curated images) and style from Phase 2.

If images were provided, the slide outline already incorporates them from Step 1.2. If not, CSS-generated visuals (gradients, shapes, patterns) provide visual interest — this is a fully supported first-class path.

**Before generating, read these supporting files:**
- [html-template.md](html-template.md) — HTML architecture and JS features
- [viewport-base.css](viewport-base.css) — Mandatory CSS (include in full)
- [animation-patterns.md](animation-patterns.md) — Animation reference for the chosen feeling

**Key requirements:**
- Single self-contained HTML file, all CSS/JS inline
- Include the FULL contents of viewport-base.css in the `<style>` block
- Use fonts from Fontshare or Google Fonts — never system fonts
- Add detailed comments explaining each section
- Every section needs a clear `/* === SECTION NAME === */` comment block
- Set `<html lang="...">` based on content language (e.g., `zh-CN` for Chinese, `en` for English, `ja` for Japanese)

---

## Phase 4: PPT Conversion

When converting PowerPoint files:

1. **Extract content** — Run `python scripts/extract-pptx.py <input.pptx> <output_dir>` (install python-pptx if needed: `pip install python-pptx`)
2. **Confirm with user** — Present extracted slide titles, content summaries, and image counts
3. **Style selection** — Proceed to Phase 2 for style discovery
4. **Generate HTML** — Convert to chosen style, preserving all text, images (from assets/), slide order, and speaker notes (as HTML comments)

🛑 **CRITICAL: STOP HERE AND WAIT for user feedback after generating the HTML before automatically proceeding to export PPTX.**

---

## Phase 5: PPTX Export

After generating the HTML presentation, ask the user if they want to export to PPTX. If yes, ask:

**Question: Export Format**
Do you want an editable native PPTX or a high-fidelity screenshot PPTX? Options:
- "Native text/shapes" (Smaller file, editable text, but font/layout might differ slightly from HTML)
- "Screenshots" (Larger file, non-editable text, but 100% preserves original HTML design and fonts)

Depending on their choice, follow the corresponding section below.

### Option A: Native PPTX (via PptxGenJS)

#### Dependencies

```bash
npm install pptxgenjs
```

#### PPTX Generation Rules

**Before generating, read these supporting files:**
- [html2pptx.md](html2pptx.md) — HTML to PPTX conversion detailed guide
- [ooxml.md](ooxml.md) — OOXML technical reference
- [generate-pptx.js](generate-pptx.js) — Reference implementation

#### Basic Structure

```javascript
const PptxGenJS = require('pptxgenjs');

// Create presentation
const pptx = new PptxGenJS();


// Metadata
pptx.author = 'Author Name';
pptx.title = 'Presentation Title';

// Layout (16:9)
pptx.defineLayout({ name: 'CUSTOM', width: 13.33, height: 7.5 });
pptx.layout = 'CUSTOM';
```

#### Important Notes

**1. Color codes — NO `#` prefix in PptxGenJS:**

```javascript
// ✅ Correct
{ color: '10B981' }
{ fill: 'F9FAFB' }

// ❌ Wrong (may corrupt file)
{ color: '#10B981' }
{ fill: '#F9FAFB' }
```

**2. Font — match the language of the content:**

```javascript
// Chinese
{ fontFace: 'Noto Sans SC' }
// English
{ fontFace: 'Arial' }
// Japanese
{ fontFace: 'Noto Sans JP' }
```

**3. Line breaks — use `\n`:**

```javascript
slide.addText('第一行\n第二行', { ... });
```

**4. Emoji — may not display in some environments. Use text as backup for important info.**

#### File Save

```javascript
pptx.writeFile({ fileName: 'output/presentation.pptx' })
  .then(fileName => console.log(`Created: ${fileName}`));
```

### Color Palette

**Use colors from the style chosen in Phase 2.** The table below is a fallback reference only:

| Usage | Color Code | Description |
|-------|-----------|-------------|
| Primary | `2563EB` | Main accent |
| Success | `10B981` | Positive/Complete |
| Warning | `F59E0B` | Attention/Preference |
| Danger | `EF4444` | Negative/Unmet |
| Neutral | `6B7280` | Secondary text |
| Background | `F9FAFB` | Background |
| Text Primary | `111827` | Main text |
| Text Secondary | `6B7280` | Secondary text |
| Border | `E5E7EB` | Border/Divider |

> **Important:** Always derive PPTX colors from the HTML presentation's style. Do not default to the above palette if a specific style was selected.

### Option B: Screenshot PPTX (via Playwright)

If the user wants a pixel-perfect screenshot presentation:

#### Dependencies

```bash
npm install playwright pptxgenjs
```

#### Screenshot Generation Rules

1. Write a Node.js script using `playwright` to launch a headless browser.
2. The script should open the generated HTML file.
3. It must wait for the initial animations to finish (e.g., `await page.waitForTimeout(2000)`).
4. Iterate through all slides (either by calling the presentation's navigation JS, like `await page.evaluate(() => app.goToSlide(i))`, or simulating keyboard events like `await page.keyboard.press('ArrowDown')`).
5. After navigating to each slide, wait for any transition/reveal animations to complete before capturing (`await page.waitForTimeout(1500)`).
6. Take a screenshot of the viewport (`const buffer = await page.screenshot()`).
7. Use `pptxgenjs` to create a new presentation, add a slide for each screenshot, and set the screenshot as the slide background or a full-size image.
8. Save the `.pptx` file.

---

## Phase 6: Delivery

1. **Clean up** — Delete `.claude-design/slide-previews/` if it exists
2. **Open** — Use `open [filename].html` to launch in browser
3. **Summarize** — Tell the user:
   - File location, style name, slide count
   - Navigation: Arrow keys, Space, scroll/swipe, click nav dots
   - How to customize: `:root` CSS variables for colors, font link for typography, `.reveal` class for animations
   - If inline editing was enabled: Hover top-left corner or press E to enter edit mode, click any text to edit, Ctrl+S to save
   - If PPTX was exported:
     - PPTX file location and file size
     - Open with PowerPoint / WPS / Keynote to verify
     - Recommend installing the appropriate font (e.g., Noto Sans SC for Chinese) for best rendering
     - Note that emoji icons may not render in all PowerPoint versions
4. **Ask** — Does the user want any adjustments?

---

## Supporting Files

| File | Purpose | When to Read |
|------|---------|-------------|
| [STYLE_PRESETS.md](STYLE_PRESETS.md) | 12 curated visual presets with colors, fonts, and signature elements | Phase 2 (style selection) |
| [viewport-base.css](viewport-base.css) | Mandatory responsive CSS — copy into every presentation | Phase 3 (generation) |
| [html-template.md](html-template.md) | HTML structure, JS features, code quality standards | Phase 3 (generation) |
| [animation-patterns.md](animation-patterns.md) | CSS/JS animation snippets and effect-to-feeling guide | Phase 3 (generation) |
| [scripts/extract-pptx.py](scripts/extract-pptx.py) | Python script for PPT content extraction | Phase 4 (conversion) |
| [html2pptx.md](html2pptx.md) | HTML to PPTX conversion detailed guide | Phase 5 (PPTX export) |
| [ooxml.md](ooxml.md) | OOXML technical reference | Phase 5 (PPTX export) |
| [generate-pptx.js](generate-pptx.js) | Reference implementation for PptxGenJS | Phase 5 (PPTX export) |
