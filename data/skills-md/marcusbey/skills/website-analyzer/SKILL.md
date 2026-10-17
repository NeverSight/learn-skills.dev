---
name: website-analyzer
description: >
  Use when analyzing, exploring, deconstructing, or reverse-engineering a website.
  Triggers on: "analyze this site", "how does this work", "deep dive", "full spec",
  "recreate this", or when user shares a URL asking about animations, scroll effects,
  or composition techniques.
---

# SKILL: Deep Website Analyzer

## TRIGGER
Use this skill when the user asks to:
- "analyze this website"
- "explore this URL"
- "create a spec for [url]"
- "deconstruct this site"
- "recreate this website"
- "what animations/effects does [url] use"
- "how is [url] built"

---

## CORE PHILOSOPHY: THE PAINTING METAPHOR

**Premium sites are NOT a stack of independent viewport-height sections.**
They are a **continuous composition** — like a large painting — where:

1. **Elements begin in one section and complete in another** (a photo that starts small in section A becomes full-bleed in section B)
2. **Typography overlaps section boundaries** (text introduced as ghost/faded in one fold becomes solid as you scroll into the next)
3. **Sticky/pinned elements act as anchors** that other content scrolls past (a portrait stays fixed while text panels scroll alongside it)
4. **Background transitions aren't section changes** — they're mood shifts in a continuous narrative
5. **Cross-section elements create visual "threads"** that pull the eye forward through the page

This is the key distinction between a $500 template and a $50,000 build.

---

## EXECUTION PROCEDURE

### PHASE 0 — SETUP

```javascript
// Always start with these steps:
// 1. Get tab ID
// 2. Navigate to URL
// 3. Set viewport to 1440×900 (standard desktop)
// 4. Wait 4 seconds for all assets and animations to load
// 5. Take initial screenshot
```

```javascript
// Disable Lenis/smooth scroll so native scrollTo works:
if (window.lenis) window.lenis.stop();
if (window.locomotive) window.locomotive.stop();
// Override scroll libraries that block native scroll
document.documentElement.style.overflow = 'auto';
```

---

### PHASE 1 — STRUCTURAL RECONNAISSANCE

Run these JS probes to build the site map before any scrolling:

```javascript
// 1. Get total page height and all named sections
JSON.stringify(Array.from(document.body.children).map((el,i) => ({
  i,
  tag: el.tagName,
  id: el.id || null,
  cls: (el.className||'').toString().substring(0,80),
  top: el.offsetTop,
  h: el.offsetHeight
})).filter(el => el.h > 50))
```

```javascript
// 2. Detect animation libraries
({
  gsap: typeof gsap !== 'undefined',
  lenis: typeof Lenis !== 'undefined' || !!window.lenis,
  locomotive: typeof LocomotiveScroll !== 'undefined',
  framerMotion: typeof window.__framer_importFromPackage !== 'undefined',
  aos: typeof AOS !== 'undefined',
  swiper: typeof Swiper !== 'undefined',
  three: typeof THREE !== 'undefined',
  scripts: Array.from(document.scripts).map(s => s.src).filter(s => s && !s.includes('chrome'))
})
```

```javascript
// 3. Extract full CSS design tokens
const root = document.documentElement;
const cs = window.getComputedStyle(root);
const tokenNames = ['--primary','--secondary','--accent','--bg','--text','--font-body',
  '--font-heading','--color-dark','--color-light','--white','--black','--radius'];
const tokens = {};
tokenNames.forEach(v => { const val = cs.getPropertyValue(v); if(val) tokens[v] = val; });
// Also get font faces
const fonts = Array.from(document.styleSheets).flatMap(s => {
  try { return Array.from(s.cssRules).filter(r => r instanceof CSSFontFaceRule).map(r => r.cssText); }
  catch(e) { return []; }
});
JSON.stringify({ tokens, fonts })
```

```javascript
// 4. Get ALL CSS rules (extract in chunks to avoid filter blocks)
const sheet = document.styleSheets[0];
let totalRules = 0;
try { totalRules = sheet.cssRules.length; } catch(e) {}
totalRules + ' rules in main stylesheet'
```

```javascript
// 5. Detect sticky/fixed/pinned elements — key for cross-viewport compositions
Array.from(document.querySelectorAll('*')).filter(el => {
  const cs = window.getComputedStyle(el);
  return cs.position === 'sticky' || cs.position === 'fixed';
}).map(el => ({
  tag: el.tagName,
  cls: (el.className||'').toString().substring(0,60),
  position: window.getComputedStyle(el).position,
  top: window.getComputedStyle(el).top,
  zIndex: window.getComputedStyle(el).zIndex
})).slice(0, 20)
```

---

### PHASE 2 — FULL SCROLL CAPTURE

**Strategy:** Scroll in increments of 40% of viewport height to catch all states.
Take a screenshot at EACH position. Do not skip increments.

```javascript
// Get scroll increment
Math.floor(window.innerHeight * 0.4)
```

For each scroll position:
1. `window.scrollTo(0, position)`
2. Wait 500ms for animations to settle
3. Take screenshot
4. Note what is visible and any elements crossing the fold boundary

**CRITICAL — At each screenshot, explicitly look for:**

#### A. CROSS-FOLD ELEMENTS (The Painting Technique)
- Is any element visible in BOTH the upper portion AND lower portion of the viewport?
- Is the same element that was visible in the PREVIOUS screenshot still visible here but in a different position/size/state?
- Are there elements that appear to "float" between sections (not clearly belonging to either)?

#### B. SECTION BOUNDARY CROSSINGS
- Does any photo, illustration, or graphic element bleed past the bottom of its parent section into the next?
- Is there text that begins faded/ghosted and becomes solid as you scroll?
- Are there elements that start partially off-screen and scroll INTO their final position?

#### C. BACKGROUND CONTINUITY
- Do sections share a continuous background or gradient that creates visual connection?
- Does a dark section transition feel like a lighting change rather than a block swap?
- Are there decorative elements (lines, curves, dots) that straddle the section border?

#### D. PINNED COMPOSITION LAYERS
- Is any large image (portrait, product, scene) staying fixed while text slides past it?
- Is there a multi-panel "slideshow" where the image is pinned and only the text changes?

---

### PHASE 3 — CROSS-VIEWPORT COMPOSITION DETECTION

This is the most important phase. Run these probes at different scroll positions:

```javascript
// Detect elements that span across the visible viewport fold (cross-boundary elements)
// Run this at multiple scroll positions
const vh = window.innerHeight;
const scrollY = window.scrollY;
const foldTop = scrollY;
const foldBottom = scrollY + vh;
const crossFold = Array.from(document.querySelectorAll('img, video, canvas, [class*="photo"], [class*="image"], [class*="portrait"], section, div'))
  .filter(el => {
    const rect = el.getBoundingClientRect();
    const elTop = rect.top + scrollY;
    const elBottom = rect.bottom + scrollY;
    // Element must START before current fold AND END after it (spanning at least 60% of viewport)
    return elTop < foldTop + (vh * 0.3) && elBottom > foldBottom - (vh * 0.3) && rect.height > vh * 0.5;
  })
  .map(el => ({
    tag: el.tagName,
    cls: (el.className||'').toString().substring(0,60),
    h: Math.round(el.getBoundingClientRect().height),
    top: Math.round(el.getBoundingClientRect().top),
    bottom: Math.round(el.getBoundingClientRect().bottom),
    position: window.getComputedStyle(el).position
  }));
JSON.stringify(crossFold.slice(0,10))
```

```javascript
// Detect scroll-driven transform animations (elements that change state on scroll)
// Look for GSAP ScrollTrigger instances
if (typeof ScrollTrigger !== 'undefined') {
  ScrollTrigger.getAll().map(st => ({
    trigger: st.trigger?.className?.substring(0,40),
    start: st.start,
    end: st.end,
    pin: !!st.pin,
    scrub: st.vars?.scrub,
    animation: st.animation ? st.animation.vars : null
  })).slice(0,20)
} else 'No ScrollTrigger detected'
```

```javascript
// Detect elements with scroll-driven opacity fades (ghost text entering from next section)
Array.from(document.querySelectorAll('*')).filter(el => {
  const cs = window.getComputedStyle(el);
  const opacity = parseFloat(cs.opacity);
  return opacity > 0 && opacity < 0.5 && el.offsetHeight > 20;
}).map(el => ({
  tag: el.tagName,
  cls: (el.className||'').toString().substring(0,50),
  text: (el.innerText||'').trim().substring(0,40),
  opacity: window.getComputedStyle(el).opacity,
  transform: window.getComputedStyle(el).transform
})).slice(0,10)
```

```javascript
// Detect clip-path animations (section reveal transitions)
Array.from(document.querySelectorAll('*')).filter(el => {
  const cs = window.getComputedStyle(el);
  return cs.clipPath !== 'none' && cs.clipPath !== '';
}).map(el => ({
  tag: el.tagName,
  cls: (el.className||'').toString().substring(0,60),
  clipPath: window.getComputedStyle(el).clipPath
})).slice(0,15)
```

---

### PHASE 4 — SECTION-BY-SECTION DEEP DIVE

For each major section detected in Phase 1:

```javascript
// Jump to section and fully characterize it
window.scrollTo(0, SECTION_TOP);

// Get section's full child structure
const el = document.querySelector('.SECTION_CLASS');
Array.from(el.querySelectorAll('*')).map(c => ({
  tag: c.tagName,
  cls: (c.className||'').toString().substring(0,60),
  text: (c.innerText||'').trim().substring(0,80),
  src: c.tagName === 'IMG' ? c.src.replace(window.location.origin,'') : null,
  href: c.tagName === 'A' ? c.getAttribute('href') : null,
  bg: window.getComputedStyle(c).backgroundImage.substring(0,80)
})).slice(0,40)
```

**For each section, document:**
- Background color / image
- All text content (headings, body, labels)
- All images (src paths)
- All interactive elements
- Entry animation (how does this section animate in?)
- Exit state (what is visible at the bottom of this section that bleeds into next?)
- **Cross-section relationship:** What element from this section appears in the NEXT section?

---

### PHASE 5 — INTERACTIVE STATE EXPLORATION

**Click every interactive element** and document state changes:

1. Navigation links / hamburger menus
2. CTA buttons (hover + click states)
3. Accordions / expandable sections
4. Tabs / filter controls
5. Carousels / sliders
6. Form inputs (focus states)
7. Any elements with `cursor: pointer`

```javascript
// Find all clickable elements
Array.from(document.querySelectorAll('button, a, [role="button"], [onclick], [data-popup], [data-modal]'))
  .map(el => ({
    tag: el.tagName,
    cls: (el.className||'').toString().substring(0,60),
    text: (el.innerText||'').trim().substring(0,40),
    href: el.getAttribute('href'),
    dataAttrs: Object.fromEntries([...el.attributes].filter(a => a.name.startsWith('data-')).map(a => [a.name, a.value]))
  })).slice(0,30)
```

For each interactive element:
- Screenshot before hover
- Screenshot during hover
- Screenshot after click / open state
- Document the animation (slide, fade, scale, clip-path expand?)

---

### PHASE 6 — MOBILE VIEWPORT

```javascript
// Resize to iPhone 14 Pro
// Width: 393, Height: 852
```

After resize:
1. Scroll full page again
2. Screenshot every major section
3. Note: What changes? What reflows? What disappears?
4. Document mobile navigation pattern
5. Check: Do cross-viewport compositions survive on mobile?

---

### PHASE 7 — CSS EXTRACTION

Extract all CSS in chunks (avoid security filters by splitting):

```javascript
const sheet = document.styleSheets[0];
const rules = [];
for (let i = 0; i < sheet.cssRules.length; i++) {
  rules.push(sheet.cssRules[i].cssText);
}
// Extract in batches of 50 rules at a time
rules.slice(0, 50).join('\n')
// Continue: rules.slice(50, 100).join('\n') etc.
```

**Always extract these specifically:**
- All `@keyframes` (complete code)
- All CSS custom properties (`:root { ... }`)
- All `@media` queries
- All `position: sticky` / `position: fixed` rules
- All `clip-path` rules
- All `transform` rules with `transition`

---

### PHASE 8 — ASSET INVENTORY

```javascript
// All images
Array.from(document.querySelectorAll('img, [style*="background-image"]')).map(el => ({
  tag: el.tagName,
  src: el.src ? el.src.replace(window.location.origin,'') :
       (el.style.backgroundImage || window.getComputedStyle(el).backgroundImage)
})).filter(el => el.src && el.src !== 'none')
```

```javascript
// All video sources
Array.from(document.querySelectorAll('video, source')).map(el => ({
  tag: el.tagName,
  src: el.src || el.getAttribute('src'),
  type: el.type
}))
```

```javascript
// All fonts
performance.getEntriesByType('resource')
  .filter(r => r.initiatorType === 'css' || r.name.includes('.woff') || r.name.includes('.ttf') || r.name.includes('.otf'))
  .map(r => r.name.replace(window.location.origin,''))
```

---

## OUTPUT FORMAT

The analysis output must be organized as follows:

### 1. OVERVIEW
- URL, title, page height
- Tech stack (libraries, CMS if detectable)
- Color palette + typography system
- Emotional arc / brand character

### 2. THE PAINTING MAP
**This is the most important section.**
A narrative description of how the page flows as a continuous composition:

> "The page opens with [describe first impression]. As you scroll, [element X] transitions from [state A] to [state B], creating a thread into the next section. The [photo/type/element] that begins [ghosted/small/partial] at the bottom of Section 2 becomes the dominant hero of Section 3 — this is the core compositional technique repeated N times throughout."

For each cross-viewport transition:
```
TRANSITION: Section [A] → Section [B]
Element: [description]
Entry state: [size/opacity/position at bottom of A]
Exit state: [size/opacity/position at top of B]
Technique: [pin | parallax | clip-path | opacity-fade | scale | none]
```

### 3. SECTION MAP (table)
Same as our TTN format — section name, scroll range, height, background, pin duration

### 4. EACH SECTION — DETAILED
- Visual composition (not just "left photo right text" but HOW they relate)
- Typography with exact values
- All assets
- Entry animation
- Exit bleed into next section

### 5. INTERACTIONS
- All clickable states
- All hover states
- All open/close animations

### 6. ANIMATION CATALOG
- All @keyframes
- All GSAP timelines (if accessible)
- All scroll-scrubbed animations

### 7. MOBILE DIFFERENCES

### 8. COMPLETE ASSET INDEX

---

## REFERENCE DOCUMENTS

For detailed guidance on specific aspects of the analysis, read these references:

- **For pattern identification** → read `references/pattern-library.md`
  Composition patterns A through J (Pinned Portrait, Gravity Cross, Ghost Reveal, Background Mood Shift, Breaking Type, Continuous Persona, Scroll-Assembled Scene, Viewport-Sized Typography, Logo-Building Transition, Sticky-Scrolled Thumbnail Navigator) plus the Premium Quality Signals Checklist.

- **For output template** → read `references/output-template.md`
  Complete example output structure showing the full spec format with all sections, tables, and scoring rubrics.

- **For personality & non-negotiables assessment** → read `references/personality-assessment.md`
  Phase 4 personality signal detection (4A–4G: page transitions, tab title, keyboard easter eggs, canvas analysis, ghost wordmarks, text selection color, personality checklist) plus Phase 5 non-negotiables assessment (10-principle grading rubric).

---

## TIPS FOR CATCHING EVERYTHING

1. **Always scroll very slowly** — premium effects are tuned to specific scroll ranges. Big jumps miss intermediate states.

2. **Hover over everything** — premium sites have hover states on elements you wouldn't expect (headings, images, decorative elements). Move the cursor across the ASCII art. Hover the logo. Hover section headings.

3. **Watch the browser tab** — does the title change? Premium studios program it to respond on hover, idle, and return from another tab.

4. **Press keys** — `C`, `G`, `⌘G`, `D`, `T`, `?`. Watch for visual changes. Easter eggs live in keyboard handlers.

5. **Watch the fold boundary** — the most important compositional decisions happen at the very bottom of each viewport. Screenshot at Y = section_bottom - 100px to catch the bleed.

6. **Run cross-fold detection at EVERY section boundary** — not just at the start.

7. **Check z-index layers** — premium compositions rely heavily on layering. Run:
   ```javascript
   Array.from(document.querySelectorAll('*'))
     .filter(el => parseInt(window.getComputedStyle(el).zIndex) > 0)
     .map(el => ({cls: (el.className||'').substring(0,40), z: window.getComputedStyle(el).zIndex, pos: window.getComputedStyle(el).position}))
   ```

8. **Look for `overflow: hidden` on parents** — this is how cross-section reveals are masked. The element is technically larger than its container; the mask creates the "entry" effect.

9. **Test resize behavior at 1240px, 768px, 480px** — premium sites reconceive layout at each breakpoint rather than just stacking.

10. **Check for `will-change`** — it signals which elements are animated and hints at the animation type.

11. **Read the inline `<style>` tags** — frequently premium sites put one-off section-specific styles inline.

12. **For multi-page sites**, navigate between pages and immediately screenshot — the transition is often the most impressive animation on the site.

13. **Highlight some text on the page** — does the selection color match the brand? Custom `::selection` is a mark of obsessive craft.

14. **Scroll to the footer and read every element** — keyboard shortcuts, ghost wordmarks, ASCII art fragments, and easter eggs live in footers. Read the tiny monospace text.

15. **Check `document.title` in the console** — then hover a button and check again. Personality lives in the tab strip.
