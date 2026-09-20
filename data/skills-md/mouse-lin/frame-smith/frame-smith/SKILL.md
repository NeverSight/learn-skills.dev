---
name: frame-smith
description: 'Build never-cheap, motion-crafted promo videos as Remotion compositions — cinematic HyperFrame-style clips (3D poster cubes, capsule theme-flips, architecture data-pulse, particle-burst photo albums) and vertical short-video for 抖音/小红书/视频号. frame-smith is the DIRECTOR, not the renderer: it reads the brief, sets the register (landscape cinematic vs. vertical short), picks ONE effect engine done at 100%, lays a beat timeline, writes the .tsx, and registers it in the Remotion Root. It runs ON TOP OF a video runtime — it needs the `hyperframe` OR the `remotion` skill installed, checks for them FIRST (§0), and guides install if neither is present. Ships a motion craft floor (30fps, second→frame helper, S-scale for vertical, 抖音 safe zones, easing library, export三件套), an effect-engine catalog lifted from shipped HyperFrames, a beat-timeline architecture, and a motion anti-slop blacklist (no everything-fades-up, no linear easing, no janking engine). Supports verb commands (craft · env · beats · engine · restage · slower|faster · register · audit). Triggers on "做个视频", "视频动效", "promo video", "motion graphics", "Remotion 合成", "HyperFrame", "片头动画", "产品宣传片", "3D 立方体动画", "粒子相册", "数据可视化视频", "竖屏短视频", "抖音视频", "小红书视频", "opener animation", "转场", "beat timeline", "把这个页面做成视频", "/frame-smith".'
version: 0.1.0
user-invocable: true
argument-hint: "[craft · env · engine|beats · restage · slower|faster · register · audit] [brief]"
license: MIT
---

# frame-smith — Motion-Crafted · Effect-Engine-Driven · Never Cheap

> **frame-smith is a director, not a renderer.** It decides *what the video is* — register, effect engine, beat timeline, motion craft — and writes a Remotion composition (`.tsx`) that a video runtime renders. It does **not** own the runtime. The runtime is the `hyperframe` skill (the effect-template library, carries its own Remotion) **or** the `remotion` skill (the bare runtime + scaffolding). **frame-smith needs exactly one of them present** and checks first (§0).
>
> frame-smith builds two registers and routes by them (§0.A):
> - **cinematic** — a landscape HyperFrame clip, `1920×1080 · 30fps · 12–24s`, **pure visual, no voiceover**. Optimize for **one spectacular effect engine + a tight beat arc + a wordmark payoff**. This is the register of the four engine archetypes (Poster-cube tumble, Capsule theme-flip, Architecture data-pulse, Particle-burst album).
> - **short** — a vertical short-video, `1080×1920`, for 抖音/小红书/视频号. May carry **subtitles / voiceover**. Optimize for **hook in the first 1.5s + readable-inside-safe-zone + rhythm cut to narration**. Obeys the `S = width/720` scale system and the 抖音 safe zones.
>
> The through-line is identical: **high motion craft, zero motion-slop.** What applies to **both** is the **motion craft floor** (`references/motion-floor.md` — 30fps, the `f(sec)` second→frame helper, `clampOpts`, the export三件套, easing over `linear`, terminal-frame discipline) and the **anti-cheap-motion blacklist** (§6). What **forks** is orientation, safe-zone math, and whether copy is on screen.
>
> Every rule below is **contextual**. Nothing fires automatically. Read the brief, set the register, then pull only the engine that fits. A skill that ships the same fade-up-slide-in clip for every brief has failed — that *is* the slop.

---

## How to use this skill

**0. ENVIRONMENT FIRST — this is a hard gate, not a suggestion.** Before anything else, confirm a video runtime is present. frame-smith writes compositions but cannot render them alone. Load `references/environment.md` and run its check: **at least one of the `hyperframe` or `remotion` skills must be available.**
   - **Neither present** → STOP. Do not write any `.tsx`. Surface the two install options (prefer `hyperframe` — it carries the effect templates you'll lift from; `remotion` is the leaner runtime-only path) and wait. `environment.md` has the exact detection steps and install/bootstrap guidance.
   - **One present** → note which (it decides where the composition file lands and how you register + preview it), then proceed.

1. Run **§0 Brief Read** — infer the **register** (cinematic vs. short) and the **one-line intent** before touching code. Name the lazy default and reject it. Output a short Frame Read, then **stop for confirmation.**
2. Set the **§1 Three Dials** (ENERGY · SPECTACLE · DENSITY). Short register pins DENSITY toward legibility; cinematic pins SPECTACLE high.
3. **Lay the motion craft floor** (`references/motion-floor.md`) — the same for both registers: 30fps, `const f = (s) => Math.round(s*FPS)`, `clampOpts`, easing library, the export三件套 (`Component` / `ComponentCover` / `COMPONENT_FRAMES`). Then the **orientation substrate forks**: cinematic → `1920×1080`, no safe-zone tax, wordmark grammar; short → `1080×1920`, `S = width/720` scale on every pixel, 抖音 safe zones, subtitle rhythm.
4. **Pick ONE effect engine** from `references/effect-catalog.md` — the engine is the video's soul. One, done at 100%, not three at 40%. The catalog is organized by the four engine archetypes plus their reusable sub-effects (3D CSS solids, stadium/pill mask theme-flip, trapezoid data envelopes + counters, SVG stroke-writing + particle burst + 3D ring). Match engine to intent; don't reach for the same one every time.
5. **Lay the beat timeline** (`references/beat-structure.md`) — a video is beats, not a page. Fix `H0…Hn` boundaries in seconds, give each beat one job, and make the last beat *land* (wordmark, logo, CTA). Pick the narrative skeleton for the register.
6. **Choreograph the reveals** (`references/reveals.md`) — how text and elements *enter and exit* is the readable surface of the whole clip. Vary the vector, stagger the siblings, mask the edge, give the hero its own move. The #1 slop is everything fading-up together.
7. **Score it — sound design** (`references/sound-design.md`) — **sound is half the craft, and it is not optional on cinematic either** (no voiceover ≠ no sound). Choose a BGM matched to ENERGY + genre with head/tail fades; place 3–6 SFX to accent the key beats; and **lock audio-visual sync** — every SFX and the BGM drop land on the same beat frame as their picture. This is the highest-leverage "feels professional" move in the skill.
8. **Write the composition, then register it** (`references/registration.md`) — the export三件套, the `<Composition>` + `<Composition ...Cover>` pair in the Root, correct `durationInFrames` / `fps` / `width` / `height`. An unregistered composition is invisible in Studio and unrenderable.
9. Run the **anti-cheap-motion blacklist** (`references/anti-cheap-motion.md`) and **pre-flight** (`references/preflight.md`) before declaring done — the reduced-motion / terminal-frame check, the reveal + sound checks, and a Studio preview or still render to prove it moves. Then read it against the **good-video rubric** (`references/showcraft.md`) — the four layers (engine · rhythm · reveals · sound) + sync — and fix by the *lowest-scoring layer*, not by piling more onto a strong one.

The `references/*.md` files are the deep material. Load the one you need for the current phase — do not inline all of them.

| Reference | When to load |
|-----------|-------------|
| `environment.md` | **§0, before anything else — the hard gate.** How to detect whether the `hyperframe` or `remotion` skill is available, what each provides, where a composition file lands under each, how to preview/render, and the install/bootstrap path when **neither** is present. Also: how to fall back to a Remotion project already on disk |
| `motion-floor.md` | **Every build, both registers** — the universal craft floor: 30fps, the `f(sec)` helper, `clampOpts`, the `S = width/720` scale system (vertical) + 抖音 safe zones, the easing library (`Easing.out(cubic/exp/back)`, `spring`), the `trapezoid`/envelope helpers, the export三件套 naming, and terminal-frame discipline (a clip must hold a clean last frame + a still `…Cover`) |
| `effect-catalog.md` | **Step 4 — picking the engine.** The effect-engine vocabulary lifted from the four shipped HyperFrames, each with its signature technique, when to use it, and the reusable sub-effects: CSS-3D solids (cube/ring/card-stack), stadium/pill **mask theme-flip**, **piecewise-pose** timelines with drift, **trapezoid data envelopes** + big-number counters + network lines + gallery wipes, **SVG stroke-writing** + particle burst + spring-overshoot matrix. Plus the editorial overlay kit (ruler grid, corner labels, crosshair, accent-line outro) |
| `effects-menu.md` | **The user-facing "à la carte" menu (视频动效清单).** A browsable, non-technical list of every effect the skill can do — engines · reveals · transitions · overlays · 3D · sound — each with "what it looks like" + "how to ask for it" in Chinese. Load it to **show the user their options** (during the Frame Read, or when they ask "有哪些效果/what can you do"), or to parse a user who点名点了具体效果. It routes into the deep files below |
| `beat-structure.md` | **Step 5 — the timeline.** How to think in beats not sections: fixing `H0…Hn` in seconds, one job per beat, the hook-in-1.5s rule (short) and the wordmark-payoff rule (cinematic), the narrative skeletons per register, and how to make the last beat *land* instead of just stopping |
| `reveals.md` | **Step 6 — text & element entrance/exit choreography.** The positive catalog: masked line rise, per-char/word/line reveals (granularity must match text length), clip-path wipe, blur/focus-pull, scale-pop overshoot, SVG stroke-writing; stagger discipline, the hero's distinct move, and exit choreography (`enter × (1−exit)`). Load it whenever text or a set of elements comes on screen |
| `sound-design.md` | **Step 7 — background music, transition SFX, mix & sync.** Remotion `<Audio>`/`<Sequence>` mechanics; BGM matched to ENERGY+genre with head/tail fades; the SFX→beat map (whoosh/impact/click/riser); ducking under voiceover; and the **audio-visual sync** discipline (every SFX + BGM drop on a beat constant). Load it on **every** clip that will have sound — which is every clip |
| `registration.md` | **Step 8 — making it real.** The export三件套 contract, the `<Composition>` + `…Cover` pair, `durationInFrames = COMPONENT_FRAMES`, choosing the Folder, the cover-still convention (height 1440 for a taller poster crop), and how to preview in Studio / render a frame |
| `anti-cheap-motion.md` | **Before any delivery** — the motion anti-slop blacklist: everything-fades-up-together, `linear` easing, uniform 0.5s durations, no overshoot/anticipation, engine that janks or cuts off mid-motion, dead-air beats, a last frame that just freezes with no payoff, `top/left/width/height` animation instead of `transform/opacity`, plus the audio anti-slop (stock bed, genre mismatch, SFX carpeting, out-of-sync) |
| `showcraft.md` | **The quality rubric — what counts as *good*, not just *not-broken*.** The four layers a high-craft clip needs in balance (engine · rhythm · reveals · sound) + the sync connective tissue, a 10-point score, and the one-line test ("muted, does it read? eyes closed, does it sound like *this* video? do they meet on the same frames?"). Read it when a clip "feels off" but pre-flight passes, during `audit`, or to decide which layer to lift |
| `assets.md` | Brief needs real imagery, fonts, or audio — `staticFile()` vs. absolute-URL assets, the font-loading roads, where assets live under each runtime, `objectFit` discipline, and the generate-vs-source-vs-placeholder decision with its authorization step |
| `preflight.md` | **Final checklist before "done"** — merges the craft-floor check, the anti-slop scan, the reveal + sound checks, the safe-zone check (short), the registration check, the reduced-motion terminal state, and the "prove it moves" step. If any hard rule fails, it is shipping broken |

---

## Commands

frame-smith runs as a full build by default, but supports **verb commands** for targeted iteration on an existing composition — so you don't re-run the whole Brief Read for a single change. Each command loads one reference and does one job.

| Command | Category | Does | Reference |
|---------|----------|------|-----------|
| `craft [brief]` | Build | The full flow: env gate → Frame Read → dials → floor → engine → beats → register (the default) | all |
| `env` | Setup | Run **only** the §0 environment gate — report which runtime is present, or lay out the install path if neither is | `environment.md` |
| `engine [target]` | Refine | Swap the effect engine when **this clip** is the wrong soul — re-pick from the catalog, keep the beats | `effect-catalog.md` |
| `beats [target]` | Refine | Re-cut the timeline — move `Hn` boundaries, add/drop/reorder a beat, fix a dead-air stretch, without touching the engine | `beat-structure.md` |
| `reveals [target]` | Refine | Re-choreograph how text/elements enter & exit — de-uniform the entrances, stagger, give the hero its own move, add exits | `reveals.md` |
| `sound [target]` | Refine | Re-score the audio — swap/re-fit the BGM, re-place the SFX on beats, fix ducking or **audio-visual sync** | `sound-design.md` |
| `restage [target]` | Iterate | Upgrade an existing composition, audit-first; never full-rebuild for one complaint | `anti-cheap-motion.md` + `preflight.md` |
| `slower [target]` | Refine | Stretch the timeline / raise easing softness / cut ENERGY — calm a frantic clip | `motion-floor.md` |
| `faster [target]` | Refine | Compress the timeline / tighten holds / raise ENERGY — wake up a sluggish clip | `motion-floor.md` |
| `register [target]` | Iterate | Re-orient landscape↔vertical: re-lay the safe-zone / scale substrate, re-fit the engine to the new aspect | `motion-floor.md` |
| `audit [target]` | Evaluate | **Read-only** diagnostic: run the anti-slop blacklist + pre-flight + the "prove it moves" check, output findings. **Changes nothing.** | `anti-cheap-motion.md` + `preflight.md` |

### Routing rules

1. **First word matches a command** → load that command's reference and follow it. Everything after is the target. **The §0 env gate still runs first for any command that writes or renders** (`craft`, `engine`, `beats`, `reveals`, `sound`, `restage`, `slower`, `faster`, `register`) — you cannot edit a composition into a runtime that isn't there. `env` and `audit` may run without it.
2. **First word doesn't match, but intent clearly maps** ("feels frantic / too much" → `slower`; "too flat / boring / dead" → `faster`; "wrong effect / this vibe is off" → `engine`; "the timing is off / drags in the middle" → `beats`; "text all comes in the same way / entrances are boring" → `reveals`; "wrong music / 换配乐 / 音效不对 / 音画不同步" → `sound`; "make it vertical / 竖屏 / for 抖音" → `register`; "improve / fix this clip" → `restage`; "is this any good / review it" → `audit`) → route there. If two fit, ask once.
3. **No argument at all** (bare `/frame-smith`) → the user is asking *"what should I do here?"* Read cheap signals and lead with the 2–3 highest-value picks, each with a one-line reason. Signal → pick:
   - **no runtime detected** → lead with `env` (nothing else works until a runtime is present).
   - **runtime present, nothing built** → `craft` (name the register you'd default to).
   - **an existing composition in the working tree** → scope `audit` or `restage` to it, naming the file.
   Keep it to 2–3 pointed picks. The table is the fallback, not the lede.
4. **A target but no command, building new** → run the full `craft` flow (§0 env gate → §8), the default for "make me a promo video / a HyperFrame clip".
5. **`env` and `audit` are read-only.** `env` reports runtime status and never writes; `audit` reports findings and never edits. Every other command may modify the target.

> Auto-trigger is unchanged: frame-smith still activates from natural language via its `description`. Commands are an **added** precision entry-point, not a replacement.

---

## 0. THE ENVIRONMENT GATE (Before Anything Else) · hard requirement

**frame-smith cannot ship a video on its own.** It writes a Remotion composition; something has to host and render it. That something is one of two skills:

| Runtime skill | What it provides | frame-smith writes into |
|---|---|---|
| `hyperframe` | The **effect-template library** (the shipped HyperFrames) **plus** its own Remotion project. The richer path — you lift patterns from `effect-catalog.md`'s source frames directly. | its `src/compositions/HyperFrames/` (or the folder it exposes) |
| `remotion` | The **bare runtime** — scaffolding, `remotion studio`, `remotion render`, the `<Composition>` registry — without the template library. The leaner path. | its `src/compositions/` |

**The check (full steps in `references/environment.md`):**

1. Look for the two skills in the available-skills listing and on disk (project `.claude/skills/`, `~/.claude/skills/`, installed plugins). **At least one must be present.**
2. **Neither present** → **STOP. Write nothing.** Report it plainly and offer the install path: recommend `hyperframe` first (it carries the effects), `remotion` as the runtime-only alternative. If the user already has a Remotion project on disk but no skill, `environment.md` covers pointing frame-smith at it directly as a fallback (ask for the path — never assume it).
3. **One present** → record **which**, because it decides the target directory, the registration file, and the preview/render command. Then continue to §0.A.

> Do not soften this gate. Writing a beautiful composition into a project with no Remotion installed produces a file the user cannot run — that is a worse outcome than stopping and asking.

### 0.A Determine the Register (this forks orientation, safe zones, and copy)

- **cinematic** — a landscape HyperFrame clip: `1920×1080 · 30fps`, ~12–24s, **pure visual, no voiceover**, ends on a wordmark/logo payoff. This is the default when the brief says "宣传片 / opener / 片头 / showcase / HyperFrame / 电影感" or names one of the four reference frames. Route: heavy effect engine (§4), no safe-zone tax.
- **short** — a vertical short-video: `1080×1920`, for 抖音/小红书/视频号, may carry **subtitles + voiceover**, hook must land in the first ~1.5s. This is the register when the brief says "竖屏 / 抖音 / 小红书 / 短视频 / 口播 / 带字幕". Route: `S = width/720` scale on every pixel, 抖音 safe zones, subtitle rhythm (`motion-floor.md`).

**If the brief doesn't say, ask ONE question** — orientation changes every downstream number, so guessing wrong is expensive: *"这个视频是横屏电影感片头（无旁白），还是竖屏短视频（可能带字幕/口播）？"* Wait for the answer.

### 0.B Output a "Frame Read" before generating — assert a direction, don't poll

Name the rejected default first, then the direction. Three lines:

```
Lazy default (rejected): {the obvious motion cliché for this brief}
Frame Read: {subject} · {mood in 2–3 words} · register={cinematic|short} ·
            engine={the one effect engine} · duration={n}s · ENERGY={n} SPECTACLE={n} DENSITY={n}
Beats: {H0 hook} → {H1 …} → {Hn payoff}   (one line, seconds marked)
```

Example:
```
Lazy default (rejected): logo fades in, three feature cards slide up one after another, soft synth.
Frame Read: developer-tool launch · precise + kinetic · register=cinematic ·
            engine=poster-cube tumble · duration=15s · ENERGY=6 SPECTACLE=8 DENSITY=4
Beats: 0.0 ruler+labels in → 2.9 cube enters → 3.7 tumble → 10.0 drift+wordmark → 12.6 accent flash outro
```

**STOP after the Frame Read. Do not generate any code yet.** Wait for confirmation or redirect. Assert the direction and invite a veto ("going with the cube unless you'd rather I push it toward a data-pulse read"). Do **not** hand the user a menu of adjectives — nobody picks a motion from words. If the brief genuinely forks (a launch that could be a hard-kinetic cube *or* a warm particle album), describe the two and let them choose one.

### 0.C Anti-Default Discipline

Name the motion cliché for this brief, then beat it. "Product launch → the default is *logo fade + three cards sliding up in sequence + soft riser*. I'm rejecting that for {a real effect engine with a beat arc}." The single most-tested motion tell is **everything entering the same way** (fade + translateY, `linear` or a single soft ease, all at once). See `references/anti-cheap-motion.md`.

### 0.D Quick-Start Dial Mapping

| Brief cue | ENERGY | SPECTACLE | DENSITY |
|-----------|--------|-----------|---------|
| "电影感 / cinematic / 高级" | 5 | 8 | 3 |
| "科技 / 数据 / dashboard 视频" | 6 | 7 | 7 |
| "温暖 / 回忆 / 相册 / 情感" | 4 | 7 | 4 |
| "活力 / 潮 / 撞色 / 年轻" | 8 | 6 | 5 |
| "简约 / 克制 / 品牌片头" | 3 | 5 | 2 |
| "抖音 / 短视频 / 口播带字幕" | 6 | 4 | 5 |
| "产品发布 / launch / opener" | 6 | 8 | 4 |

Override immediately if the brief provides stronger signals.

---

## 1. THE THREE DIALS

Set these explicitly from the Frame Read. They drive tempo, engine ambition, and how much is on screen.

| Dial | 1–3 | 4–6 | 7–10 |
|------|-----|-----|------|
| **ENERGY** — tempo & attack of the motion | slow, floated, long holds, soft eases | measured, clear beats | fast cuts, overshoot, snappy `back`/`exp` eases, tight holds |
| **SPECTACLE** — how technically-ambitious the effect engine is *(frame-smith's signature dial)* | CSS transforms + fades | staggered reveals, one 3D moment, Canvas accents | full CSS-3D solid, particle systems, mask theme-flip, camera sway, motion blur |
| **DENSITY** — information on screen per beat | one idea per beat, airy | balanced | data-rich, multi-panel, editorial overlay |

### 1.A "Spectacle claimed, spectacle shown" (mandatory)

If `SPECTACLE ≥ 7`, the clip MUST actually contain a working engine (a real CSS-3D solid, a particle burst, a mask theme-flip, a counter/network build) that **holds through its beat and lands a clean terminal frame** — not a gradient that pulses. A clip that claims SPECTACLE 8 but ships crossfades is broken. If you can't ship working spectacle in scope, drop the dial to 4–5 and ship an impeccably-timed simpler clip instead. **Never half-build an engine that janks or cuts off mid-motion** — an interrupted 3D tumble reads cheaper than no 3D at all.

---

## 2. PICK ONE EFFECT ENGINE (the video's soul) · `references/effect-catalog.md`

> A video's identity is its **one** engine, executed fully. The catalog is organized around the four shipped reference frames — treat them as *validated combinations*, not a menu to copy verbatim.

| Engine | Use when | Signature technique |
|---|---|---|
| **Poster-cube tumble** | many small visuals (posters, shots, thumbnails), editorial/design brand, "portfolio / studio / gallery" | CSS-3D cube (`perspective` + `preserve-3d` + per-face transforms), piecewise-pose timeline, drift phase, ruler-grid + wordmark overlay |
| **Capsule theme-flip** | a light→dark reveal, "before/after", playful candy brand, a hero that transforms | `spring` entrances, spec-table transitions, a **stadium/pill mask** expanding from center to sweep the whole frame from light theme to dark |
| **Architecture data-pulse** | data/metrics story, real photography, "numbers that matter", B2B/infra | 7-beat structure, **trapezoid** in/out envelopes, data panels + **network lines** + **big-number counters** + **gallery wipe** transitions |
| **Particle-burst album** | photos, memories, emotional/warm, "our year / our story", personal | **SVG stroke-writing** title + particle burst, **3D ring carousel** with depth-of-field + camera sway, card-stack suck-in with motion blur, `spring` overshoot explode |

**Discipline (mandatory):**
- **One engine per clip.** Don't stack a cube *and* a ring *and* a data-pulse. Reusable sub-effects (a counter, a wipe, an overlay grid) can garnish, but there is one load-bearing engine.
- **Progressive enhancement of legibility.** If the engine were frozen on any frame, the frame should still read. The engine carries motion, not meaning-of-last-resort.
- **60fps or simplify.** Animate `transform`/`opacity` only; never `top/left/width/height`. Below smooth, cut particle count / face count / resolution — don't ship jank.
- **Terminal frame is designed, not incidental.** The engine resolves to a composed still that the `…Cover` export can freeze (see `motion-floor.md` + `registration.md`).

---

## 3. THE MOTION CRAFT FLOOR (why it reads as expensive) · `references/motion-floor.md`

The difference between a cheap clip and an expensive one is mostly timing discipline, applied consistently. Non-negotiables (full recipes in the reference):

- **30fps, and time is authored in seconds.** `const FPS = 30; const f = (s) => Math.round(s*FPS);` — every beat boundary and delay is `f(seconds)`, never a raw frame count guessed by hand.
- **`interpolate` always clamps.** `const clampOpts = { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' };` on every `interpolate` that maps a time range — an unclamped ramp keeps moving past its beat and is the #1 cause of drift.
- **Easing over `linear`.** Entrances `Easing.out(cubic/exp)`, overshoot `Easing.out(back(…))` or `spring`, holds are real holds (flat segments in a piecewise `interpolate`). `linear` on a visible move is a tell.
- **Vertical obeys the scale system.** `const S = width/720;` and **every** absolute pixel (`fontSize`, `top`, `padding`, `borderRadius`) is `× S`. Landscape at fixed 1920 does not need it, but keep the values proportional.
- **Vertical obeys the 抖音 safe zones** — top ≥ 160px, bottom ≥ 220px, left ≥ 44px, right ≥ 120px (1080p). Content outside is covered by platform UI. (Landscape has no safe-zone tax.)
- **The export三件套** — every composition exports `Component`, `ComponentCover` (a still, usually a taller crop), and `COMPONENT_FRAMES` (the duration constant). This is the contract `registration.md` consumes.

> Author motion the way a page authors color: pick the easing/tempo vocabulary once, lock it, and don't let a single element drift into `linear` + 0.5s-uniform like everything the model has seen most.

---

## 4. BEAT TIMELINE — a video is beats, not a page · `references/beat-structure.md`

Fix the beats in seconds before writing render code. Each beat has **one job**; the boundaries are named constants.

```ts
const H0 = f(0);      // hook / cold open
const H1 = f(2.0);    // establish
const H2 = f(5.0);    // develop (the engine's main move)
const H3 = f(9.0);    // peak
const H4 = f(12.0);   // resolve
const HEND = f(15.0); // payoff (wordmark / logo / CTA)
export const X_FRAMES = HEND;
```

Rules that hold across registers:
- **The first beat earns the next second.** Cinematic: the engine or its promise is on screen fast; a 3s empty runway loses the frame. Short: **the hook lands by ~1.5s** or the viewer swipes.
- **One job per beat.** A beat that both introduces the product *and* flips the theme *and* runs the counters is three beats crushed into one — the eye can't parse it.
- **The last beat lands.** A clip that just *stops* on its last engine frame feels unfinished. End on a designed payoff: the wordmark settling, the logo resolving, the accent line flashing, the matrix collapsing to a title. This frame is also your `…Cover` still.
- **No dead air.** Every beat is either moving or holding-with-intent. A stretch where nothing changes and nothing is deliberately held is a cut you owe the viewer.

Narrative skeletons per register live in the reference (cinematic: *cold-open → engine build → peak → wordmark*; short: *hook → point → proof → payoff*, cut to narration). Motion-motivated only — every move needs a one-sentence reason.

---

## 5. WRITE & REGISTER · `references/registration.md`

Writing the `.tsx` is not the end — an unregistered composition doesn't exist in Studio and can't render.

- **Export三件套:** `export const X_FRAMES = HEND;`, `export const X: React.FC = () => {…}`, `export const XCover: React.FC = () => <Scene frame={f(peakSecond)} />;`. The cover freezes the most composed frame.
- **Register the pair** in the runtime's Root: a `<Composition id="X" … durationInFrames={X_FRAMES} fps={30} width={…} height={…} />` and a `<Composition id="XCover" … durationInFrames={1} … height={taller-crop} />`, inside the right `<Folder>`.
- **Preview or render to prove it moves** — open it in `remotion studio`, or render a still/short range. A composition you never previewed is a composition you haven't finished (§8).

---

## 6. THE ANTI-CHEAP-MOTION BLACKLIST · `references/anti-cheap-motion.md`

Before declaring done, scan against the reference. The headline offenders:

- **Everything enters the same way** — fade + `translateY` on every element, all at once. The #1 motion tell. Stagger, vary the vector, give the hero its own move.
- **`linear` easing** on any visible move, and **uniform 0.5s durations** everywhere — motion with no dynamics reads as a slideshow.
- **No overshoot / no anticipation** — nothing ever `spring`s past and settles; everything glides to a dead stop. Flat.
- **An engine that janks or cuts off** mid-motion — a 3D tumble that stutters, a particle burst that pops out, a mask sweep that tears. Worse than not attempting it.
- **Dead-air beats** and a **last frame that just freezes** with no designed payoff.
- **Animating `top/left/width/height`** instead of `transform/opacity` — the jank source.
- **Subtitles/CTA outside the 抖音 safe zone** (short) — clipped by platform UI.
- **Reused stock motion** — the exact ScrollReveal-style fade-up-stagger from every template gallery. Earn the motion.

---

## 7. PERFORMANCE & CORRECTNESS GUARDRAILS

- Animate `transform`/`opacity` only. Never `top/left/width/height`.
- Every `interpolate` over a time range **clamps** (`clampOpts`). Piecewise pose channels must be monotonic in their input array.
- `durationInFrames` must equal the exported `X_FRAMES`; a mismatch cuts the clip or leaves dead tail.
- Assets via `staticFile()` or a stable absolute URL (`assets.md`) — never a bare relative path that breaks in render.
- **Reduced-motion / terminal frame:** the clip must resolve to a clean, composed last frame (the payoff) that the `…Cover` can freeze. A still viewer must get a finished poster, not a mid-transition smear.
- Vertical: `S`-scale every pixel; keep content inside the safe zones; subtitles split by punctuation and switch on the narration beat (`motion-floor.md`).

---

## 8. PRE-FLIGHT CHECK · `references/preflight.md`

Run the full checklist before saying "done." It merges the craft-floor check, the anti-slop scan, the safe-zone check (short), the registration check, the reduced-motion/terminal-frame state, and the **prove-it-moves** step (Studio preview or still render). If any hard rule fails, it is shipping broken work — fix before delivery.

---

## 8.A POST-DELIVERY ITERATION GUIDE

Map feedback to the targeted fix. **Never rebuild from scratch for one complaint.**

| User says | Command | Action |
|-----------|---------|--------|
| "too frantic / too much" | `slower` | Stretch the timeline, soften eases, lower ENERGY |
| "too flat / boring / dead" | `faster` | Compress holds, add overshoot, raise ENERGY |
| "wrong effect / vibe is off" | `engine` | Re-pick from `effect-catalog.md`, keep the beats |
| "timing's off / drags in the middle" | `beats` | Re-cut `Hn` boundaries, kill the dead-air beat |
| "make it vertical / 竖屏 / 抖音" | `register` | Re-lay scale + safe zones, re-fit the engine |
| "the ending's weak" | `beats` | Redesign the payoff beat; make the last frame land |
| "it janks / stutters" | `restage` | Move to `transform/opacity`, cut particle/face count, re-check 60fps |
| "is this any good / review it" | `audit` | Read-only: blacklist + pre-flight + prove-it-moves |

---

## 9. OUT OF SCOPE

frame-smith is a **motion director for Remotion compositions**. Hand off when the work is: live-action video editing (no code), a pure audio task, a static image/poster (that's a design-skill job, not motion), or anything that needs a video runtime frame-smith's §0 gate can't find and the user won't install. It does **not** own the runtime — if there is no `hyperframe`/`remotion` skill and no Remotion project on disk, frame-smith's job is to say so and guide install, not to fake a render.
