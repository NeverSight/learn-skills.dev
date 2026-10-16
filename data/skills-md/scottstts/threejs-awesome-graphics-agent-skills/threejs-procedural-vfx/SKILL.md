---
name: threejs-procedural-vfx
description: Author production real-time VFX in Three.js. Use for filmic HDR lens-flare compositors, highlight-derived ghosts, field-angle pupil deformation, localized glare and bloom, raymarched aurora curtains, finite-footprint emissive slabs, uniform volume integration, equirectangular radiance probes, WebGPU voxel fire and smoke, coupled volumetric fluid fields, mesh-surface emitters, signed-distance fire collisions, ship-conforming reentry plasma, generated capsule wakes, instanced analytic sparks, timed dissolving debris, dense-swap effect pools, additive holographic projections, Fresnel rim shells, scanline banding, glitch displacement, swept shape-to-shape handovers, and explicit scene-relative HDR emission hierarchy.
---

# Procedural VFX

Build effects from an event envelope, motion field, geometry representation, and shading response. Avoid independent particle emitters that happen to share a color.

This skill contains exemplary examples and assets beyond descriptive guidance,
they're worth studying, referencing, or even copying. Use them sufficiently
when relevant and do NOT blindly skip them.

## Effect graph

```text
subject/event state
  → effect-specific geometry, voxel fields, or instance attributes
  → flow-facing masks or analytic age
  → material response
  → pool/lifetime ownership
  → HDR and bloom contribution
```

Read [references/procedural-vfx-system.md](references/procedural-vfx-system.md)
for ship-conforming reentry shells, capsule wakes, dense instanced
spark/debris pools, holographic projection shells, HDR hierarchy, and
implementation limits.

Read [references/volumetric-fluid-fire.md](references/volumetric-fluid-fire.md)
for three-dimensional texture ownership, fixed fluid-compute scheduling,
mesh-surface injection, pressure projection, moving SDF boundaries,
temperature-mapped HDR raymarching, exact presets, and failure diagnostics.

Read [references/volumetric-aurora-curtains.md](references/volumetric-aurora-curtains.md)
for finite emissive-slab bounds, warped curtain density, uniform ray steps,
gentle start jitter, matching screen/probe materials, exact constants, limits,
and failure diagnostics.

Read [references/filmic-lens-flare.md](references/filmic-lens-flare.md) for HDR
emitter extraction, optical-axis invariants, field-angle pupil deformation,
finite ghost families, spectral rings, localized bloom, film response, exact
constants, limits, and failure diagnostics.

Read the [reentry plasma implementation](examples/reentry-plasma/reentry-plasma.js)
for closed layered wake shells, flow-axis deformation, advected filament
fields, opacity shaping, and additive emission diagnostics.

Read the
[hologram projection material](examples/holographic-shape-transition/hologram-material.js)
for the additive rim shell itself: squared Fresnel incidence with grazing
falloff, footprint-filtered object-space scanlines, height-phased glitch
displacement, and index-gated participation. Read its
[shape-transition driver](examples/holographic-shape-transition/hologram-transition.js)
for the shared sweep range across a shape set, the linear progress ramp inside a
longer dwell, and the complementary-discard handover.

Read the
[volumetric fluid fire implementation](examples/volumetric-fluid-fire/volumetric-fluid-fire.js)
for the complete WebGPU/TSL velocity, dye, pressure, vorticity, emitter,
collision, raymarch, and diagnostic system plus its calibrated fire preset.

Read the
[raymarched aurora implementation](examples/raymarched-aurora-curtains/aurora-curtains.js)
for the reusable emitting field, perspective-ray material, four-sample
equirectangular radiance material, shared uniforms, and calibrated curtain
preset without sky, terrain, weather, lighting, or renderer setup.

Read the
[filmic lens-flare implementation](examples/filmic-lens-flare/filmic-lens-flare.js)
for top-origin HDR sun detection, panorama-ray reconstruction, stable source
projection, finite radial ghost families, field-deformed pupil shapes, spectral
ring and star response, localized bloom, and the complete filmic composite.

## Rules

- Every layer must have a role in silhouette, motion, illumination, or residue.
- Give velocity, dye, pressure, vorticity, and collisions explicit texture
  ownership and one fixed compute schedule.
- For low-angle aurora, use a finite shallow emitting footprint, uniform ray
  steps, gentle start jitter, and step-length-weighted accumulation. Do not add
  extinction or an elevation gate after the footprint already removes the long
  limb path.
- Keep aurora emission separable from sky, stars, atmosphere, terrain lighting,
  weather, and grading; expose the same radiance through perspective and
  equirectangular materials.
- Convert velocity to volume UVW with the world-size vector; never advect a
  non-cubic volume as though its axes had equal scale.
- Keep the pressure ping-pong endpoint consistent with the projection read.
- Use normalized lifetime curves instead of scattered time constants.
- Derive secondary motion from the same flow or event direction.
- Keep bloom as a response to HDR emission, not as the effect's only shape.
- Derive lens ghosts from an HDR emitter, keep every synthetic centre on one
  optical axis, and deform pupil footprints from object-space field angle rather
  than screen radius.
- Keep the lens-flare family finite; do not extend calibrated terminal haze into
  an arbitrary bead chain or place diffraction stars at ghost centres.
- Pool instances and trails; do not allocate per burst.
- Filter every periodic band by pixel footprint, and fade it to the band's own
  mean rather than to zero.
- Measure rim incidence in a frame built from an inverse-transpose normal matrix.
- Give a multi-shape transition one shared normalised range and complementary
  discards, never per-shape ranges or overlapping coverage.
- Expose spawn, simulation, overdraw, and luminance debug views.
- Include a non-bloom baseline that remains legible.

## Routing boundary

Use `$threejs-temporal-surfaces` only for the screen-space
frost/touch-history pipeline. Use `$threejs-precipitation-surfaces` for
falling rain or snow, splash flipbooks, and weather events that alter ground
materials. Use `$threejs-volumetric-clouds` for atmospheric weather layers and
planet-scale cloud volumes. Use `$threejs-atmosphere-aerial-perspective` for
molecular/aerosol sky scattering and surface-segment aerial perspective. Keep
standalone filmic HDR lens-flare compositors, emissive aurora curtain volumes,
bounded interactive fire and smoke, subject-space plasma, generated wakes,
sparks, pooled debris, and additive projection shells in this skill. Keep lens
flare in `$threejs-atmosphere-aerial-perspective` when it remains one stage in a
shared sky-scattering and aerial-perspective composition.
