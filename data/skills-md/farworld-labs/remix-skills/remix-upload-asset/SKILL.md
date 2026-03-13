---
name: remix-upload-asset
description: Upload images, audio, or 3D models as hosted game assets
---

# Upload Game Asset Workflow

## Overview

Upload arbitrary files (images, audio, 3D models) as hosted game assets
via the REST API. Returns a permanent URL you can reference in your game HTML.

## Prerequisites

- A game must already exist on the Remix platform (you need a game ID).
- The `REMIX_API_KEY` environment variable must be set.

## Steps

### 1. Check for Existing Game ID

**IMPORTANT: Do NOT create a new game without checking first.**

Read `.remix-settings.json` in the current directory. If it exists and contains
a `gameId`, use that value -- the game is already created.

Only if `.remix-settings.json` does not exist or has no `gameId` should you
follow the **upload-game** workflow to create one.

### 2. Upload the Asset

Send the file as multipart form data:

```
POST https://api.remix.gg/v1/games/{gameId}/assets
Authorization: Bearer $REMIX_API_KEY
Content-Type: multipart/form-data

Form fields:
  file       (required) — the binary file to upload
  assetName  (optional) — custom display name; defaults to the filename
```

**Allowed extensions:** `.jpg`, `.jpeg`, `.png`, `.webp`, `.mp3`, `.wav`,
`.hdr`, `.glb`, `.gltf`

**Max file size:** 5 MB

**Response:**

```json
{
  "success": true,
  "data": {
    "gameId": "...",
    "asset": {
      "url": "https://..."
    }
  }
}
```

Use `data.asset.url` as the hosted URL for the asset.

### 3. Use the URL in Game HTML

Reference the returned URL in your game code. Examples:

```html
<img src="https://returned-asset-url.png" width="64" height="64" />
```

```js
const img = new Image();
img.src = "https://returned-asset-url.png";
img.onload = () => ctx.drawImage(img, x, y, w, h);
```

```js
const audio = new Audio("https://returned-asset-url.mp3");
audio.play();
```

### 4. (Optional) List All Assets

Retrieve all uploaded assets for a game:

```
GET https://api.remix.gg/v1/games/{gameId}/assets
Authorization: Bearer $REMIX_API_KEY
```

## Tips

- **Name files descriptively.** Use clear filenames like `player-idle.png` or
  `jump-sfx.mp3` -- the filename becomes the default asset name.
- **Preload assets before gameplay.** Wait for `onload` / `canplaythrough`
  events before starting the game loop to avoid missing assets.
- **Stay under 5 MB per file.** Compress images and audio before uploading.
  Use `.webp` for images and `.mp3` for audio when possible.
- **Repeat for each asset.** Run through steps 2-3 for every file the game
  needs.
