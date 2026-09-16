---
name: use-vite
description: Set up Vite and Vitest as the build and test tools, with vite-plugin-checker for TypeScript checking and ESM configuration. Use when starting or configuring a frontend project.
---

Use Vite as the build system and Vitest as the test tool.

## ESM Configuration

Use ESM syntax in `vite.config.js`. Add `"type": "module"` to `package.json` so all `*.js` files are interpreted as ESM. If a file must stay CJS, use the `.cjs` extension.

Do not use the CJS build of Vite's Node API — it is deprecated and removed in Vite 6. Reference: https://vite.dev/guide/troubleshooting.html#vite-cjs-node-api-deprecated

## vite-plugin-checker

Add `vite-plugin-checker` to run TypeScript type checking alongside the build:

1. Install:

```bash
pnpm add --save-dev vite-plugin-checker
```

2. Add to `vite.config.js`:

```js
import { defineConfig } from 'vite';
import checker from 'vite-plugin-checker';

export default defineConfig({
  plugins: [
    checker({
      typescript: true,
    }),
  ],
});
```

Type errors appear in the browser overlay and terminal during development. The build fails if TypeScript errors are present — no separate type-check script needed.
