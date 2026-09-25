---
name: anidoodle
description: Code-drawn illustrations, animations and scored films in nine hand-drawn styles, zero assets, identical every render. Use for hero art, explainers, stickers, loops, animated logos, storyboards or a short film.
metadata:
  created_by: Alex Greenshpun (10x Company)
  license: Apache-2.0
---

# anidoodle

Pictures, loops and films drawn entirely in code. One pure function, `renderFrame(film, ctx,
frame, env)`, paints every frame; a second pure function writes every audio sample. A still is
that function called once. Nothing downloaded, nothing sampled, nothing random, so the source
rebuilds the same pixels on any machine, at any size, for as long as the file exists.

The engine is the easy half. Pieces get thrown away because they had no point, because the
subject looked like a road-sign icon of itself, because the style was a palette swap, because the
music sounded like a ghost crying, or because the client's patience went on approving fragments.
This skill carries the craft that prevents each of those.

## What are you making?

| Making | Scaffold | Workflow | Read |
|---|---|---|---|
| A still: hero art, spot, cover, social card, diagram, a series | `--still <name>` | **Still**, below | `styles.md`, `formats.md` |
| Motion without a story: loop, sticker, animated logo, ambient header | `--film <name>` | **Loop**, below | `formats.md`, `styles.md` |
| A film: 30 to 90 s, a transformation, a score | `--film <name>` | **Film**, below | all of `references/` |

Ask for the size, the style (or pick one from `references/styles.md` and say why) and where it
will live, if the request leaves them open. Everything else has a default.

## The seven laws

1. **Every piece has a point.** A still: one idea, one focal subject, one light. A film: one
   transformation, one payoff, one visual token that returns. → `references/storytelling.md`
2. **State the realism.** "A butterfly" gets you the road-sign icon of a butterfly. Name the
   anatomy, the view, and the reference you opened. → `references/realism-and-craft.md`
3. **A style is a way of making marks.** Change the medium, the edge and the order of the marks,
   beyond the palette. → `references/styles.md`
4. **Prove the look on ONE still, then build end to end.** One still buys the look. After that,
   gates cost more than they save. → `references/working-method.md`
5. **The contract is absolute.** Pure in `(frame, env)`, `rng(seed)` only, no clock, no
   `ctx.filter`, no assets. Texture is geometry and seeded tiles. → `references/determinism-and-contract.md`
6. **Music gets a recipe, never an adjective.** Major key, plucked, I-IV-V-I, no pads, no drones,
   no long reverb. You cannot hear your output, so you do not improvise. → `references/music-recipe.md`
7. **One directs, one builds, both write everything down.** When a session degrades, reset it;
   the files are the memory. → `references/working-method.md`

## Workflows

**Still.** (1) Say the idea in one sentence and name the focal subject and the light. (2) Open
real reference for anything that exists, and note which. (3) Pick the style and read its plate's
module first. (4) Draw: cast shadow, form, line, paper, in that medium's order. (5) Render with
`still.mjs` at full size, critique it in writing against the craft bar. ✋ **One approval.**
(6) Deliver at every size asked for from the same source, and say `reproducible` was printed.

**Loop.** As a still, plus: every motion is periodic over the loop (whole cycles only), the
subject never stops, something moves in every second. Check the seam (last frame against frame
0). Export GIF, WebM or APNG per `references/formats.md`. ✋ **One approval, on the moving file.**

**Film.**
1. **Write the story in three sentences** (setup, transformation, payoff) and name the token. If
   you cannot, stop. Do not open an editor.
2. **Put it on the grid.** 120 bpm at 30 fps is a 15-frame beat. Cuts on multiples of 15, events on
   multiples of 5. ONE cue table per film holds every frame number, and a checker runs at load.
3. **Open real reference** for anything that exists in the world, and write down which images.
4. **ONE look still**: the hardest frame, hero subject large, in its world, in the final medium
   and light. Critique it yourself in writing first. ✋ **Approval gate.**
5. **ONE 8-second music sample** from the recipe. ✋ **Approval gate.** The client listens; you can't.
6. **Build the whole film.** No per-shot approvals. Mechanical checks run continuously and need
   nobody: types, grid, contract scan, draw budget, determinism, dead air.
7. **Review the whole film once**, from the rendered file: contact sheet at one tile per beat, each
   cut as a before/after pair, the dead-air numbers. One ranked fix list. One rebuild.
8. **Verify and deliver.** ✋ **Final approval.** Say what you verified and what you cannot: you
   cannot hear it and you cannot watch it move.

Three approval gates at most. Approval is a budget; spend it where being wrong is expensive.

## The craft bar

The test: would a proud human illustrator ship this, or is it mechanical shape-assembly?

| The tell | What passes |
|---|---|
| A subject built from ellipses and capsules | Hand-placed control points over real anatomy |
| One style recoloured to look like another | The mark, the edge and the order of marks all change |
| Flat colour fields | Wash, then pattern wet-on-damp, then line; one named light; cast shadows |
| Every stroke the same weight and speed | Long strokes fast, fiddly ones slow, thick-thin, tapered |
| Even scatter, one flower stamped 200 times | Hand-placed drifts with bare rests; 4-5 authored views per species |
| Gradient sky, disc sun, oval bokeh | Granulating wash, sun as paper left light, lost edges |
| Decoration | Every element has a one-line reason or it is not drawn |
| A row of style vignettes (film) | One arc. The medium changes only when the STORY changes state |
| Things fade or scale in | Marks are MADE, in the order a hand makes them |
| Both sides do the same thing at once | One side leads, by a few frames, never half a cycle |
| A hold | The camera may creep. The subject never stops |

**No dead air** in anything that moves: something visibly changes in every second, from frame 0.
Check it with the tool AND by eye: a creeping camera changes every pixel and satisfies the tool
while the eye sees a still.

## The engine

`engine/` is the portable art core plus the tooling. Nothing in `engine/src/canvas-core` knows
about React, Remotion, the DOM, or any backend; that separation is verified, not asserted.

```bash
node <skill>/engine/tools/scaffold.mjs ~/art --still hero --film intro   # either or both
cd ~/art && npm install && npx playwright-core install chromium
node tools/still.mjs hero --out out/hero.png --scale 2   # a picture, with its reproducibility hash
node tools/render.mjs intro                               # the MP4; --out x.gif | x.webm | x.apng for loops
node tools/gate.mjs intro --mp4 out/intro.mp4            # determinism + contract + dead air
node tools/emit.mjs intro --out out/intro.html           # one self-contained offline player
```

| Tool | What it does |
|---|---|
| `scaffold.mjs` | engine + a starter still and/or film (+ `--example`) into one working project |
| `still.mjs` | one frame, full size, drawn twice, with its hash; needs a browser only |
| `render.mjs` | MP4, GIF, WebM or APNG, then a determinism probe |
| `gate.mjs` | determinism, contract, dead air, any adapter; marks checks a piece has no use for as `----` |
| `emit.mjs` | one offline HTML file that redraws the piece, then verifies the file it wrote |
| `snap.mjs` / `deadair.mjs` | contact sheets; per-frame changed-pixel fraction |
| `verify-frame-adapter.mjs` | holds a page-side seek adapter to its contract |

Four backends, one art core: `playwright`, `html-player`, `remotion`, `hyperframes`. Each is
roughly 100 lines and none is visible from the core. → `references/backends-and-adapters.md`

## Worked examples

- **The nine style plates** in `engine/src/canvas-core/` (`ranunculus`, `koi`, `pocketWatch`,
  `balloon`, `wren`, `moonPhases`, `fox`, `lighthouse`, `mellan`): one still each, the recipe in
  the header. `banner.ts` is an ambient loop; `mellanUnspool.ts` a still that draws itself.
- **MECHANICAL LEPIDOPTERA** in `example/`: 1410 frames, 47 s, a clockwork butterfly that is
  drawn, comes alive, and leaves its blueprint in the grass. Spec: `example/butterfly-film-spec.md`.
  `butterfly/alive/anatomy.ts` is realism as code; `butterfly/surface.ts` is a cache key that
  names everything its pixels depend on. `node <skill>/engine/tools/scaffold.mjs ~/study --example`

**Study them. Do not copy them.** Copying gets you somebody else's picture with your title on
it, and the craft bar is not satisfied by inheritance.

## Honest limits

You cannot hear the score and you cannot watch the film move. Every claim about either must come
from a measurement or from a human. Say which. A green checkmark is a claim, not evidence, until
you re-run it: on the worked film the dead-air gate passed while a second of near-stillness sat
in the cut, and a cache key that was wrong in one frame order survived every eye that read the
code. The machine found that one; no human was ever going to.
