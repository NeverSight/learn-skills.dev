---
name: lnn-quant-training
description: Build, diagnose, optimize, and validate quantization-aware training workflows for the local Linger 3.x project. Use when Codex must convert a PyTorch float model to a Linger constrained/QAT model, design a quantization-friendly architecture, create or review Linger YAML quantization settings, configure mixed precision or local clamp overrides with YAML parts, const_module, or quant_module, calibrate MOM or TQT quantizers correctly, recover accuracy when quantization misses its target, inspect QAT checkpoints or float-versus-quant outputs, export a trained quantized model with linger.onnx.export, inspect the resulting Linger ONNX graph, or prepare the model for Thinker packaging and consistency validation.
---

# LNN 量化训练

## 核心工作流

把量化训练视为带签收标准的工程闭环，而不是在浮点训练脚本末尾调用一次 `linger.init`。除非用户只要求其中一个阶段，否则按下面顺序推进。

1. **冻结验收条件**：记录任务指标、浮点基线、允许的精度下降、输入 shape/range、预处理、目标平台、位宽、时延和内存约束。目标平台缺失时仍可做通用 8/8-bit QAT，但不得给出部署兼容结论。
2. **审计结构**：检查算子、分支、归一化、激活、动态 shape 和输出形式。设计或修改网络前读取 `references/model-design.md`；目标平台部署约束交给同级 `$lnn-model-design` skill 复核。
3. **建立浮点基线**：保存最优 float checkpoint、固定验证集和评测脚本，并保留一组可重复的 golden inputs/outputs。没有同数据、同预处理、同 metric 的 float baseline 时，不判断量化损失。
4. **快速导图预检**：在长时间训练前，用随机权重或 float checkpoint 完成一次 `trace_layers -> init -> forward -> linger.onnx.export`，确认结构能导出。预检只证明图可生成，不证明量化效果。
5. **约束训练**：从 float checkpoint 开始，按需执行一次 `linger.trace_layers(...)`，调用 `linger.constrain(...)`，重建 optimizer，再做短周期约束微调。先确认 constrained-vs-float 指标差，再进入 QAT。
6. **量化初始化**：在同一结构变换顺序下调用 `linger.init(...)`，随后加载匹配 checkpoint 并再次重建 optimizer。MOM 让训练 forward 初始化 `running_data/scale`；TQT 任务必须先读取 `../doc/tutorial/tqt_training.md`，按其中的后端选择、单次校准、optimizer 覆盖和首个 backward 梯度审计执行。
7. **QAT 微调**：通常从浮点学习率的约 `0.1x` 起步，以实际曲线为准；同时记录 float、constrained、QAT 指标和量化器状态，保存完整 QAT `state_dict`。完整实现顺序读取 `references/training-workflow.md`。
8. **效果诊断**：先排除 checkpoint、预处理、BN/eval、量化器未初始化和样本不一致，再定位首个高误差层。量化效果不达标时必须读取 `references/accuracy-recovery.md`；涉及 mixed precision、局部 clamp、`const_module` 或 `quant_module` 时还必须读取 `references/mixed-precision.md`，按低风险到高风险顺序迭代。
9. **导图与验证**：严格重建训练时的结构和配置，加载 QAT checkpoint，执行真实输入 warm-up，切换 `eval()`，用 `torch.no_grad()` 包裹 `linger.onnx.export(...)`。完整导图和验证流程读取 `references/export-and-validation.md`。
10. **签收**：用 `references/report-template.md` 输出阶段指标、差值、配置、命令、artifact、未决风险和下一步。只有 ONNX checker、量化图审计和目标 runtime consistency 都通过时，才称为部署闭环。

## 项目事实优先级

优先以当前 checkout 的 live source 和测试为准，再参考教程；不要把旧文档中的枚举或能力描述直接当成当前实现事实。定位入口见 `references/project-sources.md`，配置字段和当前限制见 `references/configuration.md`。

## 强制规则

- 把 `linger.trace_layers`、`linger.constrain` 和 `linger.init` 都视为会改变模型结构的操作；每个结构变化后重建 optimizer/scheduler。
- 始终保留 float、constrained、QAT 三类独立 checkpoint，不要覆盖上游基线。
- 训练、恢复、评估和导图必须使用相同 model code、fusion 顺序、config、`disable_module`/`disable_submodel` 和输入契约。
- 加载 checkpoint 后检查 `missing_keys` 和 `unexpected_keys`；除非差异已逐项解释，否则不使用 `strict=False` 掩盖问题。
- `disable_module` 会修改进程级量化注册表；只把它用于隔离实验，新的对照实验优先启动新进程。
- 当前代码中 `linger.calibration()` 的内置校准函数依赖 TQT 的 `learning_data/is_calibrate`；MOM 不走该上下文，直接由训练 forward 更新统计量。
- TQT 训练使用 `quant_method: NATIVE` 或 `CUDA_GS`；当前 `CUDA` backward 不返回 `learning_data` 梯度。验证和导图前按 `../doc/tutorial/tqt_training.md` 刷新最终 scale。
- mixed precision 最终方案优先写入完整 YAML `partN`；API 覆盖只用于定位或动态 tensor op，并在恢复/导图时重放。先定位敏感层，再确认目标硬件支持；高位宽训练有效不等于 Thinker/目标芯片可部署。
- 不用普通 ONNX Runtime 是否能执行 `linger` custom-domain op 作为导图成功标准；优先做 ONNX checker、图属性审计和 Thinker/runtime consistency。
- 一次只改一个主要变量，并保存变更前后的同集指标和输出差异。

## 可执行工具

在 toolchain root 下使用：

```bash
python3 lnn-quant-training/scripts/generate_qat_config.py --output configs/qat.yaml --platform venusA --device cuda --qat-method MOM
python3 lnn-quant-training/scripts/inspect_quant_checkpoint.py checkpoints/best_qat.pt --format markdown
python3 lnn-quant-training/scripts/compare_outputs.py artifacts/float_outputs.npz artifacts/qat_outputs.npz --format markdown
python3 lnn-quant-training/scripts/inspect_quant_onnx.py artifacts/model_quant.onnx --format markdown --fail-on-issues
```

脚本的详细用途、输入约定和返回码写在各自 `--help` 中。对任意 checkpoint 只加载可信来源；检查脚本优先使用 PyTorch 的 `weights_only=True`。

## 交付物

至少保留：

- float、constrained、best-QAT checkpoint 及其 metric。
- 最终 YAML、训练参数、随机种子、代码版本和输入契约。
- golden input、float output、QAT output 和输出对比报告。
- 导出的 ONNX、ONNX 审计报告、导出命令与日志。
- 具备 Thinker 时的 pkg、memory report、`tvalidator`/runtime 结果；不具备时明确标为未验证。
