---
name: create-app-bundle
description: Create app metadata, thumbnail, and offline configuration for the Puzzmo platform
---

# Create App Bundle

Set up the metadata and assets needed for the game to appear on Puzzmo.

## Steps

1. Create a `public/` directory for static assets if it doesn't exist.

2. Create a thumbnail image:
   - Create `public/thumbnail.svg` - a simple SVG representation of the game
   - Should be 400x300 viewBox
   - Use simple shapes that represent the game visually
   - Use theme-aware colors via CSS custom properties where possible


4. Ensure `vite.config.ts` copies static assets correctly:
   ```ts
   import { defineConfig } from "vite"
   export default defineConfig({
     build: {
       outDir: "dist",
       assetsDir: "assets",
     },
   })
   ```

5. Verify the build output has:
   - `dist/index.html`
   - All JS/CSS properly bundled
   - All static assets in `dist/`

## Success Criteria

- `npm run build` completes without errors
- `dist/` directory contains a complete, self-contained game
- Thumbnail SVG exists and renders
