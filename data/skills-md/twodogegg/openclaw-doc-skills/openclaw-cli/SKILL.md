---
name: openclaw-cli
description: "回答 OpenClaw CLI 命令、参数、用法与排障问题。用户提到 openclaw 命令行、子命令、flags、配置命令、会话命令、acp 命令或需要 CLI 示例时使用。"
---

# OpenClaw CLI Docs Skill

按下面流程执行：

1. 识别用户问题对应的 CLI 主题（如 `acp`、`gateway`、`sessions`、`skills`）。
2. 读取英文文档：`references/en/cli/*.md`。
3. 若单篇文档信息不足，继续查阅同目录相关条目。
4. 输出时给出可直接执行的命令示例。

回答约束：

- 参数名、命令名保持原文大小写。
- 同时给出“最小可用命令”和“可选扩展参数”。
- 若命令行为依赖运行环境，明确说明前置条件。

参考目录：见 `references/sources.md`。
