---
name: html-slides
metadata:
  version: "0.9.4"
  author: danzhu
description: Generate polished single-file HTML slide presentations with interactive components (flip cards, charts, tables, code blocks, architecture flows, stats, timelines, and more) or creative visual themes. Use this skill whenever the user wants to create slides, presentations, decks, or any visual slide-based content as HTML. Also trigger when the user invokes /html-slides or mentions creating an HTML presentation, pitch deck, or slide deck.
---

# Frontend Slides

Create zero-dependency, animation-rich HTML presentations that run entirely in the browser.

## Agent Compatibility

This skill is optimized for **Claude Code** and uses `AskUserQuestion` for interactive prompts. If `AskUserQuestion` is not available (Gemini CLI, GitHub Copilot, OpenAI Codex, or other agents), ask the same questions as plain text in the conversation and wait for the user to respond before proceeding.

## Core Principles

1. **Zero Dependencies** — Single HTML files with inline CSS/JS. No npm, no build tools.
2. **Show, Don't Tell** — Generate visual previews, not abstract choices. People discover what they want by seeing it.
3. **Distinctive Design** — No generic "AI slop." Every presentation must feel custom-crafted.
4. **Content-Driven Design** — The content decides the visual treatment. Design each slide based on what it's communicating, not by cycling through a component catalog.
5. **Viewport Fitting (NON-NEGOTIABLE)** — Every slide MUST fit exactly within 100vh. No scrolling within slides, ever. Content overflows? Split into multiple slides.

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
| Chart slide | 1 heading + 1 chart (max 50vh height) + optional subtitle |

**Content exceeds limits? Split into multiple slides. Never cram, never scroll.**

---

## Phase 0: Detect Mode

Determine what the user wants:

- **Mode A: New Presentation** — Create from scratch. Go to Phase 1.
- **Mode B: PPT Conversion** — Convert a .pptx file. Go to Phase 4.
- **Mode C: Enhancement** — Improve an existing HTML presentation. Read it, understand it, enhance. **Follow Mode C modification rules below.**
- **Mode D: HTML Conversion** — Convert any HTML file (reveal.js, Marp, Google Slides export, article, generic page) into HTMLSlides format. Go to Phase 5.

### Mode C: Modification Rules

When modifying existing presentations, make **minimal changes** — only touch what the user asked about.

**Editing slides:**
- Read the existing HTML file first
- Modify only the requested slide(s), keep everything else intact
- If adding/removing slides, renumber all `data-slide` attributes sequentially from 0
- If changing a component type (e.g., code block → table), use the template from component-templates.md
- Update the inline `<script class="slide-notes">` block to match any content changes

**Viewport fitting (always check):**
- Before adding content, check against density limits
- Adding images: must have `max-height: min(50vh, 400px)`
- Adding text: max 4-6 bullets per slide. Exceeds? Split into multiple slides
- If modifications will cause overflow, split content and inform the user

**After ANY modification, verify all 8 spec rules:**
1. `<div class="deck" id="deck">` exists
2. All slides are `<div class="slide">` with sequential `data-slide="0"` through `data-slide="N"`
3. First slide has `class="slide active"`, no other slide has `active`
4. Global `goTo()`, `next()`, `prev()` functions exist
5. All CSS inline (except font imports)
6. All JS inline (except CDN libraries: Chart.js, Mermaid, anime.js)
7. No broken numbering gaps after insertions or deletions
8. `<meta name="generator" content="html-slides vX.Y.Z">` exists in `<head>`

**If any rule fails after editing, fix it before saving.**

---

## Phase 1: Choose Mode

**Always ask the user to choose a mode** unless they already specified one (or a specific theme) in their prompt.

Ask which mode they want (header: "Mode"):

- **Vibe** (Creative themes) — AI interprets your content freely with distinctive visual styles. Best for pitch decks, keynotes, and non-technical presentations.
- **Pro** — Structured interactive components: flip cards, charts, tables, code blocks, architecture flows, image slides, and more. Multiple themes available. Supports user-provided images. Best for technical talks, product demos, and data-rich presentations.

If the user already specified a mode or theme in their prompt, skip this question.

**If Pro:** Go to Phase 2A.
**If Vibe:** Go to Phase 2B.

---

## Phase 2A: Pro — Content & Theme

**Ask ALL questions in a single AskUserQuestion call:**

**Question 1 — Content** (header: "Content"):
Do you have content ready? Options: All content ready / Rough notes / Topic only

**Question 2 — Editing** (header: "Editing"):
Do you need to edit text directly in the browser after generation? Options:
- "Yes (Recommended)" — Can edit text in-browser, auto-save to localStorage, export file
- "No" — Presentation only, keeps file smaller

**Question 3 — Theme** (header: "Theme"):

- **Obsidian (default)** — Dark background, blue/green/orange accents
- **Excalidraw Light** — Hand-drawn, white background, sketch borders
- **Excalidraw Dark** — Hand-drawn, dark background, sketch borders
- **Binary Architect** — Hacker-elite, sharp corners, neon on void-black

If the user already specified a theme in their prompt, skip Question 3 and use that theme. If no preference, default to Obsidian.

**Question 4 — Images** (header: "Images"):
Do you have images to include? Options:
- "No images" — CSS-generated visuals only
- "Yes, I have an image folder" — Provide a folder path to scan
- "Yes, I'll paste/provide images" — Share images inline during content review

If user already provided or pasted images in their prompt, skip this question and note the images for Phase 3.

**Remember the editing choice — it determines whether edit-related code is included in Phase 3.**

If user has content, ask them to share it.

**If images were provided (folder or inline):**
1. **View each image** — Use the Read tool (Claude is multimodal)
2. **Evaluate** — For each: what it shows, usable or not (with reason), dominant colors
3. **Plan placement** — Match images to slides using the **Image Slide** component template. Logos go on title/closing slides. Screenshots and diagrams get dedicated image slides.
4. **Process if needed** — Oversized images (>1MB): resize. Logos on rounded themes: circular crop. See Image Pipeline in `references/html-template.md`.
5. **Copy to assets/** — Place images in an `assets/` folder next to the HTML file. Use relative `src="assets/..."` paths.

Then go to Phase 3.

Each theme uses the same components and navigation — only the visual style changes. Theme files are in `assets/themes/`.

---

## Phase 2B: Vibe — Content & Style Discovery

**This is the "show, don't tell" phase.** Most people can't articulate design preferences in words.

### Step 2B.1: Content Discovery

**Ask ALL questions in a single AskUserQuestion call:**

**Question 1 — Purpose** (header: "Purpose"):
What is this presentation for? Options: Pitch deck / Teaching-Tutorial / Conference talk / Internal presentation

**Question 2 — Length** (header: "Length"):
Approximately how many slides? Options: Short 5-10 / Medium 10-20 / Long 20+

**Question 3 — Content** (header: "Content"):
Do you have content ready? Options: All content ready / Rough notes / Topic only

**Question 4 — Editing** (header: "Editing"):
Do you need to edit text directly in the browser after generation? Options:
- "Yes (Recommended)" — Can edit text in-browser, auto-save to localStorage, export file
- "No" — Presentation only, keeps file smaller

**Remember the editing choice — it determines whether edit-related code is included in Phase 3.**

If user has content, ask them to share it.

### Step 2B.2: Image Evaluation (if images provided)

If user selected "No images" → skip to Step 2B.3.

If user provides an image folder:
1. **Scan** — List all image files (.png, .jpg, .svg, .webp, etc.)
2. **View each image** — Use the Read tool (Claude is multimodal)
3. **Evaluate** — For each: what it shows, USABLE or NOT USABLE (with reason), what concept it represents, dominant colors
4. **Co-design the outline** — Curated images inform slide structure alongside text. This is NOT "plan slides then add images" — design around both from the start (e.g., 3 screenshots → 3 feature slides, 1 logo → title/closing slide)
5. **Confirm via AskUserQuestion** (header: "Outline"): "Does this slide outline and image selection look right?" Options: Looks good / Adjust images / Adjust outline

**Logo in previews:** If a usable logo was identified, embed it (base64) into each style preview in Step 2B.4.

### Step 2B.3: Style Path

Ask how they want to choose (header: "Style"):
- "Show me options" (recommended) — Generate 3 previews based on mood
- "I know what I want" — Pick from preset list directly

**If direct selection:** Show preset picker and skip to Phase 3. Available presets are defined in [STYLE_PRESETS.md](references/STYLE_PRESETS.md).

### Step 2B.4: Mood Selection

Ask (header: "Vibe", multiSelect: true, max 2):
What feeling should the audience have? Options:
- Impressed/Confident — Professional, trustworthy
- Excited/Energized — Innovative, bold
- Calm/Focused — Clear, thoughtful
- Inspired/Moved — Emotional, memorable

### Step 2B.5: Preview Matching Presets

**Show, don't tell.** Instead of listing preset names, generate visual previews.

1. Read [STYLE_PRESETS.md](references/STYLE_PRESETS.md) for available presets and their specifications.
2. From the mood-matched presets below, **randomly pick 3** and generate a single-slide HTML preview for each. Save previews to `.claude-design/slide-previews/` and open them.
3. Ask the user to pick one (header: "Pick a Style"):
   - Options: "1" / "2" / "3" / "Show 3 more" / "I know what I want"

**Mood → Preset Pool:**

**Impressed / Confident:** Obsidian, Bold Signal, Electric Studio, Dark Botanical, Editorial Light

**Excited / Energized:** Creative Voltage, Neon Cyber, Binary Architect, Terminal Green, Split Pastel

**Calm / Focused:** Notebook Tabs, Paper & Ink, Swiss Modern, Excalidraw Light, Pastel Geometry

**Inspired / Moved:** Dark Botanical, Vintage Editorial, Excalidraw Dark, Pastel Geometry

If "Show 3 more" — pick 3 different presets from the same pool (avoid repeats from previous round). If the pool is exhausted, show remaining presets.

If "I know what I want" — show the full preset list for their mood category and let them pick by name.

If "Mix elements" — ask for specifics.

---

## Phase 3: Generate Presentation

Generate the full presentation using content from Phase 1 (text, or text + curated images) and style from Phase 2.

If images were provided, the slide outline already incorporates them from Step 1.2. If not, CSS-generated visuals (gradients, shapes, patterns) provide visual interest — this is a fully supported first-class path.

### Content Analysis (Pro and Vibe)

Before writing any HTML, analyze the content and plan each slide. For each slide, determine:

1. **Purpose** — What is this slide communicating?
2. **Content elements** — What specific content goes on this slide?
3. **Visual treatment** — What's the best way to present this visually?

**Key principle:** If two slides have similar content (e.g., four roadmap themes each with status items), do NOT give them all the same treatment. Vary the visual approach — different layouts, different component types, different visual metaphors. Repetition kills engagement.

**This analysis is internal — do not present the plan to the user.**

### Supporting Files

**Before generating, read these supporting files based on the chosen style:**

**For creative presets (presets 1-12):**
- [html-template.md](references/html-template.md) — HTML architecture and JS features
- [viewport-base.css](assets/viewport-base.css) — Mandatory CSS (include in full)
- [animation-patterns.md](references/animation-patterns.md) — Animation reference for the chosen feeling
- [libraries.md](references/libraries.md) — CDN libraries for diagrams and animations (use when content needs them)

**For Pro mode (structured component mode):**
- [component-templates.md](references/component-templates.md) — Component style reference for charts, code blocks, cards, tables, images. Use as a **styling guide** when your design calls for these elements — not a menu to cycle through.
- [components.css](assets/components.css) — Shared component CSS (copy verbatim into `<style>`)
- Theme CSS from `assets/themes/` — copy verbatim into `<style>`, BEFORE components.css
- [slides-runtime.js](assets/slides-runtime.js) — Navigation JS (copy verbatim into `<script>`)
- **Excalidraw themes** use CSS-only for the hand-drawn aesthetic. The theme CSS (excalidraw.css / excalidraw-dark.css) handles hachure fills, offset shadows, and rounded corners entirely with CSS — no JavaScript needed.
- [libraries.md](references/libraries.md) — CDN libraries for diagrams (Mermaid.js), orchestrated animations (anime.js). Use when the content calls for them.
- If any slides use **Chart** components, add Chart.js CDN in `<head>` before `<style>`: `<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.8/dist/chart.umd.min.js"></script>`

**Available Pro themes** (user specifies in prompt, default: Obsidian):

| Theme | File | Vibe |
|-------|------|------|
| Obsidian (default) | `assets/themes/dark-interactive.css` | Dark background, blue/green/orange accents |
| Excalidraw Light | `assets/themes/excalidraw.css` | Hand-drawn, white background, sketch borders |
| Excalidraw Dark | `assets/themes/excalidraw-dark.css` | Hand-drawn, dark background, sketch borders |
| Editorial Light | `assets/themes/editorial-light.css` | Luminous, editorial, tech-forward minimalism |
| Binary Architect | `assets/themes/binary-architect.css` | Hacker-elite, sharp corners, neon on void-black |

**Key requirements:**
- Single self-contained HTML file, all CSS/JS inline
- For Vibe mode: include the FULL contents of viewport-base.css in the `<style>` block. **CRITICAL: Do NOT redefine `.slide` positioning or layout after pasting viewport-base.css** — it already defines `.slide` with `position: relative`, `scroll-snap-align`, and flex layout. Adding a second `.slide { position: absolute; opacity: 0; }` will conflict and cause blank or overlapping slides. Only add visual styles (colors, backgrounds, typography, animations) on top.
- For Pro mode: include the chosen theme CSS + components.css in the `<style>` block, and slides-runtime.js in the `<script>` block
- Use fonts from Fontshare or Google Fonts — never system fonts
- Add detailed comments explaining each section
- Every section needs a clear `/* === SECTION NAME === */` comment block
- **Always generate speaker notes** — see Speaker Notes below

### Speaker Notes (Mandatory)

Speaker notes are **embedded inline** in each slide as a hidden JSON block. They are displayed in the browser's developer console when navigating slides — open DevTools, detach to a separate window, and you have a presenter view.

Every slide must include a `<script type="application/json" class="slide-notes">` block as its last child:

```html
<div class="slide" data-slide="0">
  <!-- visible slide content -->
  <script type="application/json" class="slide-notes">
  {"title":"Introduction","script":"HTML Slides lets you create beautiful presentations without design skills.","notes":["Zero dependencies","Works with 4 AI agents"]}
  </script>
</div>
```

**Format:** Each slide-notes block contains:
- `title` — Slide heading (for console display and presenter apps)
- `script` — What the presenter would **read aloud** for this slide. Natural, conversational, professional tone. Not a meta-description of the component — the actual words the presenter says to the audience.
- `notes` — Bullet points summarizing the **key points** the slide is communicating. Each note captures one talking point from the slide content.

**Script tone:** Write as if the presenter is speaking naturally to an audience. Conversational but professional. Example:
- GOOD: "Here's what makes this different — everything lives in one HTML file. No build step, no framework. You just open it and present."
- BAD: "This slide uses a Statement component with a glow blob background to display the main value proposition."

**Notes content:** Summarize what the slide is actually saying, not how it's built. Example:
- GOOD: ["Single self-contained HTML file", "No build tools or frameworks", "Works offline on any device"]
- BAD: ["Large centered text", "Glow blob in background", "fadeInUp animation"]

**Console output:** On each slide change, the navigation JS logs the notes to the console with styled formatting. The presenter opens DevTools (F12), detaches it to a separate window, and reads notes while presenting. A link to the HTML Slides presenter app is shown for a richer experience.

**NEVER include:**
- Delivery instructions ("Pause here", "Slow down")
- Transition cues ("Move to next slide")
- Presentation advice ("Emphasize this", "If short on time skip")
- Meta commentary ("This is the summary slide")

**Example — slide about AI agent capabilities with 4 flip cards:**
```json
{
  "title": "Four Core Capabilities",
  "script": "Agents need four things working together: reasoning, memory, tools, and evaluation.",
  "notes": [
    "Reasoning — choose the next step",
    "Memory — carry context across steps",
    "Tools — take actions in the real world",
    "Evaluation — detect errors, confirm completion"
  ]
}
```

**Example — stats slide showing "3.2x faster, 47% fewer incidents, 89% satisfaction":**
```json
{
  "title": "By the Numbers",
  "script": "AI-assisted development delivers measurable improvements across speed, quality, and satisfaction.",
  "notes": [
    "3.2x faster code review",
    "47% fewer production incidents",
    "89% developer satisfaction"
  ]
}
```

---

## Phase 4: PPT Conversion

When converting PowerPoint files:

1. **Extract content** — Run `python scripts/extract-pptx.py <input.pptx> <output_dir>` (install python-pptx if needed: `pip install python-pptx`)
2. **Confirm with user** — Present extracted slide titles, content summaries, and image counts
3. **Style selection** — Proceed to Phase 2 for style discovery
4. **Generate HTML** — Convert to chosen style, preserving all text, images (from assets/), slide order, and speaker notes (as HTML comments)

---

## Phase 5: HTML Conversion (Mode D)

Convert existing HTML files into spec-compliant HTMLSlides presentations.

### Step 5.1: Analyze Input

Read the HTML file and classify the source. Read [conversion-patterns.md](references/conversion-patterns.md) for framework detection patterns.

| Source Type | Detection | Extraction Strategy |
|-------------|-----------|-------------------|
| reveal.js | `<div class="reveal">` + `<section>` elements | Map sections 1:1 to slides |
| Marp | `<!-- marp: true -->` or `class="marpit"` | Map Marp slides 1:1 |
| impress.js | `<div id="impress">` + `div.step` | Map steps 1:1 to slides |
| Slidev | `class="slidev-layout"` or Slidev-specific classes | Map layouts 1:1 to slides |
| Google Slides | Deeply nested divs with Google-specific classes | Extract text/images from structure |
| HTMLSlides (partial) | Has some but not all of the 7 spec rules | Fix compliance gaps only |
| Article/Blog | `<article>`, `<main>`, or heading-structured HTML | Split at headings |
| Generic HTML | None of the above | Split at headings, analyze structure |

Run a compliance audit against the 7 spec rules. If all pass, tell the user the file is already compliant — no conversion needed. If partially compliant, offer to fix only the failing rules.

Report content inventory to the user: slide count, content types, external dependencies, estimated output slides. Ask for confirmation before proceeding.

### Step 5.2: Extract Content

**For slide frameworks (reveal.js, Marp, impress.js, Slidev):**
- Map existing slides 1:1 to HTMLSlides slides
- Extract title, body content, images, code blocks from each slide
- Preserve slide order
- If a source slide exceeds density limits, split it

**For articles/blog posts/generic HTML:**
- Split content at heading boundaries (h1/h2 = new slide)
- First heading becomes the title slide
- Group related paragraphs, lists, and images under their nearest heading
- Code blocks → code slides, tables → table slides, blockquotes → quote slides
- Long lists get split across multiple slides (max 6 items per slide)

**For partially compliant HTMLSlides files:**
- Keep existing slide structure intact
- Only fix the specific failing rules

**Handle dependencies:**
- External CSS → inline it. External JS → strip framework JS, keep content JS.
- Images → keep URLs, apply `max-height: min(50vh, 400px)`.
- Fonts → keep Google Fonts / Fontshare, replace others.

### Step 5.3: Style Selection

Same as Phase 1 — ask Vibe or Pro. Default to Pro. Then follow Phase 2A or 2B accordingly.

### Step 5.4: Generate

Same as Phase 3 — read the appropriate supporting files and generate. Design each slide based on its content, using component templates as a style reference when they fit.

Always embed inline speaker notes in each slide. If the source had speaker notes, preserve them as inline `<script class="slide-notes">` blocks.

### Step 5.5: Validate & Save

Before saving, verify all 8 spec rules pass. Fix any that fail. Save the HTML file.

---

## Phase 6: Delivery

1. **Clean up** — Delete `.claude-design/slide-previews/` if it exists
2. **Open** — Use `open [filename].html` to launch in browser
3. **Summarize** — Tell the user:
   - File location, style name, slide count
   - Navigation: Arrow keys, Space, scroll/swipe, click nav dots
   - Speaker notes: Open DevTools (F12), detach to separate window — notes appear in console on each slide change
   - How to customize: `:root` CSS variables for colors, font link for typography, `.reveal` class for animations
   - If inline editing was enabled: Hover top-left corner or press E to enter edit mode, click any text to edit, Ctrl+S to save

---

## Phase 7: Share & Export (Optional)

After delivery, ask: _"Would you like to share this presentation? I can deploy it to a live URL or export it as a PDF."_

Options: **Deploy to URL** / **Export to PDF** / **Both** / **No thanks**

If the user declines, stop here.

### 7A: Deploy to a Live URL (Vercel)

Deploys the presentation to a permanent shareable URL. Works on any device.

1. **Check prerequisites** — Run `npx vercel --version`. If not found, user needs Node.js first.
2. **Check login** — Run `npx vercel whoami`. If not logged in, guide through:
   - Sign up at https://vercel.com/signup (free)
   - Run `vercel login` to authorize
3. **Deploy** — Run:
   ```bash
   bash scripts/deploy.sh <path-to-presentation>
   ```
   Accepts a single HTML file or a folder with index.html.
4. **Share the URL** — Tell the user the live URL, that it works on any device, and that they can delete it from https://vercel.com/dashboard later.

**Requires:** Node.js + Vercel account (free tier)

### 7B: Export to PDF

Captures each slide as a screenshot and combines into a single PDF. Animations are not preserved (static snapshot).

1. **Run:**
   ```bash
   bash scripts/export-pdf.sh <path-to-html> [output.pdf]
   ```
   If no output path given, saves next to the HTML file.
2. **What happens:** Playwright opens a headless browser, screenshots each slide at 1920x1080, assembles PDF. Auto-installs Playwright + Chromium on first run.
3. **Large files:** If PDF exceeds 10MB, offer compact mode:
   ```bash
   bash scripts/export-pdf.sh <path-to-html> [output.pdf] --compact
   ```
   Renders at 1280x720 — typically 50-70% smaller.

**Requires:** Node.js (Playwright auto-installs)

---

## Supporting Files

| File | Purpose | When to Read |
|------|---------|-------------|
| [STYLE_PRESETS.md](references/STYLE_PRESETS.md) | Curated visual presets with colors, fonts, and signature elements | Phase 2 (style selection) |
| [viewport-base.css](assets/viewport-base.css) | Mandatory responsive CSS — copy into every presentation (presets 1-12) | Phase 3 (generation) |
| [html-template.md](references/html-template.md) | HTML structure, JS features, code quality standards (presets 1-12) | Phase 3 (generation) |
| [animation-patterns.md](references/animation-patterns.md) | CSS/JS animation snippets and effect-to-feeling guide (presets 1-12) | Phase 3 (generation) |
| [component-templates.md](references/component-templates.md) | Component style reference — use when your design calls for these elements | Phase 3 (Pro) |
| [components.css](assets/components.css) | Shared component CSS for all Pro themes — copy verbatim | Phase 3 (Pro) |
| [themes/](assets/themes/) | Theme CSS files (dark-interactive, excalidraw, excalidraw-dark, editorial-light, binary-architect) — pick one | Phase 3 (Pro) |
| [slides-runtime.js](assets/slides-runtime.js) | Navigation JS — copy verbatim | Phase 3 (Pro) |
| [libraries.md](references/libraries.md) | CDN libraries: Mermaid.js (diagrams), anime.js (animations), Chart.js (charts) | Phase 3 (when content needs them) |
| [presentation-layer.md](references/presentation-layer.md) | Shared spec: slide structure, speaker notes, 8 validation rules, navigation | Phase 3 (reference) |
| [scripts/extract-pptx.py](scripts/extract-pptx.py) | Python script for PPT content extraction | Phase 4 (PPT conversion) |
| [conversion-patterns.md](references/conversion-patterns.md) | Framework detection patterns and extraction rules | Phase 5 (HTML conversion) |
| [scripts/deploy.sh](scripts/deploy.sh) | Deploy slides to Vercel for instant sharing | Phase 7 (sharing) |
| [scripts/export-pdf.sh](scripts/export-pdf.sh) | Export slides to PDF | Phase 7 (sharing) |
