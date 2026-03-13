---
name: amd-rocm-porting
description: >
  Port NVIDIA CUDA codebases to AMD ROCm GPUs. Use when making PyTorch models run on AMD GPUs,
  replacing NVIDIA-specific libraries with AMD equivalents, fixing ROCm build/runtime failures,
  or porting C/C++ CUDA kernels to HIP. Also covers dependency debugging and environment setup
  on ROCm Docker images.
---

# AMD ROCm Porting

Port NVIDIA CUDA codebases to AMD ROCm GPUs for functional equivalence.

## 5 Critical Rules (read first)

1. **NVIDIA isolation**: Every ROCm change MUST be gated behind `is_rocm`. The NVIDIA code path
   must be byte-for-byte identical to the pre-porting state.
   ```python
   is_rocm = hasattr(torch.version, "hip") and torch.version.hip is not None
   ```

2. **Compile mode**: NEVER use `mode="reduce-overhead"` on ROCm — causes 65x slowdown.
   Use `mode="default"` on ROCm, keep original mode for NVIDIA.

3. **Inductor**: Disable `triton.cudagraphs`, `triton.cudagraph_trees`, and `memory_planning`
   on ROCm. Also override `max_autotune = False` (AMD Docker images set it `True` by default,
   causing `mode="default"` to silently behave like `max-autotune` and hang).
   Details: [references/torch-compile-and-cudagraph.md](references/torch-compile-and-cudagraph.md)

4. **Warp width**: AMD wavefronts are 64-wide (not 32). All ballot/mask operations need
   `uint64_t`. (C/C++ repos only; pure Python repos skip this.)

5. **Three-tier fallback**: AMD-optimized lib → PyTorch SDPA → pure PyTorch eager.
   Details: [references/library-and-model-adaptation.md](references/library-and-model-adaptation.md)

## Decision Tree: Which Phases to Run

```
Does the repo have C/C++ CUDA kernels (.cu / .cuh files)?
├── NO  → Skip Phases 2, 3, 4. Run Phases 1, 5, 6, 7, 8 only.
│         (Pure Python/PyTorch repos — most HuggingFace models, etc.)
└── YES → Run all 8 phases.
          Does it use flash-attn, CUTLASS, or custom extensions?
          ├── flash-attn only → Phase 5 (replace with aiter)
          ├── CUTLASS         → Phase 3 + manual CK rewrite
          └── custom kernels  → Full Phase 2 + 3 HIPIFY workflow
```

## Context Management

- **Load reference files lazily** — only read a reference when actively working on that phase.
- **Summarize findings** — after each phase, record a brief summary rather than retaining raw
  grep output in context.

## Phase Checklist

### Phase 0: Environment Setup

**Step 1 — Audit existing environment before installing anything.**
AMD Docker images often have PyTorch ROCm, aiter, flash-attn pre-installed. Check what exists:
```bash
env | grep -iE 'TORCH|INDUCTOR|AUTOTUNE|TRITON|HIP|ROCM|HSA|GPU|AMD|CUDA' | sort
pip show torch torchvision transformers 2>/dev/null | grep -E "^(Name|Version|Location)"
```
Add the repo `src/` to `sys.path` in scripts to make the package importable without `pip install`:
```python
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "src"))
```
Run the target script and note only the `ModuleNotFoundError`s that actually occur.
Install those packages individually (`pip install --no-deps <pkg>`).

**Step 2 — Never run `pip install -e .` on AMD without exclusions.**
The `pyproject.toml` was written for NVIDIA and often contains `jax[cuda12]` and `torch==X.Y.Z`.
Running `pip install -e .` will overwrite your ROCm PyTorch with CUDA versions.
Use: `pip install --no-deps --ignore-requires-python -e .`, then install only missing packages.

**CRITICAL: Protect PyTorch after any pip install.** Always verify:
```bash
python3 -c "import torch; print(torch.__version__, torch.version.hip)"
```
If `torch.version.hip` is `None`, your ROCm PyTorch was overwritten. Reinstall it.

**Step 3 — Python version constraint.**
`requires-python = ">=3.11"` is often a conservative constraint. Use `--ignore-requires-python`.

**Step 4 — Repos with JAX + PyTorch: use PyTorch-only path.**
Skip all JAX-dependent code; do not attempt to install or fix JAX for ROCm.

**Step 5 — Dependency debugging.**
If you hit `ImportError`, version mismatch, or dtype errors, read [references/dependency-debugging.md](references/dependency-debugging.md) for the diagnostic protocol.

### Phase 1: ROCm Detection & Flags
- Detect ROCm: `is_rocm = hasattr(torch.version, "hip") and torch.version.hip is not None`
- Detect GPU arch (never hardcode): `rocminfo | grep -o 'gfx[0-9a-f]*' | head -1` → e.g. `gfx942` (MI300X) or `gfx950` (MI350X)
- Set ROCm-safe env vars: `PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True` (omit `max_split_size_mb`)
- Set performance env vars:
  ```bash
  export GPU_MAX_HW_QUEUES=2  HIP_FORCE_DEV_KERNARG=1  HSA_NO_SCRATCH_RECLAIM=1  AMD_LOG_LEVEL=0
  ```
- Disable NUMA balancing (10-30% perf loss if left on): `sudo sh -c 'echo 0 > /proc/sys/kernel/numa_balancing'`
- Verify GPU: `rocm-smi`, `rocminfo | grep gfx`, `hipcc --version`
- FP8 dtype depends on arch:
  ```python
  arch = torch.cuda.get_device_properties(0).gcnArchName
  fp8_dtype = torch.float8_e4m3fnuz if "gfx942" in arch else torch.float8_e4m3fn
  ```

### Phase 2: Source Translation (C/C++ only)
- Run `hipify-perl --inplace` for initial pass, then `hipify-clang` for complex templates
- Key header mappings: `cuda_runtime.h`→`hip/hip_runtime.h`, `cublas_v2.h`→`hipblas/hipblas.h`
- Flag inline PTX (`grep -rn "asm\s*("`) — cannot be auto-ported; flag CUTLASS — needs manual CK rewrite

### Phase 3: Architecture Adaptation (C/C++ only)
- Replace 32-bit ballot masks with `uint64_t` for AMD 64-wide wavefronts
- Replace `__popc` with `__popcll` for 64-bit masks; prefer 64-element shared memory tiles

### Phase 4: Build System (C/C++ only)
- Detect GPU arch at runtime — never hardcode: `GPU_ARCH=$(rocminfo | grep -o 'gfx[0-9a-f]*' | head -1)`
- CMake: `find_package(HIP)`, set `CMAKE_HIP_ARCHITECTURES` to the detected arch
- setup.py: detect `is_rocm`, use `CUDAExtension` (hipcc handles `.cu` on ROCm)

### Phase 5: Library Replacement
- flash-attn → aiter (different API; wrap with three-tier fallback)
- NCCL → RCCL, cuBLAS → hipBLAS (drop-in via HIPIFY)
- pynvml: guard with `try/except`, use `torch.cuda.is_available()` as primary GPU check
- `PYTORCH_CUDA_ALLOC_CONF`: remove `max_split_size_mb` on ROCm (rejected by HIP allocator)
- Details + fallback patterns: [references/library-and-model-adaptation.md](references/library-and-model-adaptation.md)

### Phase 6: torch.compile Adaptation
- Gate compile mode: `"default"` on ROCm, original mode on NVIDIA
- **Audit env vars first**: `env | grep -iE 'TORCH|INDUCTOR|AUTOTUNE'` — unset `TORCHINDUCTOR_MAX_AUTOTUNE` if present (causes hangs even in `default` mode)
- Apply Inductor config: disable cudagraphs, memory_planning; set `max_autotune=False`; use `ATEN` GEMM backend
- Details + monkey-patch: [references/torch-compile-and-cudagraph.md](references/torch-compile-and-cudagraph.md)

### Phase 7: CUDAGraph / HIP Graph (optional)
- Only needed if kernel launch overhead is a bottleneck (profile first).
- Since Inductor CUDAGraphs are disabled on ROCm, use **manual CUDAGraph capture**.
- **HIP does NOT raise errors for illegal ops during capture** — it silently produces wrong results on replay. Always validate outputs.
- For capture patterns, RNG patch, and graph break debugging, see the `amd-kernel-optimization` skill's [torch-compile-and-graphs.md](../amd-kernel-optimization/references/torch-compile-and-graphs.md).

### Phase 8: Verification
- Static: grep for remaining `cuda_runtime.h`, inline PTX, NVIDIA-specific types
- Build (C/C++): `GPU_ARCH=$(rocminfo | grep -o 'gfx[0-9a-f]*' | head -1); hipcc -c kernels.hip --offload-arch=$GPU_ARCH`
- Functional: forward + backward pass, compare loss to CPU reference
- Numerical: `torch.testing.assert_close(rocm_out, cuda_ref, rtol=5e-2, atol=5e-2)`
- Details + golden vector methodology: [references/verification-methodology.md](references/verification-methodology.md)

## First-Run Compilation Penalty (NORMAL on AMD)

Every JIT component has a slow first run. **Do NOT conclude something is broken because first run is slow.**

| Component | First Run | Subsequent | Cache |
|---|---|---|---|
| torch.compile (`default`) | 2-5 min | <1s | `TORCHINDUCTOR_CACHE_DIR` |
| torch.compile (`max-autotune`) | 5-15 min | <1s | `TORCHINDUCTOR_CACHE_DIR` |
| AITER JIT kernels | 1-3 min | <1s | aiter jit/build/ |
| Triton kernels | 1-2 min | <1s | `~/.triton/cache` |
| TunableOp GEMM tuning | 1-5 min | <1s | `PYTORCH_TUNABLEOP_FILENAME` |

**Set timeout ≥ 600s for first compilation.** Do NOT kill processes under 15 minutes.

## Common Pitfalls

| Pitfall | Symptom | Fix |
|---|---|---|
| `pip install -e .` on AMD | Overwrites ROCm torch with CUDA version | Use `--no-deps --ignore-requires-python`; install missing pkgs individually |
| `TORCHINDUCTOR_MAX_AUTOTUNE=1` in Docker env | `mode="default"` hangs (silently becomes max-autotune) | `unset TORCHINDUCTOR_MAX_AUTOTUNE` before any compile |
| `reduce-overhead` compile mode | 65x slowdown, hangs | `mode="default"` on ROCm |
| `max_split_size_mb` in `PYTORCH_CUDA_ALLOC_CONF` | RuntimeError at startup | Remove on ROCm |
| Top-level `import pynvml` | ImportError | Guard with `try/except`; use `torch.cuda.is_available()` first |
| Inductor cudagraphs enabled | Slowdown, capture errors | `inductor_config.triton.cudagraphs = False` |
| Inductor memory_planning | Deep recursion crash | `inductor_config.memory_planning = False` |
| `torch.cuda.get_rng_state()` during capture | RuntimeError | Apply Dynamo RNG patch |
| `torch.backends.cuda.matmul.allow_tf32` | AttributeError on ROCm | Gate behind `if not is_rocm` |
| NUMA balancing on | 10-30% perf loss, intermittent errors | `echo 0 > /proc/sys/kernel/numa_balancing` |
| FP8 dtype mismatch | Crash or accuracy loss | gfx942=`e4m3fnuz`, gfx950=`e4m3fn` |
| 32-bit warp masks (C/C++) | Silent wrong results | Use `uint64_t` for ballot/active masks |
| Patching files into wrong site-packages path | Custom model code never loads | Verify with `inspect.getfile(TheClass)` after patching |

## References

Load only when actively working on that phase:

- **Phase 0 (deps)**: [references/dependency-debugging.md](references/dependency-debugging.md) — 4-step diagnostic protocol, version mismatch fixes, patching failures, dtype mismatch tracing
- **Phase 5**: [references/library-and-model-adaptation.md](references/library-and-model-adaptation.md) — Library mapping, aiter API, three-tier fallback, pynvml/alloc_conf fixes
- **Phase 6**: [references/torch-compile-and-cudagraph.md](references/torch-compile-and-cudagraph.md) — Inductor safety config, compile mode gating, env var audit, safety monkey-patch
- **Phase 8**: [references/verification-methodology.md](references/verification-methodology.md) — 4-level pyramid, tolerance table, static analysis greps
