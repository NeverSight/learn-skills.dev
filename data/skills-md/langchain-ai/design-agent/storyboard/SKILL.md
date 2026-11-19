---
name: storyboard
description: Plan a new film or animation before it is built, from the argument to a beat sheet, a handoff sheet and on-brand pose frames on one contact sheet for sign-off. Not for revisions to an approved or delivered video.
---

# Storyboard

The cheap gate before motion. A note here costs minutes; after production it costs an hour. The
poses are real artefacts (real tokens, real copy, the real logo), so nothing is rebuilt from a
description later.

A revision to an approved or delivered video (a word, a colour, a re-time) does not reopen the
storyboard: edit the composition, re-render, run `video-gate`, look at the changed frames, deliver.

**The unit is a change, not a slide.** A beat has an intention and an observable result; entrance,
development, read and handoff are its phases. A pose is one of the two or three moments a beat needs,
not the scene.

## 0. Intake

State sensible defaults and proceed; ask only what blocks (at most two questions). The intake heads
`projects/<slug>/storyboard.md`:

- **Core message**: the one thing the viewer leaves with.
- **Audience**: who is watching and what they already know.
- **Claims ledger**: every assertion the film makes, its source, and whether it is verified,
  measured or illustrative. Keep provenance off the frame.
- **Close**: the product name and the ask. Verify any URL or package name before it goes on an end
  card; links belong in the post.
- **Channel, aspect, duration**: 16:9 (1920×1080), 9:16 (1080×1920) or 1:1, from the brand pack's
  formats (`/workspace/brand/brand.toml`). Default 16:9 and 20-30 s. A vertical version is a reflow of
  the layout, never the wide frame cropped.
- **References**: a film the person handed you outranks everything; measure it with `film-breakdown`.
- **Must-includes**: required copy, marks, real product surfaces, things to avoid.

Exact requirements that must survive revisions go in `projects/<slug>/artifact-contract.json`
(`node /workspace/tools/artifact-contract.mjs --contract ... --phase plan`). When supplied artwork must
move, start from [templates/layer-manifest.json](templates/layer-manifest.json): each moving part is
an isolated transparent layer with bounds, anchors and attachments (check it with `--layers`). A flat
image is not animation-ready; ask for the separated layers rather than faking them with guessed crops.

## 1. The argument, then the beats

Write the argument as prose first and read the beats aloud as one sentence: if each is a
self-contained label, you have a deck. Find the turn, the one concrete thing the film pivots on.
Then one row per beat and one row per cut: the fields are in
[references/beats-and-handoffs.md](references/beats-and-handoffs.md). The two fields that carry the
film: **the change** (what develops after the entrance; a beat whose every tween is an entrance is a
slide) and **the carrier** (what crosses each cut; where nothing does, say what the semantic handoff
is). List the attention demands per frame rather than asserting a number: more than two is two beats.

Sound is part of the board when the brief has sound: the music arc and each beat's sound accent,
with a `plan.json` started beside it (`sound`). With voiceover, generate the lines now: the film is cut
to the voiceover, and timing locks at animatic approval. A silent deliverable says `sound: none`.

## 2. Poses, shot from real HTML

Per beat, one self-contained HTML page at the target size, styled from `/workspace/brand/tokens.css`
(`var(--brand-…)`, never a typed hex or family), with real copy where it carries meaning, the real
mark from `/workspace/brand/logos/`, and the real product surface where the beat says "this is the
product". Give the elements the build will animate stable ids (scene-prefixed, `#s3-card`; a carrier
unprefixed, `#carrier-issue`), with explicit `top/left/width/height` and no self-running animation.

How many poses: a static beat needs one; a beat with a change needs two (before and after); a cut with
a carrier needs three (outgoing, midpoint, incoming), and the midpoint matters most: a perfect
endpoint can hide a broken journey.

```bash
node /workspace/tools/html2png.mjs projects/<slug>/board/beat-03a.html --out projects/<slug>/board/poses \
  --name beat-03a --size 1920x1080 --brand-fonts
node /workspace/tools/brand-lint.mjs projects/<slug>/board/beat-03a.html
```

When the scene already exists as a HyperFrames composition, `hyperframes snapshot --at <t1>,<t2>`
shoots the poses from it instead. A look plate for a photographic or illustrated beat can come from
`image-generation` (no text in it; type is set in HTML on top). Emit the poses and later the film from
one generator (`build.mjs` with the beat table, copy and shared CSS), so the delivered composition is
provably the approved artwork and a re-time is one number per beat.

## 3. One contact sheet

```bash
node /workspace/tools/review-thumb.mjs --sheet projects/<slug>/board/poses/*.png \
  --out projects/<slug>/board
```

Look at it yourself first against the craft review in the reference (squint: one or two things per
frame; work, not decoration; a concept, not brand primitives; one accent; a named change per beat;
a carrier or a named handoff per cut). Redesign only the beats that fail.

If someone cannot picture a framing, draw it instead of writing more prose: a skeleton sheet with the
real copy at its intended scale or a labelled placeholder box per cell. Ship one story with the
reasoning visible; three options that share a flaw read as three more misses.

When Paper is connected and people want to nudge the board, draft it there as well (`paper-design`);
the thread still gets the sheet.

## 4. Sign-off, then build

Present the argument, the beat sheet, the handoff sheet and the contact sheet (one `upload_files`),
then wait for a clear go or specific redlines. Someone who already said "storyboard it and build it"
has given the go: present the sheet and keep going.

The build assembles the approved poses rather than re-authoring them (`motion-direction`,
`hyperframes`): namespace each pose's styles to its scene, mount the scenes in one host composition
with the carrier on its own track, then add development, camera and micro-interaction around the
named ids. Then a draft render, a review through every cut, `video-gate` at zero errors, the final
render once the look is confirmed, and the score (`sound`).
