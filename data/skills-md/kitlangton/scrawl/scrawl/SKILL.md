---
name: scrawl
description: Read and dig into Scrawl screen captures, where someone recorded their screen while talking, clicking and drawing red marks on it. Use whenever a message contains a Scrawl capture (a line like `[scrawl 0:12 · App “Window” · /path/to/….scrawl]`, a `.scrawl` bundle path, or a contact-sheet.png from one), when the user says "look at my scrawl" or refers to something they just recorded or drew, or when you need the `scrawl` CLI to zoom into a moment, pull frames, send a capture to a session, or export one as video.
---

# Scrawl captures

Scrawl records someone's screen, voice, clicks and red ink, then packs the result into a `.scrawl` folder (a bundle). They send it to show you a problem instead of describing it, so the capture is the bug report. Read it closely before you answer, and don't ask them to explain again what the capture already shows. If something is unclear, look closer with `scrawl zoom` first.

## What a paste looks like

```text
[scrawl 0:33 · OpenCode “Settings” · /Users/me/Library/Application Support/scrawl/captures/scrawl-1792432139176.scrawl]
Cropped to: the activity in OpenCode (full frames in frames-full/)
- #1 (0:04) [clicked “New tab”] “Command T makes a new session, but here it should make a tab.”
- #2 (0:07) “No, it doesn't.”
- #3 (0:10) ⚑ “It says command shift B makes a new tab.”
- #4 (0:18) clicked (x 0.51, y 0.93)
```

- The first line has the length, the app and window recorded, and the bundle path.
- Each `#N (M:SS)` line is a keyframe: what they did at that moment in brackets, then what they said while it was on screen. A line with no quote has the action alone.
- `⚑` means they flagged the moment on purpose. `⟨Name⟩` means the app reported a new screen. Lines starting `·` are events or values the app logged.
- Optional lines near the top: `For session:` (where Scrawl sent it), `Screen:` with app context, `Note:`, and `Cropped to:`.
- Coordinates are fractions of the captured area, from the top left (x 0.51 is just right of centre).

When you answer, refer to moments the same way, as in "#3 (0:10)", so the person can find them on the contact sheet.

## Reading a bundle

1. Look at `contact-sheet.png` in the bundle first (it's often attached already). It shows every keyframe in time order, left to right and top to bottom, each with a `#N M:SS` badge.
2. Read the transcript lines next to it. Speech recognition mishears names and code terms, so trust the screen when the two disagree.
3. Open `frames/frame-NN.png` for any keyframe you need at full size (`frame-03.png` is #3). When the summary says `Cropped to:`, the uncropped screens are in `frames-full/`.

What the drawings mean:

- Red strokes, circles, underlines and arrows are the person's marks, and they point at the problem. Marks drawn on the same screen all show on one keyframe.
- A ripple around the cursor shows a click or tap, and a finger trail shows a swipe.
- A glowing red trail that tapers off is the laser pointer, used to point without leaving a mark.

Other files: `scrawl.json` is the full manifest (keyframes, `marks` with shape and box, `events`, `transcript.words` with times, app `context`, and `autocrop`). `recording.mp4` or `recording.mov` and `audio.wav` are the source media. A `.media-pending` file means the video is still being copied from another Mac.

## The scrawl CLI

`scrawl` is the Scrawl app's own binary. If `command -v scrawl` finds nothing, use `/Applications/Scrawl.app/Contents/MacOS/scrawl` (or the same path under `~/Applications`), and tell the person they can put it on PATH with Install in Scrawl's Settings › Agents. It runs only on the Mac with Scrawl installed. Anywhere else, read `contact-sheet.png`, `frames/` and `scrawl.json` directly. Every command takes a bundle path, and most default to `latest`, the newest capture. Quote the path, because it usually contains `Application Support`.

### Look closer at a moment

Use `zoom` when the problem is motion (an animation, a jump, a flicker) or happens between keyframes, or when you can't tell what a mark points at:

```sh
scrawl zoom <bundle> --at 0:21                 # a time, M:SS or seconds
scrawl zoom <bundle> --at "the width changes"  # or a phrase they said
scrawl zoom <bundle> --at 0:21 --span 1 --frames 16 --full
```

It prints the path of a PNG sheet of frames around that moment, the time of each cell, and what was said. Open the PNG and look at it before you act on the feedback. `--span` is the seconds covered (default 2, a quarter of it before the moment), `--frames` the number of cells (default 12), and `--full` shows the whole screen instead of the crop. The cells are numbered from #1 within the sheet, so those numbers aren't keyframe numbers.

### Other commands

```sh
scrawl inspect <bundle>               # summary.md, the text above
scrawl inspect <bundle> --json        # scrawl.json
scrawl frames <bundle> --from 0:04 --to 0:06 [--fps 4]   # plain PNGs of a range; prints their paths
scrawl send <bundle> --session ses_…  # queue the capture into an OpenCode session
scrawl send <bundle> --clipboard      # copy the summary text to the clipboard
scrawl export <bundle> [--out demo.mp4] [--zoom] [--crop auto|full|x,y,w,h] [--size 1920]
```

- `zoom` and `frames` write into `<bundle>/zoom/`. Leave the rest of the bundle as it is, because Scrawl manages those files and cleans them up.
- `send` without `--session` goes to the session the capture was addressed to (the `For session:` line), and otherwise to the most recently active session. With a recorded destination it refuses a different `--session` unless you pass `--reroute`, so check with the person before rerouting.
- `export` writes one `.mp4` with the ink and clicks burned in and the audio in sync (default `~/Movies/Scrawl/<bundle>.mp4`). `--zoom` eases in toward the activity. `--no-ink`, `--no-clicks`, `--hevc` and `--fps` are also available.
- Video and audio go to the Trash 7 days after a capture unless the person changed that in Settings. After that `zoom`, `frames` and `export` can't read the video, but `frames/`, the contact sheet and `scrawl.json` remain.
- `scrawl <command> --help` lists every flag, and `scrawl skill` prints this guide as the installed version knows it.
