---
name: tauri
description: >-
  Tauri builds desktop and mobile apps from a web frontend and a Rust backend,
  rendering the UI in the operating system's webview instead of a bundled
  Chromium. Use when creating or extending a Tauri v2 app: scaffolding with
  create-tauri-app, writing Rust commands and calling them with invoke, pushing
  events or channel data to the frontend, adding plugins, fixing "not allowed"
  permission errors in capabilities, bundling installers, or shipping signed
  auto-updates. Trigger words: tauri, tauri v2, tauri command, tauri plugin,
  capabilities, system webview, rust desktop app.
license: Apache-2.0
compatibility: "Tauri 2.x (checked against 2.12): Rust 1.90+ via rustup; Linux needs WebKitGTK 4.1 dev packages, macOS Xcode Command Line Tools, Windows MSVC Build Tools + WebView2; Node.js LTS only for a JavaScript frontend"
metadata:
  author: terminal-skills
  version: "1.1.0"
  category: development
  tags: "tauri, desktop, rust, cross-platform, webview"
  repository: https://github.com/tauri-apps/tauri
---

# Tauri

## Overview

Tauri is a framework for building cross-platform desktop and mobile applications using any web framework for the frontend and Rust for the backend. The UI runs in the system webview (WebView2 on Windows, WKWebView on macOS and iOS, WebKitGTK on Linux), so no browser engine is shipped with the app. The frontend talks to Rust through commands (request/response), events and channels (push), and every native API it may reach has to be granted in a capability file.

This skill covers Tauri v2. A v1 project (`tauri.conf.json` with an `allowlist`) is migrated with `npm run tauri migrate`. For installing and pinning the Rust toolchain itself, use the `rust` skill.

## Instructions

### Prerequisites

Tauri 2.12 requires Rust 1.90 or newer plus the platform's webview toolchain:

```bash
# Debian / Ubuntu (22.04 or newer: Tauri v2 needs WebKitGTK 4.1)
sudo apt update
sudo apt install libwebkit2gtk-4.1-dev build-essential curl wget file \
  libxdo-dev libssl-dev libayatana-appindicator3-dev librsvg2-dev
```

On macOS run `xcode-select --install` (full Xcode only for iOS targets). On Windows install the Microsoft C++ Build Tools ("Desktop development with C++") and make sure the MSVC Rust toolchain is the default (`rustup default stable-msvc`). WebView2 ships with Windows 10 1803 and later. `npm run tauri info` prints what is missing.

### Create a project

```bash
npm create tauri-app@latest markdown-notes -- --template react-ts --manager npm --identifier io.inkwell.notes
cd markdown-notes
npm install
npm run tauri dev          # compiles the Rust side and opens the window with hot reload
```

Templates: `vanilla`, `vue`, `svelte`, `react`, `solid`, `preact` (each with a `-ts` variant), `angular`, and the Rust frontends `yew`, `leptos`, `sycamore`, `dioxus`. To add Tauri to an existing frontend instead, run `npm install -D @tauri-apps/cli@latest` and `npx tauri init`; it asks for the dev server URL and the build command and creates `src-tauri/`.

The CLI is the same whichever way it is started: `npm run tauri dev`, `pnpm tauri dev`, `bun tauri dev`, or `cargo tauri dev` after `cargo install tauri-cli --version "^2.0.0" --locked`. With npm, flags for the CLI go after `--` (`npm run tauri build -- --debug`).

### Project layout

```
src-tauri/                    # next to the frontend's package.json and src/
├── Cargo.toml                # tauri, tauri-build, tauri-plugin-* crates
├── build.rs                  # tauri_build::build()
├── tauri.conf.json           # identifier, windows, build commands, bundle, plugin config
├── capabilities/default.json # what the frontend is allowed to call
└── src/
    ├── lib.rs                # app code: commands, plugins, setup — edit this
    └── main.rs               # desktop entry point that calls lib's run(); leave as is
```

App code lives in `lib.rs` because mobile builds load the app as a library. `tauri.conf.json` v2 keys: `build.devUrl`, `build.frontendDist`, `build.beforeDevCommand`, `build.beforeBuildCommand`, `app.windows`, `app.security`, `bundle`, `plugins`. A `tauri.linux.conf.json`, `tauri.windows.conf.json` or `tauri.macos.conf.json` next to it is merged on that platform; arrays are replaced, not appended.

### Commands: call Rust from the frontend

```rust
// src-tauri/src/lib.rs
#[tauri::command]
fn word_count(note_text: String) -> usize {
    note_text.split_whitespace().count()
}

#[tauri::command]
async fn parse_port(input: String) -> Result<u16, String> {
    input.trim().parse::<u16>().map_err(|e| e.to_string())
}

#[cfg_attr(mobile, tauri::mobile_entry_point)]
pub fn run() {
    tauri::Builder::default()
        .invoke_handler(tauri::generate_handler![word_count, parse_port])
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}
```

```typescript
import { invoke } from "@tauri-apps/api/core";
const words = await invoke<number>("word_count", { noteText: "Ship the release notes" }); // 4
const port = await invoke<number>("parse_port", { input: "80800" }); // rejects with the Err string
```

- Argument keys are camelCase in JavaScript (`noteText`) for snake_case Rust parameters (`note_text`); use `#[tauri::command(rename_all = "snake_case")]` to keep snake_case on both sides.
- Arguments must implement `serde::Deserialize`, return values and errors `serde::Serialize`. Most library error types such as `std::io::Error` do not, so map them to `String` or define an error enum with `thiserror` and a manual `Serialize` impl.
- Only the last `invoke_handler` call counts: list every command in one `generate_handler![…]`.
- Commands in `lib.rs` must not be `pub`; commands in another module must be `pub` and are registered as `notes::word_count`. Names are global, not scoped by module.
- A command without `async` runs on the main thread; declare long work `async`. An async command cannot take borrowed arguments such as `&str` or `State<'_, T>` unless it returns a `Result`.
- For large binary payloads return `tauri::ipc::Response` instead of JSON.

Shared state is registered once with `.manage(Mutex::new(Session::default()))` on the builder and injected by type as `State<'_, Mutex<Session>>` (Example 1). Tauri wraps managed state in an `Arc` already. Asking for a type that was never passed to `manage` (for example `State<'_, Session>` when `Mutex<Session>` is managed) still compiles; the call then fails at runtime and `invoke` rejects with ``state not managed for field `session` on command `save_note`. You must call `.manage()` before using this command``.

### Events and channels: push from Rust

Events are JSON, untyped, and delivered to every listener; use them for small notifications. Channels are ordered and fast; use them for progress and streams.

```rust
use tauri::{ipc::Channel, AppHandle, Emitter};

#[tauri::command]
fn export_notes(app: AppHandle, on_progress: Channel<u32>) {
    for percent in [10, 45, 80, 100] {
        on_progress.send(percent).unwrap();
    }
    app.emit("export-finished", "notes-2026-10.zip").unwrap();
}
```

```typescript
import { invoke, Channel } from "@tauri-apps/api/core";
import { listen } from "@tauri-apps/api/event";
const onProgress = new Channel<number>();
onProgress.onmessage = (percent) => console.log(`${percent}%`);
const unlisten = await listen<string>("export-finished", (e) => console.log(e.payload));
await invoke("export_notes", { onProgress });
unlisten();   // call it on unmount; `listen` returns a Promise, so await it first
```

`app.emit_to("settings", …)` targets one webview by label. In Rust, `emit` needs the `tauri::Emitter` trait in scope and `listen` needs `tauri::Listener`.

### Plugins and capabilities

Native APIs moved out of the core in v2 into plugins. `tauri add` installs the crate and the npm package, registers the plugin in `lib.rs` and adds its default permission (`dialog:default`) to the default capability:

```bash
npm run tauri add dialog      # also: fs, store, opener, notification, updater, process, http, shell
```

Nothing is callable from the frontend unless a capability grants it. Capability files in `src-tauri/capabilities/` are all enabled automatically and bind permissions to window labels:

```json
{
  "$schema": "../gen/schemas/desktop-schema.json",
  "identifier": "default",
  "windows": ["main"],
  "permissions": [
    "core:default", "dialog:default", "store:default", "fs:default",
    { "identifier": "fs:allow-write-text-file", "allow": [{ "path": "$DOCUMENT/Inkwell/**" }] }
  ]
}
```

- Permission ids have the forms `fs:default`, `fs:allow-write-text-file` and `fs:deny-remove` (plugin, then command). A missing one fails at runtime with `fs.write_text_file not allowed. Permissions associated with this command: …`, which lists the ids that would fix it.
- `fs` permissions need a path scope as well. `fs:default` only reads the app's own directories (`$APPCONFIG`, `$APPDATA`, `$APPLOCALDATA`, `$APPCACHE`, `$APPLOG`); anything else needs the object form with `allow` (or `fs:scope`), otherwise the call fails with `forbidden path`. `deny` always wins over `allow`.
- Paths the user picks through the dialog plugin's `open()` or `save()` are added to the fs scope until the app restarts.
- Your own commands are allowed in every window by default. Restrict them with `tauri_build::AppManifest::new().commands(&[…])` in `build.rs`, then grant them per capability.
- The system tray and menus are core features, not plugins: enable `features = ["tray-icon"]` on the `tauri` crate and use `tauri::tray::TrayIconBuilder` or `TrayIcon` from `@tauri-apps/api/tray`.

### Build, bundle and sign

```bash
npm run tauri build                          # release build + every bundle the host OS supports
npm run tauri build -- --bundles deb,appimage
npm run tauri build -- --debug               # debug build with the web inspector, in target/debug/bundle
npm run tauri icon ./app-icon.png            # generate all icon sizes into src-tauri/icons
```

Bundle types: `deb`, `rpm`, `appimage` (Linux), `nsis`, `msi` (Windows), `app`, `dmg` (macOS). Output goes to `src-tauri/target/release/bundle/`. Build each platform on its own OS; `tauri-apps/tauri-action@v1` does this in a GitHub Actions matrix and uploads the bundles to a release. The app version comes from `version` in `tauri.conf.json`, falling back to `Cargo.toml`.

macOS signing reads `APPLE_SIGNING_IDENTITY` (or `bundle.macOS.signingIdentity`), `APPLE_CERTIFICATE` and `APPLE_CERTIFICATE_PASSWORD`; notarization reads `APPLE_API_ISSUER`, `APPLE_API_KEY`, `APPLE_API_KEY_PATH`, or `APPLE_ID`, `APPLE_PASSWORD`, `APPLE_TEAM_ID`.

### Auto-updates

```bash
npm run tauri add updater
# Asks for a key password on the terminal; without a terminal it fails, so add --ci (empty password) or -p "$KEY_PASSWORD"
npm run tauri signer generate -- -w ~/.tauri/inkwell.key    # writes inkwell.key and inkwell.key.pub
export TAURI_SIGNING_PRIVATE_KEY="$HOME/.tauri/inkwell.key"       # path or key content; password in TAURI_SIGNING_PRIVATE_KEY_PASSWORD
npm run tauri build                                         # also writes .sig files next to the bundles
```

```json
{
  "bundle": { "createUpdaterArtifacts": true },
  "plugins": {
    "updater": {
      "pubkey": "dW50cnVzdGVkIGNvbW1lbnQ6IG1pbmlzaWduIHB1YmxpYyBrZXk6IDJENEU3ODc3RTIxMjlDOTMKUldTVG5CTGlkM2hPTGVyTnNVaEcySDQwWkZOK3NaS1NHZlREVE1qK3pza0pReGRoVkFMN080ZTIK",
      "endpoints": ["https://github.com/inkwell-app/inkwell/releases/latest/download/latest.json"]
    }
  }
}
```

`pubkey` is the content of `inkwell.key.pub`, never a file path. The endpoint returns JSON with `version` and, under `platforms`, per target (`linux-x86_64`, `windows-x86_64`, `darwin-aarch64`, …) a `url` and a `signature` holding the content of the `.sig` file; `tauri-action` generates this `latest.json`. In the frontend: `const update = await check(); if (update) { await update.downloadAndInstall(); await relaunch(); }` with `check` from `@tauri-apps/plugin-updater` and `relaunch` from `@tauri-apps/plugin-process` (add `process` too).

## Examples

### Example 1: Add a Rust command that saves a note and call it from React

**User request:** "In my Tauri app, add a command that writes a note into the app data folder and returns how many notes I saved this session."

```rust
// src-tauri/src/lib.rs
use std::{fs, sync::Mutex};
use tauri::{AppHandle, Manager, State};

#[derive(Default)]
struct Session { saved: u32 }

#[tauri::command]
fn save_note(app: AppHandle, session: State<'_, Mutex<Session>>, title: String, body: String) -> Result<u32, String> {
    if title.is_empty() || title.contains(['/', '\\']) || title.contains("..") {
        return Err("invalid note title".into());
    }
    let dir = app.path().app_data_dir().map_err(|e| e.to_string())?.join("notes");
    fs::create_dir_all(&dir).map_err(|e| e.to_string())?;
    fs::write(dir.join(format!("{title}.md")), body).map_err(|e| e.to_string())?;
    let mut session = session.lock().unwrap();
    session.saved += 1;
    Ok(session.saved)
}

// in run(): .manage(Mutex::new(Session::default()))
//           .invoke_handler(tauri::generate_handler![save_note])
```

```typescript
import { invoke } from "@tauri-apps/api/core";

const saved = await invoke<number>("save_note", { title: "Release plan", body: draft });
// rejects with the Rust Err string, e.g. "invalid note title"
```

**Result:** `npm run tauri dev` rebuilds the Rust side; the call creates `Release plan.md` under the app data directory (`~/.local/share/io.inkwell.notes/notes/` on Linux) and resolves to `1`, then `2` on the next save. No capability change is needed: the file is written by Rust, not by a frontend plugin call.

### Example 2: "Export fails with fs.write_text_file not allowed"

**User request:** "I let the user pick where to export a note, but writeTextFile throws 'not allowed'. How do I fix it?"

```bash
npm run tauri add dialog && npm run tauri add fs
```

`tauri add` inserts `dialog:default` and `fs:default` into `src-tauri/capabilities/default.json`; add the write command by hand so the list reads `"permissions": ["core:default", "opener:default", "dialog:default", "fs:default", "fs:allow-write-text-file"]` (`opener:default` comes with the template; keep it).

```typescript
import { save } from "@tauri-apps/plugin-dialog";
import { writeTextFile } from "@tauri-apps/plugin-fs";

const target = await save({
  defaultPath: "release-plan.md",
  filters: [{ name: "Markdown", extensions: ["md"] }],
});
if (target) await writeTextFile(target, noteBody);   // target is null when the dialog is cancelled
```

**Result:** `tauri dev` watches `src-tauri/` and rebuilds the app when the capability file changes; after that the native save dialog opens and the file is written. The path is in scope because the user chose it in the dialog; writing to a fixed location without a dialog needs an explicit scope such as `{ "identifier": "fs:allow-write-text-file", "allow": [{ "path": "$DOCUMENT/Inkwell/**" }] }`.

## Guidelines

- Use commands for request-response patterns and events for push notifications; use a channel, not events, for progress and streamed data.
- Define all allowed APIs in `capabilities/` following the principle of least privilege: grant single `allow-*` permissions and narrow path scopes instead of `$HOME/**`. Capabilities do not protect against what your own Rust commands do, so validate their arguments (file names, paths, URLs).
- The templates ship with `"app": { "security": { "csp": null } }`, which disables the Content Security Policy. Set a restrictive `csp` before release and avoid loading scripts from a CDN.
- A window that appears in several capabilities gets the union of their permissions; capabilities match window labels, not titles.
- Use `tauri::State<Mutex<T>>` for shared mutable state; the standard `Mutex` is fine unless the guard is held across an `.await`.
- Use `@tauri-apps/plugin-store` over `localStorage` for settings the Rust side also needs: it persists to a file in the app data directory and is readable from both sides.
- Handle errors in Rust with `Result<T, E>` where `E` implements `Serialize`, so failures surface as rejected promises in JS.
- The updater cannot be used without signatures. Keep the private key and its password out of the repository (CI secrets); a `.env` file is not read. If the key is lost, installed apps can no longer be updated.
- Webviews differ per platform (WebKitGTK and WKWebView are not Chromium): test CSS and newer web APIs on every target OS.
- Build Linux bundles on the oldest distribution you support (Ubuntu 22.04 or Debian 12 are the baseline for WebKitGTK 4.1); a newer build host raises the glibc version the AppImage requires.
- Keep each `@tauri-apps/*` npm package and its `tauri*` crate on the same major and minor version; `tauri build` stops with "Found version mismatched Tauri packages" otherwise.
- When not to use Tauri: when the app depends on identical rendering everywhere or on Chromium-only APIs, an Electron-style bundled engine is the safer choice.
