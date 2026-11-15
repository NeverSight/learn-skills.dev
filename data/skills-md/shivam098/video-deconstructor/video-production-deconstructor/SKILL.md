---
name: video-production-deconstructor
description: Reverse-engineer how a YouTube or local video was made - editing pace, narration-to-picture sync, visual design system, motion/animation technique, transitions and sound design - and produce a recreation blueprint. Use when asked to analyze a video's production style, how an animation or transition was built, why a video's pacing works, or how to make a video "like this one" (e.g. Vox, Bloomberg, Kurzgesagt, 3Blue1Brown, 3D shorts, documentaries).
---

# Video production deconstructor

Models cannot watch a video file. This skill uses the `video-deconstructor` tools to turn a video into artifacts you *can* read, then walks through them in three passes.

## Tools

Prefer the MCP tools. If they are unavailable, run the CLI from the repository root (`node bin/cli.mjs ...`; add `--json` for machine-readable output).

| MCP tool | CLI | Use |
| --- | --- | --- |
| `check_environment` | `doctor` | Verify yt-dlp / ffmpeg / ffprobe before anything else if a call fails. |
| `deconstruct_video_overview` | `overview <src>` | Passes 1-2. Run once per video (optionally `start`/`end` to analyze one section of a long video). |
| `inspect_motion_or_transition` | `zoom <src> --start --end --fps` | Pass 3. 2-10 s windows at 6-12 fps. |
| `extract_highres_style_frames` | `frames <src> --timestamps` | Full-resolution stills for design detail. |
| `transcribe_audio` | `transcribe <src>` | Optional. Local Whisper speech-to-text when a video has no captions (needs `setup_whisper` once). |
| `gemini_analyze_video` | `gemini <src>` | Optional, needs the user's `GEMINI_API_KEY`. Gemini watches the video (motion + audio) and writes its own analysis. |

Downloads are cached, so follow-up `zoom`/`frames` calls on the same URL are fast.

### Optional add-ons

- **No captions?** The overview's `summary.narrationNote` says so. If `check_environment` shows Whisper is ready, the overview has already transcribed the audio. Otherwise, offer to run `setup_whisper` (a one-time download of about 142 MB), then re-run the overview or call `transcribe_audio`.
- **Gemini** is a second opinion, not a replacement. Use it only if the user asks or agrees, because it sends the video to Google (on the free tier, Google may use it to improve its products). Its observations are not measurements: prefer the measured cut times and pacing from the overview, and use Gemini for things frames can't show well, such as continuous motion, lip sync and how sound effects land. Point it at specific windows with `start`/`end`/`fps` for detailed questions.

## What the overview produces

All paths are returned in the tool result (`artifacts.*`).

- `av-timeline.md` - one row per shot: how it starts (`hard` cut / `soft` transition), start time, length, the narration spoken during it, silences, and a link to its style frame.
- `pacing-metrics.json` - shot list, average/median shot length, cuts per minute, shot-length distribution, pacing per chapter or time segment, silences, `narrationSync` (share of cuts landing near a caption start) and `visualActivity` (per-second on-screen motion with `motionHotspots`).
- `contact-sheets/sheet_NNN.jpg` - 4x4 storyboard grids, every tile stamped with its timestamp. Read left-to-right, top-to-bottom.
- `style-frames/style_NN_<time>.jpg` - native-resolution frame from the middle of representative shots.
- `audio-strip.png` - waveform (top) and spectrogram (bottom) on one time axis; red lines = hard cuts, orange = soft transitions, yellow bands = silence.
- `manifest.json` - everything above plus video metadata (title, channel, chapters, description, tags) and suggested Pass 3 windows.

## Procedure

### Pass 1 - structure, pacing and sound

1. Run the overview. Read `manifest.json` summary, then `av-timeline.md` and `pacing-metrics.json`.
2. View `audio-strip.png`. Note where cut density changes, where silences or music drops sit relative to cuts, and whether cuts cluster on narration beats (`narrationSync`).
3. View every contact sheet in order. Classify each stretch of the video by visual mode, e.g. talking head / A-roll, archival footage, documents and clippings, 2D vector animation, 2.5D parallax collage, maps, charts / data viz, kinetic typography, screen recordings, 3D renders, live-action B-roll.
4. Map the narrative: hook (first 15-30 s), setup, sections or chapters, turns, payoff, outro. Tie each beat to timestamps.

### Pass 2 - visual design system

View the style frames (and pull extra ones with `extract_highres_style_frames` for anything important). Describe:

- Layer stack from back to front: background / canvas, mid-ground assets, foreground graphics, overlays (grain, vignette, halftone, paper texture, light leaks).
- Colour roles: base, text, de-emphasised context, accent / highlight. Give approximate colours; say "approximately" because frames are compressed.
- Typography: classes (serif / grotesque sans / condensed / mono), hierarchy, how labels attach to things.
- Graphic language: highlights, arrows, callouts, framing devices, how charts reveal data, how maps are styled.
- For 3D: materials, lighting setup (key / fill / rim), depth of field, camera lens feel, render style.

### Pass 3 - motion and transitions

Pick 2-4 windows: `motionHotspots` from the manifest, soft transitions from the timeline, and any moment that looks distinctive on the contact sheets. Call `inspect_motion_or_transition` with `fps` 8-12 over 2-6 s. In the result:

- Tile-to-tile displacement shows easing: big early jumps that shrink = ease-out; slow-fast-slow = ease-in-out; overshoot then settle = spring; identical tiles in pairs = animation on twos / posterized time.
- Different layers moving at different speeds = 2.5D parallax or a 3D camera; perspective change on objects = true 3D.
- `motionCurve` in `zoom.json`: isolated spikes = cuts or flashes; sustained plateaus = continuous motion.
- Check the window's `audio-strip.png` for whooshes, hits or risers that land on the transition.

## Report format

1. **Summary** - style archetype, runtime analyzed, shots, cuts/min, average and median shot length, dominant visual modes and their rough share, likely toolchain.
2. **Structure** - table of beats: time range | narration purpose | visual approach | sound.
3. **Design system** - layer stack, colour roles, typography, graphic devices, with style-frame references.
4. **Signature techniques** - 3-6 techniques, each with timestamps, what happens frame by frame, and how it is likely built.
5. **Recreation recipe** - concrete steps in a named tool (After Effects, Blender, DaVinci Resolve, Premiere, Manim, Motion Canvas, Remotion...), including layer setup, keyframe timing, easing, effects and sound cues.

## Rules

- Separate **measured** facts (cut times, shot lengths, silences, timestamps visible on tiles) from **inferred** claims (software used, technique names, intent). Label inferences as such; tools and plugins can rarely be identified with certainty.
- Cite timestamps for every claim about the video.
- Scene detection is a heuristic. Very fast motion can register as a soft transition, and slow dissolves can be missed. Confirm important cuts on the contact sheets or with a zoom before relying on them.
- If there are no captions and no Whisper transcript, say the narration analysis is unavailable rather than guessing what is said.
- Respect copyright and the platform's terms: analyze for learning and critique, and do not redistribute downloaded media.
