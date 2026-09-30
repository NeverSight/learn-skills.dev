---
name: premiere-sfx-design
description: Sound design and SFX mixing on a Premiere Pro timeline through the Premiere MCP. Covers timing every sound to what is actually visible in the render, picking sounds from the user's SFX libraries with an audition page they judge by ear, levelling against their own mix, placing clips without touching their edits, and measuring the result. Use this whenever the user asks to add, replace, re-time or mix sound effects, whooshes, UI clicks/pops, typing, notifications or risers in Premiere ("расставь звуки", "сделай саунд-дизайн", "озвучь появляшки", "звуки рано/громко", "подбери sfx из моей библиотеки"), even if they only mention one scene or one sound.
---

# Premiere SFX design

Claude can't hear. It can see frames, measure audio and move clips precisely. So split the work: Claude times and levels, the user chooses sounds by ear. The failure modes we hit before were exactly the parts Claude guessed:
- sound choice by file name ("strange", "not cozy");
- levels by absolute numbers (too loud next to the user's own mix);
- times from layer in-points and subtitles, which were 2–3 frames to 0.5 s early.

The workflow below replaces each guess with a measurement or with the user's ear.

## Tools (in `scripts/`, Python needs numpy + pillow, plus ffmpeg)

Run the scripts with `~/.ae-bridge/venv/bin/python`. If that venv doesn't exist, create it with the user's OK: `python3 -m venv ~/.ae-bridge/venv && ~/.ae-bridge/venv/bin/pip install numpy pillow`.

| Script | Use |
|---|---|
| `timeline_summary.py` | Summarise a saved `get_full_sequence_info` result (it's too large to read inline): clips per track, time filter. |
| `contact_sheet.py` | Labelled frame grid of the render around an event. Look at it to find the frame something becomes visible. |
| `burst_times.py` | Detect the frames where banners/cards/chips appear in a region (bright-pixel growth or frame diff). |
| `sfx_analyze.py` | Onset, peak time, audible end, safe cut point, brightness, L100 level of sound files. |
| `audition_pick.py` | Shortlist varied candidates per slot from library globs (+ files the user already likes). |
| `build_audition.py` | Audition page: per slot, the same picture/VO/music clip with each candidate at the real event times. |
| `plan_hits.py` | Many repeated hits: frame-rounded starts, random non-repeating variant order, gain jitter, lane assignment. |
| `loudness_check.py` | Integrated loudness, true peak, and where the overs are, from a WAV export. |

Read `references/premiere_mcp_quirks.md` before the first MCP call of a session, and `references/timing_and_levels.md` when choosing times or levels.

## Workflow

1. **Snapshot the timeline** (`get_full_sequence_info` → saved file → `timeline_summary.py`). Anything you did not place is the user's. Don't move, trim, re-level or delete it, even if it looks wrong; ask. Re-snapshot before every batch of changes: the user edits in parallel, and your earlier clips may already be gone or moved.
2. **Find which video is the picture.** Usually the newest render on the top video track. Note its offset on the timeline. Time sounds to that file, not to the AE project or subtitles.
3. **List events and get their visual times.**
   - Use `contact_sheet.py` over each moment (6–8 columns, every frame near the event). Record the first frame where the element is clearly visible, or the motion peak for fly-bys and transitions.
   - For bursts of similar elements (notifications, list items) use `burst_times.py`, then confirm on a sheet.
   - Skip micro-events. Not every hover or toast needs a sound, and fewer good sounds beat many.
4. **Calibrate levels on the user's own SFX.**
   - Read `get_clip_volume` of clips they placed or kept, and measure the files with `sfx_analyze.py`: L100 + clip gain = the level they like.
   - Derive per-category targets from that (see references).
   - Measure the VO/music clip gains too; they are the bed.
5. **Pick sounds by ear.**
   - If the user names files, use exactly those.
   - Otherwise shortlist 5–6 candidates per slot with `audition_pick.py`. Botanica-style libraries: prefer the "main" library the user names and fill gaps from others.
   - Build the page with `build_audition.py` and serve it: `python3 -m http.server <port> --directory <out_dir>`, e.g. via a launch.json preview server.
   - Open it for them and read their picks from the page (`localStorage.sfx_pick`). Every slot has a "no sound" option and a quieter/louder switch.
6. **Place.**
   - Copy chosen files into the project folder with clean ASCII names; library paths with emoji break imports.
   - Import them into a bin of your own, and cut subclips to trim long silent heads and tails (`sfx_analyze` `tail40`).
   - Put each clip on the timeline with `overwrite_clip`, never insert. `plan_hits.py` spreads repeated hits over empty tracks so no clip truncates another.
   - Set the volume of each new clip, then re-read the tracks to confirm every clip landed where planned.
7. **Measure.**
   - Export the sequence as WAV ("Waveform Audio" preset, seconds) and run `loudness_check.py`.
   - Overs from your SFX: lower them or trim the spike with volume keyframes.
   - Overs from VO + music: MCP can't add a master effect. Tell the user to put Hard Limiter on the Mix track (−1 dB ceiling), and by how much to raise Input Boost to reach their loudness target.
8. **Save the project and report**:
   - what sits where (track + time range);
   - levels relative to their own SFX;
   - what you left for them.

## Things the user will care about

- **Timing:** hits land on the first visible frame, whooshes peak on the motion peak, typing runs only while letters appear.
- **Variety:** repeated events rotate 2–4 variants in random order, no identical neighbours, ±0.8 dB jitter.
- **Their edits are sacred:** "мои правки не трогай". Place new sounds only on empty track ranges.
- **Ask before a big redo.** When feedback is vague ("вышло плохо"), ask what is wrong (choice / loudness / timing / density) in one multiple-choice question, then fix exactly that.
