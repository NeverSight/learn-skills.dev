---
name: bevy-fluent
description: Use when adding localization to a Bevy 0.20 app with `es-fluent-manager-bevy` 0.21, defining typed messages with `#[derive(EsFluent)]`, wrapping UI text in `FluentText<T>`, auto-registering locale updates with `#[derive(BevyFluentText)]`, or switching locales via `LocaleChangeMessage` / `LocaleChangedMessage`. Covers `I18nPlugin`, `RequestedLanguageId`, `ActiveLanguageId`, `i18n.toml` config, and hot-reload of `.ftl` assets.
license: MIT
compatibility: opencode,claude-code,cursor
metadata:
  tier: "2"
  area: i18n
  bevy_version: "0.20"
---

# Bevy 0.20 — Localization (es-fluent)

## When to use this skill

- Adding Fluent-based i18n to a Bevy app (`es-fluent-manager-bevy = "0.21"`, which depends on `bevy = "0.20.1"`).
- Defining typed UI messages with `#[derive(EsFluent)]` and `#[derive(BevyFluentText)]`.
- Wrapping a UI text entity with `FluentText<T>` for automatic locale-driven refresh.
- Switching locales at runtime via `LocaleChangeMessage`; confirming via `LocaleChangedMessage`.
- Reading the requested / active locale from `RequestedLanguageId` / `ActiveLanguageId`.

## Canonical pattern — 5-file minimum shape

`Cargo.toml`:

```toml
[dependencies]
bevy                   = "0.20"
es-fluent              = "0.21"   # `derive` is a default feature
es-fluent-manager-bevy = "0.21"   # `macros` + `file_watcher` are default features
unic-langid            = "0.9"
```

`i18n.toml` (crate root, read at compile time):

```toml
fallback_language = "en"
assets_dir = "assets/locales"
```

`src/i18n.rs`:

```rust
es_fluent_manager_bevy::define_i18n_module!();
```

`src/lib.rs` — **message types must live here** (see Gotchas):

```rust
use bevy::prelude::*;
use es_fluent::EsFluent;
use es_fluent_manager_bevy::{
    BevyFluentText, FluentText, I18nPlugin, LocaleChangeMessage, RequestedLanguageId,
};
use unic_langid::langid;

pub mod i18n;

#[derive(BevyFluentText, Clone, EsFluent)]
#[fluent(namespace = "ui")]
pub enum UiMessage { StartGame, Settings, QuitGame }

pub fn build_i18n_plugin() -> I18nPlugin {
    I18nPlugin::with_language(langid!("en"))
}

pub fn setup_ui(mut commands: Commands) {
    commands.spawn(Camera2d);
    // FluentText<T> writes translations into the sibling Text (and into child Text entities).
    commands.spawn((FluentText::new(UiMessage::StartGame), Text::new("")));
}

pub fn switch_locale_on_keypress(
    keys: Res<ButtonInput<KeyCode>>,
    requested: Res<RequestedLanguageId>,
    mut locale_messages: MessageWriter<LocaleChangeMessage>,
) {
    if keys.just_pressed(KeyCode::KeyL) {
        let next = if requested.0.to_string() == "en" { langid!("fr") } else { langid!("en") };
        locale_messages.write(LocaleChangeMessage(next));
    }
}
```

`src/main.rs` — thin binary entry point:

```rust
use bevy::prelude::*;
use my_game::{build_i18n_plugin, setup_ui, switch_locale_on_keypress};

fn main() {
    App::new()
        .add_plugins(DefaultPlugins)
        .add_plugins(build_i18n_plugin())
        .add_systems(Startup, setup_ui)
        .add_systems(Update, switch_locale_on_keypress)
        .run();
}
```

Replace `my_game` with your package name (hyphens become underscores). The full
walkthrough — lib-vs-binary rationale, package-name placeholder, pure-binary
workarounds — is in [references/lib-target-layout.md](references/lib-target-layout.md).

## Topics

| Topic | Reference |
|-------|-----------|
| Why types must live in the lib target; `cargo es-fluent generate` invisibility footgun; full layout | [references/lib-target-layout.md](references/lib-target-layout.md) |
| `BevyFluentText` derive vs `FluentText<T>` component; trait bounds; `Text::new("")` | [references/components.md](references/components.md) |
| `LocaleChangeMessage` (request) vs `LocaleChangedMessage` (confirmation); `RequestedLanguageId`; `ActiveLanguageId` | [references/locale-events.md](references/locale-events.md) |
| `i18n.toml` schema, `assets_dir`, `I18nPluginConfig` runtime override | [references/i18n-toml.md](references/i18n-toml.md) |
| `generate`, `watch`, `check`, `clean`, `sync`, `tree`, `fmt`, `status`, `doctor`, `add-locale` | [references/cli.md](references/cli.md) |
| rustc 1.99+ requirement; `rust-toolchain.toml` pin; failure modes on older toolchains | [references/toolchain.md](references/toolchain.md) |

## Gotchas

1. **Version matrix.** `es-fluent-manager-bevy 0.21.x` requires `bevy ^0.20.1` and **rustc 1.99**. `0.20.x` targets Bevy 0.19; `0.18.x` targets Bevy 0.18. Pin the crate line to your Bevy line. See [references/toolchain.md](references/toolchain.md).

2. **Message types were renamed in 0.21.** `LocaleChangeEvent` → `LocaleChangeMessage`, `LocaleChangedEvent` → `LocaleChangedMessage`. Both are Bevy `Message`s: use `MessageWriter` / `MessageReader`, never `EventWriter`. Stale 0.18-era snippets fail with "cannot find type `LocaleChangeEvent`". See [references/locale-events.md](references/locale-events.md).

3. **`cargo es-fluent generate` only sees the lib target.** Message enums declared only in `src/main.rs` are invisible to the CLI and produce empty `.ftl` output with no error. See [references/lib-target-layout.md](references/lib-target-layout.md).

4. **`T` no longer needs `Component` (0.21).** `FluentText<T: FluentMessage>` is the component; registration requires `T: FluentMessage + Send + Sync + 'static`. The 0.18 `ToFluentString + Clone + Component` bound is gone. Keeping `#[derive(Component)]` on `T` is harmless. See [references/components.md](references/components.md).

5. **Bevy-side text API changed underneath (0.19/0.20).** `FluentText` writes into `Text`; styling still comes from a sibling `TextFont { font: FontSource, font_size: FontSize::Px(..), .. }`. `font_size: 24.0` and `font: handle` without `.into()` do not compile. See `bevy-ui`.

6. **`BevyI18n` and `ActiveLanguageId` are exported in 0.21.** The 0.18 workaround of querying bundles directly is no longer needed; use the `BevyI18n` system param for imperative lookups.

## See also

- `bevy-ui` — `FluentText<T>` sits next to `Text`, `TextFont`, `Node`, and `ui_widgets::Button`.
- `bevy-migration-0-19-to-0-20` — Bevy-side changes you hit while bumping the crate pair.
- `bevy-ecs-components` — `#[derive(Component)]` patterns for custom text wrappers.
- `bevy-assets` — how `AssetServer` loads `.ftl` files; relevant for hot-reload (`file_watcher` feature).
