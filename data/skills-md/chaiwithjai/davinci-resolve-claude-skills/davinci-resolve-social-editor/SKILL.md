---
name: davinci-resolve-social-editor
description: Plan, analyze, and build professional DaVinci Resolve social edits from multicam video/audio folders, podcast/interview footage, vertical 9:16 deliverables, branded social promos, burned-in captions, B-roll/overlay coverage, Resolve timelines, FCPXML/EDL handoff, or FFmpeg preview renders. Use when Codex must avoid jump cuts, preserve narrative coherence, keep the speaker in frame, balance dialogue/music, create reviewable edit decisions, or automate Resolve media/timeline setup.
---

# DaVinci Resolve Social Editor

## Core Rule

Do not cut from transcript text alone. Build a story-first edit plan, then prove it with media analysis, frame checks, audio checks, and a Resolve-ready review artifact.

The failure mode to avoid is a technically valid cut that is semantically broken: sentence fragments, jump cuts, subject out of frame, captions that do not match, or music competing with speech.

## Required Workflow

1. **Ingest and audit**
   - Scan media with `scripts/probe_media.py <project-root> --out <manifest.json>`.
   - Identify camera ISOs, HQ audio, existing Resolve projects, brand images, and prior renders.
   - Detect unusable tracks early: silent WAVs, black cameras, missing audio, mismatched duration, or odd frame rates.

2. **Sync and source strategy**
   - Prefer Resolve multicam/sync-bin or waveform sync for real edits.
   - If scripting outside Resolve, treat FFmpeg preview renders as review proxies, not the final edit model.
   - If HQ audio is silent or unusable, explicitly fall back to embedded camera audio and say so.
   - For repeat hard-drive folder inputs, use the `social-video-folder-autocutter` skill first to create the format plan, then return here for Resolve implementation.

3. **Story plan before cutting**
   - Produce a short `story_plan.md` before rendering:
     - Hook/agenda: “tell them what you will tell them.”
     - Body beats: the complete ideas in order.
     - Recap/CTA: “tell them what you told them.”
   - Use transcript timestamps only to locate source ranges. Never cut mid-idea just to hit a duration.
   - Prefer longer coherent blocks over many word-boundary edits.

4. **Edit decision list**
   - Create a human-readable `edit_decisions.csv` or JSON with:
     - source file, in/out, selected camera angle, reason for cut, story beat, transition type, crop/framing notes, audio source.
   - Every hard cut needs a rationale: new beat, angle change, gesture emphasis, B-roll, title card, or intentional stylistic hit.
   - If the same camera/crop appears on both sides of a cut, use B-roll, a punch-in/punch-out, or dissolve. Do not create visible jump cuts.

5. **B-roll plan and coverage**
   - Treat B-roll as visual evidence, not filler. For each cutaway, record the claim it proves, the story beat it supports, and the edit problem it solves.
   - Build a `broll_plan.json`/CSV before placing B-roll with: beat, spoken line/context, source clip, source in/out, shot type, reason, placement, duration, and whether it covers a jump cut.
   - Prefer a sequence grammar: establishing/wide for context, medium for action, close-up/detail for proof. A single random stock insert is weaker than a planned sequence of coverage.
   - Use authentic or context-matched moments where available. If using stock, reject clips that feel metaphorical but do not visually match the claim, audience, event, or brand world.
   - Use project-native B-roll first: whiteboards, room details, hands, laptops, forms, audience, signage, tea/desk objects, and event/workshop artifacts. These should beat generic stock whenever they prove the speaker's exact claim.
   - Use Coverr as the default free stock B-roll source when native coverage is missing. Every downloaded asset must have a `broll_asset_manifest.json` row with query, source URL, license/attribution note, local path, selected segment, intended beat, and rejection notes for alternates.
   - Build search queries from the story plan, not from generic keywords. Example mappings: "AI falls short" -> `laptop frustration`, "Business Model Canvas" -> `business planning whiteboard`, "small room of entrepreneurs" -> `workshop collaboration`, "free/donation based" -> `community event`.
   - Hold B-roll long enough to read on mobile, usually `1.2s-3.0s`, but avoid covering crucial face/emotion beats unless the A-roll cut is broken.
   - Place B-roll on complete semantic beats: after a phrase lands, at breaths, on new ideas, or over obvious jump cuts. Do not interrupt the sentence fragment that carries the message.
   - Match visual direction and energy when cutting back to A-roll. Avoid disorienting motion, unreadable crops, or unrelated locations that make the viewer ask why they are seeing it.
   - Use full-opacity cutaways or clearly designed picture-in-picture. Low-opacity B-roll over faces is a last-resort texture and must pass still inspection.
   - If the user likes the cut and only wants improvements, do not rebuild the spine just to add B-roll. Add a limited B-roll pass over obvious jump cuts/proof beats, then regenerate captions and verify.

6. **Frame safety**
   - The speaker must remain visible during spoken sections.
   - Reject black or blank camera angles during ingest; do not leave them available for automatic angle selection.
   - Reject any region where the speaker face/body is absent unless covered by intentional B-roll, branded card, graphic, screenshot, or cutaway.
   - For vertical output, keep eyes near the upper third and keep captions out of the face/mouth region and social UI danger zones.
   - Generate verification stills at representative timestamps before final answer.

7. **Audio**
   - Voice is primary. Music is texture.
   - Treat audio as the emotional spine of the edit, not an afterthought filter pass. Build the sequence around the best dialogue stem, then add music, foley, transitions, and picture changes around that spine.
   - Run `scripts/audio_quality_audit.py` before choosing the dialogue source and keep the JSON report with the edit artifacts.
   - Audit channel balance before processing. If a lav/recorder track has one weak channel and one usable channel, duplicate the good channel to centered dual-mono before compression, denoise, music ducking, captions, or Resolve handoff. Do not treat broken stereo as a publish mix.
   - Keep repair/reference audio disabled by default. A bad original camera WAV must not remain enabled underneath a clean dialogue stem.
   - Use ducking/sidechain or very conservative music gain. Do not rely on a fixed loud bed.
   - Run a loudness check. Target social dialogue around `-14` to `-16 LUFS integrated` with true peak below `-1 dBTP`.
   - If music is present, verify it does not mask speech during dense spoken sections.
   - For creator-business and workshop videos, define the audio treatment before rendering:
     - dialogue repair/EQ/compression/limiter,
     - music bed selection and ducking depth,
     - foley/SFX moments,
     - L-cut/J-cut moments,
     - target LUFS and true peak.
   - Add tactile brand foley only when motivated by the visual or transition, such as tea cup, marker, keyboard, paper, or a soft UI tick. Random sound effects are worse than silence.

8. **Color and branding**
   - For PBS/60 Minutes style, use a clean documentary grade: neutral skin, moderate contrast, lifted mids, restrained saturation, no crunchy LUT.
   - Treat logos as brand bugs or title/end cards. Do not cover the speaker’s face.
   - If keying white backgrounds from logos, inspect stills for halos or accidental transparency issues.

8a. **Named Style Target**
   - Before building graphics, captions, music, or B-roll, name the target creator style and write a one-paragraph style brief. Do not render a "generic professional" video.
   - Prefer asset-led production over hand-rolled visual effects when the quality bar is YouTube-native or paid-social-native. Use proven Resolve templates, licensed music/SFX, and style packs before drawing custom FFmpeg overlays from scratch.
   - Before hand-rolling lower-thirds, captions, transitions, or callouts, search for existing local/project assets and known Resolve template sources such as Mixkit, Motion Array, Envato Elements, The Modern Filmmaker, or the user's installed PowerBins/templates.
   - Never use unlicensed music, SFX, templates, or stock footage. If paid assets require account access or purchase, produce an acquisition manifest and ask for access rather than substituting weak generated approximations.
   - Use benchmark-derived style languages, then adapt them rather than copying a creator exactly:
     - `Creator Business Systems` from Deya/Modern Millie: clean, bright, business workflow, key-term overlays, screenshots, calm music.
     - `Evidence-First Productivity Educator` from Ali Abdaal/Vanessa Lau: fast value contract, proof stack, numbered agenda, screen evidence, close vocal.
     - `Guided Session Retention` from MadFit/Chloe Ting/Caroline Girvan: progress/timer, high-key clarity, rhythmic pacing, next-step previews.
     - `Tactile Documentary Teacher` for Chai With Jai: speaker-led authority, whiteboard/canvas evidence, warm studio, tea/keyboard/marker foley, restrained premium graphics.
   - For a Deya-informed workshop/business cut, run a hard style comparison before polishing:
     - camera grammar: main face angle, context angle, evidence angle, screen/slide insert,
     - designed visual system: title cards, checklist/roadmap, key-term overlays, screenshot proof, CTA screen,
     - retention mechanics: no more than 6-9 seconds of uninterrupted A-roll without a visual reset,
     - audio personality: close clean voice, calm music, tasteful UI/desk/tea/marker foley,
     - workflow proof: show the actual framework, page, form, canvas, or artifact being discussed.
   - If the comparison shows the edit is only a captioned podcast cut, stop polishing and rebuild from a storyboard with visual assets first.
   - Score style fidelity separately from technical correctness. A video can pass export checks and still fail because it looks programmatic.
   - For a "5K-view quality bar", require an asset manifest covering visual templates, music bed, foley/SFX, fonts, captions, and color look. If the asset manifest is empty, do not claim premium production value.

9. **Resolve handoff**
   - Prefer creating/importing into a Resolve project/timeline for review:
     - bins: `Video ISO`, `HQ Audio`, `Brand`, `Renders`, `Review`.
     - timelines: one editable timeline and one rendered-master timeline.
   - A flattened rendered master is not an editable deliverable by itself. For user-facing Resolve handoff, create a layered source timeline whenever possible:
     - original camera cuts on their own video track,
     - original dialogue/audio cuts on a repair track,
     - clean dialogue mix on a separate enabled track,
     - original repair audio disabled by default,
     - music, SFX, captions, graphics, B-roll, and master reference on separate named tracks.
   - For HITL review, include a disabled master/reference render on its own track, plus markers for every known benchmark failure. The human editor should be able to compare the source-layer edit against the reference without leaving Resolve.
   - Name tracks by their actual enabled state. Disabled reference, repair, or prior-master tracks must say `DISABLED` in the track name so the user does not mistake them for active publish layers.
   - Add markers for story beats, jump-cut risks, B-roll needs, graphics, and HITL review steps.
   - Run `scripts/resolve_timeline_audit.py` after timeline creation. A Resolve timeline is not usable if clips were inserted before the visible timeline start frame, even when the API reports track counts.
   - After a hillclimb rebuild, verify timeline item source paths, not just clip names. Resolve media pools can contain same-named clips from older cuts; basename reuse can silently attach a stale v1 segment or source repair file to a new v2 timeline.
   - Prefer fresh/versioned bins or force-imported media for each build when source paths matter. Do not reuse a media pool item by name unless its `File Path` matches the intended artifact exactly.
   - If using PNG captions, verify they have alpha transparency. Full-frame black caption PNGs are a blocking bug.
   - If Resolve scripting is unavailable, provide FCPXML/EDL/CSV plus preview render and instructions.
   - Version project exports or outputs; never overwrite the user’s original `.drp`.

10. **Verification before final**
   - Run `scripts/verify_social_export.py <render.mp4> --out-dir <review-dir>`.
   - For captioned social exports, create a burned-in caption review with `scripts/caption_burnin_pipeline.py`. Do not claim captions are done from an SRT/PNG asset alone.
   - Run or record the four-lane benchmark before calling a social edit publishable: video editing craft, creative direction, visual multimodal, and audio multimodal. A strong visual score cannot override failing audio or cut-craft scores.
   - For YouTube/retention-oriented cuts, benchmark against creator videos by observable retention mechanics, not generic polish: first-5-second promise clarity, beat density, pattern-interrupt cadence, evidence B-roll, caption readability, phone mix, CTA placement, and whether each section earns the next minute.
   - Add an `audio desirability` lane to the benchmark with the highest weight for speaker-led educational content. Viewers may forgive imperfect picture, but weak dialogue, muddy EQ, unducked music, or lifeless sound design should block publishing.
   - If a benchmark render adds new hook/CTA graphics on top of an older master, inspect the CTA frame specifically. Baked captions plus a new lower-third can collide even when automated validators pass.
   - For FFmpeg renders with still-image overlays or looped music, hard-cap output duration with `-t` and/or `-shortest`; otherwise a looped logo/music bed can silently extend the render past the edit.
   - Inspect at least opening, first body beat, middle, CTA, and closing frames.
   - Treat multimodal evaluator timestamps as approximate, not authoritative. If Gemini or another critic flags framing, captions, ghosting, or missing speaker presence, extract stills at the cited timestamp and nearby frames before changing the edit. Document any validated false positive in the hillclimb notes.
   - On repeated hillclimbs, prefer replacing fragmented word-boundary cuts with fewer complete semantic blocks before adding more transitions. Smooth audio and coherent story are higher priority than maximal angle switching.
   - Keep attention graphics sparse. QR codes, logos, and event metadata belong in the CTA/details beats, not across the entire edit, and must not compete with the speaker or captions.
   - Avoid video crossfades on talking-head source clips unless the overlap is visually inspected at the transition. In vertical social crops, even short dissolves can read as ghosting/compositing errors; use hard picture cuts with audio crossfades, J-cuts, L-cuts, punch-ins, or B-roll instead.
   - Treat B-roll as intentional coverage, not decoration. For weak talking-head moments or jump-cut repair, use full-opacity cutaways or clearly designed picture-in-picture; do not use low-opacity B-roll overlays that create double-exposed faces, muddy captions, or unclear subject focus.
   - For speaker-led educational reels, do not replace the speaker with a static whiteboard, slide, or prop shot for more than a few seconds. If the user says the speaker is not “in the cuts,” rebuild around speaker-first A-roll and use board/prop content as quick inserts, picture-in-picture, captions, or text overlays.
   - A graphic overlay can pass text-readability QA and still fail the edit if it hides the speaker's face during an A-roll moment. For warm-traffic creator promos, full-screen or large proof cards are allowed only when intentionally functioning as B-roll/title-card coverage; otherwise keep the face/mouth visible and move graphics to side panels, upper corners, or short insert beats.
   - Avoid split-board treatments that duplicate the same board in multiple panels or expose upside-down/irrelevant board writing. If a whiteboard has mixed orientations, crop to the upright claim only or keep it as a brief insert.
   - Avoid duplicate titles from both baked video filters and ASS/top caption layers. Each beat should have one top label and one spoken caption lane at most.
   - When changing vertical crop scale or y-position, force `setsar=1`/square pixels before concatenation and inspect individual stills rather than only very wide contact sheets, which can be misleading in desktop preview.
   - Do not post-process punch-in crops after text/caption compositing unless every overlay lives inside the crop-safe center. Apply punch-ins before graphics/captions, or re-render captions after the motion pass. V10-style late crop passes can make the video feel more dynamic while cutting off title/callout text.
   - If a multimodal evaluator keeps calling the mix "dry" despite technical LUFS passing, treat the music/SFX as perceptually inaudible or too generic. Add an explicit music audibility check against dialogue-only sections, and inspect waveform/spectrogram deltas before claiming a scored audio-effects fix.
   - Do not let "visible effects" become generic flash bars or programmatic rectangles. If the benchmark asks for Mixkit/Fusion-style effects, the pass needs animated title templates, keyframed in/out motion, shadows/blur/separation, and Resolve-editable layers, not just baked FFmpeg drawboxes.
   - Caption placement must be checked against both the speaker's mouth/chin and the bottom social UI safe zone. Prefer short phrase captions with a dark plate and selective brand-color highlights; do not make captions so high that they compete with the face.
   - For near-final caption fixes, use the "caption-only finishing pass": extract dialogue from the approved cut, run word-level transcription, burn short spoken phrase captions, correct only high-confidence domain terms, inspect stills, and rerun social export verification. Do not change picture/audio unless the user asks.
   - Final response must mention:
     - output path,
     - duration/resolution/fps,
     - whether Resolve timeline was updated,
     - known limitations or any checks not performed.

11. **Capstone honesty**
   - Do not count a Loom upload, flat render, or seed timeline as a capstone.
   - A capstone needs an acceptance report with source folder, story plan, edit decisions, layered Resolve validation, export verification, homework/skill evidence when requested, and remaining gaps.
   - If the user asked for workbook homework, every lesson must have a coverage row and per-lesson evidence artifact. If Computer Use times out, mark it `ui_blocked`; do not imply manual UI completion.
   - If the editable Resolve timeline has empty caption/audio/music tracks while the render contains those features baked in, call that out as a handoff limitation.
   - A useful HITL handoff can include both publish timelines and layered repair timelines: publish timelines hold the exact verified master, while repair timelines hold original camera/audio cuts, processed segment spine, and a disabled master reference. Label this clearly so the user knows which timeline to export and which timeline to edit.

## Performance Guidance

Use a two-tier pipeline:

- **Fast analysis/planning:** ffprobe, scene thumbnails, transcript timestamps, rough EDL, low-res proxies.
- **Final render/review:** Resolve timeline, FFmpeg render, or FCPXML/EDL handoff after the plan passes.

For heavy automation or repeat projects, read `references/rust-video-stack.md`. Use Rust for the planner/orchestration layer, but keep FFmpeg/GStreamer/Resolve as the media engines.

## Useful Commands

```bash
python3 skills/davinci-resolve-social-editor/scripts/probe_media.py \
  /path/to/project --out /path/to/project/output/media_manifest.json
```

```bash
python3 skills/davinci-resolve-social-editor/scripts/verify_social_export.py \
  /path/to/render.mp4 --out-dir /path/to/project/output/review
```

```bash
python3 skills/davinci-resolve-social-editor/scripts/resolve_timeline_audit.py \
  --project "Project Name" --timeline "Timeline Name" --out /path/to/project/output/resolve_timeline_audit.json
```

```bash
python3 skills/davinci-resolve-social-editor/scripts/audio_quality_audit.py \
  /path/to/audio-or-project-folder --out /path/to/project/output/audio_quality_audit.json
```

```bash
python3 skills/davinci-resolve-social-editor/scripts/caption_burnin_pipeline.py \
  --srt /path/to/reviewed.srt --ass-out /path/to/netflix_captions.ass \
  --video /path/to/review.mp4 --out /path/to/review_burned_captions.mp4
```

## References

- `references/editing-qa.md`: quality gates for story, jump cuts, frame safety, captions, and audio.
- `references/resolve-automation.md`: Resolve scripting, bins, multicam, FCPXML/EDL, and timeline handoff.
- `references/rust-video-stack.md`: Rust/FFmpeg/GStreamer/OpenCV/Whisper architecture for performant video analysis and rough cuts.
- `references/acceptance-gate.json`: machine-readable gates for layered Resolve handoff, audio, captions, and creative QA.
- `references/reels-eval-benchmark.md`: four-lane Instagram Reels benchmark and failure-to-tool mapping.
