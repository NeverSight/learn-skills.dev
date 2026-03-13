---
name: encore-inertia
description: Use when building Inertia.js pages with Encore.ts, rendering pages from raw endpoints, setting up the Inertia adapter, sharing request-scoped props, configuring Vite integration, or mounting the React client app with mountInertiaApp.
---

# encore-inertia

Inertia.js adapter for Encore.ts. Lets you build React SPAs driven by Encore raw endpoints — no client-side router needed.

## Quick Reference

| Export | Import path | Purpose |
|---|---|---|
| `createInertiaAdapter` | `encore-inertia` | Create server-side adapter (render, share, getAssetTags) |
| `mountInertiaApp` | `encore-inertia/react` | Mount React app on the client |

## Installation

```bash
npm install encore-inertia
npm install react react-dom @inertiajs/react    # peer deps for React client
npm install -D vite @vitejs/plugin-react         # build tooling
```

## Server Setup

### 1. Create an Encore service

```ts
// frontend/encore.service.ts
import { Service } from "encore.dev/service";

export default new Service("frontend");
```

### 2. Create the adapter (one per app)

```ts
// frontend/inertia-setup.ts
import { createInertiaAdapter } from "encore-inertia";

export const inertia = createInertiaAdapter({
  viteEntry: "frontend/src/app.tsx",  // must match Vite rollupOptions.input
  title: "My App",                    // optional, default "Encore App"
});
```

**Config options:**

| Option | Default | Description |
|---|---|---|
| `viteEntry` | *(required)* | Vite manifest key matching your entry file |
| `title` | `"Encore App"` | HTML `<title>` |
| `manifestPath` | `"frontend/dist/.vite/manifest.json"` | Path to Vite manifest |
| `devServerUrl` | `"http://localhost:5173"` | Vite dev server URL |
| `rootId` | `"app"` | Root element ID for React mount |
| `lang` | `"en"` | HTML lang attribute |
| `version` | `"1.0"` | Inertia protocol version |
| `head` | `""` | Extra HTML for `<head>` (meta tags, fonts) |
| `renderHtml` | *(built-in)* | Full custom HTML template function `(page, assetTags) => string` |

### 3. Define page endpoints using `api.raw`

```ts
// frontend/pages.ts
import { api } from "encore.dev/api";
import { inertia } from "./inertia-setup";
import Home from "./src/pages/Home";
import About from "./src/pages/About";

export const home = api.raw(
  { expose: true, method: "GET", path: "/" },
  async (req, res) => {
    inertia.render(req, res, Home, { greeting: "Hello!" });
  },
);

export const about = api.raw(
  { expose: true, method: "GET", path: "/about" },
  async (req, res) => {
    inertia.render(req, res, About);  // no props needed
  },
);
```

**Key rules:**
- Pass the **component function** (not a string name) — props are type-checked against the component
- Props are required when the component expects them, optional when it doesn't
- Use Encore `api.raw` endpoints — the adapter reads `req`/`res` directly

### 4. Create page components

```tsx
// frontend/src/pages/Home.tsx
import { Link } from "@inertiajs/react";

interface HomeProps {
  greeting: string;
}

export default function Home({ greeting }: HomeProps) {
  return (
    <div>
      <h1>{greeting}</h1>
      <Link href="/about">About</Link>
    </div>
  );
}
```

Components are default-exported React functions. The adapter resolves them by `component.name`, so use named function exports (not arrow functions assigned to variables).

### 5. Shared data

Use `share()` for request-scoped props merged into every page response:

```ts
export const home = api.raw(
  { expose: true, method: "GET", path: "/" },
  async (req, res) => {
    inertia.share(req, { user: { name: "Alice" } });
    inertia.share(req, { flash: { success: "Welcome!" } });
    inertia.render(req, res, Home, { greeting: "Hello!" });
    // final props = { user: ..., flash: ..., greeting: "Hello!" }
  },
);
```

- Call `share()` before `render()` — accumulates across calls
- Page-level props override shared props
- Scoped to the request (no leaking between requests)

### 6. Serve static assets

```ts
// frontend/static.ts
import { api } from "encore.dev/api";

export const assets = api.static({
  expose: true,
  path: "/assets/*path",
  dir: "./dist/assets",
});
```

### 7. Create the static assets directory

Encore requires the `api.static` directory to exist at startup. Before running `encore run` for the first time, create it:

```bash
mkdir -p frontend/dist/assets
```

After that, `npm run build` (Vite) will populate it automatically.

## Client Setup

### 1. Mount the React app

```tsx
// frontend/src/app.tsx
import { mountInertiaApp } from "encore-inertia/react";

mountInertiaApp({
  pages: import.meta.glob("./pages/**/*.tsx", { eager: true }),
});
```

`mountInertiaApp` resolves page components by matching the component name against the glob keys. The `rootId` option (default `"app"`) must match the server adapter's `rootId`.

### 2. Vite config

```ts
// vite.config.ts
import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

export default defineConfig({
  plugins: [react()],
  build: {
    manifest: true,
    outDir: "frontend/dist",
    rollupOptions: {
      input: "frontend/src/app.tsx",  // must match adapter's viteEntry
    },
  },
  server: {
    origin: "http://localhost:5173",
    cors: { origin: "http://localhost:4000" },
  },
});
```

**Critical:** `rollupOptions.input` must match the `viteEntry` passed to `createInertiaAdapter`.

### 3. Custom HTML template

For full control over the HTML shell, provide a `renderHtml` function. When set, it overrides `title`, `lang`, `head`, and `rootId`:

```ts
const inertia = createInertiaAdapter({
  viteEntry: "frontend/src/app.tsx",
  renderHtml: (page, assetTags) => `<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    ${assetTags}
</head>
<body>
    <div id="app" data-page='${JSON.stringify(page)}'></div>
</body>
</html>`,
});
```

- `page` — the Inertia page object (`{ component, props, url, version }`)
- `assetTags` — pre-built `<script>` and `<link>` tags from the Vite manifest

## Running

Add scripts to `package.json`:

```json
{
  "scripts": {
    "build": "vite build",
    "dev:frontend": "vite dev"
  }
}
```

The `"build": "vite build"` script is required for deploying to Encore Cloud — Encore runs `npm run build` during deployment to compile the frontend assets.

**Development** (two terminals):

```bash
encore run              # Terminal 1: Encore backend
npm run dev:frontend    # Terminal 2: Vite dev server with HMR
```

The adapter automatically falls back to the Vite dev server when no production manifest is found.

**Production:**

```bash
npm run build    # Build frontend assets
encore run       # Start Encore
```

## How It Works

1. A browser request hits an Encore raw endpoint
2. The endpoint calls `inertia.render(req, res, Component, { props })`
3. **First visit** (no `X-Inertia` header): responds with a full HTML page containing Vite asset tags and the page object in a `data-page` attribute
4. **Subsequent navigation** (`X-Inertia` header present): responds with just the JSON page object — the Inertia client swaps the component without a full reload

## Project Structure

```
my-app/
  encore.app
  package.json
  vite.config.ts
  frontend/
    encore.service.ts       # Encore service definition
    inertia-setup.ts        # createInertiaAdapter config
    pages.ts                # api.raw endpoints calling inertia.render()
    static.ts               # api.static for built assets
    src/
      app.tsx               # mountInertiaApp client entry
      pages/
        Home.tsx            # React page components
        About.tsx
    dist/                   # Vite build output (gitignored)
```

## Common Mistakes

| Mistake | Fix |
|---|---|
| `viteEntry` doesn't match `rollupOptions.input` | Both must be the same path string |
| Passing a string to `render()` instead of a component | Import the React component and pass it directly |
| Using `api()` instead of `api.raw()` | Inertia needs raw HTTP access — always use `api.raw` |
| Forgetting `manifest: true` in Vite config | Required for production asset resolution |
| `rootId` mismatch between server and client | Both default to `"app"` — only change if you set it in both places |
| Calling `share()` after `render()` | `share()` must be called before `render()` |
| `api.static` dir doesn't exist on first run | Run `mkdir -p frontend/dist/assets` before `encore run` |

## Peer Dependencies

```json
{
  "react": ">=18",
  "react-dom": ">=18",
  "@inertiajs/react": ">=2"
}
```

The React/Inertia deps are optional — only needed when using the `encore-inertia/react` client export.
