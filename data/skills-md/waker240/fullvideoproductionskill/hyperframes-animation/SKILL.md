---
name: hyperframes-animation
description: Build deterministic animation for HyperFrames using motion rules, transitions, scene blueprints, and runtime adapters. Use when motion or camera behavior needs implementation.
compatibility: Requires sibling skills from this pack, a local filesystem and shell, Node.js 22.20.0+, and FFmpeg/ffprobe for media work. Generation providers and desktop tools are optional, separately configured capabilities.
---

<!-- Public portability adaptation, 2026-09-26. -->

Install this skill with its sibling skills. See [runtime setup and capability boundaries](../hyperframes/references/install-portability.md) before executing commands. User instructions and the requested production stage take precedence over workflow defaults.

# HyperFrames Animation

All motion knowledge in one skill: **rules** (atomic recipes), **blueprints** (multi-phase scene templates), **transitions** (scene-to-scene), **techniques** (broader motion-design patterns), and **adapters** (per-runtime APIs).

For the composition contract (data attributes, sub-compositions, determinism) see `hyperframes-core`.

## Default: compose atomic rules

Pick 2-4 rules from `rules-index.md` and compose them on a single paused GSAP timeline. When the project admits a Spatial Canvas or fast passage, its manifest is the choreography contract; rules serve the declared route/phases rather than inventing a parallel structure.

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
| Build an admitted persistent Spatial Canvas (`SPATIAL_CANVAS.json`) with camera visits and cutaway/return | `blueprints/spatial-canvas.md` + `hyperframes-core/references/spatial-canvas.md` |
| Direct camera focus, narration retiming, precise world/HUD ownership, meaningful returns and crop/registration review | `references/directed-camera.md` |
| Implement an admitted `FAST_PASSAGES.json` trajectory after its arc is locked | `hyperframes-creative/references/fast-paced-editing.md`, then `transitions/overview.md` / `transitions/catalog.md` plus the cited rules or blueprints |
| Animate paper folds, layered cutouts, material parallax or object-led edits in a selected paper-theatre direction | `../hyperframes-creative/references/paper-theatre.md` §4–5; then the applicable rules/adapters |
| Author a scene transition (CSS-driven, between two clips)                      | `transitions/overview.md`, `transitions/catalog.md` |
| Look up a broader motion-design technique                                      | `techniques.md`                                     |
| Analyze an existing composition's animation map                                | `scripts/animation-map.mjs`                         |
| GSAP API — timeline / tweens / position parameters                             | `adapters/gsap.md`                                  |
| GSAP — drop-in effect recipes                                                  | `rules/gsap-effects.md`                             |
| GSAP — transforms / perf                                                       | `adapters/gsap-transforms-and-perf.md`              |
| GSAP — eases / stagger                                                         | `adapters/gsap-easing-and-stagger.md`               |
| GSAP — timeline / labels                                                       | `adapters/gsap-timeline-and-labels.md`              |
| Lottie / dotLottie (After Effects exports, `window.__hfLottie`)                | `adapters/lottie.md`                                |
| Three.js / WebGL after the visual-quality admission gate (`AnimationMixer`, `hf-seek`) | `adapters/three.md`                          |
| Build admitted authored 3D — beveled geometry, lathe profiles, PMREM studio, seeded materials, analytic stops/deforming cables, resource readiness | `references/authored-three-workflow.md` |
| Anime.js (`window.__hfAnime`)                                                  | `adapters/animejs.md`                               |
| CSS keyframes (`animation-delay` / `play-state` / `fill-mode`)                 | `adapters/css-animations.md`                        |
| Web Animations API (`element.animate()`, `currentTime` seek)                   | `adapters/waapi.md`                                 |
| TypeGPU / WebGPU (`navigator.gpu`, WGSL, compute pipelines)                    | `adapters/typegpu.md`                               |
| HTML-as-texture + WebGL/GLSL post-fx (capture live DOM via `drawElementImage`) | `adapters/html-in-canvas-patterns.md`               |
| Named text-animation effects (24 IDs via external `animate-text` skill)        | `adapters/animate-text.md`                          |

## Picking a runtime

- **GSAP** is the default for 95% of motion work — covers timeline orchestration, transforms, easing, stagger. All atomic rules in this skill are GSAP-based.
- **Lottie** when an asset has its own pre-baked timeline (typically After Effects exports).
- **Three.js** only when spatial causality, authored geometry/assets, and a coherent world clear `adapters/three.md`'s admission gate. For abstract agents and mechanisms, semantic 2D/2.5D is the default—not a fallback.
- **Anime.js** for lightweight tweening when GSAP is overkill.
- **CSS** for simple repeated motifs, decoration, shimmer — no JavaScript animation cost.
- **WAAPI** for native browser keyframes without a GSAP dependency.
- **TypeGPU / WebGPU** for GPU-rendered canvases (particles, liquid glass, custom shaders).

Multiple runtimes can coexist in one composition. Each registers its instances on the runtime-specific global so HyperFrames can seek all of them in one pass.

“Spatial Canvas” is a world/camera composition grammar, not a runtime choice. Default to DOM/SVG + GSAP; Canvas 2D or true 3D is optional and must still satisfy its normal admission/seek contract. Keep one persistent world owner and animate camera pose as one coupled object; departure, cutaway, and consequential return are one move.

“Fast-paced” is a bounded edit trajectory, not a license to apply every transition. Follow the manifest's exact baseline → escalation → peak → release windows and focal receivers; add one density channel at a time, preserve caption/voice legibility, and make the release mechanically visible. A `PASS` for either grammar remains correct when it does not serve the argument.

## Critical Constraints

**Prerequisite: `hyperframes-core` → Non-Negotiable Rules** (single paused timeline, `data-duration` governs length, no `Math.random` / `Date.now` / `performance.now`, no `repeat: -1`, no `gsap.set` on later-scene clips, no `display` / `visibility` animation, no timeline construction inside `async` / `setTimeout` / `Promise`). Don't restate those here.

Animation-craft additions on top of core's contract:

- **Pre-calculated layout constants** — never derive positions from `getBoundingClientRect()` at tween time. Tween-time DOM measurements desync because the renderer samples in parallel; compute coordinates once at composition setup and reuse.
- **Spatial motion uses GSAP transform aliases only** (`x`, `y`, `scale`, `rotation`). Core's allowlist also permits `opacity` / `color` / `backgroundColor` / `borderRadius` for non-spatial property tweens — but never `width` / `height` / `top` / `left` for layout changes.

## Scripts

```bash
node skills/hyperframes-animation/scripts/animation-map.mjs <composition-dir> \
  --out <composition-dir>/.hyperframes/anim-map
```

Reads every GSAP timeline registered on `window.__timelines`, enumerates tweens, samples bboxes, computes flags, outputs `animation-map.json`. Use it to audit choreography (dead zones, stagger consistency, lifecycle warnings) after authoring. It cannot judge narration match, subject quality, or world coherence; pair it with `hyperframes-creative/references/design-adherence.md`'s rendered-trajectory gate.

## See Also

- `hyperframes-core` — composition structure, data attributes, sub-compositions, deterministic render contract
- `hyperframes-creative` — palettes, typography, narration, beat planning (non-animation creative direction)
- `hyperframes-cli` — `npx hyperframes lint / validate / inspect / preview / render`
