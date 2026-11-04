---
name: collage-broll-explainers
description: Turn a ~5-second voiceover line, opinion sentence, or abstract concept into a premium editorial halftone paper-collage B-roll clip — optionally with a fitted voiceover. Load this skill whenever the user says "collage b-roll", "paper collage b-roll", "halftone collage", "collage-style visuals", "collage explainer" (or the Chinese triggers 纸拼贴 b-roll / 半调拼贴 / 拼贴风格配画面), or wants a script line turned into a collage visual metaphor. Enforces a mandatory three-gate approval flow — propose visual metaphors only, generate color collage stills only after the user confirms, and only after the stills are confirmed generate the assemble-from-empty animation. Video model is gemini-omni-flash, locked — no other video model is ever used and the choice is never offered to the user.
---

# Collage B-roll Explainers

Compress a ~5-second voiceover line into one sharp visual idea, then turn it into a premium editorial paper-collage assembly animation.

Default pipeline:

1. Design the visual metaphor only, then wait for the user to confirm
2. Generate the final still frame only, then wait for the user to confirm
3. Automatically generate the video with first/last-frame references and run QA
4. Optionally generate a fitted voiceover and mux it in

The two confirmation gates are part of the workflow, not overhead. They let the user spend their attention on aesthetics and direction, and prevent a wrong metaphor or a wrong still from burning video-generation cost.

## Runtime requirements

- **MaxFusion MCP** connected and authenticated (`https://mcp.maxfusion.ai/mcp`). All image, video, and speech generation runs through it. If it is not connected, stop and walk the user through connecting before doing anything else.
- **Local file access and ffmpeg** (e.g. Claude Code): frame preparation, video QA, silent delivery, and voiceover fitting download assets and process them locally. A sandboxed agent (no local downloads) can still run all three gates and display results in the MaxFusion widget, but must tell the user that frame preparation falls back to prompt-only color matching and that frame-by-frame self-QA, audio stripping, and voiceover fitting were skipped — the user should judge the clip by eye and mute it in their editor.

## Mandatory approval protocol

### Gate 1: Metaphor confirmation

When you receive the script line(s), propose visual metaphors first. Do not generate any image, do not generate any video, do not call any generation tool.

Deliver, for each line:

- Core meaning
- Emotion
- One-sentence visual proposition
- 3–6 key objects
- Suggested background color and local accent colors
- Intended assembly order

Then stop explicitly and wait for the user to reply "approved", "all approved", or give per-item revision notes.

If the user approves only some of the numbered items, only the approved items advance to Gate 2; keep iterating on the metaphors for the rest.

### Gate 2: Still-frame confirmation

Only after the metaphor is confirmed do you write the visual spec and the image prompt, and generate the final still with `maxfusion_generate_image`.

Save the originals into the project directory, build a numbered still contact sheet, display every still to the user (`maxfusion_display_generation`, one call per image, plus the numbered mapping), and stop again. At this stage you still do not generate any video.

If the user approves only some stills, only the approved items advance to Gate 3; regenerate the rejected stills and re-confirm them first.

### Gate 3: Video generation

Once the stills are confirmed, generate immediately. The video model is locked:

```text
video_model: gemini-omni-flash
```

No other video model is ever used. Do not offer a model choice, do not ask the user which model to use, do not fall back to anything else on failure — apply the repair playbook and re-run on gemini-omni-flash.

## Success criteria

- One line expresses exactly one clear metaphor
- A batch shares one design language, but is not forced onto a single blue background
- The background is a strong, flat, uniform color field, varied by meaning
- Subjects are built from black-and-white halftone photographic cut-outs
- Key cards, buttons, film strips, rulebooks etc. may use red, yellow, teal, orange, purple, or cream colored cardstock
- Every paper piece has crisp cut edges, a cream keyline, a soft low-opacity shadow, and paper grain
- Motion is assemble-from-empty — not gentle drift, wobble, or slow zoom
- No subtitles, no full script text, no logos, no watermark, no UI
- Default delivery: 9:16, 5 seconds, 720p, silent MP4 (audio track stripped) — or the voiced version when the user wants voiceover

## When NOT to use this skill

- Precise control of layers, occlusion, camera fly-throughs, or an editable timeline is needed: use a layered animation tool instead (e.g. an HTML-rendered layered video approach)
- The user only wants a video prompt, not a finished clip: just write the prompt, skip this flow
- The user needs a real-person product ad or an on-camera presenter: do not use this collage flow
- The user explicitly needs per-layer editable transparent assets: this skill does not deliver separated transparent layers

## Default project directory

Local working folder, named with the user's local date:

```text
~/collage-broll-projects/YYYY-MM-DD-<title>/
```

Recommended structure for batch projects:

```text
<project>/
├── brief.md
├── visual-spec.json
├── imagegen-prompts.md
├── omni-jobs.json
├── gate2-qa.md
├── gate3-qa.md
├── still-contact-sheet.jpg
├── omni-contact-sheet-all.jpg
├── video-first-frame-all.jpg
├── end-frame-comparison-all.jpg
├── 01-<concept-name>/
│   ├── omni-prompt.txt
│   ├── voiceover-raw.mp3            (optional voiceover stage)
│   ├── voiceover-trim.mp3
│   ├── frames/
│   │   ├── last-frame-original.png
│   │   ├── first-frame.png
│   │   └── last-frame.png
│   └── omni/run-v01/
│       ├── final-5s.mp4
│       ├── final-5s-noaudio.mp4
│       ├── final-5s-voiced.mp4      (optional voiceover stage)
│       ├── contact-sheet.jpg
│       ├── video-last-frame.jpg
│       └── end-frame-comparison.jpg
└── 02-<concept-name>/...
```

Also create a MaxFusion project via `maxfusion_create_project` (same name) and pass its id as `project_id` / `project_group_id` on every generation in the batch, so all assets stay grouped in the workspace. Track per item: the confirmed metaphor text, image job id + image id of the confirmed still, uploaded first/last frame `file_id`s, video job id + video id, and the QA verdict — and report these ids to the user with each gate so any item can be referenced or re-run individually.

## Phase 1: Design the visual metaphor

First compress the script line into a single visual proposition.

Extract:

- Core meaning: what must the viewer finally understand
- Emotion: calm, surprise, urgency, sudden clarity, absurdity, irony
- Action verbs: open, connect, leak, bind, archive, light up, compress, fork, assemble
- Visual metaphor candidates: machine, clock, film strip, filing cabinet, console, rulebook, funnel, rail track, chess piece

Do not put the script text verbatim into the frame. Default to one metaphor per line, held to 3–6 key objects; too many elements dilutes the meaning and makes the Omni assembly unstable.

Prefer metaphors a viewer recognizes from everyday life (a kettle, a snowball, a photo booth) over abstract ones — the spoken line does the bridging to the user's actual topic, so the visuals can stay wild without being obscure.

For batches, prefer metaphors that form a before/after narrative — e.g. first manual toil and experience leaking away, then codified process and human–machine division of labor.

### Gate 1 output example

```text
1. Core meaning: expertise gets consumed from scratch every single time
   Visual metaphor: a skilled editor circles a giant film-strip clock cutting frame by frame; the clock completes a full revolution yet yields only a short strip of finished film
   Key objects: film-strip clock, editor figure, scissors, short output strip
   Colors: burnt-orange field, cream and light-teal accents
   Assembly order: clock → figure with scissors → film strip → final short output
```

Output this and stop; wait for confirmation.

## Phase 2: Generate the color collage stills

After the metaphor is confirmed, first write a self-contained `visual-spec.json`, then the image prompt.

### Visual spec

```json
{
  "script_meaning": "",
  "visual_metaphor": "",
  "style_signature": "flat bold color field, mixed black-and-white halftone cut-outs and colored cardstock accents, crisp cut edges, cream keylines, soft paper shadows, editorial paper collage",
  "aspect_ratio": "9:16",
  "color_field": {
    "background_hex": "",
    "accent_colors": [],
    "paper_grain": "fine uncoated-paper fiber"
  },
  "elements": [
    {
      "what": "",
      "role": "",
      "motion": "",
      "placement": ""
    }
  ],
  "composition": {
    "layout": "",
    "negative_space": "",
    "final_frame": ""
  },
  "motion_plan": "structure first, subject or cards second, action and result last",
  "avoid": "typography, readable letters, numerals, logos, watermark, UI, subtitles, glossy 3D, photoreal environment"
}
```

### Color rules

Do not treat cobalt blue as the one default. Pick a strong color field from the meaning, and across a batch keep "same design language, different field colors":

- Burnt orange / red: time consumption, labor, urgency
- Mustard yellow: tools, warning, experience leaking away
- Ink green: cognition, taste, system reset
- Deep purple: rules, codification, long-term memory
- Teal: judgment, collaboration, autonomous execution

Subjects stay mostly black-and-white halftone, but every colored cardstock accent must serve the information hierarchy — never color for color's sake.

### Image prompt template

Generate with `maxfusion_generate_image` (default model, `aspect_ratio: "9_16"`, `quality: "high"`):

```text
Use case: ads-marketing
Asset type: final still frame for a 9:16 image-to-video B-roll clip
Primary request: Create a finished editorial paper-collage image expressing [one-sentence visual proposition].
Scene/backdrop: perfectly flat [color name] paper field [hex] with subtle uncoated paper fiber.
Style/medium: premium editorial stop-motion paper collage; black-and-white halftone photographic cut-outs mixed with selective [accent colors] colored cardstock.
Composition/framing: vertical 9:16 locked poster frame; central subject within the middle 70 percent; generous clean color-field negative space; 3–6 large separable paper groups for later assemble-from-empty animation.
Materials/textures: visible printed halftone dots, crisp machine-cut edges, thin warm-cream paper keylines, soft low-opacity physical drop shadows.
Constraints: [the one relationship this metaphor must communicate at a glance].
Avoid: no typography, no readable letters, no numerals, no logos, no watermark, no UI, no subtitles, no glossy 3D, no photoreal environment, no clutter.
```

If the scene contains any dial, clock face, gauge, or counter, add an explicit constraint that every mark on it is a plain tick line — never Roman numerals or digits. If the scene contains a sleeping figure, explicitly ban "Zzz" marks. Video models love sneaking these in.

Poll the job with `maxfusion_get_job` (`wait: 60`); download each still from its asset URL into `<item>/frames/last-frame-original.png` and record the image job id + image id.

### Still QA

- Is the metaphor readable at a glance
- Is the subject concentrated
- Any fake lettering, logos, watermark, or UI
- Enough pure color field left to assemble from an empty frame
- 3–6 clear large groups, not a screen full of confetti
- Across the batch: unified texture, varied field colors

Copy the passing originals into the project directory, build a numbered still contact sheet, show it to the user (plus `maxfusion_display_generation` per image), and stop for Gate 2 confirmation. Write the still QA verdicts to `<project>/gate2-qa.md`.

If the user asks to regenerate some stills, regenerate only those and produce `still-contact-sheet-v2.jpg` (v3, v4… on later rounds), keeping the old contact sheets for comparison — never overwrite them, and never reuse a rejected still downstream.

## Phase 3: Generate the video with Omni

### 1. Prepare first and last frames

Keep the imagegen original, then normalize the last frame:

```bash
ffmpeg -y -i <item>/frames/last-frame-original.png \
  -vf "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920" \
  <item>/frames/last-frame.png
```

The first frame is by default a pure empty paper field in the same background color as the last frame:

```bash
ffmpeg -y -f lavfi -i color=c=0x<HEX>:s=1080x1920 \
  -frames:v 1 <item>/frames/first-frame.png
```

(`<HEX>` is the `background_hex` from the visual spec — the same hex written into the image prompt, which is what keeps the two frames on the same color.)

Only if the user explicitly asks not to start from a fully blank field may the first frame retain one base structural object.

Upload both frames to MaxFusion with `maxfusion_upload_asset` (`purpose: "image_reference"`, `content_type: "image/png"`, exact `size_bytes`, `filename`): the tool returns an upload session — POST a multipart form to `upload.url` with every key/value from `upload.fields` exactly as given plus the file bytes as the final part named `file` (any 2xx = success), then use each returned `file_id`. Record the two `file_id`s per item.

### 2. Write the Omni animation prompt

Default action order:

```text
base structure → figure or key cards → connectors → action → final result
```

Prompt template (save per item as `<item>/omni-prompt.txt`):

```text
Paper-collage stop-motion assembly, using Image 1 as the exact empty first frame and Image 2 as the exact completed last frame. In one continuous locked-off vertical shot, open on the empty flat [color] paper field.

Assemble the scene piece by piece with crisp physical stop-motion timing: [describe, in order, how the 3–6 elements slide in, snap into place, connect, and complete the action]. End by holding the supplied completed composition.

Preserve the exact 9:16 framing, [hex] color field, colored cardstock accents, uncoated paper grain, halftone dots, cream keylines, crisp cut edges and soft shadows. Restrained tactile 2D paper craft only.

No scene cuts, no camera movement, no zoom, no morphing, no new objects, no text, no letters, no numbers, no logos, no watermark, no UI, no sound.
```

Every prompt must state that Image 1 is the empty first frame and Image 2 is the confirmed completed last frame. The final composition must land on Image 2 — do not let the model redesign it. Carry any anti-lettering constraint from the still prompt (tick-marks-only dials, no Zzz) into the video prompt too.

### 3. Submit the generation

One `maxfusion_generate_video` call per item. The reference-image order carries the frame roles: the empty first frame is the FIRST id, the normalized last frame is the SECOND, matching "Image 1" / "Image 2" in the prompt.

```text
video_model: gemini-omni-flash
ref_image_file_ids: [<first-frame file_id>, <last-frame file_id>]
prompt: <omni animation prompt>
duration: 5
aspect_ratio: 9_16
resolution: 720p
project_group_id: <batch project id>
```

Record the submitted jobs in `<project>/omni-jobs.json` (prompt, frame file_ids, job id, output path per item). Poll each job with `maxfusion_get_job` (`wait: 60`) until terminal, then download each finished video to `<item>/omni/run-v01/final-5s.mp4`. If an individual job fails, re-run only that job — never re-run items that already passed.

### 4. Enforce silent delivery

Even though the prompt says "no sound", still produce a zero-audio-track version with ffmpeg:

```bash
ffmpeg -y -i <run>/final-5s.mp4 \
  -map 0:v:0 -c:v copy -an \
  <run>/final-5s-noaudio.mp4
```

Deliver `final-5s-noaudio.mp4` by default; keep the original `final-5s.mp4` as an intermediate.

## Video QA

Do not judge from the end frame alone — check the assembly progression and the final landing.

### Contact sheet

```bash
ffmpeg -y -i <run>/final-5s-noaudio.mp4 \
  -vf "fps=1,scale=270:480,tile=5x1" \
  -frames:v 1 <run>/contact-sheet.jpg
```

Pass criteria:

- First frame is close to a pure empty color field; paper edges peeking in slightly at the borders are acceptable
- Mid-clip shows structure, figure, or cards entering step by step — not a global fade-in
- No cuts, no zoom, no 3D-ification, no drift into a photoreal scene
- No fake lettering, logos, watermark, or UI
- Final frame matches the confirmed still; minor pose or small-part drift (a slight figure pose change, a small part added or dropped) that does not affect the metaphor's meaning is a PASS — do not re-run for it
- Output is 9:16, 720p, 5 seconds, zero audio streams (verify with ffprobe)

Also extract the video's last frame and place it side by side with the confirmed still as `<run>/end-frame-comparison.jpg`. For batch projects, additionally merge three overview images:

- `omni-contact-sheet-all.jpg`: per-second frames of every finished clip
- `video-first-frame-all.jpg`: the actual first frame of every clip, verifying each truly opens on an empty color field
- `end-frame-comparison-all.jpg`: confirmed stills side by side with video end frames

Write the per-item QA verdicts — including the reasoning for any pass-with-noted-flaw — to `<project>/gate3-qa.md`.

### Repair playbook (common issues)

- Paper edges visible in the first frame: slightly acceptable; if a strictly empty opening is required, prepend the opening beat in a video editor
- Weak assembly feel: reduce the element count and rewrite the prompt as an explicit piece-by-piece slide-in / snap-into-place order
- End-frame drift: strengthen "Image 2 is the exact completed last frame" and "End by holding the supplied completed composition"
- Fake lettering appears (words, digits, Roman numerals on dials, "Zzz" on sleepers): go back and regenerate — a lettered still gets a new still; a lettered video on a clean still gets one video re-run with the explicit ban added to the prompt
- One video fails: re-run only that job, on gemini-omni-flash, never by switching models

## Phase 4: Voiceover (optional)

When the user wants the spoken line on the clip, generate it through MaxFusion and fit it locally.

### 1. Choose a voice

List voices with `maxfusion_list_platform_voices` (and `maxfusion_list_my_voices` if the user has saved voices) and ask the user to pick one. Do not design a new voice unless the user explicitly asks. Reuse the same voice for every item in a batch.

### 2. Generate and trim

Generate each line with `maxfusion_generate_speech` (the chosen `voice_id`, default `speed: 1.1` for a brisk read), download the mp3, and strip the trailing silence:

```bash
ffmpeg -y -i <item>/voiceover-raw.mp3 \
  -af "areverse,silenceremove=start_periods=1:start_threshold=-45dB,areverse" \
  <item>/voiceover-trim.mp3
```

### 3. Fit the 4–5 second window

Measure with ffprobe. The trimmed line must land between 4.0 and 5.0 seconds — shorter leaves dead air against the 5-second clip, longer gets cut off. TTS length varies ±1.5s between identical rolls, so always measure, never assume.

Fix ladder, in order:

1. Trim silence (already done above)
2. Too short → lengthen the copy slightly; too long → tighten it; regenerate at `speed: 1`
3. Last resort for a slightly-long line: inaudible tempo nudge, `-af "atempo=1.05"` maximum

### 4. Mux

Video stream is copied untouched; audio is padded to exactly 5 seconds:

```bash
ffmpeg -y -i <run>/final-5s-noaudio.mp4 -i <item>/voiceover-trim.mp3 \
  -map 0:v:0 -map 1:a:0 -c:v copy -c:a aac -af apad -t 5 \
  <run>/final-5s-voiced.mp4
```

## Default delivery

Deliver to the user:

- Each item's `<item>/omni/run-v01/final-5s-noaudio.mp4` — or `final-5s-voiced.mp4` when the voiceover stage ran (and display the generation in the MaxFusion widget via `maxfusion_display_generation`)
- Each item's contact sheet
- The batch overview contact sheet
- The end-frame comparison images
- One sentence per item explaining how the script line became its visual metaphor
- The batch's MaxFusion project name and the per-item ids needed to re-run or reference anything

If a defect stems from Omni's fast-generation limits, say so plainly; only suggest switching to a layered animation tool when precise layer control is genuinely required.

## Credits

The visual language, three-gate flow, prompt templates, color semantics, and QA/repair playbook originate from [gbro-collage-broll](https://github.com/pyang5166/gbro-collage-broll) by [pyang5166](https://github.com/pyang5166), originally written in Chinese for Codex with local Gemini scripts. This version is an English adaptation for Claude Code + MaxFusion MCP, with an added voiceover-fitting stage.
