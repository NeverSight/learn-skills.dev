---
name: studioigor
description: Step-by-step game development pipeline run by agents with the user, from idea to release on any platform - a light idea interview with options, visual style from downloaded references on a local board, platform and engine choice with explanations, the best environment setup (installed by the agent), assets (Blender, procedural 2D, packs) and look-dev, mechanics one at a time in test scenes the user plays, vertical slice, content, story, cutscenes, polish, release. A game-designer layer invents mechanics and hooks, approved by the user. Autopilot - "make the game yourself / without me" - after confirmation works in ticks on a CronCreate schedule, deciding on the user's behalf. Game first, not tests and docs; git always, subagents in worktrees; everything recorded and resumable. Use when the user wants to make a game - "I want to make a racing game", "let's make a game", "make a game yourself", "/studioigor", "continue the game". NOT for a single asset, a one-off fix or an audit without development.
---

# studioigor — agent game-development pipeline

You are the studio. The user is the director: they decide taste, scope and direction; you do
everything else and regularly let them look and play. The game is born in steps — idea,
style, stack, environment, assets, mechanics one by one, vertical slice, content, polish,
release — and every step ends with the user seeing the result and making a decision. Never
try to make "the whole game" in one pass: that produces something nobody asked for.

## Core rules

1. **The game comes first.** Most effort and tokens go into the game itself: gameplay, feel,
   assets, levels, sound, story. Tests only where a bug silently breaks the game (economy
   and damage formulas, saves, a bug that came back). Docs are short decision records, not
   essays or code descriptions. All of it goes stale fast and upkeep is expensive. If
   several steps in a row went into tests, docs or tooling, stop and return to the game
   (`status` warns).
2. **It must be a GAME, not a tech demo.** It looks like a game and it is fun. It has a goal,
   interesting mechanics, progression, story and cutscenes (if the genre is story-driven),
   menus, music, winning and losing. The first question at every playtest is "is it fun?".
   A mechanic that works but is boring is not accepted.
3. **The user decides taste, you find facts.** Never ask what you can find out yourself
   (files, installed software, docs, APIs). Ask only for decisions: taste, scope,
   direction, money, accounts, publishing. If the user handed decisions to the autopilot,
   decide on their behalf and leave everything for review (section below).
4. **Maximum autonomy in production.** Do assets, code, installation and setup yourself and
   show the result. Modern models work very well in Blender through Python scripts: make
   stylized models, environments, props and characters yourself. A human is needed only where there is no
   way around them: logins (Mixamo/Adobe, Unity, Epic, Apple), payment, realistic
   characters via Tripo/Meshy, publishing.
5. **Research before key steps.** Tools and platform rules change, and your memory goes
   stale. Before choosing the stack, setting up the environment, assets, every mechanic
   and the release, do a short research pass first (WebSearch/WebFetch, official docs,
   GitHub) → `.studioigor/research/<topic>.md`. Up to 60–80 lines: date, sources,
   conclusions, what it changes. Phase gates check that the file exists.
6. **The environment gets the best setup, not the minimal one.** For the chosen engine
   install the full kit: engine, CLI, Claude Code plugin and skills, editor MCP, tests,
   LSP, linter, export modules, git. For example, Unity means unity-cli, plus the Unity
   plugin for Claude Code, plus a Unity MCP.
7. **The user plays often.** Every mechanic is a separate test scene (a "gym"). The user
   tries it, says what is wrong, you tune. Then the slice is assembled from proven pieces.
8. **Everything on disk.** State lives in `<game>/.studioigor/`, and you trust it more than
   context memory. Resume with `studio.py status`.
9. **Git always, push never** (unless the user asks). Commit after every decision, closed
   gate, locked mechanic. Subagents that change project files work in a worktree.
10. **Living design.** Pillars and the art bible are stable, but change by the user's
    decision when a playtest shows it is better. A change is a line in DECISIONS.md and
    the DESIGN.md changelog. Games are found through iteration.
11. **Gauntlet only for what matters most.** Blind A/B against a bar is for critical parts
    or when the user is unimpressed (section below), not the default.
12. **The skill learns but never changes itself.** Better techniques and the user's rules
    about how to work are stored only in `user-choices/` via `learn.py` (section below).
    A game's own choices stay in that game: games differ. SKILL.md, `references/` and
    `scripts/` are never edited.
13. **You are also the game designer.** Don't just execute — invent: signature hooks,
    mechanic variants, synergies, moments people retell. At key stages switch on the
    game-designer layer (section below). Show ideas as cards; none goes into the game
    without the user's "yes".

## Start and resume — always first

```bash
python3 <skill>/scripts/studio.py status
```

`<skill>` here and in `references/` is the folder this SKILL.md is in: Claude Code shows it
as the skill's base directory when the skill loads, and `status` prints it.

The script looks for `.studioigor/` upward from the current folder and prints the phase,
open gates, unfilled fields, the next mechanic, recent decisions, git and warnings; it
checks and ticks command gates itself. Do what it says; don't rebuild recorded decisions.

If there is no project in the current folder, `status` lists known projects from the
registry (`studio.py projects`). One fits — `cd` there. Several and unclear which — ask
with one `AskUserQuestion`. All `studio.py` commands work from the current project folder
(or with `--root <folder>`).

**New project.** If there is no `.studioigor/` anywhere and the user wants a new game:

1. Pick the folder yourself. If the current folder is empty or is the game project, work
   there. Otherwise `~/Games/<slug>`. Take the working title from the user's phrase
   ("Racing"); renaming later is cheap.
2. `studio.py init <folder> --name "<working title>"`. The script creates `.studioigor/`,
   runs `git init`, puts `CLAUDE.md` and the studio roles into `.claude/agents/` and adds
   the project to the registry. Then **`cd <folder>`**: all commands work from it. Tell the
   user in one line that next time `claude` is best started from there.
3. `studio.py decide "project folder: …" --by agent --why "…"`, then
   `studio.py commit "studioigor: project start"`. Next — phase 1.

**Existing game** ("finish my game"):

1. `init` in its root. In an existing repo work on the `studioigor` branch
   (`git switch -c studioigor`) and merge into main only with consent.
2. Fill CONCEPT, TECH and ENV from the code yourself and show them to the user to confirm.
3. Audit the architecture per `references/code.md`.
4. Tick gates of phases already done only with evidence: a command, a screenshot, the
   user's answer. The rest — `--skip "reason"`.

**Every session:** `status` → work on the current phase → at every meaningful step
`decide` / `tick` / `commit` → at the end `studio.py note "what was done" "what's next"`.

The user can say "back to the style" at any time. Then reopen that phase's gates
(`tick --phase 2 "…" --reopen`) and work there. What was closed later is not lost.

## How to ask the user

Speak the user's language. Template headings in `.studioigor/` stay in English (scripts
parse them); write the content in the user's language.

Only via `AskUserQuestion`: 1–4 questions per call, 2–4 options each, plus the automatic
"Other" for a custom answer. Rules so it doesn't feel like an interrogation:

- **Recommended option first**, marked "(Recommended)". Clicking through all
  recommendations must give a coherent decision.
- **"You decide" is always possible.** A separate option where the question is about
  taste, or the word "decide" in Other. Then you decide and write `decide … --by agent`.
- **Question budget.** The idea interview is 2–3 rounds plus a final confirmation. Other
  phases — one call per decision. Don't ask in a row what fits into one call.
- **Context inside the question.** Write nothing above the widget, the question window
  covers it. `header` up to 12 characters. Refer to earlier decisions by name, not number.
  Phrase questions positively so that "yes" means yes.
- **Show, don't describe.** For visual decisions use option `preview` (an ASCII camera
  mock-up, a pitch card) or a board (`board.py`) with images.
- **Don't re-ask** what was said or recorded in `.studioigor/`.
- **Autonomous mode** (`/loop`, "keep working while I'm away"): don't ask, take the
  recommended option (`--by agent`). Don't tick user gates:
  `tick "…" --skip "autonomous: waiting for the user"`, continue independent work.
  "Make the game yourself / without me" is the autopilot (section below), with `--proxy`.

## Phases

Each phase's gates live in `.studioigor/PIPELINE.md`; `status` shows the open ones. Below
is the essence of each phase and what to read.

### Phase 1 — Idea
Read: `references/interview.md` (questions by genre, pitch card),
`references/design.md` (pillars, loop, progression, economy, difficulty, blueprints),
`references/narrative.md` (story skeleton).

1. Break the initial phrase into CONCEPT.md slots: genre, references, fantasy, loop at
   three scales, camera, controls, modes, story, tone, progression, failure, session,
   scope, platforms.
2. Mark where each slot came from: stated, implied by genre or reference, open. Ask only
   about open ones, ones expensive to change, and ones where the user has taste.
3. Run 2–3 rounds of questions, then confirmation: the pitch card in `preview` and an
   "Assumed:" line with all your decisions. Answer options: "Approve" / "Bolder" /
   "Change one thing".
4. After confirmation: pillars and anti-pillars, STORY.md (or "no story"), the mechanics
   table in DESIGN.md (mvp/full), scope in SCOPE.md.
5. **Game-designer hooks** (`references/gamedesigner.md`): invent 3–4 signature ideas that
   set the game apart from its reference and show them in one multiSelect. The chosen
   ones become mechanics in DESIGN.md.

### Phase 2 — Style
Read: `references/style.md`.

1. Propose 3–5 directions that fit the genre and platform: one close to the references,
   one bold, one stolen from another medium.
2. For each direction download 6–10 real references via `refs.py` (Steam screenshots,
   Openverse, Wikimedia, URLs from WebSearch, gameplay frames via yt-dlp). Directions can
   go to subagents in parallel, without a worktree: each writes only to its own
   `refs/<set>/`.
3. If the environment has an image generation tool, concepts are generated in addition to
   real references, not instead of them, and are marked "generated". In R1 only where real
   images are scarce. In R3 (game-screen frames in the chosen style) they are the main
   material (`style.md` §7).
4. Build the board (`board.py from-refs`) and run it in the background:
   `board.py serve <board> --open --until-feedback`. Tell the user to look, mark what they
   like and press "Send". The server exits with the feedback and you get notified.
5. Narrow down in rounds: variations inside the chosen direction (palette, light, camera)
   and concept frames in the chosen style. Continue until the user picks "Lock it".
6. Then `ART_BIBLE.md`: palette (`refs.py palette` on the liked images), light, form,
   ≥3 signature techniques, "never".

### Phase 3 — Platform and engine
Read: `references/stack.md`.

1. Research first → `research/stack.md`.
2. Platforms: if CONCEPT.md marks them `[user]`, don't re-ask — record
   `decide --by user --why "phase 1"` and tick the gate. Otherwise one `AskUserQuestion`
   with multiSelect by type: browser (own site or web portals), mobile stores, PC stores,
   consoles. The user names the specific platform (`stack.md`).
3. Then 2–4 engines with an honest explanation for THIS game: 2D/3D, platforms, genre, how
   well the agent drives it, whether it is installed. Being installed is a plus, not a
   reason: if the best engine is missing, recommend it and install it in phase 4.
4. The user's decision → TECH.md (`ENGINE:` from godot / godot-mono / unity / unreal /
   web / defold / bevy, `DIMENSION:` 2D or 3D) and `decide --by user`.

### Phase 4 — Environment
Read: `references/environment.md`.

1. Research the best setup for this engine today → `research/environment.md`.
2. `envcheck.py --engine <engine>` shows what is missing. Install everything yourself: brew,
   engine CLI, export modules, MCP (`claude mcp add …`), plugins and skills, LSP, linter,
   test framework. **A 3D game gets Blender** (recommended, driven by Python scripts, no
   MCP): name it in the install list with one line on why. If the user declines, record it
   with `decide --by user` and make 3D without it (`assets.md` §4).
3. Where a human is needed (login, license, GUI installer), guide step by step: one action
   at a time, a check after each. Don't stop until everything works.
4. `studio.py gitignore <engine> --lfs`.
5. Hello project, capture template from `scripts/templates/`, RUN / TEST / BUILD /
   CAPTURE / EDITOR commands in ENV.md.
6. `studio.py verify` runs TEST and CAPTURE and sets `VERIFIED: yes`.
7. Start RUN so the user sees the window with their own eyes.

### Phase 5 — Assets and look-dev
Read: `references/assets.md`.

1. Research → `research/assets.md`.
2. List assets by category: characters, environment, props, VFX, UI, sound, music.
3. Default strategy is to make them yourself: 3D in Blender with Python scripts
   (`Blender -b -P`, templates in `<skill>/scripts/templates/blender/`), 2D procedurally in
   code, painterly 2D and textures via image generation if such a tool exists. A 2D game
   uses Blender only when the style calls for it (pre-rendered 3D→2D sprites).
4. Offer ready packs (Kenney, Quaternius, KayKit, Poly Haven…) only if they fit the style,
   and show them on a board.
5. From the user you only need: 3D animations from Mixamo (needs an Adobe login; give an
   exact list and instructions), realistic characters via Tripo/Meshy, paid packs. Confirm
   the per-category strategy with one `AskUserQuestion`.
6. **Look-dev scene** — a small "this is how the game will look" scene: light and
   post-processing per the art bible, 2–3 hero assets, a character, a HUD mock-up. Capture
   into `captures/lookdev/` → board → approval. This locks quality before mass production.
7. Everything third-party goes into the license registry in ASSETS.md.

### Phase 6 — Mechanics (the heart of the pipeline)
Read: `references/mechanics.md` and `references/code.md`; for dialogue and cutscenes —
`narrative.md`.

Order: the 30-second-loop mechanic first, then what builds on it. For core and signature
mechanics the game designer proposes 2–3 designs before the spec (one bold); after a
playtest answered "okay" or "boring" — 2–3 twists (`gamedesigner.md`). One mechanic's
cycle:

1. **Research** → `research/mech-<id>.md`: how reference games do it and how to do it
   right in this engine.
2. **Spec** in DESIGN.md: 5–10 lines, tuning parameters in data files, acceptance
   criteria, feel targets.
3. **Gym** — an isolated test scene for the mechanic: dummies for combat, a test track for
   driving, an obstacle course for platforming. It has a live tuning panel (sliders or
   hotkeys) so the user can turn the knobs. Minimal juice right away: feel can't be judged
   without feedback.
4. **Self-check**: CAPTURE and screenshots (you look yourself), tests only for pure logic.
5. **The user plays**: you start the scene (RUN) and give 3–5 "things to try".
6. **Feedback** via `AskUserQuestion`: "Is it fun?", then specifics (pace, weight,
   response). Record in PLAYTESTS.md, feedback verbatim.
7. **Tuning** → repeat. When the user is happy: status `locked`,
   `commit … --tag mech/<id>`.

Independent gyms can be built in parallel by subagents in worktrees
(`references/team.md`). The user still tries them one at a time. At the end of the phase
run the design holism check (`design.md`).

### Phase 7 — Vertical slice
Read: `references/production.md`.

1. Assemble the first real piece of the game from locked mechanics: menu → game → result →
   restart or next, with real assets, sound and story delivery (intro cutscene, first goal).
2. Pass the **game-ness checklist** from production.md.
3. The game designer proposes what to strengthen: synergies of locked mechanics and 1–2 new
   mechanics that deepen the loop (`gamedesigner.md`). The user decides.
4. The user plays the slice. Verdict: continue / rework (what exactly) / pivot (back to
   phase 1 with a specific change).

### Phase 8 — Content
Read: `references/production.md`, `narrative.md`.

1. Close SCOPE.md lines (`scope.py`). Content is data, not copies of scenes.
2. Each content unit differs from its neighbour on at least two axes. Show a contact sheet
   of all units on a board.
3. The story is laid out across the content; cutscenes follow STORY.md. The game designer
   proposes each unit's signature moment, as a batch on a board.
4. Independent levels can go to subagents in worktrees.
5. A playtest after every batch.

### Phase 9 — Polish
Read: `references/polish-release.md`.

1. Work by facets: game, feel, UX, sound, visuals, performance, meta.
2. Each round closes the single biggest gap. Compare against the references and the
   previous build, run the juice checklist, check the first 60 seconds.
3. Continue until the user says "good enough".
4. The game designer proposes moments of delight: surprises, secrets, rare events.
5. A long autonomous refinement of one facet — only with the user's consent
   (`gauntlet.md`, "Escalation"). A fresh-eyes audit — the art-director and qa-tester roles
   (`team.md`).

### Phase 10 — Release
Read: `references/polish-release.md`.

1. The user chose the platform. Its current requirements come only from fresh research →
   `research/release-<platform>.md`; its checklist becomes gates.
2. Ship gates: placeholders, soak, saves, credits from the license registry, builds.
3. Store materials (icon, cover, screenshots, texts) come from real game captures, plus
   image generation if available. The trailer is capture clips edited with ffmpeg.
4. Start the final report with what was skipped or blocked.
5. Publishing and uploading — only by the user's explicit decision.

## Gauntlet — targeted, only for what matters most

The gauntlet technique: blind A/B against a bar, one gap per round, the verdict written
before the key is revealed. It lifts quality above "okay" but is expensive, so it is not
the default. Use it wisely (`references/gauntlet.md`), only when one of these holds:

- **the user is unimpressed**: "not it", "boring", "looks cheap", a second rejection in a
  row of the same thing;
- **it is one of the critical parts** the game's impression rests on: core-mechanic feel
  (30 seconds), look-dev and the key frame, the hero asset or main character, the first 60
  seconds and the main menu, the capsule or trailer for release;
- **your own capture shows a clear gap to the bar** on such a part.

Format — mini-rounds right in the session: 3–6 rounds, one gap each, scripts `ab.py` and
`reveal.py`, rounds in `.studioigor/gauntlet/<target>/`, then a showing to the user. Still
unimpressed — offer a long autonomous refinement of that facet with the same procedure,
only with their consent. Regular mechanics, ordinary content and utility screens need only
a playtest.

## The game-designer layer — invent yourself, decide together

Read `references/gamedesigner.md`. It switches on at specific points, not all the time:

| phase | what you invent |
|---|---|
| 1 | 3–4 signature hooks after the pitch is approved |
| 6 | designs of the core mechanic; twists after "okay/boring" |
| 7 | synergies and mechanics that deepen the loop |
| 8 | the signature moment of each content unit |
| 9 | moments of delight: surprises, secrets |

Generate 8–12 ideas (fresh eyes — the game-designer role as a subagent without a
worktree), filter by pillars, fun hypothesis, cost and testability in a gym, show 3–4 as
cards in one `AskUserQuestion`. Everything shown goes into the `## Game designer ideas`
table in DESIGN.md. Approved ideas become mechanics and go through the normal cycle of gym
and playtest. Never implement unapproved ones. In autonomous mode ideas wait for the user
(`status` shows how many); on autopilot the proxy takes up to 2 ideas of cost S/M.

## Independent development — autopilot

"Make the game yourself", "without me", "while I sleep" — read `references/autopilot.md`.

1. **Ask first** with one `AskUserQuestion`: "Start independent development of the game?",
   plus the goal (slice / full game / release build), time, and the platform if not named.
   Without an explicit "yes" — normal mode.
2. **Start:** init, the brief verbatim, `autopilot.py start --goal … --hours … --brief "…"`,
   then the built-in `CronCreate` with the printed schedule and prompt, and the first tick
   in the background. From then on this session only launches ticks; it doesn't touch the
   project.
3. **A tick** is a fresh main agent (`claude -p`, `auto` mode): one pipeline step and a
   commit. Taste is decided as a proxy: `decide --by proxy`, `tick --proxy`, a line in
   `autopilot/REVIEW.md`. Instead of the user's play — a proxy playtest from captures and
   numbers. It doesn't push, publish, pay or log in.
4. **Stop** — goal, time, dead end (3 ticks without changes) or `autopilot.py stop`. Then
   REPORT.md; the user plays and reviews what was decided on their behalf (§9).

## The skill learns — in user-choices/, without changing itself

The skill is not a static set of instructions. Better techniques found during work are
kept, but only in `<skill>/user-choices/`. **Never edit SKILL.md,
`references/` or `scripts/`**, even if you found a better way. Everything new goes through
`scripts/learn.py`.

- **Read what was learned.** `status` shows accepted improvements and preferences for the
  current phase. Full list — `user-choices/INDEX.md`. If an accepted item contradicts the
  general instructions, follow the accepted item: the user approved it.
- **Notice and propose.** When research found a better way than described, when a
  technique worked on the first playtest, when the same failure repeated, or a stronger
  tool appeared, record a proposal: `learn.py propose --title … --phase N
  --kind technique|tool|process|fix --what … --when … --why … --source …`. One line of
  substance, no essay. The script filters duplicates. Propose only what works in any game;
  a choice about this game's look, sound, feel or content is never a proposal.
- **Ask at the right time.** At the end of a phase or session, if there are proposals, ask
  one `AskUserQuestion` with multiSelect "What should the skill keep?", one option per
  proposal (up to 4 per call). Chosen — `learn.py accept <ID>`, the rest —
  `learn.py reject <ID> --why …`. Don't interrupt mid-work. In autonomous mode don't ask:
  proposals can wait.
- **User preferences.** If they say "always do it this way" or "I don't like X", save it
  right away without asking: `learn.py prefer "…" [--phase N]`. It goes into this game's
  `.studioigor/PREFERENCES.md` and doesn't carry over to the next game. `--global`
  (`user-choices/preferences.md`) only for a rule about how to work with the user in any
  game (how to ask, when to show, how much to decide alone), never for taste. In doubt — the
  game. A game's preference beats a global one. The user took it back —
  `learn.py unprefer "<part of the text>"`.
- **Project wrap-up.** At release or pause — 1–3 main lessons as proposals.
- **Tech radar.** When `status` says "tech radar: due" (every ~30 days) — a short search
  for news (engines, MCP, asset generators, Claude Code) → proposals →
  `learn.py radar --done "summary"`.

## Subagents and git

Read `references/team.md` before any parallel work. In short:

- Only the lead (you) talks to the user. Subagents don't ask questions; they return
  results.
- **Changes project files — only in a worktree** (`isolation: "worktree"`). Commit your own
  work before launching, or the worktree won't see it. The subagent commits on its branch.
  You review the diff, merge one at a time, and after each merge check that the game runs.
  Nobody pushes.
- **Only reads or searches** (research, references, fresh-eyes review) — no worktree.
  References are written only to its own `refs/<set>/`.
- Parallelize only independent work with non-overlapping files. No more than 3 agents at
  once: they are expensive.
- The engine editor via MCP (and a live Blender MCP, if the user has one) belongs to the
  lead only; it exists once. Subagents use headless: `Blender -b -P`, the engine CLI.
- Studio roles (game designer, art director, tech artist, gameplay programmer, level
  designer, sound, QA) live in the project's `.claude/agents/` and in
  `scripts/templates/agents/`.

## Project files

```
<game>/
  CLAUDE.md                project rules for any new session
  .claude/agents/          studio roles
  .studioigor/
    STATE.md               now, open questions, session log — read first
    PREFERENCES.md         the user's choices for this game only (learn.py prefer)
    PIPELINE.md            phases and gates (studio.py)
    DECISIONS.md           decision log: who decided and why
    CONCEPT.md  STORY.md   idea, pillars, story
    DESIGN.md              mechanics (status table), progression, economy, difficulty
    SCOPE.md               scope in numbers (scope.py)
    ART_BIBLE.md           style
    TECH.md  ENV.md        engine and platforms; verified commands
    ASSETS.md              strategy, conventions, license registry
    PLAYTESTS.md BACKLOG.md
    research/              short research summaries
    refs/ boards/          references and boards (images not in git)
    captures/              frames captured by the agent (not in git)
    autopilot/             autopilot: LOG, REVIEW (decided on the user's behalf), REPORT
```

Fill briefly: a line instead of a paragraph; update a document only when a decision changes.

## Scripts

All in `<skill>/scripts/`, stdlib Python only.

| command | purpose |
|---|---|
| `studio.py init <folder> --name "…"` | new project: `.studioigor/`, git, CLAUDE.md, roles |
| `studio.py status [--full]` | where we are and what's next; ticks passing command gates itself |
| `studio.py decide "…" --by user\|agent\|proxy --why "…" [--options "…"]` | record a decision (proxy — autopilot on the user's behalf) |
| `studio.py tick "<part of gate>" [--phase N] [--reopen \| --skip "…" \| --block "…" \| --proxy]` | tick, reopen, skip a gate (searches all phases) |
| `studio.py projects` | known projects — find the game from any folder |
| `studio.py note "done" "next"` | session log and the "Now" block |
| `studio.py verify` | run TEST and CAPTURE from ENV.md → `VERIFIED: yes` |
| `studio.py mechanics [--check]` | mechanics and the next step for each |
| `studio.py gitignore <engine> [--lfs]` | .gitignore and git-lfs for the engine |
| `studio.py commit "…" [--tag …]` | commit everything. Never pushes |
| `refs.py …` | download references (Steam, Openverse, Wikimedia, URLs, YouTube frames), palette |
| `board.py from-refs …` / `build` / `serve --open --until-feedback` | a board for the user, with feedback |
| `envcheck.py --engine <engine>` | what is installed, what is missing and how to install it |
| `scope.py <root>` | scope count from SCOPE.md |
| `autopilot.py start\|status\|stop [--now]\|prompt --cron\|tick` | independent development on a CronCreate schedule |

Templates in `scripts/templates/`: frame capture (`godot/` windowed, `web/` Playwright,
`unity/`), Blender (`blender/`: GLB export, previews), roles (`agents/`), docs (`project/`).

## References — read by phase, not all at once

| file | when |
|---|---|
| `references/interview.md` | phase 1: questions by genre, rounds, pitch card |
| `references/design.md` | phase 1 and on design changes: fun, pillars, loops, progression, economy, difficulty, holism, blueprints |
| `references/gamedesigner.md` | game-designer layer points (phases 1, 6–9) and on "come up with something": techniques, selection, idea cards |
| `references/narrative.md` | phase 1 (story skeleton), 6 (dialogue and cutscenes as mechanics), 7–8 |
| `references/style.md` | phase 2: directions, references, boards, art bible, stack ceiling |
| `references/stack.md` | phase 3: platforms and engine choice |
| `references/environment.md` | phase 4: best setup per engine, MCP, frame capture, hello project |
| `references/assets.md` | phase 5 onward: strategy, Blender, 2D, animation, sound, look-dev, licenses |
| `references/mechanics.md` | phase 6: mechanic cycle, gyms, live tuning, playtest |
| `references/code.md` | from phase 4: code standard per engine, test policy |
| `references/production.md` | phases 7–8: slice, game-ness checklist, content, level design |
| `references/polish-release.md` | phases 9–10: facets, juice, budgets, ship gates, platforms |
| `references/gauntlet.md` | only on trigger: a critical part or an unimpressed user |
| `references/autopilot.md` | "make the game yourself / without me", every autopilot tick and the user's return |
| `references/team.md` | before any parallel work |

## Self-contained

The skill doesn't rely on or refer to other skills. Environment tools (MCP, engine CLIs and
plugins, Blender, image generation) are used if present; only what phase 4 installs is
required.

## Common failures

| symptom | what's really going on | what to do |
|---|---|---|
| 70% of the code is tests and docs | effort went into infrastructure | rule 1; tests only for silently breaking logic; `status` catches the skew |
| It works, but it's a tech demo | no menu, goal, progression, sound, story | game-ness checklist (production.md) — slice gates |
| The mechanic works but is boring | it was "delivered" without asking "is it fun?" | don't lock; find the fun in the gym: pace, risk, response, choice |
| The user is tired of questions | a wall of questions, re-asking | round budget, recommendation first, "you decide", infer from context |
| Asking the obvious | a question about a fact, not a decision | find facts yourself; ask only taste and scope |
| Everything is grey, "like every AI game" | style not locked, look-dev skipped | phase 2 and phase 5 look-dev before mass production |
| Made "the whole game" at once | one-shot | one mechanic — one gym — one playtest |
| Stuck on installation | installed the minimum or waited for the user | research the setup; install yourself; one action at a time for the human |
| Decisions lost after /clear | they lived in context | `decide` / `note` / `commit` at every step; `status` first |
| Subagents broke each other's code | shared files, no worktree | worktrees, non-overlapping files, merge one at a time |
| Autopilot goes in circles | same gate, same attempts | 2 different approaches → `--block` with a reason, move on to unblocked work; 3 ticks without changes — stop |
| There is content, but it's monotonous | N copies of one thing | ≥2 axes of difference, contact sheet on a board |
| Endless polish | the bar is "beat AAA" | polish until the user's "good enough"; the rest goes to BACKLOG |
| The game has no spark, "like everyone else's" | the agent only executed | game-designer layer: hooks in phase 1, synergies after the slice |
