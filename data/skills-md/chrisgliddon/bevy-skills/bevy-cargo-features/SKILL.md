---
name: bevy-cargo-features
description: Use when picking Bevy 0.20 Cargo features — top-level `2d`/`3d`/`ui`/`audio`, mid-level `3d_api`/`3d_bevy_render`/`ui_api`/`common_api`, headless `default_app`, input opt-ins `mouse`/`keyboard`/`gamepad`, `bevy_curve` (was `bevy_math/curve`), `compressed_image_saver_universal`, `render_dev_tools`, or debugging missing UI/audio/window after `default-features = false`.
license: MIT
compatibility: opencode,claude-code,cursor
metadata:
  tier: "1"
  area: cargo
  bevy_version: "0.20"
---

# Bevy 0.20 — Cargo features

## When to use this skill

- Authoring or auditing a Bevy project's `Cargo.toml`.
- Trimming the WASM bundle (the single biggest lever).
- Building a headless server (no rendering, no windowing, no audio).
- Writing a custom renderer that needs Bevy's data types but not its render pipeline.
- Migrating a 0.18 or 0.19 manifest: `ui`, `audio`, `bevy_window` and `custom_cursor` moved collections.

## Canonical patterns

### Top-level collections (what `default` is made of)

```toml
# default = ["2d", "3d", "ui", "audio"]
[dependencies]
bevy = { version = "0.20", default-features = false, features = ["3d", "ui", "audio"] }
# 3D, no bevy_ui (bring your own UI):
bevy = { version = "0.20", default-features = false, features = ["3d", "audio"] }
# 2D, no bevy_audio (e.g. bevy_seedling):
bevy = { version = "0.20", default-features = false, features = ["2d", "ui"] }
```

`2d`, `3d` and `ui` each imply `default_app` + `default_platform` + their `*_bevy_render` stack + `scene` + `picking`. Since 0.19 they imply **neither `ui` nor `audio`**; list those explicitly.

### Mid-level: API without the default renderer

```toml
bevy = { version = "0.20", default-features = false, features = ["3d_api", "bevy_winit", "x11"] }
```

| Collection | Adds | Use for |
|---|---|---|
| `common_api` | animation, camera, color, `bevy_curve`, gizmos, image, mesh, shader, material, text, `bevy_window`, hdr, png | base of every `*_api` |
| `2d_api` / `3d_api` | `common_api` + sprite, or + light, mikktspace, ktx2, morph, luts, zstd | custom renderer |
| `ui_api` | `default_app` + `common_api` + `bevy_ui` + `bevy_input_focus` | custom UI renderer |
| `2d_bevy_render` / `3d_bevy_render` / `ui_bevy_render` | `*_api` + `bevy_render` + core pipeline + the stock renderers (`3d` also glTF, PBR, anti-alias, `gltf_animation`) | stock renderer, no `default_platform` |
| `default_app` | `async_executor`, `bevy_asset`, `bevy_log`, `bevy_state`, `reflect_auto_register` | headless |
| `default_platform` | `std`, `bevy_winit`, `bevy_gilrs`, `bevy_clipboard`, `default_font`, `multi_threaded`, `webgl2`, `x11`, `wayland`, `custom_cursor`, `sysinfo_plugin` | desktop windowing |
| `scene` | `bevy_scene` (BSN) + `bevy_world_serialization` (glTF spawning, `WorldAssetRoot`) | any glTF scene |
| `picking` | `bevy_picking` + `mesh_picking` + `sprite_picking` + `ui_picking` | pointer events |

Table derived from `bevy-0.20.1/Cargo.toml`.

### Headless server

```toml
bevy = { version = "0.20", default-features = false, features = [
    "default_app",   # ECS + assets + state + log, no window
    "multi_threaded",
    "serialize",
    "scene",         # only if you spawn glTF / serialize worlds
] }
```

```rust
use bevy::prelude::*;

fn main() {
    // Headless: pair `default-features = false` + "default_app" with
    // `MinimalPlugins`, not `DefaultPlugins` (which needs the render features).
    App::new()
        .add_plugins(MinimalPlugins)
        .add_systems(Update, tick)
        .run();
}

fn tick(time: Res<Time>) {
    let _ = time.delta_secs();
}
```

### Minimal client, opt-in input

```toml
bevy = { version = "0.20", default-features = false, features = [
    "3d_bevy_render", "bevy_winit", "x11",   # or "wayland"; "webgl2"/"webgpu" on web
    "mouse", "keyboard", "gamepad",          # input is opt-in without default_platform
    # "touch", "gestures", "bevy_gilrs" (= gamepad + gilrs backend)
] }
```

### Dev-only extras

```toml
[features]
dev = ["bevy/dev"]   # = debug + bevy_dev_tools + render_dev_tools + file_watcher
```

`render_dev_tools` compiles `RenderDebugOverlayPlugin` into `DefaultPlugins` (disabled until you insert `RenderDebugOverlayKeybindings { enable_keybindings: true, .. }`). Without the feature the overlay is absent; stock `DefaultPlugins` do not include it.

## Feature moves since 0.18

| 0.18 | 0.19 | 0.20 |
|---|---|---|
| `3d`/`2d`/`ui` imply `audio` | `audio` separate, in `default` | same |
| `3d`/`2d` imply `ui` | `ui` separate, in `default` | same |
| `bevy_window` in `default_app` | in `common_api` | same |
| `bevy_input_focus` in `default_app` | in `ui_api` | same |
| `custom_cursor` in `default_app` | in `default_platform` | same; also forwards to `bevy_picking/custom_cursor` (cursor module moved from feathers to picking) |
| `bevy_picking` implied `bevy_input_focus` | no; `ui_picking` does | same |
| `experimental_bevy_feathers` / `experimental_bevy_ui_widgets` | `bevy_feathers` / `bevy_ui_widgets` (`ui` includes widgets) | same |
| `android-game-activity` in default | neither Android activity feature is default; add one | same |
| `bevy_math/curve` (default) | same | gone: enable `bevy/bevy_curve` (in `common_api`) |
| `shader_format_wesl`, `shader_format_glsl` | present | removed: WESL always on, GLSL gone; `shader_format_spirv` stays |
| `compressed_image_saver` = Basis Universal | same | = BCn/ASTC via `ctt`; old behaviour is `compressed_image_saver_universal` |
| — | — | `bevy_shape` is a non-optional dep (no feature); its `serialize` rides on `bevy/serialize` |
| `bevy_transform/bevy_log` | removed; tracing under `trace` | same |
| audio: `vorbis` default; `wav`, `mp3`, `mp4`, `flac`, `aac`, `audio-all-formats` | since 0.19 (rodio 0.22) | same |

## Gotchas

- **`default-features = false` + `3d` drops UI and audio.** Stale 0.18 manifests then hit "no `Node`/`AudioPlayer`". Add `ui` and/or `audio`.
- **`default_app` has no window types.** `Window`, `WindowPlugin` need `bevy_window` (`common_api` or explicit).
- **`bevy_picking` without `ui_picking` gives no UI focus-on-click.** Add `ui` or `ui_picking`.
- **`bevy_math/curve` no longer exists.** `cargo` fails with "feature `curve` not found"; use `bevy/bevy_curve`.
- **`shader_format_wesl`/`shader_format_glsl` fail to resolve** in 0.20. Delete them; port GLSL to WESL.
- **Web texture compression:** use `compressed_image_saver_universal`; the new `compressed_image_saver` output is BCn (desktop) or ASTC (`BEVY_COMPRESSED_IMAGE_SAVER_ASTC=4x4`), not one-file-everywhere.
- **`multi_threaded` implies `std`.** `no_std` targets use `default_no_std`.
- **`trace_tracy` / `trace_chrome`** are separate log sinks; enable one.
- **Asset sources:** `file_watcher` (hot reload), `embedded_watcher`, `http`/`https` (`ureq`), `web_asset_cache`, `asset_processor` are all opt-in.

## See also

- `bevy-wasm-webgpu` — the trimmed WASM manifest and `webgl2`/`webgpu`.
- `bevy-assets` — `file_watcher`, `scene`, `compressed_image_saver*` at runtime.
- `bevy-migration-0-18-to-0-19` and `bevy-migration-0-19-to-0-20` — the upstream feature-move notes.
