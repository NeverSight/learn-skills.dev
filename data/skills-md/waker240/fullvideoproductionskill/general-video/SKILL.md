---
name: general-video
description: Build a custom HyperFrames video when no specialized workflow fits, including freeform multi-scene pieces, loops, reels, and title cards.
compatibility: Requires sibling skills from this pack, a local filesystem and shell, Node.js 22.20.0+, and FFmpeg/ffprobe for media work. Generation providers and desktop tools are optional, separately configured capabilities.
---

<!-- Public portability adaptation, 2026-09-26. -->

Install this skill with its sibling skills. See [runtime setup and capability boundaries](../hyperframes/references/install-portability.md) before executing commands. User instructions and the requested production stage take precedence over workflow defaults.

# general-video — general video workflow

For a complete narrated film, a mixed-media explainer, or user scene/audio review, use `/hyperframes`' studio pipeline and [review-driven-production.md](../hyperframes/references/review-driven-production.md). This freeform route remains useful for custom pieces; it must not bypass narration timing, versioned review, final assembly or the requested audit loops. Current explicit instructions and review choices supersede stale design files.

> **Confirm the route before you build.** This is the **fallback** for custom composition authoring. If the input clearly fits a specialized workflow, prefer it: marketed product → `/product-launch-video`; general site → `/website-to-video`; topic explainer → `/faceless-explainer`; GitHub PR → `/pr-to-video`; existing footage → `/embedded-captions` · `/talking-head-recut`; short unnarrated motion graphic → `/motion-graphics`; Remotion port → `/remotion-to-hyperframes`. **Out of scope**: live / at-render-time data, NLE-style editing of a finished video, or producing footage HyperFrames can't capture. Unsure? **Read `/hyperframes` first.**

Set the installed skill path before any command below. The direct commands work in legacy projects; use the shorter `npm run audio:discover` / `npm run fast:check` aliases only after canonical HyperFrames scaffold/refresh has installed them.

```bash
HYPERFRAMES_DIR="/absolute/path/to/installed/hyperframes"
```

> **Frozen media:** Every rendered BGM, SFX, image, or icon resolves to a reviewed project-local file. For audio candidates, run `node "$HYPERFRAMES_DIR/scripts/audio-discover.cjs" --type bgm --query "<job>"` or `--type sfx`; audition and rights-check one result, then use `/media-use` to resolve/freeze it. Discovery never approves an asset or supplies a render path.

**Build exactly what was asked.** A title card is a title card — not a title card + three supporting scenes + ambient music + captions. If extra scenes or elements would genuinely improve the piece, _propose_ them; don't add them silently. For small edits (fix a color, adjust one duration, add one element), skip the planning steps and go straight to the build.

## Approach

### Discovery — open-ended requests only

For vague, exploratory requests ("make something for our brand", "a cool intro") — understand intent before picking colors:

- **Audience** — who watches? developers / executives / general consumers?
- **Platform** — where does it play? social (15s) / website hero / product demo / internal?
- **Priority** — what matters most? motion quality / content accuracy / brand fidelity / speed?
- **Variations** — one best shot, or 2-3 meaningfully different options (different pacing, energy, or structure — not just color swaps)?

For specific requests ("add a title card", "fix the timing on scene 3"), skip discovery.

### Step 1 — Design system → `hyperframes-creative`

Establish the visual identity first. Read the current brief and review decisions, then reconcile existing `frame.md`, `design.md` and `DESIGN.md`; file naming alone does not make an older palette authoritative. Keep semantic colors/fonts consistent while allowing deliberately approved light/dark or material registers by scene.

**If no spec exists, read `hyperframes-creative/references/house-style.md` and `hyperframes-creative/references/video-composition.md` before choosing the design.** Use their hierarchy, scale, layers and material guidance to serve the subject. Metadata, texture and extra elements earn their place; there is no minimum object count. A simple narration-led comparison can be correct, while an elaborate flat card layout can still fail. For a named reference or repeated correction, use `hyperframes-creative/references/reference-led-direction.md` before batch production.

**Find the angle (vague brief, no spec):** before picking colors, write ONE sentence — what does this name/word/topic evoke, and what visual _world_ (metaphor, setting, instrument, motif) expresses it? E.g. a cybersecurity tool → vault doors / perimeter scan lines / lock tumblers; a meditation app → tide, breath, slow light bloom. Read the _meaning_ of the subject, not just its letters; pick a concrete angle over a literal restyle. This is the cheap substitute for prompt expansion (Step 2) on single-scene pieces, where expansion is correctly skipped — and it is the difference between a designed concept and a generic logo-on-a-gradient.

<HARD-GATE>
Before writing ANY composition HTML, verify you have ALL FOUR:
1. **A visual identity** grounded in the brief and current review choices; the house-style reference is one optional vocabulary, not a mandated palette.
2. **A one-sentence concept angle** (the "find the angle" step) for anything beyond a trivial edit — not a literal restyle of the prompt words.
3. **Deliberately chosen, available fonts** with the required glyphs and rights; embed project font files where consistent rendering requires it. User typography choices take precedence.
4. **A hierarchy/density plan from `video-composition.md`** — one clear focus, purposeful layers and a visible state/attention change. Use foreground, metadata or texture where meaningful; do not add decorative content to satisfy a count.
</HARD-GATE>

### Step 2 — Prompt expansion → `hyperframes-creative`

Run for every multi-scene composition (skip for single-scene pieces and trivial edits). Ground the request against the design spec + house style into a consistent intermediate that downstream work reads the same way. See `hyperframes-creative/references/prompt-expansion.md`.

### Step 3 — Plan

Before writing HTML, think at a high level:

1. **What** — the viewer experience: narrative arc, key moments, emotional beats.
2. **Structure** — how many compositions, sub-comp vs inline, which tracks carry video / audio / overlays / captions. For the monolithic-single-file vs modular-sub-comp call, see `hyperframes-core/references/composition-patterns.md` § Two Architectures (rule of thumb: ≥3 hard scene cuts, or any reused scene → modularize; a short single-scene piece stays one file).
   - If 3+ beats depend on one relationship geography, exact revisitation, or overview→detail→return, consider a **Spatial Canvas** before splitting them into scenes. First record the canonical `## Spatial Canvas admission` in project-root `DESIGN.md` with one explicit `PASS` or `USE` plus a concrete rationale; a higher-precedence imported `frame.md` / `design.md` remains brand truth but does not replace this executable admission. Read `hyperframes-creative/references/spatial-canvas.md`; only for `USE`, instantiate `hyperframes/templates/SPATIAL_CANVAS.example.json` as `SPATIAL_CANVAS.json` and `hyperframes/templates/DIRECTION.md` as `DIRECTION.md`. Adapt the scope, exact owner composition, host-local route, and excursion windows before building; keep the full route with one composition owner.
3. **Rhythm** — name the pattern before implementing (e.g. `fast-fast-SLOW-SHADER-hold`); see `hyperframes-creative/references/beat-direction.md`. When `momentum`, `temporal-compression`, `overwhelm`, or `panic-rupture` defines a bounded passage, read `hyperframes-creative/references/fast-paced-editing.md` and lock its baseline → escalation → peak → release/reorientation prose plan rather than treating “fast” as a style preset. Record its canonical PASS/USE admission and plan under `## Fast-paced passage admission` in project-root `DESIGN.md`; a higher-precedence imported brand spec remains brand truth, while `DESIGN.md` owns this executable admission. After the narration clock and `index.html` ownership windows are exact, instantiate `hyperframes/templates/FAST_PASSAGES.example.json` as project-root `FAST_PASSAGES.json`, then run `node "$HYPERFRAMES_DIR/scripts/check-fast-passages.cjs" --root . --sync-clock` and `node "$HYPERFRAMES_DIR/scripts/check-fast-passages.cjs" --root .`. Repeat both after any timing or ownership change.
4. **Timing** — which clips drive duration, where transitions land, the pacing.
5. **Layout** — build the end state first (see below).
6. **Animate** — then add motion via `hyperframes-animation`.

## Layout Before Animation

Position every element where it sits at its **most visible moment** — fully entered, correctly placed, not yet exiting. Write that as static HTML + CSS first. **No GSAP yet.**

**Why:** if you position elements at their animated start state (offscreen, scaled to 0, opacity 0) and tween to where you _think_ they land, you are guessing the final layout — overlaps stay invisible until render. Build the end state first and you see and fix layout problems before adding motion.

1. **Identify the hero frame** for each scene — the moment the most elements are simultaneously visible. That is the layout you build.
2. **Write static CSS** for that frame. The content container must fill the scene with padding, not absolute offsets:

```css
.scene-content {
  display: flex;
  flex-direction: column;
  justify-content: center;
  width: 100%;
  height: 100%;
  padding: 120px 160px; /* padding positions content; fills any scene size */
  gap: 24px;
  box-sizing: border-box;
}
```

Never use `position: absolute; top: Npx` on a content container — it overflows when content is taller than the space. Reserve absolute positioning for decoratives.

> ⚠ **The `width/height: 100%` above only resolves if every ancestor has a resolved height.** The root `<div data-composition-id>` and any wrapper between it and `.scene-content` must be sized (`position: relative; width: 1920px; height: 1080px` on the root — see `hyperframes-core` → "Root must be sized"). Skip this and the flex container collapses to ~0, content piles into the **top-left corner**, and the first glyph clips at x=0 — while `lint`/`inspect` still report 0 issues. And **always keep the `padding`** (≥80px) on `.scene-content`: it is the title-safe margin. Never replace it with bare `gap`.

3. **Add entrances** — animate FROM offscreen/invisible TO the CSS position with `gsap.from()` (in sub-compositions prefer `gsap.fromTo()` so the start state is explicit; see `hyperframes-core/references/sub-compositions.md`). The CSS position is ground truth; the tween is the journey to it.
4. **Exits are transition-handled** — per the scene-transition rules in `hyperframes-animation/transitions/`, only the **final** scene animates elements out; between scenes the transition IS the exit.

**Shared space across time:** if element A exits before element B enters in the same area, both still need correct CSS positions for their respective hero frames — timeline ordering keeps them from coexisting, and the layout step catches accidental overlap. Layered glows/shadows and z-stacked depth are _intentional_ overlap; the step is about catching _unintentional_ collisions (two headlines on top of each other, content bleeding off-frame).

**Spatial Canvas exception:** the viewport still fills and clips the output frame, but its `.world` wrapper is intentionally oversized and may use absolute authored world coordinates. Build and judge the static end state at every manifest camera stop; safe margins, density, and caption clearance apply after the camera transform, not to offscreen world content. One camera writer owns the world transform.

For sequence/spine scope, assemble exactly one `data-hf-spatial-host="<id>"` in `index.html` for the owner's full local route. External excursion compositions are distinct sibling mounts above it and cover their full globalized `at` / `duration` windows; the persistent world remains mounted underneath. An internal excursion instead uses one direct-root native clip in the owner with the exact local window and `data-hf-spatial-excursion` marker. Scene scope still needs one `index.html` host unless the marked root is `index.html`.

## Build — delegate to the domain skills

This maps the skill's full surface (see the `description`) to its references — non-exhaustive; when an intent isn't listed, route through `hyperframes-creative` (look/concept), `hyperframes-animation` (motion), `hyperframes-core` (contract), `hyperframes-media` (audio/captions). **The first row is ADDITIVE — read it AND your intent row, not one or the other.**

| Building…                                                             | Read first (in order)                                                                                                                                                                                |
| --------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **ALWAYS — every non-trivial piece, on top of your intent row below** | `hyperframes-creative/references/house-style.md` + `hyperframes-creative/references/video-composition.md` (also gated in Step 1 / HARD-GATE; the "produced, not generated" foreground detailing)                          |
| **Kinetic typography / text-forward**                                 | `hyperframes-animation/techniques.md` (kinetic type) + `adapters/gsap-easing-and-stagger.md` + `rules/kinetic-beat-slam.md`                                                                          |
| **Fast-paced passage / montage / overwhelm / panic**                  | `hyperframes-creative/references/fast-paced-editing.md` first, then the transition/rule/blueprint mechanics it maps to                                                                              |
| **Title card / lower-third / overlay / PiP / text-behind-subject**    | `hyperframes-creative/references/composition-patterns.md` + (for the centered/sized frame) `hyperframes-core` → "Root must be sized"                                                                 |
| **Logo / brand-mark reveal**                                          | `hyperframes-animation/rules/svg-path-draw.md` (draw-on) + `rules/3d-text-depth-layers.md` + `rules/scale-swap-transition.md`                                                                        |
| **Data / stats / numbers**                                            | `hyperframes-animation/rules/counting-dynamic-scale.md` + `rules/stat-bars-and-fills.md` + `hyperframes-creative/references/data-in-motion.md`                                                       |
| **Product / app / UI demo**                                           | `hyperframes-animation/rules/3d-page-scroll.md` + `rules/cursor-click-ripple.md` + `rules/press-release-spring.md`                                                                                   |
| **Audio-reactive / music-driven**                                     | `hyperframes-creative/references/audio-reactive.md` (pre-extract bands; map to motion)                                                                                                               |
| **Narrated / voiceover / music / SFX / captions**                     | `hyperframes-media` → the shared audio engine `scripts/audio.mjs` (one call = TTS + BGM + SFX → `audio_meta.json`); caption authoring + asset placement via `hyperframes-core`. See **Audio** below. |
| **Multi-scene / transitions**                                         | `hyperframes-animation/transitions/overview.md` **then** `transitions/catalog.md` (you are not done after the overview — the GSAP recipe is in the catalog)                                          |
| **Modular / sub-compositions**                                        | `hyperframes-core/references/composition-patterns.md` + `hyperframes-core/references/sub-compositions.md`                                                                                                             |
| **Spatial Canvas / evidence wall / relationship map / cutaway-return** | `hyperframes-creative/references/spatial-canvas.md` → `hyperframes-core/references/spatial-canvas.md` → `hyperframes-animation/blueprints/spatial-canvas.md` (one-way only: `spatial-pan-stations.md`) |

### Audio: one engine (TTS · BGM · SFX)

Only when the piece calls for it (per "build exactly what was asked" — no ambient music on a title card). Don't hand-roll TTS or vendor a copy: write a neutral `audio_request.json` and call the shared engine in `hyperframes-media`. The bundled engine implements Fish synthesis; it does not dispatch other providers. Respect an explicitly chosen provider or supplied audio through the [recorded-VO route](../hyperframes/references/pipeline.md). Read packaged Fish setup for a Fish run; never silently change the user's provider or copy credentials into project data.

BGM and SFX are not searched, retrieved, or generated by the engine. Discover local catalog candidates with `node "$HYPERFRAMES_DIR/scripts/audio-discover.cjs" --type bgm --query "<semantic job>"` or `--type sfx`; inspect source/license/hash, audition each selection, then resolve/freeze the exact reviewed file through `/media-use`. Pass only the resulting project-local paths (or SFX names backed by the project's reviewed local manifest). Full flag list and request/meta schema live in the header comment of `hyperframes-media/scripts/audio.mjs`.

```jsonc
// audio_request.json — one line per narrated segment; `id` is yours (joins audio_meta back)
{
  "lang": "en",
  "lines": [
    {
      "id": "s1",
      "text": "Your opening line.",
      "sfx": [{ "path": "assets/sfx/whoosh-soft.wav", "offset_s": 0.15, "volume": 0.35 }]
    },
    { "id": "s2", "text": "The next beat." },
  ],
  "bgm": { "path": "assets/bgm/reviewed-underscore.mp3", "volume": 0.16 },
  "sfx_manifest": "assets/sfx/manifest.json"
}
```

```bash
# <MEDIA_DIR> = the installed hyperframes-media skill dir (sibling of this skill)
node <MEDIA_DIR>/scripts/audio.mjs --request ./audio_request.json --hyperframes . --out ./audio_meta.json
```

Then read `audio_meta.json`: mount each `voices[].path` + (`bgm.path`, `sfx[]`) as `<audio>` tracks and use `voices[].words` for captions, all per `hyperframes-core` (audio tracks + caption authoring). The command is complete when it exits: there is no pending background-music job or later wait step.

When narration or another master clock changes an admitted Spatial Canvas, retime every visit and excursion `at` / `duration` / `reviewAt` in the owner's local host window before assembly. Preserve route order, semantic poses, exact/reorient tickets, and mutations; update the owner root duration and, when mounted, its host duration together. For every internal excursion, update its native clip `data-start` / `data-duration` to the same retimed manifest window before running the checker.

## Output checklist → `hyperframes-cli`

Set the requested master path before the final encoded review:

```bash
MASTER_VIDEO="renders/video.mp4" # only after a render was requested
```

- [ ] `npx hyperframes lint` and `npx hyperframes validate` pass (block on results)
- [ ] design adherence verified if a spec (`frame.md` / `design.md`) exists — checklist in `hyperframes-creative/references/design-adherence.md`
- [ ] `npx hyperframes inspect` passes, or every overflow is intentionally marked
- [ ] contrast warnings addressed; for multi-scene work, review the animation map (`hyperframes-animation/scripts/animation-map.mjs`)
- [ ] when the active design artifact or `DIRECTION.md` marks a fast passage: render/watch its full lead-in → escalation → peak → release at final fps with sound; verify comprehension, eye-trace, caption/voice intelligibility, reorientation, and restrained luminance changes
- [ ] when `FAST_PASSAGES.json` exists: run `node "$HYPERFRAMES_DIR/scripts/check-fast-passages.cjs" --root .`; if narration/timing/ownership changed, run the same command with `--sync-clock` first
- [ ] when `SPATIAL_CANVAS.json` exists: confirm one marked owner and its unique assembled host (or the one allowed root-owned scene), then run `node "$HYPERFRAMES_DIR/scripts/check-spatial-canvas.cjs" --root .` and `node "$HYPERFRAMES_DIR/scripts/snap.cjs" --root . --spatial`
- [ ] fill one exact `DIRECTION.md` row for every `<canvas-id>:<visit-id>` and `<canvas-id>:excursion-<excursion-id>`, then run `node "$HYPERFRAMES_DIR/scripts/gate.cjs" --root . --only spatial_canvas`
- [ ] after an MP4 is requested/rendered, run `node "$HYPERFRAMES_DIR/scripts/review-master.cjs" --root . --video "$MASTER_VIDEO" --spatial --out review/spatial-master` and inspect every encoded route sample
- [ ] deliver the preview; render to MP4 only on explicit request
- [ ] surface the preview **only at handoff** (it is the stable, final preview); don't pop one mid-build — build-phase snapshots are headless
