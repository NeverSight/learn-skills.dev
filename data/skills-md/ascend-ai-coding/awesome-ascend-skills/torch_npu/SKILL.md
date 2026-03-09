---
name: torch_npu
description: 华为昇腾 Ascend Extension for PyTorch (torch_npu) 的环境检查、部署与能力指引。在用户使用 @torch_npu、昇腾 NPU、CANN、或需要将 PyTorch 迁移到 NPU 时自动应用；当用户使用 @torch_npu_doc 时，基于 skill 的 reference 文档提供项目内中文文档能力说明。
---

# torch_npu 能力与使用指引

## 何时使用本 Skill

- 用户 **@torch_npu**、提到昇腾 NPU、CANN、Ascend、或 PyTorch 在 NPU 上运行。
- 用户需要 **环境检查/部署**：检查或部署 PyTorch、检查环境是否支持 NPU。
- 用户使用 **@torch_npu_doc** 时：基于本 skill 的 [reference.md](reference.md) 提供项目内中文文档能力说明与操作步骤。
- 用户需要 **NPU 格式转换的代码提示**：书写或补全 `torch_npu.npu_format_cast`、`npu_format_cast_`、`torch_npu.Format`、`get_npu_format` 时，按 §2.1 子能力提供参数与枚举提示；若不理解该功能，可建议通过本 skill 的 MCP 抓取版本文档辅助说明。

---

## 1. 环境检查与部署

### 1.1 自动检查 PyTorch 与 NPU 环境

在回答或生成脚本时，按需执行或建议用户执行以下检查：

**检查 PyTorch 与 Python 版本是否在配套范围内**（参见 README.zh.md 中的「PyTorch与Python版本配套表」）：

- 支持 PyTorch 1.11.0～2.9.0 等多版本，对应 Python 3.7～3.11（视具体 PyTorch 版本而定）。

**检查环境是否支持 NPU：**

```python
import torch
import torch_npu  # 2.5.1 及以后可不显式 import，仍建议写以便兼容

# 是否可用 NPU、设备数量
if torch.npu.is_available():
    count = torch.npu.device_count()
    # 使用 device='npu' 或 .npu()
else:
    # 未安装 CANN / 未 source set_env.sh / 无 NPU 设备
    pass
```

**检查 CANN 环境变量（安装后验证）：**

- 使用前需执行：`source /usr/local/Ascend/ascend-toolkit/set_env.sh`（路径以实际 CANN 安装为准）。
- 若 `ASCEND_HOME_PATH`、`ASCEND_OPP_PATH` 未设置或路径不存在，torch_npu 会报错并提示执行 `source set_env.sh`。

### 1.2 部署步骤摘要

1. **安装 CANN**：按 [CANN 安装指南](https://www.hiascend.com/cann) 安装，并与 README.zh.md 中「昇腾辅助软件」表核对 CANN 与 PyTorch/Extension 版本。
2. **安装 PyTorch**：x86 用 `pip3 install torch==2.7.1+cpu --index-url https://download.pytorch.org/whl/cpu`，aarch64 用 `pip3 install torch==2.7.1`（示例版本，按需替换）。
3. **安装依赖**：`pip3 install pyyaml setuptools`。
4. **安装 torch_npu**：`pip3 install torch-npu==2.7.1`（版本需与 PyTorch、CANN 配套）。
5. **验证**：`source set_env.sh` 后运行快速验证代码（见 README.zh.md「安装后验证」）。

---

## 2. torch_npu 能力目录（简略）

| 类别 | 能力说明 |
|------|----------|
| **设备与内存** | `torch.npu`：设备管理、`device_count`、`current_device`、`set_device`、`synchronize`、`Stream`/`Event`、内存统计与分配（`memory_allocated`、`empty_cache`、`MemPool` 等）。 |
| **张量/存储** | `tensor.npu()`、`tensor.is_npu`、NPU Storage、序列化 `torch.save`/`load` 支持 NPU，DDP/多进程 reductions。 |
| **训练/优化** | `torch.npu.amp` 混合精度、`torch_npu.optim`、FSDP 补丁（`ShardedGradScaler`）、梯度检查点默认 NPU。 |
| **分布式** | `torch_npu.distributed`：HCCL/LCCL 后端、`is_hccl_available`、`reinit_process_group`、RPC、symmetric memory、DTensor 规则。 |
| **扩展 API** | `torch_npu.contrib`：NMS、IoU 系列、ROIAlign、DCN、FusedAttention、自定义模块（如 `DropoutWithByteMask`）等。 |
| **图与编译** | NPU Graph（`npugraphify`）、Dynamo、Inductor、torch.compile 支持 NPU。 |
| **推理/ONNX** | ONNX 导出与 NPU 定制算子封装（如 OneHot、RoiAlign、NMS、FastGelu、MultiHeadAttention 等）。 |
| ** profiling** | `torch_npu.profiler`、MSTX 补丁、性能 dump。 |
| **其他** | HiFloat8Tensor、erase_stream、matmul_checksum、transfer_to_npu（可选）、op_plugin。 |

详细 API 以 [昇腾 Ascend Extension for PyTorch 自定义 API 参考](https://www.hiascend.com/document/detail/zh/Pytorch/720/apiref/torchnpuCustomsapi/context/%E6%A6%82%E8%BF%B0.md) 及项目 `README.zh.md` 为准。

---

## 2.1 子能力：torch_npu.npu_format_cast 代码提示

当用户在代码中书写或询问 `torch_npu.npu_format_cast`、`npu_format_cast_`、NPU 张量格式转换时，应提供以下**代码提示与补全指引**，便于在 IDE 中完成各项提示。

### API 签名与参数

- **`torch_npu.npu_format_cast(tensor, acl_format, customize_dtype=None)`**  
  - `tensor`：NPU 上的 `torch.Tensor`（需先 `.npu()`）。  
  - `acl_format`：目标存储格式，可为 **`int`** 或 **`torch_npu.Format`** 枚举成员。  
  - `customize_dtype`：可选，用于 ONNX 等场景的自定义 dtype。  
  - 返回：新张量（不修改原张量）。

- **`torch_npu.npu_format_cast_(tensor, acl_format)`**  
  - 同上，但为 **in-place** 版本，直接修改 `tensor` 的格式。

- **`torch_npu.get_npu_format(tensor)`**  
  - 返回张量当前 NPU 存储格式（`torch_npu.Format` 或整型）。

### 常用 Format 枚举（torch_npu.Format）

在代码提示中可优先提示以下常用值（来自 `torch_npu.npu._format.Format`）：

| 枚举名 | 值 | 常见用途 |
|--------|----|----------|
| `Format.NCHW` | 0 | 默认 4D 卷积布局 |
| `Format.NHWC` | 1 | 通道在后的 4D 布局 |
| `Format.ND` | 2 | 通用 ND 布局 |
| `Format.NC1HWC0` | 3 | Conv/BatchNorm 等算子常用 |
| `Format.FRACTAL_Z` | 4 | 3D 卷积等 |
| `Format.FRACTAL_NZ` | 29 | 线性/矩阵乘、Attention 权重等 |
| `Format.NDC1HWC0` | 32 | 5D |
| `Format.FRACTAL_Z_3D` | 33 | 3D 卷积 |
| `Format.UNDEFINED` | -1 | 未定义 |

其他可选：`NC1HWC0_C04`(12)、`HWCN`(16)、`NDHWC`(27)、`NCDHW`(30)、`NC`(35)、`NCL`(47)、`FRACTAL_NZ_C0_*`(50–54) 等。

### 代码提示与补全规则

1. **补全第二参数**：当用户输入 `torch_npu.npu_format_cast(x, ` 时，提示 `acl_format` 可选为 `int` 或 `torch_npu.Format.xxx`，并列出常用枚举（如 `Format.NCHW`、`Format.NHWC`、`Format.FRACTAL_NZ`、`Format.NC1HWC0`）。  
2. **补全 Format 枚举**：当用户输入 `torch_npu.Format.` 时，提示上述枚举成员列表。  
3. **配对使用**：若代码中已有 `get_npu_format(t)`，在需要转成相同格式时，可提示 `torch_npu.npu_format_cast(other, torch_npu.get_npu_format(t))`。  
4. **常见场景**：  
   - 线性层权重量子化/迁移到 NPU：`torch_npu.npu_format_cast(weight.npu(), 29)`（FRACTAL_NZ）；  
   - 与参数格式一致的梯度：`torch_npu.npu_format_cast(p.grad, torch_npu.get_npu_format(p))`；  
   - 模块迁移时 BN/Conv 的 NC1HWC0：`torch_npu.npu_format_cast(tensor, 3)` 或 `Format.NC1HWC0`。

### 文档来源说明

若需更权威的格式说明或与 CANN 的对应关系，可让用户通过本 skill 的 **MCP**（见 [mcp/README.md](mcp/README.md)）使用 `fetch_torch_npu_doc` 抓取 GitCode [Ascend/pytorch](https://gitcode.com/Ascend/pytorch) 对应分支下的版本文档（如 `docs/zh` 下与 format 或算子适配相关的文档），或在 reference 中查找「框架特性指南」相关条目。

---

## 3. 如何自动提供文档中的能力（@torch_npu_doc）

- 当用户 **@torch_npu_doc** 或明确要求查阅 torch_npu 中文文档时：
  - **优先使用本 skill 的 reference 文档**：[reference.md](reference.md)。其中包含项目内全部中文文档的索引与关键内容摘要。
  - 根据用户问题在 reference.md 的「文档索引」中定位到对应文档路径（如 `torch_npu/README.zh.md`、`torch_npu/docs/zh/quick_start/quick_start.md`、`torch_npu/docs/zh/framework_feature_guide_pytorch/`、`torch_npu/docs/zh/troubleshooting/` 等），按需读取工作区内该文件并引用相关段落。
  - 对安装、验证、卸载、版本配套：采用 README.zh.md 或 reference 中的摘要；对迁移与快速入门：采用 quick_start；对算子适配、内存、性能、图模式：采用 framework_feature_guide_pytorch 下对应文档；对报错与故障：采用 troubleshooting 下对应文档。
- 回答时用中文简要说明，并注明所引用文档路径便于用户自行查阅。

---

## 4. 参考资源

- **本 skill 文档参考**：[reference.md](reference.md)。汇总 torch_npu 项目内所有中文文档索引与要点；用户 **@torch_npu_doc** 时据此定位并引用具体文档。
- **项目中文说明**：工作区内 `torch_npu/README.zh.md`（版本表、部署、验证、参考文档链接）。
- **官方文档**：[昇腾社区 Ascend Extension for PyTorch](https://www.hiascend.com/software/ai-frameworks?framework=pytorch)、软件安装指南、模型迁移与训练、算子适配、PyTorch 原生接口清单、自定义 API 参考（见 README.zh.md 底部表格）。
- **从 GitCode 抓取版本文档**：本 skill 提供 MCP 服务，可从 [GitCode Ascend/pytorch](https://gitcode.com/Ascend/pytorch) 按分支抓取文档并保存到 `fetched_docs/`。安装与配置见 [mcp/README.md](mcp/README.md)；项目已配置 `.cursor/mcp.json`，安装依赖后重启 Cursor 即可使用工具 `fetch_torch_npu_doc`、`fetch_torch_npu_docs_batch`、`list_torch_npu_doc_paths`。
