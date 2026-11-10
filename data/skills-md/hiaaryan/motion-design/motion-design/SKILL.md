---
name: motion-design
description: "Aaryan's direction taste for work that is designed by being built — code-authored motion films (TypeScript + GSAP + Playwright + ffmpeg), promos that reproduce a real product UI, easing and camera work, sound design and score, voiceover scripts, and the review loop they run on all of it. Use when building or revising a film, promo, title sequence, scene, transition, or any timeline-driven motion; when choosing an easing curve, a duration, or a cue; when scoring or mixing; when writing or cutting VO; when reproducing product UI in a non-product surface; and whenever feedback arrives as 'feels off', 'too linear', 'too fast', 'a teensy bit', 'scrap it', or a frame number. Triggers on: film, promo, storyboard, scene, shot, timeline, GSAP, easing, ease in out, tight curve, linear, overshoot, dwell, camera, zoom, pinch, stagger, motion blur, render, 4k, 60fps, frame by frame, cue, sound effect, score, music, bed, duck, mix, voiceover, VO, script, pacing, dark mode section, UI fidelity, squircle, badge, connector, strands."
---

# Motion Design

Work that is designed by being built: no After Effects project, no mockup handed to an engineer. A film is a storyboard module, DOM, GSAP on the product's own easing curves, Playwright stepping the clock one frame at a time, ffmpeg. Sound is code too — scenes place cues, the mix is assembled offline against the same timeline. Because it is all code, changes are cheap and nothing is precious. **Films are edited like code, not redone.**

This skill carries the taste, not the pipeline. The pipeline is whatever your project already uses.

Read the companion files when you reach that work:
- `motion.md` — curve algebra, the dwell problem, cameras, speed laws, blur, chain lag
- `sound.md` — score arrangement, cue design, the mix, the VO chain
- `ui-fidelity.md` — reproducing a real product UI
- `copy.md` — on-screen sentences and VO scripts
- `working-with-me.md` — the review loop, vocabulary, escalation ladder

---

## 1. The working agreement

These come before craft. Breaking one wastes their time, and is the fastest way to lose a round.

**Never render until told.** Not once. They said *"dont render until i say so!!"* and *"always add it in preview dont talk about rendering until i say so"*. Work lands on the dev server; they watch it there. Finish a change with "it's on the dev server" — never with "want me to render it?". When they do say render, ask nothing else and render.

**"Preview" means they watch it, not that you screenshotted it.** *"by preview i mean me viewing it on the dev server."* Your screenshots are for your own verification, never a substitute for their pass.

**Phases are serial: scenes → cues and score → VO.** They imposed this twice (*"from now on forget about timing and sounds and VO. we'll come to that later. we'll just do shots and scenes for now ok?"*, *"now do cues and sound effects and music scrap the whole old thing. dont do vo yet. we'll do it at last"*). Never work ahead into a later phase, and never let an earlier phase's problem get hidden by a later phase's polish.

**"Scrap" is literal.** It means delete the ideas, not re-skin them. It has had to be said three ways, the last in capitals: *"by redesign i mean scrap the whole thing"*, and then — scrap **everything**, all the content ideas. When you hear scrap, the next thing you show must share no layout, no card, no copy and no beat with what it replaces.

**One note, one change.** Never bundle an unrequested improvement into a fix. Never "while I was in there". They revert fast (*"nah revert"*, *"no no undo increase intensity earlier was fine"*), and a bundled change makes a revert cost them two rounds.

**Keep the previous value recoverable.** Every tuning note may be undone next message. Put old numbers in the comment, not in your head.

**Give the estimate before a long job, unprompted.** *"whats the stimated time"*. When a generation ran ten minutes for a single sentence, they said so. State the number, start it in the background, and never make them ask. An estimate must come from a measured rate — see `working-with-me.md` on the ETA you got wrong.

---

## 2. Motion

### The curve

The house curve is **tight through the middle, very soft at both ends**:

```ts
function tightInOut(x: number, n = 4): number {
  const k = Math.min(1, Math.max(0, x))
  return k < 0.5 ? 2 ** (n - 1) * k ** n : 1 - (-2 * k + 2) ** n / 2
}
```

**`n` *is* the peak velocity**, in units of the move's own average, and the curve is flat to order n−1 at both ends. That is the whole reason to use it over a cubic-bezier: you set the thing you actually care about. Their note was *"the curve should be tight on center and really smooth on ends"* and, when a standard in-out was used, *"NAH IT LOOKS TOO LINEAR SMOOTH ON START THEN FAST THEN SMOOTH AT END DONT YOU KNOW HOW MOTION VIDEOS WORK"*.

Picking `n`:

| What is moving | n | Why |
|---|---|---|
| Camera between stations | 4 | A camera has mass. Starts and stops at rest, spends most of the move at speed. |
| A graphic element opening or closing | 5–7 | The move is the event; it can be quicker through the middle. |
| A crossing over an empty frame | 9 | Nothing is on screen mid-move, so spend the speed there and leave the ends almost motionless. |

**Never linear.** *"everything should be smooth ease out no linear curve please."* One exception exists in the whole film and it earned itself: a fade that must read as fading from its first frame, where any ease front-loads it so hard the element is still at nine tenths while the frame is visibly changing. If you use linear, write down which of those two conditions made it necessary.

**Never use a product's resize/state curve for a camera.** `EASE.resize` is an ease-out — right for a panel changing size under a hand, wrong for anything with mass, because it leaves at full speed and spends the rest of the move settling.

### The dwell law

**Two moves that are one gesture must never pause between them.**

This is their most-repeated structural note:
- *"see when the tile is collapsing and becomes the tiny dot there is a tiny stop it takes before splitting into two. it should not be there it should be smoothly in motion at all times same with when the dots pinch then tiny stop then zoom starts"*
- *"i dont like how the end of the list stop for a bit 0.5secs and then moves on to the next slide. it should keep moving in eased out and then move to next text frame"*
- *"ok it should not stop at the end of the list"* / *"keep moving"*

The cause is mechanical, not aesthetic: **a curve that is flat at its end, followed by a curve that is flat at its start, is a hold.** Both are doing what they were asked. Two flat ends meeting is still a stop.

The fix is `trim(f, a, b)` — the same curve with a dead end cut off and the rest stretched to fill:

```ts
const trim = (f: (x: number) => number, a = 0, b = 1) =>
  (x: number) => (f(a + (b - a) * x) - f(a)) / (f(b) - f(a))
```

- **Trim a head** (`trim(f, 0.25)`) → the move leaves at the pace it would have reached. Use when something hands over *to* this move.
- **Trim a tail** (`trim(f, 0, 0.84)`) → the move arrives moving and stops dead. This is a collision, and it is only right when something else takes over in the opposite direction at that instant.

Never trim both ends to "smooth things out". Each trim is a claim about what happens on the other side of the join.

### Moves that belong together

**Start together, end together.** *"zoom out and move up shouldnt stop till end they should run together"*, *"start together and end together"*, *"the end of zoom out and start of move up should be intertwined"*. Two numbers animating over one duration on one curve is one gesture. Sequencing them, or overlapping them by a fraction, reads as two events and they will say so.

Corollary: when they ask for a scale change *and* a translation, build them as a single move whose peak scale and peak travel land on the same frame. Leading one with the other has been tried and rejected — *"the drift is a camera waiting, however alive the number keeps it."*

### Reversals

**A gesture reversed uses the same curve *and the same duration* as the forward one.** *"the collapse of tile should have same ease out as expand"*, *"the circle zoom in should have same ease in out as the tile"*. When a reversal felt wrong, the ease was already correct — the duration differed. Check duration first.

Mirror the secondary properties too: if the forward move rounded a corner, the reverse un-rounds it on the same curve at the same time.

### Overshoot

**No overshoot** unless geometry demands it. *"why the two dots still move outward once they have reached their final point??"*, *"the arc still overshoots the angle line a bit"*. But geometric truth outranks motion polish: when an overshoot was the geometrically correct depiction they reversed themselves — *"ok nvm it can overshoot the angle line we need to keep geometry perfect"*. If a diagram's accuracy and a motion preference conflict, accuracy wins and you say which you chose.

### Sub-pixel discipline

**No vibration, ever.** *"when this single dot is moving before becoming the tile it has minor vibrations in its movement there are more elements like this can you please fix."* Don't eyeball this — sample the position every frame across the move and assert the second difference stays below a quarter pixel. Vibration almost always means two writers on one `transform`, or a value being recomputed from a rounded intermediate.

### Speed as a law, not an easing

When the note is about *the rate things arrive at* rather than the shape of one move — *"it should stop on the list first render first item then second slowly starts moving then becomes faster then stops again at the end item"*, *"the speed gain on the list should be smooth and so with speed decel"*, *"the speed gain still feels a bit sudden"* — stop writing eases and write a speed-at-position law instead. Duration then falls out of it. The logistic in distance is in `motion.md`, with the reason a clipped exponential whips and a logistic does not.

### Motion blur

**Blur is the distance actually covered in a frame, never a dialled number.** A 270° shutter is 0.75 of a frame, and the Gaussian matching a box of length L has deviation `L / sqrt(12)`. Dividing by anything else makes the blur stop agreeing with how fast things look like they are going — their note was *"the pacing is off the motion blur doesnt match with the speed also"*.

Blur in **y only** for a vertical move. CSS `blur()` is isotropic and smears a fast vertical move sideways, which reads as out of focus rather than as going quickly. Use `feGaussianBlur` with a per-axis deviation.

Anything that crosses the frame during a fast move needs the filter, not just the thing you think of as "the moving object" — a sentence the camera flies past with hard edges and no smear will strobe.

---

## 3. Sound

Full detail in `sound.md`. The rules that must not be broken:

**The bed never ducks.** No sidechain, no automation, no per-line gain rides. *"why volume is going up and down in some sections"*, *"from 17-26 volume lowers down and music becomes blurry"*, *"dont change music volume at all during vo no change in music or cues (current track) please"*. If a voice does not sit, **the voice moves** — the music stays where it is. Dynamics come from the arrangement changing at section boundaries, never from a fader.

A flat trim applied to everything that is not the voice is allowed and is not ducking (*"reduce whole audio sound a bit except vo"*). One constant, applied to score **and** cues — trimming only the music leaves a chime landing over a quietened bed at its old level.

**Keep the pacing, replace the timbre.** *"sounds too gamey and 8bitey you need to change it completely, but i liked how you paced it between frames and sections."* When they reject a score, find out whether they are rejecting the arrangement or the instruments before you throw away a structure they just praised.

**The register they want:** heavy, premium, satisfying, elegant, uplifting, fast-paced, futuristic/computery. The register they reject: childish, gamey, 8-bit, kindergarten, mysterious, awkward, bland. *"it needs to feel heavy and premium and satisfying"*.

**Cues are synced to the picture frame-exactly, and may ring on past the element.** *"they should exactly be synced with errors showing"*, *"the cues can be longer too and can go on after the element is visible yk dont have to be an instant"*.

**One family, every member different.** *"they need to start and end different for every cue like sound different but same pattern."* Same synthesis path, same envelope shape, per-cue variation in the pitched content — a shared rng stream for what the family has in common and a per-cue stream for what differs.

**The lesson that cost six attempts: summary statistics are not a sound.** Spectral flatness, crest factor and centroid all matched the reference while the result was audibly nothing like it, because the structure was absent — narrow ringing resonances, and silence between events. Read `sound.md` before touching cue design; it lists every wrong turn so you do not repeat them.

---

## 4. UI fidelity

Full detail in `ui-fidelity.md`. The law:

**If the product draws it, draw the product's version, pixel for pixel.** *"strictly use our ui no other card ui acceptable"*, *"also you have to keep the actual ui"*, *"extract every piece every edge case of the ui"*. Go read the real components in the real repo before building anything that looks like them. Every deviation they have ever found, they have named: the thinking orb's dot density, the strands' position, the connector starting at an icon's centre instead of below it, a progress ring that the product shows and the film didn't, a bar radius that changed between rising and settled.

**Never invent a colour.** Use the theme's tokens. If a surface needs a value the theme has no token for, say so rather than picking one.

**Never show developer surface.** *"why are you showing code??? we are not making this for devs"*, *"dont show json in approvalcard"*. Code, JSON, ids, counts of internal things — all out.

**No card appears twice.** *"also the cards are too repetitive across sections, no section should have same card."* Each section earns its own object.

**Roundness is squircle, and fully-round means fully-round.** *"i want all the roundness to be squircle like apple on the corners"*; badges and pill buttons are `border-radius: 50%`-equivalent, not "quite rounded".

---

## 5. Type and emphasis

**One voice, one size.** *"use same text size in ride text screens which intro has."* Every sentence the film says in its own voice is set at the title's size, in the title's face, at the title's letterfit. A size chosen for each statement on its own merits is three captions by three people.

**One line, one sentence.** *"still too much text to scan you should not add multiple lines only one line on sentence."* A statement runs two lines at most, and both statements in a pair break the same way — pick the measure that forces that, and `text-wrap: balance` only once the measure already guarantees the line count.

**Emphasis is opacity, not a second colour.** Lit words at 1, the rest at **0.42**. The note was to put the claim words and the agent's badge in the foreground and mute the rest, *exactly* as the title sequence already treated the product name. Same treatment in every statement in the film, so the whole piece reads as one voice. Multiplying into the reveal's own opacity channel gives it for free and follows the palette.

**What gets lit:** the claim, not the subject. In *"Nothing in your store changes until you approve it."* the lit words are **Nothing … until you approve it** — the condition is the promise, *in your store changes* is only what it is about.

**Smaller than you think.** They have asked for smaller type four separate times (*"the texts are just tooo big too big"*, *"font should be smaller in both text screens"*) and never once for bigger. A statement that fills the frame stops being a sentence and becomes a billboard.

**Centre statements; centre them in the space they own, measured.** Placing two statements at the top of their sections leaves each riding high; measure the rendered height and centre it.

---

## 6. Copy

Full detail in `copy.md`. The three rules they enforced hardest:

**Never tell the user something they already assume.** *"It reads your real store — not a copy, not a summary"* → *"the user already know its not a copy or summary obv."*

**Never brag with counts.** *"we dont want user to know how many things it can do but what it can do."* No "eighty-five things", no "fifty-three of them".

**Never imply a limit you don't mean.** *"And then it stops."* → *"dont want to imply it stops."*

And: no scene-setting fluff (*"buddy i dont want that morning part please"*), no dangling referents (*"every one of these what? explain it"*), and the ending names the principle rather than the mechanic — their final edit was *"your press is what does it"* → **"your consent is what does it"**.

**Say a thing once.** The close lost its wordmark, then its caption, then its VO line, each for saying a second time what the film had already said. An ending is the first place to cut, not the last.

---

## 7. Engineering that holds up

**Solve the number; never dial it.** Every constant that could be derived, derive it — a handover point by bisection on the tween, a row's arrival time by inverting the camera's own curve, a zoom target from the frame diagonal. Dialled numbers drift the moment anything upstream moves, and they change things upstream constantly.

**Guard what you derived.** A throw beats a comment:
```ts
if (COL_END > COL_BOTTOM) throw new Error(`column runs to ${COL_END}, gap starts at ${COL_BOTTOM}`)
```
This has caught real breakage three times. Any measured-vs-constant relationship gets one.

**Scene boundaries are floating point.** `t0 + dur` and the next scene's literal `at` are equal in decimal and not in binary, which produces exactly one wrong frame — their note was *"at 30.20 secs frame 1812 the ask card snaps and becomes scaled up only in that frame"*. Use a half-frame epsilon (`EDGE = 1/120`) at every handover.

**Scrubbing suppresses callbacks.** `tl.time(t, true)` does not fire them, so any state derived from the timeline must be recomputed in a per-frame syncer, never in an `onUpdate`. A film that plays correctly and scrubs wrongly has this bug.

**Draw at native size, scale down.** Never scale up — an element drawn small and enlarged is blurry at 4K. Draw it at the size it will be largest and shrink.

**Verify by measurement, and say what you measured.** Rendered opacity against cue times, corner pixels either side of a white-frame join, position deltas across a move. *"ARE YOU EVEN EVALUATING YOUR WORK FRAME TO FRAME?"* is what happens when you don't. Measuring the wrong element counts as not measuring — check your probe matched what you think it matched before you report a conclusion.

**Verify before you claim, and report failures plainly.** They catch overstatement immediately and it costs you the round.

---

## 8. Before you show them anything

Walk this list every time. Most of their notes are things on it.

1. Does anything **pause** between two moves that are one gesture?
2. Does anything move **linearly**, or on a product state-curve that should have mass?
3. Does a reversal use the forward move's **duration**?
4. Any **sub-pixel vibration**? Measure it.
5. Does **blur** match the distance actually covered this frame?
6. Is every component the **product's own**, down to density, offsets and radius?
7. Does any **card repeat** across sections?
8. Is every statement at the **same size**, two lines, centred, emphasis at 0.42?
9. Is there **any developer surface** on screen — code, JSON, counts, ids?
10. Does the **bed move** anywhere? It must not.
11. Are cues **frame-synced** to what they land on?
12. Is there **dead screen time** anywhere? They count it: *"there is literally one second of whitescreen before ask card shows."*
13. Have you said anything **twice** — on screen, in voice, and in the mark?
14. Did you change **only what they asked for**?
