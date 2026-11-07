---
name: hyperframes-animation
description: "All animation knowledge for HyperFrames — atomic motion rules, multi-phase scene blueprints, scene transitions, broader motion-design techniques, AND the seven runtime adapters (GSAP default, plus Lottie, Three.js, Anime.js, CSS keyframes, Web Animations API, TypeGPU). Use for any motion or animation task: pick 2-4 rules and compose, or load a blueprint, or look up runtime-specific API (e.g. GSAP eases / Lottie player / Three.js mixer). Also covers auditing an existing composition's choreography (animation map) and 24 named text-animation effects. HyperFrames-native: single paused timeline, seek-safe, deterministic."
---

**Plugin installs:** Before setup or freshness commands, follow [plugin execution rules](../hyperframes/references/plugin-installation.md) when this skill is inside a HyperFrames plugin. Standalone installs keep the update instructions below.

# HyperFrames Animation

## Contents

- [Default: compose atomic rules](#default-compose-atomic-rules)
- [Load a blueprint when](#load-a-blueprint-when)
- [Routing](#routing)
- [Picking a runtime](#picking-a-runtime)
- [Critical Constraints](#critical-constraints)
- [Scripts](#scripts)
- [See Also](#see-also)
- [Reference files](#reference-files)

All motion knowledge in one skill: **rules** (atomic recipes), **blueprints** (multi-phase scene templates), **transitions** (scene-to-scene), **techniques** (broader motion-design patterns), and **adapters** (per-runtime APIs).

For the composition contract (data attributes, sub-compositions, determinism) see `hyperframes-core`.

## Default: compose atomic rules

Pick 2-4 rules from `rules-index.md`, glue them together with a single paused GSAP timeline, done. This is faster and produces less code than starting from a blueprint.

## Load a blueprint when

- The scene matches an existing pre-designed multi-phase template (brand-reveal, social-proof, etc.) and reusing its phase pipeline saves real authoring time
- You want runnable ground-truth code for a complex 4-5 phase choreography

Blueprints live in `blueprints-index.md`. Each entry points to `blueprints/<id>.md` (recipe). Do not read it speculatively; load it when you've already decided you need scene-level orchestration.

## Routing

| Want to…                                                                       | Read                                                |
| ------------------------------------------------------------------------------ | --------------------------------------------------- |
| Pick an atomic motion pattern by trigger / tag                                 | `rules-index.md`                                    |
| Read one rule's full HTML / CSS / GSAP recipe                                  | `rules/<name>.md`                                   |
| Pick a multi-phase scene template                                              | `blueprints-index.md`                               |
| Read one blueprint's full recipe                                               | `blueprints/<id>.md`                                |
| Author a scene transition (CSS-driven, between two clips)                      | `transitions/overview.md`, `transitions/catalog.md` |
| Look up a broader motion-design technique                                      | `techniques.md`                                     |
| Motion blur — shutter smear on an element, and when not to use it              | `references/motion-blur.md`                         |
| Analyze an existing composition's animation map                                | `scripts/animation-map.mjs`                         |
| GSAP API — timeline / tweens / position parameters                             | `adapters/gsap.md`                                  |
| GSAP — drop-in effect recipes                                                  | `rules/gsap-effects.md`                             |
| GSAP — transforms / perf                                                       | `adapters/gsap-transforms-and-perf.md`              |
| GSAP — eases / stagger                                                         | `adapters/gsap-easing-and-stagger.md`               |
| GSAP — timeline / labels                                                       | `adapters/gsap-timeline-and-labels.md`              |
| Lottie / dotLottie (After Effects exports, `window.__hfLottie`)                | `adapters/lottie.md`                                |
| Character animation (walk cycle, mascot, jointed puppet, gestures)             | `adapters/lottie.md` → Characters                   |
| Three.js / WebGL (3D scenes, `AnimationMixer`, `hf-seek`)                      | `adapters/three.md`                                 |
| Anime.js (`window.__hfAnime`)                                                  | `adapters/animejs.md`                               |
| CSS keyframes (`animation-delay` / `play-state` / `fill-mode`)                 | `adapters/css-animations.md`                        |
| Web Animations API (`element.animate()`, `currentTime` seek)                   | `adapters/waapi.md`                                 |
| TypeGPU / WebGPU (`navigator.gpu`, WGSL, compute pipelines)                    | `adapters/typegpu.md`                               |
| HTML-as-texture + WebGL/GLSL post-fx (capture live DOM via `drawElementImage`) | `adapters/html-in-canvas-patterns.md`               |
| Named text-animation effects (24 IDs via external `animate-text` skill)        | `adapters/animate-text.md`                          |

## Picking a runtime

- **GSAP** is the default for 95% of motion work — covers timeline orchestration, transforms, easing, stagger. All atomic rules in this skill are GSAP-based.
- **Lottie** when an asset has its own pre-baked timeline (typically After Effects exports), including characters that walk, gesture or react.
- **Three.js** for 3D scenes, camera motion, shader-driven visuals.
- **Anime.js** for lightweight tweening when GSAP is overkill.
- **CSS** for simple repeated motifs, decoration, shimmer — no JavaScript animation cost.
- **WAAPI** for native browser keyframes without a GSAP dependency.
- **TypeGPU / WebGPU** for GPU-rendered canvases (particles, liquid glass, custom shaders).

Multiple runtimes can coexist in one composition. Each registers its instances on the runtime-specific global so HyperFrames can seek all of them in one pass.

## Critical Constraints

**Prerequisite: `hyperframes-core` → One paused timeline + Non-negotiable rules** (single paused timeline, `data-duration` governs length, no `Math.random` / `Date.now` / `performance.now`, no `repeat: -1` without a finite root `data-duration`, no page-load `gsap.set` on later-scene clips, no `display` or raw `visibility` tweens, and register the timeline only after it is fully built, including when the build runs inside an async callback such as `document.fonts.ready`). GSAP `autoAlpha` and zero-duration visibility sets at explicit timeline boundaries remain allowed by core. Use those exceptions only on non-clip elements or wrappers inside a clip; the framework owns `.clip` lifecycle. Don't restate the full contract here.

Animation-craft additions on top of core's contract:

- **Pre-calculated layout constants** — never derive positions from `getBoundingClientRect()` at tween time. Tween-time DOM measurements desync because the renderer samples in parallel; compute coordinates once at composition setup and reuse.
- **Spatial motion uses GSAP transform aliases only** (`x`, `y`, `scale`, `rotation`). Core's allowlist also permits `opacity` / `color` / `backgroundColor` / `borderRadius` for non-spatial property tweens — but never `width` / `height` / `top` / `left` for layout changes.

## Scripts

```bash
node <SKILL_DIR>/scripts/animation-map.mjs <composition-dir> \
  --out <composition-dir>/.hyperframes/anim-map
```

Reads every GSAP timeline registered on `window.__timelines`, enumerates tweens, samples bboxes, computes flags, outputs `animation-map.json`. Use it to audit choreography (dead zones, stagger consistency, lifecycle warnings) after authoring.

`animation-map.mjs` resolves helper packages from the current project first, then can bootstrap the bundled HyperFrames package version. Set `HYPERFRAMES_SKILL_PKG_VERSION=<version>` only when running the skill outside the bundled CLI/skill install and you need to pin that bootstrap version explicitly.

## See Also

- `hyperframes-core` — composition structure, data attributes, sub-compositions, deterministic render contract
- `hyperframes-creative` — palettes, typography, narration, beat planning (non-animation creative direction)
- `hyperframes-cli` — `hyperframes lint / check / snapshot / preview / render`

## Reference files

Read the matching file directly when its topic applies; the indexes remain available for choosing among recipes.

### Adapters

- [Text Effects — Reference](adapters/animate-text.md) — Read when using this animation runtime or adapter API.
- [Anime.js for HyperFrames](adapters/animejs.md) — Read when using this animation runtime or adapter API.
- [CSS Animations for HyperFrames](adapters/css-animations.md) — Read when using this animation runtime or adapter API.
- [Easing, Stagger, and Function-Based Values](adapters/gsap-easing-and-stagger.md) — Read when using this animation runtime or adapter API.
- [Timelines and Labels](adapters/gsap-timeline-and-labels.md) — Read when using this animation runtime or adapter API.
- [Transforms and Performance](adapters/gsap-transforms-and-perf.md) — Read when using this animation runtime or adapter API.
- [HyperFrames GSAP](adapters/gsap.md) — Read when using this animation runtime or adapter API.
- [HTML-in-Canvas Patterns](adapters/html-in-canvas-patterns.md) — Read when using this animation runtime or adapter API.
- [Lottie for HyperFrames](adapters/lottie.md) — Read when using this animation runtime or adapter API.
- [Three.js for HyperFrames](adapters/three.md) — Read when using this animation runtime or adapter API.
- [TypeGPU / WebGPU for HyperFrames](adapters/typegpu.md) — Read when using this animation runtime or adapter API.
- [Web Animations API for HyperFrames](adapters/waapi.md) — Read when using this animation runtime or adapter API.

### Blueprints

- [agent-progress-theater — Agent Progress Theater](blueprints/agent-progress-theater.md) — Read when composing this multi-phase scene.
- [camera-journey — Camera Journey](blueprints/camera-journey.md) — Read when composing this multi-phase scene.
- [comparison-split — Comparison Split-Cards](blueprints/comparison-split.md) — Read when composing this multi-phase scene.
- [constellation-hub — Constellation / Hub + Satellites](blueprints/constellation-hub.md) — Read when composing this multi-phase scene.
- [cta-morph-press — CTA Morph & Press](blueprints/cta-morph-press.md) — Read when composing this multi-phase scene.
- [cursor-ui-demo — Cursor-Driven UI Demo](blueprints/cursor-ui-demo.md) — Read when composing this multi-phase scene.
- [dataviz-countup — Data-Viz / Count-Up](blueprints/dataviz-countup.md) — Read when composing this multi-phase scene.
- [device-surface-showcase — Device / Surface Showcase](blueprints/device-surface-showcase.md) — Read when composing this multi-phase scene.
- [fixed-anchor-cycle — Fixed Anchor, Cycling World](blueprints/fixed-anchor-cycle.md) — Read when composing this multi-phase scene.
- [grid-card-assemble — Grid / Card Assemble](blueprints/grid-card-assemble.md) — Read when composing this multi-phase scene.
- [kinetic-type-beats — Kinetic-Type Beats](blueprints/kinetic-type-beats.md) — Read when composing this multi-phase scene.
- [logo-assemble-lockup — Logo Assemble → Lockup](blueprints/logo-assemble-lockup.md) — Read when composing this multi-phase scene.
- [overwhelm-surround — Overwhelm / Close-In](blueprints/overwhelm-surround.md) — Read when composing this multi-phase scene.
- [panel-edit-live-sync — Panel Edit, Live Sync](blueprints/panel-edit-live-sync.md) — Read when composing this multi-phase scene.
- [prompt-type-submit-generate — Prompt, Submit, Generate](blueprints/prompt-type-submit-generate.md) — Read when composing this multi-phase scene.
- [spatial-pan-stations — Spatial Pan / Stations](blueprints/spatial-pan-stations.md) — Read when composing this multi-phase scene.
- [ticker-takeover — Ticker Displace / Takeover](blueprints/ticker-takeover.md) — Read when composing this multi-phase scene.
- [titlecard-reveal — Title-Card / Single-Card Reveal](blueprints/titlecard-reveal.md) — Read when composing this multi-phase scene.
- [transcript-scroll-artifact-reveal — Transcript-Scroll Artifact Reveal](blueprints/transcript-scroll-artifact-reveal.md) — Read when composing this multi-phase scene.
- [typewriter-reveal — Typewriter Reveal](blueprints/typewriter-reveal.md) — Read when composing this multi-phase scene.
- [video-text-pivot — Video → Text Pivot](blueprints/video-text-pivot.md) — Read when composing this multi-phase scene.
- [zoom-out-workspace-reveal — Zoom-Out Workspace Reveal](blueprints/zoom-out-workspace-reveal.md) — Read when composing this multi-phase scene.

### Guides

- [Blueprints (the proven shapes)](blueprints-index.md) — Read when choosing a scene blueprint.
- [Rules Index](rules-index.md) — Read when choosing atomic motion rules by trigger or tag.
- [Visual Techniques Reference](techniques.md) — Read when choosing broader motion-design techniques.

### References

- [Motion blur — shutter smear on any animated element](references/motion-blur.md) — Read when choosing element-level motion blur and its limits.

### Rules

- [3D Camera Flight](rules/3d-camera-flight.md) — Read when applying this atomic motion recipe.
- [3D Page Scroll](rules/3d-page-scroll.md) — Read when applying this atomic motion recipe.
- [3D Text Depth Layers](rules/3d-text-depth-layers.md) — Read when applying this atomic motion recipe.
- [AI Tracking Box](rules/ai-tracking-box.md) — Read when applying this atomic motion recipe.
- [Ambient Glow Bloom](rules/ambient-glow-bloom.md) — Read when applying this atomic motion recipe.
- [Anchored Layout Expand](rules/anchored-layout-expand.md) — Read when applying this atomic motion recipe.
- [ASR Keyword Glow](rules/asr-keyword-glow.md) — Read when applying this atomic motion recipe.
- [Avatar Cloud Network](rules/avatar-cloud-network.md) — Read when applying this atomic motion recipe.
- [Two-Phase Camera Cursor Tracking](rules/camera-cursor-tracking.md) — Read when applying this atomic motion recipe.
- [Card Morph Anchor](rules/card-morph-anchor.md) — Read when applying this atomic motion recipe.
- [Center-Outward Expansion](rules/center-outward-expansion.md) — Read when applying this atomic motion recipe.
- [Chart Scrub Readout](rules/chart-scrub-readout.md) — Read when applying this atomic motion recipe.
- [Chromatic Glitch](rules/chromatic-glitch.md) — Read when applying this atomic motion recipe.
- [Context-Sensitive Cursor](rules/context-sensitive-cursor.md) — Read when applying this atomic motion recipe.
- [Control-Target Sync](rules/control-target-sync.md) — Read when applying this atomic motion recipe.
- [Coordinate Target Zoom](rules/coordinate-target-zoom.md) — Read when applying this atomic motion recipe.
- [Counting with Dynamic Scale](rules/counting-dynamic-scale.md) — Read when applying this atomic motion recipe.
- [CSS Patterns for Marker Highlighting](rules/css-marker-patterns.md) — Read when applying this atomic motion recipe.
- [Cursor Click Ripple](rules/cursor-click-ripple.md) — Read when applying this atomic motion recipe.
- [Cursor Drag](rules/cursor-drag.md) — Read when applying this atomic motion recipe.
- [Depth-of-Field Blur (Selective Focus / Rack Focus)](rules/depth-of-field-blur.md) — Read when applying this atomic motion recipe.
- [Depth Scatter ↔ Assemble](rules/depth-scatter-assemble.md) — Read when applying this atomic motion recipe.
- [Discrete Text Sequence](rules/discrete-text-sequence.md) — Read when applying this atomic motion recipe.
- [Dynamic Content Sequencing](rules/dynamic-content-sequencing.md) — Read when applying this atomic motion recipe.
- [Gradient Text Sweep](rules/gradient-text-sweep.md) — Read when applying this atomic motion recipe.
- [GSAP Effects for HyperFrames](rules/gsap-effects.md) — Read when applying this atomic motion recipe.
- [Hacker Flip 3D Reveal](rules/hacker-flip-3d.md) — Read when applying this atomic motion recipe.
- [Kinetic Beat Slam](rules/kinetic-beat-slam.md) — Read when applying this atomic motion recipe.
- [Motion-Blur Streak](rules/motion-blur-streak.md) — Read when applying this atomic motion recipe.
- [Multi-Cursor Choreography](rules/multi-cursor-choreography.md) — Read when applying this atomic motion recipe.
- [Multi-Phase Camera](rules/multi-phase-camera.md) — Read when applying this atomic motion recipe.
- [Nudge Curve](rules/nudge-curve.md) — Read when applying this atomic motion recipe.
- [Orbit with 3D Entry](rules/orbit-3d-entry.md) — Read when applying this atomic motion recipe.
- [Particle Burst](rules/particle-burst.md) — Read when applying this atomic motion recipe.
- [Physics Press Reaction (Cursor + Element Synced)](rules/physics-press-reaction.md) — Read when applying this atomic motion recipe.
- [Press-Release Spring Chain](rules/press-release-spring.md) — Read when applying this atomic motion recipe.
- [Reactive Displacement](rules/reactive-displacement.md) — Read when applying this atomic motion recipe.
- [Scale-Swap Transition](rules/scale-swap-transition.md) — Read when applying this atomic motion recipe.
- [Sine Wave Loop (subtle jitter / bounded ambient)](rules/sine-wave-loop.md) — Read when applying this atomic motion recipe.
- [Split Tilt Cards](rules/split-tilt-cards.md) — Read when applying this atomic motion recipe.
- [Spring-Pop Entrance](rules/spring-pop-entrance.md) — Read when applying this atomic motion recipe.
- [Stat Bars & Fills](rules/stat-bars-and-fills.md) — Read when applying this atomic motion recipe.
- [SVG Icon Enrichment](rules/svg-icon-enrichment.md) — Read when applying this atomic motion recipe.
- [SVG Path Draw](rules/svg-path-draw.md) — Read when applying this atomic motion recipe.
- [Theme Crossfade Morph](rules/theme-crossfade-morph.md) — Read when applying this atomic motion recipe.
- [Vertical Spring Ticker (Slot Machine)](rules/vertical-spring-ticker.md) — Read when applying this atomic motion recipe.
- [Viewport Change (Virtual Camera)](rules/viewport-change.md) — Read when applying this atomic motion recipe.
- [Waterfall Entry](rules/waterfall-entry.md) — Read when applying this atomic motion recipe.

### Transitions

- [Transition Registry — machine source of truth](transitions/TRANSITION-REGISTRY.md) — Read when choosing or implementing this scene transition.
- [Transition Catalog](transitions/catalog.md) — Read when choosing or implementing this scene transition.
- [3D](transitions/css-3d.md) — Read when choosing or implementing this scene transition.
- [Blur](transitions/css-blur.md) — Read when choosing or implementing this scene transition.
- [Cover](transitions/css-cover.md) — Read when choosing or implementing this scene transition.
- [Destruction](transitions/css-destruction.md) — Read when choosing or implementing this scene transition.
- [Dissolve](transitions/css-dissolve.md) — Read when choosing or implementing this scene transition.
- [Distortion](transitions/css-distortion.md) — Read when choosing or implementing this scene transition.
- [Grid](transitions/css-grid.md) — Read when choosing or implementing this scene transition.
- [Light](transitions/css-light.md) — Read when choosing or implementing this scene transition.
- [Mechanical](transitions/css-mechanical.md) — Read when choosing or implementing this scene transition.
- [Other](transitions/css-other.md) — Read when choosing or implementing this scene transition.
- [Linear / Push](transitions/css-push.md) — Read when choosing or implementing this scene transition.
- [Radial / Shape](transitions/css-radial.md) — Read when choosing or implementing this scene transition.
- [Scale / Zoom](transitions/css-scale.md) — Read when choosing or implementing this scene transition.
- [Scene Transitions](transitions/overview.md) — Read when choosing or implementing this scene transition.
