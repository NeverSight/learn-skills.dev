---
name: bevy-assets
description: Use when loading with `AssetServer::load` or `AssetServer::load_builder().with_settings(..)`, holding a `Handle<T>`, spawning a glTF scene with `WorldAssetRoot` (`Handle<WorldAsset>`), mutating through `Assets::get_mut` / `AssetMut`, polling `LoadState::is_loaded`, resolving an `AssetPath`, or replacing `AssetId::invalid()` with `Option<AssetId<T>>` in Bevy 0.20.
license: MIT
compatibility: opencode,claude-code,cursor
metadata:
  tier: "2"
  area: asset
  bevy_version: "0.20"
---

# Bevy 0.20 — Assets

## When to use this skill

- Loading a model, texture, audio file, or glTF scene.
- Reading the loaded data back from `Assets<T>` once it is ready.
- Reacting to load progress (`AssetEvent::Added` / `LoadedWithDependencies`).
- Loading with per-asset settings (sRGB off, sampler, untyped loads).
- Enabling hot-reload during development.
- Writing your own loader: see `bevy-custom-assets`.

## Canonical pattern

```rust
use bevy::asset::AssetPath;
use bevy::image::ImageLoaderSettings;
use bevy::prelude::*;

fn main() {
    App::new()
        .add_plugins(DefaultPlugins.set(AssetPlugin {
            // Hot-reload on file change. Dev-only; needs the `file_watcher` feature.
            watch_for_changes_override: Some(true),
            ..default()
        }))
        .init_resource::<MyHandles>()
        .add_systems(Startup, load_handles)
        .add_systems(Update, (react_to_loads, check_ready, tint_material))
        .run();
}

#[derive(Resource, Default)]
struct MyHandles {
    hero: Handle<WorldAsset>,
    bricks: Handle<Image>,
    normal_map: Handle<Image>,
    ground: Handle<StandardMaterial>,
}

fn load_handles(
    mut commands: Commands,
    asset_server: Res<AssetServer>,
    mut handles: ResMut<MyHandles>,
) {
    // glTF scenes are addressed by sub-asset label. 0.19+: `Scene` -> `WorldAsset`.
    handles.hero = asset_server.load("models/hero.glb#Scene0");
    commands.spawn(WorldAssetRoot(handles.hero.clone())); // was `SceneRoot` in 0.18

    handles.bricks = asset_server.load("textures/bricks.png");

    // 0.19+: advanced loads go through one builder. Replaces `load_with_settings`,
    // `load_acquire`, `load_untyped`, ... (deleted in 0.20).
    handles.normal_map = asset_server
        .load_builder()
        .with_settings(|s: &mut ImageLoaderSettings| s.is_srgb = false)
        .load("textures/bricks_normal.png");
}

fn react_to_loads(mut ev: MessageReader<AssetEvent<Image>>, images: Res<Assets<Image>>) {
    for event in ev.read() {
        if let AssetEvent::LoadedWithDependencies { id } = event {
            if let Some(img) = images.get(*id) {
                info!("image loaded: {}x{}", img.width(), img.height());
            }
        }
    }
}

fn check_ready(asset_server: Res<AssetServer>, handles: Res<MyHandles>) {
    // `LoadState` has no `PartialEq` (`Failed` carries an `Arc<AssetLoadError>`): use the predicates.
    if asset_server.load_state(&handles.hero).is_loaded() {
        // Safe to read Assets<WorldAsset> now.
    }
}

fn tint_material(handles: Res<MyHandles>, mut materials: ResMut<Assets<StandardMaterial>>) {
    // 0.19+: `get_mut` returns `AssetMut`, which emits `AssetEvent::Modified`
    // only on `DerefMut`. Compare first to avoid a GPU re-upload every frame.
    let Some(mut mat) = materials.get_mut(&handles.ground) else {
        return;
    };
    if mat.base_color != Color::WHITE {
        mat.base_color = Color::WHITE;
    }
}
```

## Asset paths

```rust
use bevy::asset::AssetPath;

let base = AssetPath::from("models/hero.glb");
let labeled = base.clone().with_label("Scene0");

// 0.19+: `resolve` / `resolve_embed` take `&AssetPath`; the `&str`
// forms are `resolve_str` / `resolve_embed_str` and return `Result`.
let sibling = base.resolve(&AssetPath::from("hero_lod1.glb"));
let sibling_str = base.resolve_str("hero_lod1.glb");

// 0.19+: `Option<&str>`, was `Option<String>`.
let ext: Option<&str> = labeled.get_full_extension();
```

## Nullable asset ids (0.20)

```rust
#[derive(Resource, Default)]
struct CurrentSkybox(Option<AssetId<Image>>); // 0.20: not `AssetId::invalid()`

fn read_skybox(current: Res<CurrentSkybox>, images: Res<Assets<Image>>) {
    let Some(id) = current.0 else { return };
    if let Some(img) = images.get(id) {
        // 0.19+: `pixel_bytes` returns `Result<_, TextureAccessError>`, was `Option`.
        let _ = img.pixel_bytes(UVec3::ZERO);
    }
}
```

## Gotchas

### 0.19 → 0.20

- **`AssetId::invalid()` and `AssetId::INVALID_UUID` are deprecated.** Store `Option<AssetId<T>>` and use `None`. `AssetId::default()` is *not* a null value; a real asset can own it.
- **Old `AssetServer` load variants are gone.** `load_with_settings`, `load_acquire`, `load_untyped`, `load_*_override` were deprecated in 0.19 and deleted in 0.20. Only `load` and `load_builder()` remain. Builder methods: `with_settings`, `with_guard`, `override_unapproved`, then `load` / `load_erased(type_id, path)` / `load_untyped`.
- **Boxed error variants.** `AssetLoadError::RequestedHandleTypeMismatch(Box<RequestedHandleTypeMismatchError>)` and `LoadDirectError::LoadError { error: Box<AssetLoadError>, .. }`. Exhaustive matches need `*`/`Box::new`.
- **`UntypedHandle::meta_transform()` is deleted.** There is no replacement.
- **Compressed texture processing.** Feature `compressed_image_saver` now means BCn/ASTC via `ctt`; the old Basis Universal path is `compressed_image_saver_universal` (use it for web). The default processor now compresses JPEG as well as PNG; restrict with `ImagePlugin { default_compressed_image_processor_extensions: ["png".into()].into(), .. }`.

### 0.18 → 0.19

- **`bevy_scene` is `bevy_world_serialization`.** `Scene` → `WorldAsset`, `SceneRoot` → `WorldAssetRoot`, `SceneInstanceReady` → `WorldInstanceReady`, `SceneSpawner` → `WorldInstanceSpawner`, `DynamicScene` → `DynamicWorld`. Paths: `bevy::world_serialization::*`; the prelude re-exports them. `bevy::scene` is now BSN. Cargo: the `scene` feature enables both.
- **`Assets::get_mut` returns `AssetMut`**, not `&mut A`. Bind it `mut`. `AssetEvent::Modified` fires only when you actually `DerefMut`; `get_mut_untracked` gives the old `&mut A`.
- **`AssetPath::resolve` / `resolve_embed` take `&AssetPath`.** String input: `resolve_str` / `resolve_embed_str` (fallible).
- **`AssetPath::get_full_extension` returns `Option<&str>`.** Add `.map(ToString::to_string)` if you stored it.
- **`Image::pixel_bytes` / `pixel_bytes_mut` / `pixel_data_offset` return `Result<_, TextureAccessError>`** (`OutOfBounds`, `UnsupportedTextureFormat`, `Uninitialized`).
- **`AssetSaver::save` takes `SavedAsset<'_, '_, A>` and an extra `asset_path: AssetPath<'_>`.**
- **`Resource` is now a `Component`.** `#[derive(Resource)]` still works for handle holders; see `bevy-ecs-components` for query conflicts.

### Still true since 0.18

- **Sub-asset labels.** `path.glb#Scene0`, `path.glb#Mesh0/Primitive0` are distinct handles. No label = the root asset.
- **`asset_server.load(...)` is non-blocking.** `Assets<T>::get` right after returns `None`. Wait for `LoadedWithDependencies` or poll `load_state(..).is_loaded()`.
- **`LoadState` is not `PartialEq`.** Stale snippets write `== LoadState::Loaded`; use `is_loaded()` / `is_failed()` or `matches!`.
- **Hot reload is dev-only** and needs the `file_watcher` Cargo feature; `watch_for_changes_override: Some(true)` polls the filesystem.
- **`AssetEvent<T>` is a `Message`**: `MessageReader<AssetEvent<T>>`, not `EventReader`.
- **`LoadContext::path()` returns `&AssetPath`**, not `&Path`; `.path()` again for the OS path.

## See also

- `bevy-custom-assets` — `AssetLoader`, `LoadContext::load_builder`, `Reader::seekable`.
- `bevy-cargo-features` — `file_watcher`, `compressed_image_saver*`, `scene`, `http`/`https` sources.
- `bevy-migration-0-19-to-0-20` and `bevy-migration-0-18-to-0-19` — full rename tables.
