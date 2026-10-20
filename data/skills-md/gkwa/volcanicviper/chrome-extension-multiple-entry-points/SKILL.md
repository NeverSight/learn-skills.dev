---
name: chrome-extension-multiple-entry-points
description: Build Chrome extensions with multiple entry points using separate Vite configs per script to avoid code-splitting issues. Use when building a Chrome extension with background, content, and popup scripts.
---

## The Problem

Chrome extensions need multiple entry points (background, content, popup), but modern bundlers create shared chunks that Chrome cannot load across isolated execution contexts.

## The Solution

Use a separate Vite config file for each entry point. Each build produces a self-contained IIFE file with no shared chunks.

## Project Structure

```
my-extension/
├── src/
│   ├── background/background.ts
│   ├── content/content.ts
│   ├── popup/
│   │   ├── popup.ts
│   │   ├── popup.html
│   │   └── popup.css
│   └── manifest.json
├── vite.background.config.ts
├── vite.content.config.ts
├── vite.popup.config.ts
└── package.json
```

## package.json Scripts

```json
{
  "scripts": {
    "build": "shx rm -rf dist && shx mkdir -p dist && pnpm run build:all && pnpm run copy:assets",
    "build:all": "pnpm run build:background && pnpm run build:content && pnpm run build:popup",
    "build:background": "vite build --config vite.background.config.ts",
    "build:content": "vite build --config vite.content.config.ts",
    "build:popup": "vite build --config vite.popup.config.ts",
    "copy:assets": "shx cp src/manifest.json src/popup/popup.html src/popup/popup.css dist/",
    "dev": "pnpm run build && pnpm run build --watch"
  },
  "devDependencies": {
    "@types/chrome": "^0.0.323",
    "typescript": "^5.8.3",
    "vite": "^6.3.5",
    "shx": "^0.3.4"
  }
}
```

## Vite Config Pattern

Each config follows the same pattern — only the input file and output filename differ:

```typescript
import { defineConfig } from "vite"
import { resolve } from "path"

export default defineConfig({
  build: {
    emptyOutDir: false,
    rollupOptions: {
      input: resolve(__dirname, "src/background/background.ts"),
      output: {
        entryFileNames: "background.js",
        dir: "dist",
        format: "iife",
        inlineDynamicImports: true,
      },
    },
    target: "es2020",
  },
  define: {
    'process.env': {},
    'global': 'globalThis'
  },
})
```

## Key Rules

- Use `format: "iife"` — not ES modules
- Set `inlineDynamicImports: true` — no shared chunks
- Use `emptyOutDir: false` — each build appends to `dist/`, not overwrites
- Use `shx` for cross-platform copy/rm commands
- Accept that dependencies are duplicated across bundles — that is intentional
