---
name: tauri-desktop
description: >-
  Tauri 2.0 project setup, Rust backend + web frontend, plugin system, IPC commands, security model, auto-update, and mobile support. Use when building lightweight cross-platform desktop or mobile apps with Tauri.
---

# Tauri Desktop Skill

Build lightweight, secure desktop (and mobile) apps with Tauri 2.0 — Rust backend, web frontend.

---

## Why Tauri

| Feature | Tauri | Electron |
|---------|-------|----------|
| Bundle size | 2-10 MB | 80-150 MB |
| Memory usage | 30-80 MB | 100-300 MB |
| Backend language | Rust | Node.js |
| Security model | Capability-based permissions | Full Node.js access |
| Mobile support | Yes (Tauri 2.0) | No |
| Auto-updater | Built-in | electron-updater |

---

## Project Structure

```
project/
├── src/                          # Frontend (any web framework)
│   ├── main.ts
│   ├── App.tsx                   # React/Vue/Svelte/vanilla
│   └── styles.css
├── src-tauri/                    # Rust backend
│   ├── src/
│   │   ├── main.rs              # Entry point
│   │   ├── lib.rs               # Commands and setup
│   │   └── commands/            # IPC command modules
│   │       ├── mod.rs
│   │       └── files.rs
│   ├── capabilities/            # Security permissions
│   │   └── default.json
│   ├── icons/                   # App icons
│   ├── Cargo.toml               # Rust dependencies
│   └── tauri.conf.json          # Tauri configuration
├── package.json
├── vite.config.ts               # Frontend bundler
└── tsconfig.json
```

---

## IPC Commands

### Rust Side (Backend)

```rust
// src-tauri/src/lib.rs
use tauri::Manager;

#[tauri::command]
fn greet(name: &str) -> String {
    format!("Hello, {}! From Rust.", name)
}

#[tauri::command]
async fn read_file(path: String) -> Result<String, String> {
    std::fs::read_to_string(&path).map_err(|e| e.to_string())
}

#[tauri::command]
async fn save_settings(
    app: tauri::AppHandle,
    settings: serde_json::Value,
) -> Result<(), String> {
    let path = app.path().app_config_dir().map_err(|e| e.to_string())?;
    std::fs::create_dir_all(&path).map_err(|e| e.to_string())?;
    let file = path.join("settings.json");
    std::fs::write(file, settings.to_string()).map_err(|e| e.to_string())
}

pub fn run() {
    tauri::Builder::default()
        .invoke_handler(tauri::generate_handler![greet, read_file, save_settings])
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}
```

### Frontend Side (TypeScript)

```typescript
import { invoke } from '@tauri-apps/api/core';

// Call Rust commands from frontend
const greeting = await invoke<string>('greet', { name: 'World' });

const content = await invoke<string>('read_file', { path: '/tmp/test.txt' });

await invoke('save_settings', {
  settings: { theme: 'dark', fontSize: 14 },
});
```

---

## Security Model (Capabilities)

```json
// src-tauri/capabilities/default.json
{
  "$schema": "../gen/schemas/desktop-schema.json",
  "identifier": "default",
  "description": "Default app permissions",
  "windows": ["main"],
  "permissions": [
    "core:default",
    "dialog:default",
    "fs:default",
    {
      "identifier": "fs:allow-read-text-file",
      "allow": [{ "path": "$APPDATA/**" }]
    },
    {
      "identifier": "fs:allow-write-text-file",
      "allow": [{ "path": "$APPDATA/**" }]
    }
  ]
}
```

Key security principles:
- Allowlist by default: Frontend can only access explicitly permitted APIs
- Scoped filesystem access: Restrict to specific directories
- No arbitrary shell access: Commands must be predefined in Rust
- CSP enforced: Content Security Policy headers set automatically

---

## Plugins (Tauri 2.0)

```toml
# src-tauri/Cargo.toml
[dependencies]
tauri = { version = "2", features = [] }
tauri-plugin-dialog = "2"
tauri-plugin-fs = "2"
tauri-plugin-shell = "2"
tauri-plugin-store = "2"
tauri-plugin-updater = "2"
tauri-plugin-notification = "2"
```

```rust
// Register plugins
tauri::Builder::default()
    .plugin(tauri_plugin_dialog::init())
    .plugin(tauri_plugin_fs::init())
    .plugin(tauri_plugin_store::Builder::new().build())
    .plugin(tauri_plugin_updater::Builder::new().build())
    .invoke_handler(tauri::generate_handler![greet])
    .run(tauri::generate_context!())
    .expect("error while running tauri application");
```

---

## Auto-Updater

```json
// src-tauri/tauri.conf.json (excerpt)
{
  "plugins": {
    "updater": {
      "pubkey": "YOUR_PUBLIC_KEY",
      "endpoints": [
        "https://releases.example.com/{{target}}/{{arch}}/{{current_version}}"
      ]
    }
  }
}
```

```typescript
// Frontend update check
import { check } from '@tauri-apps/plugin-updater';

const update = await check();
if (update) {
  await update.downloadAndInstall();
  await relaunch();
}
```

---

## Building and Distribution

```bash
# Development
npm run tauri dev

# Build for current platform
npm run tauri build

# Build for specific target
npm run tauri build --target x86_64-pc-windows-msvc
npm run tauri build --target aarch64-apple-darwin
npm run tauri build --target x86_64-unknown-linux-gnu

# Mobile (Tauri 2.0)
npm run tauri android dev
npm run tauri ios dev
```

### Distribution Formats

| Platform | Formats |
|----------|---------|
| macOS | .dmg, .app |
| Windows | .msi, .exe (NSIS) |
| Linux | .deb, .rpm, .AppImage |
| Android | .apk, .aab |
| iOS | .ipa |

---

## Development Tips

- Use `window.__TAURI__` to detect Tauri environment in frontend
- State management: Use Tauri's `State` for Rust-side state, frontend store for UI state
- File dialogs: Use `@tauri-apps/plugin-dialog` instead of browser file input
- System tray: Configure in `tauri.conf.json` with menu items
- Multi-window: Create with `WebviewWindow::new()` from Rust or `WebviewWindow.create()` from JS

---

## Related Resources

- `~/.claude/skills/rust/SKILL.md` - Rust language patterns
- `~/.claude/agents/desktop-developer.md` - Desktop development agent
- `~/.claude/rules/stacks/rust.md` - Rust stack guide

---

_Small binaries. Strong security. Native performance. Web flexibility._
