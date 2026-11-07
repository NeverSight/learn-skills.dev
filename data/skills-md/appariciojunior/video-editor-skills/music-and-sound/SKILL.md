---
name: music-and-sound
description: Scores a vlog with Epidemic Sound - one music cue per section edited to exact length, a ducking envelope baked into one bed (quiet under speech, up on B-roll), and tasteful transition sound instead of cheesy literal foley. Use for "add music", "background music", "sound effects", "SFX", or when the creator says the music or SFX feel wrong.
---

# Music and sound design

Only when asked. The creator doesn't want a list to choose from: **pick, place, and name two alternates per cue** in one line each so they can say "swap to the second one".

## Tools
Epidemic Sound as an MCP server: `SearchRecordings`, `EditRecording` + `PollEditRecordingJob` + `DownloadRecordingEdit`, `SearchSoundEffects`, `DownloadSoundEffect`. Downloads are signed URLs: fetch them with curl into `system/videos/<v>/music/src/` or `sfx/src/`.

## 1. Read the timeline as it is now
The creator has usually trimmed the cut. Read the B-roll windows from V1 of *their* timeline (times in seconds), and the speech around them.

## 2. Cues by section (moods)
Read the transcript and split it into 2–3 sections. A vlog that worked:
- **Opening / journey** (hopeful, dreamy ambient beats ~100 BPM), swelling on the travel B-roll;
- **The talk** (laid-back lo-fi ~73 BPM, sparse, nothing with a busy lead melody);
- **Ending** (warm, hopeful indie ~95 BPM) from "to close this video…" through the outro.

Search with filters `vocals: false` and a BPM range; avoid corporate stock sounds. Then ask Epidemic for an **edit at the exact section length** (`EditRecording`, `forceDuration: true`, WAV, `maxResults: 1`, max 300 s). **Check the edit's loudness over time**: one edit started fading 25 s before its end, killing the B-roll it was meant to lift. Fix: ask for a longer edit and cut it yourself with your own short fade.

## 3. One bed with a baked envelope (on A2)
Normalize each cue to the **full level**, place them with 2.5–3 s crossfades, then apply a gain envelope:
- **Full on B-roll** (and other speech-free moments): **-16 LUFS**. -19 was not enough; the creator asked for louder.
- **Under speech: -14 dB** below full (≈ -30 LUFS against a -16 LKFS voice).
- **Rise 1.2 s, starting ~0.9 s before the B-roll** (inside the speaker's tail room) so the music *flows into* the B-roll; fall 1.0 s ending as the next sentence starts.
- Write a plain **16-bit PCM WAV** with a **new file name per render** (`bed_v3.wav`) so Resolve never serves a cached old file. Verify levels per section after rendering (speech ≈ -30, B-roll ≈ -15 LUFS).

## 4. Sound effects: taste over literal
What failed: a zipper when the bag opens, cloth swooshes, a jet pass-by on the plane shot. The creator called it "the most cheesy and weird". Literal foley that mimics objects on screen feels cheap in a reflective vlog.
What works:
- **One soft swell into each B-roll**: an untuned reversed cymbal ("riser, no impact") that **peaks exactly on the cut**, ~10 dB under the music. Untuned so it never clashes with the music's key.
- **Quiet room tone** only where it sets the place (airport lounge, a city street), ~ -37 LUFS, long fades.
- The **B-roll's own natural sound** is real and usually better than library SFX.
- Find where the event happens inside each SFX file (loudness envelope) and align that point, not the file start.
- **Pre-mix each scene into one mono clip** (A3 can't hold overlapping clips), placed at the scene start.

## 5. Place and verify
Bed on **A2**, scene clips on **A3** (the creator's own timeline uses the same layout). Re-placing must never bring back clips the creator deleted: place "bed only" or "SFX only" when updating one of them.
Then make sure the bed is actually audible (render a few seconds and correlate, see `resolve-scripting`): a template's music track can be silenced by a track-level AI Music Remixer.

## Report
Each cue (section, title - artist, two alternates), the envelope numbers, each SFX scene and why, and that you couldn't listen: "this is a judgement from the files, tell me if it feels off".
