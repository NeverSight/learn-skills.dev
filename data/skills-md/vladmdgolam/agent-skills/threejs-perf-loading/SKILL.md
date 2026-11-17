---
name: threejs-perf-loading
description: >
  Performance and loading patterns for real-time Three.js/WebGL/WebGPU sites,
  based on modern approaches and best practices explored from top-notch studios
  and developers (Ivress brand site, Threejspunk cyberpunk-rain demo, igloo.inc,
  Noomo Agency showcase) plus live production profiling, rather than generic
  advice. Use when eliminating the loading-spinner-to-scene freeze/jank,
  hiding shader/pipeline compile cost behind a loading screen, designing an
  adaptive-quality or perf-budget system (including hardening it against
  false-positive degrades from transient stalls), attributing unexplained
  slow frames to a named cause (in-app frame-attribution tooling: marks
  buffer, GL-resource deltas, dispose tracer, boot tracer for the pre-mount
  window), auditing hidden render-target allocations in library material
  wrappers, tuning scroll/camera damping so input can't "outrun" a max
  speed, deciding where to spend a render-loop's cost (MRT routing,
  layer-split passes, on-demand shadows, GPU-resident particles, proximity
  gating), or building desktop/mobile quality tiers for
  bloom/post-processing. Complements the generic `three-best-practices` rule
  compendium — this skill is the "how real sites actually hide cost and avoid
  jank" companion, not a restatement of it.
---

# Three.js Performance & Loading Patterns

Patterns drawn from studying modern Three.js/WebGPU production sites built by
top-notch studios and developers, each solving a different piece of "make a
heavy real-time scene feel instant and never stutter." This file distills the
transferable patterns, organized by what problem they solve.

Don't treat any of this as an au-courant checklist to apply wholesale — each
technique below traded something (code complexity, a stubbed physical
behavior, a hard cutoff) for its win. Read the "cost" note on each one before
copying it.

## 1. Loading & warmup — hide compile/decode cost behind the spinner

The classic symptom this section solves: loading bar hits 100%, then a 1-2
second freeze before the scene appears. That freeze is (almost always) the
GPU driver compiling shader pipelines on first use — WebGL/WebGPU compile
lazily, per unique material/uniform combination, the first time it's drawn.
If your loading screen only waits for asset *fetch*, you've hidden network
latency but not compile latency.

**Fix: force every pipeline to compile while the loading UI is still up, by
actually rendering through it once.** (Source: `ivress-brand-site-teardown.md`)

```js
// Simplified from the ivress renderer's warmup phase.
class WarmupRenderer {
  async runWarmupFrame(camera) {
    // 1. Activate the section/state whose materials you're about to warm.
    this._activateSection(this.warmupSectionIndex);

    // 2. Disable frustum culling for this pass — you need EVERY mesh to
    //    actually draw, including ones off-screen from this camera, or its
    //    pipeline never compiles.
    const culled = [];
    scene.traverse((o) => {
      if (o.isMesh && o.frustumCulled) { o.frustumCulled = false; culled.push(o); }
    });

    // 3. Render a handful of real frames through the FULL post-processing
    //    chain (bloom, grade, everything) — not a stripped-down warm pass.
    //    Uncompiled post nodes will still stall on first real use otherwise.
    this.scenePass.camera = camera;
    await this.postProcessing.render();

    culled.forEach((o) => { o.frustumCulled = true; });

    // 4. Advance to the next section/state and repeat until every
    //    section's material set has drawn at least once.
  }

  completeWarmup() {
    this._restoreOriginalState();
    // Wait 2 RAFs + a microtask — let the compositor fully settle —
    // THEN fire the event your loading UI listens for to fade out.
    requestAnimationFrame(() => requestAnimationFrame(() => queueMicrotask(() => {
      emit('compileEnd');   // safe to also start loading non-critical assets now
      emit('reveal', { isIn: true });
    })));
  }
}
```

Key details that make this work, not just "render some frames":

- **Warm every distinct state your scroll/scene narrative visits**, not just
  the first view. Ivress iterates all 6 scroll sections, 3 frames each, plus
  a separate overlay-scene pass — because each section activates different
  materials/uniform branches that compile independently.
- **Force meshes to actually draw** (disable frustum culling for the warm
  pass) — a culled mesh's pipeline never compiles, so warming with the real
  camera framing isn't enough on its own.
- **The reveal event is the gate, not the asset-load event.** Loading UI
  should listen for "compile done", not "assets fetched."

**Per-camera compileAsync, cheaply.** (Source: `threejspunk-teardown.md`,
§4.9) If different cameras render different layer masks (e.g. a dedicated
rain/particle camera vs. the main beauty camera), each layer combination
produces a *different* compiled program — warming the beauty camera doesn't
warm the rain camera's program.

```js
// Two-phase warmup behind the loader.
await renderer.compileAsync(scene, beautyCamera);
// Temporarily hide the expensive stuff so this warm frame is cheap —
// you need the DRAW to happen for compile, not a full-cost frame.
setVisible(heavyObjects, false);
await renderTonePipelineOnce();
setVisible(heavyObjects, true);

// Layer-masked cameras need their own compile — a rain camera with
// layer 2 enabled produces a different program than the beauty camera.
await renderer.compileAsync(scene, rainCamera);
```

Browser-specific note from the same source: Safari's shader compiler is
slower/less async-friendly in practice, so that build makes Safari *await*
the second compile before reveal, while other browsers let it finish in the
background after the intro has already started. Don't assume `compileAsync`
resolving means the pipeline is actually ready on every browser.

**Secondary win: use "compile done" as a general readiness signal.** Once
you have a `compileEnd` event, route non-critical work through it instead of
firing it eagerly at load start — e.g. ivress defers loading secondary SFX
until after warmup, keeping it off the critical path for free.

**Gate the loader's reveal on real rendered frames, not asset progress or
timers.** (Source: live profiling of a shipped transmission-glass R3F site, 2026-08.) The
scene's first-mount block (a Suspense-gated R3F tree constructing hundreds
of objects in one commit) happens *after* every asset-progress signal has
already finished — `useProgress` reaches its final lull while the expensive
mount is still ahead, and any fixed-delay timer is a guess that breaks on
slower machines. Two attempts at timer/progress-based gating both misfired
in production (un-froze too early, or froze permanently via an effect-
cleanup bug). What worked: a `useFrame` *inside* the mounted scene counts
actually-rendered frames and fires a callback at frame ~8 — by definition
past the mount block, no guessing.

```js
// Inside the Suspense-gated scene component:
useFrame(() => {
  if (framesRef.current++ === 8) onSceneFramesReady?.();
}, -999);
```

Companion loader-UX trick: don't hide the loader's content until that
signal — show it immediately but **paused**. CSS `animation-play-state:
paused` on the animated parts freezes them at their first keyframe without
losing phase; un-pausing on the frames-ready signal reads as "the site came
alive," whereas an animation that visibly *stutters* through the mount
block reads as jank, and hidden-then-shown content reads as a broken flash.

**Chunk one-shot procedural synthesis, and schedule it at creation, not
first use.** Anything that fills a large buffer procedurally on the main
thread — a convolution-reverb impulse (a 5s stereo impulse is ~500k samples
with `Math.pow` + `Math.random` each), a noise texture, a generated mesh —
is a guaranteed one-frame stall if it runs synchronously at the moment it's
first needed. Fill it in rAF-yielded chunks (~40k samples/chunk), and kick
the fill off eagerly as soon as its owning context (AudioContext, GL
context) exists, so by first-use time it's normally already done. Keep the
synchronous path only as a fallback for "needed before the chunked fill
finished."

## 2. Render-loop cost discipline

These are ways to make the *steady-state* render loop cheaper, not the
loading path. Source: `threejspunk-teardown.md` almost entirely — it's the
deepest perf-engineering teardown of the four.

**On-demand shadow maps.** For mostly-static scenes (a static city + one sun,
not a dynamic day/night cycle), `shadowMap.autoUpdate = true` re-renders the
shadow map 60×/s for no reason.

```js
renderer.shadowMap.autoUpdate = false;
// Call this explicitly on: init, lighting changes, resize, camera-mode
// switches, any editor/inspector edit. A static scene then renders its
// shadow map a handful of times per session instead of every frame.
function requestShadowMapUpdate(reason) {
  renderer.shadowMap.needsUpdate = true;
}
```

This is one of the single biggest wins available for a static-lighting scene
and costs nothing when the scene genuinely doesn't need per-frame shadows.

**MRT your emissive channel so bloom is selective by construction.** Instead
of thresholding a blurred beauty pass to guess what should glow, write
emissive contribution to its own MRT target and have bloom read *only* that
target.

```glsl
// Main pass fragment shader, conceptually:
layout(location = 0) out vec4 outColor;
layout(location = 1) out vec4 outEmissive;
// ...
outColor = vec4(litColor, 1.0);
outEmissive = vec4(emissiveColor, 1.0);
```

Bloom then samples `outEmissive` exclusively — neon/glow elements bloom hard
without washing out non-emissive bright surfaces, and there's no threshold
tuning fighting your beauty pass's actual brightness range.

**Layer-split passes for effects that need their own culling/outputs.**
Rain/particles/anything that wants a different MRT output (e.g. a
screen-space refraction offset) than the main scene: put it on its own
render layer, give it a dedicated camera synced to the main one, and disable
that layer on the beauty camera (and vice versa).

```js
rainCamera.layers.set(RAIN_LAYER);
beautyCamera.layers.disable(RAIN_LAYER);
// beauty pass never draws rain; rain pass draws ONLY the ~1-9k particle
// sprites, nothing else — and can emit its own MRT channels (e.g. a
// per-drop UV offset for "refraction behind the rain drop") for free.
syncCameraTransforms(rainCamera, beautyCamera);
```

**GPU-resident particle motion — zero CPU per-frame cost.** Don't update
particle positions on the CPU and re-upload. Compute position from a time
uniform inside the vertex/compute shader instead.

```glsl
// Rain drop Y position wraps in-shader; CPU only advances a single
// uniform per frame, regardless of particle count.
float y = mod(vAttrY - uTime * uSpeed * vRandSeed, uCylinderHeight);
```

Pair with `frustumCulled = false` (the particle volume is usually
camera-parented anyway, so per-object bounds checks are wasted work) and a
hand-set bounding sphere on GPU-driven emitters so culling stays meaningful
where it *is* used.

**Proximity + hysteresis gating.** Anything expensive that's only visually
relevant near the camera (a "wet car surface" shader layer, a playing video
texture) should fade/disable based on distance, with separate enter/exit
thresholds to avoid flicker at the boundary:

```js
// Two different thresholds, not one — prevents boundary flapping when
// the camera hovers near a single cutoff distance.
const fadeStart = 20, fadeEnd = 32; // wetness layer
const playDist = 20, pauseDist = 50; // billboard video (bigger gap = more hysteresis)
```

**Fuse your post-processing into as few passes as possible.** A grade chain
(fog → tint → saturation → contrast → chromatic aberration → vignette →
grain) written as one fused fragment node/shader is one full-res read/write
instead of five-plus separate passes each re-reading and re-writing the
full framebuffer. Reserve genuinely separate passes for things that need a
different resolution (bloom mips) or a different input (a blurred capture
buffer) than the main grade.

**Re-link the post graph, don't rebuild it, when toggling features.**
`post.outputNode = newGraph; post.needsUpdate = true` on toggle, rather than
constructing/destroying pass objects. A disabled branch that was never
linked in costs nothing; a materially-different graph gets a single relink
instead of teardown/rebuild churn. The R3F flavor of the same rule:
`@react-three/postprocessing`'s `<EffectComposer>` rebuilds its ENTIRE pass
list — disposing and re-creating the fused EffectPass's depth texture and
render targets — whenever the `children` prop identity changes. The effects
array must be a `useMemo`, with conditionals gated so disabled features
can't change the array identity; an inline-rebuilt array cost 100-386ms per
re-render frame in Safari on a production site. Same class of bug one level
down: an effect constructed in a `useMemo` whose deps include `size`/`dpr`
gets a fresh identity on every resize — mutate the existing effect's
resolution-dependent internals in a `useLayoutEffect` instead of
reconstructing it.

**Audit hidden render-target allocations in library material wrappers —
especially across remounts.** (Source: live profiling of a shipped
transmission-glass R3F site, 2026-08.) Library convenience components can allocate real GPU
resources you never use: drei's `<MeshTransmissionMaterial>` unconditionally
creates two `useFBO` render targets per instance, even when
`transmissionSampler` or a custom `buffer` means they're never read. Worse,
drei's `useFBO(n)` called with a single number sizes WIDTH to `n` but
defaults HEIGHT to the full viewport — so "minimizing" the resolution prop
to 16 still allocates a real 16×viewport-height target per material. When
~24 shell materials remounted together (a `key` flip on a mode change),
disposing + reallocating those always-unused targets cost a measured
**936ms single frame**. Fix was a trimmed local copy of the component with
the FBO allocation deleted (shader/uniform code kept verbatim so existing
`onBeforeCompile` string patches still match). The general rule: any
`key`-driven remount of a material/component family disposes and re-creates
its GPU resources in one frame — before shipping a mode-flip `key`, check
what each instance actually allocates (a dispose-tracer with call-site
stacks makes this a 5-minute question; see §6).

## 3. Adaptive quality — degrade predictably, don't chase every frame

**Put your whole perf budget in one flat config object.** Every expensive
subsystem gets a resolution scale, a frame-skip, and/or a kill switch —
not scattered `if (isLowEnd)` checks through the codebase.

```js
const perfBudget = {
  adaptiveDpr: true, maxPixelRatio: 1.5,
  groundReflection: true, groundResolutionScale: 0.5, groundReflectionFrameSkip: 1,
  bloom: true, bloomResolutionScale: 0.5,
  dof: false,                    // expensive effects can just ship OFF by default
  smokeEnabled: true, exhaustCount: 50, ambientCount: 40,
};
```

The single flat object doubles as your debug/console API surface (expose
`app.perf.set('groundReflection', false)`) and your tuning-panel bindings —
one source of truth for every perf decision in the app.

**Latch degradation one-way; don't ratchet it every frame.** Sample FPS
over a rolling window (not every frame — that's noisy). On sustained bad
frames, drop quality once and *stay there* rather than continuously
adjusting up and down, which reads as visual flickering/instability.

```js
// Sample once per second, only AFTER the reveal — sampling during the
// loading/intro sequence means intro hitches poison your baseline.
if (allowAdaptiveSampling && twoConsecutiveWindowsBelow(50 /* fps */)) {
  forcedLow = true;                 // one-way latch, never auto-clears
  renderer.setPixelRatio(0.85);     // one deliberate step down, not a ramp
  disable(['dof', 'lensflare', 'billboardVideos']);
}
```

**The naive version of that sampler fires false positives in production —
four hardening rules.** (Source: trace analysis on the same shipped R3F site,
2026-08 — a deployed monitor built exactly to the pattern above permanently
dropped DPR because of a ~2s post-intro transient, then later nuked the
whole material tier on a 3-frame click stall. Both were confirmed false
positives: steady-state fps was fine before and after each trigger.)

1. **"Armed after the reveal" is not enough — discard the first 2-3 windows
   after arming too.** The reveal gate protects against the intro's *own*
   heavy frames, but whatever settles immediately after it (audio start,
   camera handoff, HUD reveal, deferred mounts) lands squarely in the first
   sampled windows. The observed failure: first two post-arm windows at
   45-47fps → degrade fires → 56-59fps for the next 18 seconds.
2. **A window's aggregate FPS cannot distinguish "sustained bad pacing"
   from "two huge one-off frames ate the window's budget."** A 3-frame
   570ms click transition inside a 1s window reads as 24fps. Track
   per-frame deltas and *discard* (not count either way) any window
   containing a frame slower than ~100ms — a one-off stall is a transition,
   not evidence about steady-state cost.
3. **Stage the degrade, cheapest lever first — because the degrade event
   is itself a hitch.** Swapping DPR + material mode + MSAA + composer
   config in one commit rebuilds every material and resizes every render
   target: a measured degrading session showed 794ms total GC (max 138ms)
   vs 354ms (max 25ms) in a pinned-tier session of the same length. The
   hitch can push FPS down enough to look self-reinforcing. Level 1 = DPR
   only (resizes targets, rebuilds nothing); level 2 = full tier drop. And
   skip evaluating the 1-2 windows right after each escalation, or the
   degrade's own hitch counts toward the *next* escalation.
4. **Gate escalation on the cheaper lever having measurably failed.**
   Remember the fps that triggered the last escalation; if a new bad streak
   arrives with fps clearly *better* than that, the cheap lever worked and
   the new dip is a fresh transient — don't escalate. Without this gate,
   the same 2-bad-windows counter that justified "drop DPR" will later
   justify "drop the whole material tier" on any unrelated hiccup, trading
   your hero visual feature for nothing (observed: fps unchanged at 35-36
   before and after the material drop — the scene wasn't fill-bound, which
   the DPR step had already proven, and the escalation ignored that
   evidence).

Also: freeze/suspend the adaptive monitor for the duration of any benchmark
run — a mid-run degrade swaps the workload under the measurement and the
numbers become a useless blend of two tiers. And pin the first GPU-tier
classification in localStorage: detect-gpu is not deterministic across
reloads on privacy-masked GPUs, and a tier that flaps between reloads means
the site looks different every other visit.

**UA-based feature gating at boot**, separate from backend/capability
detection — some things you want off on mobile Safari specifically (not
just "any WebGL2 fallback"), because it's a known-bad combination rather
than a measured capability gap:

```js
if (isMobile()) disable(['lensflare', 'billboards']);
if (isMobile() && (isIOS() || isSafari())) { maxPixelRatio = 1; adaptiveDpr = false; disable('smaa'); }
if (isSafari()) { disable('dof'); timestampQueriesOff = true; } // desktop Safari too
```

**Desktop/mobile as genuinely different post-processing tiers, not just a
DPR cap.** The Noomo teardown's clearest example: desktop runs a full
depth-aware raymarched volumetric glow (7 samples, 3D noise, view-ray
reconstruction from depth) as its bloom's atmosphere; mobile replaces that
entire pass with a flat blue-tint multiply on the same underlying bloom
texture — same visual identity, no depth reconstruction, no raymarch, no 3D
noise sampling at all on mobile.

```js
// Desktop: raymarch a volume mask from depth + noise, tint, composite.
// Mobile: reuse the SAME multi-mip bloom result, skip the raymarch:
mobileBloom = bloomTexture * tintColor * 0.05; // much smaller multiplier too
outputColor += mobileBloom;
```

## 4. Scroll/input smoothing — cap the step, not the value

**The primitive: clamp the per-frame step of a damped lerp, not the target
value itself.** (Source: `igloo-inc-teardown.md`) A plain lerp toward a
target can close an arbitrarily large gap in one frame if the raw input
delta is huge (a hard mouse-wheel notch, unlike inertia-smoothed trackpad
deltas, can do exactly this). Clamping the *step* guarantees a hard
"can't-outrun-this-speed" ceiling regardless of how large the input jump was.

```js
function lerpFPSLimited(current, target, lerpFactor, maxSpeed = Infinity) {
  const naive = lerpFPS(current, target, lerpFactor);      // normal frame-rate-independent lerp
  const maxStep = maxSpeed * deltaTimeRatio;                // scale by dt vs. reference frame time
  const step = clamp(naive - current, -maxStep, maxStep);   // clamp the STEP
  return current + step;
}
```

If you're in the R3F/drei ecosystem, you likely don't need to hand-roll
this: `<ScrollControls damping maxSpeed>` uses `maath`'s `easing.damp`
under the hood, which is the same `maxChange = maxSpeed * smoothTime`
step-clamp. **Gotcha found in practice:** `maxSpeed` there is
offset-units/second over the *whole* scroll rail — a value that looks
reasonable on paper can still let one hard wheel notch close most of the
rail in under a second. Tune low enough that catch-up takes multiple
seconds regardless of raw input size, and verify with an actual hard
mouse-wheel notch (not just trackpad), since that's the input that exposes
an under-tuned cap.

**When "snappy" beats "smooth": scrub an authored timeline directly instead
of layering extra damping on top.** (Source: `noomo-showcase-teardown.md`)
If your camera/object motion comes from an authored animation clip (GLB,
timeline, whatever), consider driving it directly from smoothed scroll
progress with *no second damping layer* on top:

```js
// Smooth the DOCUMENT scroll once (e.g. GSAP ScrollSmoother), then map
// progress straight onto clip time — no additional lerp/spring on the
// camera/object motion itself. The authored curve supplies its own easing.
clip.time = clip.duration * smoothedScrollProgress;
```

The comparison that surfaced this: a scroll rail with multiple smoothing
layers stacked (target lead → capped velocity → filtered offset → rubber-
band → snap detection → the renderer's own damping) reads as soft/delayed
compared to one that only smooths the input once and lets the authored
curve's own easing carry the rest. More physical layers isn't automatically
better — it's a trade between "rich interactive rail" and "immediate,
authored feel." Pick based on whether your motion is a fixed narrative
(favor direct scrub) or a live-navigable space (favor the damped rail, and
budget for it reading softer).

## 5. Transmission/glass-specific: own your render target

(Source: `igloo-inc-teardown.md`, `refraction` project comparison in the
same doc.) Three.js's built-in `MeshPhysicalMaterial` transmission
auto-manages its `transmissionRenderTarget` internally — convenient, but it
removes your ability to make per-frame decisions about whether a live
capture is worth its cost this frame.

```js
// Hand-rolled transmission material owns its RT explicitly:
this._transmissionRT = new THREE.WebGLRenderTarget(w, h, { generateMipmaps: true });

update(renderer, scene, camera) {
  if (!this.isInFocus) {
    // Skip the live capture entirely — feed a cheap static texture instead.
    this.uniforms.tTransmissionSamplerMap.value = this._staticFallbackTex;
    return;
  }
  renderer.setRenderTarget(this._transmissionRT);
  renderer.render(scene, camera);
  this.uniforms.tTransmissionSamplerMap.value = this._transmissionRT.texture;
}
```

The bigger, more transferable lesson from directly comparing this against a
pre-blurred-shared-buffer approach: **the cheapest transmission sample is
one that never recomputes a mip/bicubic filter per fragment at all.**
Pre-blurring once into a shared buffer (a Kawase pyramid or equivalent) and
doing a single flat `texture2D` tap at draw time beats even a
hand-optimized `textureLod` hot path, because the blur cost is paid once
for the whole scene rather than once per glass fragment. Owning the RT is
what *enables* the fallback-to-static trick, but the shared-pre-blurred-
buffer architecture is the actually-cheaper one if you're rendering more
than one piece of glass.

**Not worth copying**, found by directly A/B-comparing against a
production glass pipeline: stubbing out Beer's-law attenuation (`return
vec3(1.0)`) saves a handful of ALU ops per fragment — free on any modern
GPU — while losing an authored depth-of-absorption cue. Same for a hard
`totalDiffuse = transmitted.rgb` overwrite instead of `mix()`: saves one
`mix()` call, breaks partial-transmission blending. Cheap-looking
shader-math deletions are rarely where the real cost is; profile before
assuming a stubbed-out term is a meaningful win.

## 6. Frame attribution tooling — instrument before optimizing

(Source: live profiling of a shipped transmission-glass R3F site, 2026-08.) DevTools timelines
answer "was this frame slow"; they're bad at answering "which of MY systems
did it" — and profiler overhead itself inflates Safari frame times enough
that attribution runs and measurement runs must be separate runs. A small
in-app attribution layer, behind a URL flag, turns "unexplained 300ms
frame" into a named cause in one capture. The pieces that earned their
keep, all ~free when the flag is off:

- **A per-frame marks buffer.** A module-level `string[]`; any system doing
  bursty work pushes a tag (`markDevFrame('composer-mount')`). One logger
  (a low-priority `useFrame`) reads + clears it once per frame and reports
  slow frames WITH their tags. Two gotchas found the hard way: the clearing
  must be gated on *collection* being enabled (not on console-logging) — a
  collect-but-never-clear misconfiguration makes every frame report
  cumulative session history instead of its own work. And attribution must
  go into the *persisted* buffer, not just `console.warn` — otherwise a
  no-DevTools capture (a phone) has timings with no causes.
- **Timed spans for always-on per-frame work** (`begin/endDevFrameSpan`
  with a ~0.5ms report floor) instead of bare marks — a bare mark on an
  every-frame system tags every slow frame and blames work that cost
  microseconds.
- **A GL-resource delta sampler.** Once per frame, diff
  `gl.info.programs.length` / `memory.textures` / `memory.geometries`, and
  name every NEW program the moment it appears (check by program identity,
  not count — an evict-then-recompile keeps the count equal). This is what
  identifies which material compiles mid-run instead of during warmup.
- **A dispose tracer with call-site stacks.** Patch
  `Texture.prototype.dispose` / `WebGLRenderTarget.prototype.dispose` to
  record what was disposed (constructor name, dimensions) and a trimmed
  `new Error().stack`. This is the tool that turned "936ms mystery frame"
  into "24 never-used 16×viewport FBOs disposed by a material remount"
  (§2) in one capture.
- **A boot tracer that starts before your framework mounts.** Any logger
  living inside the scene tree (an R3F `useFrame`) is structurally blind to
  the loader period, first mount, and asset loading — exactly where load
  freezes get reported. A plain module-scope `requestAnimationFrame` loop,
  started at import time behind the URL flag, records every frame's delta +
  the marks buffer from navigation onward, and exports one JSON blob
  (frames + `performance.mark/measure` snapshots + UA/DPR/viewport) via a
  download button — a complete no-DevTools capture pipeline for phones.
- **React commit attribution** (if React): `<Profiler>` boundaries around
  the canvas tree and DOM tree separately (they're separate reconciler
  roots — one Profiler can't see both), reporting commits over ~30ms into
  the same marks buffer.

The negative result is a result: once marks, GL deltas, disposals, AND
commits are all instrumented and a slow frame still reports nothing, you've
proven it's GC or GPU-driver work — invisible to JS by elimination — and
can stop adding marks and change strategy (allocation audit, GPU-level
profiler) instead of guessing.

## Source material

Distilled from four case studies of shipped sites (Ivress brand site,
Threejspunk cyberpunk-rain demo, igloo.inc, Noomo Agency showcase), plus
live production profiling of a transmission-heavy R3F site (2026-08) —
the source of §6 and the adaptive-quality hardening rules, the loader
frames-ready gating, the remount/FBO disposal findings, and the
EffectComposer identity invariant, all measured with the §6 tooling rather
than inferred. No raw teardown docs are bundled with this skill — they're
working notes, not polished references, and live outside this repo. If you
need the original code excerpts or want to go deeper on one pattern than
this summary allows, ask the user where their source teardowns for these
sites live.

Reach for `three-best-practices` (if installed) for generic setup/memory/
draw-call/geometry/material/asset-compression rules — this skill doesn't
restate those.
