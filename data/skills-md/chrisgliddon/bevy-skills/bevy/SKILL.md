---
name: bevy
description: Use when starting any Bevy task, choosing between Update and FixedUpdate, picking Cargo feature flags, or recalling which sibling skill covers ECS, assets, rendering, UI, or migration. Routes to the right Bevy 0.20 skill and pins the engine version for downstream snippets.
license: MIT
compatibility: opencode,claude-code,cursor
metadata:
  tier: "1"
  area: router
  bevy_version: "0.20"
---

# Bevy 0.20 — Router

**Read this first when working on a Bevy project.** All sibling skills assume Bevy 0.20 (0.20.0 released 2026-10-08; current patch 0.20.1, requires rustc 1.97.1). If the user's `Cargo.toml` pins a different version, stop and confirm before applying patterns from this collection.

## Smallest valid app

```rust
use bevy::prelude::*;

fn main() {
    App::new()
        .add_plugins(DefaultPlugins)
        .add_systems(Startup, setup)
        .run();
}

fn setup(mut commands: Commands) {
    commands.spawn(Camera3d::default());
}
```

## When to use which skill

| Task | Skill |
|---|---|
| App / Plugin / Schedule basics, Update vs FixedUpdate, exclusive systems (`&mut World` anywhere in 0.20) | `bevy-core-concepts` |
| `#[derive(Component)]`, `#[require(...)]`, observers (`On<E>`, `On<Add<T>>`), hooks (`on_add`/`on_discard`), storage | `bevy-ecs-components` |
| `Query`, `With`/`Without`/`Or`, `Changed`/`Added`, `par_iter`, `iter_many(..).matched()`, query lenses | `bevy-ecs-queries` |
| `SystemParam`, `SystemSet`, `.run_if`, ordering, `.chain_weak()`, `remove_systems_in_set` | `bevy-ecs-systems` |
| `Cargo.toml` features: `2d`/`3d`/`ui`, `*_api`, `bevy_curve`, `compressed_image_saver*`, WASM trim | `bevy-cargo-features` |
| Upgrading from 0.19 — `On<Add<T>>`, `PointerClick`, `Hovered`/`Pressed`, WESL, `set_if_different` | `bevy-migration-0-19-to-0-20` |
| Upgrading from 0.18 — `FontSource`/`FontSize`, `bevy_world_serialization`, resources-as-components | `bevy-migration-0-18-to-0-19` |
| Upgrading from 0.17 — `MessageReader`, `On`, `RenderTarget`, `GlobalAmbientLight` | `bevy-migration-0-17-to-0-18` |
| `AssetServer`, `Handle<T>`, `load_builder`, hot-reload, `WorldAssetRoot` for glTF scenes | `bevy-assets` |
| Writing an `AssetLoader` (`Reader::seekable` is required) | `bevy-custom-assets` |
| WASM build pipeline, WebGPU vs WebGL2 | `bevy-wasm-webgpu` |
| `Camera3d`, `Projection`, `RenderTarget` component, `Tonemapping::Linear`, `ScreenSpaceTransmission`, `FreeCamera`, `PanCamera` | `bevy-cameras` |
| `StandardMaterial`, `MaterialPlugin<M>`, `AsBindGroup`, WESL custom shaders, lighting, atmosphere | `bevy-pbr-materials` |
| GPU particles (`bevy_hanabi`), Gaussian splats, flipbooks, custom VFX materials | `bevy-vfx` |
| `AnimationPlayer`, `AnimationGraph`, `AnimationTransitions`, `AnimationMask`, `AnimationEvent`, easing curves | `bevy-animation` |
| Recording a camera to MP4 or PNG sequences (`bevy_capture`) | `bevy-capture` |
| Voxel meshing with `block-mesh-rs`, chunk pipeline, greedy quads | `bevy-voxel-pipeline` |
| RON block definitions, palette, KTX2 atlas baking | `bevy-voxel-data` |
| Rebindable actions, entity `Gamepad`s, hot-plug, deadzones, Steam Deck, input into `FixedUpdate` | `bevy-input-actions` |
| `AudioPlayer`, `PlaybackSettings`, `AudioSink`, spatial listeners, mix groups, browser unlock | `bevy-audio` |
| Rapier bodies, colliders, fixed-step ordering, events, scene queries, joints, determinism | `bevy-physics` |
| Built-in vs external/headless rendering, forward vs deferred, render systems | `bevy-rendering` |
| `DiagnosticPath`, `DiagnosticsStore`, `info_span!`, `RenderDiagnosticsPlugin`, CPU/GPU timings | `bevy-diagnostics-profiling` |
| Stable IDs, versioned save DTOs, atomic native/browser writes, snapshots | `bevy-save-load` |
| Deterministic `App::update` stepping, `TimeUpdateStrategy`, `MessageCursor`, headless tests | `bevy-testing` |
| Screen readers, adaptive controllers, remapping, captions, contrast, motion safety | `bevy-a11y` |
| Voxel edit → remesh runtime: dirty/halo fan-out, revision tokens, bounded uploads | `bevy-voxel-runtime` |
| `es-fluent-manager-bevy` i18n — `FluentText<T>`, `BevyFluentText`, `LocaleChangeEvent`, `i18n.toml` | `bevy-fluent` |
| `Node`, `ui_widgets::Button` + `Hovered`/`Pressed`, `children![]`, `TextFont`/`FontSize`, `Val::Em`, `Node::border_radius`, `InputFocus` | `bevy-ui` |
| Porting from Unity, Unreal, Godot, Phaser, Flash, Defold, Roblox, GameMaker | `bevy-porting` |
| Detecting copy-paste / near-duplicate Rust code before committing (`similarity-rs --cross-file`) | `similarity-rs` |

## Cardinal rules (every Bevy 0.20 task)

1. **Events are messages.** `EventReader<E>` / `EventWriter<E>` became `MessageReader<M>` / `MessageWriter<M>` in 0.17. Observers use `On<E>`, never `Trigger<E>`.
2. **Lifecycle observers carry the bundle on the event.** `On<Add<Player>>`, not `On<Add, Player>` (changed in 0.20). `Replace` became `Discard` in 0.19.
3. **Pointer events are flat.** `On<PointerClick>`, `click.pointer.position`; not `On<Pointer<Click>>` (0.20).
4. **UI interaction is `Hovered` + `Pressed`.** `ui::Interaction` and `ui::widgets::Button` are deprecated in 0.20; spawn `ui_widgets::Button`.
5. **Text is `FontSource` + `FontSize`.** `TextFont { font: handle.into(), font_size: FontSize::Px(24.0) }` (0.19). Default size is `FontSize::Rem(1.)` (0.20).
6. **Shaders are WESL.** `.wesl`, `import a::b;`, `@if(DEF)`. naga_oil `#import` / `#ifdef` fail at asset load in 0.20.
7. **Resources are components** (0.19). `Res<T>` still works, but one type cannot be both `Component` and `Resource`.
8. **Scenes:** glTF spawns with `WorldAssetRoot` from `bevy_world_serialization`; `bevy_scene` is BSN (0.19).
9. **No `.unwrap()` in systems.** Use `let ... else { return };` or a real error path.
10. **Schedule order is explicit.** Ambiguities are ignored by default (`ScheduleBuildSettings::ambiguity_detection` is `LogLevel::Ignore`); opt into `LogLevel::Error` to catch them. Built-in sets use `.chain_weak()` in 0.20, so cross-set ordering through channels or atomics needs an explicit `.after()`.

## Gotchas

- Bevy's training-data footprint is dominated by 0.10–0.16 code. If a snippet feels obvious, check it against the three migration skills before trusting it.
- `bevy::prelude::*` doesn't re-export everything. `Hovered` is `bevy::picking::hover::Hovered`; `Pressed` is the marker `bevy::ui::Pressed` (query with `Has<Pressed>`); `Tonemapping` is `bevy::core_pipeline::tonemapping::Tonemapping`; `ScreenSpaceTransmission` is `bevy::pbr::ScreenSpaceTransmission`.
- The `bevy` crate re-exports many subcrates (`bevy_camera`, `bevy_light`, `bevy_material`, `bevy_extract`, `bevy_curve`, `bevy_shape`, `bevy_world_serialization`, `bevy_ui_widgets`, `bevy_feathers`). Subcrate APIs are stable points to depend on for plugins.
- Deprecations (`Interaction`, `set_if_neq`, `AssetId::invalid()`) compile with warnings in 0.20 and will be removed later. Fix them now.

## See also

- `bevy-migration-0-19-to-0-20` — the latest catalogue of renames and breaks.
- `bevy-cargo-features` — what to put in `Cargo.toml` before any of the above will compile the way you want.
