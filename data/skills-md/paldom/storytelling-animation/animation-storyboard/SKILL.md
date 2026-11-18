---
name: animation-storyboard
description: Turns a brief or message into a validated storyboard.json for a silent-autoplay vector explainer - hook, beats, on-screen text cards, frame timing with reading holds, transitions, CTA, length budget. Use when the user asks to storyboard, script, outline or plan the beats of a short animation or LinkedIn video, or to validate or repair a storyboard.json. Not for screen-recorded walkthroughs.
license: MIT
---

# animation-storyboard

Turns a brief into `storyboard.json`, the timing contract every later step reads.
It fixes the failure where an agent writes paragraph-length "captions", packs three
ideas into one scene, and produces beats too short to read on a muted phone feed.
No engine, no code: the output is a JSON file that passes the bundled validator.

## When to use / when NOT to use

Use when the user wants the story, script, beats, scene list, or timing for a short
animation (LinkedIn post, slide intro, product story), or wants an existing
storyboard.json fixed or validated.

Do NOT use for: laying out or drawing scenes (`vector-scene-layout`), animating
(`smooth-motion-choreography`), rendering (`animation-export-presets`), reviewing a
render (`animation-frame-qa`), narrated or voice-over videos (this contract has no
audio track), or storyboarding a screen-recorded product walkthrough.

## Workflow

1. **Read the brief; ask only what is missing.** The checklist is in
   `references/story-rules.md` (belief/action after watching, where it is watched,
   length, verbatim sentences, brand tokens, loop or once, CTA). Default target:
   `linkedin-4x5` at 30 fps unless told otherwise.
2. **Write the governing idea** in one sentence. Then choose the arc:
   problem → shift → outcome → CTA for explainers; a single card plus one motion for
   loops. Pick the beat count from the length table in the reference.
3. **Draft beats.** For each beat write `text` (≤ 8 words, a headline, not a subtitle),
   `visual` (what the storyboard still shows), `motion` (intent only), and the
   handoff `transition` into the next beat. Give every text card
   `duration_s ≥ 0.7 + overlaps + max(1.33, 0.35 × words, chars / 20)` (an 8-word card
   needs 3.5 s before overlaps). The hook carries text; the CTA beat holds still. Schema: `references/storyboard-schema.md`;
   full example: `assets/storyboard.example.json`.
4. **Validate** and fix until it exits 0:
   ```bash
   python3 "${CLAUDE_SKILL_DIR}/scripts/validate_storyboard.py" storyboard.json
   ```
   Fix rushed beats by cutting words or moving seconds between beats before
   lengthening the video; warnings about the recommended length are real trade-offs,
   say which way you resolved them.
5. **Hand off.** Print the validator summary (total frames, per-beat start and hold
   frames) and the file path. Downstream steps must use the same per-beat frame
   rounding (`timeline.ts` in the layout skill does); the summary is the schedule of
   record. Next: `vector-scene-layout`.

## Output spec

- `storyboard.json` (contract v1) that passes `validate_storyboard.py` with 0 errors.
- The one-sentence governing idea and any brief facts you assumed, stated in the reply.
- Total duration inside the target budget, or an explicit note on why it is longer.

## Gotchas

- Autoplay is muted on LinkedIn and 92% of mobile viewers watch without sound: text
  is the narration. A beat without text must still make sense as a still image.
- Reading speed is the clock (BBC: 0.33–0.375 s per word; Netflix 20 characters/s;
  DCMP minimum 40 frames). An 8-word card needs 2.8 s of stillness, so a 3.5 s beat
  with no overlaps; every overlap eats into that.
- Overlapping transitions subtract from the total: two 4 s beats with a 0.5 s fade
  play for 7.5 s. The validator does this arithmetic; do not hand-sum durations.
- One metaphor per video. If the visuals switch metaphor at the "shift" beat, the
  storyboard is two videos.
- Loops: the last beat hands off to the first (fade or matching pose, never a cut),
  and the wrap overlap costs readable time on the hook too.
- Blog posts and decks are not storyboards: reduce to one idea and 4–8 beats, and
  list what was dropped instead of transcribing.
- Durations are quantised to whole frames per beat (nearest, halves up) and the
  schedule is summed in frames; 0.1 s steps are exact at 30 fps, 0.25 s steps are not
  (7.5 frames), so the validator warns and the summary is the truth.

## Pointers

- `scripts/validate_storyboard.py` — the contract; `--json` prints the summary for
  downstream tools, `--self-test` proves the rules.
- `references/storyboard-schema.md` — fields, timing math, minimal example.
- `references/story-rules.md` — arcs, platform facts with sources, reading-speed
  policy, beat counts by length, brief checklist.
- `assets/storyboard.example.json` — a validated 546-frame (18.2 s), five-beat example.
