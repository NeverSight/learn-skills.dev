---
name: hypermotion-explainer-director
description: Direct and produce editable, multi-scene Hyper Motion product explainer videos from information gathered through direct prompts, MCP clients, connected apps, repositories, URLs, documents, product captures, brand assets, and music or narration. Use when asked to research context, storyboard, build, revise, beat-sync, validate, or render a feature explainer that combines text scenes, animated product demonstrations, feature callouts, and a logo outro into a .hype project and final MP4, WebM, or GIF.
---

# Hyper Motion Explainer Director

Turn source material into a directed sequence of distinct scenes. Keep narrative decisions in the plan and use deterministic Hyper Motion tools for scene creation, timing, validation, and rendering.

## Operating principles

- Treat the deliverable as a sequence, not one continuously animated product screen.
- Use the model to choose the story, emphasis, pacing, and shot grammar. Use tools or compiler code to generate repetitive layers, offsets, and keyframes.
- Preserve editability: use native text, frames, shapes, vectors, components, variants, and instances when supported. Use raster fallbacks only for web content Hyper Motion cannot reproduce faithfully.
- Preserve one clear idea per scene. Give the viewer time to recognize the screen before moving the camera.
- Synchronize meaningful events, not every keyframe. Prefer narration cues for meaning and musical beats for accents.
- Never claim a scene, analysis, preview, or render succeeded without tool evidence.

## Gather the production brief

Treat every available source as optional input, not as a required channel. Gather relevant information from:

- The current conversation and direct user instructions.
- MCP clients and connected apps such as Slack, Google Drive, Notion, email, issue trackers, and project-management systems.
- Local repositories, source code, documentation, design files, URLs, and running applications.
- Attached audio, video, images, transcripts, scripts, brand guides, and campaign briefs.
- Existing Hyper Motion scenes and prior approved output.

Use only connectors and sources available and authorized in the current environment. Do not imply access to a source that was not actually inspected.

Collect or infer only low-risk details:

- Objective, audience, key message, and call to action.
- Desired duration, aspect ratio, frame rate, output format, and output folder.
- Product repository or running URL, start command, authentication/test data, and feature flow.
- Audio file and whether it is music, narration, or both. Request a transcript when accurate semantic timing matters and one is not available.
- Logo, fonts, brand profile, screenshots, and any prohibited content.

Normalize gathered information into the brief contract in [brief-and-storyboard.md](references/brief-and-storyboard.md). Preserve source provenance and identify conflicts, uncertainty, and missing decisions. Do not make Hyper Motion itself depend on any communication or storage provider; resolve external context before calling Hyper Motion.

## Inspect capabilities before authoring

Call `doctor` and `get_capabilities` when the Hyper Motion MCP server is available. Use the returned node kinds, property ids, patch operations, formats, and qualities as the source of truth.

Do not invent missing MCP tools. In particular, capability-gate audio analysis, beat-grid editing, speech alignment, web-flow capture, frame previews, and contact-sheet rendering. When a required tool is absent:

1. Use an existing safe tool or an already prepared artifact.
2. State the missing capability precisely.
3. Ask for the smallest missing input only if no safe fallback exists.

## Build the storyboard before the scene

Create a scene-by-scene plan before writing `.hype` data. Read [brief-and-storyboard.md](references/brief-and-storyboard.md) for the plan contract.

Use a narrative spine appropriate to the brief, usually:

1. Hook or problem.
2. Product context.
3. Triggering action.
4. Feature mechanics or state progression.
5. Outcome and benefit.
6. Logo or call-to-action outro.

Do not force all six stages into short work. A 10–15 second piece normally supports four to seven scenes.

Assign each scene a local duration, purpose, focal subject, entry, hero action, exit, and timing anchors. Keep scene-local timing zero-based in the plan, then offset it onto the master timeline during compilation.

## Acquire product states

For product-demo scenes, read [web-product-capture.md](references/web-product-capture.md).

- Prefer a running application over source-only inference.
- Capture deterministic checkpoints such as dashboard, form, filled, submitting, success, and error.
- Record viewport, route, action, DOM bounds, computed styles, text, accessible names, SVG/image assets, and stable identifiers.
- Redact secrets, personal data, and irrelevant browser or editor chrome.
- Map stable UI elements across checkpoints before generating variants or shared-element motion.

If a capture/compiler tool is unavailable, use user-provided screenshots or build a scoped native reconstruction from inspected code. Clearly label raster fallbacks.

## Author scene types

Read [scene-types-and-motion.md](references/scene-types-and-motion.md) before composing scene layers or camera tracks.

Choose among:

- `text`: a hook, bridge, benefit, statistic, or call to action.
- `product-demo`: a captured screen and its interaction/state sequence.
- `feature-callout`: a product view with highlights, labels, masks, or an exploded 3D explanation.
- `comparison`: before/after or two-state contrast.
- `media`: an image or supplied video.
- `logo-outro`: a brand-respecting closing resolve and hold.

Use Hyper Motion's first-class project sequence:

- Create one independent composition per storyboard scene, with its own root,
  local duration, layers, animation tracks, camera ownership, default camera,
  and authored camera cuts.
- Use each composition's optional `workArea: { start, end }` for the source
  range that should appear in Master. Omission means the complete composition.
  Sequence-item trims may narrow this range for an occurrence but never expand
  beyond it.
- Add ordered sequence items that reference those compositions. Keep
  composition timing zero-based; sequence items map local time to master time.
- Put the outgoing transition on each sequence item. Use `cut` for a hard edit
  and `crossfade` only when an overlap is narratively useful.
- Capability-check the requested codec before promising transition fidelity.
  Current MP4/GIF sequence rendering composites true crossfades; use cut-only
  assembly for WebM unless the connected Hyper Motion version advertises a
  WebM crossfade compositor.
- Keep master audio continuous across the sequence. Scene-local media must be
  deliberately offset or owned; do not accidentally stack several local audio
  clips at master time zero.
- Treat parentless audio as the Master soundtrack and parented audio as a
  Scene-local overlay. A Scene preview and Scene-only export must borrow the
  exact selected occurrence window from Master, not restart the soundtrack.
- Preserve projected Master bar numbers and beat/subdivision guides in each
  Scene timeline so keyframes can snap in Scene-local time. An occurrence mute
  silences only the borrowed Master bed and never removes its timing guides or
  mutes Scene-local overlays.
- Use the Scene timeline to author a composition and the Master timeline to
  review scene order, boundaries, overlaps, and the complete runtime.
- Use timeline sections only as optional chapter labels inside a composition;
  sections do not own layers, define the persisted work area, or replace
  sequence scenes.

## Direct motion and 3D

- Choose one hero motion per scene.
- Use restrained supporting motion to establish hierarchy and causality.
- Prefer exponential deceleration (`ease-out-quart`, `ease-out-quint`, or `ease-out-expo`) and faster exits.
- Use transform and opacity for most motion. Animate layout properties only when the layout change is the subject and Hyper Motion supports the semantic property.
- For product interactions, show cause before effect: focus, pointer/press, state transition, then confirmation.
- Use `renderMode: "plane"` for independently staged UI surfaces and `renderMode: "group3d"` for groups that must preserve child depth.
- Separate only meaningful layers in Z. Keep labels readable and avoid decorative explosion of every DOM node.
- Give each composition one or more owned cameras and a valid default camera.
- Author scene-local camera cuts for intentional shot changes; a camera chosen
  only as the editor view must never change program output.
- Default camera focal length to 1000 unless the brief requests another lens feel.
- Avoid bounce, elastic easing, excessive depth-of-field, continuous camera drift, and motion on every beat.

## Time against audio

Read [audio-timing.md](references/audio-timing.md).

- For music, align scene boundaries and major reveals to strong bars or beats.
- For narration, align product actions to the matching word or phrase.
- For mixed audio, use narration for semantic events and beats for emphasis.
- Keep concurrent keyframes that form one event together when beat-syncing.
- Preserve a readable final logo hold even when the audio ends abruptly.

Use `analyze_audio`, `set_beat_grid`, and `sync_keyframes_to_beat` only when they appear in capabilities. Otherwise use persisted beat data, supplied BPM/markers, or explicit absolute timing.

## Create, validate, preview, and render

1. Create the `.hype` project with `create_scene`, including its composition
   scenes and ordered sequence when those fields are available.
2. Inspect structure with `info_scene`, `inspect_scene`, `list_scenes`,
   `get_sequence`, and targeted list/get tools.
3. Run `validate_scene`; fix every structural error.
4. Open or preview the scene when supported.
5. Review representative frames at scene starts, hero moments, transitions, and the final hold.
6. Check visual fidelity, cropping, readability, timing, audio alignment, camera continuity, and empty frames using [validation-and-delivery.md](references/validation-and-delivery.md).
7. Patch only the necessary nodes or tracks.
8. Render a low-cost proof before the final quality render when render time is material.
9. Render the requested format to the requested folder.
10. Return both the editable `.hype` path and rendered media path.

Do not stop at a storyboard when the user asked for a finished video and the required tools are available.
