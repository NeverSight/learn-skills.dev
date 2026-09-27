---
name: migrate-max-v2-to-v3
description: >
  Use when migrating a MAX model from the V2 graph API (max.nn, TensorValue,
  explicit Graph construction) to ModuleV3 (max.experimental.nn, Tensor,
  F.lazy() + compile()). Triggers on: "migrate to ModuleV3", "port a max.nn
  model to max.experimental", "convert TensorValue to Tensor", "update my
  model to the V3 API", "ModuleV3 migration". Workflow: read the concept map,
  rewrite imports and __call__ signatures, replace graph building with
  compile(weights=...), align weight names with the new module hierarchy,
  move the KV cache unflatten into forward(), port sharding to a DeviceMesh
  when the V2 model is sharded, then verify greedy outputs match the V2
  implementation.
compatibility: Requires a MAX install (pip or pixi), the V2 model source to migrate, and a GPU to verify outputs.
metadata:
  argument-hint: "[path to your V2 model code, for example 'models/my_model.py']"
---

# Migrate a MAX model from V2 to ModuleV3

**Input**: the V2 model source to migrate (`$ARGUMENTS`).

ModuleV3 (`max.experimental.nn`) is the current MAX model API. A V2 model
builds an explicit `Graph` over `TensorValue` values with layers from
`max.nn`; a ModuleV3 model declares a `forward()` over `Tensor` values and
compiles with `F.lazy()` + `compile()`. Read
[references/v2-v3-basics.md](references/v2-v3-basics.md) first. It covers
`F.lazy()`, `compile(weights=...)`, dtype handling with `auto_cast`,
`forward()` vs `__call__()`, the distributed mapping, and the import
rules.

## Workflow

### 1. Confirm the model is V2

Classify by imports, and read the file when grep and the imports disagree.
V2 code imports its layers from `max.nn` and builds an explicit `Graph`
over `TensorValue`; ModuleV3 code imports `max.experimental.nn` and
subclasses its `Module`. Scoped greps shortcut the read:

```bash
grep -rn "max.experimental" <model-path>
grep -rEn "^\s*(from|import) max\.nn" <model-path>
```

Hits from the first mean the model is already (at least partly) V3 and
needs review, not migration. Hits from the second mean V2. Imports from
`max.graph` alone don't decide: V3 code keeps `TensorType` and
`DeviceRef` from `max.graph` for input specs. A file that hits both is
mixed; read it before migrating anything.

### 2. Keep the V2 code, add the V3 variant

Leave the V2 implementation untouched so it keeps working while the V3
variant is under construction. Put the V3 code alongside it: a
`<name>_modulev3` directory when migrating a registered architecture, or a
new module file when the model lives in your own package. When migrating a
registered architecture, name the V3 variant with the `_ModuleV3` suffix;
`max serve --prefer-module-v3` selects it while the V2 name keeps serving
by default.

### 3. Rewrite imports

```python
# REMOVE:
from max.graph import Graph, TensorValue, BufferValue, ops
from max.nn.layer import Module, LayerList
from max.nn.linear import Linear
from max.nn.norm.rms_norm import RMSNorm

# ADD:
from max.experimental import functional as F
from max.experimental.tensor import Tensor
from max.experimental.nn import Module
from max.experimental.nn.linear import Linear
from max.experimental.nn.norm import RMSNorm
from max.experimental.nn.sequential import ModuleList

# KEEP (TensorValue-free, shared with V2):
from max.nn.kv_cache import KVCacheParams, KVCacheParamInterface
from max.nn.attention import MHAMaskVariant
```

- `TensorType` and `DeviceRef` stay from `max.graph`; they define input
  specs, not graph values.
- `max.nn` imports are fine when the imported class doesn't use
  `TensorValue`.
- `PagedCacheValues` comes from
  `max.experimental.nn.common_layers.kv_cache` for the V3 type. `max.nn`
  exports a `PagedCacheValues` of its own, an alias for the V2 input type
  without `from_upstream()`; import from the `max.experimental` path so
  the V3 type wins.

### 4. Rewrite the module surface

- `__call__()` becomes `forward()`.
- `TensorValue` and `BufferValue` become `Tensor`.
- `Module` takes the call signature:
  `class MyModel(Module[[Tensor, ...], tuple[Tensor, ...]])`. Prefer
  specific types; use `...` only when `forward()` has `*args`.
- Layer constructors take keyword args and drop `dtype=` and `device=`;
  V3 uses default dtype and device contexts, and `model.to(device)` moves
  the module after construction.
- `LayerList` becomes `ModuleList` from `max.experimental.nn.sequential`.
  `ModuleList` subclasses `list`, so it takes a single iterable:
  `ModuleList(layers)`; `ModuleList(*layers)` raises `TypeError`.
- Parameters are plain `Tensor` objects; create them with `Tensor.zeros()`,
  `max.experimental.random.*`, and friends.

### 5. Rewrite operations

`ops.*` becomes `F.*` (`ops.gather()` → `F.gather()`). Most shape ops are
methods on `Tensor`: `reshape()`, `transpose()`, `permute()`, `squeeze()`,
`unsqueeze()`, `split()`, `cast()`. `flatten()` is the exception; it's
functional-only (`F.flatten(tensor, start_dim)`).

### 6. Replace graph building with `compile()`

V2:

```python
nn_model = MyModel(config)
nn_model.load_state_dict(state_dict)

with Graph("my_model", input_types=input_types) as graph:
    outputs = nn_model(*graph.inputs)
    graph.output(*outputs)

model = session.load(graph, weights_registry=state_dict)
```

V3:

```python
with F.lazy():
    nn_model = MyModel(config)
    nn_model.to(device)

model = nn_model.compile(*input_types, weights=state_dict)
```

- `F.lazy()` wraps construction, recording weight tensors symbolically;
  the checkpoint passed to `compile(weights=...)` replaces them.
- Weight keys are strict: a mismatched key is an error.
- A dtype mismatch between a parameter and its loaded tensor raises by
  default. Pass `auto_cast=True` to permit safe dtype casts.
- Call the compiled model directly (`model(tokens, ...)`). Compiled outputs
  are `Tensor` objects; code that consumed `Buffer` outputs reads the
  buffer via `.driver_tensor`.

### 7. Align weight names with the compiled hierarchy

`compile(weights=...)` resolves names from the root compiled module's
attribute hierarchy. When migration introduces or renames wrapper
attributes, checkpoint key mappings must follow: a root module storing
`self.language_model = ...` needs every inner weight prefixed with
`language_model.`. After migrating, check that every state-dict key is a
valid attribute path from the root module.

Tied embeddings need explicit handling: conditionally create `lm_head`, and
multiply by `embed_tokens.weight.T` in `forward()` when
`tie_word_embeddings` is set. Keep one copy of the shared weight in the
state dict.

### 8. Move the KV cache unflatten into `forward()`

The KV cache parameter types stay in `max.nn`; the values type has a V3
home in `max.experimental.nn.common_layers.kv_cache`. Use the methods on
`kv_params` plus `PagedCacheValues.from_upstream()`:

```python
def forward(self, tokens: Tensor, ..., *variadic_args: Tensor):
    kv_inputs = iter(arg._graph_value for arg in variadic_args)
    symbolic_inputs = self.kv_params.unflatten_kv_inputs(kv_inputs)
    kv = PagedCacheValues.from_upstream(symbolic_inputs, tokens.mapping)
```

You need the `._graph_value` extraction: `variadic_args` arrive as
`Tensor` objects while the unflatten methods expect raw graph values. For
sliding plus global attention, declare `MultiKVCacheParams` and use
`unflatten_basic_kv_tree()`, wrapping each tree with its own
`PagedCacheValues.from_upstream()`.

### 9. Port sharding when the V2 model is sharded

V2 sharding sets a `ShardingStrategy` on each layer and calls
`.shard(devices)` to get a per-device module list. V3 puts a `DeviceMesh` on
the model and a placement mapping on each weight:

```python
from max.experimental.nn.common_layers.linear import row_parallel
from max.experimental.sharding import DeviceMesh

model.mesh = DeviceMesh(devices, (n_devices,), ("tp",))
linear = row_parallel(Linear(in_dim, out_dim))
```

`col_parallel()` and `row_parallel()` set which mesh axis each weight
dimension shards over; there is no per-device module list. `Signals` and
`.shard()` have no V3 equivalent: keep those imports only when the class
is TensorValue-free, or drop the multi-GPU path from the V3 variant and
revisit when V3 grows an equivalent.

### 10. Verify against V2

Run both implementations on the same inputs and compare greedy tokens
(and logits where convenient); identical outputs confirm the migration.
Run mypy over the migrated module; V3 leans on the
`Module[[...], ...]` signatures, so type errors surface real migration
bugs.

## Reference implementations

The registered architectures ship as readable Python source in the
installed MAX package, under `max/pipelines/architectures/`. The V3
migrations to read:

- Single-GPU V3: `olmo3/`, `gpt_oss_modulev3/`, `llama3_modulev3/`
- Sharded V3: `kimik2_5_modulev3/`, `gemma3_modulev3/`, `deepseekV3_modulev3/`
- V2 for comparison: `gpt_oss/`, `llama3/`

## When there is no `Tensor` equivalent

Some V2 layers and ops have no `Tensor` equivalent yet. The options, and the
wrapper pattern for bridging a `TensorValue` helper into a `Tensor` API, are
in [references/v2-v3-basics.md](references/v2-v3-basics.md).
