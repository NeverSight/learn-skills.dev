---
name: video-editing
description: Edit arbitrary supplied video, audio, images, screen recordings, and graphics into a polished deliverable. Use for cutting and restructuring footage, multi-track compositing, picture-in-picture, transitions, captions, sound work, color and framing changes, screen demos, presenter edits, social clips, and motion graphics made with FFmpeg, HTML, React, SVG, or Remotion. Includes source inspection, timeline design, reusable media tooling, transparent overlay generation, fast review artifacts, deterministic rendering, and technical validation.
---

# Video Editing

Edit whatever footage the user supplies. This is a general workbench, not a preset for one visual style. Treat each edit as an editorial system with observed source facts, explicit timing, an appropriate rendering engine, rapid review artifacts, and a validated master.

Set `SKILL_DIR` to the absolute directory containing this file. Resolve bundled scripts, references, assets, and examples relative to it.

When the primary request is to reverse-engineer a finished reference film—shots, camera behavior, sound, titles, pacing, and interview/B-roll grammar—use the adjacent `analyze-video-editing` skill first. When the request is to find, vet, or place cutaways against spoken words, use the adjacent `find-broll` skill before bringing its approved manifest into this editing workflow.

Initialize a neutral edit workspace when the task does not already have one:

```bash
python3 "$SKILL_DIR/scripts/video_workbench.py" init /path/to/edit-project
```

The generated `editorial-plan.json` is a human-and-agent planning artifact, not an executable timeline schema. Rendering remains explicit: an arbitrary FFmpeg graph through `render-ffmpeg`, a typed Remotion composition, or both. This avoids pretending a small schema can represent every edit.

## Start by observing

Never infer duration, dimensions, frame rate, stream order, rotation, color metadata, or audio from filenames. Inspect the real payloads:

```bash
python3 "$SKILL_DIR/scripts/video_workbench.py" inspect \
  --work-dir /path/to/work \
  /path/to/source-a.mp4 /path/to/source-b.mov
```

This writes raw probes, checksums, audio scans, and contact sheets. Add transcription only when speech content helps determine cuts:

```bash
python3 "$SKILL_DIR/scripts/video_workbench.py" transcribe \
  /path/to/source.mp4 /path/to/work/transcript
```

Review the sources before making an edit plan. Preserve the evidence for synchronization, speaker identity, orientation decisions, and important source defects.

## Choose the rendering lane

Use the smallest engine that comfortably expresses the edit:

- **FFmpeg:** trims, concatenation, reframing, speed, audio mixing, normalization, straightforward overlays, masks, fades, color transforms, and final encoding.
- **Remotion with React/SVG:** designed graphics, titles, captions, callouts, diagrams, data-driven scenes, browser typography, animated layouts, and mixed footage-plus-graphics work.
- **Hybrid:** render a transparent graphic overlay from Remotion, then composite it with footage in FFmpeg. This is often the cleanest lane.

Do not force a complex graphic into one unreadable FFmpeg expression. Do not create a React project for a simple cut.

Initialize the general motion project when useful:

```bash
python3 "$SKILL_DIR/scripts/video_workbench.py" init-motion /path/to/edit-motion
cd /path/to/edit-motion
npm install
npm run dev
```

The starter supports local footage, React layout, inline SVG, full-frame video, and transparent ProRes 4444 overlays. Read [references/motion-graphics.md](references/motion-graphics.md) before changing its render contract.

## Design the edit

Write down:

- delivery aspect ratio, dimensions, frame rate, duration target, and platform;
- source-time selects and output-time placement;
- track ownership: base picture, inserts, graphics, captions, music, effects, and dialogue;
- the purpose of every transition or layout change;
- audio hierarchy and loudness target;
- representative frames and transition ranges to review.

Keep source time and output time distinct. Use stable clip and beat identifiers. Derive frame numbers from one project frame rate instead of scattering timing arithmetic.

Read [references/workflow.md](references/workflow.md) for the full loop and [references/timeline-and-compositing.md](references/timeline-and-compositing.md) for reusable editorial and compositing principles.
For tested filtergraph building blocks and end-of-file choices, use [references/ffmpeg-recipes.md](references/ffmpeg-recipes.md).

## Work in cheap passes

1. Make an assembly with correct content and sync.
2. Make a low-resolution full draft.
3. Generate a contact sheet for rhythm.
4. Generate strips around every cut, transition, graphic entrance, and synchronization cue.
5. Render stills for composition, typography, safe areas, masks, and color.
6. Fix those artifacts before the master.

```bash
python3 "$SKILL_DIR/scripts/video_workbench.py" sheet draft.mp4 review/contact.jpg
python3 "$SKILL_DIR/scripts/video_workbench.py" strip \
  draft.mp4 review/transition.jpg --center 12.4 --window 1.6
python3 "$SKILL_DIR/scripts/video_workbench.py" stills \
  draft.mp4 review/stills --times 0,12.4,27.8
```

For independent quality control, give another agent the brief, source report, draft, contact sheet, and transition strips—not the implementation story—and ask it to report only concrete defects.

## Render safely

For a custom FFmpeg graph, put the graph in a file and describe the render in the generic plan format from [references/render-plan.md](references/render-plan.md):

```bash
python3 "$SKILL_DIR/scripts/video_workbench.py" render-ffmpeg render-plan.json
```

The workbench renders to a candidate, validates it, and promotes it only after it passes. Existing deliverables are archived reversibly.

For Remotion, typecheck before rendering. Use `useCurrentFrame()`, `interpolate()`, `spring()`, and `Sequence`; do not use timers, CSS keyframes, unseeded randomness, or runtime network calls. Render representative stills and ranges before a full master.

## Validate the deliverable

Run validation even when playback looks correct:

```bash
python3 "$SKILL_DIR/scripts/video_workbench.py" validate final.mp4 \
  --report /path/to/work/validation.json \
  --width 1920 --height 1080 --audio-rate 48000 --lufs -16
```

Validation checks the real output payload, full decode, expected geometry and duration when supplied, audio sample rate, loudness, and checksum. Read [references/quality-gates.md](references/quality-gates.md).

Deliver the master together with the source report, edit plan or source project, review artifacts, render command, validation report, and checksum.

## General principles

- Let meaning determine transitions; motion without an attention change is decoration.
- Keep the viewer oriented. Establish spatial context before aggressive crops.
- Make text readable at delivery size, not merely on a large monitor.
- Prefer authentic interface recordings over invented screenshots.
- Preserve original dialogue unless replacement was requested.
- Normalize dialogue before the final sample-rate conversion.
- Crossfading differently scaled copies often creates ghosting; use a motivated cut or animate one continuous layer.
- When an overlay source ends early, decide explicitly whether to hold, disappear, or reveal the base.
- Use alpha-capable assets and codecs for reusable graphics; never fake transparency with a guessed background color.

## Keep solutions general

Do not turn one successful edit into a default style. Preserve reusable mechanics—inspection, timing, compositing, motion systems, review artifacts, and validation—while choosing layouts, graphics, transitions, and sound treatment from the current material and brief.
