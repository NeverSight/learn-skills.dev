---
name: remotion-qa
description: Measure a rendered video (Remotion or any mp4) for sound-off readability before it ships - dead air after the viewer has finished reading, beats too short to read, and text hidden under the Reels/Shorts/TikTok UI - and check type sizes against mobile floors. Use after every render or re-cut of a reel, short, ad or social video, and before handing a video to anyone.
---

# remotion-qa

Measure the **rendered file**, never the composition source. A source can't tell
you whether a line wrapped, whether a card overflowed into the platform UI, or
how long a frame actually sat frozen. A readability check that compares a
duration with the value it was computed from can never fail, so it is not a check.

## 1. Pacing, in both directions

```bash
npx remotion-qa pace out/video.mp4 --beats captions.srt
```

`--beats` takes `.srt`, `.vtt`, or JSON (`[{ "start": 0, "end": 2.5, "text": "line one\nline two" }]`,
or `{ "from", "to" }` in frames with `fps`). If the project has no captions file,
write a beats file from the composition's own text and timings.

Read the output correctly:

- **A static run is not automatically dead air.** A frozen frame while the
  viewer is still reading is reading time. Dead air is only the part after
  they've finished. The tool does this subtraction for you when given beats:
  `required = longest_line_chars / 15 + 0.4s per extra line + 1s`, counted from
  when the beat arrives.
- **TOO FAST** beats are the opposite failure: the text leaves before it can
  be read sound-off. Both count.
- **Footage with a slow push registers as still** (a few % zoom over a beat is
  under a pixel per frame). Only judge runs that sit on a flat graphic ground.
- **The tail of an eased entrance reads as still** (an ease-out is ~94% done
  at half its duration). A run starting mid-entrance is part entrance, part hold.

**Fix over-holds by pacing, not trimming.** Shortening the beat trades dead air
for "too fast". Stagger the reveal so a list builds at reading pace (items
~20 frames apart, not 4), then hold only for the last item to settle.

## 2. Safe zones

```bash
npx remotion-qa safezone out/video.mp4 --frames qa-frames/
```

Reports how far ink reaches into each platform overlay (the caption, buttons,
progress bar), in canvas px. Open the saved frames: text in a shaded zone is a
defect, decoration there is fine. Bands holding footage aren't judged; say so
rather than calling them clear.

Channels: `reels-union` (default for 9:16, the worst case of IG Reels, FB Reels
and YT Shorts), `ig-reels`, `fb-reels`, `yt-shorts`, `yt-landscape`,
`feed-square`, `feed-portrait`.

## 3. Type sizes

```bash
npx remotion-qa floors --channel reels-union --font-factor 1.08
```

Floors are calibrated to a 360pt-wide Android (on-device pt = canvas px / 3 on a
1080 canvas). They are **floors, not targets**: size each element as large as
its layout allows. Lighter faces need a `--font-factor` (1.08 for Manrope
600/700). In a composition, `assertLegible(px, role)` throws below the floor.

Bigger type changes line counts, and line counts change reading time, so
**re-run pacing after any size change**.

## 4. Gate renders

```bash
npx remotion-qa render MyComp out/video.mp4 --max 5
```

Renders, then fails if any static run exceeds `--max` seconds, moving the file
to `out/video.failed-pace.mp4` so nothing sits at the path people send from.

## Report

Per file: each static run with the text on screen, its required seconds and the
dead air; each too-fast beat; each safe-zone intrusion with depth and the frame;
any type under its floor. Recommend a fix per finding, preferring a stagger to a
trim. Never change copy or timing as part of a sizing fix, or sizes as part of a
pacing fix: report what the other pass should pick up.
