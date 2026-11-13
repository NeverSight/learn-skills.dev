---
name: bevy-cameras
description: Use when spawning `Camera3d` or `Camera2d`, choosing a `Projection`, rendering to an image with the `RenderTarget` component, adding `Hdr` / `Tonemapping::Linear` / `ScreenSpaceTransmission` to a camera, wiring `FreeCamera`, `PanCamera` or the new `PanOrbitCamera` from `bevy::camera_controller`, ordering views with `Camera::order`, or setting a per-camera `AmbientLight` in Bevy 0.20.
license: MIT
compatibility: opencode,claude-code,cursor
metadata:
  tier: "2"
  area: render
  bevy_version: "0.20"
---

# Bevy 0.20 — Cameras

## When to use this skill

- Spawning the main game camera.
- Rendering to a texture (mini-map, portal, post-process target).
- Wanting a drop-in free-look, pan, or CAD-style orbit controller.
- Configuring multiple cameras with different `order` for overlays.
- Glass/translucent materials render flat (0.20 made `ScreenSpaceTransmission` opt-in).
- `Tonemapping::None` suddenly looks different (0.20 made it a pure passthrough).

## Canonical pattern

Controllers are feature-gated. In `Cargo.toml`:

```toml
bevy = { version = "0.20", features = ["free_camera", "pan_camera", "pan_orbit_camera"] }
```

```rust
use bevy::asset::RenderAssetUsages;
use bevy::camera::{Hdr, RenderTarget};
use bevy::camera_controller::free_camera::{FreeCamera, FreeCameraPlugin};
use bevy::core_pipeline::tonemapping::Tonemapping;
use bevy::prelude::*;
use bevy::render::render_resource::{Extent3d, TextureDimension, TextureFormat, TextureUsages};

fn main() {
    App::new()
        .add_plugins(DefaultPlugins)
        .add_plugins(FreeCameraPlugin) // adds the input wiring
        .add_systems(Startup, setup)
        .run();
}

fn setup(mut commands: Commands, mut images: ResMut<Assets<Image>>) {
    // 1. Main camera with the built-in free-look controller.
    commands.spawn((
        Camera3d::default(),
        Hdr,                  // `bevy::camera::Hdr` since 0.19
        Tonemapping::default(), // TonyMcMapface; `Linear` = no curve, keep grading
        FreeCamera::default(),
        Transform::from_xyz(0.0, 4.0, 8.0).looking_at(Vec3::ZERO, Vec3::Y),
    ));

    // 2. A texture target for an off-screen render pass (mini-map, portal).
    let size = Extent3d { width: 512, height: 512, depth_or_array_layers: 1 };
    let mut image = Image::new_fill(
        size,
        TextureDimension::D2,
        &[0; 4],
        TextureFormat::Bgra8UnormSrgb,
        RenderAssetUsages::default(),
    );
    image.texture_descriptor.usage = TextureUsages::TEXTURE_BINDING
        | TextureUsages::COPY_DST
        | TextureUsages::RENDER_ATTACHMENT;
    let image_handle = images.add(image);

    // 3. A second camera that draws into the texture.
    //    `RenderTarget` is a separate component, not a `Camera` field.
    commands.spawn((
        Camera3d::default(),
        Camera { order: -1, ..default() }, // lower order renders first
        RenderTarget::Image(image_handle.into()),
        Transform::from_xyz(10.0, 5.0, 0.0).looking_at(Vec3::ZERO, Vec3::Y),
    ));
}
```

## Choosing a projection

```rust
use bevy::prelude::*;

fn _proj(mut commands: Commands) {
    // Default perspective.
    commands.spawn((Camera3d::default(), Projection::default()));

    // Orthographic for top-down or strategy views.
    commands.spawn((
        Camera3d::default(),
        Projection::Orthographic(OrthographicProjection {
            scale: 10.0,
            ..OrthographicProjection::default_3d()
        }),
    ));
}
```

## Pan-orbit camera (new in 0.20)

`bevy_editor_cam` was upstreamed as `PanOrbitCamera`. It needs picking for depth-aware
zoom, so add `MeshPickingPlugin` too.

```rust
use bevy::camera_controller::pan_orbit_camera::{DefaultPanOrbitCameraPlugins, PanOrbitCamera};
use bevy::prelude::*;

fn _orbit(app: &mut App, mut commands: Commands) {
    app.add_plugins((MeshPickingPlugin, DefaultPanOrbitCameraPlugins));
    commands.spawn((Camera3d::default(), PanOrbitCamera::default()));
}
```

## Ambient light: world default vs per-camera

```rust
use bevy::light::GlobalAmbientLight;
use bevy::prelude::*;

fn _amb(app: &mut App, mut commands: Commands) {
    // World default — applies everywhere unless a camera overrides.
    app.insert_resource(GlobalAmbientLight { brightness: 200.0, ..default() });

    // Per-camera override — `AmbientLight` is a Component.
    commands.spawn((Camera3d::default(), AmbientLight { brightness: 1000.0, ..default() }));
}
```

## Gotchas

### 0.19 → 0.20

- **`ScreenSpaceTransmission` is opt-in.** `Camera3d` no longer requires it. Add `bevy::pbr::ScreenSpaceTransmission::default()` to get refraction through transmissive `StandardMaterial`s.
- **`Tonemapping::None` is a full passthrough.** No `ColorGrading`, no `DebandDither`, no clamp. Use the new `Tonemapping::Linear` for "no tone curve but keep the rest". `Camera2d` now defaults to `Tonemapping::Linear`.
- **`Tonemapping` / `DebandDither` moved to `bevy_render::view`.** The `bevy::core_pipeline::tonemapping::Tonemapping` import still works via re-export; reflected type paths in scene files changed.
- **Mixed-`Hdr` camera stacks composite instead of overwrite.** Set `blend_state` in `CameraOutputMode::Write` for the old replace behaviour. `SortedCamera::hdr` is gone.
- **`RenderDebugOverlay` keybindings.** `RenderDebugOverlayPlugin` joins `DefaultPlugins` (disabled by default) only with the `bevy_dev_tools` + `render_dev_tools` features.

### 0.18 → 0.19

- **`Hdr` moved to `bevy::camera::Hdr`** and is not extracted to the render world; read `ExtractedCamera::hdr` there.
- **`Camera3d::screen_space_specular_transmission_*` fields are gone.** They became `ScreenSpaceTransmission { steps, quality }` in `bevy_pbr`.
- **`Skybox` moved to `bevy::light`** and `image` is `Option<Handle<Image>>`.
- **`Atmosphere` is an entity**, not a camera component. The camera keeps `AtmosphereSettings`.
- **`PanCamera` pans with the mouse by default.** Set `mouse_pan_settings.enabled = false` for keyboard-only.
- **`ExtractedView::hdr` moved to `ExtractedCamera::hdr`**; `TextureFormat::bevy_default()` is deprecated — read `ExtractedView::target_format`.
- **`ViewTarget::out_texture()` returns `Option`** (`None` when the surface is occluded or `CameraOutputMode::Skip`).
- **Render graph nodes are systems** in the `Core3d` / `Core2d` schedules; `RenderSystems::ManageViews` split into `CreateViews`, `Specialize`, `PrepareViews`.

### Still true

- `RenderTarget` is its own component; `Camera { target: ... }` does not exist. `RenderTarget::None` renders prepasses only.
- `AmbientLight` is a component; the resource is `GlobalAmbientLight`.
- `Camera::order` is signed. Lower renders first.
- Controllers need their Cargo feature **and** plugin: `free_camera` + `FreeCameraPlugin`, `pan_camera` + `PanCameraPlugin`, `pan_orbit_camera` + `DefaultPanOrbitCameraPlugins`.
- Imports: `bevy::camera::{RenderTarget, Hdr}`, `bevy::camera_controller::{free_camera, pan_camera, pan_orbit_camera}`, `bevy::light::GlobalAmbientLight`. None are in the prelude.

## See also

- `bevy-pbr-materials` — materials, lights, `ContactShadows`, atmosphere.
- `bevy-capture` — recording a camera's `RenderTarget::Image` to video.
- `bevy-migration-0-19-to-0-20` — `Tonemapping::Linear`, opt-in transmission.
- `bevy-migration-0-18-to-0-19` — `Hdr`/`Skybox`/`Atmosphere` moves.
