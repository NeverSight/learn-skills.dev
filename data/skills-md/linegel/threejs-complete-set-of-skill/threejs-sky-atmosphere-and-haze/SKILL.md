---
name: threejs-sky-atmosphere-and-haze
description: Build sky, atmosphere, and haze in Three.js WebGPU/TSL. Use for authored sky/fog, planetary scattering, depth-aware aerial perspective, or atmosphere-derived sun/sky lighting.
---

# Sky, Atmosphere, and Haze

Build every branch around one atmosphere model, one scene-linear HDR path, and
one final-output owner.

## Process

### 1. Select the transport claim

Choose the least expensive branch that supports the requested observable:

| Need | Branch | Valid claim |
| --- | --- | --- |
| Regional authored sky, distance haze, or height haze | `SkyMesh` plus TSL fog/haze | Authored appearance in a bounded local frame |
| Real-time planetary sky and aerial perspective | Compact Hillaire-style LUTs | Approximate higher-order transport within measured error |
| Fixed atmosphere with stricter spectral/angular accuracy | Bruneton-style scattering orders or an offline solve | Accuracy demonstrated against the chosen reference |

Use the compact branch for changing cameras and suns. Use the higher-order
branch when its regeneration cost and higher-dimensional products fit the
actual workload. Keep an offline integrator as reference evidence rather than
visible-pixel runtime work.

**Complete when:** the implementation names one branch, its supported spatial
domain, its physical-versus-authored claim, and the error or visual criterion
that admits it.

### 2. Establish one model

Declare one length unit for radii, positions, and integration steps; store
extinction/scattering coefficients in its reciprocal unit so
`beta * ds` is dimensionless. Define the body or local frame, origin policy,
altitude model, sun direction convention, spectral/working basis, and whether
the solar source is normal irradiance or finite-disc radiance.

Initialize `WebGPURenderer`, await `renderer.init()`, and confirm the native
WebGPU backend before allocating compute/storage products. Use
`NoColorSpace` for transport data and keep radiance scene-linear until the
host output stage.

For physically dimensioned extinction, LUT radiometry, mapping equations, phase
conventions, product dependencies, imported LUT/product compatibility, or the
single unit-equivalence fixture, read
[references/atmosphere-transport.md](references/atmosphere-transport.md).

**Complete when:** every producer and consumer uses the same frame, length
conversion, sun convention, and radiometric basis; physically dimensioned
extinction also gives the same fixture optical depth on CPU and GPU.

### 3. Build products in dependency order

The authored local branch samples its sky and distance/height haze directly
from the shared model. It needs host depth only when haze is a separate
depth-aware post. For the compact LUT branch, allocate no product merely
because the branch was selected. Admit products by consumer:

| Product | Allocate only when |
| --- | --- |
| Transmittance | an admitted sky, aerial, or lighting path requires it directly or through a dependent product |
| Multiscatter | an admitted sky, aerial, or lighting closure includes higher-order response |
| Irradiance | an admitted diffuse-lighting consumer samples it |
| Sky-view | an admitted visible-sky consumer samples it |
| Aerial RGB inscattering and RGB optical depth | an admitted depth-aware composition consumer samples the paired payload |

A sky-only or lighting-only branch has no aerial allocation or aerial view
dependencies.

Give each product its own dependency key and last-update reason. Atmosphere
profile and body changes dirty base products. Camera body-relative pose,
projection, viewport, and depth mapping dirty aerial products. Camera yaw,
projection jitter, and a pure floating-origin translation leave unchanged
body-frame LUTs valid.

Write 2D products with `StorageTexture` and `textureStore()`; write 3D
products with `Storage3DTexture` and `storageTexture3D()`. Set formats,
filters, wrapping, and mip ownership explicitly. Treat
`renderer.computeAsync()` as submission, not GPU completion; synchronize
readback, reuse, and retirement with an actual completion mechanism.

**Complete when:** every sampled product names all of its physical and view
dependencies, no consumer can observe a newer dependency with an older
dependent product, superseded work cannot publish over the current model epoch,
every unadmitted product has zero allocation and no dependency state, and unchanged base LUTs survive camera-only changes.

### 4. Compose the selected branch

For an in-scene authored branch, attach the `SkyMesh` and TSL fog/haze to the
host scene and keep their output scene-linear.

For a separate depth-aware haze or LUT aerial branch, reuse the host scene
color and depth. Reconstruct the active perspective, reversed, logarithmic, or
orthographic depth convention into a metric segment, then intersect that
segment with the atmosphere and stop at the first opaque-body entry. Do not
resume integration in a far-side shell after the opaque interval. Classify sky
through explicit coverage or the declared clear-depth encoding.

For a visible surface in that branch, apply exactly:

```text
C_out = C_scene * T_segment + S_segment
```

For a sky pixel, sample sky radiance and the calibrated sun/moon disc. Keep
direct lighting, diffuse sky lighting, cloud shadows, opaque visibility, and
camera-segment transport as separate factors. Let either `renderOutput()` or
`RenderPipeline.outputColorTransform` own presentation.

For planetary bodies, exterior cameras, ellipsoids, non-perspective depth, or a
shell/post handoff, read
[references/body-depth-and-composition.md](references/body-depth-and-composition.md).

**Complete when:** each admitted in-scene branch reaches the host output path
once; each enabled depth-aware branch reconstructs known positions within the
declared tolerance, keeps sky/surface coverage stable, and returns `C_scene`
under the zero-atmosphere control; tone mapping/output conversion runs once.

### 5. Expose an admitted lighting handoff

When another system consumes atmosphere-derived lighting, expose only the
quantities it needs:

- sample time, model revision, physics frame/origin, support, filter, age, and
  error;
- sample-to-sun unit direction and disc angular radius;
- calibrated solar quantity, unit, and basis;
- either direct sun already attenuated by the atmosphere, or the unattenuated
  source plus atmosphere transmittance;
- directional sky radiance, normal-dependent sky irradiance, and whether each
  includes the direct disc;
- camera-segment RGB transmittance and RGB inscattering.

Clouds add cloud-only optical depth; geometry adds visibility; water adds its
own path extinction. A consumer chooses one atmosphere direct-light form and
applies each factor once.

**Complete when:** a visual-only branch has no unused lighting interface; every
admitted lighting consumer can identify quantity, unit, frame, sample age, and
included attenuation, and its factor trace proves that atmosphere, cloud,
geometry, water, and aerial transport each appear at most once.

### 6. Verify the selected branch

Verify the mechanisms that branch actually uses:

- LUT forward/inverse maps at texel centers, boundaries, horizon split, and
  azimuth seam;
- phase normalization and forward-lobe sign;
- optical-depth, radiance, and energy convergence against a higher-accuracy
  reference;
- body intersections and every enabled depth encoding;
- product invalidation under parameter, camera, jitter, viewport, and origin
  changes;
- fixed-view linear-HDR sky, horizon, night, surface-haze, and exterior-camera
  diagnostics;
- create, resize/tier-switch, completion, and disposal ownership.

**Complete when:** every enabled branch passes its numeric and visual gates,
every diagnostic names the product revision it displays, and repeated
resize/tier-switch cycles leave one live generation per retained product.

## Failure signatures

| Symptom | Inspect |
| --- | --- |
| Halo appears opposite the sun | phase direction sign |
| Haze changes with world scale | length/coefficient conversion |
| Horizon seam or limb pop | LUT seam, body interval, or owner transition |
| Terrain is darkened twice | direct-light or aerial factor ownership |
| Camera jitter regenerates base LUTs | dependency keys are too broad |
| Off-axis haze is too short | normalized depth was mistaken for ray distance |

## Routing boundary

This skill owns molecular/aerosol sky transport, atmosphere-derived sun/sky
lighting, and camera-segment aerial perspective. Use
`$threejs-volumetric-clouds` for weather-shaped cloud density and cloud-only
shadows, `$threejs-image-pipeline` for shared scene signals and final-output
ownership, `$threejs-exposure-color-grading` for metering/tone mapping, and
`$threejs-procedural-planets` for terrain/body detail.
