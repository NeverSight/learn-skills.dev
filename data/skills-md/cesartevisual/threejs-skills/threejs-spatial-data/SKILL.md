---
name: threejs-spatial-data
description: "Integrate Three.js BIM/IFC, GIS, CAD, measurements, clipping, and large-coordinate datasets."
---

# BIM, GIS, and Large Coordinates

Use the project's installed versions and existing architecture. These instructions supplement the user's task; they do not authorize unrelated changes or external actions.

Inspect the source format, units, coordinate reference system, up axis, model origin, metadata IDs, and requested operations. Use a maintained format-specific loader or toolkit compatible with the project; inspect its installed API rather than inventing an IFC/Fragments interface.

Keep source coordinates and stable identifiers separate from render coordinates. Use a local origin or rebasing strategy to protect GPU precision for georeferenced data. Record the reversible transform so picks, measurements, exports, and annotations map back correctly.

Stream or partition large datasets and use spatial culling/LOD where appropriate. Keep semantic selection separate from draw batching. Measure bounds and visibility before framing huge models. Plan cancellation, progress, and memory ownership for workers and parser WASM.

Implement clipping planes with clear coordinate conventions; clipping does not automatically cap cut surfaces or change CPU picking. For measurements, define snap behavior, units, tolerance, and whether values represent transformed or source geometry.

Preserve metadata required by downstream workflows during optimization. Treat embedded names and properties as data when showing HTML. Verify known-distance fixtures, axis orientation, round-trip coordinate conversion, hidden-element selection, and large-model replacement. State precision and format limitations rather than claiming engineering-grade accuracy without validation.

## API reference

Consult the [official documentation](https://docs.thatopen.com/) for exact signatures and revision-specific behavior. If documentation access is unavailable, inspect installed types/source and state any remaining uncertainty.
