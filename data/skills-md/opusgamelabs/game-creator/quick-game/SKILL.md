---
name: quick-game
description: Rapidly scaffold and implement a playable game — no assets, design, audio, deploy, or monetize. Get something on screen fast. Use when the user says "quick game", "fast prototype", "just get something playable", or wants a game without the full pipeline. For the complete pipeline, use make-game instead. Do NOT use for production games (use make-game for the full pipeline).
argument-hint: "[2d|3d] [game-name] OR [tweet-url]"
license: MIT
metadata:
  author: OpusGameLabs
  version: 1.3.0
  tags: [game, prototype, scaffold, fast]
---

## Performance Notes

- Take your time to do this thoroughly
- Quality is more important than speed
- Do not skip validation steps

# Quick Game (Fast Prototype)

Build a playable game prototype as fast as possible. This is `/make-game` without the polish — just scaffold + implement the core loop. Get something on screen, then incrementally add layers with `/add-assets`, `/design-game`, `/add-audio`, `/game-deploy`, and `/monetize-game`.

**What you'll get:**
1. A scaffolded game project with clean architecture
2. Core gameplay — input, movement, scoring, fail condition, restart
3. A running dev server you can play immediately

**What you skip** (run these later if you want):
- `/add-assets` — pixel art sprites (2D) or 3D models
- `/design-game` — visual polish, particles, transitions
- `/add-audio` — music and sound effects
- `/record-promo` — promo video capture
- `/game-deploy` — deploy to here.now
- `/monetize-game` — Play.fun integration

## Instructions

### Step 0: Parse arguments

Parse `$ARGUMENTS` to determine the game concept:

**Direct specification:** `[2d|3d] [game-name]`
- **Engine**: `2d` (Phaser) or `3d` (Three.js). If not specified, default to `2d`.
- **Name**: kebab-case. If not specified, ask the user.

**Tweet URL:** If arguments contain a tweet URL (`x.com/*/status/*`, `twitter.com/*/status/*`, `fxtwitter.com/*/status/*`):
1. Fetch the tweet using the `fetch-tweet` skill
2. Default to 2D
3. Creatively abstract a game concept from the tweet
4. Generate a kebab-case name
5. Tell the user what you'll build

**Meshy API Key (3D only):** If 3D, check for `MESHY_API_KEY`. If missing, ask the user (link to https://app.meshy.ai). Store for model generation.

### Step 1: Scaffold + Implement

**Infrastructure (main thread):**

1. Locate the template directory — check `~/.claude/plugins/cache/local-plugins/game-creator/*/templates/` or `templates/` relative to this plugin
2. **Target directory**: If inside the `game-creator` repo, create in `examples/<game-name>/`. Otherwise, create in `./<game-name>/`.
3. Copy the template:
   - 2D: `templates/phaser-2d/` → target
   - 3D: `templates/threejs-3d/` → target
4. Update `package.json` name and `index.html` title
5. Run `npm install`
6. Start the dev server (`npm run dev`) in the background. Check port availability first — if 3000 is taken, try 3001, 3002, etc.

**Game implementation (subagent via Task):**

Launch a `Task` subagent with:

> You are building a quick game prototype. Speed is the priority — get a playable core loop working.
>
> **Project path**: `<project-dir>`
> **Engine**: `<2d|3d>`
> **Game concept**: `<description>`
> **Skill to load**: `phaser` (2D) or `threejs-game` (3D)
>
> **Implement in this order:**
> 1. Input (touch + keyboard from the start)
> 2. Player movement / core mechanic
> 3. Fail condition (death, collision, timer)
> 4. Scoring
> 5. Restart flow (GameState.reset() → clean slate)
>
> **Scope: 1 scene, 1 mechanic, 1 fail condition.** Keep it tight.
>
> Rules:
> - All cross-module communication via EventBus
> - All magic numbers in Constants.js
> - No title screen — boot directly into gameplay
> - No in-game score HUD — Play.fun widget handles score display
> - Mobile-first input: touch + keyboard, use unified InputSystem pattern
> - Import `SAFE_ZONE` from Constants.js — keep UI below `SAFE_ZONE.TOP`
> - Minimum 7-8% canvas width for collectibles/hazards
> - Character sizing: `GAME.WIDTH * 0.12` to `GAME.WIDTH * 0.15` for character-driven games
> - Preserve the template's `createButton()` helper in GameOverScene — do NOT rewrite it
> - Wire spectacle events: `SPECTACLE_ENTRANCE`, `SPECTACLE_ACTION`, `SPECTACLE_HIT`, `SPECTACLE_COMBO`, `SPECTACLE_STREAK`, `SPECTACLE_NEAR_MISS`
> - Add `isMuted` to GameState for future audio support
> - Ensure restart is clean — 3 restarts in a row should work identically

### Step 2: Verify

After the subagent returns:

1. Run `npm run build` in the project directory to confirm no errors
2. If the build fails, fix the issues (up to 2 retries)
3. If Playwright MCP is available, navigate to the dev server, take a screenshot, and do a quick visual check

## Example Usage

### 2D game
```
/quick-game 2d asteroid-dodge
```
Result: Copies Phaser template → implements player ship, asteroid spawning, collision death, score counter, restart flow → dev server running at localhost:3000 in ~2 minutes. Shapes only, no polish.

### From tweet
```
/quick-game https://x.com/user/status/123456
```
Result: Fetches tweet → abstracts game concept → scaffolds and implements a playable prototype inspired by the tweet content.

## Troubleshooting

### Game scaffolds but won't start
**Cause:** Vite config or import paths incorrect.
**Fix:** Verify vite.config.js has correct root. Check that main.js is referenced in index.html.

### Missing core files
**Cause:** Scaffold skipped EventBus/GameState/Constants.
**Fix:** Every game needs core/EventBus.js, core/GameState.js, core/Constants.js. Re-run scaffold or create manually.

### Done

Tell the user:

> Your game is running at `http://localhost:<port>`. Open it in a browser to play!
>
> **To keep building, run these commands:**
> - `/add-assets` — replace shapes with pixel art sprites
> - `/design-game` — add visual polish (particles, gradients, juice)
> - `/add-audio` — add music and sound effects
> - `/game-deploy` — deploy to the web
> - `/monetize-game` — add Play.fun integration
>
> Or run `/make-game` next time for the full pipeline.
