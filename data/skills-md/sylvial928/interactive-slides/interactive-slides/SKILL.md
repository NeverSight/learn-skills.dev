---
name: interactive-slides
description: "Creates interactive, animated web presentations viewable in any browser — not PowerPoint files. Use this skill when the user wants a web-based or browser-viewable presentation, an interactive slide deck, or something more engaging than a static slide file. Perfect for pitches, proposals, data stories, reports, and technical talks. Trigger when the user says 'interactive presentation', 'web slides', 'web presentation', 'HTML presentation', or when they want slides that can be shared as a URL, need animations/motion/interactivity, or want to 'wow' their audience with something live on the web. Also trigger for scroll-based storytelling or immersive one-pagers when the context is presenting information. If the user asks for a 'presentation' or 'deck' without specifying .pptx, prefer this skill over the pptx skill unless they explicitly want a PowerPoint file."
---

# Interactive Presentation Skill

You're creating an interactive web presentation — a self-contained HTML file that opens beautifully in any browser. Not a PowerPoint. Something alive: animated, polished, web-native.

Your job is to understand what the user needs, structure their content for maximum clarity and impact, choose the right interactive format, and build something genuinely impressive.

## Phase 1: Discovery

**This phase is mandatory. Do not skip it, do not abbreviate it, do not jump to style or build.**

The discovery phase has a strict order:
1. Ask audience, goal, and delivery questions
2. Generate the style preview and get a pick
3. Produce a ghost list for confirmation (Phase 2)
4. Only then build

Before writing a line of code, understand the full picture. Ask these questions — but don't just list them dryly. **Make proposals and offer clear options** based on what you already know. If the user said "investor pitch for a fintech startup," you already know quite a bit — lead with an educated guess and let them confirm or adjust.

### Questions to cover (adapt based on what you already know)

**Audience & Goal**
- Who will see this? (executives, developers, customers, investors, students...)
- What's the core message — the one thing they should remember?
- What do you want them to feel or do after?

**Delivery**
- Will you present it live (you control the flow) or share it for async viewing (they navigate themselves)?
- Will it be shown on a big screen, shared as a URL, or embedded in a website?

**Content**
- What content do you have? Ask them to paste an outline, upload a document, describe the topic, or share a URL.
- If they give you raw content, tell them what you're going to do with it before doing it.

**Style & Brand**

Always ask this before generating any style preview. Frame it as a simple choice:

> *"Do you have a brand kit or style guidelines you'd like to use — or should I show you a few preset styles to pick from?"*

**If they have a brand kit**, accept any of these (one is enough — don't ask for all of them):

| Input | How to share it |
|-------|----------------|
| **Hex colors + font names** | Paste directly: `"primary: #2B4EFF, accent: #FF5733, body font: Helvetica Neue"` |
| **Logo file** | File path or URL — placed on every slide |
| **PPT template** | `.pptx` file path — used as the visual base for both HTML and editable export |
| **Canva Brand Kit** | In Canva: Brand Kit → copy hex colors + font names, or Share → Download → PowerPoint to get a template file |

Apply the brand colors to the HTML by creating a custom `:root {}` block instead of using a preset. Map their colors to `--bg`, `--accent`, `--text-primary`, `--text-secondary`, `--surface`. Load their fonts from Google Fonts if available.

**If they don't have a brand kit**, proceed with the preset style picker:
- Don't ask the user to describe their aesthetic in words — most people can't. Show them options instead.
- Pick 3 presets from `STYLE_PRESETS.md` that fit the topic and audience.
- Generate a `style-preview.html` file using the Style Preview Template from `STYLE_PRESETS.md`, showing all 3 presets as mini swatches side by side.
- Tell the user: *"Open `style-preview.html` in your browser — which one feels right? Or describe something different."*
- Wait for their pick before building. This one step prevents the most common iteration loop.

**Interactivity** (recommend based on delivery mode)
- Live presentation → recommend slide mode with animated reveals
- Async share → recommend slide mode with self-navigation as the default; ask if they'd prefer scroll-based storytelling instead
- Training or audience participation → recommend fully interactive (quizzes, branching)
- Portfolio/showcase → ask: slide deck or scroll-based cinematic experience?

**Default to slide mode (Mode A) unless the user specifically asks for scroll-based.** Slide mode works for both live and async sharing, gives users a familiar navigation experience, and is easier to repurpose as a .pptx later. Scroll story is a great choice but should be an opt-in, not the default.

Be direct with your recommendation: "I'd go with slide mode — click/arrow-key navigation, works live or shared async. Want scroll-based storytelling instead? It reads more like an article and works well for longer reports or portfolio pieces."

---

## Phase 2: Content Processing

### Always produce a ghost list first (unless the user already gave you one)

When the source is a document, URL, or free-form description, **do not go straight to building**. First convert the source into a proposed slide-by-slide ghost list and confirm it with the user. This prevents the most expensive iteration: building the wrong structure.

**Ghost list format:**
```
Slide 1 — [Title]
  Headline: [One-sentence slide headline]
  Content: [What goes on this slide — key point, stat, visual idea]

Slide 2 — [Title]
  Headline: ...
  Content: ...
```

After presenting the ghost list, append a density recommendation based on audience and delivery mode from Phase 1 — do not ask again, just state it. Then ask for confirmation on both together.

**Density reference table:**

| Audience / Mode | Recommended density |
|-----------------|-------------------|
| Executive, board, investor — live presentation | **Lean** — labels only, presenter fills verbally |
| Senior IC, growth, product — live presentation | **Lean-to-medium** — short labels + one sublabel line max |
| Technical audience — live presentation | **Medium** — labels + brief descriptor, code/diagram preferred over prose |
| Any audience — async share or scroll story | **Medium-to-rich** — more text is fine, reader controls pace |

**Format for the combined confirmation message:**
> "Does this structure work? Anything to add, cut, or reorder?
>
> Also — based on [audience] viewing this as a [live/async] presentation, I'd recommend **[density level]**: [one-sentence explanation of what that means in practice]. Let me know if you'd like a different approach."

Wait for the user's reply before proceeding. If they adjust the density, note it and apply it in the build.

**Density is a global default, not a per-slide rule.** Apply the recommended level as the baseline, but let individual slides deviate when the content demands it:
- Title and section-break slides are always lean regardless of global density — one strong line, nothing else.
- Evidence and data slides may carry more text even in a lean deck — a chart without context misleads.
- Conclusion and call-to-action slides return to lean — end on a clear, memorable line, not a wall of text.
- Architecture, process, and comparison slides can go medium even in lean decks — the structure IS the content.

---

### Visual Treatment Decision (runs only if lean or lean-to-medium density is confirmed)

**Step 2 — If lean or lean-to-medium density is chosen, ask about visual treatment for sparse slides:**

When content per slide is minimal, cards and layouts can look visually empty. Resolve this once globally — the choice applies across the whole deck.

Generate a small `visual-treatment-preview.html` file (similar to the style preview) showing these three options side by side using one of the deck's actual slides as the example:

| Option | Description |
|--------|-------------|
| **B — Decorative numbers** | Large faded 01 / 02 / 03 in each card. Fills visual weight without adding reading load. Consistent with lesson/principle slides. |
| **C — Icon anchors** | A relevant icon or emoji at the top of each card. Gives each item a visual identity and a focal point. |
| **D — Layout restructure** | Drop the card grid. Use a large bold number or word as a left-side anchor, with items as a vertical list on the right. High visual impact, works well for 3–5 item slides. |

Tell the user: *"Open `visual-treatment-preview.html` — which approach do you want for slides where content is sparse?"*

Apply the chosen treatment consistently across all relevant slides in the build.

**Only after both decisions are made, proceed to Phase 3 (Mode) and Phase 4 (Build).**

---

### Handling each input type

**Ghost list / outline (user already gave you one)**: Skip the ghost list step — you have it. Expand thin bullets into full slide content with context, transitions, and narrative flow. Still confirm the structure if it's complex.

**Document (PDF, Word, Markdown, URL)**: Read and extract. Identify the key ideas, reduce to essentials, create a logical arc. Build a ghost list showing what you're keeping, what you're cutting, and why. Present it for confirmation before building.

**Free-form description**: Ask clarifying questions if the topic is vague, then draft the ghost list yourself — slide titles, key messages, supporting points. Confirm before building.

### Communication best practices (apply to all content)

- **Pyramid Principle**: Lead with the conclusion. One clear headline per slide that stands alone. Details follow, not precede.
- **One idea per slide**: If you need two sentences to summarize a slide's point, split it.
- **Show, don't tell**: Replace bullet lists with visuals wherever possible — stats as large callouts, comparisons as side-by-side layouts, processes as step diagrams.
- **Narrative arc**: Hook → Problem/Tension → Solution → Evidence → Call to Action. Every presentation tells a story.
- **Audience calibration**: Executives want conclusions fast. Technical audiences want depth and data. Investors want traction and vision. Students want clarity. Match the vocabulary, depth, and pacing to who's watching. **Content density is not a fixed rule — it is a function of audience and delivery mode.** A live executive deck should have labels only (presenter fills verbally). An async technical report can carry full paragraphs. Never apply a blanket bullet limit — the answer lives in Phase 1: live presentation means lean, async means the text must stand on its own.
- **Rule of clarity**: Every slide should answer "so what?" If it doesn't, cut it or reframe it.

---

## Phase 3: Choose the Presentation Mode

**Default recommendation: Mode A (Slide Deck).** Only switch to Mode B if the user confirms they want scroll-based, or if the content is clearly a long-form report/portfolio piece.

Recommend and confirm one of these three modes before building:

### Mode A: Slide Deck
Classic slides, keyboard/click navigation (← → arrow keys, space bar). Best for live presentations.
- Each slide fills the screen
- Content enters with animated reveals (staggered text, charts that draw in, images that fade)
- Smooth slide-to-slide transitions
- Optional: presenter notes, progress bar, slide counter

### Mode B: Scroll Story
User scrolls down to advance through the narrative. Best for async sharing, reports, one-pagers.
- Each section locks into view as you scroll (scroll-jacking or smooth scroll)
- Content animates in as it enters the viewport
- Feels like an interactive article or annual report
- No navigation UI — scrolling IS the interaction

> **Note:** Do NOT use `scaleToViewport()` for scroll stories — they are full-page documents, not fixed-canvas slides. Viewport scaling is only for Mode A and Mode C.

**HTML structure:**
```html
<div class="scroll-story">
  <section class="story-section" id="section-1">
    <div class="section-content">
      <!-- slide-equivalent content goes here -->
      <!-- add class="reveal" to elements you want to animate in -->
      <div class="stagger-group">
        <h2 class="reveal">Headline</h2>
        <p class="reveal">Supporting text</p>
      </div>
    </div>
  </section>
  <!-- repeat per section -->
</div>
```

**Required CSS:**
```css
/* Full-page snap scrolling — each scroll lands on a complete section */
html {
  scroll-snap-type: y mandatory;
  overflow-y: scroll;
  height: 100%;
}

body {
  margin: 0;
  height: 100%;
  background: var(--bg);
}

.story-section {
  height: 100vh;               /* exact — snap requires fixed height, not min-height */
  overflow: hidden;            /* clip content that exceeds one screen */
  scroll-snap-align: start;
  scroll-snap-stop: always;    /* prevents fast-scroll from skipping sections */
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 5rem;               /* rem — scales with root font size scaler below */
  position: relative;
  box-sizing: border-box;
}

.section-content {
  max-width: 60rem;            /* rem — scales with root font size scaler below */
  width: 100%;
}

/* Elements start invisible — ScrollTrigger reveals them on scroll */
.reveal {
  opacity: 0;
  transform: translateY(28px);
}
```

> **scroll-snap-stop: always** is what makes "one section per scroll" work. Without it, a fast trackpad swipe can skip sections entirely. With it, every scroll gesture lands on exactly the next section — no exceptions.

**Viewport-proportional scaling — REQUIRED for scroll stories:**

Scroll stories cannot use `scaleToViewport()` (that's for fixed-canvas slide mode only). Instead, use a **root font size scaler**: a small JS snippet sets `html { font-size }` proportional to viewport width. All layout values then use `rem`, so the entire layout — headings, body text, padding, column width — scales together as the viewport grows, exactly like `scaleToViewport()` does for slide mode.

**Required JS (add near the top of your script block, before GSAP init):**
```javascript
// === SCROLL STORY SCALING ===
// Scales the entire layout by adjusting the root font size.
// All rem-based values (fonts, padding, max-width) grow proportionally.
// Reference: 1rem = 16px at a 1280px-wide viewport.
const STORY_REF_WIDTH = 1280;

function scaleStoryLayout() {
  const scale = Math.min(Math.max(window.innerWidth / STORY_REF_WIDTH, 0.5), 2.5);
  document.documentElement.style.fontSize = (16 * scale) + 'px';
}

window.addEventListener('resize', scaleStoryLayout);
scaleStoryLayout(); // run on load
```

**Required CSS for typography (all in rem — scales automatically):**
```css
.story-section h1   { font-size: 3.5rem;  line-height: 1.15; }
.story-section h2   { font-size: 2.5rem;  line-height: 1.25; }
.story-section h3   { font-size: 1.75rem; line-height: 1.35; }
.story-section p,
.story-section li   { font-size: 1.1rem;  line-height: 1.75; }
.story-section .stat  { font-size: 6rem;  font-weight: 700; }
.story-section .label { font-size: 0.75rem; letter-spacing: 0.12em; text-transform: uppercase; }
```

> **Why root font size instead of clamp():** `clamp()` only scales font sizes, but the content column width (`max-width`) and padding stay fixed in `px` — so on a 2560px projector screen, you get bigger text inside the same 960px box. Root font scaling moves the entire layout together: fonts, padding, and column width all scale as one unit, giving the same proportional feel as `scaleToViewport()` on slide mode. The `Math.min(..., 2.5)` cap prevents runaway scaling on ultra-wide displays; `Math.max(..., 0.5)` keeps it readable on small screens.

**Reveal animation setup — use IntersectionObserver, NOT ScrollTrigger:**

With CSS snap scrolling, sections jump into view rather than scrolling progressively through intermediate positions. ScrollTrigger's position-based triggers (`start: 'top 82%'`) can miss the snap moment entirely. Use IntersectionObserver instead — it fires when a section becomes visible regardless of how it got there (snap scroll, dot nav click, keyboard).

```javascript
// Observe each section — when it snaps into view, animate its .reveal elements
const revealObserver = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (!entry.isIntersecting) return;
    const section = entry.target;

    // Individual .reveal elements (not inside a stagger-group)
    const singles = [...section.querySelectorAll('.reveal')]
      .filter(el => !el.closest('.stagger-group'));
    gsap.to(singles, { opacity: 1, y: 0, duration: 0.7, ease: 'power2.out' });

    // Stagger groups — children animate in sequence
    section.querySelectorAll('.stagger-group').forEach(group => {
      gsap.to(group.querySelectorAll('.reveal'), {
        opacity: 1, y: 0, duration: 0.6, stagger: 0.12, ease: 'power2.out'
      });
    });

    revealObserver.unobserve(section); // animate once per section
  });
}, { threshold: 0.4 }); // fires when 40% of the section is visible

document.querySelectorAll('.story-section').forEach(s => revealObserver.observe(s));
```

**Reading progress bar (always include for scroll stories):**
```html
<div class="progress-bar" id="progressBar"></div>
```
```css
.progress-bar {
  position: fixed;
  top: 0; left: 0;
  height: 2px;
  width: 0%;
  background: var(--accent);
  z-index: 1000;
  transition: width 0.08s linear;
}
```
```javascript
window.addEventListener('scroll', () => {
  const scrolled = window.scrollY;
  const maxScroll = document.body.scrollHeight - window.innerHeight;
  document.getElementById('progressBar').style.width =
    Math.min((scrolled / maxScroll) * 100, 100) + '%';
}, { passive: true });
```

**Vertical section-dot nav (recommended for stories with 5+ sections):**
```html
<nav class="section-nav" id="sectionNav" aria-label="Section navigation"></nav>
```
```css
.section-nav {
  position: fixed;
  right: 28px;
  top: 50%;
  transform: translateY(-50%);
  display: flex;
  flex-direction: column;
  gap: 10px;
  z-index: 100;
}
.section-nav .dot {
  width: 7px; height: 7px;
  border-radius: 50%;
  background: var(--text-secondary);
  opacity: 0.3;
  cursor: pointer;
  border: none;
  padding: 0;
  transition: all 0.3s;
}
.section-nav .dot.active {
  background: var(--accent);
  opacity: 1;
  transform: scale(1.4);
}
```
```javascript
// Build section dots and highlight active section via IntersectionObserver
const sections = document.querySelectorAll('.story-section');
const nav = document.getElementById('sectionNav');

sections.forEach((sec, i) => {
  const dot = document.createElement('button');
  dot.className = 'dot' + (i === 0 ? ' active' : '');
  dot.setAttribute('aria-label', `Go to section ${i + 1}`);
  dot.addEventListener('click', () => sec.scrollIntoView({ behavior: 'smooth' }));
  nav.appendChild(dot);
});

const sectionObserver = new IntersectionObserver((entries) => {
  entries.forEach(e => {
    if (e.isIntersecting) {
      const i = [...sections].indexOf(e.target);
      document.querySelectorAll('.section-nav .dot')
        .forEach((d, j) => d.classList.toggle('active', j === i));
    }
  });
}, { threshold: 0.5 });

sections.forEach(s => sectionObserver.observe(s));
```

### Mode C: Interactive Deck
Slide-based but with embedded interactions. Best for training, demos, proposals with choices.
- Quizzes with scoring
- Expandable detail panels ("click to learn more")
- Branching paths ("choose your scenario")
- Embedded calculators or configurators
- Data filters / toggles

---

## Phase 4: Build

### Technical approach

Build a **single self-contained HTML file** that works in any modern browser without a server.

**Libraries (load via CDN — fast and reliable):**
- **GSAP** + **ScrollTrigger**: all animations. Don't use CSS animations for anything complex.
- **Chart.js**: data visualization when needed (charts, graphs)
- **Google Fonts**: always load from the chosen preset in `STYLE_PRESETS.md` — never default to Inter, Roboto, or Arial.

```html
<!-- CDN imports -->
<script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/gsap.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/ScrollTrigger.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
```

**CSS variables:** Copy the full `:root {}` block from the chosen preset in `STYLE_PRESETS.md` and use these variables throughout. Never hardcode colors or fonts inline — use `var(--accent)`, `var(--font-display)`, etc. This makes style iteration instant.

**File structure (all inline in one .html):**
```
<head>  — Google Fonts, all CSS
<body>  — slide/section markup
<script> — GSAP animations, navigation logic
```

### Viewport scaling — REQUIRED for slide modes (Mode A and C)

**This is the most common production bug.** Without this, text looks fine in a normal browser window but becomes tiny when fullscreened or shown on a projector.

The fix: author all slides at a fixed canvas size (1280×720), then scale the entire canvas as a unit to fill the viewport. Font sizes and padding stay consistent because they all move together.

**Required CSS structure:**
```css
body {
  margin: 0;
  overflow: hidden;
  background: #000; /* letterbox — change to match --bg if you want no bars */
}

.slides-wrapper {
  position: fixed;
  width: 1280px;
  height: 720px;
  overflow: hidden;
  /* JS sets: transform, left, top */
}

.slide {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
}
```

**Required JS (add near the top of your script block):**
```javascript
// === VIEWPORT SCALING ===
// Keeps slides full-size at any resolution, including fullscreen (F11).
// Author all content at 1280×720 — the browser scales it as a unit.
const SLIDE_W = 1280;
const SLIDE_H = 720;
const slidesWrapper = document.querySelector('.slides-wrapper');

function scaleToViewport() {
  const scaleX = window.innerWidth / SLIDE_W;
  const scaleY = window.innerHeight / SLIDE_H;
  const scale = Math.min(scaleX, scaleY);
  const offsetX = (window.innerWidth - SLIDE_W * scale) / 2;
  const offsetY = (window.innerHeight - SLIDE_H * scale) / 2;
  slidesWrapper.style.transform = `scale(${scale})`;
  slidesWrapper.style.transformOrigin = '0 0';
  slidesWrapper.style.left = offsetX + 'px';
  slidesWrapper.style.top = offsetY + 'px';
}

window.addEventListener('resize', scaleToViewport);
document.addEventListener('fullscreenchange', scaleToViewport);
scaleToViewport(); // run on load
```

> **What this does:** At 1280×720 viewport, scale = 1.0 (no change). At 2560×1440, scale = 2.0 (everything doubles). When F11 fullscreen fires, `resize` triggers the recalculation automatically. The result looks identical at any resolution.

---

### Design principles (borrow from frontend-design skill)

- **Style communicates credibility before the first word is read.** The visual preset is not a neutral aesthetic choice — it's a trust signal. Match it to the audience's expectations and the objective of the presentation. Executive/board review → authoritative and restrained (Executive Dark, Swiss Grid). Startup pitch → fluid and optimistic (Aurora). Technical deep-dive → precise and data-forward (Swiss Grid, Neon Noir). Consumer launch → warm and approachable (Studio Soft, Warm Magazine). A mismatch in visual register undermines the content no matter how strong the words are.
- **Pick a bold visual direction and commit.** Don't hedge. Minimal and precise or maximal and expressive — both work. Half-measures don't.
- **Typography matters more than anything.** Pair a distinctive display font with a clean body font. The headline font should have personality. Make the type hierarchy obvious and deliberate.
- **Color with purpose.** One dominant color (60-70% visual weight), one supporting tone, one sharp accent. Never equal weights. Match the palette to the content's emotional register.
- **Every slide needs a visual anchor** — a large stat, an icon cluster, an image, a chart. Pure text slides are forgettable.
- **Animate with restraint.** A few well-timed animations beat a dozen random ones. The first slide entrance should feel polished. Transitions should feel smooth, not showy.
- **Negative space is a design tool.** Don't fill every pixel.
- **Comment your code.** The HTML file will be opened and edited by non-engineers. Add section comments (`<!-- SLIDE 3: Problem -->`) and brief JS comments explaining the navigation logic. Comments are kindness to future-you.

### Slide layout patterns

| Pattern | Use when |
|--------|----------|
| **Full-bleed hero** | Title slide, section breaks |
| **Split (content left, visual right)** | Text + image, stat + explanation |
| **Large stat callout** | Key numbers, percentages, metrics |
| **Icon grid (2×2 or 3×3)** | Features, principles, categories |
| **Timeline / process flow** | Steps, phases, history |
| **Comparison columns** | Before/after, options, pros/cons |
| **Quote / testimonial** | Social proof, key statement |
| **Chart + insight** | Data slide with the "so what?" |

### Navigation (for slide modes)

Always include all four input methods — users navigate however feels natural to them.

```javascript
// 1. Keyboard
document.addEventListener('keydown', (e) => {
  if (e.key === 'ArrowRight' || e.key === ' ') nextSlide();
  if (e.key === 'ArrowLeft') prevSlide();
});

// 2. Click zones (left half = back, right half = forward)
document.addEventListener('click', (e) => {
  // Ignore clicks on interactive elements
  if (e.target.closest('button, a, input, [data-no-nav]')) return;
  if (e.clientX > window.innerWidth / 2) nextSlide();
  else prevSlide();
});

// 3. Touch / swipe
let touchStartX = 0;
document.addEventListener('touchstart', (e) => { touchStartX = e.touches[0].clientX; }, { passive: true });
document.addEventListener('touchend', (e) => {
  const delta = touchStartX - e.changedTouches[0].clientX;
  if (Math.abs(delta) > 50) delta > 0 ? nextSlide() : prevSlide();
}, { passive: true });

// 4. Mouse wheel
let wheelCooldown = false;
document.addEventListener('wheel', (e) => {
  if (wheelCooldown) return;
  wheelCooldown = true;
  setTimeout(() => wheelCooldown = false, 800);
  e.deltaY > 0 ? nextSlide() : prevSlide();
}, { passive: true });
```

**Navigation dots** — include a visual dot indicator:
```html
<!-- In your HTML, after the slides -->
<nav class="slide-dots" aria-label="Slide navigation">
  <!-- Generated by JS: one dot per slide -->
</nav>
```
```css
.slide-dots {
  position: fixed; bottom: 24px; left: 50%; transform: translateX(-50%);
  display: flex; gap: 8px; z-index: 100;
}
.dot {
  width: 8px; height: 8px; border-radius: 50%;
  background: var(--text-secondary); opacity: 0.4;
  cursor: pointer; transition: all 0.3s;
  border: none; padding: 0;
}
.dot.active { background: var(--accent); opacity: 1; transform: scale(1.3); }
```
```javascript
// Build dots dynamically
function buildDots() {
  const nav = document.querySelector('.slide-dots');
  slides.forEach((_, i) => {
    const dot = document.createElement('button');
    dot.className = 'dot' + (i === 0 ? ' active' : '');
    dot.setAttribute('aria-label', `Go to slide ${i + 1}`);
    dot.addEventListener('click', (e) => { e.stopPropagation(); goToSlide(i); });
    nav.appendChild(dot);
  });
}
// Update on slide change
function updateDots(index) {
  document.querySelectorAll('.dot').forEach((d, i) => d.classList.toggle('active', i === index));
}
```

### Accessibility

- Keyboard navigation always included
- `aria-label` on navigation elements
- Sufficient color contrast (WCAG AA)
- `prefers-reduced-motion` respected:

```css
@media (prefers-reduced-motion: reduce) {
  * { animation-duration: 0.01ms !important; transition-duration: 0.01ms !important; }
}
```

---

## Phase 5: Preview & Iterate

After building, open the file in the browser and describe what you made — the visual direction, the flow, the number of slides, and what interactive elements are included.

Tell the user:
- What file to open (its path)
- What to click/press to navigate
- What the key design choices were and why

Then ask: "What would you like to adjust?" Be ready to iterate on:
- Content (add/remove/rewrite slides)
- Style (colors, fonts, layout)
- Animations (more/less/different)
- Interactivity (add a quiz, add chart, add branching)

### Publishing to GitHub Pages (free hosting)

**Always output the file as `index.html`.** This is the required filename for GitHub Pages to serve it automatically.

After the user approves the presentation, offer these hosting instructions:

> **To publish free on GitHub Pages:**
> 1. Create a new GitHub repo (e.g., `my-presentation`) — or use an existing one
> 2. Add `index.html` to the root of the repo (or a `docs/` subfolder if other files are present)
> 3. Go to **Settings → Pages → Source** → select branch `main` and folder `/` (root) → click **Save**
> 4. In ~60 seconds your presentation will be live at: `https://yourusername.github.io/my-presentation/`
>
> **If the repo already has content**, put `index.html` in a `docs/` folder and set Pages source to `/docs` instead.

The presentation is a single self-contained HTML file, so it needs no build step, no server, and no dependencies — it works perfectly on GitHub Pages out of the box.

---

## Phase 6: PPT Export

Offer this **after Phase 5** once the HTML is approved. Say: *"Would you like an editable .pptx version? All text will be directly editable in PowerPoint."*

Also trigger this phase if the user asks at any point how to edit text, or requests a PowerPoint file.

### How to generate

1. Create `build-deck.js` in the same directory as `index.html`
2. Recreate each slide's content using pptxgenjs — translate HTML layout → pptxgenjs API calls
3. Map CSS variables from the chosen preset → pptxgenjs hex constants (strip the `#`)
4. Use PowerPoint-safe fonts (see mapping table below)
5. Run: `NODE_PATH=$(npm root -g) node build-deck.js`
6. Output: `[name].pptx` in the same directory

### Font mapping (HTML preset → PowerPoint)

| HTML preset font | PowerPoint equivalent |
|---|---|
| Plus Jakarta Sans, Syne, Barlow, Nunito, DM Sans | Calibri |
| Cormorant Garamond, Playfair Display, Libre Baskerville | Georgia |
| IBM Plex Mono, JetBrains Mono, Space Mono | Courier New |
| Source Serif 4 | Georgia |

### pptxgenjs rules (follow strictly — violations corrupt files or cause silent bugs)

- **NEVER prefix hex colors with `#`** — `"6C47FF"` not `"#6C47FF"` — causes file corruption
- **NEVER encode opacity in hex** — don't use 8-char hex like `"6C47FF80"`. Use `opacity: 0.5` instead
- **Always use a shadow factory function** — pptxgenjs mutates objects in-place; never share a shadow config object across calls:
  ```javascript
  const mkShadow = () => ({ type: "outer", blur: 10, offset: 2, angle: 135, color: "000000", opacity: 0.1 });
  // Call mkShadow() fresh for every addShape that needs a shadow
  ```
- **Use `breakLine: true`** in rich text arrays for multi-line content
- **Use `margin: 0`** on text boxes that must align precisely with shapes or lines

### Applying brand to the PPT

If a brand kit was collected in Phase 1, apply it here:

**Colors + Fonts** — replace the color constants at the top of `build-deck.js` with the brand colors; set `fontFace` to the user's fonts (use the mapping table above if they're not PowerPoint-safe); add logo via `slide.addImage({ path: "logo.png", x: 0.3, y: 0.2, w: 1.2, h: 0.4 })` on every slide.

**PPT Template** — use the pptx skill's editing workflow (unpack → inject content → repack) instead of generating from scratch. This gives the highest-fidelity brand output — the result inherits the template's master styles, fonts, and layouts. Refer to the `pptx` skill's `editing.md`.

**No brand kit collected** — use the same color palette from the HTML preset, translated to hex constants.

### PPT export checklist

- [ ] Content matches HTML slides (same text, same structure, same slide count)
- [ ] Colors match the HTML preset or brand kit
- [ ] All slides have correct header (eyebrow label + slide number)
- [ ] Shadow factory function used — no shared shadow objects
- [ ] No `#` prefix on any hex color string
- [ ] All fonts are PowerPoint-compatible
- [ ] `NODE_PATH=$(npm root -g) node build-deck.js` runs without errors
- [ ] Open the `.pptx` and visually scan before delivering

---

## Quick reference: Avoid these mistakes

- **Don't skip Phase 1 discovery.** Always ask about audience, goal, and delivery before anything else. These answers change the mode, structure, emphasis, and closing — skipping them wastes everyone's time.
- **Don't jump from source doc straight to building.** When the input is a document or URL, produce a ghost list first, confirm it, then build.
- **Don't choose a visual style purely on aesthetics.** When selecting 3 presets for the style preview, pick options that match the audience's expectations and the objective — not just what looks nice. An executive reviewing a board deck expects restraint and precision. A startup pitch should feel energetic. A technical talk should feel structured. Style is a trust signal, not decoration.
- **Don't ask the user to describe their aesthetic in words.** Generate the style preview file and let them react to visuals.
- **Don't echo bullet points onto slides.** Transform the content, don't transcribe it.
- **Don't use Inter, Roboto, or Arial as display fonts.** Always use the fonts from the chosen preset in `STYLE_PRESETS.md`.
- **Don't hardcode colors.** Use CSS variables from the preset throughout — it makes switching styles trivial.
- **Don't animate everything.** 3-5 well-timed animations per presentation beat 30 distracting ones.
- **Don't use purple gradients on white backgrounds.** This is the hallmark of generic AI output.
- **Don't forget the "so what?" on data slides.** A chart without an insight caption is incomplete.
- **Don't skip navigation.** Always include keyboard, click, touch, swipe, and wheel support. Navigation dots too.
- **Don't ship uncommented code.** Add slide section comments and brief JS explanations — the user will edit this file.
- **Don't forget viewport scaling.** Always include `scaleToViewport()` for slide modes — without it, text looks tiny on fullscreen/projectors.
- **Always output as `index.html`.** GitHub Pages requires this filename to serve the file automatically at the root URL.
- **After HTML approval, proactively offer the PPT export.** Don't wait for the user to ask — say "Would you like an editable .pptx version too?"
- **For PPT export, never use `#` in hex colors and never share shadow config objects.** Both silently corrupt the output. Always use a shadow factory: `const mkShadow = () => ({ ... })`.
- **For brand kits, don't overcomplicate it.** You don't need API access or OAuth. Accept hex colors + font names, a logo file, or a .pptx template — any one of these is enough to apply a brand. Guide the user to export from Canva as .pptx if they have a Canva template.
