---
name: bevy-pbr-materials
description: Use when spawning `Mesh3d` with `StandardMaterial`, writing a custom `Material` with `AsBindGroup` and a `.wesl` shader, enabling `shadow_maps_enabled` / `contact_shadows_enabled` on lights, adding `ContactShadows` or `ScreenSpaceTransmission` to a `Camera3d`, spawning an `Atmosphere` entity, loading glTF `#Material0/std` sub-assets, or fixing `#import` / `#ifdef` shader errors after the WESL switch in Bevy 0.20.
license: MIT
compatibility: opencode,claude-code,cursor
metadata:
  tier: "2"
  area: render
  bevy_version: "0.20"
---

# Bevy 0.20 — PBR Materials

## When to use this skill

- Texturing a mesh with the built-in physically based shader.
- Writing a custom `Material` (stylised shading, dissolve, world-space effects).
- Compiler error: `no field shadows_enabled` on a light (renamed in 0.19).
- Shader error: `#import` or `#ifdef` not recognised (naga_oil is gone in 0.20).
- Translucent glass renders flat (screen-space transmission is opt-in in 0.20).
- `Handle<StandardMaterial>` from a glTF sub-asset fails to load (needs `/std` since 0.19).

## Canonical pattern — StandardMaterial

```rust
use bevy::pbr::ContactShadows;
use bevy::prelude::*;

fn main() {
    App::new()
        .add_plugins(DefaultPlugins)
        .add_systems(Startup, setup)
        .run();
}

fn setup(
    mut commands: Commands,
    mut meshes: ResMut<Assets<Mesh>>,
    mut materials: ResMut<Assets<StandardMaterial>>,
) {
    let mesh = meshes.add(Cuboid::new(1.0, 1.0, 1.0));
    let material = materials.add(StandardMaterial {
        base_color: Color::srgb(0.8, 0.3, 0.2),
        perceptual_roughness: 0.4,
        metallic: 0.1,
        ..default()
    });

    commands.spawn((
        Mesh3d(mesh),
        MeshMaterial3d(material),
        Transform::from_xyz(0.0, 0.5, 0.0),
    ));

    commands.spawn((
        Camera3d::default(),
        // Screen-space contact shadows (0.19+). Requires the depth prepass,
        // which `ContactShadows` adds as a required component.
        ContactShadows::default(),
        Transform::from_xyz(0.0, 2.0, 4.0).looking_at(Vec3::ZERO, Vec3::Y),
    ));

    commands.spawn((
        DirectionalLight {
            // 0.19 renamed `shadows_enabled` to `shadow_maps_enabled`.
            shadow_maps_enabled: true,
            contact_shadows_enabled: true,
            ..default()
        },
        Transform::from_xyz(2.0, 4.0, 2.0).looking_at(Vec3::ZERO, Vec3::Y),
    ));
}
```

## Custom Material — 0.20 shape

```rust
use bevy::prelude::*;
use bevy::render::render_resource::AsBindGroup;
use bevy::shader::ShaderRef;

#[derive(Asset, AsBindGroup, TypePath, Debug, Clone)]
struct TintMaterial {
    #[uniform(0)]
    tint: LinearRgba,
}

impl Material for TintMaterial {
    // 0.20: shaders are WESL. Use the `.wesl` extension for anything with imports.
    fn fragment_shader() -> ShaderRef {
        "shaders/tint.wesl".into()
    }
}
```

`assets/shaders/tint.wesl`:

```wesl
import bevy_pbr::render::forward_io::VertexOutput;

@group(2) @binding(0) var<uniform> tint: vec4<f32>;

@fragment
fn fragment(in: VertexOutput) -> @location(0) vec4<f32> {
    return tint;
}
```

Full `Material` trait reference, `AsBindGroup` attributes and WESL translation rules:
[references/custom-material.md](references/custom-material.md).

## Topics

| Topic | Reference |
|-------|-----------|
| `PointLight`, `DirectionalLight`, `SpotLight` fields; `GlobalAmbientLight`; cascades; `Atmosphere` entity | [references/lighting.md](references/lighting.md) |
| `Plane3d`, `Cuboid`, `Sphere`, `Circle`, `Cylinder`, `Capsule3d`, `Torus` constructors and orientation | [references/mesh-primitives.md](references/mesh-primitives.md) |
| `Material` trait methods, `AsBindGroup` attributes, `ShaderRef`, WESL syntax, `MaterialPlugin` | [references/custom-material.md](references/custom-material.md) |

## Gotchas

### 0.19 → 0.20

- **Shaders are WESL.** naga_oil is gone. `#import bevy_pbr::forward_io::VertexOutput` becomes `import bevy_pbr::render::forward_io::VertexOutput;` (semicolon, module path mirrors the crate file path). `#ifdef X ... #endif` becomes `@if(X)` on a declaration. `#{MATERIAL_BIND_GROUP}` becomes `constants::MATERIAL_BIND_GROUP`. `#define_import_path` is gone. Rename files `.wgsl` → `.wesl`; plain WGSL with no directives still loads. GLSL and the `shader_format_wesl` feature are gone.
- **`ScreenSpaceTransmission` is opt-in.** `Camera3d` no longer requires it. Add `bevy::pbr::ScreenSpaceTransmission::default()` to the camera or transmissive materials render without refraction.
- **`Tonemapping::None` is a pure passthrough** (no grading, no dither, no clamp). For "no tone curve, keep the rest" use `Tonemapping::Linear`.
- **Hand-rolled `AsBindGroup`:** `unprepared_bind_group` is now `build_bind_group` writing into a `BindGroupBuilder`. `#[derive(AsBindGroup)]` users are unaffected.
- **OIT is per-material.** Override `Material::enable_oit()`; the shader def is `MATERIAL_OIT_ENABLED`.
- **`bevy_shape` split from `bevy_math`.** `Cuboid`, `Sphere`, etc. still come through `bevy::prelude::*`; direct paths are `bevy::shape::*`.

### 0.18 → 0.19

- **`shadows_enabled` → `shadow_maps_enabled`** on `PointLight`, `DirectionalLight`, `SpotLight`. New `contact_shadows_enabled` field plus the `ContactShadows` camera component.
- **`Atmosphere` is an entity, in `bevy::light`.** Spawn `Atmosphere::earth(medium)` on its own entity; the camera keeps `AtmosphereSettings`. `scene_units_to_m` is gone (scale the entity's `Transform`). `Atmosphere::earthlike` → `Atmosphere::earth`.
- **glTF materials:** `#Material0` now loads a `GltfMaterial`. Append `/std` for a `Handle<StandardMaterial>`.
- **`Skybox.image` is `Option<Handle<Image>>`** and `Skybox` lives in `bevy::light`.
- **`AlphaMode` moved to `bevy_material`** (prelude still exports it).
- **Bloom luma is linear.** Scenes look dimmer; raise `Bloom::intensity` or emissive strength.
- **Render graph nodes are systems.** `ViewNode` / `add_render_graph_node` are gone; write a system with `ViewQuery` in `Core3d`.

### Still true

- Use `Mesh3d(handle)` and `MeshMaterial3d(handle)` — the renderer queries the wrappers.
- `Plane3d::new` takes `Vec2` for `half_size`. `Color::rgb` is gone; use `Color::srgb`.
- Directional light position is ignored; only rotation matters.
- `MaterialPlugin::<M>` has no `prepass_enabled` / `shadows_enabled` fields; override `Material::enable_prepass()` / `enable_shadows()`.

## See also

- `bevy-cameras` — `Camera3d`, `Hdr`, `Tonemapping`, render targets.
- `bevy-vfx` — custom-material shader effects and GPU particles.
- `bevy-migration-0-19-to-0-20` — WESL translation and `ScreenSpaceTransmission`.
- `bevy-migration-0-18-to-0-19` — light field renames, `Atmosphere` entity, render systems.
