---
name: hyperframes-creative
description: Develop video direction, typography, color, visual mechanisms, storyboards, and asset prompts. Use for a HyperFrames design brief or review-led visual exploration.
compatibility: Requires sibling skills from this pack, a local filesystem and shell, Node.js 22.20.0+, and FFmpeg/ffprobe for media work. Generation providers and desktop tools are optional, separately configured capabilities.
---

<!-- Public portability adaptation, 2026-09-26. -->

Install this skill with its sibling skills. See [runtime setup and capability boundaries](../hyperframes/references/install-portability.md) before executing commands. User instructions and the requested production stage take precedence over workflow defaults.

# HyperFrames Creative

Brand, pacing, style, narration, and composition direction. Use after the technical contract from `hyperframes-core` is in place.

For motion patterns, scene blueprints, transitions, and CSS marker effects, use `hyperframes-animation` — this skill is intentionally non-animation.

> **Read these two FIRST for any non-trivial composition — they override web instincts:**
>
> - `references/house-style.md` — "interpret the prompt, generate real content," the lazy-default list, and the background/foreground layer recipe. This is what turns a literal restyle into a _concept_.
> - `references/video-composition.md` — video-medium scale, a designed density curve, one active focal point, and produced detail only when it earns a slot.
>
> Skipping these is the single biggest cause of generic, web-page-looking output. They are not optional rows in the routing table below — for anything beyond a one-line edit, open both before you choose colors or write HTML.

> **Then, for any anchor / hero / awe-inspiring piece — read the direction layer:**
>
> - `references/cinematic-direction.md` — the directorial doctrine: the six-regularity Spine, the **Effort Protocol** (the forcing function against the lazy competent default), the Awe Test, the substrate / externalization / receiver-runway doctrines, the Canvas · Artifact · Cinema ownership lanes, the visual vocabulary, and the scene-review diagnostics. **This is the difference between a composition that is _correct_ and one a viewer screen-records.** It also spells out *The HyperFrames Unlock*: advanced runtimes are available, while authored subject/world quality and good judgment remain the real cost.
> - `references/cinema-layer.md` — the Cinema-Layer vocabularies (charged transitions, atmosphere, 3D moves, lens personality, hand-drawn, diegetic UI, recursive shots, video-arc drift, post-fx cookbook) with HyperFrames HTML/CSS/SVG/GSAP/Three.js implementation hints.
>
> Read `video-composition.md` + `house-style.md` for the *floor* (don't ship web-page output). Read these two for the *ceiling* (ship something overwhelmingly good). Cold opens, thesis reveals, hero product beats, act opens/closes, closing images — open `cinematic-direction.md` before you shotlist.

> **When a piece feels like "elegant slides"** — competent, well-rendered, inert — read `references/visual-storytelling.md`, the film-craft companion lens (Block / Murch / Williams-Disney / McCloud / Mamet / Katz / Mascelli / McKee). It supplies the concrete levers the doctrine lacks: the visual-intensity curve, the Rule of Six + flinch test for cuts, timing-vs-spacing for alive motion, the six panel-to-panel transitions, shape-to-emotion grammar, and the **value-turn audit** (if a scene doesn't turn a value, it's a non-event — cut it). The "elegant PPT" feeling is almost always a deficit in the *temporal/relational* layers, not the surface.

## Workflow

1. If a project has a design spec, **read it first** and treat its current frontmatter tokens as brand truth (colors, fonts, spacing, tone, constraints). Which file to read (precedence `frame.md` → `design.md` → `DESIGN.md`) and how to parse it (frontmatter = normative, prose = context) are defined once in [`references/design-spec.md`](references/design-spec.md). Resolve later user instructions and revision-specific approvals before inheriting an old spec. For reference-led or iterative work, read [`references/reference-led-direction.md`](references/reference-led-direction.md): establish the active direction, protect approved intervals, and prove representative animation before multiplying a treatment across a film.
2. If no design spec exists and the user asks for visual direction, choose a route:
   - Ready-made frame-preset (optional) → `frame-presets/` (adopt a `FRAME.md` as `frame.md`; see `references/design-spec.md`)
   - Named style or mood → `references/visual-styles.md`
   - Fast defaults → `references/house-style.md`
   - Interactive selection → `references/design-picker.md`
3. For multi-scene work, record a reasoned Spatial Canvas `PASS`/`USE` before locking the scene map. Persistent relationships, revisitation, and consequential returns → `references/spatial-canvas.md` + project `SPATIAL_CANVAS.json`; otherwise use independent beats via `references/beat-direction.md`. Separately record fast-passage `PASS`/`USE`: bounded momentum, temporal compression, overwhelm, or panic → `references/fast-paced-editing.md` + project `FAST_PASSAGES.json` before transition mechanics. These are independent admissions, not format quotas.
4. For any **anchor / hero / awe-inspiring** shot (cold open, thesis reveal, hero product beat, act open/close, closing image), read `references/cinematic-direction.md` and run its **Effort Protocol** before shotlisting — declare AWE vs EASY per shot, use **Gaze → Dream → Create** to diverge. For a cold open, map only the first three seconds of narration cue-by-cue before dreaming; for true 3D, pass `hyperframes-animation/adapters/three.md`'s admission gate. Pick the Cinema-Layer treatment from `references/cinema-layer.md`.
5. For any **static asset** the composition needs (illustrations, dossier cards, plates, cutout subjects, substrate/depth layers), read `references/asset-generation.md` before generating — use the selected provider or available host image tool, inspect true alpha for cutouts, and **save every prompt** and provenance. For generated footage or exact UI over a material/character plate, read `references/generated-media-composition.md` before generation: assign material/code roles, source clocks, camera ownership and registration. For an approved B-paper / editorial paper storyboard, first read `references/paper-theatre.md` for its material, shot and layer workflow.
6. For motion-heavy work, read `references/motion-principles.md` (high-level guardrails), then go to `hyperframes-animation` for atomic rules.
7. If a built piece feels like "elegant slides" (inert despite good assets), read `references/visual-storytelling.md` and run its per-scene checklist — value-turn audit, intensity curve, cut-on-the-idea, timing-vs-spacing, transition variety.
8. Before full assembly and again on the encoded master, run `references/design-adherence.md`'s rendered-trajectory gate: establish / midpoint / resolve for every semantic scene, every admitted Spatial visit/return, every fast passage through release, plus cue-boundary samples inside the first three seconds.

## Routing

| Topic                                                                    | Read                                           |
| ------------------------------------------------------------------------ | ---------------------------------------------- |
| **Reference-led direction / repeated review** — active brief, animated benchmarks, mixed representations, PROTECT/POLISH/REBUILD, feedback acceptance tests | `references/reference-led-direction.md` |
| **Generated images/video with exact UI** — shot contract, native media clocks, planar screen replacement, occlusion, still-versus-video selection | `references/generated-media-composition.md` |
| **Direct an anchor / hero / awe shot** — doctrine, Effort Protocol, awe test, 3-layer architecture, diagnostics | `references/cinematic-direction.md`            |
| **Fix "elegant slides" / sequence & story craft** — visual-intensity curve, Rule of Six + flinch test, timing-vs-spacing, 6 panel transitions, shape-to-emotion, value-turn audit | `references/visual-storytelling.md`            |
| **Cinema-Layer treatment** — charged transitions, atmosphere, 3D, lens, hand-drawn, diegetic UI, recursion, post-fx | `references/cinema-layer.md`                    |
| **Choose 2D vs 2.5D vs true 3D** — semantic abstraction, world coherence, paused-frame quality | `references/cinematic-direction.md` · `hyperframes-animation/adapters/three.md` |
| **Generate static assets** — configured image generation, reference roles, true alpha, sizing, prompt/provenance records | `references/asset-generation.md` |
| **B-paper / editorial paper theatre** — storyboard fidelity, material foundry, physical mechanisms, layered shots, typography and encoded QA | `references/paper-theatre.md` · concrete prompts → `references/paper-theatre-prompts.md` |
| Adopt a ready-made frame-preset as `frame.md` (optional)                 | `frame-presets/` · `references/design-spec.md` |
| Default palettes, motion, typography, lazy defaults to question          | `references/house-style.md`                    |
| Named style presets, mood-to-style routing                               | `references/visual-styles.md`                  |
| Palette-specific color tokens                                            | `palettes/*.md`                                |
| Composition patterns — PiP, text-behind-subject, title card, slide show  | `references/composition-patterns.md`           |
| **Spatial Canvas admission + direction** — persistent world, semantic geography, camera itinerary, cutaway/return, synthesis | `references/spatial-canvas.md` + project `SPATIAL_CANVAS.json` |
| **Fast-paced passage admission + direction** — momentum, compression, overwhelm, rupture, sound arc, release/reorientation | `references/fast-paced-editing.md` + project `FAST_PASSAGES.json` |
| Stats / infographic presentation                                         | `references/data-in-motion.md`                 |
| Structured expansion for open-ended prompts                              | `references/prompt-expansion.md`               |
| Video-medium density, scale, color, frame composition                    | `references/video-composition.md`              |
| Per-beat direction, rhythm planning, transition timing                   | `references/beat-direction.md`                 |
| Source adherence + rendered trajectory QA (including opening and 3-state scene review) | `references/design-adherence.md`        |
| High-level motion guardrails and GSAP-quality rules                      | `references/motion-principles.md`              |
| Font selection, pairings, rendered-video type guardrails                 | `references/typography.md`                     |
| Script pacing, tone, openings, number pronunciation                      | `references/narration.md`                      |
| Precomputed audio bands mapped to motion                                 | `references/audio-reactive.md`                 |

## Scripts

- `scripts/contrast-report.mjs` — inspect contrast warnings from rendered frames.
- `scripts/extract-audio-data.py` — pre-extract audio bands for audio-reactive compositions.
- `scripts/package-loader.mjs` — support script for bundled creative tooling.

Run from the repo root with explicit paths, for example:

```bash
python skills/hyperframes-creative/scripts/extract-audio-data.py <audio-file>
```

Animation analysis (`animation-map.mjs`) lives in `hyperframes-animation/scripts/`.

## Boundaries

- Do not override `hyperframes-core` technical rules.
- Do not require a design system for a minimal technical composition.
- Do not add extra scenes, narration, music, captions, or transitions unless the request calls for them or you first propose the expansion.
- Keep recipe references task-specific; do not read every reference for simple edits.
