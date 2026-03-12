---
name: deploy-scene
description: Deploy and publish a Decentraland scene to Genesis City (LAND-based). Use when user wants to deploy, publish, upload, go live, or make their scene accessible on parcels they own.
---

# Deploying to Genesis City

Deploy to specific parcels you own or have permission to deploy to.

**Use the `/deploy` command** to deploy. It runs `npx @dcl/sdk-commands deploy` and handles the full process:
1. Build the scene
2. Upload assets to IPFS
3. Deploy to the specified parcels
4. Requires a wallet with LAND or deployment permissions

> **Deploying to a World instead?** See the `deploy-worlds` skill for Worlds deployment (personal spaces using DCL NAMEs or ENS domains).

## Pre-Deployment Checklist

Before deploying, verify:

1. **scene.json is valid**:
   - `ecs7: true` and `runtimeVersion: "7"`
   - Correct `parcels` matching your LAND (for Genesis City)
   - Valid `base` parcel
   - `main: "bin/index.js"`

2. **Code compiles**:
   ```bash
   npx tsc --noEmit
   ```

3. **Scene previews correctly**:
   Use the `preview` tool to verify the scene works (or `npx @dcl/sdk-commands start --bevy-web` manually)

4. **Dependencies installed**:
   ```bash
   npm install
   ```

5. **Assets are within limits** (check parcel count):
   | Parcels | Entities | Triangles | Textures |
   |---------|----------|-----------|----------|
   | 1 | 512 | 10,000 | 10 MB |
   | 2 | 1,024 | 20,000 | 20 MB |
   | 4 | 2,048 | 40,000 | 40 MB |
   | 8+ | Scales linearly | | |

## Deployment Process

### Using CLI
```bash
# Build first
npx @dcl/sdk-commands build

# Deploy (will open browser for wallet connection)
npx @dcl/sdk-commands deploy
```

### Using Creator Hub
1. Open Creator Hub
2. Select your scene
3. Click "Publish"
4. Connect wallet
5. Confirm transaction

## scene.json for Deployment

```json
{
  "ecs7": true,
  "runtimeVersion": "7",
  "display": {
    "title": "My Awesome Scene",
    "description": "A description for the marketplace",
    "navmapThumbnail": "images/thumbnail.png"
  },
  "scene": {
    "parcels": ["0,0", "0,1"],
    "base": "0,0"
  },
  "main": "bin/index.js",
}
```

### Spawn Points

Configure where players appear when entering the scene:

```json
{
  "spawnPoints": [
    {
      "name": "spawn1",
      "default": true,
      "position": { "x": [1, 5], "y": [0, 0], "z": [2, 4] },
      "cameraTarget": { "x": 8, "y": 1, "z": 8 }
    }
  ]
}
```

Position ranges (e.g., `[1, 5]`) spawn players randomly within the range. Use `cameraTarget` to orient the player's camera on spawn.

## Best Practices

- Always preview locally before deploying
- Use a thumbnail image (`navmapThumbnail`) for the Genesis City map
- Write a clear description for discovery
- Test with multiple browser tabs to verify multiplayer behavior
- Keep scene load time under 15 seconds (optimize assets)
