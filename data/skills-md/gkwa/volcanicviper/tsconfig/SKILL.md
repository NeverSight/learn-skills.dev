---
name: tsconfig
description: Add a tsconfig.json for TypeScript projects using Vite and/or Chrome extensions. Use when setting up TypeScript in a frontend or Chrome extension project.
---

Add a `tsconfig.json` with these settings:

```json
{
  "compilerOptions": {
    "target": "ES2020",
    "module": "ESNext",
    "moduleResolution": "bundler",
    "strict": true,
    "noEmit": true,
    "types": ["chrome", "vitest/globals"],
    "lib": ["ES2020", "DOM", "DOM.Iterable"]
  },
  "include": ["src"]
}
```

Key options:

- `"moduleResolution": "bundler"` — required for Vite to resolve ES modules correctly
- `"types": ["chrome"]` — enables IntelliSense and type checking for Chrome extension APIs (`chrome.storage`, `chrome.runtime`, etc.); remove if not building a Chrome extension
- `"noEmit": true` — lets TypeScript do type checking without conflicting with Vite's compilation
- `"target": "ES2020"` — enables async/await, optional chaining, and other modern syntax
- `"strict": true` — catches bugs early and enforces consistent coding patterns

Install the Chrome types package if building a Chrome extension:

```bash
pnpm add --save-dev @types/chrome
```
