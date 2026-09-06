---
name: threejs-procedural-planets
description: Scale procedural planetary bodies in Three.js r185 WebGPU/TSL. Use when global curvature needs a cube-sphere quadtree, a sustained ground view needs a tangent clipmap, an orbit-to-ground transition needs both, or a gas-giant cloud deck needs body-scale band fields.
---

# Procedural Planets

Choose the body-scale representation first. One set of planet-space causes must
drive geometry, normals, material identity, queries, diagnostics, water/coast
handoffs, and atmosphere inputs.

## Process

1. **Gate body scale.** Test whether curvature, horizon, global geodesy,
   orbit-to-ground transition, or atmosphere coupling is observable. A bounded
   local site belongs to procedural fields and geometry when tangent-plane
   sagitta, normal rotation, geodesic, horizon, and projected errors all pass.
   Read
   [body-model-mapping-and-lod.md](references/body-model-mapping-and-lod.md)
   when deriving the body-scale gate.

   **Complete when:** the accepted camera and data domain either proves a local
   approximation or names at least one body-scale observable that requires this
   skill.

2. **Freeze the body model and units.** Declare center, sphere radius or
   ellipsoid axes in meters, `metersPerWorldUnit`, height and sea-level datum,
   body/world transform, origin policy, surface-coordinate meaning, and
   atmosphere bottom/top geometry. When a sphere approximates an ellipsoid,
   read
   [body-model-mapping-and-lod.md](references/body-model-mapping-and-lod.md)
   and apply its position, normal, area, geodesic, horizon, atmosphere-altitude,
   and optical-depth error gate. Give each changing field one owner and one
   version.

   **Complete when:** every length and vector has units and a frame, surface
   altitude has one definition, render-origin changes leave physical field
   identity unchanged, and the spherical branch either passes every declared
   approximation gate or is rejected in favor of the ellipsoid.

3. **Select mapping and spatial representation.** Choose normalized,
   spherified, or verified equal-area cube mapping from distortion and inverse
   requirements. Choose a cube-face quadtree for arbitrary globe views, a
   tangent clipmap for sustained local views, or a hybrid with an explicit
   near/far handoff. A gas/cloud-deck body uses continuous wrapped band fields
   rather than solid-terrain displacement. Read
   [body-model-mapping-and-lod.md](references/body-model-mapping-and-lod.md)
   for a solid-body mapping, ellipsoid convention, quadtree, clipmap, or hybrid.
   Read [gas-cloud-deck.md](references/gas-cloud-deck.md) for a gas/cloud-deck
   body.

   **Complete when:** mapping Jacobian, seams, inverse/domain validity, camera
   domain, and near/far ownership all have falsifiable gates.

4. **Build error-bounded LOD and submission.** For the global branch, maintain
   six 2:1-balanced face quadtrees, continuous parent morph, and one of the 16
   four-edge transition masks. Reuse a shared indexed grid and submit compact
   patch records in instanced or indirect mask bins. For clipmaps, bound ring
   error, recentering, and far-field ownership. Evaluate physical-pixel error
   over the complete displaced support for every active view.

   A global patch identity is
   `(bodyId, mappingVersion, face, level, x, y)`. Frontier order, visibility,
   draw bin, allocation slot, and cache address are not identity. A clipmap cell
   identity is `(bodyId, mappingVersion, level, bodySpaceCellCoordinates)`.
   Reusing a physical slot binds a new identity and resets every slot-bound
   temporal or dynamic state; recentering changes slot bindings, not body-space
   field identity.

   Before allocating compute, storage, or indirect resources, run
   `await renderer.init()` and require
   `renderer.backend.isWebGPUBackend === true`. Otherwise keep planning on the
   CPU or report the native-WebGPU branch unavailable.

   **Complete when:** projected error, hysteresis, and submission bounds pass,
   plus every selected branch satisfies its own criterion:

   - **global:** 2:1 balance holds across face edges/corners, all 16 masks are
     crack-free, and production submission has no per-patch draw loop;
   - **clipmap:** rings cover the local domain, recentering preserves field
     coordinates, curvature/reconstruction error passes, and one far-body owner
     covers beyond the outer ring;
   - **hybrid:** near/far coverage has no gap and one composite owner in the
     overlap, composite position and normal remain continuous through the
     handoff, and overlap residency is bounded;
   - **gas/cloud deck:** wrapped-longitude seams, advection continuity, stable
     storm identity, and conservative advected bounds pass.

5. **Build shared causal fields.** Define common field functions for reference
   direction, displacement, tangent gradient, geology, craters, climate,
   hydrology, snow/ice, material causes, queries, and diagnostics. Direct,
   compute-cached, and CPU-visible paths use the same schema and identity
   constants. Cache only dirty patch causes, include cross-face filter support,
   and validate gradients independently before using analytic normals. Read
   [solid-fields-and-coast.md](references/solid-fields-and-coast.md) when
   implementing solid-body caches, crater fields, detail filtering, CPU/TSL
   parity, normals, materials, or coast data. Read
   [gas-cloud-deck.md](references/gas-cloud-deck.md) for gas-band fields.

   GPU patch min/max bounds use workgroup reduction plus deterministic merging,
   or a proven monotonic ordered-integer encoding with explicit sign, NaN, and
   decode-error rules. Do not rely on unsupported float atomics.

   **Complete when:** geometry and shading use the same height function, cache
   invalidation follows causes rather than cameras, parity covers every
   published channel, min/max reduction is legal and conservative, and metric
   value and normal errors pass their own gates.

6. **Publish narrow handoffs.** A field handoff states producer, consumer,
   owner, units, frame/origin, sample time or interval, represented support and
   filter, validity/staleness, version, and error. A planetary coast additionally
   publishes mean surface, seabed height, metric coast distance/frame, source
   resolution, and uncertainty. Atmosphere receives the same reference surface,
   transform, `metersPerWorldUnit`, altitude convention, shell geometry, sun
   frame, and scene-linear radiometric basis. Read
   [solid-fields-and-coast.md](references/solid-fields-and-coast.md) when a
   coast/water consumer is active. Read
   [surface-atmosphere-handoff.md](references/surface-atmosphere-handoff.md)
   when an atmosphere consumer is active.

   **Complete when:** each consumer names one authoritative producer, rejects
   invalid or stale data, and performs no frame-critical GPU readback.

7. **Bind materials and presentation.** Use `MeshStandardNodeMaterial` or
   `MeshPhysicalNodeMaterial` from shared field causes. Keep data textures
   linear, preserve declared color encodings, and hand HDR scene color to the
   one `RenderPipeline` output transform. Rebuild only dirty field tiles or LOD
   frontier state, keep in-flight cache resources immutable, and dispose retired
   buffers, textures, passes, and indirect state.

   **Complete when:** output conversion has one owner, direct and cached paths
   agree, origin rebases preserve the body, and repeated resize/replacement
   reaches a stable resource plateau.

8. **Verify the selected branches.** Capture orbit, horizon, and close views;
   unlit silhouette; flat albedo without atmosphere; grazing light; mapping,
   patch-error, transition-mask, normal, material, coast, and atmosphere
   diagnostics. Sweep split/merge boundaries and use multiple fixed seeds.

   **Complete when:** the scale and sphere/ellipsoid gates, mapping distortion,
   every selected branch criterion above, shared-field parity, derivative
   accuracy, atmosphere units, triangle/draw counts, cache bytes, timing, and
   zero runtime readbacks all have direct evidence.

## Ownership Boundary

- Use `$threejs-procedural-fields` and `$threejs-procedural-geometry` for local
  terrain whose accepted domain does not expose body curvature or global LOD.
- Use `$threejs-water-optics` for the time-varying free surface, currents,
  breaking, foam, and water optics; this skill owns the reference surface,
  seabed, and planetary coast analysis.
- Use `$threejs-sky-atmosphere-and-haze` for scattering and aerial perspective;
  this skill owns the surface-side geometry and units handoff.
- Use `$threejs-image-pipeline`, `$threejs-scalable-real-time-shadows`, and
  `$threejs-visual-validation` for shared output, shadows, and evidence.

This skill owns the body-scale surface representation, coupled planetary
fields, patch LOD/submission, query parity, and surface-side handoffs.

For work spanning multiple planet branches, use
[planet-field-and-atmosphere-systems.md](references/planet-field-and-atmosphere-systems.md)
as the branch index and common contract.
