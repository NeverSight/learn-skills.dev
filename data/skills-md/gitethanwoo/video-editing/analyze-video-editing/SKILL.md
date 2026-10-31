---
name: analyze-video-editing
description: Reverse-engineer an existing video into a timecoded account of its shots, cuts, fades, camera motion, dialogue, subtitles, titles, music, sound transitions, pacing, and editorial structure. Use when the user shares a reference video or local media and asks how it works, why it feels effective, what can be learned from it, how B-roll and interviews are interwoven, or how to translate its grammar into an original edit. Produces machine evidence, visual review artifacts, and an editorial breakdown without confusing estimates with observed facts.
---

# Analyze Video Editing

Study how a finished video creates attention, emotion, and momentum. Treat the film as synchronized picture, sound, speech, typography, and structure—not merely a list of cuts.

Set `SKILL_DIR` to the absolute directory containing this file. Use the adjacent `video-editing` skill when the user wants the resulting ideas implemented in an edit.

## Start with a source you can inspect

For a local file:

```bash
uv run "$SKILL_DIR/scripts/video_analyzer.py" analyze \
  /path/to/video.mp4 \
  --work-dir /path/to/analysis \
  --subtitles /path/to/captions.vtt
```

For a public URL, inspect the downloader's real metadata payload before choosing formats. Do not guess fields or stream availability:

```bash
uvx --from yt-dlp yt-dlp --dump-single-json --no-playlist URL > source.json
uvx --from yt-dlp yt-dlp --no-playlist \
  -f 'bv*[height<=1080]+ba/b[height<=1080]' \
  --merge-output-format mp4 -o 'source.%(ext)s' URL
```

Download captions when available. If download rights or site access are unclear, ask the user for a local copy.

Analyze a representative range first when the film is long:

```bash
uv run "$SKILL_DIR/scripts/video_analyzer.py" analyze source.mp4 \
  --work-dir analysis-first-three-minutes --start 0 --end 180 \
  --subtitles source.en.vtt --ocr
```

The script writes:

- `analysis.json`: probe facts, shot boundaries, black and quiet intervals, audio levels, beat estimates, transcript cues, motion estimates, and OCR candidates;
- `timeline.md`: a compact evidence table;
- `contact-sheet.jpg`: visual rhythm across the requested range;
- `frames/`: representative shot frames;
- `strips/`: dense frames around major cuts, black intervals, and other events.

Scene detection, optical flow, beat tracking, and OCR are candidate generators. They reduce scrubbing; they do not replace watching and editorial judgment.

When sound design, music continuity, or effects matter, pair semantic listening with signal evidence:

```bash
python3 "$SKILL_DIR/scripts/audio_listener.py" \
  source.mp4 \
  --work-dir analysis/audio-movement \
  --start 60 --end 172 --mode movement
```

This optional command extracts direct audio, renders a spectrogram, measures half-second loudness windows, and—unless `--prepare-only` is supplied—asks Gemini for an editorial sound breakdown. It reads `GEMINI_API_KEY` from the environment and never accepts credentials as command-line arguments. Use `--mode transition` for a focused high-sensitivity pass around a cut, dropout, black interval, or suspected fade.

Read [references/audio-and-timing.md](references/audio-and-timing.md) before accepting a model's classification of quiet material.

## Build the breakdown in three layers

Keep these labels explicit:

1. **Measured:** timestamps, shot duration, hard-cut score, black frames, silence, audio level, detected beat, transcript words, OCR boxes.
2. **Observed:** composition, subject, camera behavior, lighting, lens feel, text treatment, performance, apparent B-roll or interview mode.
3. **Interpreted:** tension, release, emphasis, contrast, narrative function, or why a juxtaposition works.

Never present a motion classifier or music estimate as certainty. Say “appears handheld” or “likely music re-entry” when it is an inference.

## Analyze the synchronized layers

For every important beat, ask:

- **Picture:** What is shown? What changes at the cut? Is the framing wide, medium, close, insert, or abstract?
- **Camera:** Static, locked-off, handheld, stabilized walk, pan, tilt, push-in, pull-out, rack focus, or subject motion inside a fixed frame?
- **Edit:** Hard cut, match cut, jump cut, dip to black, fade, dissolve, speed change, montage, or an unusually long hold?
- **Speech:** What line lands here? Is the next image literal illustration, contrast, reaction, or tonal counterpoint?
- **Sound:** Dialogue, room tone, ambience, effects, score, pulse, silence. What enters, exits, or changes level before or after the visual edit?
- **Typography:** Subtitle, chapter title, credit, label, or graphic motif? Record position, size, color, case, duration, entrance, and whether it obscures or complements the image.
- **Function:** Hook, escalation, orientation, reset, thesis, proof, character introduction, montage, transition, or payoff?

Read [references/editorial-analysis.md](references/editorial-analysis.md) for the reporting vocabulary and [references/audio-and-timing.md](references/audio-and-timing.md) for sound-driven analysis.

## Report at two scales

Create both:

- a **micro timeline** for the most instructive section, often every meaningful change over the first 60–180 seconds;
- a **macro grammar** for the whole film: recurring shot families, average shot length, interview/B-roll pattern, graphic system, music arcs, chapter resets, and escalation strategy.

A useful synthetic row looks like:

```text
01:03.875–01:06.167 | hard cut | handheld exterior insert |
score re-enters and beat becomes explicit | large chapter title fills frame |
turns a reflective line into a formal chapter launch
```

Avoid false precision in prose. Use frame-accurate numbers in the evidence table, then readable `mm:ss` timestamps in the explanation.

## Turn analysis into reusable learning

Extract principles, not imitations. For each device, state:

- the viewer problem it solves;
- the preconditions that make it work;
- the cost or risk;
- one way to adapt it to a different subject.

Example: “A four-second dip to black works here because the opening movement has accumulated tension and the continuing environmental sound prevents the reset from feeling like the video ended.”

If the user wants to apply the result, hand the evidence and selected principles to the `find-broll` skill for cutaway sourcing and then to `video-editing` for production. Do not encode the reference film's exact timings, fonts, or transitions as defaults.

## Quality bar

- Inspect representative frames and event strips yourself.
- Verify the transcript against picture when wording drives the edit.
- Check false cuts caused by flashes, large titles, or camera whip.
- Distinguish source subtitles from platform captions.
- Describe sound only to the resolution supported by the evidence.
- Prefer long-context semantic listening to establish cue identity, then focused passes around transitions.
- Verify alleged silence, ambience, music endings, and fades against the spectrogram and loudness trace.
- Cite the public source when the report refers to it.
- Do not redistribute the downloaded reference media.
