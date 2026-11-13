---
name: bevy-migration-0-19-to-0-20
description: Use when upgrading from Bevy 0.19 to Bevy 0.20, when `On<Add, T>` or `On<Pointer<Click>>` stops compiling (now `On<Add<T>>` and `On<PointerClick>`), when `ui::Interaction`/`ui::widgets::Button` warn as deprecated (use `ui_widgets::Button` + `Hovered` + `Pressed`), when a `.wgsl` shader with `#import`/`#ifdef` fails to load (WESL), when `iter_many` yields `Result`, when `NextState::set_if_neq` or `Tonemapping::None` behave differently, or when translucent materials stopped refracting (`ScreenSpaceTransmission` is opt-in). Index of every breaking Bevy 0.20 change.
license: MIT
compatibility: opencode,claude-code,cursor
metadata:
  tier: "1"
  area: migration
  bevy_version: "0.20"
  target_version: "Bevy 0.20"
---

# Bevy 0.19 → 0.20 — Migration cheat sheet

**Released 2026-10-08 (0.20.0); current patch 0.20.1.** Apply top-down. Coming from 0.18? Do
`bevy-migration-0-18-to-0-19` first.

## When to use this skill

- Compiler errors after a `bevy = "0.19"` → `bevy = "0.20"` bump.
- An LLM emits `On<Add, T>`, `Pointer<Click>`, `Interaction::Pressed`, `set_if_neq`, or naga_oil `#import` lines.
- Transparent or translucent scenes render differently after the bump.
- `IntoObserverSystem` errors mention "one too many generics".

## The breaks you'll hit first

```rust
use bevy::core_pipeline::tonemapping::Tonemapping;
use bevy::mesh::MeshTag;
use bevy::picking::hover::Hovered;
use bevy::prelude::*;
use bevy::ui::Pressed;
use bevy::ui_widgets::Button;

// 1. Lifecycle observers carry the bundle on the event, not on `On`.
fn on_player_added(add: On<Add<Player>>, mut commands: Commands) {
    commands.entity(add.entity).insert(Name::new(format!("player-{}", add.entity)));
}
// Dynamic components: `On<Add>` → `On<Add<()>>`.

// 2. Pointer events are flat. Fields moved onto `.pointer`.
fn on_click(click: On<PointerClick>) {
    info!("clicked {} at {:?}", click.entity, click.pointer.position);
}

// 3. `ui::Interaction` and `ui::widgets::Button` are deprecated. `Pressed` is a marker.
fn style_button(mut buttons: Query<(&Hovered, Has<Pressed>, &mut BackgroundColor), With<Button>>) {
    for (hovered, pressed, mut bg) in &mut buttons {
        bg.0 = match (pressed, hovered.get()) {
            (true, _) => Color::srgb(0.1, 0.1, 0.1),
            (false, true) => Color::srgb(0.3, 0.3, 0.3),
            _ => Color::srgb(0.2, 0.2, 0.2),
        };
    }
}

// 4. `iter_many` family yields `Result`; `.matched()` restores skip-missing behaviour.
fn visit(targets: Res<Targets>, names: Query<&Name>) {
    for name in names.iter_many(targets.0.iter()).matched() {
        info!("{name}");
    }
}

// 5. `set_if_neq` → `set_if_different` (old name is a deprecated wrapper).
fn go_play(mut next: ResMut<NextState<Phase>>) {
    next.set_if_different(Phase::Play);
}

// 6. `&mut World` is a normal `SystemParam`; it may sit anywhere in the signature.
fn world_anywhere(mut counter: Local<u32>, world: &mut World) {
    *counter += 1;
    world.spawn((Mesh3d::default(), MeshTag::new(7))); // MeshTag(7) → MeshTag::new(7)
}
```

`Player`, `Targets`, `Phase` are ordinary `Component`/`Resource`/`States` types.

## Rendering

```rust
// Camera3d no longer requires ScreenSpaceTransmission. Add it back for refraction.
commands.spawn((
    Camera3d::default(),
    bevy::pbr::ScreenSpaceTransmission::default(),
    Tonemapping::Linear, // "no tone curve" — `Tonemapping::None` is now a raw passthrough
));
```

- `Tonemapping::None` skips `ColorGrading`, `DebandDither`, and the negative clamp. Use `Linear` for the old "no curve" look. `Camera2d` now defaults to `Linear`.
- `Tonemapping` and `DebandDither` live in `bevy_render::view` (reflect paths changed; Rust imports still work).
- **WESL shaders.** naga_oil is gone. `.wgsl` + `#import`/`#ifdef`/`#define_import_path` → `.wesl` + `import bevy_pbr::render::forward_io::VertexOutput;` + `@if(DEF)`. Plain WGSL without preprocessor lines still loads. GLSL removed. `shader_format_wesl` feature removed. Module paths follow crate file paths (`bevy_pbr::mesh_view_bindings` → `bevy_pbr::render::mesh_view_bindings`). Full table: [references/wesl-shaders.md](references/wesl-shaders.md).
- `UnpreparedBindGroup` → `BindGroupBuilder`; `AsBindGroup::unprepared_bind_group` → `build_bind_group`. `#[derive(AsBindGroup)]` users: no change.
- Extraction is generic over worlds: `#[derive(ExtractComponent)] #[extract_app(RenderApp)]`, `impl SyncComponent<RenderApp>`; new `bevy_extract` crate.
- `Sprite` renders through `Mesh2d` + `SpriteMeshMaterial` and gained `alpha_mode`. Overlapping sprites at equal Z may reorder; give them explicit Z.
- OIT is per-material (`Material::enable_oit`, shader def `MATERIAL_OIT_ENABLED`); `oit_draw` wants premultiplied color.
- `MeshAabb::compute_aabb` → `get_aabb`. `WgpuWrapper` removed. `ViewDepthTexture` → `ViewDepthStencilTexture`. `AtmosphereBuffer` is a per-camera component. `RenderDebugOverlayPlugin` joins `DefaultPlugins` when the `bevy_dev_tools` + `render_dev_tools` features (the `dev` collection) are on; enable keys via `bevy::dev_tools::render_debug::RenderDebugOverlayKeybindings`.

## ECS and scheduling

- `On<E, B>` lost `B`; `IntoObserverSystem<E: EventPattern, M, Out>` has three generics. Custom bundle-generic events implement `EventPattern`.
- Exclusive systems unified: `ExclusiveSystemParam`, `ExclusiveFunctionSystem`, `System::is_exclusive`, `ExclusiveMarker` removed. Exclusivity is tracked at runtime via `SystemAccess`. `WorldId` in an exclusive system → `Local<WorldId>` or `world.id()`.
- Built-in schedules (`Render`, `RenderGraph`, `Core2d`/`Core3d`, `ExtractSchedule`, UI sets in `PostUpdate`) use `.chain_weak()`. Only tracked data conflicts are ordered. If you relied on a channel, atomic, or interior mutability across sets, add an explicit `.after(...)`.
- `FilteredResources*` deprecated → `QueryParamBuilder` + `Query<FilteredEntityRef>` with `.with::<IsResource>()`.
- `Name: From<&'static str>` only; use `Name::new(s.to_owned())` for runtime strings.
- `WorldQuery` manual impls must add empty `init_nested_access` and `update_archetypes`.
- `DeferredWorld::query` deprecated → `query_state.query_mut(&mut world)`. `ComponentInfo::id()` removed. `ComponentId` lifecycle constants are typed. `define_label!` takes no interner argument. `ScheduleBuildSettings.shuffle_seed` exists under the `debug` feature.
- `Access::reads_and_writes` → `reads`. `TypeIdMap` deprecated → `TypeIdHashMap` / `TypeIdIndexMap`.

## UI and text

- `TextFont::default().font_size` is `FontSize::Rem(1.)` (was `Px(20.)`); set `Px` explicitly for fixed sizes.
- `FontSource::SansSerif` etc → `FontSource::sans_serif()` / `GenericFontFamily`. `resolve_font_source` → `text_font.font.resolve_font_family(fonts)`. `Font::from_bytes` no longer takes a family name.
- New `Val::Em`/`Val::Rem` with `em()`/`rem()` helpers; `Node` requires `EmSize`; `Val::resolve` takes `em_size, rem_size`; `FontSize::eval` takes `RemSize`.
- `BorderRadius` is a `Node` field (`Node { border_radius: BorderRadius::all(CornerRadius::circular(px(8.))), .. }`), not a component. Its fields are `CornerRadius` (`.into()` from `Val` works); constructors are no longer `const`.
- `EditableText` + `TextInput` are separate components. `TextScroll` → `EditableText::viewport`. Escape blurs the field and now bubbles.
- `CalculatedClip` is an enum (`Rects` / `FullyClipped`). `TextReader::get` returns `TextLayoutItem`. `FocusCause::Auto` added. UI rendering is retained (`ExtractedUiNodes::changed`).
- Feathers: `cursor` module moved to `bevy_picking::cursor` (and the `custom_cursor` feature with it); `FeathersNumberInput` takes a `NumberInputValue` component; contextual theming reorganised `ThemeProps`.

## Assets, math, reflection, features

- `AssetId::invalid()` deprecated → `Option<AssetId>`. `UntypedHandle::meta_transform` removed. `AssetLoadError::RequestedHandleTypeMismatch` is boxed.
- `compressed_image_saver` now emits BCn/ASTC; old UASTC behaviour is `compressed_image_saver_universal`. JPEG joined the default processor list.
- `bevy_curve` and `bevy_shape` split from `bevy_math` (`bevy_math/curve` feature gone; enable `bevy/bevy_curve`). Prelude unchanged; direct `bevy_math::primitives::*` imports move to `bevy_shape`.
- `FromType<T>` → `CreateTypeData<T>`; `PartialReflect::to_dynamic` returns `Result`; `ReflectFromPtr::from_ptr*` → `raw_pointer_cast`; `as_reflect` → `ptr_as_reflect`.
- BSN: `@` prefix on scene references, `--` between entities, `template_value` gone. [references/bsn-syntax.md](references/bsn-syntax.md).
- `LinearRgba::with_luminance` no longer clamps. macOS activation follows `Window::focused`.

## Gotchas

- **Deprecated, not removed:** `Interaction`, `ui::widgets::Button`, `set_if_neq`, `FilteredResources`, `TypeIdMap`, `AssetId::invalid()`. Builds pass with warnings; fix them before 0.21.
- **Silent render change:** missing `ScreenSpaceTransmission` makes glass opaque-looking. No error.
- **Silent ordering change:** `chain_weak` only reorders systems with no tracked conflict. Bugs surface as flaky frames, not panics.
- **Shader errors at runtime:** a naga_oil `.wgsl` fails at asset load, not at `cargo check`. Rename to `.wesl` and convert directives.
- **rustc floor:** Bevy 0.20.1 requires rustc 1.97.1 (`wesl` crates).

## See also

- `bevy-migration-0-18-to-0-19` — the previous release's catalogue; apply it first.
- `bevy-ecs-components` — observers and lifecycle events in their 0.20 form.
- `bevy-ui` — `Button` + `Hovered` + `Pressed`, `FontSize::Rem`, `CornerRadius`.
- `bevy-pbr-materials` — WESL custom materials and `ScreenSpaceTransmission`.
- `bevy-cargo-features` — `bevy_curve`, `bevy_shape`, `compressed_image_saver*`, `custom_cursor`.
