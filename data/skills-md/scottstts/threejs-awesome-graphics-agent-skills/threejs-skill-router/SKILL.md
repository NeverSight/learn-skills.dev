---
name: threejs-skill-router
description: Route ambitious Three.js graphics work to the smallest expert skill set. Use for new visual experiences, graphics rewrites, reference matching, or requests spanning geometry, materials, atmosphere, shadows, temporal effects, and final image treatment.
---

# Three.js Visual Skill Router

Treat the model's Three.js knowledge and official documentation as prerequisites. Load only the expertise that changes the visual result.

This pack goes beyond procedural guidance: its working examples and supporting
assets contain much of its practical implementation value. When they are
relevant, give them particular attention.

## Route by the visual system being authored

| Required result | Load |
| --- | --- |
| shot composition, chase/side/orbit rigs, camera handoffs, projection ownership, pointer look, floating origins | `$threejs-camera-direction` |
| launch and docking timelines, procedural transform phases, springs, staging, rotating-frame alignment, debris motion | `$threejs-procedural-animation` |
| reusable scalar/vector fields, domain warping, causal masks, procedural normals | `$threejs-procedural-fields` |
| atlas-filtered blocks, planetary surfaces, hybrid texture-backed PBR soil/moss with procedural displacement and masks, ground and model moss accumulation, terrain wetness, deformable granular sand with mass-coupled grain shading, simulated tearable denim with implicit yarn mechanics and frayed fibres, woven cloth with GPU XPBD and yarn microstructure, simulated fur with interactive grooming and strand shading, lava/emissive surfaces, reflective wave-optical diffraction gratings, thin-film soap bubbles with Airy interference, raytraced diamond/gem refraction, dispersive glass transmission with internal reflection and volume absorption, deforming softbody jelly materials with XPBD mechanics and refractive caustics, authored frame PBR, specular AA | `$threejs-procedural-materials` |
| height-field ray marching, silhouette-aware POM, curved relief shells, relief self-shadowing | `$threejs-parallax-occlusion-mapping` |
| well-crafted and complete hard-surface object assemblies, procedural vehicles and humanoid robots, parameter-curve section tracks, tilted shell and spine lofts, pillow panels, exact polygon cuts, UV-owned apertures, spanwise airfoil lofts, sculpted rails/frames, branch rings, fin lofts, profile extrusion, inset, revolve, sweep, solidify, bevels and fillets, shell thickness, direct-topology apertures, semantic mesh writers, material slots and groups, primitive-built forms, coplanar flicker, loose/non-manifold geometry, detached parts, interpenetration, support, clearance and swept-envelope defects | `$threejs-procedural-geometry` |
| trees, surface-following ivy, painted vines, stylized grass, GPU-computed grass, GPU-culled virtual flower fields, distance-tiered plant geometry, roots, foliage, rooted wind deformation | `$threejs-procedural-vegetation` |
| buildings, façade grammars, profiles, ornaments, modular mesh writers | `$threejs-procedural-architecture` |
| planets, terrain, craters, biome fields, coastlines, spherical detail | `$threejs-procedural-planets` |
| sky scattering, planetary shells, depth-based aerial perspective | `$threejs-atmosphere-aerial-perspective` |
| weather-driven raymarched clouds and cloud shadows | `$threejs-volumetric-clouds` |
| FFT oceans, coastal breaker transitions, finite-volume shallow-water beach waves, signed-distance coastlines, shallow-water swash chains, wet sand, rock-impact spray, stylized above/below ocean optics, submerged Snell windows, total internal reflection, forward-refracted structures, pixel-footprint spectral LOD, aquatic perspective, caustic god rays, spectral cascades, choppy derivatives, Jacobian whitecaps | `$threejs-spectral-ocean` |
| photoreal shallow water with gravity-capillary FFT waves, dispersive caustics and diffraction glare, authored analytic waves, bounded heightfield pools, object ripples, differential-area caustics, ray-traced pool volume optics, shared normals, heuristic refraction, fallback absorption, crest foam | `$threejs-water-optics` |
| falling snow, snow accumulation, model snow caps, wet asphalt puddles, procedural ripple normals, splash flipbooks, rain streaks, shared weather envelopes, surface wetness | `$threejs-precipitation-surfaces` |
| curved-ray black holes, accretion disks, wormholes and throat transits, null-geodesic integration, lensed celestial spheres and star fields | `$threejs-raymarched-space-effects` |
| filmic HDR lens-flare compositors, highlight-derived radial ghosts, field-angle pupil deformation, spectral pupil rings, localized glare and bloom, raymarched aurora curtains, finite-footprint emissive slabs, uniform volume integration, equirectangular radiance probes, WebGPU voxel fire and smoke, volumetric fluid fields, mesh-surface emitters, SDF fire collisions, particles, trails, plasma, shockwaves, holographic projections, Fresnel rim shells, scanline banding, layered event effects | `$threejs-procedural-vfx` |
| accumulated screen frost, touch clearing, wet-window rain, view-aligned droplet refraction and blur | `$threejs-temporal-surfaces` |
| stable large-world shadows, cascades, clipmaps, cached updates | `$threejs-shadow-systems` |
| GTAO, bent normals, bilateral reconstruction | `$threejs-screen-space-ambient-occlusion` |
| HDR bloom and selective emission contribution | `$threejs-bloom` |
| eye adaptation, tone mapping, LUT grading, output color | `$threejs-exposure-color-grading` |
| shared depth/normal/velocity ownership and multi-pass ordering | `$threejs-image-pipeline` |
| fixed-view diagnostics, seed sweeps, temporal and budget evidence | `$threejs-visual-validation` |

## Execution order

For a new procedural scene:

1. Define a visual contract: subject, scale, camera distance, motion, and target frame budget.
2. Load `$threejs-camera-direction` when framing, lens, camera frame, or mode transitions affect the target.
3. Load the subject-generation skill.
4. Add `$threejs-procedural-animation` when object motion requires authored phases, moving frames, or spring convergence.
5. Add `$threejs-procedural-fields` when multiple visual channels must share coherent structure.
6. Add lighting/shadows and atmosphere only after silhouette and material masks read without effects.
7. Add `$threejs-image-pipeline` last.
8. Load only the atomic image effects actually needed.
9. Use `$threejs-visual-validation` for a deterministic evidence set.

## Routing constraints

- Do not load a skill for API setup alone. Inspect the installed Three.js version and use official docs.
- Do not route “make it beautiful” directly to post-processing. Find the missing authored system.
- Prefer one strong, inspectable visual rule over several independent noise layers.
- When adapting a supplied reference, preserve the mechanism that creates its character. Do not reduce it to a generic effect category.
- Keep object-space, world-space, and screen-space systems separate unless the composition explicitly requires coupling.
- If no retained skill matches, state that the pack lacks expert coverage for that system. Do not stretch the nearest skill to cover it.

## Acceptance gate

A routed task is incomplete until the implementation exposes:

- deterministic seed or reproducible inputs;
- visual debug modes for its controlling fields;
- parameters grouped by perceptual role;
- an intentional mechanism-backed quality or resolution tier when the system defines one;
- a no-post baseline that still reads.
