---
name: accel-pytorch-python
description: Python/wheel 层：为加速平台的 PyTorch 栈创建或修复 Python 环境——厂商源 vs 公共源纪律、版本匹配矩阵、环境变量、安装流程、验证与常见失败，适用任意厂商平台。Use when creating or repairing a Python environment for accelerator-platform PyTorch (vendor torch backend, torchvision/torchaudio, platform triton, vendor comm libs) on any platform. 正文为当前已验证实例（现 MUSA/摩尔线程源）；非该平台首次初始化时先按头部「如何特化」改写正文。触发词：装 torch、wheel 源、版本匹配、pip 源、依赖冲突。
---

# PyTorch Python Environment on Accelerator Platforms（Python 层，名称永不变）

## 如何特化本 skill（初始化时改写正文，不改名）

> 下方正文是**当前已验证实例**（MUSA / Moore Threads index，2026-09）。在其他平台首次初始化时按 accel-init 阶段 3 的调研结论改写；改写后本 skill 即该平台版本。已装机器不追仓库新版。

1. 双源纪律保留（厂商源 vs 公共源各平台本质相同）：换成本平台的 index URL、包族表（哪些包必须厂商源/哪些走公共源/哪些是厂商 fork）。
2. 版本匹配矩阵换成实查行（`pip index versions --index-url 厂商源`），附查询日期与重查命令。
3. 验证命令与预期输出用本机验证过的；未验证标 `(未验证)`。
4. 平台名只出现在内容里；本机事实（env 名、路径）写宿主机层。

## 当前实例：Python and PyTorch on MUSA

Use this skill after the MUSA user-space Toolkit, muDNN, MCCL, and matching `libmusa.so.1` are available. This skill handles Python package selection; it does not install the kernel driver.

## Two package indexes

Define the indexes explicitly for each install command:

```bash
export MUSA_PIP_INDEX=https://dl.mthreads.com/repo/api/pypi/pypi/simple
export PYPI_INDEX=https://pypi.org/simple
```

The Moore Threads index contains both MUSA-specific wheels and many ordinary mirrored packages. The presence of a package on that index does not mean it must be installed there.

Use the Moore Threads index for packages that contain MUSA binaries or MUSA-specific patches:

| Package family | Installation source |
| --- | --- |
| `torch` | Moore Threads index; select the MUSA-tagged wheel |
| `torch_musa` | Moore Threads index; version must match `torch` |
| `torchvision` | Prefer the matching MUSA wheel from the Moore Threads index |
| `torchaudio` | Prefer the matching MUSA wheel from the Moore Threads index |
| `triton` | Moore Threads Triton-MUSA wheel, despite the package name being `triton` |
| `tilelang_musa` | Moore Threads index |
| `mate` | Moore Threads index |
| `apache-tvm-ffi` | Moore Threads MUSA build when required by the stack |
| `torch-c-dlpack-ext` | Moore Threads MUSA build when required |
| `liteccl_ops` | Moore Threads build when required |
| `vllm_musa`, `flash_attn_3`, `flash_mla`, `deep-gemm`, `sageattention` | Moore Threads or project-specific MUSA build; validate exact release compatibility |

The current official index has, among other examples:

```text
torchvision 0.24.1.post1+musa5.2.0 for CPython 3.10/3.12
torchaudio 2.9.1+musa5.2.0 for CPython 3.10/3.12
triton 3.6.0 for CPython 3.10/3.12
```

Do not assume these versions match every torch_musa release. Query the index and use the release matrix.

Install ordinary, device-independent libraries from the public index:

```text
transformers
accelerate
huggingface-hub
safetensors
sentencepiece
numpy, scipy, pandas
requests, packaging, filelock, fsspec
protobuf, pydantic, tqdm, psutil
```

The torch_musa README identifies Transformers and Accelerate as upstream repositories with MUSA support. That means the upstream Python package is the correct starting point; it does not guarantee that every model, fused kernel, or optional extension works on MUSA.

Do not use ordinary public CUDA wheels for:

```text
torch
torch_musa
torchvision or torchaudio with compiled accelerator operators
triton
flash-attn
xformers CUDA builds
bitsandbytes
NVIDIA CUDA runtime packages
NCCL packages
CUDA-only custom extensions
```

Some repositories have Moore Threads forks rather than upstream support, including selected `pytorch3d`, `pytorch_sparse`, `pytorch_scatter`, `pytorch_cluster`, and Lightning branches. Install those only when the application actually requires them and follow the fork's branch/version instructions.

## Never mix indexes casually

Do not make the Moore Threads index the permanent global pip index for a normal Python environment. Do not use `--extra-index-url` for the core accelerator install: pip may resolve an ordinary CUDA/CPU torch from another source.

Use one of these patterns.

### Simple pattern

Install the exact accelerator set from the Moore Threads index, then install ordinary packages from public PyPI in a separate command:

```bash
python -m pip install \
  --index-url "$MUSA_PIP_INDEX" \
  "torch==<matching-version>" \
  "torch_musa==<matching-version>"

python -m pip install \
  --index-url "$PYPI_INDEX" \
  transformers accelerate datasets safetensors tokenizers
```

This allows the first command to resolve ordinary transitive dependencies from the Moore Threads mirror. Check the result with `pip check`.

### Strict separation pattern

Use this when the environment must prove which source supplied every ordinary package:

```bash
python -m pip install --no-deps \
  --index-url "$MUSA_PIP_INDEX" \
  "torch==<matching-version>" \
  "torch_musa==<matching-version>"

python -m pip install \
  --index-url "$PYPI_INDEX" \
  filelock fsspec jinja2 networkx packaging sympy typing-extensions \
  transformers accelerate datasets safetensors tokenizers
```

Add the ordinary dependencies reported by `pip check` from the public index. Use `--no-deps` for additional MUSA-specific wheels when their dependency set is controlled separately.

Do not install a complete project requirements file until it has been reviewed for `torch`, `torchvision`, `triton`, `bitsandbytes`, `nvidia-*`, CUDA extensions, and NCCL pins. A normal CUDA requirements file can silently replace the working MUSA torch.

## Select matching versions

Start with the Python ABI and MUSA SDK version:

```bash
python -V
python -m pip index versions torch --index-url "$MUSA_PIP_INDEX"
python -m pip index versions torch_musa --index-url "$MUSA_PIP_INDEX"
python -m pip index versions torchvision --index-url "$MUSA_PIP_INDEX"
python -m pip index versions torchaudio --index-url "$MUSA_PIP_INDEX"
python -m pip index versions triton --index-url "$MUSA_PIP_INDEX"
```

Select a complete row:

```text
Python ABI
MUSA SDK
torch
torch_musa
triton, if needed
```

For the local 5.2.0 stack, the available core row to validate in a new project environment is:

```text
Python 3.12
MUSA SDK 5.2.0
numpy 1.26.4
```

Do not copy this row to another SDK without checking the current wheel index.

## Required environment variables

Before importing torch, configure the selected MUSA user-space stack:

```bash
export MUSA_HOME=/path/to/musa/<version>
export MUSA_INSTALL_PATH="$MUSA_HOME"
export MUSA_DRIVER_LIB_DIR=/path/to/matching/userspace/lib
export PATH="$MUSA_HOME/bin${PATH:+:$PATH}"
export LD_LIBRARY_PATH="$MUSA_DRIVER_LIB_DIR:$MUSA_HOME/lib${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}"
export MUSA_VISIBLE_DEVICES=0
```

The matching user-space `libmusa.so.1` directory must appear before Toolkit libraries. Do not use a different SDK's `libmusa.so.1` just because it has the same SONAME.

## Installation workflow

1. Confirm the Python interpreter and MUSA variables.
2. Confirm `musa_version_query`, `musaInfo`, and `mccl_version`.
3. Query available MUSA wheel versions.
4. Install exact `torch` and `torch_musa` wheels from the Moore Threads index.
5. Install MUSA-specific add-ons from the Moore Threads index only when needed.
6. Install ordinary libraries from public PyPI.
7. Run `pip check`.
8. Run dynamic-library and MUSA compute checks.

Keep the normal pip and compiler cache paths. On managed homogeneous servers, use filesystem symlinks from those defaults to shared storage instead of adding cache variables to every Python environment. Avoid writing build artifacts into a shared base environment.

## Validation

Package metadata:

```bash
python -m pip show torch torch_musa
python -m pip check
python -m pip config list
```

The output must not show a public CUDA torch replacing the MUSA build. The local version usually contains a `+musa...` suffix.

Dynamic libraries:

```bash
TORCH_MUSA_LIB=$(printf '%s\n' "$CONDA_PREFIX"/lib/python*/site-packages/torch_musa/lib/libmusa_python.so.*)
ldd "$TORCH_MUSA_LIB" | awk '/not found/ {print}'
ldd "$CONDA_PREFIX"/lib/python*/site-packages/torch/lib/libtorch_global_deps.so | awk '/not found/ {print}'
```

No output is expected from either missing-library filter.

Python and device check:

```bash
python - <<'PY'
import torch
import torch_musa

print("torch:", torch.__version__)
print("torch_musa:", torch_musa.__version__)
print("torch.version.musa:", getattr(torch.version, "musa", None))
print("musa available:", torch.musa.is_available())
print("musa count:", torch.musa.device_count())
print("cuda available:", torch.cuda.is_available())

x = torch.randn(64, 64, device="musa", dtype=torch.bfloat16)
y = x @ x
torch.musa.synchronize()
print("matmul:", y.shape, y.dtype)

with torch.autocast(device_type="musa", dtype=torch.bfloat16):
    z = x @ x
torch.musa.synchronize()
print("autocast:", z.shape, z.dtype)
PY
```

`torch.cuda.is_available()` may be false in native torch_musa mode. Use `torch.musa.is_available()` for native MUSA code.

Distributed check:

```python
import torch.distributed as dist
dist.init_process_group("mccl", rank=rank, world_size=world_size)
```

Use a small one-process test first, then a two-process `torchrun` all-reduce. Do not test on GPUs occupied by another job.

## Common failures

`No matching distribution found`:

- Check Python ABI, platform tag, and exact package name.
- Query the Moore Threads index directly.
- Do not fall back to a public CUDA wheel without changing the compatibility plan.

`undefined symbol` or `libmusa.so`/`libmudnn.so` missing:

- Check `LD_LIBRARY_PATH` order.
- Confirm all MUSA libraries come from one SDK row.
- Run `ldd` on the failing extension.

NumPy 1.x/2.x warning:

- Use the NumPy version expected by the torch wheel and compiled extensions.
- The validated local 2.9.1 MUSA wheel uses `numpy==1.26.4`.

`torch.musa.is_available()` is false:

- Verify user-space libraries and `musaInfo` first.
- Verify that torch_musa imported and the correct `libmusa.so.1` was loaded.
- Check GPU visibility with `MUSA_VISIBLE_DEVICES`.

`torchvision` or `torchaudio` import fails:

- Check that its version matches torch.
- Prefer Moore Threads wheels or the documented Moore Threads source fork.
- Do not use an arbitrary public CUDA wheel.

`pip check` reports NVIDIA/CUDA packages:

- Inspect the requirements file that introduced them.
- Remove CUDA-only packages and reinstall the accelerator row explicitly.
