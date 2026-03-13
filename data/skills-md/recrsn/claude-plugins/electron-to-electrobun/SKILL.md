---
name: electron-to-electrobun
description: Port an Electron app to Electrobun. Runs a compatibility audit first, then migrates IPC, windows, preload, menus, dialogs, and build config to Electrobun equivalents.
allowed-tools: Bash, Read, Write, Edit, Glob, Grep, Task, WebFetch, WebSearch
---

# Electron → Electrobun Migration

Two phases: compatibility check, then migration. For mechanical transformations (import rewrites, IPC channel renames, API mappings), prefer JS/TS codemods using `jscodeshift` or `ts-morph` over manual edits.

> Many Electrobun APIs are identical to Electron: `BrowserWindow` options (`title`, `titleBarStyle`, `transparent`), methods (`setTitle`, `close`, `focus`, `minimize`/`isMinimized`, `maximize`/`unmaximize`/`isMaximized`, `setFullScreen`/`isFullScreen`, `setAlwaysOnTop`/`isAlwaysOnTop`, `setPosition`, `setSize`), events (`resize`, `focus`), menu props (`role`, `label`, `type`, `enabled`, `checked`, `submenu`), `GlobalShortcut`, `Screen`, `Session`/`Cookies`. Tables below only list differences. Caveat: `getPosition()` → `{x,y}` not `[x,y]`; `getSize()` → `{width,height}` not `[w,h]`.

## Quick reference

| Electron | Electrobun |
|---|---|
| Node.js (V8) | Bun (JavaScriptCore) |
| Bundled Chromium | System WebView (WebKit/WebView2/WebKitGTK) or CEF |
| `ipcMain.handle`/`ipcRenderer.invoke` | `BrowserView.defineRPC<S>()`/`Electroview.defineRPC<S>()` |
| `webContents.send`/`ipcRenderer.on` | RPC messages (fire-and-forget) |
| preload + contextBridge | Typed RPC (preload supported, not for IPC bridging) |
| `dialog.showOpenDialog()` | `Utils.openFileDialog()` |
| `dialog.showMessageBox()` | `Utils.showMessageBox()` |
| `Menu.buildFromTemplate()` | `ApplicationMenu.setApplicationMenu([...])` |
| `Menu.popup()` | `ContextMenu.showContextMenu([...])` |
| `clipboard.*` | `Utils.clipboard*()` |
| `new Notification()` | `Utils.showNotification({title,body,subtitle?,silent?})` |
| `app.getPath(name)` | `Utils.paths.*` |
| `shell.openExternal/openPath/showItemInFolder` | `Utils.openExternal/openPath/showItemInFolder` |
| `shell.trashItem` | `Utils.moveToTrash` |
| `safeStorage.encrypt/decrypt` | `Bun.secrets.get/set/delete` (OS keychain, key-value) |
| `app.quit()` | `Utils.quit()` |
| electron-builder/forge | `electrobun build` (built-in, BSDIFF patches) |
| `file://` / custom protocol | `views://viewname/path` |
| CSS `-webkit-app-region: drag` | CSS class `electrobun-webkit-app-region-drag` |

## RPC pattern

Key difference: Electron IPC is unidirectional — `ipcMain.handle` only serves renderer→main, `webContents.send` only pushes main→renderer. Electrobun RPC is bidirectional in a single schema — both sides can define requests (async call/response) and messages (fire-and-forget) in one type. This eliminates the need for separate IPC channel registrations, event forwarders, and bridge layers. A single `defineRPC<Schema>()` call on each side replaces `ipcMain.handle` + `webContents.send` + `contextBridge.exposeInMainWorld` + `ipcRenderer.invoke` + `ipcRenderer.on`.

Shared schema type:
```typescript
import type { RPCSchema } from "electrobun/bun";
type MySchema = {
  bun: RPCSchema<{
    requests: { myMethod: { params: { id: string }; response: Result } };
    messages: Record<string, never>;
  }>;
  webview: RPCSchema<{
    requests: Record<string, never>;
    messages: { myEvent: { data: string } };
  }>;
};
```
`bun.requests` = renderer→main (returns response). `bun.messages` = renderer→main (fire-and-forget). `webview.requests`/`messages` = main→renderer.

Bun side:
```typescript
const rpc = BrowserView.defineRPC<MySchema>({ handlers: { requests: {...}, messages: {...} } });
const win = new BrowserWindow({ url: "views://main/index.html", rpc });
win.webview.rpc.myEvent({ data: "hello" });
```

Webview side:
```typescript
const rpc = Electroview.defineRPC<MySchema>({ handlers: { requests: {...}, messages: {...} } });
const view = new Electroview({ rpc });
await view.rpc.request.myMethod({ id: "123" });
```

---

## Phase 1: Compatibility Check

### 1.1 Scan Electron API usage

Main: `import {...} from 'electron'` (list all), `BrowserWindow` (options/methods/events/`webContents`), `ipcMain.handle`/`.on` (channels), `webContents.send` (channels), `dialog.*`, `Menu.*`, `Tray`, `clipboard.*`, `globalShortcut.*`, `screen.*`, `session`/`cookies`, `shell.*`, `Notification`, `app.getPath()`, `app.on('ready')`/`whenReady()`/`'window-all-closed'`/`'before-quit'`, `safeStorage`, `nativeTheme`, `protocol.registerFileProtocol`, `autoUpdater`/`electron-updater`

Preload: `contextBridge.exposeInMainWorld` (remove), `ipcRenderer.*` (remove). Categorize each file: IPC bridge (remove) vs non-IPC (keep).

Renderer: `window.electron`/`window.api`/custom bridge names, `remote` module

Build: electron-builder/forge config, Vite/webpack electron plugins

Native modules: `*.node`, `node-gyp`, `prebuild`, `ffi-napi`, `better-sqlite3`, `keytar`, `node-pty`

### 1.2 Unsupported patterns

`remote` → RPC requests. `webRequest` → limited. No equivalent: `desktopCapturer`, `powerMonitor`, `powerSaveBlocker`, `TouchBar`, `crashReporter`, `vibrancy`/`visualEffectState` (NSVisualEffectView), `trafficLightPosition`. `systemPreferences` → limited. `nodeIntegration: true` → N/A. `dialog.showSaveDialog` → none yet. `@electron/rebuild` → Bun native modules.

### 1.3 Report template

```
## Compatibility Report
### Direct equivalents
- [ ] BrowserWindow (N instances)
- [ ] IPC: N handles, M sends → RPC
- [ ] Dialogs, Menu, Clipboard, Shortcuts, Screen, Session
### Requires refactoring
- [ ] Preload IPC bridge (N files) → strip
- [ ] Preload non-IPC (N files) → keep
### No equivalent
- [ ] ...
### Effort: N schemas, N preloads, N handlers, N events
```

STOP. Present report. Enter plan mode and draft a migration plan based on the report. Get user approval before proceeding.

---

## Phase 2: Migration

Type-check after each step.

### 2.1 Install

```bash
bun add electrobun
bun remove electron electron-builder @electron-forge/* electron-devtools-installer @electron/rebuild
```
Remove electron vite/webpack plugins.

### 2.2 `electrobun.config.ts`

```typescript
import type { ElectrobunConfig } from "electrobun";
export default {
  app: { name: "AppName", identifier: "com.x.app", version: "1.0.0" },
  build: {
    bun: { entrypoint: "src/main/index.ts" },
    views: { main: { entrypoint: "src/renderer/main.tsx" } },
    copy: { "src/renderer/index.html": "views/main/index.html" },
  },
} satisfies ElectrobunConfig;
```
With Vite: keep for dev, use `copy` for prod output.

### 2.3 RPC schemas

Per window type, create schema in `src/common/rpc/`.

`ipcMain.handle(ch)` → `bun.requests.ch`. `webContents.send(ch)` → `webview.messages.ch`. `ipcRenderer.invoke(ch)` → `rpc.request.ch()`. `ipcRenderer.on(ch)` → message handler in `defineRPC` or `rpc.addMessageListener`.

Schema keys must be valid JS identifiers — rename `:`, `.`, `/` channels.

### 2.4 Preload

Strip: `contextBridge.exposeInMainWorld()`, all `ipcRenderer`, electron imports for these.
Keep: polyfills, error handlers, globals, CSS injection, DOM prep.
Delete file if only IPC bridge code. Wire kept preloads: `preload: "views://main/preload.js"`.
Remove `global.d.ts`/`window.api` type declarations.

### 2.5 Main process

BrowserWindow constructor:

| Electron | Electrobun |
|---|---|
| `width`,`height`,`x`,`y` | `frame: {width,height,x,y}` |
| `webPreferences.preload` | `preload` (top-level, accepts `views://`, remote URL, inline JS) |
| `webPreferences.nodeIntegration` | N/A (never available) |
| `webPreferences.contextIsolation` | N/A (always isolated) |
| `webPreferences.partition` | `partition` (`persist:` prefix for persistence) |
| `frame: false` | `styleMask: {Borderless:true, Titled:false}` |
| `vibrancy` / `visualEffectState` | No equivalent (use CSS `backdrop-filter` + `transparent: true`) |
| `trafficLightPosition` | No equivalent (system default only) |
| N/A | `sandbox: true` (disables RPC), `html: "..."`, `rpc` |

`styleMask` (macOS): `Borderless`, `Titled`, `Closable`, `Miniaturizable`, `Resizable`, `UnifiedTitleAndToolbar`, `FullScreen`, `FullSizeContentView`, `UtilityWindow`, `DocModalWindow`, `NonactivatingPanel`, `HUDWindow`. `titleBarStyle` auto-sets `styleMask`.

BrowserWindow methods (differences only):

| Electron | Electrobun |
|---|---|
| `restore()` | `unminimize()` |
| `setBounds(rect)` | `setFrame(x,y,w,h)` |
| `getBounds()` | `getFrame()` → `{x,y,width,height}` |
| `loadURL(url)` | `webview.loadURL(url)` |
| `webContents` | `webview` (all `webContents.*` moves here) |
| `webContents.openDevTools({mode})` | `webview.openDevTools()` (no args) |
| N/A | `webview.toggleDevTools()` |

BrowserWindow events (differences only):

| Electron | Electrobun | Data |
|---|---|---|
| `'closed'` | `'close'` | `{id}` |
| `'move'`/`'moved'` | `'move'` | `{id,x,y}` |

Events also on `Electrobun.events.on(name, ...)`.

App lifecycle:
```typescript
// Electron:
app.whenReady().then(createWindow);
app.on('window-all-closed', () => { if (process.platform !== 'darwin') app.quit(); });
// Electrobun — no 'ready', starts immediately:
createWindow();
// exitOnLastWindowClosed in config. before-quit:
Electrobun.events.on('before-quit', (e) => { e.response = { allow: false }; });
```

`openFileDialog` options:

| Electron | Electrobun |
|---|---|
| `properties: ['openFile']` | `canChooseFiles: true` |
| `properties: ['openDirectory']` | `canChooseDirectory: true` |
| `properties: ['multiSelections']` | `allowsMultipleSelection: true` |
| `defaultPath` | `startingFolder` |
| `filters: [{extensions:[...]}]` | `allowedFileTypes: "png,jpg"` (comma-sep, `"*"` for all) |

Returns `string[]` directly (not `{filePaths, canceled}`). `showMessageBox` options/return identical.

Menus:
```typescript
// Electron: Menu.setApplicationMenu(Menu.buildFromTemplate(template));
// Electrobun — no buildFromTemplate:
ApplicationMenu.setApplicationMenu([
  { submenu: [{ label: 'Quit', role: 'quit' }] },
  { label: 'Edit', submenu: [{ role: 'undo' }, { role: 'redo' }, { type: 'separator' }, { role: 'cut' }, { role: 'copy' }, { role: 'paste' }, { role: 'selectAll' }] },
]);
```

Menu item differences:

| Electron | Electrobun |
|---|---|
| `click: () => {}` | `action: "string"` + `Electrobun.events.on('application-menu-clicked', e => e.data.action)` |
| `accelerator: "CmdOrCtrl+S"` | `accelerator: "s"` (just key, modifier auto-applied) |
| `visible: false` | `hidden: true` |
| `toolTip` | `tooltip` |

Roles: `quit`, `hide`, `hideOthers`, `undo`, `redo`, `cut`, `copy`, `paste`, `pasteAndMatchStyle`, `delete`, `selectAll`, `minimize`, `close`, `toggleFullScreen`, `zoom`, `bringAllToFront`, `cycleThroughWindows`. Separators: `{type:"separator"}` or `{type:"divider"}`. Linux: menus unsupported.

Context menus: `ContextMenu.showContextMenu([...])` + `Electrobun.events.on('context-menu-clicked', ...)`.

Shell: `shell.*` → `Utils.*`. `trashItem` → `moveToTrash` (no restore metadata on macOS). `openExternal`/`openPath` return `boolean`.

Clipboard: `clipboard.*()` → `Utils.clipboard*()`. `readImage()` → `Uint8Array` (PNG) or `null`. `availableFormats()` → `["text","image","files","html"]`.

Paths: `app.getPath(name)` → `Utils.paths.{name}`. All sync. `userData` is app-scoped: `{appData}/{identifier}/{channel}`. Extra: `Utils.paths.config`, `.cache`, `.userCache`, `.userLogs`.

Credentials:
```typescript
// Electron: safeStorage.encryptString(value); safeStorage.decryptString(buffer);
// Electrobun (OS keychain, key-value):
await Bun.secrets.set({ service: "my-app", name: "api-key", value: "secret" });
await Bun.secrets.get({ service: "my-app", name: "api-key" }); // string | null
await Bun.secrets.delete({ service: "my-app", name: "api-key" }); // boolean
```
Not raw encrypt/decrypt — refactor to key-value by service+name.

GlobalShortcut, Screen, Session/Cookies: Import from `"electrobun/bun"`. Same APIs.

### 2.6 Renderer

Replace bridge calls: `window.api.call(ch, args)` → `rpc.request.ch(args)`. `window.api.on(ch, cb)` → `rpc.addMessageListener('ch', cb)`.

Per-entrypoint `rpc.ts`:
```typescript
import { Electroview } from "electrobun/view";
import type { MySchema } from "../common/rpc/my-schema.js";
export const rpc = Electroview.defineRPC<MySchema>({ handlers: { requests: {}, messages: {} } });
const view = new Electroview({ rpc });
```

CSS: `-webkit-app-region: drag/no-drag` → classes `electrobun-webkit-app-region-drag`/`-no-drag`.

Remove `window.api`/`window.electron` type declarations, `global.d.ts`/`preload.d.ts`.

### 2.7 Build

With Vite: keep for dev, `copy` maps output in `electrobun.config.ts`. Without: `build.views` in config.

### 2.8 Verify

`bun run typecheck` → `electrobun build` → test windows/RPC/events/menus/dialogs → `electrobun build --env=stable`

## Pitfalls

1. Preload ≠ delete — strip only `contextBridge`/`ipcRenderer`; keep polyfills/globals
2. Channel names — RPC keys must be valid JS identifiers, rename `:./` consistently
3. `safeStorage` → `Bun.secrets` — key-value, not encrypt/decrypt
4. `remote` → must become RPC requests
5. Native modules — may need Bun-compatible alternatives
6. Multi-window — each window type needs its own RPC schema
7. Draggable regions — CSS property → CSS class
