---
name: electrobun-native-ui
description: Native UI integration for Electrobun desktop applications including ApplicationMenu, ContextMenu, system Tray, native dialogs, keyboard shortcuts, and platform-specific UI patterns. This skill covers creating application menus with submenus and accelerators, context menus triggered by right-click, system tray icons with menus, file/folder dialogs, message boxes, notification systems, global keyboard shortcuts, menu item roles, dynamic menu updates, platform-specific menu conventions (macOS menu bar, Windows system menu), drag-and-drop integration, and native theming. Use when implementing application menus, adding system tray functionality, creating context menus, showing file pickers, implementing keyboard shortcuts, displaying notifications or dialogs, or building platform-native UI experiences. Triggers include "menu", "tray icon", "context menu", "file dialog", "shortcuts", "accelerator", "native dialog", "system tray", "notification", "menu bar", or "right-click menu".
license: MIT
metadata:
  author: Blackboard
  version: "1.0.0"
---

# Electrobun Native UI

Comprehensive guide to native UI integration in Electrobun applications.

## Application Menu

### Basic Menu Structure

```ts
import { ApplicationMenu } from "electrobun/bun";

ApplicationMenu.setMenu([
  {
    label: "File",
    submenu: [
      {
        label: "New",
        accelerator: "CmdOrCtrl+N",
        action: () => createNewDocument()
      },
      {
        label: "Open...",
        accelerator: "CmdOrCtrl+O",
        action: () => openFile()
      },
      { type: "separator" },
      {
        label: "Save",
        accelerator: "CmdOrCtrl+S",
        action: () => saveFile()
      },
      {
        label: "Save As...",
        accelerator: "CmdOrCtrl+Shift+S",
        action: () => saveFileAs()
      },
      { type: "separator" },
      {
        label: "Quit",
        accelerator: "CmdOrCtrl+Q",
        action: () => app.quit()
      }
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
      { type: "separator" },
      { role: "selectAll" }
    ]
  },
  {
    label: "View",
    submenu: [
      {
        label: "Reload",
        accelerator: "CmdOrCtrl+R",
        action: () => currentWindow.reload()
      },
      {
        label: "Toggle DevTools",
        accelerator: "CmdOrCtrl+Shift+I",
        action: () => currentWindow.toggleDevTools()
      },
      { type: "separator" },
      {
        label: "Zoom In",
        accelerator: "CmdOrCtrl+Plus",
        action: () => adjustZoom(0.1)
      },
      {
        label: "Zoom Out",
        accelerator: "CmdOrCtrl+-",
        action: () => adjustZoom(-0.1)
      },
      {
        label: "Reset Zoom",
        accelerator: "CmdOrCtrl+0",
        action: () => resetZoom()
      }
    ]
  },
  {
    label: "Help",
    submenu: [
      {
        label: "Documentation",
        action: () => shell.openExternal("https://docs.myapp.com")
      },
      { type: "separator" },
      {
        label: "About",
        action: () => showAboutDialog()
      }
    ]
  }
]);
```

### Built-in Roles

```ts
// Standard edit roles
{ role: "undo" }        // Undo last action
{ role: "redo" }        // Redo last action
{ role: "cut" }         // Cut selection
{ role: "copy" }        // Copy selection
{ role: "paste" }       // Paste from clipboard
{ role: "selectAll" }   // Select all content

// Window roles
{ role: "minimize" }    // Minimize window
{ role: "close" }       // Close window
{ role: "quit" }        // Quit application
{ role: "reload" }      // Reload current page
{ role: "forceReload" } // Force reload (clear cache)
{ role: "toggleDevTools" } // Toggle developer tools
{ role: "toggleFullScreen" } // Toggle fullscreen

// Zoom roles
{ role: "zoomIn" }      // Zoom in
{ role: "zoomOut" }     // Zoom out
{ role: "resetZoom" }   // Reset zoom to 100%
```

### Dynamic Menus

```ts
class MenuManager {
  private currentMenu: any[] = [];
  
  updateRecentFiles(files: string[]) {
    const recentMenu = files.map(file => ({
      label: path.basename(file),
      action: () => openFile(file)
    }));
    
    // Find File menu and update Recent submenu
    const fileMenu = this.currentMenu.find(m => m.label === "File");
    const recentIndex = fileMenu.submenu.findIndex(
      (item: any) => item.label === "Recent"
    );
    
    if (recentIndex >= 0) {
      fileMenu.submenu[recentIndex] = {
        label: "Recent",
        submenu: recentMenu.length > 0 ? recentMenu : [
          { label: "No recent files", enabled: false }
        ]
      };
    }
    
    ApplicationMenu.setMenu(this.currentMenu);
  }
  
  setCheckState(menuPath: string[], checked: boolean) {
    // Navigate menu structure and update check state
    let current: any = this.currentMenu;
    
    for (let i = 0; i < menuPath.length - 1; i++) {
      current = current.find((m: any) => m.label === menuPath[i]);
      if (!current) return;
      current = current.submenu;
    }
    
    const item = current.find((m: any) => m.label === menuPath[menuPath.length - 1]);
    if (item) {
      item.checked = checked;
      ApplicationMenu.setMenu(this.currentMenu);
    }
  }
  
  enableMenuItem(menuPath: string[], enabled: boolean) {
    // Similar navigation to setCheckState
    // Set item.enabled = enabled
  }
}

// Usage
const menuManager = new MenuManager();
menuManager.updateRecentFiles(["/path/to/file1.txt", "/path/to/file2.txt"]);
menuManager.setCheckState(["View", "Show Sidebar"], true);
```

### Platform-Specific Menus

```ts
function createMenu() {
  const isMac = process.platform === "darwin";
  
  const menu = [];
  
  // macOS app menu
  if (isMac) {
    menu.push({
      label: app.name,
      submenu: [
        { role: "about" },
        { type: "separator" },
        {
          label: "Preferences...",
          accelerator: "Cmd+,",
          action: () => showPreferences()
        },
        { type: "separator" },
        { role: "services" },
        { type: "separator" },
        { role: "hide" },
        { role: "hideOthers" },
        { role: "unhide" },
        { type: "separator" },
        { role: "quit" }
      ]
    });
  }
  
  // File menu
  menu.push({
    label: "File",
    submenu: [
      { label: "New", accelerator: "CmdOrCtrl+N", action: createNew },
      { label: "Open", accelerator: "CmdOrCtrl+O", action: openFile },
      // On Windows/Linux, add Quit here
      ...(!isMac ? [
        { type: "separator" },
        { label: "Exit", action: () => app.quit() }
      ] : [])
    ]
  });
  
  return menu;
}
```

## Context Menu

### Basic Context Menu

```ts
import { ContextMenu, BrowserWindow } from "electrobun/bun";

const win = new BrowserWindow({ /* ... */ });

win.on("context-menu", (event) => {
  ContextMenu.show([
    {
      label: "Copy",
      accelerator: "CmdOrCtrl+C",
      action: () => {
        // Copy selected text
      }
    },
    {
      label: "Paste",
      accelerator: "CmdOrCtrl+V",
      action: () => {
        // Paste from clipboard
      }
    },
    { type: "separator" },
    {
      label: "Inspect Element",
      action: () => {
        win.inspectElement(event.x, event.y);
      }
    }
  ]);
});
```

### Dynamic Context Menu

```ts
// Webview sends context info
// In webview (index.ts):
document.addEventListener("contextmenu", (e) => {
  e.preventDefault();
  
  const target = e.target as HTMLElement;
  const context = {
    x: e.clientX,
    y: e.clientY,
    hasSelection: window.getSelection()?.toString().length > 0,
    isLink: target.tagName === "A",
    linkUrl: target.tagName === "A" ? (target as HTMLAnchorElement).href : null,
    isImage: target.tagName === "IMG",
    imageUrl: target.tagName === "IMG" ? (target as HTMLImageElement).src : null,
  };
  
  electroview.rpc.showContextMenu(context);
});

// Main process handles it
win.defineRpc({
  handlers: {
    async showContextMenu(context: any) {
      const menu = [];
      
      if (context.hasSelection) {
        menu.push(
          { label: "Copy", action: () => win.rpc.copy() },
          { type: "separator" }
        );
      }
      
      if (context.isLink) {
        menu.push(
          {
            label: "Open Link",
            action: () => shell.openExternal(context.linkUrl)
          },
          {
            label: "Copy Link",
            action: () => clipboard.write(context.linkUrl)
          },
          { type: "separator" }
        );
      }
      
      if (context.isImage) {
        menu.push(
          {
            label: "Save Image...",
            action: async () => {
              const result = await dialog.showSaveDialog({
                defaultPath: "image.png"
              });
              if (!result.canceled) {
                await downloadImage(context.imageUrl, result.filePath);
              }
            }
          },
          {
            label: "Copy Image",
            action: () => copyImage(context.imageUrl)
          },
          { type: "separator" }
        );
      }
      
      menu.push({
        label: "Inspect",
        action: () => win.inspectElement(context.x, context.y)
      });
      
      ContextMenu.show(menu);
    }
  }
});
```

## System Tray

### Basic Tray Icon

```ts
import { Tray } from "electrobun/bun";

const tray = new Tray({
  icon: "assets://tray-icon.png",
  tooltip: "My Application",
  menu: [
    {
      label: "Show Window",
      action: () => mainWindow.show()
    },
    {
      label: "Hide Window",
      action: () => mainWindow.hide()
    },
    { type: "separator" },
    {
      label: "Quit",
      action: () => app.quit()
    }
  ]
});
```

### Dynamic Tray Updates

```ts
class TrayManager {
  private tray: Tray;
  private status: "idle" | "working" | "error" = "idle";
  
  constructor() {
    this.tray = new Tray({
      icon: this.getIconForStatus("idle"),
      tooltip: "My App - Idle"
    });
    this.updateMenu();
  }
  
  setStatus(status: "idle" | "working" | "error") {
    this.status = status;
    this.tray.setIcon(this.getIconForStatus(status));
    this.tray.setTooltip(`My App - ${status}`);
    this.updateMenu();
  }
  
  private getIconForStatus(status: string) {
    return `assets://tray-${status}.png`;
  }
  
  private updateMenu() {
    const menu = [
      {
        label: `Status: ${this.status}`,
        enabled: false
      },
      { type: "separator" },
      {
        label: "Show Window",
        action: () => mainWindow.show()
      }
    ];
    
    if (this.status === "working") {
      menu.push({
        label: "Cancel",
        action: () => cancelWork()
      });
    }
    
    menu.push(
      { type: "separator" },
      {
        label: "Quit",
        action: () => app.quit()
      }
    );
    
    this.tray.setMenu(menu);
  }
  
  showNotification(title: string, message: string) {
    this.tray.showBalloon({
      title,
      content: message,
      icon: "assets://notification-icon.png"
    });
  }
}

const trayManager = new TrayManager();
trayManager.setStatus("working");
trayManager.showNotification("Task Complete", "Your task has finished");
```

## Native Dialogs

### File Dialogs

```ts
import { dialog } from "electrobun/bun";

// Open single file
async function openFile() {
  const result = await dialog.showOpenDialog({
    title: "Open File",
    defaultPath: paths.home,
    filters: [
      { name: "Text Files", extensions: ["txt", "md"] },
      { name: "All Files", extensions: ["*"] }
    ],
    properties: ["openFile"]
  });
  
  if (!result.canceled && result.filePaths.length > 0) {
    const content = await Bun.file(result.filePaths[0]).text();
    return { path: result.filePaths[0], content };
  }
  
  return null;
}

// Open multiple files
async function openMultipleFiles() {
  const result = await dialog.showOpenDialog({
    properties: ["openFile", "multiSelections"]
  });
  
  if (!result.canceled) {
    return result.filePaths;
  }
  
  return [];
}

// Open directory
async function openDirectory() {
  const result = await dialog.showOpenDialog({
    title: "Select Folder",
    properties: ["openDirectory"]
  });
  
  if (!result.canceled && result.filePaths.length > 0) {
    return result.filePaths[0];
  }
  
  return null;
}

// Save file
async function saveFile(defaultName = "untitled.txt") {
  const result = await dialog.showSaveDialog({
    title: "Save File",
    defaultPath: path.join(paths.home, defaultName),
    filters: [
      { name: "Text Files", extensions: ["txt"] },
      { name: "All Files", extensions: ["*"] }
    ]
  });
  
  if (!result.canceled) {
    return result.filePath;
  }
  
  return null;
}
```

### Message Boxes

```ts
// Confirmation dialog
async function confirmQuit() {
  const result = await dialog.showMessageBox({
    type: "question",
    title: "Confirm Quit",
    message: "Are you sure you want to quit?",
    detail: "Unsaved changes will be lost.",
    buttons: ["Quit", "Cancel"],
    defaultId: 1,
    cancelId: 1
  });
  
  return result.response === 0; // Returns true if "Quit" clicked
}

// Error dialog
async function showError(message: string, detail?: string) {
  await dialog.showMessageBox({
    type: "error",
    title: "Error",
    message,
    detail,
    buttons: ["OK"]
  });
}

// Warning with options
async function showWarning() {
  const result = await dialog.showMessageBox({
    type: "warning",
    title: "Warning",
    message: "This action cannot be undone",
    detail: "Are you sure you want to continue?",
    buttons: ["Continue", "Cancel", "Learn More"],
    defaultId: 1,
    cancelId: 1
  });
  
  if (result.response === 0) {
    // Continue
  } else if (result.response === 2) {
    shell.openExternal("https://docs.myapp.com/warning");
  }
}

// Info dialog
async function showInfo(message: string) {
  await dialog.showMessageBox({
    type: "info",
    title: "Information",
    message,
    buttons: ["OK"]
  });
}
```

## Keyboard Shortcuts

### Global Shortcuts

```ts
import { globalShortcut } from "electrobun/bun";

// Register global shortcut
globalShortcut.register("CommandOrControl+Shift+Space", () => {
  mainWindow.show();
  mainWindow.focus();
});

// Register multiple shortcuts
const shortcuts = [
  { key: "CommandOrControl+1", action: () => switchToTab(0) },
  { key: "CommandOrControl+2", action: () => switchToTab(1) },
  { key: "CommandOrControl+3", action: () => switchToTab(2) },
];

shortcuts.forEach(({ key, action }) => {
  globalShortcut.register(key, action);
});

// Unregister on quit
app.on("will-quit", () => {
  globalShortcut.unregisterAll();
});
```

### In-Window Shortcuts

```ts
// Define in menu (automatically registered)
{
  label: "New Window",
  accelerator: "CmdOrCtrl+N",
  action: () => createWindow()
}

// Custom accelerators in webview
document.addEventListener("keydown", (e) => {
  // Cmd/Ctrl + K
  if ((e.metaKey || e.ctrlKey) && e.key === "k") {
    e.preventDefault();
    openCommandPalette();
  }
  
  // Cmd/Ctrl + P
  if ((e.metaKey || e.ctrlKey) && e.key === "p") {
    e.preventDefault();
    openFileFinder();
  }
});
```

## Notifications

### System Notifications

```ts
import { Notification } from "electrobun/bun";

function showNotification(title: string, body: string) {
  new Notification({
    title,
    body,
    icon: "assets://notification-icon.png",
    sound: true
  }).show();
}

// With actions (on supported platforms)
const notification = new Notification({
  title: "New Message",
  body: "You have a new message from Alice",
  actions: [
    { type: "button", text: "Reply" },
    { type: "button", text: "Dismiss" }
  ]
});

notification.on("action", (index) => {
  if (index === 0) {
    openReplyWindow();
  }
});

notification.show();
```

## Resources

For more on Electrobun:
- **Core skill**: `electrobun` - Basic UI setup
- **Window management**: `electrobun-window-management` - Window coordination
- **RPC patterns**: `electrobun-rpc-patterns` - UI state sync
