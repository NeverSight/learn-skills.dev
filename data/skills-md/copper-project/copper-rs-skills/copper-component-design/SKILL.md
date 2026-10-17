---
name: copper-component-design
description: >-
  Recipe book for implementing a new copper-rs component — a `CuSrcTask`,
  `CuTask`, `CuSinkTask`, or `CuBridge`. Use when scaffolding a new crate under
  `components/` (or an app-local task): what the skeleton looks like, which
  lifecycle hooks to override, how to read the node's RON `config:` block, how
  to declare resource lifetimes, when `Freezable` needs a real impl vs the default.
  All patterns are anchored to real crates in `components/`. Complements
  `copper-arch` (traits + macro overview), `copper-api-flavor` (the taste
  rules for user-facing traits), and `copper-coding-style` (derives, error
  handling, no_std). For the RON side of the wiring see `copper-ron-config`; for
  build/verify commands see `copper-workflow`.
---

# copper-rs — component design recipes

`copper-arch` gives you four component roles. This skill is the practical answer to
"I'm about to implement one — what does a real one look like?" — with citations to
the canonical crates so you can open them side-by-side.

Trait anchors (**do not re-derive here**, cite them):

- `CuSrcTask` / `CuTask` / `CuSinkTask`, and `Freezable` (default is no-op) —
  `core/cu29_runtime/src/cutask.rs`
- `CuBridge` — `core/cu29_runtime/src/cubridge.rs`
- `Resources<'r>` model — `core/cu29_runtime/src/resource.rs` (canonical demo:
  `examples/cu_resources_test/src/resources.rs`)

Before writing anything new, read `copper-api-flavor` — the rules there (in-place
`&mut` outputs, `get_value` for enums, no cached inputs, payload/`Tov` placement,
no `Option`/nested-enum branching on the hot path, `CuTask` lifecycle) will get
enforced on review regardless of correctness.

## Cross-cutting checklist (applies to all four roles)

- `#[derive(Reflect)]` on the component struct is mandatory. Add
  `#[reflect(no_field_bounds, from_reflect = false, type_path = false)]` **only** when
  the struct is generic or holds opaque/FFI fields (e.g. `cu_mpu9250/src/lib.rs`,
  `cu_python_task/src/lib.rs`). Otherwise plain `#[derive(..., Reflect)]` (e.g.
  `cu_pid/src/lib.rs`).
- `impl Freezable for MyComp {}` is required even for stateless components — the trait
  bound is enforced. Stateless just gets the default no-op impl (`cutask.rs`).
- Payload types satisfy `CuMsgPayload` — see `copper-coding-style` for the derive
  set. Prefer reusing payloads from `components/payloads/cu_sensor_payloads/` when a
  standard type exists (IMU, image, point cloud) instead of inventing a new one.
- Use `cu29::units` types such as `Length`, `Area`, and `Ratio` for physical quantities
  in public payloads and APIs. Do not add bare numeric fields whose unit exists only in
  a name or comment, or create local unit wrappers.
- Reuse `CuRng` from `components/res/cu_rng/src/lib.rs` for randomized components and
  inject it through `CuRngBundle`/`Resources`. Do not implement a component-local PRNG
  or put a seed in a live message solely to make replay deterministic. If RNG progress
  affects later outputs, preserve equivalent progress in `freeze`/`thaw`; reseeding
  alone cannot resume a stream mid-run.
- Config extraction: `.get::<T>` for scalars, `.get_value::<T>` for anything
  structured or enum-shaped. See `copper-ron-config` for the rule.
- Do **not** stash inputs in `self` across cycles (api-flavor's no-cached-inputs
  rule). The copperlist already holds them.

**Stamping `tov`.** `Tov` means the **physical time of validity** of a measurement —
when the phenomenon was true in the world, not when the code ran. Three rules:

- It lives on the `CuMsg` envelope (`pub tov: Tov` in `cutask.rs`; the enum —
  `None`/`Time`/`Range` — is in `core/cu29_clock/src/lib.rs`), never in the payload
  (api-flavor's payload/`Tov` placement rule).
- Only a source stamps it. A `CuTask` propagates the input's stamp —
  `output.tov = imu_msg.tov;` (`cu_ahrs/src/lib.rs`). Re-stamping with `ctx.now()`
  downstream silently replaces the measurement's time of validity with processing
  time.
- Even in a source, a bare `ctx.now()` is imprecise — by the time `process` runs,
  the sample is already older than the sensor's internal sampling plus the bus
  transfer. Stamp from the sensor's own clock where the driver exposes one:
  `cu_hesai/src/lib.rs` derives per-point times from the lidar packet's own
  timestamps and stamps `Tov::Range` over the sweep. Where no sample clock is
  available, `ctx.now()` is the accepted best-effort fallback —
  `cu_mpu9250/src/lib.rs` does exactly that.

## `CuSrcTask` — sensors, data origins

Skeleton (adapted from `components/sources/cu_mpu9250/src/lib.rs`):

```rust
#[derive(Reflect)]
#[reflect(no_field_bounds, from_reflect = false, type_path = false)]
pub struct MySource<SPI, D> {
    driver: MyDriver<SPI, D>,       // hardware handle
    #[reflect(ignore)] cfg: MyCfg,  // opaque cfg struct
}

impl<SPI, D> Freezable for MySource<SPI, D> {}   // stateless: default is fine

impl<SPI, D> CuSrcTask for MySource<SPI, D>
where SPI: SpiBus<u8>, D: DelayNs,
{
    type Resources<'r> = MyRes<SPI, D>;
    type Output<'m>   = output_msg!(ImuPayload);

    fn new(cfg: Option<&ComponentConfig>, res: Self::Resources<'_>) -> CuResult<Self> {
        let settings = cfg.map(|c| c.get_value::<MyCfg>("settings")).transpose()?.flatten()
            .unwrap_or_default();
        Ok(Self { driver: MyDriver::new(res.spi.0, res.delay.0, &settings)?, cfg: settings })
    }

    fn start(&mut self, _ctx: &CuContext) -> CuResult<()> { self.driver.whoami() }

    fn process<'o>(&mut self, _ctx: &CuContext,
                   new_msg: &mut Self::Output<'o>) -> CuResult<()> {
        let raw = self.driver.read()?;
        // tov: prefer the sensor's own sample time — see Stamping `tov`
        // (cu_mpu9250 itself has no sample clock and falls back to ctx.now())
        new_msg.tov = Tov::Time(raw.sample_time);
        new_msg.set_payload(ImuPayload::from(raw));
        Ok(())
    }
}
```

**Lifecycle hooks in real sources:**

| Hook | Common use | Example |
|---|---|---|
| `new` | config parse + driver construction | `cu_mpu9250/src/lib.rs` |
| `start` | one-shot hardware validation (WHO_AM_I, calibration) | `cu_mpu9250/src/lib.rs` |
| `preprocess` | non-blocking readiness poll before `process` (streaming APIs) | no source in the tree uses it today; `cu_aligner` (task) and `cu_msp_bridge` (bridge) show the pattern |
| `process` | required — read hardware, `set_payload`, set `tov` | all sources |
| `postprocess` | update counters/stats not on the RT path | rare |
| `stop` | release fd / detach hardware | `cu_v4l`, `cu_vlp16`, `cu_rp_encoder` |

**Message shape:** `type Output<'m> = output_msg!(T);` for single, `output_msg!((A, B))`
for tuples. Always write via `&mut Self::Output<'o>`; **never** return payload by value
(api-flavor's in-place `&mut` output rule).

**Resources:** declare via the `resources!` macro (`cu_mpu9250/src/lib.rs`), then
extract handles in `new` (`res.spi.0`). Bind them from RON with
`resources: { spi: "board.spi0", ... }` — see `copper-ron-config`.

**Foot-guns**

- Blocking reads in `process` will drag the whole RT loop. Use `preprocess` to poll
  readiness and only `process` when data is ready.
- Forgetting `new_msg.tov = ...` leaves downstream tasks with a stale/`None` timestamp.
- Stamping `tov = ctx.now()` records when the driver ran, not the physical time of
  validity — stamp from the sensor's clock when the driver exposes one; `ctx.now()`
  is only a last-resort fallback (see **Stamping `tov`**).
- Tucking a timestamp into the payload struct instead of the envelope violates
  api-flavor's payload/`Tov` placement rule — `Tov` lives on `CuMsg`, never in the payload.

## `CuTask` — compute, filters, fusion

Skeleton (from `components/tasks/cu_ratelimit/src/lib.rs`):

```rust
#[derive(Reflect)]
pub struct CuRateLimit<T> { interval: CuDuration, last: Option<CuTime>, _p: PhantomData<T> }

impl<T> Freezable for CuRateLimit<T> {
    fn freeze<E: Encoder>(&self, e: &mut E) -> Result<(), EncodeError> { self.last.encode(e) }
    fn thaw<D: Decoder>(&mut self, d: &mut D) -> Result<(), DecodeError> {
        self.last = Decode::decode(d)?; Ok(())
    }
}

impl<T: CuMsgPayload> CuTask for CuRateLimit<T> {
    type Resources<'r> = ();
    type Input<'m>    = input_msg!(T);
    type Output<'m>   = output_msg!(T);

    fn new(cfg: Option<&ComponentConfig>, _r: Self::Resources<'_>) -> CuResult<Self> {
        let hz: f64 = cfg.and_then(|c| c.get::<f64>("rate").ok().flatten())
            .ok_or_else(|| CuError::from("cu_ratelimit: 'rate' Hz required"))?;
        Ok(Self { interval: CuDuration::from_secs_f64(1.0 / hz), last: None, _p: PhantomData })
    }

    fn process<'i, 'o>(&mut self, ctx: &CuContext,
                       input: &Self::Input<'i>, output: &mut Self::Output<'o>) -> CuResult<()> {
        let Some(p) = input.payload() else { output.clear_payload(); return Ok(()); };
        let now = ctx.now();
        if self.last.map_or(true, |t| now - t >= self.interval) {
            output.set_payload(p.clone()); self.last = Some(now);
        } else { output.clear_payload(); }
        Ok(())
    }
}
```

**Multi-input** (`components/tasks/cu_aligner/src/lib.rs`):

```rust
type Input<'m>  = input_msg!('m, f32, i32);   // tuple: (&CuMsg<f32>, &CuMsg<i32>)
type Output<'m> = output_msg!((CuArray<f32, N>, CuArray<i32, M>));
```

Index inputs by position: `input.0.payload()`, `input.1.payload()`.

**Stateful tasks that need real `Freezable`:**

- `cu_pid/src/lib.rs` — integral, last_error, elapsed, last_output
- `cu_ratelimit/src/lib.rs` — last tov
- `cu_peer_range_accumulator/src/lib.rs` — sample slot array
- `cu_aligner` — alignment buffer

Rule of thumb: if a field influences the next cycle's output, it must round-trip
through `freeze`/`thaw`. Otherwise resim after a keyframe will diverge.

When several structs each freeze a few named fields, the app-local
`impl_freezable_fields!` macro in `examples/cu_runtime_matrix/src/lib.rs` is a
copyable pattern (it is private to that example, not an SDK export).

**Foot-guns**

- Caching an input in `self` between cycles (api-flavor's no-cached-inputs rule).
  Re-read the input in each `process`.
- Not calling `output.clear_payload()` when suppressing output — stale payload leaks
  into the next cycle.
- Multi-rate inputs without a `cu_aligner`-style buffer produce mis-timed fusions.
- `deserialize_into` when `get_value("key")` would do — the whole `ComponentConfig`
  rarely maps 1:1 to one struct.

## `CuSinkTask` — actuators, terminal endpoints

Skeleton (from `components/sinks/cu_rp_gpio/src/lib.rs`):

```rust
#[derive(Reflect)]
pub struct RPGpio { #[reflect(ignore)] pin: LinuxOutputPin }

// `Owned<T>` takes no lifetime — only `Borrowed<'r, T>` does (`resource.rs`)
pub struct GpioResources { pub pin: Owned<LinuxOutputPin> }
// impl ResourceBindings<'r> for GpioResources { ... }

impl Freezable for RPGpio {}

impl CuSinkTask for RPGpio {
    type Resources<'r> = GpioResources;
    type Input<'m>    = input_msg!(RPGpioPayload);

    fn new(_cfg: Option<&ComponentConfig>, res: Self::Resources<'_>) -> CuResult<Self> {
        Ok(Self { pin: res.pin.0 })
    }

    fn process<'i>(&mut self, _ctx: &CuContext, input: &Self::Input<'i>) -> CuResult<()> {
        let Some(cmd) = input.payload() else { return Ok(()); };
        if cmd.on { self.pin.set_high(); } else { self.pin.set_low(); }
        Ok(())
    }
}
```

**Lifecycle hooks that show up in real sinks:**

- `new` claims the hardware handle from `Resources`.
- `start` opens/validates the device (e.g. `cu_zenoh_sink/src/lib.rs` opens the
  Zenoh session; `cu_rp_sn754410/src/lib.rs` enables the PWM outputs).
- `process` writes the payload — usually a small match on the command variant.
- `stop` closes fds / releases the handle.

Most sinks are stateless (`impl Freezable {}`). A buffering sink is the exception;
serialize the queue in `freeze`.

**Foot-guns**

- Blocking on a slow write (serial, network) stalls the RT loop; consider a background
  thread + ringbuffer if the sink can tolerate a small queue.
- Silently swallowing write errors — surface them via `CuError::new_with_cause`.

## `CuBridge` — bidirectional external transports

A bridge is **not** a source+sink pair. It owns a single transport session
(serial port, Zenoh session, CAN bus) and multiplexes Tx and Rx over that session in
one lifecycle. Trait: `cubridge.rs`.

Channel enums are declared via macros (`cubridge.rs`):

```rust
tx_channels! { state => StateMsg, [publish_empty] cmd => CmdMsg = "motor/cmd" }
rx_channels! { feedback => FeedbackMsg = "sensor/feedback", status => StatusMsg }
```

Each macro generates a typed channel enum plus a descriptor list. The RON side
declares matching channels — see `copper-ron-config`'s bridge section.

Skeleton (from `components/bridges/cu_msp_bridge/src/lib.rs`):

```rust
impl<S, E> CuBridge for CuMspBridge<S, E>
where S: SerialLike, E: MspError,
{
    type Tx = TxChannels;
    type Rx = RxChannels;
    type Resources<'r> = MspResources<S>;

    fn new(cfg, tx_channels, rx_channels, res) -> CuResult<Self> { /* wire session */ }
    fn preprocess(&mut self, _ctx: &CuContext) -> CuResult<()> {
        self.poll_serial()   // drain incoming bytes into pending batches
    }
    fn send<'a, P>(&mut self, ctx, ch, msg) -> CuResult<()> { /* match ch, transmit */ }
    fn receive<'a, P>(&mut self, ctx, ch, msg) -> CuResult<()> { /* pop batch → msg */ }
}
```

Cycle shape: `preprocess()` → `send()` × N → `receive()` × M → `postprocess()`.
`preprocess` is where transport-level I/O usually happens — a poll of the socket, a
drain of the serial buffer — so `send`/`receive` are cheap dispatches.

**When to reach for a bridge (vs. writing a matched source + sink pair):**

- Shared transport handle (a single Zenoh session, one serial port).
- Correlated bidirectional messaging (request/response batches — see MSP).
- Wire-format concerns spanning both directions (codec, framing).

Otherwise, an unrelated sensor input and command output are cleaner as a source and a
sink.

**Bridges in the tree worth reading:**

- `cu_msp_bridge` — request/response batching over serial, resource-backed.
- `cu_zenoh_bridge` — config-only, no hardware resources; `stop` closes the session.
- `cu_crsf` / `cu_bdshot` — protocol-heavy embedded transports.
- `cu_ros2_bridge`, `cu_iceoryx2_bridge` — external middleware.

**Foot-guns**

- Doing transport polling inside `send`/`receive` instead of `preprocess`. That
  couples per-channel dispatch to I/O timing.
- Not flushing pending buffers on `stop` — messages disappear on shutdown.
- Runtime channel type mismatches: `send`/`receive` do `downcast_ref`/`downcast_mut`
  (`cu_msp_bridge/src/lib.rs`); a mismatch is a codegen bug, not a bridge bug.
- Forgetting that bridges default `run_in_sim: true` (RON side; `config.rs`).
  If a real transport shouldn't run under sim, set it explicitly.

## Cross-cutting patterns table

| Concern | Source | Task | Sink | Bridge |
|---|---|---|---|---|
| Config parse | `get_value` in `new` | same | same | same + per-channel `config` |
| Resources | typical (hardware) | usually `()` | typical (hardware) | optional (session may be config-only) |
| I/O offload | `preprocess` polls readiness | upstream buffer | `preprocess` flush (rare) | `preprocess` drains transport |
| Stateful `freeze` | rare | common (filters, counters) | rare | common (pending batches) |
| Handle held in `self` | driver / fd | filter state | pin / port | session / parser |
| Where payload lives | `cu_sensor_payloads` or local | reuse or local transform type | local | batch/enum wrapper |

## Payload placement

- **Central** (`components/payloads/cu_sensor_payloads/src/lib.rs`): IMU, image, point
  cloud — reuse when a standard shape fits.
- **Local**: single-purpose payloads (`RPGpioPayload`, PID output). Keep them in the
  same crate as the component that authors them.
- **Handle-based**: large buffers wrap `CuHandle<CuSharedMemoryBuffer<u8>>` (see
  `CuImage`) to avoid per-cycle copies.
