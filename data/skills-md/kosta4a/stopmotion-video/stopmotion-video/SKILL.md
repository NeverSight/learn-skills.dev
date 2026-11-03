---
name: stopmotion-video
description: Rules, Remotion helpers and audio scripts for stop-motion style video cut to music, proposing Remotion by default to make it. A low frame rate is kept on purpose, with one pose per eighth note of the song. Pages start on bar lines, clicks land on kicks and snares, and the skill teaches when to skip a beat. Use when making or reviewing stop-motion, low frame rate, beat-synced or music-synced video. Also use for cutting a video to a song, Remotion launch films cut to a track, compositions timed to a BPM, metronome or click tracks, kinetic type timed to a beat, or scenes played live on a web page in time with a metronome. It covers measuring a song's tempo, bars and drops, and deciding where a cut, a click, a hold or a transition should land.
---

# Stop-motion video

Videos made with this skill move like stop motion shot to a song. Each pose is held for one eighth note, then everything changes together. Pages come on at bar lines. Every click sounds on a drum hit, and the big changes land on the big kicks. The frame rate stays low on purpose. When a move looks rough, its poses are spaced better; the beat is never smoothed away.

The rules come from making a 47-second launch film cut to a drum and bass track at 169.825 BPM, over a few hundred rounds of notes. The film ran at 30fps and held one pose per eighth note, which is 5.66 poses a second, 5 or 6 frames each. The values here are the film's, and in live.md those of a web page that plays scenes from it against a metronome. Where a rule generalises beyond them, the text says so.

**Vocabulary**

- **Pose**: one held picture, the song's eighth note. The code calls it a beat (`STEP_MS`, `useBeat`).
- **Song beat**: what the BPM counts, a quarter note. It is two poses long and gets one metronome click.
- **Bar**: four song beats, eight poses. In drum and bass the kick falls on pose 0 and the snares on poses 2 and 6, counting from 0.
- **Hit**: a drum sound in the song. A **big kick** is the kick that opens a phrase (every odd bar in the film's track).
- **Authored ms**: times in the code. They are written on a 200ms pose and play `SPEED` times faster (`SPEED = TEMPO / 150`).
- **Timestamps** are written m:ss.ff, where ff counts frames. That is how Remotion Studio shows time, and how notes arrive.

## Operating posture

- **Keep the low frame rate on purpose.** Never smooth the beat away to fix a move. Space the move's poses better instead.
- **Everything holds a pose for a beat and changes together**, transitions included. Nothing runs on its own clock: an embedded animation or a scrolling page steps on the pose too. Typing is the one exception: it runs quicker than the beat, as typing does, from its pose.
- **The song is the clock.** Measure it before you storyboard. Lay pages on its bars and put actions on its hits.
- **One clock for the whole video.** Count poses on the video's frames, never on a scene's.
- **Move in whole bars.** Change a page's length by whole bars, or take the poses back elsewhere before the next bar line. Otherwise everything after it falls off the song.
- **No idle poses.** Once what happens on a page is done, hold it only as long as a viewer needs to take it in.
- **Few kinds of change, one direction, nothing fades.**
- **Check by measuring.** Use stills one per pose, timings measured in the render's audio, and a metronome cut. Don't judge sync by eye.

## The tool: Remotion, by default

Propose Remotion to make the video unless the project already makes its video another way. Say so before storyboarding, with the reason, and change only if the user asks for another tool. On a web page, play it live instead ([live.md](references/live.md)); in a motion tool, the rules still hold but the helpers don't.

- **Why it fits.** Every frame is a React component worked out from the frame number, so a pose is exact on whatever frame it lands and renders the same every time. A render draws frames out of order, across several tabs, which only a video driven by the frame survives. The helpers in `assets/remotion/` are written for it, and its Studio shows time as m:ss.ff, the form notes arrive in.
- **Set it up.** `npx create-video@latest` with the blank template. Pin `remotion` and every `@remotion/*` package to one exact version (the film's: 4.0.532), and keep TypeScript on 5.x ([clock.md](references/clock.md) §7). One composition, 1920×1080 at 30fps. Copy `beat.ts` and `transitions.tsx` into `src/` and set `TEMPO`.
- **Configure it.** In `remotion.config.ts`: JPEG frames at quality 95 (the default 80 roughens flat grounds and thin type at their edges), BT.709 colour (so players show the colours as the browser does), and overwrite on.
- **Preview and render.** `npx remotion studio` to work in; `npx remotion render <Comp> out/<name>.mp4` for 1080p, with `--scale=2` for 4K; `--frames=<first>-<last>` or `npx remotion still <Comp> --frame=<n>` to check a stretch or a pose.

## The decision order

Work top to bottom. Each step constrains the next.

1. **Propose the tool.** Remotion, unless the project already makes video another way; set it up as above before anything else.
2. **Measure the song.** Find the tempo from its onsets and check that the grid holds over the stretch you use. Mark the bars and phrases, where the drums drop out and come back, and the big kicks. Cut the excerpt exact to the sample, a hair (23ms) before a phrase's first kick. See [song.md](references/song.md).
3. **Set the clock.** A pose is the song's eighth note. Author on a 200ms pose with `SPEED = TEMPO / 150`, render at 30fps, and count poses on the whole video's frames. See [clock.md](references/clock.md).
4. **Lay the pages on bars.** Write the storyboard in poses. Each page is a whole number of poses and starts on a bar line. Map the song's events to poses before you animate anything.
5. **Place the hits.** Code is typed in chunks on the eighths, and titles and a held backspace run quicker than the beat from their pose. Clicks and pops go on snares, landings and new pages on downbeats, and big changes on big kicks. The build goes in the quiet, and the landing comes when the drums return. See [hits.md](references/hits.md).
6. **Space the poses.** Pick each curve for its poses. A move's first pose is its first step, and every pose moves it visibly. Things land rather than creep. See [poses.md](references/poses.md).
7. **Change pages.** Use a hard cut on the beat, a cut of the ground, a page laid over like a sheet, the camera going into a colour, a fill from inside, an opening through a shape, or pixel blocks. Never a fade. See [hits.md](references/hits.md).
8. **Set the type.** Tracking tightens as size grows, and leading tightens with it. Every word passes 4.5:1 against its ground at every pose. Titles are typed, not faded. See [type.md](references/type.md).
9. **Make the sound.** Every click goes on the song's own hit, placed to the sample, and all clicks are baked into one track that starts with the song. Duck the music under the clicks, and keep a metronome cut for checking. See [sound.md](references/sound.md).
10. **Decide where to skip a beat.** Drop, duck, hold, snap, cut whole bars, end on a song beat. See [skipping.md](references/skipping.md).
11. **Check.** Make a contact sheet, measure the sync, and watch the metronome cut. Take notes as timestamps mapped to poses. See [checking.md](references/checking.md).
12. **Playing it live, in a browser?** The same rules against a metronome: one clock on the page's time, the picture 25ms ahead of the sound, the sound scheduled ahead on the audio clock, and with no song every change on a click. See [live.md](references/live.md).

## Rules at a glance

### Clock

| Item | Rule |
|---|---|
| Frame rate | 30fps, on purpose. A smooth 60fps variant may share the storyboard ([clock.md](references/clock.md) §8) |
| Pose | the song's eighth note: 176.65ms at 169.825 BPM, 5.66 a second, 5 or 6 frames at 30fps |
| Authoring | every time in ms on a 200ms pose; `SPEED = TEMPO / 150`; `ms()` to frames, `seconds()` for embedded clocks |
| Pose `n`'s first frame | `ceil(n × frames per pose)`, on the whole video's frames (`beatFrame`) |
| Page | a whole number of poses, starting on a bar line (pose divisible by 8) |
| Changing a length | by whole bars, or take the poses back before the next bar line |
| Studio drags | a dragged track writes a `from` offset that shifts picture against sound: remove it |

### Spacing

| Move | Curve | Poses |
|---|---|---|
| In and out (a camera move, a pass, an underline) | `easeInOutSine` | 7, 18, 25, 25, 18, 7% over six |
| In from off the frame | an ease-out | otherwise it spends its slow start out of sight |
| A page laid over another | `easeOutSine` | 38, 70, 92% over a three-pose transition |
| Zoom, thickening lines, growing openings | grows by the same factor each pose | a zoom keeps its target on a straight line to the middle |
| Not on few poses | cubic in-out (3, 12, 35, 35, 12, 3: leaps in the middle); the strong ease-out (lands on its first pose: 78, 97, 100% as a three-pose transition, 88, 99, 100% as a move with `moved()`) | |

### Things on the beat

| Thing | Rule |
|---|---|
| Click | one pose pressed, on a kick or a snare; the cursor gone the pose after its last click |
| Caret | solid while typing, then two poses on and two off |
| Spinner | at most a quarter turn a pose; over half a turn a pose reads as turning backwards |
| Rolled mark | turns by its travel over its radius, lands upright, on `easeOutSine` |
| Counter | a figure a pose on the strong ease-out, tabular figures, two poses on the round number |
| Titles | typed quicker than the beat from their pose: a word every three frames; long lines a letter every 25ms (authored) |
| Code | typed in uneven chunks of 2 to 4 characters a pose |
| Held backspace | one run, a letter every 25ms (authored), line breaks too |
| Camera rise | rises, holds dead still for two poses at the top, comes down |
| From off the frame | not drawn until it has moved |
| Placed by hand | off by at most a tenth of that pose's move, not at all once it stops; down once within a few px |

### Hits

| In the song | In the picture |
|---|---|
| Eighth notes | code typed in chunks, a move's steps |
| Snares | clicks, pops |
| Downbeats | landings, new pages, a page's first action |
| Big kicks | big changes: a page landing, the last page whole, the final click |
| Drums drop out | the build |
| Drums come back | the landing |

Clicks must be on the beat. A transition can be off it.

### Sound

| Item | Rule |
|---|---|
| Click placement | to the sample, on the song's hit (the film's hits landed 25ms after its poses) |
| Click file | 40ms of quiet before its tick, so trimming to the sample never eats it |
| Click track | every click baked into one track that starts with the song |
| Ducking | silent round a click that matters; 45% for 160ms under the others; 10ms fades |
| Metronome | a click on every song beat on its hits, the bar's first higher, music at 20%; never in the export |

### Type

| Size | Tracking | Leading |
|---|---|---|
| under 20px | 0; mono capitals +2% | 1.4–1.5 |
| 20px and up | −1% | about 1.4 |
| 32px and up | −2% | about 1.25 |
| 56px and up | −3% | 1.1–1.2; down to 0.9 for two-line display titles |

Every word must reach at least 4.5:1 against its ground at every pose. Use one family by default (Geist and Geist Mono in the examples), black on white, as tactile-design does; the film itself paired a display face with its text face and set its pages on flat colour grounds. Counters use tabular figures. Titles are typed on, never faded in.

### Live, in a browser

| Item | Rule |
|---|---|
| Clock | `beat = anchorBeat + elapsed s × BPM / 60 × 2` on `performance.now()`; re-anchored at now on a tempo change; every scene a pure function of the beat |
| Picture | reads the beat 25ms ahead; every scene committed inside the animation frame (`flushSync`) |
| Sound | a timer every 25ms schedules the next 120ms on the audio clock (`getOutputTimestamp()`); the window measured in audio time, output latency added |
| In view | only what's on screen animates; the example most on screen is heard |
| Starting | tried at load, then on the first press or key; a press that started the sound doesn't mute it (600ms); a mute remembered |
| No song | every change on a click: a move may step on the eighths but starts and lands on clicks; the click's own metronome click dropped |
| Metronome | a quiet wooden knock (880Hz in 50ms, 1320Hz on the bar's first), no thump without music, all through one limiter |
| Pause | on the nearest click: played on to it, or settled back over 160ms |
| Reduced motion | a still pose that shows the idea, moving only after a press of a sound button |
| Type | words 4.5:1, meaningful marks 3:1, a scaled scene's smallest words 9px or more as rendered |

## When to skip a beat

The grid is strict, so breaking it is a decision. Every break below has a reason in [skipping.md](references/skipping.md).

- **Drop the music round a click that matters.** It goes silent from 50ms before the click to the next bar line, with 10ms fades. The click is heard alone, and the beat comes back with what follows.
- **Duck under the other clicks.** Lower the music to 45% for 160ms so the click's thump has room.
- **Hold a result alone** for one song beat before the next thing starts, such as a tick after a copy.
- **Hold two identical poses** at the top of a rise.
- **Hold two poses on a round number** before moving on.
- **Snap a note that falls between beats** to the nearest accented beat.
- **Cut whole bars**, even when the note asks for less. Say what it costs.
- **End on a song beat.** The last page holds about 2 seconds, with the music fading over the last pose. Otherwise end right after the action.

## Never ship

- [ ] Motion smoothed off the beat to hide a badly spaced move
- [ ] A scene counting poses from its own first frame
- [ ] A page that starts off a bar line without a reason written next to it
- [ ] A length change that isn't whole bars and isn't taken back before the next bar line
- [ ] A Studio `from` offset left in the composition tree
- [ ] A click off a kick or a snare, or a click sound placed on a frame instead of to the sample
- [ ] Short click sounds started at their own frames instead of one baked track
- [ ] A move whose first pose is the pose it leaves, or that creeps its last few px
- [ ] Something from off the frame drawn before it has moved
- [ ] A spinner or wheel turning over half a turn a pose
- [ ] A fade, or a crossfade between saturated grounds
- [ ] Ground changes faster than three flashes a second
- [ ] A word under 4.5:1 against its ground at any pose
- [ ] Tracking left at 0 on display type, or a counter in proportional figures
- [ ] Idle poses after a page's action is done, or a tail that "extends for no reason"
- [ ] The metronome in the export
- [ ] CSS transitions or animations, or a library's `animate()`, in a render
- [ ] Not checked pose by pose and measured against the song
- [ ] Live: sound played on a frame, or a lookahead that leaves out the output's latency
- [ ] Live: a picture drawn after its click, or scenes committed a frame after the rest
- [ ] Live: a first press that starts the sound and mutes it, or scenes moving under reduced motion unasked

## References

Open the file for the step you're on. Each pairs a value with its reason, so it carries to a new song.

- [song.md](references/song.md): measuring the track, cutting the excerpt, and mapping it to poses and bars.
- [clock.md](references/clock.md): one clock, frames per pose, bar lines, page lengths, Remotion wiring and the 60fps variant.
- [poses.md](references/poses.md): stop-motion spacing and the rules for each kind of thing.
- [hits.md](references/hits.md): what lands where, and the transitions.
- [skipping.md](references/skipping.md): when to skip, hold, drop or duck a beat, and the reason for each.
- [sound.md](references/sound.md): clicks placed to the sample, ducking, the click track and the metronome.
- [type.md](references/type.md): type in the frame, covering tracking by size, leading, contrast and typing.
- [checking.md](references/checking.md): contact sheets, measured sync, notes as timestamps and the review loop.
- [live.md](references/live.md): playing it live, the same rules in a browser against a metronome: the page's clock, sound scheduled ahead, starting and pausing the sound, reduced motion and type on screen.

Tools:

- `assets/remotion/beat.ts`: the clock and the beat helpers (`TEMPO`, `SPEED`, `ms`, `useBeat`, `moved`, `clicked`, `press`, `blink`, the curves).
- `assets/remotion/transitions.tsx`: `onTheBeat`, `inSteps`, `onQuarters`, `slideOver`, `pixels`, `throughShape`.
- `scripts/find-tempo.mjs`: a song's tempo, grid, drift and bars, from a WAV.
- `scripts/duck.mjs`: the music silenced or lowered round clicks.
- `scripts/make-metronome.mjs`: a click track for checking.
