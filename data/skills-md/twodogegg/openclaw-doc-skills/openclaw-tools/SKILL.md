---
name: openclaw-tools
description: "回答 OpenClaw tools 能力、调用方式、参数约束与使用边界问题。用户提到 browser、exec、web、skills、subagents、tool policy 或工具联动时使用。"
---

# OpenClaw Tools Docs Skill

按下面流程执行：

1. 识别具体工具与目标任务（如登录、抓取、执行命令、调用技能）。
2. 读取英文文档：`references/en/tools/*.md`。
3. 若信息不足，继续查阅同目录相关工具文档。
4. 输出时明确“能做什么/不能做什么/推荐做法”。

回答约束：

- 区分必须参数与可选参数。
- 有风险动作时加风险提示与替代方案。
- 多工具联动时按步骤给出执行顺序。

参考目录：见 `references/sources.md`。
