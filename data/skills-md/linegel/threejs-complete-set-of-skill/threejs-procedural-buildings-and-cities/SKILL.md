---
name: threejs-procedural-buildings-and-cities
description: Compile procedural buildings, cities, and semantic site assemblies in Three.js r185 WebGPU/TSL. Use for building massing and facades, city-scale architectural batching and LOD, or deterministic placement of heterogeneous site assets around architecture.
---

# Procedural Buildings and Cities

Treat architecture as a compiler: decide the runtime package, produce and
validate a serializable plan, then emit geometry. The plan owns massing,
exposed surfaces, placements, material slots, and stable identity.

## Process

1. **Select the runtime package from mutability and repetition.**

   | Workload | Package |
   | --- | --- |
   | Static building or chunk | merged indexed `BufferGeometry` per material slot |
   | Editable varied modules | `BatchedMesh` per compatible material slot |
   | Repeated identical topology | spatially paged `InstancedMesh` |
   | District-scale streaming | bounded chunks with projected-error LOD |

   Initialize `WebGPURenderer` before gating WebGPU features. Architecture
   planning can remain CPU-deterministic; add storage or compute only for a
   measured city-scale visibility or update bottleneck.

   **Complete when:** every architectural element has one package, and every
   package has an explicit mutability, visibility, and identity reason.

2. **Produce a valid building plan.** Normalize units and settings, then apply
   the mass-operator rail: footprint pieces -> union/court subtraction ->
   extrude/stack -> inset/split -> optional connector. Choose only
   prevalidated alternatives; give every operator result a stable ID and
   validate it before the next operator. Read
   [grammar-and-mesh-compiler.md](references/grammar-and-mesh-compiler.md) when
   implementing these operators. Serialize footprints, mass volumes, exposed
   intervals, placements, module usage, ownership, material slots, UV scale,
   and budgets.

   **Complete when:** the same inputs reproduce the same operator choices and
   IDs, every operator output passes its topology/dimension/ownership gate, and
   geometry emission is unnecessary to diagnose an invalid plan.

3. **Resolve exposed boundaries before facade placement.** Subtract shared or
   blocked side regions with their vertical overlap; unequal-height neighbors
   require height bands, not whole-side removal. Quantize positive surviving
   spans into a bounded legal bay count, and attach facade, roof, trim, and
   corner placements to those surface regions.
   Read [grammar-and-mesh-compiler.md](references/grammar-and-mesh-compiler.md)
   when implementing footprint subtraction, bay quantization, placement
   ownership, or module-local frames.

   **Complete when:** no facade region lies inside occupied mass at its height,
   every legal region has a declared placement or semantic blank, and corner ownership is
   unambiguous.

4. **Close and validate the plan.** Add visible caps, decks, soffits, and
   closure surfaces for validated connectors; resolve every placement through
   the module registry; then test registry completeness, ownership uniqueness,
   general overlap, winding, bounds, material membership, and UV density.

   For a heterogeneous site assembly, keep domain assets delegated to their
   owning skills and register each ruin, dock, boat, rock, vegetation cluster,
   or prop with a stable placement ID, owner, transform/frame/scale, support and
   clearance volumes, anchor, and LOD policy. Apply the deterministic
   heterogeneous-site-placement rules in
   [grammar-and-mesh-compiler.md](references/grammar-and-mesh-compiler.md).
   When implementing candidate identity, random lanes, or phase ranking, import
   [deterministic-placement-key.mjs](scripts/deterministic-placement-key.mjs).
   Validate whole-phase key uniqueness with `validateWinnerKeys()` before
   using its reflexive comparator. The helper does not own support, clearance,
   conflict detection, or phase admission; strict local winners are not a
   maximal packing algorithm. Halo reach includes both candidate extents.
   Place the landmark first, then solve access, support, and clearance before
   repeated detail.

   **Complete when:** every placement resolves, every surface has one owner,
   overlaps are empty or explicitly permitted, support/clearance gates pass,
   stable IDs replay independently of chunk load order and unrelated family
   insertion, and all emitted geometry or delegated assets trace to a plan
   record.

5. **Compile by material slot and spatial boundary.** Keep semantic material
   identities stable while choosing merge, batch, or instance emission. In
   Three.js r185 WebGPU, `BatchedMesh` iterates visible multi-draw entries: it
   improves object/state management but does not prove GPU draw collapse.
   Merge compatible static geometry or instance identical topology when draw
   collapse is required. Read
   [grammar-and-mesh-compiler.md](references/grammar-and-mesh-compiler.md) when
   implementing slot writers, paging, projected-error LOD, or draw accounting.

   **Complete when:** slot membership is complete, indexed bounds are finite,
   pages are independently cullable with refreshed transform/count bounds and
   upload flags, LOD error is gated in physical viewport pixels, and actual
   backend draw items are reported.

6. **Bind materials and presentation.** Use `MeshStandardNodeMaterial` or
   `MeshPhysicalNodeMaterial` per semantic slot. Preserve physical texture
   scale and data/color encodings. Hand final color to the scene's one
   `RenderPipeline` output transform, then dispose replaced geometries,
   batches, textures, and node resources.

   **Complete when:** flat material, grazing light, and final output agree on
   geometry and normals; one component owns output conversion; replacement and
   disposal leave no stale bounds or live resources.

7. **Verify the compiler.** Exercise simple and compound footprints, courts,
   bridges or connectors when supported, minimum legal spans, dense placement,
   repeated modules, and district paging across multiple seeds. Inspect
   silhouette, untextured geometry, corners, openings, setbacks, roofs, and LOD
   transitions.

   **Complete when:** every fixture has a valid plan, no internal facade
   intervals or placement overlaps, a complete registry, deterministic replay,
   correct bounds and material slots, stable UV scale, and measured triangle and
   draw counts.

## Ownership Boundary

- Use `$threejs-procedural-geometry` for reusable profiles, sweeps, arches,
  frames, and low-level mesh writers.
- Use `$threejs-procedural-materials` for masonry, glass, metal, weathering,
  filtering, and material-field authoring.
- Use `$threejs-procedural-fields` for terrain and parcel fields consumed by a
  city layout.
- Use `$threejs-scalable-real-time-shadows`, `$threejs-image-pipeline`, and
  `$threejs-visual-validation` for scene-wide shadow, output, and evidence
  ownership.

This skill owns building massing, facade semantics, architectural module and
site placement, plan validation, material-slot compilation, and architectural
spatial LOD; delegated skills still own nonarchitectural asset generation.
