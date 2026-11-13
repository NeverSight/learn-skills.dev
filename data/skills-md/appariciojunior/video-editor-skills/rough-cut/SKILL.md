---
name: rough-cut
description: Editorial rules for choosing what to keep in talking-head footage (retakes, false starts, spoken notes to the editor, fillers) and the keep-list / moments formats that a planner script turns into frame-exact cuts. Use when deciding a cut, revising one from feedback, or writing keep.json.
---

# Rough cut: what stays

You decide **what** stays, by word index. A planner script decides **where** each cut lands (pads, waveform checks, pause shortening, frame snapping). Never do its job by hand.

The brief creators give: **remove retakes and silences, keep it feeling like a natural vlog.** Not a jump cut every second.

## Read first
The manifest, then every clip's word list in order. Each token: `{i, text, start, end, type}` with type `word` or `audio_event` ("(laughs)", "[lighter click]"). Read it as a story before deciding anything.

## Rules
1. **Retakes:** keep the best complete take, usually the last. Never keep a take that trails off. Cut the restart cue with it ("let me do that again", a swear at themselves).
2. **False starts:** cut an abandoned sentence plus its restart cue.
3. **Spoken notes to the editor** ("editor, roll the video here", "this slide is a video"): cut them and write each as a `note` moment → becomes a pink marker on the join where it was.
4. **Fillers stay.** It's a vlog. Only cut a filler that is clearly dead air on its own. Stumbles inside a word stay (cutting them makes a visible jump).
5. **Keep their voice:** asides, jokes, a laugh, a deliberate pause before a point.
6. **Pauses are not your job.** Give whole thoughts as one range; the planner shortens long pauses.
7. **Keep recorded order** unless asked.
8. **Unsure? Keep it and flag it.** A wrong cut is invisible to the creator; a flagged keep is a 5-second decision. Typical flags: near-identical lines in a row (deliberate repetition or retake?), self-corrections, a joke about "starting this three times".

## keep.json
```json
{
  "segments": [
    {"clip": "C0001", "from": 12, "to": 57, "why": "opening, second take"},
    {"clip": "C0002", "broll": true, "in": 0.0, "out": 4.0, "why": "camera goes into the bag"}
  ],
  "flags": [{"clip": "C0001", "at": 141, "note": "kept a stumble, check it"}],
  "summary": "3-6 lines in plain words"
}
```
`from`/`to` are inclusive word indices. B-roll segments are by seconds (see `broll`). Optional per range: `lead_in` / `tail` seconds of room (see `vlog-pacing`).

## moments.json
```json
{"moments": [
  {"type": "note", "clip": "C0001", "from": 1964, "to": 1994, "label": "VIDEO: product demo", "note": "Roll the demo here. They said: '…'"},
  {"type": "punch", "clip": "C0001", "from": 812, "to": 818, "label": "the line that lands"}
]}
```
- `note`: covers the cut words; the marker goes on the join.
- `punch`: a real punchline (conclusion, payoff, strong opinion), about one every 2–3 minutes. The picture pushes in to 115% **for that line only**, then goes back.

## After planning
Read the review file once: struck-through text must be only what you meant to cut. Report: raw vs cut length, pieces, every retake removed (timestamp + gloss), every note, every flag.

## Revisions
Creators speak in timeline times ("cut 02:14 to 02:20"). Map to word indices with the review file, edit the keep-list, re-plan, rebuild as a new version, and report only what changed.
