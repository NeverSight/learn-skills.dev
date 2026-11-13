---
name: game-design
description: Design games with soul, from idea to shipped assets and micro-feedback. A gated workflow (idea → concept → story → mechanics → unity → progression → screen flow & transitions → assets → experience control & juice), a player-psychology toolkit, a GDD template, a platform-profile system so the same method works for any engine or platform, and a low-cost asset pipeline (one generated vector master per asset, variants edited by hand in SVG) plus audio direction and loudness mastering. Image and audio generation are optional and provider-agnostic; Recraft and ElevenLabs helpers are included as recommended defaults. Use before designing, revising, or reviewing a game design, GDD, art bible, or audio bible.
license: MIT
---

# Game Design

A game is judged by what people feel, not by its technique. Every decision in this skill is tested against three pillars:

| Pillar | Question | A good answer sounds like |
|---|---|---|
| **Story** | What is this game about? | "Four chilli-sauce couriers race down a narrow alley before the market closes." |
| **Motivation** | What do we need to do? | "Deliver the most orders; bump rivals so their sauce spills." |
| **Experience** | What do I feel, physically and emotionally? | "Tense hands keeping balance, laughing when a friend slips, relief in the last second." |

Each game is a **complete module with its own soul**: world, tone, colour, sound, and feel. A host platform's own brand belongs to the platform shell, not to the game. What a game inherits from its platform is only the *technical rules*: input model, budgets, accessibility. Those live in a **platform profile** (see below).

## Before you start

1. **Load the platform profile.** Find the target's profile (input devices, screen, budgets, lifecycle hooks, what the platform owns vs. what the game owns). If none exists, write one from `templates/platform-profile.md` before stage 4. `examples/ralyoo-platform-profile.md` shows a complete one.
2. **Check the tools you have.** Read `references/providers.md`. Image and audio generation are optional; the workflow works with hand-written SVG and a written audio spec alone.
3. **Know who decides.** "Owner" below means whoever approves the design: a client, a lead, or the user. Gates are shown to them.

## Workflow (in order; do not skip stages)

1. **Idea.** Write 5–10 one-sentence ideas, pick 1–3 with reasons (see `references/philosophy.md` §Idea test).
2. **Concept.** High concept, player fantasy, experience pillars (3 emotion words), session length, why it is fun to *watch* and to *play*.
3. **Story.** World, characters, conflict, tone. A party game's story can be thin, but it must give every action a reason.
4. **Mechanics.** Core loop (seconds), round loop (minutes), session loop. Player verbs, rules, win/lose conditions, initial tuning numbers. Stay inside the platform profile.
5. **Unity.** Test every mechanic against story and experience. A mechanic that does not support the pillars is cut, however cool.
6. **Progression.** New experiences across a session and between sessions: characters, enemies, arenas, items, skills, shop, collectibles, round twists. Progression deepens; it does not just add.
7. **Screen flow & transitions.** The experience does not start at "GO!" or end at the score. Design every screen and every transition between them: title, how-to-play, round intro, HUD, round end, between rounds, final results and celebration, play again/exit, pause, player disconnect/rejoin. If the game has second screens (phones, handhelds, split views), each screen has a pair there. See `references/screen-flow.md`. **Mandatory**; a GDD without screen flow is incomplete.
8. **Assets.** Only after story, mechanics, and screen flow are approved. Assets serve the experience (unity again). Art direction first, then exploration, then production. **Generate at most one vector master per asset; poses, expressions, states, and colour variants are edited by hand in SVG; simple shapes are written directly.** Mockup QA is required before hand-off. See `references/assets.md`.
9. **Experience control & juice.** Pacing, tension–release, camera, feedback, juice, music, SFX, announcer. See `references/philosophy.md` §Game feel and `references/audio.md`.

Every stage has a gate: write the result into the GDD (`templates/gdd.md`), then continue.

- **Gate 1:** concept, story, mechanics, progression, and screen flow, shown to the owner as one package.
- **Gate 2:** art bible, audio bible, asset list with a generation budget. **Production assets are made only after Gate 2 is approved.**

## References (read by stage)

| File | When |
|---|---|
| `references/lessons.md` | Always, before a new game. What worked and what did not on a shipped game; hand-off pattern to developers. |
| `references/philosophy.md` | Always, before stage 1. Player psychology, motivation, flow, difficulty, satisfaction, game feel, local-multiplayer laws. |
| `references/screen-flow.md` | Stage 7. Required screens, transitions, platform vs. game ownership, requesting new platform capabilities. |
| `templates/platform-profile.md` | Before stage 4, if the target has no profile yet. |
| `references/assets.md` | Asset stage. Art direction, the low-cost vector pipeline, credit budget, formats, mockup QA. |
| `references/audio.md` | Juice stage. Audio direction, generation, loudness mastering. |
| `references/providers.md` | Before generating anything. Provider roles, recommended defaults, alternatives, adapter contract, no-API path. |
| `templates/gdd.md`, `templates/art-bible.md`, `templates/audio-bible.md` | Document skeletons. |
| `scripts/` | Optional helpers: `recraft.py`, `elevenlabs.py` (stdlib-only API callers), `svg2png.mjs` (render SVG to PNG to inspect edits). |

Paths in this skill are relative to the skill folder. Design documents go wherever the game project keeps them; `design/` is the suggested default.

## Rules

- Do not copy an existing game (name, characters, art, music, levels, look). Genres and common mechanics are fine; create your own identity.
- Do not use the host platform's brand kit as the game's visual style.
- Do not invent platform capabilities. If the profile does not list it, it does not exist: write it as a **platform request** in the GDD and design a fallback that works today.
- The designer owns design documents, assets, content data, and store/catalog text. Gameplay code belongs to developers unless the owner says otherwise.
- Never print, log, commit, or paste API keys. Read them from environment variables only.
- State your limits honestly: if you cannot hear audio, measure it and ask a human to listen; if you can see images, render and inspect before sending.
