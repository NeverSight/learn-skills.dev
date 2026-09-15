---
name: handoff-agent
description: Export current session to a unified markdown file for switching between agent tools (opencode/qoder), or import a previous handoff file to continue work. Use when the user wants to switch agents, run out of tokens, or says "handoff", "export session", "import session", "switch agent".
---

# Handoff Agent

在 opencode 和 qoder CLI 之间切换会话。导出当前会话为统一 markdown，另一个工具读取继续工作。

## 使用方式

- `/handoff-agent export` - 导出当前会话
- `/handoff-agent import` - 导入最近的 handoff 文件

## Export

运行脚本导出当前会话：

```bash
uv run <skill_dir>/scripts/handoff.py export
```

脚本自动完成：检测工具 → 查找会话 → 导出 → 转 markdown → 保存到 `.handoff/<标题>-latest.md`

## Import

运行脚本获取最新 handoff 文件路径：

```bash
uv run <skill_dir>/scripts/handoff.py import
```

读取输出的文件路径，用 Read 工具加载内容。这是之前 agent 会话的完整记录，包含用户意图、代码修改、tool call 历史。根据需要搜索、部分阅读或全量阅读，然后继续用户未完成的工作。

## 注意

- `.handoff/` 建议加入 `.gitignore`
- 同一会话多次导出会覆盖（文件名含 `latest`）
