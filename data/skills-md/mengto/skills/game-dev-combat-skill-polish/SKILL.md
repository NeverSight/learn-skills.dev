---
name: game-dev-combat-skill-polish
description: Score a game's combat skills and spells out of 10 with blind judges, then raise the weakest to a bar, for timing and readability (does a skill read as itself, does the blow land when it lands) and for art (detail, light, trails, impact, art direction, judged against a reference such as Diablo IV). Covers filming casts on a stopped, stepped clock, contact strips and close-ups, anonymised two-judge rounds, the levers that moved scores (hero props made from a painted concept with image-to-3D, own schedules and keyed moves, painted additive textures, camera-facing ribbons, light outside the body), the traps that cost points, asset and load budgets, and shipping each skill as its own version. Use when the user asks to score, review, improve, polish or rebuild combat skills, spells or attacks; says a skill "doesn't make sense", "looks bad" or should look like another game; names a target score; or starts a "next skill" thread. Project specifics (review hooks, harness settings, where each skill's code lives, scores so far) go in an optional local references/<project>.md next to this skill.
---

# Game dev: combat skill polish

A skill is the cast (the caster's body), the effect (what it throws, raises or tears open), and the result (the target's reaction and what it leaves behind). Polish all three, judged from real footage by people who did not make it.

There are two bars. Know which one the user means:

| Bar | Asks | Rubric | Typical target |
|---|---|---|---|
| **Readability** | Does it read as itself? Does the result land when and where the blow arrives? Is the pose its own? | `references/rubric-readability.md` (reads, timing, body, effect, reaction) | every skill 6+ |
| **Art** | Detail and texture, light, motion and trails, impact, art direction, against a named reference | `references/rubric-art.md` (Diablo IV paladin skills, described in words) | 7+ per skill |

A skill can score 7 on readability and 3 on art. Never quote a score without naming its rubric.

## 1. Pin down the job

- Which skills: all of them (a survey), or named ones (a rebuild). One skill per thread when several run at once.
- The bar and the reference. If the user shows a reference image, save it into the project so judges can open it; otherwise describe it in words in the rubric.
- Read the project reference first (`references/<project>.md`, if there is one): where each skill's code lives, the harness settings, the scorecard so far, and what other threads already learned.
- Before designing, `git fetch` and check what other threads are changing; several skill threads edit the same effect and animation files.

## 2. Film the real thing

- Work in your own git worktree off the main branch. Serve it on a free port; serve a clean main worktree on a second port for the "before".
- Film headlessly on a **stopped, stepped clock**: freeze the game clock, step it 0.05 s per frame, wait for a rendered frame, shoot. A loaded machine then still gives evenly spaced frames. (`scripts/film.mjs`; staging per skill in a scenarios file like `scripts/scenarios.example.mjs`.) The game needs review-only hooks for this: stage a state, issue a command, aim the camera, freeze and step the clock (the contract is at the top of `film.mjs`; HOOK, PAGE, READY, SETTINGS_KEY and CHROME are set from the environment).
- Stage each cast so the caster, the target, the hero object and the landing are in the crop and clear of the HUD (`frame`, `span`, `points`). A thing hidden behind a panel scores as "a speck".
- Build a **contact strip** per cast (`scripts/strips.py`, N=16 and TAIL=3 to keep the aftermath) and a **close-up** of the key frames (`scripts/close.py`). Judges need both: strips show timing, close-ups show art.
- Measure what can be measured: the frame the foe moves against the frame the blow lands (`meta.json` per-frame action and time), draw calls and triangles during the cast (`scripts/perf.mjs`), and download size.
- Never edit served source files during a film; the dev server reloads mid-capture.

## 3. Judge blind, two at a time

- Spawn **two fresh general-purpose subagents** per round. Give them the rubric, a list file and the image paths, and tell them to open no other files: no code, no earlier scores, no keys. `scripts/judge-set.py` anonymises strips under neutral ids and writes the list and a key; `templates/judge-prompt.md` has the two prompts.
- Ask for JSON: part scores, a total, the biggest fault and the single change that would raise it most. Save every reply under `judges/`.
- Keep the **lower** of the two. Never round up. Never score your own captures.
- Judge spread is about ±0.5 to 1. Before calling a 7 solid, re-judge the same pictures or mix a calibration strip (an old version) into the set. One lucky round is not a pass.
- The judges' "next" lines are the work list. When both name the same thing, do that first.

## 4. Raise it, round by round

Fix the criterion costing the most points. These moved scores before:

**Timing and readability**
- Results must land on the beat: the target reacts, is pushed or gets its status when the blow, missile or wave arrives, never on the click. Check the scene layer that draws units at their rules position every frame; it will happily show a push before the blow (the first and biggest fix on the project this skill was built on).
- A skill that borrows another's schedule (its duration and contact moment) cannot have its own body. Give it **its own schedule and keyed move**: a kneel then rise, a gather then throw, a bow then welcome. Then update every place that branched on the old schedule's name.
- Travel time for waves and missiles: the hit waits for the arrival.
- Hits across an arc are staggered along the measured blade path, not fired together.
- The target's reaction: a recoil, buckle, daze or knock-back is half the read. Status labels alone score low.

**Art**
- **The hero object's modelling is the ceiling.** Scripted primitives and hand-built meshes plateau at 5.5 to 6.5 ("plain prism", "toy"). A painted concept (gpt_image_2_5) turned into a textured model with image-to-3D (Higgsfield `image_to_3d`, Meshy, textured + PBR, about 12k triangles) took two skills past 7. Without any hero element, a skill tends to plateau around 6 (a wind skill with nothing modelled stopped at 6 after 20 rounds).
- When the hero is a small world prop, keep the prop readable and make the effect painted wisps round it (a modelled "hand of force" never read from the tactical camera).
- **Painted textures** on black for additive blending (craters, crescents, ribbons, shockwave rings, vortices) beat procedural rings and streaks. Gradient-map them to the skill's palette before shipping (lava red next to a red target marker reads wrong).
- **Ribbons and trails**: camera-facing across the path, width growing with the path drawn, soft across their width, sampled back along the motion itself (not frame by frame). A thin uniform line reads as "a laser" or "a debug line"; a wide single band reads as "a flat card".
- **Metals need something to reflect.** A tactical scene often has no environment map; give a model its own small equirect sky and a tight fresnel rim. A broad rim or warm tint washes gold to cream or copper.
- **Light**: put it on the object or beside the body toward the caster, about a metre out. A light inside the body lights nothing; a light pool under a projectile reads as "a detached disc"; too bright bleaches the target.
- **Impact**: a small hot core, debris flung and falling, dust low and dark, a mark left in the ground that cools or fades, and a strong recoil. A big white disc that hides the target always loses points.

**Things judges always mark down**: borrowed looks (another skill's ring, flash or pose); flat cream or white placeholder flashes; even radial streaks; pillars or lances of light over the target; additive dust rings that brighten the ground to cream; stretched white sparks ("white dashes"); long lingering trails ("laser", "lightning"); crack decals that read as electric; anything under the HUD.

Keep guardrails while climbing: frame budget, first-scene download budget (load new assets only when a fight that can use them starts), the readability score, the tests, and other skills' looks. Commit WIP locally each round; a restart then costs nothing.

## 5. Stop, lock in, ship

- Stop when the bar is met on the lower judge (and a re-judge agrees), or when a skill plateaus for several rounds. Then say plainly what it would take (usually a modelled hero element).
- Ship the version the judges scored, not an unjudged tweak of it.
- Add a test that locks the skill's own schedule, model or recipes in place.
- Write the scorecard: a round table (change, both scores, kept), what moved it, what is left, cost, and a before/after sheet (`scripts/beforeafter.py`).
- Ship it as its own version with three pictures (start, key moment, result), following the project's ship routine (`workflow-ship-change`), with measured sizes.
- Update the project memory with what moved scores and the new traps, so the next skill starts further on.

## Report

Lead with the result per skill, on its named rubric: "Summon Hammer 4 → 7 (art, two blind judges, lower kept)". Then the round table, how it was judged and from what footage, where it still falls short in the judges' words, the cost, and the before/after pictures sent inline. Label captures as headless browser captures, not device tests.
