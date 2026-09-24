---
name: minimax-h3-drama-producer
description: Produce or resume complete profile-driven videos in Codex with GPT-Image visual development, MiniMax-H3 shot generation through ComfyUI, optional voice and captions, sound design, deterministic FFmpeg editing, local delivery, and technical plus visual QC. Use when a user asks Codex to turn a story, campaign brief, script, storyboard, or reference bundle into a finished short drama, advertisement, social video, or other multi-shot video project under a standard outputs project directory.
---

# MiniMax-H3 Drama Producer

Own the complete local production project while keeping the sibling MiniMax-H3 skills reusable and prompt-focused. Preserve user-authored story, character, product, and brand decisions. Expand them only when the user asks or when an execution-blocking gap remains after inspecting supplied assets.

## Select mode and profile

Use `guided` mode unless the user asks to proceed immediately, says to use best judgment, or supplies `[mode=fast]`.

- In `guided`, ask one high-impact question at a time. Require a production-plan approval and then a visual-lock approval before batch H3 generation.
- In `fast`, make conservative assumptions, record them in the production brief, and continue without approval gates.
- If the user approves the plan and says later confirmation is unnecessary, skip the visual-lock gate.

Resolve one primary profile on top of `base-video`:

1. Use an explicitly supplied profile or profile path.
2. Otherwise choose from the platform and intended viewer outcome.
3. Ask only when two profiles would materially change the result.

Apply precedence in this order: current user instruction, project override, selected profile, `base-video`, built-in default. Never merge two primary profiles. Read [references/profile-spec.md](references/profile-spec.md) before selecting or resolving a profile.

## Preflight and initialize

Run the read-only environment preflight before expensive work:

```bash
python3 scripts/preflight.py --output <project>/logs/environment-report.json [--require-captions]
```

Pass `--require-captions` when the resolved profile or user instruction makes captions mandatory. Confirm the GPT-Image tool separately at agent runtime; the local report marks that check explicitly.

Do not install packages, download models, start services, or restart ComfyUI. If a critical capability is missing, finish every earlier stage that remains useful, mark the blocked stage in project state, and report the exact missing capability. A future doctor skill may consume the same report.

Create or resume the project with `scripts/init_project.py`. Read [references/project-contract.md](references/project-contract.md) for the directory contract and state rules. Use `scripts/project_state.py` for stage, job, artifact, and selected-take updates instead of rewriting the ledger ad hoc. Copy normal-sized inputs into `inputs/references/`; preserve original files and record their hashes and roles. Ask before copying unusually large inputs. Never overwrite an unrelated existing directory.

## Plan the production

Inspect the brief and all supplied text, images, video, and audio before asking for facts. Produce:

- a production brief with audience, platform, format, language, duration, and material assumptions;
- a story or message beat sheet without unrequested rewrites;
- a visual-entity ledger for recurring characters, products, mascots, animals, and environments;
- an asset ledger assigning every reference exactly one or more bounded roles and stating forbidden influence;
- a continuity plan covering identity, wardrobe or product geometry, environment, screen direction, props, lighting, and audio;
- a shot list with duration, framing, action, camera, sound, transition, reference roles, generation route, and QC intent;
- a material and generation budget that marks ordinary and key shots.

Read [references/production-workflow.md](references/production-workflow.md) for the canonical stage sequence. In guided mode, show the compact plan and wait for the production approval before image generation.

## Lock visual sources of truth

Read [references/visual-development.md](references/visual-development.md). Use supplied canonical sheets unchanged. When a recurring entity lacks a canonical sheet, load and apply the available `imagegen` skill, then use GPT-Image to create the appropriate character, product, identity, or scene master. Preserve loose source references and treat the generated sheet as a derivative, not a replacement for the originals.

Generate assets in dependency order:

1. recurring visual-entity masters;
2. scene masters with stable layout and light direction;
3. a complete visual storyboard;
4. one exact keyframe per shot that needs frame control.

Keep text labels out of generative images when exact typography matters; add labels deterministically afterward. In guided mode, show the masters, storyboard, and keyframes and wait for the visual-lock approval before H3 execution.

## Route and generate every shot

Choose one sibling specialist for each shot:

- no controlling media: read and apply `../minimax-h3-text-to-video/SKILL.md`;
- an exact opening frame or exact opening and closing frames: read and apply `../minimax-h3-frame-to-video/SKILL.md`;
- identity, design, style, motion, camera, performance, voice, or other multimodal references: read and apply `../minimax-h3-reference-to-video/SKILL.md`;
- a localized change to an existing generated clip: read and apply `../minimax-h3-video-editor/SKILL.md`.

Give every reference a bounded job. Prefer frame-to-video for shots with approved keyframes. Use first/last-frame control only for a continuous bridge whose ending must land exactly. After producing the prompt, read and apply `../minimax-h3-comfyui/SKILL.md` to prepare, validate, submit, monitor, and fetch the local ComfyUI result.

Generate one valid take for ordinary shots and up to two for profile-marked key shots. Retry once only for technical failure or an objective hard-gate failure. Do not exceed two valid takes per shot without user approval. Record workflow paths, prompt text, prompt IDs, settings, outputs, failures, and selection decisions in project state.

Default to synchronous completion. For explicit asynchronous requests, save prompt IDs and return; on resume, monitor those exact IDs rather than resubmitting them.

## Finish picture and sound

Treat voice and captions as `auto`, `on`, or `off`; the user instruction overrides the profile. Prefer user audio and voice references, then an available high-quality local TTS, then a disclosed system TTS fallback. Never call a paid voice service silently.

Prefer user-cleared audio, useful native H3 sound, locally synthesized effects, and configured licensed libraries in that order. Do not download music or reference video from the internet without explicit authorization. Record provenance and license notes.

Read [references/post-production.md](references/post-production.md) before assembling. Store the edit in `edit/timeline.yaml`; use the bundled deterministic audio, caption, and timeline helpers when their supported fields fit. Generate a project-local script only when the edit requires a documented feature the helper does not support.

## Enforce QC and deliver

Read [references/qc-policy.md](references/qc-policy.md), then run `scripts/qc_media.py`. Inspect the generated contact sheet visually and use `scripts/record_visual_qc.py` to record identity, product, environment, continuity, caption-safe-area, and narrative findings. Technical pass with visual review still pending is not an overall pass.

Do not mark the project complete while a hard gate remains. Preserve soft warnings in the report. A successful minimum delivery contains:

- `final/master.mp4`;
- `final/media-info.json`;
- `qc/qc-report.md` and `qc/qc-report.json`;
- `qc/final-contact-sheet.png`;
- `edit/timeline.yaml` and a reproducible export command or script.

Let the selected profile add previews, covers, clean masters, captions, stems, or alternate platform encodes. Do not publish or upload the result.

Return the finished video first, then link the project README or production brief, key visual sources, active profile snapshot, and QC report. Mention only material assumptions and remaining soft warnings.
