---
name: electrobun-window-management
description: Advanced window and view management patterns for Electrobun desktop applications. This skill covers multi-window architectures, BrowserView for embedded webviews, window lifecycle management, window orchestration, tab systems, and complex window hierarchies. Use this skill when building applications with multiple windows, implementing browser-like tab interfaces, managing parent-child window relationships, creating floating panels or toolbars, implementing picture-in-picture modes, managing window state persistence across sessions, or building applications that require sophisticated window coordination. Triggers include "multiple windows", "tab system", "BrowserView", "window orchestration", "floating window", "child window", "window state", "window manager", "multi-window app", or discussions about complex window management in Electrobun desktop applications.
license: MIT
metadata:
  author: Blackboard
  version: "1.0.0"
---

# Electrobun Window Management

Advanced patterns for managing windows and views in Electrobun applications.

## Multi-Window Applications

### Basic Window Manager

```ts
import { BrowserWindow } from "electrobun/bun";

class WindowManager {
  private windows = new Map<string, BrowserWindow>();
  
  createWindow(id: string, options: any) {
    const win = new BrowserWindow(options);
    this.windows.set(id, win);
    
    win.on("close", () => {
      this.windows.delete(id);
    });
    
    return win;
  }
  
  getWindow(id: string) {
    return this.windows.get(id);
  }
  
  getAllWindows() {
    return Array.from(this.windows.values());
  }
  
  closeWindow(id: string) {
    const win = this.windows.get(id);
    if (win) {
      win.close();
    }
  }
  
  closeAllWindows() {
    this.windows.forEach(win => win.close());
    this.windows.clear();
  }
}

const windowManager = new WindowManager();
```

### Window Factory Pattern

```ts
type WindowType = "main" | "settings" | "editor" | "preview";

interface WindowConfig {
  type: WindowType;
  url: string;
  width: number;
  height: number;
  frame?: boolean;
  parent?: BrowserWindow;
}

class WindowFactory {
  private configs: Record<WindowType, Partial<WindowConfig>> = {
    main: {
      url: "views://main/index.html",
      width: 1200,
      height: 800,
      frame: true,
    },
    settings: {
      url: "views://settings/index.html",
      width: 600,
      height: 500,
      frame: true,
    },
    editor: {
      url: "views://editor/index.html",
      width: 1000,
      height: 700,
    },
    preview: {
      url: "views://preview/index.html",
      width: 800,
      height: 600,
      frame: false,
    }
  };
  
  create(type: WindowType, overrides?: Partial<WindowConfig>) {
    const config = { ...this.configs[type], ...overrides };
    return new BrowserWindow(config);
  }
}

const factory = new WindowFactory();
const mainWindow = factory.create("main");
const settingsWindow = factory.create("settings", { width: 700 });
```

## BrowserView

BrowserView allows embedding webviews within a window without creating a separate window.

### Basic BrowserView

```ts
import { BrowserWindow, BrowserView } from "electrobun/bun";

const win = new BrowserWindow({
  title: "Browser App",
  width: 1200,
  height: 800,
});

const view = new BrowserView({
  bounds: { x: 0, y: 60, width: 1200, height: 740 }
});

win.addBrowserView(view);
view.loadURL("https://example.com");

// Update bounds on window resize
win.on("resize", ({ width, height }) => {
  view.setBounds({ x: 0, y: 60, width, height: height - 60 });
});
```

### Tab System with BrowserView

```ts
class TabManager {
  private tabs: Map<string, BrowserView> = new Map();
  private activeTab: string | null = null;
  private window: BrowserWindow;
  
  constructor(window: BrowserWindow) {
    this.window = window;
  }
  
  createTab(id: string, url: string) {
    const view = new BrowserView({
      bounds: this.getViewBounds()
    });
    
    view.loadURL(url);
    this.tabs.set(id, view);
    
    if (!this.activeTab) {
      this.activateTab(id);
    }
    
    return view;
  }
  
  activateTab(id: string) {
    const view = this.tabs.get(id);
    if (!view) return;
    
    // Hide current tab
    if (this.activeTab) {
      const currentView = this.tabs.get(this.activeTab);
      if (currentView) {
        this.window.removeBrowserView(currentView);
      }
    }
    
    // Show new tab
    this.window.addBrowserView(view);
    this.activeTab = id;
  }
  
  closeTab(id: string) {
    const view = this.tabs.get(id);
    if (!view) return;
    
    if (this.activeTab === id) {
      this.window.removeBrowserView(view);
      this.activeTab = null;
      
      // Activate another tab
      const otherTab = Array.from(this.tabs.keys()).find(k => k !== id);
      if (otherTab) {
        this.activateTab(otherTab);
      }
    }
    
    this.tabs.delete(id);
  }
  
  private getViewBounds() {
    const { width, height } = this.window.getBounds();
    return { x: 0, y: 60, width, height: height - 60 };
  }
  
  updateBounds() {
    const bounds = this.getViewBounds();
    this.tabs.forEach(view => {
      view.setBounds(bounds);
    });
  }
}

// Usage
const tabManager = new TabManager(mainWindow);

tabManager.createTab("tab1", "https://example.com");
tabManager.createTab("tab2", "https://github.com");
tabManager.activateTab("tab2");

mainWindow.on("resize", () => {
  tabManager.updateBounds();
});
```

## Window Lifecycle Management

### Window State Persistence

```ts
import { paths } from "electrobun/bun";
import { join } from "path";

interface WindowState {
  x: number;
  y: number;
  width: number;
  height: number;
  maximized: boolean;
}

class WindowStateManager {
  private stateFile: string;
  
  constructor(windowId: string) {
    this.stateFile = join(paths.userData, `window-state-${windowId}.json`);
  }
  
  async save(state: WindowState) {
    await Bun.write(this.stateFile, JSON.stringify(state, null, 2));
  }
  
  async load(): Promise<WindowState | null> {
    try {
      const content = await Bun.file(this.stateFile).text();
      return JSON.parse(content);
    } catch {
      return null;
    }
  }
  
  async restore(window: BrowserWindow) {
    const state = await this.load();
    if (!state) return false;
    
    window.move({ x: state.x, y: state.y });
    window.resize({ width: state.width, height: state.height });
    
    if (state.maximized) {
      window.maximize();
    }
    
    return true;
  }
  
  startTracking(window: BrowserWindow) {
    let saveTimeout: Timer;
    
    const saveState = () => {
      clearTimeout(saveTimeout);
      saveTimeout = setTimeout(async () => {
        const bounds = window.getBounds();
        await this.save({
          x: bounds.x,
          y: bounds.y,
          width: bounds.width,
          height: bounds.height,
          maximized: window.isMaximized(),
        });
      }, 500);
    };
    
    window.on("move", saveState);
    window.on("resize", saveState);
  }
}

// Usage
const stateManager = new WindowStateManager("main");
const win = new BrowserWindow({ width: 1200, height: 800 });

await stateManager.restore(win);
stateManager.startTracking(win);
```

### Window Groups & Parent-Child

```ts
class WindowGroup {
  private parent: BrowserWindow;
  private children: BrowserWindow[] = [];
  
  constructor(parent: BrowserWindow) {
    this.parent = parent;
    
    // Close children when parent closes
    parent.on("close", () => {
      this.closeAllChildren();
    });
  }
  
  addChild(options: any) {
    const child = new BrowserWindow({
      ...options,
      parent: this.parent,
    });
    
    this.children.push(child);
    
    child.on("close", () => {
      const index = this.children.indexOf(child);
      if (index > -1) {
        this.children.splice(index, 1);
      }
    });
    
    return child;
  }
  
  closeAllChildren() {
    this.children.forEach(child => child.close());
    this.children = [];
  }
  
  showAll() {
    this.parent.show();
    this.children.forEach(child => child.show());
  }
  
  hideAll() {
    this.parent.hide();
    this.children.forEach(child => child.hide());
  }
}

// Usage
const mainWindow = new BrowserWindow({ width: 1200, height: 800 });
const group = new WindowGroup(mainWindow);

const palette = group.addChild({
  url: "views://palette/index.html",
  width: 250,
  height: 600,
  frame: false,
});

const inspector = group.addChild({
  url: "views://inspector/index.html",
  width: 300,
  height: 400,
});
```

## Window Orchestration

### Broadcasting to All Windows

```ts
class WindowBroadcaster {
  private windows: Set<BrowserWindow> = new Set();
  
  register(window: BrowserWindow) {
    this.windows.add(window);
    
    window.on("close", () => {
      this.windows.delete(window);
    });
  }
  
  async broadcast(method: string, ...args: any[]) {
    const promises = Array.from(this.windows).map(win =>
      win.rpc[method](...args).catch(err => {
        console.error(`Broadcast to window failed:`, err);
      })
    );
    
    await Promise.allSettled(promises);
  }
}

const broadcaster = new WindowBroadcaster();

// Register windows
broadcaster.register(mainWindow);
broadcaster.register(settingsWindow);

// Broadcast to all
await broadcaster.broadcast("updateTheme", { theme: "dark" });
```

### Window Communication Hub

```ts
class WindowHub {
  private windows = new Map<string, BrowserWindow>();
  
  register(id: string, window: BrowserWindow) {
    this.windows.set(id, window);
    
    // Setup RPC handler for messaging
    window.defineRpc({
      handlers: {
        sendToWindow: async (targetId: string, method: string, ...args: any[]) => {
          return this.send(targetId, method, ...args);
        }
      }
    });
  }
  
  async send(targetId: string, method: string, ...args: any[]) {
    const target = this.windows.get(targetId);
    if (!target) {
      throw new Error(`Window ${targetId} not found`);
    }
    
    return await target.rpc[method](...args);
  }
  
  async broadcast(method: string, ...args: any[]) {
    const results = new Map();
    
    for (const [id, window] of this.windows) {
      try {
        const result = await window.rpc[method](...args);
        results.set(id, result);
      } catch (err) {
        results.set(id, { error: err.message });
      }
    }
    
    return results;
  }
}

const hub = new WindowHub();
hub.register("main", mainWindow);
hub.register("editor", editorWindow);

// Send from main to editor
await hub.send("editor", "updateContent", { text: "Hello" });

// Broadcast to all
await hub.broadcast("refreshData");
```

## Floating Windows & Overlays

### Always-on-Top Window

```ts
const floatingWindow = new BrowserWindow({
  url: "views://floating/index.html",
  width: 300,
  height: 200,
  frame: false,
  alwaysOnTop: true,
  skipTaskbar: true,
});

// Toggle always-on-top
floatingWindow.setAlwaysOnTop(!floatingWindow.isAlwaysOnTop());
```

### Picture-in-Picture Mode

```ts
class PictureInPicture {
  private pipWindow: BrowserWindow | null = null;
  private sourceWindow: BrowserWindow;
  
  constructor(sourceWindow: BrowserWindow) {
    this.sourceWindow = sourceWindow;
  }
  
  enter(url: string) {
    if (this.pipWindow) return;
    
    this.pipWindow = new BrowserWindow({
      url,
      width: 400,
      height: 300,
      frame: false,
      alwaysOnTop: true,
      resizable: true,
    });
    
    this.pipWindow.on("close", () => {
      this.pipWindow = null;
    });
  }
  
  exit() {
    if (this.pipWindow) {
      this.pipWindow.close();
      this.pipWindow = null;
    }
  }
  
  toggle(url: string) {
    if (this.pipWindow) {
      this.exit();
    } else {
      this.enter(url);
    }
  }
}

const pip = new PictureInPicture(mainWindow);
pip.enter("views://video-player/index.html");
```

## Advanced Patterns

### Modal Dialogs

```ts
function showModal(parent: BrowserWindow, options: any) {
  const modal = new BrowserWindow({
    ...options,
    parent,
    modal: true,
    frame: false,
  });
  
  // Disable parent interaction
  parent.setEnabled(false);
  
  modal.on("close", () => {
    parent.setEnabled(true);
    parent.focus();
  });
  
  return modal;
}

// Usage
const confirmDialog = showModal(mainWindow, {
  url: "views://confirm/index.html",
  width: 400,
  height: 200,
});
```

### Window Positioning

```ts
function centerWindow(window: BrowserWindow) {
  const { screen } = require("electrobun/bun");
  const display = screen.getPrimaryDisplay();
  const { width: screenWidth, height: screenHeight } = display.workArea;
  const { width, height } = window.getBounds();
  
  const x = Math.floor((screenWidth - width) / 2);
  const y = Math.floor((screenHeight - height) / 2);
  
  window.move({ x, y });
}

function cascadeWindows(windows: BrowserWindow[]) {
  const offset = 30;
  windows.forEach((win, index) => {
    win.move({ 
      x: 100 + (index * offset), 
      y: 100 + (index * offset) 
    });
  });
}
```

## Resources

For more on Electrobun:
- **Core skill**: `electrobun` - Basic window creation and APIs
- **RPC patterns**: `electrobun-rpc-patterns` - Window-to-window RPC
- **Native UI**: `electrobun-native-ui` - Menus and tray integration
