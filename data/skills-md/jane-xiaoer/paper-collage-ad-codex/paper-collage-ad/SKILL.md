---
name: paper-collage-ad
description: This skill should be used when the user asks to "做一个剪纸广告", "制作拼贴广告片", "把产品做成纸片定格动画", "做一个有趣的产品广告", "生成半色调剪纸分镜", "把静态拼贴图做成广告视频", "把广告拉长一点", "参考这个声音配音", or wants a complete branded paper-cut advertisement from brief to validated MP4 rather than only prompts or still images.
metadata:
  version: "1.1.0"
  compatibility: OpenAI Codex desktop and CLI
---

# Paper Collage Ad

Turn a product brief and brand assets into a complete paper-collage advertisement. Build the story around one memorable visual metaphor, generate a locked set of finished keyframes, animate the sequence, add narration and sound, validate the rendered MP4, and preserve the reusable production artifacts.

## Core outcome

Deliver all of the following:

1. A concise creative concept with one recurring visual world.
2. A time-coded storyboard with one idea and one joke per scene.
3. A locked visual system and approved first keyframe.
4. A consistent finished keyframe for every scene.
5. Narration, music and restrained sound effects.
6. A rendered MP4 with verified audio and video duration.
7. A contact sheet and all manifests needed for reproducibility.
8. Editable scene videos, selected narration and the final audio mix.

Do not stop at prompts or a storyboard when the user asks for a finished advertisement.

## Codex edition

Treat this repository as the skill directory. Install it at either `~/.codex/skills/paper-collage-ad/` for global use or `<project>/.codex/skills/paper-collage-ad/` for project-local use. Run every command from a shell available to Codex and keep generated project assets outside the skill directory.

The workflow remains framework-neutral: plain Markdown, Node, Bash and FFmpeg make the deterministic steps usable from other agents or a bare shell. The metadata, installation paths, privacy defaults and examples in this edition are maintained primarily for OpenAI Codex.

This skill is self-contained and framework-neutral: plain Markdown, Node and Bash scripts, and FFmpeg. Any agent (Claude Code, Codex, openclaw, or a bare shell) runs it identically. There is no framework-specific runtime.

Resolve `<SKILL_DIR>` to the folder containing this `SKILL.md`. Every `scripts/...` and `references/...` path below is relative to it; every project artifact is relative to the project directory you create in Phase 1.

**Phase 0: Preflight.** Before generating anything, verify the toolchain:

```bash
bash <SKILL_DIR>/scripts/check-deps.sh
```

Core tools (`ffmpeg`, `ffprobe`, `node`) must pass. The reference-voice extras are only needed for Phase 5 voice cloning. See `references/dependencies.md` for the full list.

The four deterministic, runnable steps — each fails loudly if inputs are missing and verifies its own output at the stream level:

| Route | Command | Consumes | Produces |
| --- | --- | --- | --- |
| Still-keyframe fallback | `node <SKILL_DIR>/scripts/render.mjs` | keyframes + `examples/render-manifest.json` | one MP4 from stills |
| Local layered animation | `node <SKILL_DIR>/scripts/layer-animate.mjs` | field + cut layers + finished frame + `examples/layer-manifest.json` | one scene MP4 |
| Reference-voice prep | `bash <SKILL_DIR>/scripts/prepare-indextts2-voice.sh` | one authorized user-supplied recording | private local speaker `.npz` |
| Reference-voice narration | `node <SKILL_DIR>/scripts/narrate-indextts2.mjs` | private speaker `.npz` + `examples/voice-manifest.indextts2.json` | one local 48 kHz WAV per scene |
| Final assembly | `node <SKILL_DIR>/scripts/assemble.mjs` | scene MP4s + voice + music + sfx + `examples/production-manifest.json` | mastered `final.mp4` |

Creative generation keeps a model or human in the loop for keyframes, the optional Gemini Omni motion pass, final animation and voice selection. Deterministic assembly and validation remain scripted. Follow Phases 1–6 in order; do not skip the stage gates in `references/production-workflow.md`.

## Phase 1: Lock the brief

Extract or infer the following from existing project material before asking questions:

- Product promise.
- Audience and viewing context.
- Required product facts and CTA.
- Brand assets, colors and typography.
- Length, aspect ratio and language.
- Available generation and rendering tools.

Use existing project conventions when they already answer the brief. For a desktop product with landscape marketing assets, start with 16:9 and five scenes. Treat 30 seconds as a draft constraint only. Do not lock runtime until a representative narration take has been generated and measured. For social-first content, start with 15 seconds and 9:16 only when brevity is a hard requirement.

Create the artifact structure in `references/production-workflow.md` and keep every project-bound generation inside it.

**Use the real brand assets — never invent them.** Before any generation, locate the product's real logo, app icon, UI screenshots, brand colors and wordmark inside the project. Feed the real icon/UI as reference images to the image model, and composite the exact wordmark PNG for final delivery. Do not let the model invent a mascot or approximate the logo — a made-up character or a mis-spelled AI wordmark is an instant reject.

Write the one-line creative angle before drafting scenes. Prefer a concrete metaphor that can carry the whole film. Examples include a traffic jam for tool overload, a factory for transformation, a stage performance for orchestration, or a suitcase for consolidation.

## Phase 2: Write and confirm the script — HARD GATE

**Do not generate a single keyframe, voice take, or clip until the user has approved a written script.** This gate is what separates a real ad from paper-scrap garbage. Rushing to hand in a rendered MP4 before the words are agreed is the most expensive mistake — it causes version after version of rework.

Produce, and get the user to explicitly sign off on, three things:

1. **Core dramatic action / concept** — one sentence: who wants what, blocked by what, plus the one recurring visual metaphor that carries the whole film.
2. **Storyboard** — beat by beat: `scene # · duration · 画面 (what the camera sees) · 旁白/对白`. Default 30 seconds or more unless the user asks for shorter.
3. **The actual dialogue / narration**, written out in full.

Craft rules for the writing (this is an ad concept-short, not a feature list):

- **Zero explanation — show features, never narrate them.** The voiceover must NOT list capabilities ("opens every format, sorts your photos and documents, one app for all…"). That reads as a spoken product manual and is the #1 reason ad copy feels cringe. The *visuals* carry the product story; the narration only sets mood and moves the story.
- **Few lines, spoken, with subtext.** Talk like a real person, not an essay. Say the tip of the iceberg and imply the rest. No AI-essay tone, no piled-on metaphors, no preaching, no exaggerated sales rhythm.
- **Hook in the first 5 seconds** — a slightly-off everyday image that makes the viewer ask "怎么回事?".
- **Tone must match the story.** Warm/healing story → gentle storybook narration; satirical → mock-epic or goofy; cool product → sparse and confident. A grand tragic/Shakespearean voice over a cozy little story feels wrong — match, don't clash.
- **One clean CTA** at the end: brand + one clear action (and a URL if relevant), held at least one second.

Keep each scene responsible for one idea and one main action; preserve recurring characters/props so it reads as one story, not five unrelated posters.

If the environment has a dedicated screenwriting/scriptwriting skill, invoke it to develop the script — but the sign-off gate below is mandatory either way.

**GATE: present the script + storyboard + dialogue and get an explicit approval from the user before any production. Nothing is generated until then.**

## Phase 3: Lock the visual system

Read `references/collage-dimensions.md` before generating the first frame. Specify:

- Exact background field and paper grain.
- Halftone dot shape and density.
- Cut-edge treatment and white keyline.
- Drop-shadow offset, softness and opacity.
- Brand color allocation.
- Label placement and typography character.
- Negative constraints.

Generate the first frame as the style anchor. Inspect text, brand mark, materials, shadows, character tone and negative space. Do not generate the complete set until this anchor is acceptable.

For every later frame, provide these references in order:

1. The approved first frame as the strict style reference.
2. The previous scene as the continuity reference.
3. The official brand icon or product image.
4. The most relevant real product screenshot.

Repeat the complete material description in every generation prompt. Generators have no memory between calls.

Use the prompt scaffold in `references/prompt-patterns.md`. Burn short scene labels into the image only when the generator reliably preserves them. Keep exact text brief and inspect every result for malformed Chinese, incorrect URLs and invented format labels.

## Phase 3.5: Gemini Omni motion draft and surgical edit pass (optional)

When the ChatCut plugin is installed and the user has video-generation entitlement, use **Gemini Omni** (`model: "omni"`, backend `gemini-omni-flash-preview`) between approved keyframes and final animation. Read `references/gemini-omni-flash.md` and copy `examples/omni-pass.json` as the shot plan.

Use this pass for two jobs only:

1. **Motion drafting:** animate an approved keyframe with `firstFrame` to test timing, staging and comic beats before spending on a finishing generation.
2. **Surgical repair:** pass an existing clip through `continueFrom` to change one localized property while preserving unmentioned content.

Treat Omni as an editing and drafting layer, not a finishing model. It outputs 720p/24fps, supports 3–10 second clips, and only accepts 16:9 or 9:16. Pick exactly one of `firstFrame`, `refImages` or `continueFrom`; omit `resolution`. It cannot use a last frame, extend a clip, bridge two clips, accept audio references or replace spoken audio.

Write the motion prompt in English, use positive instructions such as `locked-off static camera`, and track no more than three important subjects. Do not ask Omni to render Chinese or other CJK text. Add exact labels, URLs, UI and wordmarks later with HyperFrames or another deterministic overlay.

Approve or reject each Omni draft before final animation. If 720p is acceptable, an approved output may become the scene source. If delivery requires 1080p, longer duration, exact typography, or whole-shot motion/camera changes, use the Omni clip only as a motion reference and finish with Seedance 2, Kling or HyperFrames. Stop deep edit chains: from round four onward, regenerate from a clean source because quality loss and full regeneration cost compound.

## Phase 4: Animate

**Route A — AI image-to-video (Seedance / jimeng via `arkcli`), best for organic motion + native foley.** Prefer real element assembly when a capable image-to-video tool is available:

- Start on the empty paper field.
- Slide paper elements in from edges one by one.
- Settle each shadow as its element lands.
- Reveal the label last.
- Hold the complete frame long enough to read.

Use one video model for the delivered set to preserve motion and texture consistency. If prompt-driven assembly fails, use a start-frame and end-frame interpolation model.

**Route B — HyperFrames (code-driven, KEY-FREE) — preferred with no video-model key, and preferred for precise scenes even when you have one.** HyperFrames renders HTML + GSAP compositions to MP4 locally (node + headless Chrome + ffmpeg, no API key, no limits). It is *better than any video model* for precise, deterministic motion — the exact stuff models get wrong: a logo whose outer shutter rotates while the center stays perfectly still, a UI that reveals its file list row by row, paper elements sliding/settling in stop-motion cadence, text that bounces on beat. Read `references/hyperframes-route.md` and start from `examples/hyperframes-logo-composition.html`.

The non-negotiable rule for paper-cut in HyperFrames: **animate real paper assets, never fake paper in CSS.** Feed AI-generated cut-paper PNGs (background field + cut-out element layers) and choreograph *those* with GSAP; a flat CSS/gradient look is the "flat vector pretending to be paper" trap. The precise-logo trick: two stacked copies of the paper-cut icon — the outer one clipped to a circle and rotated, a static inner copy clipped to the center circle locking the ear in place. Bonus: all text is real HTML, so wordmarks and URLs never mis-spell (unlike AI-rendered text).

**Hybrid is ideal:** cheap motion experiments or localized short-clip repairs → Gemini Omni; organic/physical finishing scenes (files raining, chaos, natural motion + native foley) → Seedance or Kling; precise brand/UI/logo/text scenes → HyperFrames. Anyone without a video-model key can skip Omni and do the whole film in HyperFrames.

When neither is available, render the approved keyframes with the deterministic FFmpeg fallback in `scripts/render.mjs`. Use short camera movement in the first part of each shot, transition at the scene boundary, and hold the back half for reading. Do not use perpetual breathing, random drift or rapid template transitions.

For actual local cutout assembly instead of whole-frame camera motion, read `references/local-layer-animation.md` for the method, then drive it with `scripts/layer-animate.mjs`. Split each finished frame into feathered transparent-PNG paper layers, describe each layer's entrance edge and final position in a manifest matching `examples/layer-manifest.json`, and run:

```bash
node <SKILL_DIR>/scripts/layer-animate.mjs \
  --manifest ./manifests/scene-01-layers.json \
  --output ./renders/scene-01.mp4
```

The animator slides each layer in from its edge with stepped stop-motion cadence, crossfades the untouched finished frame over the assembled result for the final hold, and verifies dimensions, duration and frame count. Each layer PNG must already include its own soft shadow. This produces a scene MP4 that `assemble.mjs` can stitch.

Render every scene as its own MP4 before the final assembly. This keeps scene retiming reversible. When extending a rushed cut, slow each scene independently with source-to-target `setpts` ratios; do not globally slow the mastered MP4.

## Phase 5: Audio

Read `references/audio-production.md` before generating narration and `references/music-scoring.md` before choosing music. Generate one narration file per scene. Keep raw and selected takes separate. Validate intelligibility and pronunciation, then measure every selected file before fixing picture duration.

Set each scene to the selected voice duration plus 0.7 to 1.5 seconds. If pacing feels rushed, extend the picture first, rewrite the line second and use pitch-preserving time compression only as a last adjustment. Do not exceed about 1.12x for a final take.

For Chinese narration, verify the selected voice is actually a Chinese voice. Some local TTS pipelines silently select an English voice, produce extremely slow speech or omit lines. If this occurs on macOS, use a verified local Chinese voice such as `Tingting`, then convert the result to 48 kHz WAV.

When the user supplies an authorized reference voice and requests local cloning on Apple Silicon, use the bundled IndexTTS-2 MLX wrapper:

1. Install the third-party runtime with `scripts/setup-indextts2-mlx.sh`.
2. Require the user to place a clean 6 to 12 second recording at `<project>/assets/voice-reference/reference.wav`.
3. Precompute `<project>/assets/voice-model/speaker-v2.npz` with `scripts/prepare-indextts2-voice.sh` and the explicit `--i-have-permission` acknowledgement.
4. Generate scene WAVs from `examples/voice-manifest.indextts2.json` using `scripts/narrate-indextts2.mjs`.
5. Keep the recording, speaker file and generated private narration outside the skill repository and disclose that the delivered narration is AI-generated.

Build a scene-by-scene music cue map after picture timing is locked. Prefer a bespoke full-length cue or compatible stems over looping a short stock bed. Keep background music low enough that narration remains primary and enable voice-triggered ducking in the production manifest. Use paper whooshes, soft clicks, pops and a restrained closing chime. Place sound effects on meaningful physical actions rather than every entrance.

Mix the final audio to the exact planned duration. Start music near 0.08 to 0.12 linear volume, target approximately -16 LUFS and keep the true peak no higher than -1.5 dB. Check mean and peak volume.

## Phase 6: Render and validate

For still keyframes, create a render manifest matching `examples/render-manifest.json`. Run:

```bash
node <SKILL_DIR>/scripts/render.mjs \
  --manifest ./render-manifest.json \
  --output ./renders/paper-collage-ad.mp4
```

The renderer calculates explicit input frame counts, applies scene transitions, encodes H.264 and AAC, and verifies stream duration and frame count.

For completed scene MP4s, voice tracks, music and sound effects, create a manifest matching `examples/production-manifest.json`. Run:

```bash
node <SKILL_DIR>/scripts/assemble.mjs \
  --manifest ./manifests/production-manifest.json \
  --output ./renders/final.mp4
```

The assembly renderer retimes scenes independently, places each voice and sound effect, loops and fades music, normalizes the mix, renders H.264/AAC and verifies exact stream duration and frame count.

Do not combine `-loop 1`, `zoompan d=1` and chained `xfade` filters. That combination can create a 30-second container whose video stream ends after the first scene while the audio continues. Generate an explicit number of frames from each still instead. The bundled renderer enforces this rule.

After rendering:

1. Confirm H.264 video and AAC audio are present.
2. Confirm width, height and FPS match the manifest.
3. Confirm both streams cover the full expected duration.
4. Extract one frame from the middle of every scene.
5. Assemble and inspect a contact sheet.
6. Check the opening, every transition and the final CTA hold.

Treat a valid container as insufficient. A playable MP4 can still have a truncated video stream.

## Hard-won production rules (from real ad builds)

- **Prefer real generators; the bundled ffmpeg paths are last-resort fallbacks.** For animation, prefer a real image-to-video model (e.g. Volcengine Seedance via the `arkcli +gen --generate-audio` toolchain) over `render.mjs` camera-push, which reads as a static image. For narration, prefer a real TTS or a reference-voice clone over macOS `say`. For music, download a fitting royalty-free track (e.g. Pixabay) rather than synthesizing a tone. See `references/dependencies.md`.
- **You cannot hear audio — the user's ear is the judge.** Never blind-pick a voice, music bed, or mix. Generate 2–4 candidates (voices A/B/C, a couple of tracks) and let the user choose; then tune levels by their feedback. Voiceover, sound effects and music quality are all decided by the user, not by you.
- **One visual language, all the way through — including on-screen content.** If the film is pure paper-cut, then the content shown *inside a screen* must also be paper-cut/halftone. A realistic photo or a glossy app icon dropped into a paper-cut world clashs and looks worse once animated.
- **Sound effects: describe them in the video prompt.** Seedance's `--generate-audio` synthesizes foley from the sounds you name in the prompt (paper rustle, shutter click, notification dings, ambience). Write the motion AND the sound into every clip prompt.
- **Use Gemini Omni for convergence, not final polish.** With ChatCut, `model: "omni"` is the fast 720p drafting route and `continueFrom` is the default for one localized change. Keep its prompt in English, never put exact CJK text in the generated frame, and move to a finishing route instead of stacking four or more edits.
- **Know the model's limits and be honest.** A video model cannot reliably do precise part-level constraints (e.g. "rotate only the outer shutter blades while the ear stays perfectly still" — it morphs the whole logo). Don't force it. Do exact logo/UI/text motion in the **HyperFrames route** (`references/hyperframes-route.md`): stack two copies of the paper-cut icon, rotate the outer one clipped to a circle, keep a static inner copy clipped to the center to lock the ear. Deterministic, and the text stays real HTML (never mis-spelled).
- **Proxy / env (behind Clash/TUN):** node's `fetch` needs `HTTPS_PROXY=http://127.0.0.1:7890` for foreign APIs. Do NOT use `set -a; source .env` before node calls — it pollutes the env and makes fetch time out through the TUN fake-IP; inject only the needed keys inline in a clean env.

## Quality bar

- Understandable without narration.
- One clear visual metaphor across the entire film.
- First joke or tension inside five seconds.
- Product arrives as the solution, not as a detached logo card.
- Every feature is demonstrated through a physical paper action.
- Brand color and icon remain accurate.
- Labels and URL are legible and correct.
- No malformed text, black frames or silent gaps.
- Final CTA remains visible for at least one second.
- Jokes have room to land; no line sounds squeezed into its scene.
- Raw reference voice remains private and is not included in public deliverables.

## Resources

- `WORKFLOW.zh-CN.md`: human-facing end-to-end Chinese guide from Codex installation through final MP4 delivery.
- `references/dependencies.md`: consolidated core and optional tool list; what each script needs.
- `references/collage-dimensions.md`: precise craft vocabulary and JSON fields.
- `references/prompt-patterns.md`: reusable keyframe and motion prompt structures.
- `references/fallbacks-and-qc.md`: TTS, FFmpeg and validation failures discovered in production.
- `references/local-layer-animation.md`: local no-model method for turning flattened keyframes into layered cutout motion.
- `references/audio-production.md`: comic narration, reference-voice separation, local IndexTTS-2, timing and mix targets.
- `references/music-scoring.md`: scene cue maps, suitable instrumentation, sourcing, candidate analysis and sidechain ducking.
- `references/production-workflow.md`: project layout, stage gates, duration strategy and handoff checklist.
- `references/hyperframes-route.md`: key-free, deterministic animation via HyperFrames (HTML+GSAP) — the precise-logo trick, the "animate real paper" rule, install and render commands.
- `references/gemini-omni-flash.md`: optional ChatCut Gemini Omni motion-draft and localized-edit stage, with routing rules and hard limits.
- `examples/storyboard.json`: scene-by-scene story template (role, idea, action, joke, label, draft duration).
- `examples/prompts.json`: style-anchor and continuity keyframe prompt manifest template.
- `examples/render-manifest.json`: still-keyframe render manifest template.
- `examples/layer-manifest.json`: layered local-animation manifest template.
- `examples/hyperframes-logo-composition.html`: HyperFrames starter — paper-cut icon two-layer shutter rotation (ear locked), real-HTML two-colour URL, GSAP text bounce.
- `examples/omni-pass.json`: copyable Gemini Omni first-frame draft and `continueFrom` localized-edit plans.
- `examples/production-manifest.json`: scene-video, narration, music and sound-effect assembly template.
- `examples/voice-manifest.indextts2.json`: local IndexTTS-2 scene narration template.
- `examples/project.gitignore`: privacy-safe ignore rules for user voice, audio and rendered project assets.
- `scripts/check-deps.sh`: preflight dependency check for the whole pipeline.
- `scripts/render.mjs`: deterministic keyframe-to-MP4 renderer with verification.
- `scripts/layer-animate.mjs`: deterministic layered stop-motion animator for one scene with verification.
- `scripts/assemble.mjs`: deterministic scene-video retiming, audio mix, rendering and verification.
- `scripts/extract-reference-voice.sh`: extract and separate a merged video soundtrack for authorized voice-reference selection.
- `scripts/setup-indextts2-mlx.sh`: install the optional Apple-Silicon IndexTTS-2 MLX runtime and model outside the skill.
- `scripts/prepare-indextts2-voice.sh`: normalize one authorized recording and create a private local speaker file.
- `scripts/narrate-indextts2.mjs`: render one local 48 kHz narration WAV per scene from the private speaker file.
- `scripts/privacy-check.sh`: reject tracked voice assets and obvious credentials before publishing.
