---
name: resolve-scripting
description: Practical DaVinci Resolve Studio scripting knowledge for building edits from code - timelines from a template, frame-exact appends, zoom, grades, custom frame sizes, subtitles, renders, and the traps that silently fail or crash Resolve 21. Use when writing or debugging any script that talks to Resolve.
---

# Resolve scripting: what actually works (Resolve Studio 21)

Check the API for the installed version before trusting memory: the scripting docs ship with Resolve, and functions move (some changed between 20 and 21).

## Golden rules
- **Only add.** New timelines (never overwrite: "name v2"), imports into bins, clips on free tracks. Never touch the creator's template or their timelines/media. Never switch/create/close projects.
- **Verify every write by reading it back.** Many setters return True and do nothing.
- Save the project at the end of each step.

## Building the timeline
- Find bins by name recursively. Import files once (reuse the media pool item if the same path is already imported).
- **Copy the template** with `DuplicateTimeline(name)`, move it into the timelines bin, then empty every track (unlock locked tracks temporarily). The copy keeps the track FX chain (voice treatment on A1, music treatment on A2) - that's why we copy instead of creating.
- **Frame rate mismatch** footage vs template: stop and ask. If they choose the footage rate: `useCustomSettings=1`, `timelineFrameRate`, `timelinePlaybackFrameRate`.
- **Custom frame (e.g. 4:3 2880x2160):** set `timelineResolutionWidth/Height` and the output resolution, then input mismatch behaviour **`scaleToCrop`** ("scale full frame with crop"). The default `scaleToFit` letterboxes. Read it back.
- **`AppendToTimeline`**: `endFrame` is **exclusive**. For audio-only media, start/end frames count in the *clip's own* frame rate (a WAV reports 23.976), not the timeline's.
- **Audio duration from timecode:** at 23.976, a timecode counts **24** frames per second. `seconds = ((h*3600+m*60+s)*round(fps) + f) / fps`. Using 23.976 per second lost 16 frames on an 11-minute music bed.
- Check after laying: piece count on V1 and A1, each duration, no gaps.

## Picture
- **Zoom:** `item.SetProperty("ZoomX", z)` and `"ZoomY"` (centre anchored). Works in 21.
- **Grades:** `Timeline.ApplyGradeFromDRX` **fails in 21**. Use each item's graph: `item.GetNodeGraph().ApplyGradeFromDRX(path, 0)`. It occasionally fails on one piece and works on a retry: try twice, then count graded pieces (node count) and report.
- Never put a log look on non-log footage. Read the profile from the camera's sidecar XML, not from luma guesses.
- `SetClipColor("Green")` on B-roll pieces.

## Audio
- **Normalize:** `Timeline.NormalizeAudioLevel(items, {normalizationMode, targetLevel, targetLoudness, setLevelMode})` with `resolve.NORMALIZE_AUDIO_SET_LEVEL_INDEPENDENT`. See `voice-and-audio` for values.
- Per clip: `AudioVolume` (dB), `SetVoiceIsolationState({"isEnabled": True, "amount": 50})`, Dialogue Leveler properties. **EQ is not scriptable**; Fairlight presets can be applied if the user saved some.
- **Silent track trap:** a template's music track had a track-level **AI Music Remixer** switched on (and a Stereo Width insert). Anything placed on that track rendered as silence while the same file played on another track. The API can't read or toggle it; it's in the Edit page → select the track header → Inspector → Audio. If music is silent, check that first.

## Diagnosing audio the reliable way
When "there's no sound", don't guess. Render a few seconds of audio from Resolve and compare it with the source file:
- Project render: `SetCurrentRenderFormatAndCodec("mov", "ProRes422LT")`, `SetRenderSettings({SelectAllFrames: False, MarkIn, MarkOut, TargetDir, CustomName, ExportVideo: False, ExportAudio: True, AudioCodec: "lpcm"})`, `AddRenderJob()`.
- **From an external script, rendering only starts with `StartRendering([job], False)`** (isInteractiveMode False). Other forms return False and the job stays "Ready".
- Render into a folder **without spaces** (a path with spaces left the job unstarted).
- Wait on `GetRenderJobStatus(job)` until "Complete", not on `IsRenderingInProgress()` (it can be False before rendering begins).
- Correlate the rendered audio with the source (mono, 8 kHz, best lag): ~0.9 = present, ~0.0 = missing. Least-squares gain tells how much of an SFX is in the mix.
- **Restore the Deliver settings afterwards** (format, whole timeline, video+audio on, output folder): your test changes the creator's export settings.
- `AddRenderJob` jumps to the Deliver page; `SetTrackEnable` only works on the Edit page (on other pages it returns True and does nothing). Go back with `OpenPage("edit")`.
- Timeline export (`Timeline.Export(path, EXPORT_DRT)`) is a zip of XML with per-track fields; deeper mixer state is a compressed binary. Useful for diffing a working vs broken track.

## Subtitles
- `MediaPool.AppendToTimeline` with an imported .srt **ignores recordFrame and appends the subtitles after the end of the timeline**. Passing start/end frames for it **crashed Resolve 21.1**.
- Use **File > Import > Subtitle** in the UI (the creator clicks it, or computer-use). It places the first cue at the playhead and shifts the rest relative to it, so **make the SRT's first cue start at 00:00:00,000**, or everything lands early.
- Subtitle track style can't be set by script; read it from a DRT export if you need to record it.

## Overlays and media cache
- Re-rendered files with the **same name** can keep playing stale cached frames: give each new render a new name (`-v2`) and replace the clip.
- Place overlays on the first free unlocked track from V2 up; never on V1.

## Reading the timeline the creator edited
Before music, captions or graphics, map the timeline as it is now: walk V1 items (name, start, left offset) to find where each kept word and each B-roll landed. They trim and delete things; follow their version.
