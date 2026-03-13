---
name: cross-review
description: 对技术方案或代码进行跨模型交叉评审。用户要求"交叉评审/cross review/多视角评审/让其他 agent 看看"时触发，通过 CLI 调用外部 code agent 独立评审同一方案，汇总共识与分歧。
---

# cross-review 执行规范

目标：调用不同架构的外部 code agent 独立评审同一方案，交叉对比发现盲区。

## 可用 Agent 列表

| Agent | CLI 命令 | 模型架构 | 关键参数 |
|-------|----------|---------|---------|
| Claude | `claude -p "{prompt}"` | Claude 系列 | `--output-format text` |
| Codex | `codex exec "{prompt}"` | GPT 系列 | `--full-auto` |
| Gemini | `gemini -p "{prompt}"` | Gemini 系列 | `--output-format json` |

## 一、准备 + 分发

1. **收集评审上下文**：构建完成评审所需的最小充分上下文——被评审对象本身、做出该决策的背景与约束、以及外部 agent 理解问题所必需的依赖信息。不足则主动从代码库/对话历史中补充，而非要求用户提供。

2. **推导关注点**：根据待评审内容的性质（新功能/修复/重构/安全/性能等），推导本次评审应重点关注的维度，作为用户指定关注点的补充。

3. **选择外部 agent**：
   - 识别自身所属模型架构，从列表中排除同架构 agent。
   - 对剩余 agent 执行 `command -v {cli}` 检测可用性。
   - 全部不可用 → 提示用户安装，终止。
   - 无法确定自身身份 → 列出可用 agent 由用户选择。

4. **调用外部 agent**（多个可用时并行，超时 120s，失败则跳过并标注）：
   ```bash
   {cli_command} "{prompt}" {关键参数}
   ```
   - 将评审上下文和关注点内联到 prompt 中，stdout 捕获结果。
   - 上下文超长时降级：写入 `$TMPDIR/cross-review-<YYYYMMDD-HHMMSS>/context.md`，prompt 中引用路径。
   - Gemini 推荐非交互命令模板：
   ```bash
   gemini -p "{prompt}" --output-format json
   ```

## 二、综合输出

在对话中直接输出：

1. **参与 agent**（含跳过原因）
2. **共识问题**（多个 agent 共同指出 → 高优先级）
3. **分歧点**（仅单个 agent 提出 → 需用户判断）
4. **行动建议**（按优先级排序）

> 仅一个外部 agent 可用时跳过交叉对比，直接输出该 agent 结果 + 自身判断。
