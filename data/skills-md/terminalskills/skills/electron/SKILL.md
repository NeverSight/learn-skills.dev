---
name: electron
description: >-
  Assists with building cross-platform desktop applications using Electron. Use when
  architecting main/renderer process communication, configuring secure contexts, implementing
  auto-updates, or packaging apps for Windows, macOS, and Linux. Trigger words: electron,
  desktop app, browserwindow, ipc, auto-update, electron-builder.
license: Apache-2.0
compatibility: "Node.js 22.12+ to install the current electron package (Electron 44 bundles its own Node and Chromium)"
metadata:
  author: terminal-skills
  version: "1.1.0"
  repository: https://github.com/electron/electron
  category: development
  tags: ["electron", "desktop", "cross-platform", "ipc", "packaging"]
---

# Electron

## Overview

Electron is a framework for building cross-platform desktop applications using web technologies. It combines a Node.js main process for system access and window management with Chromium renderer processes for the UI, communicating via IPC with context isolation and preload scripts for security.

## Instructions

- When starting a project, install `electron` as a dev dependency (`npm install --save-dev electron`), or scaffold with Electron Forge (`npm init electron-app@latest my-app`). Point `main` in package.json at the main-process file and run with `electron .`. Current stable line: Electron 44 (checked 44.5.1).
- When setting up the architecture, create a main process for window management and system APIs, renderer processes for UI, and a preload script that exposes a small, named API with `contextBridge.exposeInMainWorld()`. Never expose `ipcRenderer` itself.
- When implementing IPC, use `ipcMain.handle()` / `ipcRenderer.invoke()` for request-response, and `webContents.send()` for main-to-renderer push. Validate arguments and the sender (`event.senderFrame.origin`, not the URL) inside every handler.
- When accessing native APIs, use dialogs, file system, clipboard, notifications and `shell` in the main process and reach them from the renderer only through the preload bridge.
- When configuring security, rely on the defaults (`contextIsolation: true` since Electron 12, `nodeIntegration: false`, `sandbox: true` for renderers) and do not turn them off. Add a Content Security Policy, deny unexpected navigation with `will-navigate` and `webContents.setWindowOpenHandler()`, never pass untrusted URLs to `shell.openExternal`, and flip unused fuses (`runAsNode`, `nodeCliInspect`) with `@electron/fuses`.
- When packaging, use Electron Forge (makers: Squirrel.Windows or WiX/MSI, DMG/ZIP, deb/rpm/AppImage via community makers) or `electron-builder`; sign Windows builds and sign plus notarize macOS builds.
- When implementing auto-updates, use the built-in `autoUpdater` (Squirrel) with a static storage URL or update.electronjs.org for public GitHub repos, or `electron-updater` from electron-builder, which supports GitHub Releases or a generic server, differential downloads, and a `stagingPercentage` field in the release metadata for staged rollouts. `autoUpdater` does not work on Linux; updates there come through the package manager or AppImage updaters.
- When the renderer crashes, handle `webContents.on("render-process-gone", ...)` and `app.on("child-process-gone", ...)`, and reload or show an error window.

### Minimal secure skeleton

```javascript
// main.js
const { app, BrowserWindow, ipcMain, dialog } = require("electron");
const path = require("node:path");

function createWindow() {
  const win = new BrowserWindow({
    width: 1100, height: 720,
    webPreferences: { preload: path.join(__dirname, "preload.js") }, // defaults stay secure
  });
  win.webContents.setWindowOpenHandler(() => ({ action: "deny" }));
  win.loadFile("index.html");
}

ipcMain.handle("dialog:openFile", async (event) => {
  if (event.senderFrame?.origin !== "file://") return null; // only our own page
  const { canceled, filePaths } = await dialog.showOpenDialog({ properties: ["openFile"] });
  return canceled ? null : filePaths[0];
});

app.whenReady().then(createWindow);
app.on("window-all-closed", () => { if (process.platform !== "darwin") app.quit(); });
```

```json
{
  "name": "file-manager",
  "version": "1.0.0",
  "main": "main.js",
  "scripts": { "start": "electron ." },
  "devDependencies": { "electron": "^44.5.1" }
}
```

```javascript
// preload.js
const { contextBridge, ipcRenderer } = require("electron");
contextBridge.exposeInMainWorld("files", { openFile: () => ipcRenderer.invoke("dialog:openFile") });
```

## Examples

### Example 1: Build a file manager with native dialogs

**User request:** "Create an Electron app that browses and manages files with native dialogs"

**Actions:**
1. Set up main process with `BrowserWindow` and preload script exposing file system commands
2. Implement IPC handlers for `dialog.showOpenDialog()`, `dialog.showSaveDialog()`, and file operations
3. Build a React-based renderer UI for browsing directories and previewing files
4. Add context menus and keyboard shortcuts for file operations
5. Run `npx electron .` and confirm that `window.files.openFile()` in DevTools returns a path while `require` is undefined in the renderer

**Output:** A cross-platform file manager with native OS dialogs and secure IPC-based file access.

### Example 2: Add auto-updates with staged rollout

**User request:** "Set up auto-updates for my Electron app using GitHub Releases"

**Actions:**
1. Configure `electron-builder` with `publish` settings pointing to GitHub Releases
2. Add `electron-updater` in the main process with update check on startup
3. Implement update UI in the renderer showing download progress and restart prompt
4. Set `stagingPercentage` (for example 10) in the published `latest.yml` to update a share of users first, and raise it as the release proves stable

**Output:** An Electron app that automatically checks for updates, downloads them in the background, and prompts the user to restart.

## Guidelines

- Always use context isolation and preload scripts; never enable `nodeIntegration` in the renderer or disable `sandbox`.
- Validate all IPC message data and the sender frame in the main process since the renderer is untrusted like a browser.
- Use `ipcMain.handle()` / `ipcRenderer.invoke()` for async operations over the older `send`/`on` pattern.
- Minimize main process work to keep it responsive for window management and IPC routing.
- Set CSP headers on all windows: `default-src 'self'; script-src 'self'`.
- Test on all target platforms since Windows, macOS, and Linux behave differently for menus, shortcuts, and file paths.
- Handle the `render-process-gone` event on `webContents` and monitor memory with `process.getProcessMemoryInfo()` or `app.getAppMetrics()`.
- Keep Electron current: each major ships a new Chromium, and old majors stop receiving security fixes.
- Never load remote content in a window that has a privileged preload; prefer custom protocols over `file://` for app content.
