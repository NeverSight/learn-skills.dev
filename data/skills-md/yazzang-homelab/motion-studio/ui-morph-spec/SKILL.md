---
name: ui-morph-spec
description: "Write a six-part XML state spec for a one-shape UI morph film (inputs, direction, structure, build, gotchas, start): states on downbeats, cursor-driven changes, seamless loop, approval gate. Use for 'UI morph', 'state list'."
argument-hint: "[product or URL] [number of states] [bpm]"
allowed-tools: Bash(node "${CLAUDE_SKILL_DIR}/scripts/statelist.mjs" *)
effort: xhigh
---

# UI morph spec (course step 06, level L3)

Write the state list, not the vibe. The most-bookmarked prompt of the Opus 5.5 launch week was not
a one-liner: @twoclipping's UI morph loop and @verbove's MakerMap film both used an XML spec with
inputs to ask for, a direction, a beat-by-beat state list, build rules and gotchas. The idea behind
them: one shape that never cuts. A single element changes size, radius and color from state to
state (button, loader, player, chart, command palette), a cursor causes each change with a real
click, and the last frame equals the first so the film loops.

Request arguments (may be empty), shown once:

<request>
$ARGUMENTS
</request>

Credit: the six-section layout follows @twoclipping's public template
(https://x.com/twoclipping/status/2103273003555402193; the XML is in the main post, not in a thread
reply as the course says) and @verbove's MakerMap spec
(https://x.com/verbove/status/2103483957266268381). The template in this skill is written in
motion-studio's own words: [assets/spec-template.xml](assets/spec-template.xml).

## 1. Ask for the inputs

Ask in one AskUserQuestion round (subagents cannot ask; you do):

| Input | Default | Rule |
|---|---|---|
| Product + URL | required | capture real UI and copy with `/motion-studio:product-reel` stage 3 when there is a URL |
| 8 to 12 states in story order | logo, CTA, email field, loader, check, card, chart, command palette | one per downbeat |
| Real data per state | ask | labels, numbers, names from the product; no placeholders |
| Brand colors, fonts, one accent | from capture or `studio.json` | one accent |
| Track | synthesize `minimal` at 120 BPM | a supplied track must allow this use and start on a downbeat |
| Formats | `9x16`, `1x1`, `16x9` | same timeline, reframed |
| Loop | yes | the last state morphs back into the first |

## 2. Fill the spec

Copy the template into the project as `docs/spec.xml` and fill every `[...]` with the answers.
Keep all six sections: `<inputs>`, `<direction>`, `<structure>`, `<build>`, `<gotchas>`,
`<start>`. The motion-director subagent (`motion-studio:motion-director`) can draft it from your
brief; it writes only under `docs/`.

## 3. Put the states on the beat grid

1. Project: scaffold with `--loop` if needed
   (`node "${CLAUDE_PLUGIN_ROOT}/skills/studio-init/scripts/init.mjs" <dir> --title "<Product> morph" --loop --duration <S> --install`;
   in a skills-only install use `node "${CLAUDE_SKILL_DIR}/../studio-init/scripts/init.mjs" ...` with the same
   flags, or invoke the `studio-init` skill).
2. Grid: `node tools/score.mjs --style minimal --bpm 120 --dur <S>`, or measure the supplied track
   with `node tools/beats.mjs audio/<track>`.
3. State list with exact downbeat times, loop checks and warnings:

   ```
   node "${CLAUDE_SKILL_DIR}/scripts/statelist.mjs" --states "logo,CTA button,email field,loader,check,card,chart,palette" --out docs/statelist.md
   ```

   | Flag | Use |
   |---|---|
   | `--states "a,b:2,c"` or `--file list.txt` | states in order; `:2` holds a state for two bars |
   | `--beats audio/beats.json` | measured grid (default when the file exists); `--beats none` ignores it |
   | `--bpm N`, `--beats-per-bar N` | override the grid |
   | `--no-loop` | a film that ends instead of looping |
   | `--json` | one JSON line with every state's start, end and content timing |

   It warns when the loop length differs from `studio.json` `duration`, when the first state is not
   at 0 s (a pickup in the track), or when a state holds under 1 s. Fix the duration or trim the
   track before continuing.
4. Fill the cursor action, data and sound columns of `docs/statelist.md`, and copy the table into
   `docs/shotlist.md`.

## 4. The gate

Show the state list on the beat grid and wait for the user's OK before writing any film code (the
`<start>` section says so, and so does the course). A rejected list is rewritten, not coded around.
Record the decision on the `Status:` line of `docs/shotlist.md`.

## 5. Build from the verified example

Copy [assets/morph-loop.film.js](assets/morph-loop.film.js) to `film/film.js` and adapt it: it is a
working 16 s, 8-state loop at 120 BPM that renders in every format. Replace `STATES` (sizes in
1080 px units, fill token), `COPY` and the `content` painters with the approved list and the real
data; keep the mechanics:

| Mechanic | API | Rule |
|---|---|---|
| state times | `grid.bar(i)` | never typed seconds |
| container size, radius, color channels, camera zoom | `loopTrack(t, keys, dur, spring)` | keys in `[0, duration]`; the seam change once, as a key at the first downbeat (this example) or at t = duration |
| content in and out | `swapAlpha(t, start, nextStart)` | in after the morph starts, out before the next |
| cursor | `loopTrack` on x and y, `cursor(g, x, y, { pressed })` | clicks the current element on the downbeat |
| tabs and list highlights | `indicator(t, stops, { width })` | edges on different springs |
| sounds | `cues` from `grid.bar` and `grid.beat` | click on presses, swoosh under morphs |
| grain and other frame-indexed noise | `grain(g, W, H, c.frame % LOOP_FRAMES, ...)` with `LOOP_FRAMES = Math.round(dur * fps)` | the critique compares `hash(0)` with `hash(duration, { wrap: false })`; noise seeded by the raw frame index makes the end differ from frame 0 and fails the loop check |

Every pattern with its reasoning: [references/morph-recipes.md](references/morph-recipes.md).
Set `studio.json` `"loop": true` and `duration` to the loop length, then `npm run lint`.

## 6. Critique and deliver

Run the critique loop from `/motion-studio:motion-reel` (at least 3 rounds, all axes >= 8, no open P0; each round
builds the mixed render and both evidence passes first, see its pipeline runbook).
For morph loops also check `out/review/<fmt>/loop.png` (live pass only; the `video/` pass has no loop pane) and the "loop seam" metric
(`hash(0)` equals `hash(duration, { wrap: false })`, continuity ratio <= 1.5; the `|end - first|` pane must be black,
which frame-indexed grain breaks unless its index wraps), labels during every swap in `strip.png`, and the
cursor position at each downbeat in `contact.png`. A seam jump is a P0. Then `npm run build`.

## Rules for morph films

- One container, never cut. States differ by size, radius, fill and content only.
- A cursor causes every change; no state changes by itself.
- Something moves on every beat: a press, typing, a counter, a line drawing, a highlight step.
- Real product data only. Springs with at most a hint of overshoot; none on type.
- Banned: bouncy easing, glows, gradients on UI chrome, particle bursts, dead beats.
- Never `will-change` (or any rasterizing trick) on anything the camera scales.

Next: `/motion-studio:springs` to tune the feel; `/motion-studio:ship-formats` for per-format
reframing and delivery.
