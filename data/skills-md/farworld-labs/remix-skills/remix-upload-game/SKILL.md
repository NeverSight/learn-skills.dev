---
name: remix-upload-game
description: Upload version code to a Remix game
---

# Upload Game Workflow

## Overview

This skill guides you through uploading a completed HTML game to the Remix
platform. It covers creating the game entry (if needed) and uploading the code.

## Prerequisites

- The `REMIX_API_KEY` environment variable must be set.
- A completed HTML game file, ready for upload.

## Steps

### 1. Locate the Game File

Find the path to the HTML file to upload. It should be a single self-contained
HTML document with inline CSS and JS.

### 2. Validate

Read the HTML file and verify:

1. Has `<!DOCTYPE html>` declaration
2. Has `<meta name="viewport" ...>` tag
3. Has RemixSDK script tag: `<script src="https://cdn.jsdelivr.net/npm/@remix-gg/sdk@latest/dist/index.min.js"></script>`
4. No legacy `@farcade/game-sdk` script tag
5. Calls `singlePlayer.actions.gameOver(` OR `multiplayer.actions.gameOver(` (not both)
6. Registers `.onPlayAgain(` callback
7. Registers `.onToggleMute(` callback
8. No `localStorage` or `sessionStorage` usage
9. No inline event handlers (`onclick=`, `onload=`, etc.)

Fix any reported issues before proceeding.

### 3. Create the Game (if needed)

First, check for a `.remix-settings.json` file in the project root. If it
exists and contains `gameId` and `versionId`, skip creation and proceed to
step 4.

If no settings file exists (or it lacks these IDs), create the game via REST:

```
POST https://api.remix.gg/v1/games
Authorization: Bearer $REMIX_API_KEY
Content-Type: application/json

{ "name": "<game name>" }
```

The response returns the **game ID** and **version ID**.

After creation succeeds, write the returned IDs to `.remix-settings.json`:

```json
{
  "gameId": "<returned game ID>",
  "versionId": "<returned version ID>",
  "name": "<game name>"
}
```

### 4. Upload the Code

Read `gameId` and `versionId` from `.remix-settings.json` (or use the values
just obtained from creation).

**Read the HTML file** and pass its content as the `code` field in the request body:

```
POST https://api.remix.gg/v1/games/{gameId}/versions/{versionId}/code
Authorization: Bearer $REMIX_API_KEY
Content-Type: application/json

{ "code": "<HTML file contents>" }
```

The response returns a confirmation with the game ID, version ID, and thread ID.

## Tips

- Always validate before uploading to catch issues early.
- You can re-upload code to the same version as many times as needed.
- If you need a fresh version, create a new game entry.
