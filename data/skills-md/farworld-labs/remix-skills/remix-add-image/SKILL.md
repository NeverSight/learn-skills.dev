---
name: remix-add-image
description: Generate and add images to a Remix game
---

# Add Image to Game Workflow

## Overview

This skill guides you through generating an AI image and integrating its hosted
URL into your game HTML. Image generation and asset upload are separate REST
calls.

## Prerequisites

- The game HTML file must already exist (follow the **game-creation** workflow
  first if starting from scratch).
- A game must be created on the Remix platform (you need a game ID).
- The `REMIX_API_KEY` environment variable must be set.

## Steps

### 1. Check for Existing Game ID

**IMPORTANT: Do NOT create a new game without checking first.**

Read `.remix-settings.json` in the current directory. If it exists and contains
a `gameId`, use that value -- the game is already created and you can skip
straight to step 2.

Only if `.remix-settings.json` does not exist or has no `gameId` should you
follow the **upload-game** workflow to create one.

### 2. Generate the Image

Call the image generation endpoint with the game ID and a descriptive prompt:

```
POST https://api.remix.gg/v1/games/{gameId}/images/generate
Authorization: Bearer $REMIX_API_KEY
Content-Type: application/json

{ "prompt": "a pixel-art treasure chest on a grassy hill" }
```

The response returns base64 image data.

### 3. Upload as Game Asset

Upload the generated image as a game asset using multipart form data:

```
POST https://api.remix.gg/v1/games/{gameId}/assets
Authorization: Bearer $REMIX_API_KEY
Content-Type: multipart/form-data

Form fields:
  file       (required) — the image binary (e.g. the base64-decoded data saved to a .png)
  assetName  (optional) — custom display name; defaults to the filename
```

Allowed image extensions: `.jpg`, `.jpeg`, `.png`, `.webp`

The response returns the hosted URL:

```json
{ "success": true, "data": { "gameId": "...", "asset": { "url": "https://..." } } }
```

Use `data.asset.url` as the image URL in the next step.

> For uploading non-image assets (audio, 3D models), see the
> `remix-upload-asset` skill.

### 4. Integrate the URL into the Game

Add the asset URL to the game HTML. **Size the image to match the game entity
it represents** -- do not render it at its native resolution. For example, if a
treasure chest is a 32x32 tile in your game, draw or display the image at 32x32
regardless of the source image dimensions.

The integration method depends on how the image is used:

**As an HTML image element:**
```html
<img src="https://returned-asset-url.png" alt="Treasure chest" width="32" height="32" />
```

**As a CSS background:**
```css
.game-bg {
  background-image: url("https://returned-asset-url.png");
}
```

**As a JavaScript-loaded image (for canvas games):**
```js
const img = new Image();
img.src = "https://returned-asset-url.png";
img.onload = () => {
  // draw at the entity's size, not the image's native size
  ctx.drawImage(img, x, y, entityWidth, entityHeight);
};
```

## Examples

### Adding a Background to a Canvas Game

```js
const bg = new Image();
bg.src = "https://uploaded-asset-url/background.png";
bg.onload = () => {
  function draw() {
    ctx.drawImage(bg, 0, 0, canvas.width, canvas.height);
    // draw game objects on top...
    requestAnimationFrame(draw);
  }
  draw();
};
```

### Adding a Sprite Sheet

```js
const spriteSheet = new Image();
spriteSheet.src = "https://uploaded-asset-url/player-sprites.png";
spriteSheet.onload = () => {
  // draw a 32x32 frame from the sprite sheet
  ctx.drawImage(spriteSheet, frameX, frameY, 32, 32, player.x, player.y, 32, 32);
};
```

## Tips

- **Be specific in prompts.** Include art style, color palette, and context
  (e.g. "pixel-art 16-bit style red dragon"). No need to specify transparency
  or background handling -- the server takes care of that.
- **Preload images before gameplay.** Wait for `onload` before starting the
  game loop to avoid flickering or missing assets.
- **Repeat for multiple images.** Run through steps 2-4 for each image the
  game needs.
