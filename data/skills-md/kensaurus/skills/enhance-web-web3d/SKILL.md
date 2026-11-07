---
name: enhance-web-web3d
description: >
  Add purposeful 3D/WebGL and scroll choreography to an existing site with
  Three.js/R3F, GSAP, or Motion. Use when "add 3D", "WebGL hero", "React Three
  Fiber", or "scroll-driven 3D". Motion without 3D → enhance-motion.
license: MIT
---

> Surface router: `/uiux`. You are here: `enhance-web-web3d`. Native iOS/Android (SwiftUI / Compose, no web layer) is out of scope — use Apple HIG / Material directly.

# Enhance Web with 3D & Cinematic Motion

**Degree of freedom: MIXED.** Fit and stack choice `[HIGH freedom]`; budget, fallbacks, SSR, and verify `[LOW freedom — run exactly]`.

Add Three.js / React Three Fiber scenes, GSAP scroll choreography, and physics
motion to an **existing** web project — without rewriting it, breaking the
build, blowing the performance budget, or shipping a blank canvas to users on
weak devices or with WebGL disabled.

This is **not** a "drop a spinning cube on the homepage" skill. It audits the
repo first, decides whether 3D actually serves the page, picks the smallest
library combination that fits the existing stack, and ships the effect with
fallbacks and reduced-motion support from the first commit.

> **For greenfield / from-scratch 3D library mechanics** (raw Three.js scene
> setup, R3F primitives, shader authoring), this skill points you at the
> deeper references but stays focused on *integrating into a live repo*. For
> pure visual composition (no 3D) use `enhance-web-ui`; for anti-slop landing
> pages use `enhance-web-landing`.

## This skill vs neighbors

| Skill | Owns |
|---|---|
| **enhance-web-web3d** (this) | 3D/WebGL and scroll choreography added to an existing site |
| `enhance-motion` | Motion audit and one reduced-motion-safe pass, without 3D |

## How to reason

1. **Fit** — does 3D serve comprehension/brand, or is it decoration?
2. **Choose** — minimal stack from the matrix; one system per property
3. **Integrate** — budget + reduced-motion + no-WebGL + `ssr: false` in the same change
4. **Prove** — mid-tier FPS, fallbacks, LCP not waiting on WebGL

## Worked example

> **Fit:** cookware PDP; users decide from the pot shape — a viewer earns cost; a torus knot does not.
> **Choose:** Next.js + R3F + drei; Motion overlays; no GSAP (no scroll story).
> **Integrate:** `dynamic(..., { ssr: false })`; poster as LCP; `frameloop="demand"`; Draco model.
> **Prove:** reduced-motion shows poster; WebGL-off shows the same; LCP unchanged.

## Self-critique before reporting

- **Fit passed** — non-3D alternative was considered and rejected for a reason
- **Same change** — fallbacks, reduced-motion, and SSR safety shipped with the scene
- **No blank canvas** — no-WebGL and mid-tier paths verified
- **Right owner** — no-3D polish → `enhance-web-ui`; motion without 3D → `enhance-motion`; anti-slop landing → `enhance-web-landing`

---

## How This Works

When applied to an existing project, follow this sequence. **Never skip the
audit and jump to code** — that is how 3D ends up as a 4 MB hero nobody on
mobile can load.

1. **Scan** — Read the codebase. Identify framework, rendering model (SSR /
 SSG / SPA), styling system, existing motion/3D libraries, build tool, and
 the current performance baseline.
2. **Fit check** — Decide *whether* 3D/cinematic motion belongs on this
 surface and *where*. Reject 3D-for-3D's-sake.
3. **Diagnose** — Map concrete opportunities (hero, product viewer,
 scroll-story, background ambience) and the constraints around each.
4. **Choose stack** — Use the Decision Matrix to pick the minimal library
 combination that fits the existing stack.
5. **Implement** — Build with the chosen pattern, wiring performance budget,
 fallbacks, reduced-motion, and SSR/hydration safety in the same change.
6. **Verify** — Profile on a mid-tier device, test the no-WebGL and
 reduced-motion paths, confirm Lighthouse / Web Vitals didn't regress.

---

## Phase 0: Fit Check (does 3D belong here?)  [HIGH freedom]

Before touching any library, answer these. If you can't justify the effect,
the right move is `enhance-web-ui` or `enhance-web-landing`, not WebGL.

- [ ] **Does the effect serve comprehension or brand, or is it decoration?**
 A product configurator, a data-driven globe, a hero that shows the actual
 product in 3D — these earn their cost. A generic floating-blob background
 usually does not.
- [ ] **What is the performance budget?** A marketing landing page can spend
 more than a dashboard a user opens 40× a day. Name the budget (KB, LCP, INP,
 target FPS) *before* designing.
- [ ] **Who is the audience / device mix?** Heavy mobile traffic → design the
 mobile fallback first, then enhance up. Desktop-only internal tool → you
 have more headroom.
- [ ] **Is there a non-3D alternative that's 90% as good for 10% of the cost?**
 A pre-rendered `<video>`, an animated SVG, a CSS scroll effect, or a
 high-quality image sequence often beats live WebGL. The DEV community lesson
 holds: a scripted DOM/GSAP walkthrough can be **under 40 KB gzip vs a
 multi-MB MP4/GIF** — reach for real WebGL only when interactivity or true 3D
 depth is the point.
- [ ] **Reduced-motion + no-WebGL story exists?** If you can't describe what a
 `prefers-reduced-motion` user and a no-WebGL user see, you're not ready to
 build.

> **Anti-slop guardrail.** A spinning torus knot, a particle field with no
> meaning, or a tilt-on-mouse card that fights scrolling are the 3D equivalent
> of the purple-gradient hero. Motion and depth must explain, demo, or brand —
> never just sparkle.

---

## Phase 1: Recon — Learn the Existing Stack  [HIGH freedom]

Read the entry point, layout, and any existing animated component. Then record:

```
FRAMEWORK: [Next.js (app/pages?) / Vite+React / Astro / Remix / SvelteKit / vanilla]
RENDER MODEL: [SSR / SSG / CSR — matters for hydration + dynamic import]
REACT?: [yes → R3F is on the table | no → vanilla three.js]
STYLING: [Tailwind v3/v4 / CSS modules / styled-components / vanilla]
BUILD TOOL: [Vite / Webpack / Turbopack / esbuild — affects code-split + worker setup]
EXISTING MOTION: [framer-motion/motion? GSAP? Lenis? CSS only?]
EXISTING 3D: [three? @react-three/fiber? drei? none?]
PERF BASELINE: [current LCP / bundle size / Lighthouse, if measurable]
ASSET PIPELINE: [is there a /public model dir? a CDN? Draco/KTX2 already set up?]
```

Check the dependency manifest **before importing anything** — reuse what's
installed, match the installed major version (three, @react-three/fiber, gsap,
motion vs framer-motion), and never hallucinate an import.

Search for prior art and guard comments:

```bash
rg -l "three|@react-three|gsap|ScrollTrigger|Lenis|framer-motion|\"motion\"" --type ts --type tsx package.json
rg -n "useGSAP|registerPlugin|<Canvas|useFrame|frameloop" src/
rg -n "prefers-reduced-motion|matchMedia|DO NOT|deprecated" src/
```

---

## Phase 2: Opportunity Audit — Where 3D Earns Its Place  [HIGH freedom]

Map the page to one (rarely more than two) of these archetypes. Each has a
different cost/benefit and a different stack.

| Opportunity | What it is | Earns its cost when | Default stack |
|-------------|-----------|---------------------|---------------|
| **Hero scene** | First-fold 3D centerpiece | The product *is* visual/physical | Three.js or R3F + a light entrance tween |
| **Product viewer / configurator** | Rotate/zoom/customize a model | Users decide based on the object | R3F + drei (`OrbitControls`, `Environment`) |
| **Scroll story (pinned)** | Camera/model animates as you scroll | There's a narrative or process to reveal | GSAP `ScrollTrigger` (pin + scrub) driving the scene |
| **Ambient background** | Subtle depth behind content | Brand texture, low-distraction | Cheap shader / instanced particles, `frameloop="demand"` |
| **Data viz in 3D** | Globe, graph, point cloud | The data is inherently spatial | R3F + instancing; or 2D if it reads better flat |
| **Micro-interaction** | Hover/drag physics on a card | Delight on a key CTA | Motion / React Spring (often no Three.js at all) |

> **Rule:** one focal 3D moment per page beats five. If everything moves,
> nothing is special — the same hierarchy logic as `enhance-web-ui` applies in
> three dimensions.

---

## Phase 3: Decision Matrix — Pick the Minimal Stack  [HIGH freedom]

GSAP and all of its plugins (ScrollTrigger, SplitText, MorphSVG, …) are free for every use, so licensing does not constrain the choice.

| Use case | Recommended stack | Rationale |
|----------|-------------------|-----------|
| Marketing page, scroll-driven 3D | Three.js (or R3F) + **GSAP ScrollTrigger** + HTML/Motion overlays | GSAP owns scroll orchestration; clean layer separation |
| React app, interactive 3D viewer | **R3F** + drei + Motion | Declarative, state-driven, component-based |
| Timeline-choreographed sequences | **R3F + GSAP** (timeline in `useGSAP`) | GSAP timeline control over R3F objects |
| Physics-y drag / momentum / gestures | **R3F + React Spring** (`@react-spring/three`) | Spring physics feel natural |
| High-count particles / instances | Three.js + GSAP, `InstancedMesh`/`BatchedMesh` | Imperative control, minimal overhead |
| Smooth-scroll feel under GSAP | add **Lenis** (`lenis` / `react-lenis`) | Inertia scroll that ScrollTrigger can drive |
| Pure UI delight (no real 3D) | **Motion** or **React Spring** only | Don't pull in WebGL for a hover effect |
| Non-React repo | **vanilla three.js + GSAP** | R3F requires React; don't add React for one scene |

**One animation system per property.** GSAP *or* React Spring *or* Motion
animating a given transform — never two on the same property. Coordinate by
timing or split properties (GSAP drives position, Spring drives scale).

---

## Phase 4: Integration Patterns  [HIGH freedom]

Pick the pattern that matches the stack from Phase 3. Full, current code lives
in the foundation references (see *Research & Foundation Skills*); below are the
load-bearing shapes and the integration glue.

### Pattern A — Layered Separation (vanilla three.js + GSAP + HTML)

Best for non-React repos and marketing sites. Three layers: a 3D layer
(scene/camera/render loop), an animation layer (GSAP ScrollTrigger), and an
HTML/UI overlay. The scene exposes refs (camera, key meshes); GSAP animates
those refs on scroll; HTML sits on top.

```js
// scroll.js — GSAP drives the scene's exposed refs
import gsap from "gsap";
import { ScrollTrigger } from "gsap/ScrollTrigger";
gsap.registerPlugin(ScrollTrigger);

export function initScrollAnimations({ camera, model }) {
 const tl = gsap.timeline({
 scrollTrigger: { trigger: "#stage", start: "top top", end: "+=3000", scrub: 1, pin: true },
 });
 tl.to(camera.position, { x: 5, z: 10, onUpdate: () => camera.lookAt(0, 0, 0) })
 .to(model.rotation, { y: Math.PI * 2 }, 0);
 return () => tl.scrollTrigger?.kill(); // always return teardown
}
```

### Pattern B — Unified React (R3F + Motion)

Best for React apps with interactive, state-driven 3D. `<Canvas>` holds the
scene; `motion.div` overlays carry HTML. Keep per-frame work in `useFrame`
mutating **refs**, never React state.

```tsx
// Lazy-load the canvas so WebGL never blocks first paint / SSR
const Scene = dynamic(() => import("./Scene"), { ssr: false, loading: () => <Poster /> });

<Canvas camera={{ position: [0, 2, 5], fov: 45 }} dpr={[1, 1.5]} frameloop="demand">
 <Suspense fallback={null}><Scene /></Suspense>
</Canvas>
```

### Pattern C — Hybrid (R3F + GSAP timelines)

R3F renders; GSAP choreographs. Create the timeline inside `useGSAP` (scoped,
auto-cleaned) and target the R3F object's `.current`.

```tsx
import { useGSAP } from "@gsap/react";
useGSAP(() => {
 const tl = gsap.timeline({ scrollTrigger: { trigger: ref.current, scrub: 1 } });
 tl.to(groupRef.current.position, { y: 2, ease: "power2.inOut" });
}, { scope: ref }); // useGSAP reverts on unmount — handles Strict Mode double-invoke
```

### Pattern D — Physics (R3F + React Spring)

`@react-spring/three` for drag/momentum/gesture feedback that should feel
weighty. Spring owns scale/position; nothing else touches those props.

---

## Phase 5: Performance Budget (bake in, don't bolt on)  [LOW freedom — run exactly]

WebGL is expensive and degrades hard on weak devices. Apply these from the
first commit, not after a complaint.

**Render loop**
- [ ] Cap DPR: `dpr={[1, 1.5]}` (R3F) / `renderer.setPixelRatio(Math.min(devicePixelRatio, 2))`.
- [ ] Render on demand where possible: R3F `frameloop="demand"` + `invalidate()` on change; vanilla → only render when something changed or controls are active.
- [ ] **Pause off-screen.** `IntersectionObserver` stops the loop when the canvas leaves the viewport.
- [ ] Never read/write React state in `useFrame` — mutate refs. State in the loop forces 60 fps re-renders.

**Draw calls & geometry**
- [ ] Aim for **< 100 draw calls/frame**. Use `InstancedMesh` / `BatchedMesh` for repeated objects; merge static geometry.
- [ ] Reuse geometries and materials; don't allocate inside the loop.
- [ ] LOD for large scenes; simpler shaders + reduced geometry on mobile.

**Assets**
- [ ] glTF + **Draco** for meshes (50–80% smaller); **KTX2/Basis** for textures (3–5× smaller, lower GPU memory).
- [ ] Power-of-two textures, mipmaps, correct `colorSpace` (`SRGBColorSpace`).
- [ ] **Lazy-load 3D below the fold**; code-split the Three.js/R3F bundle; preload only critical assets. Never lazy-load the LCP element itself.

**Modern renderer (optional, current)**
- [ ] WebGPU is production-ready since three r171: `import { WebGPURenderer } from "three/webgpu"` ships one renderer with **automatic WebGL2 fallback**. Use `forceWebGL: true` to test the fallback path. No urgent migration if a WebGL2 app already runs smoothly.

**Main thread (advanced)**
- [ ] For heavy scenes, consider `OffscreenCanvas` + Web Worker to keep the main thread free for UI/INP.

**Cleanup**
- [ ] `dispose()` every geometry / material / texture / render target on unmount; `renderer.dispose()`. Kill GSAP tweens/ScrollTriggers (`useGSAP` does this for you).

---

## Phase 6: Accessibility & Graceful Degradation  [LOW freedom — run exactly]

A 3D enhancement that breaks for some users is a regression, not an upgrade.

- [ ] **Reduced motion.** Respect `prefers-reduced-motion`: disable scroll
 scrub / auto-rotation / parallax, or swap to a static poster frame. Gate at
 the source so the whole scene honors it.

```ts
const reduce = typeof window !== "undefined"
 && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
// reduce ? render static poster / no scrub : full experience
```

- [ ] **No-WebGL fallback.** Feature-detect; if WebGL/WebGPU is unavailable,
 render a static image/`<video>`/SVG that preserves the visual language and the
 conversion path. Never a blank canvas.
- [ ] **Mobile fallback designed first**, then enhanced up — simpler scene,
 fewer particles, no heavy post-processing, fewer transparent layers.
- [ ] **Keep semantic HTML for anything interactive.** Buttons, links, and
 text content live in real DOM (overlay), not as click targets inside the
 canvas — screen readers and keyboard users need them, and it protects INP.
- [ ] **Don't trap scroll or focus.** Pinned scroll sections must release; the
 canvas must not steal keyboard focus or block tabbing.
- [ ] **Protect LCP.** The hero's largest contentful element should not wait on
 WebGL init — show a poster immediately, hydrate the scene after.

---

## Phase 7: SSR / Hydration Safety  [LOW freedom — run exactly]

The most common way 3D breaks an existing app is server rendering and React
Strict Mode.

- [ ] **Don't render WebGL on the server.** Next.js: `dynamic(() => import("./Scene"), { ssr: false })`. Guard any `window`/`document` access with a client check.
- [ ] **Use `useGSAP()` from `@gsap/react`**, not bare `useEffect` — it scopes
 selectors and auto-reverts animations on unmount, surviving route changes and
 Strict Mode's double-invoke. Never create tweens in the render body (a new
 animation per re-render).
- [ ] **Clean up everything on unmount** — ScrollTriggers, RAF loops, resize
 listeners, IntersectionObservers, disposables.
- [ ] **Lenis (if used):** integrate with ScrollTrigger via the recommended
 `lenis.on("scroll", ScrollTrigger.update)` + ticker wiring so scroll position
 stays in sync.

---

## Common Pitfalls

| Pitfall | Fix |
|---------|-----|
| Two libraries animate the same property | One system per property; split or sequence |
| React state mutated in `useFrame` | Mutate refs; lift state out of the loop |
| Scene renders every frame while idle/off-screen | `frameloop="demand"` + `IntersectionObserver` pause |
| GSAP tween created in render body | Wrap in `useGSAP` / `contextSafe` |
| Blank canvas on no-WebGL / slow device | Feature-detect + poster/video fallback |
| WebGL initialized on server | `ssr: false` dynamic import; window guards |
| Multi-MB model on the hero | Draco/KTX2 + lazy-load + poster + device-tier scene |
| Scroll jank under ScrollTrigger | `scrub` numeric (smoothing), Lenis, refs not state |
| Memory grows on route change | Dispose geometries/materials/textures + kill tweens |
| Parallax/tilt fights native scroll | Reduced-motion gate + clamp; don't hijack the wheel |

---

## Verification Checklist (run before declaring done)  [LOW freedom — do not skip]

- [ ] Builds and type-checks; no hallucinated imports; installed versions matched.
- [ ] Profiled on a **mid-tier / mobile** device or throttled DevTools — holds target FPS.
- [ ] Draw calls within budget (`renderer.info` / `stats-gl`); DPR capped.
- [ ] `prefers-reduced-motion` path verified (motion off / poster shown).
- [ ] No-WebGL path verified (DevTools disable WebGL, or `forceWebGL` + simulated failure) — graceful fallback, never blank.
- [ ] Mobile layout + fallback scene verified at a real narrow viewport.
- [ ] LCP/INP/CLS not regressed vs the Phase 1 baseline (Lighthouse before/after).
- [ ] SSR/hydration clean — no `window is not defined`, no hydration mismatch, no Strict Mode double-mount leak.
- [ ] Unmount is clean — disposables freed, tweens/observers killed (navigate away and back, watch memory).
- [ ] Interactive elements remain real DOM, keyboard-reachable; canvas doesn't trap focus/scroll.
- [ ] One focal 3D moment per page; the effect explains/demos/brands (passes the Phase 0 fit check).

---

## Rules

- Work with the **existing stack**. Don't add React for one scene; don't swap build tools or styling systems.
- Don't break existing functionality or the build. Lazy-load and feature-gate so the page still works if WebGL fails.
- Check the dependency manifest before importing; match installed major versions (`three`, `@react-three/fiber`, `@react-three/drei`, `gsap`, `@gsap/react`, `motion`/`framer-motion`, `@react-spring/three`, `lenis`).
- Keep changes reviewable and scoped to the surface being enhanced.
- Performance budget, fallbacks, reduced-motion, and SSR safety ship **in the same change** as the effect — not as a follow-up.
- Add comments only for non-obvious intent (why a DPR cap, why `ssr: false`), not narration.

---

## When Not To Use

- Pure visual composition / hierarchy / spacing, no 3D → `enhance-web-ui`.
- Greenfield anti-slop landing page → `enhance-web-landing`.
- Generic existing-site premium upgrade (no 3D) → `enhance-web-redesign`.
- UX heuristics / flows / data wiring → `enhance-web-ux`.
- A hover/drag delight that needs no WebGL → `design-motion`.

---

## Research & Foundation Skills

**Foundation / deeper mechanics (in this repo):**
- `design-motion` — Motion / GSAP / CSS animation patterns and physics micro-interactions.
- `audit-performance` — Core Web Vitals (LCP/INP/CLS), bundle analysis.
- `audit-accessibility` — reduced-motion, keyboard, screen-reader compliance.

**Current external anchors:**
- **GSAP is free for all use, plugins included.** Use `useGSAP()` (`@gsap/react`) for React cleanup/Strict-Mode safety. <https://gsap.com/resources/React/>
- **R3F performance docs** — WebGL is expensive on weak devices; design for graceful degradation; mutate refs not state in `useFrame`. <https://r3f.docs.pmnd.rs/advanced/scaling-performance>
- **three.js WebGPURenderer** — production-ready since r171, automatic WebGL2 fallback, `forceWebGL` to test. <https://threejs.org/manual/en/webgpurenderer.html>
- **"100 Three.js Tips That Actually Improve Performance" (2026)** — <100 draw calls, Draco/KTX2, lazy-load below the fold, dispose everything, profile with stats-gl/renderer.info/Spector.js. <https://www.utsubo.com/blog/threejs-best-practices-100-tips>
- **Cinematic 3D scroll with GSAP + Next.js + R3F** — DPR cap, refs for camera values, mobile simplification, reduced-motion, `useGSAP` cleanup, hydration safety. <https://mirax.cc/articles/cinematic-3d-scroll-gsap-nextjs-react-three-fiber>
- **R3F mobile performance (2026)** — Draco + LOD + `OffscreenCanvas`/Web Worker + instancing for stable 60 FPS. <https://www.krapton.com/blog/boosting-react-three-fiber-mobile-performance-in-2026-a-deep-dive-d6105c>
- **Optimizing 3D website performance** — device-tier detection, IntersectionObserver pause, static fallback for no-WebGL. <https://svilenkovic.com/3d/how-to-optimize-3d-website>

- **`references/css-canvas-effects.md`** — CSS, SVG and Canvas 2D effect patterns to use when Three.js / R3F is overkill.

> Adapted and generalized from the `web3d-integration-patterns` meta-skill in
> [freshtechbro/claudedesignskills](https://github.com/freshtechbro/claudedesignskills)
> (and its `threejs-webgl` / `gsap-scrolltrigger` / `react-three-fiber` /
> `motion-framer` / `react-spring-physics` foundation skills) into an
> audit-first, repo-elevation skill in the `enhance-web-*` family.
