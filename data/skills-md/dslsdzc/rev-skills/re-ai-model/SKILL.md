---
name: re-ai-model
description: >
  AI 模型文件逆向与静态分析：ONNX/PyTorch/Safetensors/TFLite 格式解析、
  网络结构还原、权重提取、文件级水印分析（权重 pattern/metadata/tensor hash/embedding 异常）。
  触发词：模型文件、权重提取、ONNX解析、safetensors、pth分析、pt文件、模型结构还原、文件级水印
capabilities: [ai-model-analysis]
---

# AI 模型逆向（ONNX / PyTorch / Safetensors）

## 何时使用 / 何时不用

- 用：拿到 .onnx / .pt / .pth / .safetensors / .tflite 等模型文件，要还原网络结构、提取权重
- 用：**文件级水印**检测（东西藏在哪里：权重 pattern / metadata / tensor hash / embedding 异常——怀疑模型是从原版复制/微调而来时先查文件侧）
- 用：模型文件本身是载荷——权重里藏数据、torch.save 打包恶意 pickle、后门/投毒模型（下载执行类样本）
- 不用：**行为级水印**（模型表现出来是什么：trigger 触发响应 / 查询响应 / 黑盒指纹）与 API 行为层攻击（走 [[re-ai-attack]]）
- 不用：纯推理脚本/训练代码（那是源码，走 [[re-script-deob]]）
- 不用：模型被打包进可执行文件（PyInstaller/pyarmor 等）——先 [[re-binary-core]] 拆包，拆出的模型文件再回本技能
- 边界：本技能定位 = 模型文件解析 / 结构分析 / 权重分析 / 文件级水印——恶意模型判定、投毒/后门行为侧、归属取证属取证域（未来独立 re-ai-malware 技能承接；当前此类需求暂在本技能范围，以安全边界（坑 2 pickle 隔离）处理，行为侧转 [[re-ai-attack]]）
- 注意：**安全提示——不要直接 torch.load 未知 pkl 文件**（pickle 反序列化可执行任意代码，见坑 2）；一切对未知 pkl 的加载默认隔离环境（[[re-analyze/platform-tips]] 沙箱最高原则），先读后跑；模型解析/权重提取为静态步骤，可免沙箱

## 工具准备

参考 [[re-analyze/platform-tips]]——模型文件 GB 级常见，静态分析按「静态优先（大型样本）」思路：先格式识别与结构解析，按需提取权重，不整载内存（坑 1）。

### python3 —— 所有解析脚本基础

- Linux: `apt install python3` / `dnf install python3` / `pacman -S python`
- macOS: `brew install python3`；Windows: `choco install python`
- 验证: `python3 --version`（本技能脚本均为 Python 3）

### onnx（pip，Python 3.10+）—— ONNX 解析主力

- `pip install onnx`（官方 PyPI；onnx 1.22 要求 Python 3.10+，自带 protobuf 依赖与 `onnx.proto3` 类型定义）
- 验证: `python3 -c "import onnx; print(onnx.__version__)"`

### netron（pip，Python 3）—— 模型可视化

- `pip install netron`（官方 PyPI，无 Python 版本上界）；桌面独立版可选: macOS `brew install --cask netron`、Windows `winget install netron`、Linux snap `snap install netron`
- 验证: `netron --help` 有输出（`pip show netron` 查版本）
- 用法: `netron model.onnx`（本地起 http 服务并开浏览器可视化；`--no-browser` 无头模式）

### torch（pip，Python >=3.10）—— PyTorch 模型加载

- Linux/Windows: `pip install torch`（默认 PyPI 轮子为带 CUDA 全量包，数 GB；仅 CPU 分析用 `pip install torch --index-url https://download.pytorch.org/whl/cpu`）
- **Python 版本下限**：当前 torch 2.x 要求 **Python >=3.10**（PyPI `requires-python`；torchvision 同步为 >=3.10）——3.9 环境要装需 pin 到仍支持 3.9 的旧版（2.8.x 及更早）。torch / torchvision / Python 的具体组合以官方 compatibility matrix 为准，别按「3.9+」泛化
- macOS: `pip install torch`（官方 wheel 为 CPU/arm64）
- 验证: `python3 -c "import torch; print(torch.__version__)"`
- **安全注**：torch.load 底层是 pickle——不要直接 load 未知 pkl 文件；PyTorch 2.6+ 默认 `weights_only=True`，旧版本/显式 `weights_only=False` 仍有任意代码执行风险；未知模型先 `unzip -l`/`xxd` 粗查（坑 2），在隔离环境用 `weights_only=True` 加载，能转 safetensors 就转

### safetensors（pip，Python 3）—— 安全格式读取

- `pip install safetensors`；验证: `python3 -c "import safetensors; print(safetensors.__version__)"`
- 设计目的即无代码执行（纯数据 + JSON 头），是未知 pkl 的替代分析入口（坑 2 对策之一）

### protobuf / protoc（onnx 是 proto）—— 底层格式

- Python 绑定: `pip install protobuf`（当前 7.x 要求 **Python >=3.10**，6.x 起下限已在抬升；3.8/3.9 需 pin 对应旧版本。onnx 已自带依赖、通常无需单独装）
- protoc 编译工具: Debian/Ubuntu `apt install protobuf-compiler`、Fedora `dnf install protobuf-compiler`、Arch `pacman -S protobuf`、macOS `brew install protobuf`
- 验证: `protoc --version`；`python3 -c "import google.protobuf; print(google.protobuf.__version__)"`

## 操作步骤

按顺序执行，每步产物（模型哈希/结构摘要/权重清单）存档 sha256 + 路径（[[re-ioc]] 证据链）。

1. **模型格式识别（onnx / safetensors / pytorch pkl / tflite）**：
   ```sh
   file model.bin && sha256sum model.bin > model.sha256 && xxd model.bin | head -2
   ```
   - **ONNX**：无固定魔数——protobuf 流，首字段为 ir_version（tag `0x08` + 变长值；**值随 ONNX 版本递增**：IR 8 对应 ONNX 1.10，当前发布已到 IR 13——所以第二个字节不是常量 `08`，不能拿 `08 08 12` 当识别特征）；producer_name（tag `0x12`，长度前缀）按规范只 SHOULD 出现，不保证紧跟其后；`onnx.checker.check_model` 可验证合法性
   - **Safetensors**：前 8 字节 = **小端** u64 头长度（`struct.unpack("<Q", data[:8])`），随后是 JSON 头（张量名/形状/dtype/偏移）
   - **PyTorch**：`file` 显示 Zip archive（`PK\x03\x04` 头）——`unzip -l model.pt` 看条目（state_dict 含 `data.pkl`；torch.jit.script 含 `data.pkl`/`constants.pkl`/`bytecode.pkl`）；老式纯 pkl 是裸 pickle 流（无 PK 头）——**不直接 load**，先 xxd/strings 粗看（坑 2）
   - **TFLite**：flatbuffers 流——无固定魔数，但字节 4–7 为文件标识符 `TFL3`（对应 schema 的 `__model_identifier` 字段），xxd/strings 可见；结构解析可用 Netron（支持 .tflite 可视化），权重提取分支思路同 onnx（flatbuffers 解析，超出本技能深度时标注"结构化 dump 为准"）
   - 判定后按格式走对应分支；拿不准先 [[re-triage]] 初勘（熵/strings 特征）

2. **结构解析（图/层/算子）**：
   ```sh
   netron model.onnx --no-browser          # 可视化（有图形界面再开浏览器）
   python3 - <<'PY'
   import onnx
   m = onnx.load("model.onnx")
   print("producer:", m.producer_name, m.producer_version)   # 框架/优化器指纹（见坑 3）
   g = m.graph
   print("inputs:", [(i.name, [d.dim_value for d in i.type.tensor_type.shape.dim]) for i in g.input])
   print("nodes:", len(g.node), "initializers:", len(g.initializer), "outputs:", [o.name for o in g.output])
   for n in g.node[:20]:
       print(n.op_type, n.name, list(n.input), "->", list(n.output))
   PY
   ```
   - PyTorch 侧：`torch.jit.load` 得 ScriptModule 可打印 `model.graph`（TorchScript 结构）；`torch.load` 的 state_dict 只有张量**没有网络结构**——结构在训练/推理脚本里，需配合源码还原（见跨域 [[re-script-deob]]）
   - 关注点：算子序列（卷积/注意力等结构指纹）、输入输出张量形状、常量节点位置（权重藏在哪）

3. **权重提取（张量 dump）**：
   ```sh
   mkdir -p weights
   # ONNX：逐 tensor 惰性落地（大模型见坑 1）
   # 注意：这不是"流式"——to_array() 对使用 external data 的 tensor 会先把该张量【完整】读进 ndarray，
   #       只是"一次一个张量"而不是"一次整个模型"；显存/内存峰值取决于最大的那个张量
   python3 - <<'PY'
   import onnx, numpy as np
   m = onnx.load("model.onnx", load_external_data=False)     # 只载图结构，不载外部权重
   for init in m.graph.initializer:
       # base_dir 默认为空字符串——外部权重不在 CWD 时必须显式指定其所在目录
       arr = onnx.numpy_helper.to_array(init, base_dir=".")   # 该张量在此处被完整 materialize
       np.save(f"weights/{init.name.replace('/', '_')}.npy", arr)
       print(init.name, arr.shape, arr.dtype)
       del arr                                                # 及时释放，为下一张量让出内存
   PY
   # Safetensors：惰性按张量读取（不整载内存）
   python3 - <<'PY'
   from safetensors import safe_open
   with safe_open("model.safetensors", framework="numpy") as f:
       print(len(f.keys()), "tensors")
       for k in list(f.keys())[:10]:
           t = f.get_tensor(k); print(k, t.shape, t.dtype)
   PY
   # PyTorch state_dict（weights_only 安全加载，见坑 2）
   python3 - <<'PY'
   import torch
   sd = torch.load("model.pth", weights_only=True)
   for k, v in list(sd.items())[:10]:
       print(k, tuple(v.shape) if hasattr(v, "shape") else type(v))
   PY
   ```
   - 产出：权重清单（张量名/形状/dtype/数值摘要）+ npy 存档——这是水印检测与窃取判定的原料

4. **模型水印/指纹检测（嵌入权重）**：
   - 权重级：逐张量统计（min/max/mean/std、直方图分桶）与疑似原版模型比对；水印常嵌在特定层（首层卷积 bias、归一化 scale、embedding 矩阵行），多为低比特位扰动——检查关键张量的低比特位模式与数值分布异常，而非精确相等（坑 4）
   - 指纹级：全权重 sha256 摘要、逐层张量 hash 序列；与候选原版逐层距离（L2/余弦）比对，输出"每层距离热点图"
   - 行为级：同一测试输入集跑两模型推理，比较 logits 与激活分布——重训练/蒸馏窃取者权重不同但行为接近
   - 产出：相似度矩阵 + 热点图，结论注明判定依据与阈值

5. **模型窃取判定（架构相似度）**：
   ```sh
   python3 - <<'PY'
   import onnx
   from difflib import SequenceMatcher
   m1 = onnx.load("suspect.onnx"); m2 = onnx.load("original.onnx")
   s1 = [n.op_type for n in m1.graph.node]; s2 = [n.op_type for n in m2.graph.node]
   print("op-seq similarity:", SequenceMatcher(None, s1, s2).ratio())   # 算子序列相似度
   # 层对齐后逐层权重余弦/L2 距离：见步骤 4 的每层距离矩阵
   PY
   ```
   - 维度：算子序列（SequenceMatcher）、输入/输出形状、逐层权重余弦/L2、输出 logits 距离
   - 判定纪律：单一维度是弱证据（同架构不同训练=正常）；多维度一致且权重分布高度接近（如逐层余弦 >0.99）才可主张窃取，结论标注各维度数值
   - 隐藏载荷检查：`m.metadata_props`（ONNX metadata 藏字符串/代码）、zip 条目中多余文件（坑 2 相关）、权重中形状/数值分布特异的异常张量

## 跨域联合

- [[re-managed]]：本网关「识别运行时」识别到 AI 模型文件后固定调用本技能（模型是"代码在数据里"的托管域分支）
- [[re-binary-core]]：模型内嵌代码、模型被打包进可执行文件（PyInstaller/pyarmor 打包的推理程序）——先二进制域拆解（格式解析/反编译），拆出的模型文件回本技能
- [[re-sandbox]]：一切未知 pkl 的 load 默认隔离环境（[[re-analyze/platform-tips]] 最高原则）
- [[re-malware]]：恶意模型载荷（pickle 恶意代码、后门权重、投毒模型分发）的行为与情报侧
- [[re-ioc]]：模型指纹（sha256/张量 hash/水印模式）进 IOC；[[re-triage]]：模型文件初勘入口与哈希存档
- [[re-script-deob]]：PyTorch 推理/训练脚本还原（state_dict 无结构时的补全路径）
- 引用 [[re-analyze/platform-tips]] 静态优先（大型样本）与沙箱最高原则分支
- [[re-ai-attack]]：**文件级证据 → 行为级验证**（单向数据流）——本技能产出的文件侧结论（结构 / 权重 / 文件级 fingerprint）作为 re-ai-attack 行为一致性验证的输入。示例：拿到 suspect.pt → 本技能提取结构+权重生成 fingerprint → 转 re-ai-attack 做行为一致性验证（API 侧比对）
- 只有 API（无文件）的评估直接进 [[re-ai-attack]]，不经本技能

## 常见坑与陷阱

- **大模型文件巨大（GB 级）**：现象——`onnx.load`/`torch.load` 吃满内存卡死，netron 打开超时，`np.save` 批量写盘满；原因——权重数 GB，一次性整体加载到内存；对策——分析前先 `du -sh`/`sha256sum` 存档；ONNX 用 `onnx.load(..., load_external_data=False)` 只载图结构，再**逐 tensor** 取值——注意 `numpy_helper.to_array()` 对该 tensor **是完整读出**（不是流式），所以峰值取决于最大的张量，且用 external data 时要**显式给 `base_dir`**（默认空字符串，权重不在 CWD 时直接失败）；Safetensors 用 `safe_open` 惰性按张量读；PyTorch 大模型 `torch.load(..., mmap=True)`；处理对象是"结构摘要 + 定向张量"，不是整个文件
- **pkl 反序列化风险（不要直接 torch.load 未知 pkl）**：现象——load 后进程反弹 shell/文件被删，或报诡异 `AttributeError`/`ModuleNotFoundError`；原因——pickle 协议可注入任意代码（`__reduce__`/`__setstate__`），torch.load 底层就是 pickle，恶意模型是投毒载荷载体；对策——**安全提示：未知模型绝不直接 `torch.load`**；先 `unzip -l`/`xxd`/`strings` 粗查（zip 头 PK vs 裸 pickle、条目有无可疑模块名），用 `weights_only=True`（PyTorch 2.6+ 默认）加载，需要全功能加载时在隔离环境（[[re-sandbox]]）执行；可转 safetensors 的样本直接转（纯数据无代码执行）
- **图优化混淆层结构**：现象——onnx-simplifier/TensorRT/onnxruntime 优化后的模型算子序列与训练态对不上（Conv+BN 融合成一个 Conv、常量折叠、名字全改），结构相似度误判；原因——优化器做算子融合/常量折叠，图结构与训练态不同，producer 字段会变；对策——先读 `m.producer_name`/`m.producer_version` 识别优化器与版本（融合 ConvBN 的特征：BN 层消失且 scale 并入 conv 权重）；架构比较前先规范化算子序列（按算子类别抽象，忽略名字与常量差异）；可用 onnx-simplifier/onnxruntime `graph_optimization_level` 对比优化前后 diff 还原原始层
- **水印鲁棒性（剪枝后仍存）**：现象——精确值比对未命中就下"无水印"结论，或两个无关模型在个别层数值巧合相似被误判"窃取"；原因——鲁棒水印经剪枝/量化/重训练后仍存活（设计目标），精确匹配必漏；正常模型同架构同数据权重分布相似，单层巧合是假阳性；对策——水印检测用"统计异常"（低比特位扰动/数值分布特异层）而非"精确相等"，窃取判定用多维度证据 + 阈值（步骤 5 纪律），结论标注置信度与证据强度
