---
name: showreel
description: "The viral one-line 'showreel for a résumé' prompt: why it works (anatomy), the credited quote, and seeded variants that avoid look-alike reels; runs it as an engine test. Use for that prompt, its variations, or a showreel."
argument-hint: "[canonical | seed] [duration] [format]"
allowed-tools: Bash(node "${CLAUDE_SKILL_DIR}/scripts/roll.mjs" *)
effort: xhigh
---

# Showreel (course step 03, level L1)

A one-line prompt produced 15 seconds of camera moves, kinetic type and synced audio for several
creators the week Opus 5.5 shipped. Use it for what it is good at: proving that this machine's
studio renders, critiques, mixes and delivers end to end. A one-liner tests the engine. It never
tests an idea, because it does not contain one.

Request arguments (may be empty), shown once:

<request>
$ARGUMENTS
</request>

## The one-liner

> make a dynamic 15-second motion graphics video that shows what an incredible motion designer
> you are, like it's your showreel for a résumé. go all out.

Prompt by @stephanlivera (Opus 5.5 on Max effort, 2026-09-25,
https://x.com/stephanlivera/status/2103315922098470926), as surfaced by the Movez course. Credit it
whenever you show or reuse it.

| Slot | Phrase | Why it works |
|---|---|---|
| Duration | "15-second" | 6 to 8 shots fit; short enough to finish in one pass |
| Subject = the model | "what an incredible motion designer you are" | shows techniques, no product facts to get wrong |
| Genre | "your showreel for a résumé" | a reel has known rules: fast cuts, best work first, a new technique every shot |
| Effort multiplier | "go all out" | stacks on xhigh or max effort; it does not replace them |

## Choose canonical or variant

| Situation | Brief |
|---|---|
| first run on a fresh setup, or the user says "canonical" | the one-liner verbatim |
| anything to publish, or the canonical already ran here | a seeded variant from the roll below |
| the user names a pattern (piano reel, anti-slop, story, agency) | the matching paraphrased template in [assets/variants.md](assets/variants.md) |
| the user names a product or URL | stop; use `/motion-studio:product-reel` |

Roll a variant (the same seed reproduces the same brief; record it):

```
node "${CLAUDE_SKILL_DIR}/scripts/roll.mjs" --seed "<seed>"
```

| Flag | Use |
|---|---|
| `--seed S` or a positional seed | default `<folder>-<date>`; print and keep it |
| `--pin p03,g11,t04` | force rows by id (see `--list`) |
| `--techniques N` | 1 to 6 distinct techniques (default 3) |
| `--seconds S`, `--format f` | override the rolled frame |
| `--json` | one JSON line with the brief and every pick |

When the rolled genre is a loop, scaffold with `--loop`. Edit or extend the tables in
[assets/variants.md](assets/variants.md); the roll reads them directly.

## Run it through the studio

1. Project: if there is no `studio.json`, scaffold one for this test:

   ```
   node "${CLAUDE_PLUGIN_ROOT}/skills/studio-init/scripts/init.mjs" showreel --title "Showreel" --duration <S> --formats <brief format first>,<others> --install
   ```

   init keeps `9x16` as `primaryFormat` whenever it is listed, so set `primaryFormat` in
   `studio.json` to the brief's format (the original reel was 16:9). Skills-only installs: invoke
   `studio-init` instead. Then `npm run doctor`.
2. Music first: synthesize (`node tools/score.mjs --style <pulse|piano|minimal|cinematic> --bpm <N> --dur <S>`).
   Sound came unprompted in the original posts; here it is part of the test. The beat grid it writes
   (`audio/beats.json`) is what the shots are timed on.
3. Treat the brief as the whole creative input. Mode is autonomous: do not wait for shot-list
   approval (there is nothing to approve), but still write `docs/shotlist.md` on that grid with the seed or
   "canonical" on its `Status:` line, 6 to 8 shots on downbeats, a different technique per shot,
   best shot first.
4. Build `film/film.js`, then run the critique loop exactly as `/motion-studio:motion-reel`
   describes: at least 3 rounds, every axis >= 8, no P0. Use `brand=na` in the review log (the only
   `na` the gate accepts by default, `gate.naAllowed`); every other axis is scored, sound from the mixed
   render (`node tools/critique.mjs --format <fmt> --video out/<fmt>/final.mp4`, evidence in `out/review/<fmt>/video/`,
   built after a draft render, `sfx` and `mix`). The plugin hook blocks the final render until `npm run gate` passes.
5. `npm run build` (or `render:final`, `sfx`, `mix`, `deliver`). It takes minutes (about 4 min of rendering for a
   12 s film in three formats): run it in the background and poll the log; the pipeline runbook of
   `/motion-studio:motion-reel` ("Long commands") has the pattern.

## Grade the engine, not the idea

Report these to the user after delivery:

| Check | Where |
|---|---|
| every tool ran without manual fixes (doctor, stills, critique, gate, render, sfx, mix, deliver) | your log |
| determinism: no mismatching hashes | `out/review/<fmt>/metrics.md` |
| loudness -14 LUFS +-0.5 and <= -1 dBTP after AAC | `npm run deliver` |
| exact duration and frame count | `out/deliver/manifest.json` |
| wall-clock time and rounds needed | your log, `docs/review_log.md` |

Then move on: the next film needs content. Offer `/motion-studio:product-reel` (a real product),
`/motion-studio:reference-style` (a look to follow) or `/motion-studio:ui-morph-spec` (a state
spec).

## Why vary it

Hundreds of people ran the same sentence the same week, and the reels rhymed with each other. The
athemeroy/awesome-opus-5-5-videos README called it "brief contagion" in commits e5a0072 to
55cce56 (26 to 27 Sep 2026); commit 10bc706 (27 Sep 2026) removed the phrase in favor of more
cautious wording. The roll spreads engine tests across persona, genre, constraint and technique
instead of letting every run land on the same default reel. The critique's variety axis still
applies to the result.

## Effort and time

- This skill sets `xhigh` while active. The originals ran on Max (@stephanlivera,
  @himanshutwtxs) and xhigh (@robj3d3, one-shot including audio), which the course reads as "xhigh
  is enough"; @himanshutwtxs also posted a Medium-effort result for comparison. Effort for later
  messages is the user's choice: `/effort <level>` or `/model`.
- Creators reported 15 to 50 minutes for L1 results; @robj3d3 said xhigh took about an hour for two
  videos. Our critique rounds add time on purpose.
- Honest framing for the user: several viral "one prompt" reels involved retries, prior setup or
  much longer briefs. The one-liner is a smoke test, not a production method.

Next: `/motion-studio:product-reel` for a real product, or `/motion-studio:motion-reel` for any
other finished film.
