---
name: faceless-explainer
description: Turn a topic, article, or script into a short faceless explainer with synthetic graphics. Use hyperframes for long-form films or an extensive scene-review workflow.
compatibility: Requires sibling skills from this pack, a local filesystem and shell, Node.js 22.20.0+, and FFmpeg/ffprobe for media work. Generation providers and desktop tools are optional, separately configured capabilities.
---

<!-- Public portability adaptation, 2026-09-26. -->

Install this skill with its sibling skills. See [runtime setup and capability boundaries](../hyperframes/references/install-portability.md) before executing commands. User instructions and the requested production stage take precedence over workflow defaults.

> **media-use**: Music and SFX must be individually reviewed and frozen under the project before use. Run `/media-use` with `--adopt` to register those local files; it does not search, download, or generate media.

# Faceless Explainer to HyperFrames

**Studio route:** for long-form narration, mixed generated footage/UI/relational canvases, reference-led production, or repeated scene review, use `/hyperframes` and its `references/review-driven-production.md` instead of this short synthetic-frame route. “Faceless” does not require every film to be asset-free. Explicit requests to preserve the complete script override this route's editorial compression; existing full discretion overrides routine confirmation steps. Requested review-before-assembly remains a real stage boundary.

Use this skill to turn a body of text into an explainer video: pick a design system, plan a teaching story, and build it frame by frame in HyperFrames. **Faceless** means every visual is invented downstream — there is no capture step and no real asset inventory.

> **Confirm the route before Step 0.** You are the orchestrator. Run each step, verify its gate, and only then continue. This skill is for **explaining a topic from text, with no product and no website to capture**. Route other intents elsewhere: a product launch/promo → `/product-launch-video`; a tour of a real site → `/website-to-video`; a GitHub PR → `/pr-to-video`; captions on existing footage → `/embedded-captions`; a short unnarrated motion graphic → `/motion-graphics`. If the user says only "make a video" or the route is uncertain, read `/hyperframes` first.

You are the orchestrator. Work in the chosen project directory (`videos/<project>/` is an example). Run steps in order and pass each gate before continuing. Honor requested review boundaries; existing authorization supersedes routine confirmation steps. Do every step yourself except Step 5, where you dispatch one sub-agent per frame. Do not put design or motion rules here; those live in the frame-worker sub-agent, `hyperframes-creative`, and `hyperframes-animation`.

Workflow: Step 0 setup → `hyperframes.json`; Step 1 brief → `capture/extracted/`; Step 2 design system → `frame.md`; Step 3 storyboard/script → `STORYBOARD.md` and `SCRIPT.md`; Step 3.1 audio → `audio_meta.json`; Step 4 visual design → enriched `STORYBOARD.md`; Step 5 frames → `compositions/frames/NN-*.html` and `index.html`; Step 6 final render → `renders/video.mp4`.

---

## Step 0: Setup and Brief

Goal: Lock the core video brief and create the HyperFrames project if needed.

Initialize only if `hyperframes.json` is missing. Name `<project>` from the topic in kebab-case, such as `compound-interest-explained`; never use workspace name or timestamp.

`npx --yes hyperframes@0.7.17 init "videos/<project>" --non-interactive --skip-skills --example=blank`

The bundled audio adapter uses Fish via `hyperframes-media`; configure the selected transport and voice. For another requested provider or supplied audio, use the [recorded-VO route](../hyperframes/references/pipeline.md). Do not silently switch providers after an error or include credentials in storyboards/manifests.

**Gate:** `hyperframes.json` exists, and angle, length, aspect ratio, and language are locked.

---

## Step 1: Brief (no capture)

Goal: Fold the user's text into the project as the source of information. There is **no website capture and no real assets** — this is a faceless explainer.

Save the user's full input verbatim, then create the synthetic capture package by hand:

- `capture/extracted/visible-text.txt` — the full article / notes / topic / brief, verbatim. This is the source of **information**, not a story template (Step 3 reshapes it).
- `capture/extracted/tokens.json` — `{ "title": "", "description": "", "colors": [], "fonts": [] }`. Fill `title`/`description` from the brief. Leave `colors`/`fonts` empty unless the user explicitly gave brand colors or fonts — then add them (the design preset supplies a complete palette regardless).

Do **not** run `npx hyperframes capture` (there is no URL). Do not create `asset-descriptions.md` or populate `capture/assets/` — faceless visuals are invented in Steps 4-5, not captured. The one exception: if the user supplied a real image, place it under `public/<basename>` and note it for Step 3.

**Gate:** `capture/extracted/visible-text.txt` and `capture/extracted/tokens.json` exist; you can state the explainer's topic and audience in one clear sentence.

---

## Step 2: Design System

Goal: Choose a shipped text/HTML frame preset; a script turns it into this video's `frame.md` + caption skin. These presets contain no font, image or audio binaries; supply required project assets and verify their availability.

You make the one judgment call — **which preset**. Read `../hyperframes-creative/references/design-spec.md` and browse `../hyperframes-creative/frame-presets/`; pick the preset whose look best fits the topic, tone, and audience. Then run:

```bash
node <SKILL_DIR>/scripts/build-frame.mjs --preset <name> --hyperframes .
```

The script does the rest deterministically: copies the preset's `FRAME.md` → `frame.md` and **remixes** it onto any brand tokens in `capture/extracted/tokens.json` (brand colors mapped onto the preset's color keys by role; the preset's display + body fonts swapped for the brand's), copies the preset's caption skin to `.hyperframes/caption-skin.html`, and self-validates (exits 1 on a broken mapping). Proceed as soon as it exits 0 — no hand-editing of the spec.

A faceless explainer usually has **no brand colors/fonts** (`tokens.json` colors/fonts empty) → the script keeps the preset's own palette, a complete shippable design. Only when the user named brand colors/fonts add them to `tokens.json` before running, and only adjust `frame.md` by hand afterward if a mapping truly needs it.

**Gate:** `build-frame.mjs` exited 0 — `frame.md` exists from a named preset, and (when the preset ships one) `.hyperframes/caption-skin.html` exists as the caption skin source.

---

## Step 3: Storyboard and Script

Goal: Turn the text into an approved frame-by-frame teaching plan.

Read `references/story-design.md`, `../hyperframes-core/references/storyboard-format.md`, and `../hyperframes-core/references/script-format.md`. Use them to write `STORYBOARD.md` and, when narration is needed, `SCRIPT.md`.

If the brief or emerging story arc needs a bounded momentum, temporal-compression, overwhelm, or panic/rupture passage, read `../hyperframes-creative/references/fast-paced-editing.md` **now**. Step 3 owns cross-frame seams: choose each participating frame's `transition_in` and add the `fast_passage` / role / focal-handoff / root-mix metadata defined in `story-design.md` before approval. Step 4 may enrich the visuals but does not repair a seam that was never planned.

Use `story-design.md` for the explainer structure (concept / how-to / listicle / story), hook strategy, clarity techniques, emotional beats, the type-enum mapping, and `VO_MODE`. The video's sequence comes from **narrative design, not the input text's paragraph order** — reorder, merge, omit, compress. Faceless visuals are invented downstream, so frames do **not** carry an asset inventory: leave `asset_candidates` empty unless the user supplied a real `public/<basename>` image. Use the exact required fields from the storyboard and script references.

If several consecutive teaching beats require one stable relationship geography and exact overview→detail→return continuity, consolidate them into one compound Spatial Canvas frame per `story-design.md`; do not distribute its regions across independent frame workers.

After drafting, show a frame-by-frame summary. In that same message ask the user two things: (a) to approve or request changes, and (b) whether they want a live preview of the storyboard scaffold (`npx hyperframes preview`) — open it only on a yes. Iterate until approved, and carry the preview choice to Step 6.

**Gate:** `STORYBOARD.md` exists, every frame has the required narrative fields, `SCRIPT.md` exists when narration is needed, and the user approved the frame-by-frame plan.

---

## Step 3.1: Audio

Goal: Generate/import the selected narration and real word timings, and attach any already-reviewed local music to the approved script.

Before starting, decide whether the explainer needs music. If it does, choose one already-reviewed local track, freeze it under `assets/bgm/`, register it with `/media-use --adopt`, and pass that exact project-local path with `--bgm`. The workflow never searches for or generates a track. If no reviewed track is available, proceed without BGM or stop clearly to obtain one; do not substitute a runtime music engine.

Start audio after Step 3 approval. Run it in the background, then continue to Step 4:

```bash
node <SKILL_DIR>/scripts/audio.mjs --script ./SCRIPT.md --storyboard ./STORYBOARD.md \
  --hyperframes . --out ./audio_meta.json \
  --bgm ./assets/bgm/reviewed-track.mp3 & # omit this final flag when there is no music
```

This adapter implements the shared Fish route, transcribes it for word timing, validates/freezes the optional local BGM, and writes timing metadata. Fish credentials and defaults remain owned by `/fish-audio-api`. If there is no narration and no `SCRIPT.md`, voice generation is skipped; an explicit `--bgm` may still be attached. With neither narration nor BGM, mark the project silent.

**Gate:** audio job has started, or the project is marked silent.

---

## Step 4: Frame Visual Design

Goal: Add the visual direction, layout intent, and motion choices to each storyboard frame.

Edit `STORYBOARD.md` in place. Do not create another storyboard. Use `frame.md` as the source of truth for color, type, layout feel, and style.

Read `references/visual-design.md`, `references/composition.md`, `references/motion-language.md`, and `../hyperframes-animation/`. Use `visual-design.md` for required frame fields and the required `## Video direction` block. Use `composition.md` for layout, hierarchy, focal points, and the invented-visual treatment. Use `motion-language.md` and `../hyperframes-animation/` for valid effects and blueprint IDs. Do not invent effect names or blueprint IDs.

If any frame carries `canvas_id`, also read `../hyperframes-creative/references/spatial-canvas.md`, instantiate `../hyperframes/templates/SPATIAL_CANVAS.example.json` once as project-root `SPATIAL_CANVAS.json`, and use the `spatial-canvas` blueprint. Add/adapt exactly one `scope: "scene"` canvas entry per distinct `canvas_id`, each pointing to that frame's exact `src`; never overwrite an earlier frame's entry. Faceless compound frames keep excursions as fixed in-composition overlays owned by the same worker—omit `cutawayComposition`; every excursion still declares its own local `at` / `duration` / `reviewAt`, exact/reorient return ticket, and mutation. After timing sync, the worker gives each excursion one direct-root native clip marker with that exact local window, per the core contract. Also create project-root `DIRECTION.md` from `../hyperframes/templates/DIRECTION.md` so route review has a ledger. The draft timing locks route proportions; Step 5 reconciles absolute times after narration sync.

For every frame, add required visual and motion fields, including `effects` and `focal` and/or `roles`. Because the explainer is faceless, `focal`/`roles` describe **invented visual elements** (a hero word, a diagram node, a data-viz series), not captured assets. Add one video-wide `## Video direction` block for overall visual direction, motion style, pacing, and design rules.

If Step 3 admitted a fast passage, use `../hyperframes-creative/references/fast-paced-editing.md` to complete its shared visual direction. Mark the consecutive frame IDs and provisional within-frame proportions, baseline/escalation roles, peak, release/reorientation, eye-trace, primary edit family, and sound/legibility plan in `## Video direction`; give every participating frame its exact visual arc role. Preserve Step 3's `transition_in` and marker fields. Do not add a second timing manifest—the storyboard's durations become authoritative after sync.

Do not change story, script, `transition_in`, or the source text. Do not write HTML in this step. There is **no asset-staging step** — faceless visuals are built by the workers in Step 5. If the user supplied a real `public/<basename>` image, reference it by path in the relevant frame's `focal`/`roles`; otherwise nothing to stage.

**Gate:** every frame has `effects` plus `focal` and/or `roles`; `## Video direction` exists; every admitted fast passage names a contiguous span, baseline/escalation/peak/release, primary family + optional accent, eye-trace, sound/legibility plan, and each participating frame has its role plus entry/exit handoff and Step-3-owned seam.

---

## Step 5: Build Frames

Goal: Build every storyboard frame as an HTML composition and assemble the playable video.

Wait for Step 3.1 audio to finish if audio was started. Then sync durations and resolve SFX from the project's reviewed local manifest; skip both if silent.

`node <SKILL_DIR>/scripts/audio.mjs sync-durations --audio-meta ./audio_meta.json --storyboard ./STORYBOARD.md`

When any frame has `fast_passage`, immediately resolve and validate the now-exact cumulative windows before dispatch:

`node <SKILL_DIR>/scripts/check-fast-passages.mjs --storyboard ./STORYBOARD.md`

This keeps `STORYBOARD.md` as the only clock, rejects orphan/noncontiguous/incomplete arcs, and prints the exact global passage/role windows plus root BGM-gain cues. Reconcile the `## Video direction` window to that output; do not change the synced durations.

Before the SFX pass, freeze every selected effect under `assets/sfx/`, register the files with `/media-use --adopt`, and ensure `assets/sfx/manifest.json` maps each storyboard cue name to one of those files. Do not leave a name-only cue without a reviewed manifest entry.

`node <SKILL_DIR>/scripts/audio.mjs fetch-sfx --storyboard ./STORYBOARD.md --hyperframes . --sfx-manifest ./assets/sfx/manifest.json`

An unresolved local cue remains nonfatal: the adapter skips it, preserves the shared engine warning in `audio_meta.json` under `anomalies`, and prints resolved/requested plus unresolved counts. Treat that warning as a cue to fix the manifest before final audio review, not as permission to claim a completely resolved SFX pass.

Duration sync is mechanical: real voice duration wins; silent frames keep estimates; never hand-edit synced durations.

If any frame has `canvas_id`, immediately reconcile the draft route to the now-locked frame duration before dispatch:

`node <SKILL_DIR>/scripts/sync-spatial-canvas.mjs --storyboard ./STORYBOARD.md --manifest ./SPATIAL_CANVAS.json`

This scales visit and excursion windows/review samples together, verifies the one-frame/one-canvas owner, and rejects external cutaway files in this workflow.

Before dispatch, read `sub-agents/frame-worker.md` and `../hyperframes-core/references/subagent-dispatch.md`. Dispatch one sub-agent per frame, in parallel if possible; otherwise run workers in waves. Each worker gets exactly one frame.

Each worker context must include `PROJECT_DIR`, `frame_id`, canvas size, caption status and keep-out band if captions are enabled, and `ANIM_DIR` as the absolute path to `../hyperframes-animation/`. A Spatial Canvas frame also receives `SPATIAL_CANVAS.json` and remains one worker/one composition for the whole route. A frame inside an admitted fast passage receives the checker's exact passage/role window plus the shared plan and its focal handoff. Each worker reads `frame.md`, its own `## Frame N` block from `STORYBOARD.md`, and the recipe body for each cited effect or blueprint ID. Each worker writes only `compositions/frames/NN-*.html`. Workers must never edit `STORYBOARD.md`.

As each worker returns, the orchestrator marks that frame as `animated` in `STORYBOARD.md`.

After audio timings exist, build captions in the background and assemble the index:

`node <SKILL_DIR>/scripts/captions.mjs build --storyboard ./STORYBOARD.md --audio-meta ./audio_meta.json --hyperframes . --out ./caption_groups.json &`

`node <SKILL_DIR>/scripts/assemble-index.mjs --storyboard ./STORYBOARD.md --hyperframes .`

The assembler revalidates fast-passage ownership and writes any per-frame `fast_bgm_gain` / `fast_bgm_ramp` cues onto the root paused timeline, so a planned hard music cut or recovery is render-real rather than prose. Frame workers still own no audio.

`captions.mjs` uses the project's `.hyperframes/caption-skin.html` (copied in Step 2) as the caption look, injecting brand tokens from `frame.md`; with no skin present it renders the built-in default pill. `captions: skipped (<reason>)` is valid. Continue without captions when explicitly skipped.

**Gate:** every frame is marked `animated`, `index.html` exists, captions are built or explicitly skipped, every admitted fast arc passed post-sync validation, and its declared root BGM cues are present when BGM exists.

---

## Step 6: Finalize

Goal: Verify the assembled video, get user approval, and render the final MP4.

Inject transitions, run checks, pause for review, then render.

`node <SKILL_DIR>/scripts/transitions.mjs inject --storyboard ./STORYBOARD.md --hyperframes .`

`node <SKILL_DIR>/scripts/transitions.mjs verify --storyboard ./STORYBOARD.md --index ./index.html`

`npx hyperframes lint`

`npx hyperframes validate`

`npx hyperframes inspect`

`npx hyperframes snapshot --at <frame-midpoints>`

`snapshot` stitches the captured frames into one contact sheet (`snapshots/contact-sheet.jpg`). Glance at it; if nothing is obviously broken, move on — don't linger here.

For every `## Video direction`-marked fast passage, render/watch the complete lead-in through release at final fps with final audio. Midpoint snapshots cannot approve its pacing. Fix any lost focal path, unreadable text/caption collision, masked narration, unearned peak, unsafe repeated luminance flash, or missing reorientation, then rerender and rewatch the same full window.

When `SPATIAL_CANVAS.json` exists, additionally run the contract and the complete route rather than relying on frame midpoints:

`node <SKILL_DIR>/../hyperframes/scripts/check-spatial-canvas.cjs --root .`

`node <SKILL_DIR>/../hyperframes/scripts/snap.cjs --root . --spatial`

Read every visit/excursion sample; under `DIRECTION.md` → `## Spatial-canvas review`, fill one exact `<canvas-id>:<visit-id>` row per visit and `<canvas-id>:excursion-<excursion-id>` row per cutaway, fix failures, then run:

`node <SKILL_DIR>/../hyperframes/scripts/gate.cjs --root . --only spatial_canvas`

If a command fails, surface stderr and stop — don't pile on recovery commands. Fix the named owner with the cheapest safe edit: that may be `SPATIAL_CANVAS.json`, `DIRECTION.md`, `index.html`, or `compositions/frames/NN-*.html`. Then rerun the failed command. If HTML or assembly changed, rerun normal lint/validate/inspect; for any Spatial Canvas fix, rerun the structural checker and full `snap --spatial` route, then re-read every regenerated sample before updating rows or running the gate.

**Known false-positive — do not chase it.** `inspect` may report a handful of `text_box_overflow` errors of ~1–4px on the **caption** highlight words (selector `#caption-word-*` / `.caption-line`). The caption pill uses a deliberately snug `line-height` (set once in `scripts/captions.mjs`) and has **no `overflow:hidden`**, so a heavy display glyph's ink spills a few px into the pill's own padding — nothing is actually clipped. Treat these as expected and proceed. Do **not** inflate the caption `line-height` (it balloons the pill, which is worse). Only act on a `text_box_overflow` when it names a **frame** element (`#el-NN-*`), not a caption word.

After checks pass, pause for user review. The video is assembled, viewable, and editable in Studio. Manage preview only once across Step 3 and Step 6: open it if the user asked earlier, offer it if they declined earlier, and do not ask again if they are already reviewing in Studio.

Preview: `npx hyperframes preview`

Render only after user approval:

`npx hyperframes render --skill=faceless-explainer --quality high --output renders/video.mp4`

For a Spatial Canvas render, audit the same route in the encoded file before delivery:

`node <SKILL_DIR>/../hyperframes/scripts/review-master.cjs --root . --video renders/video.mp4 --spatial --out review/spatial-master`

Inspect every encoded route sample. If one fails, fix the source owner, rerun normal checks plus structural/route snapshots, rerender, and repeat encoded-route review. When the encoded review is clean and no source changed after the pre-render checks, do not rerun unrelated checks merely for ceremony.

For every admitted fast passage, replay the same complete lead-in → release window from the encoded MP4 with its final mix. If comprehension, eye-trace, caption/voice intelligibility, peak/release contrast, orientation, or luminance restraint fails, fix the source plan/owner, rerender, and rewatch that encoded window.

**Gate:** `lint`, `validate`, and `inspect` passed before render; any Spatial Canvas also passed structural, route-snapshot, exact-row direction, and encoded-route review; every admitted fast passage passed full-motion source and encoded-master review with its final mix; user approved at the review pause; `renders/video.mp4` exists. Final reply states MP4 path and final duration.

---

## Quick Reference

**Formats:** landscape `1920x1080` by default; portrait `1080x1920`; square `1080x1080`. Set the format once in the storyboard frontmatter.

**Faceless deltas vs a captured-asset workflow:** no Step 1 capture (synthetic `tokens.json` + `visible-text.txt`); no `asset-descriptions.md` and no `capture/assets/`; no asset-staging in Step 4; `asset_candidates` empty by default; every visual is invented by the Step 5 workers (typography / abstract graphics / diagrams / data-viz). A user-supplied `public/<basename>` image is the only real asset path.

**Background scripts:** the workflow ships only these under `scripts/`: `build-frame` for adopting + brand-remixing a frame preset into `frame.md` (+ caption skin); `audio` for Fish TTS, transcription, explicit local BGM/SFX, and duration syncing; `check-fast-passages` for post-audio fast-arc windows/ownership; `sync-spatial-canvas` for post-audio route timing; `captions`; `transitions`; and `assemble-index`. Everything else is the `hyperframes` CLI or the canonical sibling HyperFrames validation scripts named above.

| Read                                                                                                         | When                                          |
| ------------------------------------------------------------------------------------------------------------ | --------------------------------------------- |
| `[../hyperframes-creative/frame-presets/](../hyperframes-creative/frame-presets/)`                           | Step 2: choose and adopt a frame preset.      |
| `[../hyperframes-creative/references/design-spec.md](../hyperframes-creative/references/design-spec.md)`     | Step 2: apply brand tokens correctly.         |
| `[references/story-design.md](references/story-design.md)`                                                   | Step 3: plan the explainer story.             |
| `[../hyperframes-core/references/storyboard-format.md](../hyperframes-core/references/storyboard-format.md)` | Step 3: write `STORYBOARD.md`.                |
| `[../hyperframes-core/references/script-format.md](../hyperframes-core/references/script-format.md)`         | Step 3: write `SCRIPT.md`.                    |
| [../hyperframes-media/references/tts.md](../hyperframes-media/references/tts.md)                           | Step 3.1: use the implemented Fish narration contract, or import selected-provider audio. |
| `[references/visual-design.md](references/visual-design.md)`                                                 | Step 4: enrich the storyboard visually.       |
| `[references/composition.md](references/composition.md)`                                                     | Step 4: judge composition.                    |
| `[references/motion-language.md](references/motion-language.md)`                                             | Step 4: judge motion language.                |
| `[../hyperframes-animation/](../hyperframes-animation/)`                                                     | Step 4: cite effect and blueprint IDs.        |
| `[../hyperframes-creative/references/spatial-canvas.md](../hyperframes-creative/references/spatial-canvas.md)` | Steps 3–5: compound persistent-world frames. |
| `[../hyperframes-creative/references/fast-paced-editing.md](../hyperframes-creative/references/fast-paced-editing.md)` | Steps 4–6: directed high-velocity passages. |
| `[sub-agents/frame-worker.md](sub-agents/frame-worker.md)`                                                   | Step 5: dispatch per-frame workers.           |
| `[../hyperframes-core/references/subagent-dispatch.md](../hyperframes-core/references/subagent-dispatch.md)` | Step 5: dispatch sub-agents safely.           |
