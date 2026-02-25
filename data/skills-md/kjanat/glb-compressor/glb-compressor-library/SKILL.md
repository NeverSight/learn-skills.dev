---
name: glb-compressor-library
description: Programmatic GLB/glTF 3D model compression library with a multi-phase pipeline, skinned-model awareness, and custom glTF-Transform transforms. Use when integrating compression into application code, building custom pipelines, or using individual transforms.
license: MIT
compatibility: Requires Bun >= 1.3 or Node.js >= 18.17. Externals (never bundled) - sharp, draco3dgltf, meshoptimizer.
references:
  - references/api.md
  - references/transforms.md
---

# glb-compressor Library

Programmatic API for multi-phase GLB/glTF compression. Skinned-model-aware
pipeline with gltfpack-first strategy and meshopt WASM fallback.

## Quick Start

```ts
import { compress, init, PRESETS } from 'glb-compressor';

await init(); // Pre-warm WASM (optional, called automatically)
const glbBytes = await Bun.file('model.glb').bytes();
const result = await compress(glbBytes, { preset: 'aggressive' });
await Bun.write('out.glb', result.buffer);
```

## Package Exports

```ts
import { ... } from 'glb-compressor';        // Library API
import { ... } from 'glb-compressor/server';  // Server (guarded by import.meta.main)
import { ... } from 'glb-compressor/cli';     // CLI entry
```

Conditional exports: `"bun"` field for Bun runtime, `"node"` for Node.js.

## Core API

### `init(): Promise<void>`

Pre-warm Draco + Meshopt WASM and configure glTF-Transform I/O. Called
automatically by `compress()`, but can be called at boot to eliminate cold-start
latency. Safe to call multiple times (shared promise).

### `compress(input, options?): Promise<CompressResult>`

Main entry point. Runs the full 6-phase pipeline.

**Parameters:**

| Param                   | Type             | Description                                              |
| ----------------------- | ---------------- | -------------------------------------------------------- |
| `input`                 | `Uint8Array`     | Raw GLB file bytes                                       |
| `options.preset`        | `CompressPreset` | `'default'` \| `'balanced'` \| `'aggressive'` \| `'max'` |
| `options.simplifyRatio` | `number`         | Additional simplification in `(0, 1)`                    |
| `options.onLog`         | `(msg) => void`  | Progress callback (used by SSE)                          |
| `options.quiet`         | `boolean`        | Suppress console output                                  |

**Returns:** `CompressResult`

```ts
interface CompressResult {
	buffer: Uint8Array; // Compressed GLB binary
	method: string; // 'gltfpack' | 'meshopt'
	originalSize?: number; // Input byte count
}
```

### `getHasGltfpack(): boolean`

Whether the `gltfpack` binary was found during initialization.

## In This Reference

| File                                        | Purpose                                             |
| ------------------------------------------- | --------------------------------------------------- |
| [api.md](./references/api.md)               | Full API surface: types, constants, utilities       |
| [transforms.md](./references/transforms.md) | Custom glTF-Transform transforms for a-la-carte use |

## Reading Order

| Task                       | Files to Read             |
| -------------------------- | ------------------------- |
| Basic compression          | This file only            |
| Custom pipeline / advanced | This file + transforms.md |
| Full type reference        | This file + api.md        |

## Pipeline Phases

1. **Cleanup** - dedup, prune, remove unused UVs (+ flatten/join/weld for
   static)
2. **Geometry** - merge by distance, remove degenerate faces, auto-decimate
3. **GPU** - instancing, vertex reorder, sparse encoding
4. **Animation** - resample keyframes, remove static tracks, normalize weights
5. **Textures** - compress to WebP via sharp (max 1024x1024)
6. **Final** - gltfpack (preferred) or meshopt WASM (fallback)

## Skinned Model Awareness

When skins are detected, the pipeline automatically skips destructive
transforms: flatten, join, weld, mergeByDistance, reorder, quantize, and
auto-decimate. This prevents broken skeletons, weight denormalization, and mesh
clipping.

## Presets

```ts
type CompressPreset = 'default' | 'balanced' | 'aggressive' | 'max';
```

| Preset       | Skinned behavior                                  | Static behavior |
| ------------ | ------------------------------------------------- | --------------- |
| `default`    | `-vp 20 -kn`                                      | `-vp 16`        |
| `balanced`   | + animation quant (`-at 14 -ar 10 -as 14 -af 24`) | Same + `-vp 16` |
| `aggressive` | + stronger quant (`-at 12 -ar 8 -as 12 -af 15`)   | Same + `-vp 14` |
| `max`        | + supercompression (`-cz`), simplify (`-si 0.95`) | Same            |

## Anti-Patterns

- Don't flatten/join/weld/quantize skinned models.
- Don't import from `cli/` or `server/` - lib is the dependency root.
- Don't bypass `mod.ts` barrel for public API additions.
