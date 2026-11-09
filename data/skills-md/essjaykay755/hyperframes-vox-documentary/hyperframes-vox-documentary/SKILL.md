---
name: hyperframes-vox-documentary
description: Master skill for building cinematic, stop-motion, documentary-style videos in HyperFrames (Vox aesthetic). Enforces strict rules for stepped GSAP timelines, SVG noise seed animation, boiling displacement filters, analog palettes, and brutalist typography.
---

# HyperFrames Vox-Style Documentary Skill

This skill provides architectural and aesthetic instructions for building high-end, editorial-style explainer videos (similar to Vox, Johnny Harris, or Cleo Abram) using **HyperFrames** (HTML + CSS + GSAP).

## Core Philosophy

Editorial documentaries rely on **physical imperfection**. We achieve this in code using three core pillars:

1.  **Stepped Motion Physics**: Forcing GSAP tweens to render in stepped intervals (emulating 7.5fps stop-motion) rather than smooth digital tweens.
2.  **The Boil (SVG Jitter)**: An animated SVG displacement map whose noise seed updates in steps, causing borders and lines to wobble organically.
3.  **Analog Texture & Grid Systems**: Brutalist borders, monospaced data tags, and global film grain with animated seeds.

---

## 1. The Stepped Motion Engine (GSAP)

**Never use smooth default eases (like `"power2.out"`) for layouts.** Smooth sliding breaks the analog stop-motion illusion.
Instead, you MUST configure GSAP tweens to use stepped easing functions.

```javascript
// ❌ BAD: Smooth, digital, generic easing.
tl.fromTo(".paper-card", { y: 300 }, { y: 0, duration: 0.6, ease: "power2.out" }, 1.2);

// ✅ GOOD: Stepped easing emulating a 7.5fps movement sequence (approx 5 steps in 0.6s)
tl.fromTo(".paper-card", { y: 300 }, { y: 0, duration: 0.6, ease: "steps(5)" }, 1.2);
```

For slower animations (e.g. a 2.0s paper drift), increase the steps proportionally (approx 7.5 steps per second):
```javascript
// Stepped hold/drift over 2 seconds:
tl.fromTo(".paper-card", { rotation: -3 }, { rotation: 2, duration: 2.0, ease: "steps(15)" }, 1.8);
```

---

## 2. The Boiling Jitter Filter

To emulate hand-drawn lines or stop-motion paper cutouts, elements must gently vibrate. 
Create this global SVG filter in your composition HTML (e.g. inside `main-graphics.html` root):

```html
<!-- Place at the root of the sub-composition -->
<svg style="position: absolute; width: 0; height: 0; pointer-events: none;">
  <defs>
    <filter id="jitter">
      <feTurbulence
        id="jitter-noise"
        type="fractalNoise"
        baseFrequency="0.035"
        numOctaves="2"
        result="noise"
        seed="0"
      />
      <feDisplacementMap
        in="SourceGraphic"
        in2="noise"
        scale="5"
        xChannelSelector="R"
        yChannelSelector="G"
      />
    </filter>
  </defs>
</svg>
```

### Animating the Boil Deterministically in GSAP

Animate the `seed` attribute of the turbulence filter in your GSAP timeline.
Since timelines must be seekable and deterministic, we animate the seed using a stepped ease over the entire composition duration:

```javascript
const duration = 15; // Total composition duration in seconds
const fpsStep = 7.5; // Stop-motion frame-rate
const totalSteps = Math.floor(duration * fpsStep);

// Animate the seed attribute of the turbulence element
tl.to("#jitter-noise", {
  attr: { seed: totalSteps },
  duration: duration,
  ease: `steps(${totalSteps})`
}, 0);
```

**Usage:** Apply `filter: url(#jitter);` in your CSS to any element, border, card, or text that should wobble.

---

## 3. Global Noise / Film Grain Overlay

Overlay a full-frame film grain div on top of all scenes:

```html
<!-- Absolute overlay at the end of the composition body -->
<div class="noise-overlay" class="clip" data-start="0" data-duration="15" data-track-index="99">
  <svg width="100%" height="100%" style="opacity: 0.12; pointer-events: none;">
    <filter id="grain-filter">
      <feTurbulence
        id="grain-noise"
        type="fractalNoise"
        baseFrequency="0.85"
        numOctaves="3"
        stitchTiles="stitch"
        seed="0"
      />
    </filter>
    <rect width="100%" height="100%" filter="url(#grain-filter)" />
  </svg>
</div>
```

```css
.noise-overlay {
  position: absolute;
  inset: 0;
  z-index: 9999;
  pointer-events: none;
  mix-blend-mode: multiply; /* Use mix-blend-mode: overlay for dark mode */
}
```

Animate the noise seed in GSAP to create flickering film grain:
```javascript
// Animate grain seed at double the speed of layout changes (~15fps)
const grainSteps = Math.floor(duration * 15);
tl.to("#grain-noise", {
  attr: { seed: grainSteps },
  duration: duration,
  ease: `steps(${grainSteps})`
}, 0);
```

---

## 4. Design Systems & Color Palettes

Declare these custom variables in your CSS root (`#main-graphics`):

### Palette A: Classic Sand (Warm Editorial)
```css
:root {
  --bg: #f4eedd;         /* Warm paper/sand background */
  --text: #1c1b18;       /* Charcoal/near-black */
  --box-bg: #ece5d3;     /* Slightly darker sand panels */
  --border: #1c1b18;     /* Thick charcoal borders */
  --accent-red: #d94838; /* Muted editorial red */
  --accent-navy: #1d3557;/* Deep navy blue */
  --accent-teal: #10a37f;/* Subtle pop teal */
}
```

### Palette B: Premium Dark Mode
```css
:root {
  --bg: #1c1b18;         /* Deep charcoal background */
  --text: #f4eedd;       /* Warm sand text */
  --box-bg: #2a2824;     /* Slightly lighter panel bg */
  --border: #ece5d3;     /* Warm sand borders */
  --accent-red: #e66050; /* Muted coral red */
  --accent-navy: #8ecae6;/* Soft pastel blue */
  --accent-teal: #10a37f;/* Vibrant pop teal */
}
```

---

## 5. Typography & Layout Rules

*   **View-Port Safety**: Elements must NEVER overflow the `1920x1080` screen bounds. Add explicit `padding` (e.g. `80px 120px`) to scene containers.
*   **No Unintentional Overlaps**: Layout elements static first. Use flex columns with explicit gaps (`gap: 32px;`) to guarantee borders and cards do not collide.
*   **Massive Typography Contrast**: Pair heavy display faces (e.g. `Oswald` or `Archivo Black` at `font-weight: 700/900`) with high-quality serif body text (e.g. `EB Garamond` at `font-weight: 400`).
    *   **Headline size**: `80px - 140px`
    *   **Body text**: `24px - 36px`
    *   **Data Labels / Code**: `18px - 22px` monospaced (`JetBrains Mono` or `Source Code Pro`).
*   **Brutalist Borders**: UI components must use thick solid borders (e.g. `border: 4px solid var(--border)`) and sharp corners (`border-radius: 0px` or `2px`).

---

## 6. Composition Techniques & Visual Metaphors

1.  **Cutouts & Snaps (Paper Animation)**:
    Animate elements in using `gsap.fromTo` with stepped eases. Move them onto the screen from off-frame, adding a subtle rotation to simulate paper being thrown onto a desk:
    ```javascript
    tl.fromTo(".document-card", 
      { y: 600, rotation: -12 }, 
      { y: 0, rotation: -2, duration: 0.5, ease: "steps(4)" },
      1.5
    );
    ```
2.  **Highlighter Box Effects**:
    Create an inline background span or SVG marker line. Animate its width to simulate a marker sweeping across words:
    ```html
    <span class="highlight-wrapper">
      <span class="highlight-bar"></span>
      <span class="highlight-text">key term</span>
    </span>
    ```
    ```css
    .highlight-wrapper { position: relative; display: inline-block; }
    .highlight-bar {
      position: absolute;
      left: 0; bottom: 4px;
      height: 70%; width: 0%;
      background: var(--accent-red);
      opacity: 0.35;
      z-index: 1;
    }
    ```
    ```javascript
    tl.to(".highlight-bar", { width: "100%", duration: 0.4, ease: "steps(3)" }, 2.0);
    ```
3.  **Stepped Typewriters**:
    Animate monospaced terminal logs using the GSAP `TextPlugin` or stepped clip-path reveals:
    ```javascript
    tl.fromTo(".terminal-text",
      { clipPath: "polygon(0 0, 0 0, 0 100%, 0% 100%)" },
      { clipPath: "polygon(0 0, 100% 0, 100% 100%, 0 100%)", duration: 1.0, ease: "steps(12)" },
      3.2
    );
    ```
4.  **Stepped Vector Drawing**:
    For technical blueprints, laptops, or connection grids, animate SVG paths in stepped intervals:
    ```javascript
    tl.fromTo(".blueprint-path",
      { strokeDashoffset: 1000 },
      { strokeDashoffset: 0, duration: 1.5, ease: "steps(10)" },
      4.0
    );
    ```
5.  **Shutter Flash Cuts**:
    Use a transition container to flash the screen:
    ```html
    <div id="flash-overlay" style="position: absolute; inset:0; background:white; opacity:0; z-index:9999;"></div>
    ```
    ```javascript
    // Flash white for 2 frames at t=6.0s
    tl.timeline()
      .set("#flash-overlay", { opacity: 1 }, 6.0)
      .set("#flash-overlay", { opacity: 0 }, 6.0 + (2 / 30));
    ```

---

## 7. Implementation Checklist

1.  [ ] Did you write all your GSAP tweens using `ease: "steps(N)"` (stop-motion movement)?
2.  [ ] Did you include the `#jitter` filter and animate its `seed` attribute inside the timeline?
3.  [ ] Did you add the `.noise-overlay` element and animate its seed at 15fps (`steps(15 * duration)`)?
4.  [ ] Are you strictly using CSS variables for Sand or Dark mode?
5.  [ ] Do UI cards and borders use thick strokes (4px) with sharp corners?
6.  [ ] Are headlines paired with serifs, and is data set in mono-spaced fonts?
7.  [ ] Did you verify all typography stays inside the title-safe margin (padding)?
