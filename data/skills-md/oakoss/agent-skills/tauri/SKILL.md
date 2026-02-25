---
name: tauri
description: |
  Tauri v2 framework for building desktop and mobile applications with web frontends and Rust backends. Covers project setup, IPC commands and events, window management, system tray, file system access, plugin system (clipboard, dialog, notification, updater, deep-link), multi-window apps, sidecar binaries, custom protocols, app signing, distribution, auto-updates, and the capability-based security model.

  Use when scaffolding a Tauri project, defining Rust commands, invoking backend logic from the frontend, configuring permissions and capabilities, setting up plugins, managing application state, building system tray menus, creating multi-window layouts, bundling sidecar binaries, implementing auto-updates, or signing apps for distribution.
license: MIT
metadata:
  author: oakoss
  version: '1.0'
  source: 'https://v2.tauri.app'
user-invocable: false
---

# Tauri

## Overview

Tauri is a framework for building **desktop and mobile applications** using web technologies (HTML, CSS, JavaScript/TypeScript) for the UI and **Rust** for the backend logic. It produces small, fast binaries by leveraging the OS webview instead of bundling a browser engine. The IPC layer connects the frontend to Rust commands through a capability-based permission system.

**When to use:** Cross-platform desktop/mobile apps with web UIs, system-level integrations (tray, notifications, file system), apps requiring small bundle sizes, security-sensitive applications needing fine-grained permission control.

**When NOT to use:** Pure web apps with no native requirements, Electron apps that depend heavily on Node.js APIs with no Rust migration path, projects where the team has no capacity to maintain Rust code.

## Quick Reference

| Pattern               | API / Config                                             | Key Points                                   |
| --------------------- | -------------------------------------------------------- | -------------------------------------------- |
| Create project        | `cargo create-tauri-app` or `pnpm create tauri-app`      | Scaffolds Rust backend + frontend framework  |
| Define command        | `#[tauri::command] fn name() {}`                         | Must register in `generate_handler!`         |
| Invoke from frontend  | `invoke('cmd_name', { arg: value })`                     | Returns Promise, args as camelCase JSON      |
| Emit event (frontend) | `emit('event-name', payload)`                            | Global event, all listeners receive          |
| Listen event          | `listen('event-name', handler)`                          | Returns unlisten function                    |
| Manage state          | `app.manage(MyState {})` + `State<'_, MyState>`          | No Arc needed, Mutex for mutability          |
| Window creation       | `WebviewWindowBuilder::new(app, label, url)`             | Label must be unique per window              |
| System tray           | `TrayIconBuilder::new().menu(&menu).build(app)`          | Requires `tray-icon` Cargo feature           |
| Add plugin (Rust)     | `.plugin(tauri_plugin_name::init())`                     | Register in `Builder` chain                  |
| Add plugin (frontend) | `@tauri-apps/plugin-name`                                | NPM package per plugin                       |
| Define capability     | `src-tauri/capabilities/*.json`                          | Scoped to windows, merged at build           |
| Grant permission      | `"permissions": ["plugin:scope"]`                        | Commands inaccessible without explicit grant |
| Sidecar binary        | `tauri.conf.json` `bundle.externalBin`                   | Name must match `{name}-{target_triple}`     |
| Custom protocol       | `tauri::Builder::default().register_uri_scheme_protocol` | Intercept custom `scheme://` URLs            |
| Auto-updater          | `tauri-plugin-updater` + JSON endpoint                   | Requires code signing                        |
| App bundle/sign       | `cargo tauri build`                                      | Platform-specific signing via env vars       |

## Common Mistakes

| Mistake                                         | Correct Pattern                                                                      |
| ----------------------------------------------- | ------------------------------------------------------------------------------------ |
| Multiple `generate_handler!` calls              | Pass all commands to a single `generate_handler!` invocation                         |
| Using `&str` in async command args              | Use owned `String` types in async commands                                           |
| Forgetting to add capability for plugin         | Add permission identifier in `src-tauri/capabilities/*.json`                         |
| Wrapping state in `Arc`                         | Tauri `State` handles reference counting internally                                  |
| Using `std::sync::Mutex` across `.await` points | Use `tokio::sync::Mutex` for async commands holding locks across awaits              |
| Wrong sidecar binary name                       | Binary must be named `{name}-{target_triple}` (e.g., `mybin-x86_64-pc-windows-msvc`) |
| Assuming all windows share capabilities         | Each window/webview gets capabilities scoped by label                                |
| Using `SystemTray` (v1 API)                     | Use `TrayIconBuilder` from `tauri::tray` module in v2                                |
| Not signing app before enabling updater         | Auto-updater requires valid code signing on all platforms                            |
| Using window title for security decisions       | Capabilities use window **labels**, not titles                                       |

## Delegation

- **Command pattern discovery**: Use `Explore` agent
- **Security review**: Use `Task` agent
- **Code review**: Delegate to `code-reviewer` agent

> If the `rust` skill is available, delegate Rust language patterns, error handling, and async/concurrency to it.
> If the `react-patterns` skill is available, delegate React frontend patterns to it.
> If the `svelte` skill is available, delegate Svelte frontend patterns to it.
> If the `vite` skill is available, delegate build tooling and dev server configuration to it.
> If the `github-actions` skill is available, delegate CI/CD pipeline and release workflow configuration to it.

## References

- [Project setup, configuration, and directory structure](references/project-setup.md)
- [IPC commands, events, and channels](references/ipc-commands.md)
- [State management patterns](references/state-management.md)
- [Window management and multi-window apps](references/window-management.md)
- [System tray and menus](references/system-tray.md)
- [Plugin system and official plugins](references/plugin-system.md)
- [Security model, capabilities, and permissions](references/security-model.md)
- [Sidecar binaries and custom protocols](references/sidecar-protocols.md)
- [App signing, distribution, and auto-updates](references/distribution.md)
