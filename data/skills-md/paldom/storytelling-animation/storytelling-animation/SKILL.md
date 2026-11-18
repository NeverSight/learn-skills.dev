---
name: storytelling-animation
description: Produces a finished vector storytelling animation video from a brief, end to end - storyboard, licensed assets, phone-legible layout, smooth Remotion motion, LinkedIn, PowerPoint or custom-size exports, frame QA, one gate per step. Use when the user asks to make, create or produce an animated explainer, story video or LinkedIn animation from a brief. Not for one step, narration or screencasts.
license: MIT
---

# storytelling-animation

Drives the whole pipeline from a written brief to delivered files by running the six
sibling skills in order and refusing to move on until each gate passes. It fixes the
failure where an agent jumps straight to Remotion code, guesses timing, sizes and
encoding, and declares a video done without ever looking at a frame.

## When to use / when NOT to use

Use when someone wants the animation made: "make an animated explainer from this",
"produce the LinkedIn video for this launch", "build the looping intro for the deck",
including re-runs after a brief change.

Do NOT use when the request is one step (only the storyboard, only an export, only
a review): route to that sibling directly. Not for screen-recorded walkthroughs,
narrated or AI-generated talking-head video, decks, or editing footage.

## Workflow

Read `references/pipeline.md` once (gates, files, change propagation). Then:

1. **Storyboard** with `animation-storyboard`: brief → `storyboard.json`; gate:
   its validator exits 0. Confirm targets, length, loop and any verbatim sentences.
2. **Assets** with `vector-asset-sourcing`: icons, illustrations, fonts → `public/`,
   `assets/manifest.json`, `ATTRIBUTION.md`; gate: its checker exits 0.
3. **Layout** with `vector-scene-layout`: scaffold (record the Remotion license basis
   in `animation.config.json`), tokens, one static scene per beat; gate: per-beat
   stills rendered for every target and looked at, at phone width.
4. **Motion** with `smooth-motion-choreography`: animate from the frame, transitions,
   loop wrap; gate: its linter exits 0 and the transition and seam strips look right.
5. **Export** with `animation-export-presets`: masters and deliverables per target;
   gate: its checker exits 0 per file.
6. **QA** with `animation-frame-qa`: artefacts per deliverable in `out/qa-<target>/`;
   gate: every check recorded `pass` (`qa_frames.py --record` after looking). Route any
   defect back to the owning step (table in the pipeline reference) and re-run every
   gate downstream of the fix.

At any point, or when resuming a session:
```bash
python3 "${CLAUDE_SKILL_DIR}/scripts/pipeline_status.py" --project .
```
prints each gate's state from the files on disk (re-running the sibling validators,
checking freshness against the storyboard and scenes) and the next step to take. A
gate whose validator is not installed stays open.

## Output spec

- `out/<preset>.mp4|gif` for every target, each with a passing `check_output.py`
  and a `qa-<preset>/report.json` with no failed check.
- A delivery summary: file per destination, handling notes (PowerPoint: Start
  Automatically, Loop until Stopped, no Compress Media; LinkedIn: MP4 upload, credit
  line in the post if `ATTRIBUTION.md` has one), the license basis, and the manual
  steps left (test upload, presenter machine).
- The storyboard's governing idea and anything from the brief that was dropped or
  changed, stated plainly.

## Gotchas

- The gates are the point. Skipping a still or a strip to save time is how unreadable
  phone text and broken seams ship.
- Fix upstream, re-run downstream. A timing change is a storyboard edit; a legibility
  problem is a layout edit; a seam is a motion edit; never a re-encode.
- One storyboard file: `timeline.ts` imports `storyboard.json` from the project root;
  do not keep a second copy elsewhere.
- Remotion's free tier covers individuals, companies of ≤ 3 people and non-profits;
  larger organisations need a Company License before step 5 runs.
- Silent by design: on-screen text is the narration; there is no audio track unless
  the brief adds one, and the storyboard contract has no captions field.
- Targets multiply work: each aspect ratio gets its own stills, strips and QA.
- Say "not done" when it is not done: list the open gate and what it needs.

## Pointers

- `references/pipeline.md` — gates, project layout, change propagation, preconditions.
- `scripts/pipeline_status.py` — gate state from disk; `--self-test`.
- Sibling skills: `animation-storyboard`, `vector-asset-sourcing`, `vector-scene-layout`,
  `smooth-motion-choreography`, `animation-export-presets`, `animation-frame-qa`.
