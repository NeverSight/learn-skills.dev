---
name: openclaw-gateway
description: "回答 OpenClaw Gateway 的配置、认证、网络、会话、API 与排障问题。用户提到 gateway 配置、remote/local gateway、鉴权、WebSocket/HTTP API 或网关故障时使用。"
---

# OpenClaw Gateway Docs Skill

按下面流程执行：

1. 判断问题属于配置、认证、会话、网络模型、API、排障中的哪一类。
2. 读取英文文档：`references/en/gateway/*.md`。
3. 若单篇文档信息不足，继续查阅相关子主题（含 `security/`）。
4. 输出时给出分步配置或排障路径，并标明关键配置项。

回答约束：

- 涉及安全与鉴权时，优先给出最小暴露面方案。
- 需要命令时提供完整命令，避免伪代码式命令。
- 需要配置时给出最小示例块。

参考目录：见 `references/sources.md`。
