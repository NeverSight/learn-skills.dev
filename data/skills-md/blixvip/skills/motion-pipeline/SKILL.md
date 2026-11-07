---
name: motion-pipeline
description: The end-to-end runbook for turning raw footage plus a script into a finished, non-sloppy edit — stage order, quality gates, on-disk artifact layout, engine choice, parallel shot builds, and the ship checklist. Use this as the FIRST skill whenever the ask is "edit this video", "make me a video", "add motion graphics to this", "one-shot this edit", or any request that spans more than a single isolated animation. It sequences motion-plan, motion-assets, motion-design and motion-animate; do not run those ad hoc when a whole edit is in scope.
---

# motion-pipeline

You are the **orchestrator**, not the animator. Your job is to run stages in order, refuse to advance through a failed gate, and keep every shot consistent with every other shot.

**The single cause of AI-looking edits is skipping stages.** A brilliant animation on an unplanned beat, in an invented palette, with a stock asset nobody re-graded, is slop. Order beats effort.

## Non-negotiables

1. **Never one-shot a full video.** Build shot 1 to ship quality, get it approved, *then* batch the rest against it. A rejected style after 26 scenes is 26 rewrites.
2. **Never advance through a red gate.** Say which gate failed and what is missing.
3. **Never invent a palette, a font, or an asset** when the footage, the brand kit, or the reference folder can supply one.
4. **Never decorate every line.** Density is capped at stage 2 and enforced at ship.
5. **Every decision gets written to disk**, not held in context. The next agent, the next session, and the user all read the same files.

## Stage map

| # | Stage | Skill / tool | Gate to pass |
|---|---|---|---|
| 0 | Intake | this skill | G0 Brief complete |
| 1 | Transcribe | whisper / `hyperframes transcribe` / Premiere text panel | G1 Word-level timings exist |
| 2 | Plan | `motion-plan` | G2 Every beat classified, density under cap |
| 3 | Assets | `motion-assets` | G3 Palette sampled, tokens written, zero placeholders |
| 4 | Design | `motion-design` | G4 Anti-slop pass on the pilot frame |
| 5 | Animate | `motion-animate` | G5 Motion pass on the pilot shot |
| 6 | Batch | parallel sub-agents | G6 Every shot matches the pilot |
| 7 | Integrate | Premiere / master timeline | G7 Ship checklist (Appendix A) |

## Stage 0 — Intake

Collect before touching anything. Ask only for what is genuinely missing; infer the rest and state the inference. Templates — for a complete brief, for what to default to when one is thin, and for the message you send a sub-agent at stage 6 — are in Appendix B.

- **Footage** path, resolution, fps, and whether it is already cut.
- **Script or transcript**, and whether timings exist.
- **Aspect** — 16:9, 9:16, 1:1. This changes composition, not just crop.
- **Duration target** and hard deadline.
- **Brand kit** — logo files, fonts, hex codes, prior videos to match. If none exists, say so and derive from footage at stage 3.
- **Reference links** — the single highest-leverage input. Three references beat three paragraphs of description. Ask for them by name: "send me 2–3 videos or screenshots whose look you want."
- **Engine constraint** — does the deliverable need to land in Premiere/After Effects, or is a standalone render fine?

Write `edit/BRIEF.md`. If references are absent, flag it: *no references supplied, so the style is derived from footage and stays a guess until the user reacts to shot 1.*

## Artifact layout

Create this before stage 1. Everything downstream reads and writes here; nothing important lives only in a chat.

```
edit/
  BRIEF.md            intake + inferences + constraints
  NOTES.md            running log: every user correction, verbatim
  00-source/          raw a-roll, music, sfx, brand kit
  01-transcript/      words.json (word-level), transcript.md
  02-plan/            plan.md  + plan.json (machine-readable shot rows)
  03-assets/
    brand/            logo.svg, fonts/, brand.json
    refs/             the style references, named by what they teach
    gen/              AI-generated stills/video, with prompt.txt beside each
    3d/               glb/obj + the render passes
    lottie/           .json / .lottie
    sfx/              whooshes, impacts, ui ticks
  04-design/
    tokens.css        the palette + type scale — the single source of truth
    palette.json      machine-readable, for generators
    pilot/            the approved shot-1 frame
  05-scenes/          one folder per shot: 03-stat-card/, 07-map/, ...
  06-renders/         per-shot mp4 (opaque) / mov prores4444 (alpha)
  07-master/          project file + final export
```

**`tokens.css` is law.** Every scene imports it. A scene that hardcodes a color is a bug, because it will drift from the others — palette drift between shots is the loudest structural slop tell there is.

## Stage 1 — Transcribe

Word-level or it does not count. Phrase-level timings produce uniform-length visuals, which reads as automated.

- Local: whisper (`large-v3` for final, `base` for a scratch pass) or `npx hyperframes transcribe`.
- Already in Premiere: the Text panel transcript exports with timings.
- Already on YouTube: pull the caption track.

Output `01-transcript/words.json` with `{word, start, end}` records.

**G1** — fails if you only have sentence timings. Fix it before planning; do not estimate.

## Stage 2 — Plan

Invoke `motion-plan`. It classifies every beat `VISUAL` or `REST` and writes what each visual must *show*.

Add the pipeline's density cap on top of it:

| Video length | Max VISUAL share | Typical shot count |
|---|---|---|
| under 60s (short) | 65% | 8–14 |
| 3–8 min | 40% | 15–30 |
| 8–20 min | 30% | 25–50 |
| 20 min+ | 22% | 40–80 |

Also emit `plan.json` — one row per shot: `{id, start, end, dur, text, must_show, archetype, engine, assets[]}`. Stage 6 fans out over these rows, so each row must stand alone without the surrounding conversation.

**G2** — fails if any beat is unclassified, if density exceeds the cap, or if two adjacent shots use the same archetype (monotony reads as template).

## Stage 3 — Assets

Invoke `motion-assets`. Two outputs matter:

1. `04-design/tokens.css` — palette **sampled from the footage**, never invented.
2. Every `assets[]` entry in `plan.json` resolved to a real file on disk.

**G3** — fails on any placeholder, any lorem, any "TODO: find icon", any stock asset not yet re-graded into the palette.

## Stage 4 — Design the pilot

Pick the shot that is *most representative*, not the first one. Usually a mid-video stat or concept card. Build one frame, to ship quality, using `motion-design`.

Run the `motion-design` anti-slop checklist. Three or more failures means redesign, not patch.

Then **show it to the user and stop.** One frame, one question: *this is the look — anything to change before I build the other N shots in it?*

**G4** — fails without an explicit approval, or a correction logged in `NOTES.md`.

## Stage 5 — Animate the pilot

Invoke `motion-animate` on the approved frame. Render it. Watch it against the actual audio, not in isolation.

**G5** — fails if any of the four laws break: linear easing anywhere, simultaneous entrances, a fully static camera for more than ~2s, or metronomic durations.

## Stage 6 — Batch the remaining shots

Now, and only now, parallelize.

Fan out one sub-agent per shot (or per group of 3–4 similar shots). Each agent receives, and only receives:

- Its `plan.json` row.
- `04-design/tokens.css` — **read-only**.
- The path to the approved pilot scene, as the pattern to imitate.
- The engine for this shot (see table below).
- The anti-slop and motion checklists.

Each agent returns a rendered file into `06-renders/` and a one-line note in `NOTES.md`. Agents do not talk to each other and do not modify tokens.

**Isolate the workspaces.** Parallel agents editing one project directory will clobber each other — give each a git worktree, a copy, or at minimum a disjoint subfolder, then reconcile at the end.

**G6** — sample four renders at random and put them side by side. Same palette, same type, same shadow direction, same grain, same corner radii? Any drift means the drifting agent rebuilds against the pilot, not against its own output.

### Engine choice

| The shot is... | Build it in |
|---|---|
| Data, charts, maps, counters, long programmatic sequences | Remotion |
| UI mock, terminal, kinetic type, quick HTML+GSAP, needs a tweakable inspector | HyperFrames |
| Math, geometry, graph theory, algorithm walk-through | Manim |
| Anything that must sit **on** the footage — tracking, plate integration, roto, real-camera 3D | After Effects (see `ae-extendscript`) |
| A 3D object or environment | Blender / Unreal, render passes, then composite |
| Photoreal b-roll, product beauty, impossible footage | AI image to AI video, then re-grade to `tokens.css` |
| Captions | `add-subtitles` or the caption block, styled from tokens |
| The master timeline, audio, exports | Premiere / DaVinci |

Mixing engines is normal and good — it is one of the strongest anti-template signals. What must never mix is the palette.

## Stage 7 — Integrate and ship

Assemble in the master timeline. Then run Appendix A in full. It covers what per-shot checks cannot see: audio ducking under the graphics, caption vs. lower-third collision, safe areas, pacing across the whole piece, and the render spec.

**G7** — every box ticked, or a written list of what is not and why.

## Closing the loop

Before you finish, read `NOTES.md` and ask: *which of these corrections will the user make again on the next video?*

Turn those into a **project skill** — `.claude/skills/<client>-style/SKILL.md` — holding their palette, fonts, pacing preferences, banned moves, and the corrections you had to be told. The next video then starts at stage 4, not stage 0.

This is the compounding step. An agent that does not write down what it was corrected on will be corrected on it forever.

## When the user just wants one animation

Skip to stages 3–5 for that single shot, but still: sample a palette from something real, still run both checklists, still write `tokens.css`. The gates are cheap; rebuilding is not.

---

# Appendix A · Ship checklist (G7)


Run on the assembled master, not on individual shots. Per-shot checks already passed; this catches what only appears once everything is together.

Watch the whole thing **twice**: once muted, once at full volume with the graphics hidden. Problems hide in the mix of the two.

## 1. Consistency across shots

- [ ] Every shot pulls color from `tokens.css`. Grep the scene folders for raw hex values that are not in the token file — any hit is drift.
- [ ] Shadow direction is identical in every shot.
- [ ] Grain/texture pass exists in every shot at the same strength.
- [ ] Corner radii, stroke weights, and glow intensity match.
- [ ] Type: same two families throughout, same tracking rules, same case rules.
- [ ] Recurring elements (chapter cards, counters, lower thirds, the subscribe bug) are literally the same component, not re-made per instance.
- [ ] Logo appears at consistent scale and clear-space.

## 2. Pacing across the piece

- [ ] No two adjacent shots share an archetype.
- [ ] Shot durations vary. Chart them — a flat line is a metronome and reads as automated.
- [ ] REST beats survived. If every line ended up with a visual, the plan was overridden somewhere; cut back.
- [ ] The opening 5 seconds carry the highest density; the middle breathes.
- [ ] No graphic outlives its line. A visual that hangs past the point it illustrates is dead air.
- [ ] Nothing on screen is unreadable at speed. Read every super out loud at playback rate; if you cannot finish it, it is too long or too fast.

## 3. Integration with the footage

- [ ] Graphics are graded to the plate, not pasted on it — matching black level, matching warmth, matching grain.
- [ ] Anything meant to sit in the scene has contact shadow or occlusion.
- [ ] Nothing covers the speaker's face, and nothing sits where their hands travel.
- [ ] Lower thirds and captions never collide. Decide the z-order once: graphics above captions, or captions above graphics — then hold it.
- [ ] Framing survives the crop: 9:16 exports keep the subject and the supers inside the visible area, not just inside the canvas.
- [ ] Safe areas respected — nothing critical in the outer 5%, nothing behind platform UI on shorts (bottom ~15%, right ~10%).

## 4. Audio

- [ ] Music ducks under dialogue. Generated keyframes, not a static level.
- [ ] SFX exist on the moments that need them — entrances, impacts, UI ticks, transitions — and nowhere else. Wall-to-wall whooshes is its own slop signature.
- [ ] SFX are mixed **under** the graphic, not on top of the voice. If you notice the whoosh, it is too loud.
- [ ] Every sound effect lands on the frame the motion lands on, not near it.
- [ ] Dialogue level is consistent shot to shot; no cut jumps in room tone.
- [ ] Ends clean: music resolves or fades, no hard cut on a sustained note.

## 5. The edit itself

- [ ] Cuts start on words, not on inhales.
- [ ] Repeated takes, restarts, and filler removed.
- [ ] No frame duplicated at a stitch point (a classic tell when chaining generated clips last-frame-to-first-frame — trim one frame).
- [ ] Transitions are motivated. A transition that exists because a transition was available gets cut.
- [ ] Any AI-generated b-roll has been re-graded into the palette and, if it has visible text, checked for garbled type. Garbled on-screen text is the single most recognizable generated-video artifact — crop it out or replace the shot.

## 6. Render spec

- [ ] Correct resolution, fps, and color space for the destination.
- [ ] Alpha shots exported as ProRes 4444 / QuickTime with alpha, not baked over black.
- [ ] Bitrate sane for the platform; no banding in gradients (add a touch of grain if there is).
- [ ] Audio at the platform's target loudness, peaks under 0 dBFS.
- [ ] Filename says what it is and which version it is.

## 7. The honest question

Watch it once more and answer in one sentence: **what would a viewer say gave this away as automated?**

If you can name something, fix that thing. If you genuinely cannot, ship it.

## Failure log

Anything that failed here goes in `NOTES.md` with the cause, not just the symptom. "Shot 12 had a flat background" is a symptom; "the batch agent for shot 12 did not import tokens.css" is the cause, and it is the one that becomes a rule in the project skill.

---

# Appendix B · Briefing the agent (and briefing sub-agents)


## How the user should hand you a job

The fastest, highest-quality brief has five parts. When any are missing, ask for that part specifically rather than asking an open question.

```
FOOTAGE     C:/work/raw/ep41.mp4  (4K, 30fps, uncut)
DELIVER     8-min YouTube main + 3 shorts (9:16)
LOOK        refs/ — the three images in there. Especially glass-transparency.png.
BRAND       assets/brand/  (logo.svg, Inter + Instrument Serif, #e8721f)
CONSTRAINT  must land back in Premiere as alpha MOVs; deadline Thursday
```

Then one sentence of intent: *"Editorial, confident, not hypey. Wide shots breathe, stats punch."*

That is a complete brief. Everything else is discoverable.

## What to do when the brief is thin

Do not stall on an open-ended question. Infer, state the inference, proceed, and put the decision where the user can reverse it cheaply.

| Missing | Default to | Say |
|---|---|---|
| References | palette sampled from footage, editorial archetype | "Deriving the look from your footage — react to shot 1 and I'll adjust." |
| Aspect | 16:9 | "Building 16:9; tell me now if shorts are needed, it changes composition." |
| Duration | the length the plan implies | state the number you landed on |
| Brand | footage-derived tokens | "No brand kit found, so tokens come from the footage." |
| Music | none, leave the bed empty | "Left music out — drop a track in `00-source/` and I'll mix and duck it." |

## How you brief a sub-agent

Sub-agents start cold. Everything they need must be in the message or on disk at a stated path. A vague delegation returns work that has to be redone.

```
Build shot 07 of the edit at C:/work/edit/.

ROW        02-plan/plan.json → id "07"
TOKENS     04-design/tokens.css  — read-only, import it, hardcode nothing
PATTERN    05-scenes/03-stat-card/  — the approved pilot. Match its
           background treatment, grain, shadow direction, type scale.
ENGINE     Remotion. 1920x1080 @30. Duration 4.2s exactly.
MUST SHOW  the 3-step flow, step 2 emphasised
CHECKS     motion-design, Appendix A (anti-slop)
           motion-animate — the four laws
OUTPUT     06-renders/07.mov (ProRes 4444, alpha)
           + one line appended to NOTES.md

Do not change tokens.css. Do not touch other scenes. If the row is
ambiguous, pick the reading that matches the pilot and note it.
```

The four lines that matter most: **read-only tokens**, **the pilot as pattern**, **exact duration**, **do not touch anything else**. Omit them and shots drift.

## Prompting rules that hold everywhere

- **Speak to it like a new editor on their first day**, not like a search engine. Context is what is missing from bad prompts, not keywords.
- **Attach an image for anything visual.** A screenshot with "this specific thing is wrong" beats a paragraph every time.
- **One change per round when correcting.** Batched corrections come back with the fixes tangled and something you liked lost.
- **Say what is wrong, not what to do**, when you do not know the fix: "the glass reads opaque, ref-1 is much more transparent" outperforms "reduce opacity to 40%".
- **Use the vocabulary you have.** Ease-in/ease-out, overshoot, hold, contact shadow, track matte, pre-comp, safe area, ducking. Precise editorial language produces precise results; "make it better" produces drift.
- **Ask for a plan before a build** on anything expensive: *"list the shots with timestamps and what each one shows. Do not build yet."* Reviewing a list costs a minute; reviewing 26 built scenes costs an afternoon.
- **Ask for options at decision points**, not at execution points: three hook variations, yes; three renders of the same approved frame, no.

## Handing off a running job

When a session ends mid-edit, the next agent needs exactly one message:

```
Resume the edit at C:/work/edit/.
Read BRIEF.md, NOTES.md, 02-plan/plan.json, 04-design/tokens.css.
Stage 6 in progress. Shots 01-09 rendered; 10-14 remain.
Pilot is 05-scenes/03-stat-card. Match it.
User corrections so far are at the bottom of NOTES.md — honour all of them.
```

If that message cannot be written because the state is not on disk, the state was never real. Write it down as you go, not at the end.
