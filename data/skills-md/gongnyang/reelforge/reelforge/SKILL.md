---
name: reelforge
description: Author and run ReelForge motion-graphic video projects from a brief, script, or batch of briefs. Use when the user asks in Korean or English to make a video with ReelForge, including triggers such as "ReelForge로 영상 만들어", "릴포지", "ReelForge", "브리프로 영상", "대본으로 영상", "ReelForge 쇼츠", "나레이션 영상", or "run the ReelForge pipeline". For videos outside a ReelForge engine checkout, do not use this skill.
allowed-tools: Bash(node bin/vf *), Bash(node scripts/*), Bash(ffmpeg *), Bash(npx hyperframes *), Bash(rg *)
argument-hint: "[brief | projectDir]"
---

# ReelForge

ReelForge turns one brief into a **full-bleed motion-graphic video** — never a slide deck.
This skill is a thin director and recommendation router: motion vocabulary lives in
`references/grammar/` (contract-translated) and hyperframes-animation (vendor canon);
verified choreography lives in `references/gallery/`; this file owns only procedure, gates,
and pointers. Data comes last; direction comes first. If a frame reads as a presentation
slide, the scene fails.

## Step 0 — Brief

Collect only missing production facts, then move on:

- `audience` / `goal`: who watches, what should change after watching.
- `duration target` and `format`: shorts, demo, explainer, report.
- `tone`: one or two mood words — drives preset choice and mood escalation.
- `assets`: brand, product, screenshots, music track, whether generated images are allowed.
- `constraints`: language, claims to avoid, must-include terms.

When underspecified, propose defaults and proceed (confirm at the D5 checkpoint).

## Step 1 — Direction Freeze (D1–D5, the stage that decides quality)

Produce artifacts under `<projectDir>/direction/` in this order, then freeze:

1. **D1 Concept** — `concept.md`: the dominant object, the world metaphor, and one named
   visual event per scene. Written **before any copy** — a deliberate inversion of the old
   copy-first habit, so visuals are never a decoration of frozen text.
2. **D2 Arc** — `arc.json`: pick one arc preset and assign per-scene `intensity` (0–100)
   snapped to the BPM grid — read `references/gallery/ROUTING.md` §0. With music, analyze
   the track first (`audiomap.json`, music-to-video interop); timing authority stays with
   audio metadata (silent scenes use mock audio, see Step 3).
3. **D3 Storyboard + Routing** — `STORYBOARD.md` table:
   `sceneId | duration | intent | intensity | refId | handoffAnchor`.
   Assign each scene's `refId` (1–2) by lookup in `ROUTING.md`: §A intent×band matrix →
   §B mood filter → §C budget → §D combination rules. Cells are grammar technique IDs;
   stamped gallery fragments take precedence at lint time.
4. **D4 Copy** — `copy.md`: every on-screen line, polished (gn-voice-style pass), written
   to the read-speed copy budgets in `references/design-direction.md`; scenes with a
   stamped refId additionally respect that fragment's slot budgets in `gallery-index.json`.
5. **D5 Freeze checkpoint** — show the user the arc curve and the routing table summary,
   and state: re-routing after freeze = full scene re-authoring.
   Gate: `node scripts/direction-lint.mjs <projectDir>` must pass. Errors block the
   freeze; `RF-DIR-001` warnings mark scenes as **sketch-authored** (reinforced strip QC)
   and do not block.

## Step 2 — Scene Swarm

**Pilot Gate first** (engine-enforced): author one pilot scene, compile and render it
alone, contact-sheet it, record the pass in `direction/pilot.json`
(schema: `schemas/pilot-report.schema.json`) — `vf compile` refuses a project with 2+
free scenes until that record exists (RF-PILOT-001..003).

Then dispatch one worker per scene, in parallel. Worker payload: its STORYBOARD row, the
adjacent scenes' `refId`+`handoffAnchor` rows, the assigned gallery fragment (stamped) or
grammar technique section (sketch), the keep/mutate contract, `frame.md`, and its own
`copy.md` lines. **No blank-canvas authoring — workers transform the assigned reference.**
Fragment contract, tokens, and living-motion rules: read `references/scene-authoring.md`
before dispatch and include it in worker context. Workers never run the CLI, never render,
never edit `scene_specs.json`.

## Step 3 — Assemble

`scene_specs.json` is a **thin manifest**, not an authoring surface — field reference,
Korean TTS preprocessing, and the silent-scene mock-audio procedure live in
`references/scene-authoring.md`. Compile:

```bash
node bin/vf compile <projectDir> --preset fixtures/presets/<preset>.json
```

Every failure carries a stable `RF-*` code plus a fix hint — apply the hint. Treat any
`free-missing-source`/`free-missing`/`free-invalid` degradation warning as a build failure.

## Step 4 — Render

Render serially — one render at a time per machine, no timeouts (use a watcher):

```bash
cd <projectDir>/build
PRODUCER_LOW_MEMORY_MODE=false PRODUCER_MAX_WORKERS=3 PRODUCER_BROWSER_GPU_MODE=hardware \
  npx hyperframes render . --workers 3 --quality draft -o ../renders/draft.mp4
```

Three workers render roughly 5× faster than the sub-8GB single-worker clamp; fall back to
`--workers 2` under RAM pressure, kill stray `chrome-headless` between renders, and use
`--quality high` only for the final export.

## Step 5 — Strip QC + Reharvest (max 2 rounds per scene)

1. Machine pass: contact sheet (`node scripts/craft-contact-sheet.mjs`) or a 1fps strip
   (`ffmpeg -i draft.mp4 -vf "fps=1,scale=480:-1" strip/f%02d.png`). Blank frames, low
   contrast, and frozen motion after entrance fail automatically.
2. Viewer pass on the full strip using `references/strip-qc.md` (13 bans + handoff
   continuity + refId conformance). Sketch-authored scenes get reinforced review.
3. Re-dispatch only the failing scenes with the failure reason. A scene failing twice →
   repair the gallery entry or ROUTING row (never this file); an entry failing twice is
   demoted from the gallery.
4. **Reharvest**: QC-passing choreography not yet in the gallery → propose intake through
   `node scripts/gallery-verify.mjs` (user approval), stamping it into `gallery-index.json`.

Ops: fragment-contract version bump → run `node scripts/gallery-verify.mjs --all` (stamps expire);
narration regeneration → re-check pairs-assigned scenes; per-scene re-route request →
state the cost first (that scene plus adjacent pairs re-author).

## Studio Edit Loop

```bash
node bin/vf studio <projectDir> --port <port>
```

- `E1` presentation-field edits (headline, mood, altText, subtitleMode): save, recompile, preview.
- `E2` `narration_tts` changes: re-run TTS for affected scenes, then full compile.
- `E3` scene order/insert/delete/transition changes: full compile and final render.
- Fragment edits (`scenes-src/*.html`): recompile like `E1`, then re-run strip QC for that scene.

## Ecosystem Contracts

- **Generated images**: compile prompts with `image-prompt` (`check_prompt ok:true` only)
  → `assets/images/runner/prompts.jsonl` → `codex-imagegen` consumes in parallel; recover
  via `resultPath`, never write `finalPath` directly. Contract:
  `references/codex-runner.md` §Image Runner Contract (`reelforge.image-runner.v1`) —
  never invent a new one.
- **Asset boundary**: searchable assets (stock, BGM, SFX, icons, logos, LUTs) =
  `media-use` resolve; prompt-crafted hero images = image-prompt→codex-imagegen. Register
  accepted finals in the media-use ledger (`resolve --from`) for cross-project reuse.
- **Carousels / card-news shorts** (4:5 PNG sets) → dispatch to `/card-shorts`; never
  clone its grammar here.
- **Vendor canon**: grammar pointers into hyperframes-animation rules/blueprints/adapters
  are canonical upstream — never copy them locally; cite by ID or heading only.

## Hard prohibitions

- No per-scene `duration` fields — timing derives from audio metadata only.
- Never edit generated HTML under `build/`; fragments in `scenes-src/` are the source.
- No unknown keys in `scene_specs.json`; no schema edits during video authoring.
- No motion, chrome, or scrims in `scene_specs` — free-scene motion lives in its fragment.
- An unstamped `refId` is sketch-authored out loud (RF-DIR-001) — never silently authored
  as a slide.
- Repair failures in gallery/ROUTING/index **data** — this file stays frozen.
- Free-scene `reveal`/`emphasis` stay at their sealed fixed values (`references/scene-authoring.md`).

## Appendix — optional data blocks

Eight legacy block layouts remain available for scenes carrying real quantitative data.
Contract and usage limits: `references/scene-authoring.md` Appendix.

## References — load at the stated point, not before

- `references/design-direction.md` — preset selection tree, pacing rules, copy budgets. Load at D1/D2; copy rules again at D4.
- `references/gallery/ROUTING.md` — arc grammar (§0) and routing lookup (§A–D). Load at D2/D3.
- `references/grammar/00-INDEX.md` — vocabulary index and loading discipline. Load at D3 for candidates; scene workers load only their assigned technique's section.
- `references/scene-authoring.md` — fragment contract, thin manifest, mock audio, Korean TTS. Load before worker dispatch and at Step 3.
- `references/codex-runner.md` — batch ownership, worker prompt template, image runner. Load when briefs ≥ 2 or when the image track starts.
- `references/strip-qc.md` — QC bans and the visual checklist. Load at Step 5 only.
- `docs/design-presets.md` — preset catalog and video-safe tables. Load on custom color or preset questions.
