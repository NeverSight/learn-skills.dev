---
name: bevy-migration-0-17-to-0-18
description: "Use when upgrading from Bevy 0.17 to Bevy 0.18, when an LLM writes `EventReader`/`EventWriter`/`Trigger<E>` instead of `MessageReader`/`MessageWriter`/`On<E>`, when `mesh.insert_attribute` fails to compile, when `AmbientLight` no longer works as a resource, or when `Camera { target: ... }` errors on the `target` field. Index of every breaking 0.17→0.18 change."
license: MIT
compatibility: opencode,claude-code,cursor
metadata:
  tier: "1"
  area: migration
  bevy_version: "0.18"
  target_version: "Bevy 0.18"
---

# Bevy 0.17 → 0.18 — Migration cheat sheet

**Released 2026-01-13.** Apply top-down — earlier items break later builds if skipped.

## When to use this skill

- Compiler errors after a `bevy = "0.17"` → `bevy = "0.18"` bump.
- LLM emits 0.17-era API names from training data.
- Auditing a PR for hidden 0.18-incompatible patterns.
- Hot-fixing a downstream crate that hasn't shipped 0.18 yet.

## The renames you'll hit first

### Observers: `Trigger<E>` → `On<E>`

```rust
// 0.18 (also 0.17)
fn on_hit(on: On<Damage>) { let _e = on.event(); }
```

### Buffered events: `Event` → `Message`

```rust
// 0.18
#[derive(Message)] struct Tick;
// app.add_message::<Tick>();
fn read(mut reader: MessageReader<Tick>) { for _ in reader.read() {} }
fn write(mut w: MessageWriter<Tick>) { w.write(Tick); }
```

`Event` is now reserved for observed, entity-targeted events (`#[derive(EntityEvent)]`).

### `Camera { target: ... }` → `RenderTarget` component

```rust
// 0.18
commands.spawn((Camera3d::default(), RenderTarget::Image(handle.into())));
```

### `AmbientLight` is no longer a resource

```rust
// 0.18: global default
app.insert_resource(GlobalAmbientLight { brightness: 2000.0, ..default() });
// Per-camera override:
commands.spawn((Camera3d::default(), AmbientLight { brightness: 5000.0, ..default() }));
```

### `MaterialPlugin<M>` config moved to trait methods

```rust
// 0.18
impl Material for M {
    fn enable_prepass() -> bool { false }
    fn enable_shadows() -> bool { false }
}
app.add_plugins(MaterialPlugin::<M>::default());
```

### `AsBindGroup::label()` is now required

```rust
impl AsBindGroup for MyMaterial {
    fn label() -> &'static str { "MyMaterial" }
}
```

### `AssetLoader` must `#[derive(TypePath)]`

```rust
#[derive(TypePath)]
struct MyLoader;
impl AssetLoader for MyLoader { /* ... */ }
```

### `Mesh::insert_attribute` is panicky — prefer `try_insert_attribute`

```rust
// 0.18 safe form — returns Result<(), MeshAccessError>
mesh.try_insert_attribute(Mesh::ATTRIBUTE_POSITION, positions)?;
```

### `State::set` always triggers a transition

```rust
// 0.18: always fires OnExit + OnEnter. Guard with:
next_state.set_if_neq(GameState::Playing);
```

### glTF coordinate conversion replaced

```rust
// 0.18
GltfPlugin {
    convert_coordinates: GltfConvertCoordinates {
        rotate_scene_entity: true,
        rotate_meshes: true,
    },
    ..default()
}
```

## Schedule executor

**`SimpleExecutor` was removed.** Add `.before()`, `.after()`, or `.chain()` when a
later system must observe commands from an earlier one in the same schedule. The
remaining executors use those dependencies to place `ApplyDeferred`; ambiguity
detection remains separately configurable. See
[references/schedule-renames.md](references/schedule-renames.md).

## Topics

| Topic | Reference |
|---|---|
| `On<E>`, `MessageReader`/`MessageWriter`, `Entity::index`, tick moves, `Resource 'static`, reflect syntax, hierarchy helpers | [references/ecs-renames.md](references/ecs-renames.md) |
| `RenderTarget` component, `GlobalAmbientLight`, `MaterialPlugin`, `AsBindGroup::label`, gizmos, `bevy_gizmos_render` split | [references/render-renames.md](references/render-renames.md) |
| `AssetLoader` + `TypePath`, `LoadContext::asset_path`, `asset_bytes` reader pattern, `AssetSource` channel, `try_insert_attribute` | [references/asset-renames.md](references/asset-renames.md) |
| `SimpleExecutor` removal, `ScheduleBuildError` variants, `State::set` always-fires, `or` combinator, glTF coordinates | [references/schedule-renames.md](references/schedule-renames.md) |
| `animation` → `gltf_animation`, picking-backend renames, `documentation` → `reflect_documentation`, input opt-in | [references/cargo-feature-renames.md](references/cargo-feature-renames.md) |

## Gotchas

- **`bevy_gizmos` was split.** Render-side code now lives in `bevy_gizmos_render`. Update import paths if you used internals.
- **`Resource` no longer allows non-`'static` lifetimes.** A `Resource` with a borrowed field will fail to compile.
- **Reflect attribute syntax tightened.** Only `#[reflect(...)]` (parens) is accepted; brace/bracket forms are rejected.
- **`AnimationTarget` split into two components.** Use `(AnimationTargetId(id), AnimatedBy(player))`.
- **`Atmosphere` now references a `Handle<ScatteringMedium>`** — what was a flat struct is now indirect.

## See also

- `bevy-migration-0-18-to-0-19` — the next release's rename catalogue.
- `bevy-core-concepts` — schedule executor change in detail.
- `bevy-cargo-features` — feature rename table.
- `bevy-ecs-systems` — `Message`/`MessageReader`/`MessageWriter` ergonomics.
