---
name: glb-compressor-cli
description: Compress GLB/glTF 3D models using the glb-compressor CLI. Use when running compression from the command line, writing shell scripts that compress models, or integrating into CI/CD pipelines.
license: MIT
compatibility: Requires Bun >= 1.3 or Node.js >= 18.17. Optional gltfpack binary for best compression.
---

# glb-compressor CLI

Command-line tool for compressing GLB/glTF 3D model files. Supports glob
patterns, configurable presets, mesh simplification, and batch processing.

## Binary Name

`glb-compressor` (installed via npm/bun) or `bun run cli` (from source).

## Usage

```sh
glb-compressor <files...> [options]
```

## Options

| Flag                   | Description                                | Default                                   |
| ---------------------- | ------------------------------------------ | ----------------------------------------- |
| `-o, --output <dir>`   | Output directory                           | Same as input (with `-compressed` suffix) |
| `-p, --preset <name>`  | Compression preset                         | `default`                                 |
| `-s, --simplify <0-1>` | Mesh simplification ratio (e.g. 0.5 = 50%) | None                                      |
| `-q, --quiet`          | Suppress progress output (for scripting)   | `false`                                   |
| `-f, --force`          | Overwrite existing output files            | `false`                                   |
| `-h, --help`           | Show help text                             |                                           |
| `-v, --version`        | Show version                               |                                           |

## Presets

| Preset       | Behavior                                                         |
| ------------ | ---------------------------------------------------------------- |
| `default`    | Conservative, preserves all detail                               |
| `balanced`   | Moderate animation quantization, 24 Hz resample                  |
| `aggressive` | Strong animation quantization, 15 Hz resample (best for avatars) |
| `max`        | Aggressive + supercompression + lower vertex precision           |

## Examples

```sh
# Compress a single file
glb-compressor model.glb

# Aggressive preset to an output directory
glb-compressor model.glb -p aggressive -o ./out/

# Batch compress with glob, overwrite existing
glb-compressor *.glb -f -p balanced

# Quiet mode for CI/scripts (exit code 0 = success, 1 = failure)
glb-compressor model.glb -q -p max

# Simplify mesh to ~50% vertex count
glb-compressor model.glb -s 0.5

# From source (development)
bun run cli -- model.glb -p aggressive -o ./compressed/
```

## Output Naming

Output files are named `<input>-compressed.glb`. When `-o` is specified, files
are placed in that directory. Without `-o`, output is written alongside the
input file.

## Exit Codes

| Code | Meaning                           |
| ---- | --------------------------------- |
| `0`  | All files compressed successfully |
| `1`  | One or more files failed          |

## Pipeline

The CLI runs the same 6-phase pipeline as the library:

1. **Cleanup** - dedup, prune, remove unused UVs (+ flatten/join/weld for
   static)
2. **Geometry** - merge by distance, remove degenerate faces, auto-decimate
3. **GPU** - instancing, vertex reorder, sparse encoding
4. **Animation** - resample keyframes, remove static tracks, normalize weights
5. **Textures** - compress to WebP (max 1024x1024)
6. **Final** - gltfpack (preferred) or meshopt WASM fallback

Skinned models are auto-detected and take a conservative path that skips
transforms known to break skeleton hierarchies.

## Skinned Model Awareness

When a GLB contains skins (e.g. avatars), the CLI automatically skips: flatten,
join, weld, mergeByDistance, reorder, quantize, and auto-decimate. This prevents
broken skeleton hierarchies, vertex weight denormalization, and mesh clipping
artifacts.

## Dependencies

- **gltfpack** (optional): If found in `$PATH`, used for final compression (best
  results). Falls back to meshopt WASM if unavailable.
- **sharp**: Used for texture compression to WebP.
