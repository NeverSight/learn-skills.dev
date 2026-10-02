---
name: threejs-spectral-ocean
description: Synthesize broad-band offshore seas with spectral FFT cascades in Three.js WebGPU/TSL. Use for homogeneous directional wind sea or swell, transported foam history, bounded CPU surface queries, or offshore forcing of a separate coastal model.
---

# Spectral Ocean

Build a dimensioned random sea from directional variance density to one
displaced, shaded surface. The spectral domain is a horizontally homogeneous
periodic patch with one mean depth and one dispersion relation per cascade.

## 1. Gate the representation

Choose from the required observable, not the desired look:

| Observable | Owner |
| --- | --- |
| A few authored modes or exact cheap CPU queries | Parametric waves in `$threejs-water-optics` |
| Bounded disturbances or explicit walls | Bounded heightfield in `$threejs-water-optics` |
| Broad stochastic directional sea | This spectral FFT skill |
| Depth-varying refraction, diffraction, breaking, run-up, or wet/dry fronts | Coastal branch in `$threejs-water-optics`; this skill may supply offshore forcing |
| Overturning, entrained air, jets, or three-dimensional vortices | External free-surface solver |

Select FFT cascades only when the visible wavelength band contains enough
independent modes that direct summation is more expensive or visibly
repetitive. Record the visible wavelength interval, footprint, tolerated
phase/slope error, periodic repeat distance, interaction needs, and measured
storage budget.

**Complete when:** one row owns every required water observable, and every
rejected row has a stated validity or cost reason.

## 2. Freeze the spectral convention

Use metres, seconds, radians per metre, and radians per second. Declare:

- stable horizontal physics frame and water datum;
- patch length, resolution, `Delta k`, represented radial band, and guard band
  for every cascade;
- inverse-transform sign, normalization, and centered-index correction;
- gravity, mean depth, surface tension, density, and uniform current;
- spectrum family, direction convention, seed, and cascade power windows;
- one coefficient/state clock and one render-surface owner.

The required inverse convention is

```text
f[j] = sum_n F[n] exp(+i 2 pi n dot j / N).
```

If the implementation uses a normalized inverse, rescale coefficient
initialization rather than tuning the sea afterward. Current is a separate
water velocity and Doppler term; atmospheric wind never becomes water current.

For wind sea, record the sampled wind vector, reference height, averaging
window and footprint, profile/drag calibration, stability treatment, fetch,
forcing duration or wave age, spreading model, and represented source terms.
Retarget a statistical state continuously; gusts may affect spray but do not
reseed mature waves.

Load only the reference sections for
[environment forcing](references/spectral-cascade-ocean-system.md#environment-forcing),
[wavevector and transform convention](references/spectral-cascade-ocean-system.md#wavevector-and-transform-convention),
and [dispersion and dimensional spectrum](references/spectral-cascade-ocean-system.md#dispersion-and-dimensional-spectrum)
while freezing this contract.

**Complete when:** every coefficient and clock has unambiguous units, the same
transform convention appears in initialization and validation, and replaying
one forcing snapshot reproduces the same coefficients and phase.

## 3. Build deterministic cascades

Load the reference sections for
[cascade power and deterministic coefficients](references/spectral-cascade-ocean-system.md#cascade-power-and-deterministic-coefficients),
[displacement and derivative spectra](references/spectral-cascade-ocean-system.md#displacement-and-derivative-spectra),
[packing and inverse FFT](references/spectral-cascade-ocean-system.md#packing-and-inverse-fft),
and the [transform gate](references/spectral-cascade-ocean-system.md#transform-gate).
When implementing or changing the transform, import or adapt the
[FFT convention oracle](scripts/fft-convention-oracle.mjs). Feed every
`makeConventionFixtures()` spectrum through the implementation, then pass its
`measureTransform()` metrics and caller-declared gates to `applyTolerances()`
before loading the production spectrum. The CPU oracle is deliberately limited
to sizes 8/16/32, rejects invalid numeric inputs and empty gates, and reports
zero-reference relative errors explicitly; it is not a production FFT cap.

For directional angular-frequency variance density `S_omega`,

```text
P(k_x,k_z) = S_omega(omega(k),theta) |d omega/dk| / |k|,
[P] = m^4.
```

Include `Delta k_x Delta k_z` in discrete coefficient variance. Power windows
obey `sum_c w_c(k)=1` over the represented band; smooth overlap uses
`sqrt(w_c)` on amplitude. Generate normals from
`(seed,cascade,signed_mode_x,signed_mode_z)` on the same physical grid so
centered storage shifts do not reseed surviving modes.

Evolve the intrinsic Hermitian pair and apply uniform-current advection as a
common phase. Its two stationary-chart frequencies differ; query velocity
bounds retain both. Construct derivatives in wavevector space,
then transform height, horizontal displacement, slopes, and displacement
derivatives. Treat DC and self-conjugate Nyquist cells explicitly before any
division.

**Complete when:** directional normalization, power-window sum, target versus
realized variance, coefficient determinism, Hermitian partner error, DC, both
axis bins, an oblique bin, a conjugate pair, every Nyquist parity case, CPU-DFT
error, Parseval error, and post-IFFT imaginary leakage all pass declared
gates.

## 4. Assemble one exact surface

Load only [exact displaced geometry](references/spectral-cascade-ocean-system.md#exact-displaced-geometry)
for the composite tangent, velocity, sampling, and fold rules.

Sum all cascade fields before nonlinear geometry. For

```text
P(q) = (q_x + chi D_x, h, q_z + chi D_z),
```

derive both parametric tangents from the summed displacement and set the normal
to `normalize(cross(P_qz,P_qx))`. Compute the full horizontal Jacobian,
including the mixed derivative. These compact formulas hold chi constant;
spatial or temporal variation adds its product-rule terms. A nonpositive
determinant is a fold, not a normal-map defect. Production guard bands remove
Nyquist lines; parity-only transform fixtures do not prove resolved geometry.

Choose the sign of `chi` with the one-mode criterion: under the positive
inverse convention, `h=a cos(kx)` and positive choppiness must produce
`X=x-chi a sin(kx)`, compressing the crest.

Geometry must resolve the represented displacement band. Filter or omit modes
that its footprint cannot resolve, and report their height/slope contribution.
One mesh/material owns every displayed location.

**Complete when:** the one-mode travel and displacement signs are correct;
analytic tangents and normals match finite differences; combined variance and
minimum Jacobian are measured; folds are counted; and position, normal,
velocity, foam, and temporal consumers read the same immutable state pair.

## 5. Add only represented optional state

### Foam

When foam is enabled, load only the
[foam](references/spectral-cascade-ocean-system.md#foam) section.

Build one source from combined-cascade compression, Jacobian evolution,
curvature, or a calibrated breaking proxy, then evolve one bounded history.
Declare Lagrangian parameter storage, Eulerian advection, or conservative
density transport. Source, transport, reaction, diffusion, and display
coverage remain separately inspectable.

### Queries

When CPU queries are enabled, load only the
[CPU queries](references/spectral-cascade-ocean-system.md#cpu-queries) section.

Retain a deterministic coefficient subset on CPU. Expose parameter-coordinate
sampling separately from physics-horizontal sampling. Choppy Eulerian queries
invert `X(q)=x`; the omitted-mode bound, inversion residual, numeric error, and
GPU probe discrepancy stay separate. The frame path performs no synchronous
map readback.

### Optics

When `$threejs-water-optics` is installed and available, invoke it for Fresnel,
refraction, Beer-Lambert, and receiver-caustic rules. Surface geometry,
derivatives, foam, and optics then share one cause and one final output
transform. When it is unavailable, report `missing optics owner` and keep
optics outside this implementation and its claims.

**Complete when:** each enabled option has an owner, validity interval,
support/filter, reset rule, and failure diagnostic; disabled options allocate
no state and make no claim.

## 6. Couple a coast only when required

When the sea feeds a depth-varying or wet/dry owner, load only the
[coastal donor](references/spectral-cascade-ocean-system.md#coastal-donor)
section and its phase-resolved, phase-averaged, and ownership subsections.
Before either solver runs, record the spectral donor, coastal consumer, and
forcing, reaction, render-surface, and foam owners; SI units; common physics
frame/origin and water datum; clock, sample instant or transfer interval,
cadence, and sample phase; band support, filter, and quadrature; validity,
staleness, and error; and donor/receiver state and resource versions. Keep
atmospheric forcing, mean current, wave transfer, and coastal reaction as
separate signals. Reset dependent boundary, query, foam, geometry, and temporal
state after a clock discontinuity, rebase, incompatible version,
representation change, or ownership change. Invoke `$threejs-choose-skills` if
the composed route still lacks one owner per observable.

Choose exactly one:

- **Phase resolved:** transfer elevation and depth-integrated discharge with
  common phase, intrinsic frequency, sample instant, band identity, and error.
  Prescribe only the incoming characteristic; retain the coastal outgoing one.
- **Phase averaged:** transfer dimensioned wave action/energy, intrinsic
  frequency, group velocity, current, direction, quadrature, and band identity.
  The receiver separately owns local display phase.

The FFT remains the offshore donor. It does not gain refraction, diffraction,
breaking, run-up, or wet/dry ownership by sampling bathymetry in its material.
Coherent donor/receiver copies use one spatial render owner; power windows apply
only to independent or orthogonal bands.

**Complete when:** producer, consumer, interval, sample phase, units, support,
filter, validity, staleness, error, state versions, reflection scope, and
render/foam ownership are explicit; single-mode normal and oblique tests close
phase, elevation, discharge or action, transmitted power, and reflection.

## 7. Integrate and verify the GPU path

Load only [WebGPU and performance](references/spectral-cascade-ocean-system.md#webgpu-and-performance)
for backend, resource, dispatch, precision, and lifecycle requirements.

Initialize `WebGPURenderer` before checking its backend or limits. Use
`StorageTexture` data with `NoColorSpace` and explicit precision. A global
producer/consumer dependency crosses a dispatch boundary. Select a validated
global ping-pong FFT—Stockham autosort or explicit-bit-reversal radix-2—or
workgroup-resident rows from transform correctness, initialized device limits,
occupancy, traffic, and sustained timing.

Render through one `RenderPipeline` and one output transform. Keep coefficient,
resolved-map, foam, query, and presentation generations immutable while a
render lease consumes them; resize, seed, spectrum, cadence, representation, or
origin changes either migrate compatible state or reset all dependent history.

Report actual allocations, peak live bytes, dispatches, precision comparison,
warm sustained timings, and fixed-camera final/no-foam/no-detail/no-post
captures for each named target.

**Complete when:** the initialized backend and selected limits are recorded;
all numerical gates above pass; no frame-critical readback exists; lifecycle
rebuild/dispose reaches an allocation plateau; and the final image has one
surface owner and one output transform.
