---
name: make-game
description: Full guided pipeline — scaffold, design, audio, deploy, and monetize a game from scratch
argument-hint: "[2d|3d] [game-name] OR [tweet-url]"
disable-model-invocation: true
---

# Make Game (Full Pipeline)

Build a complete browser game from scratch, step by step. This command walks you through the entire pipeline — from an empty folder to a deployed, monetized game. No game development experience needed.

**What you'll get:**
1. A fully scaffolded game project with clean architecture
2. Pixel art sprites — recognizable characters, enemies, and items (optional, replaces geometric shapes)
3. Visual polish — gradients, particles, transitions, juice
4. Chiptune music and retro sound effects (no audio files needed)
5. Live deployment to GitHub Pages with a public URL
6. Monetization via Play.fun — points tracking, leaderboards, wallet connect, and a play.fun URL to share on Moltbook
7. Future changes auto-deploy on `git push`

**Quality assurance is built into every step** — each code-modifying step runs build verification, visual review via Playwright MCP, and autofixes any issues found.

## Orchestration Model

**You are an orchestrator. You do NOT write game code directly.** Your job is to:

1. Set up the project (template copy, npm install, dev server)
2. Create and track pipeline tasks using `TaskCreate`/`TaskUpdate`
3. Delegate each code-writing step to a `Task` subagent
4. Run the Verification Protocol (build + visual review + autofix) after each code-modifying step
5. Report results to the user between steps

**What stays in the main thread:**
- Step 0: Parse arguments, create todo list
- Step 1 (infrastructure only): Copy template, npm install, playwright install, start dev server
- Verification protocol orchestration (launch QA subagent, read text result, launch autofix if needed)
- Step 4 (deploy): Interactive auth requires user back-and-forth

**What goes to subagents** (via `Task` tool):
- Step 1 (game implementation): Transform template into the actual game concept
- Step 1.5: Pixel art sprites and backgrounds
- Step 2: Visual polish
- Step 3: Audio integration

Each subagent receives: step instructions, relevant skill name, project path, engine type, dev server port, and game concept description.

## Verification Protocol

Run this protocol after **every code-modifying step** (Steps 1, 1.5, 2, 3). It delegates all QA work to a subagent to minimize main-thread context usage.

### Playwright MCP Check (once, before first QA run)

Before the first QA run (after Step 1 infrastructure setup), check if Playwright MCP tools like `browser_navigate` are available. If not:

1. Run: `claude mcp add playwright npx @playwright/mcp@latest`
2. Tell the user: "Playwright MCP has been added. Please restart Claude Code for it to take effect, then tell me to continue."
3. **Wait for user to restart and confirm.** Do not proceed until MCP tools are available.

### QA Subagent

Launch a `Task` subagent with these instructions:

> You are the QA subagent for the game creation pipeline.
>
> **Project path**: `<project-dir>`
> **Dev server port**: `<port>`
> **Step being verified**: `<step name>`
>
> Run these phases in order. Stop early if a phase fails critically (build or runtime).
>
> **Phase 1 — Build Check**
> ```bash
> cd <project-dir> && npm run build
> ```
> If the build fails, report FAIL immediately with the error output.
>
> **Phase 2 — Runtime Check**
> ```bash
> cd <project-dir> && node scripts/verify-runtime.mjs
> ```
> If the runtime check fails, report FAIL immediately with the error details.
>
> **Phase 3 — Gameplay Verification**
> ```bash
> cd <project-dir> && node scripts/iterate-client.js \
>   --url http://localhost:<port> \
>   --actions-file scripts/example-actions.json \
>   --iterations 3 --screenshot-dir output/iterate
> ```
> After running, read the state JSON files (`output/iterate/state-*.json`) and error files (`output/iterate/errors-*.json`):
> - **Scoring**: At least one state file should show `score > 0`
> - **Death**: At least one state file should show `mode: "game_over"`. Mark as SKIPPED (not FAIL) if game_over is not reached — some games have multi-life systems or random hazard spawns that make death unreliable in short iterate runs. Death SKIPPED is acceptable and does not block the pipeline.
> - **Errors**: No critical errors in error files
>
> Skip this phase if `scripts/iterate-client.js` is not present.
>
> **Phase 4 — Architecture Validation**
> ```bash
> cd <project-dir> && node scripts/validate-architecture.mjs
> ```
> Report any warnings but don't fail on architecture issues alone.
>
> **Phase 5 — Visual Review via Playwright MCP**
> Use Playwright MCP to visually review the game. If MCP tools are not available, fall back to reading iterate screenshots from `output/iterate/`.
>
> With MCP:
> 1. `browser_navigate` to `http://localhost:<port>`
> 2. `browser_wait_for` — wait 2 seconds for the game to load
> 3. `browser_take_screenshot` — save as `output/qa-gameplay.png`
> 4. Assess: Are entities visible? Is the game rendering correctly?
> 5. Check safe zone: Is any UI hidden behind the top ~8% (Play.fun widget area)?
> 6. Check entity sizing: Is the main character large enough (12–15% screen width for character games)?
> 7. Wait for game over (or navigate to it), `browser_take_screenshot` — save as `output/qa-gameover.png`
> 8. Check buttons: Are button labels visible? Blank rectangles = broken button pattern.
>
> **Screenshot timeout**: If `browser_take_screenshot` hangs for more than 10 seconds (can happen with continuous WebGL animations), cancel and proceed with code review instead. Do not let a screenshot hang block the entire QA phase.
>
> **Note on iterate screenshots**: The iterate-client uses `canvas.toDataURL()` which returns blank/black images when Phaser uses WebGL with `preserveDrawingBuffer: false`. Always prefer Playwright MCP viewport screenshots (`browser_take_screenshot`) over iterate screenshots for visual review.
>
> Without MCP (fallback):
> 1. Read the iterate screenshots from `output/iterate/shot-*.png` (may be black if WebGL — this is expected)
> 2. Fall back to code review: read scene files and assess visual correctness from the code
>
> **Return your results in this exact format (text only, no images):**
> ```
> QA RESULT: PASS|FAIL
>
> Phase 1 (Build): PASS|FAIL
> Phase 2 (Runtime): PASS|FAIL
> Phase 3 (Gameplay): Iterate PASS|FAIL, Scoring PASS|FAIL|SKIPPED, Death PASS|FAIL|SKIPPED, Errors PASS|FAIL
> Phase 4 (Architecture): PASS — N/N checks
> Phase 5 (Visual): PASS|FAIL — <issues if any>
>
> ISSUES:
> - <issue descriptions, or "None">
>
> SCREENSHOTS: output/qa-gameplay.png, output/qa-gameover.png
> ```

### Orchestrator Flow

```
Launch QA subagent → read text result
  If PASS → proceed to next step
  If FAIL → launch autofix subagent with ISSUES list → re-run QA subagent
  Max 3 attempts per step
```

### Autofix Logic

When the QA subagent reports FAIL:

1. **Read `output/autofix-history.json`** to see what fixes were already attempted. If a previous entry matches the same `issue` and `fix_attempted` with `result: "failure"`, instruct the subagent to try a different approach.
2. Launch a **fix subagent** via `Task` tool with:
   - The ISSUES list from the QA result
   - The phase that failed (build errors, runtime errors, gameplay issues, visual problems)
   - Any relevant failed attempts from `output/autofix-history.json` so the subagent knows what NOT to repeat
3. **After each autofix attempt**, append an entry to `output/autofix-history.json`:
   ```json
   { "step": "<step name>", "issue": "<what failed>", "fix_attempted": "<what was tried>", "result": "success|failure", "timestamp": "<ISO date>" }
   ```
4. Re-run the QA subagent (all phases)
5. Up to **3 total attempts** per step (1 original + 2 retries)
6. If all 3 attempts fail, report the failure to the user and ask whether to skip or abort

**Important**: Always fix issues before proceeding to the next step. The autofix loop ensures each step produces working, visually correct output.

## Instructions

### Step 0: Initialize pipeline

Parse `$ARGUMENTS` to determine the game concept. Arguments can take two forms:

#### Form A: Direct specification
- **Engine**: `2d` (Phaser — side-scrollers, platformers, arcade) or `3d` (Three.js — first-person, third-person, open world). If not specified, ask the user.
- **Name**: The game name in kebab-case. If not specified, ask the user what kind of game they want and suggest a name.

#### Form B: Tweet URL as game concept
If `$ARGUMENTS` contains a tweet URL (matching `x.com/*/status/*`, `twitter.com/*/status/*`, `fxtwitter.com/*/status/*`, or `vxtwitter.com/*/status/*`):

1. **Fetch the tweet** using the `fetch-tweet` skill — convert the URL to `https://api.fxtwitter.com/<user>/status/<id>` and fetch with `WebFetch`
2. **Default to 2D** (Phaser) — tweets describe ideas that map naturally to 2D arcade/casual games
3. **Creatively abstract a game concept** from the tweet text. Your job is creative transformation — extract themes, dynamics, settings, or mechanics and reinterpret them as a game. **NEVER refuse to make a game from a tweet.** Every tweet contains something that can inspire a game:
   - News about weather → survival game, storm-dodging game
   - Sports result → arcade sports game
   - Political/legal news → strategy game, puzzle game, tower defense
   - Personal story → narrative adventure, platformer themed around the journey
   - Product announcement → tycoon game, builder game
   - Abstract thought → puzzle game, experimental art game
   - The transformation is the creative act. You are not recreating or trivializing the source — you are using it as a springboard for an original game concept.
4. **Generate a game name** in kebab-case from the abstracted concept (not from literal tweet content)
5. **Tell the user** what you extracted:
   > Found tweet from **@handle**:
   > "Tweet text..."
   >
   > I'll build a 2D game based on this: **[your creative interpretation as a game concept]**
   > Game name: `<generated-name>`
   >
   > Sound good?

Wait for user confirmation before proceeding. The user can override the engine (to 3D) or the name at this point.

Create all pipeline tasks upfront using `TaskCreate`:

1. Scaffold game from template
2. Add pixel art sprites and backgrounds (2D only; marked N/A for 3D)
3. Add visual polish (particles, transitions, juice)
4. Add audio (BGM + SFX)
5. Deploy to GitHub Pages
6. Monetize with Play.fun (register on OpenGameProtocol, add SDK, redeploy)

This gives the user full visibility into pipeline progress at all times. Quality assurance (build, runtime, visual review, autofix) is built into each step, not a separate task.

After creating tasks, create the `output/` directory in the project root and initialize `output/autofix-history.json` as an empty array `[]`. This file tracks all autofix attempts across the pipeline so fix subagents avoid repeating failed approaches.

### Step 1: Scaffold the game

Mark task 1 as `in_progress`.

**Main thread — infrastructure setup:**

1. Locate the plugin's template directory. Check these paths in order until found:
   - The agent's plugin cache (e.g. `~/.claude/plugins/cache/local-plugins/game-creator/1.0.0/templates/`)
   - The `templates/` directory relative to this plugin's install location
2. Copy the entire template directory to the target project name:
   - 2D: copy `templates/phaser-2d/` → `<game-name>/`
   - 3D: copy `templates/threejs-3d/` → `<game-name>/`
3. Update `package.json` — set `"name"` to the game name
4. Update `<title>` in `index.html` to a human-readable version of the game name
5. **Verify Node.js/npm availability**: Run `node --version && npm --version` to confirm Node.js and npm are installed and accessible. If they fail (e.g., nvm lazy-loading), try sourcing nvm: `export NVM_DIR="$HOME/.nvm" && source "$NVM_DIR/nvm.sh"` then retry. If Node.js is not installed at all, tell the user they need to install it before continuing.
6. Run `npm install` in the new project directory
7. **Install Playwright and Chromium** — Playwright is required for runtime verification and the iterate loop:
   1. Check if Playwright is available: `npx playwright --version`
   2. If that fails, check `node_modules/.bin/playwright --version`
   3. If neither works, run `npm install -D @playwright/test` explicitly
   4. Then install the browser binary: `npx playwright install chromium`
   5. Verify success; if it fails, warn and continue (build verification still works, but runtime/iterate checks will be skipped)
8. **Verify template scripts exist** — The template ships with `scripts/verify-runtime.mjs`, `scripts/iterate-client.js`, and `scripts/example-actions.json`. Confirm they are present. The `verify` and `iterate` npm scripts are already in `package.json` from the template.
9. **Start the dev server** — Before running `npm run dev`, check if the configured port (in `vite.config.js`) is already in use: `lsof -i :<port> -t`. If occupied, update `vite.config.js` to use the next available port (try 3001, 3002, etc.). Then start the dev server in the background and confirm it responds. Keep it running throughout the pipeline. Note the actual port number — pass it to `scripts/verify-runtime.mjs` via the `PORT` env variable in subsequent runs.

**Subagent — game implementation:**

Launch a `Task` subagent with these instructions:

> You are implementing Step 1 (Scaffold) of the game creation pipeline.
>
> **Project path**: `<project-dir>`
> **Engine**: `<2d|3d>`
> **Game concept**: `<user's game description>`
> **Skill to load**: `phaser` (2D) or `threejs-game` (3D)
>
> **Core loop first** — implement in this order:
> 1. Input (touch + keyboard from the start — never keyboard-only)
> 2. Player movement / core mechanic
> 3. Fail condition (death, collision, timer)
> 4. Scoring
> 5. Restart flow (GameState.reset() → clean slate)
>
> Keep scope small: **1 scene, 1 mechanic, 1 fail condition**. Get the gameplay loop working before any polish.
>
> Transform the template into the game concept:
> - Rename entities, scenes/systems, and events to match the concept
> - Implement core gameplay mechanics
> - Wire up EventBus events, GameState fields, and Constants values
> - Ensure all modules communicate only through EventBus
> - All magic numbers go in Constants.js
> - **No title screen** — the template boots directly into gameplay. Do not create a MenuScene or title screen. Only add one if the user explicitly asks.
> - **No in-game score HUD** — the Play.fun widget displays score in a deadzone at the top of the game. Do not create a UIScene or HUD overlay for score display.
> - **Mobile-first input**: Choose the best mobile input scheme for the game concept (tap zones, virtual joystick, gyroscope tilt, swipe). Implement touch + keyboard from the start — never keyboard-only. Use the unified analog InputSystem pattern (moveX/moveZ) so game logic is input-source-agnostic.
> - Ensure restart is clean — test mentally that 3 restarts in a row would work identically
> - Add `isMuted` to GameState for audio mute support
>
> **CRITICAL — Preserve the button pattern:**
> - The template's `GameOverScene.js` contains a working `createButton()` helper (Container + Graphics + Text). **Do NOT rewrite this method.** Keep it intact or copy it into any new scenes that need buttons. The correct z-order is: Graphics first (background), Text second (label), Container interactive. If you put Graphics on top of Text, the text becomes invisible. If you make the Graphics interactive instead of the Container, hover/press states break.
>
> **Character & entity sizing:**
> - Size all entities proportionally: `GAME.WIDTH * ratio` and `GAME.HEIGHT * ratio`, never fixed pixel values like `40 * PX`.
> - For character-driven games (named personalities, mascots, famous figures): make the main character prominent — `GAME.WIDTH * 0.12` to `GAME.WIDTH * 0.15` (12–15% of screen width). Use bobblehead proportions (head = 40–50% of sprite height) for personality games.
> - Define all sizes in `Constants.js` as `GAME.WIDTH * ratio` or `GAME.HEIGHT * ratio`.
>
> **Play.fun safe zone:**
> - Import `SAFE_ZONE` from `Constants.js`. All UI text, buttons, and interactive elements (title text, score panels, restart buttons) must be positioned below `SAFE_ZONE.TOP`. The Play.fun SDK renders a 75px widget bar at the top of the viewport (z-index 9999). Use `safeTop + usableH * ratio` for proportional positioning within the usable area (where `usableH = GAME.HEIGHT - SAFE_ZONE.TOP`).
>
> **Generate game-specific test actions:**
> After implementing the core loop, overwrite `scripts/example-actions.json` with actions tailored to this game. Requirements:
> - Use the game's actual input keys (e.g., ArrowLeft/ArrowRight for dodger, space for flappy, w/a/s/d for top-down)
> - Include enough gameplay to score at least 1 point
> - Include a long idle period (60+ frames with no input) to let the fail condition trigger
> - Total should be at least 150 frames of gameplay
>
> Example for a dodge game (arrow keys):
> ```json
> [
>   {"buttons":["ArrowRight"],"frames":20},
>   {"buttons":["ArrowLeft"],"frames":20},
>   {"buttons":["ArrowRight"],"frames":15},
>   {"buttons":[],"frames":10},
>   {"buttons":["ArrowLeft"],"frames":20},
>   {"buttons":[],"frames":80}
> ]
> ```
>
> Example for a platformer (space to jump):
> ```json
> [
>   {"buttons":["space"],"frames":4},
>   {"buttons":[],"frames":25},
>   {"buttons":["space"],"frames":4},
>   {"buttons":[],"frames":25},
>   {"buttons":["space"],"frames":4},
>   {"buttons":[],"frames":80}
> ]
> ```
>
> Do NOT start a dev server or run builds — the orchestrator handles that.

**After subagent returns**, run the Verification Protocol.

**Create `progress.md`** at the game's project root. Read the game's actual source files to populate it accurately:
- Read `src/core/EventBus.js` for the event list
- Read `src/core/Constants.js` for the key sections (GAME, PLAYER, ENEMY, etc.)
- List files in `src/entities/` for entity names
- Read `src/core/GameState.js` for state fields

Write `progress.md` with this structure:

```markdown
# Progress

## Game Concept
- **Name**: [game name from project]
- **Engine**: Phaser 3 / Three.js
- **Description**: [from user's original prompt]

## Step 1: Scaffold
- **Entities**: [list entity names from src/entities/]
- **Events**: [list event names from EventBus.js]
- **Constants keys**: [top-level sections from Constants.js, e.g. GAME, PLAYER, ENEMY, COLORS]
- **Scoring system**: [how points are earned, from GameState + scene logic]
- **Fail condition**: [what ends the game]
- **Input scheme**: [keyboard/mouse/touch controls implemented]

## Decisions / Known Issues
- [any notable decisions or issues from scaffolding]
```

**Tell the user:**
> Your game is scaffolded and running! Here's how it's organized:
> - `src/core/Constants.js` — all game settings (speed, colors, sizes)
> - `src/core/EventBus.js` — how parts of the game talk to each other
> - `src/core/GameState.js` — tracks score, lives, etc.
> - **Mobile controls are built in** — works on phone (touch/tilt) and desktop (keyboard)
>
> **Next up: pixel art.** I'll create custom pixel art sprites for every character, enemy, item, and background tile — all generated as code, no image files needed. Then I'll add visual polish on top.

Mark task 1 as `completed`.

**Wait for user confirmation before proceeding.**

### Step 1.5: Add pixel art sprites and backgrounds

**For 2D games, always run this step.** For 3D games, mark task 2 as `completed` (N/A) and skip to Step 2.

Mark task 2 as `in_progress`.

Launch a `Task` subagent with these instructions:

> You are implementing Step 1.5 (Pixel Art Sprites) of the game creation pipeline.
>
> **Project path**: `<project-dir>`
> **Engine**: 2D (Phaser 3)
> **Skill to load**: `game-assets`
>
> **Read `progress.md`** at the project root before starting. It describes the game's entities, events, constants, and scoring system from Step 1.
>
> Follow the game-assets skill fully:
> 1. Read all entity files (`src/entities/`) to find `generateTexture()` / `fillCircle()` calls
> 2. Choose the palette that matches the game's theme (DARK, BRIGHT, or RETRO)
> 3. Create `src/core/PixelRenderer.js` — the `renderPixelArt()` + `renderSpriteSheet()` utilities
> 4. Create `src/sprites/palette.js` with the chosen palette
> 5. Create sprite data files (`player.js`, `enemies.js`, `items.js`, `projectiles.js`) with pixel matrices
> 6. Create `src/sprites/tiles.js` with background tiles (ground variants, decorative elements)
> 7. Create or update the background system to use tiled pixel art instead of flat colors/grids
> 8. Update entity constructors to use pixel art instead of geometric shapes
> 9. Add Phaser animations for entities with multiple frames
> 10. Adjust physics bodies for new sprite dimensions
>
> **After completing your work**, append a `## Step 1.5: Assets` section to `progress.md` with: palette used, sprites created, any dimension changes to entities.
>
> Do NOT run builds — the orchestrator handles verification.

**After subagent returns**, run the Verification Protocol.

**Tell the user:**
> Your game now has pixel art sprites and backgrounds! Every character, enemy, item, and background tile has a distinct visual identity. Here's what was created:
> - `src/core/PixelRenderer.js` — rendering engine
> - `src/sprites/` — all sprite data, palettes, and background tiles
>
> **Next up: visual polish.** I'll add particles, screen transitions, and juice effects. Ready?

Mark task 2 as `completed`.

**Wait for user confirmation before proceeding.**

### Step 2: Design the visuals

Mark task 3 as `in_progress`.

Launch a `Task` subagent with these instructions:

> You are implementing Step 2 (Visual Design) of the game creation pipeline.
>
> **Project path**: `<project-dir>`
> **Engine**: `<2d|3d>`
> **Skill to load**: `game-designer`
>
> **Read `progress.md`** at the project root before starting. It describes the game's entities, events, constants, and what previous steps have done.
>
> Apply the game-designer skill:
> 1. Audit the current visuals — read Constants.js, all scenes, entities, EventBus
> 2. Score each visual area (background, palette, animations, particles, transitions, typography, game feel, game over) on a 1-5 scale
> 3. Implement the highest-impact improvements:
>    - Sky gradients or environment backgrounds
>    - Particle effects for key gameplay moments
>    - Screen shake, flash, or slow-mo for impact
>    - Smooth scene transitions
>    - UI juice: button hover, text shadows, floating score text
> 4. All new values go in Constants.js, use EventBus for triggering effects
> 5. Don't alter gameplay mechanics
>
> **After completing your work**, append a `## Step 2: Design` section to `progress.md` with: improvements applied, new effects added, any color or layout changes.
>
> Do NOT run builds — the orchestrator handles verification.

**After subagent returns**, run the Verification Protocol.

**Tell the user:**
> Your game looks much better now! Here's what changed: [summarize changes]
>
> **Next up: music and sound effects.** I'll add chiptune background music and retro sound effects — all generated in the browser, no audio files needed. Ready?

Mark task 3 as `completed`.

**Wait for user confirmation before proceeding.**

### Step 3: Add audio

Mark task 4 as `in_progress`.

Launch a `Task` subagent with these instructions:

> You are implementing Step 3 (Audio) of the game creation pipeline.
>
> **Project path**: `<project-dir>`
> **Engine**: `<2d|3d>`
> **Skill to load**: `game-audio`
>
> **Read `progress.md`** at the project root before starting. It describes the game's entities, events, constants, and what previous steps have done.
>
> Apply the game-audio skill:
> 1. Audit the game: check for `@strudel/web`, read EventBus events, read all scenes
> 2. Install `@strudel/web` if needed
> 3. Create `src/audio/AudioManager.js`, `music.js`, `sfx.js`, `AudioBridge.js`
> 4. Add audio events to EventBus.js (including `AUDIO_TOGGLE_MUTE`)
> 5. Wire audio into main.js and all scenes
> 6. **Important**: Use explicit imports from `@strudel/web` (`import { stack, note, s } from '@strudel/web'`) — do NOT rely on global registration
> 7. **Mute toggle**: Wire `AUDIO_TOGGLE_MUTE` to `gameState.game.isMuted`. Both BGM and SFX must check `isMuted` before playing. Add M key shortcut and a speaker icon UI button.
>
> **After completing your work**, append a `## Step 3: Audio` section to `progress.md` with: BGM patterns added, SFX event mappings, mute wiring confirmation.
>
> Do NOT run builds — the orchestrator handles verification.

**After subagent returns**, run the Verification Protocol.

**Tell the user:**
> Your game now has music and sound effects! Click/tap once to activate audio, then you'll hear the music.
> Note: Strudel is AGPL-3.0, so your project needs a compatible open source license.
>
> **Next up: deploy to the web.** I'll help you set up GitHub Pages so your game gets a public URL. Future changes auto-deploy when you push. Ready?

Mark task 4 as `completed`.

**Wait for user confirmation before proceeding.**

### Step 4: Deploy to GitHub Pages

Mark task 5 as `in_progress`.

Load the game-deploy skill. **This step stays in the main thread** because it requires interactive authentication and user back-and-forth.

#### 6a. Check prerequisites

Run `gh auth status` to check if the GitHub CLI is installed and authenticated.

**If `gh` is not found**, tell the user:
> You need the GitHub CLI to deploy. Install it with:
> - **macOS**: `brew install gh`
> - **Linux**: `sudo apt install gh` or see https://cli.github.com
>
> Once installed, run `gh auth login` and follow the prompts, then tell me when you're ready.

**Wait for the user to confirm.**

**If `gh` is not authenticated**, tell the user:
> You need to log in to GitHub. Run this command and follow the prompts:
> ```
> gh auth login
> ```
> Choose "GitHub.com", "HTTPS", and authenticate via browser. Tell me when you're done.

**Wait for the user to confirm.** Then re-run `gh auth status` to verify.

#### 6b. Build the game

```bash
npm run build
```

Verify `dist/` exists and contains `index.html` and assets. If the build fails, fix the errors before proceeding.

#### 6c. Set up the Vite base path

Read `vite.config.js`. The `base` option must match the GitHub Pages URL pattern `/<repo-name>/`. If it's not set or wrong, update it:

```js
export default defineConfig({
  base: '/<game-name>/',
  // ... rest of config
});
```

Rebuild after changing the base path.

#### 6d. Create the GitHub repo and push

Check if the project already has a git remote. If not:

```bash
git init
git add .
git commit -m "Initial commit"
gh repo create <game-name> --public --source=. --push
```

If it already has a remote, just make sure all changes are committed and pushed.

#### 6e. Deploy with gh-pages

```bash
npm install -D gh-pages
npx gh-pages -d dist
```

This pushes the `dist/` folder to a `gh-pages` branch on GitHub.

#### 6f. Enable GitHub Pages

```bash
GITHUB_USER=$(gh api user --jq '.login')
gh api repos/$GITHUB_USER/<game-name>/pages -X POST --input - <<< '{"build_type":"legacy","source":{"branch":"gh-pages","path":"/"}}'
```

If Pages is already enabled, this may return an error — that's fine, skip it.

#### 6g. Get the live URL and verify

```bash
GITHUB_USER=$(gh api user --jq '.login')
GAME_URL="https://$GITHUB_USER.github.io/<game-name>/"
echo $GAME_URL
```

Wait ~30 seconds for the first deploy to propagate, then verify:

```bash
curl -s -o /dev/null -w "%{http_code}" "$GAME_URL"
```

If it returns 404, wait another minute and retry — GitHub Pages can take 1-2 minutes on first deploy.

#### 6h. Add deploy script

Add a `deploy` script to `package.json` so future deploys are one command:

```json
{
  "scripts": {
    "deploy": "npm run build && npx gh-pages -d dist"
  }
}
```

**Tell the user:**
> Your game is live!
>
> **URL**: `https://<username>.github.io/<game-name>/`
>
> **How auto-deploy works**: Whenever you make changes, just run:
> ```
> npm run deploy
> ```
> Or if you're working with me, I'll commit your changes and run deploy for you.
>
> **Next up: monetization.** I'll register your game on Play.fun (OpenGameProtocol), add the points SDK, and redeploy. Players earn rewards, you get a play.fun URL to share on Moltbook. Ready?

Mark task 5 as `completed`.

**Wait for user confirmation before proceeding.**

### Step 5: Monetize with Play.fun

Mark task 6 as `in_progress`.

**This step stays in the main thread** because it requires interactive authentication.

#### 7a. Authenticate with Play.fun

Check if the user already has Play.fun credentials. The auth script is bundled with the plugin:

```bash
node skills/playdotfun/scripts/playfun-auth.js status
```

**If credentials exist**, skip to 7b.

**If no credentials**, start the auth callback server:

```bash
node skills/playdotfun/scripts/playfun-auth.js callback &
```

Tell the user:

> To register your game on Play.fun, you need to log in once.
> Open this URL in your browser:
> **https://app.play.fun/skills-auth?callback=http://localhost:9876/callback**
>
> Log in with your Play.fun account. Credentials are saved locally.
> Tell me when you're done.

**Wait for user confirmation.** Then verify with `playfun-auth.js status`.

If callback fails, offer manual method as fallback.

#### 7b. Register the game on Play.fun

Determine the deployed game URL from Step 6 (`https://<username>.github.io/<game-name>/`).

Read `package.json` for the game name and description. Read `src/core/Constants.js` to determine reasonable anti-cheat limits based on the scoring system.

Use the Play.fun API to register the game. Load the `playdotfun` skill for API reference. Register via `POST https://api.play.fun/games`:

```json
{
  "name": "<game-name>",
  "description": "<game-description>",
  "gameUrl": "<deployed-url>",
  "platform": "web",
  "isHTMLGame": true,
  "iframable": true,
  "maxScorePerSession": <based on game scoring>,
  "maxSessionsPerDay": 50,
  "maxCumulativePointsPerDay": <reasonable daily cap>
}
```

**Anti-cheat guidelines:**
- Casual clicker/idle: `maxScorePerSession: 100-500`
- Skill-based arcade (flappy bird, runners): `maxScorePerSession: 500-2000`
- Competitive/complex: `maxScorePerSession: 1000-5000`

Save the returned **game UUID**.

#### 7c. Add the Play.fun Browser SDK

First, extract the user's API key from stored credentials:

```bash
# Read API key from agent config (stored by playfun-auth.js)
# Example path for Claude Code — adapt for your agent
API_KEY=$(cat ~/.claude.json | jq -r '.mcpServers["play-fun"].headers["x-api-key"]')
echo "User API Key: $API_KEY"
```

If no API key is found, prompt the user to authenticate first.

Then add the SDK script and meta tag to `index.html` before `</head>`, substituting the actual API key:

```html
<meta name="x-ogp-key" content="<USER_API_KEY>" />
<script src="https://sdk.play.fun/latest"></script>
```

**Important**: The `x-ogp-key` meta tag must contain the **user's Play.fun API key** (not the game ID). Do NOT leave the placeholder — always substitute the actual key extracted above.

Create `src/playfun.js` that wires the game's EventBus to Play.fun points tracking:

```js
// src/playfun.js — Play.fun (OpenGameProtocol) integration
import { eventBus, Events } from './core/EventBus.js';

const GAME_ID = '<game-uuid>';
let sdk = null;
let initialized = false;

export async function initPlayFun() {
  const SDKClass = typeof PlayFunSDK !== 'undefined' ? PlayFunSDK
    : typeof OpenGameSDK !== 'undefined' ? OpenGameSDK : null;
  if (!SDKClass) {
    console.warn('Play.fun SDK not loaded');
    return;
  }
  sdk = new SDKClass({ gameId: GAME_ID, ui: { usePointsWidget: true } });
  await sdk.init();
  initialized = true;

  // addPoints() — call frequently during gameplay to buffer points locally (non-blocking)
  eventBus.on(Events.SCORE_CHANGED, ({ score, delta }) => {
    if (initialized && delta > 0) sdk.addPoints(delta);
  });

  // savePoints() — ONLY call at natural break points (game over, level complete)
  // WARNING: savePoints() opens a BLOCKING MODAL — never call during active gameplay!
  eventBus.on(Events.GAME_OVER, () => { if (initialized) sdk.savePoints(); });

  // Save on page unload (browser handles this gracefully)
  window.addEventListener('beforeunload', () => { if (initialized) sdk.savePoints(); });
}
```

**Critical SDK behavior:**

| Method | When to use | Behavior |
|--------|-------------|----------|
| `addPoints(n)` | During gameplay | Buffers points locally, non-blocking |
| `savePoints()` | Game over / level end | **Opens blocking modal**, syncs buffered points to server |

⚠️ **Do NOT call `savePoints()` on a timer or during active gameplay** — it interrupts the player with a modal dialog. Only call at natural pause points (game over, level transitions, menu screens).

**Read the actual EventBus.js** to find the correct event names and payload shapes. Adapt accordingly.

Add `initPlayFun()` to `src/main.js`:

```js
import { initPlayFun } from './playfun.js';
// After game init
initPlayFun().catch(err => console.warn('Play.fun init failed:', err));
```

#### 7d. Rebuild and redeploy

```bash
cd <project-dir> && npm run build && npx gh-pages -d dist
```

Wait ~30 seconds, then verify the deployment is live.

#### 7e. Tell the user

> Your game is monetized on Play.fun!
>
> **Play**: `<game-url>`
> **Play.fun**: `https://play.fun/games/<game-uuid>`
>
> The Play.fun widget is now live — players see points, leaderboard, and wallet connect.
> Points are buffered during gameplay and saved on game over.
>
> **Share on Moltbook**: Post your game URL to [moltbook.com](https://www.moltbook.com/) — 770K+ agents ready to play and upvote.

Mark task 6 as `completed`.

### Pipeline Complete!

Tell the user:

> Your game has been through the full pipeline! Here's what you have:
> - **Scaffolded architecture** — clean, modular code structure
> - **Pixel art sprites** — recognizable characters (if chosen) or clean geometric shapes
> - **Visual polish** — gradients, particles, transitions, juice
> - **Music and SFX** — chiptune background music and retro sound effects
> - **Quality assured** — each step verified with build, runtime, and visual review
> - **Live on the web** — deployed to GitHub Pages with a public URL
> - **Monetized on Play.fun** — points tracking, leaderboards, and wallet connect
>
> **Share your play.fun URL on Moltbook** to reach 770K+ agents on the agent internet.
>
> **What's next?**
> - Add new gameplay features: `/game-creator:add-feature [describe what you want]`
> - Upgrade to pixel art (if using shapes): `/game-creator:add-assets`
> - Launch a playcoin for your game (token rewards for players)
> - Keep iterating! Run any step again: `/game-creator:design-game`, `/game-creator:add-audio`
> - Redeploy after changes: `npm run deploy`
