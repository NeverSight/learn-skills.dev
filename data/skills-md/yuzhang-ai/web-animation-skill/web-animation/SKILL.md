---
name: web-animation
description: Web interactive animation best practices - choosing and using animation libraries for web UI effects
metadata:
  tags: animation, web, gsap, framer-motion, motion-one, animejs, rive, lottie, d3, three-js, canvas, css
---

## When to use

Use this skill whenever you need to create interactive web animations — page transitions, scroll effects, hover micro-interactions, data visualization motion, SVG morphing, or 3D web scenes.

This is NOT for video rendering (use Remotion for that). This is for real-time browser animations.

## Quick library picker

| Need | Use |
|------|-----|
| Scroll-triggered animations | GSAP + ScrollTrigger |
| React component enter/exit | Framer Motion |
| Lightweight, no framework | Motion One |
| SVG/CSS micro-animations | Anime.js |
| Interactive character animations | Rive |
| AE-exported JSON animations | Lottie |
| Data visualization motion | D3.js transitions |
| SVG shape morphing | Flubber |
| Canvas 2D / drawing | Konva |
| 3D web scenes | Three.js |
| Simple hover/loading states | CSS Keyframes |

## Core principle

Web animations run on the browser's **main thread** via `requestAnimationFrame`. Libraries abstract this away, but the performance ceiling is the same: ~60fps on main thread. For heavy work (particles, 3D), offload to GPU via CSS `transform`/`opacity` or use Canvas/WebGL.

## Golden rule

> Prefer `transform` and `opacity` for performance. Avoid animating `width`, `height`, `top`, `left` — they trigger layout reflow.

## Getting started with each library

### GSAP
```js
import gsap from "gsap";
import { ScrollTrigger } from "gsap/ScrollTrigger";
gsap.registerPlugin(ScrollTrigger);

// Basic tween
gsap.to(".box", { x: 100, duration: 1, ease: "power2.out" });

// Scroll trigger
gsap.to(".card", {
  scrollTrigger: ".card",
  y: -50,
  opacity: 1,
  duration: 1,
});
```

### Framer Motion
```tsx
import { motion, AnimatePresence } from "framer-motion";

<motion.div
  initial={{ opacity: 0, y: 20 }}
  animate={{ opacity: 1, y: 0 }}
  exit={{ opacity: 0, y: -20 }}
/>

<AnimatePresence>
  {show && <motion.div key="modal" ... />}
</AnimatePresence>
```

### Motion One
```js
import { animate, scroll, inView } from "motion";

animate(".box", { x: 100 }, { duration: 1, easing: "ease-out" });

scroll(animate(".progress", { scaleX: [0, 1] }));

inView(".fade-in", (el) => {
  animate(el, { opacity: [0, 1] }, { duration: 0.6 });
});
```

### Anime.js
```js
import anime from "animejs";

anime({
  targets: ".box",
  translateX: 250,
  rotate: "1turn",
  duration: 800,
  easing: "easeInOutQuad",
});
```

### Rive (React)
```tsx
import { useRive } from "@rive-app/react-canvas";

const { rive, RiveComponent } = useRive({
  src: "animation.riv",
  stateMachines: "State Machine 1",
  autoplay: true,
});
return <RiveComponent />;
```

### Lottie (React)
```tsx
import { Player } from "@lottiefiles/react-lottie-player";

<Player
  autoplay
  loop
  src="https://assets.lottiefiles.com/example.json"
  style={{ width: 300 }}
/>
```

### D3.js
```js
import * as d3 from "d3";

d3.select("svg")
  .selectAll("circle")
  .data(data)
  .join("circle")
  .attr("r", 0)
  .transition()
  .duration(1000)
  .attr("r", (d) => d.value);
```

### Flubber
```js
import { interpolate } from "flubber";

// Morph between two SVG paths
const morph = interpolate(pathA, pathB);
morph(0.5); // returns midpoint path

// Animate with requestAnimationFrame
let t = 0;
function animate() {
  t += 0.02;
  pathElement.setAttribute("d", morph(Math.min(t, 1)));
  if (t < 1) requestAnimationFrame(animate);
}
```

### Konva (React)
```tsx
import { Stage, Layer, Rect } from "react-konva";

<Stage width={500} height={500}>
  <Layer>
    <Rect x={20} y={20} width={100} height={100} fill="red" />
  </Layer>
</Stage>
```

### Three.js
```js
import * as THREE from "three";

const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(75, w/h, 0.1, 1000);
const renderer = new THREE.WebGLRenderer();
// ... mesh, lights, animate loop
```

---

## Library-specific deep dives

For detailed patterns, load the corresponding rule file:

- [rules/gsap.md](rules/gsap.md) — ScrollTrigger, timelines, stagger
- [rules/framer-motion.md](rules/framer-motion.md) — Layout animations, gestures, variants
- [rules/motion-one.md](rules/motion-one.md) — Scroll, inView, timeline
- [rules/animejs.md](rules/animejs.md) — SVG, keyframes, callbacks
- [rules/rive.md](rules/rive.md) — State machines, input binding
- [rules/lottie.md](rules/lottie.md) — Player controls, interactivity
- [rules/d3.md](rules/d3.md) — Data joins, transition chaining
- [rules/flubber.md](rules/flubber.md) — Path morphing with multiple shapes
- [rules/konva.md](rules/konva.md) — Canvas layers, React binding
- [rules/three-js.md](rules/three-js.md) — Scenes, materials, animation loop
- [rules/css-keyframes.md](rules/css-keyframes.md) — @keyframes, animation properties
- [rules/scroll-animations.md](rules/scroll-animations.md) — Scroll-driven patterns across libraries
- [rules/performance.md](rules/performance.md) — 60fps profiling, will-change, layers
- [rules/choosing-library.md](rules/choosing-library.md) — Decision matrix for library selection
