---
name: openclaw-concepts
description: "回答 OpenClaw 核心概念、术语定义、机制边界与设计原理问题。用户提到 session、memory、streaming、agent loop、model providers、multi-agent 或架构概念解释时使用。"
---

# OpenClaw Concepts Docs Skill

按下面流程执行：

1. 识别问题所属概念域（如 session、memory、streaming、architecture）。
2. 读取英文文档：`references/en/concepts/*.md`。
3. 若信息不足，继续查阅相邻概念条目做交叉解释。
4. 输出时先给定义，再给边界，再给实际场景示例。

回答约束：

- 明确区分相近概念，避免混用术语。
- 涉及行为差异时给出条件说明。
- 尽量关联到 CLI/Gateway 的实际落地点。

参考目录：见 `references/sources.md`。
