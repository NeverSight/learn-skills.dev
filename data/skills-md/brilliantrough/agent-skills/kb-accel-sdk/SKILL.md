---
name: kb-accel-sdk
description: 公共知识库：各大加速计算平台（CUDA/MUSA/Ascend CANN/ROCm/阿里PPU/沐曦MACA）的 SDK 组成、安装方式、triton 与 tilelang 生态、vllm 与 sglang 推理框架生态速查。Use when working on any accelerator server, choosing SDK/wheel/inference-framework versions, or when a platform-specific package/behavior surprises you. 知识类 skill：可被覆盖刷新，不做本机特化；新事实经 writing-skill 流程回流仓库。触发词：SDK 组成、装 CANN、torch_npu、vllm 昇腾、sglang 国产卡、triton fork、tilelang、PPU。
---

# 加速平台 SDK 与生态知识库

> 知识类 skill：内容为跨平台公共知识（调研日期 2026-09-27；Ascend 节 2026-09-28 经 910B2 实机初始化验证刷新，易过期条目附重查入口）。本机特有事实不写这里（宿主机层管）。**结论与实机冲突时以实机为准，并回流更新本库。**

## 平台总览

| 平台 | 厂商 | 软件栈 | smi | torch 后端 | 通信库 | wheel 来源 |
| --- | --- | --- | --- | --- | --- | --- |
| CUDA | NVIDIA | 驱动 + CUDA Toolkit（nvcc/cuBLAS/cuDNN/NCCL/TensorRT） | nvidia-smi | 原生 | NCCL | PyPI / download.pytorch.org/whl/cuXXX |
| MUSA | 摩尔线程 | mtgpu 驱动 + MUSA SDK（musart/toolkit/muDNN/MCCL） | mthreads-gmi | torch_musa | MCCL | dl.mthreads.com 厂商 index |
| Ascend | 华为 | 驱动+固件 + CANN（toolkit/kernels/NNAL，含 HCCL、ATB；推理另有 MindIE） | npu-smi | torch_npu | HCCL | PyPI(torch_npu) + 华为云 mirrors.huaweicloud.com/ascend（triton-ascend/离线包） |
| ROCm | AMD | amdgpu 驱动 + ROCm（HIP/hipBLAS/MIOpen/RCCL） | rocm-smi | 原生（HIP 转译，device 仍叫 cuda） | RCCL | download.pytorch.org/whl/rocmX.Y |
| PPU | 阿里平头哥 | 真武 810/810E，GPGPU 路线；公开 SDK 文档极少（2026-01 才官方证实存在） | (未验证) | (未验证) | (未验证) | 阿里云渠道，无公共源 |
| 沐曦 MACA | 沐曦 | MXMACA（mcBLAS/mcDNN/mcFlashAttention） | mx-smi | mcPytorch | mcCL(未验证) | 沐曦开发者社区镜像/发布包 |

寒武纪 MLU（Neuware/torch_mlu）、海光 DCU（DTK，ROCm 系）也常遇到，速记备查。

## 生态矩阵（关键防坑表）

| 框架 | CUDA | ROCm | Ascend | MUSA | PPU |
| --- | --- | --- | --- | --- | --- |
| triton | 上游原生 | 上游原生 | **triton-ascend**（fork；**与上游 triton 同名互斥**，见 Ascend 节） | **Triton-MUSA**（fork，已至 3.6；PyPI 与上游同名，装错不报错） | 未验证 |
| transformers | 原生 | 原生 | 上游支持（torch_npu） | 上游声明支持（torch_musa README，但融合 kernel/可选扩展不保证） | 未验证 |
| tilelang | 上游原生 | 上游(HIP) | **tilelang-ascend**（tile-ai org） | **tilelang_musa**（厂商 index） | 未验证 |
| vllm | 上游原生 | 上游原生 | **vllm-ascend**（vllm-project org 官方插件，版本号对齐上游 vllm；**钉死 torch/transformers 全链**，见 Ascend 节） | **vLLM-MUSA**（官方后端，开源 fork） | 未验证 |
| sglang | 上游原生 | 未验证 | 官方支持（2025-08 起，`--device npu --attention-backend ascend`，sgl-kernel-npu 仓库） | 已合入主线（2026-05，源码装 + sgl-kernel） | 未验证 |

规律：**推理/编译生态正在从"厂商自维护 fork"转向"官方仓库插件化"**（vllm hardware plugin 机制、sglang 合入主线），查版本时先看官方仓库的硬件支持矩阵，再看厂商 fork 的 release 行。

## 各平台要点与坑

### CUDA（基准）
- pip 装 torch 默认即 CUDA 版；只有源码编译扩展才需系统 toolkit，运行只需驱动。
- 驱动版本 ≥ wheel 的 CUDA runtime 版本即可（向前兼容）；nvidia-smi 右上角就是驱动支持的 CUDA 上限。
- 容器路线最省心：nvidia-container-toolkit + 官方 NGC 镜像。

### MUSA（含 2026-09 S5000/MUSA 5.2 实机实例沉淀）
- SDK：5.1.0 对标 CUDA 12.8（2026-05 发布）；安装＝官方 apt 仓库/离线包，用户态版本化目录；5.2 包族＝musa-toolkit-5-2 / musa-musart-5-2 / libmudnn3-musa-5-2 / libmthreads-compute，**MCCL 按卡型分包**（S5000 用 mccl-s5000 非 S4000 版）；纯用户态装法不碰 mthreads-driver/dkms。
- 厂商 index 精确 URL：`https://dl.mthreads.com/repo/api/pypi/pypi/simple`；源里混着大量普通镜像包，**在厂商源里 ≠ 必须从这装**。
- 包族路由（哪些必须厂商源）：torch / torch_musa / torchvision / torchaudio / triton（即 Triton-MUSA，包名就叫 triton）/ tilelang_musa / mate / vllm_musa / flash_attn_3 / flash_mla / deep-gemm / sageattention → 厂商源；transformers / accelerate / datasets 等设备无关包 → 公共源；pytorch3d、pytorch_sparse/scatter/cluster、部分 Lightning 分支 → 摩尔 fork，按需装。
- 版本铁律：torch ↔ torch_musa **精确同版**；wheel 标 `musa5.2.0` ↔ 用户态 5.2 栈；cp310/cp312 ABI 匹配。已验证示例行（2026-09 查）：torchvision 0.24.1.post1+musa5.2.0 / torchaudio 2.9.1+musa5.2.0 / triton 3.6.0 / numpy 1.26.4。
- 坑：`pip install torch` 会用公共 CUDA 版顶掉 `+musa` 版（静默失败，重查 `pip list | grep torch`）。
- 代码面：分布式 `backend="mccl"`；muDNN 开关在 `torch.backends.mudnn`；CUDA 分配器 env（PYTORCH_CUDA_ALLOC_CONF 等）对 MUSA 进程无效；工具：mthreads-gmi（smi）/ musaInfo / musa_version_query / mccl_version。
- CUDA 兼容层：torchada（`import torchada` 让 99% CUDA 代码跑 MUSA，nccl 可映射 MCCL）+ MATE 算子库（FlashAttention/FlashMLA/DeepGEMM 接口）。完整安装/验证流程与 CUDA→MUSA API 映射表在 accel 三件套的 MUSA 实例里。

### Ascend CANN（2026-09-28 实机验证：910B2×8 / CANN 9.0.0 / aarch64 / py3.10，L1–L6 全过）
- 版本强绑定链（已验证行）：驱动 25.2.1/固件 7.7.0.9.220 ↔ CANN 9.0.0 ↔ torch 2.10.0 ↔ torch_npu 2.10.0.post4 ↔ torchvision 0.25.0 / torchaudio 2.10.0 ↔ triton-ascend 3.2.2 ↔ vllm 0.23.0 + vllm-ascend 0.23.x ↔ transformers 5.5.4。配套表查法：`curl -s https://raw.githubusercontent.com/Ascend/pytorch/master/README.md | grep -A2 CANN`；vllm-ascend 各版钉子查 `pypi.org/pypi/vllm-ascend/<ver>/json` 的 requires_dist。
- wheel 现状（2026-09-28）：torch_npu 在公共 PyPI，aarch64 从 2.9.x 起覆盖 cp310–cp313，但**正式版偶发只发部分 ABI**（2.12.0 只有 cp312/313）；查 ABI 以 simple 页文件名为准，别信 `pip index` 的 JSON 元数据（镜像上会滞后数月停在旧版）。
- **vllm-ascend 安装五坑**（2026-09-28 全踩全解）：
  1. 上游 vllm 钉的 torch 比 vllm-ascend 钉的高一档（vllm 0.23.0→torch 2.11，vllm-ascend 0.23.x→2.10）：装完 vllm **必须重钉** torch 全家 + transformers，否则 torch_npu ABI 断裂。
  2. post 版常只有 sdist（rc 版反而有全 ABI wheel）：py3.10/3.11 用同线 rc wheel + `--no-deps`，缺依赖按其 METADATA 手补（xgrammar/compressed-tensors/numba/quart 一串）。
  3. triton-ascend 与上游 triton **同名同命名空间互斥**（共存=后者遮蔽，症状 `'function' object is not subscriptable` / `No module named triton._C.libtriton.ascend`；卸载互相带走文件）：解法＝两个都卸，`--no-deps` 单装 triton-ascend，且**最后装**。
  4. triton-ascend 新版公共源发布滞后（3.2.2 只有华为云有）：`--find-links https://mirrors.huaweicloud.com/ascend/repos/pypi/triton-ascend/`。
  5. **NNAL（libatb.so）是 vllm 硬依赖**，不在 CANN toolkit 统一包（`--feature` 仅 ascendc）也无 pip 包：无官方镜像渠道时，可从 CANN 官方 docker 镜像（quay.io/ascend/cann:<ver>-910b-…）registry API 流式抽取 `/usr/local/Ascend/nnal` 落地安装；运行时必须双 source：CANN set_env + `nnal/atb/set_env.sh`，否则 `libatb.so not found` → engine 起不来。
- torch_npu 使用面（已验证）：`torch.npu.*` 镜像 CUDA API；autocast `device_type="npu"`；transformers `device_map="auto"` 可跨多 NPU 分层；HCCL 单/双进程 all_reduce 精确。910B2 每卡 HBM 按 61GB 规划（系统保留 ~3.4GB）。
- transformers 双向钉死冲突：vllm-ascend 钉 transformers（0.23.x↔5.5.4），模型 remote code 又常钉旧版（openPangu↔4.53.2，5.x 上 LossKwargs/rope 键名两处断）：解法选型＝该模型单独小环境，或走 vllm（不依赖 transformers remote code）；别在主环境逐符号打补丁（打不完）。
- 症状速查：`ERR99999 UNKNOWN application exception` 是昇腾异常收尾行，真因在其上方 traceback；`NPUCachingAllocator ... 32 padding size` warning 无害别修。
- tilelang-ascend：CANN ≥ 8.3.RC1、torch_npu ≥ 2.6.0；wheel 从 GitHub Releases 按 CANN/Python/架构匹配下载。
- 硬件差异（写 kernel 必踩）：AI Core 分 Cube/Vector；每核 UB 仅 192KB（BLOCK_SIZE 大了溢出）；**越界访问无容错，直接 Device Hang——mask 必须严格**。
- 官方自有推理引擎 MindIE 与 vllm-ascend 并存，选型看场景（MindIE 商用闭源、vllm-ascend 社区开源）。

### ROCm
- 官方支持矩阵限定发行版+内核版本，装前必查（rocm.docs.amd.com）。
- device 名仍是 `cuda`（HIP 转译），CUDA 代码基本零改动；rccl 代替 nccl。
- 上游 triton/tilelang/vllm/sglang 原生支持（版本矩阵看 pytorch.org 与各框架 release notes）。

### PPU（阿里平头哥）
- 真武 810E：GPGPU 路线（非 ASIC），大规模部署在阿里云，出货一年以上（2026-01 官方证实）。
- 公开 SDK/文档极少：装环境不靠公共源（搜不到不是不存在），主路径=阿里云实例/容器镜像 + 阿里云文档与工单。
- 首次接触：先查实例规格文档里给出的镜像与运行时说明，把"有哪些预装、怎么用"问清再动手。

### 沐曦 MACA（速记）
- 轮子带 `+metax`/`+maca` 后缀（torch 2.6.0+metax、vllm 0.8.5+maca、triton 3.0.0+metax）；防串规则同 MUSA：公共源 `pip install torch` 会顶掉适配版。
- 安装主路径=沐曦开发者社区的 docker 镜像/发布包（容器要挂 `/dev/mxcd /dev/dri`）；MACA 版本号形如 mc2.32.0.3，与发布包严格配套。
- MACA 3.3 适配 PyTorch 2.8 全算子；推理支持 vllm/SGLang/Transformers。

## 通用防坑（全平台）

- 版本四元组：驱动 ↔ SDK ↔ torch 后端 ↔ 编译器 fork（triton/tilelang），任何一环升级都要重查整链兼容矩阵。
- `pip list | grep -E 'torch|triton|vllm'` 看**本地版本后缀**（+musa/+metax/+npu…）判断是不是平台适配版；无后缀≈公共版，多半是顶掉了。
- 公共源找不到平台 wheel 是常态，不是平台不支持——去厂商文档/下载中心（见 accel-init 阶段 3 调研路径）。
- 各平台可见设备变量不同：CUDA_VISIBLE_DEVICES / MUSA_VISIBLE_DEVICES / ASCEND_RT_VISIBLE_DEVICES / HIP_VISIBLE_DEVICES(ROCm)。
- 插件也会顶版本：装 vllm-*/sglang-* 等平台插件后，立刻复核 torch/transformers/torchvision 是否被顶掉并重钉——"防串"不止防 `pip install torch`，还防一切钉 torch 的包（Ascend 2026-09-28 实例：vllm 把 torch 顶到高一档）。
- 同名互斥包族：厂商 triton fork 与上游 triton 共享命名空间（MUSA/Ascend 均实锤），共存=静默坏（kernel 装饰器失效变普通函数、后端子模块缺失）；正解=两个都卸净，`--no-deps` 单装厂商版，且放在安装序列最后。
- 镜像源的包 JSON 元数据可能滞后数月（实测清华源 torch-npu 元数据停在 2.3.1 而实际已到 2.12）：查版本/ABI 以 simple 页文件名或 pypi.org JSON 为准。
- "运行库缺失型"硬依赖常有隐藏系统包（如 Ascend vllm 之于 NNAL/libatb.so）：报 `cannot open shared object file` 时先想系统层缺件，查官方安装文档的 Requirements 表，而不是继续折腾 pip。

## 演化（本库随时准备被更新）

定位：经验流入点＝真实服务器上的实验与踩坑（装过、跑通、报错、版本不匹配都是素材）。流程：

1. 实机经验 → 找本库对应条目；没有就在正确的表/小节补一行，不新开孤儿小节。
2. 更新规则：结论带日期与证据（命令输出/官方文档链接）；`(未验证)` 条目实机验证后**转正或删掉**；被推翻的结论直接改写为当前正确版本（git 留痕，不保留过时叙述）。
3. 结构不变量：总览表 / 生态矩阵 / 平台小节 / 通用防坑四层形态保持；新平台＝总览一行＋小节一节；单平台专属的坑不上升为通用防坑。
4. 更新可以直接改在服务器本机副本上（演化发生地＝真机），改完走固定回路：下载到开发机 → 合入仓库 push → 本机重装拉新版。坑：本机修改未回流前别重跑 setup 的 kb 覆盖刷新（会冲掉它）。
