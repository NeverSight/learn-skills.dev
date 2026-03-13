---
name: remix-add-sprite
description: Generate and add sprites to a Remix game
---

# Add Sprite to Game Workflow

## Overview

This skill guides you through generating sprite sheets for canvas-based games
on the Remix platform.

## Prerequisites

- The game HTML file must already exist (follow the **game-creation** workflow
  first if starting from scratch).
- A game must be created on the Remix platform (you need a game ID).
- The `REMIX_API_KEY` environment variable must be set.

## Steps

### 1. Check for Existing Game ID

Read `.remix-settings.json` in the current directory. If it exists and contains
a `gameId`, use that value.

Only if `.remix-settings.json` does not exist or has no `gameId` should you
follow the **upload-game** workflow to create one.

### 2. Generate the Sprite Sheet

Call the sprite generation endpoint:

```
POST https://api.remix.gg/v1/games/{gameId}/sprites/generate
Authorization: Bearer $REMIX_API_KEY
Content-Type: application/json

{
  "prompt": "a pixel-art knight walking animation, 4 frames",
  "gridSize": 4,
  "imageUrl": null
}
```

Parameters:
- `prompt` (required) -- description of the sprite and animation
- `gridSize` (optional) -- number of frames in the sprite sheet grid
- `imageUrl` (optional) -- reference image URL to base the sprite on

The response returns `spriteUrl` and `transparentSpriteUrl` directly (already
hosted -- no separate upload step needed).

### 3. Integrate the Sprite Sheet into the Game

Use the returned URL with canvas `drawImage` to render individual frames:

```js
const sprite = new Image();
sprite.src = "https://returned-sprite-url.png";

const frameWidth = 64;  // width of a single frame
const frameHeight = 64; // height of a single frame
const totalFrames = 4;
let currentFrame = 0;

sprite.onload = () => {
  function animate() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    // Draw the current frame from the sprite sheet
    ctx.drawImage(
      sprite,
      currentFrame * frameWidth, 0,  // source x, y in the sprite sheet
      frameWidth, frameHeight,        // source width, height
      player.x, player.y,            // destination x, y on canvas
      frameWidth, frameHeight         // destination width, height
    );

    currentFrame = (currentFrame + 1) % totalFrames;
    requestAnimationFrame(animate);
  }
  animate();
};
```

Use `transparentSpriteUrl` when you need the sprite rendered over other
game elements without a background.

## Tips

- **Be specific about frame count and action.** "4-frame walk cycle" is better
  than "walking character".
- **Specify art style.** Include "pixel-art", "hand-drawn", "flat vector", etc.
  in your prompt.
- **Frame layout is horizontal.** Frames are arranged left-to-right in a single
  row. Divide the image width by `gridSize` to get individual frame dimensions.
- **Use `transparentSpriteUrl` for in-game sprites** that need to overlay
  backgrounds or other elements.
- **Preload before gameplay.** Wait for `onload` before starting the game loop.
