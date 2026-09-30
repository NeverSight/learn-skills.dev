---
name: lnn-model-design
description: Assist LNN/Linger/Thinker model architecture design and adaptation. Use when Codex must evaluate or iterate a neural network structure for the LNN toolchain from customer application requirements, input sizes, a base PyTorch/ONNX architecture, or an existing model; check target-platform hardware limits, parameter/input/weight/activation sizes, Linger quantization/export support, Thinker operator and precision support, tpacker memory constraints, confirm the full Linger export to Thinker package/validation flow, and prepare author-facing issue bundles when Linger/Thinker itself appears to have a program error or consistency problem. When the request does not specify the target platform or the model input size/range, stop and ask the user to confirm those items before giving a compatibility conclusion.
---

# LNN 模型辅助设计

## 核心工作流

把这个 skill 当成训练前或部署前的 architecture gate。按“审计 -> 修改 -> 复审”的短循环推进，直到模型能够通过 Linger export 和 Thinker packaging。

1. **需求收集**：收集应用目标、目标平台（`venus`、`mars`、`arcs`、`venusa`）、input shape/range、latency/memory/accuracy 目标、当前模型来源，以及模型当前处于 float、constrained、QAT 还是已导出 ONNX 状态。  
   如果 target platform 缺失，先让用户确认，再做 capability scan 或 pass/fail 判断。  
   如果 model input size、input shape 或 dynamic input range 缺失，先让用户确认，再做 parameter、activation、memory 或 compatibility 分析。
2. **能力扫描**：对本地 toolchain root 运行 `scripts/collect_toolchain_capabilities.py`。当需要查 source path、文档或命令变体时，读 `references/toolchain-sources.md`。当需要 Linger -> `tpacker` -> x86 -> `tvalidator` -> `tprofile` 的实操顺序时，读 `references/workflow-playbook.md`。
3. **静态模型审计**：如果已有 ONNX，运行 `scripts/inspect_onnx_model.py`；否则根据 PyTorch module 或结构描述估算 tensor/parameter size，并在 export 前识别不支持的 PyTorch op。
4. **适配决策**：对比 op、precision、parameter bytes、activation bytes、`tpacker` threshold、SRAM/PSRAM、dynamic shape range 和客户要求。提出结构修改建议前，先读 `references/adaptation-guidelines.md`。判断修复方式是 architecture shrinkage、threshold tuning、stream split 还是显式 op split 前，先读 `references/npu-split-strategy.md`。当 gate 失败原因不清晰时，先运行 `scripts/triage_gate_blocker.py`，对 structure / split-policy / threshold / toolchain 假设做排序，再改模型。
5. **全流程 gate**：用 Linger 导出，用 Thinker `tpacker` 打包，并在 runtime library / input 可用时，通过 `tvalidator` 或直接的 `test_thinker` / `test_dynamic` 路径做验证。参考 `references/full-flow.md`，也可以直接使用 `scripts/run_toolchain_gate.py`。如果已经有失败的 `tvalidator` log 或 runtime log，把它回灌到 `run_toolchain_gate.py`，让 gate 对 runtime/consistency 问题做 triage，并按需自动生成 author issue bundle。
6. **Toolchain bug 移交**：如果 Linger / Thinker / `tpacker` / `tvalidator` 本身表现异常，或者打包后的模型出现更像 toolchain 问题而不是 architecture 问题的 consistency mismatch，就停止大范围结构反复修改。读取 `references/author-handoff-template.md`，运行 `scripts/generate_author_issue_bundle.py`，生成 `problem.md` 和 `repro.sh`，并保存最小可复现 bundle 给作者排查。
7. **结果汇报**：输出 pass/fail matrix、明确 blocker、精确 tuning 建议、commands/logs/artifacts、下一轮动作，以及适用时的 author handoff bundle 路径。报告结构参考 `references/report-template.md`。

## 子 skill 模块

- **requirements-to-candidate**：把客户约束转换成少量对 LNN 友好的 candidate block。优先选用 Linger 和 Thinker 已列出的 op；规避非常规 control flow、不支持的 normalization、不支持的 activation，以及过大的单次 tensor。
- **capability-discovery**：从本地 `linger/` 和 `thinker/` source tree 中抽取当前 hardware、op、precision、threshold 和 x86 validation flow 信息，而不是依赖记忆。
- **model-static-audit**：对现有 architecture 或 ONNX 做检查，覆盖 op support、dtype/precision 风险、dynamic axis、parameter size、大 initializer、activation/input shape。
- **blocker-triage**：结合 ONNX 和可选的 `tpacker` / memory / `tvalidator` log，判断下一步应该优先改 structure、split policy、threshold tuning，还是直接进入 toolchain bug handoff。
- **adaptation-loop**：提出尽量小的结构修改来移除 blocker：替换 op、调整 kernel/stride/dilation、调整 channel/resolution、拆 layer、streaming、限制 dynamic shape、或调 memory threshold。先检查 single-compute limit，再区分它是 architecture 问题还是 toolchain split-policy 问题。
- **export-pack-validation**：在条件具备时，实际跑 Linger export、Thinker `tpacker` 和 `tvalidator`/runtime 检查。把 packaging 成功视为最终签收前的必要证据。
- **toolchain-bug-handoff**：当 blocker 更像 Linger/Thinker 程序缺陷或 runtime consistency 缺陷时，生成面向作者的问题文件和最小可复现 ONNX/pkg/input/script bundle。

## 必要证据

这个 skill 有两种工作模式：

1. **完整 LNN 验证模式**：本地存在 Linger/Thinker 工具时，以 `tpacker` / `tvalidator` / runtime 结果作为最终证据。  
2. **离线 architecture-audit 模式**：当 LNN 环境不可用时，仍使用 skill 内置的 hardware、operator、precision、memory 和 split 约束，给出静态 compatibility assessment。

除非工具无法运行，否则不要只根据文档就下兼容结论。证据优先级按下面顺序：

1. 导出的 ONNX 在目标平台上 `tpacker` 成功。
2. `tvalidator` consistency 通过，或有明确说明为什么不能运行。
3. 静态 ONNX 审计加 capability scan。
4. 基于 architecture 文本和 source doc 的手工估算。

如果某个工具无法运行，明确写出缺失的 dependency 或 artifact，然后继续给出当前最强的静态评估结果。在 offline 模式下，建议必须基于 skill 中保存的平台限制、operator/precision support、memory threshold 和 split rule，并明确标注该结果只是 preflight guidance，不是最终 runtime proof。如果工具看起来不是“不可用”，而是“行为本身有问题”，不要只用 prose 总结，要直接生成 author handoff bundle。

## 缺失时必须确认的输入

下面这些输入对可靠评估是强制项：

- Target platform。
- Model input size、input shape，或 dynamic input range。

如果其中任何一项缺失或有歧义，先要求用户确认。做 compatibility verdict 时，不要自行假设默认 platform 或默认 image size。

## 使用简介

简要的用户侧使用说明见 `references/usage-intro.md`。平台硬件限制速查见 `聆思芯片硬件限制.md`。

## 常用命令

在同时包含 `linger/` 和 `thinker/` 的 toolchain root 下运行：

```bash
python3 lnn-model-design/scripts/collect_toolchain_capabilities.py --platform venusa --format markdown
python3 lnn-model-design/scripts/inspect_onnx_model.py model.onnx --capabilities-json capabilities.json --platform venusa --format markdown
python3 lnn-model-design/scripts/run_toolchain_gate.py --onnx model.onnx --platform venusa --out-dir design_gate
python3 lnn-model-design/scripts/run_toolchain_gate.py --onnx model.onnx --platform venusa --out-dir design_gate --tvalidator-log design_gate/tvalidator.log --auto-author-bundle
python3 lnn-model-design/scripts/run_toolchain_gate.py --onnx model.onnx --platform venusa --out-dir design_gate --runtime-log design_gate/test_thinker.log --auto-author-bundle
python3 lnn-model-design/scripts/run_toolchain_gate.py --onnx model.onnx --platform venusa --dynamic_shape seq=32:384:32 --out-dir design_gate --runtime-log design_gate/test_dynamic.log --auto-author-bundle
python3 lnn-model-design/scripts/triage_gate_blocker.py --onnx model.onnx --platform venusa --tpacker-log design_gate/tpacker.log --memory-report workspace/model/model_memory_report.txt --format markdown
python3 lnn-model-design/scripts/generate_author_issue_bundle.py --case-name venusa_case1 --platform venusa --onnx model.onnx --tpacker-log design_gate/tpacker.log --triage-json design_gate/blocker_triage.json --repro-cmd 'PYTHONPATH=thinker/tools python3 -m tpacker.tpacker -g model.onnx -p venusa -o model.pkg -d True'
```

如果从其他目录运行这个 skill，补上 `--toolchain-root`。

当需要上报疑似 Linger/Thinker bug 时，把 issue bundle 保存在 `lnn_model_design_reports/<case>_author_issue/` 下，并至少包含 `problem.md`、`repro.sh`、`bundle_manifest.json`、最小模型 artifact、必需输入和失败日志。

## 决策规则

- 如果某个 op 在 Linger export support 或 Thinker target-platform support 任一侧缺失，先提出可支持的替代方案，再讨论 accuracy tuning。
- 如果 target platform 缺失，在运行 `collect_toolchain_capabilities.py`、`inspect_onnx_model.py` 或 `run_toolchain_gate.py` 前先让用户确认。
- 如果 model input size 或 dynamic range 缺失，在估算 activation memory、评估 dynamic shape 或给最终适配结论前，先让用户确认。
- 如果 `tpacker` 报 memory overflow，先判断最大压力来自 DMA buffer、workspace 还是 intermediate output；再结合 `references/npu-split-strategy.md` 中的 single-compute split rule，决定是减 channel、拆 height/width，还是重调 threshold / memory placement。
- 如果 `tpacker` / `tvalidator` 在一个本应受支持的 graph 上报 internal assertion、invalid runtime parameter，或者 packaging 成功后仍出现 consistency mismatch，把它视为潜在 toolchain defect；先准备 author handoff bundle，再考虑继续做大范围结构改写。
- 对 toolchain bug handoff，要尽量激进地最小化 case：保持相同 target platform 和 input shape，删除无关 layer，尽可能隔离 first failing op/subgraph，保留精确 tool flag，并包含仍能复现问题的最小 script / ONNX / pkg / input 集合。
- 在长时间训练前，优先做一次快速 preflight：让 quant-init 至少足以 export ONNX，跑 `tpacker`，先确认 graph 在结构上可部署。
- 如果 input shape 是 dynamic 的，评估时看声明的最大 shape，而不是只看常见 runtime shape。
- 如果模型还只是 proposal，先构造最小 dummy model/export harness，用随机初始化 weight 跑一遍 gate，再决定是否值得投入训练。
- 每一轮改动都尽量保持“小而可测”：一个 blocker、一个假设、一条修订后的命令、一个新的结果。
