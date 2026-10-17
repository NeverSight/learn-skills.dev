---
name: copper-ron-config
description: >-
  Deep schema reference for `copperconfig.ron`. Use when reading, writing, or
  debugging a copper-rs config file: every top-level key, every per-task/per-cnx/per-bridge
  field, typed `ComponentConfig` accessor rules (`get` vs `get_value`), and the exact
  validation errors the parser emits. All claims cite
  `core/cu29_runtime/src/config.rs`. For the runtime architecture and task-graph mental
  model see `copper-arch`; for `fmtron` formatting and the `just fmt` cycle see
  `copper-workflow`; for the "how should a new config field feel" taste rules
  (enums via `Deserialize`, no stringly parsing) see `copper-api-flavor`.
---

# copper-rs — RON config schema reference

`copperconfig.ron` is a compile-time input to `#[copper_runtime(config = "...")]`. The
parser and graph model live in `core/cu29_runtime/src/config.rs`. This
skill is the field-by-field reference into that file. It does **not** cover how the
macro consumes the config (see `copper-macro-debug`), how the runtime executes it
(see `copper-arch`), or how to format it (see `copper-workflow`).

Authority: `config.rs` is the source of truth. When the wiki/book disagrees, the code
wins (see `copper-arch` skill's authority order).

## Top-level grammar (`CuConfigRepresentation`, `config.rs`)

| Key | Type | Required | Default | Purpose |
|---|---|---|---|---|
| `tasks` | `Vec<Node>` | no | `[]` | task/source/sink declarations |
| `cnx` | `Vec<SerializedCnx>` | no | `[]` | connections between nodes (and bridge channels) |
| `resources` | `Vec<ResourceBundleConfig>` | no | `[]` | HAL resource bundles bound to tasks/bridges |
| `bridges` | `Vec<BridgeConfig>` | no | `[]` | external-world bridges (ROS, Zenoh, protocol adapters) |
| `logging` | `LoggingConfig` | no | see below | slab/section sizing, keyframes, codecs |
| `monitor` / `monitors` | `MonitorConfig` or `Vec<MonitorConfig>` | no | none | monitoring tasks; singular alias accepted |
| `runtime` | `RuntimeConfig` | no | none | rate limiting + thread pools |
| `missions` | `Vec<MissionsConfig>` | no | single implicit `default` | multi-mission support |
| `includes` | `Vec<IncludesConfig>` | no | `[]` | modular composition of sibling RON files |

A valid graph needs at least one node. `type:` strings are Rust paths resolved at the
**binary crate root** — not by RON introspection.

## Task node (`Node`, `config.rs`)

| Key | Type | Required | Default | Notes |
|---|---|---|---|---|
| `id` | `String` | **yes** | — | unique in the graph |
| `type` | `String` | no | — | fully-qualified Rust path of the task struct |
| `kind` | `TaskKind` | no | inferred | `source`\|`task`\|`sink` (aliases `src`, `regular`/`cutask`, `snk`). Inference uses graph connectivity |
| `config` | `ComponentConfig` | no | `{}` | node-level RON config; see accessors below |
| `logging` | `NodeLogging` | no | `enabled=true` | per-node: `enabled`, `codec`, `codecs: {msg_type: codec}`, `handle_content` in `all`/`touched_only`/`none` |
| `missions` | `Vec<String>` | no | all missions | omit ⇒ task participates in every mission |
| `background` | `BackgroundConfig` | no | `false` | `true` for default pool, or `(pool: "name")` for a named pool |
| `resources` | `HashMap<String,String>` | no | none | local name → `"bundle_id.field"` binding |
| `run_in_sim` | `bool` | no | **false** for sources/sinks, ignored for regular tasks | when `false`, source/sink is stubbed under sim |

`kind` is optional: **omit it and the parser infers from graph connectivity** — a node
with no incoming edges is a `source`, no outgoing is a `sink`, otherwise `task`. Setting
`kind:` explicitly is a *contract* the validator then checks against connectivity, which
is where these errors come from — hence the "no declared inputs or outputs" case
fires when neither the explicit kind nor the connectivity can decide.

`kind` inference errors (grep-able strings): `"is declared as kind 'source' but has
incoming connections"`, `"is declared as kind 'task' but has no incoming
connections"`, `"is declared as kind 'sink' but has outgoing or NC
outputs"`, `"has no declared inputs or outputs, so Copper cannot infer"`.

## Connection (`SerializedCnx`, `config.rs`)

| Key | Type | Required | Notes |
|---|---|---|---|
| `src` | `String` | **yes** | task `id`, or `"bridge_id/rx_channel_id"` |
| `dst` | `String` | **yes** | task `id`, `"bridge_id/tx_channel_id"`, or `"__nc__"` for "output intentionally unused" |
| `msg` | `String` | **yes** | fully-qualified payload Rust path |
| `missions` | `Vec<String>` | no | omit ⇒ shared across all missions |

Bridge endpoint parsing lives in `config.rs` (`parse_endpoint`). `Rx` channels
must appear as `src`, `Tx` as `dst`; the reverse is an error
(`"channel '{}' is Tx and cannot act as a source"`, `"channel '{}' is Rx
and cannot act as a destination"`). `__nc__` works only with task destinations, not
bridge channels. Cnx order is preserved from RON for deterministic execution
(`order: usize`, `config.rs`).

## Logging (`LoggingConfig`, `config.rs`)

| Field | Default | Constraint |
|---|---|---|
| `enable_task_logging: bool` | **true** | master switch — off ⇒ empty logs |
| `slab_size_mib: Option<u64>` | unbounded | — |
| `section_size_mib: Option<u64>` | unbounded | must be `≤ slab_size_mib` |
| `keyframe_interval: Option<u32>` | **100** | interval **in CopperLists**, not wall time |
| `copperlist_count: Option<usize>` | unbounded | must be `> 0` if set |
| `codecs: Vec<LoggingCodecSpec>` | `[]` | each `(id, type, config?)`; ids must be unique |

`keyframe_interval` counts copperlists — at 1 Hz that's once per 100 s; account for
`runtime.rate_target_hz` when tuning.

## Monitor / Resources / Bridges / Missions / Includes

Monitor (`MonitorConfig`, `config.rs`): `(type: "...", config?: {...})`. Top-level
key is `monitor:` or `monitors:` (both accepted).

Resources (`ResourceBundleConfig`, `config.rs`):
`(id, provider, config?, missions?)`. Tasks/bridges bind fields via
`resources: { "local": "bundle_id.field" }`. Fields must match the provider's public
API — validated only at codegen, not at RON parse.

Bridges (`BridgeConfig`, `config.rs`):
`(id, type, config?, resources?, missions?, run_in_sim?, channels: [...])`. Channel
entries are `Rx(id, route?, config?)` or `Tx(id, route?, config?)`
(`BridgeChannelConfigRepresentation`). `run_in_sim` defaults **true** for
bridges — opposite of sources/sinks. Undeclared channel names are rejected
with `"Bridge '{}' does not declare a channel named '{}'"`.

Missions (`MissionsConfig`, `config.rs`): `(id: "name")`. Any node/cnx/resource
without a `missions:` list participates in **every** mission. When a cnx repeats
across includes its mission sets are **unioned**; a repeated task/bridge/resource
`id` is **first-wins** — the later duplicate is skipped entirely, missions included.

Includes (`IncludesConfig`, `config.rs`):
`(path, params?, missions?)`. `{{key}}` in the included file is textually substituted
from `params`. Paths starting with `/` are absolute; otherwise relative
to the parent config. Included tasks/cnx are appended to the parent.

## `ComponentConfig` accessors

Every `config: {...}` block deserializes to a `ComponentConfig` map (`config.rs`).
Reach for these three in order of increasing complexity:

- **`config.get::<T>("key")? -> Option<T>`** — scalars only (`bool`, integers,
  floats, `String`). Uses `TryFrom<&Value>`. Canonical use: `cu_ratelimit/src/lib.rs`.
- **`config.get_value::<T>("key")? -> Option<T>`** — anything
  `T: DeserializeOwned`. This is the **only** correct route for enums and nested
  structs. Canonical use: `cu_peer_range_accumulator/src/lib.rs`
  (`SampleRetentionConfig`), `cu_peer_triangulation/src/lib.rs`.
- **`config.deserialize_into::<T>()`** — rare; treat the whole
  ComponentConfig as one flat struct.

**Never write a `match s.as_str() { "reuse_last" => ... }` parser** — that violates the
API-flavor rule (see `copper-api-flavor`'s strong-typing rule). Enum fields must be real
Rust enums with `#[derive(Deserialize)]` and read via `get_value`.

## Validation errors (grep-able strings)

Every message below is emitted verbatim; grep in `config.rs` to find the site.

- Graph shape: `"Task '{}' is declared as kind 'source' but has incoming connections..."`,
  `"...kind 'sink' but has outgoing or NC outputs..."`,
  `"has no declared inputs or outputs, so Copper cannot infer"`.
- Connection targets: `"Source node not found: {}"`,
  `"Destination node not found: {}"`,
  `"NC destination '{}' does not support bridge channels..."`.
- Bridges: `"Bridge '{}' does not declare a channel named '{}'"`,
  `"channel '{}' is Tx and cannot act as a source"`,
  `"channel '{}' is Rx and cannot act as a destination"`.
- Sizing: `"CopperList count cannot be zero..."`,
  `"Section size...cannot be larger than slab size..."`,
  `"Duplicate logging codec id..."`.
- Runtime block: `"Runtime rate target cannot be zero..."`,
  `"exceeds the supported maximum of ... Hz"` (the cap is `MAX_RATE_TARGET_HZ` =
  1 GHz, interpolated into the message), `"Thread pool id cannot be empty"`,
  `"Thread pool '{}' must have at least 1 thread"`,
  `"real-time priority {} is out of range"`,
  `"niceness {} is out of range"`,
  `"has an empty affinity list"`.

## RON foot-guns

1. **`type:` is resolved at the binary crate root.** A re-export in a sibling
   `lib.rs` may not be visible; the macro reads the RON path as-is.
2. **Enum variants are snake_case.** Serde aliases exist for some (see `TaskKind`
   in `config.rs`), but the canonical form is `kind: source`, `background: (pool: "vision")`.
3. **`__nc__` only works for task destinations** — not bridge channels.
4. **`section_size_mib ≤ slab_size_mib` is asymmetric** — reversing is an error.
5. **`run_in_sim` defaults differ by node type:** `false` for sources/sinks,
   **`true`** for bridges. Regular tasks ignore the field entirely.
6. **`keyframe_interval` counts copperlists, not milliseconds.** With
   `runtime.rate_target_hz: 1`, `keyframe_interval: 100` → one keyframe every 100 s.
7. **Cnx missions merge; repeated ids don't.** A cnx repeated across includes ends
   up in the **union** of both mission lists — and if either side omits `missions:`
   (= all missions), the merge collapses to all missions. A task/bridge/resource
   repeated across includes is deduplicated **first-wins**; the later definition is
   silently skipped.
8. **Never hand-format RON.** `just fmt` runs `fmtron` and is enforced in
   `fmt-check` (see `copper-workflow`). Diffs from manual edits will fail CI.
9. **`monitor:` and `monitors:` are aliases** — either one parses, but a mixed file
   with both is confusing to readers. Pick one per repo.
10. **Resource-binding field names are validated at codegen, not at RON parse.** A
    typo in `resources: { pin: "board.gpi04" }` compiles the RON fine and dies later
    in the macro.

## Examples

Minimal (`examples/cu_min_baremetal/copperconfig.ron`):

```ron
(
    tasks: [
        ( id: "src", type: "tasks::FortyKSrc" ),
        ( id: "dst", type: "tasks::FortyKSink" ),
    ],
    cnx: [ ( src: "src", dst: "dst", msg: "crate::tasks::DoraPayload" ) ],
    logging: ( keyframe_interval: 10000, section_size_mib: 1 ),
)
```

Missions + resources + bridge (excerpt from
`examples/cu_resources_test/copperconfig.ron`):

```ron
(
    missions: [ (id: "A"), (id: "B") ],
    resources: [
        ( id: "board_a", provider: "crate::resources::BoardBundle",
          config: { "label": "alpha-bus", "offset": 10 }, missions: ["A"] ),
    ],
    tasks: [
        ( id: "sensor_a", type: "tasks::SensorTask", missions: ["A"],
          resources: { "counter": "board_a.counter", "bus": "board_a.bus" } ),
    ],
    bridges: [
        ( id: "stats_a", type: "bridges::StatsBridge", missions: ["A"],
          resources: { "bus": "board_a.bus" },
          channels: [ Rx(id: "stats_rx"), Tx(id: "stats_tx") ] ),
    ],
    cnx: [
        ( src: "sensor_a", dst: "stats_a/stats_tx",
          msg: "bridges::BusReading", missions: ["A"] ),
        ( src: "stats_a/stats_rx", dst: "inspector_a",
          msg: "bridges::BusReading", missions: ["A"] ),
    ],
)
```
