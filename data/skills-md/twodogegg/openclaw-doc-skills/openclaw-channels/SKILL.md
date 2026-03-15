---
name: openclaw-channels
description: "回答 OpenClaw 各消息渠道的接入、配置、路由和排障问题。用户提到 Slack、Telegram、Feishu、Discord、WhatsApp 等渠道对接或 channel routing 时使用。"
---

# OpenClaw Channels Docs Skill

按下面流程执行：

1. 识别目标渠道与问题阶段（新接入、联调、线上故障）。
2. 读取英文文档：`references/en/channels/*.md`。
3. 若信息不足，继续查阅渠道对应与 troubleshooting 条目。
4. 输出接入步骤时按“准备 -> 配置 -> 验证 -> 排障”顺序组织。

回答约束：

- 指出每个渠道的关键差异项（鉴权、事件模型、限制）。
- 给出最小可验证路径（先打通再扩展）。
- 出现故障时给出检查顺序与定位点。

参考目录：见 `references/sources.md`。
