---
name: accel-pytorch-code-porting
description: 代码层：在本机加速平台上编写/移植/调试/运行 PyTorch 应用代码——CUDA→平台 API 映射、设备探测抽象、AMP 与数值稳定、分布式、第三方包兼容、迁移审计清单，适用任意厂商平台。Use ONLY when writing, porting, reviewing, debugging, or running application code for the local accelerator platform. 正文为当前已验证实例（现 MUSA/CUDA→MUSA 映射表）；非该平台首次初始化时先按头部「如何特化」改写正文。Python 环境与包装机用 accel-pytorch-python，系统层安装用 accel-platform-install。触发词：移植、torch.cuda 改写、设备探测、is_available、分布式后端、算子兼容。
---

# Accelerator PyTorch Code Porting（代码层，名称永不变）

## 如何特化本 skill（初始化时改写正文，不改名）

> 下方正文是**当前已验证实例**（MUSA / MTT S5000，2026-09，面向 CUDA↔MUSA 双平台代码库）。在其他平台首次初始化时按 accel-init 阶段 3 的调研结论改写；改写后本 skill 即该平台版本。已装机器不追仓库新版。

1. API 映射表是本层核心：换成本平台与 CUDA 的真实对照（设备字符串/可见设备变量/通信后端/显存 API/厂商 smi），逐行验证后再写。
2. 生态兼容节（Transformers/加速库：上游原生/厂商 fork/不支持）与扩展编译节按本平台实况重写，附证据链接。
3. 设备探测 helper、AMP、分布式、排障、迁移清单的结构保留，内容换本平台验证过的。
4. 平台名只出现在内容里；本机事实写宿主机层。

This skill guides Python/PyTorch development on the local Moore Threads MTT
S5000 platform. It is intended for CUDA-centric repositories that need one
maintainable codebase across NVIDIA CUDA and Moore Threads MUSA.

Related global skills have distinct ownership:

- `accel-pytorch-python`: Python environments, package indexes, and wheel
  compatibility;
- the host-layer skill (local `<host>-environment` / `system-profile`): this
  server's installed Toolkit paths, driver, hardware,
  and dynamic-library diagnosis;
- `accel-platform-install`: portable driver/Toolkit installation on another
  Ubuntu 22.04 host.

Repository instructions remain authoritative. Read the active repository's
`AGENTS.md`, environment documentation, and experiment rules before editing or
running anything. Never use this skill to bypass a repository's restrictions on
GPU runs, data preparation, artifact paths, commits, or pushes.

## 1. Local Platform Facts

Validated on `worker31069` on 2026-09-02:

| Component | Local value |
|---|---|
| Accelerator | 8 x MTT S5000, 81920 MiB each |
| Host driver | `3.3.5-server` |
| MUSA ToolKit / `mcc` | selectable `4.3.5` and `5.2.0` |
| muDNN / MCCL | `3.1.5` / `2.1.5` and `3.4.0` / `2.4.0` S5000 |
| Python | `3.12.14` base |
| PyTorch / `torch_musa` | not installed locally |
| Distributed backend | one- and two-GPU MCCL smoke validated |
| Host visibility variable | `MUSA_VISIBLE_DEVICES` |

The vendor PyTorch build currently registers `torch.musa` when `torch` is
imported. Shared cross-platform code should still avoid an unconditional
`import torch_musa`, because that breaks ordinary CUDA/CPU environments.

Optional compatibility/performance packages are not currently installed in the
local environment: `torchada`, Triton, bitsandbytes, flash-attn, and MATE.
Do not generate code that depends on them until the target environment has been
checked and the user has chosen to install a version matched to this MUSA stack.

## 2. Core Migration Policy

Use this order of preference:

1. **Backend-neutral PyTorch plus a small device abstraction** for maintained
   application code. Prefer `.to(device)`, `torch.autocast(device_type=...)`,
   and helper functions for synchronization, memory, and seeding.
2. **Explicit MUSA implementation behind one platform boundary** when behavior
   or kernels differ. Preserve the CUDA implementation and shared algorithm.
3. **torchada for a large legacy CUDA codebase** only when it is installed,
   version-compatible, imported at the entry point before CUDA-dependent
   modules, and tested end to end. It is an adapter, not proof that every CUDA
   kernel is correct on MUSA.
4. **Native MUSA extension or pure PyTorch fallback** for unsupported custom
   CUDA extensions. Do not silently skip a required op or pretend a CUDA wheel
   works.

Do not mechanically replace every `cuda` string. First classify each occurrence
as one of:

- device selection;
- visibility/resource ownership;
- AMP or memory API;
- distributed backend;
- CUDA-only package or extension;
- kernel/architecture assumption;
- documentation or artifact metadata;
- a genuine NVIDIA-only path that must remain unchanged.

Keep platform differences in one helper/module whenever possible. Do not fork
whole model, quantization, training, or experiment trees for MUSA.

## 3. Environment Check Before Coding

Run from the intended environment, without loading a model:

```bash
mthreads-gmi
musaInfo
mcc --version
python --version
python - <<'PY'
import importlib.metadata
import torch

print("torch:", torch.__version__)
print("torch_musa:", importlib.metadata.version("torch-musa"))
print("torch.version.musa:", getattr(torch.version, "musa", None))
print("musa available:", hasattr(torch, "musa") and torch.musa.is_available())
print("musa devices:", torch.musa.device_count() if hasattr(torch, "musa") else 0)
print("mccl available:", torch.distributed.is_backend_available("mccl"))
PY
```

If `torch.musa.is_available()` is false, check the driver, MUSA ToolKit, the
matching `torch`/`torch_musa` wheels, `MUSA_HOME`, `PATH`, and
`LD_LIBRARY_PATH`. Do not debug application code until the runtime is healthy.

Do not install a CUDA-pinned `requirements*.txt` unchanged on this host. MUSA
PyTorch wheels and vendor libraries must match the installed driver/toolkit.
Installing an ordinary public PyTorch wheel can replace the MUSA build and pull
NVIDIA runtime packages.

## 4. Device Detection and Backend Abstraction

For new cross-platform code, use a helper such as:

```python
import os

import torch


def accelerator_type() -> str:
    if hasattr(torch, "musa") and torch.musa.is_available():
        return "musa"
    if torch.cuda.is_available():
        return "cuda"
    return "cpu"


def accelerator_device(index: int | None = None) -> torch.device:
    kind = accelerator_type()
    if kind == "cpu":
        return torch.device("cpu")
    if index is None:
        index = int(os.environ.get("LOCAL_RANK", "0"))
    return torch.device(kind, index)


def set_accelerator_device(index: int) -> torch.device:
    device = accelerator_device(index)
    if device.type == "musa":
        torch.musa.set_device(device)
    elif device.type == "cuda":
        torch.cuda.set_device(device)
    return device
```

Important rules:

- Prefer `tensor.to(device)` and `model.to(device)` over `.cuda()` or `.musa()`.
- A MUSA tensor has `tensor.device.type == "musa"`, never `"cuda"`.
- Replace checks such as `device.type == "cuda"` with
  `device.type in ("cuda", "musa")` only when the branch truly supports both.
- Do not use `torch.cuda.is_available()` as a generic GPU check. It remains false
  on MUSA, including when torchada is used.
- Do not select MUSA from a hostname. Detect runtime capability.
- If both backends could be present, use the repository's documented priority;
  do not change it implicitly.

### CUDA-to-MUSA API map

| CUDA-centric code | Native MUSA equivalent |
|---|---|
| `torch.device("cuda", i)` | `torch.device("musa", i)` |
| `x.cuda()` | `x.to(device)` preferred; `x.musa()` is MUSA-only |
| `torch.cuda.is_available()` | `hasattr(torch, "musa") and torch.musa.is_available()` |
| `torch.cuda.device_count()` | `torch.musa.device_count()` |
| `torch.cuda.set_device(i)` | `torch.musa.set_device(i)` |
| `torch.cuda.current_device()` | `torch.musa.current_device()` |
| `torch.cuda.synchronize()` | `torch.musa.synchronize()` |
| `torch.cuda.empty_cache()` | `torch.musa.empty_cache()` |
| `torch.cuda.memory_allocated()` | `torch.musa.memory_allocated()` |
| `torch.cuda.memory_reserved()` | `torch.musa.memory_reserved()` |
| `torch.cuda.max_memory_allocated()` | `torch.musa.max_memory_allocated()` |
| `torch.cuda.max_memory_reserved()` | `torch.musa.max_memory_reserved()` |
| `torch.cuda.Stream/Event` | `torch.musa.Stream/Event` |
| `torch.cuda.manual_seed()` | `torch.musa.manual_seed()` |
| `torch.backends.cuda.*` | inspect the exact need; muDNN controls live under `torch.backends.mudnn` |
| `CUDA_VISIBLE_DEVICES` | `MUSA_VISIBLE_DEVICES` on this host |
| `backend="nccl"` | `backend="mccl"` |
| `nvidia-smi` | `mthreads-gmi` |

Do not assume CUDA allocator environment variables such as
`PYTORCH_CUDA_ALLOC_CONF` control MUSA memory. Use them only if the installed
vendor documentation explicitly says so; otherwise record them as irrelevant
to the MUSA process.

## 5. Minimal Single-Device Program

```python
import torch


def main() -> None:
    if not hasattr(torch, "musa") or not torch.musa.is_available():
        raise RuntimeError("MUSA is unavailable in the active PyTorch runtime")

    device = torch.device("musa", 0)
    torch.musa.set_device(device)

    model = torch.nn.Linear(1024, 1024).to(device=device, dtype=torch.bfloat16)
    optimizer = torch.optim.AdamW(model.parameters(), lr=1e-3)
    inputs = torch.randn(8, 1024, device=device, dtype=torch.bfloat16)

    optimizer.zero_grad(set_to_none=True)
    with torch.autocast(device_type="musa", dtype=torch.bfloat16):
        loss = model(inputs).float().square().mean()
    loss.backward()

    grad_norm = torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
    if not torch.isfinite(grad_norm):
        raise FloatingPointError(f"Non-finite gradient norm before Adam: {grad_norm}")
    optimizer.step()
    torch.musa.synchronize()
    print({"device": str(device), "loss": float(loss), "grad_norm": float(grad_norm)})


if __name__ == "__main__":
    main()
```

This is a platform smoke, not evidence that a real model, fused op, attention
backend, optimizer, or multi-hour training run is stable.

## 6. AMP and Numerical Stability

Use the backend-neutral AMP APIs:

```python
device_type = device.type
with torch.autocast(device_type=device_type, dtype=torch.bfloat16):
    output = model(inputs)
    loss = criterion(output, targets)
```

For fp16 training when scaling is needed:

```python
scaler = torch.amp.GradScaler(device.type)

with torch.autocast(device_type=device.type, dtype=torch.float16):
    loss = model(inputs).loss
scaler.scale(loss).backward()
scaler.unscale_(optimizer)
grad_norm = torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm)
if not torch.isfinite(grad_norm):
    raise FloatingPointError("Non-finite gradient norm before optimizer.step()")
scaler.step(optimizer)
scaler.update()
```

BF16 usually does not need gradient scaling. Keep the scientific precision
recipe unchanged during initial porting; change dtype only after isolating a
real unsupported or unstable path.

Do not infer backward correctness from a successful forward. For a new model or
operator, separately verify:

1. finite forward outputs and loss;
2. finite incoming and accumulated gradients;
3. finite gradient norm before clipping;
4. finite gradients after clipping;
5. finite parameters and optimizer moments after the step;
6. finite and noncollapsed exported state.

Fail before `optimizer.step()` when incoming gradients or the returned clipping
norm are non-finite. A finite scalar loss is insufficient.

### Local verified attention limitation

On this exact S5000/MUSA 5.2/PyTorch 2.9.1 stack, Qwen3.5-2B binary-code QAT
with Transformers SDPA produced NaN gradients during attention backward. The
same P0/data/seed/recipe completed 20 steps with eager attention. For that
validated path, select eager **before model construction**:

```python
config = transformers.AutoConfig.from_pretrained(model_path)
config._attn_implementation = "eager"
model = transformers.AutoModelForCausalLM.from_config(config)
```

or, when supported by the loader:

```python
model = transformers.AutoModelForCausalLM.from_pretrained(
    model_path,
    attn_implementation="eager",
)
```

Do not mutate attention mode only after modules are built. Do not generalize
this local Qwen3.5 finding into a claim that all MUSA SDPA forward/backward paths
are broken; test each model/runtime combination.

## 7. Transformers and Accelerate

Treat Hugging Face portability as something to verify, not assume.

- Pass an explicit `torch.device("musa", index)` or move the constructed model
  with `.to(device)` for the first single-device port.
- `device_map="auto"`, Accelerate dispatch hooks, quantized loaders, and offload
  code often contain CUDA-specific branches. Audit them before enabling.
- Do not set `dispatch=True` merely because a GPU exists; confirm the dispatch
  implementation supports MUSA.
- Record the requested and resolved attention implementation.
- Use native `torch.optim.AdamW` / Transformers `adamw_torch` first. CUDA-only
  bitsandbytes paged/fused optimizers require a MUSA-compatible build and are not
  installed in the current environment.
- FlashAttention, xFormers, Triton kernels, BitBLAS, Apex, DeepSpeed fused ops,
  and vendor-specific quantization packages need explicit MUSA support. Keep a
  pure PyTorch fallback when practical.
- Validate model load, one forward, one backward, optimizer step, save, and a
  fresh-process reload as separate gates.

When a config controls implementation choice, set it before
`from_config()`/`from_pretrained()`. Record what the created submodule actually
resolved, not only the CLI request.

## 8. Multi-GPU with MCCL

This host has validated 1/2/8-rank MCCL all-reduce. A generic DDP entry point:

```python
import os

import torch
import torch.distributed as dist


def main() -> None:
    local_rank = int(os.environ["LOCAL_RANK"])
    torch.musa.set_device(local_rank)
    device = torch.device("musa", local_rank)

    dist.init_process_group(backend="mccl", init_method="env://")
    try:
        model = build_model().to(device)
        model = torch.nn.parallel.DistributedDataParallel(
            model,
            device_ids=[local_rank],
            output_device=local_rank,
        )
        train(model, device)
    finally:
        dist.destroy_process_group()


if __name__ == "__main__":
    main()
```

Launch from the shell or scheduler-owned wrapper:

```bash
MUSA_VISIBLE_DEVICES=0,1 \
torchrun --standalone --nproc-per-node=2 train.py
```

Rules:

- `MUSA_VISIBLE_DEVICES` selects physical cards and renumbers them logically.
  Inside the process, `LOCAL_RANK=0` uses logical `musa:0`.
- Do not map `LOCAL_RANK` back to a physical ID.
- The scheduler/launcher owns visibility. Worker commands should not overwrite
  it unless the launcher contract explicitly says they should.
- `CUDA_VISIBLE_DEVICES` alone does not restrict MUSA devices on this host.
- Use one process per GPU. Avoid `DataParallel`; prefer DDP.
- Check `torch.distributed.is_backend_available("mccl")` before launch.
- Ensure every rank reaches collectives in the same order and always destroys
  the process group after success or failure.
- Use `DistributedSampler`, call `sampler.set_epoch(epoch)`, and make rank-zero
  artifact writes explicit.
- FSDP, tensor parallel, pipeline parallel, checkpoint sharding, and elastic
  recovery need their own S5000 preflight. A successful MCCL all-reduce does not
  prove those higher layers.

For code intentionally kept CUDA-shaped through torchada, `nccl` may be mapped
to MCCL. For native MUSA code, use `mccl` explicitly so runtime behavior is
auditable.

## 9. Memory, Timing, and Performance

Use native memory APIs through a backend helper:

```python
def synchronize(device_type: str) -> None:
    if device_type == "musa":
        torch.musa.synchronize()
    elif device_type == "cuda":
        torch.cuda.synchronize()


def max_memory_allocated(device: torch.device) -> int:
    if device.type == "musa":
        return torch.musa.max_memory_allocated(device)
    if device.type == "cuda":
        return torch.cuda.max_memory_allocated(device)
    return 0
```

- Synchronize before and after timing asynchronous GPU work.
- Record both allocated and reserved peak memory.
- Do not use `empty_cache()` as an OOM strategy inside the hot loop. Fix tensor
  lifetime, batch size, checkpointing, or the algorithm.
- Avoid constructing dense intermediate matrices whose size scales as
  `samples x codebook x dimension`. Chunk or stream the computation.
- Validate DataLoader `pin_memory`, nonblocking transfers, multiprocessing, and
  persistent workers on the actual MUSA runtime before treating them as a
  performance optimization.
- First establish correctness with native PyTorch ops. Add fused/vendor kernels
  one at a time with numerical and backward checks.

Performance parity and numerical parity are different. A correct eager fallback
can be accepted before a faster MATE/Triton/custom-kernel path is introduced.

## 10. CUDA Extensions and Third-Party Packages

### Native MUSA extension

The torch_musa extension interface mirrors CUDAExtension but uses MUSA tools:

```python
from setuptools import setup
from torch_musa.utils.musa_extension import BuildExtension, MUSAExtension

setup(
    ext_modules=[
        MUSAExtension(
            "my_ops",
            sources=["bindings.cpp", "kernel.mu"],
            extra_compile_args={"cxx": ["-O3"], "mcc": ["-O2"]},
        )
    ],
    cmdclass={"build_ext": BuildExtension},
)
```

CUDA assumptions that need review include `.cu` sources, `nvcc`, `CUDA_HOME`,
`sm_XX`, CUDA headers, `at::cuda`, `c10::cuda`, CUDA streams, cuBLAS/cuDNN/NCCL,
and architecture-specific intrinsics.

`torch_musa.utils.simple_porting` and `musa-converter` can accelerate source
conversion, but generated changes still require review and tests.

### torchada

torchada can translate many CUDA Python APIs, NCCL, extensions, and device
strings at runtime:

```python
import torch

if getattr(torch.version, "musa", None) is not None:
    import torchada  # Must precede modules that import CUDA extension helpers.
```

Use torchada when preserving a large CUDA-oriented upstream is more valuable
than converting every API. Before choosing it:

1. verify it is installed and supports the exact torch_musa version;
2. inventory unsupported CUDA packages and native libraries;
3. test device checks because `torch.cuda.is_available()` intentionally remains
   false and a translated `torch.device("cuda")` becomes a MUSA device whose
   `.type` is `"musa"`;
4. build extensions in a disposable/clean checkout because torchada extension
   porting may rewrite eligible CUDA sources in place;
5. compare outputs and gradients against a trusted backend.

Do not add torchada to a maintained native-MUSA codebase merely to avoid writing
a small device helper.

## 11. Debugging Backend Failures

Classify the first failure boundary:

1. import/runtime/driver;
2. device allocation or transfer;
3. unsupported operator/dtype/layout;
4. forward numerical divergence;
5. backward numerical divergence;
6. gradient clipping or AMP scaling;
7. optimizer state corruption;
8. distributed collective/hang;
9. save/export/reload mismatch;
10. performance-only regression.

Reduce to the smallest reproducer while preserving the failing dtype, shape,
layout, attention implementation, autocast state, and accumulation boundary.
Do not change five variables at once.

Useful torch_musa tools:

```python
from torch_musa.utils.compare_tool import CompareWithCPU, NanInfTracker, open_module_tracker

open_module_tracker(model)

with NanInfTracker():
    run_one_step(model)

with CompareWithCPU(atol=1e-3, rtol=1e-3, target_op=["torch.ops.aten.addmm"]):
    run_one_step(model)
```

CPU comparison can be expensive and may not support every low-precision op.
Enable it for a bounded step/rank/op range. For distributed debugging, write
separate rank logs and usually enable deep comparison on rank 0 only.

When reporting a MUSA bug, preserve:

- device model and count;
- driver, toolkit, MCCL, Python, torch, torch_musa, and framework versions;
- Git commit and complete command;
- visibility variables and logical rank mapping;
- first failing op/module/tensor;
- shape, stride, dtype, autocast, and attention backend;
- first non-finite phase and index;
- a bounded reproducer and trusted-backend comparison;
- whether eager/pure-PyTorch fallback succeeds.

## 12. Migration Audit Checklist

Before editing, search the target repository for:

```text
torch.cuda
.cuda(
device="cuda"
device.type == "cuda"
CUDA_VISIBLE_DEVICES
PYTORCH_CUDA_ALLOC_CONF
nccl
nvidia-smi
nvcc
CUDA_HOME
CUDAExtension
bitsandbytes
flash_attn
xformers
triton
BitBLAS
apex
deepspeed
```

For every match, decide whether to abstract, retain as NVIDIA-only, replace with
a MUSA equivalent, add a tested fallback, or mark unsupported.

Before declaring a port ready:

- [ ] environment and device discovery pass;
- [ ] single-device fp32 and target low-precision tensor ops pass;
- [ ] forward, backward, clipping, and optimizer state are finite;
- [ ] target attention implementation is explicit and recorded;
- [ ] save and fresh reload are verified;
- [ ] memory and wall time are measured with synchronization;
- [ ] two-rank MCCL passes before scaling to eight ranks;
- [ ] all ranks use logical `LOCAL_RANK` devices exactly once;
- [ ] CUDA-only dependencies have explicit handling;
- [ ] CUDA behavior remains unchanged in shared code;
- [ ] only a bounded preflight is used before user-authorized formal work;
- [ ] conclusions distinguish runtime success, numerical parity, and scientific
      result quality.

## 13. Agent Working Rules

When this skill is active, the Agent should:

1. inspect the current runtime and repository rules before proposing changes;
2. state whether it is using native MUSA APIs, a shared abstraction, torchada,
   or a native extension;
3. preserve the existing CUDA path unless the user explicitly removes it;
4. make the smallest compatibility change at the narrowest shared boundary;
5. perform caller/impact analysis before changing shared helpers;
6. verify static syntax first, then follow a staged runtime ladder;
7. never claim an optional library or kernel is available without checking the
   active environment;
8. never equate successful execution with cross-platform numerical parity;
9. defer expensive/formal runs to the user when repository rules require it;
10. record exact versions, commands, paths, hashes, and limitations in handoff
    reports.

## 14. Sources and Freshness

Primary references consulted for this skill:

- torch_musa README: <https://github.com/MooreThreads/torch_musa>
- torch_musa porting/debug utilities:
  <https://github.com/MooreThreads/torch_musa/blob/main/torch_musa/utils/README.md>
- torchada README: <https://github.com/MooreThreads/torchada>
- Local runtime evidence: the host's MUSA local-stack manifest, if present
  (see the host-environment skill for its location).

The MUSA ecosystem changes quickly. Re-check upstream documentation and the
active environment before relying on package availability, extension support,
attention kernels, `torch.compile`, graph capture, or performance claims.
