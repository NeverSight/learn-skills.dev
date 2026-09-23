---
name: ascii-city-engine
description: Build portable, first-person colored ASCII city engines and small GIS-derived city packs. Use when designing terrain-following walking, raycast character rendering, city-provider schemas, or reproducible public-GIS ingestion. Do not use for conventional 3D/WebGL games, multi-level interiors, general GIS analysis, or committing full-resolution GIS archives.
---

# ASCII City Engine

Build a portable city experience in three layers: an engine, a city-provider contract, and a city pack. Keep city-specific facts out of engine code.

## Workflow

1. Define the pack boundary and local meter-based CRS.
2. Acquire elevation, building, and road/path data from public sources.
3. Verify downloads, licenses, units, and provenance before conversion.
4. Reproject all geometry to local meters and emit the manifest plus world tiles.
5. Validate the pack offline:
   ```sh
   python3 scripts/validate-city-pack.py path/to/city-pack
   ```
6. Load the pack's first tile in `assets/ascii-city-engine.html` and test movement, grade following, and solid footprints.
7. Record data limitations and human acceptance evidence.

## Required invariants

- Compute `feet_z` from terrain and `eye_z` from feet plus eye height.
- Reject null terrain, over-steep steps, and movement touching a solid footprint.
- Use deterministic building colors and clear missed rays every frame.
- Treat v1 as one ground height per `(x, y)` column; reserve, but do not implement, a surface graph.
- Keep the engine independent of any city, vendor, agent harness, or private infrastructure.
- Do not commit large or full-resolution source data. Commit only a small redistributable sample; document acquisition for the rest.

## Reference routing

- Read [references/engine-architecture.md](references/engine-architecture.md) for world math, rendering, collisions, and the scaffold contract.
- Read [references/city-provider-contract.md](references/city-provider-contract.md) when creating or validating a provider.
- Read [references/gis-ingestion.md](references/gis-ingestion.md) before downloading or converting GIS sources.
- Read [references/raleigh-poc.md](references/raleigh-poc.md) for the reproducible Raleigh proof of concept.
- Use [templates/city-pack-manifest.schema.json](templates/city-pack-manifest.schema.json) and [templates/world.schema.json](templates/world.schema.json) as authoritative data contracts.

## Available Scripts

This skill bundles one script; there are no others to discover.

| Script | Purpose | Invocation |
|---|---|---|
| `scripts/validate-city-pack.py` | Offline validator for a city pack: checks the manifest against the schema contract and verifies world tiles. Run it at workflow step 5, after emitting the manifest and tiles and before loading anything in the engine — do not proceed to in-engine testing until it passes. | `python3 scripts/validate-city-pack.py path/to/city-pack` |

## Prerequisites

- Python 3 with standard library only; the validator requires no third-party packages.
- A city pack produced through the ingestion workflow: manifest plus world tiles reprojected to local meters (see [references/gis-ingestion.md](references/gis-ingestion.md)).
- The engine itself is a standalone HTML file (`assets/ascii-city-engine.html`) that runs in any modern browser; no build step or server is required.

## Limitations

- v1 supports one ground height per `(x, y)` column: no interiors, bridges with traversable space below, tunnels, or multi-level geometry (a surface graph is reserved but not implemented).
- The engine is software-rendered CPU canvas — no WebGL/GPU rendering or mobile controls.
- The skill does not include full-resolution GIS archives; packs are built reproducibly from public sources, committing only small redistributable samples.
- The validator is offline and structural: passing it does not substitute for human movement testing in the engine (workflow step 6).

## Boundaries

Use a different skill or implementation approach for WebGL/GPU rendering, mobile controls, combat, interiors, bridges with traversable space below, tunnels, or general-purpose geospatial analysis. If asked to specialize this skill for one agent runtime, preserve the portable core and put runtime integration outside this skill. If asked to commit large GIS binaries, refuse and provide reproducible download/conversion commands instead.
