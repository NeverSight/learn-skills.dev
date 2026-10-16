---
name: threejs-raymarched-space-effects
description: Build raymarched space phenomena in Three.js. Use for black-hole lensing, accretion disks, wormhole throat transits, curved-ray and null-geodesic integration, lensed celestial spheres, procedural star fields and galactic skies, relativistic-looking distortion, bounded volumetric structures, and GPU effects that need controlled numerical integration.
---

# Raymarched Space Effects

Treat these effects as numerical renderers with explicit integration state. The visual character depends on coordinate choice, step policy, and how rays interact with emissive structures.

This skill contains exemplary examples and assets beyond descriptive guidance,
they're worth studying, referencing, or even copying. Use them sufficiently
when relevant and do NOT blindly skip them.

## Workflow

1. Define the effect-space transform and camera ray.
2. Choose a physical, physically inspired, or purely artistic bending model.
3. Bound the integration domain.
4. Track ray position, direction, throughput, and accumulated radiance.
5. Detect crossings with disks, shells, throats, or event boundaries.
6. Sample the background only after integration terminates, filtered by the
   ray-bundle footprint rather than point sampled.
7. Add diagnostics for trajectory, step count, and termination reason.

Read [references/curved-ray-integrators.md](references/curved-ray-integrators.md)
for the two wormhole throat models, observer transport through a throat, the
artistic curved-ray accretion integrator, disk composition, and implementation
defects.

Read
[references/lensed-celestial-spheres.md](references/lensed-celestial-spheres.md)
for footprint-filtered skies, flux-conserving star point spreads, dust
extinction, bright sources under display clipping, progressive accumulation,
and the bloom kernel a compact source needs.

Read the
[curved-ray accretion volume](examples/curved-ray-accretion-volume/curved-ray-effect.js)
for the inverse-square steering loop, thin disk density, front-to-back
accumulation, deterministic star environment, and integrator diagnostics.

Read the
[Schwarzschild geodesic black-hole effect](examples/schwarzschild-geodesic-black-hole/geodesic-black-hole-effect.js)
for RK2 null-geodesic integration, interpolated equatorial disk crossings,
Doppler/redshift disk emission, lensed procedural deep field, and HDR bloom
composition.

Read the
[traversable wormhole transit](examples/traversable-wormhole-transit/wormhole-effect.js)
for adaptive RK4 integration of the reduced geodesic system, an observer frame
parallel-transported through the throat, exterior-region selection, progressive
Halton accumulation, and the 13-tap bloom pyramid; its
[celestial spheres](examples/traversable-wormhole-transit/celestial-spheres.js)
are a standalone GLSL chunk for the footprint-filtered galactic sky, resolved
star layers, and the analytic ringed planet a lensed ray lands on.

## Constraints

- Do not call a UV swirl “gravitational lensing.”
- Cap iterations and provide early termination.
- Use continuous crossing tests for thin structures.
- Keep numerical stability independent from frame rate.
- Separate the integrator from shading of the accretion disk or wormhole interior.
- Size the step from the local curvature scale, not from a global constant, once
  the metric has a narrow feature such as a lensing shoulder.
- Filter the background by the ray-bundle footprint. A lensed map compresses
  solid angle enough that a point sample aliases where the image is most
  interesting.
- Give capped rays a defined result. Their exit direction is arbitrary, so route
  them to a mean-radiance path rather than letting them speckle.
- Carry a transported frame, not a Cartesian camera, when the domain has no
  global Cartesian chart.
- Provide a cheaper approximation for non-hero views.

## Routing boundary

Use `$threejs-procedural-vfx` for ordinary particles, trails, plasma, and event
effects. This skill is for per-pixel numerical ray integration through curved
or bounded space-effect domains.

Progressive accumulation and the bloom pyramid shipped with the wormhole example
are owned by that renderer because the integration cost forces them. For a
scene-wide HDR bloom pass over ordinary geometry use `$threejs-bloom`, and for
exposure metering, tone-map ownership, and LUT grading use
`$threejs-exposure-color-grading`.
