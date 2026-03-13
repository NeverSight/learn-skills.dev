---
name: tauri
description: "Tauri v2 development: build cross-platform desktop/mobile apps with Rust backends and web frontends. Use when configuring tauri.conf.json, implementing Rust commands (#[tauri::command]), setting up IPC patterns (invoke, emit, channels), managing state, configuring permissions/capabilities, troubleshooting build issues, or deploying. Triggers on Tauri, src-tauri, tauri.conf.json, capabilities."
---

# Tauri v2 Development Skill

> Build cross-platform desktop and mobile apps with web frontends and Rust backends using Tauri v2.

## Core Principles

- **Architecture:** Use Rust for the backend (performance, native APIs) and any web framework for the frontend (UI, routing).
- **Communication:** Use Tauri's IPC (`invoke`, `events`, `channels`) to bridge the Rust backend and the web frontend.
- **Security-First:** Everything is denied by default. Explicitly configure permissions in `src-tauri/capabilities/` to allow frontend access to backend commands and plugins.
- **Cross-Platform:** Write once, compile to Windows, macOS, Linux, Android, and iOS. Use `lib.rs` for shared logic.

## Quick Setup Checklist

Before making changes to a Tauri project, verify:
- `src-tauri/tauri.conf.json` has `build.devUrl` and `build.frontendDist` configured.
- `src-tauri/capabilities/default.json` exists and includes necessary permissions.
- All custom Rust commands are registered in `tauri::generate_handler![]` within `lib.rs` or `main.rs`.
- `lib.rs` contains shared code, essential for mobile builds.

## Primary Workflows

### Creating and Using Commands

1. **Define the command** in Rust with `#[tauri::command]`:
   ```rust
   // src-tauri/src/lib.rs
   #[tauri::command]
   fn greet(name: String) -> Result<String, String> {
       Ok(format!("Hello, {}!", name))
   }
   ```
2. **Register the command** in `tauri::Builder`:
   ```rust
   tauri::Builder::default()
       .invoke_handler(tauri::generate_handler![greet])
       // ...
   ```
3. **Invoke the command** from the frontend:
   ```typescript
   import { invoke } from '@tauri-apps/api/core';
   const response = await invoke<string>('greet', { name: 'World' });
   ```

**For more detailed IPC patterns (async, error handling, events, channels), see [ipc.md](references/ipc.md).**

### Managing Application State

1. **Define state struct** with thread-safe types (e.g., `Mutex`):
   ```rust
   use std::sync::Mutex;
   struct AppState { counter: Mutex<u32> }
   ```
2. **Register state** in the builder:
   ```rust
   tauri::Builder::default()
       .setup(|app| {
           app.manage(AppState { counter: Mutex::new(0) });
           Ok(())
       })
   ```
3. **Access state** in commands:
   ```rust
   #[tauri::command]
   fn increment(state: tauri::State<'_, AppState>) -> Result<u32, String> {
       let mut count = state.counter.lock().map_err(|e| e.to_string())?;
       *count += 1;
       Ok(*count)
   }
   ```

### Configuring Security and Capabilities

Tauri v2 requires explicit capabilities for all IPC commands, including custom ones and core plugins.

**For a complete guide to capabilities, see [capabilities.md](references/capabilities.md).**

### Configuration and Build Settings

Manage project settings, icons, plugins, and build commands in `tauri.conf.json`.

**For `tauri.conf.json` and `Cargo.toml` configurations, see [config.md](references/config.md).**

## Critical Rules

- **Always register commands:** Commands not in `generate_handler![]` fail silently on the frontend.
- **Never use borrowed types in async commands:** Use owned types (`String`, not `&str`). Async commands cannot borrow data across await points.
- **Never block the main thread:** Use `async` or `std::thread::spawn` for heavy I/O operations.
- **Always handle errors explicitly:** Return `Result<T, AppError>` from commands where `AppError` implements `serde::Serialize`.
- **Always use `@tauri-apps/api/core`:** The `@tauri-apps/api/tauri` path is deprecated from v1.

## Troubleshooting

- **"Command not found" / Promise hangs:** Check if the command is added to `generate_handler![]`. Ensure frontend parameter names are `camelCase` and Rust parameters are `snake_case`.
- **"Permission denied":** The command or plugin lacks a capability in `src-tauri/capabilities/`.
- **White screen on launch:** Ensure the frontend dev server is running and matches `build.devUrl` in `tauri.conf.json`. Check `beforeDevCommand`.
- **Mobile build fails:** Ensure Rust targets are installed (`rustup target add aarch64-linux-android ...`) and that the app logic is in `lib.rs` rather than `main.rs`.