---
name: streamdeck-react
description: >-
  Build Stream Deck plugins with React using @fcannizzaro/streamdeck-react. Use for: creating
  action components, wiring keys/dials/touch input to React, Rollup bundling for
  Stream Deck, settings sync, shared state, and Takumi image rendering.
---

# streamdeck-react

A custom React renderer that turns JSX into rendered images for Elgato Stream Deck hardware. Each action instance gets its own isolated React root with full hooks, state, and lifecycle support.

## When to Use This Skill

Use when the user is:

- Creating or modifying a Stream Deck plugin that uses `@fcannizzaro/streamdeck-react`
- Asking about rendering React components on Stream Deck keys or dials, or handling touch input
- Working with `@elgato/streamdeck` SDK in a React-based plugin
- Implementing a custom adapter for web simulation or testing
- Setting up Rollup bundling for a Stream Deck plugin with native Takumi bindings
- Scaffolding a brand new plugin and needs a sensible project template or starter example

## Architecture (5-Stage Pipeline)

```
React Tree --> Reconciler --> VNode Tree --> Takumi --> Adapter --> setImage/setFeedback
(JSX+Hooks)   (host config)   (plain JS)   (JSX->PNG)  (bridge)    (hardware/simulator)
```

1. Your components render standard React with hooks and state.
2. A custom `react-reconciler` manages the fiber tree.
3. On commit, host nodes form a virtual tree of `{ type, props, children }` with back-pointers for dirty propagation.
4. The Takumi renderer converts the tree to a PNG/WebP image buffer via a direct VNode-to-Takumi bypass (skips createElement + fromJsx).
5. The adapter pushes the image to the backend via `action.setImage()` or `action.setFeedback()`. The default `physicalDevice()` adapter wraps the Elgato SDK; custom adapters handle it differently.

### 4-Phase Skip Hierarchy

Every render passes through a multi-tier skip hierarchy to avoid redundant work:

```
Phase 1: Dirty-flag check (O(1)) → skip if no VNode mutated
Phase 2: Merkle hash → Image cache lookup → skip if hash matches cached render
Phase 3: Takumi render (main thread or worker) → rasterize
Phase 4: xxHash output dedup → skip hardware push if identical to last frame
```

Two entry points: `renderToDataUri` (keys/dials → base64 data URI) and `renderToRaw` (TouchStrip → raw RGBA Buffer).

### Flush Coordinator

When multiple roots request flushes in the same tick, the FlushCoordinator batches them via microtask and processes in priority order:

- Priority 0 (animating) → 1 (interactive) → 2 (normal) → 3 (idle)
- Sequential execution ensures higher-priority roots get first access to the USB bus.

### Manifest Codegen

The bundler plugins (Rollup and Vite) auto-generate `src/streamdeck-env.d.ts` from `manifest.json`:

- Enables compile-time UUID validation (typos caught by TypeScript)
- Enforces controller-aware `defineAction()` types (Keypad → `key` required, Encoder → `dial` or `touchStrip` required)
- Skips write if content unchanged (avoids unnecessary recompilation in watch mode)

Each visible action instance on the hardware gets its own isolated React root. No shared state between roots unless you use an external store (Zustand, Jotai) or the wrapper API.

## Adapter Layer

The adapter layer abstracts the `@elgato/streamdeck` SDK behind a pluggable `StreamDeckAdapter` interface. This makes the SDK an optional peer dependency and enables alternative backends (web simulator, test harness).

- `physicalDevice()` is the default adapter wrapping the real Elgato SDK. It is the **only** module that value-imports from `@elgato/streamdeck`.
- Pass a custom adapter via `createPlugin({ adapter: myAdapter() })`.
- All hooks (`useOpenUrl`, `useSwitchProfile`, `useSendToPI`, `useShowAlert`, `useShowOk`, `useTitle`, `useDialHint`) route through the adapter.
- `AdapterActionHandle` is a flat interface unifying Key/Dial/Action. Inapplicable methods (e.g., `setImage` on dial) no-op.
- See [references/adapter.md](references/adapter.md) for full interface definitions and custom adapter example.

## Project Setup

### New Plugin

For greenfield projects, prefer the scaffolder first:

```bash
npm create streamdeck-react@latest
```

It asks for the plugin UUID, author, platforms, native targets, starter example, and whether to use React Compiler, then generates a working project.

To use React Compiler via CLI flag:

```bash
npm create streamdeck-react@latest --react-compiler true
```

React Compiler automatically memoizes components at build time, preventing unnecessary re-renders. This is especially beneficial in this environment because every re-render triggers an expensive rasterization pipeline (VNode tree -> Takumi layout -> Rust PNG render -> hardware).

If the user wants to build it manually, use this structure:

A minimal plugin project needs:

```
my-plugin/
  src/
    plugin.ts           # Entry point
    actions/
      my-action.tsx     # Action component
  com.example.my-plugin.sdPlugin/
    manifest.json       # Stream Deck manifest
    bin/                # Rollup output goes here
    imgs/               # Action and plugin icons
  rollup.config.mjs
  package.json
  tsconfig.json
```

### Dependencies

```bash
# Runtime
npm install @fcannizzaro/streamdeck-react react

# Runtime support used by the Stream Deck SDK
npm install ws

# Fonts (use any @fontsource or @fontsource-variable package)
npm install @fontsource-variable/inter

# Build tooling (default -- esbuild)
npm install -D rollup @rollup/plugin-node-resolve @rollup/plugin-commonjs @rollup/plugin-json rollup-plugin-esbuild

# Build tooling (with React Compiler -- replaces esbuild)
# npm install -D rollup @rollup/plugin-node-resolve @rollup/plugin-commonjs @rollup/plugin-json @rollup/plugin-babel @babel/core @babel/preset-typescript @babel/preset-react babel-plugin-react-compiler

# Types (if using TypeScript)
npm install -D @types/react
```

Also install the platform-specific Takumi native binding packages that match the targets you pass to `streamDeckReact({ targets })`, for example:

```bash
# macOS Apple Silicon
npm install @takumi-rs/core-darwin-arm64

# macOS Intel
npm install @takumi-rs/core-darwin-x64

# Windows x64
npm install @takumi-rs/core-win32-x64-msvc
```

See [references/bundling.md](references/bundling.md) for the full platform matrix.

### package.json

Must use `"type": "module"`. Example:

```json
{
  "type": "module",
  "scripts": {
    "build": "rollup -c",
    "dev": "rollup -c -w"
  }
}
```

### tsconfig.json

```json
{
  "compilerOptions": {
    "lib": ["ESNext"],
    "target": "ESNext",
    "module": "Preserve",
    "jsx": "react-jsx",
    "moduleResolution": "bundler",
    "allowImportingTsExtensions": true,
    "noEmit": true,
    "strict": true,
    "skipLibCheck": true
  },
  "include": ["src"]
}
```

## Core Workflow

### Step 1: Define Actions

```tsx
// src/actions/counter.tsx
import { useState } from "react";
import { defineAction, useKeyDown, useKeyUp, tw } from "@fcannizzaro/streamdeck-react";

function CounterKey() {
  const [count, setCount] = useState(0);
  const [pressed, setPressed] = useState(false);

  useKeyDown(() => {
    setCount((c) => c + 1);
    setPressed(true);
  });

  useKeyUp(() => setPressed(false));

  return (
    <div
      className={tw(
        "flex flex-col items-center justify-center w-full h-full gap-1",
        pressed ? "bg-[#2563eb]" : "bg-[#0f172a]",
      )}
    >
      <span className="text-white/70 text-[12px] font-medium">COUNT</span>
      <span className="text-white text-[36px] font-bold">{count}</span>
    </div>
  );
}

export const counterAction = defineAction({
  uuid: "com.example.my-plugin.counter",
  key: CounterKey,
});
```

### Step 2: Create the Plugin Entry

```ts
// src/plugin.ts
import { createPlugin } from "@fcannizzaro/streamdeck-react";
import InterRegular from "@fontsource-variable/inter/files/inter-latin-wght-normal.woff2";
import { counterAction } from "./actions/counter.tsx";

const plugin = createPlugin({
  fonts: [
    {
      name: "Inter",
      data: InterRegular,
      weight: 400,
      style: "normal",
    },
  ],
  actions: [counterAction],
});

await plugin.connect();
```

### Step 3: Configure Rollup

**Default setup (esbuild)**:

```js
// rollup.config.mjs
import { builtinModules } from "node:module";
import resolve from "@rollup/plugin-node-resolve";
import commonjs from "@rollup/plugin-commonjs";
import json from "@rollup/plugin-json";
import esbuild from "rollup-plugin-esbuild";
import { streamDeckReact } from "@fcannizzaro/streamdeck-react/rollup";

const PLUGIN_DIR = "com.example.my-plugin.sdPlugin";
const builtins = new Set(builtinModules.flatMap((m) => [m, `node:${m}`]));

export default {
  input: "src/plugin.ts",
  output: {
    file: `${PLUGIN_DIR}/bin/plugin.mjs`,
    format: "es",
    sourcemap: true,
    inlineDynamicImports: true,
  },
  external: (id) => builtins.has(id),
  plugins: [
    resolve({ preferBuiltins: true }),
    commonjs(),
    json(),
    esbuild({ target: "node20", jsx: "automatic" }),
    streamDeckReact({
      targets: [{ platform: "darwin", arch: "arm64" }],
    }),
  ],
};
```

**With React Compiler** (replaces esbuild with Babel):

```js
// rollup.config.mjs
import { builtinModules } from "node:module";
import { babel } from "@rollup/plugin-babel";
import resolve from "@rollup/plugin-node-resolve";
import commonjs from "@rollup/plugin-commonjs";
import json from "@rollup/plugin-json";
import { streamDeckReact } from "@fcannizzaro/streamdeck-react/rollup";

const PLUGIN_DIR = "com.example.my-plugin.sdPlugin";
const builtins = new Set(builtinModules.flatMap((m) => [m, `node:${m}`]));

export default {
  input: "src/plugin.ts",
  output: {
    file: `${PLUGIN_DIR}/bin/plugin.mjs`,
    format: "es",
    sourcemap: true,
    inlineDynamicImports: true,
  },
  external: (id) => builtins.has(id),
  plugins: [
    resolve({ preferBuiltins: true }),
    commonjs(),
    json(),
    babel({
      babelHelpers: "bundled",
      extensions: [".js", ".jsx", ".ts", ".tsx"],
      exclude: "**/node_modules/**",
      plugins: ["babel-plugin-react-compiler"],
      presets: ["@babel/preset-typescript", ["@babel/preset-react", { runtime: "automatic" }]],
    }),
    streamDeckReact({
      targets: [{ platform: "darwin", arch: "arm64" }],
    }),
  ],
};
```

For production builds, pass explicit `targets`. In watch mode, `streamDeckReact()` can infer the current supported host target.

### Step 4: Set Up manifest.json

```json
{
  "$schema": "https://schemas.elgato.com/streamdeck/plugins/manifest.json",
  "Actions": [
    {
      "UUID": "com.example.my-plugin.counter",
      "Name": "Counter",
      "Icon": "imgs/actions/counter",
      "Controllers": ["Keypad"],
      "States": [{ "Image": "imgs/actions/counter" }]
    }
  ],
  "Author": "Your Name",
  "CodePath": "bin/plugin.mjs",
  "Icon": "imgs/plugin-icon",
  "Name": "My Plugin",
  "Nodejs": { "Version": "20" },
  "UUID": "com.example.my-plugin",
  "Version": "0.0.0.1",
  "SDKVersion": 2,
  "Software": { "MinimumVersion": "7.1" }
}
```

> **Critical**: The `UUID` in each manifest action must exactly match the `uuid` passed to `defineAction()`.

### Step 5: Dev

```bash
npx rollup -c -w
```

Install the `.sdPlugin` folder in the Stream Deck app.

If your `package.json` has a `dev` script configured, you can also just run `bun dev` (or `npm run dev` / `pnpm dev`).

## Hook Quick Reference

| Category  | Hooks                                       | Purpose                                                   |
| --------- | ------------------------------------------- | --------------------------------------------------------- |
| Events    | `useKeyDown`, `useKeyUp`                    | Key press/release                                         |
| Events    | `useDialRotate`, `useDialDown`, `useDialUp` | Encoder rotation/press                                    |
| Events    | `useTouchTap`                               | Touch strip tap                                           |
| Events    | `useDialHint`                               | Set encoder trigger descriptions                          |
| Gestures  | `useTap`                                    | Single tap (auto-delayed when useDoubleTap is active)     |
| Gestures  | `useLongPress`                              | Key held for configurable duration (default 500ms)        |
| Gestures  | `useDoubleTap`                              | Two rapid taps within configurable window (default 250ms) |
| Settings  | `useSettings`, `useGlobalSettings`          | Bidirectional settings sync                               |
| Lifecycle | `useWillAppear`, `useWillDisappear`         | Action mount/unmount                                      |
| Context   | `useDevice`, `useAction`, `useCanvas`       | Device/action/canvas metadata                             |
| Context   | `useStreamDeck`                             | Adapter and action handle                                 |
| SDK       | `useOpenUrl`, `useSwitchProfile`            | System actions                                            |
| SDK       | `useSendToPI`, `usePropertyInspector`       | PI communication                                          |
| SDK       | `useShowAlert`, `useShowOk`, `useTitle`     | Key overlays                                              |
| Utility   | `useInterval`, `useTimeout`, `usePrevious`  | Timers and helpers                                        |
| Utility   | `useTick`                                   | Animation frame loop                                      |
| Animation | `useSpring`, `useTween`                     | Physics and easing-based value animation                  |
| Animation | `SpringPresets`, `Easings`                  | Built-in spring presets and easing functions              |

See [references/hooks.md](references/hooks.md) for full signatures and usage.

## Component Quick Reference

| Component       | Element | Purpose                                                                       |
| --------------- | ------- | ----------------------------------------------------------------------------- |
| `Box`           | `div`   | Flex container with shorthand props (`center`, `padding`, `gap`, `direction`) |
| `Text`          | `span`  | Text with shorthand props (`size`, `color`, `weight`, `align`, `font`)        |
| `Image`         | `img`   | Image with required `width`/`height`, optional `fit`                          |
| `Icon`          | `svg`   | Single SVG path icon with `path`, `size`, `color`                             |
| `ProgressBar`   | `div`   | Horizontal progress bar with `value`/`max`                                    |
| `CircularGauge` | `svg`   | Ring/arc gauge with `value`/`max`/`size`/`strokeWidth`                        |
| `ErrorBoundary` | --      | Catches errors, renders fallback                                              |

All components are optional convenience wrappers. Raw `div`, `span`, `img`, `svg` elements work directly.

See [references/components.md](references/components.md) for full props tables.

## Styling

Three approaches, all valid:

1. **Tailwind classes** via `className` -- resolved by Takumi at render time (no CSS build step):

   ```tsx
   <div className="flex items-center justify-center w-full h-full bg-[#1a1a1a]">
   ```

2. **`tw()` utility** for conditional classes (like `clsx`):

   ```tsx
   <div className={tw('w-full h-full', pressed && 'bg-green-500')}>
   ```

3. **Inline `style`** for exact control:
   ```tsx
   <div style={{ width: '100%', height: '100%', background: '#1a1a1a' }}>
   ```

## State Management Decision Guide

| Need                                             | Solution                                                              |
| ------------------------------------------------ | --------------------------------------------------------------------- |
| Simple per-action state                          | `useState` / `useReducer`                                             |
| Persist per-action settings across reloads       | `useSettings<T>()`                                                    |
| Plugin-wide shared config                        | `useGlobalSettings<T>()`                                              |
| Shared state across actions (no provider needed) | Zustand store in module scope                                         |
| Shared state with provider pattern               | Jotai/React Context via `wrapper` on `createPlugin` or `defineAction` |

## Encoder / Dial Actions

For Stream Deck+ encoders, provide a `dial` component in `defineAction`. If omitted, the `key` component is used as fallback on encoder slots.

```tsx
export const volumeAction = defineAction({
  uuid: "com.example.my-plugin.volume",
  key: VolumeKey,
  dial: VolumeDial,
});
```

In `manifest.json`, encoder actions use `"Controllers": ["Encoder"]` and require an `"Encoder"` block:

```json
{
  "UUID": "com.example.my-plugin.volume",
  "Controllers": ["Encoder"],
  "Encoder": {
    "layout": "$B1",
    "TriggerDescription": {
      "Rotate": "Adjust volume",
      "Push": "Mute / Unmute"
    }
  }
}
```

For touch interaction on Stream Deck+, use `useTouchTap()` inside the mounted action root. Treat touch as input handling, not as a separate primary rendering surface.

## Critical Gotchas

1. **Fonts are mandatory** -- the renderer cannot access system fonts. Install a font package (e.g. `@fontsource-variable/inter`) and import the font file directly. The bundler plugin inlines it as a `Buffer`. Supported formats: `.ttf`, `.otf`, `.woff`, `.woff2`.
2. **`plugin.connect()` must be called last** -- after `createPlugin()` and all setup.
3. **UUID mismatch** -- the `uuid` in `defineAction()` must exactly match the `UUID` in `manifest.json`.
4. **`streamDeckReact({ targets })` is required for production builds** -- it copies the Takumi `.node` binaries into output. Without them, the plugin crashes on startup.
5. **Install `ws` and matching `@takumi-rs/core-*` packages** -- they must line up with the targets passed to `streamDeckReact({ targets })`.
6. **No animated images** -- each `setImage` call is a static frame. Use `useTick` for manual animation loops, or the higher-level `useSpring` and `useTween` hooks for physics-based and easing-based animation.
7. **Design for 72x72 minimum** -- smallest key size. Use `useCanvas()` to adapt to larger devices.
8. **Use simple layouts** -- this is not a browser DOM. Stick to flex layouts, fixed sizes, and simple elements (`div`, `span`, `img`, `svg`, `p`).
9. **Animation FPS** -- Stream Deck hardware refreshes at max 30Hz. The `useTick`, `useSpring`, and `useTween` hooks default to 30fps (clamped). Design animations accordingly.

## Verification Checklist

When scaffolding or modifying a @fcannizzaro/streamdeck-react plugin, verify:

- [ ] `@fcannizzaro/streamdeck-react` and `react` are in dependencies
- [ ] `ws` is installed for the Stream Deck SDK runtime
- [ ] Matching `@takumi-rs/core-*` packages are installed for every `streamDeckReact({ targets })` entry
- [ ] `package.json` has `"type": "module"`
- [ ] `tsconfig.json` has `"jsx": "react-jsx"`
- [ ] At least one font is installed (e.g. `@fontsource-variable/inter`) and imported in `createPlugin()`
- [ ] Every `defineAction()` UUID matches its `manifest.json` UUID
- [ ] `rollup.config.mjs` uses `streamDeckReact({ targets })` for production builds
- [ ] `manifest.json` `CodePath` points to the Rollup output (e.g., `bin/plugin.mjs`)
- [ ] `manifest.json` declares `"Nodejs": { "Version": "20" }`
- [ ] Encoder actions have `"Controllers": ["Encoder"]` and an `"Encoder"` block in manifest
- [ ] `plugin.connect()` is called after `createPlugin()`
- [ ] Build completes without errors: `npx rollup -c`
- [ ] If React Compiler is enabled: output bundle contains `react.memo_cache_sentinel` (proof compiler is active)

## DevTools

A browser-based inspector for debugging plugins during development. When enabled, the plugin starts an HTTP + SSE (Server-Sent Events) server on `localhost` (port range 39400-39499) and the browser UI auto-discovers running plugins by scanning that range.

### Enabling

```ts
const plugin = createPlugin({
  devtools: true, // starts the devtools server (port derived from plugin UUID)
  fonts: [
    // ...your fonts
  ],
  actions: [
    /* ... */
  ],
});
```

### Opening the DevTools

- **Hosted** (no install): [streamdeckreact.fcannizzaro.com/devtools](https://streamdeckreact.fcannizzaro.com/devtools)
- **Local**: `npx @fcannizzaro/streamdeck-react-devtools` (npm package `@fcannizzaro/streamdeck-react-devtools`)

### Panels

| Panel       | Description                                                                   |
| ----------- | ----------------------------------------------------------------------------- |
| Console     | Intercepted `console.log/warn/error/info/debug` output                        |
| Network     | Intercepted `fetch` requests and responses                                    |
| Elements    | VNode tree inspector with element highlighting on the physical device         |
| Preview     | Live rendered images for every active action and touch bar                    |
| Events      | EventBus emissions (`keyDown`, `dialRotate`, `touchTap`, etc.)                |
| Performance | Render pipeline metrics: flush counts, skip rates, cache stats, render timing |

### Key Details

- **Element highlighting** -- hover a node in the Elements tree to highlight it with a cyan overlay on the Stream Deck hardware.
- **Multi-plugin support** -- discovers and switches between multiple running plugins.
- **Automatic production stripping** -- all devtools code, the `ws` dependency, and instrumentation hooks are removed from the bundle when `NODE_ENV=production` (non-watch builds). Zero overhead in release builds.

## Detailed References

- [references/api-surface.md](references/api-surface.md) -- Full public API table
- [references/adapter.md](references/adapter.md) -- Adapter layer interfaces and custom adapter guide
- [references/plugin-setup.md](references/plugin-setup.md) -- `createPlugin` and `defineAction` details
- [references/hooks.md](references/hooks.md) -- All hooks with signatures and payloads
- [references/components.md](references/components.md) -- Component props tables
- [references/bundling.md](references/bundling.md) -- Rollup/Rolldown config and native binding details
- [references/device-sizes.md](references/device-sizes.md) -- Key/encoder/touch dimensions per device
- [references/limitations.md](references/limitations.md) -- Styling constraints and known limitations
