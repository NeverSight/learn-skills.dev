---
name: animejs
description: When writing JavaScript animations using anime.js v4, including DOM element animations, timelines, stagger effects, scroll-triggered animations, SVG animations, text animations, draggable elements, layout transitions, or any motion/transition effects on websites. Also use when the user says "animate," "animation library," "anime.js," "stagger," "timeline animation," "scroll animation," "text animation," "draggable," or "motion effects."
---

# anime.js v4 Animation

You are an expert in anime.js v4 (latest: v4.3.5), the lightweight JavaScript animation library. Generate production-ready animation code using the **v4 API exclusively**. Never use v3 syntax.

## CRITICAL: v4 API Only

anime.js v4 introduced breaking changes from v3. ALWAYS use v4 syntax:

| NEVER use (v3) | ALWAYS use (v4) |
|----------------|-----------------|
| `anime({ targets: '.el', ... })` | `animate('.el', { ... })` |
| `anime.timeline()` | `createTimeline()` |
| `anime.stagger()` | `stagger()` |
| `easing: 'easeOutQuad'` | `ease: 'outQuad'` |
| `begin: fn` | `onBegin: fn` |
| `change: fn` | `onUpdate: fn` |
| `complete: fn` | `onComplete: fn` |
| `direction: 'alternate'` | `alternate: true` |
| `direction: 'reverse'` | `reversed: true` |
| `endDelay` | `loopDelay` |
| `anime.path()` | `svg.createMotionPath()` |
| `anime.setDashoffset()` | `svg.createDrawable()` |
| `animation.finished.then()` | `animation.then()` |

---

## Installation & Setup

**CDN:**
```html
<script src="https://cdn.jsdelivr.net/npm/animejs@4/lib/anime.iife.min.js"></script>
```

**npm:**
```bash
npm install animejs
```

**ES Module imports (recommended):**
```js
import { animate, stagger, createTimeline } from 'animejs';
// Additional features — import only what you need:
import { createAnimatable } from 'animejs';
import { createDraggable } from 'animejs';
import { createLayout } from 'animejs';
import { onScroll } from 'animejs';
import { waapi } from 'animejs';
import { svg } from 'animejs';
import { splitText } from 'animejs';
import { engine, utils } from 'animejs';
```

**Subpath imports (tree-shaking):**
```js
import { animate } from 'animejs/animation';
import { createTimeline } from 'animejs/timeline';
import { createDraggable } from 'animejs/draggable';
import { onScroll } from 'animejs/events';
import { splitText } from 'animejs/text';
```

---

## Core: `animate(targets, parameters)`

### Targets

```js
// CSS selector
animate('.box', { ... });

// DOM element
animate(document.querySelector('#hero'), { ... });

// Multiple elements (NodeList, Array)
animate(document.querySelectorAll('.card'), { ... });

// JavaScript object (animate numeric properties)
const obj = { progress: 0 };
animate(obj, { progress: 100, onUpdate: () => console.log(obj.progress) });
```

### Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `duration` | number | 1000 | Milliseconds |
| `delay` | number/function | 0 | Delay before start |
| `ease` | string/function | `'outQuad'` | Easing function |
| `loop` | number/boolean | `false` | `true` = infinite, number = repeat count |
| `loopDelay` | number | 0 | Delay between loops |
| `alternate` | boolean | `false` | Reverse direction each loop |
| `reversed` | boolean | `false` | Play backwards |
| `autoplay` | boolean | `true` | Start immediately |
| `frameRate` | number | - | Limit FPS |
| `playbackRate` | number | 1 | Speed multiplier (2 = double speed) |
| `composition` | string | `'replace'` | `'replace'`, `'add'`, `'blend'` |
| `modifier` | function | - | Transform animated value before applying |

### Callbacks

```js
animate('.el', {
  translateX: 250,
  onBegin: (anim) => {},      // When animation starts (after delay)
  onUpdate: (anim) => {},     // Every frame
  onComplete: (anim) => {},   // When animation finishes
  onLoop: (anim) => {},       // After each loop iteration
  onPause: (anim) => {},      // When paused
}).then((anim) => {});         // Promise-based completion
```

### Playback Controls

```js
const anim = animate('.el', { translateX: 250, autoplay: false });

anim.play();        // Play forward
anim.pause();       // Pause
anim.resume();      // Resume from current position and direction
anim.reverse();     // Reverse direction
anim.restart();     // Restart from beginning
anim.seek(500);     // Jump to 500ms
anim.reset();       // Reset to initial values
anim.complete();    // Jump to end
anim.cancel();      // Cancel and clean up
anim.revert();      // Revert targets to original values
```

### Animatable Properties

```js
animate('.el', {
  // CSS transforms
  translateX: 250,
  translateY: 100,
  rotate: '1turn',
  scale: 1.5,
  skewX: '15deg',

  // CSS properties
  opacity: [0, 1],
  backgroundColor: '#FF0000',
  borderRadius: '50%',
  width: '200px',

  // CSS variables
  '--custom-prop': 100,

  // Relative values
  translateX: '+=100',
  rotate: '-=45deg',

  // From-to syntax
  opacity: { from: 0, to: 1 },
  translateY: [50, 0],          // [from, to]

  // Per-property parameters
  translateX: { to: 250, duration: 800, ease: 'outExpo' },
  opacity: { to: 1, duration: 400, delay: 200 },

  // Function-based values (per target)
  translateX: (target, index, total) => index * 50,
  delay: (target, index) => index * 100,
});
```

---

## Keyframes

**Property-level (array of values):**
```js
animate('.el', {
  translateX: [0, 100, 50, 200],
  duration: 2000,
});
```

**Property-level (array of objects):**
```js
animate('.el', {
  translateX: [
    { to: 100, duration: 500, ease: 'outQuad' },
    { to: 50, duration: 300 },
    { to: 200, duration: 700, ease: 'inOutCubic' },
  ],
});
```

**Percentage-based:**
```js
animate('.el', {
  keyframes: {
    '0%':   { translateX: 0, opacity: 0 },
    '40%':  { translateX: 100, opacity: 1 },
    '100%': { translateX: 250, opacity: 0.5 },
  },
  duration: 2000,
});
```

---

## Stagger

Distribute values or delays across multiple targets.

```js
import { animate, stagger } from 'animejs';

// Basic delay stagger: each element starts 100ms after the previous
animate('.card', {
  opacity: [0, 1],
  translateY: [30, 0],
  delay: stagger(100),
  duration: 500,
  ease: 'outCubic',
});

// From center outward
animate('.item', { scale: [0, 1], delay: stagger(80, { from: 'center' }) });

// From edges inward
animate('.item', { scale: [0, 1], delay: stagger(80, { from: 'edges' }) });

// From specific index
animate('.item', { scale: [0, 1], delay: stagger(80, { from: 3 }) });

// Range distribution: values spread evenly between 0 and 200
animate('.item', { translateX: stagger([0, 200]) });

// Grid stagger (rows x cols)
animate('.grid-item', {
  scale: [0, 1],
  delay: stagger(50, { grid: [4, 6], from: 'center', axis: 'y' }),
});

// Eased stagger distribution
animate('.item', { opacity: [0, 1], delay: stagger(300, { ease: 'inOutQuad' }) });
```

---

## Timelines

Sequence and synchronize multiple animations.

```js
import { createTimeline, stagger } from 'animejs';

const tl = createTimeline({
  defaults: { duration: 600, ease: 'outQuad' },
});

// Animations chain sequentially by default
tl.add('.header', { opacity: [0, 1], translateY: [-30, 0] })
  .add('.subtitle', { opacity: [0, 1], translateY: [20, 0] }, '-=300')  // Overlap by 300ms
  .add('.cta-btn', { opacity: [0, 1], scale: [0.8, 1] }, '+=100')      // 100ms gap
  .add('.cards', {
    opacity: [0, 1],
    translateY: [40, 0],
    delay: stagger(80),
  }, '-=200');

// Absolute positioning (ms from timeline start)
tl.add('.bg', { opacity: [0, 0.5] }, 0);  // Starts at 0ms

// Timeline controls
tl.play();
tl.pause();
tl.seek(1000);
tl.reverse();
tl.restart();
```

---

## Text Splitting

Split text into lines, words, or characters for per-element animation.

```js
import { splitText, animate, stagger } from 'animejs';

// Split heading into characters
const splitter = splitText('.hero-title', {
  chars: true,          // Split into characters
  // words: true,       // Split into words
  // lines: true,       // Split into lines
  accessible: true,     // Maintain screen reader accessibility
});

// Animate each character
animate(splitter.chars, {
  opacity: [0, 1],
  translateY: [20, 0],
  delay: stagger(30),
  duration: 400,
  ease: 'outCubic',
});

// Revert DOM to original text when done
// splitter.revert();
```

---

## Scroll Observer

Trigger and synchronize animations with scroll position.

```js
import { animate, onScroll } from 'animejs';

// Trigger animation when element enters viewport
onScroll('.section', {
  onEnter: () => {
    animate('.section .content', {
      opacity: [0, 1],
      translateY: [40, 0],
      duration: 800,
      ease: 'outQuad',
    });
  },
});

// Directional callbacks
onScroll('.element', {
  onEnterForward: () => {},    // Scrolling down into view
  onEnterBackward: () => {},   // Scrolling up into view
  onLeaveForward: () => {},    // Scrolling down out of view
  onLeaveBackward: () => {},   // Scrolling up out of view
});

// Sync animation progress to scroll position
const anim = animate('.parallax-bg', {
  translateY: [-100, 100],
  autoplay: false,
});

onScroll('.parallax-section', {
  sync: 'playback',    // Links scroll position to animation progress
  link: anim,
});

// Thresholds
onScroll('.el', {
  enter: 'top bottom',     // When top of el crosses bottom of viewport
  leave: 'bottom top',     // When bottom of el crosses top of viewport
});
```

---

## WAAPI (Web Animation API)

Lightweight 3KB alternative using browser-native Web Animation API. Hardware-accelerated. Use for simple animations where performance is critical.

```js
import { waapi } from 'animejs';

const anim = waapi.animate('.el', {
  translateX: 250,
  opacity: [0, 1],
  duration: 600,
  ease: 'outQuad',
});
```

**When to use WAAPI vs full `animate()`:**
- WAAPI: Simple CSS transforms/opacity, high-performance needs, many simultaneous elements
- Full `animate()`: JS object animation, complex keyframes, `onUpdate` callback, modifier functions, SVG features

---

## Animatable

Reactive value animation — ideal for cursor tracking, interactive UIs, and frequently changing values.

```js
import { createAnimatable } from 'animejs';

const follower = createAnimatable('.cursor-follower', {
  x: { duration: 300, ease: 'outQuad' },
  y: { duration: 300, ease: 'outQuad' },
});

document.addEventListener('mousemove', (e) => {
  follower.x(e.clientX);  // Setter: animates to value
  follower.y(e.clientY);
});

// Getter
const currentX = follower.x();
```

---

## Layout Animations

Animate layout changes that are normally impossible (CSS display, grid, flex, DOM order).

```js
import { createLayout } from 'animejs';

const layout = createLayout('.container', {
  duration: 500,
  ease: 'outQuad',
  // Enter/exit states for added/removed elements
  enterFrom: { opacity: 0, scale: 0.8 },
  leaveTo: { opacity: 0, scale: 0.8 },
});

// Animate any layout change
layout.update(() => {
  // Toggle class, change display, reorder DOM, etc.
  container.classList.toggle('grid-view');
});

// Or manual record → animate pattern
layout.record();
// ... make DOM changes ...
layout.animate();
```

---

## Draggable

Add drag interaction with physics.

```js
import { createDraggable } from 'animejs';

const draggable = createDraggable('.card', {
  x: { snap: 100 },                // Snap to 100px grid on x-axis
  y: { snap: 100 },
  friction: 0.5,                    // Drag friction
  mass: 1,                          // Physics mass
  stiffness: 100,                   // Spring stiffness
  damping: 10,                      // Spring damping
  onGrab: (self) => {},
  onDrag: (self) => {},
  onRelease: (self) => {},
  onSnap: (self) => {},
  onSettle: (self) => {},
});

// Constrain to container
const draggable = createDraggable('.el', {
  container: '.bounds',
  x: true,
  y: true,
});
```

---

## SVG Features

```js
import { animate, svg } from 'animejs';

// Line drawing (animate stroke)
const drawable = svg.createDrawable('.svg-path');
animate(drawable, { draw: [0, 1], duration: 1500, ease: 'inOutQuad' });

// Shape morphing
animate('.shape path', {
  d: svg.morphTo('.target-shape path'),
  duration: 1000,
  ease: 'inOutQuad',
});

// Motion path (move element along SVG path)
const motionPath = svg.createMotionPath('.motion-path');
animate('.moving-element', {
  ...motionPath,         // Spread the path data
  duration: 3000,
  ease: 'linear',
  loop: true,
});
```

---

## Easings

| Family | In | Out | InOut |
|--------|-----|------|-------|
| Quad | `inQuad` | `outQuad` | `inOutQuad` |
| Cubic | `inCubic` | `outCubic` | `inOutCubic` |
| Quart | `inQuart` | `outQuart` | `inOutQuart` |
| Quint | `inQuint` | `outQuint` | `inOutQuint` |
| Sine | `inSine` | `outSine` | `inOutSine` |
| Expo | `inExpo` | `outExpo` | `inOutExpo` |
| Circ | `inCirc` | `outCirc` | `inOutCirc` |
| Back | `inBack` | `outBack` | `inOutBack` |
| Elastic | `inElastic` | `outElastic` | `inOutElastic` |

**Custom easings:**
```js
ease: 'cubicBezier(0.25, 0.1, 0.25, 1.0)'   // CSS cubic-bezier
ease: 'spring(1, 100, 10, 0)'                 // spring(mass, stiffness, damping, velocity)
ease: 'steps(5)'                               // Stepped animation
ease: 'linear'                                 // Constant speed
```

**When to use which:**
- Entrances: `outQuad`, `outCubic`, `outExpo` (fast start, slow end)
- Exits: `inQuad`, `inCubic` (slow start, fast end)
- State changes: `inOutQuad`, `inOutCubic` (smooth both ends)
- Bouncy/playful: `outBack`, `outElastic`, `spring()`
- Continuous/looping: `linear`

For the complete easing catalog with motion descriptions and presets, see [references/easing-reference.md](references/easing-reference.md).

---

## Engine Configuration

```js
import { engine } from 'animejs';

engine.timeUnit = 'ms';          // 'ms' or 's'
engine.speed = 1;                // Global speed multiplier
engine.fps = 60;                 // Max frames per second
engine.precision = 4;            // Decimal precision
engine.pauseOnDocumentHidden = true;  // Pause when tab hidden
```

---

## Utilities

```js
import { utils } from 'animejs';

utils.get('.el', 'translateX');          // Get current value
utils.set('.el', { opacity: 0.5 });     // Set without animating
utils.random(0, 100);                   // Random number
utils.clamp(value, 0, 100);             // Clamp to range
utils.snap(value, 10);                  // Snap to nearest 10
utils.mapRange(value, 0, 1, 0, 100);    // Remap range
utils.lerp(start, end, 0.5);            // Linear interpolation
```

**Selector shorthand:**
```js
import { $ } from 'animejs';
const elements = $('.card');  // Like querySelectorAll
```

---

## Common Patterns

### Fade in on load
```js
animate('.element', {
  opacity: [0, 1],
  translateY: [20, 0],
  duration: 600,
  ease: 'outQuad',
});
```

### Staggered list entrance
```js
animate('.list-item', {
  opacity: [0, 1],
  translateY: [30, 0],
  delay: stagger(80),
  duration: 500,
  ease: 'outCubic',
});
```

### Hover scale effect
```js
document.querySelectorAll('.btn').forEach(btn => {
  btn.addEventListener('mouseenter', () =>
    animate(btn, { scale: 1.05, duration: 200, ease: 'outQuad' })
  );
  btn.addEventListener('mouseleave', () =>
    animate(btn, { scale: 1, duration: 200, ease: 'outQuad' })
  );
});
```

### Loading spinner
```js
animate('.spinner', {
  rotate: '1turn',
  duration: 800,
  loop: true,
  ease: 'linear',
});
```

### Animated counter
```js
const counter = { value: 0 };
animate(counter, {
  value: 2500,
  duration: 2000,
  ease: 'outExpo',
  onUpdate: () => {
    document.querySelector('.count').textContent = Math.round(counter.value);
  },
});
```

### Scroll-triggered reveal
```js
onScroll('.reveal-section', {
  onEnter: () => {
    animate('.reveal-section .item', {
      opacity: [0, 1],
      translateY: [40, 0],
      delay: stagger(100),
      duration: 600,
      ease: 'outCubic',
    });
  },
});
```

### Text reveal
```js
const splitter = splitText('.headline', { chars: true, accessible: true });
animate(splitter.chars, {
  opacity: [0, 1],
  translateY: [20, 0],
  delay: stagger(25),
  duration: 400,
  ease: 'outCubic',
});
```

### Draggable card
```js
createDraggable('.drag-card', {
  container: '.card-area',
  x: true,
  y: true,
  friction: 0.7,
  onRelease: (self) => {
    // Snap back or process drop
  },
});
```

For complete website animation patterns (hero sections, navigation effects, parallax, modals, carousels, etc.), see [references/website-animation-patterns.md](references/website-animation-patterns.md).

---

## v3 to v4 Complete Migration Reference

| v3 (NEVER use) | v4 (ALWAYS use) |
|----------------|-----------------|
| `anime({ targets: '.el', ... })` | `animate('.el', { ... })` |
| `anime.timeline({ ... })` | `createTimeline({ ... })` |
| `anime.stagger(100)` | `stagger(100)` |
| `easing: 'easeOutQuad'` | `ease: 'outQuad'` |
| `easing: 'easeInOutExpo'` | `ease: 'inOutExpo'` |
| `begin: fn` | `onBegin: fn` |
| `change: fn` | `onUpdate: fn` |
| `complete: fn` | `onComplete: fn` |
| `changeBegin: fn` | Removed — use `onBegin` |
| `changeComplete: fn` | Removed — use `onComplete` |
| `direction: 'alternate'` | `alternate: true` |
| `direction: 'reverse'` | `reversed: true` |
| `endDelay: 500` | `loopDelay: 500` |
| `anime.remove(targets)` | `anim.revert()` |
| `anime.path('.path')` | `svg.createMotionPath('.path')` |
| `anime.setDashoffset(el)` | `svg.createDrawable(el)` |
| `animation.finished.then(fn)` | `animation.then(fn)` |
| `value: 100` (in keyframe objects) | `to: 100` |
| `import anime from 'animejs'` | `import { animate } from 'animejs'` |
