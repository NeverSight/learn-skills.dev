---
name: papercut-storyboard
description: Storyboard a papercut script before any code. Writes the Camera / Cut table, one block per scene with frame-level events on each stressed word, the SFX plan and the proof beat. Use for "storyboard this script" or "plan the camera moves and cuts".
---

# Papercut storyboard

The storyboard is the plan every scene is built from. It names the camera move and the cut for every scene, so the scene agent doesn't invent them. A brief that says "CameraPush or your own transform" gets a flat push or a hand-rolled zoom in every scene, and the kit's camera moves go unused.

## Preflight

- Install: Minimal is enough. With a library, check `library/papercut/CATALOG.md` (sections "paper/camera.tsx" and "paper/transitions.tsx") for each move's props and when it fits. If the file is missing or stale, run `python3 $PAPERCUT_LIB/tools/catalog.py`. Resolve `$PAPERCUT_LIB` from the environment, else the `PAPERCUT_LIB=` line in `~/.config/papercut-explainer/config.env`, else ask once.
- Needs `narration/script.json` and `papercut/STORYBOARD.md` with the HOOK block and the staging table (banner, set, prop, UI moment, mascot, gag per row). Missing: run `papercut-hook` and `papercut-script`.
- Backdrop sheet for choosing sets: `library/papercut/public/bg/backdrops/_sheet.jpg`. Open only what the step needs.

## 1. Global rules

Put these at the top of `STORYBOARD.md`, under the HOOK block. Palette by role (rotate background colours per set): `../papercut-explainer/references/style-guide.md` section 5. Fonts: section 6. Canvas and zones: section 4. A feature-unlock that suits one extended metaphor can use section 12.
- 1080x1920, 30 fps. Banner at 14-21% height, caption band 68-80% (it shifts per scene to stay off faces), bottom 20% clear.
- Light from the top-left. Saturation only on characters, captions and signals.

## 2. Camera / Cut table

One row per scene, before the scene blocks. Every row names a component from the kit's `paper/camera.tsx` and the `CutSeries` kind (from `paper/transitions.tsx`) for the cut into that scene.

| Scene | Camera (`paper/camera.tsx`) | Cut in (`CutSeries` kind) |
|---|---|---|
| S01Hook | `OrbitCamera` + `Depth`, `SnapZoom` on "<word>" | none |
| S04Name | `Crane` rise to <focal prop> | `tearAway` |
| S09Peak | `CrabTrack` along <lineup> | `whip` |
| S10CTA | `RackFocus` <prop> to phone | `tapePull` |

- Camera options: `OrbitCamera` + `Depth`, `SnapZoom`, `Crane`, `CrabTrack`, `DollyZoom`, `RackFocus`, `ForegroundPass`, `DutchTilt`, `FocusPulse`, `FreezeFrame`, `PullBack`, `PovMask`, `TimeRamp`, `TiltShift`, `FocusHunt`, `Handheld`, and `CameraPush` (from `paper/kit.tsx`). The catalog's `paper/camera.tsx` section says when each fits.
- Cut options: `hard`, `whip`, `zoomThrough`, `pageTurn`, `tearAway`, `tapePull`, `stampCut`, `infiniteZoom`, `popUpBook`, `keyhole`, `burnAway`.
- A plain `CameraPush` is allowed on at most a third of the scenes.
- Copy each row's camera into its scene block header. The cut column goes into `episode.json` as `"cuts": {"S04Name": {"kind": "tearAway"}}` (no entry means a hard cut), which `papercut-build` fills.

## 3. Scene blocks

One block per scene, 1.5-5 s each, cutting on sentence boundaries:

```
## S03: <beat>  (5.6-8.2 s, 78 f)   BANNER: <TAKEAWAY IN CAPS>
Location/bg: <world location + bg colour>     Camera: <camera.tsx component + params, from the table>   Cut in: <kind>
Cast: <who, accessories>                       Caption band: y=0.76
| VO word (stressed) | frame | event                                    | motion spec                   |
| "<word>"           | +6    | <prop enters / state flips / acts>       | <spring/slide/swap + frames>  |
Ambient: <LED blink, idle bob, stars, screen waveform>
Boil: banner + labels, +-1.5 px every 2 frames
SFX: <pop, chime, click...>
```

- Expand each staging-table row into frame-level events: one per stressed word (every 0.4-0.8 s), ambient motion always on. Frames are offsets from the word, later read with `cueOf(ID)(word, n)`.
- Product UI is the rough rebuild on a paper monitor or laptop, with fake interactions (cursor click, typing, progress, waveform, list scroll).
- **Proof:** once per reel, a real screenshot of the source page (a browser capture via `library/tools/capture.mjs`, not a redraw) taped onto a paper card, with a red marker circle drawing itself around the key line. Everything else stays a rough papercut rebuild.
- One callback to an earlier set before the CTA.

## 4. Camera and transition rules

- Every scene has one move. A slow push is the baseline. Add a parallax orbit on lit sets for depth, a punch-in or snap zoom on the stressed word for numbers and jokes, a foreground pass (blurred paper object across the lens) or rack focus, a pull-back to reveal scale, and a freeze frame with a label on the struggling-mascot beat.
- Mostly hard cuts on the banner change. A whip-pan with motion blur on 2-3 topic changes, a zoom-through when going "inside" a screen, door or mirror, at most one page turn or tear per reel (on the catch or a before/after contrast), and the tape pull into the CTA (a plain kraft strip, with an optional `label` to print a word on it).
- The cut out of the hook carries motion through it. Apply the rule from `papercut-hook` to S01 and S02.
- Transitions run 6-12 frames, each with its SFX (whip, zoom, page-flip, rip, tape-peel).
- In a library project, chain scenes with the kit's transition series, which keeps every scene start on its `plan.json` frame so the voice stays in sync.

## 5. SFX plan

- Air sounds (whoosh, slide, whip, zoom) together: at most one every 2.5 s of reel. `cues.py` prints a note above that. For scale, 12 in 33 s is fine and 24 in 26 s is distracting.
- Entrances get contact sounds (pop, thud, stamp) or silence. Count them in `tools/cues.json` before the audio render.
- Name SFX from `library/audio/CATALOG.md` in each block's `SFX:` line. Scene agents write the real rows to `tools/cue_sheet.d/<Scene>.json`.
- Pick the bed preset (`episode.json` "bed") and set `cutSfx` to match the cut kinds: `tearAway` rip, `tapePull` tape-peel.

## Gate

- [ ] Every scene has a camera and a cut-in, and a plain `CameraPush` is on at most a third of them.
- [ ] Every stressed word has an event; ambient motion is listed.
- [ ] One proof beat, one callback, the tape pull or whip into the CTA.
- [ ] At most one page turn or tear; air sounds within budget.

- Name the anticipation and the one exaggerated beat in each scene block's event table. The 12 principles, mapped to kit components, are in `../papercut-explainer/references/motion-principles.md`.

## Hand-off

Next is `papercut-build`, which scaffolds the project and turns the Camera / Cut table and scene boundaries into `episode.json`. It reads `STORYBOARD.md` and `narration/script.json`. The Timing section of `STORYBOARD.md` is generated later, after the voice, so leave it out.
