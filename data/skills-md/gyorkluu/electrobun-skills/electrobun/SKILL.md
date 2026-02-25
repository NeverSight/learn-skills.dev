---
name: electrobun
description: >
  Build, scaffold, debug, and ship desktop applications with Electrobun — an ultra-fast TypeScript desktop app framework using Bun as the runtime and native OS webviews. This skill provides comprehensive guidance for building cross-platform desktop applications with TypeScript, covering project scaffolding, window management, main↔webview RPC communication, native UI integration, auto-updates, and distribution. Use this skill when the user mentions Electrobun, wants to build a desktop app with TypeScript or Bun, asks about BrowserWindow, BrowserView, RPC between main and webview processes, app bundling, cross-platform desktop development, or needs help with menus, tray icons, updater setup, or packaging for distribution. Also trigger when they say "desktop app" and are using or considering Bun. Common triggers include: "create Electrobun app", "desktop application TypeScript", "Bun desktop app", "BrowserWindow", "webview RPC", "Electrobun tutorial", "desktop app updater", "cross-platform desktop", "macOS app with Bun", "Windows desktop app TypeScript", or any discussion about building native desktop applications with web technologies and Bun runtime.
license: MIT
metadata:
  author: Blackboard
  version: "1.0.0"
  repository: https://github.com/blackboardsh/electrobun
  documentation: https://blackboard.sh/electrobun/
---

# Electrobun

Electrobun is a TypeScript-first desktop app framework using Bun (runtime + bundler) and the system's native webview. Build apps that are ~14MB, with updates ~14KB, and startup <50ms.

## Quick Start

### Initialize New Project

```bash
bunx electrobun init          # Interactive scaffold
bun run dev                   # Development mode
bun run build                 # Production bundle
```

Choose from templates:
- **hello-world**: Minimal starter
- **react-tailwind-vite**: React + Tailwind + Vite
- **svelte**: Svelte framework
- **photo-booth**: Camera access example
- **multitab-browser**: Tab-based browser example

### Project Structure

```
my-app/
├── electrobun.config.ts      # Build configuration
├── src/
│   ├── bun/
│   │   └── main.ts           # Main process (Bun)
│   └── views/
│       └── mainview/
│           ├── index.html
│           └── index.ts      # Webview frontend
└── package.json
```

## Core Concepts

### Main Process vs Webview

- **Main Process** (`src/bun/main.ts`): Runs in Bun, has full system access, manages windows, handles RPC
- **Webview Process** (`src/views/*/index.ts`): Runs in OS webview, sandboxed, handles UI, calls RPC

### BrowserWindow

Create and manage application windows.

```ts
import { BrowserWindow } from "electrobun/bun";

const win = new BrowserWindow({
  title: "My App",
  url: "views://mainview/index.html",
  width: 1200,
  height: 800,
  frame: true,  // Standard window frame
  styleMask: ["titled", "closable", "miniaturizable", "resizable"],
});
```

**Key Options:**
- `title`: Window title
- `url`: Load URL (use `views://` protocol for bundled views)
- `width`, `height`: Window dimensions
- `x`, `y`: Window position (optional)
- `frame`: Show standard window frame (true/false)
- `styleMask`: Array of window controls (macOS)
- `titleBarStyle`: "default" | "hidden" | "hiddenInset"
- `trafficLightPosition`: Custom position for macOS traffic lights

**Methods:**
```ts
win.loadURL("views://otherview/index.html")
win.setTitle("New Title")
win.resize({ width: 1024, height: 768 })
win.move({ x: 100, y: 100 })
win.show() / win.hide()
win.close()
win.focus()
win.minimize() / win.maximize() / win.fullscreen()
```

### RPC: Main ↔ Webview Communication

Electrobun's killer feature — typed, fast, bidirectional RPC.

**Main Process (bun/main.ts):**
```ts
import { BrowserWindow } from "electrobun/bun";

const win = new BrowserWindow({ /* ... */ });

// Define what main exposes TO the webview
win.defineRpc({
  handlers: {
    async getUser(id: string) {
      // Full system access here
      const user = await db.getUser(id);
      return { name: user.name, id: user.id };
    },
    async saveFile(path: string, content: string) {
      await Bun.write(path, content);
      return { success: true };
    }
  }
});

// Call webview methods FROM main
const result = await win.rpc.updateUI({ data: "new data" });
```

**Webview (views/mainview/index.ts):**
```ts
import { Electroview } from "electrobun/browser";

const electroview = new Electroview();

// Call main process functions
const user = await electroview.rpc.getUser("123");
const result = await electroview.rpc.saveFile("/path/to/file.txt", "content");

// Define handlers main can call
electroview.defineRpc({
  handlers: {
    async updateUI(data: any) {
      // Update DOM here
      document.getElementById("content").textContent = data.data;
      return { updated: true };
    }
  }
});
```

**Key Points:**
- Fully type-safe (with TypeScript)
- Bidirectional (main can call webview, webview can call main)
- Async by default
- Serialize data automatically (JSON)

### Application Menu

```ts
import { ApplicationMenu } from "electrobun/bun";

ApplicationMenu.setMenu([
  {
    label: "File",
    submenu: [
      { 
        label: "New Window", 
        accelerator: "CmdOrCtrl+N",
        action: () => createWindow()
      },
      { type: "separator" },
      { 
        label: "Quit", 
        accelerator: "CmdOrCtrl+Q",
        action: () => process.exit(0)
      },
    ]
  },
  {
    label: "Edit",
    submenu: [
      { role: "undo" },
      { role: "redo" },
      { type: "separator" },
      { role: "cut" },
      { role: "copy" },
      { role: "paste" },
    ]
  }
]);
```

**Built-in roles:** `undo`, `redo`, `cut`, `copy`, `paste`, `selectAll`, `minimize`, `close`, `quit`

### Context Menu

```ts
import { ContextMenu } from "electrobun/bun";

win.on("context-menu", (event) => {
  ContextMenu.show([
    { label: "Copy", action: () => { /* copy logic */ } },
    { type: "separator" },
    { label: "Paste", action: () => { /* paste logic */ } },
  ]);
});
```

### System Tray

```ts
import { Tray } from "electrobun/bun";

const tray = new Tray({
  icon: "assets://tray-icon.png",
  tooltip: "My App",
  menu: [
    { label: "Show", action: () => win.show() },
    { label: "Hide", action: () => win.hide() },
    { type: "separator" },
    { label: "Quit", action: () => process.exit(0) },
  ]
});

// Update icon dynamically
tray.setIcon("assets://tray-icon-active.png");
```

### Auto Updater

```ts
import { Updater } from "electrobun/bun";

const updater = new Updater({
  url: "https://updates.myapp.com/latest.json",
  autoCheck: true,
  interval: 60 * 60 * 1000, // Check every hour
});

updater.on("update-available", async (info) => {
  console.log("Update available:", info.version);
  // Show dialog, then:
  updater.downloadAndInstall();
});

updater.on("update-downloaded", () => {
  console.log("Update ready, restart to apply");
});

updater.on("error", (err) => {
  console.error("Updater error:", err);
});
```

### Paths & Assets

```ts
import { paths } from "electrobun/bun";

// OS directories
paths.appData      // App data directory
paths.userData     // User-specific data
paths.resources    // Bundled resources
paths.home         // User home directory
paths.temp         // Temporary directory

// Reference bundled assets:
// views://viewname/file.html  → views folder
// assets://file.png           → assets folder
```

**Example: Persistent State**
```ts
import { join } from "path";

const stateFile = join(paths.userData, "state.json");

// Read
const state = JSON.parse(await Bun.file(stateFile).text() || "{}");

// Write
await Bun.write(stateFile, JSON.stringify(state));
```

### Window Events

```ts
win.on("close", () => {
  console.log("Window closing");
});

win.on("resize", ({ width, height }) => {
  console.log("Window resized:", width, height);
});

win.on("move", ({ x, y }) => {
  console.log("Window moved:", x, y);
});

win.on("focus", () => console.log("Window focused"));
win.on("blur", () => console.log("Window blurred"));
```

### App Lifecycle Events

```ts
import { app } from "electrobun/bun";

app.on("ready", () => {
  console.log("App ready, create windows");
});

app.on("before-quit", () => {
  console.log("App about to quit, cleanup");
});

app.on("window-all-closed", () => {
  if (process.platform !== "darwin") {
    app.quit();
  }
});
```

## Build Configuration

**electrobun.config.ts:**
```ts
import { defineConfig } from "electrobun";

export default defineConfig({
  app: {
    name: "My App",
    version: "1.0.0",
    identifier: "com.example.myapp",
  },
  build: {
    main: "src/bun/main.ts",
    views: {
      mainview: "src/views/mainview/index.ts",
      settings: "src/views/settings/index.ts",
    },
  },
  icons: {
    mac: "assets/icon.icns",
    win: "assets/icon.ico",
    linux: "assets/icon.png",
  },
  updates: {
    provider: "generic",
    url: "https://updates.myapp.com",
  },
});
```

## Common Patterns

### Multiple Windows

```ts
const windows = new Map<string, BrowserWindow>();

function createWindow(id: string, url: string) {
  const win = new BrowserWindow({
    url,
    width: 800,
    height: 600,
  });
  
  windows.set(id, win);
  
  win.on("close", () => {
    windows.delete(id);
  });
  
  return win;
}
```

### Opening External Links

```ts
import { shell } from "electrobun/bun";

// In main process
shell.openExternal("https://example.com");

// In webview, intercept link clicks
document.addEventListener("click", (e) => {
  const link = (e.target as HTMLElement).closest("a");
  if (link && link.href.startsWith("http")) {
    e.preventDefault();
    electroview.rpc.openExternal(link.href);
  }
});
```

### Draggable Title Bar

```html
<!-- In webview HTML -->
<div style="-webkit-app-region: drag; height: 40px; background: #333;">
  <h1 style="-webkit-app-region: no-drag;">My App</h1>
  <button style="-webkit-app-region: no-drag;">Click Me</button>
</div>
```

### File Dialogs

```ts
import { dialog } from "electrobun/bun";

// Open file
const result = await dialog.showOpenDialog({
  title: "Select File",
  filters: [
    { name: "Images", extensions: ["png", "jpg", "jpeg"] },
    { name: "All Files", extensions: ["*"] }
  ],
  properties: ["openFile", "multiSelections"]
});

if (!result.canceled) {
  console.log("Selected files:", result.filePaths);
}

// Save file
const saveResult = await dialog.showSaveDialog({
  title: "Save File",
  defaultPath: "untitled.txt",
  filters: [
    { name: "Text Files", extensions: ["txt"] },
  ]
});
```

## Platform Notes

### macOS
- Uses WKWebView
- Requires code signing for distribution
- Notarization required for Gatekeeper
- Install Xcode Command Line Tools for development

### Windows
- Uses WebView2 (Edge)
- Requires Visual Studio Build Tools for development
- Code signing recommended for SmartScreen

### Linux
- Uses WebKit2GTK
- Install development packages:
  ```bash
  sudo apt install libgtk-3-dev libwebkit2gtk-4.1-dev
  ```

## Next Steps

- **Advanced window management**: See `electrobun-window-management` skill for multi-window apps and BrowserView
- **RPC patterns**: See `electrobun-rpc-patterns` skill for type safety and performance
- **Native UI**: See `electrobun-native-ui` skill for menus, trays, and dialogs
- **Distribution**: See `electrobun-distribution` skill for packaging and updates
- **Debugging**: See `electrobun-debugging` skill for troubleshooting

## Resources

- **Documentation**: https://blackboard.sh/electrobun/
- **GitHub**: https://github.com/blackboardsh/electrobun
- **Discord**: https://discord.gg/ueKE4tjaCE
- **Examples**: https://github.com/blackboardsh/electrobun/tree/main/templates
