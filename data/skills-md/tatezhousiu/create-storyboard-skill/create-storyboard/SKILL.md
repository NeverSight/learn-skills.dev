---
name: create-storyboard
description: Create complete director-grade storyboard production packages for Image 2 and SceneDance/Seedance video generation. Use when the user provides a script, scene idea, ad concept, short drama, long-form drama, period drama, sci-fi animation, product video, or asks for 分镜图, 剧本分镜, SceneDance/Seedance 视频素材, Image 2/Img2 prompts, character consistency sheets, continuity bibles, shot cards, clip references, keyframes, Jianying/CapCut edit lists, or image-to-video production assets.
---

# Create Storyboard

## Mission

Turn a script into a SceneDance/Seedance-ready production package that behaves like it was prepared by a director, storyboard artist, editor, and AI video production coordinator. The output is not a list of visual descriptions; it is a continuity-controlled plan for generating many `0-15s` video clips that can be cut together smoothly.

Always optimize for:

- film continuity between independently generated clips
- one clear action chain and one main camera movement per SceneDance generation
- explicit action start/end and emotion start/end for every shot
- deliberate shot handoffs: each clip ending plants a visual, spatial, motion, or sound clue that the next clip receives
- reference-image discipline: character, scene, prop, keyframe, and storyboard inputs
- handoff and edit-point design before prompt writing
- post-production usability in Jianying/CapCut

## Runtime Assumptions

- The bundled scaffold script is deterministic and can run without an AI model once Python is available.
- Production storyboard planning needs a Codex-style agent that can read/write files, inspect scripts and generated artifacts, run the scaffold script, and revise production documents.
- Use a multimodal model when the task includes reference images, character sheets, keyframes, storyboard boards, or generated video/image review.
- Use a strong reasoning model for real production packages. The author-known-good profile is macOS, Codex-style local agent, GPT-5.5-class reasoning, and `xhigh` reasoning for complex packages.
- Use `high` reasoning for normal production work; use `xhigh` when available for long-form stories, multi-scene continuity, or dense handoff/edit matrices.
- Smaller models may run the scaffold but are more likely to weaken continuity, handoff logic, bilingual prompt consistency, deterministic board assembly, or QA decisions.
- For macOS/Windows/Linux setup details, read `references/runtime-and-platform.md` before promising reproducibility to a user.

## Hard Rules

- SceneDance/Seedance clips must be `<= 15s`.
- New projects default to `SH### = CLIP###`: one film shot equals one SceneDance video generation. A `CLIP###` may cover multiple shots only for low-risk inserts or when the user explicitly asks.
- A user request for "分镜图", "重新生成分镜图", "storyboard images", or "SceneDance inputs" means per-clip deliverables by default. Do not satisfy it with one full-film overview board unless the user explicitly asks for an overview/contact sheet.
- A full-film overview board, master storyboard sheet, or contact sheet is only for review. It is not a final SceneDance storyboard image and must not be counted as delivered `CLIP###` storyboard output.
- Every final storyboard image must cover exactly one SceneDance generation unit: `final_image_package/clip_storyboards/<CLIP###>_storyboard_<time-range>.png`.
- Final storyboard boards must be production boards, not AI-generated mood boards. Do not ask an image model to generate the final board layout, labels, captions, tables, or readable production text.
- Image models may generate only clean visual sources for storyboard boards: start panel, key-action panel, edit-out panel, handoff panel, or clean keyframes. Assemble the final storyboard board with deterministic local layout code, HTML/CSS screenshot, a design tool, or another controllable renderer.
- A final storyboard board must contain readable, deterministic production metadata: `CLIP ID`, time range, duration, scene/location, aspect ratio, tone/style, `START`, `KEY ACTION`, `EDIT OUT`, camera method, action start/end, emotion start/end, handoff-out, edit boundary, audio bridge, risk/fallback, and reference-image combination.
- Reject and regenerate/rebuild any storyboard board that has empty caption areas, missing `CLIP ID`, missing time range, missing start/key/edit-out structure, unreadable/garbled metadata, mixed multiple clips, poster-like composition, or lacks edit/handoff information.
- Durations are story-driven. Do not split by fixed totals such as 4 x 15s for a minute. Use `2-4s` for inserts/reactions, `4-7s` for clear physical actions, `8-12s` for sustained performance or atmosphere, and `12-15s` only for stable long takes.
- Every shot must define: purpose, duration, shot size, camera movement, composition, character state, action start/end, emotion start/end, receiver-in state, handoff-out state, motion vector, spatial bridge, occlusion carrier, visual bridge, reference images, SceneDance prompt, previous transition, next transition, edit note, risk, and fallback.
- Build the continuity bible before writing final prompts. Lock identity, wardrobe, hair, props, scene geography, 180-degree axis, eyelines, screen direction, light, weather, time state, color, aspect ratio, lens language, and key object positions.
- Design the handoff matrix and edit boundary matrix before image generation. Every neighboring pair needs what the prior clip hands off, what the next clip receives, spatial entrance/exit, motion direction, occlusion carrier, visual bridge, audio bridge, edit type, frame-match requirement, CapCut handling, and fallback cut.
- Default boundary strategy is editable continuity, not strict frame continuity. Prefer action match, eyeline match, screen-direction match, composition match, cutaway, insert, reaction, empty-room shot, occlusion cut, hard cut, J-cut, or L-cut. Use strict end-frame/start-frame matching only when the action truly must remain continuous.
- A boundary cannot be labeled only as "natural cut", "smooth transition", or "hard cut" unless the handoff design states the baton being passed, or the shot explicitly chooses a deliberate jump cut/emotional rupture.
- Do not ask SceneDance to solve complex multi-person blocking, multiple camera cuts, or too many action beats inside one generation. Split with close-ups, inserts, reactions, props, or atmosphere shots.
- Camera movement must be chosen for story and SceneDance stability, not repeated by habit. Use static shots only when motivated; consider tracking, lateral move, foreground occlusion push, pull-back reveal, handheld micro-move, POV, over-shoulder, low/high angle, door-frame peek, prop-led move, light-led move, or UI foreground occlusion when they serve the handoff.
- A storyboard board is not the main SceneDance input if it contains text/grid/multiple cells. The primary video input should be a clean keyframe from `final_image_package/clip_keyframes/` or `05_images/selected/`.
- If two neighboring shots are merged because their total duration is `<=15s`, they become one explicit `CLIP###` in `clip_plan.md`. Generate one clean start keyframe and one single-clip production storyboard board for that merged clip; do not feed SceneDance a two-panel or multi-shot board as the primary image.
- If the user has not specified aspect ratio, ask one concise question before final prompts or image generation. If target duration is not inferable, ask before final shot planning.

## Standard Workflow

1. Extract the brief: video type, audience/platform, target duration, aspect ratio, story intent, tone, characters/products, locations, props, dialogue/audio, and deliverable scope.
2. Analyze the script into scenes and dramatic beats. Identify emotional turns, physical actions, object interactions, reveals, and places where a shot can hand off the next space or hide generation discontinuity.
3. Create bibles:
   - `character_bible.md`
   - `scene_bible.md`
   - `product_prop_bible.md`
   - `style_bible.md`
   - `continuity_bible.md`
4. Build the asset plan: character turnarounds, expression sheets, pose sheets, scene establishing/reverse angles, prop/product sheets, clean start keyframes, key-action frames, edit-out frames, optional bridge frames, and final clip storyboard boards.
5. Create shot cards with one `SH###` per default `CLIP###`. For every shot, choose duration by action load, emotion, information density, cut rhythm, and handoff requirement.
6. Write the reference input matrix. Each SceneDance shot must list the primary clean input image and all auxiliary character/scene/prop/storyboard references.
7. Build `handoff_design_matrix.md` for every neighboring shot before final prompts. The previous clip must plant the next clip's space, motion, visual token, or sound cue; the next clip must begin by receiving it.
8. Build the edit boundary matrix from the handoff matrix. Use continuity editing: action match, eyeline match, screen direction, composition/rhythm match, shot-size progression, reaction, insert, cutaway, occlusion, J-cut, and L-cut.
9. Write Image 2 prompts in separate Chinese and English files. Do not mix languages in the same generation prompt.
10. Generate or prepare reference images first when image generation is requested. Generate clean visual panels/keyframes first, then assemble one deterministic production storyboard board per `CLIP###`. Do not use an AI-generated board layout as final output, and do not generate a full-film overview board unless explicitly requested as an extra review image.
11. Write SceneDance shot prompts: selected image, duration, receiver-in state, action start/end, emotion start/end, camera movement, continuity locks, handoff-out state, edit-out visual token, next-scene clue, edit handles, audio bridge, and avoid list.
12. Write post-edit materials: SceneDance usage list, edit continuity notes, Jianying/CapCut edit plan, risk/fallback plan, and image manifest.
13. Validate: every clip is `<=15s`, every shot has a handoff plan and boundary plan, every shot has a primary input image ID, every promised image path is tracked, and no recurring identity/space/style lock is missing.

## Production Package

Use the scaffold script for new packages:

```bash
python3 ~/.codex/skills/create-storyboard/scripts/create_storyboard_package.py <project-slug> --root <workspace-root> --title "<title>" --duration "<target-duration>" --aspect "<aspect-ratio>"
```

Omit `--aspect` only during planning. Final prompts and image generation require a confirmed aspect ratio.

When this skill folder is installed by itself, run the bundled smoke demo from the skill root:

```bash
python3 scripts/create_storyboard_package.py demo-storyboard \
  --root outputs \
  --title "Demo Storyboard" \
  --duration "30s" \
  --aspect "16:9"
```

The package contains:

```text
storyboard_projects/<project-slug>/
├── 01_script_brief/
├── 02_bibles/
├── 03_storyboard/
├── 04_prompts/
├── 05_images/
├── 06_delivery/
└── final_image_package/
```

For exact files and fields, read `assets/production_package_spec.md`. For the fillable production template, read `assets/storyboard_template.md`. For prompt structures, read `assets/img2_seedance_prompt_template.md`. For the detailed workflow and continuity/editing rules, read `references/storyboard_workflow.md`.

## Required Outputs

A complete production package must include:

- script analysis and project brief
- character, scene, prop/product, style, and continuity bibles
- asset generation list
- master storyboard and detailed shot cards
- SceneDance reference input matrix
- handoff design matrix
- edit boundary matrix
- Image 2 Chinese prompts and English prompts
- SceneDance shot prompts
- SceneDance usage list
- post-edit/Jianying/CapCut plan
- risk and fallback plan
- final image manifest

## Shot Card Schema

Every shot card must be human-readable Markdown and include a YAML block with these required keys:

```yaml
shot_id: SH001
clip_id: CLIP001
scene_id: S001
purpose: ""
duration: ""
shot_size: ""
camera_movement: ""
composition: ""
character_state: ""
action_start: ""
action_end: ""
emotion_start: ""
emotion_end: ""
receiver_in: ""
handoff_out: ""
motion_vector: ""
spatial_bridge: ""
occlusion_carrier: ""
visual_bridge: ""
handoff_risk_reduction: ""
reference_images: []
scenedance_prompt: ""
prev_transition: ""
next_transition: ""
edit_notes: ""
risks: []
fallback_plan: ""
```

## Editing Logic To Apply

Use film language deliberately:

- Establish geography before relying on eyelines or movement direction.
- Respect the 180-degree axis unless the shot card explicitly designs an axis reset.
- Treat every neighboring pair as a baton pass: the prior clip's ending must offer a receiver object, motion, foreground, light, color, doorway, UI layer, sound, or spatial clue that the next clip can inherit.
- Do not rely on AI interpolation to invent continuity between unrelated images. Design the video itself: camera movement, foreground occlusion, composition extension, spatial entrances/exits, and sound carry-over.
- Use eyeline matches: a character looks off-screen, then cut to what they see.
- Use action matches: a hand reaches, then cut to the prop close-up; a head turns, then cut to the reaction or POV.
- Use screen-direction matches: entering/exiting left/right must stay meaningful across space.
- Use shot-size rhythm: wide to medium to close-up for orientation, action, emotion; close-up to insert for detail; reaction shot to absorb discontinuity.
- Use inserts, props, empty rooms, occlusion, foreground wipes, door frames, passing vehicles, darkness, flashes, or motion blur to hide AI discontinuity.
- Use J-cuts and L-cuts: let dialogue, ambience, music, footsteps, object sounds, or impact sounds bridge across clips.
- Leave `0.5-1s` edit handles when possible, so generated starts/ends can be trimmed.

## Camera Language Library

Choose one main camera method per clip and state why it serves the shot or handoff:

- `locked-off`: stable observation, product clarity, visual contrast, or precise insert.
- `slow push-in`: emotional pressure, reveal, or attention narrowing; avoid using as the default for every shot.
- `pull-back reveal`: reveal a new space, hidden object, crowd, UI state, or consequence.
- `lateral track`: follow movement direction, hand off screen-left/screen-right geography, or pass behind foreground.
- `following track`: walk-with-character, corridor/doorway movement, entering a new space.
- `foreground occlusion push`: let a door frame, body, shelf, sign, smoke, rain, vehicle, or UI layer wipe the frame into the next clip.
- `POV / subjective`: receive an eyeline and show what the character sees.
- `over-shoulder`: preserve dialogue axis and spatial relation.
- `low/high angle`: emphasize power, vulnerability, scale, or product hero status.
- `handheld micro-move`: tension and human presence; keep motion small for SceneDance stability.
- `prop-led / light-led move`: let a held object, screen glow, flashlight, product reflection, or color field pull the viewer into the next shot.

## Image Generation Handling

When generating images:

- Generate Chinese-prompt images into `05_images/zh/`.
- Generate English-prompt images into `05_images/en/`.
- Put selected clean SceneDance inputs into `05_images/selected/`.
- Put final clean clip keyframes into `final_image_package/clip_keyframes/`.
- Put generated clean storyboard panel sources into `final_image_package/clip_storyboards/panels/` or another clearly named panel-source folder.
- Put deterministic final clip storyboard boards into `final_image_package/clip_storyboards/`.
- Put character, scene, product, prop, expression, and pose references into `final_image_package/support_assets/`.
- Keep filenames traceable: `<image-id>__zh__v01.png`, `<image-id>__en__v01.png`, `<image-id>__selected.png`.
- If direct filesystem saving is unavailable from the image tool, still create prompt files and record intended output paths. Mark image generation as blocked instead of implying reference-conditioned images exist.

## Storyboard Board Contract

Final `clip_storyboards/` files are deterministic production boards:

- Each board covers exactly one `CLIP###`.
- Each board uses clean visual panels or keyframes as image inputs; the board layout and all readable text are rendered by local deterministic tooling.
- Required visual panels: `START` / `KEY ACTION` / `EDIT OUT`. Add `RECEIVE IN` or `HANDOFF` only when it clarifies the boundary.
- Required readable fields: project/title, `CLIP ID`, time range, duration, scene/location, aspect ratio, style/tone, camera method, action start, key action, edit-out state, emotion start/end, receiver-in, handoff-out, edit type, audio bridge, reference-image combination, risk/fallback.
- Required source mapping: each visual panel must map back to a keyframe/panel path and each text field must come from `clip_plan.md`, `shot_cards.md`, `handoff_design_matrix.md`, `edit_boundary_matrix.md`, or `scenedance_shot_prompts.md`.
- Do not leave blank text boxes or placeholder captions in the final board.
- Do not rely on generated in-image text for production metadata. If an image model creates text, treat it as decorative noise and replace the board with a deterministic render.
- Do not call a final board complete until it can be read by a human editor without opening the Markdown files.

## Validation Before Delivery

Before finalizing:

- no SceneDance clip exceeds `15s`
- every new project shot defaults to `SH### = CLIP###`
- every shot card has all required YAML keys
- every shot has action start/end and emotion start/end
- every shot has `receiver_in`, `handoff_out`, `motion_vector`, `spatial_bridge`, `occlusion_carrier`, `visual_bridge`, and `handoff_risk_reduction`
- every shot has a primary clean input keyframe ID
- every shot lists its reference image combination
- every neighboring pair has a handoff design row
- every neighboring pair has an edit boundary row
- every boundary has a cut type, matching logic, audio bridge, CapCut handling, risk, and fallback, and references the handoff logic
- every recurring character/product/scene uses bible IDs
- Chinese and English Image 2 prompts are separated
- storyboard boards are not treated as the only SceneDance video input
- storyboard boards were assembled deterministically from clean panels/keyframes, not accepted as raw AI-generated board layouts
- every final storyboard board contains readable `CLIP ID`, time range, start/key/edit-out structure, camera/action/edit metadata, handoff, edit boundary, audio bridge, reference-image combination, and risk/fallback
- every final storyboard board has no blank caption areas, placeholder labels, missing timecode, mixed-clip layout, poster-like composition, or garbled production text
- all promised images are present or explicitly marked blocked
- final storyboard image count equals the final `CLIP###` count; overview/contact sheet images do not count
- `final_image_package/image_manifest.md` lists every delivered image and purpose
