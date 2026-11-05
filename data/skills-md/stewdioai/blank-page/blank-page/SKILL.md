---
name: blank-page
description: "Turn a one-line motion / animation / design brief into the full prompt: a committed look grounded in five reference images, three motion references, numbered beats with a turn, and the refs and assets attached. Also tightens edit notes. Use for \"/blank-page\", \"expand this prompt\", \"make this prompt more specific\", \"what is missing from this prompt\", \"help me write the prompt for X\", or whenever a one-line animation / composition / design brief is about to be handed to an agent."
---

# Blank page

Turn a short draft into the brief its author would have written. The drafts are usually
Stewdio composition work (motion, 3D, shaders, footage); the method applies to any
generative brief.

**A good brief is references plus beats.** The idea lives in the thing pointed at
(`recreate this <mp4>`, `in the texture of embroidery <img>`) and the beats say what
turns into what: a committed look, a copied move, a real thing, and a turn. Not more
words, not more numbers. The voice is lowercase, imperative, numbered, no filler. A new
brief stays under ~150 words counted above `refs:`, an edit note under ~50; over the
cap, drop the optional lines (realism, params, a frame line restating a default) before
tightening, never a beat or the turn.

Files in `references/`:

- `finding-references.md`: roles, the fence, are.na seeds and loop, Pinterest,
  Sketchfab, vetting. Read before step 2.
- `vocabulary.md`: the author's own words, per slot. Borrow while writing.
- `examples.md`: before / after pairs from real sessions. Read when unsure of the shape.
- `patterns.md`: corpus evidence and past failures behind the rules. Optional.

## Procedure

1. **Classify the draft.**

   | mode | signal | output shape |
   |---|---|---|
   | brief | "create", "recreate", a new comp or scene | aesthetic line + numbered beats + frame line + refs + assets |
   | batch | "create N comps", "variations", "fill the gaps" | brief + per-item one-liners + dedupe rule + shared constraints |
   | delta | "make X more/less Y", "get rid of", "fix", "move to" | target + change + magnitude + direction + keep-clause |
   | image feedback | a screenshot / contact sheet is attached | one line per observation, each naming its frame or time |
   | sequence | "at Ns", "after the X exits", beats across time | brief with a time anchor on every beat, duration cap |
   | housekeeping | rename, push, export, "check the render" | leave as is; add the exact format or target |

   Brief, batch and sequence go through steps 2-8. Delta and image feedback skip to
   step 6, searching only when the change brings in a new look or move.

2. **Ground the look: five images, before any beat.** One aesthetic, sheeted, and
   five stills from it that each do a job: the overall look, palette, material or
   surface, composition, a detail or motif. Never blend two aesthetics; if a second
   keeps winning tiles, switch to it wholesale. Its name goes in the prompt's first
   line.
   - **No fence** (the draft says nothing about the look): browse his umbrellas and
     CARI's named aesthetics and pick for remarkable, not for matching the draft's
     words.
   - **A fence** (the draft names a style, a brand or a medium, or attaches a
     reference): the word is the are.na query and the pick is the best instance
     inside it, never a different aesthetic and never a screenshot of it. It fences
     palette, material, type and components, not layout, scale, camera or the move.
     The first line names a child of the user's word (`in stripe-gradient dark`).
     How to decode and query it, and what to do when the queries come back as junk:
     "The fence" in `finding-references.md`.

3. **Ground the motion: three moving references.** gif / mp4 from the motion channels,
   each a move worth copying ("would he put this in mo-graph?"), covering three jobs:
   the main mechanic, the turn, the exit or camera. If no exit or camera move passes
   after three channels, m3 takes another beat and the camera is written in words.
   **The fence never applies to motion.** Then, as the beats need them: a copy
   reference or asset for anything recognisable (a real UI, product, artwork, a
   Sketchfab model) and a ui reference for interfaces. A user attachment fills its
   slot. Look at every candidate before it gets a role.

4. **Decide each reference's use, then write the beats.** For all eight: which beat
   it feeds and exactly what is taken (`a3's wet-stone texture is the canvas surface`,
   `m1 0.0-1.6s is beat 1 at 1.5x slower, subject swapped for cards`). A reference
   with no beat is cut. The motion refs give the beats their order and timing; each
   image sits on the beat where its quality first shows. Include **the turn**: a beat
   where something is revealed, changes medium, zooms out to a larger whole, or
   becomes something else (`the painting unravels into a single thread which becomes
   a running silhouette`). Enter, animate, hold is not finished. When the draft
   already holds a transformation (`snaps into`, `comes back as`), that verb is the
   turn: make it the biggest beat and add no second metaphor. A ≤5 s clip carries one
   idea (extra ideas go into the material and the camera, not the plot) and the action
   fills it: end hold under 1 s; a turn over by 1.6 s means compressed beats or a
   missing second half.

5. **Add ideas.** On a bare draft, expected: a prop that makes the subject specific, a
   real asset, a camera move tied to a reveal, a second beat that answers the first.
   Write them as beats; mark the one or two real forks `[? ...]`.

6. **Fill the slots** (checklist below). Inferable from the file, the previous comp,
   an attachment or the conversation: silently. Missing and creative: a
   `[? best default]` placeholder in the prompt. Missing and routine (duration,
   aspect, file): default it inline, no marker; no file named means
   `in stewdio, new file <topic>,`.

7. **Rewrite in the house shape** (templates below), keeping the author's wording
   where it exists.

8. **Output** three things and nothing else: the prompt in a fenced block; a
   "fill-ins" list (max three creative forks, each with the choice made and the one
   alternative worth considering; never duration, loop or aspect); one line pointing
   at `.context/refs/<topic>/` with the contact sheets so the user can veto a pick.
   `<topic>` is a two- or three-word kebab slug of the subject (`coffee-menu`). If a
   real thing is needed and absent (the user's own app, product, logo), say so in one
   line above the prompt and name the stand-in used. No technique, no advice.

## Slot checklist

Opener slots first; they decide the result. Edit-loop slots after.

| slot | ask | house form |
|---|---|---|
| where | tool, file, comp; for sequences the time or beat it attaches to | `in stewdio, <file>, <comp>, at 3.5s:` / `after the sticker exits:` |
| look | one aesthetic, named, from a1; a child of the user's word when there is one | `in frutiger aero style` / `everything in riso` |
| medium / technique | photo or footage, 3D rebuild, vector, shader, real model | `using threejs or 3d framework` / `real 3d texture and train models` |
| move | the mechanic from the motion ref, subject swapped | `recreate this animation, but make it nyc subway` |
| subject | the real thing, by name, with its source | `the famous ukiyo-e painting <img>` |
| beats | numbered; each = subject + action + what it reveals or becomes | `2. then at around 2s, a big wave splats across the screen, turning the entire screen into a new texture` |
| turn | the reveal / morph / zoom-out / medium switch | `the camera zooms out to reveal that ...` |
| realism | fidelity demand when it matters | `it should be very realistic` / `loyal to the og` |
| camera | move + easing + what it lands on | `camera zooms fast into the pupil, steep quadratic ease-in` / `camera stays still` |
| pace | the feel in his words, seconds only for anchors | `very snappy, ease-in-out` / `one continuous motion from the start` |
| frame | bg, aspect, duration, loop, only where it differs from the defaults | `white bg, 1:1, ~5s loop` |
| params | values to expose when the comp will be tuned | `expose params for plumpness, sheen, glow` |
| keep | edits: what must not change | `keep the old entrance speed` / `keep the rest the same` |
| magnitude + direction | edits: multiplier, phase, axis and sense | `2x faster at top speed` / `30 degree clockwise` |
| scope | edits: which comps the change touches | `only for 23` / `unrelated: also ...` |

**Standing defaults**, never written out: white bg (black for the math-graph family);
no fade, drop shadow, rounded corners, annotation text, UI chrome or guiding lines; 1:1
for social posts, 16:9 for the graph and carousel families; ~5 s for a loop, 3-4 s for
an inserted beat, under 15-20 s for a sequence; real assets for recognisable objects,
stylised on top. The look outranks them: an aesthetic with its own ground (paper
stock, a counter, dark-mode navy) replaces the white bg on the frame line, and light
that belongs to the look (raking light across paper) is not a drop shadow.

## Templates

**Brief**

```
in stewdio, <file>, [<comp>,] [at <N>s / after <beat>,] create the following, in <aesthetic from a1>[, using <technique>]:

1. <subject (c1 / asset), its state at 0s> <enters like m1: mechanic>
2. <main action from m1, subject swapped> [at ~<N>s]
3. <the turn: reveals / turns into / zooms out to show ...>
4. <exit or end state>

<realism demand if it matters>; <camera if it moves>; <pace in his words>
<frame only where it differs from the defaults>; the whole thing ~<N>s
[expose params for <list>]

refs:
- a1 <path>: look, <what it sets: overall look, framing of beat 1> (<url>, channel <slug>)
- a2 <path>: palette, <used where> (<url>, channel <slug>)
- a3 <path>: material, <which surface in which beat> (<url>, channel <slug>)
- a4 <path>: composition, <which beat's frame> (<url>, channel <slug>)
- a5 <path>: detail, <which element, which beat> (<url>, channel <slug>)
- m1 <path>: motion, beat <n>: <mechanic, time range taken, scale factor>, subject swapped, not the look (<url>, channel <slug>)
- m2 <path>: motion, beat <n>[ (the turn)]: <what is taken> (<url>, channel <slug>)
- m3 <path>: motion, beat <n>[ (the turn)]: <what is taken> (<url>, channel <slug>)
- u1 <path>: ui, <ui type> layout + components, brand-neutral (<url>, channel <slug>)
- c1 <path>: copy, <subject>, one-to-one (<url>)
assets:
- <path or url>: use as-is for <what>
- <sketchfab page> (<author>, <licence>, <faces>): <object>, one-to-one, <parts that must move> [? download]
```

Beats cite handles inline (`2. the sticker peels from the lower-left corner like m1,
on a3's wet stone`); every handle in `refs:` appears in a beat. Motion handles are
numbered in beat order, and the one feeding the turn is marked `(the turn)`. Add `orig <url>` after
the channel when the block has a source. User attachments go in the same list.

**Batch**

```
in <file>, create <N> <things>, <one-line shared description>, using <channel> as reference:

1. <item: mechanic + orientation + layout>
2. ...

for all of them: <shared constraints>; keep each ~<N>s
no overlap with <existing set>; a valid variation changes the mechanic, orientation, layout or treatment, not just direction or mirror
name them "<Prefix>: [<k> word description]"
```

**Delta**: one change per line, numbered when several, each naming its target;
"unrelated:" marks a different comp.

```
[for <comp>,] make <element> <change> <magnitude> [<direction with axis>] [at <N>s]
[get rid of <element>]
keep <what must stay>
```

**Image feedback**: `<frame or time it points at>: <one observation, quantified>`, one
line each.

## Rules

- **Pick for quality, not for match.** The most striking move or look that could
  carry the subject beats a keyword hit that shows the right object.
- **A film frame, not a web page.** One hero element takes ≥40% of the frame height at
  the beat it matters; the smallest text is ≥24 px at 1080p; nothing is rebuilt at 1:1
  browser scale. Judge sheets at thumbnail size.
- **One reference, one job.** Moving media for motion, stills for look; a motion ref
  implies a subject swap. A file used for two roles is listed twice, each scoped.
- **Assets are used, references are read.** Real footage, a real GLB, the real UI, the
  real painting, stylised on top; say the fidelity up front and never re-interpret an
  uploaded asset. Procedural only for primitives, orbs, blobs, extrusions, noise fields
  and things that must grow or morph.
- **Treat each thing as a contraption.** Animate its special mechanism (a lid closes,
  an envelope seals, a checkbox ticks), not a default draw-in. Transformations are
  in-process morphs, not a teardown and rebuild.
- **Describe the mechanism, not the adjective.** "editorial page-drag" was built as a
  slide-in; "the current image is peeled from a corner to reveal the new one already
  underneath" was built right the first time.
- **Numbers where he uses them.** Seconds for anchors and length, multipliers and
  degrees in edits, a hex only when the colour is the point (klein blue #002FA7). No
  ms staggers or px offsets in an opener.
- **Edits name an axis, a sense and a phase.** "the other way" is not a direction;
  "entrance 5x faster" needs "the fastest entrance we have had, constant speed after".
- **Keep the voice.** "get rid of", "tho", "~5s", "plz" are fine. No greetings,
  rationale or headings inside the prompt.

## Scripts

`scripts/find_refs.py`: are.na channels / umbrellas / contact sheets, Pinterest pins,
Sketchfab search + download, file downloads, video contact sheets. Run it with no
arguments for the command list.
