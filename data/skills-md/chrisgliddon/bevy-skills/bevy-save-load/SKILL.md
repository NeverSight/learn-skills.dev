---
name: bevy-save-load
description: "Use when designing Bevy 0.20 persistence with `DynamicWorldBuilder`, `DynamicWorld::serialize`, `WorldAssetRoot`, `IoTaskPool`, or `SettingsPlugin`: stable IDs, versioned save DTOs/migrations, checksums and atomic writes, snapshots plus sparse deltas, native/browser storage, and safe ECS serialization boundaries."
license: MIT
compatibility: opencode,claude-code,cursor
metadata:
  tier: "2"
  area: persistence
  bevy_version: "0.20"
---

# Bevy 0.20 — save and load

## When to use this skill

- Gameplay state must remain loadable across ECS/content/code refactors.
- Large worlds need base snapshots, sparse deltas, compaction, and recovery.
- Native and browser builds need one asynchronous save-service contract.
- Reflected world serialization is being considered as a durable save format.

A save file is a long-lived product API. Serialize an explicit, versioned data model
and convert it to/from the live ECS. Runtime `Entity` values, dense palette indices,
query order, Rust enum discriminants, and reflected component layout are not stable
persistence identities.

## Canonical pattern

```rust
use serde::{Deserialize, Serialize};

#[derive(Clone, Debug, Deserialize, Eq, Hash, PartialEq, Serialize)]
#[serde(transparent)]
struct SaveId(String);

#[derive(Debug, Deserialize, Serialize)]
struct SaveV3 {
    world_seed: u64,
    player: SaveId,
    actors: Vec<ActorV3>,
}

#[derive(Debug, Deserialize, Serialize)]
struct ActorV3 {
    id: SaveId,
    archetype: String,
    position: [f32; 3],
}
```

```text
live Bevy World
  -> validate/capture one logical revision
  -> current Save DTO with stable IDs
  -> encode + checksum envelope
  -> platform storage transaction

platform bytes
  -> size/magic/checksum validation
  -> decode declared old DTO
  -> migrate one version at a time
  -> validate current DTO
  -> allocate entities, then resolve stable-ID references
  -> rebuild derived/runtime-only state
```

Never partially mutate the active world while bytes are still being decoded or
migrated. Load into staging, validate, then commit or replace the gameplay world.

## Version the envelope and payload

Wrap encoded payload bytes with magic, format version, schema/content version,
payload length, codec/compression identifiers, and checksum. A checksum detects
accidental corruption; it does not prevent malicious tampering. Use authentication
or a signature when trust is part of the requirement.

Keep migrations as explicit `V1 -> V2 -> V3` pure functions. Test golden fixtures
from every supported version, including corrupt, truncated, duplicated-ID, unknown-ID,
and future-version files. Never deserialize an old version directly into today's
struct and hope Serde defaults reproduce old semantics.

## Stable IDs and two-pass load

Use immutable domain IDs for saved objects, content, quests, items, and voxel block
types. During load:

1. validate ID uniqueness and all size/count limits;
2. spawn/allocate objects and build `SaveId -> Entity` or stable-ID -> dense-palette
   maps;
3. resolve relationships in a second pass;
4. reject or explicitly preserve unknown content according to policy;
5. rebuild caches, handles, physics state, tasks, diagnostics, and presentation.

## Storage is platform-specific

Native writes should use a temporary file in the destination directory, flush and
sync it as required, then atomically replace/rename the committed slot. Retain a
validated backup or two-slot generation when recovery matters. Do blocking file I/O
on `IoTaskPool`, poll the `Task` with `block_on(poll_once(..))`, and send the result
back to the main world.

Browsers have no ordinary save-file path. Use IndexedDB for game saves and blobs;
small preferences may use local storage. Handle asynchronous completion, quota,
eviction, private modes, tab races, export/import, and page termination. A "save
complete" UI state requires committed storage confirmation.

`SettingsPlugin` (cargo feature `bevy_settings`, off by default) targets user settings
with native/local-storage backends; it is not a general campaign/world save schema.

## Gotchas

- **World serialization boundary.** `DynamicWorldBuilder` extracts reflected entities
  and resources with allow/deny filters. Good for authored world assets, editor
  tooling, controlled snapshots, and short-lived internal formats. It does not create
  stable gameplay IDs, schema migrations, corruption recovery, transactional storage,
  or compatibility across component refactors. Use an explicit DTO for durable player
  saves; if a filtered `DynamicWorld` is nested inside, version and migrate the
  surrounding contract and audit every reflected type.
- **`DynamicScene`/`SceneRoot` are gone (0.19).** Stale output spawns
  `SceneRoot(handle)` or builds `DynamicSceneBuilder`; 0.20 is `WorldAssetRoot`,
  `DynamicWorldRoot`, and `DynamicWorldBuilder::from_world(&world, &registry)`.
- **The builder takes a `&TypeRegistry` (0.19+).** Clone `AppTypeRegistry` out of the
  world and `.read()` it before borrowing the world for extraction.
- **`PartialReflect::to_dynamic` returns `Result` (0.20)**, and `FromType` became
  `CreateTypeData`. Custom reflect-driven converters must handle both.
- **`DynamicEnum::from` is deprecated (0.20)**; use `try_from`. `AssetId::invalid()`
  is deprecated too, so never persist an asset ID sentinel.
- **`Name` is `From<&'static str>` only (0.20).** Rebuild names on load with
  `Name::new(saved.to_owned())`.
- **`Resource` implies `Component` (0.19).** Reflected resources in a `DynamicWorld`
  are not entities; keep resource and component allowlists separate.

## Choose the relevant deep dive

| Problem | Read |
|---|---|
| DTO versions, migrations, stable IDs, validation and golden fixtures | [Schema, migrations, and IDs](references/schema-migrations-and-ids.md) |
| Atomic native writes, browser storage, async state and recovery | [Native and browser I/O](references/native-and-browser-io.md) |
| Full snapshots, sparse deltas, compaction, `DynamicWorldBuilder` snippet | [Snapshots, deltas, and world serialization](references/snapshots-deltas-and-world-serialization.md) |

## Review checklist

- Save schema types are separate from live ECS/runtime components.
- Every persistent reference uses a documented stable ID.
- Old versions migrate sequentially and have committed fixtures.
- Decoder limits untrusted lengths/counts before allocation/decompression.
- Native power-loss and browser quota/termination failures leave a recoverable slot.
- Success is reported only after the platform commit completes.
- Snapshot/delta generations cannot be mixed accidentally.
- Unknown future versions fail safely without overwriting the original.

## See also

- [`bevy-voxel-data`](../bevy-voxel-data/SKILL.md) — stable block IDs versus dense runtime palettes.
- [`bevy-testing`](../bevy-testing/SKILL.md) — deterministic migration and failure-path tests.
- [`bevy-assets`](../bevy-assets/SKILL.md) — stable asset paths/labels and `WorldAsset` readiness.
- [`bevy-migration-0-19-to-0-20`](../bevy-migration-0-19-to-0-20/SKILL.md) — reflection and `Name` changes.
- [Bevy world serialization](https://docs.rs/bevy/0.20.1/bevy/world_serialization/index.html)
- [`DynamicWorldBuilder`](https://docs.rs/bevy/0.20.1/bevy/world_serialization/struct.DynamicWorldBuilder.html)
