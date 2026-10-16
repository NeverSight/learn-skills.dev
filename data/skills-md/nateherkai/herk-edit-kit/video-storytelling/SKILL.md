---
name: video-storytelling
description: Design and build the visual layer of a long-form talking-head video as one persistent world the camera moves through, instead of a sequence of separate graphics. Use when asked to edit a video, add motion graphics, design the visuals for a script, plan an edit, or fix an edit judged confusing, text-heavy, hard to follow, or "clearly made by an AI". Covers the persistent world, camera grammar, the spotlight rule, spatial open loops, ornament and token discipline, transcript timing, and the verification gates.
---

# Video storytelling

How to build the visual layer of a long-form video so a viewer is still oriented
at minute nine. Applies to any talking-head video with a script: a news take, a
single-topic deep dive, a comparison, a tutorial, a listicle.

The failure this replaces is scene-thinking. A new graphic every few seconds
makes the viewer restart comprehension every few seconds, and no individual
graphic is at fault, which is why the feedback comes back as the vague
"confusing" or "too much going on" rather than as a specific defect.

For a neutral practice beat sheet, read `docs/STORYTELLING-WORKBOOK.md` at the
repository root. The reusable design system is in this skill's
`reference/design-system.md`; the worked open-loop geometry is in
`reference/patterns/wall-of-slots/`. Private source videos are not required.

This is not `hyperframes-video-beats`. That skill places overlay cards on top of
a talking head. This one designs the thing the video is *about*.

## 1 · The four principles

### One persistent world

The video lives in a single space, and it never resets. Everything the viewer has
already seen still exists where they left it, and new material is added to it
rather than replacing it. An element, once drawn, is never redrawn, moved, or
relabelled.

Everything else in this skill depends on that. The camera has nowhere to go if
the space keeps changing, a spotlight means nothing if there is nothing else on
screen, and an open loop cannot stay open in a world that resets.

The world also has to be worth staying in, so decide the spatial grammar before
building anything and hold it for the whole runtime. In the reference build:
left to right is toward the outcome, up is toward a human and is the only warm
thing on screen, down is into a system of record. A viewer who learns that in the
first two minutes reads the rest of the video for free.

Break the grammar exactly once, deliberately, for meaning. The reference build's
only right-to-left move in ten minutes is a resolved ticket reversing back into
the queue on the words "reopen rate". It lands without a word because direction
had meant something for the previous three minutes.

### The camera is the edit

Cutting to a new graphic costs the viewer their bearings every time. Moving
through a space that stays put costs them nothing. A push-in then reads as "look
closer at the part of the thing you already understand", and the pull-back is
where the work pays off, because everything built so far is still there.

Work in three altitudes and move between adjacent ones:

| Altitude | Shows | Used for |
| --- | --- | --- |
| World | the whole space | orienting, payoffs, "here is where we are" |
| Region | the subgraph under discussion | most of the runtime |
| Detail | one element | a number, a state change, a decision |

Jumping detail to world is disorienting unless it is a deliberate payoff beat, in
which case it is the best move available.

Rules that cost a rebuild each to learn:

- **Name framings as exact world windows, not as scale factors.** Window
  boundaries must fall *between* labels. Specifying a framing as "scale 0.6"
  slices words in half at the frame edge.
- **Reuse the same window for the same purpose.** If the orient shot is a
  particular window, always use that exact window. Near-identical framings read
  as drift.
- **Vary duration with distance travelled**, not one global preset.
- **Camera and full-frame wipes sequence, never overlap.** Concurrent, they
  guillotine content. Camera first, then wipe.
- **A cover layer goes opaque before the camera moves underneath it.** Reversed,
  part of the move is exposed and reads as a jump cut.
- **No label within 60px of the frame edge.** An element may bleed and read as
  "the world continues"; a word cut mid-glyph reads as a bug. Solve it by
  placement, not by masking, since a feather cannot catch a blade travelling
  ~1800 px/s.
- **Two sequential moves on the same subject read as a glitch.** A reframe that
  finishes and THEN a wipe that starts is a zoom, a dead stop, and a second
  motion — the client calls it "a glitch and a pause". Merge them into ONE
  gesture: shared symmetric ease (power2.inOut), landing on the same frame, so
  the panel reads as pushing the footage aside. Related: front-loaded eases
  (power3/4.out) on a *visible footage* move front-load ~90% of the travel and
  crawl to a stop; reserve them for element entrances, where the crawl reads as
  settling. (Cost a client-flagged revision on the worked example intro.)

### Attention is a spotlight

**Exactly one element at full brightness at any moment. Everything else already
drawn stays quiet but legible.** Not optional. This is the rule that lets a world
accrete to a dozen elements without ever feeling busy, and it is what makes the
pull-back readable rather than overwhelming.

Hierarchy comes from the RATIO between active and quiet, never from making
everything dark. The first prototype of the reference build had a brightest pixel
of 101/255 and was unreadable at 960x540; the fix was brighter ink, not more dim.

| State | Target luma (Y, 16-235) | Opacity in the reference |
| --- | ---: | ---: |
| Active stroke + label | 200-235 | 1.0 |
| Context, drawn and still relevant | 120-150 | 0.56 |
| Spent, said its piece | 85-105 | 0.33 |
| Any label, any state | never below 90 | |

Implementation is one function, called at every narration beat with the ids being
talked about (`build_s01.py`, `lit()`):

```python
def lit(t, active, warm=(), dur=0.5, floor=FLOOR):
    active = list(active) + [g + "-l" for g in active if g + "-l" in order]
    for gid in order:
        if gid not in opac:      # never drawn: nothing to light
            continue
        tgt = 1.0 if gid in active else (WARM if gid in warm else floor)
        if gid not in active:
            tgt = min(tgt, MUTED.get(gid, 1.0))
        ...
```

Three details in there are load-bearing:

- **A label always inherits its element's state** (the `-l` suffix fold-in). A lit
  element with an unreadable label under it is the exact defect being fixed.
- **A prop that is finished retires to opacity 0**, via a `MUTED` cap, not to 0.3.
  Muting to 0.3 leaves unexplained confetti on screen for the rest of the section.
  Generator rule: emit the `mute()` **before** any later-starting `lit()`, or the
  mute is overwritten when its tween completes.
- **Opacity events must be emitted in timeline order** or the tracker sees stale
  state and computes the wrong target. Keep a `seq()` guard that raises on
  out-of-order emission.
- **One opacity authority per element per window.** Two simultaneously-active
  tweens driving the same element's opacity to different values render smoothly
  in a standalone section but strobe at ~10Hz in the assembled master, where the
  winning tween alternates per frame. The reference build shipped this defect at
  every dock. When a sweep like `lit()` overlaps an explicit brighten or mute,
  the later-starting tween is the sole driver and the sweep skips those ids
  (`lit(..., skip=(...))`). Gate it: scan assembled renders for one-frame
  out-and-back luminance pops in every transition window
  (`qa/v4/flicker/qa-flicker.mjs` in the reference build).

### Open loops are spatial

Never say "we'll come back to this." Leave something visibly incomplete in the
world and return to it. A promise the viewer can see is a promise they can feel
outstanding.

The mechanic is identical whatever the shape:

1. **Plant it in the hook**, in the space, on the line that makes the promise.
2. **Re-show it at every boundary.** Any section handoff is a boundary. The
   re-show costs about two seconds and is the retention mechanic; skipping it is
   how a payoff ends up paying off nothing.
3. **Advance it visibly.** The viewer must see the incompleteness shrink.
4. **Close on the image you opened on.**

Pick the shape from the script:

| Script shape | The world | What is incomplete |
| --- | --- | --- |
| N parallel items | N sockets on a spine | empty slots (see `reference/patterns/wall-of-slots/`) |
| One process, deep | the full pipeline, laid out | a broken or missing link |
| Levels or tiers | a stack that builds upward | the top of the stack is a ghost |
| Comparison | two columns on one shared axis | one column empty, or an unfilled scorecard |
| News or announcement | a timeline, or a landscape map | the right side, the future, is blank |
| Tutorial or build-along | the finished architecture, ghosted | every node not yet built |

Handing an item to its slot is a live camera move, ~1.4s, never a cut to a
pre-made picture of the filled state. The viewer watches the thing they just
learned become the tile. If the video has a numeral or counter, roll it inside
that same move, as an odometer, with the same start, duration and ease for both
digits or they merge into one band mid-roll.

**The counter needs a name, not just a number.** A corner numeral tells the
viewer where they are in the sequence but not what the current item *is*; nine
minutes in, "03" carries nothing. Pair the numeral with a 1-2 word label naming
the current item (SUPPORT, VOICE AI), in the same plate chemistry, moving as one
rigid fixture with the numeral, swapping inside the same odometer roll. Client
review of the reference build asked for exactly this: the visuals were good and
the viewer still lost track of which use case was on screen.

## 2 · Discipline

### If it doesn't get a word, it doesn't get drawn

Every shape is a labelled element, a connector between labelled elements, the
travelling subject, or the ambient ground. Nothing else.

This came from a mute-test review that scored comprehension 7/10 and named the
cause: the diagram was clean, the decorations were not. A dozen unlabeled shapes
drawn in the same weight and palette as the meaningful ones, so a first-time
viewer cannot tell signal from texture and spends real attention decoding things
that were never meant to be decoded. That is "too much going on" relocated from
words into shapes.

Budget: **~20 on-screen words per section.** No sentences. Labels are 1-2 words,
under their element. The reference section 1 is 21 words in 84 seconds.

**Corollary: an anti-pattern visual never overlays the recommendation.** Take the
world to near-black first, or put the counter-example where the good diagram
isn't.

### Give the viewer one thing to follow

Carry the story on a single travelling subject whose state visibly changes: a
chip with data rows and a score bar, a document, a request. Rows fill, a bar
moves, a border changes colour. A viewer must be able to follow an entire section
by watching that one object, and it must never teleport; it moves along drawn
connectors at a constant speed.

### One global token set

Full detail in `reference/design-system.md`.

| Token | Values |
| --- | --- |
| Stroke | 1.5 / 2.5 / 4 / 7, and nothing else |
| Type | 22 / 30 / 42 / 60 / 84 |
| Radius | 10 / 22 / 40, always superellipse(2) |

Five colours, five fixed meanings, zero decoration. Warm means a human is
involved and nothing else is ever warm. Never pure white for type; it halates on
dark.

The failure this prevents, from the craft review of the first build: *"every
decision was made locally and correctly; no decision was made globally."* 18
stroke weights and 9 type sizes, most of them 0.2 apart, individually invisible
and collectively fatal. The eye gets noise instead of hierarchy. Gate it with a
token linter that fails the build.

### Motion

Entrances on `cubic-bezier(0.16,1,0.3,1)`, exits faster than entrances, duration
varies with mass so a 290px node and a 40px label do not decelerate identically,
and `back.out` **exactly once per section**, on the beat that deserves it.

**No cross-fade, ever.** Full-bleed layers enter and exit by clip on an already
opaque background. At any instant a pixel is either graphic or footage.

## 3 · Build contract

- **One generator per section.** `scripts/build_<id>.py` writes only
  `compositions/<id>.html`. Edit the generator, never the generated HTML. Section
  roots `index-*.html` are hand-maintained, so framing changes go there.
- **Shared modules stay shared.** Anything that defines shared geometry is
  imported by every section. If sections are built by parallel agents, forbid them
  from touching shared modules; divergent geometry silently breaks every handoff.
- **Namespace the SVG defs before assembly.** Each section defines its own
  `gEdge`, `shadow`, `edgeFade`. In one assembled DOM `url(#id)` resolves to the
  first match in document order, so once an earlier composition unmounts, every
  later graphic paints **nothing**. Cost in the reference build: 35 seconds of
  empty screen with every gate green. Only looking at the assembled render caught
  it.
- **Time everything to word starts** from a word-level transcript, entering
  0.15-0.25s **ahead** of the anchor word. Never divide a section evenly into
  beats.
- **Audit gaps.** Any stretch over ~1.5s with nothing happening is a dead screen;
  have the generator print them.
- **Leave air in the cut.** Aggressive pause-capping produces near-zero gaps at
  sentence boundaries that the client hears as "stutters" and jump-cuts.
  Calibrate against the speaker's own norm: flag sentence-boundary gaps that are
  ~10x tighter than their median (the reference speaker's was 470ms; the flagged
  junctions sat at 20-40ms), and repair by inserting 4-8 frames of air, words
  never touched. Air is a donor slice of the track's real room tone with 10ms
  fades, never `anullsrc`: digital silence against a -50dBFS floor is an audible
  dropout. Video holds the frame; between sentences a talking head is near-still
  and 4-8 frames of hold is invisible. Insertion-only changes shift the
  transcript deterministically, so no re-transcription is needed. **An insert's
  edges must respect the speech envelope**: butting donor tone against a word
  tail in 1ms amputates a decay that naturally takes 60-120ms, and the client
  hears the cliff as a stutter. Splice with a 40ms equal-power crossfade into
  the tail's own decay, never a hard butt.
- **Baked times mean scripted shifts.** Generators bake hundreds of proto-time
  literals, and section offsets, seam tables, and root tweens all hold absolute
  times. Any timeline change after graphics exist (even a 2s air pass) must go
  through a reviewed AST/parse-level transform that shifts every literal after
  each edit point, then a diff review, never hand edits. Derive every shift from
  the canonical edit list itself; the reference pass caught a 2-frame error in
  its own audit's precomputed offsets by re-deriving.
- `--workers 1` on render. Parallel workers make the video layer paint black.

## 4 · Gates

Run all of them, then look anyway.

```bash
node scripts/qa-tokens.mjs          # 0 off-system strokes / type sizes / radii
node scripts/qa-no-crossfade.mjs    # 0 full-bleed layers animating opacity
node scripts/qa-legibility.mjs <render>
node scripts/qa-seamjump.mjs <render> plan/cover-seams.json --control <cut>
node scripts/qa-deadframe.mjs <render> --control <cut>
node scripts/qa-presence.mjs <render> --every 1      # speaker on-screen share
node scripts/integrate.mjs --check                   # 0 gaps, 0 stale mounts
npx hyperframes lint
```

**Gates do not replace looking**, and gates that have never failed are not gates.

- **Motion smoothness is verified on contiguous frames, never on beat frames.**
  A single frame per beat proves composition; every motion defect — a jump into
  a move, a crawl to a dead stop before a second move, a freeze, a one-frame
  pop — lives *between* beat frames and survives every other gate. Before any
  delivery, tile a contiguous strip across EVERY transition window (camera
  move, wipe, reframe, dock, section seam) and read the strips:

  ```bash
  ffmpeg -i render.mp4 -vf "select='between(n,A,B)',scale=480:270,tile=layout=6x7" \
    -frames:v 1 tile-<window>.png
  ```

  Defect signatures to read for: adjacent tiles with a large jump then several
  near-identical tiles (front-loaded ease / dead stop); motion that halts and
  a *different* motion that then begins (two moves that should be one gesture);
  any single tile unlike both neighbours (pop). The worked example intro
  shipped a zoom-freeze glitch that passed tokens, cross-fade, legibility,
  dead-gap and per-beat frame reads; the client caught it in one viewing. This
  class recurs — treat this strip-read as load-bearing, not optional.
- **Legibility is not automatable.** Absolute pixel-share thresholds measure text
  volume, not legibility; a wordy build scores *higher* than a sparse one. Read a
  960x540 downscale of every major beat by eye.
- **Validate every gate against a control** known to trip it. A seam gate that
  reports zero on a broken build is worse than no gate.
- **Verify the assembled artifact**, never section prototypes. Most of the bugs
  that survived this build's gates existed only in the assembly.
- **Audit audio at the acoustic level, not the transcript level.** A transcript
  derived from the pre-edit source is structurally blind to artifacts the edit
  created, and a text sweep over it will report "clean" while the client hears
  stutters. What actually finds them, in yield order from the reference build:
  a whole-track dead-span scan (runs of digital-zero samples inside pauses whose
  real floor is ~-70dBFS read as dead holes; fill with room tone), 1ms-resolution
  envelope forensics at every junction edge (a sample-derivative click check
  passes an envelope cliff that the ear flags instantly), and a fresh ASR pass
  on the delivered audio diffed against the expected text. Phoneme-repeat
  autocorrelation found nothing: what clients call "stutters" are usually
  truncation cliffs and dead holes, not doubled words.

Presence: aim for ~40% speaker-on-screen across a graphics-led video. Long
absences are fine at payoff beats that need full width; audit them rather than
capping them.

## 5 · Order of work

1. Lock the cut and get a word-level transcript. Everything is timed to it.
2. Choose the world, the spatial grammar, and the travelling subject. Write them
   down before building.
3. Choose the open loop from the script shape and build its shared module first.
   Its geometry is referenced by the hook, every boundary, and the payoff.
4. Build **one** section end to end and render it. Prove the system there before
   touching the others.
5. Review that section by eye, muted, for ornament and legibility. Fix the
   system, not the section.
6. Build the rest against the proven section. Then namespace, assemble, render,
   gate, and read the assembled render.

Steps 4 and 5 are where the quality comes from. The reference build's entire
visual system is the output of reviewing its first section three times.
