---
name: convert-tanstack-app-to-web-component
description: Refactors a standalone TanStack-based application (React/Vue/Solid) into a standard Web Component (Custom Element), enabling framework-agnostic injection into legacy apps or micro-frontends.
---

## Step 1 — Install the required dependency

```bash
npm install @r2wc/react-to-web-component
```

---

## Step 2 — Create `src/App.tsx` (body-level app component)

Extract the body content from `src/routes/__root.tsx` into a standalone React component.
This component must NOT render `<html>`, `<head>`, or `<body>` — only the visual content (Header + router outlet).
The original `__root.tsx` stays untouched for the SSR build.

---

## Step 3 — Create `src/widget.tsx` (custom element entry)

- Import `App` from `src/App.tsx`
- Use `@r2wc/react-to-web-component` to wrap it as a custom element
- Inject Tailwind CSS into the Shadow DOM using Vite's `?inline` import:

```ts
import styles from './styles.css?inline'
// pass styles to r2wc options so they are adopted into the shadow root
```

- Register the custom element, for %app-name get the name from the package.json name:

```ts
customElements.define('%app-name', TanstackAppElement)
```


---

## Step 4 — Switch to Memory Router for the WC build

Browser history routing conflicts with the host page URL. In `src/widget.tsx`, create the router using `createMemoryHistory`:

```ts
import { createMemoryHistory } from '@tanstack/react-router'

const router = createRouter({
  routeTree,
  history: createMemoryHistory({ initialEntries: ['/'] }),
})
```

Update `src/router.tsx` to accept an optional `history` parameter so the same factory works for both SSR and WC builds.

---

## Step 5 — Create `vite.config.wc.ts` (standalone lib build)

The WC build must NOT use TanStack Start's SSR plugins (`tanstackStart()`, `nitro()`, `devtools()`).
Create a separate Vite config in lib mode:

```ts
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import tailwindcss from '@tailwindcss/vite'
import tsconfigPaths from 'vite-tsconfig-paths'

export default defineConfig({
  plugins: [react(), tailwindcss(), tsconfigPaths()],
  define: {
    'process.env.NODE_ENV': JSON.stringify('production'),
  },
  build: {
    outDir: 'webcomponent',
    lib: {
      entry: 'src/widget.tsx',
      name: 'TanstackAppWC',
      fileName: '%app-name',
      formats: ['iife'], // single self-executing bundle for easy <script> embedding
    },
  },
})
```
Add the webcomponent dir to .gitignore

---

## Step 6 — Add `build:wc` script to `package.json`

```json
"build:wc": "vite build --config vite.config.wc.ts"
```

Output: `dist/tanstack-app.iife.js` — a single file any host page can load:

```html
<script src="tanstack-app.iife.js"></script>
<tanstack-app></tanstack-app>
```

---

## Files to create / modify

| File | Action | Reason |
|------|--------|--------|
| `src/App.tsx` | Create | Body-level app (no html/head/body) |
| `src/widget.tsx` | Create | Custom element definition + bootstrap |
| `vite.config.wc.ts` | Create | Lib build without SSR plugins |
| `package.json` | Modify | Add `build:wc` script |
| `src/router.tsx` | Modify | Accept optional `history` param |
| `src/routes/__root.tsx` | No change | Kept intact for SSR build |
| `src/styles.css` | No change | Imported via `?inline` in WC entry |

---

## CSS strategy inside Shadow DOM

| Option | How | Trade-off |
|--------|-----|-----------|
| Constructable Stylesheet (recommended) | Bundle CSS as string via `?inline`, inject via `adoptedStyleSheets` | Clean isolation, no leakage |
| Light DOM (no Shadow DOM) | Pass `shadow: false` to r2wc | Simpler, but styles leak both ways |

---

## Result

The original TanStack Start SSR app remains fully functional.
The WC build is an **additive parallel output** — same source, different entry and Vite config.
