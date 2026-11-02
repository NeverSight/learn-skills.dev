---
name: reference-style
description: "Turn a reference (a frame, a video or an image library) into docs/style_guide.md and a beat-grid shot list: measure cuts, palette and pace, take grammar not content, wait for OK. Use when the user supplies or names a look."
argument-hint: "[frame | video | folder] [subject] [duration]"
effort: high
---

# Reference style (course step 05)

Given no reference, the model drifts to one default look: centered text on a gradient with every element
fading in. Rexan Wong (@rexan_wong) went through a batch of viral clips and found that
naming a style works better than describing one, and that a reference gives the model the pacing,
type and transitions to copy. This skill turns a reference into two approved documents before any
film code exists.

Request arguments (may be empty), shown once:

<request>
$ARGUMENTS
</request>

## The reference ladder

| Rung | What the user gives | What you extract | Tool |
|---|---|---|---|
| A frame | one still of a video they love | palette, type, texture, composition density | `refs.mjs analyze refs/<folder>` + look at it |
| A video | a local file of a film they admire | the above plus cut times, shot lengths, motion energy per second, transitions | `refs.mjs extract` + `analyze` |
| A library | a folder of their own images or past work | a house style nobody else can copy | `refs.mjs analyze refs/<folder>` |

Pleometric's pure-code TikTok piece started from a single frame of another viral animation; his
Donald-style film pointed Opus at his own PC-98 image gallery. Where to find references: launch
videos on whatships.com, motion on Dribbble, and competitors' launch films. Study them; never
embed or redistribute them.

## 1. Get the reference on disk

- Copy the file or folder into `refs/` in the project (scaffold with `/motion-studio:studio-init`
  first if there is no `studio.json`).
- Given only a link to someone else's video, ask the user for a local copy they are allowed to
  study. Do not download third-party media yourself.
- A single frame: put it in its own folder (`refs/frame/`) so `analyze` treats it as an image set.
- Ask what to take and what not to take when the user has an opinion ("the grain and type, not
  the characters").

## 2. Measure it

Run from the project root:

| Reference | Commands |
|---|---|
| video | `node tools/refs.mjs extract refs/<video> --every 0.5` then `node tools/refs.mjs analyze refs/<video>` |
| frame or library | `node tools/refs.mjs analyze refs/<folder>` |
| fast cutter (many cuts missed) | add `--threshold 0.2` to `analyze` |

Outputs: `refs/frames/frame_NNNN.png`, `refs/frames/frames.json`, `refs/contact.png` (labelled
sheet of up to 60 tiles; a tall sheet is paged like every contact sheet: `refs/contact.png` is page 1, then
`refs/contact-2.png`, `contact-3.png` ...; open every page, the `--json` result lists them in `contacts`), and `refs/analysis.json` with cut times, shot lengths (mean, median, range), a 6-color
palette with shares, brightness and contrast, motion energy per second with its peak, and a text
density hint. The printed summary is a starting block for the style guide.

## 3. Write the style guide and the shot list

Brief `motion-studio:style-analyst` (it may write `docs/style_guide.md`, `docs/shotlist.md` and
`refs/**`):

```
Project root: <abs path>. Reference: refs/<file or folder>. Subject: <subject>. Duration: <S> s.
Open refs/contact.png (and refs/contact-2.png ... when it is paged) and a few frames around the cuts, read refs/analysis.json.
Write docs/style_guide.md following the style-guide notes, then docs/shotlist.md for a <S> s film
about <subject> in that style, on the beat grid of audio/beats.json (or <bpm> BPM if absent).
Take the grammar of the reference, never its content, logos, characters or copy.
Return questions instead of guessing.
```

The section-by-section notes are in [assets/style-guide-notes.md](assets/style-guide-notes.md).
For users who want to paste a prompt into a fresh session, the same steps are written as
[assets/reference-prompt.md](assets/reference-prompt.md).

## 4. Take the grammar, never the content

| Take | Never take |
|---|---|
| palette relationships (dark ground, one warm accent, share of accent) | logos, characters, mascots |
| type families by class, weight, tracking, scale jumps | exact compositions or frames |
| shot lengths and where cuts fall against the beat | the reference's copy, claims or data |
| transition types (hard cut, mask wipe, match cut) | its footage, music or voice |
| camera language (push-ins, whip pans, locked-off) | brand-specific shapes or trade dress |
| texture (grain amount, paper, halftone) and how text enters and exits | anything the user did not ask to borrow |

## 5. The gate

Show both files (a compact summary of the style guide and the shot list table is enough) and wait
for the user's OK before any film code. When they reject it, rewrite the shot list (and the style
guide if the look is wrong), never patch code to "show instead". Record the decision on the
`Status:` line at the top of `docs/shotlist.md`.

## 6. Let the model pick the technique

Specify the look and the constraints, not the library. Pleometric suggested p5.js and Opus wrote
its own paper renderer instead. Within this studio that means: describe the texture and motion you
want in the style guide, and let the build choose how to draw it in the canvas engine
(`lib/draw.js` helpers or custom drawing). Name a framework only when the user needs it for reuse
(route B, `/motion-studio:seek-engine`).

Next: build with `/motion-studio:motion-reel` from its stage 5; for a UI state loop in this style,
`/motion-studio:ui-morph-spec`.
