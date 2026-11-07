---
name: isolet-widget-isolation
description: Package any component into a self-contained, isolated widget with shadow DOM, scoped styles, and multi-framework support
triggers:
  - create an isolated widget
  - package component as widget
  - shadow DOM isolation for component
  - self-contained widget bundle
  - isolet widget
  - embed widget on any page
  - build a drop-in script tag widget
  - isolate React component styles
---

# isolet Widget Isolation

> Skill by [ara.so](https://ara.so) — Daily 2026 Skills collection.

`isolet-js` packages any component (React, Solid, Svelte, vanilla JS, etc.) into a self-contained, isolated widget. Widgets render inside shadow DOM by default, so styles are fully scoped. Output formats include IIFE (script tag), ESM, and CommonJS.

## Install

```sh
npm install isolet-js
```

## Core API: `createIsolet`

```ts
import { createIsolet } from "isolet-js";

const widget = createIsolet({
  name: "my-widget",          // required: unique identifier
  mount: myMountFn,           // required: (container, props) => cleanup | void
  css: `h1 { color: red; }`,  // optional: scoped CSS
  isolation: "shadow-dom",    // "shadow-dom" | "scoped" | "none"
  shadowMode: "open",         // "open" | "closed"
  hostAttributes: { "data-widget": "true" },
  zIndex: 9999,
});

widget.mount(document.body, { title: "Hello" }); // mount into target
widget.update({ title: "Updated" });             // update props
widget.unmount();                                // tear down

// Instance properties
widget.container;   // HTMLElement — the render container
widget.shadowRoot;  // ShadowRoot | null
widget.mounted;     // boolean
```

## Framework Adapters

### React

```tsx
import { createIsolet } from "isolet-js";
import { react } from "isolet-js/react";

function Greeting({ name }: { name: string }) {
  return <h1>Hello, {name}!</h1>;
}

const widget = createIsolet({
  name: "greeting",
  mount: react(Greeting),
  css: `h1 { color: tomato; font-family: sans-serif; }`,
});

widget.mount(document.body, { name: "World" });
widget.update({ name: "Isolet" });
widget.unmount();
```

### Vanilla JS

```ts
import { createIsolet } from "isolet-js";
import { vanilla } from "isolet-js/vanilla";

const widget = createIsolet({
  name: "counter",
  mount: vanilla((container, props) => {
    let count = props.initial ?? 0;
    const btn = document.createElement("button");
    btn.textContent = `Count: ${count}`;
    btn.onclick = () => {
      btn.textContent = `Count: ${++count}`;
    };
    container.appendChild(btn);

    // Return cleanup function
    return () => container.removeChild(btn);
  }),
});

widget.mount(document.getElementById("app"), { initial: 5 });
```

### Solid

```tsx
import { createIsolet } from "isolet-js";
import { render } from "solid-js/web";
import App from "./App";

const widget = createIsolet({
  name: "solid-widget",
  mount(container, props) {
    const dispose = render(() => <App {...props} />, container);
    return dispose; // dispose is the cleanup function
  },
});
```

### Svelte

```ts
import { createIsolet } from "isolet-js";
import App from "./App.svelte";

const widget = createIsolet({
  name: "svelte-widget",
  mount(container, props) {
    const app = new App({ target: container, props });
    return () => app.$destroy();
  },
});
```

## Isolation Modes

```ts
// Full CSS isolation — shadow DOM (default)
createIsolet({ name: "w", mount: fn, isolation: "shadow-dom" });

// Scoped — plain div wrapper, styles injected globally
createIsolet({ name: "w", mount: fn, isolation: "scoped" });

// No isolation — mounts directly into target element
createIsolet({ name: "w", mount: fn, isolation: "none" });
```

## CLI

```sh
npx isolet-js init            # scaffold isolet.config.ts
npx isolet-js build           # bundle widget(s) from config
npx isolet-js build --watch   # rebuild on file changes
npx isolet-js build --minify  # minified production build
```

## Config File

```ts
// isolet.config.ts
import { defineConfig } from "isolet-js";

export default defineConfig({
  name: "my-widget",
  entry: "./src/index.ts",
  styles: "./src/widget.css",       // CSS to inline; url() assets become data URIs
  format: ["iife", "esm"],          // output formats
  outDir: "./dist",                 // default: "dist"
  globalName: "MyWidget",           // global name for IIFE builds
  external: ["react"],              // don't bundle these deps
  dts: true,                        // emit .d.ts files
  minify: true,                     // minify output
  platform: "browser",              // target platform
});
```

### Multiple Widgets

```ts
export default defineConfig([
  { name: "widget-a", entry: "./src/a.ts", styles: "./src/a.css" },
  { name: "widget-b", entry: "./src/b.ts", format: ["esm"] },
]);
```

## CSS & Asset Handling

The build pipeline handles everything automatically:

- **`styles` in config** → CSS is read, `url()` references (fonts, images) inlined as data URIs, result available as `__ISOLET_CSS__` in your entry
- **`.css` imports** → converted to JS string exports (shadow DOM safe)
- **Asset imports** (`.png`, `.woff2`, `.mp3`, etc.) → inlined as data URIs
- **`styles: "./path.css"` in `createIsolet`** → resolved and inlined at build time

```ts
// Entry file using __ISOLET_CSS__ injected by CLI
import { createIsolet } from "isolet-js";
import { react } from "isolet-js/react";
import MyComponent from "./MyComponent";

declare const __ISOLET_CSS__: string;

export const widget = createIsolet({
  name: "my-widget",
  css: __ISOLET_CSS__,   // populated from config.styles at build time
  mount: react(MyComponent),
});
```

Or reference the CSS path directly (auto-resolved at build time):

```ts
createIsolet({
  name: "my-widget",
  styles: "./widget.css",  // isolet build resolves this
  mount: react(MyComponent),
});
```

### Manual Vite Plugin Setup

If using Vite directly instead of the CLI:

```ts
// vite.config.ts
import { defineConfig } from "vite";
import {
  cssTextPlugin,
  inlineAssetsPlugin,
  autoStylesPlugin,
} from "isolet-js/plugins";

export default defineConfig({
  plugins: [cssTextPlugin(), inlineAssetsPlugin(), autoStylesPlugin()],
});
```

## Script Tag (IIFE) Usage

```html
<script src="https://unpkg.com/isolet-js/dist/index.iife.js"></script>
<script>
  const { createIsolet } = __ISOLET__;

  const widget = createIsolet({
    name: "inline-widget",
    mount(container, props) {
      container.innerHTML = `<p>Hello, ${props.name ?? "World"}!</p>`;
    },
    css: `p { font-family: sans-serif; color: navy; }`,
  });

  widget.mount(document.body, { name: "Visitor" });
</script>
```

For a bundled custom widget via IIFE:

```ts
// isolet.config.ts
export default defineConfig({
  name: "my-widget",
  entry: "./src/index.ts",
  format: ["iife"],
  globalName: "MyWidget",
  minify: true,
});
```

```html
<!-- Resulting script tag distribution -->
<script src="./dist/my-widget.iife.js"></script>
<script>
  MyWidget.widget.mount(document.getElementById("root"), { title: "Hi" });
</script>
```

## Common Patterns

### Lazy-mount on demand

```ts
const widget = createIsolet({ name: "chat", mount: react(ChatApp), css: styles });

document.getElementById("open-chat").addEventListener("click", () => {
  if (!widget.mounted) {
    widget.mount(document.body, { userId: currentUserId });
  }
});

document.getElementById("close-chat").addEventListener("click", () => {
  widget.unmount();
});
```

### z-index overlay widget

```ts
const modal = createIsolet({
  name: "modal",
  mount: react(ModalComponent),
  css: modalStyles,
  zIndex: 10000,
  hostAttributes: { role: "dialog", "aria-modal": "true" },
});
```

### Reactive props updates

```ts
const widget = createIsolet({ name: "status", mount: react(StatusBar), css });
widget.mount(document.body, { status: "idle" });

// Later, update without remounting:
widget.update({ status: "loading" });
widget.update({ status: "done" });
```

## Troubleshooting

**Styles leaking in or out**
Use `isolation: "shadow-dom"` (default). Verify your `css` option or `styles` path is correctly set — without CSS in the shadow root, the host page styles will not apply inside.

**`__ISOLET_CSS__` is undefined**
This variable is only injected by the `isolet build` CLI when `styles` is set in config. For manual Vite builds, add `autoStylesPlugin()` to your Vite config.

**Component not rendering**
Ensure the `mount` function appends to `container`, not to `document.body`. In shadow DOM mode, the container is inside the shadow root.

**Cleanup not running**
Return a cleanup function from your `mount` callback. Without it, `widget.unmount()` cannot tear down framework internals (timers, subscriptions, etc.).

**IIFE global not found**
Check `globalName` in config matches what you reference in HTML. The runtime core exposes `globalThis.__ISOLET__` when no `globalName` is set.

**External deps not found at runtime**
If you set `external: ["react"]`, the host page must provide `React` globally or via module federation before your widget script loads.
