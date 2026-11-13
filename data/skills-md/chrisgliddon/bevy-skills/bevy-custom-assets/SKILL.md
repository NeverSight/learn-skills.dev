---
name: bevy-custom-assets
description: Use when implementing `AssetLoader` for a custom format, deriving `TypePath` on the loader, loading dependencies through `LoadContext::load` or `LoadContext::load_builder().with_settings(..).load(..)`, marking handle fields `#[dependency]`, reading with `Reader::read_to_end`, seeking via `Reader::seekable` / `AsyncSeekExt`, or implementing the required `Reader::seekable` on your own reader in Bevy 0.20.
license: MIT
compatibility: opencode,claude-code,cursor
metadata:
  tier: "2"
  area: asset
  bevy_version: "0.20"
---

# Bevy 0.20 — Custom asset loaders

## When to use this skill

- Loading a custom binary or text format (game data, sidecar configs).
- Producing an asset that depends on other assets (a level that references textures).
- Loading a dependency with settings (`is_srgb = false`) or by erased type.
- Random access into the file (`reader.seekable()`), or writing your own `Reader`.
- Compiler errors: "`MyLoader: TypePath` is not implemented", "no method `loader`", "missing trait item `seekable`".

## Canonical pattern

```rust
use bevy::asset::io::Reader;
use bevy::asset::{Asset, AssetApp, AssetLoader, LoadContext};
use bevy::image::ImageLoaderSettings;
use bevy::prelude::*;
use bevy::reflect::TypePath;

#[derive(Asset, TypePath, Debug)]
pub struct LevelDef {
    pub name: String,
    pub gravity: f32,
    #[dependency] // counted toward `LoadedWithDependencies`
    pub thumbnail: Handle<Image>,
    #[dependency]
    pub normal_map: Handle<Image>,
}

#[derive(TypePath)] // required on the loader itself since 0.18
pub struct LevelLoader;

impl AssetLoader for LevelLoader {
    type Asset = LevelDef;
    type Settings = ();
    type Error = BevyError; // any `Error` converts via `?`

    async fn load(
        &self,
        reader: &mut dyn Reader,
        _settings: &Self::Settings,
        load_context: &mut LoadContext<'_>,
    ) -> Result<Self::Asset, Self::Error> {
        let mut bytes = Vec::new();
        reader.read_to_end(&mut bytes).await?;
        let text = String::from_utf8(bytes)?;

        let mut level = LevelDef {
            name: String::new(),
            gravity: 9.81,
            thumbnail: Handle::default(),
            normal_map: Handle::default(),
        };
        for line in text.lines() {
            let Some((key, value)) = line.split_once('=') else { continue };
            match key.trim() {
                "name" => level.name = value.trim().to_owned(),
                "gravity" => level.gravity = value.trim().parse()?,
                // Dependencies go through `LoadContext`, never `AssetServer`.
                "thumbnail" => level.thumbnail = load_context.load(value.trim().to_owned()),
                // 0.19+: settings, type erasure, untyped loads use `load_builder()`.
                "normal_map" => {
                    level.normal_map = load_context
                        .load_builder()
                        .with_settings(|s: &mut ImageLoaderSettings| s.is_srgb = false)
                        .load(value.trim().to_owned());
                }
                _ => {}
            }
        }
        Ok(level)
    }

    fn extensions(&self) -> &[&str] {
        &["level"]
    }
}

pub struct LevelLoaderPlugin;
impl Plugin for LevelLoaderPlugin {
    fn build(&self, app: &mut App) {
        app.init_asset::<LevelDef>()
            .register_asset_loader(LevelLoader);
    }
}
```

## Random access

```rust
use bevy::asset::io::{Reader, ReaderNotSeekableError};
use bevy::asset::AsyncSeekExt;

async fn read_footer(reader: &mut dyn Reader) -> std::io::Result<[u8; 8]> {
    let mut footer = [0u8; 8];
    match reader.seekable() {
        Ok(seekable) => {
            // `SeekableReader: Reader + AsyncSeek`; `AsyncSeekExt` is re-exported by bevy::asset.
            seekable.seek(std::io::SeekFrom::End(-8)).await?;
            let mut buf = Vec::new();
            seekable.read_to_end(&mut buf).await?;
            footer.copy_from_slice(&buf);
        }
        Err(ReaderNotSeekableError) => {
            // e.g. HTTP source: stream the whole file instead.
            let mut buf = Vec::new();
            reader.read_to_end(&mut buf).await?;
            footer.copy_from_slice(&buf[buf.len() - 8..]);
        }
    }
    Ok(footer)
}
```

## Implementing `Reader` yourself (0.19+ shape)

```rust
use bevy::asset::io::{Reader, ReaderNotSeekableError, SeekableReader};
use bevy::tasks::futures_lite::io::Cursor;
use bevy::tasks::futures_lite::{AsyncRead, AsyncSeek};
use std::pin::Pin;
use std::task::{Context, Poll};

pub struct MemReader(Cursor<Vec<u8>>);

impl AsyncRead for MemReader {
    fn poll_read(mut self: Pin<&mut Self>, cx: &mut Context<'_>, buf: &mut [u8])
        -> Poll<std::io::Result<usize>> {
        Pin::new(&mut self.0).poll_read(cx, buf)
    }
}

impl AsyncSeek for MemReader {
    fn poll_seek(mut self: Pin<&mut Self>, cx: &mut Context<'_>, pos: std::io::SeekFrom)
        -> Poll<std::io::Result<u64>> {
        Pin::new(&mut self.0).poll_seek(cx, pos)
    }
}

impl Reader for MemReader {
    // 0.19+: required. `AsyncSeekForward` is gone.
    fn seekable(&mut self) -> Result<&mut dyn SeekableReader, ReaderNotSeekableError> {
        Ok(self) // return `Err(ReaderNotSeekableError)` if you cannot seek
    }
}
```

## Gotchas

### 0.19 → 0.20

- **`LoadDirectError::LoadError { error }` is `Box<AssetLoadError>`** and `AssetLoadError::RequestedHandleTypeMismatch` wraps a `Box<RequestedHandleTypeMismatchError>`. Match through the box.
- **`NestedLoadBuilder` immediate loads** are `async`: `load_value(path).await`, `load_erased_value(type_id, path)`, `load_untyped_value(path)`, `load_value_from_reader(path, reader)`. They return `Result<LoadedAsset<A>, LoadDirectError>`.
- **`UntypedHandle::meta_transform()` is deleted.** Settings travel only through `with_settings` closures.

### 0.18 → 0.19

- **`LoadContext::loader()` is `load_builder()`** and `NestedLoader` is `NestedLoadBuilder`. Stale output: `ctx.loader().with_settings(..).load(p)`. Now: `ctx.load_builder().with_settings(..).load(p)`. `with_dynamic_type(id).load(p)` → `load_erased(id, p)`; `with_unknown_type().load(p)` → `load_untyped(p)`; `immediate().load(p)` → `load_value(p).await`.
- **`Reader` impls must implement `seekable`.** `AsyncSeekForward` is deleted; implement `AsyncSeek` (`poll_seek`) and return `Ok(self)`. Callers of the old trait use `AsyncSeekExt::seek(SeekFrom::Current(n))`.
- **`AssetSaver::save` gained a lifetime and a path:** `asset: SavedAsset<'_, '_, A>, settings: &S, asset_path: AssetPath<'_>`.
- **Resources are components.** A loader plugin that inserts a resource holding handles is fine; broad queries can now conflict with it (`bevy-ecs-components`).

### Still true since 0.18

- **`#[derive(TypePath)]` on the loader struct**, not only the asset. `AssetLoader: TypePath + Send + Sync + 'static`.
- **`LoadContext::asset_bytes()` is gone.** Use `reader.read_to_end(&mut bytes).await?` or `load_context.read_asset_bytes(path).await?` for a sibling file.
- **Dependencies must go through `LoadContext`.** `asset_server.load` inside a loader does not register the dependency, so `LoadedWithDependencies` fires early. Mark handle fields `#[dependency]` so `#[derive(Asset)]` visits them.
- **`type Error` only needs `Into<BevyError>`.** `BevyError` itself is the shortest choice; `thiserror` enums still work.
- **No Tokio inside `load`.** The executor is Bevy's; use `bevy::tasks::futures_lite` or `AsyncComputeTaskPool`.
- **`Settings` must be `Default + Serialize + DeserializeOwned`** to round-trip through `.meta` files.
- **Extensions match on the full suffix.** `"level.ron"` matches `foo.level.ron`, not `foo.ron`.
- **Do not import `AsyncReadExt` next to `dyn Reader`.** Both traits define `read_to_end`; the call becomes ambiguous. `Reader::read_to_end` is inherent to the trait.

## See also

- `bevy-assets` — using the `Handle<LevelDef>` once loaded, `load_builder` on `AssetServer`.
- `bevy-voxel-data` — RON-driven asset patterns.
- `bevy-migration-0-18-to-0-19` — `loader()` → `load_builder()`, `Reader::seekable`.
- `bevy-migration-0-19-to-0-20` — boxed error variants.
