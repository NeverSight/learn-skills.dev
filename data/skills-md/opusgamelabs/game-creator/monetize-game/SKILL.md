---
name: monetize-game
description: Register your game on Play.fun (OpenGameProtocol), add the browser SDK, and get a monetized play.fun URL
argument-hint: "[game-path]"
disable-model-invocation: true
allowed-tools: ["Bash", "Read", "Write", "Edit", "Glob", "Grep", "WebFetch", "Task"]
---

# Monetize Game (Play.fun / OpenGameProtocol)

Register your game on [Play.fun](https://play.fun) (OpenGameProtocol), integrate the browser SDK for points tracking and leaderboards, and get a shareable play.fun URL. This is the link you post to Moltbook.

**What you'll get:**
1. Your game registered on Play.fun with anti-cheat config
2. The Play.fun browser SDK integrated into your game (points widget, leaderboard, wallet connect)
3. A rebuilt + redeployed game with the SDK active
4. A play.fun game URL to share on Moltbook and social media

## Prerequisites

- A deployed game with a public URL (run `/game-creator:make-game` first, or ensure your game is deployed to GitHub Pages / Vercel / etc.)
- Node.js installed

## Instructions

### Step 0: Locate the game

Parse `$ARGUMENTS` to find the game project directory. If not provided, check the current working directory for a `package.json` with Phaser or Three.js dependencies.

Read `package.json` to confirm this is a game project. Read `vite.config.js` or similar to determine the deployed URL (look for `base` path).

### Step 1: Authenticate with Play.fun

Check if the user already has Play.fun credentials:

```bash
node skills/playdotfun/scripts/playfun-auth.js status
```

**If credentials exist and are valid**, skip to Step 2.

**If no credentials**, walk the user through authentication:

> To register your game on Play.fun, you need to authenticate first.
>
> I'll start a local auth server. Click the link below to log in:

```bash
node skills/playdotfun/scripts/playfun-auth.js callback &
```

Then tell the user:

> Open this URL in your browser:
> **https://app.play.fun/skills-auth?callback=http://localhost:9876/callback**
>
> Log in with your Play.fun account. The credentials will be saved automatically.
> Tell me when you're done.

**Wait for user confirmation.** Then verify:

```bash
node skills/playdotfun/scripts/playfun-auth.js status
```

If verification fails, offer the manual method as a fallback:

> If the callback didn't work, you can paste your credentials manually.
> Go to your Play.fun dashboard, copy your API credentials (base64 format), and I'll save them:
> ```
> node skills/playdotfun/scripts/playfun-auth.js manual <your-base64-credentials>
> ```

### Step 2: Determine the game URL

Find the deployed game URL. Check in this order:

1. Look for a GitHub Pages URL by running:
   ```bash
   GITHUB_USER=$(gh api user --jq '.login' 2>/dev/null)
   REPO_NAME=$(basename $(git remote get-url origin 2>/dev/null) .git 2>/dev/null)
   ```
   If both resolve, the URL is `https://$GITHUB_USER.github.io/$REPO_NAME/`

2. Check `vite.config.js` for a `base` path that hints at the deployment URL

3. Ask the user for their game URL if it can't be determined

Verify the URL is accessible:

```bash
curl -s -o /dev/null -w "%{http_code}" "$GAME_URL"
```

### Step 3: Register the game on Play.fun

Read the game's `package.json` for the name and description. Read `src/core/Constants.js` (or equivalent) to determine reasonable anti-cheat limits based on the scoring system.

Use the Play.fun MCP `register_game` tool if available. Otherwise, use the API directly:

Load the `playdotfun` skill for API reference. Register the game via `POST https://api.play.fun/games` with:

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

**Anti-cheat guidelines** (from the playdotfun skill):
- Casual clicker/idle: `maxScorePerSession: 100-500`
- Skill-based arcade (flappy bird, runners): `maxScorePerSession: 500-2000`
- Competitive/complex: `maxScorePerSession: 1000-5000`

Save the returned **game UUID** — you'll need it for the SDK integration.

**Tell the user:**
> Your game is registered on Play.fun!
> **Game ID**: `<uuid>`
> **Name**: `<name>`

### Step 4: Add the Play.fun Browser SDK

Integrate the SDK into the game. This is a lightweight addition — the SDK loads from CDN and provides a points widget overlay.

#### 4a. Add the SDK script and meta tag to `index.html`

First, extract the user's API key from stored credentials:

```bash
# Read API key from agent config (stored by playfun-auth.js)
# Example path for Claude Code — adapt for your agent
API_KEY=$(cat ~/.claude.json | jq -r '.mcpServers["play-fun"].headers["x-api-key"]')
echo "User API Key: $API_KEY"
```

If no API key is found, prompt the user to authenticate first (Step 1).

Then add before the closing `</head>` tag, substituting the actual API key:

```html
<meta name="x-ogp-key" content="<USER_API_KEY>" />
<script src="https://sdk.play.fun/latest"></script>
```

**Important**: The `x-ogp-key` meta tag must contain the **user's Play.fun API key** (not the game ID). Do NOT leave the placeholder `USER_API_KEY_HERE` — always substitute the actual key extracted above.

#### 4b. Create `src/playfun.js` integration module

Create a module that wires the Play.fun SDK into the game's EventBus:

```js
// src/playfun.js
// Play.fun (OpenGameProtocol) integration
// Wires game events to Play.fun points tracking

import { eventBus, Events } from './core/EventBus.js';

const GAME_ID = '<game-uuid>';

let sdk = null;
let initialized = false;

export async function initPlayFun() {
  if (typeof OpenGameSDK === 'undefined' && typeof PlayFunSDK === 'undefined') {
    console.warn('Play.fun SDK not loaded — skipping monetization');
    return;
  }

  const SDKClass = typeof PlayFunSDK !== 'undefined' ? PlayFunSDK : OpenGameSDK;
  sdk = new SDKClass({
    gameId: GAME_ID,
    ui: { usePointsWidget: true },
  });

  await sdk.init();
  initialized = true;
  console.log('Play.fun SDK initialized');

  wireEvents();
}

function wireEvents() {
  // addPoints() — call frequently during gameplay to buffer points locally (non-blocking)
  if (Events.SCORE_CHANGED) {
    eventBus.on(Events.SCORE_CHANGED, ({ score, delta }) => {
      if (sdk && initialized && delta > 0) {
        sdk.addPoints(delta);
      }
    });
  }

  // savePoints() — ONLY call at natural break points (game over, level complete)
  // WARNING: savePoints() opens a BLOCKING MODAL — never call during active gameplay!
  if (Events.GAME_OVER) {
    eventBus.on(Events.GAME_OVER, () => {
      if (sdk && initialized) {
        sdk.savePoints(); // Uses buffered points from addPoints() calls
      }
    });
  }

  // Save on page unload (browser handles this gracefully)
  window.addEventListener('beforeunload', () => {
    if (sdk && initialized) {
      sdk.savePoints();
    }
  });
}
```

**Critical SDK behavior:**

| Method | When to use | Behavior |
|--------|-------------|----------|
| `addPoints(n)` | During gameplay | Buffers points locally, non-blocking |
| `savePoints()` | Game over / level end | **Opens blocking modal**, syncs buffered points to server |

⚠️ **Do NOT call `savePoints()` on a timer or during active gameplay** — it interrupts the player with a modal dialog. Only call at natural pause points (game over, level transitions, menu screens).

**Important**: Read the actual `EventBus.js` to find the correct event names. Common patterns:
- `SCORE_CHANGED` / `score:changed` with `{ score, delta }` or `{ score }`
- `GAME_OVER` / `game:over`

Adapt the event names and payload destructuring to match what the game actually emits. If the game doesn't emit a delta, compute it by tracking the previous score.

#### 4c. Wire into main.js

Add the Play.fun init call to the game's entry point (`src/main.js`):

```js
import { initPlayFun } from './playfun.js';

// After game initialization
initPlayFun().catch(err => console.warn('Play.fun init failed:', err));
```

The `initPlayFun()` call should be non-blocking — if the SDK fails to load (e.g., ad blocker), the game still works.

### Step 5: Rebuild and redeploy

```bash
cd <project-dir> && npm run build
```

If the build fails, fix the integration code and retry.

Then redeploy:

```bash
cd <project-dir> && npx gh-pages -d dist
```

Or whatever deploy method the project uses (`npm run deploy` if available).

### Step 6: Confirm and share

Wait ~30 seconds for deployment to propagate, then verify:

```bash
curl -s -o /dev/null -w "%{http_code}" "$GAME_URL"
```

**Tell the user:**

> Your game is monetized on Play.fun!
>
> **Play your game**: `<game-url>`
> **View on Play.fun**: `https://play.fun/games/<game-uuid>`
>
> **What's live:**
> - Points widget overlay (bottom-right corner)
> - Leaderboard tracking
> - Wallet connect for claiming rewards
> - Points buffered during gameplay, saved on game over
>
> **Share on Moltbook**: Post your game URL to [moltbook.com](https://www.moltbook.com/) — 770K+ agents on the agent internet ready to play and upvote.
>
> **Next steps:**
> - Launch a playcoin for your game (token rewards for players)
> - Check your leaderboard on Play.fun
> - Share the play.fun URL on social media
