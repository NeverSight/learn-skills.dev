---
name: analyze-memory-snapshot
description: >-
  Analyze PyTorch CUDA memory snapshots from torch.cuda.memory._dump_snapshot(),
  torch.cuda.memory._snapshot(), or memory_viz artifacts. Use when the user
  wants to understand GPU memory usage, top allocation sites, deallocation
  timing, OOMs, allocator fragmentation, inactive cached memory, memory leaks,
  retained tensors, or Python reference cycles in PyTorch workloads. Supports
  diffing two snapshots from the same run to pinpoint growing allocation sites.
license: BSD-3-Clause
metadata:
  author: pytorch
  version: "1.0"
---

# Analyze Memory Snapshot

Analyze PyTorch CUDA memory snapshots by inspecting allocator state and event
history. Always prefer evidence from the snapshot over generic memory advice.

## Workflow

1. Get the snapshot path if the user did not provide one. Accept `.pickle`,
   `.pkl`, `.json`, or a directory containing rank-local snapshots. If the user
   only has a screenshot from memory_viz, ask for the underlying snapshot file.
2. Load the snapshot locally. PyTorch `_dump_snapshot()` files are pickles, so
   only unpickle files the user provided or that already live in the workspace.
   JSON snapshots can be loaded directly.
3. If available, run this skill's helper for a first-pass summary:

   ```bash
   python scripts/analyze_snapshot.py /path/to/snapshot.pickle
   ```

   If there are multiple ranks, run it per rank and compare peaks, active bytes,
   inactive bytes, OOM events, and top stack traces.

   If the user has (or can capture) two snapshots from different points in the
   same run, diff them — this converts leak hunting from interpretation into a
   lookup of which allocation sites grew:

   ```bash
   python scripts/analyze_snapshot.py step100.pickle --diff step200.pickle
   ```

   For very large snapshots (hundreds of MB of trace history), the helper caps
   trace analysis at `--max-trace-events` (default 1M) and reports how many old
   events it dropped, so it stays usable without loading everything into your
   analysis.
4. Read the raw snapshot when the helper output is insufficient. Inspect:
   - `segments`: allocator segments returned by `cudaMalloc`
   - `blocks`: live, awaiting-free, and inactive pieces inside each segment
   - `device_traces`: chronological allocation events when memory history was
     enabled
   - `frames`: stack traces for allocation sites
5. Report the memory picture in terms of allocator semantics:
   - **Reserved memory**: sum of segment `total_size`
   - **Live tensor memory**: blocks in `active_allocated`
   - **Delayed frees**: blocks in `active_awaiting_free`, often stream-related
   - **Inactive cached memory**: `inactive` blocks that PyTorch can reuse
   - **Requested vs rounded size**: `requested_size` versus block `size`

## What To Diagnose

**Where memory is going**

Group live `active_allocated` blocks by the most useful user frame. Report the
largest stack traces first, with bytes, percent of live memory, block count, and
representative file/function/line. Separate parameters, optimizer state,
activations, temporary buffers, communication buffers, and user containers when
the stack names make that clear.

Always attribute memory to the user's model code, not allocator or framework
internals. Snapshot stacks are dominated by frames inside
`torch/nn/modules/*`, `torch/autograd/*`, and `torch/optim/*`; skip past those
to the first frame in the user's own files and name the module or line that
owns the memory (for example "38% of live memory is activations of
`model.decoder.layers[*].mlp`, allocated at `modeling.py:214`"). Only fall
back to torch-internal frames when no user frame exists in the stack.

**When memory is deallocated**

Use `device_traces` to distinguish `free_requested` from `free_completed`.
Pending or delayed frees can mean tensors are still needed by another stream or
that work has not reached the free point yet. In multi-step traces, compare
repeated allocation sites with their matching free events: allocation sites that
appear every step without corresponding frees are stronger retention evidence
than one-time model or optimizer allocations. If traces include OOM events,
report the failed allocation size, `device_free`, OOM stack frame, and which live
allocation sites were holding memory immediately before the OOM.

**Leak and retention patterns**

Look for active bytes that grow across steps, repeated active allocations from
the same stack that are not freed, or a sawtooth where many tensors accumulate
and are released together. The strongest evidence is a two-snapshot diff
(`--diff` in the helper): an allocation site whose live bytes and block count
both grow between snapshots taken k steps apart is leaking or retaining.

Recognize these named patterns by their snapshot signature and give the
matching fix:

- **Retained autograd graph**: live activation blocks from step N still
  present at step N+k, often alongside a loss or output tensor per step.
  Typical cause is logging or accumulating a tensor that still holds the
  graph — fix with `loss.detach()` (or `.item()`) before appending, or find
  the `retain_graph=True` that keeps graphs alive.
- **Growing Python container**: same user-code allocation site with block
  count increasing linearly in steps. Fix by detaching and moving to CPU
  before appending, or bounding the container.
- **First-step optimizer state spike**: large `torch/optim/*`-attributed
  allocations appearing once at the first `optimizer.step()` and then stable.
  This is expected retention, not a leak — say so explicitly; the fix for OOM
  here is a smaller model/batch, a lower-memory optimizer, or sharding, not
  leak hunting.
- **Activation memory vs. checkpointing**: live memory dominated by forward
  activations that all free during backward (sawtooth in `device_traces`).
  Recommend activation checkpointing (`torch.utils.checkpoint`) and quantify
  the tradeoff from the snapshot: the activation bytes that would be freed
  versus recompute cost.
- **Gradient memory under DDP vs. FSDP**: full-size gradient and parameter
  blocks per rank suggest DDP replication; if the user is memory-bound and
  gradients+params+optimizer state dominate live memory, mention
  FSDP/ZeRO-style sharding as the structural fix.
- **Python reference cycles**: frees that only happen in bursts when GC runs.
  Recommend `from torch.utils.viz._cycles import warn_tensor_cycles` and call
  `warn_tensor_cycles()` during initialization to find object cycles that keep
  CUDA tensors alive.

**Fragmentation and allocator behavior**

Do not equate `nvidia-smi` usage with live tensors. PyTorch uses a caching CUDA
allocator, so reserved memory can be much larger than allocated tensor memory.
Large inactive blocks are reusable by PyTorch; `empty_cache()` may return fully
inactive segments to CUDA, but it does not free memory still occupied by live
tensors.

The most common confusing case is **OOM with plenty reserved**: the failed
request size exceeds the largest single contiguous inactive block even though
total inactive memory is larger. Diagnose it from the snapshot: compare the
OOM's requested size against the largest inactive block (the helper reports
"largest single reusable inactive block"), and check whether inactive memory
is split across many segments. When that pattern holds, recommend, in order:

1. `PYTORCH_ALLOC_CONF=expandable_segments:True` — lets segments grow instead
   of allocating new fixed-size ones; usually the highest-impact fix for
   fragmentation OOMs.
2. `PYTORCH_ALLOC_CONF=max_split_size_mb:<N>` — stops the allocator from
   splitting blocks above N MiB, reducing hard-to-reuse fragments; suggest N
   near the failing request size.
3. Reducing allocation-size churn in user code (varying batch/sequence sizes
   is a common cause; padding to fixed shapes helps).

State explicitly when fragmentation is *not* the problem — if live tensor
memory alone approaches device capacity, allocator tuning will not help and
the fix is model-level (batch size, checkpointing, sharding, precision).

**Non-PyTorch memory**

The snapshot only sees CUDA memory managed by the PyTorch allocator. NCCL,
custom CUDA extensions, cuDNN/cuBLAS workspaces, or direct CUDA allocations may
not appear. If device memory outside the snapshot is suspected, compare
`torch.cuda.device_memory_used(device)` or `nvidia-smi` with the snapshot's
reserved bytes.

## If The User Needs To Capture A Snapshot

Give the minimal capture pattern:

```python
import torch

torch.cuda.memory._record_memory_history(max_entries=100000)
try:
    run_your_code()
    torch.cuda.memory._dump_snapshot("memory_snapshot.pickle")
finally:
    torch.cuda.memory._record_memory_history(enabled=None)
```

Use a higher `max_entries` for long jobs, but warn that trace history has memory
overhead.

For OOM debugging, register an OOM observer so the snapshot is dumped
automatically at the moment of failure — the user should not have to reproduce
the crash twice:

```python
import torch


def dump_on_oom(device, alloc, device_alloc, device_free):
    torch.cuda.memory._dump_snapshot(f"oom_snapshot_dev{device}.pickle")


torch.cuda.memory._record_memory_history(max_entries=100000)
torch._C._cuda_attach_out_of_memory_observer(dump_on_oom)
```

For suspected leaks across training steps, capture a **pair** of snapshots —
one early (after the first optimizer step, so optimizer state is already
allocated) and one many steps later — then diff them with
`analyze_snapshot.py earlier.pickle --diff later.pickle`. Dumping at the same
point in the step (for example right after `optimizer.step()`) keeps the diff
free of within-step noise.

## Output Format

Start with the main finding in one sentence. Then provide:

1. Totals: reserved, live allocated, active-awaiting-free, inactive cached, and
   peak if trace history allows it.
2. Top allocation sites by live memory, with stack frames and percentages.
3. Deallocation timeline: frees completed, pending frees, delayed frees, and OOM
   events.
4. Diagnosis: name the matched pattern (retained graph, growing container,
   optimizer-state spike, activation pressure, fragmentation/caching,
   reference cycles, or non-PyTorch memory gap) and say which snapshot
   evidence supports it. Explicitly separate expected retention from leaks.
5. Concrete next steps: user-code locations to change (file:line from the
   snapshot stacks), the specific fix for the matched pattern, allocator
   settings to try when fragmentation is implicated, and what second snapshot
   to capture if the diagnosis needs a diff to confirm.

Be explicit about uncertainty. If the snapshot lacks history, say which
deallocation and peak questions cannot be answered from that artifact.
