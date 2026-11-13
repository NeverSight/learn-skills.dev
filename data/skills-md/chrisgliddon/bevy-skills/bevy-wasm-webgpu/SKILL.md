---
name: bevy-wasm-webgpu
description: "Use when targeting Bevy 0.20 at `wasm32-unknown-unknown`, choosing the `webgl2` or `webgpu` feature, setting `WgpuSettings { backends, priority: WgpuSettingsPriority::WebGPU }`, attaching to a canvas with `Window { canvas, fit_canvas_to_parent }`, generating glue with `wasm-bindgen`, or debugging asset HTTP 404s and `Task` cancellation in the browser."
license: MIT
compatibility: opencode,claude-code,cursor
metadata:
  tier: "2"
  area: platform
  bevy_version: "0.20"
---

# Bevy 0.20 — WASM + WebGPU

## When to use this skill

- Targeting `wasm32-unknown-unknown` for browser delivery.
- Choosing WebGL2 (reach) vs WebGPU (compute, speed).
- Trimming the bundle from 30 MB down to 5–10 MB.
- Pointing Bevy at your own `<canvas>` and keeping browser hotkeys alive.
- Configuring asset paths so the browser finds `assets/`.

## Canonical Cargo.toml

```toml
[package]
name = "myclient"
version = "0.1.0"
edition = "2024"

[dependencies]
bevy = { version = "0.20", default-features = false, features = [
    "3d_bevy_render",   # stock 3D renderer + glTF; "3d_api" if you bring your own
    "bevy_winit",       # window + event loop (not in *_bevy_render)
    "default_app",      # assets, log, state
    "scene",            # WorldAssetRoot / glTF spawning
    "webgl2",           # broadest reach; `default_platform` would add it anyway
    "webgpu",           # compute shaders, faster; still a Chrome/Edge-first story
    "mouse", "keyboard", "touch", "gestures",
    # "ui", "audio" — opt-in since 0.19; "ui" requires "picking" for clicks
] }

[profile.release]
opt-level = "z"      # size, not speed — WASM is bandwidth-bound
lto = "fat"
codegen-units = 1
strip = "debuginfo"
panic = "abort"
```

## Build & serve

```bash
cargo build --release --target wasm32-unknown-unknown
wasm-bindgen --target web --out-dir public/ \
    target/wasm32-unknown-unknown/release/myclient.wasm
wasm-opt -Oz public/myclient_bg.wasm -o public/myclient_bg.wasm   # optional, large win
# `assets/` must sit next to myclient.js: Bevy fetches `./assets/...` relative to the page.
python3 -m http.server -d public/ 8080
```

## Canvas and backend selection

```rust
use bevy::prelude::*;
use bevy::render::settings::{Backends, WgpuSettings, WgpuSettingsPriority};
use bevy::render::RenderPlugin;

fn main() {
    App::new()
        .add_plugins(
            DefaultPlugins
                .set(WindowPlugin {
                    primary_window: Some(Window {
                        // CSS selector; Bevy attaches to this element instead of
                        // appending a new <canvas> to <body>.
                        canvas: Some("#bevy".into()),
                        fit_canvas_to_parent: true,
                        // Keep F5 / Ctrl+R / Tab working in the browser.
                        prevent_default_event_handling: false,
                        ..default()
                    }),
                    ..default()
                })
                .set(RenderPlugin {
                    render_creation: WgpuSettings {
                        // None = let wgpu pick (WebGPU if the browser has it, else WebGL2).
                        backends: Some(Backends::BROWSER_WEBGPU | Backends::GL),
                        // 0.19+: `WebGPU` (was `Compatibility`). Use `WebGL2` when the
                        // `webgl2` feature is the only backend you ship.
                        priority: WgpuSettingsPriority::WebGPU,
                        ..default()
                    }
                    .into(),
                    ..default()
                }),
        )
        .run();
}
```

`WgpuSettingsPriority::WebGPU` requests WebGPU default limits (portable). `Functionality` asks for everything the adapter has. `WebGL2` adds the WebGL2 constraints. Env override: `WGPU_SETTINGS_PRIO=webgpu|functionality|webgl2`.

## Minimal `index.html`

```html
<!doctype html>
<html lang="en">
  <head><meta charset="utf-8"><title>myclient</title></head>
  <body style="margin:0;background:#000">
    <canvas id="bevy"></canvas>
    <script type="module">
      import init from "./myclient.js";
      init();
    </script>
  </body>
</html>
```

## Gotchas

### 0.19 → 0.20

- **Shaders are WESL.** `naga_oil` `#import` / `#ifdef` files fail to load; port to `.wesl` (`import bevy_pbr::render::forward_io::VertexOutput;`, `@if(FLAG)`). The `shader_format_wesl` feature is gone (always on) and GLSL support is removed. Plain WGSL still works.
- **Mesh shaders are not supported on web.** Keep the `mesh_shader_*` paths native-only.
- **Texture compression for web:** `compressed_image_saver_universal` (UASTC/Basis, one file for every GPU). The new default `compressed_image_saver` emits BCn or ASTC, which browsers only partly expose.
- **`Pointer<Press>` is `PointerPress`** (flat pointer events) if you handle touch/mouse through picking.

### 0.18 → 0.19

- **`WgpuSettingsPriority::Compatibility` → `WgpuSettingsPriority::WebGPU`**; `WGPU_SETTINGS_PRIO=compatibility` → `webgpu`.
- **Dropping a `Task<T>` on web cancels it.** Fire-and-forget work needs `task.detach()`; native behaviour is unchanged.
- **`ui`, `audio` are no longer implied by `3d`/`2d`.** A trimmed web manifest that shipped buttons or sound in 0.18 loses them silently; add the features.
- **`bevy_window` left `default_app`** (now in `common_api`). `3d_api`/`3d_bevy_render` still include it.
- **Android game activity removed from default**; irrelevant to wasm but breaks shared cross-platform manifests.

### Still true

- **`default-features = true` for WASM = 30 MB+ bundle.** Pass `default-features = false` and pick features explicitly.
- **`webgl2` and `webgpu` both exist in 0.20.1** (`bevy/webgl2` → `bevy_render/webgl` → `wgpu/webgl`; `bevy/webgpu` → `wgpu/webgpu`). Build both and let wgpu choose at runtime; with only `webgl2`, set `priority: WgpuSettingsPriority::WebGL2`.
- **Compute shaders need WebGPU.** WebGL2 has none; a compute-dependent renderer must require `webgpu` and the smaller browser pool.
- **Assets are served, not bundled.** `assets/` sits at the page URL root. Embedding needs a custom asset source (`embedded_asset!` or `AssetSourceBuilder`).
- **`wasm-pack` vs `wasm-bindgen` CLI.** For raw `<script type="module">` delivery `wasm-bindgen --target web` is leaner.
- **COOP/COEP headers** (`Cross-Origin-Opener-Policy: same-origin`, `Cross-Origin-Embedder-Policy: require-corp`) are required for `SharedArrayBuffer`; without them `multi_threaded` runs single-threaded in the browser.
- **No `std::time::Instant` in WASM.** Use `bevy::platform::time::Instant` (`bevy::time::Instant` no longer exists).
- **`println!` is a bare console line.** Use `info!`/`warn!` for structured devtools output.

## Scope

The render/window snippet above is target-agnostic and compile-checked natively. The wasm32 link, `wasm-bindgen` output and browser behaviour are not exercised by the tester crate.

## See also

- `bevy-cargo-features` — the 0.20 feature-implication table behind the manifest above.
- `bevy-assets` — asset loading rules, `http`/`https`/`web_asset_cache` sources.
- `bevy-migration-0-19-to-0-20` — WESL shader port.
