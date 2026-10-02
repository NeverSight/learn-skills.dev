---
name: threejs-procedural-geometry
description: Procedural geometry compilation for Three.js WebGPU/TSL. Use when a task needs an indexed mesh writer, contour-derived terrain or terraces, profile or branch sweeps, or a BatchedMesh, InstancedMesh, or dynamic-update decision.
---

# Procedural Geometry

Treat geometry generation as a compiler: select the representation, freeze
semantic regions and error bounds, compute exact capacity, emit topology and
render attributes, then validate both. Meaning belongs to generator inputs;
allocation, topology, groups, updates, and disposal belong to the writer.

For multi-system work, `$threejs-choose-skills` is an optional coordinator.
Fields own continuous causes, materials own PBR response, motion owns
deformation state, and this skill owns rendered topology. When geometry supplies
another system, publish stable units, coordinate/frame convention, producer and
consumer owners, revision, support, validity domain, error bound, and update
phase independently of render LOD and draw indices.

## 1. Select the representation before allocation

Choose from the observable and update pattern:

| Contract | Representation |
| --- | --- |
| one unique authored surface with material regions | indexed `BufferGeometry` with groups |
| many same-material objects with varied topology | `BatchedMesh` |
| many repeats with identical topology | `InstancedMesh` |
| GPU-owned transforms or visibility with identical topology | matrix-free instanced geometry plus storage-backed state |
| hot visibility compaction with stable buckets | storage data plus indirect draw commands |
| continuous single-valued relief | indexed adaptive grid, quadtree, or clipmap with a seam policy |
| hard terraces, cliffs, or topology-bearing bands | contour-derived caps plus explicit walls/band meshes |
| visible overhangs or caves | bounded volumetric meshing after memory/topology gates pass |

In r185 WebGPU, `BatchedMesh` manages geometry and culling but the backend still
iterates visible multi-draw entries; it is not evidence of one native draw.
`InstancedMesh` is valid only for identical topology.

This step is complete when one representation owns each surface/object class,
its culling and update unit is named, and no triangle or buffer has been emitted.

## 2. Freeze semantics and error contracts

Record coordinate frames, semantic dimensions, named regions, material slots,
smoothing groups, UV charts, hard boundaries, topology identities, LOD view
envelope, and resource owner. Gate each LOD with a conservative error bound in
physical render-target pixels at the actual target size and an unjittered view.
Include the complete support and error of geometry, active displacement or
deformation, filtering, and reconstruction. Use the exact camera projection or,
for a perspective approximation, the nearest valid positive view depth; accept
the LOD only when the projected bound is at or below that view's declared
threshold. Give each view separate enter/exit thresholds with hysteresis and a
minimum dwell, and keep both transition levels resident until the transition
finishes. Triangle ratios are supporting counts, not an error bound.

For contour-driven work, consume one versioned field source. Read
[contour topology and terrain compilation](references/profile-sweeps-and-mesh-writers.md#contour-topology-and-terrain-compilation)
before extracting a shoreline, terrace, band, cliff, or region with holes.

When placement, picking, or measurement anchors must survive LOD or rebuilds,
read [semantic anchors and LOD bindings](references/profile-sweeps-and-mesh-writers.md#semantic-anchors-and-lod-bindings)
before decimation.

This step is complete when every intended face belongs to a semantic region,
material slot, smoothing group, UV chart, topology identity, and projected-error
gate, and every required anchor has a stable source/topology identity and LOD
binding policy.

## 3. Compute exact capacity, then emit

Count render vertices after all required duplication and count indices before
allocation:

```text
vertexCount = unique (topological vertex, boundary domain, attribute values) tuples
indexCount = 3 * triangleCount
```

Count overlapping split reasons once; a material slot alone need not duplicate
identical vertex attributes. Validate safe capacity arithmetic and memory limits
before allocation. On the pinned r185 path, use `Uint16Array` only through
index `65534`, otherwise explicit `Uint32Array`: its upload adapter rewrites
`65535` in a Uint16 index to the restart sentinel and widens the buffer. Account
for the actual uploaded width separately from the CPU array. Emit through a small
writer surface such as:

```text
addVertex, addTriangle, addQuad
duplicateForBoundary
startSmoothingGroup, startUvChart, addGroup
finishGeometry
```

Every index belongs to exactly one nonoverlapping group with a stable material
index. `finishGeometry` asserts the planned and written counts match.

This step is complete when allocation equals the planned capacity exactly,
every emitted index is owned by one group, and overflow or unfilled capacity is
an explicit error.

## 4. Close topology, normals, UVs, and frames

Keep topological identity separate from render-vertex identity. Render vertices
duplicate at hard normals, material boundaries, UV seams, and mirrored tangent
spaces while topological edges still prove adjacency and closure.

Use analytic normals/tangents where the generator owns a parameterization.
`computeVertexNormals()` is for deliberately smooth shared-vertex regions. For
normal-map parity, await `MikkTSpace.ready` before
`computeMikkTSpaceTangents(...)`; r185 de-indexes indexed geometry, so recompute
counts, groups, bounds, and bytes for that distinct representation. Preserve
semantic metadata, active draw range, and attribute type/usage outside that
conversion, which does not retain all of them. Convert before GPU publication.

Production UVs express physical distance or declared repeats; normalized local
parameters belong in a separate debug attribute. Profile and branch sweeps use
a rotation-minimizing parallel-transport frame with an explicit antiparallel
fallback and closed-loop holonomy correction.

Read
[profile sweeps and transported frames](references/profile-sweeps-and-mesh-writers.md#profile-sweeps-and-transported-frames)
when emitting along a curve.

This step is complete when topology closes at every undeclared boundary,
normals/tangents match semantic boundaries, UV density is stable across LOD,
and transported frames remain continuous through zero curvature and inflections.

## 5. Wire batching and updates

Initialize and gate the renderer before allocating GPU-owned storage or
indirect commands:

```js
await renderer.init();
if (renderer.backend.isWebGPUBackend !== true) {
  throw new Error('Native WebGPU is required for geometry storage and indirect draws.');
}
```

Check the selected storage bindings and buffer usage against the initialized
device limits before compilation.

Set attribute `usage` before first render. Keep live attribute arrays when
layout compilation, raycasting, bounds, serialization, or restoration still
reads them; releasing generator intermediates is a separate operation. Dynamic
sections retain unconsumed `addUpdateRange()` component intervals until the
adapter uploads them. Empty ranges mean a full upload, not zero work. In r185,
`DynamicDrawUsage` also uploads without a version change; intermittent edits
use version-driven usage plus `needsUpdate`. Recompute affected bounds.
Capacity, item size, or usage-model changes replace the owning geometry as a
validated resource generation, with explicit retirement of the previous one.

When compute owns instance state, submit compute before the consuming render
and keep one transform owner. GPU transforms require bounds for the posed
instance domain in every view; base-mesh bounds and CPU raycasts do not observe
storage-only deformation. In r185, `computeAsync()` is not a GPU-completion
fence. Indirect commands use CPU-known byte offsets and stable homogeneous
buckets; shader masking is not visibility compaction.

Read
[batching, dynamic updates, and indirect draws](references/profile-sweeps-and-mesh-writers.md#batching-dynamic-updates-and-indirect-draws)
before adding a batch container, per-frame mutation, storage state, or indirect
draw.

This step is complete when each mutable byte range, dispatch, draw entry,
bounding volume, and disposal point has one owner and hidden work is absent from
the claimed culling result.

## 6. Validate topology and render geometry

Validate topological identities before render duplication, then the final
`BufferGeometry`:

- closed/simple/nested contour loops and declared open boundaries;
- two oppositely oriented incident faces per interior topological edge;
- no T-junctions, duplicate faces, bow-ties, or unintended non-manifold edges;
- finite attributes, in-range indices, nondegenerate triangles, and winding;
- unit normals, tangent handedness, physical UV density, group coverage, and
  bounds containing every vertex;
- protected features and topology through every LOD and mixed-LOD seam;
- stable anchor source/topology IDs, per-LOD bindings, exclusion revisions, and
  bounded position/frame error through rebuild and LOD changes;
- exact resident/upload bytes, draw/backend entries, update ranges, and
  sustained target timing where performance is claimed.

Diagnostics expose topological versus render IDs, boundaries, winding, normals,
tangents, UV density, material groups, LOD/seam error, batch identity, and dirty
ranges.

This step is complete when every semantic region passes topology, attribute,
LOD, group, bounds, byte, lifecycle, and claimed performance gates, including
adversarial contour and frame cases selected by the active branches.

## Completion

The geometry system is complete when representation precedes allocation; exact
capacity equals emitted data; semantic topology survives render duplication,
batching, updates, and LOD; every index and mutable byte has one owner; and the
final mesh passes topology, attribute, projected-error, resource, and lifecycle
checks.
