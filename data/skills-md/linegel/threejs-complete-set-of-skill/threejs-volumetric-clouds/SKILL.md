---
name: threejs-volumetric-clouds
description: Build volumetric clouds in Three.js WebGPU/TSL. Use for weather-shaped density, bounded cloud raymarching, cloud optical-depth shadows, cloud-specific temporal reconstruction, or causal cloud precipitation emission.
---

# Volumetric Clouds

Build a bounded volume whose broad mass comes from weather-scale causes, whose
fine detail erodes that mass, and whose optical, shadow, and temporal errors are
measurable.

## Process

### 1. Select the claim and workload branches

State the claim first. Procedural weather, coverage, shape, and detail usually
form an authored appearance model. Beer-Lambert attenuation is physical for the
declared density and coefficients. Dual-lobe phase fits, octave
multiple-scattering compensation, powder, and simple ground bounce remain
approximations until validated against a transport reference.

Select each independent workload branch:

| Decision | Select | Evidence |
| --- | --- | --- |
| Local versus broad | full-resolution scissored march for a small projected bound; reduced-resolution march for broad coverage | complete-branch GPU cost and image error |
| Full versus reduced current grid | full current grid for low reuse; reduced grid plus reconstruction for coherent broad clouds | current-sample, bandwidth, and reconstruction error |
| Dense versus sparse | bounded adaptive march for dense occupancy; conservative macrocell DDA for sparse occupancy | saved samples exceed hierarchy build/traversal cost |
| Receiver shadow | none when no external receiver queries cloud shadow; full-column 2D optical depth for ground/opaque receivers; short sun march or depth-aware light product for in-cloud samples | admitted receiver query and transmittance error |
| Precipitation | appearance-only cues; or causal liquid/ice emission consumed by `$threejs-rain-snow-and-wet-surfaces` | dimensioned emission, support, transport delay, and conservation error |

For causal precipitation, publish liquid and ice mass flux in `kg m^-2 s^-1`,
or interval-integrated areal mass in `kg m^-2`, explicitly identified with its
sample time, sample interval, physics frame/origin, physical support,
area/Jacobian convention, fall delay or transport model, owner, contract
version, generation, validity, conservation gate, and error. Publish each
interval once to `$threejs-rain-snow-and-wet-surfaces`. The receiver converts
flux to interval mass once, preserves the declared support/Jacobian, and applies
the declared delay or transport before accumulation.

A density/emission recipe, incompatible physics frame/origin mapping,
support/Jacobian convention, or delay model change starts a new generation.
The receiver rejects stale or incompatible generations and never reinterprets
prior interval mass. An appearance-only branch remains visual-only and
publishes no receiver input.

Allocate no receiver-shadow product for the `none` branch.

**Complete when:** all five decisions name the selected representation and its
observable; every admitted workload has a falsifiable cost or error gate; a
`none` receiver-shadow branch records no receiver consumer and zero allocation;
appearance-only precipitation publishes no receiver input; causal precipitation
has one dimensioned generation accepted by one compatible consumer.

### 2. Define one optical and motion model

Choose dimensionless shape density with `beta_s` and `beta_a` in
`length^-1`, or physical mass density with mass-specific coefficients. Keep
the convention end to end:

In the equations below, beta names the coefficient matched to rho: inverse
length for shape density, or area per mass for physical mass density.

```text
sigma_s = rho * beta_s
sigma_a = rho * beta_a
sigma_t = sigma_s + sigma_a
tau = integral sigma_t ds
T_step = exp(-sigma_t*ds)
DeltaL = T_acc * (j/sigma_t) * (1-T_step)
```

Use the zero-optical-depth limit `DeltaL = T_acc*j*ds`, selected by
`sigma_t*ds` rather than the coefficient alone, with stable expm1/series
evaluation. Here `j` is source radiance per length. For direct light, distinguish finite-disc radiance, which
needs a solid-angle integral, from a declared collimated irradiance convention.

Normalize phase so `2*pi*integral_-1^1 p(mu)dmu=1`. Let
`rayDirection` point camera-to-sample and `toSun` sample-to-sun; then
`mu=dot(toSun,rayDirection)` makes `mu=1` forward scattering. Keep
dual-lobe weights nonnegative with unit sum.

Define one physics/render frame conversion, one metre scale, one cloud state
clock, and one macro air velocity. Integrate velocity over elapsed simulation
time; treat relative weather/shape/detail motion as bounded offsets from that
macro advection.

**Complete when:** a homogeneous slab is invariant to step partition and
reaches the zero-extinction limit, phase quadrature normalizes with the expected
forward direction, and two update cadences integrate the same motion trace
within tolerance.

### 3. Build bounded, conservative density

Keep active layers separate through altitude/profile, weather, shape, optical
properties, and motion. Let a low-frequency weather field and compact vertical
profile establish cloud mass. Apply shape at resolvable scales. Use detail as
height-dependent erosion; it may roughen occupied boundaries but must preserve
the weather/base-shape empty set used by the conservative bound.

Integrate one macro offset and add bounded relative offsets:

```text
macroOffset += integral u_air(t) dt
weatherOffset = macroOffset + relativeWeatherOffset
shapeOffset   = macroOffset + relativeShapeOffset
detailOffset  = macroOffset + relativeDetailOffset
```

Intersect rays with the selected spherical shell, slab, OBB, or sparse-volume
domain, then clamp the far end to the nearest opaque scene depth. Merge occupied
altitude ranges and skip only their complementary gaps. For horizontal
sparsity, build max-density macrocells that include weather, profiles, shape,
warp reach, and every density-increasing operation. Average mips are appearance
filters, not occupancy bounds.

Read [references/density-and-marching.md](references/density-and-marching.md)
for density equations, domain intersections, conservative skipping bounds, and
step selection.

**Complete when:** a debug view proves every skipped interval/cell is empty or
inside the declared omitted-radiance bound, and brute-force versus accelerated
marches agree on transmittance, HDR radiance, and first-contribution depth.

### 4. March and light the selected representation

Write current scene-linear cloud radiance, transmittance, and the depth data
needed by the selected temporal branch. Bound steps by optical depth, resolved
field bandwidth, cell/layer exits, opaque depth, and the remaining cloud
interval. Terminate only when remaining source and background-attenuation error,
plus already accumulated skip error, fit the output gate.

On Three.js r185, run `await renderer.init()` and require
`renderer.backend.isWebGPUBackend === true` before allocating or submitting
compute/storage work. Then submit `Fn().compute(count)` through
`renderer.compute()`. Use `StorageTexture` for 2D current/history/shadow
products and `Storage3DTexture` only for writable volume fields. Treat
`computeAsync()` as enqueueing rather than a completion fence. A
`PassNode.setResolutionScale()` scales the whole pass, so keep the host scene
at its required resolution and place reduced clouds in their own pass/resources.

Compute cloud self-shadowing from cloud optical depth only. A ground receiver
can use the full sun-ray column. An in-cloud sample needs optical depth from its
own position, supplied by a short sun march, deep-opacity slices, or another
depth-aware representation.

Read
[references/lighting-and-shadows.md](references/lighting-and-shadows.md)
when the task includes scattering, atmosphere-derived light, phase fitting,
cloud shadows, or shadow filtering.

**Complete when:** step-halving and higher-light-sample controls fit the linear
HDR error gate, the cloud-off control returns unit transmittance and zero cloud
radiance, and each admitted shadow query decodes optical depth from its actual
receiver position.

### 5. Reconstruct broad clouds

For a reduced broad-coverage branch, store opacity-weighted representative
depth and depth spread:

```text
w_i = T_i * (1-T_step_i)
z_bar = sum(w_i*s_i)/sum(w_i)
variance_z = sum(w_i*(s_i-z_bar)^2)/sum(w_i)
```

Use one representative surface only for a unimodal contribution distribution.
Use front depth plus moments or split histories for broad/multiple layers.
Reproject an advected representative physical point into the previous camera.
Record immutable current-render-to-physics and
previous-physics-to-render transforms; map through them across an origin
rebase. Host surface velocity is a different signal.

Blend with frame-rate-independent current response:

```text
alpha_current = 1-exp(-dt/responseTime)
resolved = alpha_current*current + (1-alpha_current)*clippedHistory
```

Reject history outside the viewport or across depth/spread mismatch, camera
cuts, projection changes, weather/topology discontinuities, encoding changes,
resolution/tier changes, or a missing/incompatible previous origin mapping.
Raise current response for disocclusion and low confidence. Reject invalid
samples before arithmetic. Variance-clip premultiplied linear HDR radiance and transmittance separately, then upsample only interval-compatible
transport; a mean/front depth cannot remove a hidden rear contribution.

Read
[references/temporal-reconstruction.md](references/temporal-reconstruction.md)
when history, sparse phases, depth encoding, reset policy, or upsampling is in
scope.

**Complete when:** a translating-density control reprojects to the expected
previous pixel, a mapped floating-origin rebase preserves that pixel,
camera-cut/topology/incompatible-origin controls give history confidence zero,
measured ghost decay matches the response model, and depth-edge upsampling does
not cross the opaque surface.

### 6. Integrate the lighting and image handoffs

Choose one incident-light contract:

- an authored source that declares owner, revision, sample time and age, frame,
  quantity, unit, basis, direction or angular support, filter, included
  attenuation, validity, and error; or
- atmosphere lighting that declares the same tuple.

For the atmosphere branch, choose either direct light already attenuated by the
atmosphere or an unattenuated source plus atmosphere transmittance. Multiply
each admitted cloud-only transmittance and opaque-visibility factor separately.
Keep directional sky radiance distinct from hemispherical sky irradiance.

Composite clouds before the host tone map. This transfer applies to its modeled
interval; overlapping atmosphere/cloud media need a coupled or validated
interleaved camera-path solve, not two serial whole-segment haze composites:

```text
C_out = L_cloud + T_cloud * C_scene
```

Use one `WebGPURenderer` and one host `RenderPipeline`. Write data resources
with explicit format/filter/mip policy and `NoColorSpace`. Let the host
`renderOutput()` or `outputColorTransform` own the one display conversion;
mark the pipeline dirty after replacing a diagnostic output node.

**Complete when:** the incident source has a complete contract, an attenuation
trace accounts for every admitted atmosphere, cloud, and geometry factor once,
cloud buffers remain linear HDR, and toggling clouds off returns the identical
host image path.

### 7. Verify the system

Verify:

- homogeneous-slab transfer, zero-extinction limit, and phase normalization;
- bounds, opaque-depth clamp, conservative skipping, and early-exit error;
- fixed-seed weather mass, erosion, octave filtering, and advection continuity;
- each admitted ground or in-cloud shadow decoder, cadence, and stale-product
  rejection;
- for causal precipitation, flux-to-interval integration, conserved mass under
  cadence repartition and physical-support/Jacobian area repartition, declared
  delay-to-arrival mapping, and stale-generation rejection; the appearance-only
  control publishes no receiver input;
- for each admitted temporal branch, translating density, depth encoding,
  history rejection, response time, and depth-aware upsample, including mapped
  and incompatible origin rebases;
- fixed-view HDR radiance, transmittance, silhouette, and halo against a
  higher-quality reference;
- create, GPU completion, disposal, and each admitted resize/tier-switch or
  history-reset lifecycle.

**Complete when:** every selected branch passes its numeric, temporal, visual,
and lifecycle gates, and diagnostics identify each retained density, shadow,
history, and causal-precipitation generation.

## Failure signatures

| Symptom | Inspect |
| --- | --- |
| Porous smoke or boiling | weather mass cause, detail erosion, octave filter, or shared advection |
| Brightness changes with step count | source units or transfer integration |
| Cost scales with camera far plane | volume bound or opaque-depth clamp |
| Density disappears under skipping | stale/nonconservative majorant |
| Camera-motion trails | representative depth, cloud velocity, or rejection |
| Flat/detached ground shadow | receiver representation, projection, or age |
| Color changes after cloud toggle | duplicate tone map or output transform |

## Routing boundary

This skill owns weather-shaped cloud density, bounded cloud transport,
cloud-only optical-depth shadows, and cloud-specific reconstruction. Use
`$threejs-sky-atmosphere-and-haze` for molecular/aerosol transport and the
shared sun/sky source, `$threejs-image-pipeline` for scene signals and final
output, `$threejs-rain-snow-and-wet-surfaces` for causal precipitation
transport and receiver accumulation, and `$threejs-scalable-real-time-shadows`
for opaque-geometry shadow maps.
