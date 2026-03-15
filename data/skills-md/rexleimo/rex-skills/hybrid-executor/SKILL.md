---
name: hybrid-executor
description: 当需要利用 Claude 的代码重构能力或 Gemini 的超长上下文分析时使用。
---

# 混合执行指令
当你判断当前任务更适合其他模型时，请通过 shell 运行以下指令：

1. **调用 Claude Code 执行复杂重构**:
`! claude -p "请重构以下代码并优化性能：$ARGUMENTS"`

2. **调用 Gemini CLI 分析大规模文档或日志**：
`! gemini -p "分析这些日志并寻找异常：$ARGUMENTS"`

3. **获取输出并整合**：
将上述命令的返回结果读取到当前会话中，并向用户提供最终建议。

(注：Codex 会自动解析 $ARGUMENTS 为你输入的参数。)
