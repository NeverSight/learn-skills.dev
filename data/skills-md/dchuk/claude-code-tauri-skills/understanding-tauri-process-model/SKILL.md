---
name: understanding-tauri-process-model
description: Explains the Tauri process model architecture including the Core process, WebView process, inter-process communication, multiwindow handling, and process isolation security patterns.
---

# Tauri Process Model

Tauri implements a multi-process architecture similar to Electron and modern web browsers. Understanding this model is essential for building secure, performant Tauri applications.

## Architecture Overview

```
+------------------------------------------------------------------+
|                        TAURI APPLICATION                          |
+------------------------------------------------------------------+
|                                                                   |
|  +-----------------------------+                                  |
|  |       CORE PROCESS          |                                  |
|  |         (Rust)              |                                  |
|  |                             |                                  |
|  |  +----------------------+   |                                  |
|  |  | Window Manager       |   |                                  |
|  |  +----------------------+   |                                  |
|  |  | System Tray          |   |                                  |
|  |  +----------------------+   |                                  |
|  |  | Global State         |   |                                  |
|  |  +----------------------+   |                                  |
|  |  | IPC Router           |   |                                  |
|  |  +----------------------+   |                                  |
|  |  | OS Abstractions      |   |                                  |
|  +-------------+---------------+                                  |
|                |                                                  |
|                | IPC (Inter-Process Communication)                |
|                |                                                  |
|     +----------+----------+----------+                            |
|     |          |          |          |                            |
|     v          v          v          v                            |
|  +------+  +------+  +------+  +------+                           |
|  |WebView|  |WebView|  |WebView|  |WebView|                       |
|  |  #1   |  |  #2   |  |  #3   |  |  #N   |                       |
|  +------+  +------+  +------+  +------+                           |
|  | HTML |  | HTML |  | HTML |  | HTML |                           |
|  | CSS  |  | CSS  |  | CSS  |  | CSS  |                           |
|  | JS   |  | JS   |  | JS   |  | JS   |                           |
|  +------+  +------+  +------+  +------+                           |
|                                                                   |
+------------------------------------------------------------------+
```

## The Core Process

The Core process is the application's entry point and central hub. It runs Rust code and has exclusive access to operating system capabilities.

### Responsibilities

| Responsibility | Description |
|----------------|-------------|
| Window Management | Creates and orchestrates application windows |
| System Integration | Manages system tray menus and notifications |
| IPC Routing | Handles all inter-process communication |
| Global State | Manages application-wide settings and database connections |
| OS Abstractions | Provides cross-platform APIs |

### Why Rust for the Core Process

Rust powers the Core process for its memory-safety guarantees. The ownership system prevents:

- Null pointer dereferences
- Buffer overflows
- Data races
- Use-after-free bugs

This is critical because the Core process has full system access.

```
+------------------------------------------+
|            CORE PROCESS                   |
|                                          |
|  Memory Safety via Rust Ownership:       |
|  - No null pointers                      |
|  - No buffer overflows                   |
|  - No data races                         |
|  - No use-after-free                     |
|                                          |
|  Full OS Access:                         |
|  - File system                           |
|  - Network                               |
|  - System APIs                           |
|  - Hardware interfaces                   |
+------------------------------------------+
```

## The WebView Process

WebView processes render the user interface using the operating system's native WebView library.

### Platform-Specific WebViews

```
+------------------+------------------+------------------+
|     WINDOWS      |      MACOS       |      LINUX       |
+------------------+------------------+------------------+
|                  |                  |                  |
|  Microsoft Edge  |    WKWebView     |    webkitgtk     |
|    WebView2      |                  |                  |
|                  |                  |                  |
|  Chromium-based  |  Safari engine   |  WebKit engine   |
|                  |                  |                  |
+------------------+------------------+------------------+
         |                  |                  |
         +------------------+------------------+
                           |
                    Dynamic Linking
                    (Not bundled)
                           |
                    Smaller executables
```

### Key Characteristics

1. **Dynamic Linking**: WebView libraries are linked at runtime, not bundled
2. **Web Technologies**: Execute HTML, CSS, and JavaScript
3. **Framework Support**: Works with React, Vue, Svelte, Solid, etc.
4. **Isolation**: Each WebView runs in its own process space

## Process Communication (IPC)

All communication between processes flows through the Core process.

```
+----------------+                              +----------------+
|   WebView A    |                              |   WebView B    |
|                |                              |                |
|  invoke()  ----+---->+----------------+<------+---- invoke()   |
|                |     |  CORE PROCESS  |       |                |
|  <---- listen  |<----+                +------>|  listen ---->  |
|                |     |  - Validates   |       |                |
+----------------+     |  - Routes      |       +----------------+
                       |  - Filters     |
                       |  - Transforms  |
                       +----------------+
                              |
                              v
                       +----------------+
                       |   OS / System  |
                       |   Resources    |
                       +----------------+
```

### IPC Flow

1. WebView calls `invoke()` with a command name and payload
2. Core process receives the message
3. Core process validates and processes the request
4. Core process may interact with OS resources
5. Core process sends response back to WebView

### Example: Basic IPC

**Frontend (JavaScript)**
```javascript
import { invoke } from '@tauri-apps/api/core';

// Call a Rust command
const result = await invoke('greet', { name: 'World' });
```

**Backend (Rust)**
```rust
#[tauri::command]
fn greet(name: &str) -> String {
    format!("Hello, {}!", name)
}
```

## Multiwindow Handling

A single Core process manages multiple WebView processes.

```
                    +-------------------+
                    |   CORE PROCESS    |
                    |                   |
                    |  Shared State:    |
                    |  - User session   |
                    |  - App config     |
                    |  - DB connection  |
                    +-------------------+
                           /|\
                          / | \
                         /  |  \
                        /   |   \
                       /    |    \
                      v     v     v
               +------+ +------+ +------+
               |Main  | |Settings| |About|
               |Window| |Window | |Window|
               +------+ +------+ +------+
```

### Window Management Patterns

**Creating Windows**
```rust
use tauri::Manager;

#[tauri::command]
fn open_settings(app: tauri::AppHandle) {
    tauri::WebviewWindowBuilder::new(
        &app,
        "settings",
        tauri::WebviewUrl::App("settings.html".into())
    )
    .title("Settings")
    .build()
    .unwrap();
}
```

**Cross-Window Communication**
```rust
use tauri::Manager;

#[tauri::command]
fn broadcast_update(app: tauri::AppHandle, data: String) {
    // Emit to all windows
    app.emit("data-updated", data).unwrap();
}
```

**Window-Specific Events**
```rust
use tauri::Manager;

#[tauri::command]
fn notify_window(app: tauri::AppHandle, window_label: String, data: String) {
    if let Some(window) = app.get_webview_window(&window_label) {
        window.emit("notification", data).unwrap();
    }
}
```

## Process Isolation and Security

### The Principle of Least Privilege

> "If you have a gardener coming over to trim your hedge, you give them the key to your garden. You would not give them the keys to your house."

```
+------------------------------------------------------------------+
|                     SECURITY BOUNDARIES                           |
+------------------------------------------------------------------+
|                                                                   |
|  +---------------------------+   +---------------------------+    |
|  |      CORE PROCESS         |   |     WEBVIEW PROCESS       |    |
|  |      (Trusted Zone)       |   |    (Untrusted Zone)       |    |
|  +---------------------------+   +---------------------------+    |
|  |                           |   |                           |    |
|  |  - File system access     |   |  - Render UI only         |    |
|  |  - Database connections   |   |  - User input handling    |    |
|  |  - Network requests       |   |  - Display data           |    |
|  |  - Crypto operations      |   |  - Call allowed commands  |    |
|  |  - Secrets management     |   |                           |    |
|  |  - Business logic         |   |  NO DIRECT ACCESS TO:     |    |
|  |                           |   |  - File system            |    |
|  |                           |   |  - Network (direct)       |    |
|  |                           |   |  - System APIs            |    |
|  +---------------------------+   +---------------------------+    |
|                                                                   |
+------------------------------------------------------------------+
```

### Security Benefits of Process Isolation

| Benefit | Description |
|---------|-------------|
| Crash Containment | Failures in one process don't crash the entire app |
| State Recovery | Invalid processes can be restarted independently |
| Attack Surface Reduction | Compromised WebView has limited capabilities |
| Resource Protection | Sensitive data stays in Core process |

### Security Best Practices

**In the Frontend (WebView)**

1. Sanitize all user input
2. Never handle secrets
3. Defer business logic to Core process
4. Implement Content Security Policy (CSP)

**In the Backend (Core Process)**

1. Validate all IPC inputs
2. Use the capability system to restrict commands
3. Apply principle of least privilege to each window

### Capability-Based Security

Tauri uses a capability system to control what each window can access.

```
+------------------+     +------------------+     +------------------+
|   Main Window    |     | Settings Window  |     |  Viewer Window   |
+------------------+     +------------------+     +------------------+
| Capabilities:    |     | Capabilities:    |     | Capabilities:    |
| - read_file      |     | - read_config    |     | - read_file      |
| - write_file     |     | - write_config   |     | (read only)      |
| - network        |     |                  |     |                  |
| - notifications  |     |                  |     |                  |
+------------------+     +------------------+     +------------------+
```

**Example: Capability Configuration**

```json
{
  "identifier": "main-capability",
  "description": "Capability for the main window",
  "windows": ["main"],
  "permissions": [
    "core:default",
    "fs:read-files",
    "fs:write-files",
    "http:default"
  ]
}
```

## Process Lifecycle

```
+------------------------------------------------------------------+
|                      APPLICATION LIFECYCLE                        |
+------------------------------------------------------------------+
|                                                                   |
|  1. App Launch                                                    |
|     +------------------+                                          |
|     | Core Process     |  <-- Starts first                        |
|     | Initializes      |                                          |
|     +------------------+                                          |
|              |                                                    |
|              v                                                    |
|  2. Window Creation                                               |
|     +------------------+                                          |
|     | WebView Process  |  <-- Core creates WebViews               |
|     | Spawned          |                                          |
|     +------------------+                                          |
|              |                                                    |
|              v                                                    |
|  3. Running                                                       |
|     +--------+    IPC    +----------+                             |
|     | Core   |<--------->| WebViews |                             |
|     +--------+           +----------+                             |
|              |                                                    |
|              v                                                    |
|  4. Shutdown                                                      |
|     +------------------+                                          |
|     | WebViews close   |  <-- WebViews terminate first            |
|     | Core cleans up   |  <-- Core process exits last             |
|     +------------------+                                          |
|                                                                   |
+------------------------------------------------------------------+
```

## Summary

| Aspect | Core Process | WebView Process |
|--------|--------------|-----------------|
| Language | Rust | JavaScript/TypeScript |
| Quantity | One per app | One or more per app |
| OS Access | Full | None (via IPC only) |
| Role | Backend, orchestration | UI rendering |
| Security | Trusted | Untrusted |
| Crash Impact | App terminates | Window closes |

The Tauri process model provides a secure foundation for building desktop applications by maintaining strict separation between the trusted Core process and the potentially vulnerable WebView processes. All sensitive operations should be implemented in the Core process, with the WebView serving only as a presentation layer.
