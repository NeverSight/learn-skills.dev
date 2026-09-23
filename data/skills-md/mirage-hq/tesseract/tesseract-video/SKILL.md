---
name: tesseract-video
description: Edit existing footage into finished videos locally with Tesseract. Make cuts, preserve dialogue, add purposeful sound design, mix audio, and decide where native motion-graphics scenes or overlays improve the story. Use for video editing and revising Tesseract projects, not avatar or video generation.
---

# Edit video with Tesseract

The CLI may send basic usage telemetry for some commands. You can provide optional attribution via `TESSERACT_SKILL=tesseract-video` and the [other attribution variables](references/telemetry.md). Respect the CLI's telemetry opt-out setting; never enable telemetry on the user's behalf.

Make a deliberate edit from the user's material. Tesseract is the local editing and rendering engine; the agent supplies editorial judgment. The output is both a playable video and its editable project.

## Start with the material

1. Resolve this skill's root from the directory containing this `SKILL.md`. Read [CLI installation](references/installation.md) and check the required Tesseract version once per session. Use the resolved executable path throughout the task. Scripts and references are relative to the installed skill, not a guessed home directory or development checkout.
2. Read [local operation](references/local-operation.md). Probe the supplied media, sample frames at meaningful points, and listen to its audio using the host's available media tools. Metadata does not tell you what a shot depicts. If audio cannot be auditioned, disclose that limit rather than claiming a complete review.
3. Establish the deliverable, audience, aspect ratio, duration, must-keep moments, and supplied brand assets from the request. Ask only for missing information that materially changes the edit. For a small correction, preserve the existing edit's style and scope.
4. Read [editorial decisions](references/editorial-decisions.md) before planning a new edit. For each beat decide **footage**, **footage with graphics**, or **full graphics** and why. This is not a quota: do not add motion graphics just to demonstrate the engine.

For a new ad or a revision to its opening, read [ad hooks](references/ad-hooks.md). Build a visual hook in the opening seconds from the actual footage, proposition, and evidence. Consider distinct concepts, select the strongest, and map its reveal/motion and purposeful SFX to confirmed opening music cues when music is provided. Render and inspect the hook plus its handoff into the ad before polishing the rest. Preserve the scope of unrelated revisions.

Read [waveform editing](references/waveform-editing.md) when music sets the pacing or when trimming talking footage. Generate and **open** the music waveform before planning picture timing; confirm beats, phrases, and major changes by listening and map visual arrivals to them. For speech, use overview and zoomed source waveforms to choose pause trims, protect quiet word boundaries, and retain natural breathing. Waveform markers are candidates, never automatic cut decisions.

For a substantial new video, share a concise edit plan with the source moments, their narrative purpose, graphic treatment, and audio intent. Routine authorized edits can proceed. Do not require a new approval for every local preview or revision.

## Author the edit

- New edit: `tsrct project create` creates a portable `.tsrct` document; import local footage before placing its layers. Existing `.tsrct`: inspect and check out a copy of its editable JSON. Preserve the original and stable IDs. Save JSON through `project commit`, or apply supported action batches with `project apply`, before rendering.
- Read [native authoring](references/native-authoring.md) before changing project structure. Source time, edit time, and layer time are different clocks. In particular, moving a clip must not silently change which source moment it plays.
- Keep footage cuts, full scenes, and editable overlays as native layers in the document's single composition. Use groups for scenes. `activeRange` places a clip in its parent; `sourceRange` selects the source moment. Do not create base-video, caption, or audio tracks.
- For talking-head cuts, follow [eyeline continuity](references/editorial-decisions.md#talking-head-eyeline-continuity): align the speaker’s eye height and screen position across cuts with appropriate framing, including punch-ins. Check the rendered outgoing/incoming frames and playback while preserving natural head movement and intentional camera changes.
- For motion work, read [motion design](references/motion-design.md), then only the relevant authoring reference. The examples demonstrate real schema; their visual style is not a required template.
- For every new edit or sound pass, read [sound design](references/sound-design.md). Consider dialogue, music, micro-SFX, structural cues, and foley/ambience; use the roles the piece needs. Add appropriate sounds from supplied/local assets or the procedural helper without per-cue approval. Import the selected files with `project import-asset --kind audio`, then keep them as editable Audio layers. Use [audio and timing](references/audio-and-timing.md) for placement, ducking, local preparation, and measurement. Preserve useful source audio and chosen music. Do not produce invented speech or captions.
- When talking audio needs cleanup, read [speech cleanup](references/speech-cleanup.md). Diagnose room noise versus reverb/echo, use restrained EQ/dynamics or local noise reduction as appropriate, and compare at matched loudness. Preserve voice detail and timing; the plugin has no bundled dereverberation model.
- Keep typography, graphics, footage, and audio native and editable. Import supplied images as assets with `project import-asset --kind image`, not as a flattened replacement for text, vector graphics, or entire scenes. Use existing footage; this plugin provides no generative-video or avatar service.
- Respect the user's brand references. Mirage branding identifies this plugin, not every video created with it.

## Look up capabilities only as needed

Use the installed CLI's schemas through [local operation](references/local-operation.md).

Read [capabilities](references/capabilities.md) for the feature map and limits,
[FX authoring](references/fx-authoring.md) for native layers and footage, and
[motion](references/motion.md) for supported keyframe and script actions. Search
for the specific definition needed rather than dumping the whole schema. The
action schema includes supported standalone operations and their field restrictions; use
[local operation](references/local-operation.md) to choose actions versus JSON
checkout/commit. The installed schema and actual render are authoritative.

## Review and handoff

Use [filmstrip review](references/filmstrip-review.md) to inspect and correct visual
changes. For dialogue cuts and music timing, follow [waveform editing](references/waveform-editing.md).
Finish with [review and delivery](references/review-and-delivery.md); report actual
checks and any limitations. Use absolute local file links and show the video inline
when supported. Premiere round-trip, cloud sync, and publishing are not implemented.

If the host cannot execute local commands or access the local GPU/filesystem, explain that this package needs a local execution environment. Do not substitute a hosted service or silently switch rendering engines.
