---
name: threejs-exposure-color-grading
description: Meter and grade scene-linear Three.js WebGPU images. Use for choosing fixed or automatic exposure; adapting EV on the GPU; assigning tone-map and output conversion; or placing and validating 3D LUTs.
---

# Exposure And Color Grading

Keep the photographed signal scene-linear until the final image chain. One
declared owner controls each exposure group, tone map, and output conversion.

## 1. Lock the color contract

Name the scene-linear working primaries, radiance scale, alpha convention, and
every producer that enters the photographed signal. Convert irradiance through
the material/lighting model before metering radiance. Apply one shared physical
or perceptual radiance scale to lights, environment, atmosphere, emissive
materials, bloom sources, and optical effects.

Partition targets or views into exposure-control groups. A group may share GPU
state only when its radiance basis, exposure policy, and reset history are
identical; an automatic group also requires the same meter mask, key, and
sample schedule and one explicit source/combined aggregate. Independent images
with matching settings are not interchangeable meter inputs. Assign exactly
one exposure owner, one tone-map owner, and one output-conversion owner per
group.

**Complete when:** every photographed input has one basis and scale, and every
group names its members, exposure/tone-map/output owners, and state-sharing
policy.

## 2. Choose the cheapest meter that meets the image requirement

Choose in dependency order:

1. fixed EV for a controlled or calibrated view;
2. a stratified grid or tile sampler for ordinary global auto exposure;
3. exact full-pixel hierarchical reduction when every pixel or exact mask must
   contribute;
4. a log-luminance pyramid only when another feature consumes its levels or
   spatial statistics;
5. a histogram only when percentile clipping fixes a demonstrated outlier or
   bimodal-lighting failure.

Tap resolved, pre-bloom HDR by default. This keeps temporal noise out of the
meter and avoids bloom/exposure feedback. A different tap is an authored image
policy with a regression fixture.

Read [the color-pipeline reference](references/scene-referred-color-pipeline.md#meter-implementations)
when implementing sampled, exact, pyramid, or histogram metering; it contains
the weighted-log equations, traffic model, and small-emitter failure tests.

**Complete when:** fixed EV names its value/calibration and requires zero meter
source reads; otherwise one meter is selected, its source and mask are named,
and each cheaper rejected option has a concrete correctness failure.

## 3. Build the selected exposure controller

For fixed EV, bind the authored or calibrated value directly and allocate no
meter, reduction, target-publication, or adaptation state.

For automatic exposure, keep `targetEV`, `currentEV`, validity, and frame
indices in GPU state. Advance adaptation every rendered frame toward the last
valid target, even when the meter runs less often. Keep CPU readback
diagnostic-only.

Use this producer schedule only for automatic exposure:

```text
adapt currentEV from the last completed target
  -> render and present with currentEV
  -> reduce the new meter source
  -> publish targetEV for a later frame
```

Bind the source texture as a real node dependency and expose both the source
frame and state frame. Initialize or clear the source before the first
reduction. Read [GPU exposure state](references/scene-referred-color-pipeline.md#gpu-exposure-state)
for reduction state, EV adaptation, invalid aggregates, and r185 compute
semantics.

**Complete when:** fixed EV has zero metering/adaptation work, or an automatic
frame trace proves which source produced each target, adaptation remains
GPU-resident, and an invalid aggregate holds the prior valid target without a
CPU substitute.

## 4. Handle discontinuities before presentation

Give cuts an authored `hold`, `reseed`, or fixed-EV policy. Treat a radiance
basis, working-primary, quantity, nonlinear-normalization, or exposure-key
change as a new exposure epoch. For a pure positive scale change
`L_new = k * L_old` with otherwise identical semantics, preserve the displayed
product by shifting the fixed EV, or both automatic states, by `-log2(k)`:

```text
currentEV_new = currentEV_old - log2(k)
targetEV_new  = targetEV_old  - log2(k)
```

Convert normalization-dependent EV bounds too, or state that clamping breaks
preservation. This is not a shortcut for normal lighting changes. Discard queued
publications from a superseded epoch before they can overwrite converted state.

Every other incompatible change starts a new exposure epoch. Automatic
exposure resets meter accumulation and reseeds adapted state; fixed exposure
rebinds its authored value before the new signal is presented. Resize or DPR
changes rebuild only admitted resolution-dependent meter resources and sampling
coordinates. Device loss recreates and reseeds only admitted GPU state under
the new resource generation.

**Complete when:** every cut, invalid input, basis/scale change, resize, and
device-loss event maps to one conversion, hold, rebuild, or reseed action that
finishes before the affected frame is admitted, or to an explicit no-op because
the selected branch owns no affected state.

## 5. Compose one final-image chain

Use this domain order unless the LUT declares another complete contract:

```text
scene-linear HDR
  -> exposure
  -> tone map
  -> tone-mapped-linear LUT, when admitted
  -> alpha restoration
  -> output conversion
```

Unpremultiply before nonlinear RGB operations and premultiply afterward;
exposure preserves alpha. A scene-linear LUT needs a declared shaper. A
display-encoded LUT owns the exact output primaries and transfer function and
therefore sits after `renderOutput()`.

With explicit `renderOutput()`, set
`RenderPipeline.outputColorTransform = false`. Mark
`renderPipeline.needsUpdate = true` after changing the output node or output
ownership. Read [tone mapping and LUTs](references/scene-referred-color-pipeline.md#tone-mapping-and-luts)
only when loading, authoring, or placing a cube.

When a tone-mapped-linear cube is admitted, read
[the identity 3D-LUT example](examples/identity-3d-lut.mjs) for voxel ordering
and `Data3DTexture` configuration. Supply the device edge limit and byte budget;
the helper checks both before allocation. Its RGBA8 identity has a declared
quantization tolerance. It is a correctness fixture, not a look or performance
bypass.

**Complete when:** the graph contains one exposure multiply, one tone map, one
working-to-output conversion, and—only when admitted—one LUT placement in its
declared domain.

## 6. Prove the selected branches

Capture deterministic fixtures:

- for fixed exposure, a calibration card proving the authored EV and multiplier
  with zero meter source reads or adaptation state;
- for automatic exposure, a key-gray card with the expected target EV and a
  bright source entering and leaving frame with monotone target/current EV
  trajectories;
- for a sampled automatic meter, its mask, small-emitter, and cadence cases;
- for a histogram, its underflow, overflow, and accepted percentile interval;
- when a LUT is admitted, an identity LUT with ramps and saturated swatches in
  its declared domain;
- output isolation showing exactly one tone map and one output conversion.

Measure each admitted meter or LUT as a paired graph delta after warmup on the
target. GPU time is available only after post-init timestamp-query support is
proven; otherwise report the timing as unavailable.

**Complete when:** all applicable fixtures pass, the final image is inspected,
and each failed fixture identifies the meter, adaptation, LUT-domain, alpha, or
output-ownership cause.

## Routing

Use `$threejs-image-pipeline` for shared MRT, temporal history, adaptive DPR,
and transient lifetime; `$threejs-bloom` for glare source ownership; and
`$threejs-visual-validation` for fixed-view image evidence.
