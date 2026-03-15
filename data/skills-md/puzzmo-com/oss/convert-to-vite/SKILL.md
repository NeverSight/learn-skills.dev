---
name: convert-to-vite
description: Convert a standalone HTML game into a Vite project with proper module structure
---

# Convert to Vite

Convert this HTML game into a Vite-powered project.

## Steps

1. Initialize a new `package.json` with:
   - `"name"` based on the game directory name
   - `"private": true`
   - `"type": "module"`
   - `"scripts"`: `"dev": "vite"`, `"build": "vite build"`, `"preview": "vite preview"`

2. Install dependencies:
   - `vite` as a devDependency

3. Create `vite.config.ts`:
   ```ts
   import { defineConfig } from "vite"
   export default defineConfig({})
   ```

4. Extract inline `<script>` and `<style>` from `index.html`:
   - Move inline JS to `src/main.js` (or `src/main.ts`)
   - Move inline CSS to `src/style.css`
   - Replace inline content with `<script type="module" src="/src/main.js"></script>` and `<link rel="stylesheet" href="/src/style.css">`

5. Move any standalone JS/CSS files into `src/`

6. Update all asset references to use relative paths that Vite can resolve

## Success Criteria

- `npx vite build` completes without errors
- The game runs identically with `npx vite` as it did before
- No inline scripts remain in `index.html` (except small config objects)
- All JS is loaded as ES modules
