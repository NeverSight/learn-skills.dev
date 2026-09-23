---
name: threejs-geometry
description: "Create or optimize Three.js BufferGeometry, procedural meshes, instanced objects, and geometry attributes."
---

# Geometry and Instancing

Use the project's installed versions and existing architecture. These instructions supplement the user's task; they do not authorize unrelated changes or external actions.

Choose built-in geometry for simple shapes, BufferGeometry for custom topology, and instancing for repeated geometry/material combinations. Keep topology density tied to silhouette and deformation, not arbitrary high segment counts.

Define indexed versus non-indexed data deliberately. Attribute vertex counts must agree; triangle winding controls front faces. UV seams and hard normals can require duplicated vertices. Recompute normals after topology changes when appropriate; normals alone do not create missing UVs or tangents.

For dynamic attributes, allocate capacity up front, choose usage before first rendering, mutate typed arrays, and flag needsUpdate. Use supported update ranges for partial writes. Refresh bounding volumes after changes that invalidate culling or picking. A bounding box is not automatically a precise collision shape.

With InstancedMesh, maintain a stable instance ID to application ID mapping. Update instance matrices/colors and their needsUpdate flags; recompute bounds after instance transforms change. Split large instance sets spatially when one enormous bound defeats culling. Plan selection/highlighting without cloning a material for every instance.

Keep generated geometry ownership explicit, reuse immutable assets, and dispose geometry only when its last consumer releases it. Verify normals under directional lighting, seams under a checker texture, culling at camera edges, and per-instance picking after updates.

## API reference

Consult the [official documentation](https://threejs.org/docs/pages/InstancedMesh.html) for exact signatures and revision-specific behavior. If documentation access is unavailable, inspect installed types/source and state any remaining uncertainty.
